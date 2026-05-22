---
name: output-styles
source: https://code.claude.com/docs/en/output-styles
fetched: 2026-05-22
category: claude-code
rook-relevance: medium
---

# Output Styles

## What it is

Output styles change how Claude responds, not what Claude knows. They modify the system prompt to set role, tone, and output format. Use when you keep re-prompting for the same voice/format every turn, or when Claude should act as something other than a software engineer.

## Key concepts + config

### Built-in styles
- **Default** — software engineering
- **Proactive** — executes immediately, makes reasonable assumptions, prefers action over planning (stronger than auto mode)
- **Explanatory** — adds educational "Insights" alongside coding
- **Learning** — collaborative learn-by-doing; adds `TODO(human)` markers

### Change style
```json
{"outputStyle": "Explanatory"}
```
Or `/config` → Output style. Takes effect after `/clear` or new session.

### Create custom style
Save at one of three levels:
- User: `~/.claude/output-styles/`
- Project: `.claude/output-styles/`
- Managed: `.claude/output-styles/` inside managed settings dir

### Frontmatter fields
| Field | Purpose | Default |
|---|---|---|
| `name` | Display name | file name |
| `description` | Shown in `/config` picker | None |
| `keep-coding-instructions` | Keep Claude Code's built-in SWE instructions | `false` |
| `force-for-plugin` | (Plugins only) Apply automatically when plugin enabled | `false` |

### Example
```markdown
---
name: Diagrams first
description: Lead every explanation with a diagram
keep-coding-instructions: true
---

When explaining code, architecture, or data flow, start with a Mermaid diagram
showing the structure, then explain in prose.
```

### Comparison
| Feature | How it works | Use when |
|---|---|---|
| Output styles | Modifies system prompt | Different role/tone every turn |
| CLAUDE.md | User message after system prompt | Persistent project conventions |
| `--append-system-prompt` | One-off addition | Single invocation |
| Agents | Subagent with own prompt | Focused scoped task |
| Skills | Loads task-specific instructions | Reusable workflow |

## ROOK applicability

Custom output style is one option for enforcing the ROOK voice contract (banned words, lead-with-verdict rule, no preamble). Alternative to relying on CLAUDE.md alone. `keep-coding-instructions: true` keeps Claude doing SWE while ROOK enforces voice. Plugin `force-for-plugin` would let a ROOK distribution auto-apply voice when installed.

## Cross-references
- [[settings]] — `outputStyle` field
- [[skills]] — skills are an alternative for scoped behavior
- [[../guides/system-prompts]] — system prompt patterns
