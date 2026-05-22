---
name: managed-agents-shelf
source: https://docs.claude.com/en/docs/agents-and-tools/managed-agents
fetched: 2026-05-22
category: anthropic-feature
launch-date: 2026-04-23
rook-relevance: high
rook-consumers: chief-of-staff, software-dev-team, finance-manager
---

# Managed Agents — ROOK Reference Shelf

Comprehensive reference set on Anthropic's Managed Agents product (launched 2026-04-23). Deduplicated from operator-vault dept mirrors — only the canonical-content version of each topic is included.

## What's here

| File | What it covers | Source |
|---|---|---|
| [overview.md](overview.md) | The official Anthropic Managed Agents product overview (canonical doc-shelf clipping) | docs.claude.com Managed Agents overview |
| [get-started.md](get-started.md) | Setup walkthrough + initial integration patterns | Anthropic getting-started guide |
| [pricing-analysis.md](pricing-analysis.md) | Independent pricing breakdown — "Let's Talk About How We're Going to Pay for This" | Operator-curated analysis post-launch |
| [pros-cons-self-host.md](pros-cons-self-host.md) | Honest pros/cons + "how to run agents yourself" if Managed Agents doesn't fit | Operator-curated technical analysis |
| [scaling-decoupling-brain-from-hands.md](scaling-decoupling-brain-from-hands.md) | Scaling pattern — decoupling reasoning (brain) from execution (hands) | Operator-curated architectural deep dive |

## ROOK applicability

Three angles ROOK consumers should track:

| Angle | Which ROOK agent | Why it matters |
|---|---|---|
| **Architectural alternative** | chief-of-staff, software-dev-team | Managed Agents is Anthropic's hosted answer to the orchestration problem ROOK solves locally. Understanding it = understanding the competitive surface ROOK ships against. |
| **Pricing implications** | finance-manager | Per-agent hosted pricing changes the unit economics math for any customer comparing ROOK's $0/month local stack vs Anthropic-hosted runtime. |
| **Pattern absorption** | r-and-d-lead, chief-of-staff | The "decoupling brain from hands" scaling pattern in `scaling-decoupling-brain-from-hands.md` is directly applicable to ROOK's chief-of-staff → specialist-agent dispatch model. Worth a pattern-extract pass. |

## Dedup notes

Content sourced from multiple operator-curated copies; the most complete canonical version of each topic was selected during shelf intake. Stub copies (400-700 bytes) were skipped as routing placeholders.

## Cross-references

- [[../guides/skills]] — Anthropic skills spec (Managed Agents builds on skills as the unit of agent definition)
- [[../claude-code/subagents]] — local subagent dispatch (ROOK's alternative to Managed Agents)
- [[../../anthropic-cookbook/agent-patterns/orchestrator-workers]] — orchestration pattern ROOK and Managed Agents both implement differently
