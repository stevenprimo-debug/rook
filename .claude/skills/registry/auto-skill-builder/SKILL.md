---
name: auto-skill-builder
description: >
  Automatic skill creation and Git backup agent. Use this skill ANY time the user says "make this a skill,"
  "save this as a skill," "turn this into a skill," "we keep doing this," "automate this pattern,"
  "I don't want to explain this again," or any indication that a recurring workflow, formatting rule,
  process, or set of instructions should be captured as a reusable skill. Also trigger when the user
  expresses frustration that the agent "keeps forgetting" something, "doesn't follow" a rule, or
  "messes up" a repeated task — these are signals that a skill needs to be created to enforce the
  pattern. Even if the user doesn't say the word "skill," if they're describing a process they want
  consistently followed across sessions, this skill should activate. The goal is zero wasted time —
  if something has been explained twice, it becomes a skill.
---

# Auto Skill Builder + Git Backup

You are creating a new skill for the user's Claude environment. This is a recursive system — skills are how the user enforces consistency across sessions. If something needs to be done the same way every time, it becomes a skill. No exceptions, no "I'll just remember next time."

## Why This Exists

Operators run high-output workflows across multiple Claude sessions (Cowork, Projects, scheduled tasks). Without skills, every new session starts from zero — context is lost, rules get ignored, and the user has to re-explain things they've already solved. This skill ensures that every reusable pattern gets captured, saved, and backed up automatically.

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

## Step 3: Save to the Skills Vault (Git Repo)

Save the skill to the user's skills repository. The repo structure is:

```
<skills-repo>/
├── CLAUDE.md
├── [existing-skill-1]/
│   └── SKILL.md
├── [existing-skill-2]/
│   └── SKILL.md
├── [other skills]/
└── [new-skill-name]/
    ├── SKILL.md
    └── references/  (if needed)
```

### Save locations (do ALL of these):

1. **Skills repo:** `<skills-repo-path>/[skill-name]/SKILL.md`
   - This is the source of truth. Always write here first.
   - If the user has a daily auto-push configured (Task Scheduler / cron / GitHub Action), the commit will sync automatically.

2. **Local `.claude/skills/` directory:** Try writing to `<user-home>/.claude/skills/[skill-name]/SKILL.md`
   - This may fail (read-only filesystem on some environments). If it does, tell the user to copy manually:
   - "Copy the new skill folder from `<skills-repo-path>/[skill-name]/` into `<user-home>/.claude/skills/[skill-name]/`"

3. **Update the sync log:** Append a line to `<skills-repo-path>/sync-log.txt`:
   - Format: `[YYYY-MM-DD HH:MM] SKILL CREATED: [skill-name] — [one-line description]`

---

## Step 4: Verify

After creating the skill:

1. Read back the SKILL.md and confirm it's complete
2. Check that the description field covers all reasonable trigger phrases
3. Confirm the file is saved in the skills repo
4. Tell the user the manual copy step if `.claude/skills/` was read-only
5. Log it to sync-log.txt

---

## Step 5: Report to the User

Keep it short:

```
Skill created: [skill-name]
Location: <skills-repo-path>/[skill-name]/SKILL.md
Triggers on: [2-3 example phrases]
Manual step: Copy to <user-home>/.claude/skills/[skill-name]/
```

No lengthy explanations. The user can read the SKILL.md if they want details.

---

## Common Skill Patterns

These are patterns operators frequently need captured. If the current request matches one, use it as a starting point:

**Formatting enforcer** — Rules for how a specific file or file type should look. Include pre-flight checklist. Example: client document formatting rules.

**Process workflow** — Multi-step procedure that should be followed the same way every time. Include step numbering and decision points. Example: outreach pipeline.

**Document generator** — Creates a specific type of document from inputs. Include template structure and output format. Example: engineering scope, SOW.

**Email drafter** — Generates emails with specific tone, format, and sign-off rules. Include example outputs. Example: cold-outreach reply templates.

**Data processor** — Takes input data and transforms it according to rules. Include validation steps. Example: quote import, CAD reading.

---

## Anti-Patterns (Don't Do These)

- **Don't make the skill too narrow.** If it only works for one specific file, it's not reusable. Generalize where possible.
- **Don't skip the description field.** A skill with a weak description won't trigger. This is the single most important part.
- **Don't write a skill for something that should be in CLAUDE.md.** CLAUDE.md is for rules that apply to EVERY session. Skills are for rules that apply to SPECIFIC tasks.
- **Don't forget the Git backup.** If it's not in the repo, it doesn't exist. Sessions are ephemeral.
