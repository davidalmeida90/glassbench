"""Each run reads its own engine config.

The engine keeps its data config in one process-wide dict and merges updates into it
(tradingagents/dataflows/config.py). Two runs in one process therefore share vendor routing, and a
tool_vendors key set by one run stays set for every later run. Desk runs two at a time and compares
variants, so that is a contaminated experiment: on 2026-09-19 the control arm of a matched pair was
served the treatment's data. Here the run's config travels in a context variable, the same way the
capture does, and the engine's get_config reads it first.
"""

from __future__ import annotations

import contextvars
import copy
import sys

CURRENT_CONFIG: "contextvars.ContextVar[dict | None]" = contextvars.ContextVar("desk_engine_config", default=None)


def install_run_config() -> int:
    """Point every engine module's get_config at the run's own config. Safe to call again."""
    from tradingagents.dataflows import config as engine_config_module

    original = engine_config_module.get_config
    if getattr(original, "_desk_run_config", False):
        return 0

    def get_config() -> dict:
        mine = CURRENT_CONFIG.get()
        return copy.deepcopy(mine) if mine is not None else original()

    get_config._desk_run_config = True
    rebound = 0
    # Modules that did `from .config import get_config` hold their own reference, so each is rebound.
    for module in list(sys.modules.values()):
        name = getattr(module, "__name__", "") or ""
        if name.startswith("tradingagents") and getattr(module, "get_config", None) is original:
            module.get_config = get_config
            rebound += 1
    return rebound
