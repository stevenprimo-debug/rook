---
name: skills
source: https://code.claude.com/docs/en/skills
fetched: 2026-05-22
category: claude-code
rook-relevance: high
---

# Skills (Claude Code)

## What it is

Skills extend Claude Code via `SKILL.md` files. Claude loads them when relevant or via `/skill-name`. Follow the [Agent Skills](https://agentskills.io) open standard. Custom commands have been merged into skills. **Body loads only when invoked** — long reference material costs almost nothing until used.

## Key concepts + config

### Skill locations
| Location | Path | Scope |
|---|---|---|
| Enterprise | managed settings | All org users |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin enabled |

Precedence: enterprise > personal > project. Plugin skills use `plugin-name:skill-name` namespace. Live change detection watches directories.

### Skill structure
```
my-skill/
├── SKILL.md           # required entrypoint
├── reference.md       # loaded when referenced
├── examples/sample.md
└── scripts/validate.sh
```

### Frontmatter reference
```yaml
---
name: my-skill
description: What this skill does and when to use it
when_to_use: Additional trigger context
argument-hint: "[issue-number]"
arguments: [issue, branch]   # named positional
disable-model-invocation: true
user-invocable: false
allowed-tools: Read Grep
model: inherit
effort: medium
context: fork
agent: Explore
hooks: {...}
paths: ["src/**/*.ts"]
shell: bash
---
```

All fields optional; `description` recommended. Combined `description` + `when_to_use` truncated at 1,536 chars in skill listing.

### Invocation matrix
| Frontmatter | You invoke | Claude invokes | Loaded into ctx |
|---|---|---|---|
| (default) | Yes | Yes | Description always, full on invoke |
| `disable-model-invocation: true` | Yes | No | Nothing until you invoke |
| `user-invocable: false` | No | Yes | Description always, full on invoke |

### String substitutions
- `$ARGUMENTS` — full string
- `$ARGUMENTS[N]` / `$N` — by position (0-indexed)
- `$name` — declared in `arguments:` frontmatter
- `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`

### Dynamic context injection
```markdown
## Current changes
!`git diff HEAD`
```
Inline `` !`cmd` `` runs before content sent. Multi-line:
````
```!
node --version
git status
```
````
Disable via settings `"disableSkillShellExecution": true`.

### Run skill in subagent
```yaml
---
name: deep-research
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly...
```
With `context: fork`, SKILL.md content becomes the subagent prompt. Built-in agents: `Explore`, `Plan`, `general-purpose`.

### Pre-approve tools
```yaml
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
```
Grants permission while skill active. Doesn't restrict — every tool callable, settings still govern.

### Skill content lifecycle
Once invoked, rendered SKILL.md enters conversation as a single message and stays. Claude doesn't re-read on later turns. **Auto-compaction**: keeps first 5,000 tokens of each invoked skill, 25,000 token shared budget across re-attached skills.

### Override visibility via settings
```json
{"skillOverrides": {"legacy-context": "name-only", "deploy": "off"}}
```
Values: `on` | `name-only` | `user-invocable-only` | `off`.

### Restrict Claude's skill access
```text
# In permissions:
Skill                 # deny all
Skill(commit)         # exact
Skill(review-pr *)    # prefix
```

### Description budget
1% of context window (settings: `skillListingBudgetFraction`). Per-skill cap: 1,536 chars (settings: `maxSkillDescriptionChars`). Run `/doctor` to see budget overflow.

### Best practices
- Keep `SKILL.md` under 500 lines
- Move detail to supporting files
- Put key use case first in description
- State what to do, not how/why (recurring token cost)

## ROOK applicability

This IS the substrate ROOK ships on. Every one of the 20 agents is a `.claude/skills/<agent>/SKILL.md`. The frontmatter shape determines whether the agent auto-loads (default) or requires manual dispatch (`disable-model-invocation`). `paths` patterns let agents auto-activate on file types. `context: fork` is how chief-of-staff dispatches to specialists in isolated context. The 25K compaction budget is why ROOK favors compounding-append memory in `agents/*/memory/` rather than huge SKILL.md bodies.

## Cross-references
- [[../guides/skills]] — Agent Skills open standard
- [[subagents]] — `context: fork` execution
- [[hooks]] — `hooks:` frontmatter scoping
- [[settings]] — `skillOverrides`, `skillListingBudgetFraction`
- [[../../anthropic-cookbook/skills-dev/custom-skill-development]] — API-side skill packaging
