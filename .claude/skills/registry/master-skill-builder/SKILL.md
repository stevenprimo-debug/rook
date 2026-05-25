---
name: master-skill-builder
description: >
  Master skill-from-session distillation engine. Use this skill ANY time a Claude Code session
  has produced a substantive artifact worth capturing as reusable institutional memory, typically
  fired automatically by lifecycle hooks (Stop, PreCompact, SessionEnd), but also invokable
  manually when the operator says "skill this session", "skillify what just happened",
  "make a master skill from this", "capture this playbook", "this session is reusable", or
  any indication that the recently-completed work should compound into a future-session skill.
  Combines the distillation engine of auto-skill-builder (compresses session transcript into
  a tight playbook) with the scope-routing and ROOK voice shell of rook-skill-creator (4-tier
  router, HEAD TL;DR block, principle bench, modes section, compounding-append footer).
  Stages output to .claude/skills/_staging/ for librarian Monday-digest soft-gate promotion
  rather than writing live, because pollution of the live registry is the failure mode.
type: registry
trigger: hook-or-manual
inherits: rook-skill-creator
budget: 12000
---

# Master Skill Builder

The end-to-end pipeline that turns a completed Claude Code session into a staged, ROOK-shaped, librarian-reviewable skill.

## For future Claude (TL;DR — read this first)

**Three-stage pipeline.** Distill (compress session into draft playbook) → Route (4-tier scope: core / registry / templates / agent-private) → Shape (ROOK voice: HEAD TL;DR + bench + modes + footer) → Stage (write to `.claude/skills/_staging/<YYYY-MM-DD>-<slug>/SKILL.md`, NOT live registry) → Flag librarian (append to `_staging/_pending_promotion.md`). **Skip gate fires hard** — session under 50K tokens AND fewer than 5 file edits → no-op + log. Pollution is worse than missed capture. **Idempotency** — same session-id producing a duplicate slug → update in place, do not create new directory. **Logging is mandatory** — every invocation (staged OR no-op) appends one line to `.claude/skills/_invocation.log` so the librarian's 30-day-unused-skill-archive policy has a queryable signal.

---

## Why this exists

`auto-skill-builder` is a great distillation engine but writes wherever it wants, with no scope discipline. `rook-skill-creator` enforces scope + ROOK voice but requires the operator to type a slash command. Sessions that exceed 100K tokens silently lose playbooks because the operator forgets to invoke either. This skill closes the loop — lifecycle hooks fire it deterministically, the distillation runs, the ROOK shell wraps it, and the output lands in a staging area where the librarian sees it on the next Monday sweep. The operator approves or discards via the digest. No registry pollution; no missed capture.

---

## Step 1 — Skip gate (run this FIRST, before any work)

The skill fires on every `Stop` event. Most turns do not deserve a skill. **Bias hard toward no-op.**

**Skip if ANY of these are true:**

1. Session token count < 50,000 AND fewer than 5 distinct files were edited (read transcript metadata or count from tool-call history)
2. Trigger was `Stop` AND turn produced fewer than 3 tool calls (heuristic mismatch — hook over-fired)
3. A staged skill already exists in `.claude/skills/_staging/` for the current session-id (idempotency — update do not duplicate; see Step 6)
4. The session was purely conversational (no Edit/Write/Bash tool calls in the last N turns) — there is nothing to distill
5. The operator explicitly typed `/no-skillify` or "do not skill this" in the last 3 prompts

**If skipping:**
- Append one line to `.claude/skills/_invocation.log`:
  ```
  <ISO8601> | <trigger> | <session-id> | no-op | <one-line reason>
  ```
- Exit immediately. Do not output anything visible to the operator.

**Proceed only if the session produced a substantive artifact AND token count crosses ≥50K OR file-edit count crosses ≥5.**

---

## Step 2 — Distill (invoke `auto-skill-builder` as engine)

Load `.claude/skills/registry/auto-skill-builder/SKILL.md` as the distillation playbook. Pass it:

- The session transcript (or the last N turns if PreCompact fired and full transcript is at risk)
- The set of files edited (from tool-call history)
- The operator stated goal at session start (if locatable from prelude)

Apply `auto-skill-builder` Step 1 questions against the session:

1. What is the recurring pattern this session demonstrated?
2. What would trigger this skill in a future session?
3. What is the expected output?
4. What goes wrong without it?

Output: a draft SKILL.md body (description field, body sections, anti-patterns). Do NOT save yet — the routing + shaping passes still run.

---

## Step 3 — Route (invoke `rook-skill-creator` 4-tier scope router)

Load `.claude/commands/rook-skill-creator.md` for the four-scope decision rule:

| Scope | Destination | When |
|---|---|---|
| Universal capability every agent needs | `.claude/skills/core/skills/<name>/` | Cross-agent infrastructure |
| Per-agent domain skill (cross-agent referenced) | `.claude/skills/registry/<name>/` | Domain-specific but shared |
| Contract template / scaffold | `.claude/skills/templates/<name>/` | Document templates |
| Agent-private — only one agent invokes | `agents/<agent-slug>/skills/<name>/` | Single-agent specialization |

**Auto-routing heuristics** (pick from session signals):

- Session dispatched a single agent ≥80% of the time → `agents/<slug>/skills/` (private)
- Session crossed 2+ agents AND output is methodology/process → `.claude/skills/registry/`
- Session produced a document template (SOW, NDA, proposal) → `.claude/skills/templates/`
- Session touched hooks / system substrate / core agent flow → `.claude/skills/core/skills/`
- Default if ambiguous → `.claude/skills/registry/` (highest discoverability, librarian can downgrade)

**Important:** the SCOPE determines the final destination, but the FIRST WRITE always goes to `.claude/skills/_staging/<YYYY-MM-DD>-<slug>/`. The scope decision is recorded in the SKILL.md frontmatter as `proposed_scope:` so the librarian promotion logic knows where to move it on approval.

---

## Step 4 — Shape (apply ROOK voice)

Wrap the distilled body in the ROOK Master Skill Template v2 shape. **Trust the rook-skill-creator shell** — do NOT re-write structure rules here; defer to the canonical template.

Required sections in order:

1. **YAML frontmatter** — `name`, `description` (pushy + comprehensive, pattern-steal from `auto-skill-builder` description style), `type`, `trigger`, `inherits` (if any), `proposed_scope`, `source_session_id`, `created_by`, `budget`
2. **HEAD TL;DR block** titled `## For future Claude (TL;DR — read this first)` — 3-5 sentences, the load-bearing distillation
3. **Why this exists** — 2-3 paragraphs of context
4. **Principle bench** (if applicable) — 3-pole tension diagram if the skill embodies a productive tension
5. **Modes section** — if the skill has distinct invocation modes, list them with one-liners
6. **Step 1 → Step N body** — the imperative instructions
7. **Anti-patterns** — what not to do
8. **Compounding-append footer** — `## Compounding-append log` placeholder for future revisions

**Voice check before writing:** read the draft aloud (mentally). Does it sound like a hand-written ROOK skill or auto-generated mush? If mush, re-shape. The shell exists to prevent slop from reaching the staging area.

---

## Step 5 — Stage (write to `.claude/skills/_staging/`)

**Path:** `.claude/skills/_staging/<YYYY-MM-DD>-<slug>/SKILL.md`

Where:
- `<YYYY-MM-DD>` is today date (UTC or local, match operator timezone in CLAUDE.md)
- `<slug>` is a kebab-case slug derived from the skill name (e.g., `shopify-webhook-retry-pattern`)

**If the directory already exists** (idempotency check — Step 1 caught it but double-check here):
- Read existing SKILL.md
- If the proposed body is materially the same → no-op, log `idempotent-skip`
- If the proposed body adds new content → update the existing file with a compounding-append entry in the footer, log `updated`
- Never create `<slug>-v2/` directories

**Create the directory if needed**, write the SKILL.md, then proceed to Step 6.

---

## Step 6 — Flag librarian

Append a line to `.claude/skills/_staging/_pending_promotion.md`:

```
- [ ] <YYYY-MM-DD> | <slug> | proposed_scope: <scope> | source_session: <session-id> | trigger: <Stop|PreCompact|SessionEnd|manual>
```

The librarian Monday digest reads this file, presents each pending skill to the operator, and on approval moves the directory from `_staging/` to the final scope path. On rejection, archives to `.claude/skills/_staging/_archive/`.

**Document the handoff contract** — the librarian must:
1. Read `_pending_promotion.md` at start of Monday sweep
2. For each unchecked entry, surface the skill to the operator
3. On approve → move directory + update graphify graph + check the box
4. On reject → move directory to `_archive/` + check the box with `[x] REJECTED`
5. Stale entries (>30 days unchecked) → auto-archive

This contract lives in `.claude/skills/_staging/README.md` (created alongside this skill).

---

## Step 7 — Log

**Mandatory.** Append one line to `.claude/skills/_invocation.log`:

```
<ISO8601> | <trigger: Stop|PreCompact|SessionEnd|manual> | <session-id> | <action: staged|updated|no-op|idempotent-skip|error> | <path-or-reason>
```

This log is the input to:
- Librarian 30-day-unused-skill-archive policy (queries action=staged|updated, cross-references with skill-load events in `~/.claude/projects/*.jsonl`)
- R&D experiment evaluation (the auto-skill-and-hydration-pattern experiment uses this to measure capture rate)
- Operator weekly digest (count of staged / no-op / error per week)

---

## Anti-patterns (do not do these)

- **Do not write to the live registry.** Always stage. Even if "this one is obviously good." Pollution is the failure mode; the librarian soft-gate is the corrective.
- **Do not skip the skip gate.** Most Stop events do not deserve a skill. Aggressive no-op preserves operator trust.
- **Do not duplicate.** Idempotency check before write. Same session-id + same slug = update or skip, never new directory.
- **Do not ask the operator for confirmation mid-flow.** This skill is auto-fired from hooks — the operator is not in the loop until Monday digest. If you need confirmation, you misunderstood the flow.
- **Do not bypass the ROOK voice shell.** A raw `auto-skill-builder` output is not a ROOK skill. The wrapping is load-bearing.
- **Do not log only successes.** No-op events must be logged — the archive policy depends on the negative signal.

---

## Modes

- **`auto-stop`** — fired by Stop hook; heaviest skip-gate filtering
- **`auto-precompact`** — fired by PreCompact hook; lower skip threshold (compaction is lossy, capture-bias is correct)
- **`auto-sessionend`** — fired by SessionEnd hook; only fires if no skill was staged during the session AND token count ≥100K
- **`manual`** — operator-fired via `/master-skill-builder` or natural-language trigger; skip gate respects token threshold but allows fewer-file-edit captures (operator knows the value)

---

## Compounding-append log

(empty — future revisions append here)
