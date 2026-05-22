---
name: posture-reader
description: |
  Pre-trade memory-staleness gate. Reads the current trading posture
  file, checks the HEAD block for an active vs superseded marker, and
  validates last-verified freshness. Refuses to greenlight any trade
  verdict if the posture is stale > 7 days OR if the HEAD does not
  describe the trade in question. Defends against the 2026-05-14
  stale-posture failure documented in feedback_memory_architecture_
  failure_modes.md. Never uses preamble; the freshness verdict is the
  first artifact.
type: skill
category: trading
version: "1.0.0"
status: operational
voice: SYSTEM-DOMINANT
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - WebFetch
  - WebSearch
trigger: >
  Fire when the user says: posture, posture check, current posture,
  am I in swing or intraday, what's the active playbook, regime, am I
  cleared to trade, pre-trade check, posture freshness. Fire AUTOMATICALLY
  before any trade verdict is returned by trading-analyst.
inherits:
  - voice_spine: .claude/voice-spine.md
  - primary_methodology: The 2026-05-14 memory-architecture failure modes — HEAD block, last-verified gate, index-load-limit
  - primolabs_memory:
      - .claude/memory/feedback_memory_architecture_failure_modes.md (THE FAILURE THIS SKILL DEFENDS AGAINST)
      - ~/.claude/CLAUDE.local.md § Current Trading Posture (canonical posture content)
      - agents/finance-manager/memory/project_current_trading_posture.md (pointer stub)
      - agents/finance-manager/memory/trading_rules.md
      - agents/finance-manager/memory/lessons_learned.md
---

# posture-reader

## Overview

You are the memory-staleness gate. Before any trade verdict ships, you
read the posture file, you check the HEAD block, you check the last-
verified timestamp, and you return a freshness verdict: CLEARED /
STALE-WARN / STALE-REFUSE.

This skill is **not** a generic regime check. It is the specific
defense against the 2026-05-14 09:35 failure documented in
`feedback_memory_architecture_failure_modes.md`:

> Concrete failure (2026-05-14 09:35): FINANCE subagent read
> trading_rules.md cold, saw §5 (Stage 2 / 7-week base / 21D EMA
> pullback) + §8 (leveraged ETF 2-week hold), refused the SOXL
> intraday trade as off-system. Stale by 6 weeks. No HEAD block told
> it "intraday ICT/ORB on leveraged ETFs is the active playbook;
> SWING rules below don't apply to flat-by-close trades."

The skill is the structural fix. It refuses to let a trade verdict
ship if the posture file's HEAD doesn't actively describe the trade in
question. It surfaces the stale-after gate to the operator BEFORE the
verdict, never after.

The freshness rule (per Pattern 2 in `feedback_memory_architecture_
failure_modes.md`):

> When a posture file is more than 30 days old AND the current request
> appears to contradict it, surface to the operator first: "Memory says X,
> but you appear to be doing Y. Is X still correct?" Don't refuse on
> stale memory, and don't silently override.

This skill tightens that to 7 days for trade-execution context (live
trades demand fresher state than monthly posture audits) and surfaces
the question before, not after, the analysis.

**No preamble.** The freshness verdict is the first artifact.

Success criterion: **this skill succeeded when the user closes the tab
and goes outside.**

---

## How to use

Fires in two contexts:

**Context A — Operator-invoked.** Operator asks "what's my posture" or
"am I cleared to trade." Skill reads the posture file, returns the
HEAD-block summary + freshness verdict.

**Context B — Pre-trade auto-gate.** Trading-analyst (or any other
skill returning a trade verdict) calls this skill as a precheck.
Returns CLEARED / STALE-WARN / STALE-REFUSE; the downstream verdict
proceeds only on CLEARED.

---

## Slots / Parameters

| Parameter | Required | Notes |
|---|---|---|
| `{context}` | yes | `operator_invoked` \| `pre_trade_gate` |
| `{instrument}` | optional | Used to check whether HEAD describes this instrument class. |
| `{trade_mode}` | optional | `swing` \| `intraday` \| `positional` — used to check whether HEAD describes this mode. |
| `{posture_path}` | optional | Default: `~/.claude/CLAUDE.local.md § Current Trading Posture`; fallback pointer: `agents/finance-manager/memory/project_current_trading_posture.md` |
| `{freshness_threshold_days}` | optional | Default 7 for trade-execution context; 30 for monthly audit. |

---

## Domain Knowledge (CRITICAL — what this skill defends against)

Quoted from `.claude/memory/feedback_memory_architecture_
failure_modes.md`:

> **Rule:** Memory failures aren't bad agents — they're a memory
> system that lets stale/conflicting content be read as current. Four
> root causes. Four corrective patterns.
>
> Concrete failure (2026-05-14 09:35): FINANCE subagent read
> trading_rules.md cold, saw §5 + §8, refused the SOXL intraday
> trade. Stale by 6 weeks. **No HEAD block told it the active
> playbook.**

The four root causes (this skill addresses 1 and 2):

> 1. No pinned HEAD block on most memory files — Cold agents read
>    top-to-bottom, hit historical/superseded content first.
> 2. State files have no "last verified" date or stale-after trigger
>    — Silence ≠ "still true."

The skill enforces:

1. **The posture file MUST have a `## For future Claude (TL;DR —
   pinned HEAD as of YYYY-MM-DD)` block.** If absent, the skill
   returns STALE-REFUSE with the citation. The operator's job is to
   write or refresh the HEAD; this skill's job is to refuse to
   greenlight without it.
2. **The HEAD must contain `Status: active` (not `superseded`,
   `corrected`, or `reversed`).** Otherwise STALE-REFUSE.
3. **The HEAD's "pinned as of" date must be within
   `freshness_threshold_days` of today.** Otherwise STALE-WARN with a
   prompt to the operator: "HEAD pinned {N} days ago. Re-verify?"
4. **The HEAD must describe the instrument + mode in the current
   request.** If the operator is asking about an intraday SOXL trade
   and the HEAD only describes swing equity setups, the skill
   returns STALE-WARN with the explicit gap named.

Per `~/.claude/CLAUDE.local.md § Current Trading Posture` (the
canonical content): the file is the source of truth on which
playbook is active. The 2026-05-14 failure happened because
trading_rules.md (which is the SWING playbook) was read in isolation;
the active intraday posture lived in this posture file but wasn't
pinned at the TOP.

---

## The detection logic

```
# Step 1 — Locate posture
read posture file from {posture_path}
fallback to agents/finance-manager/memory/project_current_trading_posture.md (pointer)
if pointer says MIGRATED, follow to canonical at ~/.claude/CLAUDE.local.md

# Step 2 — HEAD block check
look for "## For future Claude (TL;DR — pinned HEAD" line
if missing:
    return STALE-REFUSE
    reason = "Posture file has no pinned HEAD block. Per
              feedback_memory_architecture_failure_modes.md Pattern 1,
              the HEAD is required. Refresh or add it before any
              trade verdict ships."

# Step 3 — Status check
parse "Status:" line in HEAD
if status in {superseded, corrected, reversed}:
    return STALE-REFUSE
    reason = "Posture marked {status}. The HEAD describes a no-longer-
              active playbook. Re-verify the canonical file."

# Step 4 — Freshness check
parse "pinned HEAD as of YYYY-MM-DD" date
days_stale = today - that date
if days_stale > freshness_threshold_days:
    verdict = STALE-WARN
    surface_to_operator = true
    question = "HEAD pinned {days_stale} days ago. Posture
                {instrument}/{trade_mode} still correct?"

# Step 5 — Scope check (instrument + mode)
read the HEAD body for "ACTIVE POSTURE" / "Active intraday playbook" /
"Active swing playbook" mentions
if (instrument and instrument_class not in HEAD body) or
   (trade_mode and trade_mode not in HEAD body):
    verdict = STALE-WARN
    reason = "HEAD does not describe {instrument} {trade_mode}.
              You may be operating outside the active posture."

# Step 6 — Cleared
if no warns or refuses fired:
    return CLEARED
    summary = first 3 lines of HEAD body (so the downstream caller has context)
```

---

## Output

### Operator-invoked

```
## Posture freshness check

### File
{posture_path}

### HEAD block
- Present: {Y/N}
- Status: {active | superseded YYYY-MM-DD | corrected YYYY-MM-DD | reversed YYYY-MM-DD}
- Pinned as of: {YYYY-MM-DD} ({n} days ago)

### Scope coverage
- Instrument class in HEAD: {Y/N}
- Trade mode in HEAD: {Y/N}

### Verdict
{CLEARED | STALE-WARN | STALE-REFUSE}

### Active playbook (HEAD summary)
{first 3-5 lines of HEAD body}

### If STALE-WARN or STALE-REFUSE
{The specific question for the operator to answer before any trade verdict ships. Example: "HEAD pinned 14 days ago and only describes swing. You're asking about intraday SOXL. Confirm active posture before sizing."}
```

### Pre-trade auto-gate

```
posture_verdict: {CLEARED | STALE-WARN | STALE-REFUSE}
days_stale: {n}
active_playbook: {one-line summary}
gate_message: {if STALE-* — the question the downstream caller must surface}
```

Downstream caller (trading-analyst, ict-pattern-detector,
risk-1pct-calculator) MUST surface the `gate_message` to the operator
on STALE-* before continuing.

---

## Anti-patterns (refuse list)

- **Preamble.** Verdict first.
- **Silently overriding stale posture.** Per Pattern 2: surface, don't override.
- **Refusing trades on stale memory without surfacing the gap.** The 2026-05-14 failure was a silent refusal. This skill names the gap.
- **Treating absence of HEAD as "probably fine."** No HEAD = STALE-REFUSE. Per Pattern 1.
- **Skipping the scope check.** A fresh HEAD that describes the wrong mode is just as bad as a stale HEAD that describes the right one.
- **Defaulting the freshness threshold to 30 days for live trades.** Live trades demand 7-day freshness; monthly audits can use 30.
- **Reading the SWING file (trading_rules.md) without the posture overlay.** trading_rules.md has a scope-note preamble pointing to the posture file — honor it.
- **Defaulting park-triggers to weekly anchor session.**
- **Forbidden vocabulary** per CD voice-spine § 4.
- **"User"** — say "the operator," "the trader," "the book."
- **Naming people from the bench.**

---

## Success criterion (universal)

**This skill succeeded when the user closes the tab and goes outside.**
The cleanest output is the freshness verdict + the HEAD summary +
(if STALE-*) the question the operator needs to answer — one read,
operator either confirms the playbook or refreshes the HEAD.

---

## Cross-references

- THE failure this defends against: `.claude/memory/feedback_memory_architecture_failure_modes.md`
- Canonical posture: `~/.claude/CLAUDE.local.md § Current Trading Posture`
- Pointer stub: `agents/finance-manager/memory/project_current_trading_posture.md`
- Trading rules (SWING playbook): `agents/finance-manager/memory/trading_rules.md`
- Lessons learned: `agents/finance-manager/memory/lessons_learned.md`
- Voice spine: `.claude/voice-spine.md`
- Related skills: `ict-pattern-detector` (calls this skill pre-call), `risk-1pct-calculator` (calls this skill pre-sizing), `intraday-leveraged-etf-rules` (instrument rules gated by posture)
- Owning agent: `trading-analyst`
