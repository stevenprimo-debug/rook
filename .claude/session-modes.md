# ROOK Session Modes — Operator vs Customer

Why this exists: the same ROOK vault is run in two materially different contexts.

| Mode | Who runs it | Where their data lives | What ships to cohort |
|---|---|---|---|
| **operator** | The person who built ROOK (the operator) | `memory/operator/`, `context/operator/` | NEVER — excluded from `package-for-cohort.py` |
| **customer** | A cohort member who installed ROOK | `memory/`, `context/` (default paths) | NOT APPLICABLE — they don't ship anything; this is their working vault |

The point: when the operator uses ROOK for their own work, that work accumulates in the same vault that's also the source-of-truth for what ships to cohort. Without segregation, every cohort release requires hand-sanitization to strip the operator's accumulated personal/client data.

## The convention

### Operator-mode writes

When `ROOK_SESSION_MODE=operator` is set in the environment, agents write all session-accumulated content to **subpaths under `operator/`**:

```
agents/<agent>/memory/operator/<file>.md      ← operator's real memory
agents/<agent>/memory/<file>.md               ← template / shipped baseline (empty or example)

agents/<agent>/context/operator/<file>.md     ← operator's real context
agents/<agent>/context/<file>.md              ← shipped reference material
```

### Customer-mode writes (default)

When `ROOK_SESSION_MODE` is unset or `=customer`, agents write to the standard paths:

```
agents/<agent>/memory/<file>.md
agents/<agent>/context/<file>.md
```

A customer's working vault has no `operator/` subfolders — those paths are operator-specific.

### What never travels

`scripts/package-for-cohort.py` excludes:
- `**/memory/operator/**`
- `**/context/operator/**`
- `**/operator-context/**`
- The `ROOK_SESSION_MODE` env var is never written into any file

The cohort zip contains shipped baselines only. The operator's accumulated content stays on the operator's machine.

## How an agent knows which mode it's in

Two lookup paths:

1. **Environment variable:** `ROOK_SESSION_MODE` — set by the operator in their PowerShell profile (`$env:ROOK_SESSION_MODE = "operator"`)
2. **Session context file (fallback):** `.claude/.session_context` — written by `hooks/session-mode-injector.ps1` on SessionStart

If neither is present, default is `customer`. Failing safe means a misconfigured operator session writes to the shipped paths — a contamination risk — so the SessionStart hook surfaces a warning in that case rather than silently defaulting.

## Operator setup

In your PowerShell `$PROFILE`:

```powershell
$env:ROOK_SESSION_MODE = "operator"
```

After that, every new shell session is implicitly operator-mode. The SessionStart hook surfaces the active mode at the top of each ROOK session so it's never a guess.

## Customer setup

Nothing. Default behavior. The hook will surface `mode: customer` and writes flow to standard paths.

## Why not a per-agent flag

Considered: each agent's SKILL.md frontmatter could declare its own mode. Rejected because the SAME agent runs in both modes — the mode is a property of the session, not the agent. One global env var is cleaner than 20 agent-level toggles.

## Why not a separate vault per mode

Considered: the operator could maintain two cloned repos, one for "building ROOK" and one for "using ROOK." Rejected because:
- The operator IS the customer-zero — they need the actual experience of running ROOK against their own work
- Maintaining two repos is a sync nightmare
- The `operator/` subpath convention achieves the same isolation with one repo

## Implications for ops-engineer

`vault-agents/ops-engineer/SKILL.md` already lives in `vault-agents/` (excluded from cohort zip entirely). The `operator/` memory convention is a finer-grained tool: ops-engineer doesn't need it because the whole agent is operator-only. But Tier 1 agents (account-manager, sales-director, finance-manager, etc.) ARE shipped to customers, and THEIR operator-mode memory writes are what need the segregation.

## Failure modes to watch

- **Operator forgets to set the env var** → writes go to shipped paths → contamination at next cohort release. Mitigation: SessionStart hook makes the mode visible at every session start; customer-mode banner in an operator's session is a tell.
- **Agent SKILL.md hardcodes a path that ignores the convention** → operator data leaks into shipped paths. Mitigation: ops-engineer's `contamination-audit` mode scans for this; pre-commit hook (v1.1) would catch it earlier.
- **Cohort zip includes `operator/` paths because exclusion glob is wrong** → P0 leak. Mitigation: `package-for-cohort.py` pre-flight gates include a sanity check that no `operator/` paths are in the manifest.
