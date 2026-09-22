"""Point-in-time valuation from SEC EDGAR filings, for runs dated in the past.

Yahoo's company profile (market cap, P/E, EV/EBITDA) only exists as today's snapshot, so the
engine withholds it on past dates. This module rebuilds those figures as they could have been
known on the decision date: every XBRL fact in EDGAR carries the date it was filed, and only
facts filed before the decision date are used. Price is that day's close from Yahoo, with
later stock splits undone so it matches the share count reported at the time.

Free public API; SEC asks for a User-Agent with a contact email (SEC_EDGAR_EMAIL).
"""

from __future__ import annotations

import json
import os
import time
from datetime import date, timedelta
from pathlib import Path

from .settings import DATA_DIR

EDGAR_DIR = DATA_DIR / "edgar"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"

REVENUE = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax"]
NET_INCOME = ["NetIncomeLoss", "ProfitLoss"]
OPERATING_INCOME = ["OperatingIncomeLoss"]
DA = ["DepreciationDepletionAndAmortization", "DepreciationAmortizationAndAccretionNet", "DepreciationAndAmortization", "Depreciation"]
OCF = ["NetCashProvidedByUsedInOperatingActivities", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"]
CAPEX = ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"]
CASH = ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]
SECURITIES = ["MarketableSecuritiesCurrent", "AvailableForSaleSecuritiesDebtSecuritiesCurrent", "ShortTermInvestments"]
DEBT_PARTS = [["LongTermDebtNoncurrent"], ["LongTermDebtCurrent"], ["CommercialPaper"], ["ShortTermBorrowings"]]
DEBT_TOTAL = ["LongTermDebt", "DebtInstrumentCarryingAmount"]
EQUITY = ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"]


class EdgarError(Exception):
    pass


def _headers() -> dict:
    email = os.environ.get("SEC_EDGAR_EMAIL", "").strip()
    if not email:
        raise EdgarError("SEC_EDGAR_EMAIL is not set in .env")
    return {"User-Agent": f"Desk research tool {email}", "Accept-Encoding": "gzip, deflate"}


def _get_json(url: str, cache: Path, max_age_s: float) -> dict:
    import requests

    if cache.exists() and time.time() - cache.stat().st_mtime < max_age_s:
        return json.loads(cache.read_text(encoding="utf-8"))
    res = requests.get(url, headers=_headers(), timeout=30)
    if res.status_code != 200:
        raise EdgarError(f"SEC EDGAR returned {res.status_code} for {url}")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(res.text, encoding="utf-8")
    time.sleep(0.15)  # stay far below SEC's 10 requests per second
    return res.json()


def cik_for(ticker: str) -> int:
    data = _get_json(TICKERS_URL, EDGAR_DIR / "company_tickers.json", 7 * 86400)
    symbol = ticker.upper().replace(".", "-")
    for row in data.values():
        if row["ticker"].upper() == symbol:
            return int(row["cik_str"])
    raise EdgarError(f"{ticker} is not in SEC's ticker list (EDGAR covers US filers only)")


def company_facts(ticker: str) -> dict:
    cik = cik_for(ticker)
    return _get_json(FACTS_URL.format(cik=cik), EDGAR_DIR / f"facts_{cik}.json", 86400)


# --- point-in-time fact selection -------------------------------------------------------
def _facts(data: dict, concepts: list[str], as_of: str, taxonomy: str = "us-gaap", unit: str = "USD") -> tuple[str, list[dict]] | tuple[None, list]:
    """Facts filed strictly before as_of, from the concept with the most recent period.

    Companies switch tags over the years (NVIDIA moved revenue between tags), so the first concept
    that has any data can be years stale. Within a concept, a restated period replaces the original
    only if the restatement was also filed before as_of.
    """
    best: tuple[str, list[dict]] | None = None
    best_end = ""
    for concept in concepts:
        node = data.get("facts", {}).get(taxonomy, {}).get(concept)
        if not node:
            continue
        rows = [r for r in node.get("units", {}).get(unit, []) if r.get("filed", "9999") < as_of]
        if not rows:
            continue
        latest: dict[tuple, dict] = {}
        for r in rows:
            key = (r.get("start"), r["end"])
            if key not in latest or r["filed"] > latest[key]["filed"]:
                latest[key] = r
        end = max(r["end"] for r in latest.values())
        if end > best_end:
            best, best_end = (concept, list(latest.values())), end
    return best if best else (None, [])


def _days(r: dict) -> int:
    return (date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days


def _instant(data: dict, concepts: list[str], as_of: str, taxonomy: str = "us-gaap", unit: str = "USD") -> dict | None:
    concept, rows = _facts(data, concepts, as_of, taxonomy, unit)
    rows = [r for r in rows if not r.get("start")]
    if not rows:
        return None
    best = max(rows, key=lambda r: (r["end"], r["filed"]))
    return {**best, "concept": concept}


def _ttm(data: dict, concepts: list[str], as_of: str) -> dict | None:
    """Trailing twelve months as known on as_of: the fiscal year itself, or last FY + year-to-date - prior year-to-date."""
    concept, rows = _facts(data, concepts, as_of)
    flows = [r for r in rows if r.get("start")]
    if not flows:
        return None
    end = max(r["end"] for r in flows)
    at_end = [r for r in flows if r["end"] == end]
    annual = [r for r in at_end if 350 <= _days(r) <= 380]
    if annual:
        r = max(annual, key=lambda x: x["filed"])
        return {"value": r["val"], "end": end, "method": "fiscal year", "filed": r["filed"], "form": r.get("form"), "concept": concept}
    ytd = max(at_end, key=_days)
    length = _days(ytd)
    if length > 350:
        return None
    end_d = date.fromisoformat(end)
    prior = [r for r in flows if abs((date.fromisoformat(r["end"]) - (end_d - timedelta(days=364))).days) <= 10 and abs(_days(r) - length) <= 10]
    start_d = date.fromisoformat(ytd["start"])
    fiscal = [r for r in flows if 350 <= _days(r) <= 380 and abs((date.fromisoformat(r["end"]) - (start_d - timedelta(days=1))).days) <= 10]
    if not prior or not fiscal:
        return None
    p = max(prior, key=lambda x: x["filed"])
    f = max(fiscal, key=lambda x: x["filed"])
    return {"value": f["val"] + ytd["val"] - p["val"], "end": end, "method": f"FY to {f['end']} + {round(length / 30.4)}-month YTD - prior YTD",
            "filed": ytd["filed"], "form": ytd.get("form"), "concept": concept}


def _shares(data: dict, as_of: str) -> dict | None:
    cover = _instant(data, ["EntityCommonStockSharesOutstanding"], as_of, taxonomy="dei", unit="shares")
    if cover:
        return cover
    return _instant(data, ["CommonStockSharesOutstanding"], as_of, unit="shares")


def _price_on(ticker: str, day: str) -> tuple[float, str]:
    """Close on or before day, converted back to the share basis of that date (later splits undone)."""
    import yfinance as yf

    t = yf.Ticker(ticker)
    start = (date.fromisoformat(day) - timedelta(days=10)).isoformat()
    end = (date.fromisoformat(day) + timedelta(days=1)).isoformat()
    hist = t.history(start=start, end=end, auto_adjust=False)
    if hist.empty:
        raise EdgarError(f"No Yahoo price for {ticker} near {day}")
    close = float(hist["Close"].iloc[-1])
    traded = hist.index[-1].date().isoformat()
    factor = 1.0
    for when, ratio in t.splits.items():
        if when.date().isoformat() > traded and ratio:
            factor *= float(ratio)
    return close * factor, traded


# --- the snapshot -----------------------------------------------------------------------
def valuation(ticker: str, as_of: str) -> dict:
    data = company_facts(ticker)
    price, traded = _price_on(ticker, as_of)
    shares = _shares(data, as_of)
    if not shares:
        raise EdgarError(f"No share count filed for {ticker} before {as_of}")
    mcap = price * shares["val"]

    revenue = _ttm(data, REVENUE, as_of)
    net_income = _ttm(data, NET_INCOME, as_of)
    op_income = _ttm(data, OPERATING_INCOME, as_of)
    da = _ttm(data, DA, as_of)
    ocf = _ttm(data, OCF, as_of)
    capex = _ttm(data, CAPEX, as_of)
    cash = _instant(data, CASH, as_of)
    securities = _instant(data, SECURITIES, as_of)
    equity = _instant(data, EQUITY, as_of)
    total_debt = _instant(data, DEBT_TOTAL, as_of)
    debt_value, debt_note = None, ""
    parts = [_instant(data, c, as_of) for c in DEBT_PARTS]
    parts = [p for p in parts if p and cash and p["end"] == cash["end"]]
    if parts:
        debt_value = sum(p["val"] for p in parts)
        debt_note = " + ".join(p["concept"] for p in parts)
    elif total_debt:
        debt_value, debt_note = total_debt["val"], total_debt["concept"]

    liquid = (cash["val"] if cash else 0) + (securities["val"] if securities and cash and securities["end"] == cash["end"] else 0)
    ev = mcap + (debt_value or 0) - liquid if cash else None
    ebitda = op_income["value"] + da["value"] if op_income and da and op_income["end"] == da["end"] else None
    fcf = ocf["value"] - capex["value"] if ocf and capex and ocf["end"] == capex["end"] else None

    def ratio(a, b):
        return a / b if a is not None and b not in (None, 0) and b > 0 else None

    return {
        "ticker": ticker.upper(), "as_of": as_of, "price": price, "price_date": traded, "shares": shares, "market_cap": mcap,
        "enterprise_value": ev, "debt": debt_value, "debt_note": debt_note, "cash_and_securities": liquid if cash else None,
        "ttm": {"revenue": revenue, "net_income": net_income, "operating_income": op_income, "d_and_a": da, "operating_cash_flow": ocf, "capex": capex},
        "equity": equity, "ebitda": ebitda, "free_cash_flow": fcf,
        "multiples": {
            "pe": ratio(mcap, net_income["value"] if net_income else None),
            "ps": ratio(mcap, revenue["value"] if revenue else None),
            "pb": ratio(mcap, equity["val"] if equity else None),
            "ev_ebitda": ratio(ev, ebitda),
            "ev_sales": ratio(ev, revenue["value"] if revenue else None),
            "fcf_yield": (fcf / mcap) if fcf is not None and mcap else None,
        },
    }


def _b(v: float | None) -> str:
    if v is None:
        return "n/a"
    if abs(v) >= 1e12:
        return f"${v / 1e12:,.3f}T"
    return f"${v / 1e9:,.2f}B"


def _x(v: float | None) -> str:
    return "n/a" if v is None else f"{v:.1f}x"


def valuation_text(ticker: str, as_of: str) -> str:
    """Markdown block appended to the fundamentals tool output on past-dated runs."""
    try:
        v = valuation(ticker, as_of)
    except Exception as exc:  # never break a run over optional data
        return f"## Point-in-time valuation (SEC EDGAR)\n\nNot available for {ticker} as of {as_of}: {exc}"
    t, m = v["ttm"], v["multiples"]

    def src(item, label):
        if not item:
            return f"- {label}: not reported in filings available before {as_of}"
        value = item.get("value", item.get("val"))
        extra = f", {item['method']}" if item.get("method") else ""
        return f"- {label}: {_b(value)} (period to {item['end']}{extra}; {item.get('form') or 'filing'} filed {item['filed']})"

    fcf_yield = "n/a" if m["fcf_yield"] is None else f"{m['fcf_yield'] * 100:.2f}%"
    lines = [
        f"## Point-in-time valuation for {v['ticker']} as of {as_of} (SEC EDGAR)",
        "",
        f"Built only from SEC filings filed before {as_of} and the closing price on {v['price_date']}. "
        "Forward estimates are not included: no point-in-time source for them is available.",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| Price (close {v['price_date']}) | ${v['price']:,.2f} |",
        f"| Shares outstanding | {v['shares']['val'] / 1e9:,.3f}B (as of {v['shares']['end']}, filed {v['shares']['filed']}) |",
        f"| Market cap | {_b(v['market_cap'])} |",
        f"| Enterprise value | {_b(v['enterprise_value'])} |",
        f"| P/E (TTM) | {_x(m['pe'])} |",
        f"| P/S (TTM) | {_x(m['ps'])} |",
        f"| P/B | {_x(m['pb'])} |",
        f"| EV/EBITDA (TTM) | {_x(m['ev_ebitda'])} |",
        f"| EV/Sales (TTM) | {_x(m['ev_sales'])} |",
        f"| Free cash flow yield (TTM) | {fcf_yield} |",
        "",
        "Inputs:",
        src(t["revenue"], "Revenue TTM"),
        src(t["net_income"], "Net income TTM"),
        src(t["operating_income"], "Operating income TTM"),
        src(t["d_and_a"], "Depreciation and amortisation TTM"),
        src(t["operating_cash_flow"], "Operating cash flow TTM"),
        src(t["capex"], "Capital expenditure TTM"),
        f"- Debt: {_b(v['debt'])} ({v['debt_note'] or 'not reported'})",
        f"- Cash and current marketable securities: {_b(v['cash_and_securities'])}",
    ]
    return "\n".join(lines)
