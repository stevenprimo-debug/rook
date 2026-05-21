---
name: Daily-Ops — Inventory Sub-Agent
description: >
  Per-order stock check, backorder tagging, and routing decision. Inherits
  parent daily-ops guardrails (dedupe, verify-before-write, escalate, log,
  never-invent). v1 uses Shopify Admin API only.
type: skill
parent: shopify-agent/daily-ops
sub_agent: inventory
version: "1.0.0"
status: operational
---

# Daily-Ops — Inventory Sub-Agent

**One-line role:** Check stock for every line item on an incoming order. Tag backorders. Decide whether the order proceeds to shipping or stops at comms.

## Inputs (from orchestrator)

| Field | Source |
|---|---|
| `order_id` | Shopify order GID |
| `line_items` | Array of `{variant_id, sku, quantity, fulfillment_location_id?}` |
| `processed_order_ids` | Dedupe set (read-only) |

## Outputs (handed back to orchestrator)

| Field | Meaning |
|---|---|
| `decision` | `proceed_to_shipping` \| `proceed_to_backorder_comms` \| `escalated` |
| `out_of_stock_items` | Array of SKUs that failed the stock check (empty if all in stock) |
| `log_line` | Structured JSON log per schema |

## MCP tools used

- `shopify.inventory_levels.list` (read) — check on-hand by variant_id + location
- `shopify.products.get` (read) — for SKU resolution when variant_id lookup is ambiguous
- `shopify.orders.tags.add` (write, reversibility=N) — apply `backorder` tag

## Guardrails (inherited + sub-agent-specific)

- **Inherited:** dedupe, verify-before-write, escalate-on-ambiguity, structured logging, never-invent.
- **Sub-agent-specific:**
  - Backorder tag applies ONLY when inventory check returns hard zero. Stale-cache responses or null values escalate to `ops-review` instead of tagging.
  - Multi-location inventory: if `fulfillment_location_id` is unspecified on the order, use the merchant default location. If no default is set, escalate.
  - Partial stock-out (some items in stock, others not): treat as backorder for the WHOLE order. Do not split. Splits are operator decisions.

## v1 limits / Rule #18 opt-in

- v1: Shopify Admin API only. No inventory predictions, no reorder triggers.
- Rule #18 v2 candidates: `shopify-bundles` (bundle expansion), `inventory-forecast` (ML restock signals).

## Sanitation

Generic Shopify operate-mode logic. No customer names. No vertical-specific merchant identifiers. No external client account references. Any SKU pattern, product type, or merchant size is acceptable.

## Cross-references

- Orchestrator: `../../SKILL.md`
- Log schema: `../../log_schema.json`
- Defaults: `../../config/guardrails_defaults.json`
