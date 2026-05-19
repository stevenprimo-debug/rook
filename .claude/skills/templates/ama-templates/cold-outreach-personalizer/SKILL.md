---
name: Cold Outreach Personalizer — AMA Template
description: |
  Scaffold an Anthropic Managed Agent that researches prospects (Apollo +
  Clay), writes hyper-personalized cold-email first lines anchored to
  concrete verifiable details, then triggers the appropriate MailerLite
  sequence. Three MCPs (apollo + clay + mailerlite). Distinct from
  lead-to-deal-pipeline (which is full handoff) — this one specializes in
  the WRITING step at scale. Owner agents: sales-outreach, prospecting-agent.
type: skill
category: ama-template
parent: ama-templates
version: "1.0.0"
voice: SYSTEM-DOMINANT
trigger: >
  Fire when customer says: personalize cold outreach, first lines for emails,
  MailerLite sequence personalization, Clay enrichment + outreach,
  hyper-personalized first lines, cold email writer.
inherits:
  - ama_definition: ama-definition.md
  - slot_glossary: slots.md
---

# Cold Outreach Personalizer — AMA Template

## Overview

Specialized cold-outreach AMA. Researches each prospect (recent news,
funding, product launches, tech stack, LinkedIn activity), writes a
hyper-personalized first line under 25 words anchored to a concrete
verifiable detail, enriches in Clay, triggers MailerLite sequence.
Flags prospects with insufficient public data for manual review.

## How it differs from the other sales AMAs

| AMA | Specialty |
|---|---|
| sales-triage-squad | INBOUND — enrichment + scoring + draft outreach (HubSpot + agentmail) |
| lead-to-deal-pipeline | OUTBOUND full handoff — Apollo search → HubSpot lifecycle → Slack team → Calendly link |
| **cold-outreach-personalizer** (this one) | OUTBOUND personalization at scale — Apollo + Clay enrichment → hyper-personalized first lines → MailerLite sequence trigger |

Customer with diverse stack picks the right AMA per workflow. The three
templates compose well: lead-to-deal can hand off into cold-outreach-personalizer
for the personalization step.

## Owner agents

- **sales-outreach** — primary owner; the personalization writing is the core sales-outreach work
- **prospecting-agent** — secondary; some customers run the full Apollo + Clay flow under prospecting-agent before passing to sales-outreach

## How to use

1. Customer says "build me a cold outreach personalizer" or trigger phrase
2. Skill asks for slots (default MailerLite sequence ID, target first-line word count, voice notes)
3. Skill writes filled CLI command to `_FROM_CLAUDE/YYYY-MM-DD-cold-outreach-personalizer-deploy.sh`
4. Customer deploys + creates environment + starts session
5. Operator feeds prospect lists; AMA researches each, writes first lines, enriches in Clay, triggers MailerLite

## Output per prospect

- Research summary (1-2 lines)
- Personalized first line (<25 words, conversational, anchored to specific detail)
- Clay enrichment record updated
- MailerLite sequence triggered
- Flag for manual review if insufficient public data

## Guardrails

- First lines under 25 words
- Anchor every line to concrete, verifiable detail (never generic flattery)
- Tone: conversational, not salesy
- Insufficient public data → flag for manual review, do NOT fabricate
- Forbidden vocabulary (CD voice-spine § 4): "elegant," "premium," "luxury," "delightful," "magical," "elevate," "leverage" (verb-as-filler), "deep dive," "as an AI"

## Success criterion (universal)

Customer's cold-email reply rate goes up because every first line proves
human-level research effort. The cleanest deployment is the one where
prospects feel seen, not blasted.

## Cross-references

- Source: Anthropic AMA library reference (2026-05-15)
- Parent: `skills/templates/ama-templates/README.md`
- Sister AMAs: sales-triage-squad (inbound), lead-to-deal-pipeline (full outbound handoff)
- Owner agents: `agents/sales-outreach/SKILL.md`, `agents/prospecting-agent/SKILL.md`
- 21st.dev catalog reference: cold-outreach-personalizer entry
