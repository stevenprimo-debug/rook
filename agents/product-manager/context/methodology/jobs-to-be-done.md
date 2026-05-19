# Jobs-To-Be-Done (JTBD)

## What This Framework Is

Jobs-to-be-Done is a product methodology that reframes the question
of what a product is. The conventional product question — "what
features should this product have?" — assumes the product is the
unit of analysis. JTBD inverts this: the customer is not buying the
product; the customer is **hiring the product to do a job**. The
unit of analysis is the job.

The canonical framing: people don't buy quarter-inch drills; they
hire quarter-inch drills to produce quarter-inch holes. They don't
even want quarter-inch holes — they want what the holes enable
(hanging a picture, mounting a shelf, finishing the room). The job
is the desired progress in a particular circumstance. The product
is the tool that makes that progress possible.

JTBD has three parts:
- **Functional job** — the concrete task to accomplish (mount the
  shelf).
- **Emotional job** — how the customer wants to feel during/after
  (capable, in control, not embarrassed).
- **Social job** — how the customer wants to be perceived (the
  kind of person who finishes home projects).

Most products serve all three, but the functional job is what gets
discussed in interviews; the emotional and social jobs are what
actually drive purchase decisions. A product that nails the
functional job but misses the emotional/social jobs gets used and
abandoned. A product that nails all three becomes the default.

## Why It Matters For This Agent

Product Manager's bench holds three poles: Problem-Truth-Pole,
Spec-Discipline-Pole, and User-Voice-Pole. JTBD is the central
operating frame for all three.

- **Problem-Truth-Pole** asks: "Is the problem real? Is anyone
  actually trying to make this progress?" JTBD answers by forcing
  the question "what job is the customer hiring this for?" — and
  rejecting any spec that cannot answer it concretely.

- **Spec-Discipline-Pole** asks: "Does this spec describe what the
  product does or what the job is?" JTBD demands the spec name the
  job before naming the feature. A feature without a named job is a
  feature looking for a problem.

- **User-Voice-Pole** asks: "Are we hearing the customer's
  language, or the product team's translation of it?" JTBD interview
  technique surfaces the customer's actual language — including the
  emotional and social jobs that the customer often will not name
  directly until asked.

For the operator's mission depts (the Stack, Ableton, Stage Pro), JTBD is
the discipline that prevents the trap of "build features that AV
people might want." Instead: "what job are touring playback
engineers hiring Stage Pro to do, and what are they currently hiring
instead?"

## Core Concepts

### 1. The Job Statement

A well-formed job statement follows this template:

```
When _________________ (situation/context),
I want to _________________ (motivation/action),
so I can _________________ (expected outcome).
```

Example for Stage Pro:
> When I'm prepping a show in a venue I've never worked,
> I want to verify my QLab cues against the actual room latency,
> so I can avoid mid-show audio drift in front of 5,000 people.

The job statement names the **circumstance** (venue I've never
worked — high-stakes, low-familiarity), the **action** (verify cues
against room latency), and the **outcome** (avoid mid-show drift —
emotional job: not being publicly embarrassed; social job: being
the kind of engineer venues book again).

A weak job statement reads like a feature list: "the user can
upload cue sheets and view latency data." This is what the product
does — not what job it is hired to do.

### 2. The Four Forces of Switching

Customers switch from their current solution (which might be
"nothing" or "spreadsheet" or "competitor product") based on four
forces, two pushing toward the new product and two pulling back to
the old:

- **Push of the current situation** — what's broken about the
  status quo? (Pain.)
- **Pull of the new solution** — what does the new product
  promise? (Promise.)
- **Anxiety about the new solution** — what could go wrong? (Risk.)
- **Habit of the old solution** — what's familiar and comfortable?
  (Inertia.)

A new product wins only when Push + Pull > Anxiety + Habit. JTBD
interviews are designed to surface all four forces — not just the
pain (which is what teams typically over-focus on).

For the Stack courses: the push is "I can't keep up with AI
changes." The pull is "structured curriculum + community + the operator's
experience." The anxiety is "another expensive course I won't
finish." The habit is "free YouTube tutorials." The product wins
only when push + pull narratives outweigh anxiety + habit.

### 3. Functional, Emotional, and Social Jobs

Every purchase decision involves all three. The functional job is
typically what customers articulate first ("I need a tool to manage
playback cues"). The emotional job often surfaces when probing why
the functional matters ("because I can't sleep before a show
without being sure"). The social job often surfaces only with
careful questioning ("because the kind of engineer I want to be
doesn't make rookie mistakes in front of stage managers").

A spec that addresses only the functional job ships a working
feature that fails to move the customer to switch. The emotional and
social jobs are where the wedge lives.

### 4. The Interview Protocol

JTBD interviews focus on a specific past purchase decision — not
"what would you want?" but "tell me about the day you decided to buy
X." The interview reconstructs the **timeline**:

- **First thought** — when did the idea first arise?
- **Passive looking** — when did they start noticing alternatives?
- **Active looking** — when did they start actively researching?
- **Decision** — what tipped them over?
- **First use** — what was the first experience?
- **Outcome** — did the product do the job?

The reconstruction surfaces the actual job — including the
circumstance, the forces, and the emotional/social layer — far more
reliably than abstract feature-request interviews.

### 5. Outcomes-Driven Innovation (ODI)

ODI is the quantitative extension of JTBD: for a given job,
identify all the **desired outcomes** customers want from the job,
then rate each outcome on (a) importance and (b) current
satisfaction. Outcomes that are high-importance and low-satisfaction
are **under-served**: the wedge for new product opportunity.
Outcomes that are high-importance and high-satisfaction are
**over-served**: the territory where commoditization happens.

For the Stack SaaS opportunity-scoring:
- High-importance, low-satisfaction outcome → strong opportunity.
- High-importance, high-satisfaction outcome → strong incumbent;
  hard wedge.
- Low-importance, low-satisfaction outcome → not worth solving.
- Low-importance, high-satisfaction outcome → competitor over-built.

The agent uses ODI to score product ideas before any code is
written. Ideas that fail the outcome-importance test get parked.

### 6. The "Hire/Fire" Frame

Customers hire products and fire products. A SaaS subscription that
cancels was "fired" — and the JTBD question is "what did they hire
in its place?" The replacement product is the real competitor — not
the product the team imagines is the competitor.

For Stage Pro: a touring engineer who stops using Stage Pro may have
hired a different specialized tool (real competitor), or may have
hired "QLab + spreadsheet + my own brain" (competitor is the manual
workflow), or may have hired "stop checking, just trust the cues"
(competitor is acceptance of risk).

Each replacement reveals a different job the product was actually
serving. The hire/fire frame surfaces this directly.

### 7. The Progress-Making Lens

JTBD treats every purchase as the customer attempting to make
progress in their life — from a current state to a desired state.
The product is hired when the progress feels achievable and the
status quo feels insufficient.

The progress-making lens is what separates JTBD from feature-list
product thinking: features are means; progress is end. A great
product is the one that makes the most progress possible in the
specific circumstance the customer is in.

## Common Applications

**Pre-spec discovery for a new SaaS idea:**
The agent runs a JTBD interview protocol on 5-7 prospective users.
Each interview reconstructs a specific past purchase decision for an
adjacent product. The output is a job statement, the four forces,
and a list of desired outcomes ranked by importance/satisfaction.
This output gates whether the idea proceeds to spec.

**Stage Pro feature-prioritization audit:**
The agent reads the proposed feature list and asks of each one:
"What job is this hired to do? Whose circumstance creates this job?
What forces push them to hire this feature over what they have now?"
Features that fail to answer get parked. Features that answer
clearly get prioritized by the strength of the answer.

**Stack cohort positioning:**
The agent reads the cohort marketing copy and applies JTBD: "When
[someone in this circumstance] wants to [do this], so they can
[achieve this]." If the copy describes the product (features) more
than the job (progress), it gets rewritten. The wedge surfaces:
"the kind of creator who wants to actually ship AI tools, not just
learn about them."

**Wealth-creation mode product-eval:**
Per locked feedback (60-Minute Product Evaluation Rule), the agent
applies JTBD to score the idea in <60 minutes:
- Can I write the job statement?
- Can I name the four forces?
- Can I name the under-served outcome?
- Can I name what gets fired?

Failure on any of four = park the idea.

**Competitor analysis (hire/fire frame):**
For any product the operator is considering building near, the agent asks:
"What are users firing to hire this competitor? What is the
competitor firing? What job is no one currently doing well?" The
answer is where the wedge lives.

## Anti-patterns (when this framework is misapplied)

**Feature-first product thinking.** "Let's build feature X because
users requested it." JTBD asks: "Which users? What job? What
circumstance? What forces?" Without these answers, the feature is
solving a vague demand from the loudest user — which is rarely the
job the broader customer base is trying to make progress on.

**Confusing demographics with jobs.** "Our user is a 28-35 year old
touring audio engineer with a Mac." This is a persona, not a job.
The same person hires Stage Pro for different jobs at different
moments (pre-show prep vs. tour bus downtime vs. emergency
troubleshooting). The job — not the demographic — drives behavior.

**Naming the functional job only.** A spec that addresses "manage
playback cues" without addressing the emotional job (sleep before
the show) or social job (the reputation of a reliable engineer)
ships a product that gets adopted but not loved — and competitors
who address all three jobs win the loyalty.

**Asking "what would you want?" instead of "tell me about the last
time you bought X."** Speculative feature requests are unreliable.
Past purchase decisions reveal the actual job. Per locked feedback,
"Investigate Before Apologizing for Perceived Bugs" applies here:
investigate the actual purchase event before assuming the customer's
stated preference is the truth.

**Building for the team's idealized user instead of the actual
customer.** the cohort built for "people who want to learn AI"
is too broad. Built for "touring AV technicians whose tour income
is collapsing and who need a creator-economy off-ramp" is specific.
The job-and-circumstance reveals the actual customer.

**Per locked feedback: "Brand to the customer's trade, don't sand
it off."** The customer's trade IS part of the circumstance. Job
statements that ignore the trade context produce generic positioning
that competes on price; job statements that honor the trade context
produce premium positioning that wins on fit.

**Per locked feedback: "Verify Project Status Before Speaking."**
Applied to JTBD: verify the actual job-circumstance before
generating job statements. Don't invent customer language from the
team's heads — capture it from interview data.

## Cross-references

- Agent skill: `agents/product-manager/SKILL.md`
- Bench: `agents/product-manager/personality/_bench.md` (Problem-Truth-Pole, User-Voice-Pole)
- Frameworks index: `agents/product-manager/personality/frameworks_index.md`
- Companion methodology: `agents/product-manager/context/methodology/spec-discipline.md`
- Memory: `.claude/memory/feedback_sixty_minute_rule.md`
- Memory: `.claude/memory/feedback_brand_to_customer_trade.md`
- Memory: `.claude/memory/feedback_no_patches.md`
- Memory: `agents/product-manager/CLAUDE.md`
