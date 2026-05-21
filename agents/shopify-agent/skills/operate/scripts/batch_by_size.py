#!/usr/bin/env python3
"""
Generic Shopify operate-mode helper. Sanitized from a prior client engagement.

Batch enriched orders by a sizing dimension into production sheets.
Originally built for a merchant producing physical items in discrete sizes,
where different sizes have different sheet capacities.

Generalizes to any merchant workflow where orders need to be batched into
groups with a maximum capacity per batch, optionally segmented by a size
dimension.

Configuration via environment variables (see .env.example):
  SHOPIFY_VAULT_ROOT         — base path for merchant data
  BATCH_SIZE_FIELD           — field in enriched CSV to use for size segmentation (default: pillar_h)
  BATCH_SIZES                — comma-sep list of valid sizes (default: 24,48)
  BATCH_CAP_DEFAULT          — default orders per batch (default: 7)
  BATCH_SKIP_NOTES           — skip orders matching these notes (default: cancelled,chargeback,do not make)
  BATCH_DONE_NOTES           — skip orders with these done-status notes (default: shipped,rust,paint,rba)

Usage:
    python batch_by_size.py --input enriched.csv --output-dir ./batches --manifest manifest.csv
"""

import sys
import re
import csv
import json
import os
import argparse
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = Path(os.environ.get("SHOPIFY_VAULT_ROOT", "."))
SIZE_FIELD  = os.environ.get("BATCH_SIZE_FIELD", "pillar_h")
SIZES_RAW   = os.environ.get("BATCH_SIZES", "24,48")
VALID_SIZES = [int(s.strip()) for s in SIZES_RAW.split(",")]
CAP_DEFAULT = int(os.environ.get("BATCH_CAP_DEFAULT", 7))

SKIP_NOTES_RAW = os.environ.get("BATCH_SKIP_NOTES", "cancelled,chargeback,do not make")
DONE_NOTES_RAW = os.environ.get("BATCH_DONE_NOTES", "shipped,rust,paint,rba")
SKIP_NOTES = {n.strip().lower() for n in SKIP_NOTES_RAW.split(",")}
DONE_NOTES = {n.strip().lower() for n in DONE_NOTES_RAW.split(",")}

# Per-size capacities (can be overridden via BATCH_CAPS_JSON env)
_caps_json = os.environ.get("BATCH_CAPS_JSON", "{}")
SIZE_CAPS   = {**{s: CAP_DEFAULT for s in VALID_SIZES}, **json.loads(_caps_json)}


def is_blank(val: str) -> bool:
    v = val.strip().lower()
    return not v or v in ("0", "n/a", "na", "none", "unfulfilled")


def should_skip(prod_notes: str, custom_field: str) -> bool:
    notes_lower = (prod_notes or "").lower()
    val_lower   = (custom_field or "").lower()
    return any(kw in notes_lower or kw in val_lower for kw in SKIP_NOTES)


def is_done(prod_notes: str) -> bool:
    return any(kw in (prod_notes or "").lower() for kw in DONE_NOTES)


def load_orders(csv_path: str) -> list[dict]:
    """Load enriched orders from CSV, filtering out skip/done/blank."""
    orders = []
    with open(csv_path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            val = row.get("custom_field", "").strip()
            if not val or is_blank(val):
                continue
            if should_skip(row.get("prod_notes", ""), val):
                continue
            if is_done(row.get("prod_notes", "")):
                continue
            orders.append(row)
    return orders


def assign_size(order: dict) -> int:
    """
    Determine the size bucket for an order.
    Uses SIZE_FIELD from the order dict if present,
    otherwise defaults to the first valid size.
    Override with BATCH_SIZE_FIELD env var.
    """
    raw = order.get(SIZE_FIELD, "").strip()
    try:
        size = int(raw)
        return size if size in VALID_SIZES else VALID_SIZES[-1]
    except (ValueError, TypeError):
        return VALID_SIZES[-1]  # Default to largest size


def batch_by_size(orders: list[dict]) -> dict[int, list[list[dict]]]:
    """
    Segment orders by size and batch each segment by CAP.
    Returns {size: [[batch1_orders], [batch2_orders], ...]}
    """
    buckets: dict[int, list] = {s: [] for s in VALID_SIZES}
    for o in orders:
        size = assign_size(o)
        buckets.setdefault(size, []).append(o)

    result = {}
    for size, bucket in buckets.items():
        cap = SIZE_CAPS.get(size, CAP_DEFAULT)
        sheets = []
        current = []
        for o in bucket:
            if len(current) >= cap:
                sheets.append(current)
                current = []
            current.append(o)
        if current:
            sheets.append(current)
        result[size] = sheets
        print(f"  Size {size}: {len(bucket)} orders → {len(sheets)} batches (cap={cap})")

    return result


def write_manifest(manifest_rows: list[dict], out_path: str) -> None:
    fields = ["size", "batch", "order", "custom_field", "source"]
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(manifest_rows)
    print(f"\nManifest: {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch enriched orders by size into production groups."
    )
    parser.add_argument("--input", required=True, help="Enriched CSV from enrich_orders_and_batch.py")
    parser.add_argument("--output-dir", required=True, help="Directory to write batch files")
    parser.add_argument("--manifest", default="manifest.csv", help="Manifest CSV output path")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading orders from {args.input}...")
    orders = load_orders(args.input)
    print(f"  {len(orders)} orders ready for batching")

    print("\nBatching by size...")
    batches = batch_by_size(orders)

    manifest_rows = []
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    for size, sheets in batches.items():
        size_dir = out_dir / f"{size}"
        size_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n  Writing {len(sheets)} batches for size={size}...")
        for i, batch in enumerate(sheets, 1):
            # Write batch JSON for downstream consumers
            out_path = size_dir / f"batch_{i:03d}_{size}_{ts}.json"
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(batch, f, indent=2, ensure_ascii=False)
            print(f"    [{i}/{len(sheets)}] {out_path.name} ({len(batch)} orders)")
            for o in batch:
                manifest_rows.append({
                    "size": size,
                    "batch": i,
                    "order": o.get("order", ""),
                    "custom_field": o.get("custom_field", ""),
                    "source": o.get("custom_field_source", ""),
                })

    write_manifest(manifest_rows, args.manifest)
    total = sum(len(s) for s in batches.values())
    print(f"\nDone. {total} batches written → {out_dir}")


if __name__ == "__main__":
    main()
