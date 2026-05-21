"""
Account Manager — SQLite helper module.
Thin sqlite3 wrapper: connect, query, write, migrate.
No ORM. No SQLAlchemy. stdlib sqlite3 only.
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent / "accounts.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def connect() -> sqlite3.Connection:
    """Open connection with row_factory for dict-like access."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def migrate() -> None:
    """Apply schema.sql if tables don't exist. Idempotent."""
    with connect() as conn:
        sql = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(sql)


def query(sql: str, params: tuple = ()) -> list[dict]:
    """Run a SELECT and return list of dicts."""
    with connect() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]


def write(sql: str, params: tuple = ()) -> int:
    """Run INSERT/UPDATE/DELETE. Returns lastrowid."""
    with connect() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid


def upsert_account(slug: str, name: str, stage: str, **kwargs) -> int:
    """Insert or update an account by slug."""
    existing = query("SELECT id FROM accounts WHERE slug = ?", (slug,))
    fields = {"slug": slug, "name": name, "stage": stage, **kwargs}
    if existing:
        set_clause = ", ".join(f"{k} = ?" for k in fields if k != "slug")
        vals = tuple(v for k, v in fields.items() if k != "slug") + (slug,)
        write(f"UPDATE accounts SET {set_clause}, updated_at = datetime('now') WHERE slug = ?", vals)
        return existing[0]["id"]
    else:
        cols = ", ".join(fields.keys())
        placeholders = ", ".join("?" * len(fields))
        return write(f"INSERT INTO accounts ({cols}) VALUES ({placeholders})", tuple(fields.values()))


def get_renewal_window(days_out: int = 90) -> list[dict]:
    """Return accounts whose renewal_date falls within the next N days."""
    return query(
        "SELECT * FROM accounts WHERE renewal_date IS NOT NULL "
        "AND date(renewal_date) <= date('now', ? || ' days') "
        "AND date(renewal_date) >= date('now') "
        "ORDER BY renewal_date ASC",
        (str(days_out),)
    )


def get_at_risk(unresolved_only: bool = True) -> list[dict]:
    """Return at-risk signals, optionally filtering to unresolved only."""
    sql = "SELECT s.*, a.name as account_name FROM at_risk_signals s JOIN accounts a ON s.account_id = a.id"
    if unresolved_only:
        sql += " WHERE s.resolved_at IS NULL"
    sql += " ORDER BY s.detected_at DESC"
    return query(sql)


if __name__ == "__main__":
    migrate()
    print(f"accounts.db ready at {DB_PATH}")
