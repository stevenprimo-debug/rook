# Test-Driven Development

## What This Framework Is

Test-driven development (TDD) is the discipline of writing tests
before writing the implementation those tests verify. The
framework holds that **tests written first force the developer
to specify what the code should do before deciding how it should
do it**, and that this sequencing produces three durable
benefits: clearer interface design, comprehensive coverage, and
durable regression protection.

The classical TDD loop has three phases:

1. **Red** — write a test that describes a behavior the code
   should produce. Run it; it fails (because the behavior
   doesn't exist yet).

2. **Green** — write the minimum implementation that makes the
   test pass. Don't over-build; just satisfy the test.

3. **Refactor** — clean up the implementation now that it works,
   while keeping the test passing.

The loop iterates: each new behavior follows the same Red →
Green → Refactor pattern. Over many iterations, the test suite
becomes both the specification of the code's behavior and the
regression protection against future changes.

TDD is not universally applicable. The discipline applies best
to:
- Business logic with clear input/output expectations.
- Library code with stable interfaces.
- Integration points where behavior matters more than
  implementation.
- Code in high-rigor production mode.

TDD applies less well to:
- Exploratory prototyping (high-velocity mode).
- UI work where visual outcomes matter more than logic.
- Code where the "right" interface is genuinely unknown.

The discipline requires judgment about when to apply it, not
rigid universality.

## Why It Matters For This Agent

Software-Dev-Team's Test-Driven-Pole gates work where TDD applies
on whether tests precede implementation, and whether the test
suite produces durable specification + regression protection.

The pole catches three specific failure modes:

1. **Untested logic** — business logic shipped without tests.
   Future changes break behavior; nobody catches it until users
   report. Trust damage compounds.

2. **Implementation-coupled tests** — tests written after
   implementation that lock in the implementation rather than
   specifying behavior. Changes to implementation require
   parallel changes to tests; refactor becomes painful;
   eventually tests get deleted.

3. **Brittle test suites** — tests that fail for reasons unrelated
   to behavior (flaky timing, hard-coded environment, test order
   dependence). Suite becomes ignored; protection erodes.

For the operator's products, TDD applies most cleanly to:
- **the Stack SaaS** — subscription logic, billing math, cohort
  state machines.
- **Stage Pro** — cue catalog operations, MIDI integration,
  latency calculations.
- **Client portal builds** — business rules, access control,
  data validation.

TDD applies less cleanly to:
- Early Stage Pro UI experiments (visual work, exploratory).
- Cohort marketing pages (content-driven, not logic-driven).
- Throwaway proof-of-concept prototypes.

## Core Concepts

### 1. The Red-Green-Refactor Loop

The loop is the rhythm of TDD work:

**Red:**
- Write a test that describes the new behavior.
- The test should be specific: given X input, expect Y output, in
  Z conditions.
- Run the test; it fails. The failure should be the expected
  failure (function doesn't exist yet, behavior not implemented),
  not an unexpected failure (test broken, environment issue).

**Green:**
- Write the minimum implementation that makes the test pass.
- "Minimum" is key: don't anticipate future tests; don't add
  unrequested features; just satisfy this test.
- Run the test; it passes. Run the full suite; everything still
  passes.

**Refactor:**
- Improve the implementation: remove duplication, clarify naming,
  extract helpers.
- Run tests after every change; they keep passing.
- Refactor is optional per iteration — sometimes the green code
  is good enough.

The discipline: stay in the loop. Don't write code without
a failing test driving it; don't write tests after the code is
done.

### 2. Test Specification vs. Implementation Detail

Strong tests describe **behavior** (what the code should do),
not **implementation** (how the code does it). The distinction:

- **Behavior test**: "Given an active cohort with 30 enrolled
  members, when a new application is approved, the cohort
  member count should be 31."
- **Implementation test**: "Given an active cohort, when
  approveApplication() is called on the CohortService class with
  application_id=42, the database should be updated via an
  INSERT to the cohort_members table with member_id=42."

The behavior test passes regardless of internal implementation
choices; the implementation test breaks when implementation
changes even if behavior is preserved. TDD favors behavior tests.

Implementation tests are sometimes appropriate (testing specific
algorithms, performance characteristics, security boundaries),
but they should be the minority. Most tests describe behavior at
a level the user or calling code cares about.

### 3. The Test Pyramid

Healthy test suites follow a pyramid shape:

- **Unit tests** (broadest base) — fast, focused, many. Test
  individual functions and small modules.
- **Integration tests** (middle layer) — slower, broader, fewer.
  Test interactions between modules, with real dependencies (DB,
  external services).
- **End-to-end tests** (narrow tip) — slowest, broadest,
  fewest. Test full user flows through the deployed system.

The pyramid shape exists because: unit tests catch most bugs at
lowest cost; integration tests catch wiring issues unit tests
miss; e2e tests catch deployment issues integration tests miss.
Each layer has appropriate use; balance is the discipline.

Inverted pyramids (mostly e2e tests) produce slow, flaky test
suites. Pure unit pyramids (no integration or e2e) miss whole
classes of bugs that only appear when modules connect.

### 4. The Test-Per-Behavior Pattern

Each test tests one behavior. The pattern:

```
describe "<feature or module>" {
  it "<specific behavior>" {
    // arrange (set up state)
    // act (do the thing)
    // assert (verify behavior)
  }
}
```

Tests with multiple assertions about different behaviors are
brittle: a single change can break multiple tests for different
reasons. One behavior per test produces clearer failures and
easier maintenance.

Naming convention: the test name describes the behavior in
prose. "When the cohort is full, new applications go to the
waitlist." Reading test names should produce the system's
behavioral spec.

### 5. The Test Independence Requirement

Tests run independently. Each test:
- Sets up its own state.
- Doesn't depend on other tests' state.
- Cleans up after itself if relevant.
- Runs identically regardless of order.

Test-order dependence is a smell. If test B fails when run
without test A, the tests are coupled — and that coupling
produces brittleness.

Independent tests can run in parallel, run in any order, and
fail meaningfully on their own. The discipline pays back when
the suite grows: parallel-runnable tests stay fast even at
hundreds of tests.

### 6. Mocking Discipline

External dependencies (databases, APIs, time, randomness) often
need mocking for unit tests. The discipline:

- **Mock at the boundary** — mock the external interface, not
  internal logic.
- **Don't mock what you're testing** — if you're testing the
  database layer, use a real test database, not a mock.
- **Mock only what's necessary** — over-mocking produces tests
  that pass regardless of real behavior. Each mock is a missed
  integration test.
- **Document mock contracts** — when mocking returns a specific
  value, document the assumption that the real dependency
  returns that shape.

Per locked feedback ("No Patches — Full Fix Only"): mocking
should not substitute for proper integration testing. Mocks
enable unit tests; they don't replace integration tests.

### 7. The Test Coverage Reality

Test coverage metrics (percent of lines/branches executed by
tests) are useful as a floor, not a ceiling. The discipline:

- **High coverage is necessary but not sufficient** — tests can
  execute lines without verifying behavior. Coverage measures
  what's touched; tests measure what's verified.
- **Critical paths require ~100% coverage** — billing, auth,
  data integrity. These paths have severe failure consequences.
- **Non-critical paths can have lower coverage** — internal
  utilities, admin tools, exploratory features. Coverage cost
  doesn't justify on these paths.
- **Coverage tools surface gaps** — but the developer judges
  whether each gap matters.

Per the operator's velocity-mode framework: high-rigor mode demands
high coverage on critical paths; high-velocity mode accepts
lower coverage with the trade-off explicit.

## Common Applications

**New feature in high-rigor mode:**
The agent decomposes the feature into behaviors. For each
behavior:
- Writes the failing test (Red).
- Implements the minimum to pass (Green).
- Refactors for clarity (Refactor).
Sequence produces working code with comprehensive tests in a
single workflow.

**Bug fix in any mode:**
The agent writes a failing test that reproduces the bug. Confirms
the test fails for the right reason (the bug). Fixes the bug;
test passes; full suite still passes. The bug is now covered by
a regression test that prevents recurrence.

**Refactor with test-protection:**
Before refactoring existing code, the agent verifies the
behavior is covered by tests. If gaps exist, tests get written
first (capturing current behavior). Refactor proceeds with
confidence: tests stay green throughout.

**Subagent delegation on test work:**
For comprehensive test suite expansion, the agent delegates to a
test-focused subagent. Subagent works in parallel with main-thread
feature development. Output: expanded test suite that lead agent
integrates.

**Test-suite health audit:**
Periodically, the agent reviews the test suite for: flaky tests
(fail intermittently), slow tests (drag CI), redundant tests
(test the same behavior multiple times), brittle tests (break on
implementation changes). Each category gets remediation.

**Per locked feedback: "Verification Before Done."** TDD
operationalizes this directly. Every shipped feature has tests
proving it works. The proof is the test suite.

## Anti-patterns (when this framework is misapplied)

**Test-after-the-fact.** Writing tests after the implementation
is done. The tests lock in implementation choices made without
test-driven feedback. The discipline of "tests first" produces
better interfaces; tests-after misses this.

**Test-for-coverage-metric.** Writing tests just to hit a
coverage number. Tests don't verify meaningful behavior; they
just touch lines. Coverage metric looks good; bugs slip through.

**Implementation-coupled tests.** Tests that break when
implementation changes even if behavior is preserved. The suite
becomes refactor-hostile; developers stop refactoring; debt
accumulates.

**Brittle test suites.** Tests with timing dependencies, test-order
coupling, environment assumptions. Suite produces false-positive
failures; developers learn to ignore failures; protection
disappears.

**Per locked feedback: "No Patches — Full Fix Only."** TDD bug
fixes write the regression test first. Patches without tests
allow the bug to recur silently.

**Over-mocking.** Mocking so much that tests don't verify real
behavior. The suite passes; production breaks; the gap between
test and reality is what the over-mocking created.

**Per locked feedback: "No Shortcuts — Ever."** TDD is the
shortcut-resistant alternative: comprehensive testing as a
practice rather than as an audit.

**TDD applied to exploratory work.** Forcing TDD on
high-velocity prototypes where the right interface is unknown.
Wastes time writing tests for behavior that gets discarded.
The framework requires judgment about when to apply.

**Per locked feedback: "Verification Before Done."** TDD
operationalizes verification. Skipping tests skips verification.

**Per locked feedback: "Demand Elegance."** Test code benefits
from the same discipline. Brittle, complex test code that
satisfies coverage but produces maintenance burden is not
elegant — refactor it.

**Single-test omnibus.** One test that exercises many behaviors.
Failures don't isolate which behavior broke. The test-per-behavior
discipline prevents this.

## Cross-references

- Agent skill: `agents/software-dev-team/SKILL.md`
- Bench: `agents/software-dev-team/personality/_bench.md` (Test-Driven-Pole)
- Frameworks index: `agents/software-dev-team/personality/frameworks_index.md`
- Companion methodology: `agents/software-dev-team/context/methodology/ship-velocity-production-readiness.md`
- Companion methodology: `agents/software-dev-team/context/methodology/gstack-bake-in-modes.md`
- Skill: `test-driven-development` (referenced in SKILL.md)
- Skill: `verification-before-completion`
- Memory: `.claude/memory/feedback_no_patches.md`
- Global workflow rules: `~/.claude/CLAUDE.md` (Verification Before Done, No Shortcuts, Demand Elegance)
- Dept: `agents/software-dev-team/CLAUDE.md`
- Sub-dept: `agents/software-dev-team/QA/CLAUDE.md`
