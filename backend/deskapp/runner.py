"""Runs TradingAgents with full event capture. Same steps as propagate(), plus streaming."""

from __future__ import annotations

import json
import logging
import threading
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor

from . import adapter
from .capture import CURRENT_CAPTURE, EngineLogCapture, RunCapture, _text_of
from .events import EventBus
from .reasoning import install_reasoning_tap
from .runconfig import CURRENT_CONFIG, install_run_config
from .variants import ensure_available, install_variants
from .settings import BACKTESTS_DIR, MAX_CONCURRENT_RUNS, RUNS_DIR, engine_config, engine_version
from .store import Store

log = logging.getLogger("deskapp.runner")


class RunCancelled(Exception):
    pass


class RunManager:
    def __init__(self, store: Store, bus: EventBus, workers: int = MAX_CONCURRENT_RUNS):
        self.store = store
        self.bus = bus
        self.pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="desk-run")
        self._cancel: dict[str, threading.Event] = {}
        self._log_capture = EngineLogCapture()
        logging.getLogger("tradingagents").addHandler(self._log_capture)
        install_reasoning_tap()
        install_variants()

    def submit(self, ticker: str, trade_date: str, analysts: list[str], depth: int, deep_model: str, quick_model: str,
               purpose: str = "live", backtest_id: str | None = None, memory: str = "shared", variant: str = "") -> str:
        ensure_available(variant)
        run_id = time.strftime("%Y%m%d-%H%M%S") + "-" + ticker.replace("/", "_").upper() + "-" + uuid.uuid4().hex[:4]
        self.store.create_run({
            "id": run_id, "ticker": ticker.upper(), "trade_date": trade_date, "analysts": analysts, "depth": depth,
            "deep_model": deep_model, "quick_model": quick_model, "status": "queued", "created_at": time.time(),
            "engine": "tradingagents", "engine_version": engine_version(), "provider": "deepseek",
            "purpose": purpose, "backtest_id": backtest_id, "memory": memory, "variant": variant,
        })
        self._cancel[run_id] = threading.Event()
        self.bus.emit(run_id, "run.queued", None, ticker=ticker.upper(), trade_date=trade_date, analysts=analysts,
                      depth=depth, deep_model=deep_model, quick_model=quick_model, purpose=purpose, backtest_id=backtest_id, memory=memory, variant=variant,
                      agents=[a["id"] for a in adapter.agents_for(analysts)])
        self.pool.submit(self._execute, run_id)
        return run_id

    def cancel(self, run_id: str) -> bool:
        flag = self._cancel.get(run_id)
        if flag is None:
            return False
        flag.set()
        run = self.store.get_run(run_id)
        if run and run["status"] == "queued":
            # Not started yet: settle it now instead of when a worker frees up.
            self._finish_cancelled(run_id, None)
        return True

    # ------------------------------------------------------------------------
    def _execute(self, run_id: str) -> None:
        run = self.store.get_run(run_id)
        if run is None or run["status"] != "queued":
            return  # cancelled while waiting in the queue
        cancel = self._cancel.setdefault(run_id, threading.Event())
        if cancel.is_set():
            self._finish_cancelled(run_id, None)
            return

        run_dir = RUNS_DIR / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        capture = RunCapture(self.bus, run_id, run_dir)
        capture.variant = run.get("variant") or ""
        token = CURRENT_CAPTURE.set(capture)
        config_token = None
        ticker, trade_date = run["ticker"], run["trade_date"]
        self.store.update_run(run_id, status="running", started_at=time.time())
        self.bus.emit(run_id, "run.started", None, ticker=ticker, trade_date=trade_date)

        try:
            from tradingagents.graph.trading_graph import TradingAgentsGraph
            from tradingagents.reporting import write_report_tree

            shared_memory = run.get("memory", "shared") != "off"
            # Memory off (backtests): an isolated log that is never read or scored, so no lesson from another
            # date can reach this decision and the shared live log stays untouched.
            isolated_log = None if shared_memory else BACKTESTS_DIR / (run.get("backtest_id") or "adhoc") / "memory_unused.md"
            config = engine_config(run["depth"], run["deep_model"], run["quick_model"], memory_log_path=isolated_log,
                                   variant=run.get("variant") or "")
            # The engine's data config is process-wide; this run must read its own (see runconfig.py).
            install_run_config()
            config_token = CURRENT_CONFIG.set(config)
            graph = TradingAgentsGraph(selected_analysts=run["analysts"], debug=False, config=config)
            graph.ticker = ticker

            past_context = ""
            if shared_memory:
                # Memory: score earlier decisions for this ticker, then load lessons (what the CLI skips).
                try:
                    graph._resolve_pending_entries(ticker)
                except Exception as exc:  # scoring needs prices; never block the run on it
                    capture.add_flag(None, "Memory scoring skipped", str(exc))
                past_context = graph.memory_log.get_past_context(ticker, as_of=graph._memory_as_of(trade_date))
            if past_context:
                self.bus.emit(run_id, "memory.context", "portfolio_manager", chars=len(past_context), preview=past_context[:1200])

            instrument_context = graph.resolve_instrument_context(ticker, "stock")
            self.bus.emit(run_id, "instrument.resolved", None, context=instrument_context)
            state = graph.propagator.create_initial_state(
                ticker, trade_date, asset_type="stock", past_context=past_context, instrument_context=instrument_context,
            )
            args = graph.propagator.get_graph_args(callbacks=[capture])
            args["stream_mode"] = ["updates", "messages"]

            final_state = dict(state)
            for mode, chunk in graph.graph.stream(state, **args):
                if cancel.is_set():
                    raise RunCancelled()
                if mode == "messages":
                    message, meta = chunk
                    node = (meta or {}).get("langgraph_node")
                    agent_id, kind = adapter.NODE_MAP.get(node, (None, None))
                    text = _text_of(getattr(message, "content", ""))
                    if agent_id and kind == "agent" and text and type(message).__name__.endswith("Chunk"):
                        capture.add_delta(agent_id, text)
                    continue
                for node, update in (chunk or {}).items():
                    if not isinstance(update, dict):
                        continue
                    final_state.update(update)
                    agent_id, kind = adapter.NODE_MAP.get(node, (None, None))
                    if kind != "agent":
                        continue
                    text = adapter.agent_text(agent_id, final_state)
                    if text:
                        self.bus.emit(run_id, "report.updated", agent_id, text=text)
                    if agent_id == "research_manager":
                        self.bus.emit(run_id, "decision.structured", agent_id, **adapter.parse_research_plan(final_state.get("investment_plan", "")))
                    elif agent_id == "trader":
                        self.bus.emit(run_id, "decision.structured", agent_id, **adapter.parse_trader_plan(final_state.get("trader_investment_plan", "")))
                    elif agent_id == "portfolio_manager":
                        self.bus.emit(run_id, "decision.structured", agent_id, **adapter.parse_pm_decision(final_state.get("final_trade_decision", "")))
                self._sync_totals(run_id, capture)
            capture.flush()

            rating = graph.process_signal(final_state.get("final_trade_decision", ""))
            graph.curr_state = final_state
            try:
                graph._log_state(trade_date, final_state)
            except Exception as exc:
                log.warning("engine state log failed: %s", exc)
            if shared_memory:
                graph.memory_log.store_decision(
                    ticker=ticker, trade_date=trade_date, final_trade_decision=final_state.get("final_trade_decision", ""),
                )

            write_report_tree(final_state, ticker, run_dir / "reports")
            (run_dir / "state.json").write_text(json.dumps(adapter.state_snapshot(final_state), indent=2, ensure_ascii=False), encoding="utf-8")
            decision = adapter.parse_decision(final_state)
            self._sync_totals(run_id, capture)
            self.store.update_run(run_id, status="finished", finished_at=time.time(), rating=rating, decision=decision,
                                  models_served=sorted(capture.models_served))
            self.bus.emit(run_id, "run.finished", None, rating=rating, decision=decision, **capture.totals)
        except RunCancelled:
            self._finish_cancelled(run_id, capture)
        except Exception as exc:
            capture.flush()
            self._sync_totals(run_id, capture)
            tb = traceback.format_exc(limit=6)
            log.error("run %s failed: %s", run_id, tb)
            self.store.update_run(run_id, status="failed", finished_at=time.time(), error=f"{type(exc).__name__}: {exc}"[:1000])
            self.bus.emit(run_id, "run.failed", None, error=f"{type(exc).__name__}: {exc}"[:1000], traceback=tb[-3000:])
        finally:
            CURRENT_CAPTURE.reset(token)
            if config_token is not None:
                CURRENT_CONFIG.reset(config_token)
            self._cancel.pop(run_id, None)

    def _sync_totals(self, run_id: str, capture: RunCapture) -> None:
        t = capture.totals
        self.store.update_run(run_id, tokens_in=t["tokens_in"], tokens_out=t["tokens_out"], cost_usd=round(t["cost_usd"], 6),
                              llm_calls=t["llm_calls"], tool_calls=t["tool_calls"], flags=t["flags"])

    def _finish_cancelled(self, run_id: str, capture: RunCapture | None) -> None:
        if capture:
            capture.flush()
            self._sync_totals(run_id, capture)
        self.store.update_run(run_id, status="cancelled", finished_at=time.time())
        self.bus.emit(run_id, "run.cancelled", None)
