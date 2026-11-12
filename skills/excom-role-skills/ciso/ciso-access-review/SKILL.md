---
name: ciso-access-review
description: Runs a risk-ranked review of who holds access to your systems (accounts, admins, keys, tokens, runners, mailbox delegations), gets a keep or revoke decision per entitlement from a named reviewer, and leaves a dated record an auditor can read. Use when the quarterly access review is due, someone leaves or changes role, an auditor or questionnaire asks for the last review, or someone asks "who still has admin on X".
version: 2.0.0
---
# Access review

Confirm that every account, admin right, key and runner still has an owner and a reason, and revoke the rest through approvals. A retained review record is evidence buyers and auditors ask for, and leavers with live access are the cheapest breach.

## Look up first

- The access policy: `excom_knowledge_search` for "access provisioning procedure", "offboarding checklist", "quarterly access review". Read the review cadence, the two-person rule and the revocation steps. If missing, draft a one-page procedure with `excom_save_draft` and propose it.
- The system inventory and its risk rank: search "systems and connectors" and "security posture". If no ranked list exists, use the default tiers in references/risk-tiers.md and say so.
- The people roster and roles: ask the CHRO with `excom_send_handoff` (kind question). Never infer a leaver from activity alone.
- Last review and last access snapshot: `excom_recall`. Apps you are granted decide which reads below are possible; call `excom_request_setup` for a missing one and continue.

## Steps

1. Rank the scope before collecting: High systems first, because a review that runs out of time must have finished them (references/risk-tiers.md).
2. Collect entitlements, reads only, per system you are granted:
   - Source control: `github_org_members_without_2fa`, `github_org_audit_log`, `github_people_org_members`.
   - Edge access apps: `cloudflare_list_access_apps`. An empty list from a connector is not proof of absence; confirm through a second source before concluding.
   - Mail: `zoho_group_list` or `gmail_get_settings` (forwarding, send-as), `outlook_admin_roles_members` if your tenant is Microsoft 365.
   - Runners and devices: `melaya_runner_status` for runners that belong to people who left.
   - Secrets: `excom_secret_list` for names, owners and ages only. Never read a value.
   - Compliance platform: `vanta_list_people` if it is Vanta, `drata_list_personnel` if it is Drata.
3. Correlate with the roster: leavers still holding access, role changes that kept old rights, admins without MFA, shared or orphan accounts, keys with no owner, and anyone who approved their own access (breaks the two-person rule).
4. Get certifiers: the CHRO confirms people and roles, the CTO confirms service accounts and runners. Each keep or revoke carries the reviewer's role.
5. Draft the revocation plan per finding (what, where, approver, how to verify) with `excom_save_draft` (draft). Revocations and key removals are production class.
6. After the owner or operator executes, re-read the same source to confirm, then close the row. Record the review with `excom_record_fact` and findings closed with `excom_record_measurement`.

## Output

```text
Access review <period>: scope and risk rank, sources read (tool)
| system | risk | account or key | owner | role fit | MFA | reviewer | keep/revoke | verify step | status |
Leavers checked against roster: n of n
Exceptions accepted: owner, expiry
Next review date
```

Plus one `excom_propose_task` per revocation.

## Approvals

- Revoking another person's account, session, token, key or runner (production).
- Any widening of access found missing (new admin, key, access email, OAuth scope).
- Deleting accounts or data (delete).

## Example

Acme's quarterly review: 41 entitlements across 7 systems. Two leavers still in the source control org, one admin without MFA, one runner online for a contractor who left. Four revoke rows drafted, each with the approver and the read that will verify it; the CHRO confirmed the roster and the CTO the two service accounts.

## References

- references/risk-tiers.md: default High, Medium, Low tiers and the finding types to flag. Read at step 1 when the knowledge base has no ranked inventory; load with `excom_skill_load` or by paging.

Adapted from mukul975/Anthropic-Cybersecurity-Skills (skills/performing-access-review-and-certification), Apache-2.0. Modified: rewritten generic for EXCOM.
