# Reversibility on Send

## What This Framework Is

Reversibility on send is the discipline that treats every cold
outreach email send as an irreversible action requiring explicit
operator review before it fires. The framework holds that **sent
emails cannot be unsent** — Outlook recall is unreliable on
external addresses, and the cost of a misfired cold outreach
email (wrong recipient, wrong message, embarrassing typo, off-
brand tone, factually incorrect claim) is severe: relationship
damage, professional credibility hit, account permanently
poisoned.

The framework operates as a structural pattern, not a discretionary
warning. The pattern: every outreach output is a .eml file
written to disk, not a direct send. the operator reviews the file in
Outlook, confirms it, and triggers the send manually. The agent
never directly sends.

Three layers of the discipline:

1. **File-not-send output** — the canonical output is a .eml
   file with `X-Unsent: 1` header. Opens as unsent Outlook
   draft. Send is a separate, deliberate operator action.

2. **Pre-send checklist** — before sending, the operator reviews
   recipient, content, tone, brand voice, factual accuracy.
   The checklist is the gate; the file format enables it.

3. **Outreach tracker logging** — sent messages are logged to
   the outreach tracker with date, recipient, message summary.
   The log produces the audit trail.

The pattern exists because cold outreach is the
highest-stake-per-message work in the sales surface. A
proposal goes through multiple review cycles; a contract goes
through legal; a cold email goes from "draft" to "in the named
target's inbox" in one click. The discipline introduces
deliberate friction at exactly the moment friction is most
valuable.

## Why It Matters For This Agent

Sales Outreach's Reversibility-Send-Pole is the dedicated gate
that prevents irreversible sends from firing without explicit
operator authorization. The pole catches three specific failure
modes:

1. **Wrong-recipient sends** — outreach drafted for prospect A
   accidentally sends to prospect B. The .eml file pattern
   prevents this by surfacing recipient at the review stage,
   not at the send stage.

2. **Off-brand content** — message slips into AI-default
   warmth, generic marketing-ese, or forbidden vocabulary. The
   review stage catches and corrects.

3. **Factual errors** — message claims a specific named space,
   building, or executive that's actually wrong. The review
   stage cross-references against research before send.

For the operator's [your employer] cold outreach work specifically, the framework is
the structural backstop. Per locked feedback, every [your employer] outreach
.eml uses the X-Unsent header pattern; no direct sends from the
agent. The discipline is operational, not aspirational.

## Core Concepts

### 1. The .eml File Pattern

The canonical output is a .eml file written to disk:

```
From: the operator's email
To: named target's verified email
Subject: <specific subject line>
X-Unsent: 1
Content-Type: text/plain; charset=utf-8

<body text>

Cheers,
```

The `X-Unsent: 1` header tells Outlook this is a draft, not a
sent message. Opening the file in Outlook produces an editable
draft window. the operator reviews; edits if needed; sends from
Outlook.

The pattern is enforced by the outreach pipeline (per locked
`lmg-outreach-pipeline` skill). Every output across T1-T4
tiers uses this pattern. Direct-send mechanisms are explicitly
not used.

### 2. The Pre-Send Checklist

Before triggering the send, the operator runs a pre-send checklist:

- **Recipient correct** — named target's verified current email,
  not a generic role-based alias.
- **Subject line specific** — names the circumstance or the
  proposed outcome, not generic.
- **Body specific** — references named target, named
  circumstance, named outcome (per the specificity-over-volume
  framework).
- **Brand voice held** — no AI-default warmth, no forbidden
  vocabulary, no emojis, "Cheers," sign-off, no name.
- **Factual claims verified** — named space, named building,
  named executive correct (no inferred names; per locked feedback).
- **Reversibility considered** — would I be okay if this email
  surfaced publicly? Would I be okay if it went to the wrong
  person?

The checklist is the gate. .eml files that don't pass get
edited before send. .eml files that do pass get sent from
Outlook with a single deliberate action.

### 3. The Outreach Tracker

Every sent message is logged to the outreach tracker:

- **Date sent**.
- **Recipient** (name, role, organization, email).
- **Tier** (T1-T4).
- **Subject line**.
- **Message summary** (one-line of what was proposed).
- **Trigger event** (if applicable).
- **Follow-up scheduled** (if applicable).
- **Response received** (date, type, next step).

The tracker is the audit trail. It surfaces patterns: which
trigger events produce highest response rates, which subject
patterns work, which tiers are responsive. Per locked
prospecting work, the tracker compounds account knowledge.

### 4. The Recipient-Verification Layer

Before a .eml file is even written, recipient verification:

- **Email address recency** — [your prospecting tool] or similar tool confirms
  the email within 30-60 days. People change roles; emails go
  stale.
- **Current role confirmation** — the named target still holds
  the named role at the named organization.
- **Organization current state** — the organization hasn't
  been acquired, restructured, or had the named role
  eliminated.

Recipient verification is upstream of message drafting. Sending
to a stale email wastes the message and may produce bounces
that damage sender reputation.

### 5. The Voice-Match Gate

Per the brand voice spine, every outreach message holds the operator's
executive-buyer register:

- No AI-default warmth ("I hope this finds you well," "I'm
  thrilled to share...").
- No marketing-ese ("transformative experiences," "elevate
  your space," "next-generation").
- No bullet points in client emails.
- No emojis.
- "Cheers," sign-off — no name, no emojis, plain text only.
- Direct opening, no preamble.

Voice violations get caught at the review stage. The .eml file
pattern enables the catch — direct sends bypass it.

### 6. The Factual-Accuracy Gate

Per locked feedback ("Don't Infer Client Entity Names"),
messages use the exact names the customer uses for facilities,
spaces, executives. Inferred names produce errors that erode
trust.

The verification step:
- Named building / facility — confirmed in press, public
  records, or prior verified research.
- Named space / zone — confirmed from public information or
  prior conversations.
- Named executive — confirmed in current role at named
  organization.

Errors caught at review stage get corrected. Errors that ship
in a cold email are permanent — the prospect remembers the
generic-research signal and disengages.

### 7. The Follow-Up Protocol

Outreach is a sequence, not a single message. The protocol:

- **Initial outreach** — specific message per the framework.
- **Follow-up 1** (7-10 days, if no response) — different
  angle, different named outcome.
- **Follow-up 2** (14-21 days, if no response) — value-add
  approach (share something useful, not request).
- **Final touch** (30+ days, if no response) — explicit "okay
  to close the loop?" message.

Each follow-up gets its own .eml file with review gate. The
sequence isn't "automation" — it's deliberate touches with
specificity per touch.

## Common Applications

**Standard outreach pipeline run:**
The agent runs the locked outreach pipeline: [your prospecting tool] search,
contact enrichment, .eml generation across T1-T4 tiers, log to
outreach tracker. Output: multiple .eml files ready for review
in Outlook. the operator reviews, edits as needed, sends each from
Outlook.

**Pre-send catch on factual error:**
The .eml file lists "the 240-seat town hall" — but the operator
recognizes the actual space is 180-seat. Caught at review.
Edited before send. The .eml-file pattern made the catch
possible.

**Voice-match violation catch:**
The .eml file opens with "I wanted to reach out because I saw...".
Preamble violation per locked feedback. Edited at review to
direct opening. Voice-match pole operationalized.

**Wrong-recipient near-miss:**
Two prospects with similar names; the .eml file targets the
wrong one. Caught at review (the operator recognizes the recipient
doesn't match the message content). Corrected before send.

**Follow-up sequencing:**
Initial outreach to a Tier 1 target produces no response in 10
days. The agent generates a follow-up .eml with different
angle (named different space at the facility, different
proposed outcome). Reviewed and sent. Sequence continues per
protocol.

**Per locked feedback: "[your employer] outreach .eml NOT vault-sync material."**
The .eml files are excluded from Obsidian sync to prevent
accidental cross-device exposure. The outreach tracker (sent
messages log) is the canonical record.

## Anti-patterns (when this framework is misapplied)

**Direct send.** Agent bypasses the .eml file pattern and sends
directly. Violates the reversibility-send pole. Removes the operator's
review gate.

**Bulk send.** "Send to all 50 from this list." Loses the
per-message review discipline. Specificity drops; review
quality drops; failures compound.

**Per locked feedback: ".eml + X-Unsent."** Non-negotiable.
Direct sends violate the pattern.

**Per locked feedback: "Cheers," sign-off.** Generic
"Best regards" or "Sincerely" violate the voice-match pole.

**Per locked feedback: "no emojis, no bullet points in client
emails."** Executive-buyer register refuses these. The voice
spine catches violations.

**Recipient verification skipped.** Sending to a stale email
or unverified address. Bounces, undeliverable rate, sender
reputation degradation.

**Per locked feedback: "Don't Infer Client Entity Names."**
Inferred names in outreach produce trust failures. Verified
names demonstrate research.

**Per locked feedback: "Execute, Don't Preamble."** Outreach
opening with preamble (warmth, throat-clearing, generic context)
fails the first-second-test.

**Per locked feedback: "Avoid Text Wrapping at All Costs."**
Subject lines that wrap in standard email-list previews lose
the hook. Shorten.

**Send-and-forget.** Outreach sent without logging to the
tracker. Loses the audit trail. Pattern detection fails. Follow-up
discipline collapses.

**Volume-prioritized over specificity.** Sending high volume
because "more emails = more leads." The math doesn't work; the
trust damage compounds.

**Per locked feedback: "Match Execution Mode."** When client is
live and waiting, outreach can ship at 80% rather than 100%
polish. But the review gate doesn't get skipped — the polish
gets compressed, the review remains.

**Per locked feedback: "Brand to the customer's trade."**
Generic outreach loses to trade-specific outreach. The voice
spine plus customer-truth verification produce the
trade-specificity that wins.

## Cross-references

- Agent skill: `agents/sales-outreach/SKILL.md`
- Bench: `agents/sales-outreach/personality/_bench.md` (Reversibility-Send-Pole, Voice-Match-Pole)
- Frameworks index: `agents/sales-outreach/personality/frameworks_index.md`
- Vendored reference: `agents/sales-outreach/context/references/hubspot-academy.md`
- Vendored reference: `agents/sales-outreach/context/references/hubspot-academy-1.md`
- Companion methodology: `agents/sales-outreach/context/methodology/specificity-over-volume.md`
- Related skill: `anthropic-skills:lmg-outreach-pipeline`
- Related skill: `anthropic-skills:lmg-email-replies`
- Memory: `.claude/memory/feedback_workflow.md` (.eml + X-Unsent + Cheers sign-off)
- Memory: `.claude/memory/feedback_outreach_eml_not_synced.md`
- Memory: `.claude/memory/feedback_no_inferring_entities.md`
- Memory: `.claude/memory/feedback_execute_dont_preamble.md`
- Memory: `.claude/memory/feedback_no_text_wrap.md`
- Memory: `.claude/memory/feedback_brand_to_customer_trade.md`
- Memory: `.claude/memory/feedback_match_execution_mode.md`
- Voice spine: `.claude/voice-spine.md`
- Dept: `agents/sales-director/CLAUDE.md`
