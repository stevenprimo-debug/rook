# Graphify First-Run Install Gate

> the Stack convention. Graphify is third-party OSS (`safishamsi/graphify`,
> MIT-licensed, published to PyPI as `graphifyy`). It is NOT vendored in the
> Stack repo. Customers install it on first use via a one-line approval prompt.
>
> This doc defines the gate behavior. The upstream Graphify SKILL.md at
> `src/SKILL.md` is untouched (preserves upstream-sync compatibility).

---

## When the gate fires

Every the Stack agent has `graphify` in its `skills:` block as part of the
Universal Stack. When an agent invokes `/graphify` (or any Graphify command), it
first checks whether the CLI is available.

```bash
# Check command (run silently before any Graphify invocation)
command -v graphify > /dev/null 2>&1 && echo "INSTALLED" || echo "MISSING"
```

If `MISSING`, the agent surfaces the install gate to the user. Do NOT silently
install; Graphify install adds a PyPI package + dependencies to the user's
environment, which is a customer-side change requiring approval.

## Gate prompt (exact wording)

```
Graphify (third-party OSS, MIT-licensed — safishamsi/graphify, PyPI `graphifyy`)
is not installed. Graphify is the synthesis layer of the Universal Stack —
it turns any input into a queryable knowledge graph and powers the librarian's
drift detection.

Install with:
  uv tool install graphifyy

(Equivalent: pipx install graphifyy / pip install graphifyy)

Approve install? [Y/n]
```

## On approval (Y)

Run the install command via the agent's Bash tool:

```bash
uv tool install graphifyy && graphify --version
```

If `uv` is not available, fall back to:

```bash
pipx install graphifyy 2>/dev/null || pip install graphifyy
```

Verify with `graphify --version`. Cache the install state so the gate doesn't
fire again on subsequent invocations.

## On rejection (n)

Acknowledge briefly: "Graphify not installed. Knowledge-graph features
unavailable. You can install later with `uv tool install graphifyy`."

The agent continues operating without Graphify — the other Universal Stack
tools (markitdown / obsidian-cli / html2pdf) still work. Graphify-dependent
features (librarian drift detection, deep-research synthesis, knowledge-graph
queries) degrade gracefully:
- `librarian` switches to file-based audit instead of graph-based audit
- `deep-researcher` skips graph synthesis, returns raw markdown
- `chief-of-staff` skips graph-based dispatch heuristics

## On install failure

If `uv tool install graphifyy` fails, return the error verbatim and offer:

```
Install failed. This typically means:
  - `uv` is not installed → install via https://github.com/astral-sh/uv
  - Network blocked → check connectivity to PyPI
  - Permission denied → use `pipx install --user graphifyy`

You can install Graphify manually and re-invoke. Knowledge-graph features
will activate automatically once the CLI is on PATH.
```

## Attribution

Graphify is third-party OSS by safishamsi. the Stack ships the skill
manifest (in `src/SKILL.md`) which calls the upstream binary. We do not
vendor the engine code — the customer's PyPI install is the source of truth.

License: MIT. Repo: https://github.com/safishamsi/graphify

## Why install-on-demand rather than vendor

Three reasons (v3 locked session):

1. **Upstream actively maintained.** Vendoring freezes a snapshot; PyPI gives the customer the latest version automatically.
2. **Engine size.** The Graphify engine + its dependency tree (networkx, leidenalg, etc.) would bloat the Stack repo significantly.
3. **Customer control.** Install gate keeps the customer in control of what runs on their machine. They can decline, defer, or pin a specific version.

Trade-off: customers need network + a Python package manager on first run.
That's an acceptable bar for the target audience (technical operators).

## How this gate is invoked

Every agent that has `graphify` in its `skills:` block inherits this gate.
The agent's `Step 1 — Load Context` includes a Graphify-install check before
any Graphify command runs. Implementation lives in the agent's skill body,
referencing this doc as the canonical behavior spec.
