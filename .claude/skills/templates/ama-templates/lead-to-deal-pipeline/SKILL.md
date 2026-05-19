---
name: Lead-to-Deal Pipeline — AMA Template
description: |
  Scaffold an Anthropic Managed Agent that automates the full lead-to-deal
  handoff: Apollo prospect search → HubSpot enrich + create/update with
  lifecycle stage → Slack sales-team notification → Calendly booking link
  to prospect. Single agent, 4 MCPs (apollo + hubspot + slack + calendly).
  Distinct from sales-triage-squad (inbound enrichment) — this is OUTBOUND
  prospecting end-to-end. Owner agents: prospecting-agent, sales-outreach.
type: skill
category: ama-template
parent: ama-templates
version: "1.0.0"
voice: SYSTEM-DOMINANT
trigger: >
  Fire when customer says: outbound prospecting automation, lead-to-deal
  pipeline, automate cold prospecting, Apollo + HubSpot + Slack handoff,
  prospect to booking, autonomous SDR pipeline, Calendly booking flow.
inherits:
  - ama_definition: ama-definition.md
  - slot_glossary: slots.md
---

# Lead-to-Deal Pipeline — AMA Template

## Overview

End-to-end outbound prospecting. Operator gives the AMA search criteria
(ICP, industry, company size, geography), AMA runs Apollo search,
enriches + creates in HubSpot with correct lifecycle stage, notifies the
sales team in Slack with concise prospect summary, sends Calendly
booking link to the prospect via HubSpot email OR to the rep via Slack.

## How is this different from sales-triage-squad?

| | sales-triage-squad | lead-to-deal-pipeline |
|---|---|---|
| Direction | Inbound (leads come to you) | Outbound (you go find them) |
| Phase 1 starts | Existing lead email | Apollo search criteria |
| Phase 2 | Scoring (HOT/WARM/COLD) | HubSpot lifecycle assignment |
| Phase 3 | Outreach draft | Slack team handoff + Calendly link |
| Cadence | Cron every 30 min on incoming lead queue | Operator-triggered on demand |

A customer with both inbound + outbound flows deploys BOTH templates.

## Owner agents

- **prospecting-agent** — primary owner; runs the search-to-pipeline work
- **sales-outreach** — secondary; handles the booking-link follow-up if prospect doesn't respond to initial Calendly invite

## How to use

1. Customer says "build me an outbound prospecting pipeline" or trigger phrase
2. Skill asks for slots (ICP definition, Slack channel, Calendly link, HubSpot lifecycle stage targets)
3. Skill writes filled CLI command to `_FROM_CLAUDE/YYYY-MM-DD-lead-to-deal-pipeline-deploy.sh`
4. Customer deploys + creates environment + starts session
5. Operator feeds search criteria; AMA runs end-to-end handoff

## Guardrails (per system prompt)

- Verify contact data before creating records
- Deduplicate against existing HubSpot contacts before creating new ones
- Log every action taken
- Surface errors or missing data clearly for human review

## Cost economics

Operator-triggered (not cron). Typical run: 50 prospects through full
pipeline = ~30 min session-time. At Sonnet-class AMA pricing
(~$0.08/session-hour): ~$0.04 per 50-prospect batch. Even at 100 batches/mo
= $4/mo. Effectively free compared to manual SDR time.

## Success criterion (universal)

Customer's sales team wakes up to Slack notifications with qualified
prospects already in HubSpot, lifecycle stage set, Calendly invite sent.
Zero manual handoff between prospecting → enrichment → outreach. Sales
team's only job: take the booking call.

## Cross-references

- Source: Anthropic AMA library reference (2026-05-15)
- Parent: `skills/templates/ama-templates/README.md`
- Sister AMA: `sales-triage-squad` (inbound counterpart)
- Owner agents: `agents/prospecting-agent/SKILL.md`, `agents/sales-outreach/SKILL.md`
- Original spec source: 21st.dev "Lead-to-Deal Pipeline Agent" (Hakobyan, also archived in `.claude/memory/reference_21st_dev_catalog_2026-05-13.md`)
