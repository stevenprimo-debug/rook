---
name: second-opinion-verify
description: >
  Vendor-neutral adversarial second-opinion dispatcher. When invoked, runs the
  current decision through an adversarial review chain: Perplexity API (primary),
  Claude Opus subagent (fallback), or operator manual review (final fallback).
  Returns: AGREE / DISAGREE-WITH-REASON / NEEDS-MORE-CONTEXT.
  The invoking agent then synthesizes both positions visibly.
type: skill
category: Meta / Quality Gate
version: "2.0"
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
as_of: 2026-05-22
---

# second-opinion-verify -- Adversarial Second-Opinion Skill v2.0

> Renamed from `codex-cross-verify` on 2026-05-22 -- Codex CLI is not bundled with
> ROOK and customers are not expected to have ChatGPT Plus / OpenAI API access.
> The skill is now vendor-neutral with a Perplexity-primary, Opus-fallback chain.
> Source: `_CLAUDE.md` Section 0 Rule #16.

## Overview

This skill runs an adversarial review on a decision before it executes. It is
NOT peer review or an editorial pass -- it is a stress-test. The reviewer is
explicitly prompted to look for what is wrong, what was missed, or what
assumption is shaky.

Mandatory output from the reviewer: one of three verdicts.

```
AGREE              -- Reviewed the decision. No material objections. Proceed.
DISAGREE           -- [One-sentence reason naming the specific finding]
NEEDS-MORE-CONTEXT -- [One-sentence description of what is missing]
```

Boilerplate verdicts fail format. "AGREE because it seems fine" fails.
"AGREE" alone passes. "DISAGREE because the auth flow assumes session cookies
are available but the deployment context is cookie-less" passes.

## Adversarial review chain (in order)

The invoking agent walks this chain top-to-bottom and stops at the first
available reviewer.

### Tier 1 -- Perplexity API (primary)

If `PERPLEXITY_API_KEY` is set in the environment, call the Perplexity
`sonar-pro` model (or equivalent latest reasoning-tier model) with the
dispatch prompt below. Perplexity is the primary because:

- It runs adversarial reasoning natively with current web context
- The operator already has a key (per `.env` `ARCH_SECOND_OPINION_TOOL`)
- It is the cheapest cross-model second opinion that meets the bar

### Tier 2 -- Claude Opus subagent (fallback)

If `PERPLEXITY_API_KEY` is unset OR the Perplexity call fails, spawn a Claude
Opus subagent (via the Task tool) with the same dispatch prompt. Opus is the
fallback because:

- It is always available in the Claude Code runtime -- no extra key required
- Opus follows the adversarial frame more reliably than Sonnet
- The verdict format is unchanged

### Tier 3 -- Operator manual review (final fallback)

If both Tier 1 and Tier 2 are unavailable (rare -- e.g., Task tool disabled,
no network, no key), surface the decision to the operator via
`AskUserQuestion` with the flag: "No second-opinion model available -- manual
review only." The operator becomes the adversarial reviewer.

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

## Dispatch Prompt (used by Tier 1 and Tier 2)

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

## After Receiving the Verdict

The invoking agent MUST synthesize visibly:

```
Sonnet verdict:  [summary of invoking agent's original call]
Second opinion:  [the second-opinion-verify return -- AGREE/DISAGREE/NEEDS-MORE-CONTEXT]
Reviewer tier:   [Perplexity / Opus / Operator]
My call:         [final decision]
Because:         [one sentence naming a specific reason -- not a boilerplate hedge]
```

If `AGREE`: proceed. Log the synthesis line to `memory/dispatch_log.md` as a note.

If `DISAGREE`: surface to operator via AskUserQuestion with both verdicts as
options. Do NOT auto-proceed. The operator decides.

If `NEEDS-MORE-CONTEXT`: load the missing context from the vault, re-run the
original decision, then re-invoke second-opinion-verify before proceeding.

## Filesystem Boundary (anti-confusion)

The reviewer (Perplexity or Opus subagent) operates on ONLY what the invoking
agent provides in the prompt. It does not read vault files independently.
The invoking agent is responsible for including the relevant context excerpt.

## Reference implementation (Perplexity, Python)

```python
import os, requests

def second_opinion_perplexity(decision_text: str, context_text: str) -> str | None:
    key = os.environ.get("PERPLEXITY_API_KEY")
    if not key:
        return None  # caller falls through to Tier 2
    prompt = DISPATCH_PROMPT.format(decision=decision_text, context=context_text)
    try:
        r = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "sonar-pro",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            },
            timeout=60,
        )
        if r.status_code != 200:
            return None  # caller falls through to Tier 2
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return None  # caller falls through to Tier 2
```

If the Perplexity call raises or returns non-200, the caller falls through to
Tier 2 (Opus subagent). Never silent-fail -- log the tier that handled the call.

## Logging

Append to `agents/chief-of-staff/memory/dispatch_log.md` after every
second-opinion-verify invocation:

```
| second-opinion-verify | [ISO timestamp] | Tier: [Perplexity/Opus/Operator] |
  Decision: "[1-sentence summary]" | Verdict: [AGREE/DISAGREE/NEEDS-MORE-CONTEXT] |
  Operator action: [proceed/held/re-reviewed] |
```

Source: Rule #16 (`_CLAUDE.md` Section 0). Renamed + rebuilt 2026-05-22
(was `codex-cross-verify` 2026-05-21).
