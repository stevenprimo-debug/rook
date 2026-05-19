"""Transcription — two paths.

YouTube → youtube-transcript-api (free, auto-captions, instant).
Everything else → yt-dlp downloads audio → faster-whisper transcribes locally.
"""

import logging
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .config import AUDIO_SCRATCH_DIR, WHISPER_MODEL_SIZE, MAX_VIDEO_SECONDS

logger = logging.getLogger(__name__)

YOUTUBE_HOSTS = ("youtube.com", "youtu.be", "www.youtube.com", "m.youtube.com")
INSTAGRAM_HOSTS = ("instagram.com", "www.instagram.com")


@dataclass
class TranscriptionResult:
    transcript: str            # full text
    source_method: str         # "youtube-captions" | "whisper-local"
    duration_seconds: float    # video length
    language: str              # detected language code
    title: Optional[str] = None
    uploader: Optional[str] = None
    upload_date: Optional[str] = None  # YYYYMMDD


def detect_platform(url: str) -> str:
    """Return 'youtube', 'instagram', 'tiktok', 'x', 'vimeo', or 'other'."""
    lower = url.lower()
    if any(h in lower for h in YOUTUBE_HOSTS):
        return "youtube"
    if any(h in lower for h in INSTAGRAM_HOSTS):
        return "instagram"
    if "tiktok.com" in lower:
        return "tiktok"
    if "twitter.com" in lower or "x.com" in lower:
        return "x"
    if "vimeo.com" in lower:
        return "vimeo"
    return "other"


def extract_youtube_id(url: str) -> Optional[str]:
    """Pull 11-char video ID out of a YT URL. Handles watch?v=, youtu.be/, embed/."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([A-Za-z0-9_-]{11})",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def transcribe_youtube(url: str) -> TranscriptionResult:
    """Pull YT auto-captions via youtube-transcript-api. Free, instant."""
    from youtube_transcript_api import YouTubeTranscriptApi

    video_id = extract_youtube_id(url)
    if not video_id:
        raise ValueError(f"Could not extract YouTube video ID from URL: {url}")

    api = YouTubeTranscriptApi()
    fetched = api.fetch(video_id)
    # FetchedTranscript supports iteration of FetchedTranscriptSnippet objects with .text and .duration
    snippets = list(fetched)
    transcript_text = " ".join(s.text for s in snippets if s.text and s.text.strip())
    duration = sum(s.duration for s in snippets) if snippets else 0.0
    language = getattr(fetched, "language_code", "en")

    # Get metadata via yt-dlp (no download) for title/uploader/date
    title, uploader, upload_date = _fetch_metadata_only(url)

    return TranscriptionResult(
        transcript=transcript_text,
        source_method="youtube-captions",
        duration_seconds=duration,
        language=language,
        title=title,
        uploader=uploader,
        upload_date=upload_date,
    )


def _fetch_metadata_only(url: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """yt-dlp metadata fetch with no download. Returns (title, uploader, upload_date)."""
    import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return (
            info.get("title"),
            info.get("uploader") or info.get("channel"),
            info.get("upload_date"),
        )
    except Exception as e:
        logger.warning("Metadata fetch failed for %s: %s", url, e)
        return None, None, None


def transcribe_via_whisper(url: str) -> TranscriptionResult:
    """Download audio with yt-dlp, transcribe with faster-whisper."""
    import yt_dlp
    from faster_whisper import WhisperModel

    audio_path = _download_audio(url)
    title, uploader, upload_date = _fetch_metadata_only(url)

    try:
        model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")
        segments, info = model.transcribe(str(audio_path), beam_size=1, vad_filter=True)
        text = " ".join(seg.text.strip() for seg in segments).strip()

        # VAD sometimes strips all audio on music-heavy reels — retry without it
        if not text.strip():
            logger.info("VAD produced empty transcript — retrying without VAD filter")
            segments, info = model.transcribe(str(audio_path), beam_size=1, vad_filter=False)
            text = " ".join(seg.text.strip() for seg in segments).strip()

        return TranscriptionResult(
            transcript=text,
            source_method="whisper-local",
            duration_seconds=info.duration,
            language=info.language,
            title=title,
            uploader=uploader,
            upload_date=upload_date,
        )
    finally:
        try:
            audio_path.unlink(missing_ok=True)
        except Exception:
            pass


def _download_audio(url: str) -> Path:
    """yt-dlp downloads bestaudio to scratch dir. Returns path to audio file.

    Picks bestaudio format that needs no transcoding (m4a or webm) — avoids
    requiring a separate ffmpeg install for the download step. faster-whisper's
    PyAV backend reads m4a/webm directly.
    """
    import yt_dlp

    # Use a fixed template so we can find the output deterministically
    out_template = str(AUDIO_SCRATCH_DIR / "%(id)s.%(ext)s")

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio",
        "outtmpl": out_template,
        "noplaylist": True,
        "max_duration": MAX_VIDEO_SECONDS,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded = ydl.prepare_filename(info)

    audio_path = Path(downloaded)
    if not audio_path.exists():
        # yt-dlp may have changed the extension during post-processing — find it by ID
        vid_id = info.get("id", "")
        candidates = list(AUDIO_SCRATCH_DIR.glob(f"{vid_id}.*"))
        if not candidates:
            raise RuntimeError(f"Audio download succeeded but file not found for {url}")
        audio_path = candidates[0]

    return audio_path


def _download_thumbnail(url: str) -> Optional[Path]:
    """Download reel/video thumbnail via yt-dlp. Returns path to image file or None."""
    import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "writethumbnail": True,
        "outtmpl": str(AUDIO_SCRATCH_DIR / "%(id)s.%(ext)s"),
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            vid_id = info.get("id", "")
    except Exception as e:
        logger.warning("Thumbnail download failed for %s: %s", url, e)
        return None

    image_exts = {".jpg", ".jpeg", ".png", ".webp"}
    for candidate in AUDIO_SCRATCH_DIR.glob(f"{vid_id}.*"):
        if candidate.suffix.lower() in image_exts:
            return candidate
    return None


def transcribe_via_vision(url: str) -> TranscriptionResult:
    """Vision fallback for silent/music reels: download thumbnail → Claude Vision.

    Captures on-screen text, hooks, title cards, and overlays that Whisper misses
    because there's no speech track.
    """
    import anthropic
    import base64

    from .config import ANTHROPIC_API_KEY

    title, uploader, upload_date = _fetch_metadata_only(url)
    thumb_path = _download_thumbnail(url)

    extracted = ""
    if thumb_path and thumb_path.exists():
        try:
            ext = thumb_path.suffix.lower().lstrip(".")
            mime = f"image/{'jpeg' if ext in ('jpg', 'jpeg') else ext}"
            image_data = base64.standard_b64encode(thumb_path.read_bytes()).decode("utf-8")

            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            resp = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": mime, "data": image_data}},
                        {"type": "text", "text": (
                            "This is a thumbnail from an Instagram reel or social video. "
                            "Extract ALL visible text verbatim — hooks, title cards, overlays, captions, CTAs. "
                            "Then describe what's shown in 1-2 sentences. "
                            "Format: first the extracted text, then a line break, then your description."
                        )},
                    ],
                }],
            )
            extracted = resp.content[0].text.strip()
            logger.info("Vision extracted %d chars from thumbnail", len(extracted))
        except Exception as e:
            logger.warning("Vision fallback failed: %s", e)
        finally:
            try:
                thumb_path.unlink(missing_ok=True)
            except Exception:
                pass
    else:
        logger.warning("No thumbnail found for Vision fallback: %s", url)

    return TranscriptionResult(
        transcript=extracted,
        source_method="vision-thumbnail",
        duration_seconds=0.0,
        language="visual",
        title=title,
        uploader=uploader,
        upload_date=upload_date,
    )


def transcribe(url: str) -> TranscriptionResult:
    """Top-level entry: dispatch by platform.

    YouTube → captions API (free, instant).
    Everything else → Whisper local.
    Vision fallback handled in pipeline.py after empty-transcript check.
    """
    platform = detect_platform(url)

    if platform == "youtube":
        try:
            return transcribe_youtube(url)
        except Exception as e:
            logger.warning("YT captions failed for %s (%s) — falling back to Whisper", url, e)
            return transcribe_via_whisper(url)

    return transcribe_via_whisper(url)
