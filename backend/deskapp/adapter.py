"""Everything Desk knows about TradingAgents v0.4 internals lives here.

Node names, state keys, stages and what each agent reads. If an upstream
release renames any of these, this file (and its test) is the one place to fix.
"""

from __future__ import annotations

import re

STAGES = [
    {"id": "analysts", "label": "Analysts"},
    {"id": "research", "label": "Research"},
    {"id": "trading", "label": "Trading"},
    {"id": "risk", "label": "Risk"},
    {"id": "portfolio", "label": "Portfolio"},
]

REPORTS = ["market_report", "sentiment_report", "news_report", "fundamentals_report"]
RISK_INPUTS = REPORTS + ["trader_investment_plan", "risk debate so far"]

AGENTS = [
    {"id": "market", "label": "Market", "name": "Market analyst", "stage": "analysts", "role": "quick",
     "analyst_key": "market", "node": "Market Analyst", "tool_node": "tools_market", "clear_node": "Msg Clear Market",
     "text": ["market_report"], "reads": ["Price history (yfinance)", "Technical indicators", "Verified market snapshot"]},
    # Since 0.5.1 the sentiment analyst fetches its sources before calling the model, so it has no tool node.
    {"id": "sentiment", "label": "Sentiment", "name": "Sentiment analyst", "stage": "analysts", "role": "quick",
     "analyst_key": "social", "node": "Sentiment Analyst", "tool_node": None, "clear_node": "Msg Clear Sentiment",
     "text": ["sentiment_report"], "reads": ["Yahoo news, last 7 days", "StockTwits, last 30 messages", "Reddit: wallstreetbets, stocks, investing",
                                             "Jev screening of the posts when a TypeSafe key is set"]},
    {"id": "news", "label": "News", "name": "News analyst", "stage": "analysts", "role": "quick",
     "analyst_key": "news", "node": "News Analyst", "tool_node": "tools_news", "clear_node": "Msg Clear News",
     "text": ["news_report"], "reads": ["Ticker and global news", "FRED macro series", "Polymarket probabilities"]},
    {"id": "fundamentals", "label": "Fundamentals", "name": "Fundamentals analyst", "stage": "analysts", "role": "quick",
     "analyst_key": "fundamentals", "node": "Fundamentals Analyst", "tool_node": "tools_fundamentals",
     "clear_node": "Msg Clear Fundamentals", "text": ["fundamentals_report"],
     "reads": ["Company profile and ratios", "Balance sheet", "Income statement", "Cash flow"]},
    {"id": "bull", "label": "Bull", "name": "Bull researcher", "stage": "research", "role": "quick",
     "node": "Bull Researcher", "text": ["investment_debate_state", "bull_history"],
     "reads": REPORTS + ["debate history", "bear's last argument"]},
    {"id": "bear", "label": "Bear", "name": "Bear researcher", "stage": "research", "role": "quick",
     "node": "Bear Researcher", "text": ["investment_debate_state", "bear_history"],
     "reads": REPORTS + ["debate history", "bull's last argument"]},
    {"id": "research_manager", "label": "Research Manager", "name": "Research manager", "stage": "research", "role": "deep",
     "node": "Research Manager", "text": ["investment_plan"], "reads": ["bull_history", "bear_history"]},
    {"id": "trader", "label": "Trader", "name": "Trader", "stage": "trading", "role": "quick",
     "node": "Trader", "text": ["trader_investment_plan"], "reads": ["investment_plan", "market_report"]},
    {"id": "aggressive", "label": "Aggressive", "name": "Aggressive analyst", "stage": "risk", "role": "quick",
     "node": "Aggressive Analyst", "text": ["risk_debate_state", "aggressive_history"], "reads": RISK_INPUTS},
    {"id": "conservative", "label": "Conservative", "name": "Conservative analyst", "stage": "risk", "role": "quick",
     "node": "Conservative Analyst", "text": ["risk_debate_state", "conservative_history"], "reads": RISK_INPUTS},
    {"id": "neutral", "label": "Neutral", "name": "Neutral analyst", "stage": "risk", "role": "quick",
     "node": "Neutral Analyst", "text": ["risk_debate_state", "neutral_history"], "reads": RISK_INPUTS},
    {"id": "portfolio_manager", "label": "Portfolio Manager", "name": "Portfolio manager", "stage": "portfolio", "role": "deep",
     "node": "Portfolio Manager", "text": ["final_trade_decision"],
     "reads": ["investment_plan", "trader_investment_plan", "risk debate", "past lessons (memory log)"]},
]

AGENT_BY_ID = {a["id"]: a for a in AGENTS}

# node name -> (agent id, node kind)
NODE_MAP: dict[str, tuple[str, str]] = {}
for _a in AGENTS:
    NODE_MAP[_a["node"]] = (_a["id"], "agent")
    if _a.get("tool_node"):
        NODE_MAP[_a["tool_node"]] = (_a["id"], "tools")
    if _a.get("clear_node"):
        NODE_MAP[_a["clear_node"]] = (_a["id"], "clear")


def agents_for(analyst_keys: list[str]) -> list[dict]:
    chosen = set(analyst_keys)
    return [a for a in AGENTS if a["stage"] != "analysts" or a.get("analyst_key") in chosen]


def agent_text(agent_id: str, state: dict) -> str | None:
    path = AGENT_BY_ID[agent_id]["text"]
    value: object = state
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value if isinstance(value, str) and value.strip() else None


# ---------------------------------------------------------------------------
# Data quality flags found in tool output or engine logs
FLAG_RULES = [
    (re.compile(r"NO_DATA_AVAILABLE"), "No data returned"),
    (re.compile(r"DATA_UNAVAILABLE"), "Source unavailable"),
    (re.compile(r"No news found"), "Empty news feed"),
    (re.compile(r"withheld", re.I), "Present-day values withheld for this date"),
    (re.compile(r"FRED_API_KEY environment variable is not set"), "FRED key missing"),
]
LOG_FLAG_RULES = [
    (re.compile(r"\b429\b"), "Rate limited"),
    (re.compile(r"not configured", re.I), "Data source not configured"),
]


def flag_for(text: str, rules=FLAG_RULES) -> str | None:
    for pattern, label in rules:
        if pattern.search(text or ""):
            return label
    return None


# ---------------------------------------------------------------------------
# Decisions: parse the markdown the engine renders from its structured outputs
def _field(text: str, label: str) -> str | None:
    m = re.search(rf"\*\*{re.escape(label)}\*\*:\s*(.+?)(?=\n\s*\n\*\*|\nFINAL TRANSACTION|\Z)", text or "", re.S)
    return m.group(1).strip() if m else None


def _number(value: str | None) -> float | None:
    if not value:
        return None
    m = re.search(r"-?\d[\d,]*\.?\d*", value)
    return float(m.group(0).replace(",", "")) if m else None


def parse_research_plan(text: str) -> dict:
    return {
        "recommendation": _field(text, "Recommendation"),
        "rationale": _field(text, "Rationale"),
        "strategic_actions": _field(text, "Strategic Actions"),
    }


def parse_trader_plan(text: str) -> dict:
    return {
        "action": _field(text, "Action"),
        "reasoning": _field(text, "Reasoning"),
        "entry_price": _number(_field(text, "Entry Price")),
        "stop_loss": _number(_field(text, "Stop Loss")),
        "position_sizing": _field(text, "Position Sizing"),
    }


def parse_pm_decision(text: str) -> dict:
    try:
        from tradingagents.agents.rating import extract_rating  # 0.5.1
    except ImportError:
        from tradingagents.agents.utils.rating import extract_rating

    return {
        "rating": extract_rating(text or "") or "REVIEW",
        "executive_summary": _field(text, "Executive Summary"),
        "investment_thesis": _field(text, "Investment Thesis"),
        "price_target": _number(_field(text, "Price Target")),
        "time_horizon": _field(text, "Time Horizon"),
    }


def parse_decision(state: dict) -> dict:
    return {
        "research": parse_research_plan(state.get("investment_plan") or ""),
        "trader": parse_trader_plan(state.get("trader_investment_plan") or ""),
        "portfolio": parse_pm_decision(state.get("final_trade_decision") or "") if state.get("final_trade_decision") else None,
    }


def state_snapshot(state: dict) -> dict:
    """The JSON-safe subset of final state that Desk archives per run."""
    inv = state.get("investment_debate_state") or {}
    risk = state.get("risk_debate_state") or {}
    return {
        "company_of_interest": state.get("company_of_interest"),
        "trade_date": state.get("trade_date"),
        "instrument_context": state.get("instrument_context"),
        "past_context": state.get("past_context"),
        **{k: state.get(k) for k in REPORTS},
        "investment_debate_state": {k: inv.get(k) for k in ("bull_history", "bear_history", "history", "judge_decision", "count")},
        "investment_plan": state.get("investment_plan"),
        "trader_investment_plan": state.get("trader_investment_plan"),
        "risk_debate_state": {k: risk.get(k) for k in ("aggressive_history", "conservative_history", "neutral_history", "history", "judge_decision", "count")},
        "final_trade_decision": state.get("final_trade_decision"),
    }
