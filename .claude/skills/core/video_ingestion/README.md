# video_ingestion — IG reels + YouTube → transcript + summary → routed markdown

Sibling to `inbox_ingestion/`. Same naming + frontmatter convention so the existing `inbox_routing/` pipeline picks up the output and routes to dept context folders automatically.

## Cost profile

- **YouTube URL:** ~$0.005-0.02 per video. Captions pulled via `youtube-transcript-api` (free, instant). One Claude summary call.
- **Instagram / TikTok / X / Vimeo:** ~$0.005-0.02 per video. yt-dlp downloads audio (no transcoding needed), faster-whisper transcribes locally on CPU, one Claude summary call.

10-30× cheaper per asset than `inbox_ingestion` (image vision + research enrichment).

## Setup (one-time)

```bash
cd "CORE/video_ingestion"
pip install -r requirements.txt
```

Reuses `../inbox_ingestion/.env` for the `ANTHROPIC_API_KEY` — no separate config needed.

First run on a non-YouTube URL will download the faster-whisper `small` model (~460MB). Set `WHISPER_MODEL_SIZE=tiny` in env for a 75MB model (faster, lower accuracy) or `small`/`medium`/`large-v3` for higher.

## Usage

### Single URL
```bash
python -m video_ingestion "https://www.instagram.com/reel/DWoqE9gD7iA/"
python -m video_ingestion "https://www.youtube.com/watch?v=..."
```

### Batch from Obsidian Instagram batch files
Scans `INBOX/clips/Instagram*.md` for any URLs not yet processed:
```bash
python -m video_ingestion --batch
```

### Force re-process
```bash
python -m video_ingestion <url> --force
```

## Output

Markdown sidecar lands in `INBOX/processed/` named `YYYY-MM-DD-HHMM-<slug>.md`, with frontmatter:
- `source: video-ingestion`
- `original_url: <url>`
- `platform: youtube | instagram | tiktok | x | vimeo | other`
- `transcription_method: youtube-captions | whisper-local`
- `tags: [...]` and `dept_hints: [...]` from Claude summary
- `priority: high` if any priority_rules signal matched (e.g., YC content)

Body sections:
1. ⭐ Priority block (if applicable)
2. `## Summary` — 2-3 sentence Claude-generated summary
3. `## Key Quotes` — verbatim lines from the transcript
4. `## Ways to Implement` — short imperative bullets, what the operator could build
5. `## Source` — URL, platform, title, uploader, duration
6. `## Transcript` — full transcript text

The next `inbox_routing/` run picks up the file and moves it to the right dept's `context/YYYY-MM/` folder based on tag scoring.

## Schedule

Manually run for now. Future: hook into the same `Vault-InboxIngestion` Windows scheduled task or create a sibling task on the same every-3-day-noon cadence.
