"""
ROOK — Regenerate _roster.json from SKILL.md frontmatter.

Source-of-truth: each agent's SKILL.md YAML frontmatter.
Output: _roster.json at vault root (peer to MASTER_INDEX.md).

Run:
    python scripts/regenerate-roster.py

Called automatically by librarian weekly sweep after subgraph regen.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

VAULT_ROOT = Path(__file__).parents[1]
AGENTS_DIR = VAULT_ROOT / "agents"
OUTPUT_PATH = VAULT_ROOT / "_roster.json"

SKIP_DIRS = {"_archive", "_template", ".git"}

TIER_BUCKETS = {
    1: "tier_1_vector_graph",
    2: "tier_2_sqlite",
    3: "tier_3_vectorless_pdf",
    4: "tier_4_markdown",
}


def _extract_frontmatter_text(text: str) -> str:
    """Return raw frontmatter string (without --- delimiters). Strips UTF-8 BOM if present."""
    # Strip UTF-8 BOM (﻿) that Windows editors add
    text = text.lstrip("﻿")
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[4:end]


def _parse_top_level_scalars(front: str) -> dict:
    """
    Parse only top-level (indent=0) key: value pairs from YAML frontmatter.
    Skips block scalars (lines following 'key: >' or 'key: |') until the
    next zero-indent key. Returns a flat dict of string values.
    """
    result = {}
    lines = front.split("\n")
    in_block = False

    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue

        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent == 0:
            in_block = False
            if ":" in stripped:
                key, _, rest = stripped.partition(":")
                key = key.strip()
                rest = rest.strip()
                # Remove trailing inline comments
                rest = re.sub(r"\s+#.*$", "", rest).strip()
                if rest in (">", "|", ">-", "|-"):
                    in_block = True
                    # Don't store block scalar value yet
                elif rest:
                    # Strip quotes
                    if (rest.startswith('"') and rest.endswith('"')) or \
                       (rest.startswith("'") and rest.endswith("'")):
                        rest = rest[1:-1]
                    result[key] = rest
        # If indent > 0: skip (sub-block handled separately)

    return result


def _extract_raw_block(front: str, key: str) -> str:
    """Extract the indented lines below a top-level key as a raw string."""
    lines = front.split("\n")
    capturing = False
    captured = []

    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent == 0:
            if capturing:
                break  # Next top-level key — stop
            if stripped.startswith(key + ":"):
                capturing = True
                continue  # Skip the key line itself

        if capturing and indent > 0:
            captured.append(line)
        elif capturing and indent == 0 and not stripped:
            captured.append(line)  # blank lines within block

    return "\n".join(captured)


def _parse_memory_block(raw: str) -> dict:
    """Parse the memory: sub-block."""
    scalars = {}
    for line in raw.split("\n"):
        s = line.lstrip()
        indent = len(line) - len(s)
        if indent == 2 and ":" in s and not s.startswith("-") and not s.startswith("#"):
            k, _, v = s.partition(":")
            k = k.strip()
            v = v.strip()
            v = re.sub(r"\s+#.*$", "", v).strip().strip('"').strip("'")
            if v:
                scalars[k] = v

    try:
        primary_tier = int(scalars.get("primary_tier", "4").split()[0])
    except (ValueError, AttributeError):
        primary_tier = 4

    backend = scalars.get("backend", "markdown+grep")
    schema_file = scalars.get("schema_file", "") or ""
    if schema_file in ("null", "~", ""):
        schema_file = None
    rationale = scalars.get("rationale_one_line", "")

    # Parse secondary list
    secondary = []
    in_secondary = False
    current_sec = {}
    for line in raw.split("\n"):
        s = line.lstrip()
        indent = len(line) - len(s)
        if indent == 2 and s.startswith("secondary:"):
            in_secondary = True
            continue
        if in_secondary:
            if indent == 0 and s and not s.startswith("#"):
                break  # back to top level
            if indent == 4 and s.startswith("- "):
                if current_sec:
                    secondary.append(current_sec)
                current_sec = {}
                rest = s[2:]
                if ":" in rest:
                    k, _, v = rest.partition(":")
                    try:
                        current_sec[k.strip()] = int(v.strip())
                    except ValueError:
                        current_sec[k.strip()] = v.strip().strip('"')
            elif indent >= 6 and ":" in s and not s.startswith("#"):
                k, _, v = s.partition(":")
                current_sec[k.strip()] = v.strip().strip('"')
    if current_sec:
        secondary.append(current_sec)

    return {
        "primary_tier": primary_tier,
        "backend": backend,
        "schema_file": schema_file,
        "rationale_one_line": rationale,
        "secondary": secondary,
        "queries_shared_shelf": True,
    }


def _parse_connectors_block(raw: str) -> list:
    """Parse the connectors: sub-block. Handles both structured and path-list formats."""
    connectors = []
    current = {}

    for line in raw.split("\n"):
        s = line.lstrip()
        indent = len(line) - len(s)

        if not s or s.startswith("#"):
            continue

        if indent >= 2 and s.startswith("- "):
            if current:
                connectors.append(current)
            current = {}
            rest = s[2:].strip()
            if ":" in rest:
                k, _, v = rest.partition(":")
                k = k.strip()
                v = v.strip().strip('"')
                if k == "name":
                    current["name"] = v
                else:
                    current[k] = v
            else:
                # Path-style: - .claude/connectors/gmail/
                name = rest.rstrip("/").split("/")[-1]
                current = {"name": name, "purpose": "", "reversibility": "?",
                           "auth_required": "operator-provided", "type": "REST"}
        elif indent >= 4 and ":" in s and not s.startswith("#"):
            k, _, v = s.partition(":")
            current[k.strip()] = v.strip().strip('"')

    if current:
        connectors.append(current)
    return connectors


def build_roster() -> dict:
    agent_slugs = sorted([
        d.name for d in AGENTS_DIR.iterdir()
        if d.is_dir() and d.name not in SKIP_DIRS and not d.name.startswith("_")
    ])

    agents_out = []
    model_dist = {"opus": 0, "sonnet": 0}
    tier_dist = {v: [] for v in TIER_BUCKETS.values()}
    categories_seen = set()

    dispatch_chains = {
        "designer": ["creative-director", "marketing-director", "designer"],
        "copywriter": ["creative-director", "copywriter"],
        "content-strategist": ["creative-director", "content-strategist"],
        "social-media-manager": ["creative-director", "marketing-director", "social-media-manager"],
    }

    for slug in agent_slugs:
        skill_path = AGENTS_DIR / slug / "SKILL.md"
        if not skill_path.exists():
            print(f"WARN: no SKILL.md for {slug}", file=sys.stderr)
            continue

        text = skill_path.read_text(encoding="utf-8", errors="ignore")
        front = _extract_frontmatter_text(text)

        scalars = _parse_top_level_scalars(front)

        name = scalars.get("name", slug)
        # Strip common suffixes
        for suffix in [" — Master Agent Skill", " - Master Agent Skill"]:
            name = name.replace(suffix, "").strip()

        category = scalars.get("category", "Platform")
        status = scalars.get("status", "skeleton")
        model = scalars.get("model", "sonnet").split()[0]  # strip trailing comments

        categories_seen.add(category)
        if model in model_dist:
            model_dist[model] += 1

        mem_raw = _extract_raw_block(front, "memory")
        mem = _parse_memory_block(mem_raw)

        conn_raw = _extract_raw_block(front, "connectors")
        connectors = _parse_connectors_block(conn_raw)

        tier_bucket = TIER_BUCKETS.get(mem["primary_tier"], "tier_4_markdown")
        tier_dist[tier_bucket].append(slug)

        # Role one-liner: first sentence of description (strip YAML block scalar marker)
        desc_raw = _extract_raw_block(front, "description")
        desc = " ".join(desc_raw.split()).strip()
        role_one_line = desc.split(".")[0][:150] if desc else ""

        agents_out.append({
            "slug": slug,
            "name": name,
            "category": category,
            "status": status,
            "model": model,
            "role_one_line": role_one_line,
            "memory": mem,
            "connectors": connectors,
            "dispatch": {
                "upstream_required": dispatch_chains.get(slug),
                "downstream_pattern": "returns-to-chief-of-staff",
            },
        })

    return {
        "_meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generated_by": "librarian weekly sweep",
            "version": "1.0",
            "agent_count": len(agents_out),
        },
        "agents": agents_out,
        "dispatch_chains": dispatch_chains,
        "categories": sorted(categories_seen),
        "model_distribution": model_dist,
        "memory_distribution": tier_dist,
    }


if __name__ == "__main__":
    roster = build_roster()
    OUTPUT_PATH.write_text(
        json.dumps(roster, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Written: {OUTPUT_PATH} ({roster['_meta']['agent_count']} agents)")
    # Quick sanity
    print(f"Model dist: {roster['model_distribution']}")
    print(f"Tier 1: {roster['memory_distribution']['tier_1_vector_graph']}")
    print(f"Tier 2: {roster['memory_distribution']['tier_2_sqlite']}")
