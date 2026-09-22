"""Paths, model choices, pricing and the engine config Desk hands to TradingAgents."""

from __future__ import annotations

import copy
from datetime import date
from pathlib import Path

import os

BACKEND_DIR = Path(__file__).resolve().parents[1]
DESK_DIR = BACKEND_DIR.parent          # the repository root
REPO_DIR = DESK_DIR


def _first_existing(*candidates: Path) -> Path:
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


# The TradingAgents engine: GLASSBENCH_ENGINE_DIR, else ./TradingAgents inside the repo, else a sibling clone.
ENGINE_DIR = Path(os.environ["GLASSBENCH_ENGINE_DIR"]).resolve() if os.environ.get("GLASSBENCH_ENGINE_DIR") else _first_existing(REPO_DIR / "TradingAgents", REPO_DIR.parent / "TradingAgents")
WORKSPACE_DIR = ENGINE_DIR.parent

DATA_DIR = DESK_DIR / "data"
RUNS_DIR = DATA_DIR / "runs"
BACKTESTS_DIR = DATA_DIR / "backtests"
DB_PATH = DATA_DIR / "desk.db"
FRONTEND_DIST = DESK_DIR / "frontend" / "dist"

# Keys: GLASSBENCH_ENV, else .env in the repository root. Only the allowlist below is read; values never reach the browser.
KEYS_FILE = Path(os.environ["GLASSBENCH_ENV"]).resolve() if os.environ.get("GLASSBENCH_ENV") else REPO_DIR / ".env"
# LLM providers the engine supports (tradingagents.llm_clients), the env var that holds each key (None = no key)
# and suggested model ids. Any model id can be typed in the New run dialog; these are only the suggestions.
PROVIDERS = {
    "deepseek":   {"label": "DeepSeek",       "key": "DEEPSEEK_API_KEY",   "quick": ["deepseek-v4-flash"], "deep": ["deepseek-v4-pro"]},
    "openai":     {"label": "OpenAI",         "key": "OPENAI_API_KEY",     "quick": [], "deep": []},
    "anthropic":  {"label": "Anthropic",      "key": "ANTHROPIC_API_KEY",  "quick": [], "deep": []},
    "google":     {"label": "Google",         "key": "GOOGLE_API_KEY",     "quick": [], "deep": []},
    "xai":        {"label": "xAI",            "key": "XAI_API_KEY",        "quick": [], "deep": []},
    "qwen":       {"label": "Qwen",           "key": "DASHSCOPE_API_KEY",  "quick": [], "deep": []},
    "glm":        {"label": "GLM",            "key": "ZHIPU_API_KEY",      "quick": [], "deep": []},
    "minimax":    {"label": "MiniMax",        "key": "MINIMAX_API_KEY",    "quick": [], "deep": []},
    "mistral":    {"label": "Mistral",        "key": "MISTRAL_API_KEY",    "quick": [], "deep": []},
    "kimi":       {"label": "Kimi",           "key": "MOONSHOT_API_KEY",   "quick": [], "deep": []},
    "groq":       {"label": "Groq",           "key": "GROQ_API_KEY",       "quick": [], "deep": []},
    "openrouter": {"label": "OpenRouter",     "key": "OPENROUTER_API_KEY", "quick": [], "deep": []},
    "ollama":     {"label": "Ollama (local)", "key": None,                 "quick": [], "deep": []},
}
KEY_ALLOWLIST = ("DEEPSEEK_API_KEY", "FRED_API_KEY", "ALPACA_API_KEY", "ALPACA_SECRET_KEY", "SEC_EDGAR_EMAIL", "OLLAMA_BASE_URL") + tuple(
    p["key"] for p in PROVIDERS.values() if p["key"] and p["key"] != "DEEPSEEK_API_KEY")

# Engine cache and the decision memory log (shared with a CLI install of TradingAgents if you point both here).
ENGINE_STATE_DIR = Path(os.environ["GLASSBENCH_STATE_DIR"]).resolve() if os.environ.get("GLASSBENCH_STATE_DIR") else REPO_DIR / "state"

HOST = "127.0.0.1"
PORT = 8765
MAX_CONCURRENT_RUNS = 2

MODELS = {
    "quick": ["deepseek-v4-flash", "deepseek-v4-pro"],
    "deep": ["deepseek-v4-pro", "deepseek-v4-flash"],
}

# USD per 1M tokens (input, output). Estimates: edit here when DeepSeek changes prices.
PRICING = {
    "deepseek-v4-flash": (0.14, 0.28),
    "deepseek-v4-pro": (0.435, 0.87),
}

ANALYST_KEYS = ("market", "social", "news", "fundamentals")


def estimate_cost(model: str, tokens_in: int, tokens_out: int) -> float | None:
    price = PRICING.get(model)
    if price is None:
        return None
    return (tokens_in * price[0] + tokens_out * price[1]) / 1_000_000


_ENGINE_VERSION: str | None = None


def engine_version() -> str:
    """Package version plus the clone's commit, e.g. 0.4.0+be952b8, so two runs on different commits never share a label."""
    global _ENGINE_VERSION
    if _ENGINE_VERSION is None:
        import subprocess

        try:
            from importlib.metadata import version

            pkg = version("tradingagents")
        except Exception:
            pkg = "unknown"
        sha = ""
        try:
            sha = subprocess.run(["git", "-C", str(ENGINE_DIR), "rev-parse", "--short", "HEAD"],
                                 capture_output=True, text=True, timeout=5).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
        _ENGINE_VERSION = f"{pkg}+{sha}" if sha else pkg
    return _ENGINE_VERSION


_ENGINE_BUILDS: dict[str, dict] = {}


def engine_build(version: str) -> dict:
    """Is this engine commit a TradingAgents release, or the release plus Desk's own changes?

    A commit that upstream's main branch contains is the framework as released. Anything else is
    the fork, shown as "adjusted", with the commits that set it apart so a run never passes for stock.
    """
    if version in _ENGINE_BUILDS:
        return _ENGINE_BUILDS[version]
    import subprocess

    sha = version.split("+", 1)[1] if "+" in version else ""
    build = {"version": version.split("+", 1)[0], "commit": sha, "adjusted": False, "changes": []}
    if sha:
        repo = ["git", "-C", str(ENGINE_DIR)]
        try:
            inside = subprocess.run(repo + ["merge-base", "--is-ancestor", sha, "upstream/main"], capture_output=True, timeout=5)
            if inside.returncode == 1:
                log = subprocess.run(repo + ["log", "--format=%s", f"upstream/main..{sha}"], capture_output=True, text=True, timeout=5)
                build["adjusted"] = True
                build["changes"] = [line for line in log.stdout.splitlines() if line.strip()]
        except (OSError, subprocess.SubprocessError):
            pass  # no git or no upstream remote: nothing can be claimed, so the release label stays
    _ENGINE_BUILDS[version] = build
    return build


def default_trade_date() -> str:
    # Today: Yahoo only returns recent articles, so a past date runs with an empty news feed.
    return date.today().isoformat()


def engine_config(depth: int, deep_model: str, quick_model: str, memory_log_path: Path | None = None, variant: str = "",
                  provider: str = "deepseek") -> dict:
    from tradingagents.default_config import DEFAULT_CONFIG

    cfg = copy.deepcopy(DEFAULT_CONFIG)
    cfg.update(
        llm_provider=provider,
        deep_think_llm=deep_model,
        quick_think_llm=quick_model,
        backend_url=None,
        max_tokens=8192,
        llm_max_retries=4,
        max_debate_rounds=depth,
        max_risk_discuss_rounds=depth,
        output_language="English",
        checkpoint_enabled=False,
        results_dir=str(DATA_DIR / "engine_logs"),
        data_cache_dir=str(ENGINE_STATE_DIR / "cache"),
        memory_log_path=str(memory_log_path or ENGINE_STATE_DIR / "trading_memory.md"),
    )
    if variant in ("pit_valuation", "edgar_statements", "edgar_valuation"):
        # Statements as they were filed (upstream's sec_edgar vendor, v0.5.0+), Yahoo as the fallback for non-US filers.
        tools = dict(cfg.get("tool_vendors") or {})
        for tool in ("get_balance_sheet", "get_income_statement", "get_cashflow"):
            tools[tool] = "sec_edgar,yfinance"
        if variant == "edgar_valuation":
            # Valuation as of the run date, served by the engine itself (fork branch desk/edgar-valuation).
            tools["get_fundamentals"] = "sec_edgar,yfinance"
        cfg["tool_vendors"] = tools
    return cfg
