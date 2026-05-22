---
name: auto-skill-builder
description: >
  Fast-path skill capture for ROOK. Use this skill ANY time the user says "make this a skill,"
  "save this as a skill," "turn this into a skill," "we keep doing this," "automate this pattern,"
  "I don't want to explain this again," or any indication that a recurring workflow, formatting rule,
  process, or set of instructions should be captured as a reusable skill. Also trigger when the user
  expresses frustration that Claude "keeps forgetting" something, "doesn't follow" a rule, or
  "messes up" a repeated task — these are signals that a skill needs to be created to enforce the
  pattern. Even if the user doesn't say the word "skill," if they are describing a process they want
  consistently followed across sessions, this skill should activate. The goal is zero wasted time —
  if something has been explained twice, it becomes a skill.
---

# Auto Skill Builder — Fast-Path Capture

You are capturing a new skill for the ROOK vault. This is a recursive system — skills are how ROOK enforces consistency across sessions. If something needs to be done the same way every time, it becomes a skill. No exceptions, no "I'll just remember next time."

## When to use this vs. `skill-creator`

This skill is the **FAST PATH** for capturing a recurring pattern: "we keep doing this, make it a skill, NOW." Drafts a SKILL.md from conversation context, saves it to the right `.claude/skills/` subfolder, commits. Done in one turn.

For thorough skill development with eval test cases, baseline comparisons, description optimization, and iterative improvement — use [`skill-creator`](../skill-creator/SKILL.md) instead. That's the workshop. This is the capture tool.

## Why This Exists

ROOK runs across multiple sessions in Claude Code. Skills are the unit of cross-session consistency — capture a pattern once, every future session inherits it. Without skills, every new session starts from zero — context is lost, rules get ignored, and the user has to re-explain things they've already solved. This skill ensures that every reusable pattern gets captured and committed in one turn.

---

## Step 1: Identify What the Skill Should Do

Before writing anything, answer these questions (use conversation context — don't ask the user to repeat themselves):

1. **What's the recurring task or rule?** — Name it in one sentence.
2. **What triggers it?** — What would the user say or do that should activate this skill? Think broadly: casual phrasing, frustrated complaints, file uploads, specific keywords.
3. **What's the expected output?** — A file? Formatted data? A specific process followed? An email?
4. **What goes wrong without it?** — Why does this need to be a skill? What mistake keeps happening?

---

## Step 2: Write the SKILL.md

Follow this structure:

```markdown
---
name: skill-name-here
description: >
  [Pushy, comprehensive trigger description. Include every phrase,
  keyword, and context that should activate this skill. Err on the
  side of over-triggering — it's better to activate and not be needed
  than to miss a trigger and have the user re-explain something.]
---

# [Skill Title]

[1-2 sentences: what this skill does and why it exists.]

## Why This Matters
[What goes wrong without this skill. Be specific — reference past failures if known.]

## Instructions
[The actual rules/process/workflow. Written in imperative form.
Explain the WHY behind each rule so the model can handle edge cases
intelligently rather than just following rote instructions.]

## Pre-Flight Checklist
[Verification steps before delivering output to the user.]
```

### Writing principles:
- **Explain the why.** "Use Arial because Calibri is Excel's default and leaks in silently" is better than "ALWAYS USE ARIAL."
- **Be specific about triggers.** The description field is what determines if the skill fires. Make it comprehensive. Include casual phrasing, typos-level casual, frustrated versions ("this keeps breaking"), and adjacent keywords.
- **Include edge cases.** If there are common mistakes or gotchas, call them out explicitly.
- **Keep it under 500 lines.** If it's longer, split into SKILL.md + reference files in a `references/` subdirectory.

---

## Step 3: Save to `.claude/skills/`

ROOK skills live at `.claude/skills/` inside the ROOK vault. The vault is git-versioned at its root — no separate skills repo, no scheduled push.

### Where to save

Decide the right subfolder based on skill scope:

| Skill scope | Save to | Examples |
|---|---|---|
| Universal capability every agent needs | `.claude/skills/core/skills/<skill-name>/` | markitdown, graphify, obsidian-cli, html2pdf, skill-creator |
| Domain-specific skill baked into ONE agent's frontmatter | `.claude/skills/registry/<skill-name>/` | apollo-prospect-search, ict-pattern-detector, pine-script-template |
| Contract template (SOW, NDA, MSA, proposal) | `.claude/skills/templates/<template-name>/` | msa-template, sow-template |
| Agent-private skill that only one agent calls | `agents/<agent-slug>/skills/<skill-name>/` | sales-director/skills/outreach, sales-director/skills/prospecting |

### Folder structure

```
<skill-name>/
├── SKILL.md          (required — frontmatter + body)
├── references/       (optional — docs loaded on demand)
├── scripts/          (optional — deterministic helpers)
└── assets/           (optional — templates, fonts, icons)
```

### Git
Commit the new skill to the vault git with a descriptive message: `git add .claude/skills/<scope>/<skill-name> && git commit -m 'add <skill-name> skill: <one-line purpose>'`. The vault's git history is the audit trail.

---

## Step 4: Verify

After creating the skill: (1) Re-read the SKILL.md and confirm description triggers cover the named patterns, (2) Confirm the file lands at the right scope (core/registry/templates/agent-private), (3) Run `git status` to confirm the new files are staged, (4) Stage + commit with a descriptive message.

---

## Step 5: Report

Tell the user, terse:

```
Skill created: <skill-name>
Path: .claude/skills/<scope>/<skill-name>/SKILL.md
Triggers on: <2-3 example phrases>
Committed: <git short-hash>
```

---

## Common Skill Patterns

These are patterns frequently captured. If the current request matches one, use it as a starting point:

**Formatting enforcer** — Rules for how a specific file or file type should look. Include pre-flight checklist. Example: vertical-specific formatting rules.

**Process workflow** — Multi-step procedure that should be followed the same way every time. Include step numbering and decision points. Example: outreach pipeline.

**Document generator** — Creates a specific type of document from inputs. Include template structure and output format. Example: engineering scope, SOW.

**Email drafter** — Generates emails with specific tone, format, and sign-off rules. Include example outputs. Example: email replies skill.

**Data processor** — Takes input data and transforms it according to rules. Include validation steps. Examples: CSV → JSON normalization, API response → structured record.

---

## Anti-Patterns (Don't Do These)

- **Don't make the skill too narrow.** If it only works for one specific file, it's not reusable. Generalize where possible.
- **Don't skip the description field.** A skill with a weak description won't trigger. This is the single most important part.
- **Don't write a skill for something that should be in CLAUDE.md.** CLAUDE.md is for rules that apply to EVERY session. Skills are for rules that apply to SPECIFIC tasks.
- **Don't forget to commit.** If it's not in git, the audit trail is broken. The vault's git history is how ROOK proves the compounding loop works.
