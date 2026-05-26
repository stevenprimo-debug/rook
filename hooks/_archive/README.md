# _archive/ — Reference snapshots from prior installs

These scripts shipped in earlier stack snapshots but are NOT part of the v1 hook spec. They reference hard-coded paths to the original source vault and will silent-fail (or no-op) outside that environment.

Kept here for:
1. Historical reference — what the source vault looks like internally.
2. Potential future generalization — two of these are worth porting to v1 if a customer wants the equivalent behavior: `sync-memory` (Drive-sync backup of agent memory writes) and `session-stop` (daily handoff log). The others are either scoped to dead architecture (`drift-linter`, `assignments-stale-check`) or already exist as a v1 portable hook (`vault-context-injector`).

**Not wired by INSTALL.** If you want one of these live, you must port it to the v1 portable pattern (env-var path resolution, ASCII-only, idempotent) and add it to `settings.template.json` manually.

| File | What it actually did | Status |
|---|---|---|
| `drift-linter.ps1` | PreToolUse on Edit/Write/NotebookEdit — logged inferred project context (DEPT / CLIENT / SKILL / HARNESS) to stderr so the agent could self-check for silent context pivots. Never blocked. | Scoped to a v2 `DEPARTMENTS\` layout that no longer exists. Do not port without rewriting from scratch against the v3 `agents/` layout. |
| `sync-memory.ps1` | PostToolUse on Write/Edit — mirrored any `.claude\projects\*\memory\*.md` write to a central Drive-synced `MEMORY\` folder. | Worth porting. Pattern needs to match the v3 `agents\<name>\memory\` layout instead of the old `.claude\projects\` one. |
| `session-stop.ps1` | Stop event — appended a one-line session marker (timestamp + project + path + session ID) to a daily handoff log file. | Worth porting. Only blocker is the hardcoded output path; trivial env-var swap. |
| `assignments-stale-check.ps1` | Stop event — scanned a CEO `assignments/` directory for files untouched > 14 days and appended a "STALE ASSIGNMENTS" block to that day's handoff log. | Scoped to a v2 `DEPARTMENTS\CEO\assignments\` directory that no longer exists. The v3 equivalent (`agents/chief-of-staff/assignments/`) makes this potentially viable, but the script would need a rewrite. |
| `vault-context-injector.ps1` | UserPromptSubmit — keyword-scanned the prompt against a MEMORY index and injected matching memory files into the response context. | **Already exists as a live v1 portable hook** at `hooks/vault-context-injector.ps1` (no underscore prefix). The archived copy is the pre-v1 version with the hardcoded MEMORY path. |
