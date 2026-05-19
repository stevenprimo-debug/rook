"""Daily COWORK pipeline orchestrator.

Run order is critical — video_ingestion must run BEFORE inbox_routing, because
the router moves batch files from INBOX/clips/ to dept context/ on every pass.

Usage:
    cd "C:/Users/User/Desktop/PRIMOLABS/CORE"
    python run_daily.py

Phases:
    1. video_ingestion --batch   (IG/YT URLs → transcripts in INBOX/processed/ + VIDEO/)
    2. inbox_ingestion           (screenshots/images → processed markdown)
    3. inbox_routing             (route INBOX/processed/ + clips/ + Clippings/ → dept context/)
                                 (also calls gen_indexes → per-dept INDEX.md + MASTER_INDEX.md)
"""

import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

CORE_DIR = Path(__file__).parent


def _run(module: str, *args: str, desc: str) -> bool:
    logger.info("--- %s ---", desc)
    result = subprocess.run(
        [sys.executable, "-m", module, *args],
        cwd=CORE_DIR,
    )
    ok = result.returncode == 0
    if not ok:
        logger.error("%s exited with code %d", module, result.returncode)
    return ok


def main() -> int:
    logger.info("=== COWORK Daily Pipeline ===")

    _run("video_ingestion", "--batch", desc="[1/3] video_ingestion  (IG/YT → transcripts)")
    _run("inbox_ingestion",            desc="[2/3] inbox_ingestion  (images → markdown)")
    _run("inbox_routing",              desc="[3/3] inbox_routing    (route + gen_indexes)")

    logger.info("=== Done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
