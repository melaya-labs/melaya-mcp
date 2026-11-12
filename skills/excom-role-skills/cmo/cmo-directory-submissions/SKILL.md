---
name: cmo-directory-submissions
description: Lists your products on software review sites, AI tool and agent directories, MCP registries and launch sites from one approved fact sheet, free listings first, and keeps an honest record of every attempt. Use when a product launches or changes, when a presence check shows you missing from a directory, when listings are stale, or when someone asks to "get us listed", "submit to directories" or "add us to MCP registries".
version: 2.0.0
---
# Directory and registry submissions

Listings feed AI answers for "X alternatives" queries and give buyers a neutral place to find you. One approved fact sheet keeps every listing consistent; free listings come first and paid ones always ask.

## Look up first

- Products, positioning and public prices: `excom_knowledge_search` "products", "positioning", "pricing and plans", then `excom_knowledge_read`; confirm prices on the live pricing page with `web_fetch`.
- The contact address and brand assets allowed on public listings: search "brand", "contact". Missing: ask the owner with `excom_propose_task` (needs decision); never use a personal email, phone or home address.
- Existing listings and any directory catalogue the team keeps (for example a Backlinks tab with availability and ratings): search "backlinks", "directory submissions". Missing: start the log from references/directory-waves.md.
- Browser automation for forms: check your grants. Missing: `excom_request_setup` for the browser connection.

## Steps

1. Build the fact sheet per product with references/fact-sheet-template.md, run it through skill cmo-unslop-copy, save with `excom_save_draft` and get it approved once.
2. Check presence before submitting: `backlink_discover_candidates` for listing URLs, and `backlink_fetch_page` for pages a plain fetch cannot read. An unknown result is never treated as "not listed", because a blocked fetch is not evidence of absence.
3. Order the work by the waves in references/directory-waves.md. Skip targets that are paid-only, closed or down unless step 6 applies.
4. Submit free listings through the paired browser or the browser tools in your grants. Each submission is send: one approval card showing the target and the exact copy. Never fill hidden honeypot fields; never pass a paywall by paying.
5. Read verification emails on the shared inbox your grants allow (for example `zoho_email_list` and `zoho_email_get_content`, or `gmail_search`); following the verification link is part of the approved submission.
6. Paid listings and fast tracks are never default. Write a proposal with the price and what it buys, send it to the CFO with `excom_send_handoff` (kind request), and let the owner approve the spend.
7. Record each attempt with `backlink_report`: submitted, live with the listing URL, or failed with the reason.
8. A directory asking about commercial terms goes to the CRO; a listing error confusing users goes to the CXO.
9. Monthly, count live listings and record with `excom_record_measurement`.

## Output

```text
Fact sheet (approved draft) per product
Submission log: | directory | wave | product | free/paid | status | listing URL | date | note |
Paid proposals: | directory | price | what it buys | recommendation |
```

## Approvals

- Every submission and form sent: send, one card each.
- Every paid listing, fast track or sponsored slot: spend, with the exact cost, owner approves, CFO informed.
- Pull requests to public curated lists go through whoever holds the code account.

## Example

Acme launches an MCP server. Fact sheet approved (100-character registry description included). Wave 2 first: three free MCP registries submitted, one live the same day, one pending review, one paid-only and logged as skipped with a proposal to the CFO.

## References

- references/fact-sheet-template.md: the fields every directory asks for. Read at step 1.
- references/directory-waves.md: the order of directory types and the operating rules. Read at step 3.
Both load with `excom_skill_load` or by paging.

Adapted from Illyism/seo-skills (seo/directory-submissions/SKILL.md), MIT. Modified: rewritten generic for EXCOM.
