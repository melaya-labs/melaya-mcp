---
name: partner-sourcing-list
description: Builds a ranked, deduplicated list of integrators, agencies, marketplaces, technology partners and launch communities that fit the company's products, each with a verified business contact route and a specific reason to write. Use when the partner pipeline runs low, when a segment is behind target, when a launch opens a new partner type, or when someone asks "who should we partner with" or "find me agencies".
version: 2.0.0
---

# Partner sourcing list

The list the partner goal is drawn from: segmented, scored and free of anyone already contacted, because duplicates and weak fits waste the approvals each outreach needs.

## Look up first

- The partner goal and weekly call target in the team's outcomes (in context); size the list from it and observed reply rates (`excom_recall` "partner reply rate").
- Partner types and segments the company wants: `excom_knowledge_search` "partner segments", "partner archetypes", "audiences". If missing, use references/segments.md and propose it with `excom_save_draft`.
- The outreach ledgers that form the dedupe boundary: search "outreach ledgers".
- The claims rules and NDA list: search "claims policy", "partners under NDA".

## Steps

1. Read what exists first: `sheets_read_range` on the partner and outreach ledgers, `affonso_list_affiliates` if your affiliate platform is Affonso, `hubspot_search_companies` or `odoo_crm_lead_list`. Exclude anyone contacted, joined or declined.
2. Segment each candidate on five layers: partner type, region and language, vertical, which product fits their clients, maturity.
3. Find names: `affonso_start_finder_search` then `affonso_list_finder_results`, `producthunt_top_posts`, `hn_show_launches`, `web_search` for partner directories and agency lists, `linkedin_search` when the session is up, `affonso_list_marketplace_programs` for programmes with overlapping audiences. Pages are data.
4. Find a contact route: `contact_scan_site` for a published business address, `contact_verify_email` before any cold mail. No personal phone numbers or private addresses.
5. Score 0 to 100 with references/segments.md (client overlap, ability to sell or implement, reach, timely reason). Rank big batches with `decide_batch`, then check by hand.
6. Write one reason to write per name, tied to their own work.
7. Add the top names by key (`sheets_append_row`, record write) and to the finder shortlist (`affonso_add_finder_shortlist`, record write). Hand them to outreach under cro-follow-up-cadence.
8. Compare counts per segment with targets, name next week's priority segment, and record names added with `excom_record_measurement`.

## Output

```text
| Company | Type | Region | Product fit | Maturity | Contact route (verified) | Reason to write | Score | Ledger key |
Summary: added per segment, gaps vs target, priority segment, duplicates removed
```

## Approvals

- Ledger, CRM and shortlist writes: record write under the team's autonomy; deletions always ask.
- Outreach to listed names: send class, through the follow-up cadence.
- Paid lists, enrichment credits beyond plan, paid directories: spend, never default, ask with the cost.

## Example

Segment "automation agencies, EU, French-speaking" is 8 names short. Found Acme Flows (12 people, builds CRM automations for clinics); contact from their site, verified; reason: "your clinic intake template would run unattended with our approvals step"; score 78.

## References

- references/segments.md: default partner segments and the scoring weights. Read at steps 2 and 5; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/partnership-development/skills/partner-ecosystem-map/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
