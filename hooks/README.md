# PrimoLabs Stack — Hooks

Six harness-level hooks that fire automatically once installed. They make the agent stack behave like the v1 spec promises **on first session**, with no copy-paste, no manual wiring, and no "see the docs."

## Quick install

```powershell
# Windows (PowerShell)
cd PrimoLabs_PoweredByClaude
pwsh ./hooks/INSTALL.ps1
```

```bash
# macOS / Linux
cd PrimoLabs_PoweredByClaude
bash ./hooks/INSTALL.sh
```

That's it. `INSTALL` resolves the absolute install path, merges the hook block into `~/.claude/settings.json` (preserving anything else you had there), sets the required env vars, and runs a dry-run on every hook. Re-running is idempotent — no double-wiring.

## What gets wired

| # | Hook | Event | Purpose |
|---|---|---|---|
| 1 | `routing-enforcer` | `UserPromptSubmit` | Reads `routing-rules.json`, matches the prompt against each agent's keyword set, injects matching `enforce_message` so main thread dispatches the right subagent. |
| 2 | `session-prelude` | `SessionStart` | Loads dept/agent context if cwd matches; injects last-24h modified-files list; surfaces protocol checks. |
| 3 | `superpowers-init` | `SessionStart` | Confirms `using-superpowers` skill is invocable; logs the Skill-tool requirement before any response. Falls back gracefully if missing. |
| 4 | `posture-staleness-gate` | `PreToolUse` | Blocks `trading-analyst` tool calls when `agents/trading-analyst/memory/posture*.md` HEAD `last_verified` is older than `PRIMOLABS_POSTURE_STALE_DAYS` (default 7). Defends against stale-posture trade verdicts. |
| 5 | `librarian-digest` | `PostToolUse` | Every N tool calls (`PRIMOLABS_LIBRARIAN_CADENCE`, default 50), appends a scan stub to `agents/librarian/memory/librarian_digest.md` with three sections (Findings / Hooks-created / Hooks-proposed). |
| 6 | `preference-detector` | `UserPromptSubmit` | Pattern-matches spoken preferences ("always do X", "from now on", "never do Y", etc.) and points Claude at the `auto-hook-from-preference` skill so memory rules can be converted to enforced hooks. |
| 7 | `context-watch-gate` | `UserPromptSubmit` | Proactive context-usage monitor. Silent below 70%, prints a visible chat warning between 70-84%, emits a HARD STOP system-reminder at 85% forcing the model to write a structured handoff before responding. Closes the gap that the harness `PreCompact` (fires near 100%) is too late to save in-flight work. |

Both PowerShell (`.ps1`) and Bash (`.sh`) versions ship for every hook. `INSTALL.ps1` wires the `.ps1`s; `INSTALL.sh` wires the `.sh`s.

## Files

```
hooks/
  routing-enforcer.{ps1,sh}
  session-prelude.{ps1,sh}
  superpowers-init.{ps1,sh}
  posture-staleness-gate.{ps1,sh}
  librarian-digest.{ps1,sh}
  preference-detector.{ps1,sh}
  routing-rules.json          <- manifest read by routing-enforcer
  settings.template.json      <- canonical hook block (substituted at install)
  INSTALL.{ps1,sh}            <- one-command installer
  UNINSTALL.{ps1,sh}          <- removes hooks + env vars; preserves other settings
  test/
    run-all.{ps1,sh}          <- dry-run every hook
  README.md                   <- this file
```

## Env vars (set by INSTALL, override by editing settings.json)

| Var | Default | Purpose |
|---|---|---|
| `PRIMOLABS_VAULT_ROOT` | abs path to the stack root | All hooks resolve paths relative to this |
| `PRIMOLABS_HOOKS_DIR` | abs path to `hooks/` | Routing-enforcer + INSTALL use this |
| `PRIMOLABS_POSTURE_STALE_DAYS` | `7` | Stale threshold for posture-gate |
| `PRIMOLABS_LIBRARIAN_CADENCE` | `50` | Tool-call cadence for librarian digest |
| `ROOK_CONTEXT_WARN_PCT` | `70` | context-watch-gate: pct of context window that triggers the visible chat warning |
| `ROOK_CONTEXT_HARDSTOP_PCT` | `85` | context-watch-gate: pct that triggers the HARD STOP handoff-required reminder |
| `ROOK_CONTEXT_WATCH_DISABLED` | unset | context-watch-gate: set to `1` to silence the hook entirely (escape hatch) |
| `CLAUDE_MAX_CONTEXT_TOKENS` | `200000` | context-watch-gate: override the context window size. Auto-promoted to `1000000` if the session model id includes `[1m]`. |

## Verifying the install

After `INSTALL` runs:

1. Start a **new** Claude Code session (existing sessions need a restart).
2. Type any prompt > 3 words. The first response should mention `===== SESSION PRELUDE =====` and `===== SUPERPOWERS INIT =====` in its system reminder context.
3. To explicitly test routing-enforcer, ask a trading question (e.g. "what's the SOXL setup looking like") — the agent should announce a `trading-analyst` dispatch instead of analyzing from main thread.
4. To explicitly test preference-detector, say "from now on always check X" — the agent should offer to convert it to a hook.

To re-run the dry-run suite manually:

```powershell
pwsh ./hooks/test/run-all.ps1
```

Expected output:

```
  [test] routing-enforcer.ps1 OK
  [test] session-prelude.ps1 OK
  [test] superpowers-init.ps1 OK
  [test] posture-staleness-gate.ps1 OK
  [test] librarian-digest.ps1 OK
  [test] preference-detector.ps1 OK

ALL HOOKS PASSED
```

## Disabling a specific hook

Edit `~/.claude/settings.json` and remove the entry for the hook you want disabled. Other hooks keep working. To re-enable, run `INSTALL` again — it re-adds anything missing without duplicating what's already there.

## Uninstalling

```powershell
pwsh ./hooks/UNINSTALL.ps1
# or
bash ./hooks/UNINSTALL.sh
```

Removes PrimoLabs hooks + env vars from `settings.json`. Preserves any other hooks you had. Writes a timestamped backup before changing anything.

## Adding a new hook

Two routes:

1. **Auto-route (preferred):** Say something like *"from now on always do X"* in a session. The `preference-detector` hook fires, points Claude at the `auto-hook-from-preference` skill, which drafts the new hook script + the `settings.json` edit + a memory entry, then asks you to confirm. Once approved, the hook is written to `hooks/generated/<name>.{ps1,sh}` and registered.
2. **Manual route:** Add the script to `hooks/`, then add its command to `settings.template.json` so future `INSTALL` runs pick it up, then run `INSTALL` again.

## Troubleshooting

**Hook produces no output but doesn't crash.** Likely intentional — most hooks silent-pass when their conditions aren't met (routing-enforcer with no keyword match, posture-gate with fresh posture, etc.). Run the dry-run suite to confirm the script doesn't have a parse error.

**`INSTALL` reports `routing-rules.json NOT present`.** The manifest is the source of truth for routing-enforcer. Without it, that hook silent-passes on every prompt. The manifest ships with the stack at `hooks/routing-rules.json`. If it's missing, your distribution is incomplete — re-clone the repo.

**`INSTALL` errors on existing `settings.json`.** The file exists but is invalid JSON. Fix it (or move it aside) and re-run. INSTALL refuses to overwrite a file it can't parse.

**Hooks fire but never produce visible output in the assistant's response.** Claude Code injects hook output as a system reminder, which is invisible by default. Verify with `pwsh ./hooks/test/run-all.ps1` that hooks produce JSON / text. If the dry-run produces output but the agent doesn't change behavior, the issue is upstream of hooks (agent ignoring its instructions).

**PowerShell 5.1 parse errors at session start.** Hooks ship as pure ASCII to avoid 5.1's encoding bugs with em-dashes and smart quotes. If you've edited a hook and added Unicode, replace `—` with `--` and curly quotes with straight quotes.

**Posture gate blocking everything in trading work.** Either your posture file is genuinely stale (re-run `posture_read` mode in trading-analyst), or `PRIMOLABS_POSTURE_STALE_DAYS` is too tight. The default of 7 days is intentional — macro regime moves on roughly that cadence. Increase to 14 if you want a softer gate; never disable in production trading work.

## Why these specific six hooks

Each is a defense against a real failure mode:

1. **routing-enforcer** — main-thread thesis-creep on dept work (Finance verdict from main thread, Design generic-slop without CD upstream, etc.).
2. **session-prelude** — agent starting work without knowing what changed since last session, leading to stale-context output.
3. **superpowers-init** — Claude declining to invoke skills because it didn't know they existed.
4. **posture-staleness-gate** — trade verdicts issued against a 2021 setup in 2026 macro.
5. **librarian-digest** — vault drift accumulating silently because nobody runs the librarian scan on a cadence.
6. **preference-detector** — memory rules being silently advisory; user states a preference, agent acknowledges, then forgets two sessions later.

Memory rules are advisory. Hooks are enforced. These six are the highest-leverage things to enforce at the harness level rather than ask Claude to remember.
