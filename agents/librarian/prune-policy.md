---
file: prune-policy
agent: librarian
status: customer-tunable defaults
type: policy
---

# Librarian Prune Policy

This file controls how aggressive the librarian is when sweeping your vault each week. Tune these values to match how fast your context turns over.

**Quarantine, never delete.** Every "pruned" file moves to `_archive/<YYYY-MM>/pruned/<slug>.md` with a one-line reason in `librarian-log.md`. You can restore any file at any time with one command.

---

## Default policy (out-of-box)

A file is flagged for quarantine when ALL THREE of these are true:

1. **Stale** — no read in the last 90 days (the librarian tracks read timestamps in `librarian-log.md`)
2. **Orphan** — no other file in the vault links to it (no inbound `[[wikilinks]]` or markdown links)
3. **Not pinned** — the file does NOT have `pin: true` in its frontmatter

If all three conditions hold, the file moves to `_archive/<YYYY-MM>/pruned/` on the next Sunday sweep.

---

## Tuning knobs

Edit the values below. The librarian reads this file every sweep.

```yaml
# How many days before a file is "stale"
stale_after_days: 90

# Require zero inbound links to quarantine?
# - strict: file must have ZERO inbound links AND be stale (default)
# - permissive: file is quarantined on staleness alone, regardless of links
orphan_check: strict

# What to do with files in agents/<agent>/memory/
# - same: apply the same staleness + orphan check (default)
# - never: memory/ files are never auto-quarantined; restore on demand only
# - aggressive: memory/ stale threshold drops to half (45 days at default)
memory_handling: same

# What to do with files in agents/<agent>/context/YYYY-MM/
# - same: standard rules (default)
# - keep_recent: never quarantine current month + last 2 months even if stale
context_handling: keep_recent

# Maximum quarantine count per sweep (safety brake)
# If the sweep would quarantine more than this, the librarian flags for
# manual review in the Monday digest INSTEAD of auto-quarantining.
max_quarantine_per_sweep: 100
```

---

## Pin-true: exempt a file from pruning

Add `pin: true` to any file's frontmatter and the librarian will never quarantine it, regardless of staleness or orphan status.

```yaml
---
pin: true
---
```

**When to pin:**

- Reference material you read infrequently but want kept (style guides, framework attributions, canonical decisions)
- Brand assets, color tokens, voice spine references
- Anything you'd be annoyed to restore from archive

**When NOT to pin:**

- Recent captures (the loop will read them naturally; pinning is for files you expect to go cold but want preserved)
- Active project notes (those get inbound links from current work, so the orphan check protects them)
- Tactical reminders ("buy milk" — let those decay)

Default rule of thumb: if you'd put it in a personal library shelf rather than your inbox, pin it.

---

## The librarian-log.md format

The librarian writes one entry per file per sweep action:

```
2026-05-18 | quarantined | agents/designer/context/2026-02/random-screenshot.md | reason: stale 113d, 0 inbound | restore: librarian restore random-screenshot
2026-05-18 | reconciled  | agents/sales-director/context/2026-05/competitor-pricing.md | routes-to: [marketing-director, deep-researcher] | symlinks created
2026-05-18 | refreshed   | agents/copywriter/memory/voice-patterns.md | last read: 2026-05-12 | counter reset
```

The log is append-only. You can grep it to find anything: "show me everything pruned in the last 30 days" → `grep "quarantined" librarian-log.md | tail -50`.

---

## Restoring a file

From the chat / CLI:

```
librarian restore <slug>
```

The librarian finds the file in `_archive/`, moves it back to its original path, logs the restore in `librarian-log.md`, and (if needed) re-creates symlinks for any `routes-to:` fan-out the file had.

You can also restore manually — just move the file out of `_archive/` back to where you want it. The librarian will reconcile on the next sweep.

---

## The Monday digest

Every Monday morning, the librarian writes `[your reading inbox folder]/<YYYY-MM-DD>-librarian-digest.md` (or your configured digest output path). It contains:

- **Sweep summary:** N quarantined, N reconciled, N refreshed
- **Top 10 quarantine candidates** with one-line reasons
- **Restore shortcuts** for each quarantine
- **Flag list** for anything that hit `max_quarantine_per_sweep` (requires your decision)
- **Health score:** composite 0–10 across staleness coverage, orphan ratio, sync-bloat, contradiction count

Scan it Monday morning, hit a few restores if anything looks wrong, close it. The librarian goes back to background work for the week.

---

## Edge cases the policy handles

**Files with frontmatter `last_verified` + `stale_after_days`:** the librarian uses those values instead of the default 90-day staleness. Useful for posture files that need explicit re-verification cadences.

**Files that were just created:** never quarantined within the first 14 days, regardless of read activity. Lets fresh captures sit and accumulate inbound links before being judged.

**Files with `routes-to:` frontmatter:** quarantined based on the PRIMARY agent's context folder. Symlinks in other agents' folders are removed when the primary file is quarantined. If you restore the file, symlinks rebuild on the next sweep.

**Empty or near-empty files:** `<200 chars and no frontmatter` quarantined regardless of age. These are usually accidental captures that didn't get content written into them.

---

## What the librarian will NEVER do

- Delete files (only quarantine to `_archive/`)
- Run git operations
- Modify file content (read-only on every file it touches)
- Touch files outside `agents/*/context/`, `agents/*/memory/`, and the vault inbox
- Quarantine `_template/` content (those are scaffolding)
- Quarantine `SKILL.md`, `CLAUDE.md`, or `README.md` files (those are agent contracts)

---

## Cross-references

- [`SKILL.md`](SKILL.md) — Librarian master skill (sweep mode, Monday digest template)
- [`../../context-loop.md`](../../context-loop.md) — The five-stage loop the librarian closes
- [`../../hooks/librarian-weekly-sweep.ps1`](../../hooks/librarian-weekly-sweep.ps1) — Windows cron trigger
- [`../../hooks/librarian-weekly-sweep.sh`](../../hooks/librarian-weekly-sweep.sh) — Mac/Linux cron trigger
- [`../../_archive/`](../../_archive/) — Where quarantined files go
