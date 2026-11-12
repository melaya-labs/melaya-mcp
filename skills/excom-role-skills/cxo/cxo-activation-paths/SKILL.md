---
name: cxo-activation-paths
description: Defines for each product the shortest documented path to a first success and the milestone that proves it, finds where a user or cohort is stuck, and drafts the single next step. Use when a new customer is handed over, when a partner's client starts, when a signup cohort needs a next step, when a support question shows a user stuck before first success, or when someone asks "why don't users activate".
version: 2.0.0
---

# Activation paths per product

Activated users are the ones who pay, so every new user gets one concrete next step on the one product they came for.

## Look up first

- The product list and each product's first-success tutorial: `excom_knowledge_search` "products", "getting started", "first run tutorial". Missing tutorial for a product: draft the path from the product docs with `excom_save_draft` and ask the CPO to confirm.
- Funnel rungs and who counts as a user: search "metrics definitions"; if missing, ask the CDO (`excom_send_handoff` kind question).
- Known activation blockers: search "known issues", "troubleshooting", "activation study".
- Activation targets in the team's outcomes (in context).

## Steps

1. Identify the product the user came for (signup source, plan, first actions). One product per user.
2. Read where they are: setup state, usage and failed runs through `melaya_tools` (setup status, account usage, run diagnosis); cohorts with `posthog_compute_funnel` or `ga4_run_funnel_report` when granted.
3. Build or read the milestone ladder for that product (aha, activated, sticky) with references/milestone-ladder.md.
4. Check known blockers first (references/milestone-ladder.md), because most stalls are setup, not interest.
5. Pick one next step and draft it: the step, one doc link, what to send if it persists. Plain text, the user's language. `gmail_create_draft` or `zoho_email_save_draft` (draft) and `excom_save_draft`.
6. One message per user per week across CXO and CRO: check `excom_read_tasks`. Users who reached value and hit a limit go to the CRO.
7. Weekly: write the friction list (step, count, documented answer) for the CPO, and record activated users per product with `excom_record_measurement`.

## Output

```text
| User or cohort | Product | Rung reached | Blocker (evidence) | Next step | Doc link | Draft id | Owner |
Per product: started, activated, top blocker
```

## Approvals

- Every message to a user: send class.
- Plan changes, credits or refunds: the CFO decides.
- Editing a public tutorial: asks.

## Example

Acme Bakery signed up for the phone automation product 3 days ago, verified, no device paired. Next step: "Pair your phone: open the app on the phone and enter the code shown on your screen within 5 minutes" with the pairing doc link.

## References

- references/milestone-ladder.md: the ladder template per product and the common blocker checks. Read at steps 3 and 4; loads with `excom_skill_load` (section) or by paging.

Adapted from gtmagents/gtm-agents (plugins/product-led-growth/skills/onboarding-blueprint/SKILL.md), Apache License 2.0. Modified: rewritten generic for EXCOM.
