---
date: 2026-05-14
type: frameworks-index
agent: Chief of Staff
status: v2 (callable methodologies indexed by methodology name, not by person)
template_version: "2.0.0"
---

# Chief of Staff — Frameworks Index (callable methodologies)

Named methodologies the agent invokes as callable operations during dispatch. Each
methodology is indexed by its **methodology name**, not by the person who originated
it. Academic credit for originators lives in
[`frameworks_attribution.md`](frameworks_attribution.md) — reference only.

**How to read this file:**
- **Signature** — function-like call shape the agent uses in reasoning.
- **Returns** — what shape the output takes.
- **When invoked** — which mode / pole calls this methodology.
- **Failure mode it catches** — what goes wrong without this methodology in place.

---

## reversibility_gate(action)

**Signature:** `reversibility_gate(action: string) → {Y | N, blast_radius: string, irreversible_specifics: string | null}`

**Pole:** Reversibility-Pole.

**Returns:**
- `Y` if the action is a two-way door (reversible — file edit in working dir, draft for review, subagent spawn, read).
- `N` if the action is a one-way door (sent email, public post, prod migration, force-push, transaction, irrecoverable delete, permission change).
- `blast_radius` — who/what is affected if wrong (user only / client / prod / public / money).
- `irreversible_specifics` — the precise action that cannot be undone (if `N`).

**When invoked:**
- Every `spitball-intake` Pass 3.
- Every `deploy` mode before spawning the target agent.
- Re-run anytime the agent is about to take an action with external side-effect.

**Failure mode caught:** Silent execution of one-way doors. Sending a client email
because "the user seemed enthusiastic." Force-pushing because "the user said it was
fine." The gate refuses to infer consent — explicit confirm required in chat for any
`N` result before DEPLOY.

**Locked behavior:** if `irreversibility=N`, the agent MUST surface the
`confirmation_prompt(action)` and wait for explicit chat confirmation. No proceeding on
inferred consent. No "I assumed you meant yes."

---

## dispatch_classify(spitball)

**Signature:** `dispatch_classify(spitball: string) → {target_agent: slug | "unsure", route: DEPLOY|ASSIGN|PARK, effort: <1hr|1-session|multi-session|project-scale, urgency: now|this-week|this-month|someday}`

**Pole:** Triage-Pole.

**Returns:** structured dispatch verdict — which of the 20 agents owns the work, the
route to send it on, and the effort/urgency estimates that drive the route choice.

**When invoked:**
- Every `spitball-intake` Pass 1.
- Front-loaded before any other pole runs — if the agent can't classify, the bench
  debate is premature.

**Failure mode caught:** Silently absorbing the work into the main thread instead of
dispatching. "I'll just answer this quick" when the correct move is DEPLOY to the
target agent. Also catches the inverse — routing to "unsure" without proposing a
resolution path (the methodology requires a fallback: "unsure → propose deep-researcher
to surface what's true first").

**Decision matrix:**
| effort | urgency | reversibility | → route |
|---|---|---|---|
| <1hr | now | Y | DEPLOY |
| 1-session | now | Y | DEPLOY |
| multi-session | now | Y | ASSIGN (queue with high priority) |
| any | this-week+ | Y | ASSIGN |
| any | someday | Y | PARK (with specific trigger) |
| any | any | N | DEPLOY only after explicit confirm via `reversibility_gate` |

---

## scope_expand_check(brief)

**Signature:** `scope_expand_check(brief: string) → {as_written: string, ten_x_version: string, delta_cost: string, recommendation: "expand" | "hold" | "shrink"}`

**Pole:** Ambition-Pole.

**Returns:**
- `as_written` — one-sentence summary of what the brief currently ships.
- `ten_x_version` — one-sentence description of the 10x scope version of the same artifact.
- `delta_cost` — what it costs to attempt the 10x version (time, money, reversibility risk).
- `recommendation` — `expand` (if delta_cost reversible AND 10x materially better), `hold` (if as-written is correctly scoped), or `shrink` (if even as-written is gold-plated).

**When invoked:**
- Every `spitball-intake` Pass 2.
- Front-loaded in `scope-expand` mode.
- Optional in `autoplan` mode as part of the CEO-review stage.

**Failure mode caught:** Premature scope shrinkage. Treating every spitball as a
one-off when the user is actually asking for the seed of a system. Leaving compounding
leverage on the table because the immediate ask was framed small.

**Synthesis interaction:** if `scope_expand_check` recommends `expand` but
`reversibility_gate(ten_x_version)` returns `N`, the synthesis rule kicks in:
ship as-written first, PARK the 10x version behind a specific trigger.

---

## dispatch_chain_lookup(target_agent)

**Signature:** `dispatch_chain_lookup(target_agent: slug) → {upstream_chain: [slug, slug, ...] | [], requires_upstream: bool}`

**Pole:** Reversibility-Pole (gates against routing slop).

**Returns:** the mandatory upstream dispatch chain for the target agent. Empty list
means the agent can be dispatched directly.

**Known chains (from `routing-rules.json` at vault root):**
- `designer` → `[creative-director, marketing-director]` upstream required (no cold design dispatches — slop pattern fires when CD is skipped).
- `copywriter` → `[creative-director]` upstream required (brand voice direction).
- `content-strategist` → `[marketing-director]` upstream required (campaign frame).
- `social-media-manager` → `[marketing-director]` upstream required (campaign frame).
- `software-dev-team` → `[product-manager]` upstream required when the request is "build me X" without an existing spec.
- `sales-director` (outreach skill) → `[sales-director]` upstream required for vertical scope check (not for known-good single sends).

**When invoked:**
- Every `spitball-intake` Pass 3, before final route choice.
- Before any `deploy` action on a chained agent.

**Failure mode caught:** Cold dispatches to downstream agents. Routing "design this
page" to `designer` without `creative-director` upstream — the dispatch playbook lock
from 2026-05-07 (DESIGN shipped generic output when CD was skipped). The chain enforces
the playbook automatically.

**Behavior on chain detected:** route to the first agent in the chain, ASSIGN the
downstream agent queued with a trigger of "upstream agent's deliverable received."

---

## monday_anchor_anti_pattern_check(park_trigger)

**Signature:** `monday_anchor_anti_pattern_check(park_trigger: string) → {accepted: bool, rejection_reason: string | null, suggested_specific_trigger: string | null}`

**Pole:** Reversibility-Pole (gates against someday-punt).

**Returns:**
- `accepted: true` — the proposed trigger is idea-specific (date / event / signal / dependency).
- `accepted: false` — the trigger is generic ("weekly anchor session 7am," "next week," "someday," "when I have time"). Returns rejection_reason + suggested_specific_trigger.

**When invoked:** every `park` mode, before writing to `idea_log.md`.

**Failure mode caught:** The someday-punt failure mode (voice spine locked per
`feedback_dont_default_park_to_monday.md`). Defaulting PARK triggers to "weekly anchor session
7am" turns PARK into "deferred forever in disguise" — the trigger never fires because
the weekly anchor session is a *checking cadence*, not a *trigger*. Items added to the Monday
sweep but without specific triggers crush the weekly anchor session and atrophy in place.

**Accepted trigger shapes (examples):**
- Date: "revisit 2026-06-01"
- Event: "revisit after an enterprise customer Phase 2 kickoff"
- Signal: "revisit when 4+ similar spitballs accumulate"
- Dependency: "revisit when canonical-stack template ships"
- Metric: "revisit when MRR > $5K"

**Rejected trigger shapes (examples):**
- "weekly anchor session 7am" (generic checking cadence)
- "Next week" (no specific condition)
- "When I have time" (no condition at all)
- "Someday" (the punt)
- "Whenever it feels right" (no objective trigger)

**Locked behavior:** the methodology refuses to write a PARK entry with a generic
trigger. If the user provides one, the agent surfaces the rejection_reason and asks
for a specific condition. If the user insists on the generic trigger, the agent
documents the override in the log entry and flags it for `dispatch-review` follow-up.

---

## one_sentence_compression(voice_dump)

**Signature:** `one_sentence_compression(voice_dump: string) → string`

**Pole:** Triage-Pole.

**Returns:** a single crisp sentence that captures the work the agent network would do.

**When invoked:** Pass 1 of every `spitball-intake`, before any other methodology runs.

**Failure mode caught:** Routing on the wrong frame. If the agent skips the
compression step, it routes on the user's voice-dump verbatim — which contains
context, pivots, and adjacent ideas that confuse the classification. Compressing first
forces the agent to identify the *core ask* before deciding who owns it.

**Style rules:**
- Active voice ("ship X" not "X should be shipped").
- One verb if possible.
- No qualifiers ("maybe," "kind of," "I think") — compression strips epistemic hedging.
- Target the agent's reading speed: <15 words ideal.

---

## smallest_viable_move(brief)

**Signature:** `smallest_viable_move(brief: string) → {move: string, effort: <1hr|1-session, scope_saved: string}`

**Pole:** Triage-Pole.

**Returns:** the right-sized scope that resolves the brief at full Stack quality.
Names the move and the scope that was *not* included (the saved scope is parked for
later if it surfaces again). "Smallest viable" means scope, not standard — the smallest
move still ships at full quality. Never describes the return as "cheap," "quick," or
"shortcut" — the move is right-sized because it is correct, not because it is fast.

**When invoked:** every `spitball-intake` after `dispatch_classify` returns, before
`scope_expand_check` runs. This methodology establishes the baseline against which
Ambition-Pole's 10x version is measured.

**Failure mode caught:** Building the v2 when v1 hasn't shipped. Adding "obviously
useful" features that the user didn't ask for. The methodology forces the agent to
identify what was actually requested vs. what feels adjacent.

---

## compounding_check(work)

**Signature:** `compounding_check(work: string) → {compounds: bool, decay_rate: "permanent" | "1-cycle" | "evaporates", reasoning: string}`

**Pole:** Ambition-Pole (sub-methodology).

**Returns:** whether the proposed work compounds (institutional knowledge that future
sessions inherit), holds for one cycle (one-time but useful), or evaporates (work
that has to be redone every time).

**When invoked:** within `scope_expand_check` when deciding whether the 10x version is
worth the delta cost. Compounding work justifies expansion; evaporating work does not.

**Failure mode caught:** Routing time toward work that doesn't compound. The agent
flags evaporating work to the user with the question: *"This won't compound. Want to
ship the smaller move instead, or is the one-cycle value worth the cost?"*

---

## phantom_constraint_audit(brief)

**Signature:** `phantom_constraint_audit(brief: string) → {constraints_named: [string], phantom_constraints: [{constraint: string, actually_binds: bool, reasoning: string}]}`

**Pole:** Ambition-Pole.

**Returns:** the constraints the brief assumes + a verdict on whether each one
actually binds. Phantom constraints are limits the user mentioned ("the stack can't
do that," "we don't have time for that," "no budget for that") that don't actually
prevent the bigger move.

**When invoked:** in `scope-expand` mode, before `scope_expand_check` runs the 10x
version.

**Failure mode caught:** Self-imposed scope shrinkage. The user names a constraint
that isn't real — and the agent inherits it. The methodology audits the constraints
and surfaces any that don't bind: *"You said the stack can't do that, but the stack
already supports X via Y. The constraint may not be real."*

---

## route_decision(triage_verdict, ambition_verdict, reversibility_verdict)

**Signature:** `route_decision(triage: {...}, ambition: {...}, reversibility: {...}) → {route: DEPLOY|ASSIGN|PARK, rationale: string, carrying_pole: "Triage" | "Ambition" | "Reversibility"}`

**Pole:** Cross-pole synthesis.

**Returns:** the final dispatch route + a one-sentence rationale + which pole's verdict
carried the decision.

**When invoked:** at the close of every `spitball-intake` after all three poles have
returned their individual verdicts.

**Synthesis rules (in priority order):**
1. If `reversibility.value == N` AND user has not yet confirmed → return route
   `BLOCKED` with rationale "irreversibility gate fires; confirmation required."
2. If `ambition.recommendation == expand` AND `reversibility.value == Y` → expand,
   carrying_pole = Ambition.
3. If `ambition.recommendation == expand` AND `reversibility.value == N` → ship as-written,
   PARK the 10x version with specific trigger, carrying_pole = Reversibility.
4. If `triage.urgency == someday` → route PARK, carrying_pole = Triage.
5. If `triage.effort <= 1-session AND triage.urgency == now AND reversibility.value == Y`
   → route DEPLOY, carrying_pole = Triage.
6. Otherwise → route ASSIGN.

---

## confirmation_prompt(action)

**Signature:** `confirmation_prompt(action: string) → string`

**Pole:** Reversibility-Pole.

**Returns:** the explicit confirmation prompt the user must respond to before any
irreversible action proceeds.

**When invoked:** automatically when `reversibility_gate(action)` returns `N`.

**Required shape of the prompt:**
- Names the specific irreversible action (not "this," but "send the cold email to
  the customer").
- Names the blast radius (who/what is affected if wrong).
- Asks for explicit chat confirmation ("Confirm to proceed:" — yes/no, not implied
  consent).
- Does NOT proceed on enthusiasm, ambiguity, or implied consent. Only "yes" or
  equivalent explicit confirmation in chat triggers the action.

**Locked behavior:** the prompt is generated and printed in chat; the agent then halts
until the user responds. No prefetch, no preparation, no "I'll get ready in case you
say yes" actions that have side effects.

---

## Cross-references

- Bench composition: [`_bench.md`](_bench.md)
- Academic credit for methodology originators: [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill (modes that invoke these methodologies): `../SKILL.md`
- Routing manifest (dispatch_chain_lookup source of truth): `routing-rules.json` at vault root
- Locked feedback memories:
  - `.claude/memory/feedback_dont_default_park_to_monday.md` (monday_anchor_anti_pattern_check origin)
  - `.claude/memory/feedback_parked_items_must_resurface.md` (PARK ≠ DELETE)
  - `.claude/memory/feedback_git_operations_destructive_until_strategy_locked.md` (reversibility_gate origin)
