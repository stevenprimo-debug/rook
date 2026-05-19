---
date: 2026-05-14
type: frameworks-attribution
agent: Chief of Staff
status: v2 (academic credit — reference only; never invoked in agent output)
template_version: "2.0.0"
---

# Chief of Staff — Frameworks Attribution

Academic credit for the methodologies the agent invokes from
[`frameworks_index.md`](frameworks_index.md). This file is **reference only**. The
agent **does not name these people in output**. The principle is invoked by its
methodology name; the originator is credited here for due diligence and IP hygiene.

**Why this separation exists:**

1. **The principle is universal.** Every methodology in `frameworks_index.md` has been
   independently rediscovered or expressed by many practitioners. Naming one originator
   risks treating their version as canonical when the principle itself predates them.
2. **The agent ages better when it speaks in principles.** Figures rise and fall in
   cultural relevance; principles don't. An agent that quotes "Bezos" dates itself the
   moment that figure shifts; an agent that invokes "the one-way-vs-two-way-door
   framing" stays current.
3. **IP / likeness hygiene.** Naming a living figure as the agent's bench raises
   questions of licensing, defamation, and likeness-rights when the agent ships
   externally. Crediting the methodology in a reference file is academic norm; naming
   the figure in agent output is a different category of claim.
4. **Customers shouldn't have to admire the bench to use the agent.** If the bench is
   named by figures, the customer either admires them (and adopts the agent) or
   doesn't (and rejects it). Principles are admiration-neutral.

---

## Triage-Pole methodologies

### `one_sentence_compression` / `smallest_viable_move`

**Origin lineage:**
- **Tobi Lütke** (Shopify CEO) — "innovation is much more blue-collar than people
  think" / boring-incrementalism / first-principles-decompose framing. Public via
  Shopify internal handbook + interviews.
- **Cal Newport** (Computer Science professor, author of *Deep Work* and *Slow
  Productivity*) — "do fewer things, work at natural pace, obsess over quality" / the
  Slow Productivity principles. Public via books + Cal's blog (calnewport.com).
- **Pete Drucker** (management theorist, *The Effective Executive*) — "doing the right
  things vs doing things right" / the time-log discipline / the contribution
  question. Public via *The Effective Executive*, *Management: Tasks, Responsibilities,
  Practices*.

**Why these credits, not others:** these three are the most-cited originators of the
"ship the smallest viable move" doctrine in operations literature. Other lineages
(Lean Startup, Toyota Production System, Agile Manifesto) reach the same principle
through different framings.

### `dispatch_classify`

**Origin lineage:**
- **Chief-of-staff role in executive operations** (no single originator — embedded in
  McKinsey, BCG, Bain, and high-velocity startup operations playbooks for ~40 years).
- **Pete Drucker** — "what is our business?" / mission-drift filter as the classifier
  upstream of any tactical work.

---

## Ambition-Pole methodologies

### `scope_expand_check` / `phantom_constraint_audit`

**Origin lineage:**
- **Sam Altman** (OpenAI CEO, Y Combinator) — "think bigger" / the YC office-hours
  forcing-question pattern. Public via YC essays + Altman blog (samaltman.com).
- **Marc Andreessen** — "software is eating the world" framing / the
  bigger-defensible-scope argument. Public via Andreessen Horowitz essays.
- **Patrick Collison** (Stripe CEO) — "fast" / the questions-list framing for
  expanding the frame ("Why have we not been more ambitious?"). Public via Collison
  blog + interviews.
- **Charlie Munger** (Berkshire Hathaway) — "invert, always invert" / the lattice of
  mental models for surfacing what hasn't been considered. Public via *Poor
  Charlie's Almanack*.

### `compounding_check`

**Origin lineage:**
- **Naval Ravikant** — the leverage-classification framework (Labor / Capital / Code /
  Media); compounding leverage as the central thesis. Public via "How to Get Rich"
  Twitter thread (2018) + Almanack + Naval's podcast.
- **Tobi Lütke** — "does this compound?" as a routine engineering filter.
- **Warren Buffett / Charlie Munger** — compounding-as-core-discipline from value
  investing literature.

---

## Reversibility-Pole methodologies

### `reversibility_gate` / `confirmation_prompt`

**Origin lineage:**
- **Jeff Bezos** — the one-way-door-vs-two-way-door framing for irreversible
  decisions. Public via 1997 Amazon shareholder letter + subsequent letters.
- **Andy Grove** (former Intel CEO, *Only the Paranoid Survive*) — strategic
  inflection point framing; the cost-of-being-wrong calculus.
- **Daniel Kahneman** — System 1 / System 2 framing for when slow-deliberate
  decision-making is warranted (high-stakes, irreversible). Public via *Thinking,
  Fast and Slow*.

### `dispatch_chain_lookup`

**Origin lineage:**
- **Frederick Brooks** (*The Mythical Man-Month*) — "no silver bullet" / the
  conceptual-integrity-by-architect doctrine that downstream work fails without
  upstream design.
- **David Marquet** (*Turn the Ship Around*) — intent-based leadership / "I intend
  to..." / the chain-of-clarification pattern that prevents downstream agents from
  executing without upstream sign-off.
- **Internal vault learning** — the DESIGN slop pattern (2026-05-07) when CD was
  skipped. The chain enforcement is encoded behavior, not borrowed framing.

### `monday_anchor_anti_pattern_check`

**Origin lineage:**
- **Internal vault learning** — voice spine locked per
  `feedback_dont_default_park_to_monday.md`. Not borrowed; codified from a specific
  failure pattern (defaulting PARK triggers to the Monday Anchor turned PARK into a
  someday-punt).
- **James Clear** (*Atomic Habits*) — habit-stack triggers must be specific and
  proximate; generic triggers fail to fire. The methodology generalizes Clear's
  habit-stack rule into a PARK-trigger rule.

---

## Cross-pole synthesis methodologies

### `route_decision`

**Origin lineage:**
- **The chief-of-staff role itself** — synthesis-by-triage is the central function;
  no single originator.
- **The OODA loop** (John Boyd) — Observe-Orient-Decide-Act as the canonical fast-
  synthesis framing.

---

## Bench composition (the principles, not the figures)

The three poles — Triage / Ambition / Reversibility — are named by their **principle**,
not by the figures listed above. The bench composition was selected for v2 because:

1. It covers the three most common failure modes Chief of Staff catches: gold-plating,
   under-asking, and silent one-way-door execution.
2. The poles are genuinely orthogonal — they don't collapse into one another, so the
   debate is real, not theater.
3. The synthesis rule (only expand if reversible) is operationally clean and produces
   actionable verdicts every time.
4. The principles age well — they don't depend on any single figure's cultural
   relevance.

The figures credited above are the most-cited originators of each methodology in the
relevant literature. They are not the only ones who could be credited. If a future
contributor finds a more accurate originator, this file is the place to update —
**not** the master SKILL.md.

---

## Cross-references

- Bench composition (principle-named): [`_bench.md`](_bench.md)
- Frameworks index (callable methodologies): [`frameworks_index.md`](frameworks_index.md)
- Master skill (modes that invoke these methodologies): `../SKILL.md`
- Voice spine (why principles, not people — see CD voice-spine § 4 on
  forbidden-vocab and § 7 on voice-dominance): `.claude/voice-spine.md`
