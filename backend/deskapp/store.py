"""SQLite storage for runs and their event logs."""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY,
    ticker TEXT NOT NULL,
    trade_date TEXT NOT NULL,
    analysts TEXT NOT NULL,
    depth INTEGER NOT NULL,
    deep_model TEXT NOT NULL,
    quick_model TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at REAL NOT NULL,
    started_at REAL,
    finished_at REAL,
    rating TEXT,
    decision TEXT,
    tokens_in INTEGER DEFAULT 0,
    tokens_out INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0,
    llm_calls INTEGER DEFAULT 0,
    tool_calls INTEGER DEFAULT 0,
    flags INTEGER DEFAULT 0,
    error TEXT
);
CREATE INDEX IF NOT EXISTS runs_created ON runs(created_at DESC);
CREATE INDEX IF NOT EXISTS runs_ticker ON runs(ticker, trade_date);
CREATE TABLE IF NOT EXISTS events (
    run_id TEXT NOT NULL,
    seq INTEGER NOT NULL,
    ts REAL NOT NULL,
    type TEXT NOT NULL,
    agent TEXT,
    payload TEXT NOT NULL,
    PRIMARY KEY (run_id, seq)
);
CREATE TABLE IF NOT EXISTS backtests (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at REAL NOT NULL,
    status TEXT NOT NULL,
    config TEXT NOT NULL,
    items TEXT NOT NULL,
    budget_usd REAL NOT NULL,
    note TEXT
);
CREATE VIRTUAL TABLE IF NOT EXISTS event_text USING fts5(run_id UNINDEXED, seq UNINDEXED, agent UNINDEXED, type UNINDEXED, text);
"""

# Columns added after the first release; each is applied once by _migrate.
MIGRATIONS = [
    ("engine", "ALTER TABLE runs ADD COLUMN engine TEXT DEFAULT 'tradingagents'"),
    ("engine_version", "ALTER TABLE runs ADD COLUMN engine_version TEXT DEFAULT ''"),
    ("provider", "ALTER TABLE runs ADD COLUMN provider TEXT DEFAULT 'deepseek'"),
    ("purpose", "ALTER TABLE runs ADD COLUMN purpose TEXT DEFAULT 'live'"),
    ("backtest_id", "ALTER TABLE runs ADD COLUMN backtest_id TEXT"),
    ("memory", "ALTER TABLE runs ADD COLUMN memory TEXT DEFAULT 'shared'"),
    ("variant", "ALTER TABLE runs ADD COLUMN variant TEXT DEFAULT ''"),
    ("models_served", "ALTER TABLE runs ADD COLUMN models_served TEXT"),
]

# Which event payload fields are worth full-text search.
TEXT_FIELDS = {
    "report.updated": ("text",),
    "tool.result": ("preview",),
    "tool.called": ("tool",),
    "data.flag": ("label", "detail"),
    "decision.structured": ("rationale", "reasoning", "executive_summary", "investment_thesis", "strategic_actions"),
    "llm.reasoning": ("text",),
    "run.failed": ("error",),
}

TERMINAL_STATUSES = ("finished", "failed", "cancelled")
_JSON_FIELDS = ("analysts", "decision", "models_served")


class Store:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(SCHEMA)
        self._lock = threading.Lock()
        self._migrate()

    def _migrate(self) -> None:
        cols = {row[1] for row in self._conn.execute("PRAGMA table_info(runs)")}
        for name, ddl in MIGRATIONS:
            if name not in cols:
                self._conn.execute(ddl)
        # Earlier labels: git describe ("v0.4.0-17-gbe952b8") or empty for the first runs, all on the same commit.
        self._conn.execute("UPDATE runs SET engine_version = '0.4.0+be952b8' WHERE engine_version IN ('', 'v0.4.0-17-gbe952b8')")
        # Backfill the search index for events stored before it existed.
        indexed = self._conn.execute("SELECT count(*) FROM event_text").fetchone()[0]
        if indexed == 0:
            rows = self._conn.execute("SELECT run_id, seq, type, agent, payload FROM events").fetchall()
            for r in rows:
                text = self._searchable(r["type"], json.loads(r["payload"]))
                if text:
                    self._conn.execute("INSERT INTO event_text (run_id, seq, agent, type, text) VALUES (?, ?, ?, ?, ?)",
                                       (r["run_id"], r["seq"], r["agent"], r["type"], text))
        self._conn.commit()

    @staticmethod
    def _searchable(type_: str, payload: dict) -> str:
        fields = TEXT_FIELDS.get(type_)
        if not fields:
            return ""
        return "\n".join(str(payload.get(f)) for f in fields if payload.get(f))

    # runs ------------------------------------------------------------------
    def create_run(self, run: dict) -> None:
        row = {**run}
        for field in _JSON_FIELDS:
            if field in row and not isinstance(row[field], str):
                row[field] = json.dumps(row[field])
        cols = ", ".join(row)
        marks = ", ".join("?" for _ in row)
        with self._lock:
            self._conn.execute(f"INSERT INTO runs ({cols}) VALUES ({marks})", tuple(row.values()))
            self._conn.commit()

    def update_run(self, run_id: str, **fields) -> None:
        if not fields:
            return
        for field in _JSON_FIELDS:
            if field in fields and not isinstance(fields[field], str) and fields[field] is not None:
                fields[field] = json.dumps(fields[field])
        sets = ", ".join(f"{k} = ?" for k in fields)
        with self._lock:
            self._conn.execute(f"UPDATE runs SET {sets} WHERE id = ?", (*fields.values(), run_id))
            self._conn.commit()

    def get_run(self, run_id: str) -> dict | None:
        with self._lock:
            row = self._conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        return self._row(row) if row else None

    def list_runs(self, limit: int = 200) -> list[dict]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM runs ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [self._row(r) for r in rows]

    def agent_progress(self, run_id: str) -> tuple[list[str], dict[str, str]]:
        """Agent order and per-agent state for a run in flight, from its agent events."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT type, agent, payload FROM events WHERE run_id = ? AND type IN ('run.queued', 'agent.started', 'agent.finished', 'agent.failed') ORDER BY seq",
                (run_id,),
            ).fetchall()
        order: list[str] = []
        state: dict[str, str] = {}
        for r in rows:
            if r["type"] == "run.queued":
                order = list(json.loads(r["payload"]).get("agents") or [])
            elif r["agent"]:
                state[r["agent"]] = {"agent.started": "running", "agent.finished": "done", "agent.failed": "failed"}[r["type"]]
        return order, state

    def mark_interrupted(self) -> int:
        with self._lock:
            cur = self._conn.execute(
                "UPDATE runs SET status = 'failed', error = 'Desk stopped before the run finished', finished_at = ? "
                "WHERE status IN ('queued', 'running')",
                (time.time(),),
            )
            self._conn.commit()
            return cur.rowcount

    @staticmethod
    def _row(row: sqlite3.Row) -> dict:
        data = dict(row)
        for field in _JSON_FIELDS:
            if data.get(field):
                data[field] = json.loads(data[field])
        return data

    def find_reusable_run(self, ticker: str, trade_date: str, analysts: list[str], depth: int, deep_model: str,
                          quick_model: str, memory: str, engine_version: str, variant: str = "") -> dict | None:
        """A finished run with identical inputs, so a backtest never pays for the same decision twice."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM runs WHERE status = 'finished' AND ticker = ? AND trade_date = ? AND analysts = ? AND depth = ? "
                "AND deep_model = ? AND quick_model = ? AND memory = ? AND engine_version = ? AND COALESCE(variant, '') = ? ORDER BY finished_at LIMIT 1",
                (ticker, trade_date, json.dumps(analysts), depth, deep_model, quick_model, memory, engine_version, variant),
            ).fetchone()
        return self._row(row) if row else None

    def engine_versions(self) -> list[str]:
        with self._lock:
            rows = self._conn.execute("SELECT DISTINCT engine_version FROM runs WHERE engine_version IS NOT NULL AND engine_version != ''").fetchall()
        return [r[0] for r in rows]

    def runs_by_ids(self, ids: list[str]) -> dict[str, dict]:
        if not ids:
            return {}
        marks = ", ".join("?" for _ in ids)
        with self._lock:
            rows = self._conn.execute(f"SELECT * FROM runs WHERE id IN ({marks})", ids).fetchall()
        return {r["id"]: self._row(r) for r in rows}

    # backtests ---------------------------------------------------------------
    def create_backtest(self, bt: dict) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO backtests (id, name, created_at, status, config, items, budget_usd, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (bt["id"], bt["name"], bt["created_at"], bt["status"], json.dumps(bt["config"]), json.dumps(bt["items"]),
                 bt["budget_usd"], bt.get("note")),
            )
            self._conn.commit()

    def update_backtest(self, bt_id: str, **fields) -> None:
        for key in ("config", "items"):
            if key in fields and not isinstance(fields[key], str):
                fields[key] = json.dumps(fields[key])
        sets = ", ".join(f"{k} = ?" for k in fields)
        with self._lock:
            self._conn.execute(f"UPDATE backtests SET {sets} WHERE id = ?", (*fields.values(), bt_id))
            self._conn.commit()

    def get_backtest(self, bt_id: str) -> dict | None:
        with self._lock:
            row = self._conn.execute("SELECT * FROM backtests WHERE id = ?", (bt_id,)).fetchone()
        return self._bt_row(row) if row else None

    def list_backtests(self) -> list[dict]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM backtests ORDER BY created_at DESC").fetchall()
        return [self._bt_row(r) for r in rows]

    def pause_interrupted_backtests(self) -> int:
        with self._lock:
            cur = self._conn.execute("UPDATE backtests SET status = 'paused', note = 'Desk stopped while it was running' WHERE status = 'running'")
            self._conn.commit()
            return cur.rowcount

    @staticmethod
    def _bt_row(row: sqlite3.Row) -> dict:
        data = dict(row)
        data["config"] = json.loads(data["config"])
        data["items"] = json.loads(data["items"])
        return data

    # events ----------------------------------------------------------------
    def add_event(self, event: dict) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO events (run_id, seq, ts, type, agent, payload) VALUES (?, ?, ?, ?, ?, ?)",
                (event["run_id"], event["seq"], event["ts"], event["type"], event.get("agent"), json.dumps(event["payload"])),
            )
            text = self._searchable(event["type"], event["payload"])
            if text:
                self._conn.execute("INSERT INTO event_text (run_id, seq, agent, type, text) VALUES (?, ?, ?, ?, ?)",
                                   (event["run_id"], event["seq"], event.get("agent"), event["type"], text))
            self._conn.commit()

    def events_since(self, run_id: str, after_seq: int = 0) -> list[dict]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT run_id, seq, ts, type, agent, payload FROM events WHERE run_id = ? AND seq > ? ORDER BY seq",
                (run_id, after_seq),
            ).fetchall()
        return [{**dict(r), "payload": json.loads(r["payload"])} for r in rows]

    def search(self, query: str, limit: int = 300) -> list[dict]:
        """Full-text search over reports, tool results, flags, decisions and reasoning.

        Returns one row per matching event: run_id, seq, agent, type and a snippet
        with the match marked by [[ ]]. Plain text is quoted as a phrase so
        punctuation cannot break the FTS5 query; explicit operators pass through.
        """
        q = query.strip()
        if not q:
            return []
        if not any(op in q for op in (" OR ", " AND ", " NOT ", '"', "*")):
            q = '"' + q.replace('"', " ") + '"'
        with self._lock:
            try:
                rows = self._conn.execute(
                    "SELECT run_id, seq, agent, type, snippet(event_text, 4, '[[', ']]', ' … ', 18) AS snippet, bm25(event_text) AS score "
                    "FROM event_text WHERE event_text MATCH ? ORDER BY score LIMIT ?",
                    (q, limit),
                ).fetchall()
            except sqlite3.OperationalError:
                return []
        return [dict(r) for r in rows]

    def last_seq(self, run_id: str) -> int:
        with self._lock:
            row = self._conn.execute("SELECT MAX(seq) FROM events WHERE run_id = ?", (run_id,)).fetchone()
        return row[0] or 0
