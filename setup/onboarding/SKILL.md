---
name: onboarding — ROOK Setup Interview
description: One-time interactive interview run at install time. Asks the customer ~18 questions across 6 areas (identity, schedule, business context, goals, ADHD/focus preferences, voice). Generates 6 personalization files that turn a fresh ROOK install into THEIR ROOK install. Trigger on first install OR when the customer says "redo onboarding" / "reset my personalization" / "onboard me again." Lives in setup/ because it runs once, not on a session-by-session basis like the 20 agents.
type: setup-skill
status: spec — implementation pending
version: "1.0.0-draft"
captured: 2026-05-18
---

# Onboarding — ROOK Setup Interview

> Runs once at install. Turns a fresh ROOK clone into the customer's ROOK.

## Why this exists

A fresh `git clone` of ROOK ships with 20 generic agents. They work, but they don't know the customer. The onboarding skill is the bridge between generic install and personalized operating system: a 15-minute interview that captures who the customer is and writes 6 files that make every subsequent session aware of them.

The interview is the **personalization layer**. Per Perplexity's framing earlier this build cycle: most agent products give you one configuration. ROOK gives you twenty agents × N voice modes × the customer's actual schedule, family, goals, and working style. The interview is what turns that surface area into something that fits.

## When this fires

| Trigger | Source |
|---|---|
| First-time install | `hooks/INSTALL.{ps1,sh}` calls this skill at the end of the install routine |
| Customer request | "redo onboarding" / "reset my personalization" / "onboard me again" / "update my profile" |
| Annual refresh | Optional reminder: if `CLAUDE.md` was last updated >12 months ago, the librarian's Monday digest surfaces a "consider rerunning onboarding" prompt |

The skill is idempotent — running it twice is safe. The second run loads the prior answers as defaults; the customer accepts or overrides each one.

## Interview structure — 6 sections, ~18 questions

The interview is conversational. Questions ask ONE thing at a time (per the operator's standing rule: never autonomously fabricate inputs). The agent waits for each answer before asking the next.

### Section 1 — Identity (3 questions)

1. **What's your name?** (used in greetings, sign-offs, never in agent output to others)
2. **What's your primary role?** (used to seed agent context — e.g., "founder," "sales engineer," "marketing director")
3. **What's the single sentence that describes what you're trying to build right now?** (the locked mission — used as the anchor every session opens with)

### Section 2 — Schedule (4 questions)

1. **What time do you start work most days?** (used by the session-prelude hook to know when the workday begins)
2. **What time is your hard stop?** (used by the time-call hook to nudge wrap-up; e.g., 4 PM family time)
3. **Which days are off-limits for work?** (used by the personal-time guardrail; e.g., "Saturdays" / "Sunday mornings")
4. **What's your timezone?** (used for cron schedules — librarian weekly sweep fires Sunday 11 PM customer-local-time)

### Section 3 — Business context (4 questions)

1. **What's the company / brand you operate under?** (used in proposals, contracts, email signatures — never in agent prompts)
2. **What industry / vertical do you serve?** (seeds the sales-director, deep-researcher, marketing-director context)
3. **Who are your 2-3 closest competitors?** (seeds the competitive-scan + research briefs)
4. **What CRM / prospecting tool do you currently use?** (informs sales-outreach + prospecting-agent integrations — e.g., HubSpot, Apollo, Salesforce, none)

### Section 4 — Goals (3 questions)

1. **What's your revenue target for the next 12 months?** (seeds finance-manager + sales-director + the pnl-tracker default)
2. **What's the single biggest constraint right now?** (cash / time / pipeline / team — informs what the agents prioritize surfacing)
3. **By when do you need to hit your target?** (the date the deal-economics skill measures progress against)

### Section 5 — ADHD / focus preferences (3 questions)

1. **Do you want the agents to flag a hard-stop reminder?** (Y/N — if Y, ask at what time)
2. **Do you want a daily Anchor block on a specific day?** (e.g., "Monday 7 AM weekly planning")
3. **Do you want agents to drop polish when you're moving fast?** (Y/N — informs the `match_execution_mode` behavior)

### Section 6 — Voice (1 question)

1. **Whose writing voice do you most want your agents to sound like? Or describe the voice register in 1-2 lines.** (seeds `agents/<each>/personality/voice_modes/<custom>.md` — the cohort lesson on voice authoring goes deeper later)

## Files generated (the 6-file output)

After the interview completes, the skill writes the following:

| # | File | Built from |
|---|---|---|
| 1 | `CLAUDE.md` (root, personalized section appended below the architectural section) | Sections 1, 2, 4 — identity, schedule, mission |
| 2 | `~/.claude/CLAUDE.md` (operator-personal, OUTSIDE the product folder) | Sections 1, 2, 5 — name, schedule, ADHD prefs (per Anthropic canonical pattern: personal state lives outside the product) |
| 3 | `agents/<each-of-20>/personality/voice_modes/<customer>.md` (a single default voice mode generated from Section 6) | Section 6 |
| 4 | `agents/<each-of-20>/context/00-operator-profile.md` (one-page operator-context per agent, tailored to that agent's domain) | Sections 1, 2, 3 — name, role, industry, competitors |
| 5 | `hooks/routing-rules.json` overrides for the customer's vocabulary (e.g., they call their CRM "HubSpot" not "the CRM") | Section 3 |
| 6 | `agents/librarian/prune-policy.md` — tuned `stale_after_days` + `max_quarantine_per_sweep` based on Section 4's tempo signal | Section 4 |

Each generated file carries a frontmatter line:

```yaml
generated_by: onboarding
generated_at: <YYYY-MM-DD HH:MM:SS>
interview_version: "1.0.0"
```

So that future re-runs of onboarding can detect "this file was previously generated; do you want to keep the customer's manual edits or regenerate?"

## Implementation outline (for the future build session)

This skill needs to be implemented as an interactive Claude session, not a script. The mechanics:

1. **Question delivery** — uses the `AskUserQuestion` tool (per the operator's interactive-protocol rule: ask one question at a time, never fabricate)
2. **Answer storage** — collects answers in an in-memory dict; doesn't write any file until all questions are complete
3. **Confirmation gate** — before writing, show the customer a summary of all 18 answers and the 6 files about to be generated. Customer hits Y to commit; N to revise.
4. **File writing** — uses `Write` tool per file; never `Edit` (this is a fresh generation, not an update)
5. **Verification** — after writing, runs a spot check: did each file land in the right path? Each file has the frontmatter stamp? Reports any failures to the customer.
6. **Post-onboarding nudge** — final message: "ROOK is now yours. Try invoking the chief-of-staff to verify everything works. The librarian will run its first weekly sweep next Sunday."

## Subagent strategy

The interview itself stays on the main thread (interactive). File generation can be parallelized — once all 18 answers are collected, spawn parallel subagents to write the 6 files (or 60+ files if counting per-agent voice_modes + per-agent operator-profile). One subagent per file group:

- Subagent 1: `CLAUDE.md` (root) + `~/.claude/CLAUDE.md` — 2 files
- Subagent 2: voice_modes — 20 files
- Subagent 3: operator-profile context — 20 files
- Subagent 4: `routing-rules.json` overrides + `prune-policy.md` — 2 files

Each subagent reports back a one-line success/failure. Main thread synthesizes into the final summary.

## Anti-patterns the implementation must avoid

- **Don't ask everything in one message.** The operator's interactive-protocol rule: one question at a time.
- **Don't write files before confirmation.** Show the summary first; let the customer hit Y/N.
- **Don't reference the operator's actual name in any generated agent file.** Customer names go in `~/.claude/CLAUDE.md` (personal, outside the product) only. Generated agent files use `[Your Name]` or omit entirely.
- **Don't generate "AI-slop" voice modes.** If the customer doesn't have a clear voice preference, default to the existing `_default.md` rather than fabricating a hybrid.
- **Don't skip the confirmation gate.** Even if the interview is fast, the customer must explicitly approve before files write.

## Voice spine (operator-level — what the onboarding agent itself sounds like)

The onboarding agent uses the ROOK default voice. It is warm-but-terse: complete sentences, no AI warmth defaults ("great question!"), no bullet-list-as-default-output (questions are sentences, not lists). It treats the customer as a peer operator, not a buyer. The interview reads like a senior consultant clarifying scope, not an onboarding wizard.

## Estimated build time

3-4 hours for the full implementation:
- Interview flow with `AskUserQuestion`: 1 hour
- File-generation logic (6 template files + 18 substitution variables): 1.5 hours
- Confirmation gate + post-write verification: 30 min
- Test pass with a fresh-install dry-run: 30-60 min

## Cross-references

- [`hooks/INSTALL.ps1`](../../hooks/INSTALL.ps1) + [`hooks/INSTALL.sh`](../../hooks/INSTALL.sh) — call this skill at the end of the install routine
- [`agents/librarian/prune-policy.md`](../../agents/librarian/prune-policy.md) — one of the generated files
- [`context-loop.md`](../../context-loop.md) — the substrate the interview personalizes
- [`vault-provenance.md`](../../vault-provenance.md) — the receipt the customer reads BEFORE onboarding (sets expectations)

## Open implementation questions

1. **Voice mode generation from a 1-sentence prompt** — is a 1-sentence answer enough to author a useful voice mode, or does Section 6 need 2-3 sub-questions? Current spec is minimum-viable; can expand.
2. **Onboarding as a one-shot vs a progressive disclosure** — should the customer be able to stop at any section and resume later? Current spec treats it as one continuous interview. Resumable might be friendlier for ADHD users.
3. **Schema for `agents/<each>/context/00-operator-profile.md`** — current spec says "one-page operator-context tailored to that agent's domain." Need to define the schema: what fields, what length, what variability across the 20 agents.

Park these for the implementation session.
