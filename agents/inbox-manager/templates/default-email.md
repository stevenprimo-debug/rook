# ROOK Inbox Manager — Default Email Template

**Format:** Plain text. No HTML. No markdown.
**Opener:** Always "Hello [First Name]," — no variation.
**Sign-off:** Left to operator — this template has no sign-off block.
**Voice:** ROOK default — clear, direct, no filler.

---

Hello [First Name],

[Primary point in one sentence — what you need / what you are sharing.]

- [Bullet: context or detail 1]
- [Bullet: context or detail 2]
- [Bullet: action or next step if applicable]

[Optional: single follow-up question or clear call to action in one sentence.]

---

## Usage notes

- Replace every  placeholder before sending.
- Keep bullet count to 2-4. More than 4 bullets = restructure into two emails.
- Inbox Manager will not send without explicit operator confirmation (reversibility gate).
- Tone calibration goes in  — not in this template.
- Reply patterns (common scenarios) go in .

## Operator-local override

If the operator vault has a custom email format (e.g.,  for Outlook drafts,
or a different sign-off), configure it in the operator session config — not here.
This file ships with the ROOK default. The ROOK default is NOT the operator's personal pattern.
