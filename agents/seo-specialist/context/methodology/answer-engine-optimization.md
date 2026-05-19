# Answer-Engine Optimization (AEO)

## What This Framework Is

Answer-Engine Optimization is the discipline of earning inclusion
in AI-generated answers — Google AI Overviews, Perplexity,
ChatGPT Search, Claude search, Gemini summaries — when users
search a query whose answer your content could serve. The
framework recognizes that in 2026, a meaningful fraction of
search attention is captured by AI-answer surfaces before users
ever click a traditional search result. Optimizing only for SERP
ranking misses this attention.

AEO overlaps significantly with SERP ranking fundamentals
(intent match, content depth, authority signals) but diverges
in specific ways:

- AI engines reward **answer-shaped content** (clear questions,
  direct answers, structured information) over narrative-shaped
  content.
- AI engines reward **citation-ready content** (specific claims
  with sources, data points with attribution) because the engine
  needs to attribute the answer to a source.
- AI engines reward **schema markup** (structured data telling
  the engine what the page is about, what it answers, what
  entities it covers).
- AI engines reward **brand trust signals** that may not align
  with raw backlink authority — being mentioned in
  authoritative roundups, appearing in industry publications,
  having owner-author bylines with verifiable credentials.

The framework holds that **AI-answer inclusion is the new top
of the funnel**. SERP ranking remains valuable for users who
click through; AEO captures users who never click through and
who would have been lost without inclusion in the answer.

## Why It Matters For This Agent

SEO Specialist's Intent-Match-Pole and Authority-Build-Pole both
extend into AEO. Intent matching for AI-answer surfaces requires
recognizing what AI engines surface (typically informational and
commercial-investigation queries) and structuring content to be
the cited source.

The Anti-Default-Pole (shared with Creative Director's voice
spine) also applies: AI engines tend to surface generic content
because most content is generic; specific, brand-voice content
that AI engines learn to cite earns over time.

For the operator's mission surfaces:
- **[your product]** content competing for "AI tools for touring
  AV pros" type queries must be cited by AI engines, not just
  ranked in SERP.
- **[your physical/SaaS product] / [your product]** content competing for "best
  cue management software" type queries must appear in AI
  comparisons.
- **Public [your employer] content** competing for "AV integration partner"
  type queries must appear in AI-generated shortlists.

## Core Concepts

### 1. The AI-Answer Funnel

User behavior on AI-answer surfaces follows a different funnel:

1. **Query** — user types or speaks a question.
2. **AI answer generated** — the engine assembles an answer from
   indexed content.
3. **Citations surfaced** — the engine cites 2-5 sources.
4. **User decision** — accept the answer, click a citation for
   more, refine the query, or ignore.
5. **Possible click-through** — only if the user needs more
   depth than the AI answer provided.

The funnel is shorter than traditional SERP. Many queries
resolve at step 4 — users accept the answer without clicking
through. AEO optimizes for being cited (step 3), since being
cited captures attention even when clicks don't follow.

### 2. Answer-Shaped Content

AI engines extract answer-shaped content more reliably than
narrative-shaped content. Specific patterns:

- **Question-then-answer headers** — H2 phrased as the user's
  likely question, followed by a clear, comprehensive answer in
  the first paragraph.
- **Definition paragraphs** — early in the page, a clear
  definition of the topic, framed as "X is...".
- **Lists for enumerable answers** — numbered or bulleted lists
  for items the AI can extract directly.
- **Tables for comparisons** — comparison tables for "best X for
  Y" queries.
- **Specific numbers and dates** — concrete data the AI can cite.

The discipline: write the answer-shaped section first, then
build the narrative around it. The AI engine extracts the
answer; the narrative serves users who click through.

### 3. Citation-Ready Content

AI engines need to cite sources. Content that is citation-ready
includes:

- **Specific claims** — "ICT order blocks form on the last
  opposite-color candle before a strong directional move" — not
  "order blocks form in certain places."
- **Attributed data** — "according to <source>, 47% of touring
  shows in 2025 used digital playback systems" — with source
  identifiable.
- **Named examples** — specific case studies, specific products,
  specific people (where appropriate; never name living figures
  inside agent output per the operator's locked rule).
- **Author credentials** — bylines with verifiable expertise
  signals.

Vague content cannot be cited because the AI engine can't extract
a specific claim. Citation-ready content earns inclusion.

### 4. Schema Markup

Structured data tells AI engines what the page is about. Key
schemas for AEO:

- **Article schema** — for editorial content, with author,
  publication date, headline.
- **FAQPage schema** — for Q&A content; AI engines extract these
  directly.
- **HowTo schema** — for instructional content.
- **Product schema** — for product pages, with name, price,
  rating, availability.
- **Organization schema** — for brand identity, with logo,
  social profiles, contact info.
- **BreadcrumbList schema** — for site architecture signals.

Implementation: JSON-LD in the page head. Validate with Google's
Rich Results Test or Schema.org validator. AI engines parse
schema directly; without it, the engine relies on inference and
may extract incorrectly.

### 5. Brand-Entity Recognition

AI engines build internal models of brands and entities. Pages
on a recognized brand entity earn easier inclusion than pages
on an unrecognized entity. Building brand-entity recognition:

- **Consistent naming** — same brand name, same product names
  across every surface.
- **Knowledge graph presence** — Wikipedia, Wikidata, Google
  Knowledge Graph (if eligible).
- **Authoritative mentions** — industry publications, podcasts,
  conference speakers list, review sites.
- **Social profiles** — verified profiles on major platforms,
  consistent identity.
- **About page completeness** — clear ownership, history, mission,
  team.

For [your product], [your physical/SaaS product], and [your product line], brand-entity
work is foundational: AI engines need to know what these are
before they can surface them in answers.

### 6. Conversational Query Patterns

AI-answer surfaces handle conversational queries better than
keyword queries. Users type or speak full questions:

- "What's the best AI tool for managing playback cues on tour?"
- "How does [your physical/SaaS product] compare to QLab for show prep?"
- "Who's running cohort programs for AV professionals transitioning
  to AI work?"

Content optimized for AEO mirrors these patterns. H2 headers
phrased as questions; first paragraphs that answer directly;
specific named comparisons.

Traditional SEO keyword optimization ("best AI tool playback
cues") doesn't capture these query patterns. AEO requires
optimizing for natural language.

### 7. The AI-Citation Audit Loop

Recurring discipline: track which AI engines are citing your
content for which queries.

- **Manual probes** — periodically query target keywords on
  Google AI Overviews, Perplexity, ChatGPT Search, Claude;
  record what's cited.
- **Brand-mention monitoring** — track mentions of your brand
  in AI answers, even when not directly cited.
- **Gap identification** — queries you should appear for but
  don't; queries where competitors appear and you don't.
- **Iteration** — content updates based on what AI engines
  reward in your topical neighborhood.

The loop compounds: the more your content appears in AI answers,
the more the engines learn to surface your content, which produces
more appearances. The first inclusions are the hardest.

## Common Applications

**Cohort sales page AEO refit:**
The agent reviews the cohort sales page and audits AEO readiness.
Adds an FAQ section with schema markup answering the natural
questions (who is this cohort for, what's the structure, what's
the cost, what's the outcome). Adds Article schema with author
byline. Inserts specific claims with named alumni outcomes.
Result: page becomes more citable by AI engines.

**[your physical/SaaS product] feature page AEO:**
The product page is refactored: H2 phrased as user questions
("How does [your physical/SaaS product] handle latency verification?"), first
paragraph answers directly with specific behavior, comparison
table against competitors, Product schema added with
specifications and pricing.

**Pillar page for "AI tools for [your customer audience]":**
The pillar page is built as the canonical reference for the
topical neighborhood. Comprehensive, answer-shaped, citation-rich,
schema-marked. Designed to be the source AI engines cite when
users ask about the space.

**Brand-entity build for [your product]:**
The agent identifies the entity-recognition gaps: Wikipedia
mention (if eligible), Wikidata entry, About page completeness,
verified social profiles. Builds the entity graph that AI
engines can resolve.

**Quarterly AI-citation audit:**
The agent probes target queries on major AI engines, records
citations, identifies gaps. Output: a list of pages to optimize
for specific queries where competitors are appearing but
[your product]/[your physical/SaaS product]/[your product line] are not.

**Per locked memory: AI visibility / GEO work.** The
`searchfit-seo:ai-visibility` skill operationalizes brand
appearance audits across major AI engines.

## Anti-patterns (when this framework is misapplied)

**Optimizing only for SERP, ignoring AI surfaces.** Traditional
SEO without AEO misses the AI-answer attention pool. In 2026,
this is a measurable miss.

**Optimizing only for AEO, ignoring SERP.** Pages optimized
purely for AI extraction may score poorly on user-experience
signals when humans actually click through. The discipline
requires both.

**Fabricating credentials or citations.** AI engines penalize
fabricated sources over time, and the trust loss when caught is
severe. Citations and credentials must be verifiable.

**Per locked feedback: "Verify Project Status Before Speaking."**
AEO content must reflect current product state. Pages that
overstate cause AI engines to surface inaccurate answers, which
produces trust failures and ranking demotion.

**Per locked feedback: "Client Data Publication Rule."** AEO
content that includes client names or sensitive data violates
the publication rule. AI engines learn what you publish; once
published, the data is harder to retract.

**Per locked feedback: "Don't name living figures in methodology
body."** Citations and brand-entity content must avoid the
named-figure problem in agent output. Attribution lives in
attribution files; methodology content references methodologies,
not their originators.

**Treating schema as a check-the-box exercise.** Schema markup
that doesn't match actual page content (e.g., HowTo schema on a
narrative article) gets penalized when the engine cross-checks.
Schema must match content.

**Per locked memory: AI visibility / GEO baselines.** Before
AEO work, establish baseline AI visibility per
`searchfit-seo:ai-visibility`. Otherwise improvements can't be
measured.

**Conversational-query patterns ignored.** Writing in keyword
format when users query in natural language produces content
that doesn't match the question shape. AEO requires writing
for conversational queries.

## Cross-references

- Agent skill: `agents/seo-specialist/SKILL.md`
- Bench: `agents/seo-specialist/personality/_bench.md` (Intent-Match-Pole, Authority-Build-Pole)
- Frameworks index: `agents/seo-specialist/personality/frameworks_index.md`
- Companion methodology: `agents/seo-specialist/context/methodology/serp-ranking-fundamentals.md`
- Related skill: `searchfit-seo:ai-visibility`
- Related skill: `searchfit-seo:schema-markup`
- Related skill: `searchfit-seo:answer-engine-optimization`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `.claude/memory/feedback_no_lmg_clients_in_public_marketing.md`
