"""
Inbox Manager — SQLite helper module.
Thin sqlite3 wrapper: connect, query, write, migrate.
No ORM. No SQLAlchemy. stdlib sqlite3 only.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "messages.db"
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


def get_reply_queue() -> list[dict]:
    """Return all threads needing a reply, ordered by received date."""
    return query(
        "SELECT * FROM threads WHERE category = 'REPLY_NEEDED' AND status NOT IN ('sent', 'archived') "
        "ORDER BY received_at ASC"
    )


def get_pending_drafts() -> list[dict]:
    """Return drafts awaiting operator approval."""
    return query(
        "SELECT d.*, t.subject, t.sender_name, t.sender_email FROM drafts d "
        "JOIN threads t ON d.thread_id = t.id WHERE d.status = 'pending' "
        "ORDER BY d.created_at ASC"
    )


def mark_draft_sent(draft_id: int) -> None:
    """Gate: only called after explicit operator confirm."""
    write("UPDATE drafts SET status = 'sent', sent_at = datetime('now') WHERE id = ?", (draft_id,))
    draft = query("SELECT thread_id FROM drafts WHERE id = ?", (draft_id,))
    if draft:
        write("UPDATE threads SET status = 'sent', last_activity = datetime('now') WHERE id = ?",
              (draft[0]["thread_id"],))


def log_triage_run(stats: dict) -> int:
    return write(
        "INSERT INTO triage_status (threads_reviewed, reply_needed, fyi_only, archived, "
        "drafts_created, drafts_sent) VALUES (?,?,?,?,?,?)",
        (stats.get("reviewed", 0), stats.get("reply_needed", 0), stats.get("fyi_only", 0),
         stats.get("archived", 0), stats.get("drafts_created", 0), stats.get("drafts_sent", 0))
    )


if __name__ == "__main__":
    migrate()
    print(f"messages.db ready at {DB_PATH}")
