#!/usr/bin/env python3
"""Sanitize agents/<agent>/context/ folders — operator brand-name strip.

Scope:
- All .md files under agents/*/context/ (learning-paths/, methodology/, references/)
- Excludes: agents/_template/, .git/, _archive/

The context/ folders are educational reference material — methodology, learning
paths, reference packs. They were copied from PRIMOLABS source and still contain
operator-specific product names that need to become generic placeholders so a
fresh operator forking the repo can fill them in.

Replacements (in order — most-specific first):

Product-context (NEW — only fires in context/ folders):
- "the Stack SaaS" / "the Stack saas" -> "[your product]"
- "the Stack Discord" -> "[your community]"
- "the Stack email list" -> "[your email list]"
- "the Stack pillar" -> "[your product]'s pillar"
- "the Stack pillar pages" -> "[your product]'s pillar pages"
- "the Stack content" -> "[your product] content"
- "the Stack payment" -> "[your product] payment"
- "the the Stack agent" -> "the agent"  (cleanup of pre-existing double-sub)
- "Stage Pro" -> "[your physical/SaaS product]"
- "Savant Playback Discord" -> "[your prior community]"
- "Savant Playback" -> "[your prior product]"
- "Ableton products" / "Ableton product" -> "[your product line]"

Then the existing repo-wide patterns (re-applied for safety):
- "the Stack" (remaining standalone) -> "[your product]"
- "Steven Primo" / "Primo's" / "Primo <verb>" / standalone "Primo" -> "the operator"
- "LMG SI" / "LMG" -> "[your business]"
- "Nashville" -> "[your city]"
- "rook agents" -> "the agents"
- "20-agent line" -> "the agent line"
- "Domotz" -> "[monitoring platform]"
- "Q360" -> "[your CPQ system]"
- "BSA" / "PROMETHEUS" / "COWORK" (when they're operator code-names) -> generic
- "_FROM_CLAUDE" -> "[your reading inbox folder]"

NOT touched:
- Generic terms ("the stack" lowercase referring to tech stack)
- Already-bracketed placeholders ([your business], etc.) — idempotent

Idempotent. Stdlib only.

Usage:
    python scripts/sanitize-context-folders.py            # apply
    python scripts/sanitize-context-folders.py --check    # dry-run
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TARGET_DIR = REPO / "agents"
EXCLUDE_PATHS = ["_archive", ".git", "_template"]


def should_skip(path: Path) -> bool:
    s = str(path).replace("\\", "/")
    return any(f"/{ex}/" in s or s.endswith(f"/{ex}") for ex in EXCLUDE_PATHS)


def sanitize(content: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    def sub(pattern: str, replacement: str, label: str, flags: int = 0):
        nonlocal content
        p = re.compile(pattern, flags)
        matches = p.findall(content)
        n = len(matches)
        if n:
            content = p.sub(replacement, content)
            changes.append(f"{label} (x{n})")

    # --- Product-context (most specific first) ---
    sub(r"\bthe Stack SaaS\b", "[your product]", "'the Stack SaaS' -> '[your product]'", re.IGNORECASE)
    sub(r"\bthe Stack Discord\b", "[your community]", "'the Stack Discord' -> '[your community]'")
    sub(r"\bthe Stack email list\b", "[your email list]", "'the Stack email list' -> '[your email list]'")
    sub(r"\bthe Stack pillar pages\b", "[your product]'s pillar pages", "'the Stack pillar pages' rewrite")
    sub(r"\bthe Stack pillar\b", "[your product]'s pillar", "'the Stack pillar' rewrite")
    sub(r"\bthe Stack content\b", "[your product] content", "'the Stack content' -> '[your product] content'")
    sub(r"\bthe Stack payment\b", "[your product] payment", "'the Stack payment' -> '[your product] payment'")

    # --- Pre-existing breakage cleanup ---
    sub(r"\bthe the Stack\b", "the", "'the the Stack' (double-sub cleanup) -> 'the'")
    sub(r"\bThe the Stack\b", "The", "'The the Stack' (double-sub cleanup) -> 'The'")

    # --- Operator's prior products ---
    sub(r"\bSavant Playback Discord\b", "[your prior community]", "'Savant Playback Discord' rewrite")
    sub(r"\bSavant Playback\b", "[your prior product]", "'Savant Playback' -> '[your prior product]'")
    sub(r"\bStage Pro\b", "[your physical/SaaS product]", "'Stage Pro' rewrite")
    sub(r"\bAbleton products\b", "[your product line]", "'Ableton products' rewrite")
    sub(r"\bAbleton product\b", "[your product]", "'Ableton product' rewrite")

    # --- Remaining standalone "the Stack" ---
    sub(r"\bthe Stack\b", "[your product]", "'the Stack' -> '[your product]'")

    # --- Operator personal/employer references ---
    sub(r"\bSteven Primo\b", "the operator", "'Steven Primo' -> 'the operator'")
    sub(
        r"\bPrimo\s+(says|asks|wants|prefers|requires|locks|mentions|drops|enters|seems|catches|reviews|flags|runs|confirms|lock|owns|builds|wrote|writes|invokes)\b",
        r"the operator \1",
        "'Primo <verb>' rewrite",
    )
    sub(r"\bPrimo[’']s\b", "the operator's", "'Primo's' -> 'the operator's'")
    sub(r"\bPrimo\b(?!Labs)", "the operator", "standalone 'Primo' -> 'the operator'")

    # --- Employer / location ---
    sub(r"\bLMG\s+SI\b", "[your business]", "'LMG SI' -> '[your business]'")
    sub(r"\bLMG\b", "[your business]", "'LMG' -> '[your business]'")
    sub(r"\bNashville\b", "[your city]", "'Nashville' -> '[your city]'")

    # --- Vertical-lock industry refs ---
    sub(r"\bDomotz\b", "[monitoring platform]", "'Domotz' rewrite")
    sub(r"\bQ360\b", "[your CPQ system]", "'Q360' rewrite")

    # --- Internal code-names (only when capitalized + standalone) ---
    sub(r"\bPROMETHEUS\b", "[your sales-ops platform]", "'PROMETHEUS' rewrite")

    # --- Folder convention ---
    sub(r"_FROM_CLAUDE", "[your reading inbox folder]", "'_FROM_CLAUDE' rewrite")

    # --- Agent collective ---
    sub(r"\brook agents\b", "the agents", "'rook agents' rewrite", re.IGNORECASE)
    sub(r"\bthe 20-agent line\b", "the agent line", "'20-agent line' rewrite")

    # --- Vertical-lock: touring AV / Ableton domain examples ---
    # Multi-word phrases first (most specific)
    sub(r"\btouring AV (pros|professionals|practitioners)\b", "[your customer audience]", "'touring AV <plural>' -> '[your customer audience]'")
    sub(r"\btouring AV (industry|labor market|practitioner)\b", "[your customer market]", "'touring AV <market>' -> '[your customer market]'")
    sub(r"\btouring AV\b", "[your customer industry]", "'touring AV' -> '[your customer industry]'")
    sub(r"\btouring engineer\b", "[your customer persona]", "'touring engineer' -> '[your customer persona]'")
    sub(r"\btouring crew\b", "[your customer community]", "'touring crew' -> '[your customer community]'")
    sub(r"\btouring shows\b", "[your customer projects]", "'touring shows' -> '[your customer projects]'")
    sub(r"\btouring rigs\b", "[your customer setups]", "'touring rigs' -> '[your customer setups]'")
    sub(r"\btouring professionals\b", "[your customer audience]", "'touring professionals' -> '[your customer audience]'")
    sub(r"\bplayback software\b", "[your software category]", "'playback software' -> '[your software category]'")
    sub(r"\bplayback foundations\b", "[your domain] foundations", "'playback foundations' rewrite")
    sub(r"\bplayback management\b", "[your domain] management", "'playback management' rewrite")
    sub(r"\blive show playback\b", "[your domain]", "'live show playback' rewrite")
    sub(r"\bMIDI integration for touring rigs\b", "[your domain] integration scenarios", "'MIDI integration for touring rigs' rewrite")
    sub(r"\bMax for Live\b", "[your platform]", "'Max for Live' -> '[your platform]'")
    sub(r"\bLiveAPI\b", "[your platform API]", "'LiveAPI' rewrite")
    sub(r"\bLive API\b", "[your platform API]", "'Live API' rewrite")
    sub(r"\bM4L\b", "[your platform]", "'M4L' -> '[your platform]'")
    sub(r"\bAbleton community\b", "[your community]", "'Ableton community' rewrite")
    sub(r"\bAbleton/\[your physical/SaaS product\]", "[your product line]", "'Ableton/[your physical/SaaS product]' rewrite")
    sub(r"\bAbleton, Software Dev, Product Dev\b", "mission-product depts", "'Ableton, Software Dev, Product Dev' rewrite")
    sub(r"\bAbleton, Software Dev\b", "mission-product depts", "'Ableton, Software Dev' rewrite")
    sub(r"\bAbleton public releases\b", "[your product] public releases", "'Ableton public releases' rewrite")
    sub(r"\bAbleton products?\b", "[your product line]", "remaining 'Ableton product(s)' rewrite")
    # Lone "Ableton" — last because it's broad. Skip "anthropic" / "anthropics" false-positives (none, but be safe)
    sub(r"\bAbleton\b", "[your platform]", "standalone 'Ableton' -> '[your platform]'")

    # --- Exit-path / operator career framing ---
    sub(r"\$100K-net-by-Dec-2026\b", "[your income target]", "'$100K-net-by-Dec-2026' rewrite")
    sub(r"\bby Dec 31, 2026\b", "by [your target date]", "'by Dec 31, 2026' rewrite")
    sub(r"\bon Dec 31, 2026\b", "on [your target date]", "'on Dec 31, 2026' rewrite")
    sub(r"\bthrough Dec 31, 2026\b", "through [your target date]", "'through Dec 31, 2026' rewrite")
    sub(r"\bDec 31, 2026\b", "[your target date]", "'Dec 31, 2026' rewrite")
    sub(r"\bby Dec 2026\b", "by [your target date]", "'by Dec 2026' rewrite")
    sub(r"\bDec 2026\b", "[your target date]", "'Dec 2026' rewrite")
    sub(r"\btarget_dec_2026\b", "target_milestone_date", "'target_dec_2026' var rewrite")
    sub(r"\bexit target date\b", "milestone target date", "'exit target date' rewrite")
    sub(r"\bexit target\b", "milestone target", "'exit target' rewrite")
    sub(r"\bexit date\b", "milestone date", "'exit date' rewrite")
    sub(r"\bexit math\b", "milestone math", "'exit math' rewrite")
    sub(r"\bexit pacing\b", "milestone pacing", "'exit pacing' rewrite")
    sub(r"\bexit doctrine\b", "revenue-mix doctrine", "'exit doctrine' rewrite")
    sub(r"\b4-pillar revenue framework\b", "revenue-pillars framework", "'4-pillar revenue framework' rewrite")
    sub(r"\bABLETON / SOFTWARE DEV\b", "MISSION-PRODUCT DEPTS", "'ABLETON / SOFTWARE DEV' rewrite")
    sub(r"\bABLETON\b", "[YOUR PLATFORM]", "standalone 'ABLETON' rewrite")
    sub(r"\bexit \[your employer\]", "transition off [your employer]", "'exit [your employer]' rewrite")
    sub(r"\bexit-LMG\b", "transition-off-bridge", "'exit-LMG' rewrite")
    sub(r"\b4-pillar doctrine\b", "revenue-pillars doctrine", "'4-pillar doctrine' rewrite")
    sub(r"\bfour-pillar doctrine\b", "revenue-pillars doctrine", "'four-pillar doctrine' rewrite")
    sub(r"\bincome[- ]bridge\b", "bridge-revenue", "'income-bridge'/'income bridge' rewrite", re.IGNORECASE)
    sub(r"\bbridge income\b", "bridge revenue", "'bridge income' rewrite")
    sub(r"\bwarm Discord audience\b", "warm community audience", "'warm Discord audience' rewrite")
    sub(r"\bSavant Discord\b", "[your community Discord]", "'Savant Discord' rewrite")

    return content, changes


def iter_files() -> list[Path]:
    if not TARGET_DIR.exists():
        return []
    # Scope: all .md files under agents/ (SKILL.md, README.md, CLAUDE.md,
    # context/**, methodology gap index, prune-policy.md, etc.)
    files = list(TARGET_DIR.rglob("*.md"))
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
        replacements = sum(
            int(m.group(1)) for c in changes for m in [re.search(r"\(x(\d+)\)", c)] if m
        )
        total_replacements += replacements

        rel = f.relative_to(REPO).as_posix()
        print(f"  {rel}: {replacements} replacements")
        for c in changes:
            print(f"      {c}")

        if not check_only:
            f.write_text(new_content, encoding="utf-8")

    action = "would change" if check_only else "changed"
    print(
        f"\nSummary: {action} {total_changed} files, "
        f"{total_replacements} replacements across {len(files)} files scanned."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
