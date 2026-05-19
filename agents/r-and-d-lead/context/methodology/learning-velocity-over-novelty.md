# Learning Velocity Over Novelty

## What This Framework Is

Learning velocity over novelty is the R&D operating principle that
prioritizes experiments designed to produce decision-relevant
learning fast over experiments that pursue novelty for its own
sake. The framework holds that **the R&D output that matters is
learning, not artifacts** — and that the rate at which an experiment
produces learning is the primary metric, not the technical
impressiveness or breadth of what gets built.

The discipline reframes the R&D question. The common framing is:
"What cool thing should we build?" The learning-velocity framing
is: "What hypothesis, if tested fastest, would unblock the most
downstream decisions?"

Three core moves underpin the discipline:

1. **The decision-coupling test** — what mission-dept decision
   does this experiment unblock? If the experiment doesn't couple
   to a real downstream decision, it's exploration for exploration's
   sake — fine for personal learning, not R&D resource.

2. **The cheapest-test-first principle** — whatever the experiment,
   identify the cheapest test that would generate the key learning,
   and run that first. Expensive elaborate experiments rarely
   beat cheap focused ones at producing learning.

3. **The learning-per-hour metric** — experiments are evaluated on
   how much learning they produce per hour of researcher time. High
   ratio: keep designing experiments this way. Low ratio:
   restructure.

Novelty is not refused — but novelty is not a value in itself.
Novel experiments that produce decision-relevant learning are
ideal. Novel experiments that produce no decision-relevant
learning are personal exploration that doesn't belong in R&D
resource allocation.

## Why It Matters For This Agent

R&D Lead's Learning-Velocity-Pole gates every experiment on the
rate of decision-relevant learning produced. The pole catches
three specific failure modes:

1. **Cool-prototype trap** — researchers build impressive
   prototypes that don't couple to any decision. The artifact is
   admirable; the learning is irrelevant to mission depts.

2. **Over-engineered experiments** — researchers build elaborate
   test rigs when a cheap probe would have produced the same
   learning in 1/10 the time.

3. **Learning-blind iteration** — researchers iterate on a
   prototype without naming what new learning each iteration is
   supposed to produce. Iteration without learning hypotheses is
   activity, not progress.

For the operator's R&D pipeline, learning-velocity discipline is what
prevents the mission depts from being starved while R&D produces
beautiful demos that no dept can use. the Stack, Ableton, and
Software Dev each have specific downstream decisions that R&D
can unblock — experiments not coupled to those decisions get
deprioritized.

## Core Concepts

### 1. The Decision-Coupling Test

Before any experiment starts, the agent asks: "What specific
mission-dept decision does this experiment unblock?"

Strong couplings:
- "If real-time generative visuals work at <50ms latency, Stage
  Pro adds a generative-visuals tier in the 2026 release cycle."
- "If LLM-driven cohort onboarding produces 70%+ first-week
  retention, the cohort 4 ships with this onboarding
  flow."
- "If the cue-verification UI passes touring-engineer usability
  testing, Software Dev builds it into Stage Pro core."

Weak couplings (or no couplings):
- "If TouchDesigner can produce X, we'd have cool visuals."
- "If we explored agentic commerce, we'd understand the space
  better."
- "If we built a prototype Y, we could see what it's like."

Weakly coupled experiments fail the test. Strong couplings get
priority. The mission-dept decision is the receiver; the
experiment is the unblocker.

### 2. The Cheapest-Test-First Principle

For any hypothesis, multiple test designs are possible. The
discipline: identify the cheapest test that would produce the
key learning, and run that test first.

Example — testing "real-time generative visuals at <50ms latency":

- **Expensive test**: build a full Stage Pro extension prototype
  with UI, MIDI integration, and visual library. 4-6 weeks.
- **Medium test**: build a working patch in TouchDesigner that
  responds to MIDI with one visual primitive. 1-2 weeks.
- **Cheap test**: measure baseline latency of MIDI-to-render
  pipeline in TouchDesigner with no actual visual logic. 1-2
  days.

The cheap test answers the key question (is the latency
foundation viable?). If the cheap test fails, the medium and
expensive tests would have failed for the same reason — and 5-6
weeks would have been wasted. If the cheap test succeeds, the
medium test runs next with confidence the foundation is sound.

The principle compounds: serial cheap tests, each unblocking the
next, produce learning faster than parallel expensive ones.

### 3. The Learning-Per-Hour Metric

Every experiment retrospective asks: how much learning did this
produce per researcher hour invested?

High ratio (good):
- Experiment produced 3-4 distinct learnings that change downstream
  decisions, in 8 hours.
- Cheap probe falsified hypothesis in 2 hours, freeing 40+ hours
  that would have been spent on the elaborate test.
- Single working slice surfaced 2 unknown constraints, in 6 hours.

Low ratio (restructure):
- 40 hours of elaborate prototype, learning surfaced only at the
  end: "the approach we picked doesn't work."
- 20 hours of iteration on a prototype that already met its
  criteria — diminishing returns.
- 60 hours exploring a space with no specific hypothesis;
  resulted in vague awareness, no decision unblocked.

The metric is qualitative, not strictly quantitative. The
discipline is the recurring question: "Was this hour producing
learning, or just producing artifact?"

### 4. Hypothesis Iteration

Iterating on an experiment requires naming the new hypothesis each
iteration is supposed to test. Without this naming, iteration
becomes activity without learning.

Iteration-with-hypothesis:
- v1: Does the basic pipeline work? (yes/no)
- v2: Now that v1 works, what's the latency floor? (specific
  measurement)
- v3: Now that latency floor is X, does fidelity scale with
  reduced GPU resources? (specific measurement)
- v4: Now that v3 results suggest Y, does this approach hold under
  touring laptop hardware? (specific test)

Iteration-without-hypothesis:
- v1: Got the basic thing working.
- v2: Improved it.
- v3: Refactored.
- v4: Added more features.

The latter is activity, not learning. Each iteration must name what
new hypothesis it tests.

### 5. The Adjacent-Possible Map

Per Stuart Kauffman's "adjacent possible" concept, every state of
the R&D pipeline opens specific next-state possibilities. The
discipline: at each decision point, map the adjacent possibilities
and pick the one with highest learning-velocity payoff.

Example:
- Current state: Touch Designer experiment failed latency criteria.
- Adjacent possibilities:
  - (A) Try Notch (different visual engine).
  - (B) Try Unity-based custom pipeline.
  - (C) Abandon real-time and pivot to pre-rendered cues.
  - (D) Re-scope to non-real-time use cases (post-show).
- Learning-velocity scoring:
  - (A) Cheap test: 1 week to verify Notch latency. Medium payoff.
  - (B) Expensive: 6+ weeks. High payoff if it works, but slow.
  - (C) Easy: 1 week. Low payoff (changes the product
    fundamentally).
  - (D) Cheap reframe: 2 days. Low immediate payoff but unblocks
    a different product direction.

Pick the highest learning-velocity option for the next experiment.

### 6. The Speed-of-Falsification Bias

A hypothesis you can falsify quickly is more valuable to test
than a hypothesis that takes forever to falsify — even if both
are equally plausible.

Why: in fast-moving categories (AI tooling, real-time graphics),
context shifts under you. A hypothesis that takes 6 months to
falsify may become irrelevant before the test completes. A
hypothesis that takes 1 week to falsify (or confirm) produces
learning that's still relevant.

The discipline biases experiment design toward fast-falsifiable
hypotheses. Slow-falsifiable hypotheses get restructured into
sequences of fast-falsifiable ones, with each enabling the next.

### 7. The Personal-Exploration Boundary

Some experiments are personal exploration: the researcher wants
to learn TouchDesigner, learn Unity, learn AI APIs. This is
valuable — but it's not R&D resource allocation.

The discipline: personal exploration happens on personal time, not
R&D time. R&D experiments must couple to mission decisions.

The boundary is gentle (researchers need exploration time to
remain capable; mission depts benefit from researchers who know
the landscape) but real (mission-priority work doesn't fund pure
exploration).

## Common Applications

**Pre-experiment design review:**
The agent reviews proposed experiments against the decision-coupling
test, cheapest-test-first principle, and time-box. Experiments
that fail get sent back for sharpening. Experiments that pass get
green-lit with explicit hypothesis, criteria, time-box, and
receiving dept named.

**Mid-experiment learning audit:**
The agent reviews active experiments weekly. Asks: "What learning
has this produced this week? What learning does next week's work
target?" Experiments without specific weekly learning hypotheses
get restructured.

**Post-experiment retrospective:**
At kill or graduation, the agent runs the learning-per-hour
retrospective. What learning was produced? What was the hour cost?
What patterns emerge for future experiment design? Patterns get
captured in R&D memory for future experiments to inherit.

**Cheap-probe protocol for new hypotheses:**
Before any multi-week experiment, the agent asks: "What's the
cheapest 1-2 day probe that would produce the key learning?" If
the cheap probe exists, it runs first. If the cheap probe
falsifies the hypothesis, the multi-week experiment is canceled
before it starts.

**Per locked feedback: 60-minute product evaluation rule.** The
R&D lead applies this to experiment ideation: in 60 minutes, can
this experiment show coupling to a mission decision, a clear
hypothesis, and a cheap-test path? If not, the experiment doesn't
get green-lit.

**Adjacent-possible mapping at experiment kill:**
When an experiment kills, the agent maps adjacent possibilities
for the next experiment. Picks the highest learning-velocity
option. Avoids the trap of pivoting blindly to "something
adjacent" without scoring the options.

## Anti-patterns (when this framework is misapplied)

**Cool-prototype trap.** Building impressive prototypes that don't
couple to mission decisions. The artifact is admired; the mission
depts can't use it; the resources didn't produce mission
progress.

**Over-engineering.** Elaborate test rigs when cheap probes would
produce the same learning. The 6-week prototype that surfaces a
learning the 2-day probe would have produced is the failure.

**Iteration without hypothesis.** Continuing to refine a prototype
that has already met its criteria, or iterating without naming
what new hypothesis each iteration tests. The discipline requires
hypothesis-per-iteration.

**Per locked feedback: "60-Minute Product Evaluation Rule."**
Applied to R&D: experiments must show plan + learning + decision-
coupling in 60 minutes of evaluation, or they don't enter the
R&D pipeline.

**Per locked feedback: "Demand Elegance."** R&D learning compounds
into elegant solutions when graduations happen. Inelegant prototypes
that drift in R&D without graduation produce neither learning nor
elegant solutions.

**Per locked feedback: "Self-Improvement Loop."** Each experiment's
learning becomes memory for future experiments. Skipping the
capture violates the rule and breaks the compounding.

**Personal exploration on R&D budget.** Researchers using R&D
resources to explore personal interests that don't couple to
mission decisions. The boundary is real; exploration belongs on
personal time, mission work belongs on R&D time.

**Speed-of-falsification ignored.** Designing experiments that
take months to falsify when shorter tests would produce the same
learning. The 6-month experiment that returns "this doesn't work"
when a 1-week probe would have returned the same answer is the
failure.

**Per locked feedback: "Verify Project Status Before Speaking."**
R&D status reports must reflect actual experiment state, not
optimistic recollections. Honest status enables honest
learning-velocity assessment.

## Cross-references

- Agent skill: `agents/r-and-d-lead/SKILL.md`
- Bench: `agents/r-and-d-lead/personality/_bench.md` (Learning-Velocity-Pole)
- Frameworks index: `agents/r-and-d-lead/personality/frameworks_index.md`
- Companion methodology: `agents/r-and-d-lead/context/methodology/kill-or-graduate-discipline.md`
- Memory: `.claude/memory/feedback_sixty_minute_rule.md`
- Memory: `.claude/memory/feedback_no_patches.md`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `agents/r-and-d-lead/CLAUDE.md`
