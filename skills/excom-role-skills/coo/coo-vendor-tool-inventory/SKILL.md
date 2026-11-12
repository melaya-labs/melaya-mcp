---
name: coo-vendor-tool-inventory
description: Keeps one inventory of the vendors, SaaS tools and connected services the company runs on. Each entry records owner, cost, renewal date, the data it holds, usage evidence and risk, plus renew, negotiate, replace or cut proposals, overlaps and unused seats. Use when the monthly inventory is due, when a trial, renewal or price-change notice arrives, when someone requests a new tool, when a vendor blocks a launch, or when asked "what are we paying for".
version: 2.0.0
---

# Vendor and tool inventory

Know what the company depends on, what breaks if it fails, and what nobody uses. Cut the unused, so money goes to what moves the outcomes.

## Look up first

- The stack and connected services: `excom_knowledge_search` "systems and tools" or "vendor inventory". If there is no inventory, build it from the steps below and propose it as a new note with `excom_save_draft`.
- Costs: from the CFO (`excom_send_handoff`, kind question). Never estimate a vendor price.
- Contract and security reviewers: the legal and security roles on the team.

## Steps

1. Build the list from three sources: the stack note, the services connected to the team (your grants and `excom_list_recommended_apps`), and receipts, invoices, renewals and trials in the last 90 days of mail (`gmail_list_threads`, `zoho_email_search`).
2. For each item, record:
   - Purpose and owner role.
   - Plan, cost per period and renewal or trial end date.
   - Account owner type: a company account or a personal one.
   - Data it holds: customer data, secrets, analytics.
   - Connector id, if there is one.
3. Usage evidence for the last 30 days: connector calls in tasks (`excom_read_tasks`), pipelines using it (`excom_pipeline_list`), or confirmation from a human owner. With no evidence, mark it "unused, confirm".
4. Risk:
   - A single point of failure (hosting, edge, billing).
   - Lock-in and exit cost.
   - Security posture, for vendors that hold secrets or customer data (ask the security role).
   - Contract terms (ask the legal role).
5. For vendors with a decision due this month, write a short review: total cost of ownership (subscription, setup, upkeep, exit), performance (uptime, support response), and a recommendation (renew, negotiate, replace or cut) with negotiation points.
6. Overlaps: two tools doing one job, trials that converted without approval, unused seats. Propose one tool and one owner.
7. Save with `excom_save_draft`. Writing the inventory into a sheet (`sheets_update_by_header`) is a record write and asks. Record the item count and total monthly cost with `excom_record_measurement`. Route renewals and cuts to the owner through the CFO with `excom_propose_task`.

## Output

```text
Vendor inventory, read <date>
| Vendor/tool | Purpose | Owner role | Plan and cost | Renewal | Data held | Used (evidence) | Risk | Recommendation |
Decisions this month: vendor | TCO | performance | call | negotiation points
Overlaps and unused: item | monthly cost | proposal
```

## Approvals

- Buying, renewing, upgrading, downgrading or cancelling is spend and always asks. A human acts in the vendor console.
- Accepting vendor, reviewer or licence terms is a legal action, and a human accepts it.
- Replying to vendors is a send, and asks.

## Example

Acme pays for two survey tools (8 and 15 USD a month). One had no use in 60 days and its owner confirms. Proposal: cut it at renewal on the 20th, saving 15 USD a month. The other holds customer emails: flagged for a security review.

Adapted from anthropics/knowledge-work-plugins (operations/skills/vendor-review/SKILL.md), Apache-2.0. Modified: rewritten generic for EXCOM.
