---
name: vision
source: https://platform.claude.com/docs/en/build-with-claude/vision
fetched: 2026-05-22
category: guides
rook-relevance: medium
---

# Vision / Multimodal

## What it is

Claude analyzes images. Available via claude.ai, Console Workbench, and API.

## Key concepts + config

### Image limits per request
- 20 images max on claude.ai per message
- **100 images** per API request on 200k-context models
- **600 images** per API request on other models
- Max dimensions: **8000x8000 px**. If >20 images in one request: reduced to **2000x2000 px**.

### Request size limits (often hit first)
- Standard API: 32MB per request
- Bedrock / Vertex (partner-operated): lower limits

For many images, **use Files API and reference by `file_id`** to keep payloads small.

### Source types

**Base64**:
```python
{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": "<b64>"}}
```

**URL**:
```python
{"type": "image", "source": {"type": "url", "url": "https://example.com/img.jpg"}}
```

**Files API**:
```python
{"type": "image", "source": {"type": "file", "file_id": "file_abc..."}}
```

### Supported formats
- `image/jpeg`
- `image/png`
- `image/gif`
- `image/webp`

### Best practices
- **Multiple images per message**: jointly analyzed (good for comparison/contrast)
- **Image size**: large images compute more tokens; downsample if not needed at full res
- **Resolution**: 1.15 megapixels is a good upper bound for general use
- **Use Files API for many large images** — request can still fail at the request-size limit before hitting the count limit
- **Pre-process**: rotate, crop, downsample before send

### Token cost
Image tokens scale with dimensions. Rough formula: `tokens ≈ (width * height) / 750`. Verify in `response.usage.input_tokens`.

### Limitations
- **No image citations** — citations feature is text-only as of this fetch
- **Image data not retained** if your org has ZDR — encode in request, send each time, no persistent file storage benefit
- Vision quality varies by content type — strong on diagrams, charts, photos; weaker on handwriting, dense screenshots of text

## ROOK applicability

For ROOK agents working with operator screenshots (UI bugs, design reviews, dashboards), Files API + `file_id` is the right pattern — don't base64 every screenshot. The designer agent and product-manager agent are the most likely consumers. For sanitization auditor: vision can read screenshots that contain sanitization-flag content (real names in UI mockups), but no `cited_text` to point to — auditor has to describe the issue verbatim. Vision is NOT the right tool for OCR-heavy work on dense text — convert to text via markitdown first.

## Cross-references
- [[tool-use]] — Files API for file_id references
- [[citations]] — text-only; image citations not supported
- [[prompt-caching]] — image presence invalidates message cache
