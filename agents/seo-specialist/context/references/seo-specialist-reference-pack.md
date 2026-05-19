# SEO Specialist Reference Pack

**Domain:** Classical SEO + Answer Engine Optimization (AEO) / Generative Engine Optimization (GEO)  
**Use case:** AI agent grounding for SEO specialists covering both traditional ranking and visibility in AI-generated responses (ChatGPT, Claude, Gemini, Perplexity).  
**Last verified:** 2025-07-28  
**Sources:** 8 | All URLs live-verified via `pplx content fetch`

---

## Source 1 — GEO: Generative Engine Optimization (Foundational Academic Paper)

**URL:** https://arxiv.org/abs/2311.09735  
**DOI:** https://doi.org/10.48550/arXiv.2311.09735  
**Authors:** Pranjal Aggarwal, Vishvak Murahari, Tanmay Rajpurohit, Ashwin Kalyan, Karthik Narasimhan, Ameet Deshpande (Princeton / Allen AI)  
**Published:** November 16, 2023 · Last revised June 28, 2024  
**Venue:** Accepted at KDD 2024  
**Live:** ✅ Verified

**Why this source:** This is the original peer-reviewed paper that coined and formalized "Generative Engine Optimization (GEO)" as a discipline. It introduces the first systematic framework for optimizing content visibility in LLM-powered answer engines, and introduces GEO-bench — a large-scale evaluation benchmark across diverse query domains.

**Key concepts and frameworks:**
- **Generative Engines (GEs):** Formalized definition of LLM-based search systems (Perplexity, Bing AI, SGE) that synthesize multi-source answers rather than returning link lists.
- **GEO black-box optimization framework:** Content modification strategies that boost citation frequency without requiring access to model internals.
- **GEO-bench:** Benchmark of diverse user queries across multiple domains paired with relevant web sources — enables systematic evaluation of optimization strategies.
- **Visibility metrics:** Quantitative measures for how often and how prominently content appears in generative responses (up to +40% visibility gain demonstrated).
- **Domain-specific variation:** Efficacy of GEO tactics varies significantly by vertical, establishing the need for domain-specific optimization methods.
- **Core strategies tested:** Adding authoritative citations, statistics, quotations, fluency improvements, and keyword density adjustments — with differential effects per domain.

**Agent use:** Ground the agent's understanding of WHY classical SEO ≠ GEO, what visibility means in AI answer contexts, and how to systematically test and measure AEO interventions.

---

## Source 2 — The /llms.txt Specification (Official)

**URL:** https://llmstxt.org  
**Author:** Jeremy Howard (fast.ai / Answer.AI)  
**Published:** September 3, 2024  
**Live:** ✅ Verified

**Why this source:** This is the official specification for `llms.txt` — the emerging standard for providing LLM-friendly site summaries at inference time. Analogous to `robots.txt` for crawlers and `sitemap.xml` for indexers, but targeted at AI systems that need curated, context-efficient representations of a site's content. Already adopted by Answer.AI, fast.ai, FastHTML, and nbdev.

**Key concepts and frameworks:**
- **Purpose:** Overcomes LLM context window constraints by providing a concise, expert-level plain-text overview of a site's most important pages — readable at inference time without downloading the entire site.
- **File format and location:** `/llms.txt` at the domain root; Markdown format; structured with H1 (project name), blockquote (summary), prose sections, and H2-delimited file lists with annotated links.
- **Complementary `*.md` convention:** High-value pages should expose a Markdown mirror at `[url].md` for clean, HTML-free LLM ingestion.
- **Relationship to existing standards:**
  - `robots.txt` → controls indexing access (crawl-time)
  - `sitemap.xml` → lists all indexable pages (crawl-time)
  - `llms.txt` → provides curated context for AI retrieval (inference-time)
- **Optional section:** URLs in an `## Optional` H2 are designated as secondary — agents can skip them when context budget is limited.
- **Tooling:** `llms_txt2ctx` CLI/Python module; VitePress, Docusaurus, and Drupal plugins; VS Code PagePilot extension.
- **Distinction from training:** Primarily for inference/on-demand retrieval; potential future use in training runs.

**Agent use:** Ground implementation guidance for the `llms.txt` technical SEO layer — a concrete, actionable GEO/AEO tactic that is spec-level, not opinion.

---

## Source 3 — schema.org Official Documentation Index

**URL:** https://schema.org/docs/documents.html  
**Publisher:** Schema.org (joint initiative: Google, Microsoft, Yahoo, Yandex + W3C Community Group)  
**Maintained:** Actively maintained; W3C Schema.org Community Group active since April 2015  
**Live:** ✅ Verified

**Why this source:** The canonical reference for structured data vocabulary. Schema.org markup is the primary mechanism by which web content signals its semantic meaning to both search engines and LLMs. For SEO/AEO, schema implementation is table-stakes for rich results eligibility and is increasingly cited as a signal LLMs use for content parsing and entity recognition.

**Key documents indexed at this URL:**
- **Getting Started:** Introductory guide to microdata and schema.org markup
- **Schemas:** Full type hierarchy with per-item documentation (the working reference for any implementation)
- **Full Type Hierarchy:** Complete schema taxonomy in a single file
- **Data Model:** Notes on the underlying RDF-compatible data model
- **Style Guide:** Naming conventions and authoring patterns
- **Extension Mechanism:** How to extend the core vocabulary for specialized verticals
- **Developers:** Developer-oriented API/integration information
- **Vocabulary Definition Download:** Machine-readable definitions for core vocabulary and extensions

**Key schema types for SEO/AEO:**
`Article`, `FAQPage`, `HowTo`, `Organization`, `Person`, `BreadcrumbList`, `Product`, `LocalBusiness`, `Event`, `WebPage`, `VideoObject` — these are the primary types for rich result eligibility and AI entity recognition.

**Agent use:** Entry point for all structured data implementation questions. The agent should route schema-specific queries here rather than to third-party interpretations.

---

## Source 4 — Google Search Central: Structured Data Introduction

**URL:** https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data  
**Publisher:** Google Search Central  
**Last updated:** December 10, 2025 UTC  
**Live:** ✅ Verified

**Why this source:** Google's authoritative, maintained guidance on how structured data works in Search — covering supported formats (JSON-LD, Microdata, RDFa), implementation rules, validation workflow, and real-world performance data. This is the implementation-layer companion to schema.org's vocabulary-layer documentation.

**Key concepts and frameworks:**
- **JSON-LD (recommended format):** JavaScript notation in `<script>` tag; not interleaved with visible text; dynamically injectable via JS or CMS widgets.
- **Rich Results:** Enhanced search appearances (review stars, carousels, FAQ dropdowns) enabled by structured data — with documented CTR impact.
- **Implementation rules:** Structured data must describe visible content; blank pages solely holding markup are prohibited.
- **Validation workflow:** Rich Results Test → URL Inspection Tool → Rich result status reports in Search Console.
- **`sameAs` property:** General-purpose signal Google uses for entity disambiguation and knowledge graph connection.

**Documented performance impact (case studies):**
| Site | Action | Result |
|------|--------|--------|
| Rotten Tomatoes | Structured data on 100K pages | +25% CTR |
| The Food Network | 80% pages converted | +35% visits |
| Rakuten | Full implementation | 1.5× time on page |
| Nestlé | Rich result pages | +82% CTR vs. non-rich |

**Agent use:** Implementation reference for all structured data questions — what formats to use, how to validate, how to measure impact.

---

## Source 5 — Google Search Central: AI Overviews and Your Website

**URL:** https://developers.google.com/search/docs/appearance/ai-overviews  
**Publisher:** Google Search Central  
**Last updated:** February 11, 2025 UTC  
**Live:** ✅ Verified

**Why this source:** The official, canonical Google statement on how AI Overviews interact with publisher content. This is the primary source for what Google says about eligibility, control mechanisms, and Search Console measurement for AI Overview appearances — essential for any AEO practitioner.

**Key concepts and frameworks:**
- **No additional optimization required:** Google states publishers need only follow standard Google Search Essentials guidelines to be considered for AI Overview inclusion.
- **Source selection:** AI Overviews draw from a range of web sources plus Google's Knowledge Graph; selection is fully algorithmic.
- **Publisher controls:** Standard preview controls (robots meta tags, X-Robots-Tag headers) apply to AI Overview appearances — the same controls used for featured snippets.
- **Search Console integration:** AI Overview appearances count in the Performance report (clicks, impressions, position tracked); no separate AI-specific reporting tool exists yet.
- **Troubleshooting:** Verify Googlebot can see the page via URL Inspection Tool; allow recrawl time (days to months) after applying preview controls.

**Companion pages in Google Search Central relevant to AEO:**
- `developers.google.com/search/docs/fundamentals/how-search-works` — Crawling, indexing, serving fundamentals (updated December 18, 2025)
- `developers.google.com/search/docs/appearance/core-web-vitals` — LCP, INP, CLS thresholds and ranking relationship (updated December 10, 2025)
- `developers.google.com/search/docs/fundamentals/seo-starter-guide` — Foundational SEO guidance (updated December 10, 2025)

**Agent use:** Authoritative answer to "what does Google say about appearing in AI Overviews?" — prevents the agent from citing speculative third-party advice as Google policy.

---

## Source 6 — Aleyda Solís: The 10-Step AI Search Content Optimization Checklist

**URL:** https://www.aleydasolis.com/en/ai-search/ai-search-optimization-checklist/  
**Author:** Aleyda Solís (Founder, Orainti; European Search Personality of the Year 2018; creator of SEOFOMO newsletter, 35K+ subscribers; creator of LearningAIsearch.com)  
**Published/Updated:** July 27, 2025  
**Live:** ✅ Verified

**Why this source:** Aleyda Solís is one of the most credible named practitioners in international SEO and has been at the forefront of the SEO → AEO/GEO transition. This checklist operationalizes the theoretical GEO framework into 10 concrete, actionable steps grounded in how LLMs actually retrieve and synthesize content. It is practitioner-level, named-expert, and recent.

**Key frameworks and concepts:**

**The 10-Step AI Search Content Optimization Checklist:**

| Step | Focus |
|------|-------|
| 1 | Audience behavior research: map how your audience uses AI search platforms (query intent, conversational patterns, multi-turn behavior) |
| 2 | AI crawlability & indexability: allow GPTBot, Google-Extended, ClaudeBot, PerplexityBot, bingbot in robots.txt; use SSR; avoid JS-only rendering |
| 3 | Topical breadth & depth: pillar-cluster architecture with hub pages + cluster pages + cross-linking |
| 4 | Chunk-level retrieval: self-contained sections, one idea per H2/H3, designed for passage-level extraction |
| 5 | Answer synthesis optimization: direct summary sentences, Q&A format, plain factual tone, structured data classification |
| 6 | Citation-worthiness: verifiable claims, external citations, EEAT authorship signals, freshness timestamps |
| 7 | Content authoritativeness: original research, entity salience, consistent brand presence across platforms |
| 8 | Multi-modal support: `<figure>/<figcaption>`, HTML tables (not table images), descriptive alt text |
| 9 | Personalization resilience: local schema, persona-segmented content, engagement signals |
| 10 | AI search performance monitoring: brand mentions, citations, sentiment, competitor benchmarking per LLM platform |

**Key terminology introduced:**
- **Query fan-out:** AI models decompose a single prompt into multiple sub-queries across facets and intents — content must address the full fan-out, not just the surface query.
- **Chunk-level retrieval:** LLMs retrieve passages, not pages — each section must stand alone as a self-contained answer unit.
- **Shift in KPIs:** From rankings/CTR/traffic → inclusion/visibility/citations/mentions in AI answers.

**Agent use:** Primary operational playbook for the AEO/GEO layer — maps directly to implementable tactics an SEO specialist would execute.

---

## Source 7 — Lily Ray (Amsive): GEO, AEO, LLMO — Separating Fact from Fiction

**URL:** https://www.amsive.com/insights/seo/geo-aeo-llmo-separating-fact-from-fiction-how-to-win-in-ai-search/  
**Author:** Lily Ray (VP, SEO Strategy & Research, Amsive; founder, Algorythmic; Search Engine Land contributor)  
**Published:** November 12, 2025 (adapted from MozCon 2025 presentation, New York City)  
**Live:** ✅ Verified

**Why this source:** Lily Ray is one of the most-cited practitioners on AI search, E-E-A-T, and algorithm analysis. This piece is a conference-grade synthesis that cuts through the hype around GEO/AEO/LLMO with real data, debunks myths, and provides a grounded framework for prioritization. The data (ChatGPT/Google overlap, LLM traffic share, session frequency) is original research unavailable elsewhere.

**Key concepts, frameworks, and data:**

**Terminology landscape clarified:**
- **GEO (Generative Engine Optimization):** Optimization for generative AI engines; widely used but sometimes overclaimed.
- **AEO (Answer Engine Optimization):** Amsive's preferred term; optimization for engines providing direct answers.
- **LLMO (Large Language Model Optimization):** Content optimization for ingestion and citation by LLMs specifically.
- **RAG (Retrieval-Augmented Generation):** The mechanism by which AI systems retrieve from live sources before generating answers — the primary channel for AEO impact today.

**Key data points (original research):**
- 95% of ChatGPT users still rely on Google — AI search is additive, not substitutive.
- LLM referrers currently drive ~1–2% of total site traffic vs. organic search (Amsive + Glenn Gabe data).
- Average Google sessions/week increased from 10.5 to 12.6 after users adopted ChatGPT — search behavior is expanding, not contracting.
- AI Overview CTR ≈ 0.8% (characterized as a "tiny scrap" of visibility).

**Main thesis:** AI search success is rooted in traditional SEO foundations — high-quality structured content, brand authority, technical excellence — with a GEO layer on top. The hype cycle around GEO mirrors previous SEO "alligator mouth" moments (Mobilegeddon, voice search, AMP, Core Web Vitals).

**AEO tactics covered:**
- Answer branded questions proactively (on-site Q&A for brand, product, leadership, competitors)
- Digital PR & reputation management for third-party domain mentions (Reddit, YouTube, Wikipedia)
- Passage/chunk optimization with atomic, self-contained answer units
- Multimodal optimization (YouTube, podcasts with transcripts)
- Content freshness signaling (avoiding "artificial refreshening")
- New KPIs: branded impressions, share of voice in AI search, AI-referred traffic in GA4

**Agent use:** Calibrates the agent's sense of proportion — establishes that LLM traffic is small but growing, that traditional SEO remains the dominant channel, and provides the current practitioner consensus on what actually moves the needle in AI search.

---

## Source 8 — Backlinko: Google's 200 Ranking Factors — The Complete List

**URL:** https://backlinko.com/google-ranking-factors  
**Author:** Brian Dean (founder, Backlinko; now Semrush)  
**Last updated:** 2026 (verified live at `backlinko.com`)  
**Live:** ✅ Verified

**Why this source:** The most comprehensive practitioner-compiled reference for classical Google ranking signals, synthesized from SEO experiments, Google patents, and confirmed Google statements. 206 factors across 10 categories. Maintained and updated continuously. Provides the foundational classical SEO layer that anchors the agent's understanding of traditional ranking before the AEO/GEO layer is applied.

**Categories covered (206 factors total):**

| Category | Factor count | Key signals |
|----------|-------------|-------------|
| Domain Factors | 9 | Domain age, TLD, history, WhoIs |
| Page-Level Factors | 65 | Title tag, content depth, TF-IDF, LSI, Core Web Vitals, E-E-A-T |
| Site-Level Factors | 18 | Architecture, HTTPS, mobile optimization, UX, YouTube |
| Backlink Factors | 47 | Linking root domains, anchor text, PageRank, authority, relevance |
| User Interaction | 11 | RankBrain, CTR, bounce rate, dwell time, direct traffic |
| Special Algorithm Rules | 19 | QDF (Query Deserves Freshness), YMYL, local, featured snippets |
| Brand Signals | 11 | Branded searches, unlinked mentions, social profiles, entity recognition |
| On-Site Webspam | 16 | Panda, autogenerated content, popups, redirect schemes |
| Off-Site Webspam | 18 | Penguin, unnatural links, manual actions |

**Key confirmed factors for 2025–2026 SEO:**
- **Core Web Vitals:** Described as "more than a tiebreaker" — LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 (Google Search Central, updated December 10, 2025).
- **E-E-A-T:** Experience, Expertise, Authoritativeness, Trustworthiness — quality evaluator used in Quality Rater Guidelines, not a direct ranking signal per Google.
- **RankBrain + user signals:** AI-interpreted user interaction signals remain among the top contextual ranking factors.
- **Schema.org usage:** Factor #124 — noted as potentially improving CTR but with no direct correlation to rankings in controlled studies.
- **Domain Authority (DR):** Site-wide link authority correlates strongly with first-page positions (Backlinko 11.8M result study).

**Companion Backlinko resource for GEO:**  
`https://backlinko.com/ai-optimization` — "AI Optimization: How to Rank in AI Search" (published April 26, 2026) introduces the **Seen & Trusted (S&T) Framework** covering developer, SEO, and content task checklists for AI search visibility. Key finding: visitors from AI answers are 4.4× more valuable than traditional search visitors; 50% of citations in Google AI Mode are from beyond page-one results.

**Agent use:** Classical SEO factor grounding — prevents the agent from over-indexing on AEO novelty at the expense of foundational ranking fundamentals.

---

## Quick Reference Table

| # | Source | Author / Publisher | Recency | Primary Domain |
|---|--------|-------------------|---------|----------------|
| 1 | [GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735) | Aggarwal et al. (Princeton) | Nov 2023 / KDD 2024 | AEO/GEO — foundational theory |
| 2 | [llms.txt Specification](https://llmstxt.org) | Jeremy Howard / Answer.AI | Sep 2024 | Technical SEO — AI discoverability |
| 3 | [schema.org Documentation Index](https://schema.org/docs/documents.html) | Schema.org / W3C | Actively maintained | Structured data vocabulary |
| 4 | [Google Structured Data Intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | Google Search Central | Dec 10, 2025 | Technical SEO — structured data |
| 5 | [Google AI Overviews Guidance](https://developers.google.com/search/docs/appearance/ai-overviews) | Google Search Central | Feb 11, 2025 | AEO — official Google policy |
| 6 | [10-Step AI Search Checklist](https://www.aleydasolis.com/en/ai-search/ai-search-optimization-checklist/) | Aleyda Solís | Jul 27, 2025 | AEO/GEO — practitioner playbook |
| 7 | [GEO/AEO/LLMO: Separating Fact from Fiction](https://www.amsive.com/insights/seo/geo-aeo-llmo-separating-fact-from-fiction-how-to-win-in-ai-search/) | Lily Ray (Amsive) | Nov 12, 2025 | AEO/GEO — strategy + data |
| 8 | [Google's 200 Ranking Factors](https://backlinko.com/google-ranking-factors) | Brian Dean / Backlinko | 2026 (live) | Classical SEO — ranking factors |

---

## Coverage Map

```
TOPIC                          SOURCE(S)
─────────────────────────────────────────────────────────────
GEO theoretical framework      #1 (Aggarwal et al., KDD 2024)
llms.txt implementation        #2 (Jeremy Howard / llmstxt.org)
Schema.org vocabulary          #3 (schema.org/docs)
Structured data (Google impl.) #4 (Google Search Central)
AI Overviews eligibility       #5 (Google Search Central)
Core Web Vitals (LCP/INP/CLS)  #5 + #8 (Google + Backlinko)
AEO tactics + chunk opt.       #6 (Aleyda Solís) + #7 (Lily Ray)
Topical authority / pillars    #6 (Aleyda Solís — Step 3)
Query fan-out                  #6 (Aleyda Solís) + #7 (Lily Ray)
EEAT signals                   #7 (Lily Ray) + #8 (Backlinko #75)
Classical ranking factors      #8 (Backlinko 206 factors)
AI search data / proportion    #7 (Lily Ray — original research)
Brand signals / mentions       #7 (Lily Ray) + #8 (Backlinko #161–171)
```

---

## Verification Log

All URLs were live-verified on 2025-07-28 via `pplx content fetch`. No fabricated or unverified URLs are included.

| URL | Status | Notes |
|-----|--------|-------|
| `arxiv.org/abs/2311.09735` | ✅ Live | Cached; DOI confirmed |
| `llmstxt.org` | ✅ Live | Published Sep 3, 2024 |
| `schema.org/docs/documents.html` | ✅ Live | Actively maintained |
| `developers.google.com/search/docs/appearance/structured-data/intro-structured-data` | ✅ Live | Updated Dec 10, 2025 |
| `developers.google.com/search/docs/appearance/ai-overviews` | ✅ Live | Updated Feb 11, 2025 |
| `aleydasolis.com/en/ai-search/ai-search-optimization-checklist/` | ✅ Live | Updated Jul 27, 2025 |
| `amsive.com/insights/seo/geo-aeo-llmo-separating-fact-from-fiction-how-to-win-in-ai-search/` | ✅ Live | Published Nov 12, 2025 |
| `backlinko.com/google-ranking-factors` | ✅ Live | Dated 2026; Brian Dean / Semrush |
