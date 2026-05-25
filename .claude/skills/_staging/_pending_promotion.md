# Pending promotion queue

Append-only queue read by librarian Monday digest. Format per line:

```
- [ ] <YYYY-MM-DD> | <slug> | proposed_scope: <scope> | source_session: <session-id> | trigger: <Stop|PreCompact|SessionEnd|manual>
```

Librarian checks boxes on approve/reject. Stale (>30 days) entries auto-archive.

See `README.md` in this directory for the full handoff contract.

---

<!-- entries below -->
