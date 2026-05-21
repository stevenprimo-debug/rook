# Daily-Ops Runtime

Runtime model, trigger mechanism, escalation flow, and Phase-2 deferred items for `daily-ops` mode.

## v1 trigger: `scheduled-tasks` MCP cron sweep

The `scheduled-tasks` MCP is the only trigger surface in v1. Configure one scheduled task per merchant:

| Field | Value |
|---|---|
| Schedule | `*/15 * * * *` (every 15 minutes) |
| Action | Dispatch `shopify-agent` in `daily-ops` mode with merchant_id parameter |
| Reversibility | Cron itself is reversible (pause / unpause); per-order actions are governed by per-sub-agent guardrails |

On each fire:

1. Orchestrator reads `memory/daily_ops_state.json` for `last_run_at`.
2. Queries Shopify Admin API: `orders.list?created_at_min={last_run_at}&status=any`.
3. Builds `processed_order_ids` dedupe set (empty at sweep start; populated as each order processes).
4. For each order, runs the dispatch flow (Inventory -> Shipping or Comms -> emit log line).
5. Refunds sub-agent runs as a parallel pass: query `orders.list?tag=refund-requested` (independent of `created_at_min` window).
6. On clean exit, writes `last_run_at = now()` back to state file.
7. On orchestrator exception, does NOT update `last_run_at` (next sweep retries the same window).

## v1 SLA gap

15-minute latency between order creation and first agent touch. This is acceptable for:

- Inventory checks (no customer-visible delay)
- Backorder notifications (15 min vs immediate is invisible to the buyer)
- Refund processing (always operator-paced)
- Stuck-order sweeps (cron is the natural pattern)

Not acceptable for:

- Real-time fraud signaling (defer to Shopify Flow / native fraud analysis)
- Sub-minute fulfillment SLAs (Phase 2 webhook required)

Document this gap with merchants at onboarding.

## v2 trigger: webhook receiver (DEFERRED — Phase 2)

Future surface, NOT BUILT in v1:

1. Register Shopify webhook subscription: `orders/create`, `orders/updated`, `orders/cancelled`.
2. Public HTTPS endpoint (deployed via Cloudflare Workers or Vercel edge function).
3. HMAC-SHA256 signature verification on every incoming webhook (header: `X-Shopify-Hmac-Sha256`).
4. Enqueue order_id to a durable queue (Redis / SQS / Cloudflare Queues).
5. Orchestrator pulls from queue instead of cron-sweeping Shopify.

Phase 2 dependencies: hosted HTTPS endpoint + queue infra + signature verification library. Out of scope until merchant onboarding demands sub-15-min latency.

## ops-review escalation flow

When any sub-agent fails a guardrail check or hits ambiguity:

1. Sub-agent emits JSON log line: `result_status: escalated`, `error_message: <reason>`.
2. Sub-agent applies tag `ops-review` to the Shopify order (via `write_orders` scope).
3. Sub-agent returns control to orchestrator with `escalated=true` flag.
4. Orchestrator skips remaining downstream sub-agents for this order.
5. Order remains tagged `ops-review` until operator manually clears it (drop tag or retag with explicit instruction).
6. Orchestrator on next sweep: skips orders carrying `ops-review` tag (treat as already-handled by operator).

Operator UI for the `ops-review` queue lives in operate-mode (`skills/operate/`). Daily-ops produces the queue; operate consumes it.

## Memory & state

| Path | Purpose | Format |
|---|---|---|
| `memory/daily_ops_state.json` | `last_run_at`, sweep counter, agent version | JSON |
| `memory/daily_ops.log` | Per-MCP-call structured log lines | JSONL (one log line per row) |
| `config/guardrails_defaults.json` | Tunable defaults: dedupe TTL, escalation tag name | JSON |

Logs are append-only. Rotation policy: when `daily_ops.log` exceeds 50 MB, rename to `daily_ops.log.YYYYMMDD` and start fresh. Rotation is operator-triggered, not automatic in v1.

## Rule #18 opt-in MCPs

These MCPs are scaffolded in sub-skill SKILL.md files but flagged `[NOT BUILT — REQUIRES <X> MCP]`. Activation steps when merchant grants the connector:

| MCP | Sub-agent | Activation |
|---|---|---|
| Shippo | shipping | Set env `SHIPPO_API_KEY`; remove NOT BUILT flag from `skills/shipping/SKILL.md`; capability matrix in orchestrator flips Label purchase to v1. |
| Stripe | refunds | Set env `STRIPE_API_KEY`; remove NOT BUILT flag from `skills/refunds/SKILL.md`; capability matrix flips Refund issuance to direct-via-Stripe. |
| Klaviyo | comms | Set env `KLAVIYO_API_KEY`; remove flag; capability matrix flips Email send to templated flows. (Gmail MCP remains as fallback.) |

Until activation, the orchestrator detects unavailable MCP at runtime and escalates affected orders to `ops-review`.

## Cross-references

- Orchestrator: `SKILL.md` (this directory)
- Log schema: `log_schema.json` (this directory)
- Defaults: `config/guardrails_defaults.json` (this directory)
- Sub-skills: `skills/{inventory,shipping,comms,refunds}/SKILL.md`
- Operate-mode counterpart: `../operate/SKILL.md`
