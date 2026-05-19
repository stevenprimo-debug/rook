# `vault-agents/` — Tier 2 agents (operator-only, never ship)

This folder holds agents that live in the operator's local ROOK repo but
**never ship to cohort customers**. The cohort's vault has only the 20
Tier 1 operator agents under `agents/`; this folder is excluded from the
cohort package by `scripts/package-for-cohort.py`.

## Why this exists

Some agents only make sense for the person who BUILT ROOK — not for someone
who INSTALLED it. The cohort customer:
- Didn't build the vault — they don't need an agent that audits the build
- Doesn't run CI on the system — they don't need ci-gate management
- Doesn't manage connectors across N customers — they only manage their own
- Has a different contamination risk profile — they're leaking their brand,
  not yours

Shipping vault-internal agents into a cohort vault would either be dead
weight or, worse, poke at the customer's infrastructure in ways neither
party wants.

## Current roster

| Agent | Role | Status |
|---|---|---|
| `ops-engineer` | Vault infrastructure custodian — registration sync, CI gates, sanitizer wiring, connector hygiene, cohort packaging | v1.0 written |

## Excluded from cohort package

`scripts/package-for-cohort.py` reads `vault-agents/` directory names and
excludes them from the produced zip. Ops-engineer never travels.

## When to add to vault-agents/ vs agents/

| Question | If yes |
|---|---|
| Does the customer have a reason to invoke this agent? | `agents/` (Tier 1) |
| Does this agent maintain the system that ships? | `vault-agents/` (Tier 2) |
| Does this agent touch the operator's cross-customer state (multiple customer credentials, multi-vault telemetry, package pipeline)? | `vault-agents/` (Tier 2) |
| Would it be dead weight in a fresh customer install? | `vault-agents/` (Tier 2) |

## Anthropic Managed Agents 20-cap note

The Anthropic Managed Agents 20-agent-per-coordinator cap applies to agents
the coordinator can dispatch to. Vault-only custodial agents that run on
scheduled hooks (not on prompt dispatch) don't consume coordinator slots in
the same way — ops-engineer runs via cron/hook, not via the chief-of-staff
router. Same pattern as librarian's weekly digest.
