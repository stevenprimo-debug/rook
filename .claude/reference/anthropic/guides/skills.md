---
name: skills
source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
fetched: 2026-05-22
category: guides
rook-relevance: high
---

# Agent Skills (Canonical Anthropic Spec)

## What it is

Modular capabilities that extend Claude's functionality. Each Skill is a directory with `SKILL.md` + optional resources. Same standard Claude Code follows. **NOT eligible for Zero Data Retention.**

## Key concepts + config

### Why skills (vs prompts)
- Specialize Claude for domain tasks
- Reduce repetition (create once, use automatically)
- Compose capabilities

### Three levels of progressive disclosure

| Level | When loaded | Token cost | Content |
|---|---|---|---|
| **L1 Metadata** | Always (startup) | ~100 tokens/skill | `name`, `description` from YAML |
| **L2 Instructions** | When triggered | Under 5k tokens | SKILL.md body |
| **L3+ Resources** | As needed | Effectively unlimited | Bundled files via bash |

### Required frontmatter
```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

### Field requirements
**`name`**:
- Max 64 chars
- Lowercase letters, numbers, hyphens only
- No XML tags
- Reserved words forbidden: `anthropic`, `claude`

**`description`**:
- Non-empty
- Max 1024 chars
- No XML tags
- Should state WHAT the skill does AND WHEN Claude should use it

### Skill structure
```
pdf-skill/
├── SKILL.md (main instructions, required)
├── FORMS.md (form-filling guide, loaded when referenced)
├── REFERENCE.md (detailed API reference)
└── scripts/
    └── fill_form.py (Claude runs via bash, code not in context)
```

### How skills load (architecture)
1. **Startup**: System prompt includes skill descriptions
2. **Trigger**: User request matches; Claude runs `bash: read SKILL.md` → instructions enter context
3. **Resources**: Claude reads `FORMS.md` only if needed
4. **Scripts**: Claude runs scripts via bash; output enters context, **code does NOT**

### Where skills work

| Surface | Built-in | Custom | Notes |
|---|---|---|---|
| Claude API | pptx, xlsx, docx, pdf | Yes (Skills API) | Workspace-wide sharing |
| Claude Code | No | Yes (filesystem) | `.claude/skills/`, `~/.claude/skills/` |
| claude.ai | pptx, xlsx, docx, pdf | Yes (zip upload) | Pro+/Max/Team/Enterprise, per-user |

### API beta headers (required for skills via API)
- `code-execution-2025-08-25`
- `skills-2025-10-02`
- `files-api-2025-04-14`

### Cross-surface limitations
**Custom Skills do NOT sync across surfaces**:
- claude.ai upload ≠ API upload ≠ Claude Code filesystem
- claude.ai = individual user; no centralized admin distribution
- API = workspace-wide

### Runtime environment

| Surface | Network | Package install |
|---|---|---|
| claude.ai | Varies by user/admin | No |
| Claude API | **No network** | Pre-installed packages only |
| Claude Code | Full network | Local install only (discouraged global) |

### Open-source skills
- claude-api skill: API reference + SDK docs for 8 languages (bundled in Claude Code, also in `anthropics/skills` repo)

### Security
Use only trusted sources. Audit before use:
- All bundled files (SKILL.md, scripts, images, resources)
- Watch for unusual network calls, file access patterns, ops not matching stated purpose
- External-fetch skills = highest risk (fetched content may have prompt injection)
- Treat like installing software

## ROOK applicability

This is the canonical spec ROOK's 20 agents follow. Each agent dir = a skill dir. The cross-surface non-sync is why ROOK ships its skills via filesystem (`agents/<name>/SKILL.md`) and a git clone install, not API uploads. The `name` constraint forbidding "claude" / "anthropic" matters for ROOK branding compliance. The L3 "scripts code doesn't enter context" model is what makes ROOK economically viable — librarian's git-grep helpers, deep-researcher's vector-query scripts run via bash without burning context. Security note applies: ROOK distribution must be auditable by operators since they're treating it like installing software.

## Cross-references
- [[../claude-code/skills]] — Claude Code's superset (file-based + extensions)
- [[tool-use]] — code execution tool used by skills
- [[../claude-code/subagents]] — `skills:` preload field
- [[../../anthropic-cookbook/skills-dev/custom-skill-development]] — API packaging walkthrough
