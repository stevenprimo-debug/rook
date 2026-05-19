"""Configuration for video ingestion pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Reuse the same .env as inbox_ingestion (one ANTHROPIC_API_KEY for the org)
load_dotenv(Path(__file__).parent.parent / "inbox_ingestion" / ".env", override=True)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

SUMMARY_MODEL = "claude-sonnet-4-6"

COWORK_ROOT = Path(os.environ.get(
    "COWORK_ROOT",
    r"C:\Users\User\Desktop\PRIMOLABS"
))

# Output: same INBOX/processed as image ingest so the existing inbox_routing picks it up
PROCESSED_MD_DIR = COWORK_ROOT / "INBOX" / "processed"

# Where IG/YT URL batch files live — scan ALL .md (not just Instagram*.md)
INSTAGRAM_BATCH_DIR = COWORK_ROOT / "INBOX" / "clips"
INSTAGRAM_BATCH_GLOB = "*.md"

# Obsidian clipper drops here — also scanned for video URLs
CLIPPINGS_DIR = COWORK_ROOT / "Clippings"

# Permanent VIDEO/ archive — written alongside INBOX/processed/ copy; never touched by router
VIDEO_ARCHIVE_DIR = COWORK_ROOT / "VIDEO"

# Track processed URLs so we don't re-transcribe
PROCESSED_URLS_LOG = Path(__file__).parent / "_processed_urls.txt"

# Audio scratch dir — files deleted after transcription
AUDIO_SCRATCH_DIR = Path(__file__).parent / "_audio_scratch"
AUDIO_SCRATCH_DIR.mkdir(exist_ok=True)

ERROR_LOG = Path(__file__).parent / "error_log.txt"

# faster-whisper model: 'tiny', 'base', 'small', 'medium', 'large-v3'
# 'small' is the sweet spot — ~460MB, English-good, ~6x realtime on CPU
WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "small")

# Skip videos longer than this (in seconds). 90 min default — most podcasts/talks fit.
MAX_VIDEO_SECONDS = int(os.environ.get("MAX_VIDEO_SECONDS", "5400"))

# Slug max length for filenames
MAX_SLUG_LENGTH = 60
