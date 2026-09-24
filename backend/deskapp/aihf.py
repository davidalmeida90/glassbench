"""AI Hedge Fund (virattt/ai-hedge-fund) as a second engine: what it offers, and how one run is driven.

The engine runs in its own clone and virtual environment (settings.AIHF_*), started as a subprocess by
drivers/aihf_driver.py. Every JSON line the driver prints becomes a run event on the same bus TradingAgents
runs use, so the run page, the database and the search work unchanged. This module adds the parts only
Glassbench knows: token costs, data flags, and a five tier rating mapped from the blended conviction so
AI Hedge Fund runs sit in the same tables as TradingAgents runs.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import threading
import time
from pathlib import Path

from .settings import AIHF_DATA_CACHE, AIHF_DRIVER, AIHF_PRIVATE_DIR, AIHF_ENGINE, AIHF_PYTHON, KEY_ALLOWLIST, RUNS_DIR, aihf_version, estimate_cost

log = logging.getLogger("deskapp.aihf")

STAGES = [
    {"id": "analysts", "label": "Analysts"},
    {"id": "blend", "label": "Blend"},
    {"id": "risk", "label": "Risk"},
    {"id": "execution", "label": "Execution"},
]

LABELS = {"buffett": "Buffett", "munger": "Munger", "graham": "Graham", "lynch": "Lynch",
          "druckenmiller": "Druckenmiller", "pead": "Earnings drift"}
NAMES = {"buffett": "Warren Buffett agent", "munger": "Charlie Munger agent", "graham": "Benjamin Graham agent",
         "lynch": "Peter Lynch agent", "druckenmiller": "Stanley Druckenmiller agent", "pead": "Post-earnings drift model"}
STAGE_AGENTS = [
    {"id": "blend", "label": "Blend", "name": "Strategy blend", "stage": "blend", "role": "rule",
     "reads": ["each analyst's conviction", "the strategy's blend weights and mode"]},
    {"id": "risk", "label": "Risk limits", "name": "Risk limits", "stage": "risk", "role": "rule",
     "reads": ["netted target weights", "max position 25%, max gross 100%"]},
    {"id": "execution", "label": "Execution", "name": "Simulated execution", "stage": "execution", "role": "rule",
     "reads": ["final weights", "the next completed session close"]},
]

# Glassbench's own mapping, shown with every run: AI Hedge Fund returns convictions and weights, not ratings.
RATING_BANDS = [(0.5, "Buy"), (0.15, "Overweight"), (-0.15, "Hold"), (-0.5, "Underweight")]
RATING_RULE = ("Glassbench maps the blended conviction to a rating so frameworks share one table: "
               "0.50 or more Buy, 0.15 to 0.50 Overweight, above -0.15 Hold, above -0.50 Underweight, else Sell.")

_DESCRIBE: dict | None = None
_DESCRIBE_LOCK = threading.Lock()


def installed() -> bool:
    return AIHF_PYTHON.exists() and AIHF_DRIVER.exists()


def describe(refresh: bool = False) -> dict:
    """Analysts, library strategies and models from the installed clone (cached), or why it is unavailable."""
    global _DESCRIBE
    with _DESCRIBE_LOCK:
        if _DESCRIBE is not None and not refresh:
            return _DESCRIBE
        if not installed():
            _DESCRIBE = {"installed": False, "error": f"AI Hedge Fund is not installed at {AIHF_PYTHON.parent.parent.parent}"}
            return _DESCRIBE
        try:
            out = subprocess.run([str(AIHF_PYTHON), str(AIHF_DRIVER), "--describe"], capture_output=True, text=True,
                                 encoding="utf-8", timeout=120, env=_child_env(set()))
            data = json.loads(out.stdout)
            _DESCRIBE = {"installed": True, "version": aihf_version(), **data}
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
            _DESCRIBE = {"installed": False, "error": f"describe failed: {exc}"}
        return _DESCRIBE


def meta_for_ui() -> dict:
    d = describe()
    if not d.get("installed"):
        return {"installed": False, "error": d.get("error")}
    return {
        "installed": True,
        "version": d["version"],
        "analysts": [{**a, "label": LABELS.get(a["name"], a["name"].title())} for a in d["analysts"]],
        "strategies": d["strategies"],
        "models": [{**m, "present": bool(os.environ.get(m["key"])) if m.get("key") else True} for m in d["models"]],
        "default_model": "deepseek-flash",
        "data_key": {"name": "FINANCIAL_DATASETS_API_KEY", "present": bool(os.environ.get("FINANCIAL_DATASETS_API_KEY"))},
        "rating_rule": RATING_RULE,
    }


def plan(strategy: str | None, analysts: list[str] | None) -> tuple[list[str], str]:
    """The analysts a run will staff, in order, and the label stored as the run's variant."""
    d = describe()
    if strategy:
        match = next((s for s in d.get("strategies", []) if s["name"] == strategy), None)
        if match is None:
            raise ValueError(f"Unknown strategy {strategy!r}. Choose one of: {', '.join(s['name'] for s in d.get('strategies', []))}.")
        return [m["name"] for m in match["models"]], strategy
    known = {a["name"] for a in d.get("analysts", [])}
    chosen = list(dict.fromkeys(a.strip() for a in analysts or [] if a.strip()))
    unknown = [a for a in chosen if a not in known]
    if not chosen or unknown:
        raise ValueError(f"Pick a strategy or at least one analyst. Unknown: {', '.join(unknown) or 'none given'}.")
    return chosen, "custom"


def model_key(model: str) -> str | None:
    for m in describe().get("models", []):
        if m["model_name"] == model:
            return m.get("key")
    return "ANTHROPIC_API_KEY"  # AI Hedge Fund sends unlisted ids to Anthropic


def agent_meta(analysts: list[str]) -> list[dict]:
    kinds = {a["name"]: a for a in describe().get("analysts", [])}
    out = []
    for name in analysts:
        llm = kinds.get(name, {}).get("kind", "llm") == "llm"
        reads = (["Point-in-time fundamentals snapshot", "Company facts"] if llm else ["Earnings history", "Prices"])
        out.append({"id": name, "label": LABELS.get(name, name.title()), "name": NAMES.get(name, name),
                    "stage": "analysts", "role": "quick" if llm else "rule", "reads": reads, "analyst_key": name})
    return out + [{**a, "analyst_key": None} for a in STAGE_AGENTS]


def conviction_to_rating(conviction: float) -> str:
    for floor, rating in RATING_BANDS:
        if conviction >= floor if floor > 0 else conviction > floor:
            return rating
    return "Sell"


def summarize(record: dict, executed: bool, ticker: str) -> tuple[str, dict]:
    """Rating and decision from a cycle record. The rating reads the assessment as of the run date."""
    original = record.get("original_assessment") if executed else record.get("proposal")
    original = original or record
    strategies, signals, total_slice, blended = [], [], 0.0, 0.0
    for s in original.get("strategies", []):
        conv = (s.get("convictions") or {}).get(ticker)
        strategies.append({"name": s.get("name"), "slice": s.get("slice"), "conviction": conv,
                           "weight": (s.get("weights") or {}).get(ticker, 0.0), "flat_reason": s.get("flat_reason")})
        total_slice += s.get("slice") or 0.0
        blended += (s.get("slice") or 0.0) * (conv or 0.0)
        for sig in s.get("signals", []):
            if sig.get("ticker") != ticker:
                continue
            md = sig.get("metadata") or {}
            signals.append({"analyst": sig.get("model_name"), "strategy": s.get("name"), "signal": md.get("signal"),
                            "confidence": md.get("confidence"), "conviction": sig.get("value"),
                            "abstained": bool(md.get("abstained"))})
    conviction = blended / total_slice if total_slice else 0.0
    final_weight = (original.get("final_weights") or {}).get(ticker, 0.0)
    stance = "Long" if final_weight > 1e-9 else "Short" if final_weight < -1e-9 else "Flat"
    abstained = sum(s["abstained"] for s in signals)
    # A blend that most analysts sat out is not a view: an abstention counts as zero conviction, so a "Hold" would
    # really mean "no data". More than half abstaining makes the run REVIEW, and each abstention is a data flag.
    rating = "REVIEW" if signals and abstained * 2 > len(signals) else conviction_to_rating(conviction)
    decision = {
        "engine": AIHF_ENGINE, "status": "executed" if executed else "pending", "as_of": original.get("as_of"),
        "conviction": round(conviction, 4), "rating_rule": RATING_RULE, "stance": stance,
        "target_weight": (original.get("target_weights") or {}).get(ticker, 0.0), "final_weight": final_weight,
        "clamps": original.get("clamps") or [], "strategies": strategies, "signals": signals,
        "abstained": abstained,
    }
    if executed:
        refreshed = record.get("refreshed_assessment") or {}
        decision["execution"] = {"as_of": record.get("execution_as_of"), "orders": record.get("orders"),
                                 "fills": record.get("fills"), "nav": record.get("nav"), "cash": record.get("cash"),
                                 "executed_weight": (record.get("final_weights") or {}).get(ticker, 0.0)}
        if refreshed.get("as_of") and refreshed.get("as_of") != original.get("as_of"):
            decision["execution"]["refreshed_as_of"] = refreshed.get("as_of")
    else:
        decision["execution"] = {"pending": record.get("reason"), "scheduled": record.get("scheduled_execution_date")}
    return rating, decision


# ---------------------------------------------------------------------------
def _child_env(keys: set[str]) -> dict:
    """The parent environment without the API keys this run does not need."""
    env = {k: v for k, v in os.environ.items() if k not in KEY_ALLOWLIST or k in keys}
    env.pop("HEDGE_FUND_LLM_MODEL", None)
    env["PYTHONUTF8"] = "1"
    return env


def execute(manager, run_id: str, run: dict, cancel: threading.Event, fixture: bool = False) -> None:
    """Drive one cycle and relay its events. Raises RunCancelled on cancel; any other failure marks the run failed."""
    from .runner import RunCancelled

    store, bus = manager.store, manager.bus
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    model = run["quick_model"]
    variant = run.get("variant") or "custom"
    argv = [str(AIHF_PYTHON), str(AIHF_DRIVER), "--ticker", run["ticker"], "--date", run["trade_date"],
            "--model", model, "--run-dir", str(run_dir), "--data-cache", str(AIHF_DATA_CACHE),
            "--private-dir", str(AIHF_PRIVATE_DIR / run_id)]
    argv += ["--strategy", variant] if variant != "custom" else ["--analysts", ",".join(run["analysts"])]
    if fixture:
        argv.append("--fixture")
    keys = {"FINANCIAL_DATASETS_API_KEY", model_key(model) or ""}

    totals = {"tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0, "llm_calls": 0, "tool_calls": 0, "flags": 0}
    served: set[str] = set()
    finished: dict | None = None
    failure: str | None = None

    def sync():
        store.update_run(run_id, tokens_in=totals["tokens_in"], tokens_out=totals["tokens_out"],
                         cost_usd=round(totals["cost_usd"], 6), llm_calls=totals["llm_calls"],
                         tool_calls=totals["tool_calls"], flags=totals["flags"])

    with open(run_dir / "aihf.log", "w", encoding="utf-8") as errlog:
        proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=errlog, text=True, encoding="utf-8",
                                cwd=run_dir, env=_child_env(keys))
        assert proc.stdout is not None
        try:
            for raw in proc.stdout:
                if cancel.is_set():
                    raise RunCancelled()
                try:
                    line = json.loads(raw)
                except json.JSONDecodeError:
                    errlog.write(raw)
                    continue
                type_, agent = line.pop("type", ""), line.pop("agent", None)
                if type_ == "driver.started":
                    bus.emit(run_id, "engine.started", None, engine=AIHF_ENGINE, version=line.get("aihf_version"),
                             model=line.get("model"), lanes=line.get("lanes"), spec=line.get("spec"))
                    continue
                if type_ == "driver.finished":
                    finished = line
                    continue
                if type_ == "driver.failed":
                    failure = line.get("error") or "AI Hedge Fund failed"
                    errlog.write(line.get("traceback") or "")
                    continue
                if type_ == "llm.started":
                    totals["llm_calls"] += 1
                elif type_ == "llm.finished":
                    if line.get("served_model"):
                        served.add(line["served_model"])
                    cost = estimate_cost(line.get("served_model") or "", line.get("tokens_in", 0), line.get("tokens_out", 0))
                    if cost is None:
                        cost = estimate_cost(line.get("model") or "", line.get("tokens_in", 0), line.get("tokens_out", 0))
                    line["cost_usd"] = cost
                    totals["tokens_in"] += line.get("tokens_in", 0)
                    totals["tokens_out"] += line.get("tokens_out", 0)
                    totals["cost_usd"] += cost or 0.0
                elif type_ == "tool.called":
                    totals["tool_calls"] += 1
                bus.emit(run_id, type_, agent, **line)
                if type_ == "decision.structured" and line.get("abstained"):
                    totals["flags"] += 1
                    bus.emit(run_id, "data.flag", agent, label="Analyst abstained", source="AI Hedge Fund",
                             detail=str(line.get("abstain_reason") or "no reason given")[:300])
                if type_ == "tool.result" and line.get("flag"):
                    totals["flags"] += 1
                    bus.emit(run_id, "data.flag", agent, label=line["flag"], source=line.get("tool"),
                             detail=str(line.get("preview") or "")[:200])
                if type_ in ("llm.finished", "tool.result", "agent.finished"):
                    sync()
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
    code = proc.wait()
    sync()
    if finished is None:
        raise RuntimeError(failure or f"AI Hedge Fund exited with code {code} before finishing; see aihf.log in the run folder")
    record = finished.get("record") or {}
    rating, decision = summarize(record, finished.get("status") == "executed", run["ticker"])
    store.update_run(run_id, status="finished", finished_at=time.time(), rating=rating, decision=decision,
                     models_served=sorted(served))
    bus.emit(run_id, "run.finished", None, rating=rating, decision=decision, **totals)


def version() -> str:
    return aihf_version()


def run_dir_for(run_id: str) -> Path:
    return RUNS_DIR / run_id
