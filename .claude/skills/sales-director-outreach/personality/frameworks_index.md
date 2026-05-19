---
date: 2026-05-14
type: frameworks-index
agent: Sales Outreach
status: v2 (callable methodologies indexed by methodology name)
template_version: "2.0.0"
---

# Sales Outreach — Frameworks Index

Methodologies indexed by name, not by person. Originators in
[`frameworks_attribution.md`](frameworks_attribution.md).

---

## hook_test(subject_line)

**Signature:** `hook_test(subject: string) → {specificity_score: 0-10, mobile_render: PASS|FAIL, headline_screenshot: Y|N, recommended_rewrite: string | null}`

**Pole:** Hook-Pole.

**Returns:** scored verdict on whether the subject earns the open.

**When invoked:** every `cold-draft` Pass 1; every `subject-ab` evaluation.

**Failure mode caught:** Generic subjects ("Quick question") that get filtered, deleted, or ignored.

**Scoring rubric:**
- Specificity: named entity, specific number, specific event = +3 each.
- Generic words ("quick," "touching base," "checking in") = -2 each.
- Under 40 chars = +2 (mobile-render bonus).
- Headline-screenshot test: would the prospect screenshot and share? +5 if yes.

---

## clarity_check(message)

**Signature:** `clarity_check(message: string) → {five_second_test: PASS|FAIL, cta_count: int, context_sentence_count: int, single_ask_verdict: PASS|FAIL}`

**Pole:** Clarity-Pole.

**Returns:** structural verdict on message readability.

**When invoked:** every `cold-draft` Pass 2.

**Failure mode caught:** Multi-CTA messages (3 asks is 0 asks), paragraph-of-context-before-the-ask drafts.

**Rules:**
- Single CTA mandatory. Multi-CTA = FAIL.
- Context sentences ≤ 3.
- 5-second test: read the message in 5 seconds. Can you say what it is and what to do? PASS only if yes.

---

## restraint_audit(draft)

**Signature:** `restraint_audit(draft: string) → {fake_familiarity: bool, fake_urgency: bool, trick_personalization: bool, breakup_manipulation: bool, fixes: string[]}`

**Pole:** Restraint-Pole.

**Returns:** structured trick-audit verdict.

**When invoked:** every `cold-draft` Pass 3, every `sequence` step, every `breakup` mode.

**Failure mode caught:** Tricks the prospect would resent after the read.

**Patterns rejected:**
- "Hope you're well!" (fake-familiarity)
- "Circling back," "bumping this up," "wanted to flag" (fake-urgency)
- "Noticed you posted about X on LinkedIn" without real engagement (trick-personalization)
- "Should I close your file?" (breakup-manipulation)
- "Per my last email" (passive-aggressive)
- "Per our conversation" when no conversation occurred (false-shared-context)

---

## subject_ab_generate(prospect, offer)

**Signature:** `subject_ab_generate(prospect, offer) → {variants: [{pattern: string, subject: string, hook_score: int}]}`

**Pole:** Hook-Pole (with Restraint check).

**Returns:** 8 subject-line variants across hook archetypes.

**Archetypes:**
1. Specific-number ("[42] in 30 days")
2. Named-person ("[Their CEO] mentioned [X]")
3. Observation ("[Observable specific signal] — quick question")
4. Question (real, not clickbait — "When does [their thing] hit [their constraint]?")
5. Contrarian-claim ("[Conventional wisdom] is wrong for [vertical]")
6. Shared-context ("[Real shared thing] — [specific ask]")
7. Vulnerability ("I'm probably wrong about this, but...")
8. No-trick (literal: "[Specific topic] — [specific ask]")

**When invoked:** `subject-ab` mode.

**Failure mode caught:** Single-pattern over-reliance. Lists exhaust pattern velocity if the same archetype is used repeatedly.

---

## reply_triage_classify(reply)

**Signature:** `reply_triage_classify(reply: string) → {classification: enum, recommended_move: string, draft: string | null}`

**Pole:** Cross-pole synthesis.

**Returns:** classified reply + recommended next move + optional inline draft.

**Classifications:**
- `interested` — buyer signal; draft the meeting-book reply.
- `not-now` — soft-no; draft 90-day follow-up trigger.
- `wrong-person` — referral candidate; draft polite re-routing ask.
- `unsubscribe-style` — remove; draft confirmation.
- `aggressive-pushback` — no-move; let it sit, do not escalate.
- `silent-bounce` — auto-responder or address-deliverability failure; flag for prospecting-agent.

**When invoked:** `reply-triage` mode.

**Failure mode caught:** Escalating on aggressive-pushback (which always backfires) or under-responding to interested (which loses warm leads).

---

## cadence_step_generate(step, prior_steps)

**Signature:** `cadence_step_generate(step: int, prior: step[]) → {channel: string, timing: string, subject: string, hook: string, ask: string}`

**Pole:** Cross-pole.

**Returns:** next cadence step that escalates from prior steps.

**Cadence design rules:**
- Step 1: Hook + ask, full message.
- Step 2 (D+3): Bump with new specific observation.
- Step 3 (D+7): Channel switch (LinkedIn DM or voicemail).
- Step 4 (D+14): Value-add (relevant resource, not a pitch).
- Step 5 (D+21): Different angle (different decision-maker pain).
- Step 6 (D+30): Breakup — Restraint-Pole gates against manipulation.

**When invoked:** `sequence` mode primary.

---

## first_sentence_test(opener)

**Signature:** `first_sentence_test(opener: string) → {earns_second: bool, generic_score: int, specificity_pulled_forward: bool}`

**Pole:** Hook-Pole.

**Returns:** whether the second sentence will be read.

**Rules:**
- Generic opener ("I came across your company...") = FAIL.
- Self-introduction ("My name is...") = FAIL (the reader knows; signature shows).
- Specific observation = PASS.
- Question that requires their answer = PASS.

---

## breakup_pattern_check(breakup_email)

**Signature:** `breakup_pattern_check(email: string) → {manipulative: bool, manipulative_patterns_found: string[], acceptable_rewrite: string}`

**Pole:** Restraint-Pole.

**Returns:** flags manipulative breakup patterns + offers respectful rewrite.

**Rejected patterns:**
- "Should I close your file?" (manufactured-urgency manipulation)
- "I'll assume this isn't a priority" (passive-aggressive)
- "I'll be moving on" (martyrdom)
- "Last call" (fake-scarcity)

**Acceptable pattern:**
- Brief acknowledgment + door-left-open + no demand. "I'll stop bumping this for now. If [specific signal] changes, feel free to ping me."

---

## Cross-references

- Bench: [`_bench.md`](_bench.md)
- Attribution: [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill: `../SKILL.md`
