#!/usr/bin/env python3
"""Regenerate hooks/routing-rules.json keyword arrays from each agent's SKILL.md.

Source-of-truth split (locked 2026-05-19):

    routing_keywords.primary + .secondary  --> SKILL.md is canonical
        Edit at: agents/<agent>/SKILL.md
                 -> "## Routing Keywords" -> ```yaml fence
                 -> routing_keywords.primary / .secondary

    everything else (excludes, enforce_message, dispatch_chains,
    _global_rules, _documentation)          --> routing-rules.json is canonical
        Edit at: hooks/routing-rules.json (hand-edited)

This script reads each agent's SKILL.md, extracts the primary + secondary
keyword arrays from the routing_keywords yaml block, and writes them into
routing-rules.json's agents.<agent>.primary_keywords / .secondary_keywords.

Idempotent. Safe to run on every commit. Stdlib only.

Usage:
    python scripts/regenerate-routing-rules.py
    python scripts/regenerate-routing-rules.py --check    # exit 1 if drift detected
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO / "agents"
RULES_FILE = REPO / "hooks" / "routing-rules.json"


def extract_keyword_block(skill_md_text: str) -> tuple[list[str], list[str]]:
    """Return (primary, secondary) keyword lists from a SKILL.md body."""
    match = re.search(
        r"^##\s+Routing Keywords[^\n]*\n.*?```yaml\n(.*?)\n```",
        skill_md_text,
        re.DOTALL | re.MULTILINE,
    )
    if not match:
        return [], []
    return _parse_keyword_yaml(match.group(1))


def _parse_keyword_yaml(yaml_body: str) -> tuple[list[str], list[str]]:
    """Focused parser for the routing_keywords block.

    Handles: unquoted items, double-quoted items, single-quoted items,
    inline `#` comments outside quotes. Tracks current section
    (primary / secondary / exclude / other) by key line indentation.
    """
    primary: list[str] = []
    secondary: list[str] = []
    current_list: list[str] | None = None

    for line in yaml_body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Section keys (primary:, secondary:, exclude:) — match anywhere
        # indented; assume routing_keywords is the top-level wrapper.
        if re.match(r"^primary:\s*$", stripped):
            current_list = primary
            continue
        if re.match(r"^secondary:\s*$", stripped):
            current_list = secondary
            continue
        if re.match(r"^(exclude|excludes):\s*$", stripped):
            current_list = None  # We don't mirror excludes — they live in JSON
            continue
        if re.match(r"^routing_keywords:\s*$", stripped):
            current_list = None
            continue
        # List items
        m = re.match(r"^-\s+(.*)$", stripped)
        if not m or current_list is None:
            continue
        item = _clean_item(m.group(1))
        if item:
            current_list.append(item)
    return primary, secondary


def _clean_item(raw: str) -> str:
    """Strip inline comment (only outside quotes), then surrounding quotes."""
    # Strip inline comment
    in_quote: str | None = None
    cut_at: int | None = None
    for i, ch in enumerate(raw):
        if in_quote:
            if ch == in_quote:
                in_quote = None
        elif ch in ('"', "'"):
            in_quote = ch
        elif ch == "#":
            cut_at = i
            break
    if cut_at is not None:
        raw = raw[:cut_at]
    raw = raw.strip()
    # Strip surrounding quotes
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ('"', "'"):
        raw = raw[1:-1]
    return raw


def main(argv: list[str]) -> int:
    check_only = "--check" in argv

    if not RULES_FILE.exists():
        print(f"ERROR: {RULES_FILE} not found", file=sys.stderr)
        return 2

    rules = json.loads(RULES_FILE.read_text(encoding="utf-8"))
    if "agents" not in rules:
        print("ERROR: routing-rules.json missing 'agents' key", file=sys.stderr)
        return 2

    updated: list[str] = []
    missing_skill: list[str] = []
    missing_block: list[str] = []

    for agent_name, agent_block in rules["agents"].items():
        skill_path = AGENTS_DIR / agent_name / "SKILL.md"
        if not skill_path.exists():
            missing_skill.append(agent_name)
            continue
        text = skill_path.read_text(encoding="utf-8")
        primary, secondary = extract_keyword_block(text)
        if not primary and not secondary:
            missing_block.append(agent_name)
            continue
        old_primary = agent_block.get("primary_keywords", [])
        old_secondary = agent_block.get("secondary_keywords", [])
        if old_primary != primary or old_secondary != secondary:
            updated.append(agent_name)
            if not check_only:
                agent_block["primary_keywords"] = primary
                agent_block["secondary_keywords"] = secondary

    # Warnings
    for name in missing_skill:
        print(f"WARN: {name}: no SKILL.md at agents/{name}/SKILL.md — skipped")
    for name in missing_block:
        print(f"WARN: {name}: no `## Routing Keywords` ```yaml block — skipped")

    if check_only:
        if updated:
            print(f"DRIFT: {len(updated)} agent(s) out of sync:")
            for name in updated:
                print(f"  - {name}")
            print(f"\nRun: python scripts/regenerate-routing-rules.py")
            return 1
        print("OK: routing-rules.json keyword arrays match all SKILL.md sources.")
        return 0

    if updated:
        # Preserve trailing newline + 2-space indent to match existing file style
        RULES_FILE.write_text(
            json.dumps(rules, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Updated keyword arrays for {len(updated)} agent(s):")
        for name in updated:
            print(f"  - {name}")
    else:
        print("No changes — routing-rules.json keyword arrays already match all SKILL.md sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
