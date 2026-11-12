---
name: cdo-metric-definitions
description: Keeps the team's metrics definitions note current, so each KPI has one definition, one source of truth, one owner and a cohort rule. It checks quoted numbers against the note, reconciles two numbers reported for one metric, and drafts definitions that are new or missing. Use when a KPI is quoted, disputed or added, when two roles report different numbers, when an outcome counts affiliates, partners or customers, or when someone asks "how do we count this".
version: 2.0.0
---

# Metric definitions, one source per KPI

Two numbers for one metric is the most common data failure. This skill keeps one definitions note that every role reads instead of restating, starting with the metrics behind the team's outcomes.

## Look up first

- The definitions note: `excom_knowledge_search` "metrics definitions", then `excom_knowledge_read`. If it does not exist, draft it with `excom_save_draft`, starting from the outcomes in your context, and propose it to the owner with `excom_propose_task` (needs_decision).
- The decision each metric drives. A metric that drives no decision needs a note, not a definition.

## Steps

1. For every outcome in your context, make sure the note defines its metric: name, formula, source of truth (tool or table), cohort rule (registered in the window or all users), exclusions (staff and test accounts), consent dependency, retention, owner.
2. Apply the source-of-truth rule: first-party data wins for registrations, activation and purchases (server events, billing). A vendor wins only for its own surface (impressions, crawl, ad spend). Ad-platform conversion counters are context, never registrations.
3. If an outcome counts affiliates or partners and the note lacks a definition, propose the defaults in references/worked-examples.md to the owner: an active affiliate has at least one referred signup; a signed partner has a signed agreement filed in its partner folder.
4. When a number is quoted or disputed, read both sources this turn (for example `stripe_list_subscriptions` against the first-party funnel, or `ga4_run_report` against registrations). Name the gap (exclusions, cohort, consent, blockers, time zone) and which source is authoritative.
5. For a new or changed definition, show before and after on one real window. Check the event rules: server-authoritative or client-emitted, and allowed fields only.
6. Tell every role that uses the metric with `excom_send_handoff` (kind question). Ask them to link the note rather than restate it.
7. Save the proposal with `excom_save_draft`. Record the agreed definition with `excom_record_fact`. Send event or code changes to engineering with `excom_propose_task`.

## Output

```text
KPI check: <metric> as quoted (value, window, source)
Canonical: definition | source | cohort | exclusions | owner | match
Gap: source A | source B | cause | authoritative
Proposal: name | formula | source | cohort | exclusions | consent | retention | owner | before/after on <window>
Roles notified
```

## Approvals

- Writing the definitions note, a glossary or a dictionary sheet is a record write, and asks.
- Creating or changing a key event or custom definition in analytics (`ga4_create_key_event`, `ga4_update_key_event`, `ga4_create_custom_dimension`) is a record write, and asks.
- Publishing a metric externally needs the owner. User counts and client shares are never published.

## Example

The CEO's brief says "180 affiliates". Affonso shows 180 enrolled, but only 41 have a referred signup. Under the team's definition, the outcome counts 41. The brief is corrected, and the CRO links the definitions note in their pipeline report.

## References

- references/worked-examples.md: two complete definitions (active affiliate, signed partner) showing what a good definition contains. It loads with `excom_skill_load`.

Adapted from alirezarezvani/claude-skills (c-level-advisor/skills/chief-data-officer-advisor/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
