---
name: obsidian-capture
description: >
  Process and organize captures into Obsidian. Trigger on: /capture,
  /capture setup, /capture install, "process my clips", "process this reel", "process this video",
  "route my inbox", "organize my notes", "run the pipeline", "set up capture", or when the user
  pastes a video URL and wants it processed. Also trigger when the user asks if the system is
  installed or configured.
---

# Vault Capture

One command to capture, process, and organize everything in your Obsidian vault.

---

## First time? Run setup

```
/capture setup
```

That installs everything automatically — Python packages, folder structure, API key config. Takes about 2 minutes. You never need to touch the terminal again after this.

---

## Daily usage

```
/capture                          — process + organize everything
/capture "Instagram 5.5.26"       — process a specific batch file by name
/capture https://instagram.com/…  — process a single video URL
/capture route                    — organize what's already been clipped
```

---

## How Claude handles each command

### `/capture setup` or `/capture install`

Run the self-installer. Claude executes:

```bash
cd "<VAULT_ROOT>/CORE"
python install.py
```

The installer:
1. Checks Python version (needs 3.10+)
2. Installs all packages: `anthropic`, `yt-dlp`, `faster-whisper`, `youtube-transcript-api`, `pillow`, `playwright`
3. Installs Playwright's Chromium browser
4. Creates all required folders (`VIDEO/`, `INBOX/clips/`, `INBOX/processed/`, `Clippings/`, etc.)
5. Prompts for Anthropic API key and Google Drive path
6. Tests the API connection
7. Prints confirmation

If anything fails, Claude reads the error and fixes it.

---

### `/capture` (no args)

Run the full daily pipeline in the correct order:

```bash
cd "<VAULT_ROOT>/CORE"
python run_daily.py
```

Order: video transcription → screenshot ingestion → routing + indexing.

Claude reports: how many videos processed, images processed, files routed, any failures.

---

### `/capture "filename"` or `/capture filename`

Find the batch file and process all video URLs in it.

Claude checks `INBOX/clips/` for a file matching that name, then runs:

```bash
cd "<VAULT_ROOT>/CORE"
python -m video_ingestion --source-file "INBOX/clips/<filename>.md"
python -m inbox_routing
```

The batch file moves to `VIDEO/` after processing. Transcripts land in `VIDEO/` alongside it.

---

### `/capture <url>`

Process one video URL directly.

```bash
cd "<VAULT_ROOT>/CORE"
python -m video_ingestion "<url>"
python -m inbox_routing
```

Works with: Instagram reels, YouTube, TikTok, Facebook video, Vimeo.

---

### `/capture route`

Skip processing — just route and index what's already been captured.

```bash
cd "<VAULT_ROOT>/CORE"
python -m inbox_routing
```

Use this after clipping a bunch of web pages via Web Clipper and wanting them filed.

---

## What gets captured and where it goes

| What you do | Where it ends up |
|---|---|
| Add video links to a file in `INBOX/clips/` | `VIDEO/` — transcripts + your batch note |
| Clip a page with Obsidian Web Clipper | `agents/<dept>/context/YYYY-MM/` |
| Take an iPhone screenshot → save to Drive | `agents/<dept>/context/YYYY-MM/` |

**Finding anything:**
- Video transcripts → `VIDEO/` folder
- Everything from this month → `MASTER_INDEX.md` at vault root
- Everything in one topic → `agents/<dept>/context/INDEX.md`

---

## What the installer creates in your vault

`/capture setup` adds these folders to your Obsidian vault. Nothing existing is touched or deleted.

```
YOUR-VAULT/
│
├── VIDEO/                        ← NEW — permanent home for all video transcripts
│   ├── 2026-05-05-instagram-...  ←   transcripts land here (never moved)
│   └── Instagram 5.5.26.md       ←   your batch notes with labels land here too
│
├── INBOX/                        ← NEW — staging area (files move through, then get filed)
│   ├── clips/                    ←   drop your video URL batch files here
│   ├── processed/                ←   pipeline writes here before routing
│   └── processed_images/         ←   original screenshot images kept here
│
├── Clippings/                    ← created by Obsidian Web Clipper (may already exist)
│   └── (web clips land here)     ←   router picks these up automatically
│
├── agents/                  ← NEW — where everything gets filed after routing
│   ├── MARKETING/
│   │   └── context/
│   │       └── 2026-05/          ←   routed captures, organized by month
│   ├── PERSONAL/
│   │   └── context/
│   │       └── 2026-05/
│   └── (one folder per dept)     ←   you define your departments and keywords
│
└── MASTER_INDEX.md               ← NEW — auto-generated cross-dept index of everything
```

**Important:** The installer creates folders only — it does not touch any existing notes, folders, or settings in your vault.

**Recommended:** Start with a fresh Obsidian vault so the structure is clean from day one. If you're adding to an existing vault, everything goes into new folders and your existing notes are untouched.

---

## One-time capture setup (after `/capture setup` completes)

**Web Clipper** (browser extension — clips any webpage into Obsidian):
1. Install **Obsidian Web Clipper** for Chrome / Firefox / Safari
2. Set vault name to match your Obsidian vault (exactly, case-sensitive)
3. Set note location to `Clippings/`

**iPhone screenshots** (screenshot → Drive → auto-processed):
1. Install Google Drive app on iPhone
2. Take a screenshot → Photos share sheet → Save to Drive
   Or: create an iOS Shortcut that saves screenshots to Drive automatically

**Video links** (fastest path):
1. Create a `.md` file in `INBOX/clips/`
2. Paste any IG/YT/FB video links, add your own notes on each
3. Type `/capture` — done

---

## If something goes wrong

Claude will read the error output and fix it. Common issues:

- **"Python not found"** → install Python 3.10+ from python.org, then re-run `/capture setup`
- **"API key invalid"** → update `CORE/inbox_ingestion/.env` with your key from console.anthropic.com
- **"No files found"** → make sure your batch file is in `INBOX/clips/` and contains IG/YT URLs
- **"Empty transcript"** → the pipeline tries Whisper → no-VAD Whisper → Vision automatically. If all fail, the reel is music-only with no text overlays.
