"""
ROOK — Regenerate per-agent graphify subgraphs.

Iterates all 20 agent folders and runs graphify over each agent's memory/
directory. Output lands at agents/<slug>/graphify-out/.

Run:
    python scripts/regenerate-agent-subgraphs.py          # all agents
    python scripts/regenerate-agent-subgraphs.py <slug>   # one agent

Called automatically by librarian weekly sweep, after shared-shelf graphify.
Cost: ~30s per agent × 20 = ~10 min runtime. Disk: ~1-5MB per agent.
"""
import subprocess
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).parents[1]
AGENTS_DIR = VAULT_ROOT / "agents"

SKIP_DIRS = {"_archive", "_template", ".git"}


def regenerate_subgraph(slug: str) -> bool:
    """
    Run graphify over agents/<slug>/memory/ and emit to agents/<slug>/graphify-out/.
    Returns True on success, False on failure.
    """
    agent_dir = AGENTS_DIR / slug
    memory_dir = agent_dir / "memory"
    output_dir = agent_dir / "graphify-out"

    if not memory_dir.exists():
        print(f"  SKIP {slug}: no memory/ directory")
        return True

    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, "-m", "graphify",
        str(memory_dir),
        "--output", str(output_dir),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(VAULT_ROOT),
        )
        if result.returncode == 0:
            print(f"  OK  {slug} → {output_dir.relative_to(VAULT_ROOT)}")
            return True
        else:
            # graphify may not be installed in this env — write a stub so the path exists
            stub = output_dir / "REPORT.md"
            if not stub.exists():
                stub.write_text(
                    f"# {slug} — graphify subgraph\n\n"
                    f"> Auto-generated stub. Run `python -m graphify {memory_dir} "
                    f"--output {output_dir}` to populate.\n\n"
                    f"**Status:** graphify not installed or returned error.\n\n"
                    f"```\n{result.stderr[:500]}\n```\n",
                    encoding="utf-8",
                )
            print(f"  STUB {slug}: graphify error (stub written)")
            return False
    except FileNotFoundError:
        # graphify not installed — write stub
        stub = output_dir / "REPORT.md"
        if not stub.exists():
            stub.write_text(
                f"# {slug} — graphify subgraph\n\n"
                f"> Auto-generated stub. Run `python -m graphify {memory_dir} "
                f"--output {output_dir}` to populate.\n\n"
                f"**Status:** graphify module not found. Install via `pip install graphify` "
                f"or the ROOK requirements.\n",
                encoding="utf-8",
            )
        print(f"  STUB {slug}: graphify not installed (stub written)")
        return False
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT {slug}: graphify took >120s")
        return False


def main():
    if len(sys.argv) > 1:
        # Single agent
        slug = sys.argv[1]
        if not (AGENTS_DIR / slug).exists():
            print(f"ERROR: agents/{slug}/ not found")
            sys.exit(1)
        slugs = [slug]
    else:
        slugs = sorted([
            d.name for d in AGENTS_DIR.iterdir()
            if d.is_dir() and d.name not in SKIP_DIRS and not d.name.startswith("_")
        ])

    print(f"Regenerating subgraphs for {len(slugs)} agent(s)...")
    ok = 0
    fail = 0
    for slug in slugs:
        success = regenerate_subgraph(slug)
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\nDone. {ok} OK, {fail} failed/stubbed.")
    if fail > 0:
        print("Stubbed agents still have graphify-out/REPORT.md for path-existence checks.")


if __name__ == "__main__":
    main()
