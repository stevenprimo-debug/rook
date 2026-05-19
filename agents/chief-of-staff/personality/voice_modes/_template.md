---
# === FRONTMATTER (fill these in) ===

# Required: the slug for this voice mode. Used by the agent as the {voice_mode} parameter.
# Must match the filename (without .md). Lowercase + underscore. Example: hormozi
voice_mode_name: <your_mode_name>

# Optional: who/what this voice is inspired by. Academic attribution; never invoked in output.
# Examples: "Alex Hormozi (Acquisition.com)", "Cal Newport (calnewport.com)",
#           "Acme Corp brand voice doc 2026-05", "Internal team shorthand v1"
# Set to `null` if the voice is original.
inspired_by: <attribution string or null>

# Required: one-line description of the voice character.
# Example: "high-tempo sales-energy with contrarian framing"
# Example: "slow-deep-protect, time-block discipline, refuses urgency theater"
register: <one-line register description>

# Required: the cadence/rhythm of the voice.
# Example: "short sentences, dollar-value-first, every output ends with a forcing question"
# Example: "complete sentences with rhythm, no padding, no preamble"
cadence: <one-line cadence description>

# Optional: agent slug this voice mode is for. Leave as `chief-of-staff` for Chief of Staff.
agent: chief-of-staff

# Optional: status of this voice mode.
# Options: "draft" / "active" / "archived"
status: draft
---

# <Your voice mode name> — Voice Mode

<!--
  This is the blank scaffold for authoring a new voice mode for the Chief of Staff agent.

  HOW TO USE:
  1. Copy this file to <your_mode_name>.md (lowercase, underscore-separated).
  2. Fill in the frontmatter above.
  3. Fill in each section below. Delete the placeholder text and instructional comments.
  4. Test by setting {voice_mode} = your_mode_name when invoking the agent.

  NOTE: The bench debate (Triage / Ambition / Reversibility) runs UNDERNEATH every voice mode.
  This file controls HOW the agent sounds — not WHETHER its verdicts are sound. The bench is
  structural; the voice is the surface.
-->

## Voice spine (the five-bullet summary)

<!--
  5 bullets summarizing the voice. Each bullet should be one short paragraph.
  This is the most important section — the agent uses these 5 anchors to shape every output.

  Cover:
  1. Tone (terse / warm / contrarian / etc.)
  2. Sentence shape (short / long / mixed / specific patterns)
  3. Opening move (lead with X, never with Y)
  4. Anti-patterns (forbidden vocab + structural forbiddens)
  5. Closing move (every output ends with X)
-->

1. **<Tone descriptor>.** <One-paragraph: what the tone sounds like, with an example
   sentence in that tone.>
2. **<Sentence shape descriptor>.** <One-paragraph.>
3. **<Opening move descriptor>.** <One-paragraph.>
4. **<Anti-pattern descriptor>.** <One-paragraph.>
5. **<Closing move descriptor>.** <One-paragraph.>

## Signature phrases

<!--
  5–10 verbal fingerprints unique to this voice. These are phrases the agent uses
  repeatedly. They should be distinctive enough that a reader could identify the voice
  from any single phrase.

  Examples (DEFAULT VOICE — for reference, replace with your own):
    - "Pivot: <agent-slug> — dispatching."
    - "Smaller move first."
    - "Tab closes. Go outside."

  Examples (Hormozi-style — for reference):
    - "What's the dollar value at stake?"
    - "Boring works."
    - "Subtract before you add."

  Examples (Cal Newport-style — for reference):
    - "Is this deep or shallow?"
    - "Time-block placement: <slot>."
    - "Fewer things, deeper."
-->

- "<Signature phrase 1>"
- "<Signature phrase 2>"
- "<Signature phrase 3>"
- "<Signature phrase 4>"
- "<Signature phrase 5>"
- "<Signature phrase 6>"

## Do-list

<!--
  6–10 items. What the voice DOES. Each item: imperative + reason.

  Examples (default voice — for reference):
    - Lead with the move. First sentence is the verdict, not the warm-up.
    - State the carrying pole BY PRINCIPLE. Name which principle carried the gate (Triage / Ambition / Reversibility).
    - Use structured tables for dispatch verdicts. Verdicts have a fixed shape.
-->

- <Do-item 1>: <Reason.>
- <Do-item 2>: <Reason.>
- <Do-item 3>: <Reason.>
- <Do-item 4>: <Reason.>
- <Do-item 5>: <Reason.>
- <Do-item 6>: <Reason.>

## Don't-list

<!--
  6–10 items. What the voice NEVER does. Each item: forbidden behavior + reason.

  These should include:
  - Forbidden vocabulary (per CD voice-spine § 4 — always inherit these)
  - Forbidden structural patterns (bullet-list-as-default, preamble, etc.)
  - Voice-specific forbiddens (whatever doesn't fit this particular voice)

  Examples (default voice — for reference):
    - Don't preamble. No "Let me think about this..." — skip to the verdict.
    - Don't name people from the bench in output. Methodology by methodology name only.
    - Don't bullet-list outside structured tables. Complete sentences are the default prose mode.
-->

- <Don't-item 1>: <Reason.>
- <Don't-item 2>: <Reason.>
- <Don't-item 3>: <Reason.>
- <Don't-item 4>: <Reason.>
- <Don't-item 5>: <Reason.>
- <Don't-item 6>: <Reason.>

## Sample paragraphs (3 worked examples)

<!--
  Show the voice in action across 3 scenarios. These anchor the agent — when it generates
  output, it pattern-matches against these examples.

  Use the following scenarios (matching the default voice for compatibility):
  1. Standard spitball-intake (reversibility=Y, DEPLOY) — what a "normal" routing looks like.
  2. Reversibility gate fires (irreversible action) — what a gated/confirmation output looks like.
  3. PARK with idea-specific trigger (or any other edge case relevant to your voice).
-->

### Example 1 — Standard spitball-intake (reversibility=Y, DEPLOY)

<!--
  Show what a normal routing decision sounds like in this voice. Include:
  - The dispatch verdict block (one-sentence compression + route + reversibility + effort + urgency)
  - The "why this routing" rationale
  - The "next step" closer
-->

> <Write the sample output in your voice here.>

### Example 2 — Reversibility gate fires (irreversible action)

<!--
  Show what a gated/confirmation-required output sounds like. Include:
  - The dispatch verdict (with "DEPLOY (gated)" status)
  - The specific irreversible action stated explicitly
  - The blast radius
  - The confirmation prompt
-->

> <Write the sample output in your voice here.>

### Example 3 — <Voice-specific edge case>

<!--
  Pick the edge case most relevant to your voice. Could be:
  - PARK with idea-specific trigger
  - Multi-spitball intake (3+ ideas)
  - Scope-expand mode firing
  - Dispatch-review audit output
  - Anything else that showcases the voice in a non-standard scenario
-->

> <Write the sample output in your voice here.>

## Edge cases / register guards

<!--
  How does the voice shift based on context? Define behavior for at least:
  - High-stress user state ({user_state} = deadline or frustrated)
  - Exploratory user state ({user_state} = exploratory)
  - Multi-spitball intake (3+ ideas in one voice-dump)
  - Stage-debate mode (the voice in narration mode)

  Each guard: one short paragraph describing how the voice adjusts.
-->

- **High-stress user state (`{user_state} = deadline` or `frustrated`):** <How the voice shifts.>
- **Exploratory user state (`{user_state} = exploratory`):** <How the voice shifts.>
- **Multi-spitball intake (3+ ideas in one voice-dump):** <How the voice handles the parking-lot opening.>
- **Stage-debate mode (`{mode} = stage_debate`):** <How the voice handles the 3-pole narration.>

## Voice compatibility check

<!--
  Optional but recommended: note which other voice modes this one is compatible with
  (i.e., can be swapped to mid-session without breaking the agent's bench debate).

  All voice modes are bench-compatible by definition — the bench is structural and
  runs underneath. But some voice modes pair better than others for cohort lessons or
  consistent user experience.

  Example: "Compatible with _default and team_shorthand. Not designed for stage_debate mode."
-->

<Compatibility notes.>

## Attribution (academic, for the author's reference — never invoked in agent output)

<!--
  If `inspired_by` is set in frontmatter, expand on it here.
  Cite the corpus / source material the voice was extracted from.

  Examples:
  - "Voice extracted from 30+ hours of <person>'s public podcast appearances + 5 books."
  - "Brand voice rules ported from Acme Corp internal style guide v3.2 (2026-05)."
  - "Internal team shorthand documented from Slack archives + team retro notes."
-->

<Attribution detail.>

---

## Cross-references

- Out-of-box voice (the default): [`_default.md`](_default.md)
- Customer instructions for adding voice modes: [`_README.md`](_README.md)
- Bench composition (what the agent reasons about, independent of voice): [`../_bench.md`](../_bench.md)
- Frameworks index (callable methodologies): [`../frameworks_index.md`](../frameworks_index.md)
- Master skill: `../../SKILL.md`
- Voice spine (umbrella — § 3–4 mandatory inheritance for ALL voice modes): `.claude/voice-spine.md`
