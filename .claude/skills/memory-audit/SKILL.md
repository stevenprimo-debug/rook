---
name: memory-audit
description: Active audit of the operator's memory system. Runs 5 health checks (index size, missing HEAD blocks, stale posture files, sync-bloat folders, contradiction map). Writes a dated report to `_output/` so the operator reads it on the operator's phone. Designed to run on `/schedule` daily OR `/loop` interval OR manually. No autonomous fixes — surfaces issues, asks the operator to lock decisions. The active layer that the passive memory storage was missing.
when_to_use: Daily health check on the memory system. Run on `/schedule` (cron, nightly while the operator is offline) OR manually when something feels off. NOT a fix-it agent — a surface-issues agent.
dept: CEO
owner: CEO master / cross-cutting meta
version: v1
captured: 2026-05-14
status: active
---

## For future Claude (TL;DR — pinned HEAD as of 2026-05-14)

**What this is:** Active audit layer for the memory system. The corrective pattern from `feedback_memory_architecture_failure_modes.md` (Pattern 1-3).

**5 checks (in order):**
1. **Index file size vs 24KB load limit** — flag MEMORY.md, MEMORY_PROJECTS.md, MEMORY_DEPTS.md if any are over.
2. **Files without HEAD blocks** — every `*/memory/*.md` should have `## For future Claude` in first 30 lines. Skip log files (`*_log.md`), capture-keyword YAML, index files.
3. **Posture files past stale-after gate** — read `last_verified` + `stale_after_days` frontmatter. Flag any file whose age exceeds the gate.
4. **Sync-bloat folders** — top 10 folders by size. Flag any >500MB that aren't in Obsidian `userIgnoreFilters`.
5. **Contradiction map** — files that mention the same concept (e.g., "brand palette", "brand colors") with different active values. Surfaces silent conflicts.

**Output:** Single markdown file `out/YYYY-MM-DD-memory-audit.md`. Phone-readable summary. Issues + action recommendations + zero autonomous fixes.

**Run modes:**
- Manual: `pwsh agents/chief-of-staff/skills/memory-audit/run.ps1`
- `/loop 1h` — every hour during a session
- `/schedule` — cron, daily 6am CT (recommended)

## Why this exists

Memory architecture failed 3 days in a row in early May 2026:
- 2026-05-12 — DESIGN slop (CREATIVE DIRECTOR not dispatched first)
- 2026-05-13 — Skill abstract-curriculum vs real-skill mismatch
- 2026-05-14 — FINANCE refused SOXL on stale Apr-24 posture

Root cause: memory is passive storage; no active recall, no staleness gate, no contradiction surfacing. The product can't ship in this state. This skill is the first piece of the active layer.

## Invocation

**Manual run:**
```powershell
pwsh agents/chief-of-staff/skills/memory-audit/run.ps1
```

**Output path:**
```
_output/YYYY-MM-DD-memory-audit.md
```

**Scheduled run (after the operator confirms cadence):**
- Use `mcp__scheduled-tasks__create_scheduled_task` with cron `0 6 * * *` (6:00 AM CT daily)
- Task body: invokes this skill, writes report
- the operator gets a fresh report on the operator's phone every morning via Obsidian Sync

## What this skill DOES NOT do

- ❌ Auto-fix issues. Surfaces only.
- ❌ Git operations. Per locked rule 2026-05-09.
- ❌ Delete files. Per Compounding-Append rule 2026-05-09.
- ❌ Rewrite memory content. Pure read + report.

## Drift axes (what this skill watches over time)

| Axis | Healthy | Warning | Critical |
|---|---|---|---|
| Index size | <20KB | 20-24KB | >24KB |
| HEAD coverage | >80% | 50-80% | <50% |
| Stale posture files | 0 | 1-2 | 3+ |
| Sync-bloat folders | 0 | 1 | 2+ |
| Contradictions | 0 | 1-2 | 3+ |

Composite health score 0-10. Posted at top of every report.

## Self-improvement protocol

After each run, if the operator corrects a check (false positive, missed issue, output format), append to `memory/audit_lessons.md` in this skill's folder. Refine the next run accordingly.
