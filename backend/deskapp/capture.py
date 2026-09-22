"""Turns LangChain/LangGraph callbacks and engine log warnings into Desk events."""

from __future__ import annotations

import contextvars
import logging
import threading
import time
from pathlib import Path
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler

from . import adapter
from .events import EventBus
from .settings import estimate_cost

PREVIEW_CHARS = 700
DELTA_FLUSH_SECONDS = 0.25


def _text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return str(content or "")


class RunCapture(BaseCallbackHandler):
    """One per run. Attributes every callback to an agent via the LangGraph node name."""

    raise_error = False

    def __init__(self, bus: EventBus, run_id: str, run_dir: Path):
        super().__init__()
        self.bus = bus
        self.run_id = run_id
        self.tool_dir = run_dir / "tool_outputs"
        self._lock = threading.Lock()
        self._nodes: dict[Any, dict] = {}  # chain run_id -> {agent, kind, start}
        self._llm: dict[Any, dict] = {}
        self._tools: dict[Any, dict] = {}
        self._visits: dict[str, int] = {}
        self._buffers: dict[tuple[str, str], list[str]] = {}
        self._last_flush = time.monotonic()
        self.current_agent: str | None = None
        self.variant = ""
        self.models_served: set[str] = set()
        self.totals = {"tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0, "llm_calls": 0, "tool_calls": 0, "flags": 0}

    # nodes -------------------------------------------------------------------
    def on_chain_start(self, serialized, inputs, *, run_id, parent_run_id=None, metadata=None, **kwargs):
        name = kwargs.get("name")
        node = (metadata or {}).get("langgraph_node")
        if not name or name != node or name not in adapter.NODE_MAP:
            return
        agent, kind = adapter.NODE_MAP[name]
        if kind == "clear":
            return
        visit = 0
        with self._lock:
            self._nodes[run_id] = {"agent": agent, "kind": kind, "start": time.time()}
            if kind == "agent":
                self._visits[agent] = self._visits.get(agent, 0) + 1
                visit = self._visits[agent]
        if kind == "agent":
            self.current_agent = agent
            self.flush()
            self.bus.emit(self.run_id, "agent.started", agent, visit=visit)
        else:
            self.bus.emit(self.run_id, "tools.started", agent)

    def on_chain_end(self, outputs, *, run_id, **kwargs):
        info = self._nodes.pop(run_id, None)
        if not info:
            return
        duration = round(time.time() - info["start"], 3)
        if info["kind"] == "agent":
            self.flush()
            self.bus.emit(self.run_id, "agent.finished", info["agent"], duration=duration)
        else:
            self.bus.emit(self.run_id, "tools.finished", info["agent"], duration=duration)

    def on_chain_error(self, error, *, run_id, **kwargs):
        info = self._nodes.pop(run_id, None)
        if info:
            self.bus.emit(self.run_id, "agent.failed", info["agent"], error=str(error)[:500])

    # llm calls -----------------------------------------------------------------
    def on_chat_model_start(self, serialized, messages, *, run_id, metadata=None, **kwargs):
        node = (metadata or {}).get("langgraph_node")
        agent = adapter.NODE_MAP.get(node, (None,))[0]
        params = kwargs.get("invocation_params") or {}
        model = params.get("model") or params.get("model_name") or (metadata or {}).get("ls_model_name") or "unknown"
        prompt_chars = sum(len(_text_of(getattr(m, "content", ""))) for batch in messages for m in batch)
        with self._lock:
            self._llm[run_id] = {"agent": agent, "model": model, "start": time.time()}
            self.totals["llm_calls"] += 1
        self.bus.emit(self.run_id, "llm.started", agent, call=str(run_id), model=model, prompt_chars=prompt_chars)

    def on_llm_end(self, response, *, run_id, **kwargs):
        info = self._llm.pop(run_id, None)
        if not info:
            return
        usage: dict = {}
        try:
            message = response.generations[0][0].message
            usage = getattr(message, "usage_metadata", None) or {}
        except (IndexError, AttributeError):
            pass
        tokens_in = int(usage.get("input_tokens", 0) or 0)
        tokens_out = int(usage.get("output_tokens", 0) or 0)
        cached = int((usage.get("input_token_details") or {}).get("cache_read", 0) or 0)
        reasoning = int((usage.get("output_token_details") or {}).get("reasoning", 0) or 0)
        served = None
        try:
            served = (response.generations[0][0].message.response_metadata or {}).get("model_name")
        except (IndexError, AttributeError):
            pass
        if served:
            self.models_served.add(f"{info['model']} -> {served}")
        cost = estimate_cost(info["model"], tokens_in, tokens_out)
        with self._lock:
            self.totals["tokens_in"] += tokens_in
            self.totals["tokens_out"] += tokens_out
            self.totals["cost_usd"] += cost or 0.0
        self.flush()
        self.bus.emit(
            self.run_id, "llm.finished", info["agent"], call=str(run_id), model=info["model"],
            duration=round(time.time() - info["start"], 3), tokens_in=tokens_in, tokens_out=tokens_out,
            cached=cached, reasoning=reasoning, cost_usd=cost, served_model=served,
        )

    def on_llm_error(self, error, *, run_id, **kwargs):
        info = self._llm.pop(run_id, None)
        if info:
            self.bus.emit(self.run_id, "llm.failed", info["agent"], call=str(run_id), error=str(error)[:500])

    # tool calls ----------------------------------------------------------------
    def on_tool_start(self, serialized, input_str, *, run_id, metadata=None, inputs=None, **kwargs):
        node = (metadata or {}).get("langgraph_node")
        agent = adapter.NODE_MAP.get(node, (None,))[0]
        tool = (serialized or {}).get("name") or kwargs.get("name") or "tool"
        with self._lock:
            self._tools[run_id] = {"agent": agent, "tool": tool, "start": time.time()}
            self.totals["tool_calls"] += 1
        args = inputs if isinstance(inputs, dict) else {"input": input_str}
        self.bus.emit(self.run_id, "tool.called", agent, call=str(run_id), tool=tool, args=args)

    def on_tool_end(self, output, *, run_id, **kwargs):
        info = self._tools.pop(run_id, None)
        if not info:
            return
        text = _text_of(getattr(output, "content", output))
        self.tool_dir.mkdir(parents=True, exist_ok=True)
        # Parallel calls share a timestamp prefix in their UUIDv7 ids; the tail is unique.
        file_name = f"{info['agent']}_{info['tool']}_{str(run_id).replace('-', '')[-12:]}.txt"
        (self.tool_dir / file_name).write_text(text, encoding="utf-8")
        flag = adapter.flag_for(text)
        if flag:
            with self._lock:
                self.totals["flags"] += 1
        self.bus.emit(
            self.run_id, "tool.result", info["agent"], call=str(run_id), tool=info["tool"],
            duration=round(time.time() - info["start"], 3), chars=len(text), preview=text[:PREVIEW_CHARS],
            file=f"tool_outputs/{file_name}", flag=flag,
        )
        if flag:
            self.bus.emit(self.run_id, "data.flag", info["agent"], label=flag, source=info["tool"], detail=text[:200])

    def on_tool_error(self, error, *, run_id, **kwargs):
        info = self._tools.pop(run_id, None)
        if info:
            self.bus.emit(self.run_id, "tool.failed", info["agent"], call=str(run_id), tool=info["tool"], error=str(error)[:500])

    # streamed text -------------------------------------------------------------
    def add_delta(self, agent: str, text: str) -> None:
        self._buffer(("llm.delta", agent), text)

    def add_reasoning(self, agent: str, text: str) -> None:
        self._buffer(("llm.reasoning", agent), text)

    def _buffer(self, key: tuple[str, str], text: str) -> None:
        with self._lock:
            self._buffers.setdefault(key, []).append(text)
        if time.monotonic() - self._last_flush >= DELTA_FLUSH_SECONDS:
            self.flush()

    def flush(self) -> None:
        with self._lock:
            buffers, self._buffers = self._buffers, {}
            self._last_flush = time.monotonic()
        for (event_type, agent), parts in buffers.items():
            text = "".join(parts)
            if text:
                self.bus.emit(self.run_id, event_type, agent, text=text)

    def add_flag(self, agent: str | None, label: str, detail: str) -> None:
        with self._lock:
            self.totals["flags"] += 1
        self.bus.emit(self.run_id, "data.flag", agent or self.current_agent, label=label, source="engine log", detail=detail[:300])


CURRENT_CAPTURE: "contextvars.ContextVar[RunCapture | None]" = contextvars.ContextVar("desk_capture", default=None)


class EngineLogCapture(logging.Handler):
    """Routes engine WARNING logs (rate limits, missing sources) to the run that produced them.

    The run thread sets CURRENT_CAPTURE; LangGraph copies the context into its worker
    threads, so logs from inside a node still resolve to the right run.
    """

    def __init__(self):
        super().__init__(level=logging.WARNING)

    def emit(self, record: logging.LogRecord) -> None:
        capture = CURRENT_CAPTURE.get()
        if capture is None:
            return
        label = adapter.flag_for(record.getMessage(), adapter.LOG_FLAG_RULES)
        if label:
            capture.add_flag(None, label, record.getMessage())
