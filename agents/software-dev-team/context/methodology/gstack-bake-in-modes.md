# gstack Bake-In Modes

## What This Framework Is

gstack bake-in modes is the discipline of integrating the gstack
virtual engineering team — CEO review, eng manager, designer, QA,
security, release engineer — into every software build at
appropriate points. The framework holds that **gstack is not
optional tooling**: it is the operating system the operator's software-
dev work runs on, and skipping bake-in points produces builds
that fail review gates after the fact.

gstack is installed at `~/.claude/skills/gstack`. The full team
deploys across the standard build loop:

```
/office-hours → /autoplan → build → /review → /qa → /ship
```

Each step corresponds to a specific role:
- **CEO / Strategist**: `/office-hours`, `/plan-ceo-review` —
  before starting any new product or feature.
- **Eng Manager**: `/plan-eng-review`, `/autoplan` — lock
  architecture before writing code.
- **Designer**: `/design-consultation`, `/design-shotgun`,
  `/design-html` — any UI surface.
- **QA Lead**: `/qa`, `/qa-only` — after every build, tests in
  real browser.
- **Security Officer**: `/cso` — before any launch.
- **Release Engineer**: `/ship`, `/land-and-deploy` — ships PRs,
  deploys.
- **Investigator**: `/investigate` — debugging root causes.
- **Retrospective**: `/retro` — weekly.

The discipline: each role's bake-in point is hit at the right
phase. Skipping a bake-in point is allowed only with explicit
reason logged. The default is full bake-in.

Bake-in modes vary by project type:
- **High-velocity mode** — compressed bake-in: `/autoplan` →
  build → `/qa` → `/ship`. CEO review, security review, design
  review may be deferred or compressed.
- **Balanced mode** — standard bake-in across the full loop.
- **High-rigor mode** — full bake-in including `/plan-design-review`,
  `/cso`, `/plan-eng-review`, multiple rounds of `/qa`.

Mode-by-bake-in matching is the discipline. High-velocity work
with full bake-in is overkill; high-rigor work with compressed
bake-in is dangerous.

## Why It Matters For This Agent

Software-Dev-Team's bench gates on three principles: Ship-Velocity-Pole,
Production-Readiness-Pole, and Test-Driven-Pole. gstack bake-in
modes is the cross-cutting discipline that calibrates the build
process to the project mode.

The framework prevents two failure modes:

1. **Bake-in skipping** — running through the build loop without
   hitting gstack roles, producing builds that fail review gates
   when they finally encounter the role's discipline (post-launch
   QA reveals critical bugs; post-launch security review reveals
   vulnerabilities).

2. **Bake-in over-application** — running every gstack role on
   every micro-change, producing process overhead that crashes
   velocity in high-velocity work.

For the operator's product builds, gstack bake-in is what produces
shipped products that meet the production-readiness bar without
absorbing infinite process time. The framework calibrates the
overhead to the stakes.

## Core Concepts

### 1. The Standard Build Loop

The canonical loop (per locked memory) for any non-trivial build:

**`/office-hours`** — for new products or features, validates
whether the build is worth doing at all. Office hours surfaces
the demand reality, the wedge, the customer truth. New the Stack
SaaS ideas, new Stage Pro features, new product lines all start
here.

**`/autoplan`** — runs the full review gauntlet (CEO, design, eng,
DX) with auto-decisions. Surfaces taste decisions at a final
approval gate. One command, fully reviewed plan out.

**Build phase** — actual implementation with TDD discipline (per
companion methodology). Subagent delegation for focused work.

**`/review`** — pre-landing PR review for diff analysis: SQL
safety, LLM trust boundary violations, conditional side effects,
structural issues.

**`/qa`** — systematic QA testing in real browser with iterative
bug fixing. Before/after health scores. Ship-readiness summary.

**`/ship`** — branch detection + tests + diff review + VERSION
bump + CHANGELOG + commit + push + PR.

The loop is sequential by default. Phases can run in parallel
within constraints (e.g., design work in parallel with backend
build), but each phase has its bake-in point.

### 2. The Mode Compression Pattern

Different modes compress the loop differently:

**High-velocity compression:**
- `/autoplan` (skipped or minimal — explicit reason required).
- Build with minimum TDD on critical paths.
- `/qa-only` for report-only QA (skip the auto-fix phase).
- `/ship` directly.
- `/cso` and `/plan-design-review` deferred to next milestone.

**Balanced standard:**
- `/autoplan` runs.
- Build with TDD on business logic.
- `/qa` with auto-fix loop.
- `/ship`.
- `/cso` and `/plan-design-review` for releases that justify it.

**High-rigor full:**
- `/office-hours` for validation.
- `/autoplan` plus `/plan-design-review` separately if UI work.
- Build with full TDD coverage on critical paths.
- `/qa` with multiple rounds.
- `/cso` before any launch.
- `/ship` with full review.
- `/land-and-deploy` for production rollout.

Mode classification gates compression. High-velocity mode is not
the default for everything; it requires explicit justification
(early validation work, throwaway prototype, time-critical bug
fix).

### 3. The `/autoplan` Bake-In

`/autoplan` runs the full review gauntlet at planning time:

- CEO review (strategic fit, ambition check).
- Eng review (architecture, edge cases, performance).
- Design review (UI surfaces, before implementation).
- DX review (developer-facing surfaces).

Output: a reviewed plan with surfaced taste decisions. The plan
is the contract for the build phase.

The bake-in is at the start of the build cycle, not retroactively.
Building first and reviewing later produces rework — the review
surfaces issues the build already committed to.

### 4. The `/qa` Bake-In

`/qa` runs at the end of every build, before ship. The skill:

- Systematically tests the web application.
- Fixes bugs iteratively in source code.
- Re-verifies with before/after screenshots.
- Commits each fix atomically.
- Produces a ship-readiness summary.

The discipline: every shipped build runs `/qa` (or `/qa-only` for
report-only mode). The agent doesn't ship work that hasn't been
QA-tested.

The bake-in is non-negotiable in balanced and high-rigor modes;
high-velocity mode may skip with explicit reason.

### 5. The `/cso` Bake-In

`/cso` runs before any launch with significant external exposure.
The skill:

- Infrastructure-first security audit.
- Secrets archaeology, dependency supply chain, CI/CD pipeline
  security.
- LLM/AI security, skill supply chain scanning.
- OWASP Top 10, STRIDE threat modeling.
- Daily mode (zero-noise, 8/10 confidence gate) and
  comprehensive mode (monthly deep scan, 2/10 bar).

The bake-in is at launch time, not retroactively. Security
issues surface at the most expensive moment when caught
post-launch (active exploitation, customer trust damage,
regulatory exposure).

In high-rigor mode (payment processing, financial data, trust-
sensitive operations), `/cso` runs before any release. In balanced
mode, `/cso` runs for releases that justify it. In high-velocity
mode, `/cso` is deferred but tracked in TECHDEBT.

### 6. The `/ship` Bake-In

`/ship` is the release engineer role:

- Detects + merges base branch.
- Runs tests.
- Reviews diff.
- Bumps VERSION.
- Updates CHANGELOG.
- Commits.
- Pushes.
- Creates PR.

The discipline (per the operator's global rules): proactively invoke
this skill — do NOT push or PR directly — when the user says
code is ready, asks about deploying, wants to push code up, or
asks to create a PR. The skill is the canonical mechanism.

### 7. The `/investigate` Bake-In

`/investigate` runs whenever debugging is required. Four phases:
investigate, analyze, hypothesize, implement. Iron Law: no fixes
without root cause.

Per the operator's global rules: proactively invoke this skill — do NOT
debug directly — when the user reports errors, 500 errors, stack
traces, unexpected behavior, or is troubleshooting why something
stopped working.

The discipline catches the failure mode where developers fix
symptoms instead of root causes, producing patches that survive
until the next symptom surfaces.

## Common Applications

**New the Stack SaaS feature build (balanced mode):**
The agent classifies as balanced. Build loop:
1. `/autoplan` produces the reviewed plan.
2. Build with TDD on business logic.
3. `/qa` runs and surfaces 3 bugs; auto-fixes 2; flags 1 for
   manual decision.
4. `/ship` creates the PR.
The cycle takes 1-2 days for a medium feature; bake-in overhead
is ~20% of total time; quality is balanced-mode appropriate.

**Stage Pro experimental feature (high-velocity mode):**
The agent classifies as high-velocity (early validation, no users
yet on this feature). Compressed loop:
1. `/autoplan` skipped (explicit reason: validation-stage; will
   discard if signal is weak).
2. Build with smoke tests only.
3. `/qa-only` for report-only.
4. `/ship` direct.
Cycle takes hours, not days. Bake-in overhead is ~5%.

**the Stack payment integration (high-rigor mode):**
The agent classifies as high-rigor (financial transactions).
Full loop:
1. `/office-hours` to validate the approach.
2. `/autoplan` + `/plan-design-review` separately.
3. Build with full TDD coverage on payment logic.
4. `/qa` with multiple rounds.
5. `/cso` before any deploy to production.
6. `/ship` with full review.
7. `/land-and-deploy` for canary monitoring.
Cycle takes 1-2 weeks; bake-in overhead is ~40%; high-rigor mode
justifies the cost.

**Production bug investigation:**
A user reports a Stage Pro error. The agent triggers
`/investigate` rather than debugging directly. Four phases run:
investigate (gather data), analyze (identify root cause),
hypothesize (propose fix), implement (apply fix with test).

**Weekly retro:**
End of week, the agent runs `/retro`. Reviews shipped work,
patterns, code quality metrics. Output: lessons for next week's
work. Memory file updated with patterns.

**Pre-launch security check:**
Before launching the the Stack SaaS publicly, `/cso` runs
comprehensive mode. Output: list of findings with severity.
Critical findings block launch; lower findings get logged in
TECHDEBT with remediation plan.

## Anti-patterns (when this framework is misapplied)

**Bake-in skipping silently.** Running through the build loop
without hitting gstack roles, claiming velocity reasons. Builds
that haven't been QA-tested ship with bugs; builds that haven't
been `/cso`-reviewed launch with security issues. The framework
requires explicit reason logged for any skipped bake-in.

**Bake-in over-application.** Running every gstack role on every
micro-change. Process overhead crashes velocity. The mode
classification is the prevention.

**Per locked feedback: "Plan Before Executing."** `/autoplan` is
the canonical plan-before-execute mechanism. Skipping it for
non-trivial work means executing without a plan.

**Per locked feedback: "Verification Before Done."** `/qa` is
the canonical verification mechanism. Skipping it means claiming
done without verification.

**Per locked feedback: "Self-Improvement Loop."** `/retro` is
the canonical reflection mechanism. Weekly retros compound
learning. Skipping retros means learning doesn't compound.

**Direct git operations.** Pushing or creating PRs without `/ship`.
Misses the version-bump + changelog + diff-review discipline.
Per the operator's global rules, the skill is the canonical mechanism.

**Direct debugging without `/investigate`.** Debugging symptoms
without root-cause discipline. Per the operator's global rules, the
skill is the canonical mechanism. Bypass produces patches that
survive only until the next symptom.

**Mode classification skipped.** Building without classifying
the velocity mode. Default-compression applies; high-rigor work
ships under high-velocity discipline; quality suffers.

**`/cso` deferred indefinitely.** "We'll do security review
later." Later doesn't arrive; launch happens; security issues
surface post-launch at the worst possible time. The bake-in is
at launch time, not later.

**Per locked feedback: "Demand Elegance."** Bake-in points are
the elegance forcing-function. Skipping bake-in produces hacky
work; running bake-in produces work that passes review gates.

**Per locked feedback: "Compound Knowledge."** `/retro` outputs
get written to memory. Skipping the write means lessons don't
compound across sessions.

## Cross-references

- Agent skill: `agents/software-dev-team/SKILL.md`
- Bench: `agents/software-dev-team/personality/_bench.md`
- Frameworks index: `agents/software-dev-team/personality/frameworks_index.md`
- Companion methodology: `agents/software-dev-team/context/methodology/ship-velocity-production-readiness.md`
- Companion methodology: `agents/software-dev-team/context/methodology/test-driven-development.md`
- gstack install: `~/.claude/skills/gstack`
- Global workflow rules: `~/.claude/CLAUDE.md` (gstack — Virtual Engineering Team section)
- Dept: `agents/software-dev-team/CLAUDE.md`
- Memory: `.claude/memory/project_canonical_stack.md`
