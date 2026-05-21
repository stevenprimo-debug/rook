# Master Shopify App — Embedded Frontend Spec (v1)

**Date:** 2026-05-21
**Owner:** chief-of-staff (operator)
**Surface:** Embedded frontend only. Backend = `2026-05-21-shopify-app-backend-spec.md`.
**Runtime:** Shopify-embedded React iframe, Cloudflare Pages hosted.
**Status:** Draft for operator lock-in.

---

## 1. Executive summary

The frontend is what the merchant sees inside Shopify admin — a Polaris-native embedded app whose primary surface is a chat window where the merchant talks to their store. v1 ships five tabs (Chat, Orders, Settings, Activity Log, Pricing), an SSE-streaming chat with inline approve/reject action cards, three-tier posture switcher, big-red-button kill switch, and the Shopify Billing API integration for Starter/Pro/Premium subscription. Default posture is `notify_only` — the merchant approves writes one tap at a time until trust is earned. Deferred to v2: SMS, mobile-app embed, multi-language, bulk ops in chat, custom workflow builder.

---

## 2. UX principles

These are derived from operator anxiety, not generic SaaS heuristics. Every screen is checked against them.

- **Visibility over autonomy.** The agent's reasoning is rendered inline as it streams. Merchant never sees "your store is doing something" — they see "the agent looked at order #1234, found stock=0, proposed tagging it backorder, here's why." Hidden work = no trust.
- **Action buttons over typed commands.** The merchant never types `/approve refund-abc123`. The agent surfaces an Approve/Reject card. Typed commands exist (`/pause`, `/posture pre_approve`) but are escape hatches, not the primary path.
- **Context over abstraction.** When a write is proposed, the affected order is rendered next to the chat (right rail) — line items, customer, address, fulfillment status. The merchant decides with the order in front of them, not from memory.
- **Trust ramp over autopilot.** Default `notify_only`. Auto-graduation does not ship in v1. Merchant must manually click "I trust this — switch to pre-approve" after watching it work.
- **Polaris-native, not third-party bolt-on.** Every component is Polaris React. No custom buttons, no custom typography, no Tailwind. The App must read like a first-party Shopify feature.

---

## 3. Information architecture

App navigation (Polaris `Frame` + left `Navigation`):

| Tab | Route | Role |
|---|---|---|
| **Chat** (default landing) | `/` | Primary surface — conversation with the store |
| **Orders** | `/orders` | Timeline view of orders processed by the agent, ops-review queue |
| **Settings** | `/settings` | Posture, kill switch, sub-agent toggles, notification prefs, key config |
| **Activity log** | `/activity` | Structured JSON viewer per MCP call, filterable |
| **Pricing** | `/pricing` | Read-only subscription state, upgrade flow via Shopify Billing |

Top bar (Polaris `TopBar`) is persistent across all tabs and shows:
- Shop name (left)
- Posture indicator pill — green `Notify Only` / amber `Pre-Approve` / red `Auto Execute`
- Global kill switch button (top right, icon only until hovered)
- Unread escalations badge (red dot on a bell icon when ops-review items are pending)

---

## 4. Chat UI spec

The chat is the product. Everything else is configuration.

### Layout

Two-column Polaris `Page` layout:
- **Left (60%):** Message list + input box
- **Right (40%):** Context rail — renders the order/customer being discussed; empty state shows agent status (idle, thinking, waiting for approval)

### Message list

- Polaris `Card` per turn, no chat-bubble custom styling — flat Polaris cards stacked.
- Assistant messages stream token-by-token via SSE (native `EventSource`).
- User messages render immediately on submit (optimistic UI).
- Tool-use start renders an inline status row: spinner + "Looking up order #1234" + collapsible JSON preview.
- Tool-use result collapses by default; merchant clicks to expand the raw JSON.
- Conversation history paginates older turns above the fold (Polaris `Pagination`, 20 turns per page, infinite scroll up).

### Input box

- Multi-line `TextField` with auto-grow up to 6 rows.
- Submit on Cmd/Ctrl+Enter; plain Enter inserts newline.
- Autocomplete drawer on `/` for slash commands (`/pause`, `/resume`, `/posture`, `/orders`, `/help`).
- Disabled state when `kill_switch=on` with inline reason.

### Empty state

First-load state: full-card empty state with headline "Talk to your store." and helper text "Ask anything. The agent will look it up, propose actions, and wait for your approval."
Three suggested-prompt buttons:
- "Any orders need attention?"
- "What shipped today?"
- "Walk me through what you do."

### Streaming SSE handler

- Single long-lived `EventSource` per chat session, opened on tab mount.
- Reconnect with exponential backoff on disconnect (1s, 3s, 9s, then 30s steady).
- Heartbeat ping every 30s; missing 2 pings = drop and reconnect.
- Event types handled (per backend section 6): `delta`, `tool_use_start`, `tool_use_result`, `action_proposed`, `action_approved`, `action_denied`, `action_executed`, `error`, `done`.
- On `action_proposed`: stream pauses, action card injects into message list, context rail updates with affected order.

---

## 5. Action card pattern

This is the load-bearing UX. Every reversibility=N write surfaces here.

### Trigger

Backend section 6 emits an `action_proposed` SSE event when posture is `notify_only` or `pre_approve` and the agent proposes a gated tool call. Frontend pauses the stream and renders an inline `Card` with `sectioned` Polaris layout.

### Card contents

- **Header:** action type icon + plain-English summary ("Issue $42.50 refund to Tenant 1 customer Jane D.")
- **Body block 1 — proposed change:** before/after diff styled as Polaris `DataTable` (line item, old value, new value)
- **Body block 2 — affected order context preview:** order number, customer name, total, current tags, current fulfillment status
- **Body block 3 — MCP call preview:** collapsed by default; expand shows the exact `shopify.refund.create` payload as syntax-highlighted JSON
- **Body block 4 — expected outcome:** one-line description of what the agent will do AFTER approval ("Refund issued, customer emailed via Gmail, order tagged `refunded`")

### Buttons

Three Polaris `Button`s in a `ButtonGroup`:
- **Approve** (primary, green) — fires `POST /chat/:shop/approve` with the signed action token
- **Reject** (default) — fires deny endpoint; agent acknowledges in next stream turn ("Got it — not refunding. Anything else?")
- **Escalate** (plain) — adds `ops-review` tag, sends operator a Gmail, removes from active queue

### Token security

Each action card carries an `action_id` and an HMAC-signed action token (backend-generated, 24h expiry, single-use). Click handlers send the token back — backend validates HMAC + checks token-already-spent table in D1. Stale tokens render a Polaris `Banner` with "This approval expired — refresh chat to re-propose."

### Mobile / small viewport

Polaris `Stack` reflows the three buttons to full-width stacked. Card tap targets at least 44px. Tested at 375px width (smallest mobile Shopify admin).

---

## 6. App Bridge integration

App Bridge 4.x React hooks. Single `Provider` wrap at app root with API key from build env.

| Capability | Use |
|---|---|
| **Session token** | `useAppBridge().idToken()` on every backend request; refreshed automatically every 60s |
| **Toast API** | `app.toast.show(...)` triggered by SSE `action_executed` events; non-blocking ambient confirmation |
| **Modal API** | `app.modal.show(...)` for kill-switch confirmation, posture-change confirmation, uninstall flow |
| **Resource picker** | `app.resourcePicker({type: 'Order'})` invoked from chat input toolbar — merchant picks an order, frontend injects `@order/1234` into prompt |
| **Navigation API** | `app.navigate(...)` for deep links — clicking an order number in chat opens that order in Shopify admin in a new tab |

Loss-of-token handling: if `idToken()` throws, frontend renders a full-page Polaris `Banner` "Session expired — reload the app" with a reload button. No silent retry — token loss almost always means the merchant got logged out of Shopify.

---

## 7. Notification surfaces

Priority order — frontend respects backend's notification dispatch but owns the in-app surfaces.

1. **In-app Toast (App Bridge).** Fires when the user is actively in the App. Ambient, dismissable, no action required. Used for `order_received`, `action_executed`, `ops_review_escalated`. Toast click navigates to relevant chat turn.
2. **Browser tab badge count.** Document title updates to `(3) Master Shopify App` when there are unread escalations. Cleared on tab focus + chat scroll-to-bottom.
3. **Gmail digest.** Backend-owned. Frontend has no involvement except a "Preview today's digest" button in Activity log.
4. **Optional SMS.** v2 only. Settings UI shows the toggle as disabled with a "Coming v2" tooltip.

### Dedupe

Backend tracks `last_notified_at` per event. Frontend POSTs to `/chat/:shop/ack` when a toast is shown OR an escalation badge is clicked. Backend updates D1; the Gmail digest queue drops events that already got an in-app ack within the last 5min.

---

## 8. Settings UI

Single Polaris `Page` with `Layout.Section`s. Each section is a discrete concern.

### Posture selector

Three Polaris `ChoiceList`-styled radio cards (custom Polaris pattern, not a dropdown):
- **Notify Only** — agent proposes, you approve every write. (Default. Recommended for first 4 weeks.)
- **Pre-Approve** — agent proposes via chat + Gmail email; whichever you click first wins.
- **Auto Execute** — agent executes most writes; refunds and money-out still always gated.

Each card carries a one-line tradeoff sentence + an "Edit" link to a modal explaining what changes.

Changing posture fires a Polaris `Modal` confirmation: "You are switching to Auto Execute. The agent will send shipped notifications without asking. Confirm?" — single confirm button, no nag.

### Per-sub-agent toggle

Polaris `Card` with four `Toggle` rows: Inventory, Shipping, Comms, Refunds. Off = sub-agent skipped entirely (backend honors `tenant_features.enabled=0`).

### Kill switch

Big red Polaris `Button` with `destructive` variant, full-width inside its own `Card`. Label: "Pause Agent." Click opens `Modal` requiring the merchant to type the word "pause" before the Confirm button enables. On confirm, fires `/settings/kill` and posture indicator flips to red `Paused` across all tabs.

Resume button replaces Pause when paused; same modal pattern but no typed confirmation (resuming is the safe direction).

### Notification preferences

Toggle rows: In-app (always on, disabled toggle), Email digest (default on), Email approval requests (default on for `pre_approve` posture only), SMS (disabled, "Coming v2").

### Anthropic key configuration

Two Polaris `Card`s side by side:
- **Pooled (default for Starter/Free)** — shows current month usage as Polaris `ProgressBar` against the $5 cap, with upgrade nudge at over 80% used.
- **BYO key (Pro/Premium)** — `TextField` with masked input, validation on save, plus a "Test key" button that fires a one-token Anthropic call to confirm.

### Connected accounts

Gmail OAuth row: shows connected address + scopes + last refresh timestamp. "Disconnect" button (with confirmation modal) and "Re-authenticate" button. No other OAuth providers in v1.

---

## 9. Activity log UI

Polaris `Page` with a `Filters` header + `IndexTable`.

### Filters

- Sub-agent (select: Inventory / Shipping / Comms / Refunds / All)
- Action type (select: Read / Write-internal / Write-visible / Money / All)
- Date range (Polaris `DatePicker` ranged)
- Status (Success / Escalated / Failed / Pending)

### Table

Columns: timestamp, sub-agent, tool name, target (order #/customer), status badge, action_id.

Row click opens a Polaris `Modal` with the full structured JSON (see backend section 12) — syntax-highlighted, copy-button, with PII automatically redacted in the rendered view (customer email shows `j***@***.com`).

### Export

"Export CSV" button — frontend builds CSV from currently filtered rows (max 10K), downloads via `Blob`. Larger exports return a "Request full export" banner that queues a backend job.

### Daily digest preview

A `Card` above the table renders the same content the merchant gets emailed each morning. Useful for "did I miss something yesterday?" without checking Gmail.

---

## 10. Onboarding flow

Target: 5 minutes from install-click to first approved smoke-test action.

### Step 1 — Welcome (15 seconds)

Polaris `Page` with three-card `Layout.Section`:
- "Talk to your store." (chat icon)
- "Approve every action." (lock icon)
- "Earn trust, then automate." (graduation icon)

Single "Get started" primary button.

### Step 2 — Gmail OAuth connection (60 seconds)

Polaris `Card` with "Connect Gmail" button. Click opens OAuth popup. On callback, frontend polls backend for `gmail_connected=true`, then advances.

If user closes popup or rejects scopes: render `Banner` with "Gmail is required for the agent to email customers. Retry?" + retry button + "Skip for now" (disables Comms sub-agent until reconnected).

### Step 3 — Set initial posture (30 seconds)

Same three radio cards from Settings section 8, but pre-selected to `notify_only` with the other two grayed out and a footnote "You can change this anytime — we recommend starting here for the first 4 weeks."

Continue button.

### Step 4 — Notification preferences (30 seconds)

Pre-filled with sensible defaults (in-app on, email digest on, SMS disabled). Single "Looks good" button advances.

### Step 5 — First-action walkthrough (2 minutes)

"Want to test with a $0.01 test order?" — Yes button creates a draft order in the merchant's store (backend section 10), fires the order_received pipeline, surfaces an action card in chat with an inline tutorial overlay ("This is an action card. Click Approve to test.").

Merchant approves -> success state with confetti animation + "You're done. Talk to your store anytime."

Skip button on this step jumps to a final "done" state with sample-chat pre-populated.

### Step 6 — Done state

Lands on Chat tab with a starter message from the assistant: "Hi — I'm watching your store. Right now I'm in Notify Only mode, so I'll ask before every write. Try `What can you do?` to start."

---

## 11. Pricing UI + Shopify Billing API

Three Polaris `Card`s side by side, current plan highlighted with Polaris `Badge`.

### Tiers

| Tier | Price | Volume | Key | Model |
|---|---|---|---|---|
| **Free** | $0 | under 100 orders/mo | Pooled, $5 Anthropic soft cap | Sonnet 4.6 |
| **Pro** | $99/mo | Unlimited | BYO Anthropic key required | Sonnet 4.6 |
| **Premium** | $299/mo | Unlimited | BYO Anthropic key | Opus 4.7 + priority support |

### Upgrade flow

"Upgrade to Pro" button fires Shopify Billing API `appSubscriptionCreate` mutation with the recurring charge spec. Shopify redirects merchant to confirmation screen. On approve, Shopify redirects back to `/billing/callback` -> backend marks `plan_tier=pro` in D1 -> frontend re-renders with new plan highlighted.

Usage charges (overage beyond pooled-key soft cap on Free tier): handled via Shopify Billing `usageRecord` API. Backend tracks Anthropic spend, posts usage records, Shopify bills merchant via their existing Shopify billing relationship.

Downgrade flow: confirmation modal warning about feature loss, then `appSubscriptionCancel` mutation.

### Contextual upgrade prompts

Free tier nag triggers (Polaris `Banner` at top of Chat tab):
- At 80% Anthropic cap: "You've used 80% of this month's allotment. Upgrade to Pro for unlimited."
- At over 100 orders/mo: "Your store is growing — Pro removes the order limit."
- On attempted use of Opus 4.7 tier features: "This requires Premium. Upgrade?"

---

## 12. Tech stack

| Layer | Choice |
|---|---|
| Framework | React 18 + TypeScript |
| Design system | Polaris React (latest) |
| Shopify integration | App Bridge React + hooks |
| Data fetching | TanStack Query (cache + invalidation) |
| Streaming | Native `EventSource` API (SSE) |
| Build | Vite |
| Hosting | Cloudflare Pages |
| Testing | Vitest (unit), Playwright (e2e smoke) |
| Lint | ESLint + Shopify ESLint config |

No Tailwind, no custom UI library, no styled-components — Polaris owns all styling. Bundle target: under 250KB gzipped initial load.

---

## 13. Shopify Partners + App Store listing prep

### App listing copy

- **Title:** _(pending operator lock — see section 16)_
- **Tagline (60 char max):** "Talk to your store. Approve every action."
- **Long description (200 words):** describes the trust-ramp model, notify_only default, the four sub-agents (Inventory / Shipping / Comms / Refunds), the embedded chat surface, and the BYO-key option for Pro/Premium tiers.
- **Screenshots (6 required, 1600x900):** 1) chat empty state, 2) action card mid-flow, 3) settings posture selector, 4) activity log, 5) onboarding step 1, 6) pricing page.
- **Demo video (optional but recommended):** 60s screencap of install -> onboarding -> first action approved.

### Required URLs

- App URL: `https://app.{domain}/dashboard`
- Allowed redirect URLs: `https://app.{domain}/oauth/callback`
- Privacy policy URL: _(flag out-of-scope — operator/legal must draft before public listing)_
- Terms of service URL: _(flag out-of-scope — same)_
- Support email: _(operator to lock — see section 16)_

### Required scopes

Cross-reference backend section 3: `read_orders`, `read_customers`, `read_inventory`, `read_fulfillments`, `write_orders`, `write_fulfillments`, `write_draft_orders`, optional `read_shopify_payments_disputes`.

### App Bridge embedded config

`shopify.app.toml`:
- `embedded = true`
- `application_url = "https://app.{domain}/dashboard"`
- `redirect_urls = ["https://app.{domain}/oauth/callback"]`
- `[access_scopes].scopes = "<list above>"`

### Pricing tiers in Shopify Partners

Three plans registered as `appSubscription` definitions: Free, Pro ($99/mo), Premium ($299/mo). Free trial set to 14 days on Pro/Premium.

### GDPR webhooks (mandatory for App Store approval)

Three webhook endpoints implemented in backend (cross-reference backend spec — flag if missing):
- `customers/data_request` — return JSON of all customer data agent has touched in last 30d
- `customers/redact` — purge specified customer's mentions from `mcp_logs` and conversation history
- `shop/redact` — purge entire tenant after 48h grace period post-uninstall

### Submission checklist (Shopify review)

- [ ] App installs cleanly on a fresh dev store
- [ ] OAuth flow completes without errors
- [ ] Embedded App loads under 3s (Shopify hard requirement)
- [ ] All required webhooks respond under 5s with valid HMAC verification
- [ ] GDPR webhooks implemented and tested
- [ ] Privacy policy + ToS URLs live and reachable
- [ ] Pricing tiers documented in listing copy match Shopify Billing API definitions
- [ ] App uninstalls cleanly and triggers `shop/redact` after grace period
- [ ] Screenshots match current UI (no stale designs)
- [ ] Support email is monitored

---

## 14. Cost model (frontend-specific)

### Cloudflare Pages

- Free tier: 500 builds/month, unlimited bandwidth, unlimited requests.
- A typical week ships about 5 builds — well under the limit.
- Cost contribution: **$0** at v1 scale.

### Shopify revenue share

Shopify Partner Program 2024 policy:
- First $1M annual partner revenue: **0% revenue share**
- $1M+: 15% revenue share

Per-tier net revenue (during 0% share period):
- Free: $0 in, about $1-3 Anthropic cost out -> negative per merchant, recovered via upgrade conversion
- Pro: $99/mo in, $0 Anthropic cost (BYO) -> **$99/mo net**
- Premium: $299/mo in, $0 Anthropic cost (BYO) -> **$299/mo net**

### Break-even merchant count

Assuming about $200/mo fixed operator cost (Cloudflare paid tier + Anthropic pooled buffer + domain):
- **Break-even at about 3 Pro subscribers** OR **1 Premium subscriber**.

Once partner revenue crosses $1M/year (about 840 Pro subs), factor in 15% Shopify cut.

---

## 15. First-tenant onboarding playbook ("Tenant 1")

Sanitized. Replace `tenant-1` with actual merchant subdomain at execution.

1. **Pre-flight (operator, day before):**
   - Confirm Shopify Partners app deployed in unlisted mode.
   - Confirm Cloudflare Pages build deployed and reachable at `app.{domain}/dashboard`.
   - Confirm App Bridge configured with correct API key.
   - Smoke-test the App on the operator's own dev store first.

2. **Invite to private listing:**
   - In Shopify Partners dashboard, generate a private install link for the app.
   - Send to Tenant 1 via Gmail with a 3-line install instruction.

3. **Install + onboarding (Tenant 1):**
   - Click install link, approve OAuth scopes.
   - Walk through section 10 onboarding flow (Welcome -> Gmail OAuth -> Posture -> Notifications -> Smoke test).
   - Land on Chat tab.

4. **Smoke test (joint, 15-min sync call):**
   - Operator on Zoom share with Tenant 1.
   - Trigger $0.01 test order via the onboarding wizard.
   - Confirm Toast fires + chat scroll-to-bottom shows agent summary.
   - Confirm action card renders with full context preview.
   - Click Approve.
   - Confirm Shopify order shows fulfillment + tracking attached.
   - Confirm Gmail sent folder has the shipped-notification email.
   - Open Activity log -> confirm 3-4 rows logged with correct posture tag.

5. **Success criteria:**
   - All four smoke-test steps complete with no errors.
   - Tenant 1 self-reports "I understood what was happening at every step."
   - No backend errors in `wrangler tail` during the session.

6. **Rollback if smoke test fails:**
   - Tenant 1 uninstalls App from Shopify admin (single click).
   - `app/uninstalled` webhook fires, backend soft-deletes tenant row.
   - Operator runs `scripts/purge_tenant.ts` for full cleanup.
   - Diagnose via `wrangler tail` + Activity log structured JSON.
   - Fix root cause, redeploy, restart from step 2.

---

## 16. Open questions for operator to lock

1. **App name / branding.**
   Options:
   - (a) "ROOK Shopify" — leverages ROOK vault name recognition, ties product to operator lineage.
   - (b) "PrimoLabs Shopify" — leverages PrimoLabs umbrella brand, leaves room for non-Shopify products under same brand.
   - (c) Brand-new name (e.g., "Storekeeper," "Floor," "Maitre") — clean slate, no operator-baggage, but requires fresh brand investment.
   **Recommendation: (c) brand-new** — Shopify App Store merchants don't care about ROOK or PrimoLabs; they want a name that signals the product's job. Brand-new clears trademark + SEO and reads naturally in screenshots. Defer specific name selection to a CREATIVE DIRECTOR -> DESIGN dispatch.

2. **Free tier soft cap — $5/mo pooled Anthropic or stricter.**
   Options:
   - (a) $5/mo soft cap (backend default — about 400 orders/mo at Sonnet 4.6 pricing).
   - (b) $3/mo cap — tighter unit economics, more upgrade pressure.
   - (c) Order-count cap (e.g., 50 orders/mo) — simpler to explain than dollar cap.
   **Recommendation: (a) $5/mo with (c) 100-orders/mo as a hard secondary cap.** Two caps, whichever hits first. The dollar cap protects operator from spend surprise; the order cap is the upgrade story for merchants.

3. **Premium tier ($299) model — Opus 4.7 vs Sonnet 4.6 + faster SLA.**
   Options:
   - (a) Premium = Opus 4.7 (1M context) for genuinely harder reasoning turns.
   - (b) Premium = same Sonnet 4.6 but with priority support, dedicated Slack channel, faster bug response.
   - (c) Both — Opus 4.7 + priority support.
   **Recommendation: (c) both.** Opus is the technical differentiator; priority support is the business one. At $299/mo there's margin for both. Most Premium merchants won't actually need Opus — but having it justifies the price gap from $99 Pro.

---

## 17. Out of scope for v1

- **SMS notifications.** v2 — Twilio integration via backend. Settings toggle ships disabled.
- **Mobile-native Shopify Mobile app embed.** v2 — requires separate App Bridge config + mobile-specific layouts. v1 is desktop Shopify admin only.
- **Multi-language localization.** v2 — English only. Polaris supports localization via its i18n provider but no translated strings ship v1.
- **Bulk order operations in chat.** v2 — v1 chat handles one order at a time. ("Refund all backorders from Tuesday" returns a "please do these one at a time" message.)
- **Custom workflow builder UI.** v3 — v1 ships fixed daily-ops sub-agents. Custom sub-agent definitions per tenant deferred.
- **In-app analytics dashboards.** v2 — v1 has Activity log (raw) + Daily digest (email). Charted dashboards deferred.
- **Multi-store management.** v2 — v1 is single-store-per-install. Multi-store operators install once per shop.
- **White-label / agency reseller mode.** v3 — v1 brands as a single App; reseller program deferred.
- **Marketplace integrations** (Etsy, Amazon, eBay). v3 — Shopify-only v1.

---

**End of spec.**
