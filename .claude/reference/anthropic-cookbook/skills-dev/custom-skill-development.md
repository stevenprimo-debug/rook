---
name: custom-skill-development
source: https://github.com/anthropics/claude-cookbooks/blob/main/skills/notebooks/03_skills_custom_development.ipynb
fetched: 2026-05-22
category: Skills Development
rook-relevance: high
rook-status: already-implemented
---

# Custom Skill Development

## What it is

Anthropic's canonical pattern for building Claude skills. Three phases:

1. **Creation** — directory with required `SKILL.md` (YAML frontmatter: name ≤64 chars, description ≤1024 chars) + markdown instructions + optional `scripts/` + `resources/`.
2. **Deployment** — `client.beta.skills.create()` bundles + assigns skill_id; staged loading (metadata always visible, instructions on-demand, scripts/resources lazy).
3. **Management** — version-pinned; `client.beta.skills.versions.create()` adds versions; workspace-private; composable.

Recommended instructions ≤5000 tokens. Single-responsibility principle: one skill, one domain.

## Key code/config

```
skill_name/
├── SKILL.md          # required: name, description, instructions
├── *.md              # multiple .md allowed
├── scripts/          # Python or JS
└── resources/        # templates, data
```

SKILL.md frontmatter:
```yaml
---
name: lowercase-with-hyphens
description: What it does (1024 chars max)
---
```

Progressive disclosure stages:
- Stage 1: metadata always visible
- Stage 2: all `.md` files loaded when relevant
- Stage 3: scripts/resources loaded on-demand at execution

## Measured improvements / costs

None. This is a how-to notebook.

## ROOK applicability

**ROOK's `agents/_template/SKILL.md` already implements this pattern, plus more.** ROOK's template adds: 3-pole principle bench, voice-spine inheritance, frameworks-index, mode declarations, routing keywords, memory tier assignment. The Anthropic shape is a strict subset of ROOK's.

The one alignment item: ROOK's SKILL.md frontmatter has more fields than Anthropic's minimum (name + description). That's intentional — ROOK runs in Claude Code, not API-direct skill-uploads. But for cohort customers who later push ROOK agents up to API-direct skills, frontmatter would need to slim to the Anthropic minimum.

## Recommended action

**already-implemented** — `agents/_template/SKILL.md` is a superset. Optional add: a `scripts/export-as-anthropic-skill.py` utility that strips ROOK-specific frontmatter and emits an Anthropic-API-compatible skill bundle. Half-day work; only matters when a cohort customer asks for API-direct deployment.
