"""Two threads asking for the same prices must not interleave rows in the cache file, and a damaged cache is refetched."""

import threading
import unittest
from unittest import mock

import pandas as pd

from deskapp import simulate


def _frame():
    idx = pd.to_datetime(["2025-04-17", "2025-04-21", "2025-04-22"])
    return pd.DataFrame({"Open": [1.0, 2.0, 3.0], "High": [1.5, 2.5, 3.5], "Low": [0.5, 1.5, 2.5], "Close": [1.2, 2.2, 3.2]}, index=idx)


class PriceCache(unittest.TestCase):
    def setUp(self):
        import tempfile, pathlib
        self.tmp = tempfile.TemporaryDirectory()
        self.patch = mock.patch.object(simulate, "PRICES_DIR", pathlib.Path(self.tmp.name))
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def test_concurrent_loads_leave_a_clean_file(self):
        calls = []

        class Slow:
            def __init__(self, t): pass
            def history(self, **k):
                calls.append(1)
                threading.Event().wait(0.05)
                return _frame()

        with mock.patch("yfinance.Ticker", Slow):
            out = []
            ts = [threading.Thread(target=lambda: out.append(simulate.load_bars("AAPL", "2025-01-01"))) for _ in range(6)]
            [t.start() for t in ts]; [t.join() for t in ts]
        self.assertEqual(len(out), 6)
        self.assertEqual(len(calls), 1, "one download, the other threads read the cache")
        files = list(simulate.PRICES_DIR.glob("AAPL_*.csv"))
        self.assertEqual(len(files), 1)
        self.assertTrue(all(len(line.split(",")) == 5 for line in files[0].read_text().splitlines()))

    def test_damaged_cache_is_refetched(self):
        with mock.patch("yfinance.Ticker") as T:
            T.return_value.history.return_value = _frame()
            simulate.load_bars("NVDA", "2025-01-01")
            f = next(simulate.PRICES_DIR.glob("NVDA_*.csv"))
            f.write_text(f.read_text() + "2025-04-23,1,2,3,4,5,6\n")
            bars = simulate.load_bars("NVDA", "2025-01-01")
            self.assertEqual(T.return_value.history.call_count, 2)
            self.assertEqual(len(bars.dates), 3)


if __name__ == "__main__":
    unittest.main()
