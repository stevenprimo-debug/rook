---
name: Sales Triage Squad — AMA Template Generator
description: |
  Scaffold an Anthropic Managed Agent (AMA) that transforms raw inbound leads
  into scored, enriched contacts with ready-to-send personalized first-touch
  emails. Three-phase headless pipeline: Enrichment → Scoring → Outreach
  Drafting. Customer deploys via `ant beta:agents create` using their own
  Apollo / HubSpot / Slack / agentmail MCP credentials. Runs autonomously on
  cron (default every 30 minutes) or via webhook. Never uses preamble. The
  template scaffolds the AMA; the customer's MCPs power it.
type: skill
category: ama-template
parent: ama-templates
version: "1.0.0"
status: operational
voice: SYSTEM-DOMINANT
tools:
  - Read
  - Write
  - Edit
  - Bash
trigger: >
  Fire when the user says: build me a sales triage pipeline, automate inbound
  leads, scaffold a sales squad, set up a lead enrichment agent, build an AMA
  for sales, deploy a managed agent for outreach, triage inbound leads
  automatically, sales pipeline that runs itself, autonomous SDR.
inherits:
  - ama_definition: ama-definition.md
  - slot_glossary: slots.md
---

# Sales Triage Squad — AMA Template Generator

## Overview

This skill scaffolds an **Anthropic Managed Agent** — not an in-session agent.
The output is a deployable AMA definition the customer runs via the Anthropic
CLI. Once deployed, the AMA runs autonomously: every 30 minutes (or per
webhook), it pulls new leads, enriches them via Apollo, scores them, writes
back to HubSpot, drafts personalized first-touch emails, and posts the daily
summary to Slack.

Three sequential phases (single AMA orchestrates all three):

1. **Enrichment Agent** — Apollo lookup + HubSpot dedupe check (skip if contact already has deal ≥ Qualified) + HubSpot create-or-update
2. **Scoring Agent** — Weighted scoring (title 30% / company size 25% / industry 20% / tech overlap 15% / source 10%) → HOT (75-100) / WARM (50-74) / COLD (0-49) → write to HubSpot custom property
3. **Outreach Drafter Agent** — For HOT + WARM only: compose 3-5 sentence personalized email referencing real enrichment data, stage as draft via agentmail, never auto-send

## How to use

1. Customer says "build me a sales triage pipeline" or similar trigger phrase
2. Skill loads `ama-definition.md` (system prompt template) + `slots.md` (slot glossary)
3. Skill asks for slot fills:
   - ICP definition (title seniority, company size band, industry list, technology overlap signals)
   - Slack channel for daily summaries
   - Cron schedule (default: every 30 minutes during business hours)
   - Auto-send vs draft-only (default: draft-only — never auto-send without explicit override)
   - HubSpot custom property names for `lead_score` and `lead_tier`
   - Halt threshold for enrichment failures (default: 20%)
4. Skill writes the filled CLI command + system prompt to `out/YYYY-MM-DD-sales-triage-squad-deploy.sh`
5. Skill prints the deploy command for the customer to run
6. Customer runs `ant beta:agents create ...` using their Anthropic API key
7. Customer creates an environment via `ant beta:environments create ...`
8. Customer starts a session with the agent ID + environment ID; AMA begins running on schedule

## Prerequisites (customer-side)

- Anthropic CLI installed: `brew install anthropics/tap/ant`
- Anthropic API key with Managed Agents access (research-preview gated; customer must have access)
- MCP server credentials for: Apollo, HubSpot, Slack, agentmail
- HubSpot custom properties created: `lead_score` (number), `lead_tier` (enum: HOT/WARM/COLD)

If the customer doesn't have Managed Agents access yet, this skill outputs the
form URL (https://claude.com/form/claude-managed-agents) and stages the
deployment for after approval.

## Output deliverables

The skill writes three files:

1. `out/YYYY-MM-DD-sales-triage-squad-deploy.sh` — the full `ant beta:agents create` CLI command with all slots filled
2. `out/YYYY-MM-DD-sales-triage-squad-system-prompt.md` — the standalone system prompt (for review before deploy)
3. `out/YYYY-MM-DD-sales-triage-squad-runbook.md` — operator runbook covering: how to monitor the AMA, how to update the ICP, how to pause/resume, how to interpret the daily Slack summary

## Guardrails (baked into the AMA system prompt)

- Never fabricate enrichment data. Incomplete enrichment → flag as INCOMPLETE in HubSpot, note missing fields
- Never auto-send emails unless `auto_send: true` is explicitly in config (default: draft-only)
- Log every API call + decision (skip / score / draft) to structured JSON action log returned in final output
- If >X% of leads fail enrichment (X = customer-configured halt threshold), post Slack alert and halt the pipeline
- On any ambiguous company match or duplicate uncertainty, flag for human review in Slack — never guess

## Cost economics (surface to customer)

At Sonnet-class pricing (~$0.08/session-hour Managed Agents billing):
- Cron every 30 min × 8 business hours × 22 business days = ~352 session-hours/mo
- ≈ $28/mo at current Anthropic pricing
- Compared to manual SDR time at $60-80k loaded: obvious win

## Anti-patterns (refuse list)

- **Preamble in the AMA system prompt.** The AMA dispatches; no warm-up.
- **Generic subject lines.** "Quick question" or "Following up" — explicitly forbidden in the system prompt. Always personalized.
- **Auto-send without explicit customer opt-in.** Default is draft-staging.
- **Guessing on dedupe.** Ambiguous match → human review, never guess.
- **Forbidden vocabulary** per CD voice-spine § 4 — applies to drafted outreach emails: no "elegant," "premium," "delightful," etc.

## Success criterion (universal)

This skill succeeded when the AMA is deployed, running on schedule, and the
customer is reviewing well-personalized first-touch drafts in their agentmail
inbox each morning. The cleanest deployment is the one where the customer's
human time goes from "manually triaging leads" to "approving drafts and
hitting send."

## Cross-references

- Parent category: `skills/templates/ama-templates/README.md`
- AMA definition (system prompt template): `ama-definition.md`
- Slot glossary: `slots.md`
- Anthropic Managed Agents docs: https://claude.com/form/claude-managed-agents
- Owner agent: `agents/sales-director/SKILL.md` (sales-director invokes this skill when customer asks for autonomous lead triage)
- Sister AMA templates (pending build): customer-onboarding-squad, content-strategy-squad, code-review-squad, memory-audit-squad, rfp-response-squad
- Source: Anthropic AMA library reference — Sales Triage Squad example (2026-05-15)
