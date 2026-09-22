"""Backtest batches: generate agent decisions over past dates, cost-capped and resumable.

This module only produces decisions. Every run goes through RunManager, so it lands in the
runs table with its full event log like any live run, tagged purpose='backtest'. Replaying
those decisions into positions and returns is a separate, LLM-free step.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from datetime import date

from .runner import RunManager
from .settings import ANALYST_KEYS, engine_version
from .store import TERMINAL_STATUSES, Store

log = logging.getLogger("deskapp.backtest")

# USD per run by analyst count, used until real runs with the same shape exist in the database.
FALLBACK_COST_PER_RUN = {1: 0.030, 2: 0.040, 3: 0.052, 4: 0.062}
MAX_ATTEMPTS = 2  # a failed run is retried once, then left flagged as failed (never treated as a Hold)


def weekly_dates(start: str, end: str, calendar_ticker: str = "SPY") -> list[str]:
    """Last trading day of each week between start and end, from the exchange's actual trading days."""
    import yfinance as yf

    hist = yf.Ticker(calendar_ticker).history(start=start, end=_next_day(end), auto_adjust=False)
    if hist.empty:
        raise ValueError(f"No trading days found between {start} and {end}")
    days = [d.date() for d in hist.index]
    last_of_week: dict[tuple[int, int], date] = {}
    for d in days:
        last_of_week[d.isocalendar()[:2]] = d
    today = date.today()
    # Drop a week still in progress (Monday to Friday): its last trading day is not known yet.
    in_progress = today.isocalendar()[:2] if today.weekday() < 5 else None
    return [d.isoformat() for key, d in sorted(last_of_week.items()) if key != in_progress and d < today]


def _next_day(iso: str) -> str:
    return date.fromordinal(date.fromisoformat(iso).toordinal() + 1).isoformat()


def sample_evenly(dates: list[str], n: int) -> list[str]:
    """n dates spread across the grid, always including the first and last, so a pilot's runs are reusable later."""
    if n >= len(dates):
        return list(dates)
    if n == 1:
        return [dates[-1]]
    step = (len(dates) - 1) / (n - 1)
    return [dates[round(i * step)] for i in range(n)]


class BacktestManager:
    def __init__(self, store: Store, runs: RunManager):
        self.store = store
        self.runs = runs
        self._threads: dict[str, threading.Thread] = {}
        self._stop: dict[str, threading.Event] = {}
        self._lock = threading.Lock()

    # --- setup -----------------------------------------------------------------
    def create(self, name: str, tickers: list[str], dates: list[str], analysts: list[str], depth: int,
               deep_model: str, quick_model: str, budget_usd: float, grid: dict | None = None, variant: str = "") -> dict:
        analysts = [a for a in ANALYST_KEYS if a in analysts]
        bt_id = time.strftime("bt-%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
        config = {
            "tickers": tickers, "dates": sorted(dates), "analysts": analysts, "depth": depth,
            "deep_model": deep_model, "quick_model": quick_model, "memory": "off",
            "engine": "tradingagents", "engine_version": engine_version(), "grid": grid or {}, "variant": variant,
        }
        # Chronological order, tickers interleaved within each date.
        items = [{"ticker": t, "date": d, "run_ids": [], "reused": False} for d in config["dates"] for t in tickers]
        bt = {"id": bt_id, "name": name, "created_at": time.time(), "status": "ready", "config": config,
              "items": items, "budget_usd": budget_usd}
        self.store.create_backtest(bt)
        return self.detail(bt_id)

    def estimate_per_run(self, analysts: list[str], depth: int) -> float:
        """Average cost of finished runs with the same analyst set and depth; fallback table otherwise."""
        rows = [r for r in self.store.list_runs(100_000)
                if r["status"] == "finished" and r["analysts"] == analysts and r["depth"] == depth and r["cost_usd"]]
        if len(rows) >= 3:
            return sum(r["cost_usd"] for r in rows) / len(rows)
        return FALLBACK_COST_PER_RUN.get(len(analysts), 0.062) * depth

    # --- control ---------------------------------------------------------------
    def start(self, bt_id: str) -> dict:
        bt = self.store.get_backtest(bt_id)
        if bt is None:
            raise KeyError(bt_id)
        with self._lock:
            if bt_id in self._threads and self._threads[bt_id].is_alive():
                return self.detail(bt_id)
            self._stop[bt_id] = threading.Event()
            self.store.update_backtest(bt_id, status="running", note=None)
            thread = threading.Thread(target=self._loop, args=(bt_id,), name=f"desk-{bt_id}", daemon=True)
            self._threads[bt_id] = thread
            thread.start()
        return self.detail(bt_id)

    def pause(self, bt_id: str) -> dict:
        """Stop submitting new runs; runs already in flight finish and are kept."""
        flag = self._stop.get(bt_id)
        if flag:
            flag.set()
        self.store.update_backtest(bt_id, status="paused", note="Paused: runs in flight will finish")
        return self.detail(bt_id)

    def cancel(self, bt_id: str) -> dict:
        flag = self._stop.get(bt_id)
        if flag:
            flag.set()
        bt = self.store.get_backtest(bt_id)
        runs = self.store.runs_by_ids([rid for it in bt["items"] for rid in it["run_ids"]])
        for run in runs.values():
            if run["status"] not in TERMINAL_STATUSES:
                self.runs.cancel(run["id"])
        self.store.update_backtest(bt_id, status="cancelled", note="Cancelled")
        return self.detail(bt_id)

    # --- the batch loop --------------------------------------------------------
    def _loop(self, bt_id: str) -> None:
        stop = self._stop[bt_id]
        try:
            while not stop.is_set():
                bt = self.store.get_backtest(bt_id)
                cfg, items = bt["config"], bt["items"]
                runs = self.store.runs_by_ids([rid for it in items for rid in it["run_ids"]])
                in_flight = [r for r in runs.values() if r["status"] not in TERMINAL_STATUSES]
                per_run = self.estimate_per_run(cfg["analysts"], cfg["depth"])
                spent = sum((r["cost_usd"] or 0) for r in runs.values() if r.get("backtest_id") == bt_id)

                pending = [i for i, it in enumerate(items) if self._needs_run(it, runs)]
                if not pending and not in_flight:
                    self.store.update_backtest(bt_id, status="finished", note=None)
                    return
                if not pending or len(in_flight) >= self.runs.pool._max_workers:
                    time.sleep(2)
                    continue

                # Hard cap: money already spent + a full estimate for every run still in flight + the next run.
                committed = spent + sum(max(per_run - (r["cost_usd"] or 0), 0) for r in in_flight)
                if committed + per_run > bt["budget_usd"]:
                    if in_flight:
                        time.sleep(2)
                        continue
                    self.store.update_backtest(
                        bt_id, status="paused",
                        note=f"Budget cap reached: ${spent:.2f} spent of ${bt['budget_usd']:.2f}; next run estimated ${per_run:.3f}",
                    )
                    return

                idx = pending[0]
                it = items[idx]
                reusable = None if it["run_ids"] else self.store.find_reusable_run(
                    it["ticker"], it["date"], cfg["analysts"], cfg["depth"], cfg["deep_model"], cfg["quick_model"],
                    "off", cfg["engine_version"], cfg.get("variant", ""),
                )
                if reusable:
                    it["run_ids"].append(reusable["id"])
                    it["reused"] = True
                else:
                    run_id = self.runs.submit(it["ticker"], it["date"], cfg["analysts"], cfg["depth"], cfg["deep_model"],
                                              cfg["quick_model"], purpose="backtest", backtest_id=bt_id, memory="off",
                                              variant=cfg.get("variant", ""))
                    it["run_ids"].append(run_id)
                self.store.update_backtest(bt_id, items=items)
        except Exception as exc:
            log.exception("backtest %s loop failed", bt_id)
            self.store.update_backtest(bt_id, status="paused", note=f"Stopped by an error: {type(exc).__name__}: {exc}"[:500])

    @staticmethod
    def _needs_run(item: dict, runs: dict[str, dict]) -> bool:
        if not item["run_ids"]:
            return True
        last = runs.get(item["run_ids"][-1])
        if last is None or last["status"] == "finished":
            return False
        if last["status"] in ("queued", "running"):
            return False
        # failed or cancelled: retry until the attempt limit
        return last["status"] == "failed" and len(item["run_ids"]) < MAX_ATTEMPTS

    # --- read model --------------------------------------------------------------
    def detail(self, bt_id: str) -> dict:
        bt = self.store.get_backtest(bt_id)
        if bt is None:
            raise KeyError(bt_id)
        cfg = bt["config"]
        runs = self.store.runs_by_ids([rid for it in bt["items"] for rid in it["run_ids"]])
        rows, spent, counts = [], 0.0, {"finished": 0, "running": 0, "queued": 0, "failed": 0, "cancelled": 0, "pending": 0}
        for it in bt["items"]:
            attempts = [runs[r] for r in it["run_ids"] if r in runs]
            spent += sum((r["cost_usd"] or 0) for r in attempts if r.get("backtest_id") == bt_id)
            last = attempts[-1] if attempts else None
            status = last["status"] if last else "pending"
            counts[status] = counts.get(status, 0) + 1
            rows.append({
                "ticker": it["ticker"], "date": it["date"], "status": status, "reused": it["reused"],
                "attempts": len(attempts), "run_id": last["id"] if last else None,
                "rating": last.get("rating") if last and status == "finished" else None,  # errors are never Holds
                "cost_usd": sum((r["cost_usd"] or 0) for r in attempts),
                "duration_s": round(last["finished_at"] - last["started_at"]) if last and last.get("finished_at") and last.get("started_at") else None,
            })
        per_run = self.estimate_per_run(cfg["analysts"], cfg["depth"])
        remaining = counts["pending"] + counts["queued"] + counts["running"]
        return {**{k: bt[k] for k in ("id", "name", "created_at", "status", "budget_usd", "note")}, "config": cfg,
                "items": rows, "counts": counts, "spent_usd": round(spent, 4), "estimate_per_run_usd": round(per_run, 4),
                "estimate_remaining_usd": round(remaining * per_run, 4), "estimate_total_usd": round(len(rows) * per_run, 4)}
