---
type: process
description: "<One sentence: the incident or recurring operation this runbook handles and its end state.>"
tags:
  - area/<section-slug>
  - topic/runbook
related:
  - "[[<Hub or MOC>]]"
audience: internal
publish: false
owner: <on-call role>
status: draft
source_of_truth:
  - "<system, dashboard or document each step relies on, with date>"
updated: {{date}}
reviewed: {{date}}
review_every: 30d
---

# {{title}}

<One sentence: when to open this runbook.>

> [!warning] Safety
> <What must never be done during this runbook, and who must approve the risky step.>

## At a glance

- Signal: <alert, symptom or request that starts it>.
- Severity and time to act: <levels and targets>.
- Escalate to: <role> after <time or condition>.

## Steps

1. Confirm the signal: <check and expected result>. ^confirm
2. Contain: <action>. ASK <approver> before <risky action>. ^contain
3. Fix: <action>. ^fix
4. Verify: <how you know it is resolved>. ^verify
5. Record: add a line to the incident log and to this note's Changelog. ^record

## Rollback

1. <How to undo step 3.>

## Related

- [[<Hub or MOC>]]
- [[<System reference note>]]

## Changelog

- {{date}} <who>: runbook created from the runbook template.
