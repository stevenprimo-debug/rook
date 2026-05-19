"""Frontmatter validation — ensures emitted markdown matches the INBOX schema."""

import re
from pathlib import Path
from unittest.mock import patch

import pytest

from inbox_ingestion.ingest import process_single_image
from inbox_ingestion.vision import VisionResult

REQUIRED_FIELDS = {
    "source",
    "captured_date",
    "captured_via",
    "original_filename",
    "image_ref",
    "status",
    "tags",
}


def _parse_frontmatter(md_text: str) -> dict:
    """Extract YAML frontmatter from markdown as a flat dict."""
    match = re.match(r"^---\n(.+?)\n---", md_text, re.DOTALL)
    assert match, "No frontmatter block found"
    fm = {}
    for line in match.group(1).strip().split("\n"):
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm


class TestFrontmatterSchema:
    @patch("inbox_ingestion.ingest.analyze_image")
    def test_all_required_fields_present(self, mock_analyze, tmp_dirs, sample_png):
        mock_analyze.return_value = VisionResult(
            extracted_text="OCR text",
            description="A screenshot.",
            tags=["demo", "test"],
            slug="demo-screenshot",
        )
        process_single_image(
            sample_png,
            api_key="fake",
            md_dir=tmp_dirs["md_dir"],
            img_dir=tmp_dirs["img_dir"],
            processed_dir=tmp_dirs["processed"],
            failed_dir=tmp_dirs["failed"],
            error_log=tmp_dirs["error_log"],
        )

        md_files = list(tmp_dirs["md_dir"].glob("*.md"))
        assert len(md_files) == 1

        content = md_files[0].read_text(encoding="utf-8")
        fm = _parse_frontmatter(content)

        for field in REQUIRED_FIELDS:
            assert field in fm, f"Missing frontmatter field: {field}"

    @patch("inbox_ingestion.ingest.analyze_image")
    def test_source_is_drive_ingestion(self, mock_analyze, tmp_dirs, sample_png):
        mock_analyze.return_value = VisionResult("", "desc", ["t"], "slug")
        process_single_image(
            sample_png, api_key="fake",
            md_dir=tmp_dirs["md_dir"], img_dir=tmp_dirs["img_dir"],
            processed_dir=tmp_dirs["processed"], failed_dir=tmp_dirs["failed"],
            error_log=tmp_dirs["error_log"],
        )
        content = list(tmp_dirs["md_dir"].glob("*.md"))[0].read_text()
        fm = _parse_frontmatter(content)
        assert fm["source"] == "drive-ingestion"

    @patch("inbox_ingestion.ingest.analyze_image")
    def test_status_is_processed(self, mock_analyze, tmp_dirs, sample_png):
        mock_analyze.return_value = VisionResult("", "desc", ["t"], "slug")
        process_single_image(
            sample_png, api_key="fake",
            md_dir=tmp_dirs["md_dir"], img_dir=tmp_dirs["img_dir"],
            processed_dir=tmp_dirs["processed"], failed_dir=tmp_dirs["failed"],
            error_log=tmp_dirs["error_log"],
        )
        content = list(tmp_dirs["md_dir"].glob("*.md"))[0].read_text()
        fm = _parse_frontmatter(content)
        assert fm["status"] == "processed"

    @patch("inbox_ingestion.ingest.analyze_image")
    def test_image_ref_points_to_processed_images(self, mock_analyze, tmp_dirs, sample_png):
        mock_analyze.return_value = VisionResult("", "desc", ["t"], "my-slug")
        process_single_image(
            sample_png, api_key="fake",
            md_dir=tmp_dirs["md_dir"], img_dir=tmp_dirs["img_dir"],
            processed_dir=tmp_dirs["processed"], failed_dir=tmp_dirs["failed"],
            error_log=tmp_dirs["error_log"],
        )
        content = list(tmp_dirs["md_dir"].glob("*.md"))[0].read_text()
        fm = _parse_frontmatter(content)
        assert fm["image_ref"].startswith("../processed_images/")
        assert "my-slug" in fm["image_ref"]
