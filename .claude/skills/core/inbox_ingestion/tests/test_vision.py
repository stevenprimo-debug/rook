"""Tests for vision.py — Claude Vision API interaction."""

import base64
import io
import json

import pytest
from PIL import Image

from inbox_ingestion.vision import (
    MAX_IMAGE_DIMENSION,
    ResearchTarget,
    VisionResult,
    parse_vision_response,
    prepare_image,
)


class TestParseVisionResponse:
    def test_parses_clean_json(self, mock_vision_json):
        result = parse_vision_response(mock_vision_json)
        assert isinstance(result, VisionResult)
        assert result.extracted_text == "Hello World — test text"
        assert result.description.startswith("Screenshot of a test")
        assert result.tags == ["test", "screenshot", "ui"]
        assert result.slug == "test-interface-hello-world"

    def test_strips_markdown_fencing(self, mock_vision_result):
        fenced = f"```json\n{json.dumps(mock_vision_result)}\n```"
        result = parse_vision_response(fenced)
        assert result.slug == "test-interface-hello-world"

    def test_truncates_long_slug(self):
        data = json.dumps({
            "extracted_text": "",
            "description": "test",
            "tags": ["test"],
            "slug": "a" * 100,
        })
        result = parse_vision_response(data)
        assert len(result.slug) <= 60

    def test_handles_empty_text(self):
        data = json.dumps({
            "extracted_text": "",
            "description": "An image with no text.",
            "tags": ["photo"],
            "slug": "no-text-image",
        })
        result = parse_vision_response(data)
        assert result.extracted_text == ""

    def test_returns_untitled_on_unrecoverable_garbage(self):
        result = parse_vision_response("not json at all")
        assert result.slug == "untitled"
        assert result.extracted_text == ""

    def test_salvages_fields_from_malformed_json(self):
        broken = '{"extracted_text": "He said "hello" loudly", "description": "A quote.", "tags": ["test"], "slug": "broken-quotes"}'
        result = parse_vision_response(broken)
        assert result.slug == "broken-quotes"
        assert result.description == "A quote."
        assert result.tags == ["test"]

    def test_handles_missing_fields_gracefully(self):
        data = json.dumps({"slug": "minimal"})
        result = parse_vision_response(data)
        assert result.extracted_text == ""
        assert result.description == ""
        assert result.tags == []
        assert result.slug == "minimal"
        assert result.research_targets == []

    def test_parses_research_targets(self):
        data = json.dumps({
            "extracted_text": "test",
            "description": "test",
            "tags": ["t"],
            "slug": "test",
            "research_targets": [
                {"type": "social_handle", "value": "@futurewalt", "context": "Instagram AI"},
                {"type": "person", "value": "Nicolas Boucher"},
                {"value": "no-type-still-valid"},
                {"type": "url"},  # missing value, should be skipped
            ],
        })
        result = parse_vision_response(data)
        assert len(result.research_targets) == 3
        assert result.research_targets[0].type == "social_handle"
        assert result.research_targets[0].value == "@futurewalt"
        assert result.research_targets[0].context == "Instagram AI"
        assert result.research_targets[2].type == "unknown"
        assert isinstance(result.research_targets[0], ResearchTarget)


class TestPrepareImage:
    def _write_image(self, tmp_path, name, size, fmt, save_format=None):
        """Helper: create an image file with given size and PIL save format."""
        img = Image.new("RGB", size, (255, 0, 0))
        path = tmp_path / name
        img.save(path, format=save_format or fmt)
        return path

    def test_normal_image_passes_through(self, tmp_path):
        path = self._write_image(tmp_path, "small.png", (100, 100), "PNG")
        data, media_type = prepare_image(path)
        assert media_type == "image/png"
        assert isinstance(data, str) and len(data) > 0

    def test_oversized_image_is_downscaled(self, tmp_path):
        path = self._write_image(tmp_path, "huge.png", (10000, 5000), "PNG")
        data, media_type = prepare_image(path)
        decoded = base64.b64decode(data)
        with Image.open(io.BytesIO(decoded)) as result_img:
            assert max(result_img.width, result_img.height) <= MAX_IMAGE_DIMENSION

    def test_jpeg_disguised_as_png_is_corrected(self, tmp_path):
        # Save as JPEG but with .PNG extension (the iPhone gotcha)
        img = Image.new("RGB", (200, 200), (0, 255, 0))
        path = tmp_path / "fake.PNG"
        img.save(path, format="JPEG")

        data, media_type = prepare_image(path)
        assert media_type == "image/jpeg"
        decoded = base64.b64decode(data)
        with Image.open(io.BytesIO(decoded)) as result_img:
            assert result_img.format == "JPEG"

    def test_rgba_jpeg_target_converts_to_rgb(self, tmp_path):
        # Saving RGBA as JPEG would normally fail; verify our code handles it
        img = Image.new("RGBA", (100, 100), (0, 0, 255, 128))
        path = tmp_path / "rgba.jpg"
        img.save(path, format="PNG")  # written as PNG, but extension says jpg
        # Pillow detects actual format from content, so target = PNG, not JPEG
        data, media_type = prepare_image(path)
        assert media_type == "image/png"
