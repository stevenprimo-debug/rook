---
name: prompt-engineering
source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
fetched: 2026-05-22
category: guides
rook-relevance: high
---

# Prompt Engineering Overview

## What it is

Anthropic's prompt engineering hub. The overview page itself is light; the substantive content lives in [`claude-prompting-best-practices`](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — single reference for prompt engineering with Claude Opus 4.7, Opus 4.6, Sonnet 4.6, Haiku 4.5.

## Key concepts + config

### Prerequisites (before prompt engineering)
1. Clear success criteria
2. Empirical tests against those criteria
3. First-draft prompt to improve

### Console tools (not API)
- Prompt generator (Console workbench)
- Templates and variables
- Prompt improver

### Best-practices techniques (from `claude-prompting-best-practices`)

**Response length & verbosity (Opus 4.7)**: Calibrates length to task complexity automatically. Override:
```
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

**Core techniques** (covered in best-practices):
- Clarity & directness
- Examples (multishot)
- XML structuring (use tags like `<instructions>`, `<examples>`, `<context>`)
- Role / persona setting via system prompt
- Chain-of-thought / thinking
- Prompt chaining (split complex tasks into focused steps)

### Tutorials
- GitHub: https://github.com/anthropics/prompt-eng-interactive-tutorial
- Google Sheets interactive: https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8

### Caveat
> Not every failing eval is best solved by prompt engineering — latency and cost can sometimes be improved by selecting a different model.

## ROOK applicability

XML structuring is the right pattern for ROOK agents that bundle context (e.g., `<dispatch_brief>`, `<idea_log_entry>`, `<contradiction>`). Role setting is how each of the 20 agents establishes identity in their SKILL.md body. Prompt chaining = the chief-of-staff dispatch pattern (each agent gets a focused subprompt instead of a giant kitchen-sink prompt). The "shorter prompts on simple lookups" Opus 4.7 default is why ROOK voice contract still needs explicit "lead with verdict" rules — model defaults aren't the same as terse output.

## Cross-references
- [[system-prompts]] — role-setting patterns
- [[extended-thinking]] — chain-of-thought via thinking
- [[tool-use]] — examples + XML for tool descriptions
- [[../claude-code/output-styles]] — output styles modify the system prompt
