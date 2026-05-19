# _archive/

Quarantined content — the librarian's "delete is forbidden, archive only" landing zone.

## What goes here

When the librarian's weekly sweep determines a file is no longer load-bearing in the active vault:

- The file moves to `_archive/YYYY-MM/<slug>.md`
- A tombstone (one-line pointer at the original path) stays in place
- The active vault no longer surfaces the file in agent context loads, but the history is preserved

## Folder structure

```
_archive/
├── README.md                 ← this file
├── YYYY-MM/                  ← monthly buckets, librarian-created
│   ├── pruned/               ← stale files no longer load-bearing
│   └── superseded/           ← files replaced by versioned-append successors
└── HANDOFFS/                 ← session handoff logs (append-only, auto-generated)
```

## What you do here

Nothing routine. The archive is the audit trail. Files here:

- Are append-only (never edit an archived file)
- Get referenced by the librarian's Monday digest when relevant
- Can be restored to active path via the librarian's `archive-pass` mode if needed

## Restore path

If a file was archived prematurely and needs to come back to the active vault:

1. Invoke librarian: "restore [path]"
2. Librarian moves the file back to its active path
3. The archive entry stays (with a `restored YYYY-MM-DD` note) — history of the restoration is preserved

## Why not just delete?

Compounding history is the moat. The audit trail of decisions, lessons, contradictions surfaced, and "we tried this and it didn't work" is what makes the vault get smarter over time. Deletion breaks the loop. Archive preserves the loop while keeping the active vault fast.

If you find yourself wanting to delete content from the archive itself, stop. The archive is frozen. Add a tombstone elsewhere if you need to mark something as "do not surface."
