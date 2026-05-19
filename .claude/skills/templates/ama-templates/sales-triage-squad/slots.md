# Sales Triage Squad — Slot Glossary

> What the SKILL.md asks the customer before generating the deploy command.
> Required slots have no default; optional slots have defaults the customer
> can accept verbatim.

---

## Required slots

| Slot | What customer provides | Example |
|---|---|---|
| `{CUSTOMER_NAME}` | The customer's company name (appears in AMA name) | "Acme Corp" |
| `{CUSTOMER_SHORT_NAME}` | Lowercase slug for environment naming | "acme" |
| `{ICP_TITLE_FLOOR}` | Minimum title seniority for scoring | "Director+ titles, including VP, Head of, Chief" |
| `{ICP_COMPANY_SIZE_BAND}` | Target company size | "50–5000 employees" |
| `{ICP_INDUSTRIES}` | Comma-separated industries | "B2B SaaS, fintech, e-commerce" |
| `{ICP_TECH_STACK}` | Tech-stack signals for overlap scoring | "Shopify, HubSpot, Vercel, Supabase" |
| `{SLACK_CHANNEL}` | Where daily summaries land | "#sales-pipeline" |

## Optional slots (defaults provided)

| Slot | Default | Customer can override |
|---|---|---|
| `{CRON_SCHEDULE}` | "every 30 minutes during business hours, M-F 8am-6pm in {TIMEZONE}" | Yes — set custom cadence |
| `{CRON_EXPRESSION}` | `*/30 8-18 * * 1-5` | Yes — any valid cron |
| `{TIMEZONE}` | "America/Chicago" | Yes — IANA timezone string |
| `{MODEL_ID}` | `claude-sonnet-4-6` | Rare — only if customer has access to a different model |
| `{DEDUPE_DEAL_STAGE_FLOOR}` | "Qualified" | Yes — any HubSpot deal stage name |
| `{HUBSPOT_SCORE_PROPERTY}` | `lead_score` | Yes — match customer's HubSpot property name |
| `{HUBSPOT_TIER_PROPERTY}` | `lead_tier` | Yes — match customer's HubSpot property name |
| `{ICP_SOURCE_TIERS}` | "Tier 1: inbound demo request, Tier 2: content download, Tier 3: cold outbound reply" | Yes — customer's lead-source taxonomy |
| `{SENDER_VOICE_NOTES}` | "warm but direct, no jargon, mirror the recipient's industry vocabulary" | Yes — customer's brand voice; recommend dispatching CREATIVE DIRECTOR first if voice matters |
| `{AUTO_SEND_DEFAULT}` | `false` (draft-only) | Yes — set `true` for auto-send (NOT recommended without monitoring period) |
| `{HALT_THRESHOLD_PCT}` | `20` | Yes — % of enrichment failures that triggers halt |
| `{DATE}` | Today's date in `YYYY-MM-DD` | No — auto-filled |
| `{AGENT_ID_FROM_CREATE_COMMAND}` | Output of `ant beta:agents create` | No — customer pastes after create |
| `{ENV_ID_FROM_ENVIRONMENT_CREATE}` | Output of `ant beta:environments create` | No — customer pastes after env create |

## Pre-fill prompts (the SKILL asks in this order)

The SKILL.md asks slot questions in this sequence to minimize back-and-forth:

1. "What customer is this AMA for?" → fills `{CUSTOMER_NAME}` + auto-derives `{CUSTOMER_SHORT_NAME}` (lowercase, hyphens, no special chars)
2. "Define your ICP — title seniority floor, company size band, target industries, tech overlap signals?" → fills 4 slots in one prompt
3. "Slack channel for daily summaries?" → fills `{SLACK_CHANNEL}` (validate format starts with `#`)
4. "Lead source tiers — what's a Tier 1 source for you? Tier 2? Tier 3?" → fills `{ICP_SOURCE_TIERS}`
5. "Cron schedule — accept default (every 30 min, business hours M-F) or customize?" → fills `{CRON_EXPRESSION}` + `{TIMEZONE}`
6. "Voice notes for the drafted emails — accept the default or want to dispatch CREATIVE DIRECTOR first to lock the brand voice?" → fills `{SENDER_VOICE_NOTES}` OR triggers CD dispatch chain
7. "HubSpot dedupe gate — skip leads with existing deal at what stage or higher?" → fills `{DEDUPE_DEAL_STAGE_FLOOR}`
8. "Auto-send drafts, or draft-only for human review?" → fills `{AUTO_SEND_DEFAULT}` (strong recommend: draft-only for first 2 weeks of operation)
9. "Enrichment failure halt threshold — accept default 20% or adjust?" → fills `{HALT_THRESHOLD_PCT}`

## Defaults locked from Stack best practices

- **Draft-only by default.** Customer must explicitly opt into auto-send. Per `feedback_execute_dont_preamble.md` adjacent reasoning: irreversible actions (sending email) require explicit confirm.
- **HOT/WARM/COLD tier thresholds locked** (75 / 50 / 0). These are calibrated to typical B2B SaaS funnel conversion rates; customer can adjust but defaults work for most ICPs.
- **Forbidden vocabulary list inherits from CD voice-spine § 4.** Even though this AMA runs autonomously, its outputs (drafted emails) follow Stack voice rules.
- **Subject line personalization is mandatory.** Generic subjects ("Quick question", "Following up", "Touching base") are explicitly forbidden in the system prompt.
