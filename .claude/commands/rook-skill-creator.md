---
name: rook-skill-creator
description: Scaffold a new skill against the ROOK Master Skill Template v2 contract. Use when the operator says "make this a skill", "save this as a skill", "turn this into a skill", "we keep doing this", "automate this pattern", "I don't want to explain this again", or describes any recurring workflow / formatting rule / process that should be captured for cross-session reuse. Picks the right destination (.claude/skills/core/ for universal stack, .claude/skills/registry/ for per-agent domain skills, .claude/skills/templates/ for contract scaffolds, or agents/<slug>/skills/ for agent-private skills) based on declared scope.
argument-hint: <description of the skill to scaffold — what it does, when it fires, expected output, intended scope>
---

Load the skill at `.claude/skills/core/skills/skill-creator/SKILL.md` and apply its full skill-authoring workflow to the following input:

<input>
$ARGUMENTS
</input>

Follow the canonical flow:

1. **Capture intent** — what should the skill enable, what triggers it, what is the expected output, what goes wrong without it
2. **Decide scope + destination:**
   - Universal capability every agent needs → `.claude/skills/core/skills/<name>/`
   - Per-agent domain skill referenced in one agent's frontmatter → `.claude/skills/registry/<name>/`
   - Contract template (SOW / NDA / MSA / proposal) → `.claude/skills/templates/<name>/`
   - Agent-private skill only one agent invokes → `agents/<agent-slug>/skills/<name>/`
3. **Write SKILL.md** against the Master Skill Template v2 contract — frontmatter (name, description, type, agent, tools, model, skills, memory, trigger, inherits, budget), 3-pole bench if applicable, Step 1 context-load gate, routing keywords if applicable, the prompt body, worked examples
4. **Verify** — re-read the SKILL.md, confirm description triggers cover the named patterns, confirm the file lands at the right scope, run `git status` to confirm the new files are staged
5. **Commit** to vault git with a descriptive message: `git add <path> && git commit -m 'add <skill-name> skill: <one-line purpose>'`

Report terse:

```
Skill created: <skill-name>
Path: .claude/skills/<scope>/<skill-name>/SKILL.md
Triggers on: <2-3 example phrases>
Committed: <git short-hash>
```

If `$ARGUMENTS` is empty, ask the operator what the skill should do. Do not narrate the authoring process — the SKILL.md file is the artifact.
