#!/usr/bin/env python3
"""One-shot sanitizer: strip voice_modes from every agent SKILL.md.

Removes:
1. The `## Voice Modes` H2 section (operational pointer block we just compressed)
2. The `voice_modes: personality/voice_modes/` line in frontmatter inherits
3. The `{voice_mode}` row in Step 2 Parameters table
4. The `voice_mode: {voice_mode}` line in `<parameters>` XML block
5. Knowledge_base reads that target `personality/voice_modes/`

Idempotent. Safe to re-run. Stdlib only.

Usage:
    python scripts/strip-voice-modes.py            # process all 21 SKILL.md files
    python scripts/strip-voice-modes.py --check    # report what would change, no writes
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO / "agents"


def strip(content: str) -> tuple[str, list[str]]:
    """Return (new_content, list_of_changes_applied)."""
    changes = []
    original = content

    # 1. Strip ## Voice Modes H2 section.
    # Match: "## Voice Modes" (with anything after on the heading line)
    # through to the next blank-line + heading-marker (## or ---) OR end of file.
    pattern_section = re.compile(
        r'\n## Voice Modes[^\n]*\n.*?(?=\n## |\n---\n|\Z)',
        re.DOTALL,
    )
    if pattern_section.search(content):
        content = pattern_section.sub('\n', content)
        changes.append("removed '## Voice Modes' section")

    # 2. Strip voice_modes line from inherits block.
    pattern_inherits = re.compile(
        r'\n\s*-\s*voice_modes:[^\n]*\n',
    )
    if pattern_inherits.search(content):
        content = pattern_inherits.sub('\n', content)
        changes.append("removed 'voice_modes:' from inherits block")

    # 3. Strip {voice_mode} parameter table row.
    pattern_table_row = re.compile(
        r'\n\|\s*`?\{voice_mode\}`?\s*\|[^\n]*\n',
    )
    if pattern_table_row.search(content):
        content = pattern_table_row.sub('\n', content)
        changes.append("removed {voice_mode} row from parameters table")

    # 4. Strip voice_mode line from <parameters> XML block.
    pattern_xml_param = re.compile(
        r'\nvoice_mode:\s*\{voice_mode\}\n',
    )
    if pattern_xml_param.search(content):
        content = pattern_xml_param.sub('\n', content)
        changes.append("removed 'voice_mode: {voice_mode}' from <parameters>")

    # 5. Strip knowledge_base READ items targeting voice_modes.
    # Handles "N. READ `personality/voice_modes/<...>.md` ..." and variants.
    pattern_kb_read = re.compile(
        r'\n\d+\.\s+READ[^\n]*voice_modes/[^\n]*\n',
        re.IGNORECASE,
    )
    if pattern_kb_read.search(content):
        content = pattern_kb_read.sub('\n', content)
        changes.append("removed voice_modes READ from <knowledge_base>")

    # 6. Strip Step 1 table rows referencing voice_modes path.
    pattern_step1_row = re.compile(
        r'\n\|[^\n]*personality/voice_modes/[^\n]*\|[^\n]*\n',
    )
    if pattern_step1_row.search(content):
        content = pattern_step1_row.sub('\n', content)
        changes.append("removed voice_modes path row from Step 1 table")

    # 7. Strip bullet-list references in Cross-references/References footer sections.
    pattern_xref_bullet = re.compile(
        r'\n\s*-\s+Voice modes[^\n]*personality/voice_modes/[^\n]*\n',
        re.IGNORECASE,
    )
    if pattern_xref_bullet.search(content):
        content = pattern_xref_bullet.sub('\n', content)
        changes.append("removed Voice-modes cross-reference bullet")

    # 8. Strip First-Run Setup checklist items that probe for voice_modes files.
    pattern_setup_check = re.compile(
        r'\n\s*-\s+\[\s*\][^\n]*personality/voice_modes/[^\n]*\n',
    )
    if pattern_setup_check.search(content):
        content = pattern_setup_check.sub('\n', content)
        changes.append("removed voice_modes First-Run Setup checklist item")

    # 9. Replace inline `voice_modes/<{voice_mode}>.md` references in prose
    # (typically in stage_debate / output sections) with the voice spine reference.
    pattern_inline = re.compile(
        r'`?voice_modes/<\{voice_mode\}>\.md`?',
    )
    if pattern_inline.search(content):
        content = pattern_inline.sub('`.claude/voice-spine.md`', content)
        changes.append("rewrote inline voice_modes refs -> voice-spine.md")

    # 10. Strip standalone "voice_modes/" path references that survived.
    pattern_path = re.compile(
        r'personality/voice_modes/',
    )
    if pattern_path.search(content):
        content = pattern_path.sub('', content)
        changes.append("cleaned residual 'personality/voice_modes/' paths")

    # 11. Collapse 3+ consecutive blank lines down to 2 (cleanup after deletions).
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content, changes


def main(argv: list[str]) -> int:
    check_only = "--check" in argv

    skill_files = sorted(AGENTS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print(f"ERROR: no SKILL.md files found under {AGENTS_DIR}", file=sys.stderr)
        return 2

    total_files_changed = 0
    total_lines_removed = 0

    for skill in skill_files:
        agent = skill.parent.name
        original = skill.read_text(encoding="utf-8")
        new_content, changes = strip(original)

        if not changes:
            print(f"  {agent}: no voice_modes references found — skipped")
            continue

        delta_lines = len(original.splitlines()) - len(new_content.splitlines())
        total_files_changed += 1
        total_lines_removed += delta_lines

        print(f"  {agent}: -{delta_lines} lines | " + " | ".join(changes))

        if not check_only:
            skill.write_text(new_content, encoding="utf-8")

    action = "would change" if check_only else "changed"
    print(f"\nSummary: {action} {total_files_changed} files, removed {total_lines_removed} lines total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
