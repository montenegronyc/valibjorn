"""ValiBjorn SQLite database layer — concurrent-safe with per-request connections."""

import sqlite3
import os
import json
import threading
from contextlib import contextmanager
from pathlib import Path

DB_PATH = os.getenv(
    "VALIBJORN_DB_PATH",
    str(Path(__file__).parent.parent.parent / "data" / "valibjorn.db"),
)

_schema_initialized = False
_schema_lock = threading.Lock()


def _get_fresh_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=30000")
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn: sqlite3.Connection):
    global _schema_initialized
    if _schema_initialized:
        return
    with _schema_lock:
        if _schema_initialized:
            return
        _init_schema(conn)
        _schema_initialized = True


def _init_schema(conn: sqlite3.Connection):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            founder_context TEXT,
            business_type TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS validation_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_id INTEGER NOT NULL REFERENCES concepts(id),
            verdict TEXT,
            confidence_score REAL,
            overall_score REAL,
            brief TEXT,
            status TEXT NOT NULL DEFAULT 'running',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            completed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS agent_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL REFERENCES validation_runs(id),
            agent_name TEXT NOT NULL,
            output TEXT NOT NULL,
            summary TEXT,
            confidence_score REAL,
            signals TEXT,
            risks TEXT,
            frameworks_applied TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS name_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept_id INTEGER REFERENCES concepts(id),
            proposed_name TEXT NOT NULL,
            verdict TEXT,
            conflicts TEXT,
            domain_status TEXT,
            alternatives TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_runs_concept ON validation_runs(concept_id);
        CREATE INDEX IF NOT EXISTS idx_outputs_run ON agent_outputs(run_id);
        CREATE INDEX IF NOT EXISTS idx_outputs_agent ON agent_outputs(agent_name);
        CREATE INDEX IF NOT EXISTS idx_concepts_name ON concepts(name);
        CREATE INDEX IF NOT EXISTS idx_name_searches_concept ON name_searches(concept_id);
    """
    )

    # Migration: add summary column to existing agent_outputs tables
    existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(agent_outputs)").fetchall()}
    if "summary" not in existing_cols:
        conn.execute("ALTER TABLE agent_outputs ADD COLUMN summary TEXT")


@contextmanager
def get_cursor():
    conn = _get_fresh_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def execute_query(sql: str, params: tuple = ()) -> list[dict]:
    with get_cursor() as cur:
        cur.execute(sql, params)
        if cur.description:
            return [dict(row) for row in cur.fetchall()]
        return []


def execute_one(sql: str, params: tuple = ()) -> dict | None:
    with get_cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None


def execute_insert(sql: str, params: tuple = ()) -> int:
    with get_cursor() as cur:
        cur.execute(sql, params)
        return cur.lastrowid
