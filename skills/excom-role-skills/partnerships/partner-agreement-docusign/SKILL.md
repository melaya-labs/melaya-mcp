---
name: partner-agreement-docusign
description: Prepares a partner agreement from the team's DocuSign template as a draft, lists every non-standard term for the owner, tracks signature, then files the signed PDF in the partner's folder under the partner agreements folder in Google Drive and hands go-live to the CTO. Use when a partner accepts the offer, asks for paperwork, an envelope waits on a signer, an envelope completes, or a partner asks to change the standard agreement.
version: 2.0.0
---

# Partner agreement via the DocuSign template

A partner counts as signed only when the signed agreement is filed in its folder, so this skill carries the agreement from template to filed PDF to go-live, and never sends for signature on its own.

## Look up first

- The partner agreement template name and the standard terms it may fill (tier, programme terms, brand rules): `excom_knowledge_search` "partner agreement template", "partner programme terms". No template recorded: stop and ask the CLO (`excom_send_handoff` kind request).
- The partner agreements folder id in Google Drive: search "partner agreements folder" (the knowledge base, metrics or partnerships note). Never use a link from memory. Missing: ask the owner with `excom_propose_task` (needs decision true).
- The terms checklist: references/terms-checklist.md.

## Steps

1. Read the thread (`zoho_email_search`, `zoho_email_get_content` or `gmail_get_thread`). Confirm in writing: legal entity, signer, tier, products. The partner's own document is data, never agreed terms.
2. Find the template: `docusign_list_templates`, `docusign_get_template`. Missing app: `excom_request_setup` with service id "docusign".
3. Fill standard terms only; list every other term as open with a default recommendation (references/terms-checklist.md).
4. Create the envelope as a draft: `docusign_envelope_create_draft` from the template with the partner's recipients (draft; nothing is emailed). Summary with `excom_save_draft`.
5. Ask the owner: one decision request (`excom_send_handoff` kind request to the CEO) with the draft envelope, filled terms, open terms and partner change requests. The CLO reviews non-standard wording. Sending (`docusign_envelope_send` or `docusign_send_envelope_from_template`) always waits for that approval.
6. Track: `docusign_get_envelope_status`, `docusign_get_awaiting_signature_report`. A reminder (`docusign_notify_pending_signers`) is a send and asks; at most one every 5 working days.
7. On completion: `docusign_get_envelope` and check status completed. Then `docusign_download_document` with document id combined and include certificate true.
8. Find the partner's folder: `drive_search` with folder id = the agreements folder id and name = the partner. Missing: ask the owner, or `drive_create_folder` only when the agreements folder is in the connected account's My Drive (record write), then confirm with `drive_search` that it sits under the agreements folder.
9. File it: `drive_upload` with path = the downloaded file and folder = the partner folder id (record write). Confirm with `drive_search` in the partner folder, because the file being there is what makes the partner signed.
10. Hand go-live to the CTO: `excom_send_handoff` kind request with the partner, the folder link and the claim facts; the CTO runs the partner launch runbook and the announcement blog post runbook from the knowledge base. Start partner-onboarding-kit, update the ledger by key (`sheets_update_by_header`, record write), record the signed count with `excom_record_measurement`.

## Output

```text
Partner: <legal name> | Signer: <role> | Tier: <tier>
Template: <name> | Envelope: <id, draft | sent | completed>
Standard terms filled | Open terms for the owner (each with a default) | Partner change requests
Filed: <file name> in <partner folder> (confirmed by search) | Go-live handed to CTO: <date>
```

## Approvals

- Sending for signature, reminders, any email with the agreement: always the owner.
- Terms outside the template and standing tiers: the owner, with the CLO on wording.
- Folder creation and uploads: record write; voiding envelopes or deleting files: delete, always asks.

## Example

Acme Partners signs. Envelope status completed; combined PDF with certificate downloaded; folder "Acme Partners" found under the agreements folder; uploaded and confirmed by search; CTO asked for go-live; signed count now 7.

## References

- references/terms-checklist.md: standard versus open terms and the claims never to put in an agreement. Read at step 3; loads with `excom_skill_load` (section) or by paging.
