---
date: 2026-05-14
type: frameworks-index
agent: Deep Researcher
status: v2 (callable methodologies -- named by methodology, not by originator)
---

# Deep Researcher -- Frameworks Index (callable methodologies)

Each framework is a runnable operation the agent invokes. Originator credit lives in
[`frameworks_attribution.md`](frameworks_attribution.md) -- never invoked in output.

## Rigor-Pole methodologies

### `evidence_hierarchy(claim)`

**Description:** Maps claim to evidence tier: primary research / meta-analysis / single study / mechanism / expert opinion / anecdote.

**Rule:** Tier the source, not the volume.

### `mechanism_check(claim)`

**Description:** Does the claim name a specific mechanism?

**Rule:** Phenomenology without mechanism = anecdote.

### `protocol_extraction(study)`

**Description:** Returns the operational protocol from the source.

**Rule:** No protocol = not actionable.

### `replication_status(claim)`

**Description:** Audits whether the claim has been replicated.

**Rule:** Single study = single hypothesis.

---

## Synthesis-Pole methodologies

### `time_log(question_history)`

**Description:** Tracks what the user spends research time on vs. what they say.

**Rule:** Stated vs. revealed research preference.

### `contribution_question(brief)`

**Description:** What is THIS research uniquely contributing?

**Rule:** 5-min-Google check.

### `mission_drift_check(scope)`

**Description:** Has the research scope drifted from the original question?

**Rule:** Drift compounds; catch early.

### `MBO_cascade(research_objective)`

**Description:** Cascades the research objective into measurable sub-objectives.

**Rule:** Sub-objectives = research milestones.

---

## Actionability-Pole methodologies

### `access_to_tools_audit(decision)`

**Description:** Does the decision-maker have what they need to act on this research?

**Rule:** Research without tools is academic.

### `pace_layering(decision)`

**Description:** Maps decision to time-horizon layer; calibrates depth-of-rigor.

**Rule:** Match rigor to pace.

### `long_now_horizon(research_question)`

**Description:** Audits whether the research question is fashion-layer (3 months) or infrastructure-layer (30 years).

**Rule:** Don't research fashion at infrastructure depth.

---

## Cross-pole methodologies

### `right_question_first(brief)`

**Description:** Before any research starts, locks the question.

**Rule:** Wrong question = wasted rigor.

### `decision_journal(research_session)`

**Description:** Captures the decision the research informed; tracks against outcomes.

**Rule:** Journal = retrospective leverage.


---

## Invocation pattern

Modes in `../SKILL.md` invoke these frameworks by name. The framework name is the
contract -- what happens inside is the methodology. Output to the user names the
methodology, not the originator.

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Originator credit (academic): [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill (invocation): `../SKILL.md`
