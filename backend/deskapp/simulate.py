"""Replay saved agent decisions into positions, fills, costs and returns. No LLM calls.

Rules (see BACKTEST_PLAN.md):
- A decision is made after the close of its date and trades at the next session's open.
- Rating targets: Buy 100% long, Overweight 50%, Hold keeps the position, Underweight and Sell flat.
- A failed or unrated run keeps the position and is flagged; it is never counted as a Hold.
- Costs: cost_bps on every traded dollar. Cash earns nothing. Long only, no leverage.
- "Trader levels" mode also trades the levels inside each decision: a Hold with an entry below the
  decision close is a limit buy on a pullback, above it a buy stop on confirmation (each adds 50%,
  capped at 100%); the stop exits the whole position. Orders live until the next decision fills.
  A position is never stopped out on the bar it was entered (daily bars cannot order those events).
"""

from __future__ import annotations

import threading

import os

import itertools
import math
import random
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, timedelta

import numpy as np

from .settings import DATA_DIR

PRICES_DIR = DATA_DIR / "prices"
RATING_TARGET = {"Buy": 1.0, "Overweight": 0.5, "Underweight": 0.0, "Sell": 0.0}
KNOWN_RATINGS = ("Buy", "Overweight", "Hold", "Underweight", "Sell")
HOLD_ADD = 0.5
PLACEBO_SIMS = 1000
MA_FAST, MA_SLOW = 50, 200


# --- prices -------------------------------------------------------------------------
@dataclass
class Bars:
    dates: list[str]
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray

    def index_on_or_before(self, day: str) -> int | None:
        idx = None
        for i, d in enumerate(self.dates):
            if d <= day:
                idx = i
            else:
                break
        return idx


_PRICE_LOCKS: dict[str, "threading.Lock"] = {}
_PRICE_LOCKS_GUARD = threading.Lock()


def _price_lock(path) -> "threading.Lock":
    with _PRICE_LOCKS_GUARD:
        return _PRICE_LOCKS.setdefault(str(path), threading.Lock())


def load_bars(ticker: str, start: str) -> Bars:
    """Daily OHLC from Yahoo, adjusted like the engine's own price tools, cached once per day."""
    import pandas as pd
    import yfinance as yf

    PRICES_DIR.mkdir(parents=True, exist_ok=True)
    safe = "".join(c for c in ticker if c.isalnum() or c in "-_.^=")
    today = date.today().isoformat()
    path = PRICES_DIR / f"{safe}_{start}_{today}.csv"
    # One lock per cache file: the results page and the variant comparison ask for the same prices at the same
    # moment, and two writers on one CSV interleave their rows. The write goes to a temp file and is renamed.
    with _price_lock(path):
        df = None
        if path.exists():
            try:
                df = pd.read_csv(path, index_col=0)
            except (ValueError, pd.errors.ParserError):
                path.unlink(missing_ok=True)          # a damaged cache is refetched, never trusted
        if df is None:
            tomorrow = (date.today() + timedelta(days=1)).isoformat()
            df = yf.Ticker(ticker).history(start=start, end=tomorrow, auto_adjust=True)[["Open", "High", "Low", "Close"]]
            if df.empty:
                raise ValueError(f"No price data for {ticker} from {start}")
            df.index = [d.date().isoformat() for d in df.index]
            tmp = path.with_suffix(f".{os.getpid()}.{threading.get_ident()}.tmp")
            df.to_csv(tmp)
            os.replace(tmp, path)
    df = df.dropna()
    return Bars(list(df.index.astype(str)), df["Open"].to_numpy(float), df["High"].to_numpy(float),
                df["Low"].to_numpy(float), df["Close"].to_numpy(float))


# --- decisions ------------------------------------------------------------------------
@dataclass
class Decision:
    date: str
    rating: str | None  # None: failed, cancelled or unparseable
    run_id: str | None = None
    entry: float | None = None
    stop: float | None = None
    status: str = "finished"


@dataclass
class Book:
    cash: float = 100.0
    shares: float = 0.0
    trades: list = field(default_factory=list)

    def equity(self, price: float) -> float:
        return self.cash + self.shares * price

    def weight(self, price: float) -> float:
        eq = self.equity(price)
        return self.shares * price / eq if eq > 0 else 0.0

    def rebalance(self, target: float, price: float, cost_bps: float, day: str, reason: str, run_id: str | None) -> bool:
        price = float(price)
        before = float(self.weight(price))
        if abs(target - before) < 1e-9:
            return False
        eq = self.equity(price)
        new_shares = target * eq / price
        traded = abs(new_shares - self.shares) * price
        cost = traded * cost_bps / 10_000
        self.cash -= (new_shares - self.shares) * price + cost
        self.shares = new_shares
        self.trades.append({"date": day, "side": "buy" if target > before else "sell", "price": round(price, 4),
                            "weight_before": round(before, 4), "weight_after": round(self.weight(price), 4),
                            "cost": round(cost, 6), "reason": reason, "run_id": run_id})
        return True


def simulate(bars: Bars, decisions: list[Decision], cost_bps: float = 10, mode: str = "rating",
             hold_rule: str = "keep", start_weight: float = 0.0, trigger: str = "close") -> dict:
    """Daily equity (starting at 100 on the first decision's close) and trades for one ticker.

    trigger="close" (default): a confirmation entry fires when a daily close reaches its level and a
    stop fires when a daily close falls to it; both fill at the next open, matching how the trader's
    plans are written ("a daily close above", "a decisive close below"). Pullback entries stay limit
    orders filled during the day. trigger="touch" fires both on intraday highs and lows instead.
    """
    decisions = sorted(decisions, key=lambda d: d.date)
    start = bars.index_on_or_before(decisions[0].date)
    if start is None:
        raise ValueError("First decision is before the price history")
    fills: dict[int, tuple[Decision, int]] = {}
    for d in decisions:
        idx = bars.index_on_or_before(d.date)
        if idx is not None and idx + 1 < len(bars.dates):
            fills[idx + 1] = (d, idx)  # a later decision on the same bar replaces an earlier one

    book = Book()
    if start_weight:
        book.rebalance(start_weight, bars.close[start], cost_bps, bars.dates[start], "start invested", None)
    equity, weights = [book.equity(bars.close[start])], [book.weight(bars.close[start])]
    stop: dict | None = None  # {"level", "run_id"}
    order: dict | None = None  # {"level", "kind", "run_id"}
    pending_exit: dict | None = None  # stop confirmed on a close, sells at the next open
    pending_entry: dict | None = None  # confirmation seen on a close, buys at the next open

    for t in range(start + 1, len(bars.dates)):
        o, h, lo, c, day = bars.open[t], bars.high[t], bars.low[t], bars.close[t], bars.dates[t]
        held_since_yesterday = book.shares > 0
        entered_today = False

        if t in fills:
            # A new decision replaces every order and trigger left by the previous one.
            pending_exit = pending_entry = None
            d, d_idx = fills[t]
            stop, order = None, None
            if d.rating in RATING_TARGET:
                target = RATING_TARGET[d.rating]
            elif d.rating == "Hold":
                target = HOLD_ADD if hold_rule == "half" else None
            else:
                target = None  # failed or unrated: keep the position
            if target is not None:
                before = book.shares
                book.rebalance(target, o, cost_bps, day, f"rating {d.rating}", d.run_id)
                entered_today = book.shares > before + 1e-12
            if mode == "levels" and d.rating in ("Buy", "Overweight", "Hold"):
                ref = bars.close[d_idx]
                if d.stop and 0.5 * ref < d.stop < ref:
                    stop = {"level": d.stop, "run_id": d.run_id}
                if d.rating == "Hold" and d.entry and 0.7 * ref < d.entry < 1.3 * ref and abs(d.entry - ref) > 1e-9:
                    order = {"level": d.entry, "kind": "limit" if d.entry < ref else "stop", "run_id": d.run_id}
        else:
            if pending_exit and book.shares > 0:
                book.rebalance(0.0, o, cost_bps, day, pending_exit["reason"], pending_exit["run_id"])
            if pending_entry:
                target = min(book.weight(o) + HOLD_ADD, 1.0)
                if book.rebalance(target, o, cost_bps, day, pending_entry["reason"], pending_entry["run_id"]):
                    entered_today = True
            pending_exit = pending_entry = None

        stopped = False
        if mode == "levels" and trigger == "touch" and stop is not None and book.shares > 0 and held_since_yesterday and not entered_today:
            level = stop["level"]
            if o <= level:
                stopped = book.rebalance(0.0, o, cost_bps, day, f"stop {level:.2f} gapped, filled at open", stop["run_id"])
            elif lo <= level:
                stopped = book.rebalance(0.0, level, cost_bps, day, f"stop {level:.2f}", stop["run_id"])

        if mode == "levels" and order and not stopped:
            level, kind = order["level"], order["kind"]
            if kind == "limit":
                price = o if o <= level else (level if lo <= level else None)
                if price is not None:
                    target = min(book.weight(price) + HOLD_ADD, 1.0)
                    if book.rebalance(target, price, cost_bps, day, f"pullback entry {level:.2f}", order["run_id"]):
                        entered_today = True
                    order = None
            elif trigger == "touch":
                price = o if o >= level else (level if h >= level else None)
                if price is not None:
                    target = min(book.weight(price) + HOLD_ADD, 1.0)
                    if book.rebalance(target, price, cost_bps, day, f"confirmation entry {level:.2f}", order["run_id"]):
                        entered_today = True
                    order = None
            elif c >= level:
                pending_entry = {"reason": f"confirmation entry: close {c:.2f} above {level:.2f}", "run_id": order["run_id"]}
                order = None

        if mode == "levels" and trigger == "close" and stop is not None and book.shares > 0 and c <= stop["level"]:
            pending_exit = {"reason": f"stop: close {c:.2f} at or below {stop['level']:.2f}", "run_id": stop["run_id"]}
            pending_entry = None
            order = None  # a broken stop cancels the plan's remaining entries

        equity.append(book.equity(c))
        weights.append(book.weight(c))

    return {"equity": equity, "weights": weights, "trades": book.trades}


# --- metrics ------------------------------------------------------------------------
def metrics(equity: list[float], weights: list[float], trades: list[dict]) -> dict:
    eq = np.asarray(equity, float)
    rets = eq[1:] / eq[:-1] - 1 if len(eq) > 1 else np.array([])
    n = len(rets)
    std = float(np.std(rets, ddof=1)) if n > 1 else 0.0
    peak = np.maximum.accumulate(eq)
    return {
        "total_return": float(eq[-1] / eq[0] - 1),
        "annual_return": float((eq[-1] / eq[0]) ** (252 / n) - 1) if n else None,
        "volatility": std * math.sqrt(252) if n > 1 else None,
        "sharpe": float(np.mean(rets) / std * math.sqrt(252)) if std > 0 else None,
        "max_drawdown": float(np.min(eq / peak - 1)),
        "time_in_market": float(np.mean(weights[1:])) if n else 0.0,
        "trades": len(trades),
        "costs": float(sum(tr["cost"] for tr in trades) / eq[0]),
        "days": n,
    }


def drawdown(equity: list[float]) -> list[float]:
    eq = np.asarray(equity, float)
    return [round(float(x), 6) for x in eq / np.maximum.accumulate(eq) - 1]


# --- benchmarks ---------------------------------------------------------------------
def ma_decisions(bars: Bars, days: list[str]) -> list[Decision] | None:
    out = []
    for day in days:
        idx = bars.index_on_or_before(day)
        if idx is None or idx + 1 < MA_SLOW:
            return None
        fast = bars.close[idx + 1 - MA_FAST: idx + 1].mean()
        slow = bars.close[idx + 1 - MA_SLOW: idx + 1].mean()
        out.append(Decision(day, "Buy" if fast > slow else "Sell"))
    return out


def placebo(bars: Bars, decisions: list[Decision], cost_bps: float, seed: int = 7) -> dict:
    """Same ratings, shuffled across the same dates. Every distinct ordering when there are few, else 1,000 draws."""
    ratings = [d.rating for d in decisions]
    counts = Counter(ratings)
    distinct = math.factorial(len(ratings)) // math.prod(math.factorial(v) for v in counts.values())
    if distinct <= PLACEBO_SIMS:
        orders = sorted(set(itertools.permutations(ratings)), key=lambda p: [str(x) for x in p])
    else:
        rng = random.Random(seed)
        orders = []
        for _ in range(PLACEBO_SIMS):
            shuffled = ratings[:]
            rng.shuffle(shuffled)
            orders.append(tuple(shuffled))
    curves = np.array([
        simulate(bars, [Decision(d.date, r) for d, r in zip(decisions, order)], cost_bps)["equity"] for order in orders
    ])
    return {"curves": curves, "sims": len(orders), "exhaustive": distinct <= PLACEBO_SIMS}


def band(curves: np.ndarray) -> dict:
    return {k: [round(float(x), 4) for x in np.percentile(curves, q, axis=0)] for k, q in (("p5", 5), ("p50", 50), ("p95", 95))}


# --- one backtest ----------------------------------------------------------------------
STRATEGY_LABELS = {
    "agents_levels": "Agents · trader levels",
    "agents_rating": "Agents · rating only",
    "buy_hold": "Buy and hold",
    "ma_cross": "50/200-day MA rule",
}
SENSITIVITY_LABELS = {
    "agents_rating": "Hold keeps position, start flat (plan)",
    "hold_half": "Hold means 50% long",
    "start_invested": "Start fully invested",
    "levels_touch": "Trader levels on intraday touches, not closes",
}


def _round_list(values) -> list[float]:
    return [round(float(v), 4) for v in values]


def exposure_periods(bars: Bars, start: int, result: dict) -> list[dict]:
    """Split the book into periods of constant exposure, each opened by the trades that caused it.

    For one stock, a trade's return equals the stock's return over the same days, so the useful
    comparison is what the stock did while the book was out of it: gains missed or losses avoided.
    Trades on the same day share one number, which the charts use as their label.
    """
    groups: list[dict] = []
    for trade in result["trades"]:
        if groups and groups[-1]["date"] == trade["date"]:
            groups[-1]["trades"].append(trade)
        else:
            groups.append({"date": trade["date"], "trades": [trade]})

    periods: list[dict] = []
    cur = {"start": bars.dates[start], "price": float(bars.close[start]), "weight": float(result["weights"][0]), "opened_by": None}

    def close(end_date: str, end_price: float, ongoing: bool) -> None:
        stock = end_price / cur["price"] - 1
        w = cur["weight"]
        verdict = "held" if w > 1e-6 else ("missed gain" if stock > 0 else "avoided loss" if stock < 0 else "flat")
        periods.append({"start": cur["start"], "end": end_date, "start_price": round(cur["price"], 4), "end_price": round(end_price, 4),
                        "weight": round(w, 4), "stock_return": stock, "book_return": w * stock, "verdict": verdict,
                        "ongoing": ongoing, "opened_by": cur["opened_by"]})

    for n, g in enumerate(groups, start=1):
        if g["date"] != cur["start"]:  # a trade on the start date (start invested) opens no empty period
            close(g["date"], g["trades"][0]["price"], False)
        last = g["trades"][-1]
        for trade in g["trades"]:
            trade["n"] = n
        cur = {"start": g["date"], "price": last["price"], "weight": last["weight_after"],
               "opened_by": {"n": n, "side": last["side"], "reasons": [t["reason"] for t in g["trades"]], "run_id": last["run_id"],
                             "price": last["price"], "weight_before": g["trades"][0]["weight_before"], "weight_after": last["weight_after"]}}
    close(bars.dates[-1], float(bars.close[-1]), True)
    return periods


def run_ticker(ticker: str, decisions: list[Decision], cost_bps: float, bars: Bars | None = None) -> dict:
    decisions = sorted(decisions, key=lambda d: d.date)
    if bars is None:
        first = date.fromisoformat(decisions[0].date)
        bars = load_bars(ticker, (first - timedelta(days=420)).isoformat())
    start = bars.index_on_or_before(decisions[0].date)
    dates = bars.dates[start:]
    notes = []
    last_idx = bars.index_on_or_before(decisions[-1].date)
    if last_idx is not None and last_idx + 1 >= len(bars.dates):
        notes.append(f"Decision of {decisions[-1].date} trades at the next open, which has not happened yet.")
    unrated = [d for d in decisions if d.rating not in KNOWN_RATINGS]
    if unrated:
        notes.append(f"{len(unrated)} decision(s) without a rating kept the prior position: " + ", ".join(d.date for d in unrated))

    strategies = []

    def add(key: str, result: dict):
        periods = exposure_periods(bars, start, result)
        strategies.append({"key": key, "label": STRATEGY_LABELS[key], "equity": _round_list(result["equity"]),
                           "weights": _round_list(result["weights"]), "drawdown": drawdown(result["equity"]),
                           "trades": result["trades"], "periods": periods,
                           "metrics": metrics(result["equity"], result["weights"], result["trades"])})

    add("agents_levels", simulate(bars, decisions, cost_bps, mode="levels"))
    rating_result = simulate(bars, decisions, cost_bps)
    add("agents_rating", rating_result)
    add("buy_hold", simulate(bars, [Decision(decisions[0].date, "Buy")], cost_bps))
    ma = ma_decisions(bars, [d.date for d in decisions])
    if ma:
        add("ma_cross", simulate(bars, ma, cost_bps))

    sensitivity = [
        {"key": "agents_rating", "label": SENSITIVITY_LABELS["agents_rating"], "metrics": metrics(rating_result["equity"], rating_result["weights"], rating_result["trades"])},
    ]
    for key, kwargs in (("hold_half", {"hold_rule": "half"}), ("start_invested", {"start_weight": 1.0}), ("levels_touch", {"mode": "levels", "trigger": "touch"})):
        res = simulate(bars, decisions, cost_bps, **kwargs)
        sensitivity.append({"key": key, "label": SENSITIVITY_LABELS[key], "metrics": metrics(res["equity"], res["weights"], res["trades"])})

    pb = placebo(bars, decisions, cost_bps)
    finals = pb["curves"][:, -1]
    agent_final = rating_result["equity"][-1]
    placebo_out = {**band(pb["curves"]), "sims": pb["sims"], "exhaustive": pb["exhaustive"],
                   "agent_percentile": float(np.mean(finals <= agent_final + 1e-9))}

    decision_rows = []
    for i, d in enumerate(decisions):
        idx = bars.index_on_or_before(d.date)
        nxt = bars.index_on_or_before(decisions[i + 1].date) if i + 1 < len(decisions) else len(bars.dates) - 1
        fwd = float(bars.close[nxt] / bars.close[idx] - 1) if idx is not None and nxt is not None and nxt > idx else None
        decision_rows.append({"date": d.date, "rating": d.rating, "status": d.status, "run_id": d.run_id, "entry": d.entry,
                              "stop": d.stop, "close": round(float(bars.close[idx]), 4) if idx is not None else None,
                              "forward_return": fwd})

    by_rating = []
    for rating in KNOWN_RATINGS:
        rows = [r for r in decision_rows if r["rating"] == rating and r["forward_return"] is not None]
        if not rows:
            continue
        fwd = [r["forward_return"] for r in rows]
        hit = None
        if rating in ("Buy", "Overweight"):
            hit = sum(f > 0 for f in fwd) / len(fwd)
        elif rating in ("Underweight", "Sell"):
            hit = sum(f < 0 for f in fwd) / len(fwd)
        by_rating.append({"rating": rating, "n": len(rows), "mean_forward_return": float(np.mean(fwd)),
                          "share_up": sum(f > 0 for f in fwd) / len(fwd), "hit_rate": hit})

    return {"ticker": ticker, "dates": dates, "close": _round_list(bars.close[start:]), "decisions": decision_rows,
            "strategies": strategies, "placebo": placebo_out, "placebo_curves": pb["curves"], "sensitivity": sensitivity,
            "by_rating": by_rating, "notes": notes}


def combine(tickers: list[dict]) -> dict:
    """Equal-weight portfolio of the per-ticker books, each starting at 100 on the common first date."""
    common = sorted(set.intersection(*(set(t["dates"]) for t in tickers)))
    keys = [s["key"] for s in tickers[0]["strategies"] if all(any(x["key"] == s["key"] for x in t["strategies"]) for t in tickers)]
    strategies = []
    for key in keys:
        curves, weights, trades = [], [], []
        for t in tickers:
            s = next(x for x in t["strategies"] if x["key"] == key)
            pos = {d: i for i, d in enumerate(t["dates"])}
            eq = np.array([s["equity"][pos[d]] for d in common])
            curves.append(eq / eq[0] * 100)
            weights.append(np.array([s["weights"][pos[d]] for d in common]))
            trades.extend(s["trades"])
        eq = np.mean(curves, axis=0)
        w = np.mean(weights, axis=0)
        strategies.append({"key": key, "label": STRATEGY_LABELS[key], "equity": _round_list(eq), "weights": _round_list(w),
                           "drawdown": drawdown(list(eq)), "metrics": {**metrics(list(eq), list(w), trades), "trades": len(trades)}})
    rng = np.random.default_rng(7)
    stacked = []
    for t in tickers:
        pos = [t["dates"].index(d) for d in common]
        curves = t["placebo_curves"][:, pos]
        curves = curves / curves[:, :1] * 100
        pick = rng.choice(curves.shape[0], size=PLACEBO_SIMS, replace=curves.shape[0] < PLACEBO_SIMS)
        stacked.append(curves[pick])
    combined_curves = np.mean(stacked, axis=0)
    rating = next((s for s in strategies if s["key"] == "agents_rating"), None)
    placebo_out = {**band(combined_curves), "sims": int(combined_curves.shape[0]), "exhaustive": False,
                   "agent_percentile": float(np.mean(combined_curves[:, -1] <= rating["equity"][-1] + 1e-9)) if rating else None}
    return {"ticker": "Combined", "dates": common, "strategies": strategies, "placebo": placebo_out}
