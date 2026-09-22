"""HTTP API: runs, live events (Server-Sent Events with replay), files, metadata."""

from __future__ import annotations

import os

import asyncio
import csv
import io
from datetime import datetime
import json
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from . import __version__, adapter, brokers
from .events import TERMINAL_EVENTS, EventBus
from .keys import key_status, load_keys
from . import simulate as sim
from .backtest import BacktestManager, sample_evenly, weekly_dates
from .runner import RunManager
from .frameworks import frameworks as framework_sheets
from .variants import VARIANTS
from .settings import ANALYST_KEYS, DB_PATH, FRONTEND_DIST, MODELS, PRICING, PROVIDERS, RUNS_DIR, default_trade_date, engine_build, engine_version
from .store import TERMINAL_STATUSES, Store

store = Store(DB_PATH)
bus = EventBus(store)
manager: RunManager | None = None
backtests: BacktestManager | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global manager, backtests
    load_keys()
    bus.loop = asyncio.get_running_loop()
    store.mark_interrupted()
    store.pause_interrupted_backtests()
    manager = RunManager(store, bus)
    backtests = BacktestManager(store, manager)
    yield
    manager.pool.shutdown(wait=False, cancel_futures=True)


app = FastAPI(title="Desk", version=__version__, lifespan=lifespan)


class RunRequest(BaseModel):
    tickers: list[str] = Field(min_length=1, max_length=30)
    trade_date: str = Field(default_factory=default_trade_date, pattern=r"^\d{4}-\d{2}-\d{2}$")
    analysts: list[str] = Field(default_factory=lambda: list(ANALYST_KEYS), min_length=1)
    depth: int = Field(default=1, ge=1, le=5)
    deep_model: str = "deepseek-v4-pro"
    quick_model: str = "deepseek-v4-flash"
    provider: str = "deepseek"

    @field_validator("tickers")
    @classmethod
    def clean_tickers(cls, value: list[str]) -> list[str]:
        cleaned = []
        for t in value:
            t = t.strip().upper()
            if not t or len(t) > 15 or not all(c.isalnum() or c in ".-^=/" for c in t):
                raise ValueError(f"Ticker '{t}' is not a valid symbol")
            if t not in cleaned:
                cleaned.append(t)
        return cleaned

    @field_validator("analysts")
    @classmethod
    def known_analysts(cls, value: list[str]) -> list[str]:
        unknown = [a for a in value if a not in ANALYST_KEYS]
        if unknown:
            raise ValueError(f"Unknown analysts: {', '.join(unknown)}")
        return [a for a in ANALYST_KEYS if a in value]


# --- metadata ---------------------------------------------------------------
@app.get("/api/meta")
def meta():
    return {
        "version": __version__,
        "stages": adapter.STAGES,
        "agents": [{k: a[k] for k in ("id", "label", "name", "stage", "role", "reads")} | {"analyst_key": a.get("analyst_key")} for a in adapter.AGENTS],
        "analysts": list(ANALYST_KEYS),
        "models": MODELS,
        "providers": [{"id": pid, "label": p["label"], "key": p["key"], "present": bool(os.environ.get(p["key"])) if p["key"] else True,
                       "quick": p["quick"], "deep": p["deep"]} for pid, p in PROVIDERS.items()],
        "pricing": {m: {"input": p[0], "output": p[1]} for m, p in PRICING.items()},
        "default_trade_date": default_trade_date(),
        "engine_version": engine_version(),
        "engine_builds": {v: engine_build(v) for v in {engine_version(), *store.engine_versions()}},
        "variants": VARIANTS,
        "keys": key_status(),
    }


@app.get("/api/frameworks")
def list_frameworks():
    counts: dict[str, int] = {}
    for run in store.list_runs(100_000):
        key = "tradingagents" if (run.get("engine") or "tradingagents") == "tradingagents" else run["engine"]
        counts[key] = counts.get(key, 0) + 1
    return {"frameworks": framework_sheets(counts)}


# --- runs -------------------------------------------------------------------
@app.post("/api/runs")
def create_runs(req: RunRequest):
    provider = PROVIDERS.get(req.provider)
    if provider is None:
        raise HTTPException(400, f"Unknown provider {req.provider!r}. Choose one of: {', '.join(PROVIDERS)}.")
    if provider["key"] and not os.environ.get(provider["key"]):
        raise HTTPException(400, f"{provider['key']} is missing. Put it in .env at the repository root, then restart Glassbench.")
    if not req.deep_model.strip() or not req.quick_model.strip():
        raise HTTPException(400, "Both model ids are required: the quick model reads and debates, the deep model decides.")
    ids = [manager.submit(t, req.trade_date, req.analysts, req.depth, req.deep_model.strip(), req.quick_model.strip(), provider=req.provider)
           for t in req.tickers]
    return {"run_ids": ids}


@app.get("/api/runs")
def list_runs(limit: int = 200):
    runs = store.list_runs(limit)
    for run in runs:
        if run["status"] in ("running", "queued"):
            order, state = store.agent_progress(run["id"])
            run["progress"] = {"order": order, "state": state}
    return {"runs": runs}


EXPORT_COLUMNS = [
    "id", "ticker", "trade_date", "status", "purpose", "backtest_id", "memory", "variant", "models_served", "engine", "engine_version", "engine_adjusted", "provider", "rating", "research_recommendation", "trader_action", "entry_price",
    "stop_loss", "price_target", "time_horizon", "analysts", "debate_rounds", "quick_model", "deep_model",
    "started_at", "duration_s", "llm_calls", "tool_calls", "tokens_in", "tokens_out", "cost_usd_est", "flags", "error",
]


def _export_row(run: dict) -> dict:
    d = run.get("decision") or {}
    research, trader, pm = d.get("research") or {}, d.get("trader") or {}, d.get("portfolio") or {}
    started = run.get("started_at")
    return {
        "id": run["id"], "ticker": run["ticker"], "trade_date": run["trade_date"], "status": run["status"],
        "purpose": run.get("purpose") or "live", "backtest_id": run.get("backtest_id") or "", "memory": run.get("memory") or "shared",
        "variant": run.get("variant") or "", "models_served": " ".join(run.get("models_served") or []),
        "engine": run.get("engine") or "", "engine_version": run.get("engine_version") or "", "engine_adjusted": engine_build(run.get("engine_version") or "")["adjusted"], "provider": run.get("provider") or "",
        "rating": run.get("rating") or "", "research_recommendation": research.get("recommendation") or "",
        "trader_action": trader.get("action") or "", "entry_price": trader.get("entry_price") or "",
        "stop_loss": trader.get("stop_loss") or "", "price_target": pm.get("price_target") or "",
        "time_horizon": pm.get("time_horizon") or "", "analysts": " ".join(run.get("analysts") or []),
        "debate_rounds": run["depth"], "quick_model": run["quick_model"], "deep_model": run["deep_model"],
        "started_at": datetime.fromtimestamp(started).isoformat(timespec="seconds") if started else "",
        "duration_s": round(run["finished_at"] - started) if started and run.get("finished_at") else "",
        "llm_calls": run["llm_calls"], "tool_calls": run["tool_calls"], "tokens_in": run["tokens_in"],
        "tokens_out": run["tokens_out"], "cost_usd_est": round(run["cost_usd"] or 0, 6), "flags": run["flags"],
        "error": run.get("error") or "",
    }


@app.get("/api/search")
def search_logs(q: str, limit: int = 300):
    """Full-text search inside run logs. One entry per run with up to 3 snippets."""
    hits = store.search(q, limit)
    by_run: dict[str, dict] = {}
    for h in hits:
        entry = by_run.setdefault(h["run_id"], {"run_id": h["run_id"], "hits": 0, "snippets": []})
        entry["hits"] += 1
        if len(entry["snippets"]) < 3:
            entry["snippets"].append({"agent": h["agent"], "type": h["type"], "seq": h["seq"], "snippet": h["snippet"]})
    return {"query": q, "runs": list(by_run.values()), "total_hits": len(hits)}


@app.get("/api/runs.csv")
def export_runs():
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=EXPORT_COLUMNS)
    writer.writeheader()
    for run in store.list_runs(100_000):
        writer.writerow(_export_row(run))
    name = f"desk_runs_{datetime.now():%Y%m%d_%H%M}.csv"
    return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv; charset=utf-8",
                             headers={"Content-Disposition": f'attachment; filename="{name}"'})


@app.get("/api/runs/{run_id}")
def get_run(run_id: str):
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(404, "Run not found")
    return run


@app.post("/api/runs/{run_id}/cancel")
def cancel_run(run_id: str):
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(404, "Run not found")
    if run["status"] in TERMINAL_STATUSES:
        raise HTTPException(409, f"Run already {run['status']}")
    manager.cancel(run_id)
    return {"cancelling": True, "note": "Stops after the current agent step finishes"}


@app.get("/api/runs/{run_id}/events")
async def run_events(run_id: str, request: Request, after: int = 0):
    run = store.get_run(run_id)
    if run is None:
        raise HTTPException(404, "Run not found")
    last_event_id = request.headers.get("last-event-id")
    if last_event_id and last_event_id.isdigit():
        after = max(after, int(last_event_id))

    async def stream():
        queue = bus.subscribe(run_id)
        last = after
        try:
            for event in store.events_since(run_id, after):
                last = event["seq"]
                yield _sse(event)
            current = store.get_run(run_id)
            if current and current["status"] in TERMINAL_STATUSES:
                yield "event: end\ndata: {}\n\n"
                return
            while True:
                if await request.is_disconnected():
                    return
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15)
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
                    continue
                if event["seq"] <= last:
                    continue
                last = event["seq"]
                yield _sse(event)
                if event["type"] in TERMINAL_EVENTS:
                    yield "event: end\ndata: {}\n\n"
                    return
        finally:
            bus.unsubscribe(run_id, queue)

    return StreamingResponse(stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


def _sse(event: dict) -> str:
    return f"id: {event['seq']}\ndata: {json.dumps(event, ensure_ascii=False)}\n\n"


# --- backtests ----------------------------------------------------------------
class BacktestRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    tickers: list[str] = Field(min_length=1, max_length=30)
    start: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    end: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    sample: int | None = Field(default=None, ge=1, le=520, description="Spread this many dates evenly over the weekly grid (pilot)")
    analysts: list[str] = Field(default_factory=lambda: ["market", "fundamentals"], min_length=1)
    depth: int = Field(default=1, ge=1, le=5)
    deep_model: str = "deepseek-v4-pro"
    quick_model: str = "deepseek-v4-flash"
    budget_usd: float = Field(gt=0, le=200)
    variant: str = ""

    _tickers = field_validator("tickers")(RunRequest.clean_tickers.__func__)
    _analysts = field_validator("analysts")(RunRequest.known_analysts.__func__)


@app.post("/api/backtests")
def create_backtest(req: BacktestRequest):
    if req.end <= req.start:
        raise HTTPException(400, "End date must be after start date")
    try:
        grid = weekly_dates(req.start, req.end)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    if req.variant not in VARIANTS:
        raise HTTPException(400, f"Unknown variant '{req.variant}'")
    dates = sample_evenly(grid, req.sample) if req.sample else grid
    return backtests.create(req.name, req.tickers, dates, req.analysts, req.depth, req.deep_model, req.quick_model,
                            req.budget_usd, grid={"frequency": "weekly", "start": req.start, "end": req.end,
                                                  "grid_size": len(grid), "sample": req.sample}, variant=req.variant)


@app.get("/api/backtests")
def list_backtests():
    return {"backtests": [backtests.detail(b["id"]) for b in store.list_backtests()]}


def _backtest_action(bt_id: str, action):
    try:
        return action(bt_id)
    except KeyError:
        raise HTTPException(404, "Backtest not found")


@app.get("/api/backtests/{bt_id}")
def get_backtest(bt_id: str):
    return _backtest_action(bt_id, backtests.detail)


_results_cache: dict[tuple, dict] = {}
SIBLING_KEYS = ("dates", "analysts", "depth", "deep_model", "quick_model", "memory", "engine_version")


def _siblings(bt_id: str) -> list[dict]:
    """Backtests on the same stocks, dates, analysts and models that differ only by framework variant."""
    me = store.get_backtest(bt_id)
    if me is None:
        return []
    mine = me["config"]
    out = []
    for bt in store.list_backtests():
        cfg = bt["config"]
        if sorted(cfg["tickers"]) == sorted(mine["tickers"]) and all(cfg.get(k) == mine.get(k) for k in SIBLING_KEYS):
            detail = backtests.detail(bt["id"])
            out.append({"id": bt["id"], "name": bt["name"], "variant": cfg.get("variant", ""), "status": bt["status"],
                        "finished": detail["counts"]["finished"], "total": len(detail["items"]), "spent_usd": detail["spent_usd"],
                        "created_at": bt["created_at"]})
    order = {"": 0, "prompt_pre1196": 1, "pit_valuation": 2, "edgar_statements": 3, "edgar_valuation": 4}
    return sorted(out, key=lambda s: (order.get(s["variant"], 9), s["created_at"]))


@app.get("/api/backtests/{bt_id}/compare")
def compare_variants(bt_id: str, cost_bps: float = 10):
    """Headline numbers for every variant of this backtest, per stock and combined."""
    rows = []
    for sib in _siblings(bt_id):
        if sib["finished"] == 0:
            rows.append({**sib, "views": {}})
            continue
        res = backtest_results(sib["id"], cost_bps)
        views = {}
        for view in res["tickers"] + ([res["combined"]] if res["combined"] else []):
            get = {s["key"]: s["metrics"] for s in view["strategies"]}
            ratings = [d["rating"] or d["status"] for d in view.get("decisions") or []]
            if view["ticker"] == "Combined":
                ratings = [d["rating"] or d["status"] for t in res["tickers"] for d in t["decisions"]]
            views[view["ticker"]] = {
                "ratings": {r: ratings.count(r) for r in dict.fromkeys(ratings)},
                "levels": get.get("agents_levels"), "rating_only": get.get("agents_rating"),
                "buy_hold": (get.get("buy_hold") or {}).get("total_return"),
            }
        rows.append({**sib, "views": views})
    return {"backtest_id": bt_id, "cost_bps": cost_bps, "variants": rows}


@app.get("/api/backtests/{bt_id}/results")
def backtest_results(bt_id: str, cost_bps: float = 10):
    """Positions, returns, benchmarks and placebo from the saved decisions. Free: replays stored ratings only."""
    if not 0 <= cost_bps <= 200:
        raise HTTPException(400, "cost_bps must be between 0 and 200")
    detail = _backtest_action(bt_id, backtests.detail)
    runs = store.runs_by_ids([it["run_id"] for it in detail["items"] if it["run_id"]])
    key = (bt_id, cost_bps, sim.date.today().isoformat(), tuple((it["run_id"], it["status"]) for it in detail["items"]))
    if key in _results_cache:
        return {**_results_cache[key], "siblings": _siblings(bt_id)}
    tickers = []
    for ticker in detail["config"]["tickers"]:
        decisions = []
        for it in detail["items"]:
            if it["ticker"] != ticker or it["status"] in ("pending", "queued", "running"):
                continue
            run = runs.get(it["run_id"]) or {}
            trader = ((run.get("decision") or {}).get("trader") or {})
            rating = run.get("rating") if it["status"] == "finished" else None
            decisions.append(sim.Decision(it["date"], rating, it["run_id"], trader.get("entry_price"), trader.get("stop_loss"), it["status"]))
        if not decisions:
            continue
        try:
            tickers.append(sim.run_ticker(ticker, decisions, cost_bps))
        except ValueError as exc:
            raise HTTPException(502, str(exc))
    if not tickers:
        raise HTTPException(409, "No finished decisions to replay yet")
    combined = sim.combine(tickers) if len(tickers) > 1 else None
    for t in tickers:
        t.pop("placebo_curves", None)
    result = {
        "backtest_id": bt_id, "name": detail["name"], "config": detail["config"], "spent_usd": detail["spent_usd"],
        "tickers": tickers, "combined": combined,
        "assumptions": {"cost_bps": cost_bps, "fill": "next session open", "cash_return": 0.0, "hold_add": sim.HOLD_ADD,
                        "prices": "Yahoo daily, adjusted for splits and dividends (same basis as the engine)",
                        "placebo_sims": sim.PLACEBO_SIMS, "ma": [sim.MA_FAST, sim.MA_SLOW], "risk_free": 0.0},
    }
    if len(_results_cache) >= 12:
        _results_cache.pop(next(iter(_results_cache)))
    _results_cache[key] = result
    return {**result, "siblings": _siblings(bt_id)}


@app.post("/api/backtests/{bt_id}/start")
def start_backtest(bt_id: str):
    if not any(k["name"] == "DEEPSEEK_API_KEY" and k["present"] for k in key_status()):
        raise HTTPException(400, "DEEPSEEK_API_KEY is missing from .env.")
    return _backtest_action(bt_id, backtests.start)


@app.post("/api/backtests/{bt_id}/pause")
def pause_backtest(bt_id: str):
    return _backtest_action(bt_id, backtests.pause)


@app.post("/api/backtests/{bt_id}/cancel")
def cancel_backtest(bt_id: str):
    return _backtest_action(bt_id, backtests.cancel)


# --- settings: broker --------------------------------------------------------
class IbkrConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = Field(default=4002, ge=1, le=65535)
    client_id: int = Field(default=17, ge=0, le=999)


class BrokerSettings(BaseModel):
    broker: str
    ibkr: IbkrConfig | None = None


@app.get("/api/settings")
def get_settings():
    return {**brokers.load_settings(), "brokers": brokers.BROKERS}


@app.put("/api/settings")
def put_settings(body: BrokerSettings):
    try:
        saved = brokers.save_settings(body.broker, body.ibkr.model_dump() if body.ibkr else None)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return {**saved, "brokers": brokers.BROKERS}


@app.post("/api/broker/check")
def broker_check(body: BrokerSettings):
    return brokers.check_connection(body.broker, body.ibkr.model_dump() if body.ibkr else None)


# --- files ------------------------------------------------------------------
def _run_dir(run_id: str) -> Path:
    if store.get_run(run_id) is None:
        raise HTTPException(404, "Run not found")
    return RUNS_DIR / run_id


LABELS = {
    "reports/1_analysts/market.md": "Market analyst report",
    "reports/1_analysts/sentiment.md": "Sentiment analyst report",
    "reports/1_analysts/news.md": "News analyst report",
    "reports/1_analysts/fundamentals.md": "Fundamentals analyst report",
    "reports/2_research/bull.md": "Bull argument",
    "reports/2_research/bear.md": "Bear argument",
    "reports/2_research/manager.md": "Research manager plan",
    "reports/3_trading/trader.md": "Trader proposal",
    "reports/4_risk/aggressive.md": "Aggressive argument",
    "reports/4_risk/conservative.md": "Conservative argument",
    "reports/4_risk/neutral.md": "Neutral argument",
    "reports/5_portfolio/decision.md": "Portfolio manager decision",
    "reports/complete_report.md": "Complete report",
    "state.json": "Final state (JSON)",
    "events.jsonl": "Event log (JSONL)",
}


@app.get("/api/runs/{run_id}/files")
def list_files(run_id: str):
    base = _run_dir(run_id)
    files = []
    if base.exists():
        for path in sorted(base.rglob("*")):
            if path.is_file():
                rel = path.relative_to(base).as_posix()
                files.append({"path": rel, "label": LABELS.get(rel), "bytes": path.stat().st_size,
                              "group": "tool_outputs" if rel.startswith("tool_outputs/") else "artifacts"})
    order = list(LABELS)
    files.sort(key=lambda f: (f["group"] != "artifacts", order.index(f["path"]) if f["path"] in order else len(order), f["path"]))
    return {"files": files}


@app.get("/api/runs/{run_id}/files/{file_path:path}")
def get_file(run_id: str, file_path: str, download: bool = False):
    base = _run_dir(run_id).resolve()
    target = (base / file_path).resolve()
    if base not in target.parents or not target.is_file():
        raise HTTPException(404, "File not found")
    media = "text/plain; charset=utf-8" if target.suffix in (".md", ".txt", ".jsonl", ".log") else None
    return FileResponse(target, media_type=media, filename=target.name if download else None,
                        content_disposition_type="attachment" if download else "inline")


@app.get("/api/runs/{run_id}/bundle.zip")
def bundle(run_id: str):
    base = _run_dir(run_id)
    run = store.get_run(run_id)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in base.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(base).as_posix())
        zf.writestr("run.json", json.dumps(run, indent=2))
    buffer.seek(0)
    name = f"{run['ticker']}_{run['trade_date']}_{run_id[-4:]}.zip"
    return StreamingResponse(buffer, media_type="application/zip", headers={"Content-Disposition": f'attachment; filename="{name}"'})


# --- frontend -----------------------------------------------------------------
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa(full_path: str):
        base = FRONTEND_DIST.resolve()
        candidate = (base / full_path).resolve()
        if full_path and base in candidate.parents and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(base / "index.html")
else:
    @app.get("/", include_in_schema=False)
    def no_frontend():
        return HTMLResponse("<p>Desk API is running. Build the frontend with <code>npm run build</code> in desk/frontend.</p>")
