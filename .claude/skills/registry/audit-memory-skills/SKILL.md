---
name: audit-memory-skills
owner: librarian
budget:
  time_budget_minutes: 8
  token_budget: 50000
  max_dispatch_depth: 1
description: Recursive integrity audit on the ROOK ecosystem — verifies MEMORY.md indexes are current, daily skills are backed up, handoff files are functional, and the folder structure is evolving toward an org-chart model with department-scoped sub-agents and skills. Use this skill ANY time the operator says "audit memory", "audit skills", "check memory", "check backups", "run memory check", "is my framework compounding", "did we save X", "handoff audit", or any phrasing about verifying that the compounding loop (conversation → memory → skill → backup → next session) is intact. Also fire proactively at the start of any session where the operator mentions handoffs, org-chart structure, or recursive agent frameworks. The librarian agent invokes this skill as her canonical audit engine.
---

# Audit Memory & Skills — Compounding Loop Integrity Check

You are performing a recursive integrity audit on the ROOK ecosystem. The goal is to guarantee that memory compounds across sessions, skills are backed up daily, handoffs carry state forward, and the folder structure stays consistent with the locked org-chart model where each agent folder contains its own sub-skills and memory.

## Root to audit

Vault-root resolution (in order):
1. `$env:PRIMOLABS_VAULT_ROOT` (if set)
2. `git rev-parse --show-toplevel` (if cwd is inside a git repo)
3. Walk up from cwd looking for the first directory that contains `agents/` + `hooks/` siblings

Use `<vault-root>` as the substitution token in this skill's prose — the script resolves it at runtime.

## Ground rules
- **Audit only. Do not fix anything** until the operator explicitly approves which items to address.
- Respect the constraint-aware Protocol — lock the mission before starting, don't spiral into fixes mid-audit.
- Report as a numbered punch list (done vs. missing). Terse. No trailing summaries.

## Execution order

### 1. MEMORY.md hygiene
- Locate every `MEMORY.md` index file under `<vault-root>`. Expected locations: `<vault-root>/agents/<agent>/memory/MEMORY.md` (per-agent) and any top-level `MEMORY.md` if present.
- For each index found, verify:
  (a) every linked `.md` memory file actually exists on disk
  (b) every `.md` memory file in the folder is indexed (no orphans)
  (c) no duplicate entries
  (d) index stays under 200 lines
- **Cross-check this conversation's artifacts against memory.** Any important fact learned this session that matches the user/feedback/project/reference criteria but was never written to memory = gap. "Important" = surprising, non-obvious, or load-bearing for future decisions.
- If `MEMORY.md` is missing entirely from an agent that should have one, flag as **P0** — without it, memory accumulates but does not compound.

### 2. Daily skill backup verification
- Enumerate every skill under BOTH:
  - `<vault-root>/agents/*/skills/` (per-agent sub-skills)
  - `<vault-root>/.claude/skills/registry/` (shared registry skills)
- For each skill, check modification date. Any skill touched in the last 24 hours must have a corresponding backup — verify via git (the ROOK vault is a git repo; check `git log --since=yesterday`).
- (Optional, operator-local) Check `CLAUDE_CONFIG/sync-log.txt` if it exists — this is an operator-local manual change log, NOT a ROOK convention. Verify it reflects recent changes, but note it is not a real backup (prose log only, no file contents preserved).
- Verify every skill folder has a `SKILL.md`. Flag orphan folders (folder without SKILL.md).
- Flag split storage: if the same skill exists in `agents/<agent>/skills/<sub>/` AND `.claude/skills/registry/<same-name>/` with different contents, warn.
- If no git history exists at all, flag as **P0** and recommend `git init` at vault root with pre-commit hook (preferred, gives diffs + rollback).

### 3. Org-chart folder framework scan
ROOK's locked structure (per `_CLAUDE.md` Section 0):
- `agents/<agent-slug>/` — one folder per agent (20 agents)
  - `SKILL.md`, `CLAUDE.md`, `README.md`, `personality/`, `memory/`, optional `skills/<sub>/`
- `.claude/reference/` — shared shelf (API docs, templates, methodology — readable by all agents)
- `.claude/skills/core/` — universal capabilities (pdf, docx, pptx, xlsx, skill-creator, prompt-builder)
- `.claude/skills/registry/` — named operational skills (broad capability set)
- `hooks/` — runtime hook scripts wired into Claude Code

Steps:
- Map the current `<vault-root>` folder tree (2 levels deep).
- Compare to the org-chart ideal above.
- Identify: (a) which agent folders are missing required structure (SKILL.md / personality/ / memory/), (b) which skills are mislocated (agent-specific skills in `.claude/skills/registry/` instead of `agents/<x>/skills/`), (c) which memory files belong on the shared shelf instead of agent-scoped.

### 4. Handoff & compounding loop check
- Read every file in `<vault-root>/agents/chief-of-staff/memory/session_handoffs/` (canonical handoff location).
- Verify each handoff file actually contains: Mission, Done, Parked, Next (the 4 fields required by session close-out). Handoff files that are only timestamp logs = **broken**.
- Confirm skill creation activity — look for skills created in the last 7 days (check folder mtimes under `agents/*/skills/` and `.claude/skills/registry/`).
- Trace the compounding loop: conversation → memory → skill → backup → next session. Name every broken link.

### 5. Plain-text wikilink hygiene

Detect plain-text mentions of named entities that should be wikilinks but aren't. Pattern lifted from the operator's working `link_audit.py` script.

**Config-driven entity list** — read from `<vault-root>/.claude/audit-memory-config.yml` if it exists. Schema:

```yaml
entities:
  - name: <Client Name>
    canonical_path: <agents/account-manager/memory/<client>.md>
    pattern: '\b<Client Name>\b'
  - name: <Project Codename>
    canonical_path: <agents/chief-of-staff/memory/projects/<codename>.md>
    pattern: '\b<Codename>\b'
scope_dirs:
  - agents/*/memory
  - inbox
  - _from_rook
skip_dirs:
  - _archive
  - worktrees
  - .claude
recency_days: 14
```

If `audit-memory-config.yml` is missing, skip this section gracefully.

**Detection algorithm:**
1. For each file under `scope_dirs` (skipping `skip_dirs`), filter by mtime > now - recency_days
2. Strip existing wikilinks: `re.sub(r'\[\[[^\]]+\]\]', '', txt)`
3. Strip markdown links: `re.sub(r'\[[^\]]+\]\([^)]+\)', '', stripped)`
4. For each entity pattern, count matches in the stripped text
5. Aggregate by entity → list of `(file, mention_count)`
6. Output top-5 files per entity, sorted by mention count

**Reported as:**
```
WIKILINK HYGIENE — plain-text mentions not wrapped

<Entity Name> → N mentions across M files. Canonical: <path>
    NNx  <relative-path>
    NNx  <relative-path>
    ...
```

Do NOT auto-wrap mentions — surface for operator review only. The pattern catches drift; the operator decides whether each mention should become a wikilink or stay plain text (sometimes intentional).

## Report format

```
## Audit Results — YYYY-MM-DD

### ✅ Working
- ...

### ⚠️ Gaps
- ...

### 🚨 P0 (fix before next session)
- ...

### Wikilink hygiene
- <Entity> → N plain-text mentions across M files

### Proposed org-chart adjustments
<tree diagram of recommended moves>

### Recommended next actions (in order)
1. ...
```

After delivering the report, STOP. Wait for the operator to approve which items to fix. Do not modify any files during the audit phase.

## Output discipline
- Terse. No preamble, no trailing summary.
- Flag findings, don't narrate the search.
- If the operator asks to fix items, address them one at a time — do not batch-fix without confirmation on each.

## Owner

This skill is owned by the **librarian** agent. Librarian's autonomous-by-design audit cycle invokes this skill as her canonical audit engine. See `agents/librarian/SKILL.md` for the wrapper that schedules and gates this skill's invocation.
