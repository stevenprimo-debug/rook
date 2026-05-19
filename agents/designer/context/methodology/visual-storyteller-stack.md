# Visual Storyteller Stack

## What This Framework Is

The Visual Storyteller Stack is a 4-pack methodology that combines
visual story brain, design composition critique, motion craft, and
anti-slop taste enforcement into a single operating discipline for
any visual surface. The stack treats visual design as a storytelling
medium first and a styling exercise second — every element on screen
either serves the narrative the surface is telling, or it gets
cut.

The four components:

1. **Visual story brain** — frames the surface as a story: who is
   the reader, what state are they in when they arrive, what state
   should they be in when they leave, what visual sequence carries
   them from one to the other.

2. **Design composition critique** — applies the four core
   composition principles (color, typography, spatial hierarchy,
   visual rhythm) to every element, with explicit pass/fail criteria.

3. **Motion craft** — treats animation as functional storytelling:
   motion either reveals information, signals state change, or
   guides attention. Decorative motion that does none of these is
   cut.

4. **Anti-slop taste enforcement** — the discipline of recognizing
   and refusing AI-default visual patterns: stock-photo gradients,
   meaningless geometric flourishes, generic icon sets,
   over-rounded "friendly" UI, every-element-has-a-shadow noise.

The stack assumes the designer is operating with restraint, not
abundance. Visual storytellers do less, not more — but every element
that stays earns its place by carrying narrative weight.

## Why It Matters For This Agent

Designer's bench gates on three principles: Story-Service-Pole,
Restraint-Pole, and Craft-Pole. The Visual Storyteller Stack is
the operating implementation of all three.

- **Story-Service-Pole** asks: "Does every element serve the story
  this surface is telling?" The stack's visual-story-brain component
  is the gate.

- **Restraint-Pole** asks: "Is this design doing less by adding
  more, or doing more by subtracting?" The stack's composition
  critique and anti-slop enforcement components are the gate.

- **Craft-Pole** asks: "Is the typography, spacing, motion, and
  detail at production quality, or is it AI-default?" The stack's
  composition and anti-slop components are the gate.

For the operator's commercial surfaces — [your employer] proposal covers, the Stack
cohort landing pages, Ableton product pages, Stage Pro feature
announcements, social-media assets — the stack is the standard.
Surfaces that ship without stack discipline produce AI-slop output
that the audience reads as low-effort.

## Core Concepts

### 1. The Visual Story Brain

Every surface tells a story. The story has a reader, a starting
state, a desired ending state, and a sequence of visual moves
that connect them. The designer's first job is to write the
story before placing any element on the canvas.

Three questions:
- **Who arrives at this surface?** (Touring AV engineer prepping
  a show? CFO evaluating an integration platform? Touring DJ
  considering a new playback tool?)
- **What state are they in?** (Skeptical, hurried, evaluating
  three competitors, looking for a reason to leave.)
- **What state should they be in when they leave?** (Convinced
  enough to reply to the email, book the call, download the demo.)

The visual sequence is the path between starting state and ending
state. Hero element answers "is this for me" in <2 seconds. Second
zone builds the case. Third zone delivers proof. Fourth zone offers
the action.

When the story is written first, every visual element either
advances the sequence or gets cut.

### 2. Composition Principles — Color

Color carries emotional weight, hierarchy, and brand identification.
The discipline: every color on the surface comes from the brand
system, not from the designer's preference. Brand color systems
typically have 3-5 anchor colors plus a small set of functional
colors (alert, success, warn, info).

Specific rules:
- **No off-system colors.** If the design needs a color the
  system doesn't provide, the system gets extended (with brand
  approval), not extended ad-hoc.
- **Contrast must pass accessibility.** WCAG AA minimum on body
  text (4.5:1), AAA preferred on critical CTAs (7:1).
- **Color hierarchy matches information hierarchy.** The most
  important element gets the highest-contrast, most brand-loaded
  color treatment. Secondary elements step down predictably.

### 3. Composition Principles — Typography

Typography is the carrier of voice. The discipline: every typeface
on the surface is intentional, with explicit role assignment
(display, body, eyebrow, supporting).

Specific rules:
- **2-3 typefaces maximum.** A display face, a body face, and
  optionally a monospaced face for code/data. More than three
  introduces visual noise.
- **Type scale follows a system.** Don't use 14px, 15px, 16px,
  17px — use 14, 16, 20, 28, 40 (modular scale). Predictable
  steps produce visual rhythm.
- **No mono in proposals.** Per locked feedback: "Mono fonts read
  as code-text — never in proposals, decks, or client marketing
  materials."
- **Line length is 50-75 characters for body text.** Beyond 75,
  the reader's eye loses the next line. Below 50, the rhythm
  breaks.
- **Letterspacing matches the typeface.** Display faces often
  need tightened tracking; small body sizes often need slight
  opening.

### 4. Composition Principles — Spatial Hierarchy

Space is a design tool. Empty space is not wasted — it is the
gravity that pulls the reader's eye to the elements that matter.

Specific rules:
- **8-point grid.** All spacing is a multiple of 8 (or 4 for fine
  adjustments). 8, 16, 24, 32, 48, 64, 96. Predictable spacing
  produces visual rhythm.
- **Generous margins.** Cramped margins read as low-effort.
  Generous margins read as confident.
- **One focal point per zone.** Every screen-zone (hero, content,
  proof, action) has one element that gets the eye first. Two
  competing focal points produce visual noise.
- **No element fights the grid.** Every element snaps to the
  spacing system. The eye reads grid-aligned compositions as
  "trustworthy"; misaligned compositions read as "rushed."

### 5. Composition Principles — Visual Rhythm

Rhythm is the cadence of the design — the predictable beat that
makes the surface feel orchestrated rather than assembled.

Specific rules:
- **Spacing rhythm**: section-to-section spacing follows a system
  (e.g., 96px between major zones, 48px within zones, 24px between
  cards).
- **Type rhythm**: heading-to-body spacing is consistent across the
  surface (e.g., 24px between H2 and following body).
- **Element rhythm**: card grids use consistent card dimensions;
  buttons use consistent height; icons use consistent size.
- **No breaks in rhythm without intentional reason.** A larger
  card in a row of standard cards must be doing emphasis work —
  not "we had a bigger image to fit."

### 6. Motion as Functional Storytelling

Motion answers three functional questions:

- **What just changed?** (State transition: form submitted, modal
  opened, item added to cart.)
- **Where am I now?** (Navigation transition: page change, drawer
  open, drilldown.)
- **Where should I look next?** (Attention guide: highlight on hover,
  focus on field, pulse on CTA.)

Motion that doesn't answer one of these three is decoration. The
stack cuts decoration ruthlessly. Decorative motion adds
performance cost and slows the user — for no narrative gain.

Specific rules:
- **Animation duration**: 150-300ms for micro-interactions, 300-500ms
  for transitions, never longer for functional motion.
- **Easing**: ease-out for "arrival" animations (something
  appearing), ease-in for "departure" (something leaving),
  ease-in-out for "transition" (something changing position).
- **Respect prefers-reduced-motion.** Users with motion sensitivity
  get static states.
- **No infinite loops.** Looping animations are distraction
  generators.

### 7. Anti-Slop Taste Enforcement

The anti-slop component recognizes and refuses AI-default visual
patterns. Common slop signatures:

- **Stock-photo gradient overlays** on every hero image.
- **Geometric flourishes** (orbital lines, particle dots) that
  don't carry narrative weight.
- **Generic icon sets** (every concept gets a Heroicons match
  whether it fits or not).
- **Over-rounded UI** (every corner radius is 12-16px because
  "rounded = friendly").
- **Shadow noise** (every element has a subtle shadow, producing
  visual chatter).
- **AI-generated illustrations** that all look the same: vaguely
  pastel, vaguely abstract, vaguely "tech."
- **Centered everything** when left-aligned would be stronger.
- **Three-column feature grids** that pad the surface but don't
  advance the story.

The discipline: every element gets the "does this serve the story
or is it AI-default?" audit. AI-default gets cut.

## Common Applications

**[your employer] proposal cover design:**
The story: a enterprise facilities VP arrives at the cover, has
30 seconds to decide whether this proposal merits their attention.
Visual story → hero element answers "this is for your specific
facility" in <2 seconds (named building, named space). Type
hierarchy puts the proposal value-stake at second-glance position.
Brand color carries the [your employer] identity. No mono. Per [example enterprise customer] v4
template. Per locked feedback.

**the cohort landing hero:**
The story: a touring AV pro arrives skeptical that AI cohorts are
worth the money. Visual story → hero copy names their specific
circumstance (industry shift, gig changes). Hero visual is
specific to the practitioner, not generic. Below-fold builds proof:
named alumni, named outcomes, named community. Single action.
Brand restraint, no AI-illustration defaults.

**Stage Pro product page:**
The story: a touring engineer arrives wanting to know if Stage Pro
solves their specific cue-management problem. Visual story → hero
shows the actual product UI in the actual use scenario (pre-show
prep). Feature zones each name a specific cue-management job, not
generic "powerful." Motion: form interaction confirms, transition
between sections is functional, no decorative loops.

**Social-media asset design:**
The story: scroll-stopper for a 1.5-second eyeball. Hero visual +
single line of copy + brand signature. No clutter, no chrome, no
decorative geometric overlay. The reader either stops or scrolls
in <2 seconds — design for that decision.

**Pre-design competitive audit:**
Per locked feedback: "Always Research Design Trends Before
Designing." Before generating, the agent reviews Dribbble + 2026
trends + the operator's reference shots for the specific audience, then
generates with awareness of what the audience expects to see.

## Anti-patterns (when this framework is misapplied)

**Style applied without story.** A polished visual that doesn't
serve a specific reader's specific path through the surface.
Beautiful AND useless. The Story-Service-Pole gate refuses.

**"Make it pop."** Vague directives produce vague execution. The
discipline demands specific direction: which element should
emphasize, why, what visual move (size, color, weight, motion)
carries the emphasis.

**Per locked feedback: "AI slop" patterns.** Generic three-column
feature grids, every-card-has-a-shadow, AI-pastel illustrations,
over-rounded corners. The agent recognizes these and cuts them.

**Per locked feedback: "No Mono Fonts in Client Proposals."** Mono
typefaces read as code-text — never on commercial surfaces.

**Per locked feedback: "Avoid Text Wrapping at All Costs."** KPI
cards, labels, badges, buttons that wrap on standard widths.
Shorten or restructure.

**Per locked feedback: "Clean Contemporary Design Standard."**
Cards not stacks, 3 items = 3 cols, no wrap, brand palette only,
no AI-slop. The standard is the gate.

**Per locked feedback: "Brand to the customer's trade."** The
visual language of the surface respects the customer's trade. [your employer]
proposals for industrial clients lean into industrial materiality;
the cohort visuals lean into the practitioner aesthetic of
the audience.

**Motion for motion's sake.** Animation that doesn't answer "what
just changed, where am I now, where should I look next" is
decorative. Cut.

**Decoration disguised as design.** Floating geometric shapes,
particle backgrounds, orbital lines — the AI-default flourishes
that mark "tech aesthetic" without doing narrative work. Cut.

## Cross-references

- Agent skill: `agents/designer/SKILL.md`
- Bench: `agents/designer/personality/_bench.md` (Story-Service-Pole, Restraint-Pole, Craft-Pole)
- Frameworks index: `agents/designer/personality/frameworks_index.md`
- Vendored reference: `agents/designer/context/references/50-modern-fonts.md`
- Companion methodology: `agents/designer/context/methodology/restraint-as-discipline.md`
- Memory: `.claude/memory/feedback_design_quality_standard.md`
- Memory: `.claude/memory/feedback_no_mono_in_proposals.md`
- Memory: `.claude/memory/feedback_no_text_wrap.md`
- Memory: `.claude/memory/feedback_brand_to_customer_trade.md`
- Memory: `.claude/memory/feedback_research_before_design.md`
- Memory: `agents/designer/memory/visual_storyteller_stack.md`
- Voice spine: `.claude/voice-spine.md`
