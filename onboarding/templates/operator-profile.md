---
file: 00-operator-profile
agent: {{agent_name}}
generated_by: onboarding
generated_at: {{generated_at}}
interview_version: "1.0.0"
pin: true   # Never auto-quarantined by the librarian; load-bearing for every session.
---

# Operator Profile — {{agent_name}}

The customer-context this agent loads on every session start. Generated from the onboarding interview.

## Who they are

- **Role:** {{role}}
- **Mission (current):** {{mission_sentence}}
- **Company / brand:** {{company_brand}}
- **Industry:** {{industry}}

## How to work with them

- **Workday:** {{workday_start}}–{{hard_stop}} ({{timezone}})
- **Off-days:** {{off_days}}
- **Biggest constraint right now:** {{biggest_constraint}}
- **Revenue target (12-mo):** ${{revenue_target_12mo}} by {{target_date}}

## Their working preferences

- **Hard-stop reminder:** {{hard_stop_reminder}}
- **Weekly anchor:** {{weekly_anchor}}
- **Drop polish when moving fast:** {{drop_polish_when_fast}} — when this is `true`, ship 80% over wait at 100% during live / time-pressured / client-facing work

## Competitive context for {{agent_name}}

{{agent_specific_competitive_block}}

The customer's named competitors (across all agents): {{competitors}}

## Tooling they use

- **CRM / prospecting:** {{crm_tool}}

## Standing rules

- Never use the customer's name (`{{name}}`) in any output that leaves this agent — only in greetings + acknowledgments + personal CLAUDE.md. Public surfaces are name-neutral.
- Never name the company brand in agent prompts as if it's the user's identity — `{{company_brand}}` is the customer's COMPANY, not their self-concept.
- Honor the customer's voice mode (`personality/voice_modes/{{voice_mode_slug}}.md`) for every output.

## Updating this file

The customer can edit this file directly. Or re-run onboarding to regenerate from a fresh interview.

The `pin: true` frontmatter exempts this from the librarian's weekly quarantine sweep — this is load-bearing context for every session, never to be archived automatically.
