# graphify (vendored)

**Source vendored at `skills/core/graphify/src/`.**
Originally installed user-global at `~/.claude/skills/graphify/`; copied to repo
on 2026-05-14 for upstream-disappearance safety. No nested `.git/` — the
user-global install was not a git repo.

## Vendored contents

```
skills/core/graphify/src/
├── SKILL.md              # the skill itself (canonical instructions)
└── .graphify_version     # version pin
```

The skill is self-contained — instructions live in `src/SKILL.md`. Claude Code
loads it by name; the vendored copy guarantees the skill survives even if the
user-global directory is wiped or the originating author disappears.

## How agents invoke it

Via the canonical Universal Stack wrapper:

```python
graph = graph_query(corpus_path, question)
```

Or directly via slash-command:

```
/graphify <path>
/graphify <repo-url>
/graphify <path> --mode deep
```

## Resolution order

Claude Code's skill loader resolves `graphify` against (in order):
1. Project-local `skills/` (if present)
2. User-global `~/.claude/skills/graphify/`
3. The vendored copy at `skills/core/graphify/src/` (this repo)

For the Stack customers who clone this repo fresh — without an existing
user-global install — the vendored copy is what gets used. No external download
required.

## Cross-reference

Listed as the **Synthesis** capability in `agents/_template/SKILL.md` →
"Universal Stack Capabilities". Paired with MarkItDown (Input) and Obsidian CLI
(Vault I/O) to complete the file → knowledge → vault pipeline.
