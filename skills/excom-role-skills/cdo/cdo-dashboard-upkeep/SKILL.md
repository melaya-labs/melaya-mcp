---
name: cdo-dashboard-upkeep
description: Keeps dashboards and report sheets true. It checks every tile's definition, source, cohort, window and refresh against the definitions note, re-reads a tile per dashboard at the source, removes dead and duplicate tiles, and keeps one outcome view current. It never uses sample data. Use when the monthly check is due, after a definition change or a tracking release, when a dashboard disagrees with a brief, or when the CEO asks for a new view.
version: 2.0.0
---

# Dashboard upkeep

A dashboard promises that every tile shows the canonical number, fresh, from the right source. This skill keeps that promise and removes tiles nobody uses.

## Look up first

- The definitions note: `excom_knowledge_search` "metrics definitions".
- The dashboards in use and their owners. If there is no list, build one in step 1 and propose it as a note.
- The outcomes (in your context): one view must show all of them.

## Steps

1. Take inventory:
   - PostHog, if granted: `posthog_list_dashboards`, `posthog_list_insights`.
   - GA4 metadata: `ga4_get_metadata`.
   - Report sheets: `sheets_list_tabs`, `sheets_read_range`.
   - Usage: ask each role which dashboard they use, and for which decision (`excom_send_handoff`, kind question).
2. Write down each dashboard's purpose: audience, the decision it serves, two to four headline metrics, its dimensions, and its refresh cadence.
3. Check every tile:
   - Its definition matches the note.
   - Its source is the authoritative one.
   - The cohort, exclusions, window and time zone are shown.
   - Its last refresh time is visible.
   Re-read one tile per dashboard at the source this turn (`posthog_get_insight`, `ga4_run_report`, `stripe_list_subscriptions`).
4. Keep one outcome view current: each outcome with baseline, today, expected today, target and status, matching the CEO's goal tracker for the same window.
5. Find dead and duplicate tiles: tiles nobody uses, tiles that duplicate another under a different definition, and tiles reading zero because an event was renamed. Propose a removal or a fix for each.
6. New or rebuilt views: two to four headline tiles first, then one to three trend charts, then a detail table, with filters for product and window. Never fill a tile with sample or invented data. An unmeasured metric shows "not measured".
7. Draft the changes with `excom_save_draft`. Mark known breaks (a deploy, a tracking change) as annotations (`posthog_create_annotation` or `ga4_manage_annotation`). Annotations are record writes and ask. Record the tiles checked and the mismatches with `excom_record_measurement`.

## Output

```text
Dashboard upkeep <date>
| Dashboard | Owner role | Decision served | Tiles | Mismatches | Dead | Last refresh | Action |
Mismatches: tile | shows | canonical (source, time) | cause | fix
Outcome view: present and matching (yes/no)
Proposed changes and annotations (record writes)
```

## Approvals

- Creating, editing or deleting dashboards, insights, sheets, annotations or analytics settings is a record write or a delete, and asks.
- Sharing a dashboard outside the team is a send, and asks.

## Example

Acme's "Weekly growth" dashboard shows 260 signups. The definitions note, read on the first-party source, gives 214. The tile counts the ad platform's sign-up conversions. Fix: switch the tile to first-party registrations, annotate the change, and tell the CMO.

Adapted from anthropics/knowledge-work-plugins (data/skills/build-dashboard/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
