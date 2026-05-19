---
name: nesting-engine
description: >
  2D part-nesting skill for sheet-material layout optimization — laser cuts, waterjet,
  plasma, sheet-metal blanks, fabric, leather, plywood. Wraps Deepnest.io (desktop/CLI),
  SVGnest (JS core), and nest2D (Python binding to libnest2d). Use this skill ANY time
  the operator asks to "nest these parts", "optimize the sheet layout", "pack parts onto
  stock", "minimize scrap", "compute material utilization", "generate a nesting plan",
  "nest SVGs/DXFs", "lay out the cuts", or describes a fabrication job with multiple
  parts cut from sheet stock. Also trigger for sheet-metal nesting + API projects —
  this skill is the nesting-engine layer that SALES will call. Free, open-source, local.
---

# Nesting Engine — 2D Sheet Layout Optimization

## When to use

Trigger this skill whenever the job is packing 2D parts onto 2D stock to maximize material utilization:
- Sheet metal blanks (laser, waterjet, plasma)
- Plywood / MDF / acrylic CNC routing
- Fabric / leather / vinyl cutting
- Label / sticker sheet layout
- Any "how many parts fit on this sheet?" question

For 3D packing (3D printer build-plate, shipping volume), this skill does NOT apply — flag and request 3D packer alternative (`py3dbp`, `rectpack3d`, etc.).

## Engine selection

Three engines, each with a distinct sweet spot. Pick before starting.

| Engine | Interface | Strength | When to pick |
|---|---|---|---|
| **Deepnest.io** | Desktop Electron app + batch CLI | Best open heuristic; merges shared cuts (common-line cutting); great for real fab work | Primary choice for laser/waterjet jobs where shared-line cutting saves time |
| **SVGnest** | Browser JS (no-fit polygon) | Reference algorithm; pure SVG in/out; easy to embed in a web app | When building a web tool — directly servable |
| **nest2D** (Python) | `pip install nest2D` → libnest2d via pybind11 | In-process Python; good for scripting, batch, APIs | Server-side APIs; programmatic pipelines; **sheet-metal nesting API projects** |

**Default for the [example project]: `nest2D` (Python)** — allows a FastAPI/Flask endpoint that accepts DXFs, returns nested SVG + utilization metrics, without shelling out to Electron.

## Install (one-time, per engine)

### nest2D (Python, primary)
```powershell
pip install nest2D shapely svgwrite ezdxf
```

### Deepnest.io (desktop)
- Download latest release: https://deepnest.io/
- CLI exists but is undocumented; scripting via Electron main process

### SVGnest (JS)
- Clone https://github.com/Jack000/SVGnest and serve `index.html`, or `npm i svgnest` for a node build

## Core API (nest2D pattern)

```python
from nest2D import Point, Box, Item, SVGWriter, nest
import ezdxf

def parts_from_dxf(path):
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    items = []
    for lwp in msp.query("LWPOLYLINE"):
        pts = [Point(int(p[0]*1000), int(p[1]*1000)) for p in lwp.get_points("xy")]
        items.append(Item(pts))
    return items

items = parts_from_dxf("parts.dxf")
sheet = Box(1220_000, 2440_000)   # 4'x8' in microns
result = nest(items, sheet)

svg = SVGWriter()
svg.write_svg(result, "nested.svg")

# Utilization
used = sum(item.area for item in items)
total = sheet.width * sheet.height * len(result)
print(f"Utilization: {used/total*100:.1f}%")
```

Units are microns internally — scale inputs by 1000× (mm → µm) or 25400× (in → µm).

## Nesting parameters (tune per job)

| Parameter | nest2D setting | Default | Notes |
|---|---|---|---|
| Part spacing | `ConfigureNestParameters.min_obj_distance` | 2000 µm (2mm) | Match kerf + thermal margin for laser/waterjet |
| Rotations allowed | `ConfigureNestParameters.rotations` | 4 (0/90/180/270°) | Bump to 16 for fabric where grain doesn't matter |
| Accuracy | `ConfigureNestParameters.accuracy` | 0.65 | Higher = slower but tighter |
| Alignment | `NestControl.alignment` | `BOTTOM_LEFT` | Center-pack or left-align depending on sheet |

## Multi-sheet nesting

Wrap `nest()` in a loop — it returns a list of filled sheets. Report per-sheet utilization and total sheets needed. Flag any unplaceable parts (too large for the sheet stock).

## Deepnest CLI invocation (when common-line cutting matters)

Deepnest headless is fragile — the supported path is the desktop app with XML project file imports:

```powershell
# Launch Deepnest, file → import SVG, start nest, export SVG + DXF
# Batching via CLI is experimental — forum thread:
# https://github.com/Jack000/Deepnest/issues/?q=cli
```

For pure scripted workflows, prefer nest2D. Reach for Deepnest when the operator needs the shared-line heuristics on real cut jobs.

## Output convention

Every nest job returns:
1. `nested.svg` — visual layout (viewable in browser or Inkscape)
2. `nested.dxf` — CAD-ready output for the cutter
3. `nesting_report.json`:
   ```json
   {
     "sheet_size_mm": [1220, 2440],
     "sheets_used": 3,
     "parts_placed": 47,
     "parts_unplaced": 0,
     "utilization_pct": 68.3,
     "total_cut_length_mm": 14782,
     "estimated_cut_time_min": 24.6
   }
   ```
4. `unplaced.json` (only if any parts could not fit)

Save outputs under `agents/engineering-lead/nesting/<job-id>/` unless the calling dept (e.g., SALES for a sheet-metal customer) specifies otherwise.

## [example project] integration pattern

When SALES formalizes a sheet-metal nesting + API project, this skill becomes the engine behind the API:

```
SALES/<customer> API ─HTTP──▶ ENGINEERING/nesting-engine ─libnest2d──▶ nested output
     │                        │
     │                        ▼
     │                  nesting_report.json
     ▼
   Quote / invoice
```

Expose as a FastAPI endpoint. Accept: DXF/SVG parts list + sheet spec + material. Return: nested SVG/DXF + utilization + cost estimate. No license cost, no per-call fees, pure OSS.

## Guardrails

- **Units must be explicit.** nest2D is micron-native; a wrong scale = 1000× error. Validate every DXF load by checking a known part's dimensions.
- **Never trust a 100% utilization report.** That's a bug — real packs land 60–85% depending on geometry variety.
- **Part rotations on grain-sensitive materials** (fabric, wood, composite): lock rotations to 0°/180° only.
- **Common-line cutting assumes adjacent parts share a cut.** Deepnest handles this; nest2D does not — if shared-line is required, use Deepnest.
- **Report unplaceable parts loudly.** A silent drop on a fab job causes field surprises.

## Upstream

- nest2D: https://github.com/markfink/nest2D (Python binding, MIT)
- libnest2d: https://github.com/tamasmeszaros/libnest2d (C++ core, LGPL)
- Deepnest: https://github.com/Jack000/Deepnest (Electron fork, MIT)
- SVGnest: https://github.com/Jack000/SVGnest (JS reference, MIT)
