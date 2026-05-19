#!/usr/bin/env bash
# INSTALL.sh — PrimoLabs Stack hook installer (macOS / Linux)
# ---------------------------------------------------------------------------
# Usage:  bash ./hooks/INSTALL.sh
#
# Idempotent. Wires 6 hooks into ~/.claude/settings.json, sets env vars,
# dry-runs each hook, reports.
#
# Requires: jq (https://stedolan.github.io/jq/)

set -u

CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
    esac
done

step() { printf "\033[36m[INSTALL]\033[0m %s\n" "$*"; }
ok()   { printf "  \033[32mOK   \033[0m %s\n" "$*"; }
warn() { printf "  \033[33mWARN \033[0m %s\n" "$*"; }
err()  { printf "  \033[31mFAIL \033[0m %s\n" "$*"; }

# ---- jq required ----------------------------------------------------------
if ! command -v jq >/dev/null 2>&1; then
    err "jq is required but not installed. Install with: brew install jq  (mac)  /  apt install jq  (linux)"
    exit 2
fi

# ---- Resolve paths --------------------------------------------------------
HOOKS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_ROOT="$( cd "$HOOKS_DIR/.." && pwd )"

step "Resolving paths"
ok "Hooks dir:  $HOOKS_DIR"
ok "Vault root: $VAULT_ROOT"

mkdir -p "$CLAUDE_HOME"
SETTINGS_PATH="$CLAUDE_HOME/settings.json"

# ---- Verify hooks ---------------------------------------------------------
step "Verifying hook scripts exist"
REQUIRED_HOOKS=(
    "routing-enforcer.sh"
    "session-prelude.sh"
    "superpowers-init.sh"
    "posture-staleness-gate.sh"
    "librarian-digest.sh"
    "preference-detector.sh"
)
MISSING=0
for h in "${REQUIRED_HOOKS[@]}"; do
    if [[ -f "$HOOKS_DIR/$h" ]]; then
        ok "$h"
        chmod +x "$HOOKS_DIR/$h" 2>/dev/null || true
    else
        err "$h NOT FOUND"
        MISSING=$((MISSING + 1))
    fi
done
if [[ "$MISSING" -gt 0 ]]; then
    err "Missing $MISSING hook scripts. Aborting."
    exit 1
fi

# routing-rules.json check
if [[ -f "$HOOKS_DIR/routing-rules.json" ]]; then
    SIZE=$(wc -c < "$HOOKS_DIR/routing-rules.json" | tr -d ' ')
    ok "routing-rules.json present ($SIZE bytes)"
else
    warn "routing-rules.json NOT present — routing-enforcer will silent-pass until manifest exists."
fi

# ---- Build hook command strings ------------------------------------------
build_cmd() { echo "bash \"$HOOKS_DIR/$1\""; }

CMD_ROUTING=$(build_cmd "routing-enforcer.sh")
CMD_PRELUDE=$(build_cmd "session-prelude.sh")
CMD_SUPERPOWERS=$(build_cmd "superpowers-init.sh")
CMD_POSTURE=$(build_cmd "posture-staleness-gate.sh")
CMD_LIBRARIAN=$(build_cmd "librarian-digest.sh")
CMD_PREFERENCE=$(build_cmd "preference-detector.sh")

# ---- Load or initialize settings.json ------------------------------------
step "Reading $SETTINGS_PATH"
if [[ -f "$SETTINGS_PATH" ]]; then
    if ! jq empty "$SETTINGS_PATH" >/dev/null 2>&1; then
        err "settings.json exists but is invalid JSON. Fix or remove it and re-run."
        exit 2
    fi
    ok "Existing settings.json loaded"
    SETTINGS=$(cat "$SETTINGS_PATH")
else
    warn "No settings.json — creating fresh"
    SETTINGS='{}'
fi

# Ensure env + hooks objects exist
SETTINGS=$(echo "$SETTINGS" | jq '
    if (.env // null) == null then .env = {} else . end
    | if (.hooks // null) == null then .hooks = {} else . end
')

# ---- Env vars -------------------------------------------------------------
step "Wiring env vars"

# Path vars always overwrite
SETTINGS=$(echo "$SETTINGS" | jq \
    --arg vr "$VAULT_ROOT" \
    --arg hd "$HOOKS_DIR" \
    '.env.PRIMOLABS_VAULT_ROOT = $vr | .env.PRIMOLABS_HOOKS_DIR = $hd')
ok "PRIMOLABS_VAULT_ROOT = $VAULT_ROOT"
ok "PRIMOLABS_HOOKS_DIR = $HOOKS_DIR"

# Default vars only if missing
set_default() {
    local k="$1" v="$2"
    EXISTING=$(echo "$SETTINGS" | jq -r ".env.$k // empty")
    if [[ -z "$EXISTING" ]]; then
        SETTINGS=$(echo "$SETTINGS" | jq --arg v "$v" ".env.$k = \$v")
        ok "$k = $v (default)"
    else
        ok "$k = $EXISTING (preserved)"
    fi
}
set_default PRIMOLABS_HARDSTOP_HOUR     "16"
set_default PRIMOLABS_HARDSTOP_ENABLED  "1"
set_default PRIMOLABS_HARDSTOP_TZ       "America/Chicago"
set_default PRIMOLABS_POSTURE_STALE_DAYS "7"
set_default PRIMOLABS_LIBRARIAN_CADENCE "50"

# ---- Wire hooks (idempotent) ---------------------------------------------
step "Wiring hooks into settings.json"

# Build jq filter: for each event, remove any of our hooks from existing groups,
# then prepend (or append) our matcher group with our hooks.
# Names to detect as "ours":
OUR_NAMES_JSON=$(printf '%s\n' "${REQUIRED_HOOKS[@]}" | jq -R . | jq -s .)

# Helper: strip our hooks from a settings event array, then append our group
build_event() {
    local event="$1" json="$2"
    shift 2
    # Remaining args: pairs of (cmd, timeout)
    local our_hooks_jq='[]'
    while [[ $# -gt 0 ]]; do
        local cmd="$1" timeout="$2"
        shift 2
        our_hooks_jq=$(jq -n --arg c "$cmd" --argjson t "$timeout" --argjson acc "$our_hooks_jq" \
            '$acc + [{"type":"command","command":$c,"timeout":$t}]')
    done
    local our_group_jq
    our_group_jq=$(jq -n --argjson hooks "$our_hooks_jq" '{"matcher":"","hooks":$hooks}')

    echo "$json" | jq --argjson ourGroup "$our_group_jq" --argjson ourNames "$OUR_NAMES_JSON" --arg evt "$event" '
        .hooks[$evt] = (
            (.hooks[$evt] // [])
            | map(
                .hooks = (.hooks // [] | map(
                    select(
                        ([.command // ""] | first) as $cmd |
                        ($ourNames | any(. as $n | $cmd | contains($n))) | not
                    )
                ))
              )
            | map(select(.hooks | length > 0))
        ) + [$ourGroup] | .hooks[$evt] = .hooks[$evt]
    '
}

# Re-shape using a single jq pipeline for clarity:
SETTINGS=$(echo "$SETTINGS" | jq \
    --argjson ourNames "$OUR_NAMES_JSON" \
    --arg cmdRouting   "$CMD_ROUTING" \
    --arg cmdPrelude   "$CMD_PRELUDE" \
    --arg cmdSp        "$CMD_SUPERPOWERS" \
    --arg cmdPost      "$CMD_POSTURE" \
    --arg cmdLib       "$CMD_LIBRARIAN" \
    --arg cmdPref      "$CMD_PREFERENCE" \
'
def strip_ours($arr):
    ($arr // [])
    | map(
        .hooks = (.hooks // [] | map(
            select(
                (.command // "") as $cmd
                | ($ourNames | any(. as $n | $cmd | contains($n))) | not
            )
        ))
      )
    | map(select((.hooks // []) | length > 0));

.hooks.SessionStart     = strip_ours(.hooks.SessionStart) + [{
    matcher: "", hooks: [
        {type:"command", command:$cmdSp,      timeout:8},
        {type:"command", command:$cmdPrelude, timeout:12}
    ]}]
| .hooks.UserPromptSubmit = strip_ours(.hooks.UserPromptSubmit) + [{
    matcher: "", hooks: [
        {type:"command", command:$cmdRouting, timeout:10},
        {type:"command", command:$cmdPref,    timeout:8}
    ]}]
| .hooks.PreToolUse      = strip_ours(.hooks.PreToolUse) + [{
    matcher: "", hooks: [
        {type:"command", command:$cmdPost, timeout:6}
    ]}]
| .hooks.PostToolUse     = strip_ours(.hooks.PostToolUse) + [{
    matcher: "", hooks: [
        {type:"command", command:$cmdLib, timeout:8}
    ]}]
')

ok "SessionStart :: superpowers-init.sh, session-prelude.sh"
ok "UserPromptSubmit :: routing-enforcer.sh, preference-detector.sh"
ok "PreToolUse :: posture-staleness-gate.sh"
ok "PostToolUse :: librarian-digest.sh"

# ---- Write ----------------------------------------------------------------
step "Writing settings.json"
if [[ "$DRY_RUN" -eq 1 ]]; then
    warn "Dry-run: not writing. Would write:"
    echo "$SETTINGS" | jq .
else
    if [[ -f "$SETTINGS_PATH" ]]; then
        BACKUP="$SETTINGS_PATH.primolabs-backup-$(date +%Y%m%d-%H%M%S)"
        cp "$SETTINGS_PATH" "$BACKUP"
        ok "Backup: $BACKUP"
    fi
    echo "$SETTINGS" | jq . > "$SETTINGS_PATH"
    ok "Wrote $SETTINGS_PATH"
fi

# ---- Dry-run hooks --------------------------------------------------------
step "Dry-run testing hooks"
TEST_DIR="$HOOKS_DIR/test"
if [[ -d "$TEST_DIR" && -f "$TEST_DIR/run-all.sh" ]]; then
    export PRIMOLABS_VAULT_ROOT="$VAULT_ROOT"
    export PRIMOLABS_HOOKS_DIR="$HOOKS_DIR"
    if bash "$TEST_DIR/run-all.sh"; then
        ok "All hooks passed dry-run"
    else
        warn "Some hooks soft-failed in dry-run"
    fi
else
    warn "test/run-all.sh missing — skipping"
fi

# ---- Summary --------------------------------------------------------------
step "Install complete"
echo ""
echo "  Settings:   $SETTINGS_PATH"
echo "  Vault:      $VAULT_ROOT"
echo "  Hooks dir:  $HOOKS_DIR"
echo ""
echo "Next:"
echo "  1. Start a new Claude Code session."
echo "  2. The first prompt triggers SessionStart + UserPromptSubmit hooks."
echo "  3. To disable a hook, edit $SETTINGS_PATH."
echo ""
exit 0
