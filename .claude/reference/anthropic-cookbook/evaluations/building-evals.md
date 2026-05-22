---
name: building-evals
source: https://github.com/anthropics/claude-cookbooks/blob/main/misc/building_evals.ipynb
fetched: 2026-05-22
category: Evaluations
rook-relevance: high
rook-status: absorb-recommended
---

# Building Evals

## What it is

Foundational eval framework: input prompts + model outputs + golden answers + grades. Three grading methods ranked by cost-per-rerun:

1. **Code-based grading** — exact match, regex, structured comparison. Fastest, most reliable, requires constrained output design.
2. **Model-based grading** — Claude-as-judge with a grader prompt that compares output against rubric, outputs `<correctness>` tags. Handles open-ended tasks.
3. **Human grading** — irreducible-ambiguity backstop. Unsustainable at scale.

Key insight: "often all that lies between you and an automatable eval is clever design." Reformat tasks into multiple-choice or constrained outputs to enable code-grading.

## Key code/config

Dataset shape:
```json
[{"input_field": "prompt", "golden_answer": "reference"}]
```

Grader prompt:
```
Compare <answer> against <rubric>. Output 'correct' or 'incorrect' in <correctness> tags with reasoning.
```

Aggregate by parsing `<correctness>` XML tags into pass/fail percentages.

## Measured improvements / costs

No improvement numbers reported. The notebook shows mechanics, not before/after metric lifts.

## ROOK applicability

**Major gap.** ROOK currently has zero regression-testing layer for agents. Every agent SKILL.md change is tested by vibes. As ROOK ships to cohort and customer changes start flowing in, agents will drift silently — voice-contract violations, mode coverage gaps, regression on dispatch logic.

A `.claude/evals/` shelf with:
- Per-agent eval datasets (e.g., `agents/chief-of-staff/evals/dispatch.jsonl` with `{prompt, expected_route}`)
- A `scripts/run-evals.py` harness
- Grader prompts per agent (some code-graded for routing decisions, some Claude-judge for synthesis quality)

...would catch regressions BEFORE they ship. This pairs with Rule #16 (second-opinion-verify) — instead of only verifying production decisions, verify the agent itself on a fixed test set per release.

## Recommended action

**absorb-recommended** — highest-payoff item in this gap analysis. Build `.claude/evals/` scaffold + 3 starter eval sets (chief-of-staff routing, copywriter voice, librarian retrieval). Effort: ~2-3 days for scaffold + first 3 sets. Payoff: zero-cost regression detection before ship-vault zip. Should land in v3.1.
