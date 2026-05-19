#!/usr/bin/env python3
"""Repo-wide sanitization sweep — beyond just SKILL.md files.

Scope:
- All .md / .ps1 / .sh / .py / .json files under .claude/skills/, hooks/, scripts/
- Excludes: .git/, _archive/, .cookbook-tmp/, this script itself, the brand-bleed
  sanitizer script (which has operator names as patterns-to-find, not contamination)

Replacements:
- "the Stack ships ..." -> "this agent ships ..."
- "the Stack" -> "this system"
- "rook agents" -> "the agents"
- "20-agent line" / "the 20-agent line" -> "the agent line"
- "Steven Primo" -> "the operator"
- "Primo says/asks/wants/etc." -> "the operator <verb>"
- "Primo's" -> "the operator's"
- "LMG SI" -> "[your business]"
- "LMG" (standalone) -> "[your business]"
- "Nashville" -> "[your city]"
- "Chloe" / "Silas" -> dropped from docstrings (those are personal family refs)

NOT touching (flag for manual review):
- Hardcoded paths "C:\\Users\\User\\Desktop\\PRIMOLABS\\..." — Python configs need env-var refactor
- "_FROM_CLAUDE/" folder references in AMA templates — operator-specific convention
- routing-rules.json enforce_message updates — JSON content needs careful hand-edit

Idempotent. Stdlib only.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TARGET_DIRS = [REPO / ".claude" / "skills", REPO / "hooks", REPO / "scripts"]
FILE_EXTS = {".md", ".ps1", ".sh", ".py", ".json"}
EXCLUDE_PATHS = [
    "_archive",
    ".git",
    ".cookbook-tmp",
    "sanitize-brand-bleed.py",
    "sanitize-repo-wide.py",
    "sanitize-context-folders.py",
]


def should_skip(path: Path) -> bool:
    s = str(path).replace("\\", "/")
    return any(ex in s for ex in EXCLUDE_PATHS)


def sanitize(content: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    # 1. "the Stack ships ..." (most common)
    p = re.compile(r"\bthe Stack ships\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("this agent ships", content)
        changes.append(f"'the Stack ships' -> 'this agent ships' (x{n})")

    # 2. "the Stack doesn't ship" (curly + straight apostrophe)
    p = re.compile(r"\bthe Stack doesn[’']t ship\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("this agent doesn't ship", content)
        changes.append(f"'the Stack doesn't ship' rewrite (x{n})")

    # 3. Remaining "the Stack" -> "this system"
    p = re.compile(r"\bthe Stack\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("this system", content)
        changes.append(f"'the Stack' -> 'this system' (x{n})")

    # 4. "the 20-agent line" / "20-agent line"
    p = re.compile(r"\bthe 20-agent line\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("the agent line", content)
        changes.append(f"'the 20-agent line' -> 'the agent line' (x{n})")

    # 5. "rook agents" (case-insensitive)
    p = re.compile(r"\brook agents\b", re.IGNORECASE)
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
    p = re.compile(
        r"\bPrimo\s+(says|asks|wants|prefers|requires|locks|mentions|drops|enters|seems|catches|reviews|flags|runs|confirms|lock|owns|builds|wrote|writes|invokes)\b"
    )
    n = len(p.findall(content))
    if n:
        content = p.sub(r"the operator \1", content)
        changes.append(f"'Primo <verb>' -> 'the operator <verb>' (x{n})")

    # 8. "Primo's"
    p = re.compile(r"\bPrimo[’']s\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("the operator's", content)
        changes.append(f"'Primo's' -> 'the operator's' (x{n})")

    # 9. Standalone "Primo" -> "the operator" (word boundary; NOT "PrimoLabs")
    # Negative lookahead for "Labs" to preserve the product brand name.
    p = re.compile(r"\bPrimo\b(?!Labs)")
    n = len(p.findall(content))
    if n:
        content = p.sub("the operator", content)
        changes.append(f"standalone 'Primo' -> 'the operator' (x{n})")

    # 10. "LMG SI"
    p = re.compile(r"\bLMG\s+SI\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("[your business]", content)
        changes.append(f"'LMG SI' -> '[your business]' (x{n})")

    # 11. Standalone "LMG"
    p = re.compile(r"\bLMG\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("[your business]", content)
        changes.append(f"'LMG' -> '[your business]' (x{n})")

    # 12. "Nashville"
    p = re.compile(r"\bNashville\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("[your city]", content)
        changes.append(f"'Nashville' -> '[your city]' (x{n})")

    # 13. "_FROM_CLAUDE" (operator-specific Obsidian inbox folder)
    p = re.compile(r"_FROM_CLAUDE")
    n = len(p.findall(content))
    if n:
        content = p.sub("out", content)
        changes.append(f"'_FROM_CLAUDE' -> 'out' (x{n})")

    # 14. PRIMOLABS-namespaced hardcoded path comments
    p = re.compile(r"\bPRIMOLABS memory system\b")
    n = len(p.findall(content))
    if n:
        content = p.sub("operator memory system", content)
        changes.append(f"'PRIMOLABS memory system' -> 'operator memory system' (x{n})")

    # 15. Vertical-lock: touring AV / Ableton domain examples
    vertical_patterns = [
        (r"\btouring AV (pros|professionals|practitioners)\b", "[your customer audience]"),
        (r"\btouring AV (industry|labor market|practitioner)\b", "[your customer market]"),
        (r"\btouring AV\b", "[your customer industry]"),
        (r"\btouring engineer\b", "[your customer persona]"),
        (r"\btouring crew\b", "[your customer community]"),
        (r"\btouring shows\b", "[your customer projects]"),
        (r"\btouring rigs\b", "[your customer setups]"),
        (r"\btouring professionals\b", "[your customer audience]"),
        (r"\bplayback software\b", "[your software category]"),
        (r"\blive show playback\b", "[your domain]"),
        (r"\bMax for Live\b", "[your platform]"),
        (r"\bLiveAPI\b", "[your platform API]"),
        (r"\bLive API\b", "[your platform API]"),
        (r"\bM4L\b", "[your platform]"),
        (r"\bAbleton community\b", "[your community]"),
        (r"\bAbleton, Software Dev, Product Dev\b", "mission-product depts"),
        (r"\bAbleton, Software Dev\b", "mission-product depts"),
        (r"\bABLETON / SOFTWARE DEV\b", "MISSION-PRODUCT DEPTS"),
        (r"\bAbleton products?\b", "[your product line]"),
        (r"\bAbleton public releases\b", "[your product] public releases"),
        # Lone "Ableton" / "ABLETON" — last (broadest).
        (r"\bABLETON\b", "[YOUR PLATFORM]"),
        (r"\bAbleton\b", "[your platform]"),
    ]
    for pat, repl in vertical_patterns:
        p = re.compile(pat)
        n = len(p.findall(content))
        if n:
            content = p.sub(repl, content)
            changes.append(f"vertical-lock '{pat}' rewrite (x{n})")

    # 16. Exit-path / operator career framing
    exit_patterns = [
        (r"\$100K-net-by-Dec-2026\b", "[your income target]"),
        (r"\bby Dec 31, 2026\b", "by [your target date]"),
        (r"\bon Dec 31, 2026\b", "on [your target date]"),
        (r"\bthrough Dec 31, 2026\b", "through [your target date]"),
        (r"\bDec 31, 2026\b", "[your target date]"),
        (r"\bby Dec 2026\b", "by [your target date]"),
        (r"\bDec 2026\b", "[your target date]"),
        (r"\btarget_dec_2026\b", "target_milestone_date"),
        (r"\bexit target date\b", "milestone target date"),
        (r"\bexit target\b", "milestone target"),
        (r"\bexit date\b", "milestone date"),
        (r"\bexit math\b", "milestone math"),
        (r"\bexit pacing\b", "milestone pacing"),
        (r"\bexit doctrine\b", "revenue-mix doctrine"),
        (r"\bexit-LMG\b", "transition-off-bridge"),
        (r"\b4-pillar revenue framework\b", "revenue-pillars framework"),
        (r"\b4-pillar doctrine\b", "revenue-pillars doctrine"),
        (r"\bfour-pillar doctrine\b", "revenue-pillars doctrine"),
        (r"\bincome-bridge\b", "bridge-revenue"),
        (r"\bincome bridge\b", "bridge revenue"),
        (r"\bbridge income\b", "bridge revenue"),
        (r"\bwarm Discord audience\b", "warm community audience"),
        (r"\bSavant Discord\b", "[your community Discord]"),
    ]
    for pat, repl in exit_patterns:
        p = re.compile(pat)
        n = len(p.findall(content))
        if n:
            content = p.sub(repl, content)
            changes.append(f"exit-framing '{pat}' rewrite (x{n})")

    return content, changes


def iter_files() -> list[Path]:
    files = []
    for d in TARGET_DIRS:
        if not d.exists():
            continue
        for ext in FILE_EXTS:
            files.extend(d.rglob(f"*{ext}"))
    return [f for f in files if not should_skip(f)]


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    files = iter_files()
    total_changed = 0
    total_replacements = 0

    for f in files:
        try:
            original = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        new_content, changes = sanitize(original)
        if not changes:
            continue

        total_changed += 1
        replacements = sum(int(m.group(1)) for c in changes for m in [re.search(r"\(x(\d+)\)", c)] if m)
        total_replacements += replacements

        rel = f.relative_to(REPO).as_posix()
        print(f"  {rel}: {replacements} replacements")
        for c in changes:
            print(f"      {c}")

        if not check_only:
            f.write_text(new_content, encoding="utf-8")

    action = "would change" if check_only else "changed"
    print(f"\nSummary: {action} {total_changed} files, {total_replacements} replacements across {len(files)} files scanned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
