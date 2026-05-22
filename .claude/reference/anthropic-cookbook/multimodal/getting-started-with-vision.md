---
name: getting-started-with-vision
source: https://github.com/anthropics/claude-cookbooks/blob/main/multimodal/getting_started_with_vision.ipynb
fetched: 2026-05-22
category: Multimodal
rook-relevance: low
rook-status: skip
---

# Getting Started with Vision

## What it is

Two image input methods: base64-encoded in JSON, or URL-referenced. Image content blocks nest in the `content` array alongside text. Multiple images per message enabled for comparative analysis.

## Key code/config

```json
{
  "type": "image",
  "source": {
    "type": "base64",
    "media_type": "image/jpeg",
    "data": "<base64>"
  }
}
```

Best-practice notes: include explicit text prompts describing what to analyze; high-contrast images preferred; specify output format expectations.

## Measured improvements / costs

None reported. This is a basics-and-shapes notebook.

## ROOK applicability

ROOK's markitdown skill already wraps the input layer — it handles images-with-OCR as part of the universal file→markdown pipeline. The agent never sees raw image content blocks; it sees the markdown markitdown produced. Direct vision API patterns are below the agent's abstraction.

## Recommended action

**skip** — markitdown owns this layer. No agent-level pattern to absorb.
