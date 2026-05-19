---
date: 2026-05-14
type: frameworks-index
agent: Copywriter
status: v2 (callable methodologies -- named by methodology, not by originator)
---

# Copywriter -- Frameworks Index (callable methodologies)

Each framework is a runnable operation the agent invokes. Originator credit lives in
[`frameworks_attribution.md`](frameworks_attribution.md) -- never invoked in output.

## Clarity-Pole methodologies

### `long_copy_default(brief)`

**Description:** Defaults to longer copy when the product is considered; short copy only when impulse.

**Rule:** Plain language defaults; verbs do the work.

### `research_before_writing(brief)`

**Description:** Audits whether the writer has 3+ specific customer-language artifacts before writing a word.

**Rule:** No copy without source.

### `verb_audit(draft)`

**Description:** Flags weak verbs, passive voice, abstract nouns; returns rewrites.

**Rule:** Strong verbs, concrete nouns.

---

## Wit-Pole methodologies

### `5_stages_of_awareness(reader)`

**Description:** Returns reader stage: unaware / problem-aware / solution-aware / product-aware / most-aware.

**Rule:** Headline must match stage.

### `5_stages_of_sophistication(market)`

**Description:** Returns market freshness; later-stage markets need bigger claims or new mechanisms.

**Rule:** Match the level of skepticism.

### `headline_stage_match(headline, reader_stage)`

**Description:** Audits whether the headline fits the reader's awareness stage; flags mismatches.

**Rule:** Mismatch = no engagement.

---

## Utility-Pole methodologies

### `starving_crowd_check(offer, market)`

**Description:** Does the market actually ache for this? If no, copy can't save it.

**Rule:** Demand precedes craft.

### `AIDA_lint(copy)`

**Description:** Attention / Interest / Desire / Action -- flags missing rungs.

**Rule:** Every rung earns its place.

### `headline_doctor(headline)`

**Description:** Returns 10 alternative headlines; force-tests specificity, curiosity, reader-state match.

**Rule:** First draft is rarely the headline.

---

## Cross-pole methodologies

### `big_idea_test(campaign)`

**Description:** Does the campaign have a Big Idea, or is it a collection of clever lines?

**Rule:** Big Idea is structural; clever lines are tactical.

### `personal_letter_voice_check(copy)`

**Description:** Does the copy read like one human writing to another, or like a brand broadcasting?

**Rule:** One human to one human.


---

## Invocation pattern

Modes in `../SKILL.md` invoke these frameworks by name. The framework name is the
contract -- what happens inside is the methodology. Output to the user names the
methodology, not the originator.

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Originator credit (academic): [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill (invocation): `../SKILL.md`
