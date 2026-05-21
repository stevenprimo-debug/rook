---
name: Dispatch Log
description: >
  APPEND-ONLY table of every cross-agent dispatch chief-of-staff has issued. Pairs with
  `idea_log.md` (what came in) — this is what went OUT. One row per dispatch. Per
  `_CLAUDE.md` Section 2 — IMMUTABLE rows; only append.
type: memory
date: 2026-05-20
confidence: stated
ai-first: true
---

## For future Claude (TL;DR)

Every cross-agent dispatch (DEPLOY or ASSIGN) appends a row here. Source of truth for "who did chief-of-staff call?" Used by:
- librarian's weekly digest to track dispatch volume per agent
- new chief-of-staff sessions to see who's been busy and who's idle
- post-mortems to trace "where did this work originate?"

**Row format:**

```
YYYY-MM-DD HH:MM | <from-agent> | <to-agent> | <dispatch-type> | <one-line brief> | <outcome-or-pending>
```

**Dispatch types:**
- `DEPLOY` — sub-agent spawned in main session
- `ASSIGN` — brief written for later pickup
- `HANDOFF` — work transferred mid-session (e.g. sales-director → account-manager after close)
- `ESCALATE` — gated decision sent upstream for confirm

---

## Log

| Row | Timestamp | From | To | Type | Brief | Outcome |
|-----|-----------|------|-----|------|-------|---------|
| 1 | 2026-05-20 18:00 | chief-of-staff | chief-of-staff | LOCKED | "Dispatch log scaffolded. Next row is row 2." | n/a |

<!--
APPEND BELOW THIS LINE. Never edit rows above.

Example formats:

| 2 | 2026-05-21 09:14 | chief-of-staff | designer | DEPLOY | "Refresh pricing-page hero, brand voice tight" | shipped 09:47, see designer/memory/2026-05-21-pricing-hero.md |
| 3 | 2026-05-21 11:02 | chief-of-staff | software-dev-team | ASSIGN | "Webhook sig validation for X webhook" | brief at assignments/2026-05-21-webhook-sig.md, pending |
| 4 | 2026-05-21 14:33 | sales-director | account-manager | HANDOFF | "Customer X closed; renewal in 11 months" | account-manager confirmed receipt 14:35 |
-->
