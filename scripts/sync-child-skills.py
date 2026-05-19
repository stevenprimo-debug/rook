#!/usr/bin/env python3
"""Mirror child skills from agents/<agent>/skills/<skill>/ to .claude/skills/<agent>-<skill>/.

Why this exists:
- Anthropic's Claude Code discovers skills at `.claude/skills/<name>/SKILL.md`.
- The agent-with-child-skills folder convention puts skills at
  `agents/<agent>/skills/<skill>/SKILL.md` — readable but NOT auto-discovered.
- This script bridges the two: copies the child SKILL.md + context/ into a
  flattened `.claude/skills/<agent>-<skill>/` namespace so Claude Code sees them.

Naming convention: `<parent-agent>-<child-skill>` so the parent is visible in
the skill name and there's no collision risk across agents.

Mirror, not move. Source-of-truth stays in agents/<agent>/skills/. Re-run after
edits to either rebuild the mirror or to detect drift.

Idempotent. Stdlib only.

Usage:
    python scripts/sync-child-skills.py            # write the mirror
    python scripts/sync-child-skills.py --check    # dry-run; exit 1 if drift
"""
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO / "agents"
CLAUDE_SKILLS_DIR = REPO / ".claude" / "skills"


def find_child_skills() -> list[tuple[str, str, Path]]:
    """Return list of (parent_agent, child_skill, source_path) tuples."""
    found: list[tuple[str, str, Path]] = []
    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        if not agent_dir.is_dir() or agent_dir.name.startswith("_"):
            continue
        skills_dir = agent_dir / "skills"
        if not skills_dir.exists() or not skills_dir.is_dir():
            continue
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
                continue
            if not (skill_dir / "SKILL.md").exists():
                continue
            found.append((agent_dir.name, skill_dir.name, skill_dir))
    return found


def sync_one(parent: str, child: str, source: Path, check_only: bool) -> tuple[bool, str]:
    """Copy source -> .claude/skills/<parent>-<child>/. Return (changed, message)."""
    target_name = f"{parent}-{child}"
    target = CLAUDE_SKILLS_DIR / target_name

    if check_only:
        if not target.exists():
            return True, f"MISSING: {target_name}"
        source_files = {p.relative_to(source) for p in source.rglob("*") if p.is_file()}
        target_files = {p.relative_to(target) for p in target.rglob("*") if p.is_file()}
        if source_files != target_files:
            return True, f"DRIFT (file set differs): {target_name}"
        for rel in source_files:
            sb = (source / rel).read_bytes()
            tb = (target / rel).read_bytes()
            if sb != tb:
                return True, f"DRIFT (content differs in {rel}): {target_name}"
        return False, f"in sync: {target_name}"

    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    return True, f"mirrored: agents/{parent}/skills/{child} -> .claude/skills/{target_name}"


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    CLAUDE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    children = find_child_skills()
    if not children:
        print("No child skills found under agents/*/skills/.")
        return 0

    changed = 0
    for parent, child, source in children:
        is_changed, msg = sync_one(parent, child, source, check_only)
        print(f"  {msg}")
        if is_changed:
            changed += 1

    action = "would mirror" if check_only else "mirrored"
    print(f"\nSummary: {action} {changed} of {len(children)} child skills.")

    if check_only and changed > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
