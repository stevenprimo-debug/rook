# Spec Discipline

## What This Framework Is

Spec discipline is the operating practice of writing product
specifications that survive contact with implementation. A spec is
not a description of what the team agreed to build; it is the
artifact that makes the build correct, the QA possible, and the
ship-no-ship decision evidence-based. A spec that does not survive
contact with implementation is not a spec — it is a wish list with
formatting.

The framework's spine is **problem-first**: every spec starts with
the problem (named, sized, owned by a specific customer in a
specific circumstance), then states the desired outcome (what
"solved" looks like, measurably), and only then describes the
solution. Specs that invert this order — solution first, problem
hand-waved — fail predictably: the team builds the wrong thing well,
or builds the right thing in a way that misses the actual outcome
the customer needed.

A disciplined spec answers six questions before any implementation
discussion:

1. **What problem does this solve?** (Named job, named customer.)
2. **What does solved look like?** (Measurable outcome.)
3. **Who is this for?** (Specific customer in specific circumstance.)
4. **What's in scope?** (Hard boundary; out-of-scope listed.)
5. **What are the constraints?** (Time, budget, dependencies, risk.)
6. **What does shipped look like?** (Acceptance criteria, demo path.)

When all six questions have honest answers, the implementation is a
direct translation. When any of the six is hand-waved, the spec
will be re-litigated during build — at much higher cost.

## Why It Matters For This Agent

Product Manager's Spec-Discipline-Pole is the gate that prevents
the most common product failure mode: shipping the wrong thing well.
A team building from a sloppy spec produces working code that
solves the wrong problem; a team building from a disciplined spec
produces working code that solves the actual problem.

The pole catches three specific failure modes:

1. **Solution-first specs** — specs that name a feature without
   naming the problem the feature solves. The spec describes "add
   tagging functionality"; the pole inverts to "what job does
   tagging do? Is anyone hiring for it?"

2. **Unmeasurable outcomes** — specs that say "improve the
   experience" without naming what gets measured. The pole demands
   a concrete success metric: time-on-task reduces from X to Y,
   cohort retention rises from A to B, support tickets drop by Z%.

3. **Scope-creep tolerance** — specs that lack a hard "out of scope"
   section, leaving every adjacent improvement candidate as a
   negotiation during build. The pole requires explicit
   out-of-scope listing, with parking-lot for what gets revisited
   next cycle.

For the operator's mission products, spec discipline is what allows him to
run multiple product lines ([your product], [your platform] tools, Stage
Pro, sellable client builds) without each one collapsing under
"one more thing" requests. The spec is the contract; the contract
is what scopes attention.

## Core Concepts

### 1. Problem-First Structure

A disciplined spec opens with the problem, not the solution. The
problem statement names:

- **The customer**: who specifically (the touring playback engineer
  prepping a new venue, not "the user").
- **The circumstance**: when this problem occurs (in venues they've
  never worked, mid-prep, low-time-budget).
- **The current pain**: what's broken in the status quo (manual
  cross-reference of QLab cues against latency specs is slow and
  error-prone).
- **The progress they want to make**: what they're trying to
  accomplish (verify cues with confidence in <10 minutes).

Only after these four are stated does the spec describe the
solution. A spec that opens with "build a latency verification UI"
has skipped the problem definition and will produce a UI that
solves a problem nobody clearly named.

### 2. Outcomes Over Outputs

Spec discipline measures the spec on **outcomes** the customer
experiences, not **outputs** the team produces. Outputs are easy to
ship: lines of code, features released, screens designed. Outcomes
are what the customer can now do that they couldn't before:

- Time to complete the job (reduced from X to Y).
- Confidence in the result (measured by re-verification rate).
- Cohort behavior shift (X% of users now complete this workflow).

A spec whose acceptance criteria are "tag system is implemented and
tested" measures output. A spec whose acceptance criteria are "80%
of cohort completes tagging within 30 seconds, support tickets on
'how do I tag X' drop to <2/week" measures outcomes. The latter
spec is much harder to write — and much harder to game.

### 3. The Scope Boundary

Every spec lists **in scope** AND **out of scope**. The out-of-scope
list is the more important of the two: it names the adjacent
improvements that look obvious during build but are deferred. The
out-of-scope list does three things:

- **Prevents scope creep during implementation** — when the team
  asks "should we also...?", the spec is the answer.
- **Surfaces dependencies** — what was assumed to exist already,
  what was assumed to be handled elsewhere.
- **Creates the backlog for next cycle** — out-of-scope items
  become candidates for the next spec, not floating ideas.

A spec without an out-of-scope section will be re-litigated daily
during build. A spec with a robust out-of-scope section absorbs
those negotiations upfront, in one round, on paper.

### 4. Acceptance Criteria

Acceptance criteria are the **demo path**: the specific sequence of
actions and outcomes that constitute "shipped." Written as
testable statements:

- "User clicks Verify Cues; system returns latency comparison in
  <2 seconds for catalogs ≤100 cues."
- "User receives 3 categorical results: OK, WARN, FAIL, with
  WARN/FAIL surfacing the specific cue and the actionable
  remediation."
- "On QLab catalog re-import, prior verification state persists for
  unchanged cues."

The acceptance criteria are what QA will test against. If a
criterion cannot be tested, it is not a criterion — it is a vague
wish. Specs that lack testable criteria produce ship-no-ship
debates based on opinion rather than evidence.

### 5. The Constraint Set

Specs name constraints honestly:

- **Time** — when does this need to ship, and what happens if it
  slips? (Cohort start date, client deadline, conference demo.)
- **Budget** — engineering hours, infrastructure cost, third-party
  API spend.
- **Dependencies** — what other work must complete first, what
  external services are required.
- **Risk** — what could go wrong, what is the fallback, what is
  acceptable failure mode.

Constraints that are not surfaced in the spec become surprises
during build. The spec's job is to surface them before they
surprise.

### 6. The Customer Reference

Every spec cites the customer — the actual person whose words
shaped the problem statement. The citation may be an interview
quote, a support ticket, a user behavior pattern from analytics.
The point: the customer is named, not assumed.

For [your product] specs, this often means citing Discord conversations,
cohort interviews, or specific email exchanges. The customer
reference is what makes the spec defensible against the most
common pushback: "are we sure anyone wants this?"

### 7. The Decision Log

A spec is a living document. As implementation surfaces new
information — a constraint that wasn't visible, a tradeoff that
emerged, a customer learning — the decision is logged in the spec
itself. Future readers (including the agent re-reading the spec
next quarter) need to know not just what was decided but **why**
it was decided.

The decision log makes the spec compound — future specs cite past
decisions, future agents inherit past reasoning, future audits
trace cause-and-effect rather than guessing.

## Common Applications

**Spec audit before implementation kickoff:**
The agent reads the proposed spec and runs the 6-question gate.
Any unanswered question is surfaced and resolved before kickoff.
Result: the team starts building from a complete spec, not a partial
one.

**Scope-creep refusal during build:**
Mid-build, a feature request arrives: "while we're in there, can we
also add X?" The agent reads the spec, locates the out-of-scope
section, and either confirms X was anticipated (parked for next
cycle) or surfaces X as a true scope expansion requiring spec
update + estimate revision.

**Acceptance-criteria translation for QA:**
The agent translates each acceptance criterion into a testable QA
case. Vague criteria get pushed back to the spec author for
sharpening. Result: QA is testing the spec, not interpreting it.

**Spec compounding via decision log:**
At each major decision point during build, the agent updates the
spec's decision log: "Decided 2026-05-12: API rate limit set to
30/min based on cost analysis; tradeoff = power users on free tier
hit limit but Stripe paid-tier conversion incentive remains intact."
Future specs cite this decision when similar tradeoffs arise.

**Cohort-driven spec revision:**
After cohort launch, the agent reads the cohort feedback
(Discord conversations, exit surveys) and surfaces spec elements
that did not produce the outcomes the spec promised. The next spec
inherits the learning.

## Anti-patterns (when this framework is misapplied)

**Spec written after implementation begins.** "We'll figure out the
spec as we build." This is not iterative development — this is
spec abdication. Iterative development writes a tight spec, builds
the slice, learns, then writes the next tight spec. There is always
a spec; only the scope of each spec is small.

**Vague outcomes.** "Improve the user experience." "Make it more
intuitive." These are aspirations, not outcomes. The spec must name
what gets measured and what threshold means "shipped."

**Solution-disguised-as-problem.** "Users need a tagging system."
This is a solution, not a problem. The actual problem is "users
can't find prior projects when searching by topic." The solution
(tagging) is one of several possible answers. The spec must state
the problem first, then evaluate solutions against it.

**No out-of-scope section.** Every spec eventually faces "should we
also...?" The absence of out-of-scope listing converts each such
question into a fresh negotiation. With out-of-scope listing, the
negotiation happened once on paper.

**Acceptance criteria that cannot fail.** "Tagging is implemented
and works correctly." Cannot be tested — what constitutes "works
correctly"? Acceptance criteria must be specific enough that a QA
engineer (or a QA agent) can produce a pass/fail verdict without
asking the spec author for clarification.

**Per locked feedback: "No Patches — Full Fix Only."** Applied to
spec discipline: if the spec is incomplete, the spec is rewritten
before build. Band-aid additions ("we'll also need to handle X")
fragment the spec and produce inconsistent implementation.

**Per locked feedback: "Verify Project Status Before Speaking."**
Applied to spec discipline: the agent reads memory/project state
before drafting a new spec. Specs that don't reference prior
decisions reinvent solved problems.

**The "platform spec" trap.** Writing one giant spec that covers
multiple jobs ("the platform"). Spec discipline requires
breaking this into job-sized specs, each independently shippable,
each with its own acceptance criteria. Platform specs hide
trade-offs and never finish.

## Cross-references

- Agent skill: `agents/product-manager/SKILL.md`
- Bench: `agents/product-manager/personality/_bench.md` (Spec-Discipline-Pole)
- Frameworks index: `agents/product-manager/personality/frameworks_index.md`
- Companion methodology: `agents/product-manager/context/methodology/jobs-to-be-done.md`
- Memory: `.claude/memory/feedback_no_patches.md`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `.claude/memory/feedback_sixty_minute_rule.md`
- Memory: `agents/product-manager/CLAUDE.md`
