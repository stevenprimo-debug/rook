---
name: Daily-Ops — Refunds Sub-Agent
description: >
  Cron-driven refund processing. v1 = Shopify draft refund only (operator
  approves before issuing). v2 = Stripe MCP direct refund via Rule #18 opt-in.
  Runs as a parallel pass to the order sweep, scanning tag:refund-requested.
type: skill
parent: shopify-agent/daily-ops
sub_agent: refunds
version: "1.0.0"
status: operational-partial
---

# Daily-Ops — Refunds Sub-Agent

**One-line role:** Sweep orders tagged `refund-requested`, verify the charge exists, create a Shopify draft refund (v1) or issue direct Stripe refund (v2).

## Inputs (from orchestrator — refund cron pass)

| Field | Source |
|---|---|
| `order_id` | Shopify order GID (filtered by `tag:refund-requested`) |
| `requested_amount` | From order metadata or order note |
| `reason` | From order metadata or order note |

## Outputs (handed back to orchestrator)

| Field | Meaning |
|---|---|
| `decision` | `draft_refund_created` \| `direct_refund_issued` \| `escalated` |
| `refund_id` | Shopify refund GID or Stripe refund ID |
| `log_line` | Structured JSON log per schema |

## MCP tools used

- `shopify.orders.get` (read) — fetch order + transactions
- `shopify.transactions.list` (read) — verify a captured Shopify Payments transaction or Stripe charge ID exists
- `shopify.refunds.create_draft` (write, reversibility=N) — create draft refund for operator approval (v1 path)
- `stripe.refunds.create` (write, reversibility=N) — **[NOT BUILT — REQUIRES Stripe MCP via Rule #18]**

## Guardrails (inherited + sub-agent-specific)

- **Inherited:** dedupe, verify-before-write, escalate-on-ambiguity, structured logging, never-invent.
- **Sub-agent-specific:**
  - **Verify before write:** Stripe charge ID OR Shopify Payments transaction ID MUST exist on the order. No charge ID -> escalate. Never invent a transaction ID.
  - **Amount match:** `requested_amount` MUST be less than or equal to the original captured amount. Over-refund attempts escalate.
  - **Conflict check:** if the order is also tagged `shipped` or `fulfilled` AND `refund-requested`, treat as ambiguous -> escalate to `ops-review`. A shipped order may legitimately need partial refund, but the agent does not decide.
  - **Tag transition:** on successful draft creation, tag becomes `refund-pending-approval` (v1) or `refund-issued` (v2). The original `refund-requested` tag is removed.
  - **Reversibility=N:** even draft refund creation is reversibility=N because it locks the refund window for that order in Shopify's accounting view.

## v1 limits / Rule #18 opt-in

- **v1 path (today):** create Shopify draft refund. Operator manually approves via Shopify admin or operate-mode tooling. Direct refund issuance is NOT performed by the agent.
- **v2 path (Rule #18 opt-in):** Stripe MCP grants `stripe.refunds.create`. Activates direct refund issuance for narrow guardrailed cases (verified charge ID + amount-match + no shipped conflict). Even with v2 active, escalate any order that fails any guardrail.

## Sanitation

Generic Shopify refund logic. No merchant-specific decision thresholds (e.g., no hard-coded dollar limits, no specific vertical refund policies, no external client account text). Threshold values live in `config/guardrails_defaults.json` and are merchant-tunable.

## Cross-references

- Orchestrator: `../../SKILL.md`
- Log schema: `../../log_schema.json`
- Defaults: `../../config/guardrails_defaults.json`
