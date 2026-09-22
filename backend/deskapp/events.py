"""Event bus: every step of a run becomes a numbered event, stored and pushed live."""

from __future__ import annotations

import asyncio
import json
import threading
import time
from collections import defaultdict

from .settings import RUNS_DIR
from .store import Store

TERMINAL_EVENTS = {"run.finished", "run.failed", "run.cancelled"}


class EventBus:
    def __init__(self, store: Store):
        self.store = store
        self.loop: asyncio.AbstractEventLoop | None = None
        self._lock = threading.Lock()
        self._seq: dict[str, int] = {}
        self._subs: dict[str, list[asyncio.Queue]] = defaultdict(list)

    def emit(self, run_id: str, type_: str, agent: str | None = None, **payload) -> dict:
        with self._lock:
            if run_id not in self._seq:
                self._seq[run_id] = self.store.last_seq(run_id)
            self._seq[run_id] += 1
            event = {"run_id": run_id, "seq": self._seq[run_id], "ts": time.time(), "type": type_, "agent": agent, "payload": payload}
            self.store.add_event(event)
            run_dir = RUNS_DIR / run_id
            run_dir.mkdir(parents=True, exist_ok=True)
            with open(run_dir / "events.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
            subscribers = list(self._subs.get(run_id, ()))
        if self.loop is not None:
            for queue in subscribers:
                self.loop.call_soon_threadsafe(queue.put_nowait, event)
        return event

    def subscribe(self, run_id: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        with self._lock:
            self._subs[run_id].append(queue)
        return queue

    def unsubscribe(self, run_id: str, queue: asyncio.Queue) -> None:
        with self._lock:
            if queue in self._subs.get(run_id, []):
                self._subs[run_id].remove(queue)
