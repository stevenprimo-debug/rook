#!/usr/bin/env python3
"""COWORK CORE — self-installer.

Checks and installs all dependencies, creates folder structure,
and walks through one-time configuration. Safe to re-run at any time.

Usage:
    python install.py              # full setup
    python install.py --check      # check status without installing
    python install.py --folders    # create folders only
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

CORE_DIR = Path(__file__).parent
COWORK_ROOT = CORE_DIR.parent
ENV_FILE = CORE_DIR / "inbox_ingestion" / ".env"
ENV_EXAMPLE = CORE_DIR / "inbox_ingestion" / ".env.example"

REQUIRED_PYTHON = (3, 10)

PACKAGES = [
    ("anthropic",              "anthropic>=0.40.0"),
    ("dotenv",                 "python-dotenv>=1.0.0"),
    ("PIL",                    "pillow>=10.0.0"),
    ("yt_dlp",                 "yt-dlp>=2024.1.0"),
    ("faster_whisper",         "faster-whisper>=1.0.0"),
    ("youtube_transcript_api", "youtube-transcript-api>=0.6.0"),
    ("playwright",             "playwright>=1.40.0"),
]

REQUIRED_FOLDERS = [
    COWORK_ROOT / "INBOX" / "clips",
    COWORK_ROOT / "INBOX" / "processed",
    COWORK_ROOT / "INBOX" / "processed_images",
    COWORK_ROOT / "VIDEO",
    COWORK_ROOT / "Clippings",
    COWORK_ROOT / "DEPARTMENTS",
]

SEP = "-" * 60


def header(text: str) -> None:
    print(f"\n{SEP}\n  {text}\n{SEP}")


def ok(msg: str) -> None:
    print(f"  [OK]  {msg}")


def warn(msg: str) -> None:
    print(f"  [!!]  {msg}")


def info(msg: str) -> None:
    print(f"        {msg}")


def check_python() -> bool:
    v = sys.version_info
    if v >= REQUIRED_PYTHON:
        ok(f"Python {v.major}.{v.minor}.{v.micro}")
        return True
    warn(f"Python {v.major}.{v.minor} found — need {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+")
    info("Download from https://python.org/downloads")
    return False


def check_packages(install: bool = False) -> bool:
    all_ok = True
    for import_name, pip_spec in PACKAGES:
        try:
            __import__(import_name)
            ok(import_name)
        except ImportError:
            if install:
                info(f"Installing {pip_spec} ...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", pip_spec, "--quiet"],
                    capture_output=True,
                )
                if result.returncode == 0:
                    ok(f"{import_name} (just installed)")
                else:
                    warn(f"Failed to install {pip_spec}")
                    info(result.stderr.decode()[-300:])
                    all_ok = False
            else:
                warn(f"{import_name} — not installed (run without --check to install)")
                all_ok = False
    return all_ok


def install_playwright_browsers() -> None:
    """Install Chromium for html-to-pdf after playwright package is installed."""
    try:
        import playwright  # noqa: F401
        info("Installing Playwright Chromium browser ...")
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
        )
        if result.returncode == 0:
            ok("Playwright Chromium")
        else:
            warn("Playwright Chromium install had issues — html-to-pdf may not work")
    except ImportError:
        pass


def create_folders() -> None:
    for folder in REQUIRED_FOLDERS:
        folder.mkdir(parents=True, exist_ok=True)
        ok(str(folder.relative_to(COWORK_ROOT)))


def check_env(configure: bool = False) -> bool:
    if ENV_FILE.exists():
        content = ENV_FILE.read_text(encoding="utf-8")
        key = ""
        for line in content.splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
        if key and key != "sk-ant-YOUR_KEY_HERE":
            ok("Anthropic API key configured")
            return True
        else:
            warn(".env exists but ANTHROPIC_API_KEY is not set")

    if not configure:
        info("Run setup to configure your API key")
        return False

    print()
    print("  You need an Anthropic API key to use Claude.")
    print("  Get one at: https://console.anthropic.com/settings/keys")
    print()
    key = input("  Paste your API key (sk-ant-...): ").strip()
    if not key.startswith("sk-"):
        warn("That doesn't look like a valid key — you can update it later in CORE/inbox_ingestion/.env")

    # Detect Google Drive path
    default_drive = _default_drive_path()
    print()
    print(f"  Google Drive path (default: {default_drive})")
    drive = input(f"  Press Enter to use default, or paste your path: ").strip()
    if not drive:
        drive = default_drive

    # Detect vault root
    vault_root = str(COWORK_ROOT)
    print()
    print(f"  Vault root is: {vault_root}")

    env_content = f"""ANTHROPIC_API_KEY={key}
COWORK_ROOT={vault_root}
INBOX_SOURCE_DIR={drive}
INBOX_ENABLE_RESEARCH=1
WHISPER_MODEL_SIZE=small
"""
    ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    ENV_FILE.write_text(env_content, encoding="utf-8")
    ok(".env created")
    return True


def _default_drive_path() -> str:
    system = platform.system()
    if system == "Windows":
        return r"G:\My Drive"
    elif system == "Darwin":
        user = os.environ.get("USER", "user")
        return f"/Users/{user}/Google Drive/My Drive"
    else:
        user = os.environ.get("USER", "user")
        return f"/home/{user}/GoogleDrive"


def verify_api_key() -> bool:
    """Quick test that the API key actually works."""
    try:
        from dotenv import load_dotenv
        load_dotenv(ENV_FILE)
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=5,
            messages=[{"role": "user", "content": "hi"}],
        )
        ok("API key verified — Claude connection works")
        return True
    except Exception as e:
        warn(f"API key test failed: {e}")
        return False


def install_skill() -> None:
    """Copy obsidian-capture SKILL.md to ~/.claude/skills/ so Claude Code picks it up."""
    import shutil

    skill_src = CORE_DIR.parent / "SKILLS" / "obsidian-capture" / "SKILL.md"
    skill_dst_dir = Path.home() / ".claude" / "skills" / "obsidian-capture"

    if not skill_src.exists():
        warn("obsidian-capture SKILL.md not found — skipping skill registration")
        return

    skill_dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill_src, skill_dst_dir / "SKILL.md")
    ok("obsidian-capture skill registered in Claude Code")
    info("Type /capture in any Claude Code session to use it")


def main() -> int:
    parser = argparse.ArgumentParser(description="COWORK CORE installer")
    parser.add_argument("--check",   action="store_true", help="Check status without installing")
    parser.add_argument("--folders", action="store_true", help="Create folders only")
    args = parser.parse_args()

    print("\n  COWORK CORE — Setup\n")

    if args.folders:
        header("Creating folders")
        create_folders()
        return 0

    install = not args.check

    header("Python version")
    if not check_python():
        return 1

    header("Python packages")
    check_packages(install=install)

    if install:
        install_playwright_browsers()
        header("Skill registration")
        install_skill()

    header("Folder structure")
    create_folders()

    header("API key + configuration")
    env_ok = check_env(configure=install)

    if install and env_ok:
        header("Verifying connection")
        verify_api_key()

    header("Summary")
    if install:
        print("\n  Setup complete. Open Claude Code in your vault and type:\n")
        print("    /capture          ← process + organize everything")
        print("    /capture route    ← organize what's already clipped")
        print()
        print("  Web Clipper: install the Obsidian Web Clipper browser extension,")
        print(f"  set vault name to: {COWORK_ROOT.name}")
        print()
    else:
        print("\n  Run without --check to install missing items.\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
