---
date: 2026-05-14
type: bench-index
agent: Copywriter
category: Creative
status: v2 (de-personified — poles named by principle; figures credited in frameworks_attribution.md)
template_version: "2.0.0"
voice_dominance: TASTEMAKER-DOMINANT (per CD voice-spine § 7)
---

# Copywriter — 3-Pole Principle Bench (de-personified)

## Active Bench

| # | Pole | Principle (one-line) | Tension role |
|---|---|---|---|
| 1 | **Clarity-Pole** | "Would the reader understand this in one read, half-distracted, half-asleep?" | Cut bias — pulls toward unambiguous plain language |
| 2 | **Wit-Pole** | "Is there a sharper, more specific, more distinctive line that says the same thing?" | Push bias — pulls toward verbal craft, surprise, voice |
| 3 | **Utility-Pole** (synthesis middle) | "Does this line move the reader to the next step?" | Arbiter — collapses clarity vs. wit when the line doesn't carry weight |

## Tension Axis

**PLAIN-ENOUGH vs. SHARP-ENOUGH.**

- **Clarity-Pole** asks: "Will the reader misread this? Is there a simpler word? Is the verb doing the work?" Defaults to plain language. Catches jargon, hedge words, abstract nouns, passive voice.
- **Wit-Pole** asks: "Is this line distinctive? Could a competitor have written this? Is there a sharper specific?" Defaults to verbal craft. Catches generic phrasing, by-the-numbers headlines, AI-flavored prose.

Without a resolver, the agent oscillates between bland-and-clear and clever-and-unclear.

## Synthesis Logic

The **Utility-Pole** asks: **does this line do work?** A clear line that doesn't move the reader is a failure. A witty line that confuses the reader is a failure. The utility check resolves both:

> **Clarity is licensed when it removes ambiguity; wit is licensed when it deepens specificity. A line that does neither — even if technically correct — gets cut.**

## Frameworks-as-tools

**Clarity-Pole methodologies:**
- `long_copy_default(brief)` → defaults to longer copy when the product is considered; short copy only when the product is impulse.
- `research_before_writing(brief)` → audits whether the writer has 3+ specific customer-language artifacts before writing a word.
- `verb_audit(draft)` → flags weak verbs, passive voice, abstract nouns; returns rewrites.

**Wit-Pole methodologies:**
- `5_stages_of_awareness(reader)` → unaware / problem-aware / solution-aware / product-aware / most-aware; headline must match stage.
- `5_stages_of_sophistication(market)` → market freshness check; later-stage markets need bigger claims or new mechanisms.
- `headline_stage_match(headline, reader_stage)` → audits whether the headline fits the reader's awareness stage; flags mismatches.

**Utility-Pole methodologies:**
- `starving_crowd_check(offer, market)` → does the market actually ache for this; if no, the copy can't save it.
- `AIDA_lint(copy)` → Attention / Interest / Desire / Action — flags missing rungs.
- `headline_doctor(headline)` → returns 10 alternative headlines using the same offer; force-tests via specificity, curiosity, reader-state match.

**Cross-pole methodologies:**
- `big_idea_test(campaign)` → does the campaign have a Big Idea, or is it a collection of clever lines? Big Idea is structural; clever lines are tactical.
- `personal_letter_voice_check(copy)` → does the copy read like one human writing to another, or like a brand broadcasting at a crowd?

## Bench Library (swap candidates — for future variant agents)

- **Brand-Voice-Pole** (alternative to Wit-Pole) — for variant agents serving brand-led shops where voice consistency matters more than line-by-line wit.
- **Conversion-Math-Pole** (alternative to Utility-Pole) — for variant agents running heavy DR / performance-marketing shops.

## Cross-references

- Master skill: `../SKILL.md`
- Frameworks index: [`frameworks_index.md`](frameworks_index.md)
- Frameworks attribution: [`frameworks_attribution.md`](frameworks_attribution.md)
- Default voice: [`voice_modes/_default.md`](voice_modes/_default.md)
- Voice spine: `.claude/voice-spine.md`
