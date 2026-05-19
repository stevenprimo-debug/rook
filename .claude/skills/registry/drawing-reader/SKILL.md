---
name: drawing-reader
description: >
  General-purpose mechanical drawing interpretation skill — reads DWG, DXF, PDF,
  and scanned-blueprint inputs and extracts title blocks, dimensions, BOMs,
  revision blocks, notes, and part lists. Free/OSS pipeline: ezdxf + ODA File
  Converter + pdfplumber + PaddleOCR + Camelot + Claude vision. Use this skill
  ANY time the operator uploads a mechanical drawing and asks to "read this drawing", "extract the BOM", "pull
  the dimensions", "what's the title block say", "get the part list", "parse
  this DWG/DXF", or "what's this drawing about". Also trigger when the agent
  needs to ingest a customer-supplied drawing as input for downstream FreeCAD
  modeling, nesting, quoting, or DFM analysis. Works on any mechanical/product
  drawing — sheet metal, machined parts, assemblies, weldments.
---

# Drawing Reader — Mechanical Drawing Ingestion (Free/OSS)

## Scope vs related skills

| Input | Use this skill | Use instead |
|---|---|---|
| Mechanical part drawing (PDF, DXF, DWG) | **drawing-reader** | — |
| Sheet-metal or machined-part blueprint | **drawing-reader** | — |
| Scanned / photographed blueprint | **drawing-reader** | — |
| 3D CAD file (STEP, IGES, STL) | — | `freecad-mcp` (open + query) |
| Need to CREATE a new part from the drawing | **drawing-reader** (parse) + `freecad-mcp` (model) | — |

## Pipeline

Input is classified first, then routed to the correct extractor:

```
  ┌──────────────┐
  │  Input file  │
  └──────┬───────┘
         ▼
    ┌────────┐    DXF      ┌─────────┐
    │classify├────────────▶│  ezdxf  │
    └────────┘             └─────────┘
     │     │
     │     │   DWG (needs conversion)
     │     └──▶ ODA File Converter → DXF → ezdxf
     │
     │   PDF (vector) ──▶ pdfplumber ──▶ structured text + lines + rects
     │     +
     │              ──▶ Camelot (lattice) ──▶ BOM tables
     │
     │   PDF (scanned) / image
     └────▶ PaddleOCR 3.0 ──▶ text + bboxes
                │
                └─▶ Claude vision (for title block, revision block, BOM pairing)
```

## One-time install

```powershell
pip install ezdxf pdfplumber "camelot-py[cv]" paddleocr opencv-python numpy pandas
```

External binary (DWG → DXF bridge):
- Download **ODA File Converter**: https://www.opendesign.com/guestfiles/oda_file_converter
- Windows default install path: `C:\Program Files\ODA\ODAFileConverter 25.x.x\ODAFileConverter.exe`

PaddleOCR auto-downloads its English model on first run.

## Classification (mandatory first step)

```python
from pathlib import Path
import pdfplumber

def classify(path):
    ext = Path(path).suffix.lower()
    if ext == ".dxf": return "dxf"
    if ext == ".dwg": return "dwg"
    if ext in (".png", ".jpg", ".jpeg", ".tif", ".tiff"): return "raster"
    if ext == ".pdf":
        with pdfplumber.open(path) as p:
            page = p.pages[0]
            # A vector PDF has chars/lines/rects; a scan is a single image.
            if len(page.chars) > 20 or len(page.lines) > 10:
                return "pdf_vector"
            return "pdf_scan"
    raise ValueError(f"Unknown input type: {ext}")
```

Branch on the result. Never assume — a PDF may be a scan even if it says "CAD" in the filename.

## DXF extraction (ezdxf)

```python
import ezdxf

def read_dxf(path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    return {
        "title_block": _extract_title_block(doc),     # INSERT + ATTRIB
        "dimensions":  _extract_dimensions(msp),      # DIMENSION entities
        "text":        _extract_text(msp),            # TEXT + MTEXT
        "layers":      [l.dxf.name for l in doc.layers],
        "blocks":      [b.name for b in doc.blocks if not b.name.startswith("*")],
    }
```

Title blocks are nearly always `INSERT` entities with named `ATTRIB` children. Iterate `msp.query("INSERT")`, pull `.attribs`, and match common names: `TITLE`, `DWG NO`, `DRAWN BY`, `REV`, `DATE`, `SCALE`, `SHEET`.

Dimension entities expose `.dxf.text` (override) OR the measured value if no override. Always prefer the override — that's what's printed on the drawing.

## DWG → DXF (ODA File Converter)

Shell out to ODA's CLI:

```python
import subprocess
ODA = r"C:\Program Files\ODA\ODAFileConverter 25.x.x\ODAFileConverter.exe"

subprocess.run([
    ODA,
    str(src_dir), str(out_dir),
    "ACAD2018", "DXF", "0", "1",
    "*.DWG"
], check=True)
```

Arguments: input dir, output dir, output CAD version, output format, recurse flag, audit flag, wildcard.

## Vector PDF extraction (pdfplumber + Camelot)

```python
import pdfplumber, camelot

def read_pdf_vector(path):
    with pdfplumber.open(path) as pdf:
        pages = []
        for i, page in enumerate(pdf.pages):
            pages.append({
                "page": i + 1,
                "text": page.extract_text(),
                "words": page.extract_words(),  # bboxes
                "lines": page.lines,
                "rects": page.rects,
            })

    # BOM tables (lattice mode for ruled tables)
    tables = camelot.read_pdf(path, pages="all", flavor="lattice")
    boms = [t.df.to_dict("records") for t in tables]

    return {"pages": pages, "tables": boms}
```

If lattice mode returns empty, fall back to `flavor="stream"` for unruled tables.

## Scanned PDF / raster extraction (PaddleOCR + Claude vision)

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="en")

def read_raster(path):
    # Paddle returns [[bbox, (text, conf)], ...] per region
    result = ocr.ocr(str(path), cls=True)
    return [
        {"text": r[1][0], "conf": r[1][1], "bbox": r[0]}
        for r in result[0]
    ]
```

Then hand the image + OCR JSON to Claude vision for:
- Title block field mapping (TITLE / DWG NO / REV / DATE / SCALE / SHEET)
- Revision block timeline
- BOM line-item pairing (part number ↔ description ↔ qty ↔ material)
- General "what is this drawing of" triage

## Claude-vision guardrails (CRITICAL)

Claude vision benchmarks at ~40% on engineering drawings. Misassigns dimensions in multi-view layouts. Use it ONLY for:

**SAFE with Claude vision:**
- Title blocks, revision blocks, vendor logos
- BOM line-item pairing (cross-validation)
- Notes / general-info blocks
- "What category of part is this"
- Sanity-checking OCR output

**NEVER with Claude vision (without human review):**
- Authoritative dimension readout
- GD&T feature control frames
- Tolerance stackups
- Material callouts going to shop floor
- Anything safety/compliance-critical

If the operator asks for dimensions: use ezdxf (for DXF) or pdfplumber text extraction (for vector PDF) as the source of truth. Scanned drawings with only OCR + vision are flagged as UNVERIFIED in the output.

## Output schema

Every read returns a consistent JSON:

```json
{
  "source": "path/to/file.dxf",
  "source_type": "dxf | dwg | pdf_vector | pdf_scan | raster",
  "title_block": {
    "title": "...", "drawing_number": "...", "revision": "...",
    "drawn_by": "...", "date": "...", "scale": "...", "sheet": "1 of 3",
    "confidence": "high | medium | unverified"
  },
  "revision_block": [
    {"rev": "A", "date": "...", "description": "...", "by": "..."}
  ],
  "bom": [
    {"item": 1, "qty": 2, "part_no": "...", "description": "...", "material": "...", "notes": "..."}
  ],
  "dimensions": [
    {"value": "25.4", "unit": "mm", "type": "linear | radial | angular",
     "tolerance": "+0.05/-0.05", "location": {"page": 1, "bbox": [...]},
     "confidence": "high | medium | unverified"}
  ],
  "notes": ["..."],
  "pages": 3,
  "flags": [
    "Dimension on page 2 extracted from scanned OCR — mark unverified."
  ]
}
```

## Common pitfalls

- **Scanned PDFs masquerading as vector.** A drawing saved as "Reduce File Size" in Acrobat often flattens to raster. Always run `classify()`.
- **Title block names vary wildly.** `TITLE` / `TTL` / `DRAWING_TITLE` / `DWG_TITLE` — match loosely.
- **Dimension overrides ≠ measured values.** Old DXFs sometimes have a drawing showing `25` but the measured entity is `24.97`. The override wins.
- **OFE / OFB markers.** If the drawing has Customer-Furnished or Off-BOM items, flag them separately — they can break downstream quoting.
- **Multi-sheet drawings.** Sheets 1..N may have different title blocks; don't overwrite. Keep an array.

## Upstream

- ezdxf: https://ezdxf.readthedocs.io (MIT)
- ODA File Converter: https://www.opendesign.com/guestfiles/oda_file_converter (free, not OSS)
- pdfplumber: https://github.com/jsvine/pdfplumber (MIT)
- Camelot: https://camelot-py.readthedocs.io (MIT)
- PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR (Apache-2.0)
