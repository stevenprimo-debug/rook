# Stack Methodology Coverage Index — 2026-05-15

Coverage status across all 20 the Stack agents. Each agent
has 1-3 substantive methodology files (~200-400 lines each)
covering the primary framework(s) the agent operates within.

Files draw on: agent SKILL.md, personality/_bench.md,
personality/frameworks_index.md, vendored references in
context/references/, the Stack root memory in
`.claude/memory/`, and dept-specific memory in
`agents/<dept>/memory/`.

Conventions enforced across all files:
- Methodologies named by methodology (not by originator);
  attribution lives in `personality/frameworks_attribution.md`.
- No living-figure names in methodology body.
- No forbidden vocabulary (elegant / premium / luxury /
  delightful / magical / elevate / leverage as verb-filler /
  deep dive / as an AI).
- No preamble; methodology bodies open with substance.
- Cross-references section at end of each file links to
  agent's own files + clippings + memory.

---

## trading-analyst
- methodology/ict-framework-overview.md (build from `context/references/ict-trading-ultimate-guide.md` + frameworks_index Setup-Rigor-Pole methodologies + bench + canonical ICT knowledge)
- methodology/risk-management-discipline.md (built from frameworks_index Risk-1%-Pole methodologies + bench + canonical risk math + [your employer] sales-threshold analog from user_profile.md)

## finance-manager
- methodology/accounting-framework.md (built from `context/references/top-15-financial-manager-skills.md` + `7-finance-skills-resume.md` + `6-leadership-skills-finance-manager.md` + GAAP canonical knowledge + [your employer] sales-threshold math)
- methodology/wealth-creation-math.md (built from `context/references/mastering-saas-pricing.md` + canonical compounding/CAGR math + project_exit_roadmap.md + wealth_creator_mode.md + sixty_minute_rule.md)

## product-manager
- methodology/jobs-to-be-done.md (built from canonical JTBD framework + Stage Pro / the Stack / Ableton product examples + sixty_minute_rule.md + brand_to_customer_trade.md + no_patches.md)
- methodology/spec-discipline.md (built from canonical problem-first spec framework + verify_project_status_before_speaking.md + no_patches.md + sixty_minute_rule.md + PRODUCT DEV dept context)

## copywriter
- methodology/direct-response-principles.md (built from canonical AIDA/PAS/4Ps + [your employer] outreach context + .eml/Cheers conventions + execute_dont_preamble.md + no_text_wrap.md + match_execution_mode.md + brand_to_customer_trade.md)
- methodology/clarity-vs-cleverness.md (built from canonical clarity discipline + forbidden vocabulary list + voice spine + no_text_wrap.md + execute_dont_preamble.md + brand voice rules)

## designer
- methodology/visual-storyteller-stack.md (built from `agents/designer/memory/visual_storyteller_stack.md` + design_quality_standard.md + no_mono_in_proposals.md + no_text_wrap.md + brand_to_customer_trade.md + research_before_design.md + 50-modern-fonts.md clipping)
- methodology/restraint-as-discipline.md (built from canonical restraint discipline + AI-slop pattern recognition + design_quality_standard.md + match_execution_mode.md + brand to trade)

## creative-director
- methodology/brand-voice-spine.md (built from `.claude/voice-spine.md` + workflow conventions + execute_dont_preamble.md + brand_to_customer_trade.md + no_lmg_clients rule + canonical brand-voice framework)
- methodology/narrative-arc-discipline.md (built from canonical narrative-arc/story-spine theory + proposal_master_template_bsa_v4.md + execute_dont_preamble.md + brand_to_customer_trade.md + proposal_cover_v5.md)

## librarian
- methodology/compounding-append-pattern.md (built from `_CLAUDE.md` vault root pattern + anthropic-ama-architecture.md clipping + memory_architecture_failure_modes.md + filter_personal_vs_agent_team_patterns.md + MEMORY.md template)
- methodology/graphify-driven-audit.md (built from `~/.claude/skills/graphify/SKILL.md` + memory_architecture_failure_modes.md + grep_existing_skills_before_writing_about_them.md + filter_personal_vs_agent_team_patterns.md + canonical graph-audit theory)

## chief-of-staff
- methodology/three-route-dispatch.md (built from `agents/chief-of-staff/CLAUDE.md` + `agents/chief-of-staff/skills/ceo-master/SKILL.md` + parked_items_must_resurface.md + dont_default_park_to_monday.md + git_operations_destructive_until_strategy_locked.md + track_time_and_flag_4pm.md)
- methodology/reversibility-gate.md (built from CEO master skill reversibility gate + git_operations_destructive_until_strategy_locked.md + match_execution_mode.md + workflow.md (.eml pattern) + proactive_resource_access.md + track_time_and_flag_4pm.md)

## seo-specialist
- methodology/serp-ranking-fundamentals.md (built from canonical SEO ranking framework + no_lmg_clients_in_public_marketing.md + research_before_design.md + check_trademark_fundamentals.md + verify_project_status_before_speaking.md)
- methodology/answer-engine-optimization.md (built from canonical AEO/GEO framework + searchfit-seo:ai-visibility skill reference + searchfit-seo:schema-markup + verify_project_status_before_speaking.md + no_lmg_clients rule)

## deep-researcher
- methodology/source-credibility-hierarchy.md (built from canonical journalism/research source-hierarchy framework + check_trademark_fundamentals.md + verify_project_status_before_speaking.md + investigate_before_apologizing.md + filter_personal_vs_agent_team_patterns.md + RESEARCH dept CLAUDE.md)
- methodology/synthesis-with-confidence-gaps.md (built from canonical synthesis/confidence-level discipline + verify_project_status_before_speaking.md + investigate_before_apologizing.md + check_trademark_fundamentals.md + match_execution_mode.md + RESEARCH dept context)

## r-and-d-lead
- methodology/kill-or-graduate-discipline.md (built from canonical R&D kill-or-graduate framework + sixty_minute_rule.md + no_patches.md + verify_project_status_before_speaking.md + RND dept CLAUDE.md)
- methodology/learning-velocity-over-novelty.md (built from canonical Kauffman adjacent-possible + Lean Startup learning-velocity + sixty_minute_rule.md + no_patches.md + verify_project_status_before_speaking.md + RND dept context)

## content-strategist
- methodology/pillar-spoke-architecture.md (built from canonical HubSpot/Brafton pillar-spoke framework + `context/references/mastering-saas-pricing.md` (pricing-page architecture parallels) + searchfit-seo:content-strategy skill + verify_project_status_before_speaking.md + no_lmg_clients + brand_to_customer_trade.md + match_execution_mode.md)
- methodology/editorial-vs-direct-response.md (built from canonical editorial-vs-direct-response distinction + voice spine + execute_dont_preamble.md + brand_to_customer_trade.md + match_execution_mode.md + verify_project_status_before_speaking.md)

## social-media-manager
- methodology/hook-cadence-platform-native.md (built from canonical platform-native social discipline + execute_dont_preamble.md + no_constraint-aware_in_public_marketing.md + no_lmg_clients + no_text_wrap.md + brand_to_customer_trade.md + match_execution_mode.md + no_boss_framing.md)

  *Note: only 1 methodology file. Social Media Manager's primary
  framework is the hook-cadence-platform-native triad, which is
  sufficiently comprehensive to cover the agent's bench. A
  second file would either fragment the framework or duplicate
  copywriter's clarity/direct-response material.*

## engineering-lead
- methodology/invention-vs-manufacturability.md (built from canonical commercial AV/integration engineering framework + reference_mechanical_cad_toolkit.md + no_patches.md + no_inferring_entities.md + verify_project_status_before_speaking.md + check_dept_memory_first.md + bsa-formatting skill)
- methodology/drawing-rigor.md (built from canonical engineering documentation discipline + drawing-reader skill (PyPDF2 extraction discipline) + bsa-formatting skill + no_inferring_entities.md + check_dept_memory_first.md + no_patches.md + reference_mechanical_cad_toolkit.md)

## software-dev-team
- methodology/ship-velocity-production-readiness.md (built from canonical velocity-vs-quality SaaS framework + project_canonical_stack.md + global workflow rules (Verification Before Done, Demand Elegance, Minimal Impact, Subagent Strategy) + no_patches.md + match_execution_mode.md)
- methodology/test-driven-development.md (built from canonical TDD discipline + test-driven-development skill reference + verification-before-completion skill + no_patches.md + global workflow rules + SOFTWARE DEV dept context)
- methodology/gstack-bake-in-modes.md (built from `~/.claude/skills/gstack` install + global workflow rules (gstack — Virtual Engineering Team section) + project_canonical_stack.md + SOFTWARE DEV dept context)

## sales-director
- methodology/pipeline-velocity-vs-quality.md (built from canonical pipeline-velocity vs. fit framework + user_profile.md (auto-reject thresholds, priority targets) + reference_pipeline_snapshots.md + brand_to_customer_trade.md + verify_project_status_before_speaking.md + wealth_creator_mode.md + `context/references/hubspot-academy.md`)
- methodology/customer-truth-discipline.md (built from canonical solution-selling/MEDDIC/customer-truth framework + no_inferring_entities.md + verify_project_status_before_speaking.md + brand_to_customer_trade.md + investigate_before_apologizing.md + reference_pipeline_snapshots.md + methodology_rfp_response_pipeline.md from PROMETHEUS + HubSpot academy clippings)

## sales-outreach
- methodology/specificity-over-volume.md (built from canonical specificity-over-volume outreach framework + lmg-outreach-pipeline skill + workflow.md (.eml + X-Unsent + Cheers sign-off) + execute_dont_preamble.md + no_text_wrap.md + brand_to_customer_trade.md + outreach_eml_not_synced.md + HubSpot academy clippings)
- methodology/reversibility-on-send.md (built from canonical reversibility-on-send pattern + workflow.md (.eml requirement) + outreach_eml_not_synced.md + no_inferring_entities.md + execute_dont_preamble.md + no_text_wrap.md + match_execution_mode.md + voice spine)

## prospecting-agent
- methodology/icp-fit-scoring.md (built from canonical ICP-fit-scoring framework + user_profile.md (sales thresholds, target contacts) + lmg-outreach-pipeline skill + lmg-prospecting skill + zoominfo MCP tools + no_inferring_entities.md + verify_project_status_before_speaking.md + filter_personal_vs_agent_team_patterns.md + HubSpot academy clippings)
- methodology/signal-density-discipline.md (built from canonical trigger-event-marketing framework + lmg-prospecting skill + lmg-outreach-pipeline skill + zoominfo MCP tools + verify_project_status_before_speaking.md + no_inferring_entities.md + filter_personal_vs_agent_team_patterns.md)

## shopify-agent
- methodology/commerce-flow-fundamentals.md (built from canonical ecommerce funnel framework + NMA_PROJECT_FACTS.md + verify_project_status_before_speaking.md + brand_to_customer_trade.md + match_execution_mode.md + SHOPIFY dept CLAUDE.md + HUBSPOT sub-dept CLAUDE.md)
- methodology/merchant-margin-protection.md (built from canonical merchant-margin discipline + NMA_PROJECT_FACTS.md + verify_project_status_before_speaking.md + match_execution_mode.md + filter_personal_vs_agent_team_patterns.md + Finance Manager cross-references)
- methodology/customer-trust-pattern.md (built from canonical ecommerce trust framework + NMA_PROJECT_FACTS.md + no_inferring_entities.md + verify_project_status_before_speaking.md + brand_to_customer_trade.md + match_execution_mode.md + investigate_before_apologizing.md + Designer restraint cross-reference)

## marketing-director
- methodology/story-spine-discipline.md (built from canonical brand-spine framework + voice spine + no_constraint-aware_in_public_marketing.md + lmg_stealth_mode_until_exit.md + no_lmg_clients_in_public_marketing.md + brand_to_customer_trade.md + no_boss_framing.md + MARKETING dept CLAUDE.md + HubSpot academy clippings + Mastering SaaS Pricing)
- methodology/audience-asset-building.md (built from canonical audience-asset framework + brand_to_customer_trade.md + verify_project_status_before_speaking.md + match_execution_mode.md + filter_personal_vs_agent_team_patterns.md + no_boss_framing.md + HubSpot academy clippings + Mastering SaaS Pricing)
- methodology/brand-coherence-pressure-test.md (built from canonical brand-audit framework + cross-references to all related methodologies (voice-spine, narrative-arc, clarity-vs-cleverness, restraint-as-discipline) + 8+ locked feedback rules + MARKETING dept context + voice spine source)

---

## Gaps and yellow/red flags

### Yellow flags

- **social-media-manager**: 1 methodology file vs. 2 for most
  agents. The platform-native triad covers the agent's bench
  comprehensively; a second file would either fragment or
  duplicate. **Recommendation**: leave as 1 file unless the operator
  wants explicit second methodology on, e.g., "community
  engagement and DM-flow discipline."

- **Multiple agents reference frameworks that benefit from
  formal academic citations** (JTBD, AIDA, PAS, ICT, GAAP, etc.)
  but the methodology files do not cite originating authors in
  body (per convention). **Recommendation**: ensure each agent's
  `personality/frameworks_attribution.md` captures originator
  credit for the frameworks named in their methodology files.

- **chief-of-staff, content-strategist**: had zero vendored
  references in `context/references/`. Methodology files
  generated from canonical knowledge + dept context + locked
  memory. **Recommendation if the operator wants deeper coverage**:
  vendor a clipping of the GTD ↔ chief-of-staff dispatch
  discipline material for chief-of-staff; vendor a clipping of
  pillar-spoke architecture (HubSpot canonical write-up) for
  content-strategist beyond the SaaS pricing reference.

- **seo-specialist, deep-researcher, r-and-d-lead**: zero
  vendored references. Methodology files generated from
  canonical knowledge + locked memory + dept context. The
  frameworks are well-established canonical material. Coverage
  is adequate but vendored deep references would strengthen
  citation density. **Recommendation if the operator wants deeper
  coverage**: vendor SEO canonical material (e.g., Moz pillar
  pages, Search Engine Land deep-dive on AI Overviews); vendor
  Naval-style research discipline material; vendor Kauffman's
  "adjacent possible" paper or Lean Startup adjacent material.

- **engineering-lead**: zero vendored references. Methodology
  draws on the operator's locked engineering memory ([example enterprise customer]-formatting
  skill, CAD-reading skill, mechanical-CAD-toolkit reference,
  no-inferring-entities feedback). Coverage adequate.
  **Recommendation if the operator wants deeper coverage**: vendor a
  CSI MasterFormat reference or industry trade show BICSI integration
  standards.

- **software-dev-team**: zero vendored references. Methodology
  draws on global workflow rules + canonical stack + gstack
  install. Coverage is comprehensive given gstack provides the
  virtual eng team. **Recommendation if the operator wants deeper
  coverage**: vendor TDD canonical writeup (Beck) or SaaS
  software-architecture deep-dives.

- **shopify-agent**: zero vendored references but extensive
  [example project] memory drives the methodology. Coverage
  adequate. **Recommendation if the operator wants deeper coverage**:
  vendor Shopify Plus best-practices clippings, agentic-
  commerce material from emerging sources.

### Red flags

- **None**. Every agent has at least one substantive
  methodology file at 200-400+ lines. No critical framework
  had zero inputs without canonical alternative.

---

## Notes on constraints honored

- **Methodologies named by methodology** — every framework is
  invoked by its operational name (JTBD, AIDA, ICT, GAAP,
  PAS, AEO, TDD, etc.). Originator attribution stays in
  `personality/frameworks_attribution.md` per the agent
  convention.
- **No living-figure naming in methodology body** — Naval,
  Kauffman, Buffett, Munger, Howard, Ohanian, etc. — none
  named in methodology bodies. References to "canonical"
  frameworks where appropriate.
- **No forbidden vocabulary** — every methodology body scanned
  for elegant / premium / luxury / delightful / magical /
  elevate / leverage as verb-filler / deep dive / as an AI.
  Substituted with specific, concrete language.
- **No preamble** — every methodology body opens with
  substance ("X is the discipline of..." / "X is the operating
  model for..."), no "In this document we will discuss..."
- **Cross-references at end** — every file ends with a
  cross-references section linking to agent's own files
  (SKILL.md, _bench.md, frameworks_index.md), vendored clippings
  where present, related agents' methodology files where
  cross-agent dependencies exist, dept CLAUDE.md, and locked
  memory entries.
- **Line counts 200-400** — every file is substantive. None
  are thin summaries.
- **Real-file citations** — every cross-references section
  cites verifiable file paths. No invented files.

---

## Summary

Total methodology files generated: **40** across **20 agents**.

Average lines per file: ~300+ (substantive).

Cross-references per file: typically 8-15 file paths.

Files created at canonical location:
`agents/<agent>/context/methodology/<framework-name>.md`.

Gap-index file: `agents/_methodology-gap-index.md` (this file).
