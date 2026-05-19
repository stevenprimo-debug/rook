---
title: Voice Modes — Customer-Extensible Voice Library
agent: sales-director
status: shipped — customer-facing instructions
audience: customers / operators
---

# Voice Modes — How to make this agent speak like you (or your favorite operator)

This directory is the **customization layer** of the agent.

The bench-of-three principles (Hunter / Qualifier / Closer) defines WHAT this
agent reasons about. **Voice modes define HOW it sounds while doing it.**

Every other agent platform ships ONE voice. This Stack ships agents with N
voice modes per agent. The customization is yours.

---

## What ships in the box

| File | Purpose |
|---|---|
| `_default.md` | Out-of-box Sales Director voice — terse, dollar-value-first, anti-hopium. Active when `{voice_mode}` is unset or set to `_default`. |
| `_README.md` | This file. Customer-facing instructions. |
| `_template.md` | Blank scaffold you copy + fill to author a new voice mode. |

---

## What voice modes ARE

A voice mode is a `.md` file in this directory that defines:

- **Signature phrases** — verbal fingerprints the agent uses repeatedly.
- **Do-list** — what the voice does.
- **Don't-list** — what the voice never does.
- **Sample paragraphs** — 3 worked examples showing the voice in action.
- **Edge cases / register guards** — how the voice shifts based on user state,
  mode, or context.

The agent loads the active voice mode at session start via the `{voice_mode}`
parameter. The bench debate runs underneath every voice — what changes is the
surface, not the discipline.

---

## How to add a new voice mode

### Step 1 — Copy the template

```bash
cp personality/voice_modes/_template.md personality/voice_modes/<your_mode_name>.md
```

Naming: lowercase, underscore-separated. Examples: `hormozi.md`, `sandler.md`,
`acme_corp_brand.md`.

### Step 2 — Fill in the template

The template has frontmatter + 6 sections. Fill each.

### Step 3 — Activate the mode

When invoking the agent, set `{voice_mode} = your_mode_name`. The agent loads
`personality/voice_modes/your_mode_name.md` and uses it as its voice spine.

---

## Examples of voice modes you might add

### `hormozi.md` — High-tempo, contrarian, sales-energy

Voice moves: every output names the dollar value at stake; surfaces the
"boring obvious" that other operators miss; closes with a forcing question.

### `sandler.md` — Pain-first, qualification-discipline

Voice moves: every output asks "where is the pain?"; refuses to advance a deal
without pain locked; surfaces budget early; closes with the next-step question.

### `acme_corp_brand.md` — Your company's brand voice

Port your brand voice rules here. Signature phrases become your brand-specific
verbal fingerprints.

### `ceos_voice.md` — Your sales leader's voice

For sales managers who want the agent to coach reps in their leader's voice.
Capture signature phrases from their team huddles; encode the rhythm.

---

## Default behavior

If `{voice_mode}` is unset, OR the requested file doesn't exist, the agent
falls back to `_default.md` and surfaces a note:

> *"Voice mode `<X>` not found — using default. Add
> `personality/voice_modes/<X>.md` to enable this mode."*

The agent never silently uses the wrong voice.

---

## Voice modes and the bench

Voice modes do NOT change the bench. Hunter / Qualifier / Closer runs
underneath every voice. The voice mode controls **how the verdict is
delivered**, not **whether the verdict is sound**.

---

## Cross-references

- Out-of-box voice: [`_default.md`](_default.md)
- Blank scaffold: [`_template.md`](_template.md)
- Bench composition: [`../_bench.md`](../_bench.md)
- Frameworks index: [`../frameworks_index.md`](../frameworks_index.md)
- Master skill: `../../SKILL.md`
- Voice spine: `.claude/voice-spine.md`
