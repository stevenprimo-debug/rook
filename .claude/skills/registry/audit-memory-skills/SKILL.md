---
name: audit-memory-skills
description: Recursive integrity audit on the operator's Claude ecosystem — verifies MEMORY.md indexes are current, daily skills are backed up, handoff files are functional, and the folder structure is evolving toward an org-chart model with department-scoped sub-agents and skills. Use this skill ANY time the operator says "audit memory", "audit skills", "check memory", "check backups", "run memory check", "is my framework compounding", "did we save X", "handoff audit", or any phrasing about verifying that the compounding loop (conversation → memory → skill → backup → next session) is intact. Also fire proactively at the start of any session where the operator mentions handoffs, org-chart structure, or recursive agent frameworks.
---

# Audit Memory & Skills — Compounding Loop Integrity Check

You are performing a recursive integrity audit on the operator's Claude ecosystem. The goal is to guarantee that memory compounds across sessions, skills are backed up daily, handoffs carry state forward, and the folder structure is evolving toward a company-org-chart model where each "department" folder contains its own sub-agents, skills, and memory.

## Root to audit
``

## Ground rules
- **Audit only. Do not fix anything** until the operator explicitly approves which items to address.
- Respect the constraint-aware Protocol — lock the mission before starting, don't spiral into fixes mid-audit.
- Report as a numbered punch list (done vs. missing). Terse. No trailing summaries.

## Execution order

### 1. MEMORY.md hygiene
- Locate every `MEMORY.md` index file under `PRIMOLABS\`. Expected location: `CLAUDE CODE\MEMORY\MEMORY.md`.
- For each index found, verify:
  (a) every linked `.md` memory file actually exists on disk
  (b) every `.md` memory file in the folder is indexed (no orphans)
  (c) no duplicate entries
  (d) index stays under 200 lines
- **Cross-check this conversation's artifacts against memory.** Any important fact learned this session that matches the user/feedback/project/reference criteria but was never written to memory = gap. "Important" = surprising, non-obvious, or load-bearing for future decisions.
- If `MEMORY.md` is missing entirely, flag as **P0** — without it, memory accumulates but does not compound.

### 2. Daily skill backup verification
- Enumerate every skill under BOTH:
  - `SKILLS\` (production set)
  - `C:\Users\User\.claude\skills\` (CLI-local set)
- For each skill, check modification date. Any skill touched in the last 24 hours must have a corresponding backup — verify via git (if `SKILLS\` is a repo, check `git log --since=yesterday`) or via a timestamped copy in `SKILLS_BACKUP\`.
- Check `CLAUDE_CONFIG\sync-log.txt` — this is the operator's manual skill change log. Verify it reflects recent changes, but note it is NOT a real backup (prose log only, no file contents preserved).
- Verify every skill folder has a `SKILL.md`. Flag orphan folders (folder without SKILL.md).
- Flag split storage: if the same skill exists in both locations with different contents, warn.
- If no backup mechanism exists at all, flag as **P0** and recommend: `git init` at `SKILLS\` with pre-commit hook (preferred, gives diffs + rollback) OR daily `robocopy` to `SKILLS_BACKUP\YYYY-MM-DD\`.

### 3. Org-chart folder framework scan
the operator heard a podcast describing a structure where the top-level is a `CLAUDE.md`-rooted folder, and subfolders are modeled like a company org chart — each department folder (Sales, Engineering, an enterprise customer, Email, Personal, Core) contains its own sub-agents, skills, and memory scoped to that department's work.

- Map the current `PRIMOLABS\` folder tree (2 levels deep).
- Compare to the org-chart ideal.
- Identify: (a) which your employer functions already have dedicated folders, (b) which are missing, (c) which existing skills/memories should be relocated for better scoping.
- Propose a target tree organized by agent surface area. Example shape:
  - `agents/<agent-slug>/skills/` — per-agent skill folders
  - `agents/<agent-slug>/memory/` — per-agent compounding learnings
  - `.claude/reference/` — shared shelf (API docs, templates, methodology — readable by all agents)
  - `.claude/skills/core/` — universal capabilities (pdf, docx, pptx, xlsx, skill-creator, prompt-builder)
- Each agent folder has `SKILL.md`, `CLAUDE.md`, `personality/`, `memory/`, and (optionally) child `skills/`.

### 4. Handoff & compounding loop check
- Read every file in `CLAUDE CODE\HANDOFFS\`.
- Verify each handoff file actually contains: Mission, Done, Parked, Next (the 4 fields required by the constraint-aware Protocol session close-out rule). Handoff files that are only timestamp logs = **broken**.
- Confirm `auto-skill-builder` skill has been firing — look for skills created in the last 7 days (check `sync-log.txt` and folder mtimes).
- Trace the compounding loop: conversation → memory → skill → backup → next session. Name every broken link.

## Report format

```
## Audit Results — YYYY-MM-DD

### ✅ Working
- ...

### ⚠️ Gaps
- ...

### 🚨 P0 (fix before next session)
- ...

### Proposed org-chart tree
<tree diagram>

### Recommended next actions (in order)
1. ...
```

After delivering the report, STOP. Wait for the operator to approve which items to fix. Do not modify any files during the audit phase.

## Output discipline
- Terse. No preamble, no trailing summary.
- Flag findings, don't narrate the search.
- If the operator asks to fix items, address them one at a time — do not batch-fix without confirmation on each.
