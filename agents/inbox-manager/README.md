# Inbox Manager

**Category:** Operations
**Part of:** ROOK
**Status:** Operational — master skill wired.
**Memory:** Tier 2 (SQLite) for structured thread state, Tier 4 (markdown + grep) for voice corpus + reply patterns

## What it does
Triages every inbound message across Gmail, WhatsApp Business, and connected inbox surfaces. Drafts replies in the operator's voice. Never sends without explicit operator confirm per item or per batch. Read + draft are autonomous; send is gated at the hardest reversibility gate of any agent.

## The bench
Three orthogonal poles in productive tension (named by principle, not by person):
- **Voice-Fidelity-Pole** — "Does this draft sound like the operator, not like an AI?" Reads the voice spine, samples prior sent threads, mirrors cadence and vocabulary. Catches: AI-shaped drafts, generic professional tone, template language. Bias: voice over speed.
- **Inbox-Reduction-Pole** — "Did the queue shrink this cycle?" Nothing rots unread; every thread is categorized, drafted, or archived in the same pass. Catches: cherry-picking easy replies, partial passes, leaving hard threads indefinitely. Bias: full sweep over partial sweep.
- **Reversibility-Discipline-Pole** — "Has the operator explicitly confirmed every external state change?" Never sends, never deletes, never modifies inbox state without explicit operator confirm. Catches: autonomous send attempts, silent archives, batch operations without per-item confirm. Bias: confirm before commit.

## Memory
- `memory/messages.db` — SQLite: messages, threads, drafts, escalations, triage_status
- `memory/voice_corpus.md` — compounding-append: prior sent threads that landed well (voice training signal)
- `memory/reply_patterns.md` — what reply shape lands for what message shape (per sender pattern)

## Connectors
- `gmail` — read inbox, write drafts (reversibility-gated send)
- `whatsapp-business` — read messages, write drafts (reversibility-gated send)

## Installation
See repo-root `INSTALL.md` for the full vault install.

## License
MIT (curated catalog — not accepting external contributions; fork freely).
