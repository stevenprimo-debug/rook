"""Perplexity API client — Search + Agent + Embeddings.

Reads PERPLEXITY_API_KEY from environment. Never hardcoded.

Usage:
    from claude_connectors.perplexity import PerplexityClient
    ppx = PerplexityClient.from_env()
    result = ppx.search(query="...", max_results=5)
    print(result.summary)
    for cite in result.citations:
        print(cite["url"])

All endpoints are read-only (no external state change). Consumers should
respect `max_results` and avoid paginated loops without explicit operator
confirm — pricing is per-query.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://api.perplexity.ai"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3


@dataclass
class SearchResult:
    summary: str
    citations: list[dict[str, Any]]
    raw: dict[str, Any]


class PerplexityError(Exception):
    """Raised on non-recoverable Perplexity API errors."""


class PerplexityClient:
    def __init__(self, api_key: str, *, timeout: int = DEFAULT_TIMEOUT) -> None:
        if not api_key:
            raise ValueError("PerplexityClient requires a non-empty api_key")
        self._api_key = api_key
        self._timeout = timeout

    @classmethod
    def from_env(cls, *, env_var: str = "PERPLEXITY_API_KEY") -> "PerplexityClient":
        key = os.environ.get(env_var)
        if not key:
            raise PerplexityError(
                f"{env_var} is not set. Store the key in your PowerShell profile "
                f"or ~/.claude/credentials/perplexity.json and re-export."
            )
        return cls(api_key=key)

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        url = f"{BASE_URL}{path}"
        payload = json.dumps(body).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        last_err: Exception | None = None
        for attempt in range(MAX_RETRIES):
            try:
                req = Request(url, data=payload, headers=headers, method="POST")
                with urlopen(req, timeout=self._timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except HTTPError as e:
                if e.code == 429 and attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
                if 400 <= e.code < 500:
                    try:
                        detail = json.loads(e.read().decode("utf-8"))
                    except Exception:
                        detail = {"raw_body": "<unparseable>"}
                    raise PerplexityError(f"HTTP {e.code}: {detail}") from e
                last_err = e
            except URLError as e:
                last_err = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
        raise PerplexityError(f"Request failed after {MAX_RETRIES} attempts: {last_err}")

    def search(
        self,
        query: str,
        *,
        max_results: int = 5,
        max_tokens_per_page: int = 512,
    ) -> SearchResult:
        """Synthesized search with citations.

        Returns SearchResult with .summary (str), .citations (list[dict]), .raw (dict).
        """
        body = {
            "query": query,
            "max_results": max_results,
            "max_tokens_per_page": max_tokens_per_page,
        }
        raw = self._post("/search", body)
        summary = raw.get("answer") or raw.get("summary") or ""
        citations = raw.get("citations") or raw.get("results") or []
        return SearchResult(summary=summary, citations=citations, raw=raw)

    def responses(
        self,
        input_text: str,
        *,
        preset: str = "fast-search",
        previous_response_id: str | None = None,
    ) -> dict[str, Any]:
        """Agent (Responses) API — synthesized answer over web search.

        Endpoint: POST /v1/responses
        Body: {"preset": "fast-search", "input": "..."}

        Returns the full Responses API dict. Use `extract_text()` and
        `extract_citations()` to pull the answer + citation URLs out of
        the nested output structure.
        """
        body: dict[str, Any] = {"preset": preset, "input": input_text}
        if previous_response_id:
            body["previous_response_id"] = previous_response_id
        return self._post("/v1/responses", body)

    @staticmethod
    def extract_text(response: dict[str, Any]) -> str:
        """Pull the assistant's text answer out of a /v1/responses response."""
        for msg in response.get("output", []):
            for block in msg.get("content", []):
                if block.get("type") == "output_text":
                    return block.get("text", "")
        return ""

    @staticmethod
    def extract_citations(response: dict[str, Any]) -> list[dict[str, Any]]:
        """Pull citation annotations from a /v1/responses response.

        Returns list of citation dicts (shape: {title, url, ...} when present).
        """
        out: list[dict[str, Any]] = []
        for msg in response.get("output", []):
            for block in msg.get("content", []):
                for ann in block.get("annotations", []) or []:
                    out.append(ann)
        return out

    def synthesize(
        self,
        query: str,
        *,
        preset: str = "fast-search",
    ) -> tuple[str, list[dict[str, Any]]]:
        """Convenience: one-shot synthesized answer + citations.

        Returns (answer_text, list_of_citations).
        """
        response = self.responses(input_text=query, preset=preset)
        return self.extract_text(response), self.extract_citations(response)

    def embed(self, texts: list[str], *, model: str = "embed-v1") -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        body = {"model": model, "input": texts}
        raw = self._post("/embeddings", body)
        return [item["embedding"] for item in raw.get("data", [])]
