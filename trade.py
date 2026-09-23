"""Glassbench trade: let the TradingAgents committee decide, then send its decision to the
Interactive Brokers PAPER account as one bracket order per stock.

  py -3 trade.py MSFT NVDA              run the 12 agents live on each stock (about 8 minutes), then trade
  py -3 trade.py MSFT NVDA --reuse      skip the wait: replay each stock's latest finished run, then trade
  py -3 trade.py MSFT --dry-run         everything except sending the orders

What becomes an order (long only, one decision, fixed size):
  Buy or Overweight     BUY  $10,000 worth, marketable limit, the trader's stop attached, the
                        portfolio manager's target attached when it gave one
  Hold                  nothing
  Underweight or Sell   SELL what is held; nothing when nothing is held

Safety: paper ports and DU accounts only, one order per stock (an existing working order stops it),
size capped, and a y/N confirmation. Broker notices go to data/trade.log, never to the screen.
Needs the Glassbench server (glassbench.ps1) and TWS logged into the paper account.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import re
import threading
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from ib_async import IB, LimitOrder, Stock, StopOrder
from rich.console import Console
from rich.padding import Padding
from rich.text import Text

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
STATUS = DATA / "trade_status.json"          # the recording script reads this to know where the run is
ORDERS = DATA / "orders.jsonl"
LOG = DATA / "trade.log"
API = "http://127.0.0.1:8765"
PAPER_PORTS = {7497, 4002}
NOTIONAL_CAP = 25_000

con = Console(highlight=False)
LABEL = 20
BLUE, RED, GOLD, DIM = "#6FA8DC", "#E06C66", "#E5B93C", "grey62"
RATING_STYLE = {"Buy": BLUE, "Overweight": BLUE, "Hold": GOLD, "Underweight": RED, "Sell": RED}
AGENT_NAMES = {
    "market": "Market analyst", "sentiment": "Sentiment analyst", "social": "Sentiment analyst", "news": "News analyst",
    "fundamentals": "Fundamentals", "bull": "Bull researcher", "bear": "Bear researcher",
    "research_manager": "Research manager", "trader": "Trader", "aggressive": "Risk aggressive",
    "conservative": "Risk conservative", "neutral": "Risk neutral", "portfolio_manager": "Portfolio manager",
}
ROLE_LINE = {"bull": "argues to buy", "bear": "argues against", "aggressive": "for more size",
             "conservative": "for less risk", "neutral": "weighs both"}
DECIDERS = {"research_manager", "trader", "portfolio_manager"}
print_lock = threading.Lock()


def rating_word(text) -> str:
    """The model sometimes writes a sentence after the word: keep the word."""
    m = re.match(r"\s*(Buy|Overweight|Hold|Underweight|Sell)", str(text or ""), re.I)
    return m.group(1).title() if m else str(text or "none")[:14]

logging.basicConfig(filename=str(LOG), level=logging.INFO, format="%(asctime)s %(message)s")
logging.getLogger("ib_async").setLevel(logging.CRITICAL)
log = logging.getLogger("trade")


# ---------------------------------------------------------------- screen
def stamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


def section(n: int, title: str, right: str = "") -> None:
    t = Text()
    t.append(f"\n {n}  ", style=GOLD)
    t.append(title.upper(), style="bold")
    if right:
        t.append("  " + right, style=DIM)
    con.print(t)


def row(label: str, value, style: str = "", note: str | list[str] = "") -> None:
    """note: one string rides on the value's line when it fits; a list always goes underneath, one line each."""
    t = Text()
    t.append(f"{label:<{LABEL}}", style=DIM)
    t.append(str(value), style=style or "bold")
    below = list(note) if isinstance(note, list) else []
    if isinstance(note, str) and note:
        if 4 + LABEL + len(str(value)) + 3 + len(note) <= con.width:
            t.append("   " + note, style=DIM)
        else:
            below = [note]
    con.print(Padding(t, (0, 0, 0, 4)), no_wrap=True, overflow="ellipsis")
    for line in below:
        con.print(Padding(Text(line, style=DIM), (0, 0, 0, 4 + LABEL)), no_wrap=True, overflow="ellipsis")


def say(text: str, style: str = "") -> None:
    con.print(Padding(Text(text, style=style), (0, 0, 0, 4)))


def event(ticker: str, who: str, text: str, style: str = "", who_w: int = 18) -> None:
    """One line, never wrapped: the terminal is a narrow column on camera (49 characters at 35% of the screen)."""
    t = Text("  ")
    t.append(stamp() + " ", style=DIM)
    t.append(f"{ticker:<5}", style="bold")
    t.append(f"{who:<{who_w}}", style=DIM)
    t.append(text, style=style)
    with print_lock:
        con.print(t, no_wrap=True, overflow="ellipsis")


def mask(account: str) -> str:
    return account[:3] + "•••" + account[-3:] if len(account) > 6 else account


def status(stage: str, **more) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps({"stage": stage, "at": time.time(), **more}), encoding="utf-8")


def stop(message: str) -> "SystemExit":
    """A clean sentence instead of a traceback: the terminal is on camera."""
    status("stopped", message=message)
    return SystemExit("\n    " + message + "\n")


# ---------------------------------------------------------------- Glassbench
def api(path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"}, method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


def events(run_id: str):
    """The run's event stream: everything stored so far, then live until the run ends."""
    req = urllib.request.Request(f"{API}/api/runs/{run_id}/events", headers={"Accept": "text/event-stream"})
    with urllib.request.urlopen(req, timeout=1800) as res:
        for raw in res:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            ev = json.loads(line[5:])
            yield ev
            if ev["type"] in ("run.finished", "run.failed", "run.cancelled"):
                return


def money(v) -> str:
    try:
        return f"{float(v):,.2f}"
    except (TypeError, ValueError):
        return "none"


def follow(ticker: str, run_id: str, out: dict, pace: float | None) -> None:
    """Print one short line per agent as the committee works. pace: seconds to replay a stored run in."""
    tools: dict[str, int] = {}
    seen: set[str] = set()
    stored = list(events(run_id)) if pace else None
    span = (stored[-1]["ts"] - stored[0]["ts"]) if stored else 0
    last_ts = stored[0]["ts"] if stored else 0
    for ev in (stored if stored is not None else events(run_id)):
        if stored is not None and span > 0:
            time.sleep(min(2.5, max(0.0, (ev["ts"] - last_ts) * pace / span)))
            last_ts = ev["ts"]
        kind, agent, p = ev["type"], ev.get("agent"), ev.get("payload") or {}
        who = AGENT_NAMES.get(agent or "", agent or "")
        if kind == "tool.called":
            tools[agent] = tools.get(agent, 0) + 1
        elif kind == "decision.structured":
            seen.add(agent)
            if agent == "research_manager":
                rec = rating_word(p.get("recommendation"))
                event(ticker, who, rec, RATING_STYLE.get(rec, ""))
            elif agent == "trader":
                event(ticker, who, f"{rating_word(p.get('action'))} at {money(p.get('entry_price'))}", "bold")
            elif agent == "portfolio_manager":
                rec = rating_word(p.get("rating"))
                event(ticker, who, rec, "bold " + RATING_STYLE.get(rec, "white"))
        elif kind == "report.updated" and agent not in seen and agent not in DECIDERS:
            seen.add(agent)
            if agent in ROLE_LINE:
                event(ticker, who, ROLE_LINE[agent], BLUE if agent == "bull" else RED if agent == "bear" else "")
            elif agent in AGENT_NAMES:
                n = tools.get(agent, 0)
                event(ticker, who, f"{n} tool calls" if n else "report in")
        elif kind == "run.finished":
            out[ticker] = {"run_id": run_id, "rating": p.get("rating"), "decision": p.get("decision") or {},
                           "cost": p.get("cost_usd"), "seconds": ev["ts"] - (stored[0]["ts"] if stored else ev["ts"])}
        elif kind in ("run.failed", "run.cancelled"):
            out[ticker] = {"run_id": run_id, "rating": None, "decision": {}, "error": (p.get("error") or kind)[:80]}
            event(ticker, "run", "did not finish", RED)


def latest_finished(ticker: str) -> dict | None:
    for run in api("/api/runs?limit=200")["runs"]:
        if run["ticker"] == ticker and run["status"] == "finished" and run.get("rating"):
            return run
    return None


# ---------------------------------------------------------------- Interactive Brokers
def connect() -> tuple[IB, str]:
    ib = IB()
    ib.errorEvent += lambda rid, code, msg, c: log.info("TWS %s %s", code, msg)       # to the log, never the screen
    for port in sorted(PAPER_PORTS, reverse=True):
        try:
            ib.connect("127.0.0.1", port, clientId=41, timeout=12)
            break
        except Exception as e:                                                          # noqa: BLE001
            log.info("connect %s failed: %s", port, e)
    if not ib.isConnected():
        raise stop("Cannot reach TWS on a paper port. Open TWS, log into the paper account, enable API socket clients.")
    account = (ib.managedAccounts() or [""])[0]
    if not account.startswith("DU"):
        ib.disconnect()
        raise stop("This is not a paper account (paper accounts start with DU). Nothing was sent.")
    return ib, account


def last_price(ib: IB, contract, fallback: float | None) -> float | None:
    try:
        bars = ib.reqHistoricalData(contract, "", "1 D", "1 min", "TRADES", useRTH=False, formatDate=2, timeout=12)
        if bars:
            return float(bars[-1].close)
    except Exception as e:                                                              # noqa: BLE001
        log.info("bars failed: %s", e)
    try:
        ib.reqMarketDataType(3)
        tick = ib.reqTickers(contract)[0]
        for v in (tick.marketPrice(), tick.last, tick.close):
            if v and not math.isnan(v):
                return float(v)
    except Exception as e:                                                              # noqa: BLE001
        log.info("ticker failed: %s", e)
    return fallback


def number(v) -> float | None:
    try:
        f = float(str(v).replace(",", "").replace("$", ""))
        return f if f > 0 else None
    except (TypeError, ValueError):
        return None


def plan_order(ticker: str, result: dict, price: float | None, held: float, working: int, notional: float) -> dict:
    """Turn one committee decision into at most one order. Returns {'text', 'note'} and, when there is one, the order fields."""
    rating = result.get("rating")
    trader, pm = result["decision"].get("trader") or {}, result["decision"].get("portfolio") or {}
    if rating is None:
        return {"text": "no order", "note": ["the run did not finish"]}
    if working:
        return {"text": "no order", "note": ["has working orders"]}
    if rating == "Hold":
        return {"text": "no order", "note": ["the committee says hold"]}
    if rating in ("Underweight", "Sell"):
        if held <= 0:
            return {"text": "no order", "note": [f"{rating.lower()}, none held", "long only"]}
        return {"text": f"SELL {int(held)}  MKT-LMT", "note": [f"{rating.lower()}", "close what is held"], "side": "SELL", "qty": int(held),
                "limit": round(price * 0.997, 2) if price else None}
    if not price:
        return {"text": "no order", "note": ["no broker price"]}
    qty = int(min(notional, NOTIONAL_CAP) // price)
    stop_px, target = number(trader.get("stop_loss")), number(pm.get("price_target"))
    if qty < 1:
        return {"text": "no order", "note": ["one share > order size"]}
    if not stop_px or not (price * 0.5 < stop_px < price * 0.995):
        return {"text": "no order", "note": ["no usable stop given"]}
    limit = round(price * 1.003, 2)
    target = target if target and target > price * 1.01 else None
    note = [f"stop    {stop_px:,.2f}"] + ([f"target  {target:,.2f}"] if target else [])
    return {"text": f"BUY {qty}  LMT {limit:,.2f}", "note": note, "side": "BUY", "qty": qty, "limit": limit, "stop": stop_px, "target": target}


def send(ib: IB, contract, ticker: str, plan: dict, run_id: str) -> dict:
    parent = LimitOrder(plan["side"], plan["qty"], plan["limit"])
    parent.orderId, parent.tif, parent.orderRef = ib.client.getReqId(), "DAY", f"glassbench:{run_id}"[:40]
    children = []
    if plan.get("target"):
        tp = LimitOrder("SELL", plan["qty"], plan["target"])
        tp.orderId, tp.parentId, tp.tif = ib.client.getReqId(), parent.orderId, "GTC"
        children.append(("target", tp))
    if plan.get("stop"):
        sl = StopOrder("SELL", plan["qty"], plan["stop"])
        sl.orderId, sl.parentId, sl.tif = ib.client.getReqId(), parent.orderId, "GTC"
        children.append(("stop", sl))
    orders = [("entry", parent)] + children
    for i, (_, o) in enumerate(orders):
        o.transmit = i == len(orders) - 1                # the last one releases the whole bracket
    trades = {name: ib.placeOrder(contract, o) for name, o in orders}
    event(ticker, "order", f"{plan['side']} {plan['qty']} sent, id {parent.orderId}", "bold", who_w=8)
    t0 = time.time()
    while time.time() - t0 < 25 and trades["entry"].orderStatus.status not in ("Filled", "Cancelled", "Inactive"):
        ib.waitOnUpdate(timeout=1)
    st = trades["entry"].orderStatus
    if st.status == "Filled":
        event(ticker, "fill", f"{int(st.filled)} at {st.avgFillPrice:,.2f}", BLUE if plan["side"] == "BUY" else RED, who_w=8)
    else:
        event(ticker, "order", f"working at {plan['limit']:,.2f}", GOLD, who_w=8)
    ib.sleep(1.0)
    for name, _ in children:
        px = plan["stop"] if name == "stop" else plan["target"]
        event(ticker, name, f"{px:,.2f} attached, GTC", RED if name == "stop" else BLUE, who_w=8)
    return {"ticker": ticker, "run_id": run_id, "at": datetime.now().isoformat(timespec="seconds"), **{k: plan.get(k) for k in ("side", "qty", "limit", "stop", "target")},
            "entry_id": parent.orderId, "status": st.status, "filled": st.filled, "avg_price": st.avgFillPrice}


def flatten(tickers: list[str]) -> int:
    """Between takes: cancel what is working and close what is held, in these stocks only."""
    ib, account = connect()
    for trade in ib.reqAllOpenOrders() or ib.openTrades():
        if trade.contract.symbol in tickers and trade.orderStatus.status not in ("Filled", "Cancelled", "Inactive"):
            ib.cancelOrder(trade.order)
    ib.sleep(2.0)
    for pos in ib.positions():
        if pos.contract.symbol in tickers and pos.position:
            contract = Stock(pos.contract.symbol, "SMART", "USD")
            ib.qualifyContracts(contract)
            px = last_price(ib, contract, pos.avgCost)
            side = "SELL" if pos.position > 0 else "BUY"
            order = LimitOrder(side, abs(int(pos.position)), round(px * (0.995 if side == "SELL" else 1.005), 2))
            order.tif = "DAY"
            ib.placeOrder(contract, order)
    ib.sleep(4.0)
    held = {p.contract.symbol: p.position for p in ib.positions() if p.contract.symbol in tickers and p.position}
    left = [t for t in ib.reqAllOpenOrders() or [] if t.contract.symbol in tickers and t.orderStatus.status not in ("Filled", "Cancelled", "Inactive")]
    say(f"{mask(account)}: held {held or 'nothing'}, working orders {len(left)}")
    ib.disconnect()
    return 0


# ---------------------------------------------------------------- the run
def main() -> int:
    ap = argparse.ArgumentParser(description="TradingAgents decisions to an Interactive Brokers paper bracket order.")
    ap.add_argument("tickers", nargs="+")
    ap.add_argument("--reuse", action="store_true", help="replay each stock's latest finished run")
    ap.add_argument("--pace", type=float, default=38, help="seconds a replayed run takes on screen")
    ap.add_argument("--notional", type=float, default=10_000)
    ap.add_argument("--dry-run", action="store_true", help="show the orders, send nothing")
    ap.add_argument("--start-delay", type=float, default=0)
    ap.add_argument("--flatten", action="store_true", help="cancel working orders and close positions in these stocks, then exit")
    a = ap.parse_args()
    tickers = [t.upper() for t in a.tickers][:4]
    time.sleep(a.start_delay)
    status("starting", tickers=tickers)

    try:
        meta = api("/api/meta")
    except Exception:                                                                    # noqa: BLE001
        raise stop("Glassbench is not running. Start it with glassbench.ps1, then run this again.")

    if a.flatten:
        return flatten(tickers)

    say("Paper account only. The committee's ratings are language model output, not investment advice.", DIM)
    section(1, "Account", "Interactive Brokers, paper")
    ib, account = connect()
    values = {v.tag: v.value for v in ib.accountSummary() if v.currency in ("USD", "")}
    positions = {p.contract.symbol: p.position for p in ib.positions()}
    open_trades = ib.reqAllOpenOrders() or ib.openTrades()
    working = {t: sum(1 for o in open_trades if o.contract.symbol == t and o.orderStatus.status not in ("Filled", "Cancelled", "Inactive")) for t in tickers}
    row("Account", mask(account), note="paper trading")
    row("Net liquidation", "$" + money(values.get("NetLiquidation")))
    row("Holding now", "  ".join(f"{t} {int(positions.get(t, 0))}" for t in tickers))
    row("Order size", "$" + money(a.notional), note="per stock, long only")

    engine = (meta.get("engine_version") or "").split("+")[0]
    section(2, "The committee", f"TradingAgents {engine}")
    status("committee")
    results: dict[str, dict] = {}
    if a.reuse:
        runs = {t: latest_finished(t) for t in tickers}
        for t, r in runs.items():
            if r is None:
                raise stop(f"No finished run for {t} yet. Run without --reuse first.")
            say(f"{t}  run of {r['trade_date']}, {r['id'][-4:]}", DIM)
        jobs = [(t, r["id"], a.pace) for t, r in runs.items()]
    else:
        ids = api("/api/runs", {"tickers": tickers, "analysts": meta["analysts"], "depth": 1})["run_ids"]
        say(f"{len(ids)} runs started, about 8 minutes", DIM)
        jobs = [(t, i, None) for t, i in zip(tickers, ids)]
    threads = [threading.Thread(target=follow, args=(t, i, results, p), daemon=True) for t, i, p in jobs]
    [th.start() for th in threads]
    [th.join() for th in threads]

    section(3, "Decisions")
    for t in tickers:
        r = results.get(t) or {"rating": None, "decision": {}}
        trader, pm = r["decision"].get("trader") or {}, r["decision"].get("portfolio") or {}
        rating = r.get("rating") or "none"
        con.print(Padding(Text(t, style="bold"), (1 if t != tickers[0] else 0, 0, 0, 4)))
        row("Final rating", rating, RATING_STYLE.get(rating, ""))
        row("Trader", rating_word(trader.get("action")))
        entry, stop_px, target = number(trader.get("entry_price")), number(trader.get("stop_loss")), number(pm.get("price_target"))
        row("Entry", money(entry))
        row("Stop loss", money(stop_px), RED if stop_px else "", note=f"{(stop_px / entry - 1):+.1%} from entry" if stop_px and entry else "")
        row("Price target", money(target), BLUE if target else "", note=f"{(target / entry - 1):+.1%} from entry" if target and entry else "")
        row("Horizon", pm.get("time_horizon") or "none")

    section(4, "Orders", "one bracket order per stock")
    contracts, plans = {}, {}
    for t in tickers:
        contracts[t] = Stock(t, "SMART", "USD")
        ib.qualifyContracts(contracts[t])
        r = results.get(t) or {"rating": None, "decision": {}}
        px = last_price(ib, contracts[t], number((r["decision"].get("trader") or {}).get("entry_price")))
        plans[t] = plan_order(t, r, px, float(positions.get(t, 0)), working.get(t, 0), a.notional)
        style = BLUE if plans[t].get("side") == "BUY" else RED if plans[t].get("side") == "SELL" else DIM
        row(t, plans[t]["text"], style, note=plans[t]["note"] + ([f"last    {px:,.2f}"] if px and plans[t].get("side") else []))
    to_send = [t for t in tickers if plans[t].get("side")]

    if not to_send:
        say("")
        say("Nothing to send. The committee gave no order today.", GOLD)
        status("done", sent=0)
        ib.disconnect()
        return 0
    if a.dry_run:
        say("")
        say("Dry run: nothing was sent.", GOLD)
        status("done", sent=0)
        ib.disconnect()
        return 0

    say("")
    status("confirm", orders=len(to_send))
    with print_lock:
        answer = con.input(Text(f"    Send {len(to_send)} order{'s' if len(to_send) > 1 else ''} to the PAPER account? [y/N] ", style=GOLD))
    if answer.strip().lower() != "y":
        say("Not sent.", DIM)
        status("done", sent=0)
        ib.disconnect()
        return 0

    section(5, "Execution", mask(account))
    status("sending")
    sent = []
    for t in to_send:
        record = send(ib, contracts[t], t, plans[t], results[t]["run_id"])
        sent.append(record)
        with ORDERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    section(6, "Result")
    ib.sleep(1.5)
    now = {p.contract.symbol: p.position for p in ib.positions()}
    row("Holding now", "  ".join(f"{t} {int(now.get(t, 0))}" for t in tickers))
    row("Orders sent", len(sent), note="each linked to its run")
    row("Open in Glassbench", "  ".join(r["run_id"][-9:] for r in sent), DIM)
    status("done", sent=len(sent))
    ib.disconnect()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        status("stopped", message="interrupted")
        raise SystemExit("\n    Stopped.\n")
