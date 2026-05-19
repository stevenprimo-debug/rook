#!/usr/bin/env python3
"""Final SKILL.md cleanup pass — strip remaining bloat + fix tier dishonesty.

Strip targets:
1. 'Why principles, not people' rationale paragraph (belongs in _bench.md, not in 20 SKILL.md files)
2. '## Universal Stack Capabilities' section (explanatory; content lives in _CLAUDE.md)
3. '## Drift Audit Checklist' section (still in 18 agents — already stripped from 3)
4. '## Master Skill as Skill-Builder' section (15-line meta-explanation; MODE is in <task>)

Tier honesty fix:
5. For 7 agents declaring tier 1/2/3 with no backing files: tier -> 4, declared_tier -> original

NOT stripping:
- The 3-pole bench TABLE (operational, locked)
- 'Tension axis:' line (operational summary of the axis; only multi-line elaborations remain in a few agents)
- Anything in the <role>/<task>/<output> blocks

Idempotent. Stdlib only.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO / "agents"

# Agents with tier dishonesty (declared non-4, no backing files verified)
TIER_DISHONESTY = {
    "finance-manager": 2,
    "sales-director": 2,
    "shopify-agent": 2,
    "trading-analyst": 2,
    "deep-researcher": 1,
    "engineering-lead": 3,
    "librarian": 1,
}


def strip_h2_section(content: str, heading: str) -> tuple[str, int]:
    """Strip an H2 section from 'heading' through the next H2/---/EOF."""
    pattern = re.compile(
        r'\n## ' + re.escape(heading) + r'[^\n]*\n.*?(?=\n## |\n---\n|\Z)',
        re.DOTALL,
    )
    matches = len(pattern.findall(content))
    if matches:
        content = pattern.sub('\n', content)
    return content, matches


def cleanup(content: str, agent_name: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    # 1. Strip 'Why principles, not people' rationale paragraph.
    # Matches the bolded header + the rationale prose until the next blank line + section break.
    p = re.compile(
        r'\n\*\*Why principles, not people:\*\*[^\n]*\n(?:[^\n\*\#][^\n]*\n)*',
    )
    n = len(p.findall(content))
    if n:
        content = p.sub('\n', content)
        changes.append(f"stripped 'Why principles, not people' rationale (x{n})")

    # 2. Strip '## Universal Stack Capabilities' section.
    content, n = strip_h2_section(content, "Universal Stack Capabilities")
    if n:
        changes.append(f"stripped '## Universal Stack Capabilities' section (x{n})")

    # 2b. Also strip 'Universal Stack Capabilities (baked into every agent)' variant.
    content, n = strip_h2_section(content, "Universal Stack Capabilities (baked into every agent)")
    if n:
        changes.append(f"stripped '## Universal Stack Capabilities (baked...)' variant (x{n})")

    # 3. Strip '## Drift Audit Checklist' section.
    content, n = strip_h2_section(content, "Drift Audit Checklist")
    if n:
        changes.append(f"stripped '## Drift Audit Checklist' section (x{n})")

    # 4. Strip '## Master Skill as Skill-Builder' section.
    # The MODE: scaffold_skill is still in <task> — operational invocation pattern.
    # The H2 section is just meta-explanation about the pattern.
    content, n = strip_h2_section(content, "Master Skill as Skill-Builder")
    if n:
        changes.append(f"stripped '## Master Skill as Skill-Builder' section (x{n})")

    content, n = strip_h2_section(content, "Master Skill as Skill-Builder (meta-capability)")
    if n:
        changes.append(f"stripped '## Master Skill as Skill-Builder (meta...)' variant (x{n})")

    # 5. Tier honesty: only for agents in TIER_DISHONESTY map
    if agent_name in TIER_DISHONESTY:
        declared = TIER_DISHONESTY[agent_name]
        # Match `  tier: <N>` line in frontmatter (with optional inline comment)
        p = re.compile(r'(\n  tier: )([123])([ \t]*(?:#[^\n]*)?)\n')
        match = p.search(content)
        if match and int(match.group(2)) == declared:
            replacement = (
                f'\n  tier: 4  # CURRENT — declared_tier={declared} below preserves architectural intent (no backing files yet)\n'
                f'  declared_tier: {declared}\n'
            )
            content = p.sub(replacement, content, count=1)
            changes.append(f"tier honesty: {declared} -> 4 (declared_tier={declared} preserves intent)")

    # 6. Collapse 3+ blank lines down to 2.
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content, changes


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    skill_files = sorted(AGENTS_DIR.glob("*/SKILL.md"))
    total_changed = 0
    total_lines_removed = 0

    for skill in skill_files:
        agent = skill.parent.name
        original = skill.read_text(encoding="utf-8")
        new_content, changes = cleanup(original, agent)

        if not changes:
            continue

        delta = len(original.splitlines()) - len(new_content.splitlines())
        total_changed += 1
        total_lines_removed += delta

        print(f"  {agent}: -{delta} lines | {len(changes)} changes")
        for c in changes:
            print(f"      {c}")

        if not check_only:
            skill.write_text(new_content, encoding="utf-8")

    action = "would change" if check_only else "changed"
    print(f"\nSummary: {action} {total_changed} files, removed {total_lines_removed} lines.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
