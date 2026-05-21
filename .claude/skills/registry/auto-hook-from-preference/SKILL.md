---
name: auto-hook-from-preference
description: Convert the operator's spoken preference ("always do X", "every time", "from now on", "never", "remind me to", "before/after Y") into a real harness-enforced rule -- a hook script + settings.json wire-up + memory entry. Closes the drift loop. Memory rules are advisory; this skill produces enforced rules. Trigger when the operator states a recurring preference, OR when the operator says "/auto-hook" or "make this a rule" or "make this a hook" or "always do this".
type: skill
owner: CEO (meta-system)
output: PowerShell hook script + settings.json edit + memory entry
runtime: <2 min Claude execution including 1 user confirm
---

# auto-hook-from-preference

## Why this exists

Built 2026-05-07 after a session where Claude broke 6 protocol rules that had been written to memory for weeks. **Memory rules are advisory — Claude must remember to read and apply them.** When Claude is tired, distracted, or context-switching, memory rules silently fail. The fix is to convert preferences into **harness-level enforcement** — hooks that fire automatically regardless of Claude's state.

The drift gap this closes:

> the operator (week 1): "always check the time before responding"
> Claude: "got it" *(writes memory)*
> the operator (week 4): "why didn't you remind me about 4pm?!"
> Claude: "I forgot to check the memory"

With this skill: the operator says it once → hook ships → harness enforces → drift impossible.

## When to fire

Trigger this skill when ANY of these signals appear:

**Explicit invocation:**
- `/auto-hook` slash command
- "make this a hook"
- "make this a rule"
- "make this automatic"
- "auto-hook this"

**Preference statements (Claude should detect and offer to invoke):**
- "always [do X]"
- "every time [Y happens]"
- "from now on [behavior]"
- "never [do X]"
- "remind me to [Y]"
- "whenever [I do X]"
- "before [responding/replying/anything]"
- "after [tool/action]"
- "when [event]"
- "make sure to always [X]"
- "stop [doing X]"

**When detected but not explicitly invoked:** ASK the operator: *"You said 'always X'. Want me to convert that to a hook so the harness enforces it automatically?"* — then proceed if yes.

## Workflow (4 steps, ~2 min total)

### Step 1: Classify the preference

Use this table to pick the hook event (or non-hook outcome):

| Pattern | Hook event | Notes |
|---|---|---|
| "always include X in the response" / behavioral | **Memory only** (no hook) | Claude reads memory; not enforceable at harness level. Still write the memory. |
| "before responding" / "every prompt I send" | **UserPromptSubmit** | Inject context into prompt. |
| "after every Write/Edit" / "every time you save a file" | **PostToolUse** with matcher | Match tool name. |
| "before running [tool X]" / "always check before [tool]" | **PreToolUse** with matcher | Can block tool. |
| "at session start" / "when I open a session" / "boot" | **SessionStart** | Loads context once per session. |
| "at session end" / "when I close" / "before stopping" | **Stop** | Wraps session. |
| "every Monday at 7am" / "at [time] daily" / cron-like | **Scheduled task** | Use `mcp__scheduled-tasks__create_scheduled_task`, NOT a hook. |
| "remind me at [specific time]" | **Scheduled task** (one-shot) | One-time execution. |
| "every N tool uses" | **PostToolUse** with counter | Stateful — needs file-based counter. |
| "if [condition] then [action]" | **Conditional hook** | Hook script does the conditional check internally. |

**Edge cases:**
- Preference is too vague to classify? Ask the operator ONE clarifying question, then re-classify.
- Preference would conflict with an existing hook? Surface the conflict; offer to merge or replace.
- Preference is purely informational ("from now on call me by my preferred name")? Memory-only, no hook needed.

### Step 2: Draft the artifacts

Three files to draft (some may not apply):

#### A) Hook script (PowerShell, Windows)

Location: `C:\Users\User\.claude\hooks\<descriptive-name>.ps1`

Template structure:

```powershell
# <hook-name>.ps1
# Fires on <event>. Purpose: <one-line>.
# Stdout is <how it's used by Claude Code>.

$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { $data = $null }

# === Hook logic ===
<actual logic here>

# === Output ===
<lines or signal Claude needs>
```

**Critical rules for hook scripts:**
- Use ASCII only. PowerShell 5.1 chokes on em-dashes (—), curly quotes ("), etc. Use `--` and straight quotes.
- Wrap risky operations in try/catch — a hook failure should never crash the harness.
- Set `-NoProfile -NonInteractive` in the settings.json command.
- Keep execution under the timeout (default 10s; configurable).

#### B) settings.json edit

Location: `C:\Users\User\.claude\settings.json` (user-global) or `<project>/.claude/settings.json` (project-scoped).

Default to user-global unless the operator specifies project-scoped.

Schema (matches existing structure):

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<regex or empty>",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -NoProfile -NonInteractive -File \"C:\\Users\\User\\.claude\\hooks\\<name>.ps1\"",
            "timeout": <seconds>
          }
        ]
      }
    ]
  }
}
```

Use `Edit` tool with surgical change — preserve existing hooks, add new entry to the right event array.

#### C) Memory entry

Location: `CLAUDE CODE\MEMORY\feedback_<descriptive>.md`

Even when the hook handles enforcement, write a memory entry so future Claudes understand WHY the hook exists. Use the standard frontmatter:

```yaml
---
name: <Rule name>
description: <one-line>
type: feedback
hook_enforced: true
hook_path: C:\Users\User\.claude\hooks\<name>.ps1
hook_event: <event>
---

# <Title>

<rule statement>

**Why:** <the operator's stated reason or session context>

**How to apply:** <when this triggers>

**Hook enforcement:** This rule is enforced by the harness via `<hook-name>.ps1` on `<event>`. If the hook fails, fall back to manual application of the rule.
```

### Step 3: Show the operator the diff, ask ONE confirm

Format:

```
Converting your preference to a harness-enforced rule.

Preference: "<verbatim the operator quote>"
Classification: <event> hook (or scheduled task / memory-only)

Files I'll create/edit:
  + C:\Users\User\.claude\hooks\<name>.ps1 (NEW, <X> lines)
  ~ C:\Users\User\.claude\settings.json (add <event> entry)
  + PRIMOLABS\CLAUDE CODE\MEMORY\feedback_<name>.md (NEW)

Hook does: <one-sentence behavior>
Fires when: <trigger condition>

Ship it? [y/n]
```

If the operator says yes (or "ship", "go", "do it") → execute Step 4.
If the operator wants changes → adjust and re-show.
If the operator says no → save the preference as memory-only (still write the memory entry — knowledge isn't lost).

### Step 4: Ship

Execute in order:
1. Write hook script (`Write` tool, ASCII only)
2. Test the script runs without errors: `echo '{}' | powershell -NoProfile -NonInteractive -File <path>` — REQUIRED, never skip
3. Edit `settings.json` (`Edit` tool, surgical change)
4. Write memory entry (`Write` tool)
5. Confirm to the operator: "Shipped. Hook fires on next <event>. Memory entry at <path>."

**If the test in step 2 fails:** Fix the script. Don't ship a broken hook.

## Built-in hook script templates

### UserPromptSubmit (inject context)

```powershell
# <name>.ps1 -- UserPromptSubmit hook
$raw = [Console]::In.ReadToEnd()

$lines = @()
$lines += ""
$lines += "===== <BLOCK NAME> ====="
$lines += "<your context here>"
$lines += "===== END ====="
$lines += ""

$lines -join "`n"
```

### PostToolUse (run after specific tools)

```powershell
# <name>.ps1 -- PostToolUse hook
$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { $data = $null }

$tool = if ($data.tool_name) { $data.tool_name } else { "" }
$path = if ($data.tool_input.file_path) { $data.tool_input.file_path } else { "" }

# Your logic here. Examples:
# - Sync to Drive: robocopy ...
# - Validate file: lint check
# - Append to log: Add-Content ...

# Optional: write to stderr if you want Claude to see a warning
# (stdout is silent for PostToolUse unless you signal otherwise)
```

### Stop (session end)

```powershell
# <name>.ps1 -- Stop hook
$raw = [Console]::In.ReadToEnd()
try { $data = $raw | ConvertFrom-Json } catch { $data = $null }

$cwd = if ($data.cwd) { $data.cwd } else { $PWD.Path }
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Your logic here. Examples:
# - Append session marker
# - Run final lint
# - Generate handoff summary
```

### Time-based check (in any UserPromptSubmit hook)

```powershell
$ct = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZone((Get-Date), "Central Standard Time")
$hour = $ct.Hour
$minute = $ct.Minute

if ($hour -ge 16) {
    "*** HARD STOP: $($ct.ToString('h:mm tt')) CT ***"
}
```

## Anti-patterns (DO NOT)

- **DO NOT** ship a hook without testing it (`echo '{}' | powershell ...`). Untested hooks crash the harness.
- **DO NOT** use Unicode (em-dash, curly quotes, etc.) in hook scripts. PowerShell 5.1 parser fails. Stick to ASCII.
- **DO NOT** silently overwrite an existing hook with the same name. Diff and ask.
- **DO NOT** put expensive work in UserPromptSubmit (it adds latency to every prompt). Cap at ~5s.
- **DO NOT** convert a one-off ("remind me Tuesday") into a recurring hook. Use scheduled tasks for one-shots.
- **DO NOT** skip the memory entry just because the hook handles enforcement. The memory entry documents the WHY for future Claudes.
- **DO NOT** classify a preference as "memory-only" if it could be hook-enforced. Default to hook when ambiguous — that's the whole point of this skill.

## Examples (real preferences → real conversions)

### Example 1: "Always remind me about my configured stop time"

Classification: UserPromptSubmit (inject time check on every prompt) + Stop (catch end of response)

Result: hook reads the customer's onboarding-configured stop time and injects warnings at the configured threshold. Customer who didn't configure a stop time = no warnings.

### Example 2: "From now on, every time you Write or Edit a file, sync it to Drive"

Classification: PostToolUse with `matcher: "Write|Edit"`

Result: `sync-memory.ps1` already exists for memory-only; this would extend to all writes.

### Example 3: "Always use ASCII em-dashes in PowerShell scripts because PS 5.1 fails on Unicode"

Classification: Memory-only (Claude must apply this when writing PS).

Result: feedback memory entry, no hook (you can't lint Claude's drafting in real-time at the harness level — yet).

### Example 4: "At every session start, load the recent project files and protocol checks"

Classification: SessionStart (additional wiring of session-prelude.ps1)

Result: New SessionStart entry in settings.json pointing to session-prelude.ps1.

### Example 5: "Remind me to check commission ledger every Monday at 7am"

Classification: Scheduled task (NOT a hook — hooks don't fire on cron-like schedules).

Result: Use `mcp__scheduled-tasks__create_scheduled_task` to create the recurring agent.

## Provenance

Built 2026-05-07 in response to OS audit verdict `production_grade: no`. The audit identified "no say-it-once -> hook converter" as the #1 drift cause. This skill closes that loop. Without it, the product cannot ship to customers — every customer would hit the same drift the operator did. With it, preferences become enforced rules at harness level, regardless of Claude's runtime state.

Owner: CEO (meta-system). Used by: every dept, every session, on every the operator-stated preference.
