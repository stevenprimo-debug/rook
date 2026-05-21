---
name: Shopify Agent — Operate Mode
description: >
  Merchant operations: pull orders, draft CS emails, generate analytics reports,
  monitor chargebacks, and prepare production handoff batches. Uses Shopify Admin
  API as the source of truth for live data; SQLite for historical archive (>60 days).
type: skill
parent: shopify-agent
mode: operate
version: "1.0.0"
status: operational
shopify_scopes:
  required:
    - read_orders
    - read_customers
    - read_fulfillments
    - read_products
  optional:
    - read_shopify_payments_disputes   # when Shopify Payments active (see KNOWN_ISSUES.md KI-001)
    - write_orders                     # for order tagging — reversibility=N
    - write_fulfillments               # for fulfillment marks — reversibility=N
    - write_draft_orders               # for refund drafts — reversibility=N
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
---

# Shopify Agent — Operate Mode

Handles the merchant's day-to-day operational workflow: order intelligence,
chargeback tracking, CS drafting, analytics, and production handoff prep.

## Data architecture (non-negotiable)

**Shopify Admin API = source of truth.** All live queries hit the API.
SQLite (`memory/shopify.db`) = historical archive ONLY — orders outside
the 60-day API window. Do not position SQLite as the primary data store.

## Workflow

### Pull orders

```bash
SHOPIFY_STORE_HANDLE=my-store \
SHOPIFY_CLIENT_ID=... \
SHOPIFY_CLIENT_SECRET=... \
python skills/operate/scripts/shopify_order_pull.py \
  --created-at-min 2026-01-01 \
  --output orders_$(date +%Y%m%d).xlsx
```

Incremental pull: `--since-id <last_known_order_id>`

### Parse production spreadsheet

For Google Sheet export (markdown table via MCP):
```bash
python skills/operate/scripts/parse_gsheet.py \
  --input tool_result.json \
  --format json_mcp \
  --output canonical.csv
```

For xlsx or csv export:
```bash
python skills/operate/scripts/parse_gsheet.py \
  --input merchant_sheet.csv \
  --format csv \
  --output canonical.csv
```

### Enrich with house numbers / custom fields

```bash
SHOPIFY_API_XLSX=orders_20260521.xlsx \
SHOPIFY_CSV_PATH=shopify_export.csv \
python skills/operate/scripts/enrich_orders_and_batch.py \
  --gsheet canonical.csv \
  --output enriched.csv \
  --batch
```

### Batch by size

```bash
python skills/operate/scripts/batch_by_size.py \
  --input enriched.csv \
  --output-dir ./batches \
  --manifest manifest.csv
```

### Check chargebacks

**Primary path (when Shopify Payments active):**
```bash
SHOPIFY_VAULT_ROOT=./data \
python skills/operate/scripts/parse_disputes.py \
  --local bulk_disputes.jsonl
```

**Fallback path (when Payments paused — see KNOWN_ISSUES.md KI-001):**
- Export orders CSV from Shopify admin
- Filter `financial_status = 'chargeback'`
- Run `build_handoff_excel.py --flag-chargebacks` to mark orders

### Generate analytics report

The agent renders `templates/analytics-report.html.j2` with merchant data
and can convert to PDF via the `html2pdf` skill for sharing.

Query the SQLite archive for historical data (>60 days):
```python
from memory import db
chargebacks = db.get_chargeback_orders(merchant_id=1)
```

### Build handoff Excel

```bash
SHOPIFY_COLOR_MAP=config/status_color_map.json \
python skills/operate/scripts/build_handoff_excel.py \
  --source master.xlsx \
  --output handoff.xlsx \
  --chargebacks "#3091,#3052"
```

### Draft CS email

Use `templates/cs-email-default.md`:
- Opener: `Hello {first_name},`
- Situation summary (1-2 sentences)
- Bullet points: what happened / what we're doing / what they need to do
- Next step + ETA
- Closing line slot
- NO sign-off — operator picks
- Plain text only — not HTML (Rule #17 customer-facing default)

### Ingest historical archive (one-time)

For orders outside the 60-day API window:
```bash
SHOPIFY_MERCHANT_SLUG=my-store \
python skills/operate/scripts/ingest_archive.py \
  --orders historical_orders.jsonl \
  --disputes historical_disputes.jsonl \
  --merchant my-store
```

## Dual-path chargeback detection

See `KNOWN_ISSUES.md` KI-001 for the full explanation.

**Primary:** `bulk_disputes.jsonl` → `disputes` table → `db.get_disputes()`

**Fallback:** CSV `financial_status='chargeback'` → `orders.has_chargeback = 1` → `db.get_chargeback_orders()`

The `get_chargeback_orders()` helper queries both paths — always use it
instead of querying `disputes` table directly.

## Planned capabilities

### Ship-label automation (Rule #18 opt-in)

[NOT BUILT IN PHASE A — documented for future implementation]

When the operator's prompt matches keywords [ship, label, shipping, carrier, rate],
offer via AskUserQuestion before executing:

- "Buy shipping label?" — runs carrier rate shop + insurance calc + label purchase
- Carrier API: Shopify Shipping (when Payments active) OR Shippo/EasyPost (fallback)
- Insurance: auto-compute to subtotal + 15% buffer; operator confirms
- **Reversibility=N on every label buy** — no undo after purchase
- Tracking number writes back to Shopify order fulfillment

Implementation requires:
1. `read_shopify_payments_disputes` scope active (implies Payments not paused)
2. OR Shippo/EasyPost API key in env
3. Operator explicit confirmation per Rule #18

### Auto-fulfillment marking (Rule #18 opt-in)

[NOT BUILT IN PHASE A]

Mark orders as fulfilled after confirmed shipment. Requires `write_fulfillments` scope.
Reversibility=N — once fulfilled in Shopify, sends customer notification.

### Customer email dispatch (Rule #18 opt-in)

[NOT BUILT IN PHASE A]

Send drafted CS emails via Shopify email. Reversibility=N after send.
Use AskUserQuestion with draft preview before dispatch.

## Configuration

All scripts are config-driven via env vars. See `.env.example` in this directory
for the full variable list. Never hardcode store handles, paths, or credentials.

Key env vars:
- `SHOPIFY_STORE_HANDLE` — myshopify.com subdomain
- `SHOPIFY_CLIENT_ID` / `SHOPIFY_CLIENT_SECRET` — OAuth credentials
- `SHOPIFY_VAULT_ROOT` — base path for merchant data files
- `SHOPIFY_CUSTOM_PROPERTY` — line-item property name (e.g. "House number")
- `SHOPIFY_COLOR_MAP` — path to `config/status_color_map.json`
- `BATCH_SKIP_NOTES` / `BATCH_DONE_NOTES` — production status filtering

## Non-negotiables

- Shopify API first; SQLite only for historical (>60 days) or offline cross-reference
- Reversibility=N on: label buys, fulfillment marks, customer email dispatch — always AskUserQuestion
- CS emails: plain text, `Hello {first_name},` opener, bullets — never HTML, never operator `.eml` pattern
- Sanitation: no merchant-specific identifiers in any shipped file
