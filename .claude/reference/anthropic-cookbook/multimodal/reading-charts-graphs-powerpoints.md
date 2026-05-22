---
name: reading-charts-graphs-powerpoints
source: https://github.com/anthropics/claude-cookbooks/blob/main/multimodal/reading_charts_graphs_powerpoints.ipynb
fetched: 2026-05-22
category: Multimodal
rook-relevance: medium
rook-status: absorb-recommended
---

# Reading Charts, Graphs, PowerPoints

## What it is

Claude reads chart-heavy and slide-heavy PDFs better than text-extraction-only pipelines because it uses BOTH extracted text and vision simultaneously. Three accuracy-tightening techniques:

1. **Detail extraction** — prompt "describe every data point you see" to trigger chain-of-thought
2. **Color identification first** — for grouped/multi-series charts, ask Claude to "first identify colors using HEX codes" before reading the data
3. **Slide narration with persona** — narrate as if the presenter, structured XML output per slide for downstream RAG

Failure modes called out: arithmetic errors, color-dependent visualizations. Mitigations: give Claude a calculator tool, explicit color labeling.

## Key code/config

```python
client = Anthropic(default_headers={"anthropic-beta": "pdfs-2024-09-25"})
```

XML output for narration:
```
<narration>slide content here</narration>
```
Parsed via regex `r"<narration>(.*?)</narration>"`.

100-page document limit per request.

## Measured improvements / costs

No formal benchmarks. Demonstrated successful analysis of Carvana and Twilio financial reports.

## ROOK applicability

ROOK's engineering-lead is Tier 3 (markitdown + PDF) — it reads drawing packs and vendor specs. Charts/graphs in vendor proposals + drawing-pack legends are exactly the chart-and-color failure mode the cookbook addresses. markitdown's default extraction may flatten chart context the way PyPDF does.

The chart-reading patterns (color-first, "describe every data point") could be folded into engineering-lead's drawing-pack reading mode as prompt heuristics — not as new infra, just as prompt patterns in its SKILL.md.

Marketing-director / sales-director also touch vendor decks and competitor reports where chart accuracy matters.

## Recommended action

**absorb-recommended** — add a "chart and slide reading" prompt-pattern section to engineering-lead's SKILL.md (and reference it from sales-director, marketing-director). Effort: ~2 hours. Payoff: tighter vendor-spec extraction on multi-color/multi-series charts.
