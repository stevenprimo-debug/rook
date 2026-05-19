---
name: SEO Keyword Research — AMA Template
description: |
  Scaffold an Anthropic Managed Agent that takes a seed keyword and clusters
  related queries, estimates intent (informational / transactional /
  navigational / commercial-investigation), and surfaces content gaps relative
  to competitor SERPs. Powered by Exa MCP. Single-agent (not a multi-phase
  squad), interactive chat UI by default. Owner agent: seo-specialist.
type: skill
category: ama-template
parent: ama-templates
version: "1.0.0"
voice: SYSTEM-DOMINANT
trigger: >
  Fire when customer says: SEO keyword research, find content gaps, cluster
  keywords, competitor SERP analysis, keyword universe, build keyword strategy.
inherits:
  - ama_definition: ama-definition.md
  - slot_glossary: slots.md
---

# SEO Keyword Research — AMA Template

## Overview

Single-agent AMA, Exa MCP. Customer provides a seed keyword; agent runs 3-5
Exa searches to build a keyword universe, clusters by intent, ranks
competitor URLs returned by Exa, identifies content gaps with citations.

## How to use

1. Customer asks "build me an SEO research agent" or trigger phrase
2. Skill asks for slots (default Exa MCP credentials, output format preference)
3. Skill writes filled CLI command to `_FROM_CLAUDE/YYYY-MM-DD-seo-keyword-research-deploy.sh`
4. Customer deploys: `ant beta:agents create ...` + `ant beta:environments create ...` + `ant beta:sessions start ...`
5. Customer interacts with the AMA in chat — feeds seed keywords, gets clustered results with gap analysis

## Owner agent

seo-specialist invokes this skill when customer wants autonomous keyword
research. seo-specialist's in-session work is lighter (quick checks, single-page
audits); this AMA handles deep keyword universe building.

## Output

- Keyword cluster table: cluster name / representative keywords / estimated intent / gap indicator
- Ranked content gap opportunities with brief justifications
- Citations to actual Exa-returned competitor URLs (never fabricated)
- Search trail log (every Exa query the agent issued)

## Guardrails (in the system prompt)

- Never fabricate volume / difficulty numbers (no access to volume data; say so)
- Deduplicate keywords across clusters
- Disambiguate ambiguous seeds before proceeding (e.g., "apple" = fruit or tech?)
- Log every Exa search query
- Cite actual URLs only — no hallucination
- When presenting gaps, cite which competitor pages were analyzed and what they lacked

## Success criterion (universal)

Customer's SEO content strategy gets sharper with less manual research time.
The cleanest deployment is the one where the customer goes from "what should
I write about?" to "here are 12 content gaps ranked by opportunity" in under
five minutes per seed keyword.

## Cross-references

- Source: Anthropic AMA library reference (2026-05-15)
- Parent: `skills/templates/ama-templates/README.md`
- Owner agent: `agents/seo-specialist/SKILL.md`
- Pairs with searchfit-seo skill suite (in-session counterparts for ad-hoc work)
