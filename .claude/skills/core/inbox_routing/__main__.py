"""CLI: python -m inbox_routing [--dry-run]"""

import argparse
import logging
import sys

from .router import run


def main():
    parser = argparse.ArgumentParser(description="Route INBOX/Clippings markdown to dept context/ folders.")
    parser.add_argument("--dry-run", action="store_true", help="Print decisions without moving files")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    stats = run(dry_run=args.dry_run)
    print(
        f"\nTotal: {stats['total']}  Routed: {stats['routed']}  Unrouted: {stats['unrouted']}",
        file=sys.stderr,
    )
    if stats["unrouted"] > 0:
        sys.exit(2 if args.dry_run else 0)


if __name__ == "__main__":
    main()
