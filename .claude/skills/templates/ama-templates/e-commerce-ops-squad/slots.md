# E-commerce Ops Squad — Slot Glossary

## Required slots

| Slot | Description |
|---|---|
| `{CUSTOMER_NAME}` | Customer's company name |
| `{CUSTOMER_SHORT_NAME}` | Lowercase slug for environment naming |
| `{CUSTOMER_WEBHOOK_INGRESS_URL}` | Customer's webhook receiver URL (typically `https://mcp.shopify.com/webhook/<customer-id>`) |
| `{SHOPIFY_STORE_DOMAIN}` | e.g., `acme-store.myshopify.com` |

## MCP credentials required (customer pre-configure)

| MCP | What customer provides |
|---|---|
| shopify | Admin API access token with read/write scopes on orders + inventory + fulfillment + tags |
| shippo | API key |
| klaviyo | API key + profile sync configured for transactional events |
| stripe | Restricted API key with refund permission only (NOT full account access) |

## Shopify pre-flight (customer sets up before deploy)

| Setup item | Where |
|---|---|
| Custom order tags created | `backorder`, `refund-requested`, `refunded`, `refund-escalate`, `ops-review` |
| Product metafields for package dimensions | `custom.package_length`, `custom.package_width`, `custom.package_height`, `custom.package_weight` |
| Webhook subscriptions | `orders/create` → customer's ingress URL |
| Klaviyo event templates | `order_shipped`, `order_backorder`, `refund_processed` (mapped to existing flows) |

## Optional slots (defaults)

| Slot | Default | Override? |
|---|---|---|
| `{MODEL_ID}` | `claude-sonnet-4-6` | Rare |
| `{DATE}` | Today's date | Auto-filled |
| `{CRON_SCHEDULE_SWEEP}` | `*/15 * * * *` (every 15 min) | Yes — adjust for low-volume stores (every 30 min or hourly) |
| `{REFUND_REASON_REQUIRED}` | `true` (Refunds Agent checks notes) | Yes — set `false` if customer trusts manual queue |
| `{DEDUPE_WINDOW_HOURS}` | 1 (Communications Agent dedupe) | Yes — shorter for high-velocity stores |

## Customer prompts (skill asks in this order)

1. "What customer is this AMA for?" → `{CUSTOMER_NAME}` + auto-derive `{CUSTOMER_SHORT_NAME}`
2. "Shopify store domain?" → `{SHOPIFY_STORE_DOMAIN}`
3. "Pre-flight: have you created the 5 order tags + 4 product metafields + Klaviyo event templates?" → if N, offer to scaffold a pre-flight checklist
4. "MCP credentials ready for shopify + shippo + klaviyo + stripe?" → confirm
5. "Cron sweep cadence — default every 15 min, or adjust for store volume?" → `{CRON_SCHEDULE_SWEEP}`
6. "Webhook ingress URL (where Shopify sends `orders/create` events)?" → `{CUSTOMER_WEBHOOK_INGRESS_URL}`

## [customer] fit

This AMA is the **Phase 2 capstone** for the [customer-short] engagement. [Customer Name] currently
manually triages backlog (Phase 1 = clearance via SOW). Phase 2 deploys this
AMA + the cost-calc system. Phase 3 = the productized "Custom-Fab Operator
Dashboard" extending this pattern.

Reference: `_FROM_CLAUDE/2026-05-14-nma-sow-draft.md` (Phase 1 scope),
`agents/shopify-agent/briefs/2026-05-11-nma-cost-calc-system-brief.md` (full
[customer-short] roadmap).
