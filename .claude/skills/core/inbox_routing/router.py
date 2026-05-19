"""Route markdown captures to dept context/ folders based on keyword matches.

Sources scanned: INBOX/processed/, INBOX/clips/, Clippings/
Targets: DEPARTMENTS/<dept>/context/YYYY-MM/<file>.md (primary)
         DEPARTMENTS/<secondary>/context/YYYY-MM/<file>.md (cross-ref stubs)
         DEPARTMENTS/CEO/context/YYYY-MM/<file>.md (always — CEO sees everything routed)

Routing rules:
- File already has `dept_routed:` frontmatter → respect existing primary, recompute secondaries.
- Score = count of case-insensitive keyword hits in (filename + frontmatter tags + body).
- Primary = highest-scoring dept (ties → alphabetical).
- Secondary = any dept with score >= SECONDARY_MIN_HITS AND >= SECONDARY_MIN_RATIO of primary score, excluding primary.
- All scores == 0 → leave in place, log WARN.

Keyword source resolution (per dept), in priority order:
1. `DEPARTMENTS/<dept>/skills/<dept-master>/SKILL.md` — `## Routing Keywords` block w/ ```yaml fence
   (single source of truth — supports primary/secondary/exclude lists AND `imports:` field)
2. Fallback: `DEPARTMENTS/<dept>/memory/capture_routing_keywords.md` (legacy mirror)

After every successful SKILL.md read, the resolved (post-import) keyword list is written back
to `memory/capture_routing_keywords.md` as a backup mirror — supports manual override scenarios
and gives a stable on-disk record of what the router actually used.

Shared keyword packs live at `SKILLS/_shared_keyword_packs/<name>.yaml`. A SKILL.md can declare
`imports: [pack-name, pack-name2]` inside its routing_keywords block to inherit. Pack keywords
are flattened (all categories merged) and merged into the dept's `primary` list (treated as
strong-signal vocabulary). Excludes from packs are NOT inherited — each dept owns its excludes.

CHANGELOG:
- 2026-05-06: refactored to read from SKILL.md directly + shared keyword pack imports.
              Auto-mirrors resolved keywords to memory/capture_routing_keywords.md. Backwards
              compatible: depts without SKILL.md routing_keywords block still load via mirror.
"""

from __future__ import annotations

import logging
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

COWORK_ROOT = Path(__file__).parent.parent.parent
DEPARTMENTS_DIR = COWORK_ROOT / "DEPARTMENTS"
SHARED_PACKS_DIR = COWORK_ROOT / "SKILLS" / "_shared_keyword_packs"

DEFAULT_SOURCE_DIRS = [
    COWORK_ROOT / "INBOX" / "processed",
    COWORK_ROOT / "INBOX" / "clips",
    COWORK_ROOT / "Clippings",
]

SECONDARY_MIN_HITS = 4
SECONDARY_MIN_RATIO = 0.50
CEO_DEPT_NAME = "CEO"
WRITE_CEO_STUBS = False  # CEO sees routing via tags + INDEX.md, not stubs — keeps file count down


@dataclass
class DeptRule:
    name: str
    keywords: list[str]
    keywords_path: Path  # source file the rules were loaded from (SKILL.md or mirror)

    @property
    def context_dir(self) -> Path:
        return DEPARTMENTS_DIR / self.name / "context"


@dataclass
class RouteDecision:
    file: Path
    primary: str | None
    secondaries: list[str]
    scores: dict[str, int]


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Minimal YAML parser — only handles flat scalars and lists."""
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    fm_block = text[4:end]
    body = text[end + 5:]

    fm: dict = {}
    current_list_key: str | None = None
    for raw_line in fm_block.splitlines():
        if not raw_line.strip():
            current_list_key = None
            continue
        if raw_line.startswith("  - ") and current_list_key:
            fm[current_list_key].append(raw_line[4:].strip().strip('"').strip("'"))
            continue
        if ":" in raw_line and not raw_line.startswith(" "):
            key, _, val = raw_line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                fm[key] = []
                current_list_key = key
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                fm[key] = [s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()]
                current_list_key = None
            else:
                fm[key] = val.strip('"').strip("'")
                current_list_key = None
        else:
            current_list_key = None
    return fm, body


# ---------------------------------------------------------------------------
# Shared keyword pack loading
# ---------------------------------------------------------------------------

def _load_shared_pack(pack_name: str, packs_dir: Path | None = None) -> list[str]:
    """Load a shared keyword pack from SKILLS/_shared_keyword_packs/<name>.yaml.

    Pack format:
        keywords:
          category_a:
            - kw1
            - kw2
          category_b:
            - kw3

    Returns flattened list of all keywords across all categories. Returns [] if missing.
    `packs_dir` defaults to the module-level SHARED_PACKS_DIR (looked up dynamically
    so tests can monkeypatch it).
    """
    if packs_dir is None:
        # Read from module globals so tests can monkeypatch SHARED_PACKS_DIR
        import inbox_routing.router as _self
        packs_dir = _self.SHARED_PACKS_DIR
    pack_path = packs_dir / f"{pack_name}.yaml"
    if not pack_path.exists():
        logger.warning("Shared keyword pack not found: %s", pack_path)
        return []
    try:
        text = pack_path.read_text(encoding="utf-8")
    except OSError as e:
        logger.warning("Failed reading shared keyword pack %s: %s", pack_path, e)
        return []

    # Minimal YAML parse for the keywords: section. Each category is a 2-space indented key
    # with a list of "    - value" items beneath it. We accept any nesting under `keywords:`.
    keywords: list[str] = []
    in_keywords = False
    keywords_indent = -1
    for raw in text.splitlines():
        # Skip comments / blank lines
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.lstrip()
        indent = len(raw) - len(stripped)

        if not in_keywords:
            if stripped.startswith("keywords:"):
                in_keywords = True
                keywords_indent = indent
            continue

        # We're inside the keywords: block. Exit when we dedent past it.
        if indent <= keywords_indent and not stripped.startswith("-"):
            in_keywords = False
            continue

        # List item — collect its value
        if stripped.startswith("- "):
            val = stripped[2:].strip().strip('"').strip("'")
            if val:
                keywords.append(val)

    return keywords


# ---------------------------------------------------------------------------
# Keyword extraction from SKILL.md
# ---------------------------------------------------------------------------

_ROUTING_KW_BLOCK_RE = re.compile(
    r"##\s+Routing\s+Keywords[^\n]*\n+```ya?ml\s*\n(?P<body>.*?)\n```",
    re.IGNORECASE | re.DOTALL,
)


def _parse_routing_keywords_yaml(yaml_body: str) -> dict:
    """Parse the YAML body found inside the SKILL.md ## Routing Keywords ```yaml fence.

    Returns dict with keys: primary (list[str]), secondary (list[str]), exclude (list[str]),
    imports (list[str]). Missing keys default to [].

    Recognized shapes (exactly the conventions used across SKILL.md files):
        routing_keywords:
          imports: [media-domain]
          primary:
            - foo
            - bar
          secondary:
            - baz
          exclude:
            - quux

    Tolerates:
    - inline list form `imports: [a, b]`
    - quoted scalars `- "ableton link"`
    - inline comments after the value (`- foo  # note`)
    - any indentation depth as long as nested-list items are indented further than their parent key
    """
    result: dict[str, list[str]] = {"primary": [], "secondary": [], "exclude": [], "imports": []}

    # Track current key path. We only care about top-level routing_keywords children.
    current_key: str | None = None
    parent_indent = -1  # indent of the routing_keywords: line
    key_indent = -1     # indent of the current_key (e.g., primary:)

    for raw in yaml_body.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.lstrip()
        indent = len(raw) - len(stripped)

        # Detect routing_keywords: header (top-level of this YAML block)
        if stripped.startswith("routing_keywords:"):
            parent_indent = indent
            current_key = None
            continue

        # Direct children of routing_keywords (primary:, secondary:, exclude:, imports:)
        if parent_indent >= 0 and indent == parent_indent + 2 and ":" in stripped and not stripped.startswith("-"):
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = _strip_inline_comment(val.strip())
            if key in result:
                current_key = key
                key_indent = indent
                # Inline list form: imports: [a, b]
                if val.startswith("[") and val.endswith("]"):
                    inner = val[1:-1]
                    items = [s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()]
                    items = [_strip_inline_comment(it) for it in items if it]
                    result[key] = [it for it in items if it]
                    current_key = None  # inline form is self-contained
            else:
                current_key = None
            continue

        # List items under the current key
        if current_key and stripped.startswith("- ") and indent > key_indent:
            val = stripped[2:].strip()
            val = _strip_inline_comment(val)
            val = val.strip().strip('"').strip("'")
            if val:
                result[current_key].append(val)
            continue

        # Anything else at top-level resets current key tracking
        if indent <= parent_indent and parent_indent >= 0:
            # we've left routing_keywords entirely
            break

    return result


def _strip_inline_comment(s: str) -> str:
    """Strip a `  # comment` tail from a YAML scalar value while preserving #-in-strings.

    Heuristic: split on `  #` (two spaces + #) — this is the YAML convention for inline comments.
    """
    idx = s.find("  #")
    if idx >= 0:
        s = s[:idx]
    # Also handle `# ` at start (rare; defensive)
    if s.lstrip().startswith("#"):
        return ""
    return s.rstrip()


def _find_skill_md(dept_dir: Path) -> Path | None:
    """Find the canonical dept SKILL.md.

    Convention: DEPARTMENTS/<dept>/skills/<some-master>/SKILL.md
    If multiple skills folders exist, prefer one named `*-master`. Fall back to the first found.
    """
    skills_dir = dept_dir / "skills"
    if not skills_dir.exists():
        return None
    # Prefer master skills (resolume-master, ableton-master, etc.)
    master_candidates = sorted(skills_dir.glob("*master*/SKILL.md"))
    if master_candidates:
        return master_candidates[0]
    # Fall back to any SKILL.md one level down
    any_skill = sorted(skills_dir.glob("*/SKILL.md"))
    if any_skill:
        return any_skill[0]
    return None


def _resolve_keywords_from_skill_md(skill_md: Path) -> list[str] | None:
    """Read `## Routing Keywords` ```yaml block from SKILL.md, resolve imports, return flat list.

    Returns None if the block isn't present (caller should fall back to mirror).
    """
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError as e:
        logger.warning("Failed reading SKILL.md %s: %s", skill_md, e)
        return None

    m = _ROUTING_KW_BLOCK_RE.search(text)
    if not m:
        return None

    parsed = _parse_routing_keywords_yaml(m.group("body"))

    # Resolve imports — flatten each shared pack into the primary list
    imported: list[str] = []
    for pack_name in parsed.get("imports", []):
        pack_kws = _load_shared_pack(pack_name)
        imported.extend(pack_kws)

    # Final flat list = primary + imported + secondary. Dedupe preserving order.
    flat: list[str] = []
    seen: set[str] = set()
    for kw in list(parsed.get("primary", [])) + imported + list(parsed.get("secondary", [])):
        kw_lc = kw.lower().strip()
        if kw_lc and kw_lc not in seen:
            seen.add(kw_lc)
            flat.append(kw)

    return flat


def _mirror_keywords_to_memory(dept_dir: Path, dept_name: str, keywords: list[str], source: Path) -> None:
    """Write resolved keywords back to memory/capture_routing_keywords.md as a backup.

    Preserves existing description if mirror exists; otherwise stamps a default.
    Marker comment at top makes it clear this file is auto-generated.
    """
    mem_dir = dept_dir / "memory"
    if not mem_dir.exists():
        try:
            mem_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.warning("Could not create memory dir for %s: %s", dept_name, e)
            return

    mirror_path = mem_dir / "capture_routing_keywords.md"
    try:
        rel_source = source.relative_to(COWORK_ROOT).as_posix()
    except ValueError:
        rel_source = source.as_posix()
    description = f"Auto-mirrored from {rel_source}. Keywords that auto-route captures to {dept_name}."

    # Preserve user-set description if present
    if mirror_path.exists():
        try:
            old_text = mirror_path.read_text(encoding="utf-8")
            old_fm, _ = parse_frontmatter(old_text)
            if isinstance(old_fm.get("description"), str) and old_fm["description"].strip():
                description = old_fm["description"]
        except OSError:
            pass

    lines = [
        "<!-- AUTO-GENERATED by inbox_routing.router. Source of truth: dept SKILL.md. Edit there, not here. -->",
        "---",
        f"name: Capture routing keywords — {dept_name}",
        f"description: {description}",
        "type: reference",
        f"dept: {dept_name}",
        "keywords:",
    ]
    for kw in keywords:
        lines.append(f"  - {kw}")
    lines.append("---")
    lines.append("")

    try:
        mirror_path.write_text("\n".join(lines), encoding="utf-8")
    except OSError as e:
        logger.warning("Failed writing mirror %s: %s", mirror_path, e)


def _load_keywords_from_mirror(kw_file: Path) -> tuple[list[str], str | None]:
    """Legacy fallback: load keywords from memory/capture_routing_keywords.md.

    Returns (keywords, dept_name_from_frontmatter).
    """
    text = kw_file.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    keywords = fm.get("keywords", [])
    dept_name = fm.get("dept")
    if not isinstance(keywords, list):
        keywords = []
    return keywords, dept_name


def load_dept_rules(departments_dir: Path = DEPARTMENTS_DIR) -> list[DeptRule]:
    """Discover dept routing rules. Prefers SKILL.md as source of truth, falls back to mirror.

    For each dept dir:
    1. Look for skills/<dept-master>/SKILL.md and parse `## Routing Keywords` block
       (with shared-pack imports resolved). On success, mirror the resolved list to memory/.
    2. If SKILL.md has no routing block (or no SKILL.md exists), fall back to the mirror file.
    """
    rules = []
    if not departments_dir.exists():
        return rules

    for dept_dir in sorted(departments_dir.iterdir()):
        if not dept_dir.is_dir():
            continue
        dept_name = dept_dir.name

        keywords: list[str] | None = None
        source: Path | None = None

        # Path 1: SKILL.md (single source of truth)
        skill_md = _find_skill_md(dept_dir)
        if skill_md is not None:
            resolved = _resolve_keywords_from_skill_md(skill_md)
            if resolved:
                keywords = resolved
                source = skill_md
                # Auto-mirror as backup
                _mirror_keywords_to_memory(dept_dir, dept_name, resolved, skill_md)

        # Path 2: legacy mirror fallback
        if keywords is None:
            mirror = dept_dir / "memory" / "capture_routing_keywords.md"
            if mirror.exists():
                kws, fm_dept = _load_keywords_from_mirror(mirror)
                if kws:
                    keywords = kws
                    source = mirror
                    if fm_dept:
                        dept_name = fm_dept

        if keywords:
            rules.append(DeptRule(name=dept_name, keywords=keywords, keywords_path=source or dept_dir))

    return rules


# ---------------------------------------------------------------------------
# Scoring + routing (unchanged from prior version)
# ---------------------------------------------------------------------------

def score_file_against_rules(file_path: Path, rules: list[DeptRule]) -> dict[str, int]:
    """Count keyword hits per dept. Searches filename + frontmatter tags + body, case-insensitive."""
    text = file_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    haystack = file_path.name.lower() + "\n"
    tags = fm.get("tags", [])
    if isinstance(tags, list):
        haystack += " ".join(str(t) for t in tags).lower() + "\n"
    haystack += body.lower()

    scores: dict[str, int] = {}
    for rule in rules:
        n = 0
        for kw in rule.keywords:
            kw_lc = kw.lower().strip()
            if not kw_lc:
                continue
            # word-ish boundary so "ict" doesn't match "predict"; allow chars within keyword
            pattern = r"(?<![a-z0-9])" + re.escape(kw_lc) + r"(?![a-z0-9])"
            n += len(re.findall(pattern, haystack))
        if n > 0:
            scores[rule.name] = n
    return scores


def decide_route(file: Path, rules: list[DeptRule]) -> RouteDecision:
    scores = score_file_against_rules(file, rules)
    if not scores:
        return RouteDecision(file=file, primary=None, secondaries=[], scores={})
    sorted_depts = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    primary_name, primary_score = sorted_depts[0]
    secondaries = [
        name for name, n in sorted_depts[1:]
        if n >= SECONDARY_MIN_HITS and n / primary_score >= SECONDARY_MIN_RATIO
    ]
    return RouteDecision(file=file, primary=primary_name, secondaries=secondaries, scores=scores)


def _yyyy_mm(file: Path) -> str:
    """YYYY-MM bucket from frontmatter captured_date if present, else file mtime."""
    text = file.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    cd = fm.get("captured_date", "")
    if isinstance(cd, str) and len(cd) >= 7 and cd[4] == "-":
        return cd[:7]
    dt = datetime.fromtimestamp(file.stat().st_mtime)
    return dt.strftime("%Y-%m")


def _rewrite_image_paths(body: str, depth_to_inbox: str) -> str:
    """Update `../processed_images/...` → `<depth>/INBOX/processed_images/...` after move."""
    return body.replace("../processed_images/", f"{depth_to_inbox}/INBOX/processed_images/")


def _stub_for_secondary(primary_dept: str, primary_path: Path, primary_filename: str, captured_date: str) -> str:
    """5-line cross-ref stub for a secondary or CEO dept.

    Uses full vault-relative path in the wikilink so Obsidian can disambiguate when stubs
    and primary share the same basename across multiple dept context/ folders.
    """
    try:
        rel = primary_path.relative_to(COWORK_ROOT).with_suffix("").as_posix()
    except ValueError:
        rel = primary_path.with_suffix("").as_posix()
    label = primary_path.stem
    return f"""---
cross_ref: true
primary_dept: {primary_dept}
captured_date: {captured_date}
source_filename: "{primary_filename}"
primary_path: "{rel}.md"
---

> **Cross-reference.** Primary capture filed under `{primary_dept}`. See [[{rel}|{label}]].
"""


def route_file(file: Path, rules: list[DeptRule], dry_run: bool = False) -> RouteDecision:
    """Route one markdown. Move primary, write secondary + CEO stubs."""
    decision = decide_route(file, rules)
    if not decision.primary:
        logger.warning("No keyword hits — leaving in place: %s", file.name)
        return decision

    yyyy_mm = _yyyy_mm(file)
    primary_dir = DEPARTMENTS_DIR / decision.primary / "context" / yyyy_mm
    target_path = primary_dir / file.name

    text = file.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    captured_date = fm.get("captured_date", "") or datetime.fromtimestamp(file.stat().st_mtime).isoformat()

    # Compute depth from primary context/YYYY-MM/ back to INBOX/processed_images/
    # COWORK/DEPARTMENTS/<dept>/context/YYYY-MM/file.md → up 4 → COWORK → INBOX/processed_images/
    body_rewritten = _rewrite_image_paths(body, "../../../..")

    # Update frontmatter to record routing decision; rewrite any image_ref path on move.
    rebuilt_fm_lines = ["---"]
    handled_keys = {"dept_routed", "dept_secondary", "routing_score"}
    for key, val in fm.items():
        if key in handled_keys:
            continue
        if key == "image_ref" and isinstance(val, str) and val.startswith("../processed_images/"):
            val = "../../../../INBOX/processed_images/" + val[len("../processed_images/"):]
        if isinstance(val, list):
            if val:
                rebuilt_fm_lines.append(f"{key}: [{', '.join(val)}]")
            else:
                rebuilt_fm_lines.append(f"{key}: []")
        else:
            rebuilt_fm_lines.append(f"{key}: {val}")
    rebuilt_fm_lines.append(f"dept_routed: {decision.primary}")
    if decision.secondaries:
        rebuilt_fm_lines.append(f"dept_secondary: [{', '.join(decision.secondaries)}]")
    score_str = ", ".join(f"{k}={v}" for k, v in sorted(decision.scores.items()))
    rebuilt_fm_lines.append(f'routing_score: "{score_str}"')
    rebuilt_fm_lines.append("---")
    new_content = "\n".join(rebuilt_fm_lines) + "\n" + body_rewritten

    if dry_run:
        logger.info(
            "[DRY RUN] %s → %s (secondaries: %s, scores: %s)",
            file.name, decision.primary, decision.secondaries, decision.scores,
        )
        return decision

    primary_dir.mkdir(parents=True, exist_ok=True)
    target_path.write_text(new_content, encoding="utf-8")
    file.unlink()
    try:
        rel = target_path.relative_to(COWORK_ROOT)
    except ValueError:
        rel = target_path
    logger.info("Routed %s -> %s", file.name, rel)

    # Cross-ref stubs in secondary depts (CEO stubs disabled per WRITE_CEO_STUBS — too noisy)
    stub_dests = list(decision.secondaries)
    if WRITE_CEO_STUBS and CEO_DEPT_NAME not in stub_dests and decision.primary != CEO_DEPT_NAME:
        stub_dests.append(CEO_DEPT_NAME)
    for sec in stub_dests:
        sec_dir = DEPARTMENTS_DIR / sec / "context" / yyyy_mm
        sec_dir.mkdir(parents=True, exist_ok=True)
        stub_content = _stub_for_secondary(decision.primary, target_path, file.name, captured_date)
        (sec_dir / file.name).write_text(stub_content, encoding="utf-8")

    return decision


def collect_pending(source_dirs: list[Path] | None = None) -> list[Path]:
    """Return all .md files in source dirs (top-level only)."""
    sources = source_dirs or DEFAULT_SOURCE_DIRS
    pending: list[Path] = []
    for src in sources:
        if not src.exists():
            continue
        for f in sorted(src.iterdir()):
            if f.is_file() and f.suffix.lower() == ".md":
                pending.append(f)
    return pending


def run(*, source_dirs: list[Path] | None = None, dry_run: bool = False) -> dict:
    rules = load_dept_rules()
    if not rules:
        logger.error("No dept rules loaded — aborting.")
        return {"total": 0, "routed": 0, "unrouted": 0, "decisions": []}

    pending = collect_pending(source_dirs)
    stats = {"total": len(pending), "routed": 0, "unrouted": 0, "decisions": []}
    for f in pending:
        decision = route_file(f, rules, dry_run=dry_run)
        stats["decisions"].append(decision)
        if decision.primary:
            stats["routed"] += 1
        else:
            stats["unrouted"] += 1

    if not dry_run and stats["routed"] > 0:
        from .gen_indexes import regenerate
        regenerate()

    return stats
