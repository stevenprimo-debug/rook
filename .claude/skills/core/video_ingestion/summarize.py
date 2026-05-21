"""Single Claude call per video to produce summary, dept-routing tags, and 'ways to implement' bullets."""

import json
import logging
from dataclasses import dataclass

import anthropic

from .config import ANTHROPIC_API_KEY, SUMMARY_MODEL

logger = logging.getLogger(__name__)


SUMMARY_SYSTEM_PROMPT = """\
You are a research analyst summarizing video transcripts for the operator's ROOK knowledge vault.
ROOK is a 20-agent Agentic OS. The operator routes captured content to the agent(s) most likely
to act on it. Prioritize specificity — what's actually claimed, what could actually be built.

For each transcript you receive, return a JSON object with this exact shape:

{
  "title_slug": "kebab-case-slug-under-60-chars-summarizing-content",
  "summary": "2-3 sentence summary of what the video actually says.",
  "key_quotes": ["quote 1 verbatim from transcript", "quote 2 verbatim from transcript"],
  "tags": ["tag1", "tag2", "tag3"],
  "agent_hints": ["agent-slug"],
  "ways_to_implement": [
    "One short sentence: what the operator could build/use/test from this. Imperative tense.",
    "Another short sentence."
  ],
  "priority_signals": ["yc"]
}

Rules:
- `title_slug`: kebab-case, ≤60 chars, descriptive. Use the actual topic/speaker/product, not generic.
- `summary`: ≤3 sentences. What's actually claimed in the video, not meta-commentary.
- `key_quotes`: 1-3 verbatim lines from the transcript that capture the substance. Empty list OK.
- `tags`: 3-6 lowercase kebab-case tags for the inbox routing system to score.
- `agent_hints`: which ROOK agents care about this content. Pick from the agent slugs:
  account-manager, chief-of-staff, content-strategist, copywriter, creative-director, deep-researcher,
  designer, engineering-lead, finance-manager, inbox-manager, librarian, marketing-director,
  product-manager, r-and-d-lead, sales-director, seo-specialist, shopify-agent, social-media-manager,
  software-dev-team, trading-analyst. Multiple OK if cross-relevant. Be honest about scope.
- `ways_to_implement`: VERY SHORT (≤2 sentences each), 0-3 items. Concrete actions the operator could take.
  Skip if nothing actionable — empty list is correct.
- `priority_signals`: from this list ONLY: ["yc", "anthropic-launch", "karpathy", "sequoia-ai",
  "garry-tan"]. Empty list if none apply. The system uses these to auto-flag priority.

Output JSON only, no preamble, no markdown fences."""


@dataclass
class SummaryResult:
    title_slug: str
    summary: str
    key_quotes: list[str]
    tags: list[str]
    agent_hints: list[str]
    ways_to_implement: list[str]
    priority_signals: list[str]


def summarize(transcript: str, *, source_url: str, platform: str, api_key: str | None = None) -> SummaryResult:
    """One Claude call, structured JSON out."""
    client = anthropic.Anthropic(api_key=api_key or ANTHROPIC_API_KEY)

    user_msg = f"""SOURCE_URL: {source_url}
PLATFORM: {platform}

TRANSCRIPT:
{transcript}"""

    resp = client.messages.create(
        model=SUMMARY_MODEL,
        max_tokens=1500,
        system=SUMMARY_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    text = resp.content[0].text.strip()
    # Defensive: if model wrapped in fences, strip them
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        text = text.strip()
        # strip optional language tag like "json"
        if text.startswith("json"):
            text = text[4:].strip()

    data = json.loads(text)

    return SummaryResult(
        title_slug=data.get("title_slug", "untitled-video")[:60],
        summary=data.get("summary", ""),
        key_quotes=data.get("key_quotes", []),
        tags=data.get("tags", []),
        agent_hints=data.get("agent_hints", data.get("dept_hints", [])),
        ways_to_implement=data.get("ways_to_implement", []),
        priority_signals=data.get("priority_signals", []),
    )
