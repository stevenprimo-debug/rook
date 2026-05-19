#!/usr/bin/env python3
"""Auto-generate .claude/agents/<agent>.md handle files from agents/<agent>/SKILL.md.

For each agent in agents/<agent>/SKILL.md:
- Parse the YAML frontmatter (name, description, tools, model)
- Extract bench-pole principle names from the body
- Extract mode names from <task> block
- Write .claude/agents/<agent>.md with:
    - Anthropic-canonical subagent registration frontmatter
    - Concise body that points at the SKILL.md for deep operational detail

Single source of truth: agents/<agent>/SKILL.md
Mirror: .claude/agents/<agent>.md
Drift never returns — re-run this script after any SKILL.md change.

Idempotent. Stdlib only.

Usage:
    python scripts/regenerate-claude-agents.py            # write the handle files
    python scripts/regenerate-claude-agents.py --check    # dry-run; exit 1 if drift
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO / "agents"
CLAUDE_AGENTS_DIR = REPO / ".claude" / "agents"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_text) from a SKILL.md."""
    # Strip UTF-8 BOM if present
    if text.startswith("﻿"):
        text = text[1:]
    # Normalize CRLF -> LF
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m:
        return {}, text
    fm_text = m.group(1)
    body = m.group(2)

    fields: dict = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([a-z_][a-z0-9_]*):(\s*)(.*?)$", line)
        if not m:
            i += 1
            continue
        key = m.group(1)
        val = m.group(3).strip()

        if val == ">" or val == "|":
            # Folded / literal scalar — collect indented continuation
            continuation: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                if lines[i].strip():
                    continuation.append(lines[i].strip())
                i += 1
            fields[key] = " ".join(continuation).strip()
            continue
        elif val == "":
            # Multi-line list or dict (next lines indented)
            items: list = []
            sub_dict: dict = {}
            i += 1
            while i < len(lines):
                nl = lines[i]
                if nl.startswith("  - "):
                    # Strip inline comment if any
                    item_val = nl[4:].strip()
                    if "#" in item_val:
                        item_val = item_val.split("#", 1)[0].strip()
                    if item_val:
                        items.append(item_val)
                    i += 1
                elif nl.startswith("  ") and ":" in nl and not nl.startswith("    "):
                    # Nested dict entry
                    sm = re.match(r"^  ([a-z_][a-z0-9_]*):(\s*)(.*?)$", nl)
                    if sm:
                        sub_dict[sm.group(1)] = sm.group(3).strip()
                    i += 1
                elif nl.startswith("    "):
                    # Deeper nested — skip (we don't need it)
                    i += 1
                elif nl.strip() == "":
                    i += 1
                else:
                    break
            if items:
                fields[key] = items
            elif sub_dict:
                fields[key] = sub_dict
            continue
        elif val.startswith("[") and val.endswith("]"):
            # Inline list
            fields[key] = [x.strip() for x in val[1:-1].split(",") if x.strip()]
        else:
            # Strip inline comment
            if "#" in val:
                val = val.split("#", 1)[0].strip()
            fields[key] = val
        i += 1

    return fields, body


def extract_bench_poles(body: str) -> list[str]:
    """Pull principle-named poles like 'Vigilance-Pole' from the bench section."""
    m = re.search(
        r"## The 3-Pole Principle Bench[^\n]*\n(.*?)(?=\n## |\n---\n|\Z)",
        body,
        re.DOTALL,
    )
    if not m:
        return []
    section = m.group(1)
    poles = re.findall(r"\*\*([A-Z][a-zA-Z]*-Pole)\*\*", section)
    seen: set = set()
    result: list[str] = []
    for p in poles:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def extract_modes(body: str) -> list[str]:
    """Pull mode names like 'triage' from `### MODE: triage` headings."""
    return re.findall(r"^### MODE:\s*([a-z_-]+)", body, re.MULTILINE)


def normalize_model(model: str) -> str:
    """Normalize model field for Claude Code subagent registration."""
    if not model:
        return "sonnet"
    # e.g., 'claude-sonnet-latest' -> 'sonnet'; 'claude-opus-4-7' -> 'opus'
    m = re.search(r"(opus|sonnet|haiku)", model.lower())
    if m:
        return m.group(1)
    return "sonnet"


def format_tools(tools) -> str:
    """Format tools as inline list for handle frontmatter."""
    if isinstance(tools, list):
        return "[" + ", ".join(t.strip() for t in tools) + "]"
    if isinstance(tools, str):
        return tools
    return "[Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch]"


def generate_handle(agent_slug: str, fm: dict, bench_poles: list[str], modes: list[str]) -> str:
    description = fm.get("description", "")
    # Tighten description — Claude Code reads this to decide when to invoke
    if len(description) > 700:
        # Truncate at sentence boundary
        truncated = description[:700]
        last_dot = truncated.rfind(". ")
        if last_dot > 400:
            description = truncated[: last_dot + 1]
        else:
            description = truncated + "..."

    tools = format_tools(fm.get("tools"))
    model = normalize_model(fm.get("model", ""))

    bench_line = " / ".join(bench_poles[:3]) if bench_poles else "see SKILL.md"
    modes_line = " · ".join(modes) if modes else "see SKILL.md"

    body = f"""---
name: {agent_slug}
description: {description}
tools: {tools}
model: {model}
---

# {agent_slug}

**This is the subagent registration handle. Full operating skill lives at `agents/{agent_slug}/SKILL.md` — STEP 0 of every invocation: load that file before any work.**

## Identity

{description}

## Bench (principles in productive tension)

{bench_line}

Principle-named, not person-named. Originators credited in `agents/{agent_slug}/personality/frameworks_attribution.md`; never invoke by name in output.

## Modes

{modes_line}

Per-mode operational detail (steps, brief schemas, output formats) in the full SKILL.md.

## Operating invariants (always apply)

- **No preamble.** First line of output IS the verdict / artifact / diff.
- **Reversibility gate** fires before any irreversible action (client email, prod push, public post, money). Explicit operator confirm required.
- **Compounding-append** for memory writes — never silent overwrite. Contradictions surface as questions for the operator to lock.
- **Pivot acknowledgment** — when the operator changes topic mid-thread, name the pivot in one line; never silently absorb.
- **Forbidden vocab** (per `.claude/voice-spine.md`): elegant, premium, delightful, magical, deep dive, as an AI, great question, happy to help, let's dive in.

## Reference

- Full skill: `agents/{agent_slug}/SKILL.md`
- Bench detail: `agents/{agent_slug}/personality/_bench.md`
- Memory: `agents/{agent_slug}/memory/`
- Voice spine (org-wide): `.claude/voice-spine.md`

## Success criterion

This agent succeeded when the operator closes the tab and goes outside. Engagement is the failure mode. Tab-closure is the win.

---

*Auto-generated from `agents/{agent_slug}/SKILL.md` by `scripts/regenerate-claude-agents.py`. Do not hand-edit — changes will be overwritten on next regen. To update behavior, edit the SKILL.md.*
"""
    return body


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    CLAUDE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    skill_files: list[Path] = []
    for p in sorted(AGENTS_DIR.glob("*/SKILL.md")):
        # Exclude _template and any underscore-prefixed system folders
        if p.parent.name.startswith("_"):
            continue
        skill_files.append(p)

    regenerated: list[str] = []
    unchanged: list[str] = []
    warnings: list[str] = []

    for skill in skill_files:
        agent_slug = skill.parent.name
        text = skill.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        if not fm:
            warnings.append(f"{agent_slug}: no frontmatter found")
            continue

        bench_poles = extract_bench_poles(body)
        modes = extract_modes(body)
        handle_content = generate_handle(agent_slug, fm, bench_poles, modes)
        handle_path = CLAUDE_AGENTS_DIR / f"{agent_slug}.md"

        existing = handle_path.read_text(encoding="utf-8") if handle_path.exists() else ""
        if existing == handle_content:
            unchanged.append(agent_slug)
            continue

        regenerated.append(f"{agent_slug} (modes={len(modes)}, poles={len(bench_poles)})")

        if not check_only:
            handle_path.write_text(handle_content, encoding="utf-8")

    for w in warnings:
        print(f"  WARN: {w}")

    if regenerated:
        print(f"\nRegenerated {len(regenerated)} handle files:")
        for r in regenerated:
            print(f"  - {r}")

    if unchanged and not regenerated:
        print(f"\nAll {len(unchanged)} handle files already in sync. No changes.")

    action = "would regenerate" if check_only else "regenerated"
    print(f"\nSummary: {action} {len(regenerated)} files, {len(unchanged)} unchanged.")

    if check_only and regenerated:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
