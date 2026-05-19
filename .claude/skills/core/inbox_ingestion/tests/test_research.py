"""Tests for research.py + enrich.py — research orchestration and retrofit."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from inbox_ingestion.enrich import (
    append_research_section,
    enrich_one,
    parse_existing_markdown,
)
from inbox_ingestion.research import ResearchResult, enrich
from inbox_ingestion.vision import ResearchTarget


class TestEnrichResearch:
    def test_returns_none_when_no_targets(self):
        result = enrich([], description="test", extracted_text="test", api_key="fake")
        assert result is None

    @patch("inbox_ingestion.research.anthropic.Anthropic")
    def test_calls_api_with_web_search_tool(self, mock_anthropic):
        mock_response = MagicMock()
        text_block = MagicMock(); text_block.type = "text"; text_block.text = "## Research result"
        search_block = MagicMock(); search_block.type = "server_tool_use"; search_block.name = "web_search"
        mock_response.content = [text_block, search_block, search_block]
        mock_response.stop_reason = "end_turn"

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        targets = [ResearchTarget(type="person", value="Test Person", context="test")]
        result = enrich(targets, description="d", extracted_text="t", api_key="fake")

        assert result is not None
        assert result.search_count == 2
        assert result.markdown == "## Research result"
        assert result.truncated is False

        call_kwargs = mock_client.messages.create.call_args.kwargs
        tools = call_kwargs["tools"]
        assert any(t.get("type") == "web_search_20250305" for t in tools)

    @patch("inbox_ingestion.research.anthropic.Anthropic")
    def test_marks_truncated_on_max_tokens(self, mock_anthropic):
        mock_response = MagicMock()
        text_block = MagicMock(); text_block.type = "text"; text_block.text = "partial"
        mock_response.content = [text_block]
        mock_response.stop_reason = "max_tokens"
        mock_anthropic.return_value.messages.create.return_value = mock_response

        result = enrich(
            [ResearchTarget(type="brand", value="X")],
            api_key="fake",
        )
        assert result.truncated is True


class TestParseExistingMarkdown:
    def test_extracts_description_and_text(self, tmp_path):
        md = tmp_path / "sample.md"
        md.write_text("""---
source: drive-ingestion
status: processed
---

## Extracted Text

Hello World some text here

## Summary

This is a screenshot of something interesting.

## Source Image

![](../foo.png)
""", encoding="utf-8")

        parsed = parse_existing_markdown(md)
        assert "Hello World" in parsed["extracted_text"]
        assert parsed["description"] == "This is a screenshot of something interesting."
        assert parsed["has_research"] is False

    def test_detects_already_enriched(self, tmp_path):
        md = tmp_path / "sample.md"
        md.write_text("""---
status: processed
---

## Extracted Text

text

## Summary

desc

## Research

prior research here

## Source Image

![](../foo.png)
""", encoding="utf-8")

        parsed = parse_existing_markdown(md)
        assert parsed["has_research"] is True

    def test_strips_no_text_placeholder(self, tmp_path):
        md = tmp_path / "sample.md"
        md.write_text("""---
status: processed
---

## Extracted Text

_No visible text detected._

## Summary

A photo with no text.

## Source Image

![](../foo.png)
""", encoding="utf-8")

        parsed = parse_existing_markdown(md)
        assert parsed["extracted_text"] == ""


class TestAppendResearchSection:
    def test_inserts_before_source_image(self, tmp_path):
        md = tmp_path / "sample.md"
        md.write_text("""---
status: processed
---

## Summary

x

## Source Image

![](../foo.png)
""", encoding="utf-8")

        append_research_section(md, "### Found stuff\n- thing 1\n- thing 2")

        result = md.read_text(encoding="utf-8")
        assert "## Research" in result
        assert "Found stuff" in result
        assert result.index("## Research") < result.index("## Source Image")


class TestEnrichOne:
    @patch("inbox_ingestion.enrich.enrich")
    @patch("inbox_ingestion.enrich.infer_targets")
    def test_skips_if_already_enriched(self, mock_infer, mock_enrich, tmp_path):
        md = tmp_path / "x.md"
        md.write_text("""---\nstatus: processed\n---\n\n## Research\n\nold\n\n## Source Image\n\n![](x.png)\n""")
        result = enrich_one(md, api_key="fake")
        assert result["skipped"] is True
        mock_infer.assert_not_called()

    @patch("inbox_ingestion.enrich.enrich")
    @patch("inbox_ingestion.enrich.infer_targets", return_value=[])
    def test_skips_if_no_targets(self, mock_infer, mock_enrich, tmp_path):
        md = tmp_path / "x.md"
        md.write_text("""---\nstatus: processed\n---\n\n## Extracted Text\n\nfoo\n\n## Summary\n\nbar\n\n## Source Image\n\n![](x.png)\n""")
        result = enrich_one(md, api_key="fake")
        assert result["skipped"] is True
        assert "no research targets" in result.get("reason", "")
        mock_enrich.assert_not_called()

    @patch("inbox_ingestion.enrich.enrich")
    @patch("inbox_ingestion.enrich.infer_targets")
    def test_writes_research_when_found(self, mock_infer, mock_enrich, tmp_path):
        mock_infer.return_value = [ResearchTarget(type="person", value="Test")]
        mock_enrich.return_value = ResearchResult(
            markdown="### Test\n- found stuff",
            search_count=2,
        )
        md = tmp_path / "x.md"
        md.write_text("""---\nstatus: processed\n---\n\n## Extracted Text\n\nfoo\n\n## Summary\n\nbar\n\n## Source Image\n\n![](x.png)\n""")

        result = enrich_one(md, api_key="fake")

        assert result["skipped"] is False
        assert result["targets"] == 1
        assert result["searches"] == 2
        assert "## Research" in md.read_text()
        assert "found stuff" in md.read_text()

    @patch("inbox_ingestion.enrich.infer_targets")
    def test_dry_run_does_not_write(self, mock_infer, tmp_path):
        mock_infer.return_value = [ResearchTarget(type="person", value="Test")]
        md = tmp_path / "x.md"
        original = """---\nstatus: processed\n---\n\n## Extracted Text\n\nfoo\n\n## Summary\n\nbar\n\n## Source Image\n\n![](x.png)\n"""
        md.write_text(original)

        result = enrich_one(md, api_key="fake", dry_run=True)

        assert result["skipped"] is True
        assert "dry-run" in result.get("reason", "")
        assert md.read_text() == original
