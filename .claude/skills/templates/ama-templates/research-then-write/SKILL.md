---
name: Research-then-Write — AMA Template (Multi-agent)
description: |
  Scaffold an Anthropic Managed Agent that produces sourced long-form
  articles in Notion. Three sequential sub-agent phases: Researcher (Exa
  search → 8-15 high-quality sources with summaries) → Writer (long-form
  article with inline citations, every claim traces to a source) → Editor
  (factual consistency check, grammar, Sources section, citation
  matching). Auto-publishes to Notion as Draft. Owner agents:
  content-strategist + copywriter.
type: skill
category: ama-template
parent: ama-templates
version: "1.0.0"
voice: SYSTEM-DOMINANT
trigger: >
  Fire when customer says: research and write an article, long-form content
  generation, sourced article, Notion publishing, content pipeline, article
  on {topic}, blog post with citations.
inherits:
  - ama_definition: ama-definition.md
  - slot_glossary: slots.md
---

# Research-then-Write — AMA Template

## Overview

Three-phase multi-agent AMA: Researcher → Writer → Editor → Notion publish.
Webhook or cron-triggered. Customer feeds a topic + target length + audience +
Notion database ID; AMA produces a fully-cited article published as Notion
Draft.

**Key differentiator vs deep-researcher AMA:** this one PUBLISHES output to a
customer destination (Notion). deep-researcher returns synthesis to the chat;
this one ships finished articles to a CMS pipeline.

## How to use

1. Customer asks "build me a content pipeline" or trigger phrase
2. Skill asks for slots (Notion database ID, default target length, audience profile, style notes)
3. Skill writes filled CLI command to `out/YYYY-MM-DD-research-then-write-deploy.sh`
4. Customer deploys + creates environment + sets webhook/cron trigger
5. Each invocation produces one article published to Notion as Draft

## Owner agents

- **content-strategist** — invokes when customer wants autonomous long-form content production
- **copywriter** — pairs with this for the in-session writing work; this AMA handles the autonomous publishing pipeline

Dispatch chain: CREATIVE DIRECTOR → MARKETING → content-strategist invokes this AMA (per `dispatch_chains.MARKETING` — brand voice locked upstream before article generation).

## Input payload (JSON)

```json
{
  "topic": "string (required)",
  "target_length": "number (default 1500 words)",
  "audience": "string (default 'general professional')",
  "notion_database_id": "string (required)",
  "style_notes": "string (optional — tone, format preferences)"
}
```

## Three phases

| Phase | Agent | Output |
|---|---|---|
| 1 — Researcher | Searches Exa for 8-15 high-quality sources; structured research brief | Research brief (title + URL + date + 2-3 sentence summary per source) |
| 2 — Writer | Long-form article matching target_length; inline citations; every claim traces to Phase 1 source | Markdown draft with citations |
| 3 — Editor | Factual consistency check vs brief; grammar; tone alignment; Sources section append | Final polished article + Sources section |
| Publish | Notion MCP creates page in specified database | Notion page (Status=Draft, Generated=today) |

## Guardrails

- Never invent sources, statistics, quotes
- Prefer primary sources / peer-reviewed / reputable publications
- Discard duplicates by canonical URL
- If fewer than 5 credible sources found: log warning, proceed
- If topic ambiguous or potentially harmful: create Notion page titled `[ESCALATION] {topic}` with explanation, STOP
- Every inline citation has matching Sources entry and vice versa
- Notion write failure → retry once → log article content in error output for manual recovery
- Log each phase completion as structured JSON comment in Notion page

## Anti-patterns

Per CD voice-spine § 4 — the AMA's drafted articles MUST avoid:
"elegant," "premium," "luxury," "delightful," "magical," "elevate" (verb),
"leverage" (verb-as-filler), "deep dive," "as an AI."

## Success criterion (universal)

Customer's content calendar fills itself with cited, brand-voice-aligned
long-form articles. The cleanest deployment is the one where the customer
opens Notion to a queue of polished drafts ready for review + publishing.

## Cross-references

- Source: Anthropic AMA library reference (2026-05-15)
- Parent: `skills/templates/ama-templates/README.md`
- Owner agents: `agents/content-strategist/SKILL.md`, `agents/copywriter/SKILL.md`
- Sister AMA: `deep-researcher` (chat-based; no Notion publish)
- Upstream dispatch chain: CREATIVE DIRECTOR → MARKETING → content-strategist → this AMA
- Pairs with `copywriter` in-house skill (for in-session writing variants)
