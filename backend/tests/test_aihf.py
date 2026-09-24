"""AI Hedge Fund engine: rating mapping, decision summary, and one full run through the real driver on fixtures."""

from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from deskapp import aihf, events
from deskapp.events import EventBus
from deskapp.store import Store


def _assessment(as_of, conviction, weight):
    return {
        "as_of": as_of,
        "strategies": [{
            "name": "deep-value", "slice": 1.0, "convictions": {"AAPL": conviction}, "weights": {"AAPL": weight},
            "flat_reason": None if weight else "no_eligible_positions",
            "signals": [
                {"model_name": "graham", "ticker": "AAPL", "value": conviction, "metadata": {"signal": "bullish", "confidence": 80}},
                {"model_name": "buffett", "ticker": "AAPL", "value": 0.0, "metadata": {"abstained": True}},
            ],
        }],
        "target_weights": {"AAPL": weight}, "final_weights": {"AAPL": weight}, "clamps": [],
    }


class RatingTest(unittest.TestCase):
    def test_conviction_bands(self):
        cases = [(0.9, "Buy"), (0.5, "Buy"), (0.49, "Overweight"), (0.15, "Overweight"), (0.149, "Hold"), (0.0, "Hold"),
                 (-0.149, "Hold"), (-0.15, "Underweight"), (-0.49, "Underweight"), (-0.5, "Sell"), (-1.0, "Sell")]
        for conviction, rating in cases:
            with self.subTest(conviction=conviction):
                self.assertEqual(aihf.conviction_to_rating(conviction), rating)


class SummaryTest(unittest.TestCase):
    def test_rates_the_run_date_and_shows_a_later_refresh(self):
        record = {
            **_assessment("2026-09-13", 0.1, 0.0),  # the refreshed view the order used
            "original_assessment": _assessment("2026-09-11", 0.6, 0.25),
            "refreshed_assessment": _assessment("2026-09-13", 0.1, 0.0),
            "execution_as_of": "2026-09-14", "orders": [], "fills": [], "nav": 100000.0, "cash": 100000.0,
        }
        rating, decision = aihf.summarize(record, executed=True, ticker="AAPL")
        self.assertEqual(rating, "Buy")  # 0.6 as of the run date, not the refreshed 0.1
        self.assertEqual((decision["stance"], decision["final_weight"]), ("Long", 0.25))
        self.assertEqual(decision["execution"]["refreshed_as_of"], "2026-09-13")
        self.assertEqual(decision["execution"]["executed_weight"], 0.0)
        self.assertEqual([s["abstained"] for s in decision["signals"]], [False, True])

    def test_most_analysts_abstaining_is_review_not_hold(self):
        record = _assessment("2026-05-13", 0.0, 0.0)
        signals = record["strategies"][0]["signals"]
        signals.append({"model_name": "munger", "ticker": "AAPL", "value": 0.0, "metadata": {"abstained": True}})
        signals[0]["metadata"] = {"abstained": True}  # three of three abstain here; two of three below
        rating, _ = aihf.summarize({"proposal": record, "reason": "x"}, executed=False, ticker="AAPL")
        self.assertEqual(rating, "REVIEW")
        signals[0]["metadata"] = {"signal": "neutral", "confidence": 50}
        rating, decision = aihf.summarize({"proposal": record, "reason": "x"}, executed=False, ticker="AAPL")
        self.assertEqual((rating, decision["abstained"]), ("REVIEW", 2))

    def test_pending_proposal_with_every_analyst_abstaining(self):
        proposal = _assessment("2026-09-23", 0.0, 0.0)
        for sig in proposal["strategies"][0]["signals"]:
            sig["metadata"] = {"abstained": True}
        rating, decision = aihf.summarize({"proposal": proposal, "reason": "no later session"}, executed=False, ticker="AAPL")
        self.assertEqual(rating, "REVIEW")
        self.assertEqual(decision["status"], "pending")
        self.assertEqual(decision["execution"]["pending"], "no later session")


@unittest.skipUnless(aihf.installed(), "AI Hedge Fund clone not installed")
class FullRunTest(unittest.TestCase):
    """The real driver in its own venv, on canned data and answers: no network, no key, no cost."""

    def test_full_run_on_fixtures(self):
        from deskapp.runner import RunManager

        # Windows keeps a file locked while SQLite holds it open, hence the explicit close below.
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            runs_dir = Path(tmp) / "runs"
            private_dir = Path(tmp) / "private"
            with mock.patch.object(events, "RUNS_DIR", runs_dir), mock.patch.object(aihf, "RUNS_DIR", runs_dir), \
                    mock.patch.object(aihf, "AIHF_PRIVATE_DIR", private_dir):
                store = Store(Path(tmp) / "desk.db")
                manager = RunManager(store, EventBus(store), workers=1)
                manager.aihf_fixture = True
                try:
                    run_id = manager.submit_aihf("AAPL", "2026-09-11", "deep-value", None, "deepseek-flash")
                    deadline = time.time() + 180
                    while store.get_run(run_id)["status"] in ("queued", "running") and time.time() < deadline:
                        time.sleep(0.5)
                    run = store.get_run(run_id)
                    self.assertEqual(run["status"], "finished", run.get("error"))
                    self.assertEqual((run["engine"], run["variant"]), ("ai_hedge_fund", "deep-value"))
                    self.assertEqual(run["analysts"], ["graham", "buffett", "munger"])
                    # Fixture answers: graham -0.6 at double weight, buffett +0.7, munger 0, so the blend is -0.125
                    self.assertEqual(run["rating"], "Hold")
                    self.assertAlmostEqual(run["decision"]["conviction"], -0.125)
                    self.assertEqual(run["decision"]["stance"], "Flat")
                    self.assertEqual(run["llm_calls"], 3)
                    self.assertGreater(run["tool_calls"], 0)
                    evs = store.events_since(run_id)
                    kinds = {(e["type"], e["agent"]) for e in evs}
                    for agent in ("graham", "buffett", "munger", "blend", "risk", "execution"):
                        self.assertIn(("agent.finished", agent), kinds)
                    self.assertIn(("engine.started", None), kinds)
                    self.assertIn(("run.finished", None), kinds)
                    self.assertEqual(evs[0]["type"], "run.queued")
                    self.assertEqual([a["id"] for a in evs[0]["payload"]["agent_meta"]][-3:], ["blend", "risk", "execution"])
                    self.assertTrue((runs_dir / run_id / "record.json").exists())
                    # Raw vendor data and prompts live in the private folder, never in the published run folder
                    self.assertFalse((runs_dir / run_id / "prompts").exists())
                    self.assertFalse((runs_dir / run_id / "tool_outputs").exists())
                    self.assertTrue((private_dir / run_id / "prompts").is_dir())
                    saved = list((private_dir / run_id / "tool_outputs").glob("*.json"))
                    self.assertTrue(any(p.name.startswith("financial_metrics_AAPL") for p in saved), saved)
                    self.assertTrue(any(p.name.startswith("prices_SPY") for p in saved), saved)  # outside any lane, kept too
                    # The event log holds counts and dates, never the vendor's values (fixture ROE 0.25, gross margin 0.45)
                    previews = [e["payload"].get("preview", "") for e in evs if e["type"] == "tool.result"]
                    self.assertTrue(previews and all("fields per row" in p or "no " in p for p in previews), previews)
                    self.assertFalse(any("0.25" in p or "0.45" in p for p in previews), previews)
                    files = [e["payload"].get("file") for e in evs if e["type"] == "tool.result"]
                    self.assertTrue(all(f and f.startswith("private/tool_outputs/") for f in files), files)
                finally:
                    manager.pool.shutdown(wait=True)
                    store._conn.close()


if __name__ == "__main__":
    unittest.main()
