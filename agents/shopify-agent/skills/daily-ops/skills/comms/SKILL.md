---
name: Daily-Ops — Comms Sub-Agent
description: >
  Transactional customer email send via Gmail MCP. Templates use Rule #17
  pattern (Hello first_name plus plain text plus bullets, NO sign-off).
  Dedupe via subject + order_id. v1 transactional only — no marketing
  segmentation.
type: skill
parent: shopify-agent/daily-ops
sub_agent: comms
version: "1.0.0"
status: operational
---

# Daily-Ops — Comms Sub-Agent

**One-line role:** Send transactional emails to buyers (backorder notice, shipped notice, refund-pending notice) via Gmail MCP using Rule #17 templates.

## Inputs (from orchestrator)

| Field | Source |
|---|---|
| `order_id` | Shopify order GID |
| `customer_email` | From Shopify order |
| `customer_first_name` | From Shopify order (MCP response, never synthesized) |
| `template_id` | `backorder` \| `shipped` \| `refund_pending` |
| `template_vars` | Order-specific fill-ins (tracking #, ETA, item list) |

## Outputs (handed back to orchestrator)

| Field | Meaning |
|---|---|
| `decision` | `sent` \| `skipped_duplicate` \| `escalated` |
| `gmail_message_id` | Gmail message ID on successful send |
| `log_line` | Structured JSON log per schema |

## MCP tools used

- `gmail.messages.send` (write, reversibility=N) — send the transactional email
- `gmail.messages.list` (read) — dedupe check (search subject + order_id for prior send)
- `shopify.customers.get` (read) — verify customer email + first_name from authoritative source

## Templates (Rule #17 pattern)

Templates live as plain-text strings inside this sub-skill. They follow Rule #17 strictly:

- Greeting: `Hello {first_name},` (comma, not exclamation)
- Body: 1-2 short paragraphs OR a bulleted list — never both
- NO sign-off line. NO Cheers. NO name. NO emoji.
- Subject line: includes order_id for dedupe (e.g., `Order #1042 — backorder notice`)

Available v1 templates:

| template_id | Purpose | Subject prefix |
|---|---|---|
| `backorder` | Notify buyer of stock-out + ETA | `Order #<id> — backorder notice` |
| `shipped` | Notify buyer of label + tracking | `Order #<id> — shipped` |
| `refund_pending` | Notify buyer refund is being processed | `Order #<id> — refund pending` |

The cs-email-default template at `../../../operate/templates/cs-email-default.md` is the canonical Rule #17 reference. Daily-ops uses the same skeleton, parameterized.

## Guardrails (inherited + sub-agent-specific)

- **Inherited:** dedupe, verify-before-write, escalate-on-ambiguity, structured logging, never-invent.
- **Sub-agent-specific:**
  - Dedupe: before sending, search Gmail sent folder for messages with subject containing the order_id. If a prior send is found, skip with `result_status: skipped`.
  - first_name: MUST come from `shopify.customers.get` response. If null or empty, fall back to `Hello,` (no name). Never invent a name.
  - customer_email: if missing or invalid format, escalate (do not attempt send).
  - Marketing content is forbidden: no promotional copy, no upsell links, no discount codes. Transactional content only.
  - NO sign-off line (per Rule #17 — distinct from operator's personal `Cheers` pattern).

## v1 limits / Rule #18 opt-in

- v1: Gmail MCP only. Single From: address per merchant. Plain text. No templated flows, no segmentation, no A/B testing.
- Rule #18 v2 candidates: Klaviyo MCP for templated flows + segmentation. Postmark / SendGrid MCP for transactional-grade infrastructure (higher deliverability than Gmail).

## Sanitation

Generic transactional comms. Templates are placeholder-only — no specific merchant brand voice, no specific customer name patterns, no external client account text. `{first_name}` and `{order_id}` are the only required interpolations.

## Cross-references

- Orchestrator: `../../SKILL.md`
- Rule #17 reference template: `../../../operate/templates/cs-email-default.md`
- Log schema: `../../log_schema.json`
- Defaults: `../../config/guardrails_defaults.json`
