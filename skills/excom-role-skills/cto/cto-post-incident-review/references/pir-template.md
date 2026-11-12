# Post-incident review template

Use the team's own severity table when the knowledge base has one. This default applies only when it does not.

## Default severity table

| Severity | Availability meaning | Response expectation |
|---|---|---|
| SEV1 | outage of a surface all customers rely on, or one that moves money, or confirmed data loss | commander assigned at once, updates every 15 minutes, executive notified within 15 to 30 minutes |
| SEV2 | a product degraded, or a subset of customers affected | commander within 30 minutes, updates every 30 minutes |
| SEV3 | internal or limited impact with a workaround | handled in business hours, update at milestones |
| SEV4 | informational, cosmetic, monitoring gap | normal ticket |

Security incidents use the CISO's table and process; the CTO adds the technical section.

## Template

```text
PIR <short name>

Summary
  What happened, in three sentences a customer could understand.

Severity
  SEV<n> (changed from SEV<m> because ...)

Timeline (UTC)
  hh:mm  event  (source: log query, annotation, build, task)
  ...    [gap: no record between hh:mm and hh:mm]

Impact
  Duration from first error to recovery
  Products and routes affected
  Runs failed or interrupted (count, source)
  Customers who reported it (count)

Root cause (five whys)
  Why 1: ... evidence
  Why 2: ... evidence
  ...
  Root cause: ... (if removed, the incident would not have happened)

Contributing causes
  Code / config and pins / deploy process / monitoring and alerting / capacity / handoffs

Response
  Time to detect, declare, mitigate, recover
  Went well: ...
  Went badly: ...
  Rollback plan existed before the deploy: yes/no

Actions
  action | owner role | due | proof of done | task id

Known-issues entry
  Symptom | Cause | Fix
```

## Rules

- Every timeline line and impact number has a source read during the review; gaps are marked, never filled.
- Blameless: name roles and systems, not people.
- Each action has one owner role, a date and a proof that can be checked.
- Write within 72 hours of resolution; a SEV3 may use a short form (summary, root cause, actions).
