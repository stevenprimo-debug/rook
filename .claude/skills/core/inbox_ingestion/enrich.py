"""Retrofit existing INBOX markdown with web research without re-OCR.

Reads each .md file in INBOX/processed/, infers research targets from the
existing description + extracted_text via Claude, runs web research, and
appends a `## Research` section. Idempotent — skips files that already
have a Research section.

Run from CORE/:
    python -m inbox_ingestion.enrich               # process all
    python -m inbox_ingestion.enrich --dry-run     # show what would run
    python -m inbox_ingestion.enrich --limit 5     # process N files
    python -m inbox_ingestion.enrich --file foo.md # one specific file
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

import anthropic

from .config import ANTHROPIC_API_KEY, PROCESSED_MD_DIR, VISION_MODEL
from .research import enrich
from .vision import ResearchTarget

logger = logging.getLogger(__name__)

TARGET_INFERENCE_PROMPT = """\
A screenshot was previously captured with this metadata:

**Description:** {description}

**Extracted text:**
{extracted_text}

Identify external entities worth researching from this content. Return a JSON array of objects with these fields:
- "type": one of "url", "social_handle", "person", "brand", "product", "article"
- "value": the identifier
- "context": optional 3-8 word disambiguation hint

Return [] if the content is purely personal (private chat, family note, no external references).
Otherwise return 1-4 specific targets. Prefer specific identifiers over generic ones.

Return ONLY the JSON array, no markdown fencing or commentary."""


def parse_existing_markdown(path: Path) -> dict:
    """Extract description and extracted_text from an existing INBOX markdown file."""
    content = path.read_text(encoding="utf-8")

    text_match = re.search(
        r"## Extracted Text\s*\n(.*?)(?=\n## )",
        content,
        re.DOTALL,
    )
    extracted_text = text_match.group(1).strip() if text_match else ""
    if extracted_text == "_No visible text detected._":
        extracted_text = ""

    desc_match = re.search(
        r"## Summary\s*\n(.*?)(?=\n## )",
        content,
        re.DOTALL,
    )
    description = desc_match.group(1).strip() if desc_match else ""

    has_research = "## Research" in content

    return {
        "description": description,
        "extracted_text": extracted_text,
        "has_research": has_research,
        "content": content,
    }


def infer_targets(description: str, extracted_text: str, api_key: str) -> list[ResearchTarget]:
    """Use Claude to infer research targets from existing OCR + description."""
    if not description and not extracted_text:
        return []

    prompt = TARGET_INFERENCE_PROMPT.format(
        description=description or "(none)",
        extracted_text=extracted_text[:1500] or "(no text)",
    )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=VISION_MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Could not parse target inference response: %s", raw[:200])
        return []

    targets = []
    for t in data:
        if isinstance(t, dict) and t.get("value"):
            targets.append(ResearchTarget(
                type=t.get("type", "unknown"),
                value=str(t["value"]),
                context=t.get("context", "") or "",
            ))
    return targets


def append_research_section(md_path: Path, research_markdown: str) -> None:
    """Append `## Research` to the markdown file before `## Source Image`."""
    content = md_path.read_text(encoding="utf-8")
    research_block = f"\n## Research\n\n{research_markdown}\n"

    if "## Source Image" in content:
        new_content = content.replace(
            "## Source Image",
            f"{research_block}\n## Source Image",
            1,
        )
    else:
        new_content = content.rstrip() + "\n" + research_block

    md_path.write_text(new_content, encoding="utf-8")


def enrich_one(md_path: Path, api_key: str, dry_run: bool = False) -> dict:
    """Enrich a single markdown file. Returns stats dict."""
    parsed = parse_existing_markdown(md_path)
    stats = {"file": md_path.name, "skipped": False, "targets": 0, "searches": 0}

    if parsed["has_research"]:
        stats["skipped"] = True
        stats["reason"] = "already enriched"
        return stats

    targets = infer_targets(parsed["description"], parsed["extracted_text"], api_key)
    stats["targets"] = len(targets)

    if not targets:
        stats["skipped"] = True
        stats["reason"] = "no research targets identified"
        return stats

    if dry_run:
        stats["skipped"] = True
        stats["reason"] = f"dry-run, would research: {[t.value for t in targets]}"
        return stats

    result = enrich(
        targets,
        description=parsed["description"],
        extracted_text=parsed["extracted_text"],
        api_key=api_key,
    )

    if result and result.markdown:
        append_research_section(md_path, result.markdown)
        stats["searches"] = result.search_count
    else:
        stats["skipped"] = True
        stats["reason"] = "research returned empty"

    return stats


def main():
    parser = argparse.ArgumentParser(description="Retrofit research enrichment to existing INBOX markdown")
    parser.add_argument("--dry-run", action="store_true", help="Identify targets without running research")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N files")
    parser.add_argument("--file", type=str, default=None, help="Enrich one specific .md file")
    parser.add_argument("--md-dir", type=str, default=None, help="Override INBOX/processed/ directory")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    if not ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY not set")
        sys.exit(1)

    md_dir = Path(args.md_dir) if args.md_dir else PROCESSED_MD_DIR

    if args.file:
        files = [md_dir / args.file]
    else:
        files = sorted(md_dir.glob("*.md"))
        if args.limit:
            files = files[: args.limit]

    logger.info("Found %d markdown file(s) to consider.", len(files))

    totals = {"enriched": 0, "skipped": 0, "failed": 0, "searches": 0}
    for i, f in enumerate(files, 1):
        logger.info("[%d/%d] %s", i, len(files), f.name)
        try:
            stats = enrich_one(f, api_key=ANTHROPIC_API_KEY, dry_run=args.dry_run)
            if stats["skipped"]:
                totals["skipped"] += 1
                logger.info("  skipped: %s", stats.get("reason", ""))
            else:
                totals["enriched"] += 1
                totals["searches"] += stats["searches"]
                logger.info("  enriched: %d targets, %d searches", stats["targets"], stats["searches"])
        except Exception as e:
            totals["failed"] += 1
            logger.error("  failed: %s", e)

    logger.info(
        "Done: %d enriched, %d skipped, %d failed, %d total searches",
        totals["enriched"], totals["skipped"], totals["failed"], totals["searches"],
    )


if __name__ == "__main__":
    main()
