---
name: E-commerce Ops Squad — AMA Template (Multi-agent)
description: |
  Scaffold a four-agent Anthropic Managed Agent squad that manages new
  Shopify orders end-to-end: Inventory Agent (stock check), Shipping Agent
  (Shippo label purchase + tracking), Communications Agent (Klaviyo
  transactional emails), Refunds Agent (Stripe refund handling). Two
  triggers — webhook on every new Shopify order + cron every 15 min for
  stuck/failed sweep. Owner agent: shopify-agent.
type: skill
category: ama-template
parent: ama-templates
version: "1.0.0"
voice: SYSTEM-DOMINANT
trigger: >
  Fire when customer says: e-commerce automation, Shopify order processing,
  automate fulfillment, autonomous order ops, shipping + refunds agent,
  end-to-end order flow, Shopify squad.
inherits:
  - ama_definition: ama-definition.md
  - slot_glossary: slots.md
---

# E-commerce Ops Squad — AMA Template

## Overview

Four-agent multi-agent AMA. Coordinates: Inventory → Shipping →
Communications → Refunds. Two triggers: (1) webhook per new Shopify
order, (2) cron every 15 min for stuck/failed sweep. MCPs: shopify +
shippo + klaviyo + stripe.

## How to use

1. Customer asks "build me a Shopify ops squad" or trigger phrase
2. Skill asks for slots (Shopify store, Shippo account, Klaviyo profile, Stripe account)
3. Skill writes filled CLI command to `_FROM_CLAUDE/YYYY-MM-DD-e-commerce-ops-squad-deploy.sh`
4. Customer deploys + creates environment + starts session with both webhook + cron triggers
5. Squad runs autonomously — every new order goes through all four phases

## Owner agent

**shopify-agent** invokes this skill when customer wants autonomous
order-flow management. In-session shopify-agent handles ad-hoc Shopify
work (product setup, theme tweaks, customer questions); this AMA handles
recurring autonomous order operations.

## The four sub-agents (orchestrated by the AMA)

1. **Inventory Agent** — On new order webhook: retrieve line items via `shopify.getOrder`, check each SKU via `shopify.getInventoryLevel`. All in stock → ready-to-ship + pass to Shipping. Any out-of-stock → tag `backorder` + notify Communications + log. **Never decrements inventory** (Shopify handles on fulfillment).

2. **Shipping Agent** — Pulls package dimensions from product metafields (`shopify.getProduct`), creates Shippo shipment, gets rates, purchases cheapest label, writes tracking back via `shopify.createFulfillment`, passes tracking + carrier to Communications.

3. **Communications Agent** — Sends transactional emails via Klaviyo (`klaviyo.triggerEvent`): `order_shipped` (tracking URL + carrier + ETA), `order_backorder`, `refund_processed`. Dedupe via `klaviyo.getProfileEvents` lookup before triggering (no duplicate sends within 1 hour for same order+event).

4. **Refunds Agent** — Runs on 15-min cron. Finds orders tagged `refund-requested`, verifies reason in notes, calls `stripe.createRefund` with charge ID from `shopify.getOrderTransactions`. Success → tag `refunded` + pass to Communications. Failure → tag `refund-escalate` + log (no auto-retry).

## Guardrails

- Deduplicate: maintain in-memory processed-order set per invocation
- Verify before write: confirm Stripe charge ID exists, confirm tracking number non-empty
- Escalate on ambiguity: conflicting tags or missing data → tag `ops-review`, halt
- Structured JSON log line per MCP tool call
- Never invent data — all customer info, SKUs, prices, addresses, tracking numbers from MCP responses

## Cost economics

At Sonnet-class AMA pricing + typical e-commerce volume (50-200 orders/day):
- Webhook trigger ~30 sec session per order → 50 orders × 0.5 min × 30 days = 12.5 hours
- Cron sweep every 15 min × 24h × 30 days = 720 cron runs × ~30 sec = 6 hours
- ~18.5 session-hours/mo ≈ $1.48/mo at $0.08/hour Managed Agents billing
- vs human ops time: easily 30+ hours/mo at $25/hour loaded = $750/mo

**This is the highest-leverage AMA template in the library.** Pays for itself
within the first day of operation.

## Success criterion (universal)

Customer's order-ops work hours go to zero. The cleanest deployment is the
one where the customer wakes up to a clean inbox, every order shipped, every
refund handled, every backorder email sent — without touching a thing.

## Cross-references

- Source: Anthropic AMA library reference (2026-05-15)
- Parent: `skills/templates/ama-templates/README.md`
- Owner agent: `agents/shopify-agent/SKILL.md`
- Pairs with `agents/sales-director/SKILL.md` for revenue-side reporting
