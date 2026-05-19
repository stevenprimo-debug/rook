---
title: Voice Modes — Customer-Extensible Voice Library
agent: chief-of-staff
status: shipped — customer-facing instructions
audience: customers / cohort students / Stack operators
---

# Voice Modes — How to make this agent speak like you (or like your favorite operator)

This directory is the **customization layer** of the agent.

The bench-of-three principles (Triage / Ambition / Reversibility) defines WHAT this
agent reasons about. **Voice modes define HOW it sounds while doing it.**

Every other agent platform ships ONE voice. The Stack ships 20 agents × N voice modes
per agent. The customization is yours.

---

## What ships in the box

| File | Purpose |
|---|---|
| `_default.md` | The out-of-box Chief of Staff voice — terse dispatcher tone, founder-personal register, anti-AI-slop. Active when `{voice_mode}` is unset or set to `_default`. |
| `_README.md` | This file. Customer-facing instructions for adding voice modes. |
| `_template.md` | Blank scaffold you copy + fill to author a new voice mode. |

---

## What voice modes ARE

A voice mode is a `.md` file in this directory that defines:

- **Signature phrases** — the verbal fingerprints the agent uses repeatedly.
- **Do-list** — what the voice does (lead with the move, complete sentences, etc.).
- **Don't-list** — what the voice never does (forbidden vocab, forbidden patterns).
- **Sample paragraphs** — 3 worked examples showing the voice in action across
  different scenarios.
- **Edge cases / register guards** — how the voice shifts based on user state, mode,
  or context.

The agent loads the active voice mode at session start via the `{voice_mode}`
parameter. Whatever file you point to becomes the agent's voice spine for the
session. The bench debate (Triage / Ambition / Reversibility) runs underneath every
voice mode — what changes is the surface, not the discipline.

---

## How to add a new voice mode

Three steps.

### Step 1 — Copy the template

```bash
cp personality/voice_modes/_template.md personality/voice_modes/<your_mode_name>.md
```

Naming convention: lowercase, underscore-separated. Examples: `hormozi.md`,
`cal_newport.md`, `acme_corp_brand.md`, `team_shorthand.md`.

### Step 2 — Fill in the template

The template has frontmatter + 6 sections. Fill each:

1. **Frontmatter** — `voice_mode_name`, `inspired_by` (optional attribution),
   `register` (one-line description of the voice), `cadence` (rhythm/length).
2. **Voice spine** — 5 bullets summarizing the voice.
3. **Signature phrases** — 5–10 verbal fingerprints unique to this voice.
4. **Do-list** — what the voice does. 6–10 items.
5. **Don't-list** — what the voice never does. 6–10 items.
6. **Sample paragraphs** — 3 worked examples covering common scenarios (standard
   intake, gated action, edge case).
7. **Edge cases / register guards** — how the voice shifts based on context.

### Step 3 — Activate the mode

When invoking Chief of Staff, set the `{voice_mode}` parameter:

```
{voice_mode} = your_mode_name
```

The agent loads `personality/voice_modes/your_mode_name.md` and uses it as its voice
spine for the session.

---

## Examples of voice modes you might add

These are not shipped — they're illustrative. The cohort lesson goes deeper on
authoring each one.

### `hormozi.md` — High-tempo, contrarian, sales-energy

Inspired by the operator who built and exited a $100M+ portfolio in 8 years. Voice
moves: every output names the dollar value at stake; surfaces the "boring obvious"
that other operators miss; refuses to add complexity until simpler version is
exhausted; closes with a forcing question.

### `cal_newport.md` — Slow-deep-protect, time-block discipline

Inspired by the computer science professor and author of *Deep Work* / *Slow
Productivity*. Voice moves: every output asks "is this deep or shallow?"; defaults
to fewer-things-deeper; refuses busy-work; closes with the time-block placement
recommendation.

### `acme_corp_brand.md` — Your company's brand voice

If your company has a brand-voice document, port its rules here. Signature phrases
become your brand-specific verbal fingerprints. The do-list and don't-list become
your brand-voice guardrails. Sample paragraphs become your brand in agent prose.

### `team_shorthand.md` — Your internal team's vernacular

If your team has a shared vocabulary (acronyms, in-jokes, shared frameworks), encode
it here. The agent now speaks your team's language — onboarding new hires becomes a
matter of "read the voice mode file."

### `ceos_voice.md` — Your CEO's tone

For executive assistants and chiefs of staff who want the agent to draft in the
voice of the person they support. Capture the CEO's signature phrases from emails +
internal docs; encode the rhythm; ship the voice. Now drafts written by the agent
read like drafts written by them.

---

## The cohort lesson (the Stack)

Voice-mode authoring is taught as a skill in the the cohort. The lesson covers:

1. **Voice corpus collection** — how to pull 50+ samples of a voice from public
   writing, podcasts, emails.
2. **Pattern extraction** — what makes a voice distinctive (signature phrases,
   sentence shapes, vocabulary preferences, rhetorical moves).
3. **Do-and-don't construction** — converting voice analysis into actionable rules
   the agent can follow.
4. **Sample paragraph authoring** — writing 3 worked examples that the agent uses as
   anchors.
5. **Register guards** — how the voice shifts under stress, deadline, exploration.
6. **Eval testing** — how to verify the agent is actually speaking in the voice
   (qualitative review + corpus comparison).

The intake form for the cohort generates a seed `<custom>.md` based on a few prompts:

> *"Whose writing voice do you like? Who would you want speaking in your inbox?
> What's the energy register your brand uses? Are there 3 sentences you've seen
> recently that captured how you want this agent to sound?"*

Cohort students refine the seed into a full voice mode across 4 lessons. By the end
they have their own custom voice mode authored for every agent in the line.

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

Voice modes do NOT change the bench. The Triage / Ambition / Reversibility debate
runs underneath every voice. What changes is the surface.

A `hormozi.md` voice will still refuse to DEPLOY on irreversible action without
confirmation — that's the Reversibility-Pole, which is structural, not stylistic. A
`cal_newport.md` voice will still surface the 10x version when the user is
under-asking — that's the Ambition-Pole.

The voice mode controls **how the verdict is delivered**, not **whether the verdict
is sound**. The bench is structural; the voice is cosmetic. (Cosmetic is not a
diminishment — it's the customization layer that makes the agent feel like *yours*.)

---

## Cross-references

- Out-of-box voice: [`_default.md`](_default.md)
- Blank scaffold: [`_template.md`](_template.md)
- Bench composition (what the agent reasons about): [`../_bench.md`](../_bench.md)
- Frameworks index (callable methodologies): [`../frameworks_index.md`](../frameworks_index.md)
- Master skill: `../../SKILL.md`
- Voice spine (umbrella for all voice modes — § 3–4 mandatory + § 7 voice-dominance map): `.claude/voice-spine.md`
