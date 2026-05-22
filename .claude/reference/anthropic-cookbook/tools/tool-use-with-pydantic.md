---
name: tool-use-with-pydantic
source: https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/tool_use_with_pydantic.ipynb
fetched: 2026-05-22
category: Tools & Tool Use
rook-relevance: medium
rook-status: absorb-recommended
---

# Tool Use with Pydantic

## What it is

Pydantic models act as a contract layer between Claude's tool calls and Python business logic. Define BaseModel classes for tool inputs/outputs → auto-emit JSON Schema for Claude → validate Claude's returned arguments by reconstructing the Pydantic instance. Invalid emails, out-of-range integers, malformed nested objects fail loudly at validation time, before any side effect runs. Pydantic becomes the single source of truth: schema, validation, type hints.

## Key code/config

```python
class Author(BaseModel):
    name: str
    email: EmailStr

class Note(BaseModel):
    note: str
    author: Author
    priority: int = Field(ge=1, le=5, default=3)
    is_public: bool = False
```

Validate on tool call:

```python
note = Note(
    note=tool_input["note"],
    author=Author(**tool_input["author"]),
    priority=tool_input.get("priority", 3),
)
```

If Claude provides an invalid email or out-of-range priority, `ValidationError` raises with a structured message that can be returned to Claude for self-correction.

## Measured improvements / costs

No quantitative metrics. Qualitative wins: type safety, runtime input validation, executable schema docs, self-healing when validation errors return to Claude. Cost: ~10-15 lines of boilerplate per tool.

## ROOK applicability

ROOK's Tier 2 SQLite agents (account-manager, finance-manager, sales-director, shopify-agent, trading-analyst, inbox-manager) all write structured records — exactly the use case where Pydantic validation prevents silent corruption. Currently they validate ad-hoc inside SKILL.md mode steps. A `.claude/reference/templates/pydantic-schemas/` shelf with canonical models (Deal, Invoice, Order, Setup, Thread) would centralize the contract and eliminate per-agent drift. Engineering-lead's BOM parsing is another fit.

## Recommended action

**absorb-recommended** — add a Pydantic-schema shelf at `.claude/reference/schemas/` for Tier 2 agents. Each Tier 2 agent's SKILL.md Step 2 loads the relevant schema module. Effort: ~1 day to write the 6 schemas + retrofit one agent as proof.
