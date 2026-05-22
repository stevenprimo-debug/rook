---
name: headless
source: https://code.claude.com/docs/en/headless
fetched: 2026-05-22
category: claude-code
rook-relevance: high
---

# Headless / Non-Interactive Mode (`claude -p`)

## What it is

Run Claude Code programmatically via CLI. Same agent loop as interactive mode but for scripts, CI/CD, build pipelines. From June 15 2026, draws from a separate Agent SDK credit on subscription plans.

## Key concepts + config

### Basic
```bash
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

### Bare mode (recommended for CI)
```bash
claude --bare -p "Summarize this file" --allowedTools "Read"
```
Skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory, CLAUDE.md. Reduces startup time. Bash/file-read/file-edit tools available by default. Auth must come from `ANTHROPIC_API_KEY` or `apiKeyHelper` in `--settings`. **Will become default for `-p` in a future release.**

### Bare mode context loaders
| Context | Flag |
|---|---|
| System prompt additions | `--append-system-prompt`, `--append-system-prompt-file` |
| Settings | `--settings <file-or-json>` |
| MCP servers | `--mcp-config <file-or-json>` |
| Custom agents | `--agents <json>` |
| Plugin | `--plugin-dir <path>`, `--plugin-url <url>` |

### Pipe data
```bash
cat build-error.txt | claude -p 'explain root cause' > output.txt
```
**stdin capped at 10MB** (v2.1.128+). Larger inputs: write to file, reference path.

### Output formats
- `text` (default)
- `json` — `{result, session_id, total_cost_usd, ...}` with per-model cost breakdown
- `stream-json` — newline-delimited events (use with `--verbose --include-partial-messages`)

### JSON schema-conformant output
```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```
Structured output lives in `.structured_output` field.

### jq patterns
```bash
# extract text result
claude -p "Summarize" --output-format json | jq -r '.result'
# stream text deltas
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

### Stream events of note

**`system/api_retry`** — fires on retryable errors:
```
{type, subtype: "api_retry", attempt, max_retries, retry_delay_ms, error_status, error, uuid, session_id}
```
`error` values: `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `rate_limit`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `unknown`.

**`system/init`** — first event; includes `plugins[]` (loaded) and `plugin_errors[]` (unsatisfied deps, load failures). Use to fail CI on plugin load issues.

**`system/plugin_install`** — when `CLAUDE_CODE_SYNC_PLUGIN_INSTALL` set:
```
{status: "started"|"installed"|"failed"|"completed", name?, error?, uuid, session_id}
```

### Auto-approve tools
```bash
# Per-tool
claude -p "..." --allowedTools "Bash,Read,Edit"

# Or permission mode (whole session)
claude -p "Apply lint fixes" --permission-mode acceptEdits
# dontAsk = deny anything not in permissions.allow (or read-only set) — locked CI
# acceptEdits = auto-approve writes + mkdir/touch/mv/cp; other shell commands still need allowlist
```

### Permission rule syntax for `--allowedTools`
```bash
--allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```
Space before `*` required for prefix match (`Bash(git diff *)` ≠ `Bash(git diff*)`).

### Built-in commands NOT available
User-invoked skills like `/commit` and built-ins like `/compact` only work in interactive mode. In `-p` describe the task.

### Customize system prompt
```bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```
Also: `--system-prompt` (fully replace), `--append-system-prompt-file`.

### Continue conversations
```bash
claude -p "Review codebase" 
claude -p "Now focus on db queries" --continue       # most recent
# Or capture + resume specific
session_id=$(claude -p "Start review" --output-format json | jq -r '.session_id')
claude -p "Continue review" --resume "$session_id"
```

### Build script integration
```json
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

## ROOK applicability

This is how ROOK runs in CI — sanitization auditor, second-opinion-verify, librarian sweeps. `--bare` is the right default for cohort distribution because it skips local hook/MCP discovery (consistent on every machine). `--json-schema` is how the second-opinion-verify skill can demand structured pass/fail output. `system/init.plugin_errors` is the CI gate to catch when a ROOK-bundled plugin failed to load.

## Cross-references
- [[../agent-sdk/overview]] — Python/TypeScript SDK alternative
- [[settings]] — `--settings`, `apiKeyHelper`
- [[mcp]] — `--mcp-config`
- [[subagents]] — `--agents` JSON shape
