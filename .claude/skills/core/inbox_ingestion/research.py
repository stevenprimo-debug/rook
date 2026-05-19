"""Web research enrichment via Claude's server-side web_search tool."""

import logging
from dataclasses import dataclass
from typing import Iterable

import anthropic

from .config import ANTHROPIC_API_KEY, VISION_MODEL
from .vision import ResearchTarget

logger = logging.getLogger(__name__)

RESEARCH_SYSTEM_PROMPT = """\
You are a research analyst enriching captured screenshots for a personal knowledge vault.

For each research target the user gives you, use the web_search tool to find authoritative information. Then write structured markdown that includes:
- The official source (website, profile URL, or canonical link) — always linked
- 2-4 key facts about the target (what they do, what they're known for, recent activity)
- Why it might matter to someone capturing this in a knowledge inbox (be concrete, not generic)

Format the response as markdown using ### headings (one per target) with bullet points underneath. Be concise — this is a research note, not an article. If a target is unfindable or ambiguous, say so honestly in one line and move on. Never fabricate links.

End with a "## Connections" section if you notice meaningful overlap between targets (shared people, shared ecosystem, shared thesis). Skip the section if there's no real connection."""

MAX_SEARCH_USES = 6


@dataclass
class ResearchResult:
    markdown: str
    search_count: int
    truncated: bool = False


def enrich(
    targets: Iterable[ResearchTarget],
    *,
    description: str = "",
    extracted_text: str = "",
    api_key: str | None = None,
) -> ResearchResult | None:
    """Run web research on the given targets and return synthesized markdown.

    Returns None if no targets provided. Raises on API errors.
    """
    targets = list(targets)
    if not targets:
        return None

    key = api_key or ANTHROPIC_API_KEY
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    targets_str = "\n".join(
        f"- **{t.type}**: {t.value}" + (f" _({t.context})_" if t.context else "")
        for t in targets
    )
    snippet = extracted_text[:1200].strip()

    user_msg = f"""Context — the user captured this screenshot:

**Description:** {description or '(none provided)'}

**Visible text excerpt:**
{snippet if snippet else '(no text)'}

**Research these targets:**
{targets_str}

Use web_search to investigate each. Return the structured markdown research note per the format spec."""

    client = anthropic.Anthropic(api_key=key)
    response = client.messages.create(
        model=VISION_MODEL,
        max_tokens=4096,
        system=[{
            "type": "text",
            "text": RESEARCH_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": MAX_SEARCH_USES,
        }],
        messages=[{"role": "user", "content": user_msg}],
    )

    markdown_parts = []
    search_count = 0
    for block in response.content:
        if block.type == "text":
            markdown_parts.append(block.text)
        elif block.type == "server_tool_use" and block.name == "web_search":
            search_count += 1

    markdown = "\n\n".join(p.strip() for p in markdown_parts if p.strip())
    truncated = response.stop_reason == "max_tokens"

    return ResearchResult(
        markdown=markdown.strip(),
        search_count=search_count,
        truncated=truncated,
    )
