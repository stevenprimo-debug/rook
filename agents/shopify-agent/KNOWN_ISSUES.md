# Shopify Agent — Known Issues

## KI-001: Disputes API returns empty arrays when Shopify Payments is paused

**Severity:** High — affects chargeback detection accuracy  
**Discovered:** 2026-05-21  
**Status:** Open (merchant-side resolution required)

### Symptom

Calling the bulk Disputes query returns `disputes: []` for all orders, even orders
that have confirmed chargebacks visible in the Shopify admin UI.

### Root cause

When a merchant's Shopify Payments account is paused (e.g., payout hold, verification
required, Payments suspended), the Payments suspension also suspends access to the
`read_shopify_payments_disputes` API scope. The disputes field in bulk operation
JSONL returns empty arrays for all orders during the suspension window.

### Dual-path workaround

The operate-mode pipeline implements two chargeback detection paths:

**Primary path (bulk JSONL — accurate when Payments active):**
1. Request a bulk operation for disputes via GraphQL Admin API
2. Download the resulting `bulk_disputes.jsonl`
3. Ingest via `ingest_archive.py` → `disputes` table
4. Filter by `NEEDS_RESPONSE | UNDER_REVIEW | ACCEPTED` status

**Fallback path (CSV financial_status — always available):**
1. Export orders CSV from Shopify admin
2. Filter rows where `financial_status = 'chargeback'`
3. Set `orders.has_chargeback = 1` for matching order IDs
4. Query `get_chargeback_orders()` from `db.py` — returns both paths

The `get_chargeback_orders()` helper in `memory/db.py` combines both paths:
```sql
WHERE has_chargeback = 1 OR financial_status = 'chargeback'
```

### Merchant resolution path

1. Merchant contacts Shopify Support to resolve the Payments pause
2. After resolution, re-authorize the `read_shopify_payments_disputes` scope
3. Re-run bulk disputes ingestion to backfill the disputes table
4. The fallback flag (`has_chargeback`) remains as a permanent cross-check

### Operator note

When onboarding a new merchant, check `merchants.shopify_payments_active` flag
before attempting disputes API queries. Set to `0` if the merchant is known to
have Payments paused, and route to the CSV fallback path automatically.

---

## KI-002: Bulk export signed URLs expire

**Severity:** Low — affects replay of historical bulk operations  
**Status:** By design (GCS signed URL TTL)

### Symptom

A previously recorded signed URL for a bulk JSONL export returns 403/410 when
replayed after expiry.

### Workaround

Never hardcode signed URLs in scripts. Use config-driven URL fetching:
1. Store `merchants.bulk_export_signed_url_expires_at` in the merchants table
2. Before fetching, check expiry; if expired, request a new bulk operation via API
3. The `shopify_order_pull.py` script reads `SHOPIFY_STORE_HANDLE` from env, not
   hardcoded store handles

---

## KI-003: cursor pagination incompatible with additional filters

**Severity:** Medium — causes 422 errors on subsequent pages  
**Status:** By design (Shopify API)

### Symptom

Passing filters (status, created_at_min, etc.) alongside `page_info` cursor
parameter returns HTTP 422.

### Workaround

The `shopify_order_pull.py` script handles this correctly: cursor pages use
`page_info + limit` only; all filters apply only to the first page request.
Do not add filter params to cursor-page requests.
