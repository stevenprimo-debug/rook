# `.claude/connectors/` — vault-level connector configs

Connectors are how an agent talks to an external service. Each service gets
its own sub-folder.

## Convention (locked 2026-05-19)

```
.claude/connectors/
├── README.md                       ← this file (convention)
├── <service>/
│   ├── README.md                   ← agent-facing: setup, reversibility, when to invoke
│   ├── api-reference.md            ← full API docs as context (verify against live docs)
│   └── client.py                   ← Python helper Client class (optional — only when API-direct)
```

## Why vault-level (not per-agent)

A connector is **credentials + endpoints + reversibility class**. Multiple
agents share the same credentials (one HubSpot account, one Gmail, one
Stripe) — duplication across agents creates drift and credential-rotation
nightmares.

What's per-agent is **which connectors an agent is authorized to invoke** —
declared in the agent's `SKILL.md` frontmatter under `connectors:`. What's
per-agent or per-skill is **parameters** (which HubSpot pipeline view
sales-director uses vs account-manager) — those live in
`agents/<agent>/context/connectors/<service>.md` when they exist.

## When a connector lives here

Any service the operator actively uses across the agent line. No minimum
consumer count — centralized credential management is the point.

If the service is operator-specific to one agent (e.g., an experimental SDK
only r-and-d-lead is testing), it can live at `agents/<agent>/connectors/`
or `agents/<agent>/skills/<skill>/connectors/`. Promote upward when a second
agent needs it.

## Integration kinds

| Kind | What it means | Has `client.py`? |
|---|---|---|
| **MCP-backed (Anthropic-wired)** | Service is exposed via an Anthropic-hosted MCP already in the operator's setup (Gmail, GCal, Vercel, Cloudflare, Supabase, Drive, ZoomInfo) | No — agents call MCP tools directly |
| **MCP-backed (community)** | Service has a community MCP worth wiring (Figma) | Optional — MCP preferred when stable |
| **API-direct** | No MCP exists or is reliable; agents call the API via Python helper | Yes — `client.py` is the entry point |

## What every `README.md` must include

1. **Status** — v1 stub, v1 written, v1 shipped, deferred to v1.1
2. **Consumers** — which agents declare this connector in their frontmatter
3. **Credentials** — env var names + storage convention
4. **Endpoints** — what the connector talks to (or "uses MCP namespace X")
5. **Reversibility class per operation** — Y for read-only, N for any external state change
6. **Invocation pattern** — minimum runnable example
7. **Operator setup checklist** — checkboxes for first-time setup

## What every `api-reference.md` must include

1. Auth shape (headers, token form)
2. Endpoints with method, purpose, reversibility per endpoint
3. Error patterns and recommended backoff
4. First-use notes (verify against live docs, this snapshot may go stale)

## Reversibility convention

Every connector classifies its operations:

- **Y (reversible)** — read endpoints, draft endpoints (saves to local state
  or service drafts folder), internal state updates. Agents invoke autonomously.
- **N (irreversible)** — sends, deletes, archives, mutations, money movement,
  external publishing. Agents NEVER invoke without explicit operator confirm.

Inbox Custodian's `send` actions are the canonical example of N — the
Reversibility-Discipline-Pole in inbox-manager's bench enforces per-item
operator confirm before any external send. Same pattern applies to
sales-director/skills/outreach when it sends, sales-director/skills/closing
when it triggers a DocuSign or Adobe Sign envelope, finance-manager when it
hits Stripe with anything but a read.

## Credentials storage

Per-operator, never committed:
- PowerShell profile env vars (preferred for local dev)
- `~/.claude/credentials/<service>.json` (gitignored)
- Vault-level secret manager (when going multi-machine)

The repo's `.gitignore` already covers `**/.env`, `**/*api-key*`, `**/credentials.json`, etc.

## How an agent invokes a connector

For MCP-backed connectors, the agent calls the MCP tool by name (auto-discovered).

For API-direct connectors:

```python
from claude_connectors.perplexity import PerplexityClient
ppx = PerplexityClient.from_env()
result = ppx.search(query="...", max_results=5)
```

The `.claude/connectors/<service>/client.py` is the canonical entry. Convention: every client class exposes `from_env()` as the standard constructor and reads its credential from a documented env var.
