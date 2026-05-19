# Compounding-Append Pattern

## What This Framework Is

The Compounding-Append pattern is the memory-architecture
discipline that governs how knowledge accumulates across sessions,
agents, and time. The framework holds that **memory is the moat**
— an agent (or organization) that compounds its lessons reliably
outperforms one that does not, regardless of raw capability — and
that the compounding mechanism is the discipline of append rather
than rewrite.

The framework is named "git-shape" because it borrows the
discipline of version control: every memory update is a new
record appended to history, never a silent rewrite of past
records. When facts contradict, the contradiction is surfaced as
a question for the operator to lock — never resolved by the
agent inferring which version is "correct" and quietly
overwriting.

Three operating principles:

1. **Append, don't rewrite.** New information adds to memory; old
   information is preserved with its timestamp and context.
   History is the moat.

2. **Surface contradictions.** When new information contradicts
   prior memory, the agent surfaces the conflict to the operator
   — never resolves it silently.

3. **HEAD pointer at top.** The most-current "what to know now"
   summary lives in a pinned `## For future Claude (TL;DR)` block
   at the top of each memory file, refreshed when the underlying
   knowledge changes.

The pattern is distinct from "Karpathy-shape" memory architecture
(which rewrites the memory wiki on each update). The 25% of
Karpathy-shape that fits — contradiction-surface, future-Claude
preamble, confidence levels — is codified directly. The 75% that
doesn't fit — rewrite-on-update, scheduled rewrite agents, external
research commands — is rejected.

## Why It Matters For This Agent

Librarian's bench gates on three principles: Compounding-Pole,
Contradiction-Surface-Pole, and Pruning-Pole. The Compounding-Append
pattern is the operating implementation of the first two.

- **Compounding-Pole** asks: "Did this session's lessons get
  written to memory in a way that compounds for future sessions?"
  The pattern answers: lessons are appended with timestamp and
  context, never rewritten or lost.

- **Contradiction-Surface-Pole** asks: "When new information
  contradicts prior memory, did I surface the conflict for the
  operator?" The pattern answers: contradictions trigger
  operator-lock requests, never silent reconciliation.

For the operator's organization, the compounding pattern is what allows
multi-agent operations across many sessions and projects to share
institutional knowledge without losing fidelity. Without it, each
session is amnesiac — the agent that learned a lesson in May
forgets it by July, and the same mistakes repeat.

## Core Concepts

### 1. The Append Rule

Every memory update is a new entry, timestamped, appended to the
relevant memory file. Prior entries remain. Format:

```markdown
## 2026-05-15 — Lesson: <slug>

<New information, with context and reasoning>

**Status:** Active / Superseded by <date>
```

When a new entry supersedes an older one, the older entry is
marked `Status: Superseded by 2026-05-15` — but the older entry
remains in the file. Future readers can trace the evolution.

Why this matters: the reasoning that produced the older entry is
preserved. When the older entry's reasoning later becomes relevant
again (the conditions that caused the superseding event reverse),
the original reasoning is still available.

### 2. The Contradiction-Surface Discipline

When new information contradicts prior memory, the agent does NOT:
- Silently overwrite the old memory.
- Pick the "newer" one and discard the older.
- Try to reconcile by inferring which is "correct."

The agent DOES:
- Surface the contradiction to the operator.
- Present both versions with their context and timestamps.
- Request operator-lock on which version is correct (or whether
  both are correct in different contexts).
- Append the operator's lock decision to memory.

Example surfaced contradiction:

> Memory says "[your employer] stealth mode active — no public marketing
> mentioning [your employer]" (2026-04-15).
> New session input: "Going full public with [your employer] name in
> marketing." (2026-04-28)
>
> These contradict. Lock decision?
>
> Operator: "Stealth reversed. Full public mode."
>
> → Append: "2026-04-28: Stealth mode REVERSED. Full public
> launch greenlit. Supersedes 2026-04-15 entry."

The original 2026-04-15 entry remains in memory with `Superseded
by 2026-04-28` annotation.

### 3. The HEAD Pointer (Future-Claude TL;DR)

Each memory file opens with a pinned block:

```markdown
## For future Claude (TL;DR)

<2-5 bullets capturing the current "what to know now" summary>

Last verified: 2026-05-15
```

This block is the HEAD pointer — the most-current operating
summary, designed for a future agent (or the same agent in a
future session) to absorb quickly without reading the full
versioned history.

The HEAD block is updated whenever the underlying knowledge
changes. The append-discipline still applies: the prior HEAD
content moves into the body of the file with timestamp, and the
new HEAD reflects current state.

Why this matters: agents that load memory in a token-constrained
context need a fast-path to current state. Without the HEAD
pointer, the agent reads chronological history and may absorb
older versioning state before reaching current state.

### 4. Confidence Levels

Each memory entry carries an implicit or explicit confidence
level:

- **Locked** — the operator has confirmed this directly. Highest
  confidence.
- **Observed** — derived from session data (the operator's behavior,
  observed pattern, repeated correction).
- **Inferred** — agent's working hypothesis from incomplete data.
  Lowest confidence; flag for operator confirmation.

When agents load memory, they weight inferred entries less than
locked entries. Inferred entries that survive multiple sessions
without contradiction can be promoted to observed; observed
entries confirmed by the operator are promoted to locked.

Promotion is appended, not overwritten:

```markdown
**Status:** Inferred 2026-04-12 → Observed 2026-04-29 → Locked 2026-05-06
```

### 5. The Pruning Discipline

Append-forever risks file bloat. The pattern prescribes:

- **Cap individual memory files at ~400 lines.** When approaching,
  split by topic into sister files.
- **Quarterly audit cycle.** Review memory files, identify
  permanently-superseded entries that can be archived (moved out
  of active memory into an archive file, not deleted).
- **Index discipline.** A top-level `MEMORY.md` indexes all memory
  files with one-line descriptions. When files grow, the index
  is updated.

Archived entries remain accessible (in case the conditions that
produced them recur), but they are not loaded by default.

### 6. The Index Pattern

Every memory hierarchy (root, dept-scoped, sub-dept-scoped) has
an `MEMORY.md` index file. The index lists every memory file
with a one-line description. Loading the index gives an agent
the table of contents; the agent then loads specific files as
needed.

Index hierarchy for the operator's vault:
- Root: `.claude/memory/MEMORY.md` — global memory loaded
  every session.
- Sister indices: `MEMORY_PROJECTS.md`, `MEMORY_DEPTS.md` — split
  when the main index grew past 200 lines.
- Dept-scoped: `agents/<dept>/memory/MEMORY.md` (when the
  dept memory volume justifies an index).

### 7. The Failure-Mode Diagnostic

Memory architecture has specific failure modes (per locked
feedback file `feedback_memory_architecture_failure_modes.md`):

- **Wall failures** — agent reaches a memory wall and can't
  proceed because the relevant memory isn't loadable.
  *Diagnostic:* HEAD blocks missing, index-load limits exceeded,
  or routing false-positives loading wrong dept memory.
- **Drift failures** — agent loads memory but operates against
  outdated state. *Diagnostic:* last-verified timestamps stale,
  HEAD not updated when underlying knowledge changed.
- **Contradiction failures** — two memory entries contradict and
  agent picks the wrong one. *Diagnostic:* contradiction never
  surfaced, never locked.

The pattern operationalizes the fixes: HEAD pointers, last-verified
timestamps, index discipline, contradiction-surface protocol.

## Common Applications

**Session-end memory write:**
The agent identifies lessons learned in the session, drafts entries
for each, and appends them to the relevant memory files. New
entries include timestamp, context, and a one-line summary suitable
for index inclusion.

**Contradiction detection during session start:**
When the agent loads memory at session start and detects two
entries that contradict (one says X, another says not-X), the
agent surfaces the contradiction to the operator before proceeding. Lock
decision is appended.

**HEAD refresh:**
When a memory file's underlying knowledge changes (a project
status updates, a feedback rule is added or reversed, a process
is locked), the agent updates the `## For future Claude (TL;DR)`
block at the top of the file. The prior HEAD content moves into
the body with timestamp.

**File-split trigger:**
A memory file grows past 400 lines. The agent identifies the
natural split (by topic, by time period, by project) and proposes
the split to the operator. Approval triggers split; old file becomes
archive or sister index entry.

**Quarterly memory audit:**
The agent runs `anthropic-skills:audit-memory-skills` (or
equivalent). Output: list of memory entries flagged for
review (stale timestamps, contradicted but never locked, indexed
incorrectly). the operator reviews and locks resolutions; agent appends
the locks.

**Cross-agent memory share:**
A memory entry in `agents/memory/` becomes relevant
to a separate agent's domain. Rather than copying, the relevant
agent's memory references it via wikilink. Single source of truth
maintained; references compound across agents.

## Anti-patterns (when this framework is misapplied)

**Silent rewrite.** Overwriting prior memory with new information
without preserving the prior version. The reasoning that produced
the prior entry is lost. When conditions reverse, the original
reasoning cannot be retrieved.

**Contradiction silent-resolve.** Agent decides which contradicting
entry is "correct" and updates accordingly without surfacing to
operator. the operator loses the chance to confirm the operating reality,
and memory drifts from his actual current state.

**HEAD pointer rot.** The `## For future Claude (TL;DR)` block
becomes outdated because nobody refreshed it when underlying state
changed. Agents load memory and operate against stale current-state
summary.

**Index abandonment.** Memory files proliferate without index
updates. New agents can't find relevant memory because the index
doesn't list it.

**Per locked feedback: "Compounding-Append + Contradiction-Surfacer
pattern."** The locked pattern (2026-05-09) is the standard. Any
deviation requires the operator lock.

**Per locked feedback: "Memory Architecture Failure Modes."** The
specific failure modes (HEAD blocks missing, last-verified
timestamps stale, index-load-limit exceeded, routing
false-positives) are the diagnostic checklist.

**Per locked feedback: "Filter — Personal-Tool Patterns vs
Agent-Team Patterns."** The append pattern serves multi-agent
team operations. Single-user "just rewrite my notes" patterns are
not the standard.

**Pruning by deletion.** Removing memory entries because they
seem stale, without operator lock. Stale entries get archived,
not deleted. The reasoning that produced them may become relevant
again.

**Per locked feedback: "Self-Improvement Loop."** Every correction
becomes a memory entry. Skipping the write fails the workflow
rule.

## Cross-references

- Agent skill: `agents/librarian/SKILL.md`
- Bench: `agents/librarian/personality/_bench.md` (Compounding-Pole, Contradiction-Surface-Pole)
- Frameworks index: `agents/librarian/personality/frameworks_index.md`
- Vendored reference: `agents/librarian/context/references/anthropic-ama-architecture.md`
- Companion methodology: `agents/librarian/context/methodology/graphify-driven-audit.md`
- Vault root rules: `_CLAUDE.md` (compounding-append pattern git-ops rule locked)
- Memory: `.claude/memory/MEMORY.md`
- Memory: `.claude/memory/feedback_memory_architecture_failure_modes.md`
- Memory: `.claude/memory/feedback_filter_personal_vs_agent_team_patterns.md`
- Memory template: `.claude/memory/_template_memory.md`
