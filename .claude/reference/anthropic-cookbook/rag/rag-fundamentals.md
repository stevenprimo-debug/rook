---
name: rag-fundamentals
source: https://github.com/anthropics/claude-cookbooks/blob/main/capabilities/retrieval_augmented_generation/guide.ipynb
fetched: 2026-05-22
category: RAG & Retrieval
rook-relevance: high
rook-status: absorb-recommended
---

# RAG with Summary Indexing + Reranking

## What it is

Three-tier RAG progression: (L1) baseline cosine-similarity over heading-chunked embeddings, (L2) summary indexing — hierarchical doc-section summaries matched first, then granular retrieval, (L3) Claude-as-reranker passing top-K candidates through Claude itself to reorder by semantic relevance to the query. Each layer adds latency + cost but lifts retrieval precision and end-to-end answer accuracy.

The notebook uses Voyage AI embeddings (`voyage-2`) at 128-token chunks split on headings.

## Key code/config

- **Chunking**: heading-based semantic boundaries; 128-token windows
- **Embeddings**: batch through Voyage AI `voyage-2`
- **Summary index**: separate embedding pass over LLM-generated section summaries → matched before chunk retrieval to broaden query → chunk mapping
- **Reranker**: Claude reads `(query, candidates)` and returns reordered list with relevance scores

## Measured improvements

Three-tier pipeline vs. baseline:

| Metric | Baseline | Optimized | Delta |
|---|---|---|---|
| Precision | 0.43 | 0.44 | +0.01 |
| Recall | 0.66 | 0.69 | +0.03 |
| F1 | 0.52 | 0.54 | +0.02 |
| MRR | 0.74 | 0.87 | **+0.13** |
| End-to-end accuracy | 71% | 81% | **+10pts** |

MRR jump is the headline — relevant docs land near the top of the result set far more often.

## ROOK applicability

ROOK's librarian + deep-researcher are Tier 1 (ChromaDB + graphify). They currently do single-pass embedding retrieval. Adding (a) a summary-index layer and (b) a Claude-reranker step at the top of result sets would directly improve research quality — exactly the failure mode where deep-researcher returns the right doc but ranked #5 instead of #1. graphify already extracts entities (similar shape), but the reranker step is the bigger lift for measurable accuracy.

## Recommended action

**absorb-recommended** — add a reranker step to librarian + deep-researcher's retrieval pipeline. graphify queries top-20 → Claude-rerank → return top-5. Effort: ~2 days. Payoff: based on cookbook numbers, +10pts end-to-end accuracy on research questions. Summary-indexing is a follow-on (more effort, smaller incremental win).
