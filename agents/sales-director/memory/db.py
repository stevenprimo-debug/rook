"""
Sales Director — SQLite helper module.
Thin sqlite3 wrapper: connect, query, write, migrate.
No ORM. No SQLAlchemy. stdlib sqlite3 only.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "pipeline.db"
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


def get_open_pipeline() -> list[dict]:
    """Return all non-closed deals with weighted value."""
    stage_weights = {
        "discovery": 0.10, "scoping": 0.25, "proposal": 0.50,
        "negotiation": 0.75, "closed-won": 1.0
    }
    deals = query(
        "SELECT * FROM deals WHERE stage NOT IN ('closed-won', 'closed-lost') "
        "ORDER BY close_date ASC"
    )
    for d in deals:
        d["weighted_value"] = d.get("value", 0) * stage_weights.get(d["stage"], 0.1)
    return deals


def log_stage_transition(deal_id: int, from_stage: str, to_stage: str, notes: str = None) -> None:
    write(
        "INSERT INTO stage_transitions (deal_id, from_stage, to_stage, notes) VALUES (?,?,?,?)",
        (deal_id, from_stage, to_stage, notes)
    )
    write("UPDATE deals SET stage = ?, updated_at = datetime('now') WHERE id = ?", (to_stage, deal_id))


def get_stalled_deals(days: int = 30) -> list[dict]:
    """Deals with no stage transition in N days."""
    return query(
        "SELECT d.* FROM deals d WHERE d.stage NOT IN ('closed-won', 'closed-lost') "
        "AND NOT EXISTS (SELECT 1 FROM stage_transitions st WHERE st.deal_id = d.id "
        "AND st.transitioned_at > date('now', ? || ' days')) ORDER BY d.close_date ASC",
        (f"-{days}",)
    )


if __name__ == "__main__":
    migrate()
    print(f"pipeline.db ready at {DB_PATH}")
