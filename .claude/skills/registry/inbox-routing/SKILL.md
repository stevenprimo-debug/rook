---
name: inbox-routing
description: >
  Route processed markdown captures to the correct department folder in your Obsidian vault based on keyword scoring. Trigger when the user says "route my inbox", "run the router", "file my captures", "organize my notes", "why didn't this file to the right folder", or asks about routing/indexing. Also trigger on "regenerate my indexes", "update MASTER_INDEX", or "run inbox routing".
---

# Inbox Routing

Automatically files processed markdown notes into the right folder in your vault using keyword scoring. No manual tagging or drag-and-drop — every capture goes where it belongs.

## How it works

1. Scan three source directories: `INBOX/processed/`, `INBOX/clips/`, `Clippings/`
2. For each `.md` file, count keyword hits per department (searches filename + frontmatter tags + body)
3. Move the file to `agents/<primary-dept>/context/YYYY-MM/`
4. Write cross-reference stubs in secondary departments if the file scores highly there too
5. Regenerate all `INDEX.md` files and `MASTER_INDEX.md` at vault root

## Setup (one-time)

No pip install needed — stdlib only.

**Create a keyword file for each department:**

`agents/<dept>/memory/capture_routing_keywords.md`

```yaml
---
dept: MARKETING
keywords: [instagram, funnel, content, audience, social, viral, growth, linkedin, newsletter]
---

Keywords that route captures to this department.
```

Create one of these for each folder in your `agents/` directory. The more specific your keywords, the more accurate the routing.

## Usage

```bash
cd CORE

# Route all pending files
python -m inbox_routing

# Preview routing without moving anything
python -m inbox_routing --dry-run

# Regenerate indexes only (no routing)
python -m inbox_routing.gen_indexes
```

## Routing logic

| Condition | Action |
|---|---|
| File has highest keyword score | Moved to that dept as primary |
| File scores ≥ 4 hits AND ≥ 50% of primary score | Cross-ref stub written in that dept too |
| All scores = 0 | File left in place, logged as WARN |
| `dept_routed:` already in frontmatter | Existing primary respected, secondaries recomputed |

Tie-breaking: alphabetical by dept name.

## What gets added to frontmatter

```yaml
dept_routed: MARKETING
dept_secondary: [PRIMOLABS, CEO]
routing_score: "CEO=2, MARKETING=12, PRIMOLABS=5"
```

## Indexes generated automatically

After every routing pass, two indexes are regenerated:

**`agents/<dept>/context/INDEX.md`** — per-dept index with monthly buckets, links to every file, marks cross-reference stubs.

**`MASTER_INDEX.md`** (vault root) — three views of everything:
- **By Date** — newest month first, dept label on every file
- **By Department** — dept summary with file count + link to dept index
- **By Topic Tag** — tags with ≥2 files (signal filter, reduces noise)

## Folder layout

```
YOUR-VAULT/
├── MASTER_INDEX.md               ← cross-dept index, regenerated on every run
├── INBOX/
│   ├── processed/                ← source (files moved out after routing)
│   ├── clips/                    ← source (URL batch files, also scanned)
│   └── processed_images/         ← images (not routed, kept as-is)
├── Clippings/                    ← source (Obsidian Web Clipper output)
└── agents/
    ├── <dept>/
    │   ├── context/
    │   │   ├── INDEX.md          ← auto-regenerated
    │   │   └── YYYY-MM/
    │   │       └── <filename>.md ← routed captures land here
    │   └── memory/
    │       └── capture_routing_keywords.md  ← YOU configure this
```

## Tuning routing accuracy

- **Too many false positives in a dept?** Remove overly generic keywords (e.g., "tool", "system", "app")
- **Files not routing to the right place?** Add more specific terms your content actually uses
- **Same file always goes to wrong dept?** Check if that dept has a higher keyword density than expected — trim its list or add more specific terms to the correct dept
- **Dry run first** when changing keyword files: `python -m inbox_routing --dry-run` shows routing decisions without moving anything

## Requirements

None — pure Python stdlib.
