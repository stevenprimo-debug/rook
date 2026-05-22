---
name: knowledge-graph
source: https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/knowledge_graph/guide.ipynb
fetched: 2026-05-22
category: RAG & Retrieval
rook-relevance: high
rook-status: already-implemented
---

# Knowledge Graph Construction from Unstructured Text

## What it is

Build typed entity-relation graphs from documents using Claude's structured outputs. Three-stage pipeline:

1. **Extraction** — Claude reads each doc and emits `{entities: [{name, type, description}], relations: [{source, predicate, target}]}` via Pydantic schema. Types: PERSON, ORG, LOCATION, EVENT, ARTIFACT. Prompt emphasizes central entities only (noise control).
2. **Entity resolution** — duplicates are clustered by Claude using one-sentence descriptions as disambiguation context (e.g., "Edwin Aldrin" and "Buzz Aldrin" collapse to one canonical node despite zero string overlap).
3. **Graph assembly** — canonical entities → NetworkX MultiDiGraph nodes. Edges carry predicate + source doc. Multi-hop queries serialize relevant subgraphs back to Claude for synthesis.

## Key code/config

```python
class ExtractedGraph(BaseModel):
    entities: list[Entity]   # name, type, description
    relations: list[Relation]  # source, predicate, target
```

Benchmark on 6 Apollo Wikipedia summaries: 22 canonical entities from 36 raw mentions (39% dedup), 34 typed relations, 1 connected component.

## Measured improvements

| Criterion | KG | Vector RAG |
|---|---|---|
| Multi-hop chains | Native traversal | Token budget exhausted |
| Latency | ms | Moderate (API) |
| Setup cost | Higher (extract + resolve) | Lower (embed + index) |
| Hallucination | Lower (grounded edges) | Moderate |

No A/B accuracy numbers given. The argument is structural: chained facts that flat RAG can't answer.

## ROOK applicability

**ROOK already does this.** `graphify` is a markdown→knowledge-graph builder; every agent has a `graphify-out/` subgraph; librarian + deep-researcher are Tier 1 (ChromaDB + graphify). The cookbook pattern matches ROOK's architecture closely.

The ONE gap worth noting: cookbook does *typed* entity resolution via Claude-clustering on descriptions. graphify's resolution heuristic (verify) may be lighter — string-similarity rather than LLM-clustering. If graphify currently produces duplicate canonical entities for "Buzz Aldrin" / "Edwin Aldrin"-shaped cases, adopting Claude-based resolution would tighten it.

## Recommended action

**already-implemented** — graphify covers the core pattern. Optional follow-up: audit graphify's entity-resolution layer; if string-based, add a Claude-clustering pass for high-confidence dedup. Worth a 1-day investigation, not a sprint item.
