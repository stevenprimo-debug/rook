---
name: plan-mode
source: https://code.claude.com/docs/en/permission-modes
fetched: 2026-05-22
category: claude-code
rook-relevance: medium
---

# Plan Mode (Permission Modes)

## What it is

`/en/plan-mode` returns 404 — plan mode is documented under [permission-modes](https://code.claude.com/docs/en/permission-modes). Six modes control whether Claude asks before edits/commands. Cycle with `Shift+Tab` in CLI.

## Key concepts + config

### Six modes
| Mode | What runs without asking | Best for |
|---|---|---|
| `default` | Reads only | Sensitive work |
| `acceptEdits` | Reads + file edits + `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed` (in scope) | Iterating on reviewed code |
| `plan` | Reads only | Exploring before changing |
| `auto` | Everything (with classifier safety) | Long tasks, reduce prompt fatigue |
| `dontAsk` | Only pre-approved tools | Locked-down CI |
| `bypassPermissions` | Everything | Isolated containers/VMs only |

### Set mode
```bash
claude --permission-mode plan
```
```json
{"permissions": {"defaultMode": "acceptEdits"}}
```
Mid-session: `Shift+Tab` to cycle. `auto` and `bypassPermissions` only after opt-in via `--dangerously-skip-permissions` or settings.

### Plan mode specifics
- Reads, runs shell to explore, writes a plan
- Does NOT edit source
- Permission prompts still apply (= default mode)
- Enter via `Shift+Tab` or prefix prompt with `/plan`
- Approve options: auto mode | acceptEdits | review each | keep planning | refine with Ultraplan
- Approval names the session automatically from plan content (unless `--name` or `/rename` set)
- `Ctrl+G` opens plan in default editor
- `showClearContextOnPlanAccept` setting offers to clear context first

### Auto mode requirements
- Plan: All plans
- Admin: Team/Enterprise admin must enable
- Model: Sonnet 4.6+, Opus 4.6+, Opus 4.7. NOT Sonnet 4.5, Opus 4.5, Haiku, claude-3
- Provider: Anthropic API only (NOT Bedrock, Vertex, Foundry)

### Auto mode classifier
- Blocks by default: `curl|bash`, sending sensitive data externally, prod deploys, mass deletion, IAM grants, irreversible destruction, force push to `main`
- Allows by default: local file ops, declared deps install, `.env` read + send to matching API, read-only HTTP
- **Boundaries in conversation** ("don't push", "wait until review") block matching actions — but not stored as rules; re-read from transcript on each check (lost on compaction). For hard guarantees use deny rules.
- Fallback: 3 consecutive blocks OR 20 total → pauses auto, resumes prompts
- In `-p` headless mode, repeated blocks abort session
- Auto drops broad allow rules at entry: `Bash(*)`, `PowerShell(*)`, `Bash(python*)`, package-manager run, `Agent` allow rules. Narrow rules carry over.

### Protected paths (never auto-approved except bypassPermissions)
**Dirs**: `.git`, `.vscode`, `.idea`, `.husky`, `.claude` (except `.claude/commands`, `.claude/agents`, `.claude/skills`, `.claude/worktrees`)
**Files**: `.gitconfig`, `.gitmodules`, `.bashrc`, `.bash_profile`, `.zshrc`, `.zprofile`, `.profile`, `.ripgreprc`, `.mcp.json`, `.claude.json`

### dontAsk
Auto-denies every prompt-requiring call. Only `permissions.allow` rules and read-only Bash commands execute. Explicit `ask` rules → deny. Fully non-interactive.

### bypassPermissions
- Equivalent to `--dangerously-skip-permissions`
- v2.1.126+: also disables protected-path checks
- `rm -rf /` and `rm -rf ~` still prompt as circuit breaker
- Refuses to start as root/sudo on Linux/macOS (unless sandboxed)
- Disable via managed `permissions.disableBypassPermissionsMode: "disable"`

## ROOK applicability

`dontAsk` is the right mode for ROOK headless agents in CI (sanitization auditor, librarian sweep). `acceptEdits` is the working default for chief-of-staff in interactive mode. Auto mode requires Anthropic API + recent model — won't work for ROOK on Bedrock/Vertex. Protected-paths list is what ROOK's hooks shouldn't try to override. Boundary-in-conversation behavior is a footgun for ROOK rules — codify everything via deny rules and hooks, not voice instructions.

## Cross-references
- [[settings]] — `permissions.defaultMode`, `permissions.allow|deny`
- [[hooks]] — `PreToolUse` / `PermissionRequest` hooks for custom logic
- [[headless]] — `-p` + permission-mode interplay
