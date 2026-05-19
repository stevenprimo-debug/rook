# _archive/ — Reference snapshots from prior installs

These scripts shipped in earlier stack snapshots but are NOT part of the v1 hook spec. They reference hard-coded paths to Primo's local source vault and will silent-fail (or no-op) outside that environment.

Kept here for:
1. Historical reference — what the source vault looks like internally.
2. Potential future generalization — some of these are good ideas that need to be made portable before promoting back into the active hook set (drift-linter, sync-memory, session-stop).

**Not wired by INSTALL.** If you want one of these live, you must port it to the v1 portable pattern (env-var path resolution, ASCII-only, idempotent) and add it to `settings.template.json` manually.

| File | What it did | Portability blocker |
|---|---|---|
| `drift-linter.ps1` | PreToolUse on Edit/Write — caught off-context edits | Hardcoded vault path |
| `sync-memory.ps1` | PostToolUse — reminded agent to write memory entries | Hardcoded MEMORY/ path |
| `session-stop.ps1` | Stop event — wrap-up protocol | Hardcoded handoff path |
| `assignments-stale-check.ps1` | SessionStart — flagged stale CEO assignments | Hardcoded assignments dir |
| `vault-context-injector.ps1` | UserPromptSubmit — injected vault-level rules | Hardcoded MEMORY/ wikilink scan |
| `hardstop-4pm.ps1` | Stop — extra 4pm reminder | Folded into session-prelude in v1 |
