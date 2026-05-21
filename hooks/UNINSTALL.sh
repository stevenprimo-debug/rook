#!/usr/bin/env bash
# UNINSTALL.sh -- Removes PrimoLabs Stack hooks from ~/.claude/settings.json.

set -u
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SETTINGS_PATH="$CLAUDE_HOME/settings.json"

if [[ ! -f "$SETTINGS_PATH" ]]; then
    echo "[UNINSTALL] No settings.json -- nothing to do."
    exit 0
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "[UNINSTALL] jq required. Install: brew install jq  /  apt install jq"
    exit 2
fi

BACKUP="$SETTINGS_PATH.primolabs-uninstall-$(date +%Y%m%d-%H%M%S)"
cp "$SETTINGS_PATH" "$BACKUP"
echo "  OK    Backup: $BACKUP"

OUR_NAMES=$(jq -n '[
    "routing-enforcer.sh","routing-enforcer.ps1",
    "session-prelude.sh","session-prelude.ps1",
    "superpowers-init.sh","superpowers-init.ps1",
    "posture-staleness-gate.sh","posture-staleness-gate.ps1",
    "librarian-digest.sh","librarian-digest.ps1",
    "preference-detector.sh","preference-detector.ps1",
    "context-watch-gate.sh","context-watch-gate.ps1"
]')

NEW=$(jq --argjson ourNames "$OUR_NAMES" '
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

.hooks = (.hooks // {})
| .hooks.SessionStart     = strip_ours(.hooks.SessionStart)
| .hooks.UserPromptSubmit = strip_ours(.hooks.UserPromptSubmit)
| .hooks.PreToolUse       = strip_ours(.hooks.PreToolUse)
| .hooks.PostToolUse      = strip_ours(.hooks.PostToolUse)
| .hooks.Stop             = strip_ours(.hooks.Stop)
| .env = (.env // {} | del(
    .PRIMOLABS_VAULT_ROOT, .PRIMOLABS_HOOKS_DIR,
  ))
' "$SETTINGS_PATH")

echo "$NEW" | jq . > "$SETTINGS_PATH"
echo "  OK    PrimoLabs hooks + env vars removed"
echo ""
echo "To re-install: bash ./hooks/INSTALL.sh"
exit 0
