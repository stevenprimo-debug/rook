"""Shared fixtures for inbox_ingestion tests."""

import json
import struct
from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def tmp_dirs(tmp_path):
    """Create the full directory tree needed for pipeline testing."""
    source = tmp_path / "source"
    source.mkdir()
    md_dir = tmp_path / "processed"
    md_dir.mkdir()
    img_dir = tmp_path / "processed_images"
    img_dir.mkdir()
    return {
        "source": source,
        "md_dir": md_dir,
        "img_dir": img_dir,
        "failed": source / "_failed_ingestion",
        "error_log": tmp_path / "error_log.txt",
    }


@pytest.fixture
def sample_png(tmp_dirs):
    """Create a minimal valid 1x1 red PNG file in the source directory."""
    img_path = tmp_dirs["source"] / "test_screenshot.png"
    img_path.write_bytes(_minimal_png())
    return img_path


def _minimal_png() -> bytes:
    """Generate a minimal valid 1x1 red PNG (67 bytes)."""
    import zlib

    def _chunk(chunk_type: bytes, data: bytes) -> bytes:
        c = chunk_type + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    raw_data = zlib.compress(b"\x00\xff\x00\x00")  # filter=none, R=255 G=0 B=0
    return sig + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", raw_data) + _chunk(b"IEND", b"")


@pytest.fixture
def mock_vision_result():
    """Standard mock VisionResult data."""
    return {
        "extracted_text": "Hello World — test text",
        "description": "Screenshot of a test interface showing Hello World text.",
        "tags": ["test", "screenshot", "ui"],
        "slug": "test-interface-hello-world",
    }


@pytest.fixture
def mock_vision_json(mock_vision_result):
    """JSON string matching a Claude vision response."""
    return json.dumps(mock_vision_result)
