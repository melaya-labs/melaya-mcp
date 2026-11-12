---
name: cpo-roadmap-from-evidence
description: Ranks what to build next from weighted evidence (product usage, support threads, bug reports, sales and partner asks) into a top five of problems, each with its sources, effort, riskiest assumption and cheapest test. Use when planning the roadmap, when someone pushes a feature request, when the same complaint shows up in several places, or when asked "what should we build next" or "is this worth building".
version: 2.0.0
---
# Roadmap from weighted evidence

Turn scattered asks into a ranked list of problems worth solving, each backed by evidence, so the roadmap moves the team's outcomes instead of the loudest request.

## Look up first

- The team's outcomes and your charter objectives (in your context). If none is measurable, ask the owner which outcome the roadmap serves with `excom_propose_task` (needs decision).
- Earlier rankings and decisions: `excom_recall` "roadmap", so you compare instead of restarting.
- The product list and metric definitions: `excom_knowledge_search` "products", "metrics definitions", "activation events". If missing, draft the note with `excom_save_draft` and propose it.
- Which apps you are granted (analytics, support, CRM, mail). Missing ones: `excom_request_setup` and mark that source "not measured".

## Steps

1. Usage: `melaya_eval_report` for run acceptance per product, `posthog_query_trends` or `ga4_run_report` for activation events.
2. Support and community: `intercom_search_conversations`, `zoho_email_search` or `gmail_list_threads` with a label query, `reddit_search_posts`, `producthunt_get_post_comments`. Bug reports: ask the CQO with `excom_send_handoff` (kind question) for open reports and their states.
3. Sales and partners: `hubspot_search_deals` and `hubspot_get_deal` for deals that name a missing capability; ask the CRO for lost-deal reasons. Record the problem behind each ask, never the customer's proposed solution, because customers describe symptoms well and solutions badly.
4. Group items into problem themes, one row per problem, duplicates merged across sources.
5. Weight each theme with the scoring table in references/scoring.md: source weight times reach times outcome fit.
6. Ask the CTO for effort and risk (S, M, L; migration, release, store submission) with `excom_send_handoff` (kind question).
7. Rank the top five. For each: problem, evidence with sources, two alternative solutions, riskiest assumption, cheapest test.
8. Save the ranking as a draft; after a human approves it, record it with `excom_publish_decision` and open tasks with `excom_propose_task`.

## Output

```text
Roadmap evidence <date>: outcome served, window, sources read (tool, count)
| rank | problem | evidence (source x weight) | reach | outcome fit | score | effort | riskiest assumption | cheapest test |
Deprioritized: theme, why
Not measured: missing data and who could unlock it
```

Saved with `excom_save_draft`, plus up to five tasks.

## Approvals

- Publishing the ranking as a decision (the owner approves on the card).
- Any reply to a customer, partner or prospect is send class; the support or sales executive sends it.
- Paid research or survey tools: never default, ask first with the cost.
- Pricing and plan limits are the CEO's call with the CRO and CFO; prepare options only.

## Example

Acme's goal is N paying customers this quarter. Three sources (eval failures on a connector, 14 support threads, two lost deals) point at "setup of connector X fails silently". It ranks first: weight 3+1+3, reach 40 accounts, direct outcome fit. Cheapest test: a clearer error and a doc fix before a rebuild.

## References

- references/scoring.md: the source weights, reach and outcome-fit multipliers and the opportunity score. Read at step 5 (`excom_skill_load` with the section, or page through).

Adapted from phuryn/pm-skills (pm-product-discovery/skills/analyze-feature-requests and prioritize-features), MIT. Modified: rewritten generic for EXCOM.
