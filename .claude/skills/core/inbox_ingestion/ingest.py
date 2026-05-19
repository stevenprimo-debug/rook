"""Main ingestion pipeline: scan → analyze → write → move."""

import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .config import (
    ENABLE_RESEARCH,
    ERROR_LOG,
    PROCESSED_IMG_DIR,
    PROCESSED_MD_DIR,
    SOURCE_DIR,
    SOURCE_FAILED_DIR,
    SUPPORTED_EXTENSIONS,
)
from .research import ResearchResult, enrich
from .vision import VisionResult, analyze_image

logger = logging.getLogger(__name__)


def get_pending_images(source_dir: Path | None = None) -> list[Path]:
    """Return top-level images in source_dir. Subfolders are NOT scanned."""
    src = source_dir or SOURCE_DIR
    if not src.exists():
        logger.warning("Source directory does not exist: %s", src)
        return []

    pending = []
    for f in sorted(src.iterdir()):
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
            pending.append(f)
    return pending


def build_filename(image_path: Path, slug: str) -> str:
    """Build YYYY-MM-DD-HHMM-<slug>.<ext> from file mtime."""
    mtime = image_path.stat().st_mtime
    dt = datetime.fromtimestamp(mtime, tz=timezone.utc).astimezone()
    prefix = dt.strftime("%Y-%m-%d-%H%M")
    ext = image_path.suffix.lower()
    return f"{prefix}-{slug}{ext}"


def build_markdown(
    filename_stem: str,
    image_filename: str,
    result: VisionResult,
    original_filename: str,
    captured_date: str,
    research: ResearchResult | None = None,
) -> str:
    """Generate the paired markdown file content."""
    tags_yaml = ", ".join(result.tags)
    research_section = ""
    if research and research.markdown:
        research_section = f"\n## Research\n\n{research.markdown}\n"

    return f"""---
source: drive-ingestion
captured_date: {captured_date}
captured_via: drive-ingestion
original_filename: "{original_filename}"
image_ref: ../processed_images/{image_filename}
status: processed
tags: [{tags_yaml}]
---

## Extracted Text

{result.extracted_text if result.extracted_text else "_No visible text detected._"}

## Summary

{result.description}
{research_section}
## Source Image

![](../processed_images/{image_filename})
"""


def process_single_image(
    image_path: Path,
    *,
    api_key: str | None = None,
    md_dir: Path | None = None,
    img_dir: Path | None = None,
    failed_dir: Path | None = None,
    error_log: Path | None = None,
) -> bool:
    """Process one image. On success: source is DELETED from Drive (COWORK copy is canonical).
    On failure: source moves to _failed_ingestion/ for manual review."""
    _md_dir = md_dir or PROCESSED_MD_DIR
    _img_dir = img_dir or PROCESSED_IMG_DIR
    _failed_dir = failed_dir or SOURCE_FAILED_DIR
    _error_log = error_log or ERROR_LOG

    try:
        result = analyze_image(image_path, api_key=api_key)

        research = None
        if result.research_targets and ENABLE_RESEARCH:
            try:
                research = enrich(
                    result.research_targets,
                    description=result.description,
                    extracted_text=result.extracted_text,
                    api_key=api_key,
                )
                logger.info(
                    "Research: %d targets, %d searches",
                    len(result.research_targets),
                    research.search_count if research else 0,
                )
            except Exception as research_err:
                logger.warning("Research enrichment failed for %s: %s", image_path.name, research_err)
        elif result.research_targets:
            logger.info(
                "Research SKIPPED (ENABLE_RESEARCH=0): %d targets identified, no web_search calls made",
                len(result.research_targets),
            )

        new_filename = build_filename(image_path, result.slug)
        stem = Path(new_filename).stem

        mtime = image_path.stat().st_mtime
        dt = datetime.fromtimestamp(mtime, tz=timezone.utc).astimezone()
        captured_date = dt.isoformat()

        md_content = build_markdown(
            filename_stem=stem,
            image_filename=new_filename,
            result=result,
            original_filename=image_path.name,
            captured_date=captured_date,
            research=research,
        )

        _img_dir.mkdir(parents=True, exist_ok=True)
        _md_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(image_path, _img_dir / new_filename)
        (_md_dir / f"{stem}.md").write_text(md_content, encoding="utf-8")

        # COWORK copy is canonical now. Drive source can be deleted —
        # an empty Drive root means "all caught up".
        image_path.unlink()

        logger.info("Processed: %s → %s (source deleted)", image_path.name, new_filename)
        return True

    except Exception as e:
        logger.error("Failed to process %s: %s", image_path.name, e)
        try:
            _failed_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(image_path), str(_failed_dir / image_path.name))
        except Exception as move_err:
            logger.error("Failed to move %s to _failed: %s", image_path.name, move_err)

        _error_log.parent.mkdir(parents=True, exist_ok=True)
        with open(_error_log, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} | {image_path.name} | {e}\n")
        return False


def run_pipeline(
    *,
    source_dir: Path | None = None,
    api_key: str | None = None,
    md_dir: Path | None = None,
    img_dir: Path | None = None,
    dry_run: bool = False,
) -> dict:
    """Run the full ingestion pipeline. Returns stats dict."""
    src = source_dir or SOURCE_DIR
    pending = get_pending_images(src)

    failed_dir = src / "_failed_ingestion" if source_dir else SOURCE_FAILED_DIR

    stats = {"total": len(pending), "success": 0, "failed": 0, "skipped": 0}

    if not pending:
        logger.info("No new images to process.")
        return stats

    logger.info("Found %d image(s) to process.", len(pending))

    if dry_run:
        for img in pending:
            logger.info("[DRY RUN] Would process: %s", img.name)
        stats["skipped"] = len(pending)
        return stats

    for img in pending:
        ok = process_single_image(
            img,
            api_key=api_key,
            md_dir=md_dir,
            img_dir=img_dir,
            failed_dir=failed_dir,
        )
        if ok:
            stats["success"] += 1
        else:
            stats["failed"] += 1

    logger.info(
        "Pipeline complete: %d success, %d failed out of %d total.",
        stats["success"], stats["failed"], stats["total"],
    )

    # Auto-route the markdowns we just produced (and any pending in INBOX/clips/ + Clippings/).
    try:
        from inbox_routing.router import run as run_routing
        routing_stats = run_routing()
        logger.info(
            "Routing complete: %d routed, %d unrouted out of %d total.",
            routing_stats["routed"], routing_stats["unrouted"], routing_stats["total"],
        )
        if routing_stats["routed"] > 0:
            from inbox_routing.gen_indexes import regenerate
            n = regenerate()
            logger.info("Regenerated %d INDEX.md files.", n)
    except Exception as e:
        logger.warning("Routing/index step failed (ingest succeeded): %s", e)

    return stats
