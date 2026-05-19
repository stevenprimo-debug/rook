"""CLI entry point: python -m inbox_ingestion"""

import argparse
import logging
import sys

from .ingest import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Drive → COWORK INBOX image ingestion pipeline"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List pending images without processing",
    )
    parser.add_argument(
        "--source-dir",
        type=str,
        default=None,
        help="Override source directory (default: G:\\My Drive — top-level images only)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    from pathlib import Path
    source = Path(args.source_dir) if args.source_dir else None

    stats = run_pipeline(source_dir=source, dry_run=args.dry_run)

    if stats["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
