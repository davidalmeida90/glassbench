"""Backtest batch rules, checked with a fake runner: no LLM calls, no cost."""

import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from deskapp import backtest as bt_module
from deskapp.backtest import BacktestManager, sample_evenly
from deskapp.store import Store


class FakeRuns:
    """Stands in for RunManager: each submitted run finishes at once with a fixed cost and outcome."""

    def __init__(self, store: Store, cost: float = 0.04, outcomes: list[str] | None = None):
        self.store, self.cost, self.outcomes = store, cost, list(outcomes or [])
        self.pool = ThreadPoolExecutor(max_workers=2)
        self.submitted: list[tuple[str, str]] = []

    def submit(self, ticker, trade_date, analysts, depth, deep_model, quick_model, purpose="live", backtest_id=None, memory="shared", variant=""):
        run_id = f"run-{len(self.submitted)}-{ticker}-{trade_date}"
        status = self.outcomes.pop(0) if self.outcomes else "finished"
        self.store.create_run({
            "id": run_id, "ticker": ticker, "trade_date": trade_date, "analysts": analysts, "depth": depth,
            "deep_model": deep_model, "quick_model": quick_model, "status": status, "created_at": time.time(),
            "started_at": time.time(), "finished_at": time.time(), "cost_usd": self.cost, "rating": "Hold",
            "engine_version": "test", "purpose": purpose, "backtest_id": backtest_id, "memory": memory, "variant": variant,
        })
        self.submitted.append((ticker, trade_date))
        return run_id

    def cancel(self, run_id):
        return True


class BacktestRules(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / "desk.db")
        self._version = bt_module.engine_version
        bt_module.engine_version = lambda: "test"

    def tearDown(self):
        bt_module.engine_version = self._version
        self.store._conn.close()
        self.tmp.cleanup()

    def run_batch(self, runs, dates, budget, tickers=("AAPL", "NVDA")):
        manager = BacktestManager(self.store, runs)
        manager.estimate_per_run = lambda analysts, depth: 0.04
        bt = manager.create("t", list(tickers), dates, ["fundamentals", "market"], 1, "deep", "quick", budget)
        manager._stop[bt["id"]] = __import__("threading").Event()
        manager._loop(bt["id"])
        return manager.detail(bt["id"])

    def test_sample_keeps_first_and_last(self):
        grid = [f"d{i:02d}" for i in range(53)]
        picked = sample_evenly(grid, 4)
        self.assertEqual(len(picked), 4)
        self.assertEqual((picked[0], picked[-1]), ("d00", "d52"))
        self.assertEqual(sample_evenly(grid[:3], 10), grid[:3])

    def test_runs_all_items_in_date_order_and_tags_them(self):
        runs = FakeRuns(self.store)
        detail = self.run_batch(runs, ["2026-01-09", "2025-09-12"], budget=1.0)
        self.assertEqual(detail["status"], "finished")
        self.assertEqual(runs.submitted, [("AAPL", "2025-09-12"), ("NVDA", "2025-09-12"), ("AAPL", "2026-01-09"), ("NVDA", "2026-01-09")])
        stored = self.store.list_runs()
        self.assertTrue(all(r["purpose"] == "backtest" and r["memory"] == "off" and r["backtest_id"] == detail["id"] for r in stored))
        self.assertAlmostEqual(detail["spent_usd"], 0.16)

    def test_budget_cap_stops_before_overspending(self):
        runs = FakeRuns(self.store)
        detail = self.run_batch(runs, ["2025-09-12", "2026-01-09"], budget=0.10)  # room for 2 runs at $0.04
        self.assertEqual(len(runs.submitted), 2)
        self.assertEqual(detail["status"], "paused")
        self.assertIn("Budget cap", detail["note"])
        self.assertLessEqual(detail["spent_usd"], 0.10)

    def test_finished_runs_are_reused_not_paid_twice(self):
        first = FakeRuns(self.store)
        self.run_batch(first, ["2025-09-12"], budget=1.0)
        second = FakeRuns(self.store)
        detail = self.run_batch(second, ["2025-09-12", "2026-01-09"], budget=1.0)
        self.assertEqual(second.submitted, [("AAPL", "2026-01-09"), ("NVDA", "2026-01-09")])
        self.assertEqual(sum(1 for it in detail["items"] if it["reused"]), 2)
        self.assertAlmostEqual(detail["spent_usd"], 0.08)  # reused runs cost this backtest nothing

    def test_failed_run_retried_once_then_left_failed(self):
        runs = FakeRuns(self.store, outcomes=["failed", "failed"])
        detail = self.run_batch(runs, ["2025-09-12"], budget=1.0, tickers=("AAPL",))
        self.assertEqual(len(runs.submitted), 2)
        self.assertEqual(detail["items"][0]["status"], "failed")
        self.assertEqual(detail["items"][0]["attempts"], 2)
        self.assertIsNone(detail["items"][0]["rating"])


if __name__ == "__main__":
    unittest.main()
