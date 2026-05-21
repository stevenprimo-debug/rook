---
name: codex-cross-verify
description: >
  Adversarial second-opinion dispatcher. When invoked, dispatches the current
  decision or verdict to an Opus-tier subagent for adversarial review.
  Returns: AGREE / DISAGREE-WITH-REASON / NEEDS-MORE-CONTEXT.
  The invoking agent then synthesizes both positions visibly.
type: skill
category: Meta / Quality Gate
version: "1.0"
status: operational
model: opus
preamble-tier: 1
fire_when:
  - reversibility=N decisions before execution
  - "this is the right answer" high-stakes claims
  - routing-critical infrastructure verdicts
  - any action the operator would have to apologize for if wrong
skip_when:
  - reversibility=Y with clear vault evidence
  - factual lookups where the vault has the answer
  - format/style preferences with no downstream impact
as_of: 2026-05-21
---

# codex-cross-verify -- Adversarial Second-Opinion Skill v1.0

> Adapted from GStack `/codex` adversarial review pattern (codex/SKILL.md.tmpl).
> Stripped of Garry-isms and Codex CLI dependency. ROOK-native: pure subagent dispatch.
> Source: `_CLAUDE.md` Section 0 Rule #16.

## Overview

This skill dispatches an Opus-tier subagent to adversarially review a decision
before it executes. It is NOT a peer-review or editorial pass. It is a stress-test:
the subagent is explicitly prompted to look for what is wrong, what was missed, or
what assumption is shaky.

Mandatory output from the subagent: one of three verdicts.

```
AGREE       -- Reviewed the decision. No material objections. Proceed.
DISAGREE    -- [One-sentence reason naming the specific finding]
NEEDS-MORE-CONTEXT -- [One-sentence description of what is missing]
```

Boilerplate verdicts fail format. "AGREE because it seems fine" fails.
"AGREE" alone passes. "DISAGREE because the auth flow assumes session cookies
are available but the deployment context is cookie-less" passes.

## When To Fire

Mandatory (no bypass):
- Any action where `reversibility=N` (client email, prod push, public post, money)
- Any routing decision that affects 2+ agents with no rollback path
- Any "this is definitely the right architecture" claim the operator will build on

Recommended (use judgment):
- When the invoking agent is operating outside its primary domain
- When two plausible options both seem correct and the stakes are high

Skip (do not waste tokens):
- Reversible work with vault evidence
- Factual lookups confirmed by a file read
- Format and style calls with no downstream consequences

## Dispatch Template

The invoking agent spawns a subagent with this prompt structure:

```
You are an adversarial reviewer. Your job is NOT to be helpful.
Your job is to find what is wrong, what was missed, and what assumption
is shaky in the following decision.

DECISION UNDER REVIEW:
[Paste the full decision text, including the reasoning and the proposed action]

CONTEXT:
[The vault files or prior session context relevant to this decision]

FILESYSTEM BOUNDARY:
Do NOT read or execute any files under ~/.claude/, .claude/skills/,
or any path the invoking agent did not explicitly provide above.

OUTPUT FORMAT (required -- no exceptions):
Line 1: AGREE / DISAGREE-WITH-REASON / NEEDS-MORE-CONTEXT
Line 2 (if DISAGREE or NEEDS-MORE-CONTEXT): one sentence naming the
specific finding or the specific missing context.

Boilerplate verdicts fail. "Looks good" fails. Name the thing.
```

## After Receiving the Subagent Verdict

The invoking agent MUST synthesize visibly:

```
Sonnet verdict: [summary of invoking agent's original call]
Opus review:    [the codex-cross-verify return -- AGREE/DISAGREE/NEEDS-MORE-CONTEXT]
My call:        [final decision]
Because:        [one sentence naming a specific reason -- not a boilerplate hedge]
```

If `AGREE`: proceed. Log the synthesis line to `memory/dispatch_log.md` as a note.

If `DISAGREE`: surface to operator via AskUserQuestion with both verdicts as options.
Do NOT auto-proceed. The operator decides.

If `NEEDS-MORE-CONTEXT`: load the missing context from the vault, re-run the
original decision, then re-invoke codex-cross-verify before proceeding.

## Filesystem Boundary (anti-confusion)

The codex-cross-verify subagent operates on ONLY what the invoking agent
provides in the prompt. It does not read vault files independently.
The invoking agent is responsible for including the relevant context excerpt.
This is the ROOK-native equivalent of GStack's Codex filesystem boundary prompt.

## Logging

Append to `agents/chief-of-staff/memory/dispatch_log.md` after every
codex-cross-verify invocation:

```
| codex-cross-verify | [ISO timestamp] | Decision: "[1-sentence summary]" |
  Verdict: [AGREE/DISAGREE/NEEDS-MORE-CONTEXT] | Operator action: [proceed/held/re-reviewed] |
```

Source: Rule #16 (`_CLAUDE.md` Section 0). GStack adaptation locked 2026-05-21.
