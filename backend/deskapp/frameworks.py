"""Reference sheets for the frameworks Desk knows: what each one is, how it flows, what it reads.

Static content, checked against each project's repository. Run counts are joined at request time.
"""

from __future__ import annotations

from . import adapter
from .settings import engine_version

# Written explanations for TradingAgents agents; structure (stage, role, reads) comes from the adapter.
TA_AGENT_NOTES = {
    "market": ("Pulls price history and a set of technical indicators (moving averages, MACD, RSI, Bollinger Bands, ATR, VWMA), "
               "then writes a technical report with levels and a trend read.", "get_stock_data, get_indicators, get_verified_market_snapshot"),
    "sentiment": ("Reads recent social and news chatter and scores mood and its drivers. On past dates this feed is present-day data, "
                  "so Desk backtests leave it out.", "get_news (Yahoo), StockTwits, Reddit"),
    "news": ("Summarises company and macro news, FRED series and Polymarket odds into a news report. Yahoo keeps only recent "
             "articles, so past dates come back nearly empty.", "get_news, get_global_news, FRED, Polymarket"),
    "fundamentals": ("Reads the company profile and the three statements and writes a fundamentals report: growth, margins, cash, "
                     "balance sheet, valuation when available (withheld on past dates).", "get_fundamentals, get_balance_sheet, get_income_statement, get_cashflow"),
    "bull": ("Argues the long case from the four reports, replying to the bear's last point each round.", None),
    "bear": ("Argues the short case from the same reports, replying to the bull each round.", None),
    "research_manager": ("Judges the debate and writes the investment plan: a five-tier recommendation with rationale and actions. "
                         "Uses the deep model.", None),
    "trader": ("Turns the plan into a proposal: action, entry price, stop loss and position sizing, checked against the market report.", None),
    "aggressive": ("Risk debate, first voice: pushes for more exposure and higher reward.", None),
    "conservative": ("Risk debate: pushes for protection, smaller size and tighter stops.", None),
    "neutral": ("Risk debate: weighs both and looks for the balanced plan.", None),
    "portfolio_manager": ("Final decision: rating (Buy, Overweight, Hold, Underweight, Sell), executive summary, thesis, price target and "
                          "horizon. Uses the deep model.", None),
}


def _ta_agents() -> list[dict]:
    out = []
    for a in adapter.AGENTS:
        text, tools = TA_AGENT_NOTES.get(a["id"], ("", None))
        out.append({"id": a["id"], "name": a["name"], "stage": a["stage"], "role": a["role"], "reads": a["reads"],
                    "what": text, "tools": tools})
    return out


TRADINGAGENTS = {
    "id": "tradingagents",
    "name": "TradingAgents",
    "org": "Tauric Research",
    "version": None,  # filled from the clone at request time
    "status": "connected",
    "tagline": "A trading firm in twelve agents: analysts, a bull and bear debate, a trader, a risk debate and a portfolio manager.",
    "summary": (
        "TradingAgents runs one stock on one date through a fixed committee. Four analysts pull data in parallel and write reports; "
        "a bull and a bear argue over them; a research manager rules and writes a plan; a trader turns it into a proposal; three risk "
        "analysts debate the proposal; a portfolio manager gives the final five-tier rating. Every agent is an LLM call, quick or deep, "
        "and every analyst uses tools to fetch real data before writing."
    ),
    "links": [
        {"label": "GitHub", "url": "https://github.com/TauricResearch/TradingAgents"},
        {"label": "Paper (arXiv 2412.20138)", "url": "https://arxiv.org/abs/2412.20138"},
        {"label": "Docs", "url": "https://tauricresearch.github.io/TradingAgents/"},
    ],
    "facts": [
        {"label": "GitHub stars", "value": "105k", "note": "September 2026"},
        {"label": "Licence", "value": "Apache-2.0"},
        {"label": "Language", "value": "Python, LangGraph"},
        {"label": "LLM calls per run", "value": "11 to 19", "note": "depends on analysts and debate rounds"},
        {"label": "Cost per run on DeepSeek", "value": "$0.03 to $0.06"},
        {"label": "Time per run", "value": "4 to 9 min"},
    ],
    "flow": {
        "stages": [
            {"id": "data", "label": "Data", "mode": "tools", "nodes": [
                {"id": "prices", "label": "Prices, indicators", "kind": "data", "sub": "Yahoo"},
                {"id": "fund", "label": "Statements", "kind": "data", "sub": "Yahoo, Alpha Vantage"},
                {"id": "newsd", "label": "News and macro", "kind": "data", "sub": "Yahoo, FRED, Polymarket"},
                {"id": "social", "label": "Social", "kind": "data", "sub": "StockTwits, Reddit"},
            ]},
            {"id": "analysts", "label": "Analysts", "mode": "parallel", "nodes": [
                {"id": "market", "label": "Market", "kind": "quick"},
                {"id": "fundamentals", "label": "Fundamentals", "kind": "quick"},
                {"id": "news", "label": "News", "kind": "quick"},
                {"id": "sentiment", "label": "Sentiment", "kind": "quick"},
            ]},
            {"id": "research", "label": "Research debate", "mode": "rounds", "nodes": [
                {"id": "bull", "label": "Bull", "kind": "quick"},
                {"id": "bear", "label": "Bear", "kind": "quick"},
            ]},
            {"id": "rm", "label": "Ruling", "mode": "sequential", "nodes": [
                {"id": "research_manager", "label": "Research manager", "kind": "deep", "sub": "investment plan"},
            ]},
            {"id": "trading", "label": "Trading", "mode": "sequential", "nodes": [
                {"id": "trader", "label": "Trader", "kind": "quick", "sub": "entry, stop, sizing"},
            ]},
            {"id": "risk", "label": "Risk debate", "mode": "rounds", "nodes": [
                {"id": "aggressive", "label": "Aggressive", "kind": "quick"},
                {"id": "conservative", "label": "Conservative", "kind": "quick"},
                {"id": "neutral", "label": "Neutral", "kind": "quick"},
            ]},
            {"id": "pm", "label": "Decision", "mode": "sequential", "nodes": [
                {"id": "portfolio_manager", "label": "Portfolio manager", "kind": "deep", "sub": "five-tier rating"},
            ]},
        ],
        "edges": [
            ["prices", "market"], ["fund", "fundamentals"], ["newsd", "news"], ["social", "sentiment"],
            ["market", "bull"], ["fundamentals", "bull"], ["news", "bull"], ["sentiment", "bull"],
            ["market", "bear"], ["fundamentals", "bear"], ["news", "bear"], ["sentiment", "bear"],
            ["bull", "bear", "both"],
            ["bull", "research_manager"], ["bear", "research_manager"],
            ["research_manager", "trader"],
            ["trader", "aggressive"], ["trader", "conservative"], ["trader", "neutral"],
            ["aggressive", "conservative", "both"], ["conservative", "neutral", "both"],
            ["aggressive", "portfolio_manager"], ["conservative", "portfolio_manager"], ["neutral", "portfolio_manager"],
        ],
        "notes": [
            "Analysts run in parallel and independently; each one's tool messages are wiped after its report so the next stage sees only the report.",
            "Bull and bear alternate for the configured number of rounds (Desk default: 1). The same holds for the three risk voices.",
            "Quick model: analysts, debaters, trader. Deep model: research manager and portfolio manager.",
        ],
    },
    "agents": _ta_agents(),
    "data": [
        {"source": "Yahoo Finance (yfinance)", "used_for": "prices, indicators, statements, company profile, recent news", "point_in_time": "prices and statements filtered to the date; profile withheld on past dates; news only recent"},
        {"source": "Alpha Vantage", "used_for": "alternative vendor for the same data", "point_in_time": "same rules"},
        {"source": "FRED", "used_for": "macro series for the news analyst", "point_in_time": "yes, by date"},
        {"source": "StockTwits, Reddit, Polymarket", "used_for": "sentiment and event odds", "point_in_time": "no: present-day feeds"},
        {"source": "SEC EDGAR (Desk variant)", "used_for": "point-in-time valuation multiples on past dates", "point_in_time": "yes, by filing date"},
    ],
    "evidence": [
        {"claim": "Paper, Jan to Mar 2024: +26.6% on AAPL vs -5.2% buy and hold, Sharpe 8.2", "source": "arXiv 2412.20138",
         "note": "one quarter, three stocks, single run, no costs; authors call the Sharpe outside the expected range"},
        {"claim": "ICAIF 2026 reproducibility study: 15.8% ± 4.2% on GOOG vs 19.1% buy and hold", "source": "ACM 10.1145/3800973.3801029",
         "note": "several runs; a single good seed is called cherry-picking"},
        {"claim": "Desk pilot, 8 past dates on AAPL and NVDA: every decision Hold; trader levels -7% vs +33% buy and hold", "source": "Backtests page",
         "note": "8 decisions, memorisation possible; run on engine 0.4.0 (be952b8). The Hold default came from the manager wording of 1 Sep 2026 (a4acd8a); upstream fixed it on 14 Sep in 62d3479 after issue #1321 measured 86 to 89% Hold over 110 analyses"},
    ],
}

AI_HEDGE_FUND = {
    "id": "ai_hedge_fund",
    "name": "AI Hedge Fund",
    "org": "virattt",
    "version": None,
    "status": "planned",
    "tagline": "A fund of pluggable analysts: LLM agents in the voice of famous investors and quant models, blended into positions.",
    "summary": (
        "AI Hedge Fund is being rebuilt as a persistent fund rather than a one-shot script. A mandate names strategies, each strategy "
        "bundles analysts (alpha models) with a blending policy, an allocator splits capital across strategies, portfolio construction "
        "turns convictions into target positions, a risk model applies hard limits, and execution goes through a simulated or real "
        "broker. Every cycle is written to a ledger. Analysts come in two kinds that share one interface: LLM investor agents "
        "(Buffett, Munger, Graham, Lynch, Druckenmiller) and quant models (post-earnings drift). Each returns a conviction in [-1, +1] "
        "and a written thesis. Data comes from the Financial Datasets API, which needs its own key."
    ),
    "links": [
        {"label": "GitHub", "url": "https://github.com/virattt/ai-hedge-fund"},
        {"label": "Vision", "url": "https://github.com/virattt/ai-hedge-fund/blob/main/VISION.md"},
        {"label": "Roadmap", "url": "https://github.com/virattt/ai-hedge-fund/blob/main/ROADMAP.md"},
    ],
    "facts": [
        {"label": "GitHub stars", "value": "63k", "note": "September 2026"},
        {"label": "Licence", "value": "MIT"},
        {"label": "Language", "value": "Python"},
        {"label": "Paper", "value": "none", "note": "educational project"},
        {"label": "Data", "value": "Financial Datasets API", "note": "paid key required"},
        {"label": "LLM providers", "value": "Anthropic, OpenAI, DeepSeek, Google, xAI, Kimi"},
    ],
    "flow": {
        "stages": [
            {"id": "data", "label": "Data", "mode": "tools", "nodes": [
                {"id": "fd", "label": "Prices, fundamentals, earnings", "kind": "data", "sub": "Financial Datasets"},
            ]},
            {"id": "analysts", "label": "Analysts (alpha models)", "mode": "parallel", "nodes": [
                {"id": "buffett", "label": "Buffett", "kind": "quick", "sub": "LLM agent"},
                {"id": "munger", "label": "Munger", "kind": "quick", "sub": "LLM agent"},
                {"id": "graham", "label": "Graham", "kind": "quick", "sub": "LLM agent"},
                {"id": "lynch", "label": "Lynch", "kind": "quick", "sub": "LLM agent"},
                {"id": "druck", "label": "Druckenmiller", "kind": "quick", "sub": "LLM agent"},
                {"id": "pead", "label": "Earnings drift", "kind": "data", "sub": "quant model"},
            ]},
            {"id": "strategy", "label": "Strategy blend", "mode": "sequential", "nodes": [
                {"id": "blend", "label": "Conviction-weighted blend", "kind": "rule", "sub": "per strategy"},
            ]},
            {"id": "portfolio", "label": "Portfolio", "mode": "sequential", "nodes": [
                {"id": "alloc", "label": "Allocator", "kind": "rule", "sub": "capital per strategy"},
                {"id": "construct", "label": "Portfolio construction", "kind": "rule", "sub": "target positions"},
            ]},
            {"id": "risk", "label": "Risk", "mode": "sequential", "nodes": [
                {"id": "limits", "label": "Risk limits", "kind": "rule", "sub": "hard caps"},
            ]},
            {"id": "exec", "label": "Execution", "mode": "sequential", "nodes": [
                {"id": "broker", "label": "Broker", "kind": "rule", "sub": "simulated or live"},
                {"id": "ledger", "label": "Ledger", "kind": "rule", "sub": "positions, P&L, decisions"},
            ]},
        ],
        "edges": [
            ["fd", "buffett"], ["fd", "munger"], ["fd", "graham"], ["fd", "lynch"], ["fd", "druck"], ["fd", "pead"],
            ["buffett", "blend"], ["munger", "blend"], ["graham", "blend"], ["lynch", "blend"], ["druck", "blend"], ["pead", "blend"],
            ["blend", "alloc"], ["alloc", "construct"], ["construct", "limits"], ["limits", "broker"], ["broker", "ledger"],
        ],
        "notes": [
            "No debate: each analyst scores independently and a policy blends the convictions (deep-value strategy: Graham at double weight, plus Buffett and Munger).",
            "Strategies are YAML files; the same pipeline runs a backtest, paper trading or live trading by swapping the clock and the broker.",
            "Desk adapter not built yet: it would map each analyst to a lane and each cycle to a run.",
        ],
    },
    "agents": [
        {"id": "buffett", "name": "Warren Buffett agent", "stage": "analysts", "role": "quick", "reads": ["fundamentals", "prices"], "what": "Quality businesses at fair prices, in Buffett's public style. Stylised approximation, not the person.", "tools": None},
        {"id": "munger", "name": "Charlie Munger agent", "stage": "analysts", "role": "quick", "reads": ["fundamentals", "prices"], "what": "Mental-model checklist, avoiding stupidity over seeking brilliance.", "tools": None},
        {"id": "graham", "name": "Benjamin Graham agent", "stage": "analysts", "role": "quick", "reads": ["fundamentals", "prices"], "what": "Margin of safety, net current assets, earnings stability.", "tools": None},
        {"id": "lynch", "name": "Peter Lynch agent", "stage": "analysts", "role": "quick", "reads": ["fundamentals", "prices"], "what": "Growth at a reasonable price, PEG, understandable businesses.", "tools": None},
        {"id": "druck", "name": "Stanley Druckenmiller agent", "stage": "analysts", "role": "quick", "reads": ["fundamentals", "prices"], "what": "Macro and momentum, asymmetric bets, concentration when convinced.", "tools": None},
        {"id": "pead", "name": "Post-earnings drift model", "stage": "analysts", "role": "rule", "reads": ["earnings", "prices"], "what": "Quant model: rides the drift after earnings surprises. Pure maths, no LLM.", "tools": None},
        {"id": "blend", "name": "Strategy blend", "stage": "strategy", "role": "rule", "reads": ["convictions"], "what": "Weights analyst convictions into one view per strategy.", "tools": None},
        {"id": "construct", "name": "Portfolio construction", "stage": "portfolio", "role": "rule", "reads": ["blended views", "capital"], "what": "Turns views into target positions within the strategy's gross target.", "tools": None},
        {"id": "limits", "name": "Risk limits", "stage": "risk", "role": "rule", "reads": ["target positions"], "what": "Hard limits the analysts cannot override.", "tools": None},
    ],
    "data": [
        {"source": "Financial Datasets API", "used_for": "prices, fundamentals, earnings", "point_in_time": "to be checked in the adapter"},
    ],
    "evidence": [
        {"claim": "No published evaluation; the project states it is educational and does not trade", "source": "README", "note": ""},
    ],
}

FRAMEWORKS = [TRADINGAGENTS, AI_HEDGE_FUND]


def frameworks(run_counts: dict[str, int]) -> list[dict]:
    out = []
    for fw in FRAMEWORKS:
        item = {**fw, "runs": run_counts.get(fw["id"], 0)}
        if fw["id"] == "tradingagents":
            item["version"] = engine_version()
        out.append(item)
    return out
