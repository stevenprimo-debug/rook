---
name: citations
source: https://platform.claude.com/docs/en/build-with-claude/citations
fetched: 2026-05-22
category: guides
rook-relevance: medium
---

# Citations

## What it is

Claude provides verified pointers into source documents. Eligible for Zero Data Retention. All active models support it (except Haiku 3). Better than prompt-based "quote me" approaches: cheaper (cited_text doesn't count toward output tokens), more reliable (parsed to valid pointers), higher quality (better recall of relevant quotes per eval).

## Key concepts + config

### Enable
```python
{
    "type": "document",
    "source": {"type": "text", "media_type": "text/plain", "data": "..."},
    "title": "My Document",
    "context": "trustworthy document",   # optional, not citable
    "citations": {"enabled": True},
}
```
**All-or-none per request**: enable on every document or none.

### Three document types
| Type | Chunking | Citation format |
|---|---|---|
| Plain text | Per sentence | char index (0-indexed, exclusive end) |
| PDF | Per sentence | page number (1-indexed, exclusive end) |
| Custom content | None (provided blocks) | block index (0-indexed, exclusive end) |

NOT supported as document blocks: `.csv`, `.xlsx`, `.docx`, `.md`, `.txt`. Convert to plain text.

### Plain text (inline)
```python
{"type": "document",
 "source": {"type": "text", "media_type": "text/plain", "data": "Plain text..."},
 "citations": {"enabled": True}}
```

### Plain text (Files API)
```python
{"type": "document",
 "source": {"type": "file", "file_id": "file_011CNvxoj286tYUAZFiZMf1U"},
 "citations": {"enabled": True}}
```

### PDF (base64)
```python
{"type": "document",
 "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_b64},
 "citations": {"enabled": True}}
```

### Custom content (your own chunks, no auto-chunking)
```python
{"type": "document",
 "source": {"type": "content", "content": [
     {"type": "text", "text": "First chunk"},
     {"type": "text", "text": "Second chunk"},
 ]},
 "citations": {"enabled": True}}
```
For RAG: each chunk → one plain text document if you want sentence-level cites, OR custom content if you want chunk-level cites only.

### Citation output formats
**Char location**:
```python
{"type": "char_location", "cited_text": "...", "document_index": 0,
 "document_title": "...", "start_char_index": 0, "end_char_index": 50}
```

**Page location**:
```python
{"type": "page_location", "cited_text": "...", "document_index": 0,
 "document_title": "...", "start_page_number": 1, "end_page_number": 2}
```

**Content block location**:
```python
{"type": "content_block_location", "cited_text": "...", "document_index": 0,
 "document_title": "...", "start_block_index": 0, "end_block_index": 1}
```

### Citable vs non-citable
- `source.content` text → citable
- `title`, `context` → passed to model but NOT cited

### Token costs
- Slight input bump (system additions + chunk overhead)
- **`cited_text` does NOT count toward output tokens** (or input on re-pass)
- Very efficient on output

### Feature compatibility
- Works with prompt caching (cache the document, not the citation blocks)
- Works with token counting, batch processing
- **INCOMPATIBLE with Structured Outputs** — enabling both returns 400

### Cache + citations pattern
```python
{"type": "document",
 "source": {"type": "text", "media_type": "text/plain", "data": long_doc},
 "citations": {"enabled": True},
 "cache_control": {"type": "ephemeral"}}
```

### Streaming
Citations stream as `citations_delta` events, one per citation, attached to current `text` block:
```
event: content_block_delta
data: {"type": "content_block_delta", "index": 0,
       "delta": {"type": "citations_delta",
                 "citation": {"type": "char_location", ...}}}
```

## ROOK applicability

Citations is the right surface for ROOK's deep-researcher when grounding outputs in cached docs (e.g., source-of-truth PDFs, competitive-intel briefs). Better than prompting Claude to "quote your sources." For deep-researcher's compounding-append memory pattern, citations into the operator's own past briefs would let downstream agents trace claims back to their origin. Note the Structured Outputs incompatibility — if a ROOK agent needs both schema-conformant JSON AND citations, must run two passes or use json_schema in headless mode without citations.

## Cross-references
- [[prompt-caching]] — cache documents, not citation blocks
- [[vision]] — image citations not yet supported
- [[tool-use]] — Files API + tool_use patterns
