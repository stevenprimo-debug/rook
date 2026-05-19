#!/usr/bin/env python3
"""Package the cohort-shippable subset of ROOK into a clean zip.

What goes IN the cohort zip:
- agents/                          (20 Tier 1 operator agents)
- .claude/agents/                  (handle files)
- .claude/skills/                  (skills + child-skill mirrors)
- .claude/connectors/              (connector configs — but NOT secrets)
- .claude/voice-spine.md           (org-wide voice rules)
- hooks/                           (UserPromptSubmit + SessionEnd hooks; portable)
- scripts/regenerate-*.py          (operator runs these locally)
- scripts/sync-child-skills.py
- scripts/sanitize-*.py            (so cohort can run their own sanitization)
- _CLAUDE.md, MASTER_INDEX.md      (vault-level conventions)
- README.md                        (the install guide)

What stays OUT of the cohort zip:
- vault-agents/                    (Tier 2 — operator-only)
- _archive/                        (historical artifacts; not customer-relevant)
- ~/.claude/credentials/           (operator credentials, never travels)
- **/.env*, **/credentials.json    (already gitignored, but belt + suspenders)
- agents/**/memory/*.db            (operator's runtime state)
- agents/**/memory/.vector-index/  (operator's vector cache)
- graphify-out/, graphify-out-memory/  (operator's graph output)
- .git/                            (zip is a fresh start, not a clone)

Pre-flight gates (all must pass before zip is written):
1. sanitize-repo-wide.py --check  (zero brand-bleed residuals)
2. sanitize-context-folders.py --check
3. regenerate-routing-rules.py --check  (manifest matches SKILL.md ground truth)
4. regenerate-claude-agents.py --check  (handle files match SKILL.md frontmatter)
5. sync-child-skills.py --check  (child-skill mirrors are in sync)

If ANY pre-flight fails, the zip is not produced. The operator sees what
failed and runs the corresponding write-mode regen to fix.

Idempotent. Stdlib only.

Usage:
    python scripts/package-for-cohort.py            # dry-run: show what would ship + run pre-flights
    python scripts/package-for-cohort.py --ship     # produce out/rook-cohort-<DATE>.zip
"""
import shutil
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "out"

INCLUDE_DIRS = [
    "agents",
    ".claude",
    "hooks",
    "scripts",
]

INCLUDE_FILES = [
    "_CLAUDE.md",
    "MASTER_INDEX.md",
    "INSTALL.md",
    "requirements.txt",
    ".gitignore",
]

# Path globs (relative to REPO) that are EXCLUDED even if under an INCLUDE_DIRS
EXCLUDE_GLOBS = [
    "vault-agents",
    "_archive",
    ".git",
    ".gstack",
    "graphify-out",
    "graphify-out-memory",
    "**/__pycache__",
    "**/*.pyc",
    "**/.vector-index",
    "**/*.db",
    "**/*.db-journal",
    "**/*.db-shm",
    "**/*.db-wal",
    "**/.env",
    "**/.env.local",
    "**/.env.production",
    "**/credentials.json",
    "**/secrets.json",
    "**/*.pem",
    "**/*.key",
    "out",  # don't recursively zip output
    # Operator-mode session paths — see .claude/session-modes.md
    "**/memory/operator",
    "**/context/operator",
    "**/operator-context",
    ".claude/.session_context",
    # Third-party dependencies — customer installs at install-time via requirements.txt / go install
    "**/vendor",                               # Go vendor dirs
    "**/site-packages",                        # Python site-packages
    ".claude/skills/core/markitdown",          # markitdown is `pip install markitdown`
    ".claude/skills/core/obsidian-cli",        # obsidian-cli is `go install` or pre-built binary
    "**/node_modules",                         # JS node_modules (defensive — not currently present)
    "**/.venv",                                # Python venvs
    "**/venv",
    "**/.tox",
    "**/.mypy_cache",
    "**/.pytest_cache",
    "**/dist",                                 # build artifacts
    "**/build",
]

# Pre-flight gates — every command must exit 0
PREFLIGHT = [
    ["python", "scripts/sanitize-repo-wide.py", "--check"],
    ["python", "scripts/sanitize-context-folders.py", "--check"],
    ["python", "scripts/regenerate-routing-rules.py", "--check"],
    ["python", "scripts/regenerate-claude-agents.py", "--check"],
    ["python", "scripts/sync-child-skills.py", "--check"],
]


def run_preflight() -> tuple[bool, list[str]]:
    failures: list[str] = []
    for cmd in PREFLIGHT:
        print(f"  running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
        if result.returncode != 0:
            failures.append(f"FAIL: {' '.join(cmd)} (exit {result.returncode})")
            if result.stdout:
                failures.append(f"  stdout: {result.stdout.strip().splitlines()[-3:]}")
            if result.stderr:
                failures.append(f"  stderr: {result.stderr.strip().splitlines()[-3:]}")
    return (not failures), failures


def path_is_excluded(path: Path) -> bool:
    rel = path.relative_to(REPO).as_posix()
    parts = rel.split("/")
    for ex in EXCLUDE_GLOBS:
        if ex.startswith("**/"):
            tail = ex[3:]
            if any(p == tail or p.endswith(tail.lstrip("*")) for p in parts):
                return True
            # Match on suffix
            if rel.endswith(tail.lstrip("*")):
                return True
        else:
            if rel == ex or rel.startswith(ex + "/"):
                return True
    return False


def iter_files_for_zip() -> list[Path]:
    files: list[Path] = []
    for d in INCLUDE_DIRS:
        root = REPO / d
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and not path_is_excluded(p):
                files.append(p)
    for fname in INCLUDE_FILES:
        p = REPO / fname
        if p.exists() and not path_is_excluded(p):
            files.append(p)
    return sorted(files)


def main(argv: list[str]) -> int:
    ship = "--ship" in argv

    print(">>> Pre-flight gates")
    ok, failures = run_preflight()
    if not ok:
        print("\n!! Pre-flight FAILED. Zip not produced.")
        for line in failures:
            print(f"  {line}")
        print("\nFix the failures and re-run. To see what regenerator would write,")
        print("run the corresponding script without --check.")
        return 1
    print("  all pre-flight gates passed.\n")

    files = iter_files_for_zip()

    # P0 sanity-check: zero tolerance for operator-mode paths in the manifest
    leaked = [p for p in files if "/operator/" in p.relative_to(REPO).as_posix() or p.name == ".session_context"]
    if leaked:
        print("\n!! OPERATOR-PATH LEAK DETECTED in manifest. ABORTING.")
        print("The following files would have shipped to cohort but contain operator-mode data:")
        for p in leaked[:20]:
            print(f"  {p.relative_to(REPO).as_posix()}")
        if len(leaked) > 20:
            print(f"  ... and {len(leaked) - 20} more")
        print("\nThis is a P0 contamination bug. Check EXCLUDE_GLOBS — operator paths should be excluded.")
        return 2

    total_bytes = sum(p.stat().st_size for p in files)
    print(f">>> Manifest: {len(files)} files, {total_bytes / 1024:.0f} KB total")

    if not ship:
        print("\n  (dry-run — re-run with --ship to produce the zip)")
        print("\n  Sample of files that would ship (first 20):")
        for p in files[:20]:
            print(f"    {p.relative_to(REPO).as_posix()}")
        if len(files) > 20:
            print(f"    ... and {len(files) - 20} more")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    zip_name = f"rook-cohort-{date.today().isoformat()}.zip"
    zip_path = OUT_DIR / zip_name

    print(f"\n>>> Writing {zip_path.relative_to(REPO).as_posix()}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            arc = p.relative_to(REPO).as_posix()
            zf.write(p, arcname=arc)

    final_size = zip_path.stat().st_size
    print(f"  wrote {len(files)} files, {final_size / 1024:.0f} KB on disk.")
    print(f"\n>>> Cohort zip ready at {zip_path.relative_to(REPO).as_posix()}")
    print("    Hand to the customer with the README install guide.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
