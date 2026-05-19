# Three-Route Dispatch

## What This Framework Is

Three-route dispatch is the operating system that converts every
spitball, voice-dump, hunch, or unstructured idea into one of three
explicit dispositions: **DEPLOY**, **ASSIGN**, or **PARK**. The
framework exists because the failure mode it prevents is severe:
ideas that silently die in inboxes, voice memos, or working memory.
Every idea has a destination. No idea ends in "we'll see."

The three routes serve different time horizons and energy profiles:

- **DEPLOY** — spawn a target agent's subagent now in this session.
  The idea is actionable, the operator has bandwidth, and the
  scope is well-defined enough that immediate execution beats
  waiting. Used when the work fits inside the current session
  and the operator can stay engaged with the output.

- **ASSIGN** — write a brief to `assignments/YYYY-MM-DD-<slug>.md`
  for the dept to pick up later. The idea is actionable but not
  for this session — either because scope exceeds the current
  session, because dependencies aren't met yet, or because the
  operator's attention belongs elsewhere right now. The brief is
  the canonical artifact; the dept owner picks it up when ready.

- **PARK** — log to `memory/idea_log.md` with a follow-up trigger.
  The idea may be valuable later but isn't ready now. It might
  need more evidence, a different season, a maturity threshold to
  cross, or simply more thinking. The trigger is the specific
  condition that resurfaces the idea — never a vague "we'll see."

The framework is enforced through two non-negotiables:

1. **Every spitball ends in DEPLOY / ASSIGN / PARK.** Never an
   ambiguous "interesting, let's think about it." The operator
   gets a decision.

2. **The decision lands in the log.** Per the canonical rule: if
   it didn't land in `idea_log.md`, it didn't happen. The log is
   the source of truth.

## Why It Matters For This Agent

Chief-of-Staff's bench gates on three principles: Dispatch-Decisively-
Pole, Reversibility-Gate-Pole, and Family-Time-Pole. The three-route
dispatch is the operating implementation of the Dispatch-Decisively-
Pole.

- **Dispatch-Decisively-Pole** asks: "Did every spitball end in a
  named disposition?" The framework answers: DEPLOY, ASSIGN, or
  PARK — explicit, logged, no ambiguity.

For the operator's constraint-aware operating mode (per locked memory), three-route
dispatch is the structural backstop against ideas drifting into
working memory and consuming attention. The operator's working
memory is finite; the dispatch system absorbs ideas into
externalized structure so they don't compete for cognitive
resources.

The framework also serves the larger mission: ideas that route
to mission-priority depts ([your product], mission-product depts,
Product Dev) get DEPLOY treatment more often than ideas that
route to [your employer] bridge-revenue work. Mission-first dispatch
discipline is what compounds toward exit-by-Dec-2026.

## Core Concepts

### 1. The Decision Point

Every spitball arrives at the same decision: which of three
routes? The decision is made on five inputs:

- **Reversibility** — is the action reversible (low stakes) or
  irreversible (high stakes: client emails sent, money spent,
  public posts, force-pushes)? Reversibility=N triggers the
  reversibility gate before DEPLOY.
- **Scope** — is the work session-sized, multi-session-sized, or
  unclear?
- **Bandwidth** — does the operator have attention available
  right now, or is current attention committed elsewhere?
- **Maturity** — is the idea ready to act on (specific enough,
  evidence-backed), or does it need to mature?
- **Mission-fit** — does this advance mission ([your product],
  mission-product depts) or fall under bridge-revenue
  ([your employer]) or experimental (RND)?

The framework synthesizes these into a route recommendation. The
operator can override; the framework records the override and
the reason.

### 2. DEPLOY — Now, In Session

DEPLOY is the immediate-execution route. The chief-of-staff spawns
the target dept's subagent and the work begins now.

DEPLOY criteria:
- Scope fits in current session.
- Operator has attention available.
- Idea is mature enough to act on (no pre-work required).
- Reversibility is acceptable (or reversibility gate has been
  passed for N=irreversible actions).

DEPLOY format:
```
ROUTE: DEPLOY
TARGET: <dept>
SCOPE: <one-sentence summary>
SUBAGENT BRIEF: <what the subagent should produce>
REVERSIBILITY: Y / N (if N, confirm before spawn)
LOG: appended to idea_log.md
```

The subagent runs; output returns to the chief-of-staff session;
operator reviews; next disposition follows (ship, revise, park
result).

### 3. ASSIGN — Brief Written, Picked Up Later

ASSIGN converts the idea into a written brief saved to
`assignments/YYYY-MM-DD-<slug>.md`. The dept owner reads the
brief when ready and executes.

ASSIGN criteria:
- Scope exceeds current session, OR
- Operator's attention is committed elsewhere, OR
- Dependencies aren't met yet (but will be soon).

ASSIGN brief template includes:
- Target dept.
- Problem statement (the spitball, distilled to specifics).
- Desired outcome (what "done" looks like).
- Constraints (timing, budget, dependencies).
- References to relevant memory and prior decisions.
- Acceptance criteria.

The brief is the contract. The dept owner doesn't re-litigate the
spitball — the brief carries the operator's intent.

### 4. PARK — Logged With Trigger

PARK converts the idea into a log entry in `memory/idea_log.md`
with an explicit resurfacing trigger.

PARK criteria:
- Idea may have value but isn't ready (needs evidence, season,
  maturity).
- Scope is unclear and would consume attention to define right now.
- Idea is interesting but not aligned with current priorities.

PARK entry format:
```
## <date> — PARK: <one-line idea>
**Context:** <where the idea came from, what triggered it>
**Trigger:** <specific condition that resurfaces it>
**Notes:** <relevant context for future self>
```

The trigger is the discipline. Per locked feedback ("Parked Items
Must Resurface — Never Die in idea_log"), every PARK needs an
idea-specific follow-up trigger. Triggers cannot default to
"Monday Anchor" (the weekly planning block is a checking cadence,
not a trigger).

Valid trigger examples:
- "When [your physical/SaaS product] hits 50 paid users."
- "When [your CRM] implementation completes."
- "When second [your employer] client requests similar capability."
- "When the cohort 4 closes."

Invalid trigger examples (per locked feedback):
- "Monday Anchor" — too vague, not idea-specific.
- "Later" — no condition specified.
- "When I think about it" — no condition at all.

### 5. The Reversibility Gate

Per the locked rule: reversibility=N actions (client emails sent,
prod changes, force-pushes, public posts, money spent) require
explicit operator confirmation before DEPLOY.

The gate mechanism:
1. Chief-of-staff identifies the proposed action.
2. Classifies reversibility (Y or N).
3. If N, surfaces the consequence and asks for explicit confirm.
4. Operator confirms or rejects.
5. Confirmation appended to log; action proceeds.

The gate exists because DEPLOY of an irreversible action without
explicit confirm produces consequences that compound. The
30-second confirmation cost is trivial; the cost of un-doing a
sent client email is high.

### 6. The Idea Log as Source of Truth

`memory/idea_log.md` is the canonical record of every spitball
and its disposition. Read first every session. Updated every
dispatch.

Each entry includes:
- Date.
- One-line idea.
- Route (DEPLOY, ASSIGN, or PARK).
- Status (executing, completed, parked, deprecated).
- Cross-references (assignment file if ASSIGN, dept subagent if
  DEPLOY, trigger if PARK).

The log is what enables compounding dispatch: the chief-of-staff
reads the log at session start and sees what's in flight, what's
parked with triggers active, and what completed recently.

### 7. The Dispatch-Log Companion

`memory/dispatch_log.md` is the companion record specifically for
ASSIGN-route briefs. Lists every brief written, target dept,
status (open, in-progress, completed, deprecated), and
cross-reference to the assignment file.

Useful for: tracking dept workload, identifying briefs that have
gone stale (open but not picked up), surfacing patterns of
ASSIGN volume by dept.

## Common Applications

**Morning spitball intake:**
the operator arrives with three unstructured ideas. Chief-of-staff
classifies each: one is session-sized and mission-fit (DEPLOY
to PRODUCT DEV); one needs CAD reading and exceeds current
session (ASSIGN to ENGINEERING with brief); one is interesting
but premature (PARK with trigger "when [your physical/SaaS product] hits 50 paid
users"). All three end with explicit disposition. None float.

**Mid-session pivot detection:**
the operator, mid-work on a [your physical/SaaS product] feature, says "oh also, I should
think about that LinkedIn post." Chief-of-staff identifies the
pivot, surfaces it explicitly: "current work is [your physical/SaaS product] feature
build; LinkedIn post is a separate thread. PARK for end-of-session?
ASSIGN to MARKETING for tomorrow?" the operator chooses; the dispatch
prevents the silent context-switch that produces unfinished work
on both threads.

**Reversibility gate on client email:**
the operator: "Send the [your employer] follow-up to the [enterprise client] CIO." Chief-of-
staff: "Reversibility=N (client communication). Confirming
content and recipient before send." Operator reviews .eml output;
confirms; send proceeds.

**Mission-fit routing:**
A spitball arrives that could route to either MARKETING ([your employer]
content) or PRIMOLABS (cohort marketing). Chief-of-staff checks
mission-priority order: PRIMOLABS is mission-first (red priority);
MARKETING for [your employer] is bridge-revenue (yellow priority). Default
routing favors PRIMOLABS. Override requires operator decision with
mission-cost noted.

**PARK trigger audit:**
End of week. Chief-of-staff reviews idea_log.md for PARKed items
with active triggers. Surfaces any whose trigger conditions have
been met ([your physical/SaaS product] hit 50 paid users? PRIMOLABS cohort 4 closed?).
Items whose triggers fired get re-routed via the dispatch system.

**Family-time guardrail check:**
A time-sensitive DEPLOY arrives at 3:45pm CT on a Thursday (per
locked schedule, Thursday is one of the operator's remote/family
afternoons). Chief-of-staff surfaces the family-time guardrail:
"DEPLOY is time-sensitive; current time is 3:45pm Thursday
(family afternoon). Defer to morning, or confirm override?"
Operator decides; the guardrail prevented silent absorption of
family time.

## Anti-patterns (when this framework is misapplied)

**Silent absorption.** Chief-of-staff sees an incoming idea and
quietly starts working on it without classifying. The idea
becomes the operator's session whether the operator chose that
or not. The framework requires explicit dispatch.

**Vague dispositions.** "Let's table this" or "we'll see" or
"interesting, let me come back to it." These are not routes.
The framework demands DEPLOY, ASSIGN, or PARK with the trigger
specified.

**PARK without trigger.** Per locked feedback: "Parked Items
Must Resurface." A PARK that defaults to "later" dies in the log.
Every PARK has an idea-specific trigger.

**Per locked feedback: "Don't Default Park Triggers to Monday
Anchor."** Monday Anchor is the weekly planning cadence, not a
trigger. PARK triggers are idea-specific (when X happens, when
Y matures).

**DEPLOY without reversibility check.** Spawning a subagent that
will send a client email, post publicly, or commit destructive
git operations without explicit confirm. The gate exists for a
reason; bypassing it is the failure mode the framework prevents.

**Per locked feedback: "Git operations are DESTRUCTIVE until
strategy is locked."** Applies to all reversibility=N actions.

**Per locked feedback: "Execute, Don't Preamble."** The dispatch
decision is itself the deliverable; no preamble about why this
is a good system or how the chief-of-staff is thinking about it.
Just dispatch.

**ASSIGN-brief vagueness.** A brief that says "look into X" is
not a brief — it's a re-spitball. Briefs require problem
statement, desired outcome, constraints, acceptance criteria.

**Ignoring the log.** Operating without checking idea_log.md at
session start. Drift accumulates: items get parked and forgotten;
DEPLOY items get spawned twice; ASSIGN briefs go stale. The log
is read first.

**Per locked feedback: "Track Session Time + Flag 4pm Hard
Stop."** Dispatch decisions account for time-of-day; deferring
DEPLOY actions past 3:50pm respects the hard-stop guardrail.

## Cross-references

- Agent skill: `agents/chief-of-staff/SKILL.md`
- Bench: `agents/chief-of-staff/personality/_bench.md` (Dispatch-Decisively-Pole)
- Frameworks index: `agents/chief-of-staff/personality/frameworks_index.md`
- Companion methodology: `agents/chief-of-staff/context/methodology/reversibility-gate.md`
- CEO dept: `agents/chief-of-staff/CLAUDE.md`
- CEO master skill: `agents/chief-of-staff/skills/ceo-master/SKILL.md`
- Dispatch playbooks: `agents/chief-of-staff/skills/dispatch-playbooks/SKILL.md`
- Memory: `.claude/memory/feedback_parked_items_must_resurface.md`
- Memory: `.claude/memory/feedback_dont_default_park_to_monday.md`
- Memory: `.claude/memory/feedback_git_operations_destructive_until_strategy_locked.md`
- Memory: `.claude/memory/feedback_track_time_and_flag_4pm.md`
- Memory: `.claude/memory/feedback_monday_anchor.md`
