"""Paired comparison of two backtests that share their cells and differ in one variant.

Usage (from desk/backend):  python -m deskapp.paired <control backtest id> <treatment backtest id>

Built for the valuation test (EDGAR statements, with and without valuation as of the run date),
and reusable for any matched pair. It reads what the agents wrote, never ratings alone:

- how often a report says valuation is missing, withheld or unavailable
- how many valuation multiples are cited with a number, and how many of those match the figure
  that was true on the run date (within 5%), by agent
- whether valuation reaches the research manager and the portfolio manager
- ratings, cost, tokens and time per arm

No LLM calls. The as-of-date truth comes from the engine's own sec_edgar vendor (SEC + Yahoo, cached).
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict

from .settings import DATA_DIR

VALUATION_WORDS = r"(?:valuation|market cap(?:itali[sz]ation)?|multiples?|P/E|price[- ]to[- ]earnings|enterprise value)"
ABSENT_WORDS = (r"(?:withheld|unavailable|not available|not provided|no (?:current |reliable )?data|cannot be (?:assessed|computed|"
                r"determined|calculated)|can't be (?:assessed|computed)|(?:is|are|was|were|data|remains?) missing|missing (?:data|"
                r"valuation|market|multiples?|from)|absent|absence of|lacks?|lacking)")
# "without" and a bare "missing" were dropped after reading the hits: "a 9.7x sales multiple without regulatory risk" and
# "missing the re-rating" use a multiple, they do not report one as absent.
MISSING = re.compile(rf"{VALUATION_WORDS}[^.\n|]{{0,90}}{ABSENT_WORDS}|{ABSENT_WORDS}[^.\n|]{{0,70}}{VALUATION_WORDS}", re.I)

# label -> (row in the vendor report, pattern that finds "label ... 12.3x" in prose)
MULTIPLES = {
    "P/E": ("PE Ratio (TTM)", r"(?:P/E|PE ratio|price[- ]to[- ]earnings)"),
    "P/S": ("Price to Sales (TTM)", r"(?:P/S|price[- ]to[- ]sales)"),
    "P/B": ("Price to Book", r"(?:P/B|price[- ]to[- ]book)"),
    "EV/EBITDA": ("EV to EBITDA (TTM)", r"(?:EV\s?/\s?EBITDA|EV to EBITDA)"),
    "EV/Sales": ("EV to Sales (TTM)", r"(?:EV\s?/\s?(?:Sales|Revenue)|EV to Sales)"),
}
# Agents write both "P/E of 35.9x" and "35.9x TTM earnings, 28.1x EV/EBITDA", so a multiple is any "N.Nx" token
# with valuation wording close by, and it is checked against the whole set of true multiples, not one label.
TOKEN = re.compile(r"(?<![\d.$])(\d{1,4}(?:\.\d+)?)\s?[x×](?![\w])")
CONTEXT = re.compile(r"P/E|\bPE\b|earnings|P/S|\bsales\b|revenue|P/B|\bbook\b|EBITDA|\bEV\b|multiple|valuation|free cash flow|FCF", re.I)
# Same "N.Nx" shape, different meaning: liquidity ratios, growth factors, coverage.
NOT_A_MULTIPLE = re.compile(r"current ratio|quick ratio|liquidity|coverage|leverage|turnover|grew|growth|rose|increase|routinely|FY\d\d\b|cover(?:ed|s|age)?\b|net debt|liabilit|OCF/NI|net income|forward|annuali[sz]ed", re.I)
STAGES = {"fundamentals": "Fundamentals analyst", "bull": "Bull", "bear": "Bear", "research_manager": "Research manager",
          "trader": "Trader", "aggressive": "Risk: aggressive", "conservative": "Risk: conservative", "neutral": "Risk: neutral",
          "portfolio_manager": "Portfolio manager"}


def truth_for(ticker: str, day: str) -> dict[str, float]:
    """The multiples that were true on the run date, from the engine's vendor."""
    try:
        from tradingagents.dataflows.vendors import sec_edgar  # 0.5.1 moved vendors into a subpackage
    except ImportError:
        from tradingagents.dataflows import sec_edgar

    from .keys import load_keys

    load_keys()
    out = {}
    try:
        report = sec_edgar.get_fundamentals(ticker, day)
    except Exception:
        return out
    for label, (row, _) in MULTIPLES.items():
        line = next((l for l in report.splitlines() if l.startswith(row)), "")
        found = re.search(r": (\d+(?:\.\d+)?)x", line)
        if found:
            out[label] = float(found.group(1))
    return out


def cited(text: str) -> list[float]:
    found = []
    for m in TOKEN.finditer(text):
        near = text[max(0, m.start() - 45): m.end() + 45]
        if CONTEXT.search(near) and not NOT_A_MULTIPLE.search(text[max(0, m.start() - 40): m.end() + 30]):
            found.append(float(m.group(1)))
    return found


def load(db: sqlite3.Connection, backtest_id: str) -> dict[tuple[str, str], dict]:
    runs = {}
    for r in db.execute("select * from runs where backtest_id=? and status='finished'", (backtest_id,)):
        texts = {}
        for e in db.execute("select agent, payload from events where run_id=? and type='report.updated' order by seq", (r["id"],)):
            texts[e["agent"]] = json.loads(e["payload"]).get("text", "")
        runs[(r["ticker"], r["trade_date"])] = {"run": dict(r), "texts": texts}
    return runs


def measure(cell: dict, truth: dict[str, float]) -> dict:
    by_agent = {}
    for agent, text in cell["texts"].items():
        if agent not in STAGES:
            continue
        quotes = cited(text)
        matched = [q for q in quotes if any(abs(q - t) <= 0.05 * t for t in truth.values())]
        by_agent[agent] = {"missing": len(MISSING.findall(text)), "cited": len(quotes), "matched": len(matched)}
    return by_agent


def compare(control_id: str, treatment_id: str) -> str:
    db = sqlite3.connect(str(DATA_DIR / "desk.db"))
    db.row_factory = sqlite3.Row
    arms = {"control": load(db, control_id), "treatment": load(db, treatment_id)}
    names = {arm: db.execute("select name from backtests where id=?", (bt,)).fetchone()["name"]
             for arm, bt in (("control", control_id), ("treatment", treatment_id))}
    cells = sorted(set(arms["control"]) & set(arms["treatment"]))
    truths = {cell: truth_for(*cell) for cell in cells}

    totals = {arm: defaultdict(Counter) for arm in arms}
    per_cell = []
    for cell in cells:
        row = {"cell": cell}
        for arm in arms:
            m = measure(arms[arm][cell], truths[cell])
            for agent, counts in m.items():
                totals[arm][agent].update(counts)
            run = arms[arm][cell]["run"]
            row[arm] = {"rating": run["rating"], "cost": run["cost_usd"], "tokens": run["tokens_in"] + run["tokens_out"],
                        "seconds": (run["finished_at"] or 0) - (run["started_at"] or 0),
                        "missing": sum(c["missing"] for c in m.values()), "cited": sum(c["cited"] for c in m.values()),
                        "matched": sum(c["matched"] for c in m.values()),
                        "pm_cites": m.get("portfolio_manager", {}).get("cited", 0) + m.get("research_manager", {}).get("cited", 0)}
        per_cell.append(row)

    n = len(cells)
    out = [f"# Paired comparison, {n} matched cells", "",
           f"- Control: `{control_id}` {names['control']}", f"- Treatment: `{treatment_id}` {names['treatment']}", ""]
    if not n:
        return "\n".join(out + ["No matched finished cells yet."])

    def total(arm, key):
        return sum(r[arm][key] for r in per_cell)

    out += ["## Per arm", "", "| Measure | Control | Treatment |", "|---|---:|---:|"]
    for label, key, fmt in (("Statements that valuation is missing", "missing", "{:.0f}"), ("Multiples cited with a number", "cited", "{:.0f}"),
                            ("of which match the run date's figure (5%)", "matched", "{:.0f}"),
                            ("Multiples cited by research or portfolio manager", "pm_cites", "{:.0f}"),
                            ("LLM cost, USD", "cost", "{:.3f}"), ("Tokens", "tokens", "{:,.0f}"), ("Run time, minutes", "seconds", None)):
        a, b = total("control", key), total("treatment", key)
        if fmt is None:
            out.append(f"| {label} (mean per run) | {a / n / 60:.1f} | {b / n / 60:.1f} |")
        else:
            out.append(f"| {label} | {fmt.format(a)} | {fmt.format(b)} |")
    for arm in arms:
        reached = sum(1 for r in per_cell if r[arm]["pm_cites"] > 0)
        out.append(f"| Runs where a manager cites a multiple ({arm}) | {reached if arm == 'control' else ''} | {reached if arm == 'treatment' else ''} |")

    # Sign test on the paired difference in missing-valuation statements: exact, two sided.
    from math import comb

    wins = sum(1 for r in per_cell if r["treatment"]["missing"] < r["control"]["missing"])
    losses = sum(1 for r in per_cell if r["treatment"]["missing"] > r["control"]["missing"])
    k, m = min(wins, losses), wins + losses
    p = min(1.0, 2 * sum(comb(m, i) for i in range(k + 1)) / 2 ** m) if m else 1.0
    out += ["", f"Fewer missing-valuation statements with valuation served in {wins} of {n} cells, more in {losses}, equal in {n - wins - losses}; "
                f"exact sign test p = {p:.4f}."]

    out += ["", "## Ratings", "", "| Rating | Control | Treatment |", "|---|---:|---:|"]
    mix = {arm: Counter(r[arm]["rating"] for r in per_cell) for arm in arms}
    for rating in ("Buy", "Overweight", "Hold", "Underweight", "Sell"):
        out.append(f"| {rating} | {mix['control'][rating]} | {mix['treatment'][rating]} |")
    changed = [r for r in per_cell if r["control"]["rating"] != r["treatment"]["rating"]]
    out.append(f"\n{len(changed)} of {n} cells changed rating. Ratings are reported for completeness; one run per cell cannot separate "
               "the effect of the data from run-to-run noise.")

    out += ["", "## By agent", "", "| Agent | Missing C | Missing T | Cited C | Cited T | Matched C | Matched T |", "|---|---:|---:|---:|---:|---:|---:|"]
    for agent, label in STAGES.items():
        c, t = totals["control"][agent], totals["treatment"][agent]
        out.append(f"| {label} | {c['missing']} | {t['missing']} | {c['cited']} | {t['cited']} | {c['matched']} | {t['matched']} |")

    out += ["", "## By cell", "", "| Ticker | Date | True P/E | Rating C | Rating T | Missing C | Missing T | Cited C | Cited T | Matched C | Matched T |",
            "|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|"]
    for r in per_cell:
        pe = truths[r["cell"]].get("P/E")
        c, t = r["control"], r["treatment"]
        out.append(f"| {r['cell'][0]} | {r['cell'][1]} | {f'{pe:.1f}x' if pe else 'n/m'} | {c['rating']} | {t['rating']} | {c['missing']} | {t['missing']} | "
                   f"{c['cited']} | {t['cited']} | {c['matched']} | {t['matched']} |")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.stdout.reconfigure(encoding="utf-8")
    print(compare(sys.argv[1], sys.argv[2]))
