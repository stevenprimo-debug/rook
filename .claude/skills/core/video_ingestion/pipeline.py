"""Orchestrator: URL → transcribe → summarize → routed markdown."""

import logging
import re
from datetime import datetime
from pathlib import Path

from .config import (
    CLIPPINGS_DIR,
    ERROR_LOG,
    INSTAGRAM_BATCH_DIR,
    INSTAGRAM_BATCH_GLOB,
    PROCESSED_MD_DIR,
    PROCESSED_URLS_LOG,
    VIDEO_ARCHIVE_DIR,
)
from .summarize import SummaryResult, summarize
from .transcribe import TranscriptionResult, detect_platform, transcribe

logger = logging.getLogger(__name__)


URL_PATTERN = re.compile(r"https?://[^\s\)\]\}]+")

# Only extract IG/YT URLs from general .md scans (avoids false positives from Obsidian notes)
VIDEO_URL_RE = re.compile(
    r"https?://(?:www\.)?(?:"
    r"instagram\.com/(?:reel|p|tv)/[^\s\)\]\}]+"
    r"|youtu\.be/[^\s\)\]\}]+"
    r"|youtube\.com/(?:watch|shorts)/[^\s\)\]\}]+"
    r")"
)


def load_processed_urls() -> set[str]:
    if not PROCESSED_URLS_LOG.exists():
        return set()
    return {line.strip() for line in PROCESSED_URLS_LOG.read_text(encoding="utf-8").splitlines() if line.strip()}


def mark_processed(url: str) -> None:
    PROCESSED_URLS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED_URLS_LOG.open("a", encoding="utf-8") as f:
        f.write(url + "\n")


def log_error(url: str, error: Exception) -> None:
    ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ERROR_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {url} | {type(error).__name__}: {error}\n")


def find_urls_in_batch_files(extra_files: list[Path] | None = None) -> list[tuple[str, Path]]:
    """Scan INBOX/clips/*.md + Clippings/*.md + any extra_files for IG/YT URLs.

    Returns [(url, source_file), ...]. Uses VIDEO_URL_RE so general Obsidian notes
    don't produce false positives when scanned from Clippings/.
    """
    scan_dirs = [
        (INSTAGRAM_BATCH_DIR, INSTAGRAM_BATCH_GLOB),
        (CLIPPINGS_DIR, "*.md"),
    ]

    found: list[tuple[str, Path]] = []
    seen: set[Path] = set()

    def _extract(md: Path) -> None:
        if md in seen:
            return
        seen.add(md)
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            return
        for match in VIDEO_URL_RE.finditer(text):
            url = match.group(0).rstrip(".,);:")
            found.append((url, md))

    for scan_dir, glob_pat in scan_dirs:
        if not scan_dir.exists():
            continue
        for md in scan_dir.glob(glob_pat):
            _extract(md)

    for md in (extra_files or []):
        _extract(md)

    return found


def build_filename(slug: str, captured_at: datetime) -> str:
    """Match image-ingest convention: YYYY-MM-DD-HHMM-<slug>.md."""
    safe_slug = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-")[:60]
    return f"{captured_at.strftime('%Y-%m-%d-%H%M')}-{safe_slug}.md"


def render_markdown(
    *,
    url: str,
    transcription: TranscriptionResult,
    summary: SummaryResult,
    captured_at: datetime,
    source_md: Path | None,
) -> str:
    """Build the sidecar markdown matching image-ingest frontmatter shape."""
    platform = detect_platform(url)

    # Priority handling per priority_rules.md (e.g. YC content)
    priority_block = ""
    priority_field = ""
    if summary.priority_signals:
        signals = ", ".join(summary.priority_signals)
        priority_field = (
            "\npriority: high"
            f"\npriority_reason: \"matched priority_rules signals: {signals}\""
            f"\npriority_tags: {summary.priority_signals}"
        )
        priority_block = (
            "\n> ## ⭐ Primo priority — auto-flagged\n"
            f"> Matched priority signals: **{signals}**.\n"
            "> See `DEPARTMENTS/CEO/conventions/priority_rules.md` for action template.\n"
        )

    # Frontmatter
    yaml_tags = "[" + ", ".join(summary.tags) + "]"
    yaml_depts = "[" + ", ".join(summary.dept_hints) + "]"
    title_safe = (transcription.title or "").replace('"', "'")
    uploader_safe = (transcription.uploader or "").replace('"', "'")

    duration_min = transcription.duration_seconds / 60.0
    source_ref = f"\nsource_batch_md: {source_md.name}" if source_md else ""

    fm = f"""---
source: video-ingestion
captured_date: {captured_at.isoformat()}
captured_via: yt-dlp+{transcription.source_method}
original_url: {url}
platform: {platform}
title: "{title_safe}"
uploader: "{uploader_safe}"
upload_date: {transcription.upload_date or ''}
duration_seconds: {transcription.duration_seconds:.1f}
duration_minutes: {duration_min:.1f}
language: {transcription.language}
transcription_method: {transcription.source_method}
status: processed
tags: {yaml_tags}
dept_hints: {yaml_depts}{priority_field}{source_ref}
---
"""

    quotes_block = ""
    if summary.key_quotes:
        quotes_lines = "\n".join(f"> {q}" for q in summary.key_quotes)
        quotes_block = f"\n## Key Quotes\n\n{quotes_lines}\n"

    impl_block = ""
    if summary.ways_to_implement:
        impl_lines = "\n".join(f"- {item}" for item in summary.ways_to_implement)
        impl_block = f"\n## Ways to Implement\n\n{impl_lines}\n"

    body = f"""{priority_block}
## Summary

{summary.summary}
{quotes_block}{impl_block}
## Source

- **URL:** {url}
- **Platform:** {platform}
- **Title:** {transcription.title or 'unknown'}
- **Uploader:** {transcription.uploader or 'unknown'}
- **Duration:** {duration_min:.1f} min
- **Transcribed via:** {transcription.source_method}

## Transcript

{transcription.transcript}
"""

    return fm + body


def process_url(url: str, *, source_md: Path | None = None, force: bool = False) -> Path | None:
    """Full pipeline for one URL. Returns path to written markdown, or None if skipped."""
    if not force and url in load_processed_urls():
        logger.info("Skip (already processed): %s", url)
        return None

    captured_at = datetime.now().astimezone()

    try:
        logger.info("Transcribing: %s", url)
        trans = transcribe(url)
        logger.info(
            "  → %s, %.1fs (%s)",
            trans.source_method,
            trans.duration_seconds,
            trans.language,
        )

        if not trans.transcript.strip():
            # No speech — try Vision on the thumbnail (catches text overlays, hooks, title cards)
            logger.info("No speech transcript — trying Vision fallback on thumbnail")
            from .transcribe import transcribe_via_vision
            trans = transcribe_via_vision(url)
            if not trans.transcript.strip():
                raise RuntimeError("No usable content: empty after Whisper + Vision fallback (likely music-only, no text overlays)")

        logger.info("Summarizing via Claude...")
        summ = summarize(trans.transcript, source_url=url, platform=detect_platform(url))
        logger.info(
            "  → slug=%s, depts=%s, priority=%s",
            summ.title_slug,
            summ.dept_hints,
            summ.priority_signals or "—",
        )

        md_text = render_markdown(
            url=url,
            transcription=trans,
            summary=summ,
            captured_at=captured_at,
            source_md=source_md,
        )

        PROCESSED_MD_DIR.mkdir(parents=True, exist_ok=True)
        filename = build_filename(summ.title_slug, captured_at)
        out_path = PROCESSED_MD_DIR / filename
        out_path.write_text(md_text, encoding="utf-8")

        # Permanent copy in VIDEO/ — not touched by the router; always findable
        VIDEO_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        (VIDEO_ARCHIVE_DIR / filename).write_text(md_text, encoding="utf-8")

        mark_processed(url)
        logger.info("Wrote: %s (+ VIDEO/%s)", out_path, filename)
        return out_path

    except Exception as e:
        logger.error("FAILED: %s — %s: %s", url, type(e).__name__, e)
        log_error(url, e)
        return None


def process_batch(extra_files: list[Path] | None = None) -> dict:
    """Scan INBOX/clips/*.md + Clippings/*.md (+ extra_files) for video URLs, process unseen ones."""
    import shutil

    urls = find_urls_in_batch_files(extra_files=extra_files)
    processed_set = load_processed_urls()

    pending = [(u, src) for u, src in urls if u not in processed_set]
    logger.info("Batch: %d URLs found, %d unprocessed", len(urls), len(pending))

    succeeded = []
    failed = []
    for url, src in pending:
        out = process_url(url, source_md=src)
        if out:
            succeeded.append((url, out))
        else:
            failed.append(url)

    # Move INBOX/clips/ batch files to VIDEO/ — they've been processed, VIDEO/ is their permanent home
    # Clippings/ files are left in place (router handles those separately)
    VIDEO_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    source_files = {src for _, src in urls if src is not None}
    for src in source_files:
        if src.exists() and src.parent == INSTAGRAM_BATCH_DIR:
            dest = VIDEO_ARCHIVE_DIR / src.name
            shutil.move(str(src), dest)
            logger.info("Moved batch note → VIDEO/%s", src.name)

    return {
        "found": len(urls),
        "pending": len(pending),
        "succeeded": len(succeeded),
        "failed": len(failed),
    }
