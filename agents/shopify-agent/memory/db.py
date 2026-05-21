"""
Shopify Agent — SQLite helper module.
Thin sqlite3 wrapper: connect, query, write, migrate.
No ORM. No SQLAlchemy. stdlib sqlite3 only.

NOTE: SQLite = historical archive only (>60-day window).
      Live queries always hit the Shopify Admin API.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "shopify.db"
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


# ── Merchant helpers ──────────────────────────────────────────────────────────

def get_merchant(slug: str) -> dict | None:
    rows = query("SELECT * FROM merchants WHERE slug = ?", (slug,))
    return rows[0] if rows else None


def upsert_merchant(slug: str, name: str, **kwargs) -> int:
    existing = query("SELECT id FROM merchants WHERE slug = ?", (slug,))
    fields = {"slug": slug, "name": name, **kwargs}
    if existing:
        set_clause = ", ".join(f"{k} = ?" for k in fields if k != "slug")
        vals = tuple(v for k, v in fields.items() if k != "slug") + (slug,)
        write(f"UPDATE merchants SET {set_clause}, updated_at = datetime('now') WHERE slug = ?", vals)
        return existing[0]["id"]
    cols = ", ".join(fields.keys())
    placeholders = ", ".join("?" * len(fields))
    return write(f"INSERT INTO merchants ({cols}) VALUES ({placeholders})", tuple(fields.values()))


# ── Order helpers ─────────────────────────────────────────────────────────────

def get_unfulfilled_orders(merchant_id: int) -> list[dict]:
    return query(
        "SELECT o.* FROM orders o "
        "WHERE o.merchant_id = ? AND (o.fulfillment_status IS NULL OR o.fulfillment_status = 'partial') "
        "ORDER BY o.created_at ASC",
        (merchant_id,)
    )


def get_order_with_items(order_id: int) -> dict:
    order = query("SELECT * FROM orders WHERE id = ?", (order_id,))
    if not order:
        return {}
    items = query("SELECT * FROM line_items WHERE order_id = ?", (order_id,))
    result = order[0]
    result["line_items"] = items
    return result


def get_chargeback_orders(merchant_id: int) -> list[dict]:
    """Return all orders flagged as chargebacks (either via disputes table or CSV fallback flag)."""
    return query(
        "SELECT o.* FROM orders o "
        "WHERE o.merchant_id = ? AND (o.has_chargeback = 1 OR o.financial_status = 'chargeback') "
        "ORDER BY o.created_at DESC",
        (merchant_id,)
    )


# ── Dispute helpers ───────────────────────────────────────────────────────────

def get_disputes(merchant_id: int, status: str | None = None) -> list[dict]:
    """
    Return disputes for a merchant, optionally filtered by status.
    Primary path: disputes populated via bulk_disputes.jsonl ingestion.
    Fallback: orders.has_chargeback flag set from CSV financial_status column.
    See KNOWN_ISSUES.md — disputes API returns empty arrays when Shopify Payments is paused.
    """
    if status:
        return query(
            "SELECT d.*, o.order_number FROM disputes d "
            "JOIN orders o ON d.order_id = o.id "
            "WHERE o.merchant_id = ? AND d.status = ? "
            "ORDER BY d.opened_at DESC",
            (merchant_id, status)
        )
    return query(
        "SELECT d.*, o.order_number FROM disputes d "
        "JOIN orders o ON d.order_id = o.id "
        "WHERE o.merchant_id = ? "
        "ORDER BY d.opened_at DESC",
        (merchant_id,)
    )


def upsert_dispute(order_id: int, dispute_data: dict) -> int:
    """Insert or update a dispute record from bulk JSONL data."""
    existing = query("SELECT id FROM disputes WHERE dispute_id = ?", (dispute_data.get("dispute_id"),))
    if existing:
        write(
            "UPDATE disputes SET status = ?, finalized_on = ?, raw_json = ? WHERE dispute_id = ?",
            (dispute_data.get("status"), dispute_data.get("finalized_on"),
             dispute_data.get("raw_json"), dispute_data.get("dispute_id"))
        )
        return existing[0]["id"]
    return write(
        "INSERT INTO disputes (dispute_id, order_id, opened_at, reason_code, amount, currency, "
        "status, evidence_due_by, finalized_on, raw_json) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (
            dispute_data.get("dispute_id"), order_id, dispute_data.get("opened_at"),
            dispute_data.get("reason_code"), dispute_data.get("amount"),
            dispute_data.get("currency", "USD"), dispute_data.get("status"),
            dispute_data.get("evidence_due_by"), dispute_data.get("finalized_on"),
            dispute_data.get("raw_json"),
        )
    )


# ── House number helpers ──────────────────────────────────────────────────────

def get_house_number(order_id: int) -> dict | None:
    """
    Retrieve the cached house number for an order.
    Immutable once set — authoritative once confirmed from line_item_property.
    """
    rows = query("SELECT * FROM house_numbers WHERE order_id = ?", (order_id,))
    return rows[0] if rows else None


def set_house_number(order_id: int, house_digits: str, source: str,
                     street: str = None, side_text: str = None) -> int:
    """
    Write house number record. Immutable once set — do not update.
    source: line_item_property | csv_shipping_address | manual
    """
    existing = get_house_number(order_id)
    if existing:
        return existing["id"]
    return write(
        "INSERT INTO house_numbers (order_id, house_digits, street, side_text, source) "
        "VALUES (?,?,?,?,?)",
        (order_id, house_digits, street, side_text, source)
    )


if __name__ == "__main__":
    migrate()
    print(f"shopify.db ready at {DB_PATH}")
