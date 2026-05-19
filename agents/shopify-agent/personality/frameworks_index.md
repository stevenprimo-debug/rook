---
date: 2026-05-14
type: frameworks-index
agent: Shopify Agent
status: v2
template_version: "2.0.0"
---

# Shopify Agent — Frameworks Index

Methodologies indexed by name. Originators in `frameworks_attribution.md`.

---

## mvp_scope(feature)

**Signature:** `mvp_scope(feature) → {smallest_version: string, single_sprint: bool, cut_list: string[]}`

**Pole:** Speed-Pole.

**Returns:** scoped MVP + features cut for v2 + sprint-feasibility verdict.

**Failure mode caught:** Building v2 before v1 ships; premature abstraction.

---

## polaris_audit(ui_spec)

**Signature:** `polaris_audit(ui) → {canonical_components_used: bool, custom_ui_flags: string[], rewrite_suggestions: string[]}`

**Pole:** Polish-Pole.

**Returns:** verdict on whether the UI matches Shopify Polaris canonical patterns.

**Failure mode caught:** Custom admin UI invented when Polaris components exist; merchant confusion and app-store rejection risk.

---

## feature_conversion_check(feature)

**Signature:** `feature_conversion_check(feature) → {named_metric: string | null, instrumentation_planned: bool, estimated_lift: float | null}`

**Pole:** Conversion-Pole.

**Returns:** verdict on whether feature has a named conversion metric + instrumentation plan + lift estimate.

**Failure mode caught:** Feature-bloat without metric attachment.

**Rule:** if `named_metric == null`, halt and ask. No-metric features get cut.

---

## app_review_checklist(app)

**Signature:** `app_review_checklist(app) → {pass: int, fail: int, gaps: [{requirement, status, fix}]}`

**Pole:** Polish-Pole.

**Returns:** app-store submission readiness verdict.

**Checklist includes:**
- GDPR webhooks (customer/data/redact, customer/redact, shop/redact)
- App listing copy (clear value prop, no superlatives, screenshots accurate)
- Embedded admin compliance (App Bridge, Polaris)
- Billing API correctness (recurring vs usage)
- OAuth scope minimization (request only what you use)
- App icon + screenshots specs

**Failure mode caught:** 30%+ first-submission rejection rate.

---

## mobile_first_check(layout)

**Signature:** `mobile_first_check(layout) → {mobile_pass: bool, breakpoint_issues: string[]}`

**Pole:** Polish-Pole.

**Returns:** mobile-render verdict.

**Failure mode caught:** Admin UI built desktop-first; 70%+ of merchants open admin on mobile.

---

## app_extension_type_select(use_case)

**Signature:** `app_extension_type_select(use_case) → {extension_type: theme_app_extension | admin_ui_extension | post_purchase | checkout_ui_extension | function | discount, rationale: string}`

**Pole:** Cross-pole.

**Returns:** correct Shopify extension type for the use case.

**Failure mode caught:** Wrong extension type chosen — e.g., building a theme app extension when checkout extensibility is required.

---

## hydrogen_vs_liquid_decision(merchant)

**Signature:** `hydrogen_vs_liquid_decision(merchant) → {recommendation: hydrogen | liquid_theme | hybrid, rationale: string}`

**Pole:** Speed-Pole + Conversion-Pole.

**Returns:** architectural recommendation.

**Rules:**
- Standard / Basic plan + simple catalog → Liquid theme (Dawn/Sense fork).
- Plus + complex catalog + custom checkout → Hydrogen / Oxygen.
- Hybrid: Hydrogen storefront + Liquid admin extensions.

---

## merchant_tier_check(plan)

**Signature:** `merchant_tier_check(plan) → {plan: basic|standard|advanced|plus, available_features: string[], blocked_features: string[]}`

**Pole:** Cross-pole (gates feasibility).

**Returns:** what the merchant's plan supports.

**Failure mode caught:** Building a custom checkout UI extension for a non-Plus merchant.

---

## funnel_measurement(merchant)

**Signature:** `funnel_measurement(merchant) → {steps: [{name, rate}], leakiest_step: string}`

**Pole:** Conversion-Pole.

**Returns:** funnel rates per step + leakiest step diagnosis.

**Standard funnel:** session → product view → ATC → checkout-start → completion → repeat-purchase-30d.

---

## metric_instrumentation_audit(feature)

**Signature:** `metric_instrumentation_audit(feature) → {events_defined: bool, events_firing: bool, event_names: string[]}`

**Pole:** Conversion-Pole.

**Returns:** verdict on whether the feature ships with working analytics events.

**Failure mode caught:** Features that ship without measurement; cannot validate the conversion claim.

---

## single_sprint_check(scope)

**Signature:** `single_sprint_check(scope) → {feasible: bool, estimated_hours: int, cut_to_fit: string[]}`

**Pole:** Speed-Pole.

**Returns:** whether the scope ships in one sprint + what to cut if not.

---

## empty_state_audit(ui)

**Signature:** `empty_state_audit(ui) → {empty_states_covered: bool, missing_states: string[]}`

**Pole:** Polish-Pole.

**Returns:** verdict on whether every screen handles zero-state.

**Failure mode caught:** App opens to blank screen with no guidance — instant uninstall risk.

---

## premature_abstraction_audit(code)

**Signature:** `premature_abstraction_audit(code) → {factory_patterns: int, justified: bool, simplification_proposed: string | null}`

**Pole:** Speed-Pole.

**Returns:** verdict on whether abstractions earn their place.

**Rule:** factory patterns only after the third merchant asks for the same variation.

---

## Cross-references

- Bench: [`_bench.md`](_bench.md)
- Attribution: [`frameworks_attribution.md`](frameworks_attribution.md)
- Master skill: `../SKILL.md`
