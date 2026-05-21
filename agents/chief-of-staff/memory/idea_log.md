---
name: Idea Log
description: >
  APPEND-ONLY ledger of every spitball, hunch, capture, or unstructured idea routed through
  chief-of-staff. Source of truth for "did this idea get logged?" Every DEPLOY / ASSIGN / PARK
  decision appends a row here. Per `_CLAUDE.md` Section 2 — IMMUTABLE rows; only append.
type: memory
date: 2026-05-20
confidence: stated
ai-first: true
---

## For future Claude (TL;DR)

This is the canonical idea-log. Every spitball gets one row, no exceptions. New entries at the BOTTOM. Never rewrite existing rows. If an idea is reassessed, append a new row referencing the old one ("UPDATED 2026-XX-XX, see row N above").

**Row format:**

```
YYYY-MM-DD HH:MM | <status> | <target-agent> | "<one-sentence summary>" | <follow-up trigger>
```

**Status values:**
- `DEPLOY` — agent spawned in this session
- `ASSIGN` — brief written to `assignments/YYYY-MM-DD-<slug>.md` for later pickup
- `PARK` — logged with a specific re-surface trigger (NEVER default to "next week" — use an idea-specific event)
- `LOCKED` — decision made, no further action
- `UPDATED` — supersedes a prior row (cite row number)

**Trigger discipline (per `feedback_parked_items_must_resurface.md`):**
PARK requires an idea-specific re-surface event ("when sales-director next runs a campaign", "if customer-X renewal comes within 60 days"). Never use generic cadences like "next Monday" — that pattern was deprecated for letting parked items silently die.

---

## Log

| Row | Timestamp | Status | Target | Summary | Trigger |
|-----|-----------|--------|--------|---------|---------|
| 1 | 2026-05-20 18:00 | LOCKED | chief-of-staff | "Idea log scaffolded. Next row is row 2." | n/a |

<!--
APPEND BELOW THIS LINE. Never edit rows above. Increment Row number monotonically.

Example formats:

| 2 | 2026-05-21 09:14 | DEPLOY | designer | "Customer wants new pricing page hero." | n/a — work shipped same session |
| 3 | 2026-05-21 11:02 | ASSIGN | software-dev-team | "Webhook signature validation for X." | "next sprint" — brief at assignments/2026-05-21-webhook-sig.md |
| 4 | 2026-05-21 14:33 | PARK | sales-director | "Test pricing-page lift on inbound landing page." | "when sales-director next runs an outbound campaign" |
-->
