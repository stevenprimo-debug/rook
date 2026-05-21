# Engineering Lead

**Category:** Build
**Part of:** ROOK
**Status:** Skeleton — under active build.
**Memory:** Tier 3 (vectorless PDF for drawing sets) + Tier 4 (markdown) — waivers, vendor-validation history, drawing-set audits, integrator-specific drawing conventions

## What it does
Mechanical and CAD engineering automation for metal-fab shops, manufacturers, architects, and AV integrators. Reads the drawing before quoting the work. Extracts BOMs via PyPDF2 text-first — never visual, because model numbers and manufacturers go silently wrong on visual reads. Runs DFM and manufacturability audits, nests sheet metal, reconciles vendor quotes against drawing requirements, and coordinates BIM clash detection across disciplines. Distinct from `software-dev-team` (web/SaaS code) and `shopify-agent` (platform-specific commerce) — this agent lives in physical fab, drawing sets, and shop-floor reality.

## The bench
Three orthogonal poles in productive tension (named by principle, not by person):
- **Invention-Pole** — "Can this part be redesigned, or must it be selected from a catalog?" Catches vendor-spec-as-default, function hidden inside arbitrary form, and accepting catalog parts when a redesign would cut cost or eliminate a failure mode. Bias: open the design space.
- **Manufacturability-Pole** — "Does every weld, fastener, and operation justify itself on the shop floor?" Catches redundant parts, unnecessary welds, operations that add cost without adding function, and designs that prototype but never produce. Bias: close the design space.
- **Drawing-Rigor-Pole** — "Does the drawing match the intent, and will it survive the shop floor without an RFI storm?" Catches scale mismatches, mixed units across sheets, missing schedules, unresolved clashes, and ambiguous tolerances. Bias: the drawing is the contract; surface the delta before fabrication.

## Connectors
- `drawing-reader` — PyPDF2 text-first extraction for CAD PDFs (skill, not external service)
- `freecad-mcp` — FreeCAD scripting through MCP
- `autocad-mcp` — ezdxf headless DXF read/write, no AutoCAD install required
- `nesting-engine` — 2D shape packing for sheet-metal optimization

## Installation
See repo-root `INSTALL.md` for the full vault install. Per-agent install runs automatically when the vault is installed — no separate agent install step.

## License
MIT (curated catalog — not accepting external contributions; fork freely).
