"""Video ingestion pipeline: IG reels + YouTube → transcripts + summaries → routed markdown.

Two transcription paths:
- YouTube URLs → youtube-transcript-api (free, uses YT auto-captions, instant)
- Everything else (IG, TikTok, X, Vimeo) → yt-dlp downloads audio → faster-whisper transcribes locally

Output: markdown sidecar in INBOX/processed/ with same naming + frontmatter convention as
image ingest. Routed to dept context/ on next inbox_routing run.
"""
