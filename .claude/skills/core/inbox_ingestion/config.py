"""Configuration for the Drive → COWORK INBOX ingestion pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

VISION_MODEL = "claude-sonnet-4-6"

# Research enrichment: when True, each image's vision-extracted targets get
# web-searched (up to 6 web_search invocations per image) and synthesized as
# markdown research notes. Expensive but Primo values the enrichment — that's
# why we batch via the every-3-day schedule rather than killing it. Default ON.
# To skip research for a one-off run: $env:INBOX_ENABLE_RESEARCH="0"
ENABLE_RESEARCH = os.environ.get("INBOX_ENABLE_RESEARCH", "1") == "1"

# Source: Google Drive root — iPhone screenshot button-action lands files here.
# Only top-level images are scanned. Subfolders are skipped.
SOURCE_DIR = Path(os.environ.get(
    "INBOX_SOURCE_DIR",
    r"G:\My Drive"
))

# Destination: COWORK INBOX folders
COWORK_ROOT = Path(os.environ.get(
    "COWORK_ROOT",
    r"C:\Users\User\Desktop\PRIMOLABS"
))

PROCESSED_MD_DIR = COWORK_ROOT / "INBOX" / "processed"
PROCESSED_IMG_DIR = COWORK_ROOT / "INBOX" / "processed_images"

# Failures move to a quarantine folder at Drive root so they don't get re-scanned.
# Successful ingests are DELETED from source — Drive root staying empty = "all caught up".
SOURCE_FAILED_DIR = SOURCE_DIR / "_failed_ingestion"

ERROR_LOG = Path(__file__).parent / "error_log.txt"

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}

MAX_SLUG_LENGTH = 60
