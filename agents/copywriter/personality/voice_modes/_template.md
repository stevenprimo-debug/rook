---
voice_mode_name: <your_mode_name>
inspired_by: <attribution string or null>
register: <one-line register description>
cadence: <one-line cadence description>
agent: copywriter
status: draft
---

# <Your voice mode name> — Voice Mode

<!--
  Blank scaffold for authoring a new voice mode for Copywriter.

  HOW TO USE:
  1. Copy this file to <your_mode_name>.md (lowercase, underscore-separated).
  2. Fill in the frontmatter above.
  3. Fill in each section below. Delete the placeholder text.
  4. Test by setting {voice_mode} = your_mode_name when invoking the agent.

  The bench debate (Clarity / Wit / Utility) runs UNDERNEATH every voice mode.
  This file controls HOW the agent sounds — not WHETHER its verdicts are sound.
-->

## Voice spine (the five-bullet summary)

1. **<Tone descriptor>.** <One paragraph.>
2. **<Sentence shape descriptor>.** <One paragraph.>
3. **<Opening move descriptor>.** <One paragraph.>
4. **<Anti-pattern descriptor>.** <One paragraph.>
5. **<Closing move descriptor>.** <One paragraph.>

## Signature phrases

- "<Signature phrase 1>"
- "<Signature phrase 2>"
- "<Signature phrase 3>"
- "<Signature phrase 4>"
- "<Signature phrase 5>"

## Do-list

- <Do-item 1>: <Reason.>
- <Do-item 2>: <Reason.>
- <Do-item 3>: <Reason.>
- <Do-item 4>: <Reason.>
- <Do-item 5>: <Reason.>
- <Do-item 6>: <Reason.>

## Don't-list

- <Don't-item 1>: <Reason.>
- <Don't-item 2>: <Reason.>
- <Don't-item 3>: <Reason.>
- <Don't-item 4>: <Reason.>
- <Don't-item 5>: <Reason.>
- <Don't-item 6>: <Reason.>

## Sample paragraphs (3 worked examples)

### Example 1 — Standard workflow

> <Write the sample output in your voice here.>

### Example 2 — Gated/confirmation scenario

> <Write the sample output in your voice here.>

### Example 3 — <Voice-specific edge case>

> <Write the sample output in your voice here.>

## Edge cases / register guards

- **High-stress user state (`{user_state} = deadline` or `frustrated`):** <How the voice shifts.>
- **Exploratory user state (`{user_state} = exploratory`):** <How the voice shifts.>
- **Multi-artifact intake:** <How the voice handles batched work.>
- **Stage-debate mode (`{mode} = stage_debate`):** <How the voice handles 3-pole narration.>

## Voice compatibility check

<Compatibility notes.>

## Attribution (academic — never invoked in agent output)

<Attribution detail.>

---

## Cross-references

- Out-of-box voice: [`_default.md`](_default.md)
- Customer instructions: [`_README.md`](_README.md)
- Bench composition: [`../_bench.md`](../_bench.md)
- Frameworks index: [`../frameworks_index.md`](../frameworks_index.md)
- Master skill: `../../SKILL.md`
- Voice spine: `.claude/voice-spine.md`
