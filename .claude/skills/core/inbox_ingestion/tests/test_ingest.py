"""Tests for ingest.py — pipeline logic."""

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from inbox_ingestion.ingest import (
    build_filename,
    build_markdown,
    get_pending_images,
    process_single_image,
    run_pipeline,
)
from inbox_ingestion.tests.conftest import _minimal_png
from inbox_ingestion.vision import VisionResult


class TestGetPendingImages:
    def test_finds_images_in_source(self, tmp_dirs, sample_png):
        pending = get_pending_images(tmp_dirs["source"])
        assert len(pending) == 1
        assert pending[0].name == "test_screenshot.png"

    def test_ignores_non_image_files(self, tmp_dirs):
        (tmp_dirs["source"] / "notes.txt").write_text("hello")
        (tmp_dirs["source"] / "data.csv").write_text("a,b")
        pending = get_pending_images(tmp_dirs["source"])
        assert len(pending) == 0

    def test_skips_subfolders(self, tmp_dirs, sample_png):
        sub = tmp_dirs["source"] / "subfolder"
        sub.mkdir()
        (sub / "nested.png").write_bytes(_minimal_png())
        pending = get_pending_images(tmp_dirs["source"])
        assert len(pending) == 1
        assert pending[0].name == "test_screenshot.png"

    def test_returns_empty_for_nonexistent_dir(self, tmp_path):
        pending = get_pending_images(tmp_path / "nope")
        assert pending == []

    def test_handles_multiple_extensions(self, tmp_dirs):
        for name in ["a.png", "b.jpg", "c.jpeg", "d.gif"]:
            (tmp_dirs["source"] / name).write_bytes(_minimal_png())
        pending = get_pending_images(tmp_dirs["source"])
        assert len(pending) == 4


class TestBuildFilename:
    def test_format_matches_convention(self, sample_png):
        filename = build_filename(sample_png, "hello-world")
        assert filename.endswith("-hello-world.png")
        parts = filename.split("-")
        assert len(parts[0]) == 4  # year
        assert len(parts[1]) == 2  # month
        assert len(parts[2]) == 2  # day

    def test_preserves_extension(self, tmp_dirs):
        jpg = tmp_dirs["source"] / "photo.JPG"
        jpg.write_bytes(b"fake jpg")
        filename = build_filename(jpg, "test")
        assert filename.endswith("-test.jpg")


class TestBuildMarkdown:
    def test_contains_required_frontmatter_fields(self):
        result = VisionResult(
            extracted_text="some text",
            description="A test image.",
            tags=["test", "demo"],
            slug="test-image",
        )
        md = build_markdown(
            filename_stem="2026-05-02-1430-test-image",
            image_filename="2026-05-02-1430-test-image.png",
            result=result,
            original_filename="IMG_0394.PNG",
            captured_date="2026-05-02T14:30:00-05:00",
        )
        assert "source: drive-ingestion" in md
        assert "captured_date: 2026-05-02T14:30:00-05:00" in md
        assert "captured_via: drive-ingestion" in md
        assert 'original_filename: "IMG_0394.PNG"' in md
        assert "image_ref: ../processed_images/2026-05-02-1430-test-image.png" in md
        assert "status: processed" in md
        assert "tags: [test, demo]" in md

    def test_contains_extracted_text_section(self):
        result = VisionResult(
            extracted_text="Hello World",
            description="Test.",
            tags=[],
            slug="test",
        )
        md = build_markdown("s", "s.png", result, "o.png", "2026-01-01T00:00:00Z")
        assert "## Extracted Text" in md
        assert "Hello World" in md

    def test_no_text_placeholder(self):
        result = VisionResult(
            extracted_text="",
            description="Photo with no text.",
            tags=[],
            slug="test",
        )
        md = build_markdown("s", "s.png", result, "o.png", "2026-01-01T00:00:00Z")
        assert "_No visible text detected._" in md

    def test_inline_image_reference(self):
        result = VisionResult(
            extracted_text="",
            description="Test.",
            tags=[],
            slug="test",
        )
        md = build_markdown("s", "my-image.png", result, "o.png", "2026-01-01T00:00:00Z")
        assert "![](../processed_images/my-image.png)" in md


class TestProcessSingleImage:
    @patch("inbox_ingestion.ingest.analyze_image")
    def test_success_copies_to_cowork_and_deletes_source(self, mock_analyze, tmp_dirs, sample_png):
        mock_analyze.return_value = VisionResult(
            extracted_text="Test",
            description="A test.",
            tags=["test"],
            slug="test-slug",
        )
        ok = process_single_image(
            sample_png,
            api_key="fake-key",
            md_dir=tmp_dirs["md_dir"],
            img_dir=tmp_dirs["img_dir"],
            failed_dir=tmp_dirs["failed"],
            error_log=tmp_dirs["error_log"],
        )
        assert ok is True

        md_files = list(tmp_dirs["md_dir"].glob("*.md"))
        assert len(md_files) == 1
        assert "test-slug" in md_files[0].name

        img_files = list(tmp_dirs["img_dir"].glob("*.png"))
        assert len(img_files) == 1

        # Source MUST be deleted on success — empty Drive root = "all caught up".
        assert not sample_png.exists()

    @patch("inbox_ingestion.ingest.analyze_image", side_effect=Exception("API boom"))
    def test_failure_moves_to_failed(self, mock_analyze, tmp_dirs, sample_png):
        ok = process_single_image(
            sample_png,
            api_key="fake-key",
            md_dir=tmp_dirs["md_dir"],
            img_dir=tmp_dirs["img_dir"],
            failed_dir=tmp_dirs["failed"],
            error_log=tmp_dirs["error_log"],
        )
        assert ok is False
        assert (tmp_dirs["failed"] / "test_screenshot.png").exists()
        assert tmp_dirs["error_log"].exists()
        assert "API boom" in tmp_dirs["error_log"].read_text()


class TestRunPipeline:
    @patch("inbox_ingestion.ingest.analyze_image")
    def test_dry_run_does_not_modify(self, mock_analyze, tmp_dirs, sample_png):
        stats = run_pipeline(
            source_dir=tmp_dirs["source"],
            dry_run=True,
        )
        assert stats["skipped"] == 1
        assert stats["success"] == 0
        assert sample_png.exists()
        mock_analyze.assert_not_called()

    @patch("inbox_ingestion.ingest.process_single_image", return_value=True)
    def test_processes_all_pending(self, mock_process, tmp_dirs, sample_png):
        (tmp_dirs["source"] / "second.png").write_bytes(_minimal_png())

        stats = run_pipeline(
            source_dir=tmp_dirs["source"],
            api_key="fake",
        )
        assert stats["total"] == 2
        assert mock_process.call_count == 2

    def test_empty_source_returns_zero(self, tmp_dirs):
        stats = run_pipeline(source_dir=tmp_dirs["source"])
        assert stats["total"] == 0
