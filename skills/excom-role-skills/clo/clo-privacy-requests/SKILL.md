---
name: clo-privacy-requests
description: Handles data subject requests (access, portability, correction, erasure, restriction, objection, consent withdrawal) on a dated clock and answers customer DPA, subprocessor and privacy questionnaire requests from the published privacy policy and DPA. Use when a person asks for their data or deletion, when a customer asks for a signed DPA, transfer mechanism or breach terms, or when an employee, contractor or affiliate asks about their own data.
version: 2.0.0
---
# Privacy and data-processing requests

Answers personal-data requests on time and on the record, and customer privacy questions from what the company actually publishes. A missed deadline is a regulatory breach; a slow DPA answer stalls a deal.

## Look up first

- The data subject rights procedure (deadline, identity checks, self-serve paths): `excom_knowledge_search` "data subject rights procedure", then `excom_knowledge_read`. If missing, use `references/rights-and-escalation.md` and propose saving it as the procedure with `excom_save_draft`.
- The published privacy policy, DPA, subprocessor list and retention schedule: `excom_knowledge_search` "privacy policy and DPA", "subprocessor list", "data retention".
- Which certifications and attestations the company actually holds: same sources. If not stated, claim none.
- The request itself: `zoho_email_search` or `gmail_search` (read).

## Steps

1. Record the receipt date with `excom_record_fact` and compute the due date from the procedure (under GDPR one month, extendable with notice inside the first month).
2. Classify: controller request (your own users and contacts) or processor request (a customer's end user; forward to the customer and do not answer directly unless instructed).
3. Self-serve rights: point the person to the account's privacy controls listed in the procedure. Draft the reply with `gmail_create_draft` or `zoho_email_save_draft`.
4. Assisted path: verify identity proportionately (collect no more than needed), log the request with `docs_create` (record write), locate the data stores with the CDO through `excom_send_handoff` (kind request), and propose the admin action with `excom_propose_task`. Admin actions are done by a human.
5. Check the escalation triggers in the reference; on any trigger, stop and ask the owner.
6. Customer DPA or questionnaire: answer only from published pages, each answer citing page and section, with honest status words (live, gap, target). Never claim a certification the sources do not show. A customer mark-up of the DPA goes through `clo-contract-review` (load with `excom_skill_load`).
7. Close after approval: log completion date, scope, exclusions and the notice sent. Record response time with `excom_record_measurement`.

## Output

```text
Privacy request: id  received <date>  due <date>  type  role (controller/processor)
Path: self-serve | assisted | forwarded to customer
Identity check: method, date (no document copies kept)
Actions: action | owner | approval | done date
Escalation: trigger / none | Reply draft
Questionnaire: item | answer | source page and section | status
```

## Approvals

- Replies to requesters or customers: send.
- Account freeze, deletion or export done for someone: an admin human (delete class when data is removed).
- Signing a DPA or accepting customer changes: legal or people, the owner with counsel.

## Example

A user of Acme writes "delete everything you have on me" on day 0. Controller request, self-serve erasure exists: the reply draft points to the account deletion control and explains what is kept for legal reasons (billing records). Due date recorded; closed on day 2 with the completion logged.

## References

- `references/rights-and-escalation.md`: rights matrix, escalation triggers and DPA checklist; read at steps 3 to 6.

Adapted from anthropics/knowledge-work-plugins (legal/skills/compliance-check, legal/skills/legal-response), Apache-2.0. Modified: rewritten generic for EXCOM.
