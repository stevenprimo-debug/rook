#!/usr/bin/env python3
"""
Generic Shopify operate-mode helper. Sanitized from a prior client engagement.

One-time historical load from bulk JSONL exports into SQLite archive.
Use this for the >60-day window that the Shopify Admin API no longer returns.

IMPORTANT: SQLite = historical archive ONLY. Live queries always hit the Shopify API.
           Run this once after onboarding a merchant with a historical bulk export.

Supports:
  - Orders bulk JSONL (from Shopify bulk operation: { query { orders } })
  - Disputes bulk JSONL (from Shopify bulk operation: { query { orders { disputes } } })

Configuration via environment variables (see .env.example):
  SHOPIFY_VAULT_ROOT   — base path for this merchant's data folder
  SHOPIFY_MERCHANT_SLUG — merchant slug for SQLite merchant record

Usage:
    python ingest_archive.py --orders path/to/orders.jsonl --merchant my-store
    python ingest_archive.py --disputes path/to/disputes.jsonl --merchant my-store
    python ingest_archive.py --orders orders.jsonl --disputes disputes.jsonl --merchant my-store
"""

import json
import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "memory"))

VAULT_ROOT    = Path(os.environ.get("SHOPIFY_VAULT_ROOT", "."))
MERCHANT_SLUG = os.environ.get("SHOPIFY_MERCHANT_SLUG", "")


def get_or_create_merchant(db, slug: str) -> int:
    """Get merchant ID, creating a placeholder record if needed."""
    existing = db.query("SELECT id FROM merchants WHERE slug = ?", (slug,))
    if existing:
        return existing[0]["id"]
    return db.write(
        "INSERT INTO merchants (slug, name) VALUES (?, ?)",
        (slug, slug)
    )


def ingest_orders(jsonl_path: str, merchant_id: int, db) -> dict:
    """
    Ingest orders bulk JSONL into SQLite.
    Returns {shopify_order_id: internal_order_id} mapping for dispute ingestion.
    """
    order_id_map = {}
    inserted = 0
    skipped = 0

    with open(jsonl_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)

            shopify_id = obj.get("id", "")
            order_number = obj.get("name", "")
            financial_status = obj.get("financialStatus", "") or obj.get("financial_status", "")
            fulfillment_status = obj.get("fulfillmentStatus", "") or obj.get("fulfillment_status", "")
            created_at = obj.get("createdAt", "") or obj.get("created_at", "")
            total_price = float(obj.get("totalPriceSet", {}).get("shopMoney", {}).get("amount", 0) or 0)
            has_chargeback = 1 if "chargeback" in (financial_status or "").lower() else 0

            existing = db.query(
                "SELECT id FROM orders WHERE shopify_order_id = ? AND merchant_id = ?",
                (shopify_id, merchant_id)
            )
            if existing:
                order_id_map[shopify_id] = existing[0]["id"]
                skipped += 1
                continue

            internal_id = db.write(
                "INSERT INTO orders (merchant_id, shopify_order_id, order_number, "
                "total_price, financial_status, fulfillment_status, has_chargeback, created_at) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (merchant_id, shopify_id, order_number, total_price,
                 financial_status, fulfillment_status, has_chargeback, created_at)
            )
            order_id_map[shopify_id] = internal_id
            inserted += 1

    print(f"Orders: {inserted} inserted, {skipped} already present")
    return order_id_map


def ingest_disputes(jsonl_path: str, order_id_map: dict, db) -> None:
    """
    Ingest disputes bulk JSONL into SQLite.
    Links disputes to orders via order_id_map.

    NOTE: This may return empty arrays if Shopify Payments was paused during
    the bulk export window. See KNOWN_ISSUES.md KI-001.
    """
    inserted = 0
    skipped = 0
    unmatched = 0

    with open(jsonl_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)

            order_gid = obj.get("id", "")
            disputes = obj.get("disputes", [])

            if not disputes:
                continue

            internal_order_id = order_id_map.get(order_gid)
            if not internal_order_id:
                unmatched += 1
                continue

            for d in disputes:
                dispute_id = d.get("id", "")
                existing = db.query("SELECT id FROM disputes WHERE dispute_id = ?", (dispute_id,))
                if existing:
                    skipped += 1
                    continue

                db.write(
                    "INSERT INTO disputes (dispute_id, order_id, opened_at, reason_code, "
                    "amount, currency, status, evidence_due_by, finalized_on, raw_json) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (
                        dispute_id, internal_order_id,
                        d.get("initiatedAt", ""),
                        d.get("reasonCode", "") or d.get("reason", ""),
                        float(d.get("amount", {}).get("amount", 0) or 0),
                        d.get("amount", {}).get("currencyCode", "USD"),
                        d.get("status", ""),
                        d.get("evidenceDueBy", ""),
                        d.get("finalizedOn", ""),
                        json.dumps(d),
                    )
                )
                inserted += 1

    print(f"Disputes: {inserted} inserted, {skipped} already present, {unmatched} unmatched orders")


def main():
    import db as shopify_db

    parser = argparse.ArgumentParser(
        description="Ingest historical bulk JSONL exports into SQLite archive."
    )
    parser.add_argument("--orders", type=str, default="", help="Path to orders bulk JSONL")
    parser.add_argument("--disputes", type=str, default="", help="Path to disputes bulk JSONL")
    parser.add_argument("--merchant", type=str, default=MERCHANT_SLUG,
                        help="Merchant slug (from SHOPIFY_MERCHANT_SLUG env or --merchant flag)")
    args = parser.parse_args()

    if not args.merchant:
        print("ERROR: --merchant flag or SHOPIFY_MERCHANT_SLUG env var required.", file=sys.stderr)
        sys.exit(1)

    if not args.orders and not args.disputes:
        print("ERROR: At least one of --orders or --disputes is required.", file=sys.stderr)
        sys.exit(1)

    # Ensure schema is current
    shopify_db.migrate()

    merchant_id = get_or_create_merchant(shopify_db, args.merchant)
    print(f"Merchant: {args.merchant} (id={merchant_id})")

    order_id_map = {}

    if args.orders:
        print(f"\nIngesting orders: {args.orders}")
        order_id_map = ingest_orders(args.orders, merchant_id, shopify_db)

    if args.disputes:
        if not order_id_map:
            # Build map from existing DB records
            rows = shopify_db.query(
                "SELECT shopify_order_id, id FROM orders WHERE merchant_id = ?",
                (merchant_id,)
            )
            order_id_map = {r["shopify_order_id"]: r["id"] for r in rows}
            print(f"Built order map from DB: {len(order_id_map)} orders")

        print(f"\nIngesting disputes: {args.disputes}")
        ingest_disputes(args.disputes, order_id_map, shopify_db)

    print(f"\nIngest complete.")


if __name__ == "__main__":
    main()
