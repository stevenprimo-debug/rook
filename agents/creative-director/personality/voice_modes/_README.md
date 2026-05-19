---
title: Voice Modes — Customer-Extensible Voice Library
agent: creative-director
status: shipped — customer-facing instructions
audience: customers / cohort students / Stack operators
---

# Voice Modes — How to make this agent speak like you (or like your favorite operator)

This directory is the **customization layer** of the agent.

The bench-of-three principles (Provocation / Restraint / Coherence) defines WHAT this
agent reasons about. **Voice modes define HOW it sounds while doing it.**

Every other agent platform ships ONE voice. The Stack ships 20 agents × N voice modes
per agent. The customization is yours.

---

## What ships in the box

| File | Purpose |
|---|---|
| `_default.md` | The out-of-box Creative Director voice — terse tastemaker; refuses safe vocabulary; closes on the gate. Active when `{voice_mode}` is unset or set to `_default`. |
| `_README.md` | This file. Customer-facing instructions for adding voice modes. |
| `_template.md` | Blank scaffold you copy + fill to author a new voice mode. |

---

## What voice modes ARE

A voice mode is a `.md` file in this directory that defines:

- **Signature phrases** — the verbal fingerprints the agent uses repeatedly.
- **Do-list** — what the voice does.
- **Don't-list** — what the voice never does (always inherits forbidden vocabulary from CD voice-spine § 4).
- **Sample paragraphs** — 3 worked examples showing the voice in action across different scenarios.
- **Edge cases / register guards** — how the voice shifts based on user state, mode, or context.

The agent loads the active voice mode at session start via the `{voice_mode}`
parameter. Whatever file you point to becomes the agent's voice spine for the
session. The bench debate (Provocation / Restraint / Coherence) runs underneath every
voice mode — what changes is the surface, not the discipline.

---

## How to add a new voice mode

Three steps.

### Step 1 — Copy the template

```bash
cp personality/voice_modes/_template.md personality/voice_modes/<your_mode_name>.md
```

Naming convention: lowercase, underscore-separated. Examples: `paula_scher.md`,
`tibor_kalman.md`, `acme_corp_brand.md`, `team_shorthand.md`.

### Step 2 — Fill in the template

The template has frontmatter + 7 sections. Fill each:

1. **Frontmatter** — `voice_mode_name`, `inspired_by` (optional attribution), `register`, `cadence`.
2. **Voice spine** — 5 bullets summarizing the voice.
3. **Signature phrases** — 5–10 verbal fingerprints unique to this voice.
4. **Do-list** — what the voice does. 6–10 items.
5. **Don't-list** — what the voice never does. 6–10 items.
6. **Sample paragraphs** — 3 worked examples covering common scenarios (creative brief, reductive critique, edge case).
7. **Edge cases / register guards** — how the voice shifts based on context.

### Step 3 — Activate the mode

When invoking Creative Director, set the `{voice_mode}` parameter:

```
{voice_mode} = your_mode_name
```

The agent loads `personality/voice_modes/your_mode_name.md` and uses it as its voice
spine for the session.

---

## Default behavior

If `{voice_mode}` is unset, OR the requested file doesn't exist, the agent falls back
to `_default.md` and surfaces a note:

> *"Voice mode `<X>` not found — using default. Add
> `personality/voice_modes/<X>.md` to enable this mode."*

This is intentional. The agent never silently uses the wrong voice; it always
surfaces the fallback so the customer knows the mode they requested didn't load.

---

## Voice modes and the bench

Voice modes do NOT change the bench. The Provocation / Restraint / Coherence debate
runs underneath every voice. What changes is the surface.

A `paula_scher.md` voice will still refuse to ship work without a named belief — that's
the Coherence-Pole, which is structural, not stylistic. A `tibor_kalman.md` voice will
still push for specificity — that's the Provocation-Pole. The voice mode controls how
the verdict is delivered, not whether the verdict is sound.

---

## Cross-references

- Out-of-box voice: [`_default.md`](_default.md)
- Blank scaffold: [`_template.md`](_template.md)
- Bench composition: [`../_bench.md`](../_bench.md)
- Frameworks index: [`../frameworks_index.md`](../frameworks_index.md)
- Master skill: `../../SKILL.md`
- Voice spine (umbrella for all voice modes): `.claude/voice-spine.md`
