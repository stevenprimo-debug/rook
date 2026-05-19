---
name: Voice Modes — README
description: How to add a custom voice mode for the librarian agent. The bench-of-three defines WHAT the agent reasons about; voice modes define HOW it sounds while doing it.
type: voice-mode-readme
agent: librarian
version: "2.0.0"
---

# Voice Modes — How to Add Your Own

The librarian ships with `_default.md` as its out-of-box voice. You can replace it for any session by authoring a new voice mode file in this folder.

## What a voice mode controls

- **Cadence** — sentence rhythm, paragraph length, the music of the output.
- **Register** — how formal/casual the librarian sounds when it writes the digest.
- **Vocabulary inclusions** — verbs and nouns specific to your craft (e.g., an "archivist" voice uses different language than a "forensic_auditor" voice).
- **Opening shapes** — how the librarian starts every reply.
- **Closing patterns** — how the librarian ends every reply.

## What a voice mode CANNOT override

The following are voice-spine § 4 locks. Every voice mode inherits them:

- **No preamble.** First line of output IS the verdict.
- **No forbidden vocabulary.** "Elegant," "premium," "magical," "deep dive," "as an AI...", "great question," "happy to help," "synergy," "leverage" (as filler verb), "10x," "crush it," "grindset," "circle back," "unpack," "actionable" (as filler), "drive value," "move the needle." Full list in `_default.md`.
- **No "cheap," "shortcut," or "lazy" framing.** Right-sized scope ships at full quality.
- **No bullet-list-as-default** outside structured tables.
- **No naming a person from the bench in output.** Methodology by name; credit lives in `frameworks_attribution.md` only.
- **No deletion.** Archive only.

## How to author a new voice mode

1. **Copy `_template.md`** to a new file with your voice mode's slug — for example, `quiet_curator.md`, `forensic_auditor.md`, `archivist.md`, or `<your_brand>_archivist.md`.
2. **Fill the template sections** — cadence, register, vocabulary inclusions, opening shapes, closing patterns. Be specific. "Sounds professional" is not a voice mode; "uses 1-3 word verdict sentences followed by one long causal sentence" is.
3. **Test the voice** by invoking the agent with `{voice_mode} = <your-slug>` (set in the agent invocation parameters).
4. **Iterate.** Read the output. If it sounds like default Claude with your voice tacked on, the voice mode isn't doing enough work. The voice should override the substrate, not sit on top of it.

## Recommended starter voices for the librarian

These are not shipped — you add them yourself:

- **`quiet_curator.md`** — minimal output, lots of white space, never volunteers context.
- **`forensic_auditor.md`** — investigative tone, every claim cited, comfortable with uncertainty stated explicitly.
- **`archivist.md`** — librarian-classical voice, more verbose than default, prefers full prose to count-summaries.
- **`<your_brand>.md`** — your company's house voice, applied to custodial reports.

## How the agent loads your voice mode

At invocation, the agent reads `personality/voice_modes/<{voice_mode}>.md`. If the file exists, that voice mode is active for the session. If the file does not exist, the agent falls back to `_default.md` and surfaces a note: *"Voice mode `<X>` not found — using default. Add `personality/voice_modes/<X>.md` to enable this mode."*

## Cohort lesson hook

The the cohort goes deeper than this README. You'll learn to:

- Author voice modes with corpus citations (so the agent can cite specific phrases that match your brand).
- Build do-and-don't lists at scale.
- Set register guards (when to soften, when to harden).
- Stress-test voice modes against forbidden patterns.

That's the depth. This README is the entry point.

## What "good" looks like

The litmus test from the voice spine: if you removed the voice mode name from the top of the file, could you still tell which voice it was from the output? If yes, the voice mode is doing its job. If no, the voice mode is sitting on default-Claude-warmth without overriding it.

## Cross-references

- Out-of-box voice: `_default.md`
- Blank scaffold: `_template.md`
- Voice spine (umbrella every voice mode inherits): `.claude/voice-spine.md`
- Bench (what the agent reasons about): `../_bench.md`
- Frameworks index: `../frameworks_index.md`
