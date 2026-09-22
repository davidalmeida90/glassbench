"""Simulator rules on hand-built price bars, checked by hand. No network, no LLM."""

import unittest

import numpy as np

from deskapp.simulate import Bars, Decision, combine, metrics, placebo, run_ticker, simulate


def bars(rows):
    """rows: (date, open, high, low, close)"""
    return Bars([r[0] for r in rows], *(np.array([r[i] for r in rows], float) for i in range(1, 5)))


FLAT_UP = bars([
    ("2026-01-01", 100, 100, 100, 100),
    ("2026-01-02", 110, 112, 108, 110),
    ("2026-01-05", 110, 121, 110, 121),
    ("2026-01-06", 121, 121, 121, 121),
])


class RatingRules(unittest.TestCase):
    def test_buy_fills_next_open_with_cost(self):
        res = simulate(FLAT_UP, [Decision("2026-01-01", "Buy")], cost_bps=10)
        trade = res["trades"][0]
        self.assertEqual((trade["date"], trade["price"]), ("2026-01-02", 110.0))  # not the decision day's close
        self.assertAlmostEqual(trade["cost"], 0.1)  # 10 bps of $100
        # bought 100/110 shares at 110, paid 0.10: equity at 121 = (100/110)*121 - 0.10
        self.assertAlmostEqual(res["equity"][-1], 100 / 110 * 121 - 0.1, places=9)
        self.assertEqual(res["equity"][0], 100.0)  # the gap from 100 to 110 is missed, as it should be

    def test_hold_keeps_flat_position(self):
        res = simulate(FLAT_UP, [Decision("2026-01-01", "Hold")], cost_bps=10)
        self.assertEqual(res["trades"], [])
        self.assertEqual(res["equity"], [100.0] * 4)

    def test_failed_run_keeps_position_and_is_not_a_hold(self):
        res = simulate(FLAT_UP, [Decision("2026-01-01", "Buy"), Decision("2026-01-02", None, status="failed")], cost_bps=0)
        self.assertEqual(len(res["trades"]), 1)
        self.assertAlmostEqual(res["weights"][-1], 1.0)

    def test_overweight_is_half_and_sell_goes_flat(self):
        res = simulate(FLAT_UP, [Decision("2026-01-01", "Overweight"), Decision("2026-01-02", "Sell")], cost_bps=0)
        self.assertAlmostEqual(res["trades"][0]["weight_after"], 0.5)
        self.assertEqual(res["trades"][1]["side"], "sell")
        self.assertEqual(res["trades"][1]["date"], "2026-01-05")
        self.assertEqual(res["weights"][-1], 0.0)

    def test_hold_half_and_start_invested_variants(self):
        half = simulate(FLAT_UP, [Decision("2026-01-01", "Hold")], cost_bps=0, hold_rule="half")
        self.assertAlmostEqual(half["trades"][0]["weight_after"], 0.5)
        invested = simulate(FLAT_UP, [Decision("2026-01-01", "Hold")], cost_bps=0, start_weight=1.0)
        self.assertAlmostEqual(invested["equity"][-1], 121.0)

    def test_decision_without_next_bar_does_not_trade(self):
        res = simulate(FLAT_UP, [Decision("2026-01-06", "Buy")], cost_bps=0)
        self.assertEqual(res["trades"], [])


class LevelRules(unittest.TestCase):
    def test_pullback_limit_entry_then_stop_not_on_entry_bar(self):
        b = bars([
            ("2026-01-01", 100, 100, 100, 100),
            ("2026-01-02", 99, 99, 90, 92),   # limit 95 fills at 95; low 90 is below the stop but it is the entry bar
            ("2026-01-05", 92, 93, 88, 89),   # stop 91 fills at 91 (open 92 above the stop)
            ("2026-01-06", 89, 89, 89, 89),
        ])
        res = simulate(b, [Decision("2026-01-01", "Hold", entry=95, stop=91)], cost_bps=0, mode="levels", trigger="touch")
        self.assertEqual([(t["date"], t["side"], t["price"]) for t in res["trades"]],
                         [("2026-01-02", "buy", 95.0), ("2026-01-05", "sell", 91.0)])
        self.assertAlmostEqual(res["trades"][0]["weight_after"], 0.5)
        self.assertAlmostEqual(res["equity"][-1], 100 - 50 / 95 * 4)

    def test_confirmation_stop_entry_and_gapped_stop(self):
        b = bars([
            ("2026-01-01", 100, 100, 100, 100),
            ("2026-01-02", 101, 106, 101, 105),  # buy stop 104 fills at 104
            ("2026-01-05", 97, 98, 96, 97),      # gap below the stop 99: fills at the open, 97
        ])
        res = simulate(b, [Decision("2026-01-01", "Hold", entry=104, stop=99)], cost_bps=0, mode="levels", trigger="touch")
        self.assertEqual([(t["side"], t["price"]) for t in res["trades"]], [("buy", 104.0), ("sell", 97.0)])
        self.assertIn("gapped", res["trades"][1]["reason"])

    def test_close_trigger_confirmation_and_stop_fill_next_open(self):
        b = bars([
            ("2026-01-01", 100, 100, 100, 100),
            ("2026-01-02", 101, 106, 101, 103),  # high 106 touches 104 but closes below it: no entry
            ("2026-01-05", 103, 106, 103, 105),  # close 105 above 104: entry confirmed
            ("2026-01-06", 106, 107, 98, 100),   # buys at the open 106; low 98 pierces the stop but closes above it
            ("2026-01-07", 100, 100, 97, 98),    # close 98 at or below 99: stop confirmed
            ("2026-01-08", 97, 99, 96, 97),      # sells at the open 97
        ])
        res = simulate(b, [Decision("2026-01-01", "Hold", entry=104, stop=99)], cost_bps=0, mode="levels")
        self.assertEqual([(t["date"], t["side"], t["price"]) for t in res["trades"]],
                         [("2026-01-06", "buy", 106.0), ("2026-01-08", "sell", 97.0)])
        self.assertIn("close 105.00 above 104.00", res["trades"][0]["reason"])

    def test_new_decision_cancels_pending_close_trigger(self):
        b = bars([
            ("2026-01-01", 100, 100, 100, 100),
            ("2026-01-02", 100, 106, 100, 105),  # confirmation on the close
            ("2026-01-05", 105, 105, 105, 105),  # a Sell decision fills today and replaces the plan
        ])
        res = simulate(b, [Decision("2026-01-01", "Hold", entry=104), Decision("2026-01-02", "Sell")], cost_bps=0, mode="levels")
        self.assertEqual(res["trades"], [])

    def test_orders_expire_when_next_decision_fills(self):
        b = bars([
            ("2026-01-01", 100, 100, 100, 100),
            ("2026-01-02", 100, 101, 99, 100),
            ("2026-01-05", 100, 101, 80, 85),  # would hit the old limit 95, but the Sell decision replaced it
        ])
        res = simulate(b, [Decision("2026-01-01", "Hold", entry=95), Decision("2026-01-02", "Sell")], cost_bps=0, mode="levels")
        self.assertEqual(res["trades"], [])

    def test_implausible_levels_are_ignored(self):
        res = simulate(FLAT_UP, [Decision("2026-01-01", "Hold", entry=10, stop=500)], cost_bps=0, mode="levels")
        self.assertEqual(res["trades"], [])


class ExposurePeriods(unittest.TestCase):
    def test_periods_split_at_trades_with_reasons_and_missed_gains(self):
        from deskapp.simulate import exposure_periods

        b = bars([
            ("2026-01-01", 100, 100, 100, 100),
            ("2026-01-02", 100, 100, 100, 100),
            ("2026-01-05", 110, 121, 110, 121),   # in cash: the stock rose 100 -> 110 at the next trade's fill
            ("2026-01-06", 121, 121, 121, 132),
        ])
        res = simulate(b, [Decision("2026-01-01", "Hold", "r1"), Decision("2026-01-02", "Buy", "r2")], cost_bps=0)
        periods = exposure_periods(b, 0, res)
        self.assertEqual([(p["start"], p["end"], p["weight"], p["verdict"]) for p in periods],
                         [("2026-01-01", "2026-01-05", 0.0, "missed gain"), ("2026-01-05", "2026-01-06", 1.0, "held")])
        self.assertAlmostEqual(periods[0]["stock_return"], 0.10)
        self.assertEqual(periods[1]["opened_by"]["reasons"], ["rating Buy"])
        self.assertEqual((periods[1]["opened_by"]["n"], periods[1]["opened_by"]["run_id"], res["trades"][0]["n"]), (1, "r2", 1))
        self.assertTrue(periods[1]["ongoing"])
        self.assertAlmostEqual(periods[1]["stock_return"], 132 / 110 - 1)


class Evaluation(unittest.TestCase):
    def test_metrics_drawdown_and_return(self):
        m = metrics([100, 120, 90, 110], [0, 1, 1, 1], [])
        self.assertAlmostEqual(m["total_return"], 0.10)
        self.assertAlmostEqual(m["max_drawdown"], -0.25)
        self.assertEqual(m["days"], 3)

    def test_placebo_enumerates_distinct_orderings(self):
        decisions = [Decision("2026-01-01", "Buy"), Decision("2026-01-02", "Hold"), Decision("2026-01-05", "Hold")]
        pb = placebo(FLAT_UP, decisions, cost_bps=0)
        self.assertTrue(pb["exhaustive"])
        self.assertEqual(pb["sims"], 3)  # Buy can sit on any of the 3 dates

    def test_run_ticker_and_combine_without_network(self):
        decisions = [Decision("2026-01-01", "Buy", "r1"), Decision("2026-01-05", "Hold", "r2")]
        one = run_ticker("AAA", decisions, 0, bars=FLAT_UP)
        two = run_ticker("BBB", decisions, 0, bars=FLAT_UP)
        self.assertEqual([s["key"] for s in one["strategies"]], ["agents_levels", "agents_rating", "buy_hold"])  # MA needs 200 days
        self.assertAlmostEqual(one["decisions"][0]["forward_return"], 0.21)
        both = combine([one, two])
        rating = next(s for s in both["strategies"] if s["key"] == "agents_rating")
        self.assertAlmostEqual(rating["equity"][-1], 110.0)


if __name__ == "__main__":
    unittest.main()
