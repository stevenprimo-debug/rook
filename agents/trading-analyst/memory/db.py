"""
Trading Analyst — SQLite helper module.
Thin sqlite3 wrapper: connect, query, write, migrate.
No ORM. No SQLAlchemy. stdlib sqlite3 only.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "trading.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def migrate() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def query(sql: str, params: tuple = ()) -> list[dict]:
    with connect() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def write(sql: str, params: tuple = ()) -> int:
    with connect() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid


def get_active_setups() -> list[dict]:
    return query("SELECT * FROM setups WHERE status IN ('watching', 'active') ORDER BY setup_date DESC")


def get_current_posture() -> dict | None:
    rows = query("SELECT * FROM posture_history ORDER BY recorded_at DESC LIMIT 1")
    return rows[0] if rows else None


def log_trade_result(setup_id: int, entry_price: float, exit_price: float, notes: str = None) -> dict:
    setup = query("SELECT * FROM setups WHERE id = ?", (setup_id,))
    if not setup:
        raise ValueError(f"Setup {setup_id} not found")
    s = setup[0]
    pnl = (exit_price - entry_price) * s.get("position_size", 1) * (1 if s["side"] == "long" else -1)
    pnl_pct = (exit_price - entry_price) / entry_price * 100 * (1 if s["side"] == "long" else -1)
    outcome = "win" if pnl > 0 else ("loss" if pnl < 0 else "breakeven")
    journal_id = write(
        "INSERT INTO journal (setup_id, entry_price, exit_price, pnl, pnl_pct, outcome, thesis) "
        "VALUES (?,?,?,?,?,?,?)",
        (setup_id, entry_price, exit_price, pnl, pnl_pct, outcome, notes)
    )
    write("UPDATE setups SET status = 'closed' WHERE id = ?", (setup_id,))
    return {"journal_id": journal_id, "pnl": pnl, "pnl_pct": pnl_pct, "outcome": outcome}


if __name__ == "__main__":
    migrate()
    print(f"trading.db ready at {DB_PATH}")
