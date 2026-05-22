---
name: rook-prompt-builder
description: Structure an unstructured prompt retroactively into the ROOK 7-section XML pattern. Use when the operator pastes a long voice-dump (>200 words, no headers / XML tags / labeled sections / dispatch syntax), needs a shippable system prompt for an API call or downstream agent, or is asking Claude 2+ clarifying questions back-to-back because the original ask was underspecified. Also fires when the operator wants their request reshaped into the canonical <role> + <task> + <constraints> + <output> shape, or types phrases like "structure this", "tighten this prompt", "rewrite this as a system prompt", "make this XML-shaped", or "give me a proper prompt for this".
argument-hint: <unstructured prompt or voice-dump to retroactively structure>
---

Load the skill at `.claude/skills/core/skills/prompt-builder/SKILL.md` and apply its structured-prompt-generation workflow to the following input:

<input>
$ARGUMENTS
</input>

Follow the skill's canonical flow:

1. **Understand the task** in one sentence — what is Claude producing and for whom
2. **Fill the required tags** — `<role>`, `<task>`, `<output>` are almost always needed
3. **Add supporting tags** as signal warrants — `<context>` for background, `<examples>` when format precision matters, `<constraints>` for hard rules, `<thinking>` for reasoning-heavy tasks
4. **Skip what doesn't add signal** — a 3-tag prompt that's tight beats a 7-tag prompt with filler
5. **Show the assembled prompt** in a clean code block, ready to copy-paste
6. **Offer one refinement pass** — ask if role, constraints, or output format need adjusting

If `$ARGUMENTS` is empty, ask the operator for the prompt they want structured. Do not narrate the structuring process — return the structured prompt as the artifact.
