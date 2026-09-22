"""Two runs in one process must not share vendor routing. No network."""

import threading
import unittest

from deskapp.runconfig import CURRENT_CONFIG, install_run_config
from deskapp.settings import engine_config


class RunConfigIsolation(unittest.TestCase):
    def test_concurrent_runs_each_see_their_own_vendors(self):
        from tradingagents.dataflows import interface
        from tradingagents.dataflows.config import set_config

        install_run_config()
        seen, barrier = {}, threading.Barrier(2)

        def run(variant):
            config = engine_config(1, "deepseek-v4-pro", "deepseek-v4-flash", variant=variant)
            CURRENT_CONFIG.set(config)
            set_config(config)          # what TradingAgentsGraph does: merges into the process-wide dict
            barrier.wait(timeout=10)    # both configs are now set, the last writer won globally
            seen[variant] = interface.get_vendor("fundamental_data", "get_fundamentals")

        threads = [threading.Thread(target=run, args=(v,)) for v in ("edgar_statements", "edgar_valuation")]
        [t.start() for t in threads]
        [t.join() for t in threads]
        self.assertEqual(seen["edgar_valuation"], "sec_edgar,yfinance")
        self.assertEqual(seen["edgar_statements"], "yfinance")

    def test_a_stock_run_after_a_variant_run_is_stock_again(self):
        from tradingagents.dataflows import interface
        from tradingagents.dataflows.config import set_config

        install_run_config()
        for variant, expected in (("edgar_valuation", "sec_edgar,yfinance"), ("", "yfinance")):
            config = engine_config(1, "deepseek-v4-pro", "deepseek-v4-flash", variant=variant)
            token = CURRENT_CONFIG.set(config)
            set_config(config)
            try:
                self.assertEqual(interface.get_vendor("fundamental_data", "get_balance_sheet" if variant else "get_fundamentals"),
                                 expected)
                self.assertEqual(interface.get_vendor("fundamental_data", "get_fundamentals"), expected)
            finally:
                CURRENT_CONFIG.reset(token)


if __name__ == "__main__":
    unittest.main()
