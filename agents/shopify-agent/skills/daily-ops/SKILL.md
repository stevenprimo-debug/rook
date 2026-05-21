---
name: Shopify Agent — Daily-Ops Mode
description: >
  Event-driven autopilot for Shopify merchant operations. Runs continuously via
  cron sweep. Distinct from operate-mode (operator-in-the-loop, batch tooling).
  Orchestrates four sub-agents — Inventory, Shipping, Comms, Refunds — through
  guardrailed dispatch with dedupe, verify-before-write, escalate-on-ambiguity,
  and structured JSON logging. v1 is cron-driven via scheduled-tasks MCP;
  webhook receiver is Phase 2.
type: skill
parent: shopify-agent
mode: daily-ops
version: "1.0.0"
status: operational
shopify_scopes:
  required:
    - read_orders
    - read_customers
    - read_inventory
    - read_fulfillments
    - write_orders        # for ops-review tag, backorder tag — reversibility=N
    - write_fulfillments  # for tracking write-back — reversibility=N
  optional:
    - read_shopify_payments_disputes
    - write_draft_orders  # v1 refund fallback — reversibility=N
  external_mcps_required_for_full_capability:
    - gmail               # transactional sends (v1)
    - scheduled-tasks     # cron sweep mechanism (v1)
    - shippo              # label purchase (Rule #18 opt-in, v2)
    - stripe              # direct refunds (Rule #18 opt-in, v2)
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
---

# Shopify Agent — Daily-Ops Mode (Orchestrator)

**One-line role:** Event-driven autopilot for Shopify merchant operations. Runs continuously via cron sweep. Distinct from operate-mode (operator-in-the-loop).

Operate-mode is the human running batch scripts to pull orders, draft CS, write reports.
Daily-ops is the agent running the store on a 15-minute heartbeat — picking up new orders, checking stock, dispatching shipping, sending transactional comms, and surfacing refund candidates for operator approval.

The orchestrator does not execute the work itself. It dispatches one of four sub-agents per order, observes structured JSON log lines, and enforces the guardrail stack.

---

## Trigger model

**v1 — cron sweep only.** The `scheduled-tasks` MCP fires the orchestrator every 15 minutes. Each invocation:

1. Queries Shopify Admin API for orders with `created_at >= last_run_at` (window stored in `memory/daily_ops_state.json`).
2. Loads `processed_order_ids` dedupe set for this invocation (TTL = single sweep).
3. For each new order, runs the dispatch flow below.
4. Persists `last_run_at = now()` on clean exit.

**v2 — webhook receiver (DEFERRED, do not build).** Shopify `orders/create` webhook → HTTPS endpoint → enqueue order_id → orchestrator pulls from queue. Requires public HTTPS surface + webhook signature verification (HMAC-SHA256). See `RUNTIME.md` § Phase 2.

**Why cron-only for v1:** webhook surface needs hosted endpoint + signature verification + retry queue. Cron via `scheduled-tasks` MCP works inside Claude Code today with zero infra. 15-min latency is acceptable for inventory / comms / refund use cases; fulfillment SLA gap is documented in `RUNTIME.md`.

---

## Dispatch flow

```
[scheduled-tasks MCP cron fires every 15min]
        |
        v
[ORCHESTRATOR]
  1. Pull orders where created_at >= last_run_at
  2. Build processed_order_ids dedupe set
  3. For each order:
        |
        v
   [INVENTORY sub-agent]
     - Check stock for every line item
     - If any out-of-stock -> tag order `backorder`, hand to COMMS, halt for this order
     - If all in-stock -> hand to SHIPPING
        |
        v
   [SHIPPING sub-agent]   --------> [COMMS sub-agent] (shipped notification)
     - Rate shop (Rule #18: requires Shippo MCP — v1 NOT BUILT)
     - Label purchase (v2)
     - Fulfillment write to Shopify (v1 capable when tracking provided manually)
        |
        v
   [REFUNDS sub-agent]    (separate cron path — sweeps tag:refund-requested)
     - v1: Shopify draft refund only
     - v2: Stripe MCP direct refund (Rule #18 opt-in)
  4. Emit structured JSON log line per MCP call
  5. Persist last_run_at on clean exit
```

The orchestrator never writes to Shopify itself. It delegates the write to the appropriate sub-agent, which carries its own scoped guardrails.

---

## Guardrails

These guardrails are inherited by every sub-agent. Sub-agents may ADD constraints; they may not relax these.

| Guardrail | Behavior |
|---|---|
| **Dedupe** | Maintain `processed_order_ids` set per cron invocation. If an order_id appears twice in the same sweep, skip the second occurrence. TTL = single invocation; the set does not survive across sweeps (Shopify `created_at >= last_run_at` filter is the cross-sweep dedupe). |
| **Verify before write** | Before refund: confirm Stripe charge ID exists on the order (or Shopify Payments transaction). Before fulfillment write: confirm tracking number is non-empty AND carrier is named. Before backorder tag: confirm inventory check returned hard zero (not stale cache). |
| **Escalate on ambiguity** | Conflicting tags (e.g., `refund-requested` + `shipped`), missing customer email on a transactional comm, address validation failure, or any sub-agent exception -> apply tag `ops-review`, emit JSON log line with `result_status: escalated`, do not process further. Operator picks up `ops-review` queue manually. |
| **Logging** | Every MCP call emits one structured JSON line conforming to `log_schema.json`. Log lines write to `memory/daily_ops.log` (JSONL, append-only). No free-form prose logs. |
| **Never invent data** | Customer first names, SKUs, prices, addresses, tracking numbers, charge IDs — all must come from MCP responses. The agent never synthesizes a missing field. If a field is missing, escalate. |
| **Reversibility=N gate** | Every write (fulfillment, refund, label, comm send, order tag) is reversibility=N. Pre-declared guardrails (this table) scope the action narrowly enough that no per-action operator confirm is required. If a guardrail check fails, the action is NOT performed — it is escalated. |

Defaults live in `config/guardrails_defaults.json`.

---

## Sub-agents

| Sub-agent | File | One-line role |
|---|---|---|
| Inventory | `skills/inventory/SKILL.md` | Stock check per line item; backorder tag; hand-off to shipping or comms. |
| Shipping | `skills/shipping/SKILL.md` | Rate shop, label purchase, fulfillment write. Rule #18: Shippo MCP for full v1 capability. |
| Comms | `skills/comms/SKILL.md` | Gmail MCP transactional sends. Dedupe via subject + order_id. Plain text + Hello first_name pattern. |
| Refunds | `skills/refunds/SKILL.md` | Sweeps tag:refund-requested. v1 = Shopify draft refund only. v2 = Stripe MCP (Rule #18). |

---

## Capability matrix

| Capability | v1 (today) | v2 (Rule #18 opt-in) |
|---|---|---|
| Inventory check | Shopify Admin API | — |
| Stock-out backorder tag | Shopify Admin API | — |
| Email send (transactional) | Gmail MCP | Klaviyo MCP via Rule #18 (templated flows, segmentation) |
| Label purchase | Declared, NOT BUILT | Shippo MCP via Rule #18 |
| Refund issuance | Shopify draft refund only | Stripe MCP direct refund via Rule #18 |
| Fulfillment write | Shopify Admin API (tracking supplied manually) | Auto-tracking via Shippo MCP |
| Webhook receiver | DEFERRED to v2 | Hosted HTTPS + HMAC signature verification |
| Cron scheduling | scheduled-tasks MCP | — |

Anything marked `Rule #18 opt-in` is scaffolded in the sub-skill SKILL.md but flagged `[NOT BUILT — REQUIRES <X> MCP]`. The orchestrator detects unavailable MCP at runtime and escalates the order to `ops-review` rather than failing silently.

---

## State files

| File | Purpose |
|---|---|
| `memory/daily_ops_state.json` | `last_run_at` timestamp + sweep counter |
| `memory/daily_ops.log` | JSONL append-only structured log (per `log_schema.json`) |
| `config/guardrails_defaults.json` | Dedupe TTL, escalation tag, never-invent flags |

---

## Operator handoff: ops-review queue

Orders tagged `ops-review` are the operator's manual queue. The agent does not retry escalated orders on subsequent sweeps. The operator clears them via operate-mode tooling (drop the tag, optionally retag with explicit instruction like `refund-approved`).

This is the single point of human control over the autopilot. Tag in -> autopilot stops. Tag out -> autopilot may resume next sweep.

---

## What this mode is NOT

- Not a webhook receiver (Phase 2).
- Not a Python script. v1 is skill content only — no `scripts/` directory. The agent reads MCP tools at runtime per the dispatch flow above.
- Not a replacement for operate-mode. Operate is the operator-in-the-loop batch tool; daily-ops is the autopilot. Both modes coexist.
- Not authorized to issue refunds without verify-before-write + tag gating.
- Not authorized to send marketing email. Transactional comms only (order confirmation, backorder notice, shipped notice). Marketing flows are out of scope — defer to Klaviyo (Rule #18 v2).

---

## Cross-references

- Parent agent SKILL: `agents/shopify-agent/SKILL.md`
- Operate-mode counterpart: `skills/operate/SKILL.md`
- Runtime details: `RUNTIME.md` (this directory)
- Log schema: `log_schema.json` (this directory)
- Guardrails defaults: `config/guardrails_defaults.json` (this directory)
- Voice spine: `.claude/voice-spine.md`
- Rule #17 (transactional email pattern): Hello first_name pattern + plain text + bullets, NO sign-off
- Rule #18 (MCP opt-in): external MCPs are scaffolded but flagged unbuilt until merchant grants the connector
