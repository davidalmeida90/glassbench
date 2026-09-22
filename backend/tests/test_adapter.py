"""Run after every `git pull` of TradingAgents:  ..\\.venv\\Scripts\\python.exe -m unittest discover tests

Fails loudly if the engine renamed a node, a state key or the decision markdown Desk parses.
"""

import unittest

from deskapp import adapter


class AdapterMatchesEngine(unittest.TestCase):
    def test_node_names(self):
        from tradingagents.graph.analyst_execution import ANALYST_NODE_SPECS
        from tradingagents.graph.setup import DEBATE_PATH_MAP, RISK_ANALYSIS_PATH_MAP

        specs = ANALYST_NODE_SPECS.values()
        engine = (
            set(DEBATE_PATH_MAP) | set(RISK_ANALYSIS_PATH_MAP) | {"Trader"}
            | {s.agent_node for s in specs} | {s.tool_node for s in specs} | {s.clear_node for s in specs}
        )
        self.assertEqual(engine, set(adapter.NODE_MAP), "Engine node names changed: update adapter.AGENTS")

    def test_analyst_keys(self):
        from tradingagents.graph.analyst_execution import ANALYST_NODE_SPECS

        self.assertEqual(set(ANALYST_NODE_SPECS), {a["analyst_key"] for a in adapter.AGENTS if a["stage"] == "analysts"})

    def test_state_keys(self):
        from tradingagents.graph.propagation import Propagator

        state = Propagator().create_initial_state("SPY", "2026-09-13")
        for agent in adapter.AGENTS:
            root = agent["text"][0]
            if root in ("investment_plan", "trader_investment_plan", "final_trade_decision"):
                continue  # written by the engine later, not present in the initial state
            self.assertIn(root, state, f"{agent['id']}: state key '{root}' missing")
            if len(agent["text"]) > 1:
                self.assertIn(agent["text"][1], state[root], f"{agent['id']}: nested key missing")

    def test_decision_markdown(self):
        from tradingagents.agents.schemas import (
            PortfolioDecision, PortfolioRating, ResearchPlan, TraderAction, TraderProposal,
            render_pm_decision, render_research_plan, render_trader_proposal,
        )

        rm = adapter.parse_research_plan(render_research_plan(ResearchPlan(
            recommendation=PortfolioRating.HOLD, rationale="Both sides overreach.", strategic_actions="Keep size.")))
        self.assertEqual(rm["recommendation"], "Hold")
        self.assertEqual(rm["rationale"], "Both sides overreach.")

        tr = adapter.parse_trader_plan(render_trader_proposal(TraderProposal(
            action=TraderAction.HOLD, reasoning="Split tape.", entry_price=766.88, stop_loss=757.5, position_sizing="neutral")))
        self.assertEqual((tr["action"], tr["entry_price"], tr["stop_loss"]), ("Hold", 766.88, 757.5))

        pm = adapter.parse_pm_decision(render_pm_decision(PortfolioDecision(
            rating=PortfolioRating.OVERWEIGHT, executive_summary="Add slowly.", investment_thesis="Trend intact.",
            price_target=230.0, time_horizon="1-3 months")))
        self.assertEqual((pm["rating"], pm["price_target"], pm["time_horizon"]), ("Overweight", 230.0, "1-3 months"))


if __name__ == "__main__":
    unittest.main()
