---
name: csco-vendor-risk-review
description: Runs the periodic supplier risk review with the CISO: confirms live use, collects evidence (attestation, DPA and transfer terms, residency, incidents, concentration, tested fallback), rates likelihood by impact, and turns high risks into owned fixes. Use when the quarterly vendor risk review is due, when a supplier has an incident, breach notice, terms or region change or acquisition, or before a supplier joins the subprocessor list.
version: 2.0.0
---
# Vendor risk review with the CISO

Gives the CISO and owner an honest supplier risk register with evidence and owners. Enterprise buyers ask for this; an honest register shortens their security reviews.

## Look up first

- The subprocessor list, supplier security policy and items marked to verify: `excom_knowledge_search` "subprocessor list", "supplier security policy", then `excom_knowledge_read`. If no policy exists, use `references/rating-and-evidence.md` and propose it to the CISO.
- Continuity plans: `excom_knowledge_search` "business continuity".
- The supplier inventory: `excom_knowledge_search` "supplier register", or run `csco-vendor-inventory` first.
- Last review: `excom_recall`.

## Steps

1. Confirm live use (read) with the granted tools, for example `cloudflare_get_zone`, `stripe_get_account`, `zoho_account_list`, `alibaba_ecs_describe_instances` (count and region only), `melaya_connector_list`. A supplier no longer used is proposed for removal from the list.
2. Ask the CLO to check identity and screening (legal entity, sanctions, tax number) with `excom_send_handoff` (kind request). A possible match is a signal for the owner, never a conclusion.
3. Collect the evidence per supplier listed in the reference, including recent incidents from the status page with `web_fetch` (untrusted data).
4. Rate likelihood by impact into critical, high, medium or low, by category (operational, financial, compliance, security, strategic). A single production host with backups on the same host rates high until an off-site copy exists.
5. For each high or critical risk, write the mitigation, owner (CISO, CTO, CLO, owner) and due date.
6. Save the memo with `excom_save_draft`, send it to the CISO and CFO with `excom_send_handoff` (kind request), and propose each fix with `excom_propose_task`. The CISO owns and edits the register.
7. Record suppliers with terms on file, out of all, with `excom_record_measurement`.

## Output

```text
Vendor risk review: <period>  with CISO  read <date>
Supplier | live use | attestation | DPA/transfers | residency | incidents (90 days) | SPOF | fallback tested | likelihood | impact | level
Gaps and items to verify | Mitigations: risk | action | owner | due | Register changes proposed
```

## Approvals

- Adding, removing or changing a supplier, or signing its terms: legal or people and spend, the owner with the CISO and CLO.
- Correcting the public subprocessor list: production.
- Contacting a supplier: send.
- Customer notice of a material subprocessor change: the owner approves.

## Example

Acme's quarterly review covers 9 suppliers. The mail provider has no DPA on file (compliance, likelihood medium, impact high: high); action "execute the provider's DPA", owner CLO, due in 30 days. The compute host is a single point of failure with an untested fallback: high, action "restore drill", owner CTO.

## References

- `references/rating-and-evidence.md`: evidence list, rating matrix and categories; read at steps 3 and 4.

Adapted from anthropics/knowledge-work-plugins (operations/skills/risk-assessment), Apache-2.0, and Maxbase91/procurement-skills (supplier-truthcheck), MIT, Copyright (c) 2026 Maximilian Ziermann. Modified: rewritten generic for EXCOM.
