#!/usr/bin/env python3
"""Thin CLI for the Perplexity connector — ping-pong from any session.

Reads PERPLEXITY_API_KEY from environment.

Usage:
    python scripts/ppx.py "your query"
    python scripts/ppx.py "your query" --max-results 5 --max-tokens 1024
    python scripts/ppx.py --agent "system prompt" "first user message"

Output: prints the summary, then a numbered list of citations.
"""
import argparse
import io
import sys
from pathlib import Path

# Force UTF-8 stdout (Windows cp1252 default chokes on common API response chars)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Import the connector client by path (no package install needed)
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / ".claude" / "connectors" / "perplexity"))

from client import PerplexityClient, PerplexityError  # type: ignore  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Perplexity ping-pong CLI")
    parser.add_argument("query", help="Your question (synthesis mode by default)")
    parser.add_argument("--search-only", action="store_true",
                        help="Use /search endpoint — returns raw results without synthesis")
    parser.add_argument("--preset", default="fast-search",
                        help="Responses API preset (fast-search, deep-research, etc.)")
    parser.add_argument("--max-results", type=int, default=5,
                        help="(search-only mode) — number of raw results")
    parser.add_argument("--max-tokens", type=int, default=1024,
                        help="(search-only mode) — max tokens per page snippet")
    args = parser.parse_args(argv)

    try:
        ppx = PerplexityClient.from_env()
    except PerplexityError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    try:
        if args.search_only:
            result = ppx.search(
                query=args.query,
                max_results=args.max_results,
                max_tokens_per_page=args.max_tokens,
            )
            for i, cite in enumerate(result.citations, 1):
                url = cite.get("url") or cite.get("link") or "(no url)"
                title = cite.get("title") or "(no title)"
                snippet = cite.get("snippet", "").strip()
                print(f"[{i}] {title}")
                print(f"    {url}")
                if snippet:
                    print(f"    {snippet[:300]}")
                print()
        else:
            content, citations = ppx.synthesize(
                query=args.query,
                preset=args.preset,
            )
            print(content)
            if citations:
                print()
                print("Annotations:")
                for i, cite in enumerate(citations, 1):
                    url = cite.get("url") or cite.get("link")
                    title = cite.get("title") or ""
                    if url:
                        print(f"  [{i}] {title} — {url}".strip(" —"))
                    else:
                        print(f"  [{i}] {cite}")
    except PerplexityError as e:
        print(f"API error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
