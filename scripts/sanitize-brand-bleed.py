#!/usr/bin/env python3
"""Sanitize operator-specific brand references in agent SKILL.md files.

Replacements:
- "the Stack ships" -> "this agent ships"
- "the Stack doesn't ship" -> "this agent doesn't ship"
- "the Stack" (other contexts) -> "this system"
- "the 20-agent line" -> "the agent line"
- "rook agents" -> "the agents"
- "Steven Primo" -> "the operator"
- "Primo says/asks/wants/prefers/etc." -> "the operator <verb>"
- "Primo's" -> "the operator's"
- "LMG SI" / "LMG" -> "[your business]"
- "Nashville" -> "[your city]"
- Brand lock table rows referencing operator-specific files -> removed
- Cross-references to project_rook_brand.md / project_primolabs_north_star.md -> removed

NOTE: Leaves "PrimoLabs" alone (product brand stays; only operator-specific
references like file paths get cleaned up via dedicated patterns above).
NOTE: Leaves "ROOK" alone (product name).

Idempotent. Stdlib only. Run with --check for dry-run.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO / "agents"


def sanitize(content: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    # 1. "the Stack ships ..." — most common brand-bleed
    p = re.compile(r"\bthe Stack ships\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("this agent ships", content)
        changes.append(f"'the Stack ships' -> 'this agent ships' (x{n})")

    # 2. "the Stack doesn't ship" (curly + straight apostrophe variants)
    p = re.compile(r"\bthe Stack doesn[’']t ship\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("this agent doesn't ship", content)
        changes.append(f"'the Stack doesn’t ship' rewrite (x{n})")

    # 3. Remaining "the Stack" -> "this system"
    p = re.compile(r"\bthe Stack\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("this system", content)
        changes.append(f"'the Stack' -> 'this system' (x{n})")

    # 4. "the 20-agent line"
    p = re.compile(r"\bthe 20-agent line\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("the agent line", content)
        changes.append(f"'the 20-agent line' -> 'the agent line' (x{n})")

    # 5. "rook agents" (lowercase phrase, NOT ROOK product name)
    p = re.compile(r"\brook agents\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("the agents", content)
        changes.append(f"'rook agents' -> 'the agents' (x{n})")

    # 6. "Steven Primo" -> "the operator"
    p = re.compile(r"\bSteven Primo\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("the operator", content)
        changes.append(f"'Steven Primo' -> 'the operator' (x{n})")

    # 7. "Primo says/asks/wants/etc."
    p = re.compile(r"\bPrimo\s+(says|asks|wants|prefers|requires|locks|mentions|drops|enters|seems|catches|reviews|flags)\b")
    n = len(p.findall(content))
    if n:
        content = p.sub(r"the operator \1", content)
        changes.append(f"'Primo <verb>' -> 'the operator <verb>' (x{n})")

    # 8. "Primo's" -> "the operator's"
    p = re.compile(r"\bPrimo[’']s\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("the operator's", content)
        changes.append(f"'Primo’s' -> 'the operator’s' (x{n})")

    # 9. "LMG SI" -> "[your business]"
    p = re.compile(r"\bLMG\s+SI\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("[your business]", content)
        changes.append(f"'LMG SI' -> '[your business]' (x{n})")

    # 10. "LMG" (standalone) -> "[your business]"
    p = re.compile(r"\bLMG\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("[your business]", content)
        changes.append(f"'LMG' -> '[your business]' (x{n})")

    # 11. "Nashville" -> "[your city]"
    p = re.compile(r"\bNashville\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("[your city]", content)
        changes.append(f"'Nashville' -> '[your city]' (x{n})")

    # 12. Table rows pointing at operator-specific brand-lock files
    p = re.compile(
        r"\n\|[^\n]*Brand lock[^\n]*project_(rook_brand|primolabs_north_star)\.md[^\n]*\|[^\n]*\n"
    )
    n = len(p.findall(content))
    if n:
        content = p.sub("\n", content)
        changes.append(f"removed Brand-lock table row (operator-specific) (x{n})")

    # 13. Cross-reference bullets pointing at operator-specific brand files
    p = re.compile(
        r"\n\s*-[^\n]*project_(rook_brand|primolabs_north_star)\.md[^\n]*\n"
    )
    n = len(p.findall(content))
    if n:
        content = p.sub("\n", content)
        changes.append(f"removed cross-ref to operator-specific brand file (x{n})")

    # 14. Collapse 3+ blank lines.
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content, changes


def main(argv: list[str]) -> int:
    check_only = "--check" in argv

    skill_files = sorted(AGENTS_DIR.glob("*/SKILL.md"))
    total_files_changed = 0
    total_replacements = 0

    for skill in skill_files:
        agent = skill.parent.name
        original = skill.read_text(encoding="utf-8")
        new_content, changes = sanitize(original)

        if not changes:
            continue

        delta_lines = len(original.splitlines()) - len(new_content.splitlines())
        total_files_changed += 1
        # Count total replacements (sum of (xN) numbers in change strings)
        replacements = sum(
            int(m.group(1))
            for c in changes
            for m in [re.search(r"\(x(\d+)\)", c)]
            if m
        )
        total_replacements += replacements

        print(f"  {agent}: -{delta_lines} lines, {replacements} replacements")
        for c in changes:
            print(f"      {c}")

        if not check_only:
            skill.write_text(new_content, encoding="utf-8")

    action = "would change" if check_only else "changed"
    print(f"\nSummary: {action} {total_files_changed} files, {total_replacements} total replacements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
