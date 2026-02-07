"""ValiBjorn SQLite database layer."""

import sqlite3
import os
import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

DB_PATH = os.getenv(
    "VALIBJORN_DB_PATH",
    str(Path(__file__).parent.parent.parent / "data" / "valibjorn.db"),
)

_connection = None


def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is not None:
        try:
            _connection.execute("SELECT 1")
            return _connection
        except sqlite3.Error:
            _connection = None

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    _connection = sqlite3.connect(DB_PATH)
    _connection.row_factory = sqlite3.Row
    _connection.execute("PRAGMA journal_mode=WAL")
    _connection.execute("PRAGMA foreign_keys=ON")
    _init_schema(_connection)
    return _connection


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
            confidence_score REAL,
            signals TEXT,
            risks TEXT,
            frameworks_applied TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_runs_concept ON validation_runs(concept_id);
        CREATE INDEX IF NOT EXISTS idx_outputs_run ON agent_outputs(run_id);
        CREATE INDEX IF NOT EXISTS idx_outputs_agent ON agent_outputs(agent_name);
        CREATE INDEX IF NOT EXISTS idx_concepts_name ON concepts(name);
    """
    )


@contextmanager
def get_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


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
