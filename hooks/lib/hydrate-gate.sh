#!/usr/bin/env bash
# WebFetch host allowlist gate (fail-closed) — bash thin wrapper.
#
# Usage:
#   hydrate-gate.sh <url> [service-hint]
#   Exit 0 = allowed, 1 = blocked, 2 = malformed input.
#
# Delegates to .claude/connectors/_gate.py so all logic lives in one place.
# This file ONLY locates the repo root + invokes Python.

set -u

URL="${1:-}"
HINT="${2:-}"

if [ -z "$URL" ]; then
  echo "usage: hydrate-gate.sh <url> [service-hint]" >&2
  exit 2
fi

# Locate repo root: walk up from this script until we see .claude/connectors + agents.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CUR="$SCRIPT_DIR"
ROOT=""
for _ in 1 2 3 4 5 6 7 8; do
  if [ -d "$CUR/.claude/connectors" ] && [ -d "$CUR/agents" ]; then
    ROOT="$CUR"
    break
  fi
  PARENT="$(dirname "$CUR")"
  if [ "$PARENT" = "$CUR" ]; then break; fi
  CUR="$PARENT"
done

if [ -z "$ROOT" ]; then
  echo "BLOCK reason=repo-root-not-found" >&2
  exit 1
fi

PY="python"
if ! command -v python >/dev/null 2>&1; then
  if command -v python3 >/dev/null 2>&1; then
    PY="python3"
  else
    echo "BLOCK reason=python-not-on-path" >&2
    exit 1
  fi
fi

"$PY" "$ROOT/.claude/connectors/_gate.py" "$URL" "$HINT"
exit $?
