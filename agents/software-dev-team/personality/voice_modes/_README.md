---
title: Voice Modes — Customer-Extensible Voice Library
agent: software-dev-team
status: shipped — customer-facing instructions
audience: customers / cohort students / Stack operators
---

# Voice Modes — How to make this agent speak like you

This directory is the **customization layer** of the agent.

The bench-of-three principles (Ship-Velocity / Production-Readiness / Debuggability) defines WHAT this agent reasons about.
**Voice modes define HOW it sounds while doing it.**

Every other agent platform ships ONE voice. The Stack ships 20 agents × N voice modes per agent. The customization is yours.

---

## What ships in the box

| File | Purpose |
|---|---|
| `_default.md` | The out-of-box Software Dev Team voice. Active when `{voice_mode}` is unset or set to `_default`. |
| `_README.md` | This file. Customer-facing instructions. |
| `_template.md` | Blank scaffold you copy + fill to author a new voice mode. |

---

## What voice modes ARE

A voice mode is a `.md` file in this directory that defines:

- **Signature phrases** — verbal fingerprints unique to the voice.
- **Do-list** — what the voice does.
- **Don't-list** — what the voice never does (inherits forbidden vocab from CD voice-spine § 4).
- **Sample paragraphs** — 3 worked examples showing the voice in action.
- **Edge cases / register guards** — how the voice shifts based on user state, mode, or context.

The bench debate (Ship-Velocity / Production-Readiness / Debuggability) runs underneath every voice mode — what changes is the surface, not the discipline.

---

## How to add a new voice mode

### Step 1 — Copy the template
```bash
cp personality/voice_modes/_template.md personality/voice_modes/<your_mode_name>.md
```
Naming: lowercase, underscore-separated. Examples: `hormozi.md`, `acme_corp_brand.md`.

### Step 2 — Fill in the template

Frontmatter + 7 sections: voice spine, signature phrases, do-list, don't-list, sample paragraphs, edge cases, attribution.

### Step 3 — Activate the mode
```
{voice_mode} = your_mode_name
```

The agent loads `personality/voice_modes/your_mode_name.md` and uses it as its voice spine for the session.

---

## Default behavior

If `{voice_mode}` is unset OR the requested file doesn't exist, the agent falls back to `_default.md` and surfaces a note. The agent never silently uses the wrong voice.

---

## Voice modes and the bench

Voice modes do NOT change the bench. The Ship-Velocity / Production-Readiness / Debuggability debate runs underneath every voice. What changes is the surface. The bench is structural; the voice is cosmetic (which is the customization layer that makes the agent feel like *yours*).

---

## Cross-references

- Out-of-box voice: [`_default.md`](_default.md)
- Blank scaffold: [`_template.md`](_template.md)
- Bench composition: [`../_bench.md`](../_bench.md)
- Frameworks index: [`../frameworks_index.md`](../frameworks_index.md)
- Master skill: `../../SKILL.md`
- Voice spine: `.claude/voice-spine.md`
