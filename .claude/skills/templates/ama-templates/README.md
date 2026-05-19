# AMA Templates — Anthropic Managed Agent Squad Library

> **Category:** Turnkey multi-agent pipeline definitions for the Anthropic
> Managed Agents (AMA) platform. Customers deploy these squads via
> `ant beta:agents create` using their own MCP credentials.

---

## What an AMA template is (and isn't)

| AMA template | In-session agent skill |
|---|---|
| Multi-agent pipeline (e.g., Enrichment → Scoring → Drafter) | Single agent invoked in a session |
| Deployed via `ant beta:agents create` CLI | Loaded via `Skill` tool at conversation time |
| Runs autonomously on cron or webhook | Runs when user invokes |
| Uses customer's OWN MCP credentials | Uses Stack-bundled tools |
| Cron-scheduled, headless, hands-off | Interactive, session-bound |
| Charged via Anthropic Managed Agents billing | Charged via the customer's Anthropic API usage |
| Examples: Sales Triage Squad, Code Review Squad | Examples: sow-template, nda-template, brainstorming |

**Both ship in this system.** Agents in the line know when to scaffold one
vs the other.

## How customers use these

1. Customer asks a Stack agent (typically chief-of-staff or the relevant domain agent — sales-director for Sales Triage, software-dev-team for Code Review) to spin up an autonomous pipeline.
2. The agent invokes the matching AMA template skill.
3. Skill asks for slot fills (ICP parameters, MCP credentials they want to wire, cron schedule, alerting channels).
4. Skill outputs the filled `ant beta:agents create` command + the system prompt body.
5. Customer runs the command. AMA spawns on the Anthropic Managed Agents platform.
6. AMA runs autonomously per its schedule, posts results to the configured channels.

## Why this category exists

Most agent products ship single agents. this agent ships **turnkey multi-agent pipelines as deployable templates.** This is a differentiator: customers get autonomous squads that operate without supervision, paying the Anthropic Managed Agents per-session-hour rate instead of staffing the work themselves.

## Catalog

| Squad | Status | Owner agent | Purpose |
|---|---|---|---|
| **sales-triage-squad** (4-phase multi-agent) | ✅ Live | sales-director | Enrichment → scoring → outreach drafting for inbound leads |
| **seo-keyword-research** (single agent) | ✅ Live | seo-specialist | Seed keyword → Exa search universe → clustered + intent-tagged + gap analysis |
| **deep-researcher** (single agent) | ✅ Live | deep-researcher | Topic → 3-5 sub-questions → multi-source synthesis with inline citations + confidence-and-gaps |
| **meta-ads-creative-critic** (single agent) | ✅ Live | marketing-director / social-media-manager | Meta Ads performance analysis → winning pattern extraction → 3-5 variant briefs per winner |
| **e-commerce-ops-squad** (4-agent multi-agent) | ✅ Live | shopify-agent | Inventory → Shipping (Shippo) → Communications (Klaviyo) → Refunds (Stripe) end-to-end |
| **research-then-write** (3-phase multi-agent) | ✅ Live | content-strategist / copywriter | Researcher (Exa) → Writer → Editor → publish to Notion as Draft |
| **lead-to-deal-pipeline** (single agent, 4 MCPs) | ✅ Live | prospecting-agent / sales-outreach | Apollo search → HubSpot enrich + lifecycle → Slack team notify → Calendly booking link |
| **cold-outreach-personalizer** (single agent, 3 MCPs) | ✅ Live | sales-outreach / prospecting-agent | Apollo + Clay enrichment → hyper-personalized first lines (<25 words) → MailerLite sequence trigger |
| customer-onboarding-squad | 🔴 To build | shopify-agent / chief-of-staff | Signup → provisioning → welcome flow |
| content-strategy-squad | 🔴 To build | content-strategist / marketing-director | (Subsumed by research-then-write — close as duplicate?) |
| code-review-squad | 🔴 To build | software-dev-team | Diff analysis → security scan → review comments |
| memory-audit-squad | 🔴 To build | librarian | Scheduled drift detection → digest writing → hook proposals |
| rfp-response-squad | 🔴 To build | sales-director / deep-researcher | RFP parse → answer drafting → compliance matrix |

## Template structure (every AMA template has these files)

```
ama-templates/<squad-name>/
├── SKILL.md           — meta-skill (when to invoke, what slots to ask)
├── ama-definition.md  — the AMA spec (system prompt + CLI command template)
├── slots.md           — slot glossary (what customer fills)
└── README.md          — overview for this specific squad
```

## Cost economics (worth surfacing to customer)

Anthropic Managed Agents billing (per public pricing): ~$0.08/session-hour at
Sonnet-class. A Sales Triage Squad running every 30 minutes for 8 hours/day
across 22 business days = ~352 session-hours/month ≈ $28/mo. Compared to a
human SDR ($60-80k loaded) doing the same enrichment-scoring-drafting work
manually, the math is obvious.

**Customer pricing for this system (the product subscription) covers the AMA templates
themselves; the customer pays Anthropic directly for AMA runtime.**

## Cross-references

- Anthropic Managed Agents docs: https://claude.com/form/claude-managed-agents (research preview gate, filed 2026-05-14)
- Sister category: `skills/templates/` (contracts: sow / nda / msa / proposal; operations: sop)
- In-house meta-skill: `skill-creator` (knows the AMA pattern as one of its output modes)
- Source: 2026-05-15 — turnkey multi-agent pipelines added to this system to expand agent capacity beyond single-session work
