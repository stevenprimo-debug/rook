# ROOK — Customer Install Guide

You just extracted the ROOK cohort zip. Three install steps stand between you and a running vault.

## Prerequisites

| Tool | Why |
|---|---|
| Python 3.11+ | Most skills + connector helpers are Python |
| Git | The vault uses git for memory versioning |
| Claude Code CLI | The runtime — `npm install -g @anthropic-ai/claude-code` |
| Go (optional) | Only if you want `obsidian-cli` for programmatic Obsidian vault I/O |

## Step 1 — Install Python dependencies

```powershell
# Windows (PowerShell)
python -m pip install -r requirements.txt

# Mac / Linux
pip install -r requirements.txt
```

This installs `markitdown`, `playwright`, `weasyprint`, `pypdf2`, `pyyaml`, `requests`, `pytest`.

After install, run the playwright browser setup (one-time):
```
python -m playwright install chromium
```

## Step 2 — Install `obsidian-cli` (optional)

If you use Obsidian as your vault interface and want agents to read/write programmatically:

```
go install github.com/Yakitrak/obsidian-cli@latest
```

Verify with: `obsidian-cli --help`

Skip this step if you don't use Obsidian. Agents fall back to direct filesystem reads.

## Step 3 — Configure your connector credentials

The vault ships with connector documentation but **no credentials** — those are operator-specific. For each service you'll use, see the matching `.claude/connectors/<service>/README.md` for the operator setup checklist.

Recommended minimum for first run:
- `.claude/connectors/gmail/` — read inbox, draft replies
- `.claude/connectors/perplexity/` — second-opinion synthesis for deep-researcher

Each connector reads credentials from environment variables. Add to your PowerShell `$PROFILE` (Windows) or `~/.bashrc` / `~/.zshrc` (Mac/Linux):

```powershell
$env:PERPLEXITY_API_KEY = "pplx-..."
$env:GMAIL_OAUTH_REFRESH_TOKEN = "..."
# etc — see each connector's README for the env var names
```

## Step 4 — Build your shared-shelf knowledge graph

The shared shelf at `.claude/reference/` (API docs, templates, methodology, learning paths) is queried by every agent via graphify before answering domain questions. The graph index is per-customer — it lives at `.claude/reference/graphify-out/` and is gitignored, so you build it once on install and the librarian regenerates it weekly.

```bash
pip install graphifyy
python -m graphify .claude/reference/
```

Expect 60-90 seconds the first time. You'll see a node + edge count when it finishes (~600 nodes, ~600 edges for the default shipped shelf).

Verify the graph built:

```bash
python -m graphify query "shopify webhook auth"
# → returns 5-10 relevant files from .claude/reference/shopify/
```

If you see relevant results, the shelf is queryable and every agent's `Step 1 — Load Context` will work.

## Step 5 — Hooks + smoke test

Wire ROOK hooks into your Claude Code settings.json (idempotent — safe to re-run):

```bash
# Windows
powershell -ExecutionPolicy Bypass -File hooks/INSTALL.ps1

# Mac/Linux
bash hooks/INSTALL.sh
```

Then run the inbox-routing tests:

```bash
cd .claude/skills/core/inbox_routing
python -m pytest tests/
# Should print: "27 passed in <N>s"
```

Finally, the Hello World smoke test — open Claude Code in this directory and type:

> `chief-of-staff what's in this vault?`

Expected response: a one-paragraph orientation listing the 20 agents by category, NOT a placeholder. If you get a placeholder, re-run Step 5 (hooks didn't wire).

## What you do NOT do during install

- **Do NOT** set `ROOK_SESSION_MODE=operator` — that's a build-time flag for the operator who built ROOK. As a cohort customer, you stay in default (`customer`) mode, and your memory writes go to standard paths.
- **Do NOT** commit your `.claude/credentials/` to git — it's in `.gitignore` for a reason.

## First-run

Open Claude Code in this directory. The session-mode injector will surface:

```
===== ROOK SESSION MODE: CUSTOMER =====
Active mode: CUSTOMER (default — operator did not set ROOK_SESSION_MODE)
Memory writes go to: agents/<agent>/memory/<file> (shipped paths)
```

That's the signal everything is wired up correctly. Start with:

> "Hey chief-of-staff, what's in this vault?"

Chief of Staff will walk you through the 20-agent roster.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `markitdown` not found | `pip install markitdown` (Step 1 didn't run) |
| `playwright` browser fails | `python -m playwright install chromium` |
| Connector calls return 401 | Credential env var not set — check the connector's README |
| Agent doesn't recognize a keyword | Check `routing-rules.json` — that's where routing lives; SKILL.md is the source-of-truth for the keyword arrays |

## Support

If you're stuck: the documentation for every agent is at `agents/<agent>/SKILL.md`. Every agent's bench (its 3-pole principles) is at `agents/<agent>/personality/_bench.md`.
