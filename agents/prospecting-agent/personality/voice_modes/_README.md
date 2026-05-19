---
title: Voice Modes — Customer-Extensible Voice Library
agent: prospecting-agent
status: shipped — customer-facing instructions
audience: customers / operators
---

# Voice Modes — How to make this agent speak like you (or your favorite operator)

This directory is the **customization layer** of the agent.

The bench-of-three principles (Signal / Scale / Fit) defines WHAT this
agent reasons about. **Voice modes define HOW it sounds while doing it.**

## What ships in the box

| File | Purpose |
|---|---|
| `_default.md` | Out-of-box voice — terse, signal-first, table-oriented. Active when `{voice_mode}` is unset. |
| `_README.md` | This file. |
| `_template.md` | Blank scaffold for customer-authored modes. |

## What voice modes ARE

A voice mode is a `.md` file defining: signature phrases, do-list, don't-list,
3 sample paragraphs, edge-case register guards.

The bench debate runs underneath every voice — what changes is the surface,
not the discipline.

## How to add a new voice mode

### Step 1 — Copy template

```bash
cp personality/voice_modes/_template.md personality/voice_modes/<your_mode>.md
```

### Step 2 — Fill template

6 sections + frontmatter. Replace placeholders with your voice.

### Step 3 — Activate

Set `{voice_mode} = your_mode_name` when invoking the agent.

## Default behavior

If `{voice_mode}` is unset OR file missing, agent falls back to `_default.md`
and surfaces a note.

## Voice modes and the bench

Voice modes do NOT change the bench. Signal / Scale / Fit runs underneath
every voice. Voice controls how the verdict is delivered, not whether it is sound.

## Cross-references

- Out-of-box voice: [`_default.md`](_default.md)
- Blank scaffold: [`_template.md`](_template.md)
- Bench: [`../_bench.md`](../_bench.md)
- Frameworks index: [`../frameworks_index.md`](../frameworks_index.md)
- Master skill: `../../SKILL.md`
- Voice spine: `.claude/voice-spine.md`
