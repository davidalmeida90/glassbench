"""Read DeepSeek's streamed reasoning text as it arrives.

langchain-openai drops `delta.reasoning_content` from streamed chunks, so a thinking
model looks silent for 20 to 40 seconds before its first visible word. This tap reads
that field from the raw chunk and forwards it to the run's capture. The chunk passed on
to LangChain is untouched, so engine behaviour does not change. No engine files are edited.
"""

from __future__ import annotations

import logging

from . import adapter
from .capture import CURRENT_CAPTURE

log = logging.getLogger("deskapp.reasoning")
_installed = False


def install_reasoning_tap() -> None:
    global _installed
    if _installed:
        return
    try:
        from langchain_core.runnables.config import var_child_runnable_config
        from tradingagents.llm_clients.openai_client import DeepSeekChatOpenAI
    except ImportError as exc:  # engine layout changed; run without reasoning text
        log.warning("reasoning tap not installed: %s", exc)
        return

    original = DeepSeekChatOpenAI._convert_chunk_to_generation_chunk

    def tapped(self, chunk, default_chunk_class, base_generation_info):
        try:
            capture = CURRENT_CAPTURE.get()
            if capture is not None and isinstance(chunk, dict):
                choices = chunk.get("choices") or chunk.get("chunk", {}).get("choices") or []
                text = (choices[0].get("delta") or {}).get("reasoning_content") if choices else None
                if text:
                    config = var_child_runnable_config.get() or {}
                    node = (config.get("metadata") or {}).get("langgraph_node")
                    agent_id, kind = adapter.NODE_MAP.get(node, (None, None))
                    if agent_id and kind == "agent":
                        capture.add_reasoning(agent_id, text)
        except Exception:  # never let observation break a run
            pass
        return original(self, chunk, default_chunk_class, base_generation_info)

    DeepSeekChatOpenAI._convert_chunk_to_generation_chunk = tapped
    _installed = True
