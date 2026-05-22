---
name: rook-brand
parent-brand: PrimoLabs
brand-status: LOCKED
# Authoritative for ROOK customer-output rendering: BSA v4 contract templates (production client deliverables).
# Operator-instance source files (Primo's local copies — customer instances differ):
#   - spec-source-operator-local: ~/Desktop/PRIMOLABS/DEPARTMENTS/PRIMOLABS/brand_spec_2026-04-28.md
#   - palette-source-operator-local: ~/Desktop/PRIMOLABS/DEPARTMENTS/PRIMOLABS/primolabs-site-v2-next/src/app/globals.css
# For SHIPPED ROOK: tokens below are bundled directly; no external resolve needed.
last-synced: 2026-05-22
palette-name: Burnt Operator
attribution: Powered by Claude · Built by PrimoLabs
read-by: .claude/templates/html/brand-loader.py
---

# ROOK Brand Source — Burnt Operator (PrimoLabs)

ROOK is a PrimoLabs product. Shared brand identity. Burnt orange Rook chess piece. Same colors, fonts, and voice as the PrimoLabs parent brand. This file is the bundled snapshot of the locked brand tokens — synced from the production site at `primolabs-site-v2-next/src/app/globals.css`.

## Two-tier brand surface system

ROOK ships two distinct treatments. **Use the right one for the artifact class:**

| Tier | When to use | Bg | Type | Density |
|---|---|---|---|---|
| **Brand surface** (default) | READMEs, dashboards, briefs, plans, reports, marketing pages, HTML companions, cover pages | Dark `#15110d` | Outfit display + Geist body | Visual, expressive |
| **Legal body** (special-case) | Contract bodies ONLY (NDAs, MSAs, SOWs, license agreements, partnership agreements) — never anywhere else | White `#ffffff` | Times New Roman 12pt | Law-firm-grade, justified, double-spaced (`line-height: 2`), 1in margins |

Contracts are a hybrid: branded cover page (Tier 1) + legal body (Tier 2) on subsequent pages. The contract HTML at `PrimoLabs_PoweredByClaude_OPERATOR/accounts/<client>/contracts/*.html` is the canonical reference.

## Palette — Burnt Operator (BSA v4 architecture · LOCKED)

Authoritative token source: client-deliverable HTML templates (BSA v4) — what actually ships in customer hands. Site palette (`primolabs-site-v2-next/src/app/globals.css`) is a sibling treatment; if values diverge, the BSA v4 tokens here win for any ROOK customer-output rendering.

### Background + surface (Tier 1 — brand)

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#15110d` | Warm near-black base — slight red-brown undertone (NOT pure black) |
| `--bg-up` | `#1f1a14` | Elevated panel / card surface |
| `--bg-card` | `#2a231b` | Mid-tone warm surface for nested cards |
| `--rule` | `rgba(248, 244, 237, 0.10)` | Hairline divider rule on dark |

### Accent + signal (Tier 1 — brand)

| Token | Hex | Use |
|---|---|---|
| `--accent` | `#EA580C` | PrimoLabs orange (Tailwind orange-600) — primary accent, CTAs, links, `.AI` wordmark, divider bars |
| `--accent-hi` | `#F97316` | Brighter highlight orange — hover states, signal pulses |
| `--accent-deep` | `#C2410C` | Deeper burnt orange — emphasis, accent-foreground when needed |

### Text (Tier 1 — brand)

| Token | Hex | Use |
|---|---|---|
| `--text` | `#F8F4ED` | Warm off-white (NOT pure white — cream undertone) — body text on dark |
| `--text-dim` | `#C8C2BC` | Secondary text — meta, subtitles |
| `--text-muted` | `#8A8278` | Tertiary text — captions, footer, legal small print |

### Legal body (Tier 2 — contracts only)

| Token | Value | Use |
|---|---|---|
| Background | `#ffffff` | White paper background |
| Text | `#1a1a1a` | Near-black ink |
| Body font | `'Times New Roman', Times, serif` | Legal gravitas |
| Body size | `12pt` | Standard legal-doc size |
| Line height | `2` (double-spaced) | Law-firm-grade readability + redline space |
| Margins | `1in` | Letter-size standard |
| Sig-line border | `1px solid #1a1a1a` | Signature input field |
| Footer text | `#555` | Gray legal footer |
| Page number | `#555`, 10pt, bottom-right | Page numbering |

## Typography

| Role | Family | Weights | Use |
|---|---|---|---|
| **Display** | **Outfit** | 700–900 | Hero, headlines, wordmarks, cover-page client names — letter-spacing `-0.05em` to `-0.08em` for hero, `-0.035em` for client name |
| **Body** | **Geist** | 300–700 | All body copy on brand surfaces, UI labels, navigation |
| **Mono** | **JetBrains Mono** | 400–700 | Code blocks, dashboard data, file paths, operator surfaces |
| **Legal body** | **Times New Roman** | 400 / 700 | Contract bodies ONLY — never anywhere else |

System fallback: `'Outfit', system-ui, sans-serif` (display) / `'Geist', system-ui, -apple-system, sans-serif` (body).

**Note:** brand_spec_2026-04-28.md §5 flagged evaluating Outfit replacements but the BSA v4 architecture (production client deliverables) kept Outfit as canonical display. Outfit STANDS for ROOK customer-output rendering.

## Voice (two registers)

### Register A — Lifestyle / Brand surfaces (hero, ads, social, email subjects)

Plainspoken, human, slightly understated. Specific outcome + specific human moment. No jargon, no aggression, no performance.

**North Star sentence:** *"My organization shipped X this week, while I was at the gym, with my kid on Saturday, with my partner on her day off."*

**Headline territory:**
- "An AI team that works for you. And grows with you."
- "You're the CEO. We built your team."
- "Hire the team you couldn't afford."
- "Your team. Not your tool."

### Register B — Product / Infrastructure (dashboard, settings, docs, builder pages)

Operator voice. Terse. Confident. Verbs over nouns. Technical credibility lives INSIDE the product, not on the front door.

### Banned voice tics (universal)

`Hey there!`, emoji bullets, "we're so excited to," "imagine if," "what if I told you," **"boss"** as a product noun (retired 2026-04-29), "10X your output," "unlock," "level up," "game-changer," any phrase a course-launch coach would put on a landing page, any phrase that sounds like a hacker-terminal manifesto.

### The Jessica test

Would Jessica (non-technical solo CMO) understand AND want this? If only builders pass → it's Register B, goes below the fold or behind a "How it's built" link.

## Wedge

**Team, not tool.** A team that *works for you* and *grows with you* via recursive memory.

**The wedge nobody else owns:** a productized AI organization sold to people who want **less screen time, not more**. Every other AI brand competes on engagement-in-tool. PrimoLabs competes on **engagement-in-life**. We win when you log off.

## Visual juxtaposition (signature move)

- **Hero photography:** people outside — hiking, with kids, farmers markets, reading at 2pm Tuesday. NO desks. NO screens in hands. NO laptop-on-cafe-table stock-photo energy.
- **Caption pattern:** "Your team is working. You're not." / "Stop scrolling. Touch grass." / "Your agent could be doing this for you."
- **Behind-the-photo overlay:** subtle dark-on-dark dashboard frame proving the org chart is running. Life on top, infrastructure underneath.

## Motion language

- **Scramble** (text decode) — operator-terminal feel. SIGNATURE.
- **Typewriter** — pairs with hero copy. SIGNATURE.
- **Sharp directional accent flashes** — single orange-red highlight pulse on hover/load. Console blink, not aurora.
- **Translucent frosted panel reveals** — 2026 AI-product pattern.
- **GSAP scroll-triggered timelines** — hero choreography, NOT cute decoration.

**Forbidden motion:** floating particles, parallax depth-fakes, rotating gradient blobs, glow halos, soft auroras — anything "AI startup 2023."

## Counter-anchors (what to AVOID)

- MindStudio purple gradient softness
- Cole Medin friendly-creator vibe
- Jamie pastel polish
- "Hacker terminal" / "Cursor IDE clone" aesthetic
- Datadog/Sentry/Honeycomb purple convergence

## Reference anchors (what TO emulate)

| Inspiration | Surface |
|---|---|
| Enterprise asset-portal dashboards | Executive UI, dense data, confident |
| Linear / Vercel / Raycast | Premium SaaS ceiling for infrastructure surfaces |
| Patagonia / Filson / Howler Bros / Tracksmith | Lifestyle photography tone for hero/ad surfaces |

## Attribution

Every customer-facing ROOK README, HTML render, and PDF export carries:

```
Powered by Claude · Built by PrimoLabs
```

With link targets:
- `Claude` → `https://www.anthropic.com/claude`
- `Claude Agent SDK` → `https://code.claude.com` (in long-form attribution)
- `PrimoLabs` → `https://primolabs.ai` (placeholder until prod URL)

Logo files for HTML/PDF render:
- Anthropic Claude logo: per [anthropic.com/trademark-policy](https://www.anthropic.com/trademark-policy) — usage allowed for built-with-Claude attribution
- PrimoLabs Rook chess piece logo: TBD — needs file path once asset folder lands

## Sync protocol

This file is the **bundled brand snapshot** that ships with ROOK. The **canonical source** is the production site CSS:

```
C:\Users\User\Desktop\PRIMOLABS\DEPARTMENTS\PRIMOLABS\primolabs-site-v2-next\src\app\globals.css
```

When the production site updates brand tokens, run a re-sync of this file. Quarterly cadence minimum; daily if a brand refresh is in flight.

## How this file is consumed

1. **HTML renders** — `.claude/templates/html/brand-loader.py` reads this file, emits a JSON dict, Jinja2 templates (`brief.html.j2`, `plan.html.j2`, `proposal.html.j2`, `report.html.j2`) pull tokens from the dict
2. **Markdown attribution** — README footers reference the attribution block
3. **Agent voice** — every agent's voice spine references the "Banned voice tics" + "Wedge" sections via `_CLAUDE.md` Rule #17 (HTML default for human-eyes artifacts)

---

## Amendments — 2026-05-22 (post-absorb-audit, librarian Stream B)

> Versioned-append per Compounding-Append rule (`_CLAUDE.md` Section 3). Body above stays intact as v1 (locked 2026-05-22). The amendments below extend the canonical brand source — they do NOT rewrite prior decisions.

### Amendment 1 — Site palette vs contract palette divergence policy

Two orange tokens are live in the PrimoLabs ecosystem:

- **Site palette** (`primolabs-site-v2-next/src/app/globals.css`): `#ff5722` deep-orange
- **BSA v4 contract palette** (this file, § Palette → `--accent`): `#EA580C` Tailwind orange-600

**Precedence rule: BSA v4 wins for any ROOK customer-output rendering.** Site palette is a sibling treatment — authoritative for the marketing site only, not for customer deliverables (contracts, dashboards, briefs, reports, HTML companions, PDF exports).

Rationale: customer-output is the highest-stakes surface. The contract palette is what lands in a buyer's hand and a customer counsel's redline. If the marketing site palette drifts further, that's a sibling — not authoritative for anything customer-facing.

If the operator decides the site palette becomes new canonical, run a re-sync of this file and bump `last-synced` in frontmatter. Until then, BSA v4 stands. Source: 2026-05-22 absorb-audit § A8.

### Amendment 2 — Outfit retention rationale (callout — supersedes brand_spec_2026-04-28 §5)

Outfit display font is RETAINED as ROOK's canonical display font. This amendment makes the policy explicit (replacing the brand_spec_2026-04-28 §5 evaluation recommendation that is now superseded — see `DEPARTMENTS/PRIMOLABS/brand_spec_2026-04-28.md` § OVERRIDDEN 2026-05-22 block).

**Policy: Outfit STANDS. Do NOT propose Outfit replacement absent operator-initiated brand refresh.**

Outfit is used for: hero, headlines, wordmarks, cover-page client names — letter-spacing `-0.05em` to `-0.08em` for hero, `-0.035em` for client name. BSA v4 production templates kept Outfit; production wins. Source: 2026-05-22 absorb-audit § A9; methodology detail at `.claude/reference/methodology/designer-two-tier-brand-surface.md` (already promoted by librarian morning pass).

### Amendment 3 — Attribution usage rules subsection

The attribution block (`Powered by Claude · Built by PrimoLabs`) is REQUIRED on customer-facing artifacts and NOT required on operator-internal artifacts.

| Surface class | Attribution required? | Placement |
|---|---|---|
| Customer-facing README (shelf, top-level, MASTER_INDEX) | **Required** | Footer, last line |
| Customer-facing HTML render (proposal, brief, plan, report, dashboard) | **Required** | Footer, `<sub>` HTML, 9pt equivalent |
| Customer-facing PDF export (any artifact rendered to PDF for signature or distribution) | **Required** | Footer, 9pt |
| Customer-facing reading-inbox doc (`_from_rook/*.md`) | **Required** | Footer, last line |
| Operator-internal SKILL.md | NOT required | n/a |
| Operator-internal CLAUDE.md (routing files) | NOT required | n/a |
| Operator-internal memory files (`agents/*/memory/*.md`) | NOT required | n/a |
| Operator-internal session handoffs (`_archive/HANDOFFS/`) | NOT required | n/a |

Link targets are locked:

- `Claude` → `https://www.anthropic.com/claude`
- `Claude Agent SDK` (long-form attribution only) → `https://code.claude.com`
- `PrimoLabs` → `https://primolabs.ai`

Placement rule: always last, always small (`<sub>` HTML or 9pt PDF). Never compete with body content. Source: 2026-05-22 absorb-audit § C.

### Amendment 4 — Operator-vault path convention for branded outputs

Operator-vault branded outputs follow a single canonical path pattern:

```
PrimoLabs_PoweredByClaude_OPERATOR/accounts/<client-slug>/contracts/<filename>.{md,html,pdf}
```

File naming: `YYYY-MM-DD_<Client>_<PurposeSlug>_v<N>` — e.g., `2026-05-22_BSA_MasterServicesAgreement_v1.md`.

Companion artifact pattern (per _CLAUDE.md Rule #20 — MD source + HTML companion contract): every contract is authored as `.md` (canonical source) → rendered to `.html` (branded companion: BSA v4 cover + legal body) → exported to `.pdf` (final signature artifact). MD = source. HTML = generated. PDF = signature.

**Vault boundary:** operator-vault path (`PrimoLabs_PoweredByClaude_OPERATOR/`) is distinct from ship-vault (`PrimoLabs_PoweredByClaude/`). Real client data lives in operator vault ONLY. Ship vault is sanitized. Any account-manager (or any agent) authoring a contract / NDA / SOW / partnership doc for a real client MUST write to operator-vault path. Never to ship vault. Source: 2026-05-22 absorb-audit § A10 + § C.

### Amendment 5 — Anti-slop guardrail bullets (visual composition extension)

Today's `frontend-design` integration surfaced concrete anti-slop tics to add to the existing § Visual juxtaposition + § Motion language forbidden lists. Motion already has its forbidden list (floating particles, parallax depth-fakes, rotating gradient blobs, glow halos, soft auroras). Add an equivalent VISUAL-composition forbidden list:

**Forbidden visual composition (Tier 1 brand surfaces):**

- Stock-photo desk shots (laptop-on-cafe-table, hands-on-keyboard, woman-smiling-at-screen)
- "10X your output" headlines or any course-launch-coach phrase
- Gradient-text wordmarks (the AI-startup-2023 tell — body copy stays solid color)
- Emoji bullets in body copy (signals consumer-blog or course landing)
- "AI startup 2023" aesthetic markers (purple gradients, soft pastels, glowing orbs as decoration, "powered by AI" badges)
- Generic-isometric illustrations of cubes/blobs/abstract-tech-shapes
- Hero photo of a person at a desk looking at a screen (contradicts the "Your team is working. You're not." wedge directly)

The Jessica test still applies: if a non-technical solo CMO would skim this and think "another AI startup," the visual composition has failed. Source: 2026-05-22 absorb-audit § C anti-slop guardrail bullets.

---

*Amendments 1-5 appended 2026-05-22 by librarian Stream B (post-absorb-audit close-out). v1 body above is preserved verbatim per Compounding-Append rule.*
