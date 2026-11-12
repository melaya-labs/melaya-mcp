---
name: clo-partner-affiliate-agreements
description: Takes a partner or affiliate from "yes" to a SIGNED agreement filed in the partner's folder: checks the ask against the published programme terms, screens the counterparty, prepares the e-signature envelope from the agreement template, tracks signatures and files the executed copy. Use when a partner or affiliate is ready to sign, asks for different commission or discount terms, when envelopes are waiting for signature, or when counting signed partners.
version: 2.0.0
---
# Partner and affiliate agreement terms

Gets agreements signed without inventing terms. A partner counts as SIGNED only when its signed agreement is filed in the partner's folder under the team's partner agreements folder.

## Look up first

- The programme terms and tiers the team may offer without asking: `excom_knowledge_search` "partner programme terms", "affiliate programme terms". Quote them exactly; anything else goes to the owner. If missing, ask with `excom_propose_task` (needs_decision true).
- The agreement template and where it lives: `excom_knowledge_search` "partner agreement template". If your e-signature platform is DocuSign, confirm with `docusign_list_templates` and `docusign_get_template`.
- The partner agreements folder location: `excom_knowledge_search` "partner agreements folder". If missing, ask the owner; never guess a folder.
- The partner goal (in context) and the partner launch runbook: `excom_knowledge_search` "partner launch runbook".

## Steps

1. Compare the ask with the published tiers: standard (tier name) or non-standard (what differs, why, revenue effect estimated with the CFO). Non-standard goes to the owner.
2. Screen the counterparty before any agreement or payout, using `references/pre-signature-and-screening.md`: `sanctions_screen`, `gleif_get_lei` or a national registry, `vies_check_vat`, `rdap_domain`. A possible match is a signal for the owner and counsel, never a conclusion. Record date, tools and verdict; copy no personal data.
3. Check status: `docusign_list_envelopes`, `docusign_get_envelope_status`, partner mail with `zoho_email_search`. Report gaps (no NDA, no DPA where the partner will process customer data).
4. Fill the template fields (tier, legal names, effective date) and run the pre-signature checklist.
5. Create the draft envelope with `docusign_envelope_create_draft` (record write). Sending with `docusign_send_envelope_from_template` or `docusign_envelope_send` has legal effect: the owner approves every time.
6. Track weekly with `docusign_get_awaiting_signature_report` and monthly with `docusign_get_contracts_expiring`. Reminders with `docusign_notify_pending_signers` are a send.
7. After signature, file it: `docusign_download_document`, then find or create the partner's folder under the partner agreements folder with `drive_search` and `drive_create_folder`, and `drive_upload` the executed copy (record writes). Only then count the partner as signed.
8. Hand platform set-up (tracking link, group) to the CRO or partnerships role and any public page or logo use to the CMO with `excom_send_handoff` (kind request). Record signed partners (filed agreements) with `excom_record_measurement`.

## Output

```text
Agreement pack: <partner>  type <partner/affiliate/reseller>  DRAFT
Terms: standard <tier> | non-standard <difference>, needs owner
Screening: tool | date | result (clear / possible match for owner)
Status: NDA | agreement | DPA if processing | envelope | state | sent
Pre-signature checklist: pass / issues
Filed: folder path | file name | filed date   (signed = filed)
```

## Approvals

- Sending envelopes, reminders or messages: send, the owner.
- Signing, accepting or changing terms: legal or people, the owner.
- Non-standard commercial terms: the owner.
- Voiding envelopes or deleting templates: delete.
- Commissions and payouts: spend, the CFO prepares.

## Example

Acme Integrations accepts the standard partner tier. Screening is clear, the template is filled, the owner approves sending. Signed four days later; the executed PDF is uploaded to Partner agreements / Acme Integrations, and the signed-partner count moves from 6 to 7.

## References

- `references/pre-signature-and-screening.md`: pre-signature checklist, screening layers and the filing convention; read at steps 2, 4 and 7.

Adapted from anthropics/knowledge-work-plugins (legal/skills/signature-request, legal/skills/vendor-check), Apache-2.0, and Maxbase91/procurement-skills (supplier-truthcheck), MIT, Copyright (c) 2026 Maximilian Ziermann. Modified: rewritten generic for EXCOM.
