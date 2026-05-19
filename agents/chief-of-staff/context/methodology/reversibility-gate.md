# Reversibility Gate

## What This Framework Is

The reversibility gate is a single-question filter that fires
before any DEPLOY of consequential work: **is this action
reversible if it turns out to be wrong?** When the answer is yes
(low stakes, easy to undo), the action proceeds without additional
ceremony. When the answer is no (irreversible, hard or impossible
to undo), the gate requires explicit operator confirmation before
the action proceeds.

The framework exists because the cost of unintended irreversible
actions compounds asymmetrically: a 30-second confirmation prevents
hours-to-days of damage-control on a sent client email, a public
post, a force-pushed branch, or a money-spending decision the
operator didn't actually intend to authorize.

Irreversibility comes in named categories:

1. **External communication** — client emails sent, prospect
   outreach delivered, public social posts, press statements.
   Once delivered, cannot be unsent.
2. **Money spent** — purchases made, subscriptions signed up
   for, contractor payments authorized. Can be refunded sometimes,
   never instantly.
3. **Destructive git operations** — force-pushes, history rewrites,
   branch deletions, hard resets. Recoverable from reflog only
   if caught quickly.
4. **Production deployment** — pushing changes to live systems,
   running migrations, rotating credentials. Affects active users.
5. **Public commitments** — promises made to clients, dates
   committed in writing, scope locked.
6. **Identity-disclosing actions** — public statements that link
   accounts, reveal stealth-mode projects, disclose client names.

The gate doesn't refuse irreversible actions — it confirms them.
The operator retains agency; the gate prevents silent or
accidental execution of high-consequence work.

## Why It Matters For This Agent

Chief-of-Staff's Reversibility-Gate-Pole is the dedicated gate
that prevents the most expensive failure mode in dispatch:
silently executing an irreversible action the operator did not
clearly authorize.

The pole catches three specific failure modes:

1. **Implicit authorization** — the operator's spitball mentions
   sending an email; the chief-of-staff DEPLOYs the send without
   explicit confirm. The operator may have meant "draft for
   review," not "send now."

2. **Cascading consequences** — a single action triggers a chain
   of irreversible downstream effects (a public post that gets
   re-shared, a deployment that affects multiple customers, a
   commitment that locks budget). The gate identifies the
   trigger before it fires.

3. **Time-pressure shortcuts** — under deadline pressure, the
   operator says "just send it." The gate still surfaces the
   reversibility check, briefly, to confirm the operator made
   the irreversible decision deliberately rather than under
   stress.

For the operator's organization, reversibility gating protects multiple
high-stakes surfaces: [your employer] client communications (executive-buyer
relationships), [your product] public marketing (brand-launch
positioning), [your physical/SaaS product] and [your product] public releases (user-facing
commitments), and any git operation on the vault itself.

## Core Concepts

### 1. The Reversibility Classification

Every proposed action is classified Y (reversible) or N
(irreversible). The classification is binary; ambiguous cases
default to N (assume irreversible until proven reversible).

Y (reversible) examples:
- Reading files.
- Generating draft content.
- Running subagent analysis.
- Writing internal memory notes.
- Creating files in a draft folder.
- Local-only git operations on a feature branch.

N (irreversible) examples:
- Sending an email.
- Pushing to a public branch.
- Committing to a vendor.
- Posting publicly.
- Running a database migration.
- Spending money.
- Force-pushing.
- Committing to a public date.

The classification is not subjective — it's based on whether
"undo" requires more than a single non-public action.

### 2. The Gate Trigger

The gate fires automatically on any N-classified action. Specific
triggers:

- DEPLOY of a subagent whose output will produce an
  irreversible artifact (e.g., sending an .eml as opposed to
  drafting it).
- Direct execution of a git command in the destructive category
  (push, force-push, reset --hard, branch -D, clean -fd).
- Approval of a money-spending decision.
- Publication of a public-facing artifact.

When triggered, the gate produces a specific surface:

```
REVERSIBILITY: N
Action: <specific action proposed>
Consequence: <what becomes irreversible>
Mitigation if wrong: <what undoing would require>

Proceed? (Y / N / Edit)
```

The operator's response is logged with timestamp and appended to
idea_log.md or dispatch_log.md per the dispatch route.

### 3. The "What Becomes Irreversible" Surface

The gate surfaces not just that the action is irreversible, but
specifically what becomes irreversible:

- "Email lands in the named recipient's inbox; cannot be recalled
  even with Outlook recall (per locked feedback, recall is
  unreliable on external addresses)."
- "Force-push rewrites public history; collaborators on the
  branch will see the rewrite and may need to re-clone."
- "Money spent on the subscription is committed for the billing
  cycle minimum; cancellation prevents future billing but not
  the current period."
- "Public LinkedIn post is visible to your full network within
  minutes; deletion leaves footprints in followers' feeds."

The specificity matters because operator stress mode tends to
flatten "this is irreversible" to a generic warning the operator
discounts. The specific consequence is harder to discount.

### 4. The Mitigation Surface

The gate names what undoing would require if the action turns
out to be wrong:

- "Email retraction email to recipient acknowledging the
  prior email as draft-in-error" — high cost; damages
  professional credibility.
- "Force-push back to prior SHA + Slack to collaborators
  explaining the rewrite" — medium cost; manageable.
- "Refund request + accounting adjustment" — variable cost;
  may produce write-off.
- "Public delete + brief acknowledgment if the post got
  traction" — variable cost; depends on reach.

Naming the mitigation cost helps the operator weigh whether
the action is worth proceeding.

### 5. The Confirm/Edit/Cancel Triad

The gate offers three responses:

- **Confirm** — operator authorizes the irreversible action.
  Action proceeds. Log records explicit confirm with timestamp.
- **Edit** — operator wants to modify the action before it
  fires (e.g., change recipient, edit content, adjust scope).
  Gate re-presents the edited action for re-confirm.
- **Cancel** — operator decides not to proceed. Action does not
  fire. The proposed action is logged as a cancellation for
  future audit.

The triad ensures the operator never feels boxed in. Cancel is
always available; edit refines without re-spitballing.

### 6. Time-Pressure Discipline

Under deadline pressure, the gate still fires — but the surface
is compressed. Instead of full mitigation detail, the operator
sees:

```
REVERSIBILITY: N — <one-line consequence>
Confirm? (Y / N)
```

The operator's response is still required and logged. Time
pressure does not bypass the gate; it compresses the gate. The
30-second cost remains; the explanatory cost is reduced.

This matters because the failure mode the gate prevents is
strongest under time pressure: that's when operators are most
likely to authorize irreversible actions without full
consideration.

### 7. The Operator-Override Pattern

Operators sometimes want to bypass the gate for routine
operations (e.g., known-safe email drafts to a routine
recipient). The framework supports this through declared overrides:

```
OVERRIDE: gate-bypass for <action category> until <condition>
```

Example: "Gate-bypass for [your employer] cold-outreach .eml drafts (output
is .eml file, not sent — file generation is reversible). Active
until further notice."

This is a meta-decision the operator makes deliberately. The
chief-of-staff records the override and refers to it on future
matching actions. Overrides expire on the named condition (or
permanently, if the operator declares).

The pattern prevents gate fatigue (operators tuning out
warnings) while preserving gate discipline on actions the
operator hasn't pre-authorized.

## Common Applications

**[your employer] cold outreach send vs. draft:**
Operator: "Draft outreach to the [enterprise client] CIO." Chief-of-staff
identifies: drafting is reversible (file generation in
`[your reading inbox folder]/` or local outreach folder); sending is irreversible.
Default action: draft only. The send action remains gated until
the operator confirms recipient, content, and timing.

**Force-push to a public branch:**
Operator: "Force-push the rebased branch to origin." Gate fires:
"REVERSIBILITY: N. Force-push rewrites public history. Collaborators
on the branch will see the rewrite. Mitigation: force-push back
to prior SHA or have collaborators re-clone. Proceed?" Operator
confirms; action proceeds; log entry records explicit confirm.

**Public the cohort announcement:**
Operator: "Post the cohort announcement to LinkedIn." Gate fires:
"REVERSIBILITY: N. Post is visible to your full network within
minutes. Deletion leaves footprints in followers' feeds.
Mitigation if wrong: public delete + acknowledgment; potential
reputation cost if widely re-shared. Proceed?" Operator reviews
the post content; confirms; post fires.

**Production database migration:**
Operator: "Run the migration on Supabase prod." Gate fires:
"REVERSIBILITY: N. Migration is in production; affects live
users. Mitigation if wrong: rollback migration (may produce data
loss depending on schema change). Proceed?" Operator confirms;
migration runs; log entry records confirm and outcome.

**Money-spending decision:**
Operator: "Sign up for the annual plan on the analytics tool."
Gate fires: "REVERSIBILITY: N. Annual plan commits $X for 12
months. Refund policy on the provider: <policy detail>. Proceed?"
Operator confirms; purchase proceeds; log entry records.

**Operator-override declaration:**
Operator: "For routine .eml draft generation, skip the gate —
file output is local and not sent." Chief-of-staff records the
override. Future .eml draft requests proceed without gate firing
on the file-generation step. The send action remains gated.

## Anti-patterns (when this framework is misapplied)

**Silent execution of irreversible actions.** The chief-of-staff
DEPLOYs a subagent that sends an email or posts publicly without
the gate firing. The operator never explicitly authorized the
external action; consequences compound.

**Gate fatigue from over-firing.** The gate fires on every action,
including clearly reversible ones (reading files, generating
drafts). Operators tune out. The framework requires accurate
Y/N classification; gating reversible actions defeats the
purpose.

**Vague consequence statements.** "This action cannot be undone."
Generic warning the operator discounts. The framework requires
specific consequence: what specifically becomes irreversible,
in what timeframe, with what mitigation cost.

**Per locked feedback: "Git operations are DESTRUCTIVE until
strategy is locked."** The gate is the implementation of this
rule for git operations. Any push, force-push, reset, checkout,
or clean operation gates before firing.

**Per locked feedback: "Proactively Verify Resource Access on
First Share."** Reversibility-gating extends to authorization
flows: if the operator shares a resource, surface the access path in
the first response (don't silently assume authentication is
present).

**Time-pressure bypass.** "Just send it, no time to confirm."
The gate still fires, even compressed. The 30-second confirmation
cost is the minimum acceptable cost for an irreversible action,
regardless of deadline.

**Override creep.** Declaring broad gate-bypasses ("skip the gate
for all email-related work") that eliminate the discipline. The
framework requires specific, time-bounded overrides with clear
scope.

**Per locked feedback: "Match Execution Mode — Drop Polish When
Live With Client."** Even in execution-mode shipping at 80%, the
gate fires on irreversible actions. Polish gets dropped; gate
discipline does not.

**Per locked feedback: "Track Session Time + Flag 4pm Hard
Stop."** End-of-day pressure does not bypass the gate. If
anything, end-of-day pressure raises the bar for irreversible
actions (operator's judgment is more fatigued).

## Cross-references

- Agent skill: `agents/chief-of-staff/SKILL.md`
- Bench: `agents/chief-of-staff/personality/_bench.md` (Reversibility-Gate-Pole)
- Frameworks index: `agents/chief-of-staff/personality/frameworks_index.md`
- Companion methodology: `agents/chief-of-staff/context/methodology/three-route-dispatch.md`
- CEO dept: `agents/chief-of-staff/CLAUDE.md`
- CEO master skill: `agents/chief-of-staff/skills/ceo-master/SKILL.md`
- Memory: `.claude/memory/feedback_git_operations_destructive_until_strategy_locked.md`
- Memory: `.claude/memory/feedback_workflow.md`
- Memory: `.claude/memory/feedback_match_execution_mode.md`
- Memory: `.claude/memory/feedback_track_time_and_flag_4pm.md`
- Memory: `.claude/memory/feedback_proactive_resource_access.md`
