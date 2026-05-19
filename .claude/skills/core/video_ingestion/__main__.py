"""CLI entry: `python -m video_ingestion [URL | --batch]`."""

import argparse
import logging
import sys

from .pipeline import process_batch, process_url


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="Video ingestion: URL → transcript → markdown")
    parser.add_argument("url", nargs="?", help="Single video URL to process")
    parser.add_argument("--batch", action="store_true", help="Scan INBOX/clips/*.md + Clippings/*.md for URLs")
    parser.add_argument("--source-file", action="append", dest="source_files",
                        metavar="PATH", help="Extra .md file to scan for video URLs (repeatable)")
    parser.add_argument("--force", action="store_true", help="Re-process even if URL already in log")
    args = parser.parse_args()

    if args.batch or args.source_files:
        from pathlib import Path
        extra = [Path(p) for p in (args.source_files or [])]
        stats = process_batch(extra_files=extra)
        print("\n=== Batch summary ===")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        return 0

    if not args.url:
        parser.print_help()
        return 1

    out = process_url(args.url, force=args.force)
    if out:
        print(f"\nWrote: {out}")
        return 0
    print("\nSkipped or failed (see error_log.txt)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
