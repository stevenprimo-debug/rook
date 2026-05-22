---
name: rook-cookbook-gap-analysis
fetched: 2026-05-22
prior-coverage: chief-of-staff agent (already), contextual retrieval (already), sub-agents Haiku/Opus (already)
total-notebooks-reviewed: 13
---

# ROOK ↔ Anthropic Cookbook Gap Analysis

## Executive summary

ROOK already matches the cookbook on the structural patterns that matter most (chief-of-staff orchestration, knowledge-graph construction via graphify, skill folder shape, sub-agent dispatch). The biggest unfilled gap is **evaluation infrastructure** — ROOK ships zero regression coverage today. Second-biggest: **prompt caching** for cohort customers building API-direct pipelines on top of ROOK agents. Recommended action breakdown across 13 reviewed notebooks: **3 already-implemented, 5 absorb-recommended, 3 inherit-via-skill, 2 skip.**

## Already implemented (ROOK matches cookbook pattern)

| ROOK surface | Cookbook source | How ROOK does it |
|---|---|---|
| Knowledge graph over corpus | `capabilities/knowledge_graph/guide.ipynb` | `graphify` skill builds entity+relation graph; every agent has `graphify-out/`; librarian + deep-researcher Tier 1 |
| Skill folder + frontmatter shape | `skills/notebooks/03_skills_custom_development.ipynb` | `agents/_template/SKILL.md` is a superset (adds bench, voice spine, modes, routing) |
| Hierarchical retrieval routing | `third_party/LlamaIndex/Multi_Document_Agents.ipynb` | chief-of-staff dispatches to domain agents at the agent level (same idea, different granularity) |

## Absorb-recommended (high-leverage gaps)

Sorted by payoff/effort ratio descending.

| Gap | Cookbook source | Which ROOK agent/skill absorbs | Effort | Expected payoff |
|---|---|---|---|---|
| Eval scaffold (`.claude/evals/` + harness + 3 starter sets) | `misc/building_evals.ipynb` + `tool_evaluation/tool_evaluation.ipynb` | New cross-agent infra; consumed by all 20 agents at ship-vault QA | 3-4 days | Catches regression BEFORE cohort zip; replaces vibes-testing |
| Claude-as-reranker on top of graphify retrieval | `capabilities/retrieval_augmented_generation/guide.ipynb` | librarian + deep-researcher | 2 days | Cookbook reports +10pts end-to-end accuracy, +0.13 MRR |
| Pydantic schemas shelf for Tier 2 agents | `tool_use/tool_use_with_pydantic.ipynb` | account-manager, finance-manager, sales-director, shopify-agent, trading-analyst, inbox-manager | 1 day (6 schemas) | Eliminates silent record corruption; self-healing tool errors |
| Chart-and-color reading patterns | `multimodal/reading_charts_graphs_powerpoints.ipynb` | engineering-lead (drawing packs); sales-director + marketing-director (vendor decks) | 2 hours | Tighter extraction on multi-series charts; prompt-level fix |
| Prompt caching guidance for cohort | `misc/prompt_caching.ipynb` | New `.claude/reference/prompt-caching.md` shelf | Half day | Up to 90% cost cut for customers wiring API-direct flows |

## Inherit-via-skill (customer-extensibility surface)

Patterns the customer should be able to opt-in to.

| Pattern | Cookbook source | How to expose |
|---|---|---|
| Batch-tool meta-pattern for parallel calls | `tool_use/parallel_tools.ipynb` | Document in `.claude/reference/` for API-direct paths; Claude Code's native parallel `function_calls` blocks already cover the runtime |
| Extended thinking + tool use | `extended_thinking/extended_thinking_with_tool_use.ipynb` | Document signed-thinking-block preservation for operators building API-direct second-opinion verifiers |
| Metaprompt template generator | `misc/metaprompt.ipynb` | `prompt-builder` + `skill-creator` skills already cover this; optionally fold "identify variables before drafting" heuristic into chief-of-staff dispatch-brief template |

## Skip (intentional non-implementation)

| Pattern | Cookbook source | Why ROOK doesn't need it |
|---|---|---|
| Direct vision content blocks | `multimodal/getting_started_with_vision.ipynb` | markitdown owns the input layer; agents never see raw image blocks |
| LlamaIndex multi-document agents | `third_party/LlamaIndex/Multi_Document_Agents.ipynb` | LangChain/LlamaIndex explicitly not-installed (`_CLAUDE.md` §7); ROOK uses graphify + ChromaDB |

## Recommended v3.1 absorb sprint scope

Ordered top-5 absorb-recommended items with first-pass acceptance criteria.

1. **Eval scaffold** (3-4 days) — `.claude/evals/` directory with: (a) `scripts/run-evals.py` harness, (b) 3 starter eval sets — chief-of-staff routing (code-graded JSONL), copywriter voice (Claude-judge rubric), librarian retrieval precision (code-graded). Acceptance: `python scripts/run-evals.py` returns aggregate pass-rate across all 3 sets; harness fails CI if pass-rate drops below baseline.

2. **Claude-reranker for graphify retrieval** (2 days) — librarian + deep-researcher Step 2 changes: query graphify for top-20 → pass `(query, candidates)` through Claude with relevance-scoring prompt → return top-5. Acceptance: A/B against current baseline on 20 fixed research questions shows ≥5pt end-to-end accuracy lift OR documented null result.

3. **Pydantic schemas shelf** (1 day) — `.claude/reference/schemas/` with 6 BaseModel modules (Deal, Invoice, Order, Setup, Thread, Outreach). Each Tier 2 agent's SKILL.md Step 2 loads relevant schema. Acceptance: one Tier 2 agent (sales-director) fully retrofitted; remaining 5 follow same pattern.

4. **Prompt caching reference shelf** (half day) — `.claude/reference/prompt-caching.md` mapping ROOK context surfaces (voice spine, SKILL.md, MEMORY.md) to cache_control strategies with recommended TTLs. Acceptance: customer-facing doc that maps Rule #12 context-load gate to cache breakpoints.

5. **Chart-reading prompt patterns** (2 hours) — append "chart and slide reading" prompt-pattern block to engineering-lead's SKILL.md. Cross-reference from sales-director, marketing-director. Acceptance: three agents updated; pattern includes color-first extraction + "describe every data point" + structured XML narration.

**Total sprint estimate: 7-8 days for all 5 items.** Items 1+2+3 are core regression-and-quality infrastructure; items 4+5 are documentation + prompt heuristics with thin code surface.
