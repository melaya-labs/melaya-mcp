---
name: cdo-data-quality-checks
description: Checks numbers before they leave the data role: population and definitions, re-reads at the source, join explosion, partial periods, denominator shifts, averages of averages, time zones, retention bounds and instrumentation zeros. It ends in one verdict: ready, share with caveats, or needs revision. Use when a weekly brief, monthly report, investor update or partner data reply is about to go out, when a number jumps unexpectedly, or after a deploy that touched tracking or billing.
version: 2.0.0
---

# Data quality checks

A wrong number in a brief sends the company after the wrong goal. The usual causes are known, and a short pass catches them.

## Look up first

- The definitions note: `excom_knowledge_search` "metrics definitions" (cohort rules, exclusions, sources of truth).
- Each system's time zone and the raw event retention: the same note, or "systems of record". If unknown, ask the owner which zone reports use, and state your assumption.
- The artefact to check, with its sources and windows (from the requesting role).

## Steps

1. Question and population. Does the number answer the question asked? Is the population right: external accounts only, the stated cohort, the stated product?
2. Definitions. Each metric matches the note, or the difference is stated. Vendor counters are never presented as registrations, activations or purchases.
3. Re-read two or three figures at the source this turn (for example `stripe_list_subscriptions`, `affonso_get_affiliate_analytics`, `ga4_run_report`, `posthog_query_trends`). Mark any figure you cannot re-read as unverified.
4. Run the pitfalls in references/pitfalls.md: join explosion, survivorship, incomplete periods, denominator shift, average of averages, time zones, retention bounds, selection bias.
5. Instrumentation sanity. A zero funnel while the ground-truth table has rows is an instrumentation error. A sudden large jump after a release is more often a logging bug than a result: check for duplicated events and bots first.
6. Reasonableness. Any change over 30 percent against last week or last month needs a named cause. Product totals add up to the company total.
7. Verdict: ready to share, share with caveats (list them), or needs revision (fixes by priority).
8. Save with `excom_save_draft` and return it to the requester with `excom_send_handoff` (kind request). Record the issue count with `excom_record_measurement`. Repeated issues become an engineering task (`excom_propose_task`).

## Output

```text
Data quality report: <artefact>, checked <time>
Verdict: ready | share with caveats | needs revision
Population and definitions: findings
Spot checks: figure | source re-read | match
Pitfalls: type | where | effect | fix
Caveats readers must see
```

## Approvals

- Correcting data at the source (analytics settings, affiliate records, billing metadata, event code) is a record write or an engineering change, and asks.
- Deleting or archiving data always asks, and this role never proposes it.
- The artefact's owner asks for its send.

## Example

Acme's monthly report says activation rose 35 percent. The re-read shows the window changed from 28 to 31 days and the staff exclusion was dropped. Corrected on the same 28-day window with staff excluded: plus 6 percent. Verdict: needs revision.

## References

- references/pitfalls.md: each pitfall with how to detect and prevent it. It loads with `excom_skill_load`.

Adapted from anthropics/knowledge-work-plugins (data/skills/validate-data/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
