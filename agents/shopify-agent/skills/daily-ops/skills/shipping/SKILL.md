---
name: Daily-Ops — Shipping Sub-Agent
description: >
  Per-order rate shop, label purchase, and fulfillment write-back. v1 capable
  for fulfillment write only (tracking supplied manually). Rate shop + label
  purchase require Shippo MCP via Rule #18 opt-in.
type: skill
parent: shopify-agent/daily-ops
sub_agent: shipping
version: "1.0.0"
status: operational-partial
---

# Daily-Ops — Shipping Sub-Agent

**One-line role:** Rate-shop carriers, purchase the label, write tracking + carrier back to Shopify as a fulfillment.

## Inputs (from orchestrator)

| Field | Source |
|---|---|
| `order_id` | Shopify order GID |
| `ship_to_address` | From Shopify order |
| `parcel_dimensions` | From order metadata or merchant product setup |
| `service_level` | Merchant default or order-tag override |

## Outputs (handed back to orchestrator)

| Field | Meaning |
|---|---|
| `decision` | `fulfilled` \| `label_purchased_awaiting_fulfillment` \| `escalated` |
| `tracking_number` | Carrier tracking string (populated when label bought) |
| `carrier` | Carrier name (USPS, UPS, FedEx, DHL) |
| `log_line` | Structured JSON log per schema |

## MCP tools used

- `shopify.orders.get` (read) — fetch full order incl. shipping address
- `shopify.fulfillments.create` (write, reversibility=N) — write tracking + carrier back
- `shippo.rates.list` (read) — rate-shop carriers — **[NOT BUILT — REQUIRES Shippo MCP via Rule #18]**
- `shippo.transactions.create` (write) — purchase label — **[NOT BUILT — REQUIRES Shippo MCP via Rule #18]**

## Guardrails (inherited + sub-agent-specific)

- **Inherited:** dedupe, verify-before-write, escalate-on-ambiguity, structured logging, never-invent.
- **Sub-agent-specific:**
  - Before fulfillment write: tracking_number MUST be non-empty AND carrier MUST be a recognized name. Empty or null -> escalate, do not write.
  - Address validation: if `ship_to_address` is missing zip/postal_code or country, escalate.
  - Service-level override: order tags like `expedite` or `ground` may override merchant default. If the override is unrecognized, escalate (do not silently default).

## v1 limits / Rule #18 opt-in

- v1 capable: fulfillment write to Shopify when tracking is supplied externally (e.g., merchant uploads a CSV via operate-mode, daily-ops picks it up).
- v1 NOT BUILT: rate shop and label purchase. These require the Shippo MCP. Until activated, orders flagged for shipping without external tracking input are escalated to `ops-review`.
- Rule #18 v2 activation: Shippo MCP grants `shippo.rates.list` and `shippo.transactions.create`. Flip capability matrix in orchestrator.

## Sanitation

Generic Shopify shipping. No reference to specific merchants, verticals, or external client accounts. Carrier names (USPS, UPS, FedEx, DHL) are platform-standard and acceptable.

## Cross-references

- Orchestrator: `../../SKILL.md`
- Log schema: `../../log_schema.json`
- Defaults: `../../config/guardrails_defaults.json`
