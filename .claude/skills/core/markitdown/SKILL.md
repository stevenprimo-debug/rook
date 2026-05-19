---
name: markitdown
description: >
  Universal file → markdown conversion. PDF, DOCX, XLSX, PPTX, HTML, audio, video,
  YouTube URLs, EPub, ZIP, images (OCR) → clean markdown. The "Input" layer of the
  Universal Stack pipeline.
source: Microsoft (MIT-licensed, AutoGen team)
upstream: https://github.com/microsoft/markitdown
---

# markitdown

Canonical `file_ingest()` for every the Stack agent. Customer uploads any artifact;
agent normalizes it to markdown before reasoning over it.

## Install status

**Source vendored at `skills/core/markitdown/src/` for upstream-disappearance safety.**
Original repo: [microsoft/markitdown](https://github.com/microsoft/markitdown) (MIT-licensed).
Vendored 2026-05-14 via shallow clone; `.git/` removed (no nested repos).

Two install paths supported:

```bash
# Standard (PyPI, recommended for end users)
python -m pip install "markitdown[all]"

# Vendored (offline / upstream-down scenarios)
python -m pip install "skills/core/markitdown/src/packages/markitdown[all]"
```

Binary after install: `<python-scripts>/markitdown.exe` (Windows) or `markitdown` (Unix).

## How agents invoke it

Agents call the canonical wrapper:

```python
markdown = file_ingest(path_or_url)
```

Under the hood:

```bash
markitdown <path> -o <out.md>
markitdown < <path>            # stdin → stdout
python -m markitdown <path>    # module form (no PATH dependency)
```

## Supported inputs

| Type | Extensions |
|---|---|
| PDF | `.pdf` (text-layer; scanned needs OCR pre-pass) |
| Office | `.docx`, `.xlsx`, `.pptx` |
| Web | `.html`, URLs |
| Audio | `.mp3`, `.wav`, `.m4a` (Whisper) |
| Video | `.mp4`, `.mov`, YouTube URLs |
| Image | `.png`, `.jpg` (OCR + optional LLM caption) |
| Archive | `.zip`, `.epub` |

## Cross-reference

The **Input** capability in `agents/_template/SKILL.md` → "Universal Stack Capabilities".
Paired with Graphify (Synthesis) + Obsidian CLI (Vault I/O). All 20 agents inherit
`file_ingest()`; none re-implement it.

## Verification

`python -m markitdown --help` returns usage. Confirmed 2026-05-14.
