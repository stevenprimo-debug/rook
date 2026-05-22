---
name: llamaindex-multi-doc-agents
source: https://github.com/anthropics/claude-cookbooks/blob/main/third_party/LlamaIndex/Multi_Document_Agents.ipynb
fetched: 2026-05-22
category: Integrations
rook-relevance: medium
rook-status: skip
---

# LlamaIndex Multi-Document Agents

## What it is

Hierarchical RAG for large doc collections. Each document gets its own ReAct agent with two query engines (vector for retrieval, summary for synthesis). Per-doc agents wrap as IndexNodes with descriptive metadata. A top-level VectorStoreIndex routes queries by semantic match on summary descriptions. Hierarchical = scales to 1000s of docs without a flat index.

Tradeoff: multi-hop latency vs. precision + interpretability.

## Key code/config

Per doc: VectorStoreIndex(chunk_size=512) + SummaryIndex → wrapped as QueryEngineTool → ReActAgent → IndexNode(text=summary, obj=agent).

Top level: VectorStoreIndex over IndexNodes → similarity_top_k=1 picks the right agent.

LLM: claude-opus-4-1 (temp=0). Embeddings: BAAI/bge-base-en-v1.5.

## Measured improvements / costs

No benchmarks. Qualitative routing demo only.

## ROOK applicability

**The PATTERN is interesting; the STACK is not.** LangChain/LlamaIndex are explicitly not-installed in ROOK (`_CLAUDE.md` Section 7). ROOK uses graphify + ChromaDB + sentence-transformers for the same job.

The architectural idea — per-document specialist agents under a top-level router — already exists in ROOK at the agent level: chief-of-staff routes to domain-specialist agents (sales-director, designer, etc.). The cookbook applies it at the document level. ROOK could mirror this with per-project subagents (e.g., projects/<customer-name>/agents/) but that's a v4 architectural decision, not a v3.1 sprint item.

## Recommended action

**skip** — LlamaIndex integration is explicitly out-of-stack. The hierarchical-routing pattern is already covered by ROOK's chief-of-staff dispatch model at the right level of granularity. Reconsider in v4 if customer projects accumulate 100+ docs that need per-project specialist agents.
