---
name: metaprompt
source: https://github.com/anthropics/claude-cookbooks/blob/main/misc/metaprompt.ipynb
fetched: 2026-05-22
category: Responses & Prompt Engineering
rook-relevance: medium
rook-status: inherit-via-skill
---

# Metaprompt

## What it is

Use Claude to generate task-specific prompt templates. User describes their task + input variables; a long multi-shot meta-prompt (~6 examples across customer support, math tutoring, document analysis, function calling) teaches Claude to emit a structured instruction template with `{$VARIABLE_NAME}` placeholders. Three-stage generation: identify input variables → plan instruction layout → draft instructions. Includes scratchpad reasoning for complex tasks.

Output is a starting point, explicitly not optimal — designed to solve the blank-page problem.

## Key code/config

Generated templates use XML-tagged sections + `{$VAR}` placeholders. Variables positioned before lengthy content blocks; output requirements include justification-before-score for graded outputs.

Extraction:
```python
extract_between_tags("Instructions", metaprompt_response)
```

Cookbook uses Sonnet-4-6 for metaprompt generation, Haiku-4-5 for template testing.

## Measured improvements / costs

No quantitative metrics. Qualitative example shown (email drafting template).

## ROOK applicability

ROOK already has the official `prompt-builder` and `skill-creator` skills. Both cover the same "scaffold a prompt from scratch" need. The metaprompt cookbook predates skill-creator and overlaps significantly.

Where it might add: chief-of-staff dispatch-brief generation. When chief-of-staff writes an ASSIGN brief to a downstream agent, the brief shape is freeform. A metaprompt-style template generator could standardize brief shape across agents.

## Recommended action

**inherit-via-skill** — keep `prompt-builder` and `skill-creator` as the canonical scaffolders. Optionally extract the metaprompt's "identify variables before drafting" heuristic into chief-of-staff's dispatch-brief template. Half-day, low priority.
