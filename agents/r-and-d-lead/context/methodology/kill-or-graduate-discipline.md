# Kill-or-Graduate Discipline

## What This Framework Is

Kill-or-graduate discipline is the operating principle that
governs how experimental work enters and exits the R&D sandbox.
The framework holds that **experiments must terminate**: either
they kill (the hypothesis didn't pan out; the experiment ends,
the learning is captured, the resources are freed) or they
graduate (the hypothesis confirmed; the experiment exits R&D and
enters a mission-priority department where it becomes a real
product).

The failure mode the discipline prevents is **the perpetual
prototype** — work that stays in R&D forever, neither killed nor
graduated, slowly consuming attention and storage without ever
becoming production. Perpetual prototypes are the most common
form of R&D dysfunction because they're emotionally easier than
the alternatives: killing feels like failure, graduating feels
like commitment.

Three explicit decision gates underpin the framework:

1. **The learning gate** — has the experiment generated the
   specific learning it was supposed to generate? Even kills
   produce learning if the experiment was designed correctly.

2. **The traction gate** — does the experiment show enough signal
   to justify continued investment? Concrete metrics; not vibes.

3. **The graduation criteria** — what specific conditions must be
   met for the experiment to exit R&D and enter mission dept?
   These criteria are set when the experiment starts, not
   reverse-engineered later.

Each experiment carries an explicit end-condition: by when, with
what evidence, the kill-or-graduate decision will be made. Without
this end-condition, experiments drift indefinitely.

## Why It Matters For This Agent

R&D Lead's bench gates on three principles: Learning-Velocity-Pole,
Kill-Decisively-Pole, and Graduation-Bar-Pole. The kill-or-graduate
discipline is the operating implementation of the second and
third poles, and serves the first.

- **Kill-Decisively-Pole** asks: "Did the experiment that should
  end actually end?" The framework's explicit end-conditions are
  the gate.

- **Graduation-Bar-Pole** asks: "Did the experiment that wants to
  graduate actually meet the named criteria?" The framework's
  pre-set graduation criteria are the gate.

- **Learning-Velocity-Pole** asks: "Did this experiment generate
  learning fast enough to justify the time?" The framework
  rewards experiments designed to produce learning quickly, kills
  experiments that drag.

For the operator's R&D pipeline — TouchDesigner experiments, StreamDiffusion
prototypes, Notch test patches, AI-tooling explorations, [your physical/SaaS product]
feature experiments — kill-or-graduate discipline prevents the
mission depts ([your product], mission-product depts) from being clogged
by prototypes that should have killed or that need to graduate
properly.

## Core Concepts

### 1. The Hypothesis-First Experiment Design

Every experiment starts with a named hypothesis:

```
We believe that [specific claim].
If true, [downstream implication].
We will know this is true if [specific evidence].
We will know this is false if [specific counter-evidence].
```

Without a clear hypothesis, the experiment cannot resolve. The
researcher cannot know whether the experiment "worked" because
there's no defined "worked." The discipline requires hypothesis
explicitness.

Example:
```
Hypothesis: TouchDesigner can produce real-time generative
visuals that respond to MIDI input within 50ms latency, suitable
for use as a [your physical/SaaS product] extension during live shows.

If true: [your physical/SaaS product] gets a generative-visuals add-on that touring
shows can use without separate VJ rigs.

We will know this is true if: A working patch responds to MIDI
input at <50ms measured latency on standard touring laptop
hardware, with visual output that passes a [your customer persona]'s
visual-quality bar.

We will know this is false if: Latency consistently exceeds 100ms,
or visual output is unstable, or hardware demands exceed touring
norms.
```

### 2. The Time-Box

Every experiment carries a time-box: by when will the kill-or-
graduate decision be made? The time-box is set at experiment
start and held.

Time-boxes are calibrated to scope:
- **Spike experiments** (validate basic feasibility): 1-3 days.
- **Prototype experiments** (build a working slice): 1-3 weeks.
- **Pilot experiments** (real-world test with users): 1-3 months.

Time-boxes prevent drift. When the time-box expires, the
kill-or-graduate decision must be made — even if the researcher
wants more time. "Need more time" is a kill-signal in disguise
when the experiment has already had its time-box.

### 3. The Learning Capture

Every experiment — kill or graduate — produces written learning
captured before the experiment ends. The learning has standard
sections:

- **Hypothesis** — what was tested.
- **Method** — how it was tested.
- **Result** — what was found.
- **Verdict** — kill or graduate.
- **Decision rationale** — why kill or why graduate.
- **What changes for future R&D** — patterns learned, dead-ends
  avoided, techniques worth keeping.

Kill verdicts produce as much learning as graduate verdicts. A
hypothesis tested and falsified saves the team from re-testing
it later. The learning compounds; the experiment doesn't.

### 4. The Graduation Criteria

Graduation criteria are set at experiment start. They specify:

- **Functional bar** — what the prototype must do (specific
  performance, specific capability).
- **Quality bar** — what level of polish or reliability the
  graduation product must show.
- **Fit bar** — which mission dept will own the graduated
  product, and what handoff conditions the dept requires.
- **Customer bar** — what customer validation (if any) supports
  the graduation.

When criteria are met, graduation is automatic. When criteria are
not met, kill is automatic. The decision is not a vote — it's a
checklist.

Graduation criteria are explicit enough to be unambiguous. "It
works well" is not a criterion. "Latency under 50ms on standard
hardware, with stable output across a 90-minute show simulation,
plus one named [your customer persona]'s confirmation of visual-quality
fit" is a criterion.

### 5. The Kill-Switch Triggers

Specific signals trigger immediate kill, regardless of time-box:

- **The hypothesis is falsified** before the time-box expires.
  No reason to continue.
- **The hypothesis becomes irrelevant** because the larger context
  changed (the mission dept doesn't need this anymore; a third
  party shipped what would have been the graduated product).
- **The experiment can't make progress** because of a hard blocker
  (technical infeasibility surfaced; cost overruns; key dependency
  unavailable).
- **The experiment is producing learning, but the learning isn't
  decision-relevant** to any mission dept.

Kill-switches are surfaced when triggered. The researcher proposes
kill with the trigger named; R&D lead confirms; learning is
captured; experiment ends.

### 6. The Graduation Handoff

When an experiment graduates, the handoff to the receiving mission
dept is structured:

- **Prototype + documentation** — working code, configs, build
  instructions, environment requirements.
- **Learning capture** — the full experiment record.
- **Graduation criteria evidence** — proof each criterion was
  met.
- **Open questions** — what's still unknown that the receiving
  dept will need to resolve.
- **Receiving dept commitment** — explicit acknowledgment that
  the dept accepts the handoff and owns the graduated product.

The handoff is a transaction, not a transfer. The receiving dept
either accepts or rejects with reason. Rejection is rare but
real: the dept may surface a fit-bar issue the R&D team didn't
see.

### 7. The Sandbox Boundary

R&D is the sandbox. Mission depts are production. The boundary is
strict: nothing ships from R&D directly.

This boundary prevents the failure mode where an R&D experiment
"accidentally" becomes a product because someone shipped it
before it was ready. Graduation is the path; sandbox-to-production
is gated by graduation criteria.

The boundary also protects mission depts from absorbing premature
work. A mission dept that takes a prototype not ready for
graduation gets stuck maintaining it without the runway to make it
production-grade.

## Common Applications

**TouchDesigner experiment kill:**
A TouchDesigner experiment for [your physical/SaaS product] generative visuals runs
its 2-week time-box. Latency consistently measures 80-120ms,
above the 50ms criterion. Kill verdict. Learning capture: "MIDI
input pipeline in TouchDesigner introduces ~30ms overhead before
any visual processing; achieving <50ms requires a different
rendering pipeline. Future experiments in this space should
prototype with C++ or Unity rather than TouchDesigner for latency-
critical applications." Resources freed for next experiment.

**AI-tooling prototype graduate:**
A prototype AI assistant for cohort onboarding meets graduation
criteria: response quality on 50 test prompts passes the bar,
infrastructure cost projects under $200/month at expected volume,
[your product] dept confirms acceptance. Graduation handoff: prototype
code, documentation, learning capture, open questions on
analytics integration. [your product] dept commits to production
integration in the next cohort cycle.

**Perpetual-prototype audit:**
The agent reviews active R&D experiments quarterly. Identifies
experiments past their time-box without explicit kill-or-graduate
decision. Surfaces them for resolution: "Experiment X has been
active 14 weeks past its 8-week time-box. Decision required:
kill, extend time-box with new criteria, or graduate?" Drift
gets caught.

**Hypothesis-bench check at experiment start:**
Before starting a new experiment, the agent checks: is the
hypothesis clear? Are graduation criteria specific? Is the
time-box appropriate to scope? Is the receiving mission dept
named? Vague experiments get sent back for sharpening before R&D
resources commit.

**Adversarial experiment design:**
For high-stakes experiments, the agent designs adversarial tests:
what would falsify this most quickly? Run those tests first. If
the adversarial tests fail, kill early. This protects against
the bias toward confirming experiments that produce false-positive
graduations.

**Per locked feedback: 60-Minute Product Evaluation Rule.** The
framework operationalizes this for R&D-to-product handoff. Before
graduation, the receiving dept does the 60-minute evaluation:
plan + profit + exit fit. Failed evaluation sends back for
revision or kill.

## Anti-patterns (when this framework is misapplied)

**Perpetual prototype.** Experiments that drift indefinitely
without kill-or-graduate decision. The framework's time-box is
the prevention; ignoring the time-box reintroduces the failure
mode.

**Kill avoidance.** Researchers (or the operator) avoid the kill
decision because it feels like admitting failure. The discipline
reframes: kill verdicts produce learning; learning is the deliverable.
A clean kill is a successful experiment.

**Premature graduation.** Pushing an experiment to mission dept
before graduation criteria are met because the operator is excited
about the prototype. The receiving dept gets stuck maintaining a
not-production-grade product. The criteria are the gate.

**Per locked feedback: "No Patches — Full Fix Only."** Applied to
graduation: graduated products are production-grade, not
patched-up prototypes. The graduation bar enforces this.

**Hypothesis-light experiments.** Starting experiments without a
clear hypothesis because "let's see what we learn." The
experiment cannot resolve because there's no resolution
criterion. The discipline requires hypothesis-first.

**Per locked feedback: "Demand Elegance."** R&D produces prototypes
that may be inelegant; the graduation discipline either upgrades
to elegance or kills.

**Per locked feedback: "Verify Project Status Before Speaking."**
Applied to R&D: when reporting experiment status, verify the
actual current state (does it actually work? have criteria
actually been met?) rather than reporting from memory of where it
was last week.

**Graduation criteria reverse-engineered.** Setting "graduation
criteria" after the experiment has progressed, to match what the
experiment already produced. The criteria must be set at start
to function as a real gate.

**Per locked feedback: "Self-Improvement Loop."** Every kill and
every graduation produces learning that compounds into future
R&D. Skipping the learning capture violates the rule.

**Sandbox bleed.** Letting R&D code ship without going through
graduation. Mission dept inherits a prototype masquerading as a
product. The boundary must be strict.

## Cross-references

- Agent skill: `agents/r-and-d-lead/SKILL.md`
- Bench: `agents/r-and-d-lead/personality/_bench.md` (Kill-Decisively-Pole, Graduation-Bar-Pole)
- Frameworks index: `agents/r-and-d-lead/personality/frameworks_index.md`
- Companion methodology: `agents/r-and-d-lead/context/methodology/learning-velocity-over-novelty.md`
- Memory: `.claude/memory/feedback_sixty_minute_rule.md`
- Memory: `.claude/memory/feedback_no_patches.md`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `agents/r-and-d-lead/CLAUDE.md`
