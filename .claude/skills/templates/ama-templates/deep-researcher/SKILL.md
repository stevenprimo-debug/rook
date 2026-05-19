---
name: Deep Researcher — AMA Template
description: |
  Scaffold an Anthropic Managed Agent that conducts multi-step web research
  with source synthesis and citations. Given a question or topic, decomposes
  into 3-5 sub-questions, runs targeted searches, reads sources in full
  (not skim), extracts specific claims + data points + quotes with
  attribution, synthesizes structured report with inline citations and
  confidence-and-gaps section. Single-agent, no MCP servers required —
  uses the built-in agent_toolset web search. Owner agent: deep-researcher.
type: skill
category: ama-template
parent: ama-templates
version: "1.0.0"
voice: SYSTEM-DOMINANT
trigger: >
  Fire when customer says: deep research, research this topic, comprehensive
  research, source synthesis, research report, multi-source analysis,
  literature review.
inherits:
  - ama_definition: ama-definition.md
  - slot_glossary: slots.md
---

# Deep Researcher — AMA Template

## Overview

Single-agent AMA. No external MCPs — uses the built-in web search in
`agent_toolset_20260401`. Decomposes a research question into 3-5
sub-questions, runs targeted searches per sub-question, reads sources in
full, extracts claims with attribution, synthesizes a structured report.

## How to use

1. Customer asks "build me a deep research agent" or trigger phrase
2. Skill writes filled CLI command to `_FROM_CLAUDE/YYYY-MM-DD-deep-researcher-deploy.sh`
3. Customer deploys + starts interactive session
4. Customer feeds questions/topics; agent returns structured reports with citations

## Owner agent

deep-researcher invokes this skill when customer needs autonomous deep
research with full source synthesis. In-session deep-researcher does
lighter ad-hoc lookups; this AMA handles thorough multi-step research.

## Output structure (per system prompt)

- Decomposition: 3-5 sub-questions
- Per-sub-question synthesis with inline citations
- Direct quotes with attribution
- "Confidence & gaps" section noting source disagreements + coverage holes
- Skeptical posture: explicitly flags uncertainty rather than papering over

## Guardrails

- Prefer primary sources, official docs, peer-reviewed work over blogs and aggregators
- Read sources in full — don't skim
- Cite every non-obvious claim inline
- Flag source disagreements explicitly; explain which is more credible and why
- Never confident-sounding prose over uncertainty

## Success criterion (universal)

Customer gets a research report they can trust and cite. The cleanest
deployment is the one where the customer's research time goes from days
to one good question fed to the AMA + a polish pass.

## Cross-references

- Source: Anthropic AMA library reference (2026-05-15)
- Parent: `skills/templates/ama-templates/README.md`
- Owner agent: `agents/deep-researcher/SKILL.md`
- Pairs with enterprise-search skill suite (in-session counterparts for ad-hoc lookups)
