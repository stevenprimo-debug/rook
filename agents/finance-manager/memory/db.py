"""
Finance Manager — SQLite helper module.
Thin sqlite3 wrapper: connect, query, write, migrate.
No ORM. No SQLAlchemy. stdlib sqlite3 only.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "finance.db"
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


def get_overdue_invoices() -> list[dict]:
    return query(
        "SELECT * FROM invoices WHERE status IN ('pending', 'sent') "
        "AND due_date < date('now') ORDER BY due_date ASC"
    )


def get_pending_commissions() -> list[dict]:
    return query(
        "SELECT * FROM commissions WHERE status = 'earned' "
        "AND actual_pay_date IS NULL ORDER BY expected_pay_date ASC"
    )


def evaluate_deal(deal_name: str, total_value: float, gp_pct: float, hours: float = None) -> dict:
    """Run auto-reject logic per the operator's commission floor rules."""
    gp_dollars = total_value * gp_pct
    commission = gp_dollars * 0.10
    dph = (gp_dollars / hours) if hours and hours > 0 else None

    reject = False
    reason = None
    if total_value < 100_000:
        reject, reason = True, "below $100K deal floor"
    elif gp_pct < 0.15:
        reject, reason = True, "below 15% GP floor"
    elif commission < 15_000:
        reject, reason = True, "below $15K commission floor"
    elif dph and dph < 300:
        reject, reason = True, "below $300/hr efficiency floor"

    result = {
        "deal_name": deal_name, "total_value": total_value, "gp_pct": gp_pct,
        "gp_dollars": gp_dollars, "commission": commission, "dollars_per_hour": dph,
        "auto_reject": reject, "reject_reason": reason
    }
    write(
        "INSERT INTO deal_economics (deal_name, total_value, gp_pct, fulfillment_hours, "
        "dollars_per_hour, auto_reject, reject_reason) VALUES (?,?,?,?,?,?,?)",
        (deal_name, total_value, gp_pct, hours, dph, int(reject), reason)
    )
    return result


if __name__ == "__main__":
    migrate()
    print(f"finance.db ready at {DB_PATH}")
