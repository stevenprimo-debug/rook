# Methodology Coverage — Roadmap

**Status: in progress. Not all methodologies are written yet.**

Each agent in this vault carries a `personality/_bench.md` (operating principles) and `personality/frameworks_index.md` (named frameworks the agent operates within). Deeper methodology documents — 200-400 line writeups of each framework — are planned but not yet present.

## What exists today

- 20 agents with `SKILL.md` + `README.md` + `CLAUDE.md`
- 20 agents with `personality/_bench.md` + `personality/frameworks_index.md` + `personality/frameworks_attribution.md`
- Sub-skills where the agent's work decomposes naturally (e.g., `agents/shopify-agent/skills/{build,operate,daily-ops,agentic-buyer}/`)

## What does not yet exist

Methodology-deep files at `agents/<slug>/methodology/*.md`. These are planned for v1.1+.

## How to read agent capability today

1. Read `agents/<slug>/SKILL.md` for what the agent does and when it fires.
2. Read `agents/<slug>/personality/_bench.md` for the productive-tension poles that guide the agent's judgment.
3. Read `agents/<slug>/personality/frameworks_index.md` for the named frameworks the agent draws on.
4. Read `agents/<slug>/personality/frameworks_attribution.md` for originator credit on those frameworks.

If you need framework details beyond those four files, consult vendored references at `.claude/reference/` or the originator's canonical material.

## Replaces

`agents/_methodology-gap-index.md` (archived 2026-05-21 to `_archive/2026-05/methodology-gap-index-aspirational/`). The archived file claimed 40 methodology documents existed when none did. This file replaces it with an honest roadmap.
