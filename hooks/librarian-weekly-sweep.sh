#!/usr/bin/env bash
# librarian-weekly-sweep.sh
# Trigger: cron, weekly (default: Sunday 23:00 local)
#
# Walks every agent's context/ and memory/, identifies stale files per
# agents/librarian/prune-policy.md, quarantines them to _archive/<YYYY-MM>/pruned/,
# writes librarian-log.md and a Monday digest scaffold.
#
# Complementary to librarian-digest.sh (in-session counter). This is the
# OUT-OF-SESSION cron sweep.
#
# Install: registered by hooks/INSTALL.sh as a crontab entry.
#
# Usage (manual run): bash hooks/librarian-weekly-sweep.sh

set -euo pipefail

# Resolve vault root
VAULT_ROOT="${PRIMOLABS_VAULT_ROOT:-}"
if [ -z "$VAULT_ROOT" ]; then
    VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

if [ ! -d "$VAULT_ROOT/agents" ]; then
    echo "ERROR: $VAULT_ROOT does not look like a ROOK vault (no agents/ folder)." >&2
    exit 2
fi

POLICY_FILE="$VAULT_ROOT/agents/librarian/prune-policy.md"
if [ ! -f "$POLICY_FILE" ]; then
    echo "ERROR: prune-policy.md not found at $POLICY_FILE" >&2
    exit 1
fi

# Parse tuning knobs (simple grep, defaults if missing)
STALE_DAYS=$(grep -oE 'stale_after_days:\s*[0-9]+' "$POLICY_FILE" | grep -oE '[0-9]+' | head -1 || echo 90)
CONTEXT_HANDLING=$(grep -oE 'context_handling:\s*\w+' "$POLICY_FILE" | awk '{print $2}' | head -1 || echo 'keep_recent')
MEMORY_HANDLING=$(grep -oE 'memory_handling:\s*\w+' "$POLICY_FILE" | awk '{print $2}' | head -1 || echo 'same')
MAX_QUARANTINE=$(grep -oE 'max_quarantine_per_sweep:\s*[0-9]+' "$POLICY_FILE" | grep -oE '[0-9]+' | head -1 || echo 100)

TODAY=$(date +%Y-%m-%d)
ARCHIVE_MONTH=$(date +%Y-%m)
ARCHIVE_ROOT="$VAULT_ROOT/_archive/$ARCHIVE_MONTH/pruned"
LOG_FILE="$VAULT_ROOT/agents/librarian/librarian-log.md"
DIGEST_DIR="$VAULT_ROOT/_FROM_CLAUDE"
DIGEST_PATH="$DIGEST_DIR/${TODAY}-librarian-digest.md"

mkdir -p "$ARCHIVE_ROOT" "$DIGEST_DIR"

# Helper: check if file is pinned, contract, or recent
is_protected() {
    local f="$1"
    local base
    base=$(basename "$f")
    case "$base" in
        SKILL.md|CLAUDE.md|README.md) return 0 ;;
    esac
    # Pin check
    if head -20 "$f" 2>/dev/null | grep -qE '^pin:\s*true'; then return 0; fi
    # Recent (under 14 days since creation/modification)
    local mtime
    mtime=$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f" 2>/dev/null || echo 0)
    local now
    now=$(date +%s)
    local age_days=$(( (now - mtime) / 86400 ))
    if [ "$age_days" -lt 14 ]; then return 0; fi
    return 1
}

# Helper: check if file has inbound links anywhere in agents/
has_inbound() {
    local slug="$1"
    grep -rqE "\[\[${slug}\]\]|\(${slug}\.md\)|\(${slug}\)" "$VAULT_ROOT/agents/" 2>/dev/null
}

# Collect candidates
CANDIDATES_FILE=$(mktemp)
trap "rm -f $CANDIDATES_FILE" EXIT

for agent_dir in "$VAULT_ROOT"/agents/*/; do
    agent_name=$(basename "$agent_dir")
    [ "$agent_name" = "_template" ] && continue

    for sub in context memory; do
        walk_root="$agent_dir$sub"
        [ ! -d "$walk_root" ] && continue

        effective_stale="$STALE_DAYS"
        if [ "$sub" = "memory" ] && [ "$MEMORY_HANDLING" = "aggressive" ]; then
            effective_stale=$(( STALE_DAYS / 2 ))
        fi

        find "$walk_root" -type f -name '*.md' | while read -r file; do
            if is_protected "$file"; then continue; fi

            # context_handling: keep_recent → exempt current + last 2 months
            if [ "$sub" = "context" ] && [ "$CONTEXT_HANDLING" = "keep_recent" ]; then
                month_folder=$(basename "$(dirname "$file")")
                if echo "$month_folder" | grep -qE '^[0-9]{4}-[0-9]{2}$'; then
                    folder_epoch=$(date -d "${month_folder}-01" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "${month_folder}-01" +%s 2>/dev/null || echo 0)
                    now_epoch=$(date +%s)
                    age_days=$(( (now_epoch - folder_epoch) / 86400 ))
                    [ "$age_days" -lt 90 ] && continue
                fi
            fi

            mtime=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null || echo 0)
            now=$(date +%s)
            age_days=$(( (now - mtime) / 86400 ))
            [ "$age_days" -lt "$effective_stale" ] && continue

            slug=$(basename "$file" .md)
            if has_inbound "$slug"; then continue; fi

            size=$(stat -c %s "$file" 2>/dev/null || stat -f %z "$file" 2>/dev/null || echo 0)
            reason="stale ${age_days}d, 0 inbound"
            [ "$size" -lt 200 ] && reason="near-empty (${size} bytes)"

            relative="${file#$VAULT_ROOT/}"
            echo "$file|$slug|$reason|$relative" >> "$CANDIDATES_FILE"
        done
    done
done

CANDIDATE_COUNT=$(wc -l < "$CANDIDATES_FILE" | tr -d ' ')
QUARANTINED=0
FLAGGED=0
DIGEST_ENTRIES=""

if [ "$CANDIDATE_COUNT" -gt "$MAX_QUARANTINE" ]; then
    FLAGGED="$CANDIDATE_COUNT"
    DIGEST_ENTRIES="## FLAGGED FOR MANUAL REVIEW (over max_quarantine_per_sweep=$MAX_QUARANTINE)\n\n$CANDIDATE_COUNT files flagged; auto-quarantine skipped. Re-run with higher threshold to override.\n"
    while IFS='|' read -r file slug reason relative; do
        DIGEST_ENTRIES="${DIGEST_ENTRIES}- ${relative} — ${reason}\n"
    done < <(head -20 "$CANDIDATES_FILE")
else
    while IFS='|' read -r file slug reason relative; do
        target="$ARCHIVE_ROOT/${slug}.md"
        mv "$file" "$target" 2>/dev/null || continue
        echo "> archived $TODAY → _archive/$ARCHIVE_MONTH/pruned/${slug}.md" > "$file"
        QUARANTINED=$(( QUARANTINED + 1 ))
        echo "$TODAY | quarantined | $relative | reason: $reason | restore: librarian restore $slug" >> "$LOG_FILE"
        DIGEST_ENTRIES="${DIGEST_ENTRIES}- ${relative} — ${reason}. Restore: \`librarian restore ${slug}\`\n"
    done < "$CANDIDATES_FILE"
fi

# --- Tier 1 vector index rebuild ---
# Walk every agent's SKILL.md, find agents with `tier: 1` in the memory: block,
# rebuild their vector index at agents/<agent>/memory/.vector-index/
TIER1_REBUILT=""
TIER1_FAILED=""

for agent_dir in "$VAULT_ROOT"/agents/*/; do
    agent_name=$(basename "$agent_dir")
    [ "$agent_name" = "_template" ] && continue

    skill_path="${agent_dir}SKILL.md"
    [ ! -f "$skill_path" ] && continue

    # Match `tier: 1` inside the memory: block (look in first ~80 lines of frontmatter)
    if head -80 "$skill_path" | awk '/^memory:/,/^[a-z]/' | grep -qE '^\s+tier:\s*1\b'; then
        index_path="${agent_dir}memory/.vector-index"
        context_dir="${agent_dir}context"
        memory_dir="${agent_dir}memory"

        # Clear existing index, rebuild from scratch
        rm -rf "$index_path" 2>/dev/null
        mkdir -p "$index_path"

        # Invoke graphify (universal-stack tool)
        if command -v graphify >/dev/null 2>&1; then
            if graphify "$context_dir" "$memory_dir" --output "$index_path" --quiet 2>/dev/null; then
                cat > "$index_path/index.meta.json" <<EOF
{
  "rebuilt_at": "$(date '+%Y-%m-%d %H:%M:%S')",
  "sweep_type": "weekly-cron",
  "agent": "$agent_name"
}
EOF
                TIER1_REBUILT="${TIER1_REBUILT}${agent_name} "
            else
                TIER1_FAILED="${TIER1_FAILED}${agent_name} "
            fi
        else
            TIER1_FAILED="${TIER1_FAILED}${agent_name}(no-graphify) "
        fi
    fi
done

if [ -n "$TIER1_REBUILT" ]; then
    echo "$TODAY | vector-index-rebuilt | tier-1 agents: $TIER1_REBUILT" >> "$LOG_FILE"
fi
if [ -n "$TIER1_FAILED" ]; then
    echo "$TODAY | vector-index-FAILED | $TIER1_FAILED" >> "$LOG_FILE"
fi

# Write Monday digest scaffold
HEALTH_NOTE="within threshold"
[ "$FLAGGED" -gt 0 ] && HEALTH_NOTE="⚠️ exceeds threshold"

cat > "$DIGEST_PATH" <<EOF
---
date: $TODAY
sweep_type: weekly-cron
health: $HEALTH_NOTE
quarantined: $QUARANTINED
flagged_for_review: $FLAGGED
---

# Librarian Weekly Digest — $TODAY

## Sweep Summary

- Quarantined: $QUARANTINED files → \`_archive/$ARCHIVE_MONTH/pruned/\`
- Flagged for review: $FLAGGED files

## Quarantines This Sweep

$(echo -e "$DIGEST_ENTRIES")

## Awaiting Librarian Agent

Open the librarian to:
- Read this scaffold and fill in drift narrative
- Surface contradictions in the vault
- Propose hooks for compounding patterns
- Re-rank quarantines by load-bearing-ness

## Restore Instructions

To restore any quarantined file: \`librarian restore <slug>\`
Or manually: move from \`_archive/$ARCHIVE_MONTH/pruned/<slug>.md\` back to its original path.

---

*Generated by \`hooks/librarian-weekly-sweep.sh\`. The librarian agent reads this on next dispatch and fills in the intelligent analysis.*
EOF

echo "weekly sweep complete — $QUARANTINED quarantined, $FLAGGED flagged, digest: $DIGEST_PATH"
exit 0
