# Synthesis with Confidence Gaps

## What This Framework Is

Synthesis with confidence gaps is the discipline of producing
research outputs that are honest about both what is known and
what remains uncertain. The framework holds that **a research
brief that surfaces its own gaps is more useful than one that
papers over them**, because the operator who reads the brief
needs to know where to dig further, where to act with caution,
and where the evidence is solid enough to commit.

Most research outputs fail in two opposite ways:

1. **Over-confident synthesis** — the brief presents a clean
   narrative that hides the evidence's actual messiness. The
   operator commits based on the narrative; later discovers the
   evidence didn't actually support it.

2. **Under-confident hedging** — the brief is so full of
   qualifications, caveats, and "it depends" that the operator
   gets no usable signal. The brief produces no action.

The framework operates between these extremes: state the
conclusions clearly, name the confidence level for each, and
explicitly surface the gaps that would raise or lower confidence.

Confidence levels operate on a discrete scale, not a continuous
percentage. Three named levels:

- **High confidence** — multiple independent high-tier sources
  agree; the conclusion is locked unless contrary high-tier
  evidence surfaces.
- **Medium confidence** — evidence is suggestive but not
  conclusive; the conclusion is a working hypothesis;
  decision-relevant for low-stakes actions, requires more
  evidence for high-stakes commitment.
- **Low confidence** — preliminary signal; surface for the
  operator's awareness; flag the specific evidence that would
  upgrade confidence.

## Why It Matters For This Agent

Deep-Researcher's Synthesis-Honesty-Pole and Confidence-Gap-Pole
both require this framework.

- **Synthesis-Honesty-Pole** asks: "Did the synthesis represent
  the evidence honestly, including the gaps?" The framework's
  confidence-tier discipline is the gate.

- **Confidence-Gap-Pole** asks: "Are the unknowns named, and is
  it clear what evidence would close them?" The framework's
  explicit-gap surfacing is the gate.

For the operator's research surfaces, honest synthesis prevents the
expensive failure mode: committing to a decision based on a
research brief whose conclusions sounded firmer than the
evidence actually supported. Pre-meeting briefs, market-research
syntheses, competitive analyses, and trademark/name reviews all
require this discipline — the operator acts on these briefs, and
silent over-confidence converts to bad decisions.

## Core Concepts

### 1. The Confidence-Tier Discipline

Every conclusion in a research output is tagged with a confidence
level (high / medium / low). The tagging is explicit, not
implicit. The reader can see at a glance which conclusions are
solid and which are working hypotheses.

Tagging convention:

```
Conclusion: The [your customer market] is shifting toward AI-augmented
workflows over the 2026-2028 horizon.
Confidence: Medium.
Evidence base: Two industry trade-press analyses (Tier 3), three
named-practitioner blog posts (Tier 4), industry survey from a
trade association (Tier 4, n=312).
Gaps: No academic labor-economics research specifically on [your customer industry]
yet; no longitudinal data tracking the shift over the past 24 months;
no compensation data confirming the wage compression hypothesis.
What would raise confidence: Tier 2 academic research on
creative-industry technology shifts; longitudinal survey data over 24+
months; compensation data from named [your customer projects].
```

The tag is the contract. The operator reading the brief sees
exactly how much weight to put on the conclusion.

### 2. Independent Triangulation

High-confidence conclusions require independent triangulation:
multiple sources, with distinct origin chains, agreeing on the
claim.

"Independent" matters. Three articles all citing the same
original survey are not three independent sources — they are one
source plus two retransmissions. The agent traces the origin
chains and assesses independence before assigning confidence.

When triangulation is absent, confidence drops to medium or low
even if multiple sources agree.

### 3. The Gap-Surfacing Discipline

Every conclusion is paired with an explicit gap statement: what
specific evidence would raise or lower confidence?

Gaps are concrete:
- "No academic research specifically on this question."
- "No longitudinal data — current evidence is point-in-time."
- "No data on the segment we care most about (e.g., [your customer industry])."
- "Source diversity is low — most evidence traces to one
  industry analyst firm."
- "Recency gap — most data is 18+ months old in a fast-moving
  category."
- "Adversarial evidence is absent — the brief found only
  supporting evidence, suggesting either consensus or selection
  bias in the search."

Concrete gaps give the operator (or the researcher in a follow-up
session) a clear next step. Vague gaps ("more research needed")
fail this test.

### 4. The Adversarial Search

Every synthesis includes an adversarial search: what would
falsify the conclusion? The researcher actively looks for
contrary evidence, not just confirming evidence.

If the adversarial search finds nothing, confidence rises (the
conclusion survived a real attempt to break it). If the
adversarial search finds something, that something is surfaced
in the brief — even if the something doesn't fully overturn the
conclusion.

Common adversarial patterns:
- Search for the opposite claim explicitly.
- Look for cases where the conclusion would predict X but X
  didn't happen.
- Surface counter-examples named by domain practitioners.
- Check whether respected dissenters exist.

### 5. The Decision-Relevance Filter

Not all gaps matter equally. Some gaps would change the
operator's decision; others wouldn't. The framework distinguishes:

- **Decision-relevant gaps** — closing this gap would change
  the recommended action.
- **Background gaps** — closing this gap would refine
  understanding but not change the action.

Decision-relevant gaps get priority surfacing. Background gaps
are noted but don't drive the brief's structure.

Example:
- Conclusion: Stack cohort positioning should target touring
  AV pros transitioning to creator-economy work.
- Decision-relevant gap: Cohort price elasticity in this segment
  (would the segment pay $2K vs. $5K?). Closing this gap changes
  the pricing strategy.
- Background gap: Geographic distribution of the segment.
  Closing this gap refines marketing channel selection but
  doesn't change the cohort design.

### 6. The "What I Found vs. What I Looked For" Frame

The brief is honest about both what was found and what was
searched for. This prevents the silent-omission failure mode:
the researcher didn't find evidence on X but didn't say "I
didn't find evidence on X" — leaving the operator to assume X
wasn't relevant or wasn't checked.

Standard format:

```
Searched for: <named questions, named sources, named methods>
Found: <evidence summary>
Did not find: <questions that remained unanswered after the search>
Did not search for: <questions that were out of scope but might
be relevant>
```

The frame is the discipline. It prevents the brief from sounding
more comprehensive than it actually is.

### 7. The Confidence-Update Mechanism

Research is iterative. New evidence updates confidence. The
brief is a snapshot; the next iteration may move conclusions to
different confidence tiers.

The update mechanism:
- New high-tier evidence agreeing with the conclusion → confidence
  rises.
- New high-tier evidence disagreeing → confidence falls or
  conclusion is revised.
- New gaps surfaced → confidence may fall pending closure.
- Time passing without new evidence → confidence may fall for
  fast-moving categories, stay stable for evergreen ones.

Per the compounding-append pattern, confidence updates are
appended with timestamps, not silent rewrites. The history of how
confidence evolved is part of the record.

## Common Applications

**Pre-meeting client brief:**
The agent researches the client and produces a tier-tagged brief.
"Client is investing $X in capex this fiscal year (Tier 1: SEC
filing, high confidence). They are evaluating multiple AV
integrators (Tier 3: trade press, medium confidence). They have a
new facilities VP who prefers premium integrators per LinkedIn
signals (Tier 6: medium-low confidence — verify in conversation)."
the operator reads and knows which claims to trust without verifying and
which to verify in the meeting.

**Market-research synthesis for cohort positioning:**
The agent surveys the [your customer industry] market shift narrative. Produces
a synthesis with confidence tags. "The shift is real and accelerating
(High confidence: multiple Tier 3-4 sources, independent
triangulation). The timing window is 18-24 months (Medium
confidence: industry-analyst predictions, no longitudinal data).
Compensation pressure on traditional roles is severe (Low
confidence: anecdotal evidence only, no compensation surveys
specific to [your customer industry])." Cohort positioning rests on
high-confidence claims; messaging tone calibrated to medium-confidence
timing; compensation framing avoids the low-confidence claim.

**Trademark / name-collision review:**
Per locked feedback, the agent runs USPTO checks (Tier 1) and
domain availability (Tier 1). Produces a brief: "Name X is
available in trademark classes Y and Z (High confidence: USPTO
search returned clean). Domain is available (High confidence:
WHOIS clean). Real watchout is SEO collision: existing brand at
named.com has medium SEO authority in adjacent category (Medium
confidence: estimated from third-party SEO tools)." the operator decides
based on high-confidence trademark/domain claims while weighing the
medium-confidence SEO consideration.

**Competitive intelligence on AI-tooling category:**
Adversarial search included: "Is this category overheated?" Brief
finds: "Multiple well-funded startups in category (Tier 3, high
confidence). Limited evidence of customer retention or
profitability (Tier 4, medium confidence). Adversarial search
surfaced: at least two named experts predict consolidation by
2027 (Tier 4, low-medium confidence)." the operator decides on entry
with explicit awareness of the category-overheat hypothesis.

**Pre-[your product] content publication review:**
Before publishing content that makes claims about AV industry
trends, the agent runs the confidence audit. Claims labeled
high-confidence pass. Claims labeled medium need explicit hedging
in the content ("based on industry surveys" rather than "the
industry has shifted"). Claims labeled low get pulled or
reframed as observations.

## Anti-patterns (when this framework is misapplied)

**Confidence-tagging that doesn't reflect actual evidence
strength.** Tags that are applied for form but don't change the
synthesis. The discipline requires that high-confidence
conclusions are actually defensible at high-confidence; lowering
the tag is the honest move when evidence is weaker.

**Hedge spam.** Tagging everything "medium confidence" because
honest assessment requires high-confidence threshold and the
researcher didn't do the triangulation. Hedge spam looks careful
but produces no usable signal.

**Buried gaps.** Listing gaps in a footnote section the operator
skips. The framework requires gaps surfaced near the
corresponding conclusions, with explicit decision-relevance
weighting.

**Missing adversarial search.** A synthesis that only finds
confirming evidence is suspicious. The researcher must
deliberately look for disconfirming evidence and report what
was found (or that nothing was found and why that's noteworthy).

**Per locked feedback: "Verify Project Status Before Speaking."**
Applied to synthesis: confidence assessment requires verifying
the underlying source state, not assuming stale sources are
current.

**Per locked feedback: "Investigate Before Apologizing for
Perceived Bugs."** Applied to research: if the operator pushes
back on a conclusion, the researcher investigates the actual
disagreement before retreating; the operator may be right, or
the operator may be working from a different evidence base, or
the operator may be wrong — all three require different
responses.

**Conclusions disguised as observations.** Hedging language
("some observers note that...") that produces conclusion-shaped
content without the confidence-tagging discipline. The framework
requires explicit tags; hedging-language without tags is
under-confident dressed as nuance.

**Per locked feedback: "Filter — Personal-Tool Patterns vs
Agent-Team Patterns."** Research outputs read by multiple
agents must use the team-compatible synthesis frame. Single-user
research can be sloppier; team research compounds errors when
confidence isn't explicit.

**Per locked feedback: "Match Execution Mode."** Even in
fast-execution mode, the confidence tagging is required. The
form may be compressed (one-line tags rather than full gap
analysis), but the discipline holds.

## Cross-references

- Agent skill: `agents/deep-researcher/SKILL.md`
- Bench: `agents/deep-researcher/personality/_bench.md` (Synthesis-Honesty-Pole, Confidence-Gap-Pole)
- Frameworks index: `agents/deep-researcher/personality/frameworks_index.md`
- Companion methodology: `agents/deep-researcher/context/methodology/source-credibility-hierarchy.md`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `.claude/memory/feedback_investigate_before_apologizing.md`
- Memory: `.claude/memory/feedback_check_trademark_fundamentals.md`
- Memory: `.claude/memory/feedback_match_execution_mode.md`
- Memory: `agents/deep-researcher/CLAUDE.md`
