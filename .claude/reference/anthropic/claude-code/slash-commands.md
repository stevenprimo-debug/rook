---
name: slash-commands
source: https://code.claude.com/docs/en/slash-commands
fetched: 2026-05-22
category: claude-code
rook-relevance: high
---

# Slash Commands (merged into Skills)

## What it is

Custom commands have been merged into Skills as of recent Claude Code. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work identically. Skills add: supporting-files directory, frontmatter for invocation control, auto-load when relevant.

See [[skills]] for the canonical reference — slash-commands is now a redirect/legacy surface.

## Key concepts + config

### Legacy commands form
`.claude/commands/<name>.md` files still work. Use same frontmatter as skills (`description`, `disable-model-invocation`, `allowed-tools`, `argument-hint`, `arguments`, etc.).

### Precedence
If a skill and a command share the same name, **the skill takes precedence**.

### Argument substitution (same as skills)
- `$ARGUMENTS` — full string
- `$ARGUMENTS[N]` / `$N` — positional
- `$name` — named (declared via `arguments:` frontmatter)
- `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`

### Dynamic context injection
```markdown
## Current changes
!`git diff HEAD`
```
Inline `` !`cmd` `` runs before send. Multi-line via fenced ` ```! `.

### Built-in skills (bundled)
`/code-review`, `/batch`, `/debug`, `/loop`, `/claude-api`, `/run`, `/verify`, `/run-skill-generator`, `/init`, `/review`, `/security-review`.

## ROOK applicability

ROOK ships agents as skills (`.claude/skills/<agent>/SKILL.md`). The merger means `/chief-of-staff`, `/librarian`, `/deep-researcher` etc. all work as both Claude-invoked and user-invoked. Legacy `.claude/commands/` still works for one-off shortcuts the operator doesn't want as full skills.

## Cross-references
- [[skills]] — canonical reference (this is now mostly redirect surface)
- [[../guides/skills]] — Agent Skills open standard
