---
name: auto-skill-builder
description: >
  Automatic skill creation and Git backup agent. Use this skill ANY time the operator says "make this a skill,"
  "save this as a skill," "turn this into a skill," "we keep doing this," "automate this pattern,"
  "I don't want to explain this again," or any indication that a recurring workflow, formatting rule,
  process, or set of instructions should be captured as a reusable skill. Also trigger when the operator
  expresses frustration that Claude "keeps forgetting" something, "doesn't follow" a rule, or
  "messes up" a repeated task — these are signals that a skill needs to be created to enforce the
  pattern. Even if the operator doesn't say the word "skill," if he's describing a process he wants
  consistently followed across sessions, this skill should activate. The goal is zero wasted time —
  if something has been explained twice, it becomes a skill.
---

# Auto Skill Builder + Git Backup

You are creating a new skill for the operator's Claude environment. This is a recursive system — skills are how the operator enforces consistency across sessions. If something needs to be done the same way every time, it becomes a skill. No exceptions, no "I'll just remember next time."

## Why This Exists

the operator runs a high-output workflow across multiple Claude sessions (Cowork, Projects, scheduled tasks). Without skills, every new session starts from zero — context is lost, rules get ignored, and the operator has to re-explain things he's already solved. This skill ensures that every reusable pattern gets captured, saved, and backed up automatically.

---

## Step 1: Identify What the Skill Should Do

Before writing anything, answer these questions (use conversation context — don't ask the operator to repeat himself):

1. **What's the recurring task or rule?** — Name it in one sentence.
2. **What triggers it?** — What would the operator say or do that should activate this skill? Think broadly: casual phrasing, frustrated complaints, file uploads, specific keywords.
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
  than to miss a trigger and have the operator re-explain something.]
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
[Verification steps before delivering output to the operator.]
```

### Writing principles:
- **Explain the why.** "Use Arial because Calibri is Excel's default and leaks in silently" is better than "ALWAYS USE ARIAL."
- **Be specific about triggers.** The description field is what determines if the skill fires. Make it comprehensive. Include casual phrasing, typos-level casual, frustrated versions ("this keeps breaking"), and adjacent keywords.
- **Include edge cases.** If there are common mistakes or gotchas, call them out explicitly.
- **Keep it under 500 lines.** If it's longer, split into SKILL.md + reference files in a `references/` subdirectory.

---

## Step 3: Save to the Skills Vault (Git Repo)

Save the skill to the operator's CLAUDE_SKILLS_REPO. The repo structure is:

```
CLAUDE_SKILLS_REPO/
├── CLAUDE.md
├── bsa-formatting/
│   └── SKILL.md
├── lmg-email-replies/
│   └── SKILL.md
├── lmg-engineering-scope/
│   └── SKILL.md
├── [other skills]/
└── [new-skill-name]/
    ├── SKILL.md
    └── references/  (if needed)
```

### Save locations (do ALL of these):

1. **Git repo:** `/sessions/*/mnt/CLAUDE_SKILLS_REPO/[skill-name]/SKILL.md`
   - This is the source of truth. Always write here first.
   - The auto-push script (Windows Task Scheduler, 3:55 PM CST daily) will push to GitHub.

2. **Cowork skills directory:** Try writing to `/sessions/*/mnt/.claude/skills/[skill-name]/SKILL.md`
   - This may fail (read-only filesystem). If it does, tell the operator to copy manually:
   - "Copy `C:\Users\User\Documents\GitHub\CLAUDE_SKILLS_REPO\[skill-name]\` into `C:\Users\User\.claude\skills\[skill-name]\`"

3. **Update the sync log:** Append a line to `CLAUDE_SKILLS_REPO/sync-log.txt`:
   - Format: `[YYYY-MM-DD HH:MM] SKILL CREATED: [skill-name] — [one-line description]`

---

## Step 4: Verify

After creating the skill:

1. Read back the SKILL.md and confirm it's complete
2. Check that the description field covers all reasonable trigger phrases
3. Confirm the file is saved in the Git repo
4. Tell the operator the manual copy step if `.claude/skills/` was read-only
5. Log it to sync-log.txt

---

## Step 5: Report to the operator

Keep it short:

```
Skill created: [skill-name]
Location: CLAUDE_SKILLS_REPO/[skill-name]/SKILL.md
Triggers on: [2-3 example phrases]
Manual step: Copy to C:\Users\User\.claude\skills\[skill-name]\
```

No lengthy explanations. the operator can read the SKILL.md if he wants details.

---

## Common Skill Patterns

These are patterns the operator frequently needs captured. If the current request matches one, use it as a starting point:

**Formatting enforcer** — Rules for how a specific file or file type should look. Include pre-flight checklist. Example: [example enterprise customer] formatting rules.

**Process workflow** — Multi-step procedure that should be followed the same way every time. Include step numbering and decision points. Example: outreach pipeline.

**Document generator** — Creates a specific type of document from inputs. Include template structure and output format. Example: engineering scope, SOW.

**Email drafter** — Generates emails with specific tone, format, and sign-off rules. Include example outputs. Example: email replies skill.

**Data processor** — Takes input data and transforms it according to rules. Include validation steps. Example: [your CRM] import, CAD reading.

---

## Anti-Patterns (Don't Do These)

- **Don't make the skill too narrow.** If it only works for one specific file, it's not reusable. Generalize where possible.
- **Don't skip the description field.** A skill with a weak description won't trigger. This is the single most important part.
- **Don't write a skill for something that should be in CLAUDE.md.** CLAUDE.md is for rules that apply to EVERY session. Skills are for rules that apply to SPECIFIC tasks.
- **Don't forget the Git backup.** If it's not in the repo, it doesn't exist. Sessions are ephemeral.
