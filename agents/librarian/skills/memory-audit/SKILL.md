---
name: Memory Audit
description: >
  Sweeps every agent's memory/ folder, surfaces stale files (no inbound links + last-read >90d),
  duplicate/near-duplicate notes (cosine on slug + title overlap), broken wikilinks, and orphan
  files (no inbound, no outbound). Returns a single audit report the librarian appends to
  `agents/librarian/memory/audit_log.md`. Generic — works against any ROOK vault.
type: skill
agent: librarian
parent_agent: librarian
version: "2.0.0"
status: operational
---

# Memory Audit — Librarian Skill

## When this fires

- Weekly librarian sweep (Sunday-night cadence) — auto-invoked by `agents/librarian/SKILL.md` modes `daily-graph-audit` and `rebuild-shelf-graph`.
- On explicit operator invocation: "audit my memory", "find stale notes", "what's orphaned", "find duplicate notes".
- Never auto-modifies files. Audit is a SURFACING operation — operator decides what to quarantine via `agents/librarian/prune-policy.md`.

## Inputs (auto-detected — no operator config required)

| Param | How resolved | Default |
|---|---|---|
| `vault_root` | `$ROOK_ROOT` env var → falls back to repo root (4 levels up from this SKILL.md) | repo root |
| `scope` | Optional `--agent <slug>` to scope a single agent's memory; otherwise sweeps all | all agents |
| `stale_threshold_days` | Reads from `agents/librarian/prune-policy.md` frontmatter | 90 |
| `min_inbound_links` | Same source | 1 |

## What the audit measures (per agent's `memory/` folder)

1. **Staleness** — files where `last_modified < today - stale_threshold_days` AND `inbound_link_count < min_inbound_links`. Per-file `last_verified` + `stale_after_days` frontmatter overrides the global threshold.
2. **Duplicates** — files with title overlap ≥0.85 (token-level Jaccard on slug + H1 + first paragraph). Surfaces clusters; never auto-merges.
3. **Orphans** — files with zero inbound AND zero outbound wikilinks. Often accidental captures.
4. **Broken wikilinks** — `[[target]]` references that resolve to nothing.
5. **Stub files** — `< 200 chars` body with no frontmatter. Usually capture failures.
6. **Frontmatter compliance** — files missing required keys per `agents/librarian/SKILL.md` § canonical template (`name`, `description`, `type`, `date`, `confidence`, `ai-first`).

## Output

A single markdown report at `agents/librarian/digests/<YYYY-MM-DD>-memory-audit.md`:

```markdown
# Memory Audit — {date}

## Scope
{agent count, file count}

## Findings
- {N} stale candidates (see table below)
- {N} duplicate clusters
- {N} orphan files
- {N} broken wikilinks
- {N} stub files
- {N} frontmatter violations

## Stale candidates
| File | Last modified | Inbound | Restore-via |
|---|---|---|---|
| ... |

## Duplicate clusters
{cluster table}

## Recommended actions
1. {N} files to quarantine to `_archive/` via `librarian quarantine <slug>` (operator confirms each)
2. {N} duplicate clusters to dedup — surface to operator for canonical pick
3. {N} broken wikilinks to fix (auto-fix candidates listed inline)
```

Append a one-line summary row to `agents/librarian/memory/audit_log.md`:

```
{date} | {scope} | stale={N} dup={N} orphan={N} broken={N} stub={N} fm-violations={N}
```

## What this skill will NEVER do

- Modify a memory file's body
- Delete a file (only quarantine to `_archive/` via the `librarian quarantine` flow)
- Run git operations
- Touch files outside `agents/*/memory/`, `.claude/reference/`, and `inbox/`
- Quarantine `SKILL.md`, `CLAUDE.md`, `README.md`, or any `_template*` file (agent contracts)
- Auto-merge duplicates (only surfaces clusters)

## How the librarian invokes this

In `agents/librarian/SKILL.md`, modes `daily-graph-audit` and `rebuild-shelf-graph` both end with a call to this skill. The librarian also exposes a standalone `audit-memory` mode that runs only this skill (no graph rebuild).

Implementation lives at `agents/librarian/skills/memory-audit/run.py` (created on first invocation — pure Python, stdlib only, no external deps).

## Cross-references

- Quarantine policy: `agents/librarian/prune-policy.md`
- Audit log: `agents/librarian/memory/audit_log.md`
- Graphify shelf rebuild: `agents/librarian/SKILL.md` § `rebuild-shelf-graph`
- Canonical memory template: `agents/_template/memory/_template_memory.md`
