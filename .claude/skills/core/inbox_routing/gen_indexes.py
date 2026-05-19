"""Regenerate INDEX.md for each dept's context/ folder + MASTER_INDEX.md at vault root.

Run after routing to refresh all indexes:
    cd "<COWORK ROOT>/CORE" && python -m inbox_routing.gen_indexes

Generates:
- DEPARTMENTS/<dept>/context/INDEX.md  (per-dept, monthly buckets)
- MASTER_INDEX.md at vault root        (cross-dept, three views: by-date, by-dept, by-tag)
"""

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re

COWORK_ROOT = Path(__file__).parent.parent.parent
DEPARTMENTS_DIR = COWORK_ROOT / "DEPARTMENTS"


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter as a flat dict. Best-effort, no PyYAML dependency."""
    if not text.startswith("---"):
        return {}
    try:
        end = text.index("\n---", 3)
    except ValueError:
        return {}
    fm_text = text[3:end].strip()
    out: dict = {}
    current_list_key = None
    for raw in fm_text.splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if current_list_key and line.startswith("  - "):
            out.setdefault(current_list_key, []).append(line[4:].strip().strip('"\''))
            continue
        current_list_key = None
        m = re.match(r"^([\w_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            current_list_key = key
            continue
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            out[key] = [v.strip().strip('"\'') for v in inner.split(",") if v.strip()]
        else:
            out[key] = val.strip('"\'')
    return out


def regenerate(departments_dir: Path = DEPARTMENTS_DIR) -> int:
    generated = 0
    for dept in sorted(departments_dir.iterdir()):
        if not dept.is_dir():
            continue
        ctx = dept / "context"
        if not ctx.exists():
            continue

        months = sorted([p for p in ctx.iterdir() if p.is_dir()])
        if not months:
            continue

        lines = [
            f"# {dept.name} Context Index",
            "",
            f"Auto-routed captures filed under `{dept.name}/`. See [[{dept.name}/CLAUDE.md|{dept.name} dept overview]] and `memory/capture_routing_keywords.md` for what routes here.",
            "",
            "Cross-reference stubs (`cross_ref: true` frontmatter) point to a primary capture filed elsewhere — the wikilink navigates to the canonical file.",
            "",
        ]

        for month_dir in months:
            files = sorted([
                f for f in month_dir.iterdir()
                if f.suffix == ".md" and f.name not in ("INDEX.md", "README.md")
            ])
            if not files:
                continue
            lines.append(f"## {month_dir.name}")
            lines.append("")
            for f in files:
                is_xref = "cross_ref: true" in f.read_text(encoding="utf-8")
                rel = f"DEPARTMENTS/{dept.name}/context/{month_dir.name}/{f.stem}"
                tag = " *(xref)*" if is_xref else ""
                lines.append(f"- [[{rel}|{f.stem}]]{tag}")
            lines.append("")

        lines.append("---")
        lines.append(f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} — regenerate via `python -m inbox_routing.gen_indexes`.*")

        (ctx / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
        readme = ctx / "README.md"
        if readme.exists():
            readme.unlink()
        generated += 1

    regenerate_master_index(departments_dir)
    return generated


def regenerate_master_index(departments_dir: Path = DEPARTMENTS_DIR) -> Path:
    """Build cross-dept MASTER_INDEX.md at vault root with three views: by-date, by-dept, by-tag."""

    by_dept: dict = defaultdict(list)         # dept -> [(month, stem, title, tags, fpath)]
    by_month: dict = defaultdict(list)        # YYYY-MM -> [(dept, stem, title, tags)]
    by_tag: dict = defaultdict(list)          # tag -> [(dept, stem, title, fpath)]
    total_files = 0

    for dept in sorted(departments_dir.iterdir()):
        if not dept.is_dir():
            continue
        ctx = dept / "context"
        if not ctx.exists():
            continue
        for month_dir in sorted(p for p in ctx.iterdir() if p.is_dir()):
            month = month_dir.name
            for f in sorted(month_dir.iterdir()):
                if f.suffix != ".md" or f.name in ("INDEX.md", "README.md"):
                    continue
                try:
                    text = f.read_text(encoding="utf-8")
                except OSError:
                    continue
                fm = parse_frontmatter(text)
                title = fm.get("title", f.stem).strip('"\'')
                raw_tags = fm.get("tags", []) or []
                if isinstance(raw_tags, str):
                    raw_tags = [raw_tags]
                tags = [t.strip().lower() for t in raw_tags if t and t.strip()]

                rel = f"DEPARTMENTS/{dept.name}/context/{month}/{f.stem}"
                by_dept[dept.name].append((month, f.stem, title, tags, rel))
                by_month[month].append((dept.name, f.stem, title, tags, rel))
                for t in tags:
                    by_tag[t].append((dept.name, f.stem, title, rel))
                total_files += 1

    lines: list = [
        "# COWORK Master Index",
        "",
        f"Cross-dept index of every routed capture. **{total_files} files indexed across {len(by_dept)} depts.**",
        "",
        "Three views below — same data, different lenses. For dept-scoped browsing, follow the dept link to its own `context/INDEX.md`.",
        "",
        "---",
        "",
    ]

    # ---- VIEW 1: By Date (newest month first) ----
    lines.append("## By Date")
    lines.append("")
    lines.append("*Chronological — find by \"when did I clip this?\"*")
    lines.append("")
    for month in sorted(by_month.keys(), reverse=True):
        items = sorted(by_month[month], key=lambda x: x[1], reverse=True)  # newest stem first
        lines.append(f"### {month} ({len(items)} files)")
        lines.append("")
        for dept_name, stem, title, _tags, rel in items:
            lines.append(f"- **[{dept_name}]** [[{rel}|{title}]]")
        lines.append("")

    # ---- VIEW 2: By Department ----
    lines.append("---")
    lines.append("")
    lines.append("## By Department")
    lines.append("")
    lines.append("*Find by \"where did the router put it?\"*")
    lines.append("")
    for dept_name in sorted(by_dept.keys()):
        items = by_dept[dept_name]
        months_present = sorted({m for m, *_ in items})
        lines.append(
            f"- **{dept_name}** — {len(items)} files across {len(months_present)} months → "
            f"[[DEPARTMENTS/{dept_name}/context/INDEX|{dept_name} dept index]]"
        )
    lines.append("")

    # ---- VIEW 3: By Tag (only tags with ≥2 files to keep noise down) ----
    lines.append("---")
    lines.append("")
    lines.append("## By Topic Tag")
    lines.append("")
    lines.append("*Find by \"what is it about?\" — only tags with ≥2 files shown.*")
    lines.append("")
    sorted_tags = sorted(by_tag.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    for tag, files in sorted_tags:
        if len(files) < 2:
            continue
        depts_for_tag = sorted({d for d, *_ in files})
        lines.append(
            f"- **#{tag}** ({len(files)} files) — depts: {', '.join(depts_for_tag)}"
        )
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"*Auto-generated {datetime.now().strftime('%Y-%m-%d %H:%M')} — regenerated on every router run via `python -m inbox_routing.gen_indexes`.*")

    out = COWORK_ROOT / "MASTER_INDEX.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


if __name__ == "__main__":
    n = regenerate()
    print(f"Generated {n} per-dept INDEX.md files + MASTER_INDEX.md at vault root")
