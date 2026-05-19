---
name: Meta Ads Creative Critic — AMA Template
description: |
  Scaffold an Anthropic Managed Agent that analyzes Meta Ads creative
  performance and generates new variant briefs informed by winning hooks.
  Powered by meta-ads MCP. Pulls account/campaign/ad-set/ad-level data
  (spend, impressions, CTR, CPC, CPM, ROAS, thumbstop ratio, hook rate),
  ranks creatives by KPI, extracts winning patterns, outputs Creative
  Scorecard + 3-5 variant briefs per winning ad. Owner agents:
  marketing-director, social-media-manager.
type: skill
category: ama-template
parent: ama-templates
version: "1.0.0"
voice: SYSTEM-DOMINANT
trigger: >
  Fire when customer says: analyze my Meta Ads, ad creative critic, Facebook
  Ads performance, ad variant briefs, what's working on Meta, creative
  scorecard, thumbstop ratio analysis.
inherits:
  - ama_definition: ama-definition.md
  - slot_glossary: slots.md
---

# Meta Ads Creative Critic — AMA Template

## Overview

Single-agent AMA, meta-ads MCP. Customer connects their ad account; agent
pulls performance data (last 90 days default), ranks creatives by ROAS or
CTR, identifies top 20% winners + bottom 20% underperformers, extracts
winning hook phrases / CTA types / emotional tones / formats, generates
3-5 new variant briefs per winning ad.

## How to use

1. Customer asks "build me an ad creative critic" or trigger phrase
2. Skill asks for slots (default KPI, date range, ad account selection mode)
3. Skill writes filled CLI command to `_FROM_CLAUDE/YYYY-MM-DD-meta-ads-creative-critic-deploy.sh`
4. Customer deploys + starts interactive session
5. Customer feeds ad-account selections; agent returns Creative Scorecard + variant briefs

## Owner agents

- **marketing-director** — campaign-level strategy + variant prioritization
- **social-media-manager** — short-form creative + platform-native variant briefs

Either agent invokes this skill when customer wants autonomous Meta Ads
analysis. In-session these agents handle ad-hoc questions; this AMA handles
full performance analysis runs.

## Output

- Top 5 winners with reasons (hook phrase, format, audience alignment)
- Bottom 5 underperformers with diagnosed weaknesses
- Aggregate pattern summary (winning emotional tones, format mix, CTA types)
- 3-5 variant briefs per winning ad with: suggested headline, primary text (with hook), recommended format, CTA, source insight

## Guardrails

- Never fabricate metrics — every number comes from meta-ads MCP response
- If data incomplete or API call fails: tell customer exactly what's missing
- No sensitive billing/PII storage beyond current analysis
- Always cite which winning ad inspired each variant (reference ad ID or name)
- Ambiguous requests → ask clarifying question, never guess
- Log every meta-ads tool call for customer audit

## Anti-patterns (per CD voice-spine § 4 — applies to variant briefs)

Variant brief headlines / primary text must NOT use forbidden vocabulary:
"elegant," "premium," "luxury," "delightful," "magical," "elevate" (verb),
"leverage" (verb-as-filler), "deep dive," "as an AI." The AMA respects this
even though it runs autonomously.

## Success criterion (universal)

Customer's ad CPA goes down because winning patterns inform every new
creative. The cleanest deployment is the one where the customer stops
guessing what works and starts iterating on data.

## Cross-references

- Source: Anthropic AMA library reference (2026-05-15)
- Parent: `skills/templates/ama-templates/README.md`
- Owner agents: `agents/marketing-director/SKILL.md`, `agents/social-media-manager/SKILL.md`
- Pairs with `copywriter` in-house skill (for the variant brief writing itself)
- Upstream dispatch chain: CREATIVE DIRECTOR → MARKETING → this AMA (if customer voice/brand matters; recommend CD dispatch before deploy)
