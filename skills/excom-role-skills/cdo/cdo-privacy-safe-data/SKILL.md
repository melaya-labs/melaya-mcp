---
name: cdo-privacy-safe-data
description: Keeps data handling privacy-safe whenever data leaves its system. It classifies fields as personal, pseudonymous or aggregate, minimises, checks consent and purpose, vets the destination and sets retention. It also supports data subject requests by listing where a person's data sits, and checks new events against the privacy rules. Use when preparing a brief, export, sheet, vendor upload or partner reply, when a new event or field is proposed, or when a deletion or access request arrives.
version: 2.0.0
---

# Privacy-safe data handling

Growth work touches personal data: customer lists, affiliate payouts, funnel events, partner reports. This skill keeps every share and export safe, so pushing the outcomes never creates a breach or a consent problem.

## Look up first

- The privacy rules and event rules: `excom_knowledge_search` "privacy rules" or "data handling". If missing, use the defaults below and propose them as a note to the owner and the legal role.
- Consent settings and open privacy decisions: `excom_knowledge_search` "risks and open questions".
- For a data subject request: the request from the legal role, which owns it and its deadline.

## Steps

1. Classify each field:
   - Personal: name, email, IP, payment details, device labels, free text, URLs that can carry personal data.
   - Pseudonymous: user id.
   - Aggregate.
   Free text and URLs count as personal by default.
2. Minimise. Use aggregates where they answer the question. Mask names and emails in briefs. Never put personal data in `excom_record_measurement` or `excom_record_fact`. Merge or suppress groups smaller than five.
3. Consent and purpose:
   - Client-side tracking is consent-gated; server events define conversions.
   - Never reuse data for a purpose people were not told about, for example training a model on customer content.
4. Check the destination:
   - Vendors and observability tools receive metadata only: no arguments, results, names or emails.
   - Partners and affiliates receive only their own aggregates, with written approval for any public use.
   - Public corpora or help content never receive client material or internal runbooks.
5. Retention: state how long the copy lives and where. Give shared sheets an end date. Prefer anonymising over keeping raw rows.
6. Data subject request:
   - List the internal stores keyed by the user id (event tables, milestone tables, usage meters).
   - Note what does not cascade on account deletion, for example funnel history.
   - List the connected vendors that may hold the person's data (billing, affiliate platform, mail, analytics).
   Hand the list to the legal role (`excom_send_handoff`, kind request). A GA4 deletion is `ga4_submit_user_deletion`, which always asks.
7. New events or fields: allow flat enums and counts only. No typed text, URLs, selectors, page text, names, device labels or raw IPs. Send compliant specs to engineering (`excom_propose_task`).
8. Save the review with `excom_save_draft`. A leak or a credential you come across goes to the security role at once (`excom_send_handoff`, kind request), and is never quoted.

## Output

```text
Privacy check: <artefact or request>, <date>
Fields: field | class | kept / masked / dropped
Destination: recipient | allowed | approval needed
Consent and purpose: basis | issue
Retention: duration | location | end date
DSR: internal stores | vendors | non-cascading data | handed to legal on <date>
```

## Approvals

- Any deletion of personal data (`ga4_submit_user_deletion`, or deletes in any system) always asks. Internal deletions are executed by engineering after the owner approves.
- Exporting personal data to a vendor, partner or sheet is a send or record write. It asks, with the legal role consulted.
- Changing retention, redaction or consent settings (`ga4_update_data_retention`, `ga4_update_data_redaction`) is a record write, and asks.

## Example

The CRO wants a sheet of affiliate payouts with names and emails, to share with an agency. Check: the agency needs totals per affiliate code only. Output: an aggregate sheet keyed by code, with no emails, and an end date set for 30 days.

Adapted from TerminalSkills/skills (skills/gdpr-compliance/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
