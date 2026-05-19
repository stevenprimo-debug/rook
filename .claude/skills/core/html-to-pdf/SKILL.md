---
name: html-to-pdf
description: Convert standalone HTML files to seamless single-page PDFs that match what Chrome renders — no page breaks, no pagination artifacts, no orphan headings. Default mode is `--seamless`: one tall PDF page sized to the full content height, inspired by div riots' html.to.design Figma plugin (https://html.to.design/) which imports HTML into a single Figma frame. Use this skill ANY time the operator asks to "convert this HTML to PDF", "make a PDF of this proposal", "html2pdf", "render this scope as PDF", "turn this HTML into a PDF", "save this proposal as PDF", "export this engineering scope to PDF", "make these seamless", "no page breaks", "single-page PDF", or drops an .html file (with custom fonts, base64 images, and full-bleed cover pages) and wants a PDF version. Also trigger when Chrome's built-in print-to-PDF is breaking — viewport-unit covers (min-height: 100vh) not filling the page, Google Fonts falling back to serif, page breaks splitting headings from content. Paginated mode is available via --paginated for cases that need traditional letter/A4 pages. The CLI lives at .claude/skills/core/html-to-pdf/html2pdf.py and wraps headless Chromium via Playwright. Wide net: any time HTML and PDF are both mentioned in the same sentence, or any time a proposal/scope/SOW HTML needs to ship as a PDF, this skill should fire.
license: Internal — PRIMOLABS
---

# html-to-pdf

Wraps Playwright's headless Chromium to render standalone HTML files as
**seamless single-page PDFs**. Works on any HTML — proposals, scopes,
SOWs, reports, and landing pages with custom fonts, base64-embedded images,
and full-bleed cover pages.

## Why this exists

Chrome's built-in "Print to PDF" breaks on v5 proposals because:

1. **`min-height: 100vh` covers** don't fill the page — Chrome uses the
   browser viewport, not the print page size, so the cover renders short.
2. **Google Fonts** (DM Sans) sometimes don't finish loading before the
   print snapshot, so headings render in the serif fallback.
3. **Page breaks** split headings from content, tables break mid-row, and
   the document looks horrid no matter how clean the HTML is.

This CLI fixes all three. Default behavior is **seamless**: one tall PDF
page sized to full content height, no page breaks at all — the PDF reads
like the HTML scrolled top-to-bottom in a browser. Inspired by div riots'
html.to.design Figma plugin, which imports HTML into a single Figma frame
the same way.

A `--paginated` mode exists for the rare case that letter/A4 pages with
page-number footers are required (e.g., a recipient who insists on
printing one page at a time).

## Quick start

```bash
# Default — seamless single-page PDF
python "CORE/html-to-pdf/html2pdf.py" \
    "~/Desktop/MyProposal.html"

# Custom output path
python ".../html2pdf.py" input.html -o /path/to/output.pdf

# Batch mode — every *.html in the folder becomes a seamless PDF next to it
python ".../html2pdf.py" "~/Desktop/Proposals/"

# Old-school paginated PDF (letter, page-number footer)
python ".../html2pdf.py" input.html --paginated

# Paginated, A4, no footer, tighter margins
python ".../html2pdf.py" input.html --paginated --format A4 \
    --no-headers --margin 0.25in
```

## Install (one-time)

```bash
python -m pip install playwright
python -m playwright install chromium
```

Already done on the operator's Razer 18 (verified 2026-04-28). On a fresh
machine, both lines are required — `pip install` only fetches the Python
wrapper, the second command pulls down ~110 MB of Chromium.

## Modes

### `--seamless` (DEFAULT)

One tall PDF page sized to full HTML content height. No page breaks, no
headers, no footers, no margins. The PDF is the HTML.

How it works:
1. Render at fixed 850 × 1100 px viewport (matches v5 `.page` max-width
   and a Letter-ish height for `vh` resolution).
2. Wait for `networkidle` + `document.fonts.ready` + 400ms settle.
3. Walk the DOM and freeze any computed `vh`/`vw` heights to concrete
   pixel values — so resizing the PDF page to full content length doesn't
   make `min-height: 100vh` blow up the cover to the entire document.
4. Measure full content size (`scrollWidth` × `scrollHeight`).
5. `page.pdf()` with `width=<contentW>px height=<contentH>px margin=0`.

The result on a typical 19-section v5 proposal: a single 8.86" × 148"
PDF page, ~1.5–2 MB. Opens in any PDF reader, scrolls top to bottom like
the original HTML.

### `--paginated`

Traditional multi-page PDF with letter/A4 pages and a page-number footer.
Use when a recipient explicitly needs to print individual pages.

| Flag | Default | Notes |
|---|---|---|
| `--format` | `Letter` | One of `Letter`, `A4`, `Legal`, `Tabloid`. |
| `--margin` | `0.5in` | Applied to all sides. Use `0` to honor the HTML's own `@page` rules. |
| `--landscape` | off | Rotate to landscape. |
| `--no-headers` | off | Drop the page-number footer. |

Footer template uses `<span class="title">` and
`<span class="pageNumber">` / `<span class="totalPages">` — these are
Chromium-native and auto-fill from the document.

## Validation

Tested 2026-04-28 against
`~/Desktop/MyScope_v1.0.html`
(933 KB v5 template, DM Sans, base64 images, full-bleed cover, 19 sections):

**Seamless (default):**
- 1 PDF page
- 8.86" × 148.47" (one continuous scroll)
- 1.8 MB
- Cover renders edge-to-edge with watermark and constellation graphics
- DM Sans loaded for all weights (400–800), no serif fallback
- All 19 sections flow continuously, no break artifacts anywhere
- Brand colors and gradients preserved

**Paginated (`--paginated`):**
- 19 pages, Letter, 0.5in margins, page-number footer
- 2.6 MB
- Available as fallback but not the default for v5 proposals

## Common issues

**Cover renders short / `100vh` doesn't fill** — only happens in paginated
mode. Run with `--paginated --margin 0` to honor the HTML's own
`@page { margin: 0 }` rule. Or just use the default seamless mode where
this isn't a concern.

**Fonts rendering as serif** — Google Fonts CDN unreachable. Check
internet. If it's still happening on a stable connection, bump the
`wait_for_timeout(400)` line in `html2pdf.py` to 1000ms. Long-term:
embed the font as base64 in the HTML or self-host.

**`networkidle` timeout (60s)** — the HTML references something that
never finishes loading. Either inline the external resource as base64
(preferred for portable v5-style proposals) or change
`wait_until="networkidle"` to `wait_until="load"` in `_load_and_settle`.

**Seamless PDF feels too tall to scroll comfortably** — that's the point;
it's a continuous document. If a recipient needs paginated, run
`--paginated`. If they need both, run twice.

## Where it lives

- CLI: `CORE/html-to-pdf/html2pdf.py`
- README: `CORE/html-to-pdf/README.md`
- This skill: `CORE/html-to-pdf/SKILL.md`

CORE is shared across all departments (per PRIMOLABS org chart).
SOFTWARE DEV, SALES, ENGINEERING, and PRIMOLABS all use this for
proposal/scope/SOW rendering.

## Future v2 ideas (parking lot)

1. Local font caching / self-hosted DM Sans bundle so seamless mode
   works fully offline.
2. `--theme` flag for prebuilt seamless profiles (different default
   widths, e.g. 1200px for marketing pages vs 850px for proposals).
3. Concurrent batch rendering (currently serial).
4. `--png` / `--png-pdf` flag to output a single tall PNG image instead
   of a PDF (useful for embedding in decks or Notion).
5. Watermark injection (`--watermark "DRAFT"`) without modifying source
   HTML.
6. Sellable graduation: this is adjacent to div riots' html.to.design
   ($19/mo Figma plugin). HTML→PDF as a hosted SaaS or CLI/desktop tool
   is a viable SIDE-HUSTLE candidate after the operator dogfoods for 2 weeks
   per the 60-min product rule.
