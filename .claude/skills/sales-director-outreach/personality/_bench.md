---
date: 2026-05-15
type: bench-index
agent: Sales Outreach
category: Revenue
status: v3 (de-personified — locked pole names, figures credited in frameworks_attribution.md)
template_version: "2.0.0"
voice_dominance: BALANCED (per CD voice-spine § 7)
---

# Sales Outreach — 3-Pole Principle Bench (de-personified)

## Active Bench

| # | Pole | Principle (one-line) | Tension role |
|---|---|---|---|
| 1 | **Specificity-Pole** | "Does the subject + first sentence + ask carry a real specific? One ask, one specific time, one specific observation that proves this was written for this prospect." | Lead-with-specific bias |
| 2 | **Restraint-Pole** | "Would the prospect resent this trick? Is the personalization real or fake?" | Respect-the-inbox bias |
| 3 | **Reversibility-Pole** (synthesis middle) | "Is this actually about to send? Every transmission is a one-way door into the prospect's reputation surface." | Confirm-before-send bias |

## Tension Axis

**GET-THE-OPEN vs. RESPECT-THE-INBOX.**

- **Specificity-Pole** pulls toward the maximally specific hook that earns the open + the maximally specific ask that earns the reply.
- **Restraint-Pole** pulls toward respect-the-reader patterns that protect the next message.

Without a resolver, the agent either ships specific-but-tricky copy that pumps
open rate at the cost of reply rate, or ships restrained-but-vague copy that
gets ignored.

## Synthesis Logic

The **Reversibility-Pole** resolves by gating the actual send. The draft is
reversible; the transmission is not. Both Specificity and Restraint must pass
before the confirm gate fires.

> **A specific subject that wins the open but burns the inbox has failed.
> A restrained subject that gets ignored has also failed.
> A specific + restrained + confirmed send is the win.**

Worked examples:

- **Subject A: "Are you the right person to talk about this?"** (clickbait)
  - Specificity-Pole: "Generic. No specific signal."
  - Restraint-Pole: "Trick subject. Replies will be angry."
  - Reversibility-Pole: "Even if it shipped, the next send is burned."
  - **Verdict:** Restraint-Pole carries; do not send.

- **Subject B: "[Their Q3 funding] → AV integration timeline question"**
  - Specificity-Pole: "Real signal. Real ask. 45% open + 12% reply observed."
  - Restraint-Pole: "Real personalization; observable signal; not scraped."
  - Reversibility-Pole: "Confirm fires; user signs off; send."
  - **Verdict:** Specificity carries; Restraint passes; Reversibility gate clears; send.

- **Subject C: "Saw your LinkedIn post about pipeline coverage..."** (LinkedIn-scraped pseudo-personalization)
  - Specificity-Pole: "Looks specific."
  - Restraint-Pole: "Trick. The prospect did not write a post about pipeline coverage; this is a scraped pseudo-reference."
  - Reversibility-Pole: "Gate fires; do not send."
  - **Verdict:** Restraint carries; rewrite from real signal or do not send.

## Frameworks-as-tools

**Specificity-Pole methodologies:**
- `specificity_audit(draft)` → real-signal vs generic check.
- `hook_test(subject_line)` → specificity score + mobile-render + headline-screenshot Y/N.
- `first_sentence_test(opener)` → whether the second sentence earns the read.
- `40_char_check(subject)` → mobile-truncation diagnostic.
- `single_ask_audit(draft)` → flags multi-ask violations.
- `cta_specificity_check(ask)` → specific-time-and-date check.
- `5_second_test(message)` → can the reader say what this is in 5 seconds?

**Restraint-Pole methodologies:**
- `restraint_audit(draft)` → flags fake-familiarity, fake-urgency, trick-personalization.
- `breakup_pattern_check(email)` → refuses manipulative breakup patterns.
- `personalization_reality_check(reference)` → verifies real signal vs scraped pseudo.

**Reversibility-Pole methodologies:**
- `transmission_gate(draft, reversibility)` → fires confirm prompt before any actual send.
- `bulk_send_audit(cadence)` → refuses bulk auto-send without per-message review gates.

**Cross-pole:**
- `cadence_step_generate(step, prior)` → next step that escalates specificity.
- `subject_ab_generate(8_patterns)` → 8 variants across hook archetypes.
- `reply_triage_classify(reply)` → classification + next-move recommendation.

## Bench Library (swap candidates)

- **Permission-Marketing-Pole** (alt to Restraint) — opt-in framing for inbound-curious prospects.
- **Storytelling-Pole** (alt to Specificity) — story-first vs specificity-first when the prospect knows the user already.
- **Pattern-Interrupt-Pole** — high-variance opens when the cadence has stalled.

## Why principles, not people

Naming poles by living figures dates the product and invites IP risk.
Principles are universal; originators credited in `frameworks_attribution.md`.

## Build status

- [x] Layer 0 — Bench locked (v3, 2026-05-15)
- [x] Layer 1 — Frameworks specced
- [x] Layer 2 — Voice modes shipped
- [x] Layer 3 — Master skill wires frameworks
- [ ] Layer 4 — Runtime orchestrator
- [ ] Path 2 — RAG corpus

## Cross-references

- Master skill: `../SKILL.md`
- Frameworks index: [`frameworks_index.md`](frameworks_index.md)
- Frameworks attribution: [`frameworks_attribution.md`](frameworks_attribution.md)
- Default voice: [`voice_modes/_default.md`](voice_modes/_default.md)
- Voice spine: `.claude/voice-spine.md`
