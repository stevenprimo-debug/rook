# Onboarding

One-time interactive setup that turns a fresh ROOK install into the customer's ROOK.

## What it does

Walks the customer through a ~15-minute interview (6 sections, ~18 questions) and writes 6 personalization files. After onboarding, every agent reads the customer's profile + voice + schedule on session start.

## When to run

| Trigger | How |
|---|---|
| First-time install | Automatically invoked at the end of `hooks/INSTALL.{ps1,sh}` |
| Customer wants to redo | Customer says "redo onboarding" / "reset my personalization" / "onboard me again" → invokes this skill manually |
| Annual refresh | Librarian Monday digest surfaces a "consider re-running onboarding" prompt if `CLAUDE.md` was last updated >12 months ago |

## How to invoke manually

Inside Claude Code, after install:

```
> Run onboarding.
```

The agent reads `setup/onboarding/SKILL.md` and `setup/onboarding/questions.yml`, walks the interview, shows a confirmation summary, then writes the 6 files.

## What it generates

| # | File | Why |
|---|---|---|
| 1 | `CLAUDE.md` (root product) — personalized section appended | Top-level routing knows who you are |
| 2 | `~/.claude/CLAUDE.md` (operator-personal, OUTSIDE the product) | Global session context follows you across every Claude Code session |
| 3 | `agents/<each-of-20>/personality/voice_modes/<customer>.md` | Each agent speaks in the customer's voice |
| 4 | `agents/<each-of-20>/context/00-operator-profile.md` (`pin: true`) | Each agent reads the customer's profile on session start |
| 5 | `hooks/routing-rules.json` overrides | Inbox routing knows the customer's vocabulary (CRM name, brand, industry) |
| 6 | `agents/librarian/prune-policy.md` (tuned section overwritten) | Librarian sweep tuned to the customer's tempo |

## Layout

```
setup/onboarding/
├── SKILL.md                                    # The interview spec + file-generation logic (full)
├── README.md                                   # This file
├── questions.yml                               # 6 sections × ~18 questions, structured
└── templates/
    ├── voice_mode.md                           # → personality/voice_modes/<customer>.md (per agent)
    ├── operator-profile.md                     # → context/00-operator-profile.md (per agent)
    ├── claudemd-personalized-section.md        # → root CLAUDE.md append block
    ├── personal-claudemd-out-of-vault.md       # → ~/.claude/CLAUDE.md
    ├── prune-policy-overrides.md               # → agents/librarian/prune-policy.md tuned section
    └── routing-rules-overrides.md              # → hooks/routing-rules.json overlay
```

## Design principles

- **One question at a time.** The interview uses Claude Code's `AskUserQuestion` tool. The agent waits for each answer before asking the next. Never fabricates inputs.
- **Confirmation gate.** Before writing any file, the agent shows the customer a summary of all 18 answers and the 6 files about to be generated. Customer hits Y to commit, N to revise.
- **Idempotent.** Re-running is safe. The agent loads prior answers as defaults, the customer accepts or overrides each one.
- **Frontmatter stamps.** Every generated file carries `generated_by: onboarding` + `generated_at: <timestamp>` + `interview_version: "1.0.0"` so future re-runs can detect and update without overwriting customer manual edits.
- **No customer name in agent prompts.** The customer's actual name goes only in greetings, sign-offs, and `~/.claude/CLAUDE.md`. Agent-facing files use `{{name}}` placeholders that the agent reads but doesn't echo into customer-facing output.

## Implementation status

- [x] Spec written — `SKILL.md`
- [x] Questions structured — `questions.yml`
- [x] All 6 templates written — `templates/`
- [ ] Interview-runner agent built — next session
- [ ] First-install integration via `hooks/INSTALL.{ps1,sh}` — next session
- [ ] Test pass with a fresh-clone dry-run — next session

Estimated 3-4 hr to runnable from current state (spec + templates done; implementation glue + integration + test remaining).

## Cross-references

- [`SKILL.md`](SKILL.md) — full spec including subagent strategy + anti-patterns + voice spine
- [`questions.yml`](questions.yml) — the 6-section question structure
- [`templates/`](templates/) — the 6 file templates
- [`../../hooks/INSTALL.ps1`](../../hooks/INSTALL.ps1) + [`../../hooks/INSTALL.sh`](../../hooks/INSTALL.sh) — where the first-install hook calls this
