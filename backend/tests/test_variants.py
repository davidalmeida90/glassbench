"""Variants must change exactly what they claim, and EDGAR data must respect filing dates. No network."""

import unittest

from deskapp import edgar
from deskapp.variants import PROMPT_SWAPS, _swap, check_prompt_texts


class PromptVariant(unittest.TestCase):
    def test_old_wording_variant_tracks_the_engine(self):
        """Available only while the engine still carries the a4acd8a wording; refused after upstream's 62d3479 fix."""
        import inspect

        from tradingagents.agents.managers import research_manager

        from deskapp import variants

        fixed_upstream = "conflict alone is not a reason to Hold" in inspect.getsource(research_manager)
        problem = check_prompt_texts()
        if fixed_upstream:
            self.assertIsNotNone(problem)
            variants._prompt_check = problem
            with self.assertRaises(RuntimeError):
                variants.ensure_available("prompt_pre1196")
            variants.ensure_available("pit_valuation")
        else:
            self.assertIsNone(problem)

    def test_swap_reaches_nested_payload_and_counts(self):
        new_rm, old_rm = PROMPT_SWAPS[0]
        new_schema, old_schema = PROMPT_SWAPS[3]
        payload = {"messages": [{"role": "user", "content": f"intro {new_rm} outro"}],
                   "tools": [{"function": {"parameters": {"properties": {"rating": {"description": new_schema}}}}}]}
        counts = [0] * len(PROMPT_SWAPS)
        out = _swap(payload, counts)
        self.assertEqual(out["messages"][0]["content"], f"intro {old_rm} outro")
        self.assertEqual(out["tools"][0]["function"]["parameters"]["properties"]["rating"]["description"], old_schema)
        self.assertEqual(counts, [1, 0, 0, 1])
        self.assertIn(new_rm, payload["messages"][0]["content"])  # original payload untouched


class ValuationPair(unittest.TestCase):
    """Control and treatment differ in exactly one routed tool."""

    def test_only_the_treatment_routes_fundamentals_to_edgar(self):
        from deskapp.settings import engine_config

        control = engine_config(1, "deepseek-v4-pro", "deepseek-v4-flash", variant="edgar_statements")["tool_vendors"]
        treatment = engine_config(1, "deepseek-v4-pro", "deepseek-v4-flash", variant="edgar_valuation")["tool_vendors"]
        self.assertNotIn("get_fundamentals", control)
        self.assertEqual(treatment["get_fundamentals"], "sec_edgar,yfinance")
        self.assertEqual({k: v for k, v in treatment.items() if k != "get_fundamentals"}, control)

    def test_treatment_needs_an_engine_that_serves_valuation(self):
        from deskapp import variants

        if variants.engine_serves_valuation():
            variants.ensure_available("edgar_valuation")
        else:
            with self.assertRaises(RuntimeError):
                variants.ensure_available("edgar_valuation")
        variants.ensure_available("edgar_statements")


def fact(val, end, filed, start=None, form="10-Q"):
    row = {"val": val, "end": end, "filed": filed, "form": form}
    if start:
        row["start"] = start
    return row


FACTS = {"facts": {"us-gaap": {
    "NetIncomeLoss": {"units": {"USD": [
        fact(100, "2024-12-31", "2025-02-01", "2024-01-01", "10-K"),   # FY2024
        fact(30, "2024-06-30", "2024-08-01", "2024-01-01"),            # 6M 2024
        fact(40, "2025-06-30", "2025-08-01", "2025-01-01"),            # 6M 2025
        fact(50, "2025-12-31", "2026-02-01", "2025-01-01", "10-K"),    # FY2025, filed later
    ]}},
    "OldRevenueTag": {"units": {"USD": [fact(5, "2019-12-31", "2020-02-01", "2019-01-01", "10-K")]}},
    "Revenues": {"units": {"USD": [fact(900, "2024-12-31", "2025-02-01", "2024-01-01", "10-K")]}},
}}}


class EdgarPointInTime(unittest.TestCase):
    def test_ttm_uses_only_filings_before_the_date(self):
        ttm = edgar._ttm(FACTS, ["NetIncomeLoss"], "2025-09-15")
        self.assertEqual(ttm["value"], 100 + 40 - 30)  # FY2024 + 6M 2025 - 6M 2024
        self.assertEqual(ttm["end"], "2025-06-30")
        later = edgar._ttm(FACTS, ["NetIncomeLoss"], "2026-03-01")
        self.assertEqual((later["value"], later["method"]), (50, "fiscal year"))

    def test_filing_on_the_decision_date_is_excluded(self):
        ttm = edgar._ttm(FACTS, ["NetIncomeLoss"], "2025-08-01")
        self.assertEqual(ttm["value"], 100)  # the 6M 2025 filing arrives that day: not yet usable

    def test_most_recent_tag_wins_over_stale_tag(self):
        concept, rows = edgar._facts(FACTS, ["OldRevenueTag", "Revenues"], "2025-09-15")
        self.assertEqual(concept, "Revenues")


if __name__ == "__main__":
    unittest.main()
