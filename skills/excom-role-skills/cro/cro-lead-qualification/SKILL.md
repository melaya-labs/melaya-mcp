---
name: cro-lead-qualification
description: Scores new leads on fit and intent, matches each to the one product it needs, and routes it to a reply, a call, nurture or recycle. Use when signups, inbound emails, bookings, partner referrals or outreach replies pile up, when the pipeline review needs qualified counts, when someone asks "which leads should we work first", or before spending approvals on outreach.
version: 2.0.0
---

# Lead qualification by fit and intent

Ranks leads so scarce approvals and founder time go to the ones most likely to pay, with a written reason per score.

## Look up first

- The team's outcomes and your charter objectives (in context) for the customer and partner goals the score serves.
- The qualified-lead definition: `excom_knowledge_search` "qualified lead definition" or "metrics definitions". If missing, use the default below and ask the owner to confirm it with `excom_propose_task` (needs decision true).
- Products, who each fits, and the priority audiences: search "products" and "positioning" and "audiences".
- Plans: search "pricing and plans".

## Steps

1. Read the leads. Mail: `gmail_search`, `gmail_get_thread`, `zoho_email_search`, `zoho_email_get_content`. CRM: `hubspot_search_contacts`, `hubspot_list_deals`, `odoo_crm_lead_list`. Ledgers: `sheets_read_range`. Bookings: `calendly_list_events`. A missing app means `excom_request_setup` with its service id, never a guess.
2. Read first-party intent for leads with an account: usage and subscription through `melaya_tools`, checkout starts with `stripe_search_customers` and `stripe_list_checkout_sessions`. No read means intent is "unknown", because a lead's own claim is not evidence.
3. Score four dimensions 0 to 25 each with the table in references/scoring.md: firmographics, intent, timing, solution match. Exactly one product per lead.
4. Tier: 80 and above hot, 60 to 79 warm, 40 to 59 nurture, below 40 recycle. For big batches rank with `decide_batch`, then check the top and bottom five by hand.
5. Route: hot to a reply draft or call prep today; warm to the follow-up cadence; nurture to the CXO onboarding sequence (`excom_send_handoff` kind request); partner leads to the partnerships executive; recycle stays logged with a reason.
6. Write by key to the CRM or ledger (`hubspot_update_contact`, `odoo_crm_lead_update`, `sheets_update_by_header`): record write. Never by row number.
7. Record hot plus warm by product with `excom_record_measurement`.

## Output

```text
| Lead | Source | Product | F | I | T | S | Total | Tier | Two signals that decided it | Next action | Owner |
Summary: count per tier, per product, leads with unknown intent
```

Saved with `excom_save_draft`; one `excom_propose_task` per hot lead.

## Approvals

- Any send to a lead: send class, card by card unless a rule matches.
- CRM and ledger writes under the team's autonomy; deleting leads always asks.
- Any price, discount or term mentioned to a lead: the owner decides.

## Example

Acme Ops (12 people) started a checkout yesterday and ran two successful pipelines: F 18, I 25, T 15, S 22, total 80, hot, product "workflow builder", next action "reply today with the plan that fits".

## References

- references/scoring.md: the point table for each dimension and the default qualified-lead definition. Read it before scoring; it loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/sales-prospecting/skills/lead-qualification/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
