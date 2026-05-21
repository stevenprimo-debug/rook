# Master Shopify App — Backend Runtime Spec (v1)

**Date:** 2026-05-21
**Owner:** chief-of-staff (operator)
**Surface:** Backend only. Embedded UI frontend is a separate spec.
**Runtime:** Cloudflare Workers, multi-tenant.
**Source skill:** `agents/shopify-agent/skills/daily-ops/` (system prompt + sub-agents + log schema).
**Status:** Draft for operator lock-in.

---

## 1. Executive summary

The backend is the runtime that powers the Master Shopify App — a Shopify App Store listing that installs a chat-first ops co-pilot inside merchant admin. The merchant talks to a Polaris+App Bridge chat surface; the backend (this spec) handles OAuth, webhooks, cron sweeps, Anthropic chat streaming with tool use, multi-tenant secret isolation, and the automation-posture state machine that governs whether a write is auto-executed, queued for approval, or merely surfaced.

v1 scope: one Cloudflare Worker hosts N merchants, OAuth install per shop, HMAC-verified webhooks queued to Cloudflare Queues, 15-min cron sweep against Shopify Admin GraphQL, SSE chat route streaming Claude responses with tool-use routing to Shopify + Gmail, posture default `notify_only` (the trust ramp), and App Bridge Toast + Gmail digest as the two notification surfaces.

v2 deferred: Shippo label buy, Stripe direct refunds, Klaviyo, SMS, multi-region failover, auto-posture-graduation.

Cost model summary: free Cloudflare tier covers up to ~1K merchants at LOW volume; Anthropic API is the dominant variable cost (~$0.04-$0.18 per order processed at Sonnet 4.6 pricing). Recommended SaaS pricing tiers from $29/mo (LOW) to $299/mo (HIGH).

---

## 2. Architecture diagram

```
+--------------------------+         +----------------------------+
|  Shopify Admin (merchant)|         |   Gmail (merchant inbox)   |
|                          |         |                            |
|  +--------------------+  |         |   - approval requests      |
|  |  App iframe        |  |         |   - daily digests          |
|  |  (Polaris+AppBridge)| |         |   - ops-review escalations |
|  |  - chat UI         |  |         +-------------+--------------+
|  |  - Toast surface   |  |                       ^
|  +---------+----------+  |                       |
+------------|-------------+                       |
             | session token (JWT)                 | (Gmail MCP send)
             | SSE chat / fetch                    |
             v                                     |
+----------------------------------------------------------------+
|              CLOUDFLARE WORKER (multi-tenant)                  |
|                                                                |
|  /oauth/install     /oauth/callback     /webhook/:shop/*       |
|  /chat/:shop (SSE)  /cron (scheduled)   /uninstall             |
|                                                                |
|  +--------------------+   +-----------------+   +-----------+  |
|  | Session JWT verify |   | HMAC verify     |   | Posture   |  |
|  | (Shopify JWKS)     |   | (X-Shopify-Hmac)|   | engine    |  |
|  +--------------------+   +--------+--------+   +-----+-----+  |
|                                    |                  |        |
|                                    v                  |        |
|                          +-------------------+        |        |
|                          | Cloudflare Queues |        |        |
|                          +---------+---------+        |        |
|                                    |                  |        |
|                                    v                  v        |
|                          +----------------------------------+  |
|                          |  Orchestrator (daily-ops prompt) |  |
|                          |  - Anthropic API (Sonnet 4.6)    |  |
|                          |  - tool_use routing              |  |
|                          +-------+--------------------+-----+  |
|                                  |                    |        |
|        +-------------------------+                    |        |
|        v                                              v        |
|  +-----------+                                +--------------+ |
|  | D1 store  |  per-tenant config,            | Secrets Store| |
|  | logs,     |  conversation history,         | per-tenant   | |
|  | state     |  last_run_at                   | tokens       | |
|  +-----------+                                +--------------+ |
+----------------------------------------------------------------+
       |                          |                       |
       v                          v                       v
+--------------+        +------------------+      +----------------+
| Anthropic API|        | Shopify Admin GQL|      | Gmail API      |
| (claude)     |        | (per-shop token) |      | (per-tenant)   |
+--------------+        +------------------+      +----------------+

NOTIFICATION PATH:
  Webhook fires -> Worker -> {
     in-app: App Bridge Toast (push via SSE channel to open chat)
     out-of-app: Gmail digest (if no live SSE session in last 5min)
  } -> embedded chat opens with order context preloaded
```

---

## 3. OAuth + session token flow

### Shopify Partners app registration

- **App URL:** `https://app.{domain}/dashboard` (loads embedded iframe)
- **Allowed redirection URLs:** `https://app.{domain}/oauth/callback`
- **Embedded:** Yes (App Bridge 4.x)
- **Required scopes** (from `shopify_scopes:daily_ops` in source skill):
  - `read_orders`, `read_customers`, `read_inventory`, `read_fulfillments`
  - `write_orders` (ops-review tag, backorder tag — reversibility=N)
  - `write_fulfillments` (tracking write-back — reversibility=N)
  - `write_draft_orders` (v1 refund fallback — reversibility=N)
- **Optional scopes:** `read_shopify_payments_disputes`
- **Webhooks subscribed at install:** `orders/create`, `orders/updated`, `refunds/create`, `app/uninstalled`, `shop/update`

### Install flow

1. Merchant clicks Install on App Store listing.
2. Shopify redirects browser to `/oauth/install?shop=<shop>.myshopify.com` on the Worker.
3. Worker validates `shop` param (regex `^[a-z0-9-]+\.myshopify\.com$`), generates nonce, redirects to Shopify OAuth grant URL with scopes + state=nonce.
4. Merchant approves scopes in Shopify UI.
5. Shopify redirects to `/oauth/callback?code=...&shop=...&state=<nonce>`.
6. Worker verifies state nonce + HMAC on query string, exchanges code for permanent access token.
7. Worker writes per-tenant secret to Cloudflare Secrets Store: key `shopify_token:<shop_domain>`, value = access token.
8. Worker writes tenant row to D1 with default config (posture=`notify_only`, kill_switch=`off`, gmail_account=`unset`, anthropic_key_owner=`pooled`).
9. Worker registers webhooks via Shopify Admin GraphQL `webhookSubscriptionCreate` for each topic above (HMAC shared secret = the app's Shopify API secret).
10. Redirect merchant to embedded app: `https://<shop>.myshopify.com/admin/apps/<app-handle>`.

### Session token validation (per request)

Every request from the embedded iframe carries an `Authorization: Bearer <jwt>` header issued by App Bridge.

- Worker fetches Shopify's JWKS route once at cold start, caches in memory (TTL 1h).
- Verifies JWT signature (RS256) against JWKS.
- Verifies claims: `iss` is `https://<shop>.myshopify.com/admin`, `aud` is the app's API key, `exp` > now, `nbf` < now.
- Extracts `dest` claim -> shop domain -> looks up tenant in D1.
- If tenant missing or kill_switch=on -> return 403.

### App uninstall webhook

- Topic: `app/uninstalled`, HMAC-verified.
- Action: delete tenant secret from Secrets Store, mark D1 row `status=uninstalled` (soft delete — retain log history for 30d), unschedule cron for this tenant.

---

## 4. Webhook receiver

### HMAC verification

Every webhook POST carries `X-Shopify-Hmac-Sha256` header. Worker computes `base64(hmac_sha256(body, app_secret))`, constant-time compares. Mismatch -> 401, no further processing.

### Per-merchant route

`POST /webhook/:shop_domain/:topic`

Topics handled in v1: `orders-create`, `orders-updated`, `refunds-create`, `app-uninstalled`, `shop-update`.

### 5-second response budget

Shopify retries on >5s response. Worker MUST:

1. Verify HMAC (sub-millisecond).
2. Push raw event onto Cloudflare Queue with key `tenant:<shop_domain>:event:<topic>:<event_id>`.
3. Return `200 OK` immediately.

Total budget target: <100ms p99.

### Queue mechanism — Cloudflare Queues (chosen)

**Choice:** Cloudflare Queues, not Durable Objects.

**Justification:**
- Native producer/consumer with at-least-once delivery and configurable retries (3 attempts, exponential backoff, then DLQ).
- 1M ops/month free tier covers tens of thousands of orders/day across all tenants.
- Built-in batching (consume up to 100 events per Worker invocation) cuts CPU cost.
- Durable Objects add per-tenant statefulness we don't need at the webhook layer; D1 already holds per-tenant state with cheaper reads.

DLQ -> `ops-review` escalation: events failing after 3 attempts get tagged in D1 `failed_events` table and the tenant gets a Gmail digest record.

### Notification fan-out on webhook fire

When an `orders/create` event clears the queue and is processed:

1. Orchestrator runs the daily-ops dispatch (inventory check -> shipping handoff or backorder).
2. Notification dispatch:
   - **If merchant has live SSE chat session open (heartbeat within 5min):** push `order_received` event over SSE -> App Bridge Toast fires + chat scroll-to-bottom shows the auto-summary message.
   - **Else:** queue a Gmail digest record. Digest emits at next 15-min boundary (batches multiple events into one email).
3. If posture=`pre_approve` AND a write is needed: surface action card in chat (if open) OR send single approval email (if not). Both surfaces carry the same `action_id`; whichever the merchant clicks first wins, the other expires.

---

## 5. Cron sweep

### Configuration

`wrangler.toml`:

```toml
[triggers]
crons = ["*/15 * * * *"]
```

15-min default cadence. Per-tenant override stored in D1 (`cron_cadence_min`); high-volume tenants can opt into 1-min sweeps via embedded UI toggle (Worker filters tenants whose `cron_cadence_min` divides current minute).

### What the sweep does

For each active tenant (not paused, not uninstalled):

1. Read `last_run_at` from D1.
2. Query Shopify Admin GraphQL: `orders(query: "updated_at:>=${last_run_at}")` with pagination.
3. Diff against `processed_event_ids` in D1 to dedupe vs webhook deliveries.
4. For each new/changed order, enqueue same as webhook path (same orchestrator code).
5. Process any retry-eligible items from `failed_events` table.
6. Process `tag:refund-requested` sweep (refunds sub-agent — separate cadence).
7. Persist `last_run_at = now()` on clean exit.

### Why cron + webhooks (both)

Webhooks fire instantly but miss events during Shopify outages or transient Worker errors. Cron is the safety net — catches everything within 15min worst case. Dedupe via `processed_event_ids` (D1 unique constraint on `tenant_id + event_id`) ensures no double processing.

### State

D1 table `tenant_sweep_state`:
- `tenant_id` PK
- `last_run_at` TIMESTAMP
- `sweep_count` INT
- `last_error` TEXT NULLABLE
- `cron_cadence_min` INT default 15

---

## 6. Chat endpoint (SSE streaming)

### Route

`POST /chat/:shop_domain`

Body:
```json
{
  "message": "string",
  "conversation_id": "uuid",
  "client_msg_id": "uuid"
}
```

### Flow

1. Verify session JWT (per §3).
2. Verify `:shop_domain` matches `dest` claim in JWT.
3. Load tenant config from D1 (posture, kill_switch, anthropic_key_owner).
4. If `kill_switch=on` -> return SSE with single error event + close.
5. Load conversation history from D1 (last 20 turns, capped at 60K tokens).
6. Open SSE response.
7. Call Anthropic Messages API with `stream: true`:
   - system = daily-ops orchestrator system prompt + per-tenant config injection
   - messages = history + new user message
   - tools = scoped to tenant posture (see §7)
   - max_tokens, temperature: see §7
8. Forward Anthropic SSE deltas to client SSE channel.
9. On `tool_use` block:
   - If reversibility=N AND posture=`notify_only`: pause stream, emit `action_proposed` SSE event with action card payload, persist `pending_action` row in D1, close stream with status `awaiting_approval`. Frontend renders approve/deny buttons. Merchant click hits `POST /chat/:shop_domain/approve` which resumes by feeding `tool_result` back to Anthropic.
   - If reversibility=Y OR posture=`auto_execute`: execute tool, feed `tool_result` back to Anthropic, continue streaming.
   - If posture=`pre_approve`: same as `notify_only` but the approval card ALSO emits a Gmail approval email; whichever surface approves first wins.
10. On stream end: persist full conversation turn to D1 (user msg + assistant msg + tool calls).

### Reversibility classification

Reversibility=N tool calls (write actions, always gated when posture is not auto_execute):
- `shopify.refund.create`
- `shopify.fulfillment.create`
- `shopify.order.tag.add` (when tag is `ops-review`, `backorder`, or any merchant-visible tag)
- `gmail.send` (any outbound customer email)
- `shopify.draft_order.create`

Reversibility=Y tool calls (reads + internal-only writes, never gated):
- `shopify.order.read`, `shopify.customer.read`, `shopify.inventory.read`
- `shopify.order.tag.add` when tag is internal-only (e.g., `internal:processed`)
- `gmail.draft.create` (creates a draft for operator review — does not send)

### SSE event types emitted to UI

- `delta` — text token from Claude
- `tool_use_start` — Claude is about to call a tool
- `tool_use_result` — tool returned (only in auto modes)
- `action_proposed` — write action gated, awaiting approval (`action_id`, summary, payload)
- `action_approved` / `action_denied` — after approval click
- `action_executed` — write completed
- `error` — terminal stream error
- `done` — clean stream end

---

## 7. Anthropic API wiring

### Model recommendation: Claude Sonnet 4.6

**Default:** `claude-sonnet-4-6-20250929` (or current Sonnet 4.6 stable).

**Justification:**
- Daily-ops is structured tool-use over well-defined sub-agent prompts — Sonnet handles this at near-Opus quality.
- Cost: Sonnet 4.6 is ~5x cheaper than Opus 4.7 per token. For per-order processing (~2K input + 500 output tokens typical), Sonnet runs $0.012/order vs Opus $0.063/order.
- Latency: Sonnet streams faster — better for chat UX inside the embedded iframe.

**When to escalate to Opus 4.7 (1M context):**
- Tenant config flag `model_tier=premium` (paid tier upsell).
- Specific tool-use ambiguity cases (e.g., merchant asks "should I refund this?") — daily-ops orchestrator can fork to Opus for reasoning-heavy turns. v2.

### System prompt assembly

At Worker cold start:
1. Read daily-ops `SKILL.md` from bundled assets (embedded at build time via `wrangler.toml` `[assets]`).
2. Read each sub-agent `SKILL.md` (inventory/shipping/comms/refunds).
3. Concatenate into a single system prompt with `<sub_agent>` XML tags per sub-skill.
4. Cache in Worker memory.

Per-request, append per-tenant injection block:

```
<tenant_config>
shop_domain: {shop}
posture: {notify_only|pre_approve|auto_execute}
gmail_account: {address}
notification_email: {address}
last_run_at: {timestamp}
escalation_tag: ops-review
</tenant_config>
```

### Tool definitions exposed per posture

| Tool | notify_only | pre_approve | auto_execute |
|---|---|---|---|
| shopify reads (orders, customers, inventory) | Y | Y | Y |
| shopify.order.tag.add (internal tags) | Y | Y | Y |
| shopify.order.tag.add (visible tags) | Gated | Gated | Y |
| shopify.fulfillment.create | Gated | Gated | Y |
| shopify.refund.create | Gated | Gated | Gated (always — Rule 18) |
| gmail.draft.create | Y | Y | Y |
| gmail.send | Gated | Gated | Y (transactional only) |
| ops-review escalate (add tag) | Y | Y | Y |

"Gated" = action requires approval surface; "Y" = direct execute.

Note: refunds are ALWAYS gated regardless of posture in v1. Operator anxiety dictates that money-out actions never auto-execute.

### Per-tenant API key model: hybrid

**Recommended:** Hybrid model.

- **Free tier (default):** PrimoLabs-pooled Anthropic key. Soft cap at $5/mo of API spend per tenant (~400 orders/mo at Sonnet 4.6 rates). Beyond cap -> tenant gets nag to upgrade or BYO.
- **Pro tier:** Tenant brings own Anthropic key, stored in Cloudflare Secrets `anthropic_key:<shop_domain>`. Removes spend cap. Tenant pays Anthropic directly; PrimoLabs charges flat SaaS fee.
- **Enterprise tier (v2):** PrimoLabs-managed key with negotiated Anthropic volume pricing, billed-through.

**Why hybrid:** Pure pooled = PrimoLabs eats spend risk at scale. Pure BYO = friction at onboarding ("get an Anthropic key" is the #1 churn point). Hybrid lets onboarding be one-click free trial, with explicit upgrade path.

### API config

- `max_tokens`: 4096 (chat); 2048 (orchestrator)
- `temperature`: 0.3 (orchestrator — deterministic dispatch); 0.5 (chat — natural voice)
- `retry policy`: 3 attempts, exponential backoff 1s/3s/9s, on 429/500/502/503/504; on 4xx other than 429 -> fail loud
- `timeout`: 60s per Anthropic call; chat SSE total budget 120s

---

## 8. Automation posture system

### Three postures

| Posture | Reads | Internal writes (tags) | Visible writes (fulfillment, send) | Money writes (refund, label buy) |
|---|---|---|---|---|
| **notify_only** | Auto | Auto | Surface card to UI, await approve | Surface card + always require approve |
| **pre_approve** | Auto | Auto | Surface card to UI + Gmail email, await approve | Surface card + Gmail + always require approve |
| **auto_execute** | Auto | Auto | Auto (transactional comms only) | Surface card — refunds ALWAYS gated |

### v1 default: `notify_only` — justification

The operator's load-bearing anxiety driver is "I don't want autonomous automation by default. I want visibility, control, and a trust ramp."

`notify_only` is the trust ramp:
- Agent does all the reading, classification, drafting, and decision-making.
- Every write — even sending the shipped-notification email — surfaces as an action card.
- Merchant either clicks Approve in the embedded chat (one tap), or ignores it.
- Over weeks of approving, merchant builds confidence the agent's calls are right.
- Then merchant manually graduates (in embedded UI) to `pre_approve` or `auto_execute`.

Anything else as default contradicts the anxiety driver.

### Per-merchant override

D1 column `tenants.posture` (default `notify_only`). Editable from embedded chat command (`/posture pre_approve`) or settings panel. Change is immediate; in-flight pending actions retain the posture they were created under.

### Graduation criteria

**v1:** Manual only. Merchant toggles in UI. No auto-graduation.

**v2 (deferred):** Auto-graduation candidate signal: if a tenant has >50 approved actions in a category (e.g., shipped-notification emails) with <2% reversal rate, surface "ready to auto" upsell. Still requires explicit click.

### Reversibility=N actions ALWAYS surface to UI

Even in `auto_execute`, these never auto-fire in v1:
- `shopify.refund.create` (money out)
- `shopify.fulfillment.create` with label purchase (money out via Shippo, v2 anyway)
- Customer email outside the transactional whitelist (anything not in: order_received, backorder_notice, shipped_notice)

---

## 9. Embedded chat notification surface

### Two channels, same event vocabulary

| Event type | App Bridge Toast (in-app) | Gmail digest (out-of-app) |
|---|---|---|
| `order_received` | Toast "New order #1234 from {first_name}" + auto-summary chat msg | Batched into 15-min digest |
| `action_proposed` | Toast "Approval needed" + chat card | Single email per action (no batching for approvals) |
| `action_executed` | Toast "Refund issued" (info) | Daily digest |
| `ops_review_escalated` | Toast "Needs review" + chat card | Immediate email |

### App Bridge Toast API

Worker -> SSE -> frontend -> `app.toast.show({message, isError, duration})`.

Frontend maintains long-lived SSE connection while embedded app is open. Heartbeat every 30s. If heartbeat fails, frontend reconnects; Worker treats >5min gap as "offline".

### Gmail digest cadence

- Default: every 15 min, batched, only if there are events.
- Approval emails: NOT batched, fire immediately (these are blocking the merchant).
- Daily digest at 7am tenant-local time: previous day's summary (X orders processed, Y emails sent, Z actions awaiting approval).
- Configurable in embedded UI.

### Notification dedupe

Each event has a unique `event_id`. When dispatching:
1. Check Worker memory cache (LRU, 5min TTL) for `event_id`.
2. If seen: skip.
3. If not: dispatch to BOTH surfaces (Toast if live, digest queue regardless), insert `event_id` into cache.

Critical: the Toast and the Gmail digest record for the same `event_id` carry the same `action_id` — clicking approve in either resolves the action atomically (D1 unique constraint on `action_id`).

---

## 10. Multi-tenant routing

### Secrets storage

Cloudflare Secrets Store, namespace `shopify-app-prod`:

| Key pattern | Value |
|---|---|
| `shopify_token:<shop_domain>` | Shopify Admin API access token |
| `gmail_refresh:<shop_domain>` | Gmail OAuth refresh token (per-tenant) |
| `anthropic_key:<shop_domain>` | Tenant-owned Anthropic key (only present if Pro tier) |
| `app_secret` | Shopify app shared secret (global, HMAC verification) |
| `anthropic_key_pooled` | PrimoLabs pooled Anthropic key (global, free tier) |

### Tenant config (D1)

Table `tenants`:

```
shop_domain          TEXT PK
posture              TEXT default 'notify_only'
kill_switch          INT default 0
notification_email   TEXT
gmail_account        TEXT
anthropic_key_owner  TEXT default 'pooled'  -- 'pooled' | 'byo'
cron_cadence_min     INT default 15
plan_tier            TEXT default 'free'    -- 'free' | 'pro' | 'enterprise'
status               TEXT default 'active'  -- 'active' | 'paused' | 'uninstalled'
created_at           TIMESTAMP
updated_at           TIMESTAMP
```

Sub-agent pause flags:

```
tenant_features
  shop_domain TEXT
  feature     TEXT  -- 'inventory' | 'shipping' | 'comms' | 'refunds'
  enabled     INT default 1
  PK (shop_domain, feature)
```

### Onboarding flow

1. Merchant finds app in Shopify App Store -> click Install.
2. OAuth grant (§3).
3. First load of embedded app: setup wizard (3 screens):
   - Screen 1: Confirm notification email (defaults to shop's billing email).
   - Screen 2: Connect Gmail (OAuth to operator's Gmail account; refresh token stored).
   - Screen 3: Confirm posture (default `notify_only`, explained as trust ramp).
4. Smoke test prompt: "Want to test with a $0.01 test order?" -> if yes, Worker creates draft order in tenant's Shopify, triggers the order_received pipeline, surfaces approval card. Merchant clicks approve -> confirms shipping mark + transactional email send works -> marks onboarding complete.
5. If smoke fails: surface error in chat with troubleshoot link, offer to retry or contact operator.

---

## 11. Kill switch

Four layers of kill, increasing granularity:

### Global kill (operator-level)

Cloudflare environment var `ROOK_DAILYOPS_PAUSED=1`. Worker checks at every cron tick + every chat request. If set -> cron skips ALL tenants, chat returns SSE error event + closes. Operator sets via `wrangler secret put` or dashboard.

Use case: emergency halt during incident, before rolling fix.

### Per-tenant kill

`tenants.kill_switch=1` in D1. Toggled from embedded UI ("Pause Agent" button in settings panel) or via chat command (`/pause`).

Cron skips this tenant. Chat returns a paused-mode message ("Agent paused. Type /resume to reactivate.").

Webhooks STILL accepted (200 OK, queued, but orchestrator skips processing).

### Sub-agent granular pause

`tenant_features` table. Pause specific sub-agent (e.g., "Pause refunds only").

UI: toggles in settings. Useful when merchant wants comms automated but wants to hand-control refunds.

### Shopify tag kill (dev mode)

If shop has tag `tag:dev-mode` (set via Shopify admin metafield or shop tag), orchestrator skips entirely. Honored for shops doing platform migration / sandbox work.

---

## 12. Observability

### Cloudflare logs (free tier)

- Worker request logs: every request logged for 24h, queryable via `wrangler tail`.
- Cron execution logs: every tick logged with tenant count + duration.

### Structured JSON log per MCP call

Conforms to existing `log_schema.json` shipped with daily-ops skill. Every Anthropic tool_use that hits Shopify/Gmail emits one JSONL record:

```json
{
  "ts": "2026-05-21T14:32:11Z",
  "tenant": "tenant-1.myshopify.com",
  "conversation_id": "uuid",
  "tool": "shopify.order.tag.add",
  "params": {...redacted PII...},
  "result_status": "success|escalated|failed",
  "latency_ms": 124,
  "posture": "notify_only",
  "action_id": "uuid"
}
```

Storage: D1 table `mcp_logs` for queryable last 30d; Cloudflare R2 for cold archive after 30d.

### `wrangler tail` for real-time debug

Operator runs `wrangler tail --format=json` during incident, sees live request stream filtered by tenant.

### Daily digest

Cron job at 7am tenant-local sends `Daily Summary — {date}` email:
- Orders processed: N
- Emails sent: N
- Actions awaiting approval: N (with link)
- Errors / escalations: N (with details)
- Cost-to-date this month: $X (if BYO key, omitted on pooled)

---

## 13. Cost model

### Cloudflare free-tier headroom

- Workers: 100K requests/day free. At 50 req/order (chat + webhooks + tool calls), supports ~2K orders/day per account.
- Workers paid: $5/mo for 10M requests + 30M CPU-ms.
- Queues: 1M ops/month free; $0.40 per additional 1M.
- D1: 5M reads + 100K writes/day free. Comfortably covers 100s of tenants.
- Secrets Store: free.

### Anthropic API estimate per order processed

Average per-order processing (Sonnet 4.6 input $3/MTok, output $15/MTok):
- Orchestrator dispatch: ~2K input + 500 output = $0.006 + $0.0075 = $0.0135
- One sub-agent call (e.g., inventory): ~1K input + 300 output = $0.003 + $0.0045 = $0.0075
- Chat turns (avg 2/order in notify_only): ~3K input + 1K output x 2 = $0.018 + $0.03 = $0.048
- **Per-order total estimate: ~$0.07** (notify_only with merchant interaction)
- **Auto-execute: ~$0.02** (no chat interaction)

### Per-merchant monthly cost tiers

| Tier | Orders/day | Orders/mo | Anthropic | CF infra | **Total infra** |
|---|---|---|---|---|---|
| LOW | <10 | <300 | $6-$21 | ~$0 | **~$6-21** |
| MED | 10-50 | 300-1500 | $21-$105 | ~$0.50 | **~$21-105** |
| HIGH | 50-200 | 1500-6000 | $105-$420 | ~$2 | **~$107-422** |

### Recommended SaaS subscription pricing (if PrimoLabs-managed)

| Tier | Price/mo | Includes |
|---|---|---|
| Starter | $29 | LOW volume, pooled key, $5 Anthropic cap |
| Growth | $99 | MED volume, pooled key, $50 Anthropic cap |
| Pro | $299 | HIGH volume, BYO Anthropic key required |
| Enterprise | custom | SLA, dedicated infra |

### Shopify App Store revenue share

Shopify takes 0% on first $1M annual app revenue per partner (2024 policy), 15% after that. Above $1M tier 2 = 15%.

For the first ~$1M/year (~280 Growth subs), zero revenue share. After that, factor 15% into margin model.

### Margin model

At 100 active merchants split 60/30/10 across Starter/Growth/Pro:
- Revenue: 60 x $29 + 30 x $99 + 10 x $299 = $1,740 + $2,970 + $2,990 = **$7,700/mo**
- Infra cost (mid-estimate): ~$2,500/mo
- Gross margin: **~$5,200/mo (~68%)**
- Net of Shopify rev share: same (under $1M annual).

---

## 14. First-tenant onboarding checklist (Tenant 1)

Generic checklist — replace `tenant-1` with actual shop subdomain at execution.

1. **Pre-flight (operator):**
   - Confirm Shopify Partners app published in unlisted mode (review test).
   - Confirm Cloudflare Worker deployed to `app.{domain}` with prod env.
   - Confirm Anthropic pooled key has $50 prepay loaded.
   - Confirm Gmail OAuth client ID/secret configured.

2. **Install (merchant):**
   - Merchant clicks unlisted install link.
   - Approves Shopify scopes.
   - Lands in embedded setup wizard.

3. **Setup wizard (merchant):**
   - Step 1: confirm notification email.
   - Step 2: Gmail OAuth grant.
   - Step 3: confirm posture = `notify_only` (default; explained as trust ramp).

4. **Smoke test:**
   - Wizard offers $0.01 test order creation.
   - Merchant approves.
   - Worker creates draft order in Shopify, marks paid, fires order_received.
   - Inventory sub-agent runs (test SKU has stock=999 seeded).
   - Shipping sub-agent surfaces "Ready to fulfill" action card in chat.
   - Comms sub-agent surfaces "Send shipped notification?" card.
   - Merchant clicks Approve on both.
   - Worker writes fulfillment + tracking, sends Gmail to merchant's own address.
   - Wizard marks `onboarding_complete=true` in D1.

5. **Verify (operator + merchant together, 30-min sync call):**
   - Look at chat history — does it read natural?
   - Look at Gmail sent folder — is the email rendered correctly?
   - Look at Shopify order detail — is tracking attached?
   - Look at D1 `mcp_logs` — is every call logged with correct posture tag?

6. **Rollback if smoke fails:**
   - Operator instructs merchant to uninstall app from Shopify admin.
   - `app/uninstalled` webhook fires, Worker soft-deletes tenant row.
   - Operator manually cleans D1 + Secrets records (script `scripts/purge_tenant.ts`).
   - Diagnose via `wrangler tail` logs, fix, redeploy, restart from step 1.

---

## 15. Open questions for operator

1. **Anthropic key model — pooled vs BYO vs hybrid?**
   Recommendation: **hybrid** (free tier on pooled, Pro tier requires BYO). Locks unit economics, removes onboarding friction. Alternative: pooled-only with hard per-tenant cap — simpler but PrimoLabs eats overflow risk.

2. **Posture default — `notify_only` confirmed?**
   Recommendation: **`notify_only`**. Matches anxiety driver. Alternative: `pre_approve` if you want Gmail to be the primary surface and chat to be secondary. I don't recommend it — it doubles notification noise without adding control.

3. **24h approval timeout default behavior?**
   Options:
   - (a) Re-notify (default — gentle nudge, no escalation)
   - (b) Auto-escalate to `ops-review` tag + operator email
   - (c) Auto-deny (silent drop, no action taken)
   Recommendation: **(a) re-notify at 24h, then (b) escalate at 72h, then (c) auto-deny at 7d**. Three-tier escalation.

4. **Cron cadence default — 15-min or faster?**
   Recommendation: **15-min default, 1-min opt-in for HIGH tier**. Free Worker tier handles 15-min comfortably; 1-min is a paid Pro feature.

5. **Domain — `app.primolabs.ai` or `shop.primolabs.ai` or other?**
   Operator to lock. Sub-domain affects Shopify Partners app registration. (Personal recommendation: `shop.primolabs.ai` reads cleaner than `app.`.)

6. **Listing model — public App Store vs unlisted at v1?**
   Recommendation: **unlisted at v1**, public after 5 paying tenants prove the smoke test holds. Shopify review process for public listing takes ~2 weeks and requires hardened error handling we should validate first.

---

## 16. Out of scope for v1

Explicit non-goals — defer to v2 unless escalated:

- **Embedded App frontend.** Separate spec, separate dispatch. This doc is backend only.
- **Stripe direct refunds.** Rule #18 opt-in v2. v1 issues Shopify draft refunds only.
- **Shippo rate-shop + label buy.** Rule #18 opt-in v2.
- **Klaviyo marketing flows.** Gmail covers v1 transactional. Klaviyo v2.
- **SMS notifications.** v2 (Twilio MCP, opt-in).
- **Multi-region failover.** Cloudflare's global anycast covers basic geo; active-active multi-region is v3.
- **Auto-graduation between postures.** Manual toggle only in v1.
- **Advanced analytics dashboard.** v1 has daily digest email + structured logs queryable via wrangler. Real dashboard v2.
- **Multi-language support.** English only v1.
- **Webhook-to-Webhook forwarding.** No outbound webhooks to merchant systems v1.
- **Custom tool definitions per tenant.** All tenants get the same daily-ops tool surface in v1.

---

**End of spec.**
