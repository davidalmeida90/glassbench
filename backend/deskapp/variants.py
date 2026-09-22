"""Labelled framework variants, applied per run at runtime. The TradingAgents clone is never edited.

A variant changes one thing, so a run can be compared with the stock framework on the same
ticker and date. Every change a variant makes is written to the run's event log.

- prompt_pre1196: restores the manager wording from before commit a4acd8a (1 Sep 2026, issue
  #1196), which told the managers to be decisive and reserve Hold for genuinely balanced
  evidence. Swapped in the outgoing request, so only runs with this variant see it.
- pit_valuation: appends point-in-time valuation from SEC EDGAR to the fundamentals tool output
  on past-dated runs, where the engine withholds Yahoo's present-day profile.
- edgar_statements / edgar_valuation: a matched pair for the upstream contribution. Both read
  statements as filed; only the second also gets valuation as of the run date, from the engine's
  own sec_edgar vendor. Same cells, one difference, so the pair isolates what valuation adds.
"""

from __future__ import annotations

import logging
from datetime import date

from . import adapter
from .capture import CURRENT_CAPTURE

log = logging.getLogger("deskapp.variants")

VARIANTS = {
    "": {"label": "Stock", "detail": "TradingAgents as released"},
    "prompt_pre1196": {"label": "Decisive wording", "detail": "Manager prompts from before commit a4acd8a (reserve Hold for genuinely balanced evidence). Only for engines between a4acd8a and 62d3479; upstream fixed the Hold default in 62d3479 (v0.5.0), so newer engines refuse this variant."},
    "edgar_statements": {"label": "EDGAR statements", "detail": "Control of the valuation test: statements as they were filed (engine's sec_edgar vendor); the company profile stays withheld on past dates, as released"},
    "edgar_valuation": {"label": "EDGAR statements + valuation", "detail": "Treatment of the valuation test: statements as filed plus market cap and multiples as of the run date, served by the engine's sec_edgar vendor (fork branch desk/edgar-valuation)"},
    "pit_valuation": {"label": "+ EDGAR as filed", "detail": "Past dates only: statements as they were filed (engine's sec_edgar vendor, v0.5.0+) plus Desk's point-in-time valuation block from SEC filings"},
}

# (text in the current engine, text before commit a4acd8a). Checked against the engine at install.
PROMPT_SWAPS = [
    (
        "Commit to a directional stance only when the debate's strongest arguments clearly warrant one. Choose Hold when the evidence is balanced, materially conflicting, ambiguous, or insufficient to justify changing exposure; do not manufacture a direction merely to appear decisive. Weigh the bull and bear cases on their merits, independent of which side spoke first or last.",
        "Commit to a clear stance whenever the debate's strongest arguments warrant one; reserve Hold for situations where the evidence on both sides is genuinely balanced.",
    ),
    (
        "Ground every conclusion in specific evidence from the analysts. Commit to a directional call only when the evidence clearly supports one; choose Hold when the case is balanced, materially conflicting, ambiguous, or insufficient to justify changing exposure, rather than forcing a direction to appear decisive. Weigh the analysts on their merits, independent of speaking order.",
        "Be decisive and ground every conclusion in specific evidence from the analysts.",
    ),
    (
        "The investment recommendation. Exactly one of Buy / Overweight / Hold / Underweight / Sell. Choose Hold when the evidence is balanced, materially conflicting, ambiguous, or insufficient to justify changing exposure; otherwise commit to the side with the clearly stronger arguments. Do not pick a direction merely to be decisive.",
        "The investment recommendation. Exactly one of Buy / Overweight / Hold / Underweight / Sell. Reserve Hold for situations where the evidence on both sides is genuinely balanced; otherwise commit to the side with the stronger arguments.",
    ),
    (
        "The final position rating. Exactly one of Buy / Overweight / Hold / Underweight / Sell, picked based on the analysts' debate. Choose Hold when the case is balanced, materially conflicting, ambiguous, or insufficient to justify changing exposure, rather than forcing a direction to appear decisive.",
        "The final position rating. Exactly one of Buy / Overweight / Hold / Underweight / Sell, picked based on the analysts' debate.",
    ),
]

_installed = False
_prompt_check: str | None = None  # None when the engine text matches; otherwise why the variant is unavailable


def check_prompt_texts() -> str | None:
    """Confirm every current-engine text exists, so the swap can never silently do nothing."""
    import inspect

    from tradingagents.agents import schemas
    from tradingagents.agents.managers import portfolio_manager, research_manager

    sources = inspect.getsource(research_manager) + inspect.getsource(portfolio_manager)
    descriptions = [schemas.ResearchPlan.model_fields["recommendation"].description, schemas.PortfolioDecision.model_fields["rating"].description]
    missing = [new[:60] for new, _ in PROMPT_SWAPS[:2] if new not in sources]
    missing += [new[:60] for new, _ in PROMPT_SWAPS[2:] if new not in descriptions]
    return f"engine prompt text changed, variant unavailable: {missing}" if missing else None


def ensure_available(variant: str) -> None:
    if variant not in VARIANTS:
        raise ValueError(f"Unknown variant '{variant}'")
    if variant == "prompt_pre1196" and _prompt_check:
        raise RuntimeError(_prompt_check)
    if variant == "edgar_valuation" and not engine_serves_valuation():
        raise RuntimeError("this engine has no sec_edgar valuation vendor; check out the fork branch desk/edgar-valuation")


def engine_serves_valuation() -> bool:
    from tradingagents.dataflows import interface

    return "sec_edgar" in interface.VENDOR_METHODS["get_fundamentals"]


def _swap(value, counts: list[int]):
    if isinstance(value, str):
        for i, (new, old) in enumerate(PROMPT_SWAPS):
            if new in value:
                counts[i] += value.count(new)
                value = value.replace(new, old)
        return value
    if isinstance(value, list):
        return [_swap(v, counts) for v in value]
    if isinstance(value, dict):
        return {k: _swap(v, counts) for k, v in value.items()}
    return value


def install_variants() -> None:
    global _installed, _prompt_check
    if _installed:
        return
    from langchain_core.runnables.config import var_child_runnable_config
    from tradingagents.dataflows import interface
    from tradingagents.llm_clients.openai_client import DeepSeekChatOpenAI

    _prompt_check = check_prompt_texts()
    if _prompt_check:
        log.warning(_prompt_check)

    original_payload = DeepSeekChatOpenAI._get_request_payload

    def payload_with_variant(self, input_, *, stop=None, **kwargs):
        payload = original_payload(self, input_, stop=stop, **kwargs)
        capture = CURRENT_CAPTURE.get()
        if capture is None or getattr(capture, "variant", "") != "prompt_pre1196":
            return payload
        counts = [0] * len(PROMPT_SWAPS)
        payload = _swap(payload, counts)
        if any(counts):
            config = var_child_runnable_config.get() or {}
            agent_id, _ = adapter.NODE_MAP.get((config.get("metadata") or {}).get("langgraph_node"), (None, None))
            capture.bus.emit(capture.run_id, "variant.applied", agent_id, variant="prompt_pre1196", swaps=counts,
                             detail="Replaced current Hold wording with the pre-a4acd8a text in this request")
        return payload

    DeepSeekChatOpenAI._get_request_payload = payload_with_variant

    for vendor, fn in list(interface.VENDOR_METHODS["get_fundamentals"].items()):
        interface.VENDOR_METHODS["get_fundamentals"][vendor] = _with_valuation(fn, vendor)

    _installed = True


def _with_valuation(fn, vendor: str = ""):
    def get_fundamentals(ticker, curr_date=None, *args, **kwargs):
        out = fn(ticker, curr_date, *args, **kwargs)
        capture = CURRENT_CAPTURE.get()
        if capture is not None and getattr(capture, "variant", "") == "edgar_valuation" and vendor == "sec_edgar":
            cap_line = next((line for line in out.splitlines() if line.startswith("Market Cap")), "served")
            capture.bus.emit(capture.run_id, "variant.applied", "fundamentals", variant="edgar_valuation", chars=len(out),
                             detail=f"Engine sec_edgar valuation as of {curr_date}: {cap_line}")
            return out
        if capture is None or getattr(capture, "variant", "") != "pit_valuation" or not curr_date or curr_date >= date.today().isoformat():
            return out
        from .edgar import valuation_text

        block = valuation_text(ticker, curr_date)
        capture.bus.emit(capture.run_id, "variant.applied", "fundamentals", variant="pit_valuation", chars=len(block),
                         detail=block.splitlines()[0])
        return f"{out}\n\n{block}"

    get_fundamentals.__name__ = getattr(fn, "__name__", "get_fundamentals")
    get_fundamentals.__doc__ = fn.__doc__
    return get_fundamentals
