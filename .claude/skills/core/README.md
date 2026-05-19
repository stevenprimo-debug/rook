# Obsidian Capture — AI-Powered Knowledge Pipelines

Four tools that turn Obsidian into a self-organizing knowledge base. Every capture — phone screenshot, web clip, IG reel, YouTube video — lands in the right department automatically with a full transcript or structured note attached.

## How to use it (the short version)

Install Claude Code, add the `obsidian-capture` skill, then just type:

```
/capture                         ← process + organize everything
/capture "Instagram 5.5.26"      ← process a specific batch file
/capture https://...             ← process one video URL
/capture route                   ← organize what's already been processed
```

That's the whole interface. The rest of this README is for people who want to understand what's happening under the hood or customize the system.

---

## The Four Pipelines

```
[Phone screenshot]        ──► inbox_ingestion  ──► INBOX/processed/ ──►┐
[Web Clipper clip]        ──►┐                                         │
[FB post / article / any] ──►┤ Clippings/                             ├──► inbox_routing ──► agents/<dept>/context/YYYY-MM/
[IG/YT/FB video URL]      ──► video_ingestion  ──► INBOX/processed/ ──►│               └──► VIDEO/ (permanent archive)
[HTML document]           ──► html-to-pdf      ──► .pdf output          ┘
```

**Rule of thumb:**
- Link to a video (IG reel, YT, FB video, TikTok) → `video_ingestion` → `VIDEO/`
- Link to a page, post, or article → Obsidian Web Clipper → `Clippings/` → routed
- Phone screenshot → Google Drive → `inbox_ingestion` → routed

Run order when running all at once: `python run_daily.py`

---

## What gets installed — full folder structure

`/capture setup` (or `python install.py`) creates the following inside your Obsidian vault. Nothing existing is deleted or modified.

```
YOUR-VAULT/
│
├── VIDEO/                           ← CREATED — permanent archive for all video transcripts
│   ├── 2026-05-05-0930-slug.md      ←   one file per processed video (never moved or deleted)
│   └── Instagram 5.5.26.md          ←   your batch notes with labels (moved here after processing)
│
├── INBOX/                           ← CREATED — staging area (files pass through, then get filed)
│   ├── clips/                       ←   drop your video URL batch files here
│   ├── processed/                   ←   pipelines write here; router moves files out after filing
│   └── processed_images/            ←   original screenshot images kept here permanently
│
├── Clippings/                       ← CREATED if missing (Web Clipper default — may already exist)
│   └── My clipped article.md        ←   web clips land here automatically
│
├── agents/                     ← CREATED — final destination for all routed captures
│   ├── MARKETING/
│   │   ├── context/
│   │   │   ├── INDEX.md             ←   auto-generated dept index (regenerated on every run)
│   │   │   └── 2026-05/
│   │   │       └── routed-file.md   ←   captures routed here, organized by month
│   │   └── memory/
│   │       └── capture_routing_keywords.md  ← YOU configure this (what routes here)
│   ├── PERSONAL/
│   │   └── context/ ...
│   └── (add as many departments as you want)
│
└── MASTER_INDEX.md                  ← CREATED — auto-generated cross-dept index of everything
```

**Nothing in your existing vault is touched.** The installer only creates new folders.

**Recommended:** Start with a fresh Obsidian vault so the structure is clean from day one. If adding to an existing vault, all new folders appear alongside your existing notes — nothing is overwritten.

---

## Capture Methods — How content gets into the system

### Method 1: Phone screenshot → Google Drive

**iPhone setup (one-time):**
1. Install **Google Drive** app on iPhone
2. Take a screenshot normally (side button + volume up)
3. In the Photos share sheet, tap **Save to Drive** — or create an iOS Shortcut to do this automatically on every screenshot

The screenshot lands in your **Google Drive root** (`My Drive/`). The next `inbox_ingestion` run picks it up, runs Claude Vision on it, and deletes it from Drive. Drive root empty = all caught up.

**What gets captured:** Any screenshot — tweets, LinkedIn posts, articles, code, whiteboard photos, receipts, app screens. Claude Vision extracts all visible text and tags it automatically.

---

### Method 2: Obsidian Web Clipper → Clippings/

**Desktop setup (one-time):**
1. Install the **Obsidian Web Clipper** browser extension (Chrome, Firefox, Safari, Edge)
2. Open extension settings → set **Vault** to your exact Obsidian vault name (must match exactly — case sensitive)
3. Set **Note location** to `Clippings/`
4. Click the extension icon on any page → clip → it lands in `Clippings/` immediately

**iPhone/iPad setup (one-time):**
1. Install **Obsidian** on iPhone with your vault open
2. Install the Web Clipper extension in **Safari** via App Extensions
3. On any page in Safari: Share → Web Clipper → saves to `Clippings/` in your vault

**What gets captured:** The full text of any webpage — articles, FB posts, LinkedIn posts, Twitter threads, documentation, anything with a URL. Structured as markdown automatically.

The next `inbox_routing` run picks up everything in `Clippings/` and files it to the right department.

---

### Method 3: Video URL batch file → VIDEO/

1. Create a `.md` file in `INBOX/clips/` (name it anything — e.g., `Instagram 5.5.26.md`)
2. Paste IG reel links, YouTube links, or FB video links — one per line, mixed with your own notes is fine
3. Run `python -m video_ingestion --batch`
4. Transcripts land in `VIDEO/`, your batch note moves to `VIDEO/` alongside them

---

## 1. `inbox_ingestion` — Phone screenshots → structured markdown

**What it does:** Scans `G:\My Drive` (top level) for iPhone screenshots, passes each through Claude Vision to extract text + description + tags, writes a structured markdown file, deletes from Drive, moves to `INBOX/processed/`.

Optional research enrichment: web-searches entities found in the image and appends synthesized research notes.

**Setup:**
```bash
cd CORE/inbox_ingestion
pip install -r requirements.txt   # anthropic, pillow, python-dotenv
cp .env.example .env              # add ANTHROPIC_API_KEY
```

**Usage:**
```bash
python -m inbox_ingestion          # scan Drive, process all images
INBOX_ENABLE_RESEARCH=0 python -m inbox_ingestion   # skip research enrichment
```

**Cost:** ~$0.05–0.20 per image (Vision + optional research web searches). Research enrichment fires up to 6 web searches per image — disable for high-volume days.

**Output frontmatter fields:** `source`, `captured_date`, `image_ref`, `description`, `tags`, `extracted_text`

---

## 2. `video_ingestion` — IG reels + YouTube → transcript + summary

**What it does:** Takes IG/YouTube URLs from batch `.md` files in `INBOX/clips/` or `Clippings/`, downloads audio (IG/TikTok) or fetches captions (YouTube), transcribes with faster-whisper (local CPU), summarizes with Claude, writes markdown to `INBOX/processed/` AND a permanent copy to `VIDEO/`.

**Setup:**
```bash
cd CORE/video_ingestion
pip install -r requirements.txt   # yt-dlp, faster-whisper, anthropic, youtube-transcript-api
# Reuses ../inbox_ingestion/.env — no separate config needed
```

First non-YouTube run downloads the faster-whisper `small` model (~460MB). Set `WHISPER_MODEL_SIZE=tiny` in env for a lighter model.

**Usage:**
```bash
# Single URL
python -m video_ingestion "https://www.instagram.com/reel/DWoqE9gD7iA/"
python -m video_ingestion "https://www.youtube.com/watch?v=..."

# Batch (scans INBOX/clips/*.md + Clippings/*.md)
python -m video_ingestion --batch

# Retroactively process a file that was already moved by the router
python -m video_ingestion --source-file "path/to/file-with-urls.md"

# Force re-process a URL already in the log
python -m video_ingestion <url> --force
```

**Cost:** ~$0.005–0.02 per video. yt-dlp and Whisper are free/local. One Claude summary call per video. 10–30× cheaper than running Vision on screenshots.

**Output:** `VIDEO/<slug>.md` (permanent) + `INBOX/processed/<slug>.md` (routed). Body sections: Summary, Key Quotes, Ways to Implement, Source, full Transcript.

**Batch file format:** Any `.md` file containing IG/YT URLs, one per line. File can have frontmatter and notes — the pipeline extracts only URLs matching `instagram.com/reel|p|tv` or `youtube.com/watch|shorts` or `youtu.be/`.

---

## 3. `inbox_routing` — Route everything to dept context folders

**What it does:** Scans `INBOX/processed/`, `INBOX/clips/`, and `Clippings/` for `.md` files. Scores each file against per-dept keyword lists. Moves the file to `agents/<primary-dept>/context/YYYY-MM/`. Writes cross-ref stubs for secondary departments. Regenerates all `INDEX.md` files and `MASTER_INDEX.md` at vault root.

**Setup:** No pip install. Pure stdlib. Just configure keyword files — one per department.

**Keyword file location:** `agents/<dept>/memory/capture_routing_keywords.md`

```yaml
---
dept: MARKETING
keywords: [instagram, funnel, content, audience, social, viral, growth]
---
```

**Usage:**
```bash
cd CORE
python -m inbox_routing           # route all pending files
python -m inbox_routing --dry-run # preview routing without moving files
python -m inbox_ingestion.gen_indexes  # regenerate indexes only (no routing)
```

**Routing logic:**
- Score = count of case-insensitive keyword hits in (filename + frontmatter tags + body)
- Primary dept = highest score (ties → alphabetical)
- Secondary dept = score ≥ 4 AND ≥ 50% of primary score
- Score = 0 → file left in place, logged as WARN

**Output:** `agents/<dept>/context/YYYY-MM/<filename>.md` with added frontmatter: `dept_routed`, `dept_secondary`, `routing_score`

---

## 4. `html-to-pdf` — HTML documents → design-quality PDFs

**What it does:** Wraps Playwright headless Chromium to convert HTML files to PDF. Output matches exactly what Chrome renders — correct fonts, embedded images, brand colors.

**Setup:**
```bash
pip install playwright
playwright install chromium
```

**Usage:**
```bash
# Single file — seamless (single tall page, default)
python html2pdf.py proposal.html

# Single file — paginated (letter pages with footers)
python html2pdf.py proposal.html --paginated

# Directory — convert all *.html files
python html2pdf.py ./proposals/

# Custom output path
python html2pdf.py proposal.html -o output/proposal-v5.pdf
```

**Two modes:**
- `--seamless` (default): single tall PDF page sized to full content height. No breaks, no headers. Looks identical to scrolling the HTML in a browser. Best for proposals, scopes, marketing docs.
- `--paginated`: traditional Letter/A4 pages with page-number footers. Use when recipient needs to print individual pages.

---

## 5. `run_daily.py` — Orchestrator (run all in correct order)

```bash
cd CORE
python run_daily.py
```

Runs in sequence: `video_ingestion --batch` → `inbox_ingestion` → `inbox_routing` (+ gen_indexes). Order matters: routing must run last so it sees all freshly processed files.

---

## Configuration

All pipelines share a single `.env` at `CORE/inbox_ingestion/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
VAULT_ROOT=C:\Users\YourName\Desktop\YOUR-VAULT-NAME
INBOX_ENABLE_RESEARCH=1
WHISPER_MODEL_SIZE=small
```

---

## Finding your captures

| Where to look | What's there |
|---|---|
| `VIDEO/` | Every video transcript, permanent, never moved |
| `agents/<dept>/context/YYYY-MM/` | Everything routed to that dept |
| `MASTER_INDEX.md` (vault root) | Cross-dept index: by date, by dept, by tag |
| `agents/<dept>/context/INDEX.md` | Dept-scoped index with monthly buckets |

---

## Requirements summary

| Pipeline | Key dependencies |
|---|---|
| `inbox_ingestion` | `anthropic`, `pillow`, `python-dotenv`, Google Drive mounted |
| `video_ingestion` | `yt-dlp`, `faster-whisper`, `youtube-transcript-api`, `anthropic` |
| `inbox_routing` | stdlib only |
| `html-to-pdf` | `playwright` + Chromium |
