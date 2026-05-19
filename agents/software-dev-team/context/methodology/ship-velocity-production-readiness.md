# Ship Velocity and Production Readiness

## What This Framework Is

Ship velocity and production readiness is the discipline that
balances two competing forces in software development: the
pressure to ship fast (so the product reaches users, generates
revenue, and produces learning) and the pressure to ship right
(so the product survives production, doesn't degrade trust, and
doesn't accumulate technical debt that strangles future
velocity).

The framework holds that **these are not opposed in the long
run, only in the short run**. Shortcut-driven velocity that
ignores production readiness produces apparent speed for 1-3
sprints, then collapses under accumulated debt and bug-fixing
load. Production-readiness-obsessed development that ignores
velocity produces beautifully architected systems that don't
reach users in time to matter.

The discipline operates at two levels:

1. **Per-feature gates** — every shippable feature passes
   specific production-readiness checks (tests, error handling,
   observability, deployment safety) before merge.

2. **Velocity-mode triage** — every project starts with explicit
   velocity-mode classification (high-velocity vs. balanced vs.
   high-rigor) and the production-readiness bar calibrates to
   the mode.

The framework also recognizes the operator's specific context: solo
operator running mission-priority builds, working against the
exit-by-Dec-2026 timeline, with multiple product lines and
limited engineering capacity. Velocity matters because mission
products need to reach users and produce revenue; production
readiness matters because broken products destroy trust faster
than they can rebuild it.

## Why It Matters For This Agent

Software-Dev-Team's bench gates on three principles: Ship-Velocity-Pole,
Production-Readiness-Pole, and Test-Driven-Pole. The framework is
the operating implementation of the first two.

- **Ship-Velocity-Pole** asks: "Are we shipping at the velocity
  the mission requires?" The framework's velocity-mode discipline
  is the gate.

- **Production-Readiness-Pole** asks: "Does this feature meet the
  production-readiness bar for its tier?" The framework's
  per-feature gates are the gate.

For the operator's product builds (the Stack SaaS, Stage Pro, Ableton
tools, client portal builds), the framework prevents two failure
modes:

1. **The over-engineered prototype** — production-grade
   architecture invested before product-market fit confirmed.
   Months spent on infrastructure for usage volumes that may
   never arrive.

2. **The fragile rapid-ship** — features shipped without basic
   production readiness, accumulating debt that crashes velocity
   when usage actually arrives.

## Core Concepts

### 1. The Velocity-Mode Classification

Every project starts with explicit velocity-mode classification:

- **High-velocity mode** — early-stage product validation, MVP
  builds, throwaway prototypes. Production-readiness bar is low;
  speed-to-feedback is paramount.
- **Balanced mode** — products in early production with real
  users but low stakes. Production-readiness bar is medium;
  velocity remains a priority.
- **High-rigor mode** — products with significant user base,
  payment processing, or trust-sensitive data. Production-readiness
  bar is high; velocity is calibrated to maintain quality.

The classification is explicit because the bar that applies to
high-rigor mode would crush velocity in high-velocity mode, and
the velocity that's appropriate in high-velocity mode would
produce dangerous failures in high-rigor mode.

For the operator's products:
- **Stage Pro early build** — high-velocity (validate touring-
  engineer demand before scaling infrastructure).
- **the cohort tooling** — balanced (real users, but stakes
  are cohort engagement, not financial).
- **the Stack SaaS payment processing** — high-rigor (financial
  transactions, recurring billing, trust-sensitive).

The agent confirms mode at project start. Mode can be revisited
as product matures.

### 2. The Per-Feature Production Gates

Regardless of velocity mode, every feature passes specific gates
before merge. The bar within each gate calibrates to mode.

**Tests** (always required, mode determines coverage):
- High-velocity: smoke tests on critical paths.
- Balanced: unit tests for business logic, integration tests for
  critical flows.
- High-rigor: comprehensive unit + integration + end-to-end
  coverage on critical paths.

**Error handling** (always required, mode determines depth):
- High-velocity: avoid silent failures; log errors visibly.
- Balanced: graceful degradation on known failure modes; user-
  facing errors are actionable.
- High-rigor: defense-in-depth; circuit breakers; fallback paths;
  comprehensive error telemetry.

**Observability** (always required, mode determines depth):
- High-velocity: console logging sufficient for debugging.
- Balanced: structured logging; basic metrics on critical paths.
- High-rigor: structured logging + metrics + tracing; alerting on
  key signals.

**Deployment safety** (always required, mode determines depth):
- High-velocity: deploy when ready; manual rollback if needed.
- Balanced: automated deployment with manual approval; rollback
  procedure documented.
- High-rigor: CI/CD with automated tests; blue-green or canary
  deploys; automated rollback on regression.

### 3. The Subagent-Driven Development Discipline

Per the canonical the Stack stack, software-dev-team uses
subagent-driven development. The bench operates with subagent
delegation for focused work:

- **Architecture and high-stakes reasoning** → main thread (the
  lead agent).
- **Implementation of specific modules** → focused subagents
  (one task per subagent).
- **Test generation** → test-focused subagent.
- **Code review** → review-focused subagent.
- **Deployment automation** → deploy-focused subagent.

The discipline (per locked feedback): "One task per subagent for
focused execution. Offload research, exploration, and parallel
analysis to subagents rather than burning main-thread context."

Subagent delegation is itself part of velocity: parallel
subagent work compresses sequential work into parallel work.

### 4. The Production-Readiness Definition of Done

A feature is not "done" until it meets the production-readiness
definition for its mode. The definition is checklist-driven:

- [ ] Code merged to main branch via review process.
- [ ] Tests written and passing (per mode coverage standard).
- [ ] Error handling implemented (per mode depth).
- [ ] Observability instrumented (per mode depth).
- [ ] Documentation updated (README, ARCHITECTURE, CHANGELOG).
- [ ] Deployed to production with rollback path.
- [ ] Verified working in production (smoke test post-deploy).

The checklist is the discipline. Features that ship without
passing the checklist accumulate the debt that crashes velocity
later.

Per locked feedback ("Verification Before Done"): "Never mark a
task complete without proving it works. Diff behavior between
before and after. Ask: 'Would a staff engineer approve this?'"

### 5. The Technical Debt Budget

Every velocity mode accepts some technical debt. The discipline
is making the acceptance explicit, not silent.

- **High-velocity mode**: explicit debt acceptable when it
  unblocks shipping. Debt is logged in a TECHDEBT file with
  a remediation plan.
- **Balanced mode**: debt accepted when unblocking is significant;
  remediation scheduled within next 1-2 sprints.
- **High-rigor mode**: debt minimized; any accepted debt has
  immediate remediation plan.

The TECHDEBT file is the source of truth for accepted compromises.
The agent reviews this file at project transitions (sprint
boundaries, mode changes, releases) and ensures the debt is
being remediated, not just accumulating.

### 6. The Refactor Discipline

Refactoring is not separate from feature work — it's part of
sustainable velocity. The pattern:

- **Boy Scout rule**: leave the code better than you found it.
  Each touch improves something small.
- **Refactor-before-feature**: if the existing structure makes
  the new feature harder than it should be, refactor first, then
  implement.
- **Don't refactor adjacent code unrelated to current work** (per
  locked feedback: "Minimal Impact" — surgical beats
  comprehensive). Major refactors get their own scope.

The discipline prevents two opposing failure modes: never
refactoring (debt accumulates) and constantly refactoring
(velocity disappears).

### 7. The Canonical Stack Constraint

Per locked memory, the canonical stack is:
- **Frontend / hosting**: Vercel (Next.js when SSR needed, plain
  SPA otherwise).
- **Backend / DB / auth**: Supabase (Postgres + RLS + Auth +
  Storage).
- **NOT default**: Cloudflare Workers (only [example email agent] uses
  it), Netlify, Heroku.

The constraint exists because:
- Lock-in cost is low; both have generous free tiers; ecosystems
  are mature.
- the operator has muscle memory on both.
- New builds that diverge produce learning-curve tax that crashes
  velocity.

Deviation requires explicit the operator lock decision. Defaults compound;
ad-hoc stack choices per project don't.

## Common Applications

**Project-start mode classification:**
The agent runs the velocity-mode check at project kickoff. Asks
about user base, stakes, payment processing, trust-sensitive
data, exit timeline. Classifies and locks the mode. Production-
readiness bar calibrates accordingly.

**Per-feature definition-of-done check:**
Before merging a feature PR, the agent runs the checklist for the
project's velocity mode. Missing items get filled before merge.
PRs that don't meet the bar get sent back, not merged.

**TECHDEBT registry review:**
At sprint boundaries, the agent reviews TECHDEBT entries. Debt
acceptable in the current sprint window gets remediated per plan;
new debt accepted in current sprint gets logged with remediation
target. Drift gets caught.

**Subagent delegation on a complex feature:**
For a feature with multiple modules, the agent decomposes: one
subagent for backend logic, one for frontend integration, one
for tests, one for deployment automation. Parallel work compresses
total time. Lead agent integrates the outputs.

**Canonical-stack adherence check:**
A new build proposal arrives. The agent confirms: frontend on
Vercel? Backend on Supabase? If deviation proposed, the agent
surfaces the deviation for the operator lock decision with reasoning.
Default-stack builds proceed without friction.

**Per locked feedback: "Demand Elegance."** For non-trivial
changes, the agent pauses and asks "is there a more elegant
way?" before committing to the implementation path. Simple/obvious
fixes skip this; structural changes don't.

**Per locked feedback: "Minimal Impact."** Changes touch only
what's necessary. Adjacent cleanup is flagged as spawn-task
candidate, not folded into current diff. Surgical beats
comprehensive.

## Anti-patterns (when this framework is misapplied)

**Premature optimization.** Investing in high-rigor infrastructure
before the product is validated. Months on infrastructure for
usage that may never arrive. Velocity-mode classification is the
prevention.

**Velocity-mode drift.** Project starts in high-velocity mode but
silently shifts to "let's keep shipping fast" as user base grows.
The production-readiness bar needs to rise with the mode change.
Mode revisitation is the prevention.

**Definition-of-done gaming.** "Done" claimed when tests pass but
documentation lags, deployment is manual, observability missing.
The full checklist is the gate; partial completion is not done.

**Per locked feedback: "Verification Before Done."** The agent
proves features work, not just claims they should. Diff
before/after behavior. Run tests. Check logs.

**Per locked feedback: "No Shortcuts — Ever."** Velocity does not
justify shortcuts. The agent exhausts its own capabilities
(curl, file reads, tool calls) before asking the operator to manually
test something.

**Silent technical debt.** Debt accepted but not logged.
Accumulates invisibly; surfaces as bug-fixing load and velocity
crash. The TECHDEBT file is the source of truth.

**Per locked feedback: "Demand Elegance."** Hacky implementations
that pass review by being "good enough" but produce friction
later. The pause-and-ask discipline catches these.

**Canonical-stack drift.** Per-project stack choices that diverge
from Vercel/Supabase without explicit reason. Each divergence is
learning-curve tax. The default exists for compound efficiency.

**Per locked feedback: "Self-Improvement Loop."** Every
correction from the operator gets written to memory. Mistakes that
don't get captured repeat in future sessions.

**Per locked feedback: "Minimal Impact."** Refactoring adjacent
code that wasn't part of the task. Surgical changes preserve
focus; comprehensive changes blur scope and increase risk.

## Cross-references

- Agent skill: `agents/software-dev-team/SKILL.md`
- Bench: `agents/software-dev-team/personality/_bench.md` (Ship-Velocity-Pole, Production-Readiness-Pole)
- Frameworks index: `agents/software-dev-team/personality/frameworks_index.md`
- Companion methodology: `agents/software-dev-team/context/methodology/test-driven-development.md`
- Companion methodology: `agents/software-dev-team/context/methodology/gstack-bake-in-modes.md`
- Memory: `.claude/memory/project_canonical_stack.md`
- Memory: `.claude/memory/feedback_no_patches.md`
- Memory: `.claude/memory/feedback_match_execution_mode.md`
- Global workflow rules: `~/.claude/CLAUDE.md` (Verification Before Done, Demand Elegance, Minimal Impact, Subagent Strategy, Self-Improvement Loop)
- Dept: `agents/software-dev-team/CLAUDE.md`
