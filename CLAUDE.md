# ROOK — Powered by Claude

A 20-agent operating system. This file is the top-level routing contract; agent bodies live in `agents/<name>/SKILL.md`.

## What this is

A shippable team of 20 specialized agents. Each agent is a master skill with a principle bench, customer-extensible voice modes, and the universal file → knowledge → vault → export pipeline. Customers invoke any agent from their Claude Code workspace after installation.

## Dispatch

**chief-of-staff** is the front door. Every session that doesn't already know which agent it needs starts there. **librarian** is the memory custodian — runs in the background, audits the vault, writes a weekly digest.

See [`.claude/agents/_ROSTER.md`](.claude/agents/_ROSTER.md) for the canonical 20-agent list.

## Workspace layout

```
.claude/
├── agents/        ← 20 subagent registrations (one .md per agent)
├── skills/        ← Shared skills (core/, registry/, templates/)
└── rules/         ← Glob-scoped context rules

agents/            ← 20 agent bodies (SKILL.md + personality/ + context/ + memory/)
projects/          ← Job-shaped work (use _template/ to scaffold)
hooks/             ← Runtime hooks (run INSTALL.ps1 or INSTALL.sh)
_archive/          ← Retired content (append-only)
```

## Per-agent contract (5 required items)

Every agent must have:
1. `.claude/agents/<name>.md` — subagent registration
2. `agents/<name>/SKILL.md` — agent body
3. `agents/<name>/personality/` — bench + voice modes + framework attribution
4. `agents/<name>/memory/` — agent-written learned state (librarian-audited)
5. `agents/<name>/context/` — human-curated reference material (read-only to agents)

## Install hooks

```
# Windows
.\hooks\INSTALL.ps1

# Mac/Linux
./hooks/INSTALL.sh
```

Installs all runtime hooks into `~/.claude/settings.json`. Idempotent.

## Anti-patterns (never in agent SKILL.md files)

Customer-facing agent content must remain neutral and generic. Do NOT include:

- **Real company names** (your employer, your customers, any actual organization)
- **Named individuals** (real people, including yourself)
- **City or location references** tied to a specific operator
- **Industry-vertical framing** that locks the agent to one industry (use generic role language instead)
- **Personal finance, commission, or trading specifics** tied to a particular user

Use placeholders like `[Your Company]`, `[Your Industry]`, `[your employer]` when example context is required. Operator-specific state belongs in `~/.claude/CLAUDE.md` (outside this folder), not in agent files.
