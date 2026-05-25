# `.claude/skills/_staging/` — auto-distilled skill quarantine

This directory is the **soft-gate staging area** for skills produced by `master-skill-builder` from session lifecycle hooks (`Stop`, `PreCompact`, `SessionEnd`).

## Why staging exists

The lifecycle hooks fire deterministically on every session event. Most events do not deserve a skill. The skip gate in `master-skill-builder` filters aggressively, but some over-fires will still happen. Staging gives the operator a **soft-gate review** via the librarian Monday digest before anything pollutes the live skill registry.

**Operator instinct (per r-and-d-lead experiment_auto_skill_and_hydration_pattern.md § 7.5 question 6):** stage to `_staging/`, librarian promotes on Monday. Live-write was rejected — registry hygiene matters more than 7-day lag.

---

## Layout

```
_staging/
├── README.md                       ← this file
├── _pending_promotion.md           ← librarian-readable queue (append-only)
├── _archive/                       ← rejected / stale skills (librarian moves here)
│   └── <YYYY-MM-DD>-<slug>/        ← preserves history of rejected drafts
└── <YYYY-MM-DD>-<slug>/            ← one directory per staged skill
    └── SKILL.md
```

Every staged skill is a complete directory. The librarian promotion logic moves the whole directory (preserving the SKILL.md + any references/ subdir produced by the distillation engine).

---

## Librarian handoff contract

The librarian Monday digest MUST:

1. **Read** `.claude/skills/_staging/_pending_promotion.md` at the start of the weekly sweep.
2. **For each unchecked line item (`- [ ]`)** present the staged skill to the operator with:
   - The `proposed_scope:` from the SKILL.md frontmatter
   - A 1-line summary from the HEAD TL;DR block
   - The source session-id + trigger that produced it
3. **On operator approve:**
   - Move the staged directory from `_staging/<YYYY-MM-DD>-<slug>/` to the path indicated by `proposed_scope:` (e.g., `.claude/skills/registry/<slug>/` or `agents/<agent>/skills/<slug>/`)
   - Update graphify graph to include the new skill node (existing `rebuild-shelf-graph` mode)
   - Check the box in `_pending_promotion.md` as `[x]`
4. **On operator reject:**
   - Move the staged directory to `_staging/_archive/<YYYY-MM-DD>-<slug>/`
   - Check the box as `[x] REJECTED — <one-line reason from operator>`
5. **Stale entries (>30 days unchecked):**
   - Auto-archive to `_staging/_archive/` with `[x] AUTO-ARCHIVED — stale 30d`
   - Operator instinct: if it was not worth approving in 30 days, it is not worth keeping

---

## Hook → master-skill-builder → staging chain

```
[ Stop / PreCompact / SessionEnd hook fires ]
            ↓
  [ master-skill-builder-trigger.ps1 (or .sh) ]
            ↓
  [ skip-gate filter — most events no-op here ]
            ↓
  [ master-skill-builder skill body invoked ]
            ↓
  [ auto-skill-builder distills session → draft body ]
            ↓
  [ rook-skill-creator routes scope → frontmatter proposed_scope ]
            ↓
  [ ROOK voice shell wraps → final SKILL.md text ]
            ↓
  [ WRITE to _staging/<YYYY-MM-DD>-<slug>/SKILL.md ]
            ↓
  [ APPEND to _pending_promotion.md ]
            ↓
  [ LOG to _invocation.log ]
            ↓
  [ librarian Monday digest surfaces for approval ]
```

---

## What does NOT live here

- **Live skills** — once promoted by librarian, they live in their `proposed_scope:` destination
- **Hand-written skills** — operator-authored skills via `/rook-skill-creator` go straight to their final scope; this staging area is for auto-distilled outputs only
- **Reference material** — `references/` subdirs travel with their parent skill on promotion

---

## Anti-patterns

- **Do not edit `_pending_promotion.md` by hand to "approve" things** — the librarian promotion logic handles the directory move and graph update. Manual edits desync the queue.
- **Do not manually move staged directories to live scope** — bypasses the graph-update step and breaks discoverability.
- **Do not delete `_archive/` entries** — the rejection history is the operator signal for tuning the skip gate. Pruning lives in the 30-day-unused-skill-archive policy.
- **Do not auto-promote without librarian** — staging is the soft gate. Live-write bypasses the gate and recreates the pollution risk the staging was built to prevent.
