# Source Credibility Hierarchy

## What This Framework Is

Source credibility hierarchy is the discipline of ranking sources
by trustworthiness and using the rank to weight the conclusions
drawn from them. The framework holds that **all sources are not
equal**, and that research outputs that treat them as equal —
weighting a Reddit comment the same as a peer-reviewed study, a
vendor's marketing page the same as a regulatory filing — produce
conclusions that fail when stakes rise.

The hierarchy is a working tool, not a rigid rulebook. Lower-tier
sources can be useful (a Reddit thread may surface a real
practitioner's experience faster than a white paper); they are
just weighted differently when the conclusions are drawn. The
discipline requires the researcher to be explicit about the
weight: a strong conclusion needs strong-tier evidence; weaker-tier
evidence supports working hypotheses, not locked conclusions.

The framework has six tiers, top to bottom:

1. **Primary sources with verification** — court filings,
   regulatory filings (SEC, FDA, FTC), patent applications,
   official government data, raw datasets, signed contracts,
   verified financial statements.

2. **Peer-reviewed research and authoritative reference works** —
   academic journals (with citation count signals), specialty
   encyclopedias, standards bodies (IEEE, ISO, W3C).

3. **Established journalism and industry analysis** — major
   newspapers and magazines with fact-checking discipline, named
   industry analysts at established firms, industry-specific
   trade publications.

4. **Specialist secondary sources** — vendor documentation,
   industry consortium reports, professional association
   guidelines, named-expert blog posts with verifiable expertise.

5. **General secondary sources** — Wikipedia (good starting
   point, weak ending point), general-interest publications,
   independent blogs without verifiable expertise.

6. **User-generated and unverified sources** — Reddit, forum
   posts, social media, anonymous user reviews, AI-generated
   summaries without source citations.

Each tier has appropriate uses; each tier has appropriate
weights when conclusions are drawn.

## Why It Matters For This Agent

Deep-Researcher's bench gates on three principles: Source-Quality-Pole,
Synthesis-Honesty-Pole, and Confidence-Gap-Pole. The source
credibility hierarchy is the operating implementation of the
first pole and feeds the other two.

- **Source-Quality-Pole** asks: "Is the evidence for this
  conclusion appropriate to the conclusion's weight?" The
  hierarchy answers: tier matters.

- **Synthesis-Honesty-Pole** asks: "Am I being honest about how
  much of this synthesis rests on weak sources?" The hierarchy
  answers: tier-aware synthesis shows the operator where the
  weak links are.

- **Confidence-Gap-Pole** asks: "Where are the unknowns, and
  what tier of evidence would close them?" The hierarchy answers
  by naming what tier of source would resolve the gap.

For the operator's research surfaces — competitive intelligence on
[your product] and [your physical/SaaS product] categories, pre-meeting client briefs,
trademark and name research, market trend analysis — source
credibility discipline prevents the failure mode of confident
conclusions drawn from unreliable sources. When [your employer] outreach
references an industry trend, the researcher knows what tier
supports the claim.

## Core Concepts

### 1. Primary Sources with Verification (Tier 1)

Primary sources are the raw record: court filings, regulatory
filings, patents, government data, original datasets, contracts,
verified statements. They are not interpretations of evidence —
they are the evidence.

Verification means the source can be independently confirmed.
A court filing on PACER is primary and verifiable. A "leaked
contract" passed around social media is primary but unverified
— it might be real, fabricated, or modified.

Uses:
- Strongest claims rest on Tier 1.
- Legal, financial, and regulatory questions require Tier 1.
- Verifying claims made by lower-tier sources.

Limitations:
- Tier 1 sources are often dense, technical, and require domain
  expertise to interpret correctly.
- Access can be paywalled or restricted.
- Time-lagged (filings reflect past states, not current ones).

### 2. Peer-Reviewed Research (Tier 2)

Peer-reviewed academic research is the gold standard for
factual claims about how things work — mechanisms, causation,
data analysis. Quality signals:

- **Citation count** — highly-cited papers have stood up to
  scrutiny.
- **Journal reputation** — high-impact journals have stricter
  review.
- **Author affiliation** — established institutions, named
  researchers with track records.
- **Recency** — for fast-moving fields, recent papers matter
  more.

Limitations:
- Replication crisis means even peer-reviewed claims can fail
  to replicate.
- Industry-funded research carries conflicts of interest.
- Fields with weaker methodological standards produce weaker
  consensus.

Reference works (specialty encyclopedias, standards documents)
sit alongside peer-reviewed research as Tier 2.

### 3. Established Journalism and Industry Analysis (Tier 3)

Major newspapers, magazines with fact-checking departments, named
industry analysts at established firms (Gartner, Forrester,
McKinsey research reports), and respected trade publications.

Quality signals:
- **Named author** with verifiable byline history.
- **Fact-checking process** — most major outlets have
  institutional fact-checking.
- **Correction history** — outlets that correct errors openly
  are more trustworthy than those that don't.
- **Editorial independence** from sources.

Uses:
- Synthesis of complex topics for non-specialist audiences.
- Industry analysis with named analyst track records.
- Current-events reporting from professional newsrooms.

Limitations:
- Even strong outlets have biases (political, commercial).
- Industry analysts have commercial relationships with vendors.
- Trade press can be captured by vendor sponsorship.

### 4. Specialist Secondary Sources (Tier 4)

Vendor documentation, professional association guidelines, named-
expert blog posts, conference talks with publicly available
slides, industry consortium reports.

Vendor documentation is the canonical source for how vendor
products work — but vendors also have commercial interest in
presenting their products favorably. Use vendor docs for "how
does this work" questions; cross-reference for "is this good"
questions.

Named-expert blog posts vary widely. Practitioners with deep
expertise often share knowledge informally that doesn't appear
elsewhere. The credibility test: is the expertise verifiable
(track record, public work, peer recognition)?

Uses:
- Implementation questions (how-to).
- Practitioner-perspective questions (what works in practice).
- Cross-referencing higher-tier sources.

### 5. General Secondary Sources (Tier 5)

Wikipedia, general-interest publications, independent blogs
without verifiable expertise.

Wikipedia is a starting point — its citation discipline lets the
researcher jump to higher-tier sources. Wikipedia itself should
not be the citation in research output; follow Wikipedia's
sources to find the citation.

General-interest publications and unverified blogs may surface
useful framings or initial pointers but should not anchor
conclusions.

### 6. User-Generated and Unverified Sources (Tier 6)

Reddit, forums, social media, anonymous reviews, AI-generated
summaries without citations.

Lowest credibility but sometimes highest signal-on-novel-topics:
practitioners discuss real problems before they appear in
higher-tier sources. The researcher treats Tier 6 sources as
**lead generators** — surfaces that point at questions worth
asking — not as conclusion sources.

Concrete example: a [your customer persona]'s Reddit thread about
[your software category] issues is valuable as a lead (this is a real
problem, here are the specifics they encountered) but cannot
anchor a research claim about market opportunity. The lead points
at where to look in higher tiers (industry surveys, vendor
reports, named-expert analysis).

### 7. The Triangulation Discipline

Strong conclusions require triangulation — the same claim
verified by multiple independent sources, ideally at multiple
tiers. The discipline:

- Three independent Tier 4+ sources agree on the claim → solid
  basis for strong conclusion.
- One Tier 1 or Tier 2 source + corroboration from Tier 3-4 →
  strong basis.
- Single source at any tier → working hypothesis, not locked
  conclusion.
- Tier 6 sources only → flag-worthy lead, requires upgrade
  before conclusion.

Independence matters: three articles all citing the same
original source are not three independent sources. Triangulation
requires distinct origin chains.

## Common Applications

**Pre-meeting client research:**
The agent researches the client's recent corporate activity. Tier 1
(SEC filings) reveals financial trajectory and capital allocation
priorities. Tier 3 (industry trade press) reveals recent news and
strategic narrative. Tier 4 (vendor case studies, named-analyst
reports) reveals competitor relationships. Tier 6 (employee
Glassdoor reviews) surfaces cultural signals that may inform
positioning. Synthesis: tier-weighted, with the strongest claims
anchored in Tier 1.

**Trademark and name research:**
Per locked feedback ("Check Trademark Fundamentals Before Flagging
Name Collisions"), the agent prioritizes Tier 1 (USPTO trademark
database) and Tier 3 (specialized trademark databases) over Tier 6
(forum posts speculating on name conflicts). The real-watchout
distinction (SEO vs. legal collision) is grounded in tier-appropriate
sources.

**Competitive intelligence on AI-tooling categories:**
The agent surveys the category landscape. Tier 4 (vendor docs,
product pages) reveals capability claims. Tier 3 (named-analyst
reports, established trade press) reveals market positioning.
Tier 6 (Reddit, Discord, X) reveals practitioner experiences.
Conclusion synthesis weights tiers explicitly.

**Market-trend research for Stack cohort positioning:**
The agent investigates the [your customer market] shift narrative.
Tier 2 (academic labor-economics research on creative-industry
shifts), Tier 3 (industry trade press on tour-economy changes),
Tier 4 (named-expert blog posts from [your customer audience]),
Tier 6 (community-forum discussions). Conclusions about the size
and timing of the shift rest on the higher tiers; specifics about
practitioner experiences are surfaced from lower tiers.

**Fact-check on a vendor claim:**
A vendor's marketing page (Tier 4) claims "industry-leading
performance." The agent checks Tier 2-3 sources for independent
benchmark data. If the claim is corroborated by independent
sources, it earns the citation. If not, the claim is flagged as
vendor self-report.

**Pre-publication review on [your product] content:**
Before publishing a piece that makes claims about the AI tooling
landscape, the agent runs the source audit. Claims with Tier 4+
backing pass; claims with only Tier 6 backing get downgraded to
"observation" framing or pulled.

## Anti-patterns (when this framework is misapplied)

**Tier collapse — treating all sources equally.** The most common
failure mode. A research output that weights a Reddit post the
same as a peer-reviewed study produces confident-sounding
conclusions on weak foundations.

**Single-source conclusions.** Drawing a conclusion from one
source at any tier. Even Tier 1 sources can be wrong, incomplete,
or context-dependent. Triangulation is the discipline.

**Vendor-marketing as Tier 2.** Treating vendor product pages or
sponsored research as if they were peer-reviewed. Vendor
documentation is Tier 4 (good for implementation questions),
not Tier 2 (not appropriate for "is this good" conclusions).

**Wikipedia as the citation.** Wikipedia is a finder; the citation
is the source Wikipedia points to. Research output that cites
Wikipedia surfaces unverified second-hand knowledge.

**Per locked feedback: "Verify Project Status Before Speaking."**
Applied to research: verify the current state of the named
entity before drawing conclusions. Stale sources produce stale
conclusions.

**Per locked feedback: "Check Trademark Fundamentals Before
Flagging Name Collisions."** The framework anchors this: trademark
questions go to Tier 1 (USPTO database), not Tier 6 (forum
speculation).

**Per locked feedback: "Investigate Before Apologizing for
Perceived Bugs."** Applied to research: investigate the actual
source claim before concluding the source is wrong; the source
may be right and the researcher's reading wrong.

**AI-summary as primary source.** AI-generated summaries (AI
Overviews, ChatGPT outputs) are Tier 6 — they aggregate
unspecified sources and may hallucinate. Use them as lead
generators only; the citation must be an underlying source.

**Per locked feedback: "Filter — Personal-Tool Patterns vs
Agent-Team Patterns."** Research outputs that will be read by
multiple agents need tier-explicit weighting. Single-user
research can be looser; team research compounds errors when
tiers are not visible.

**Recency bias.** Treating the most recent source as the most
credible. Newer sources are sometimes more accurate (for
fast-moving topics) and sometimes less (rushed publication,
weak fact-checking). Recency is a signal, not a substitute
for tier evaluation.

## Cross-references

- Agent skill: `agents/deep-researcher/SKILL.md`
- Bench: `agents/deep-researcher/personality/_bench.md` (Source-Quality-Pole)
- Frameworks index: `agents/deep-researcher/personality/frameworks_index.md`
- Companion methodology: `agents/deep-researcher/context/methodology/synthesis-with-confidence-gaps.md`
- Memory: `.claude/memory/feedback_check_trademark_fundamentals.md`
- Memory: `.claude/memory/feedback_verify_project_status_before_speaking.md`
- Memory: `.claude/memory/feedback_investigate_before_apologizing.md`
- Memory: `.claude/memory/feedback_filter_personal_vs_agent_team_patterns.md`
- Memory: `agents/deep-researcher/CLAUDE.md`
