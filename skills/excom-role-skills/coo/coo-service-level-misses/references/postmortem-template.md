# Postmortem template

Blameless: describe systems, queues and decisions, never people's faults.

```text
Postmortem: <title>
Date: <date> | Duration: <hours> | Severity: SEV<n> | Author: COO | Reviewed by: <roles>

Summary: 2 to 3 sentences, what happened and the effect
Impact: users affected | duration | runs lost | revenue or signups at risk | data affected (yes/no)
Timeline (with time zone):
  <time> detected by <signal>
  <time> classified SEV<n>
  <time> routed to <role>
  <time> mitigated
  <time> resolved
Root cause: the technical cause in plain words
Five whys:
  1. Why did users see <symptom>? Because ...
  2. Why ...? Because ...
  3. ...
  4. ...
  5. ...
What went well: ...
What went poorly: ...
Where we got lucky: ...
Action items:
  | Action | Owner | Due | Type (prevent / detect / mitigate) |
Lessons: one or two sentences for the runbook owner
```

## Status update format (during the incident)

```text
Incident update: <title>
Severity: SEV<n> | Status: investigating / identified / monitoring / resolved
Current status: one or two sentences
Actions taken: bullets
Next update: <time>
```

## Rules

- Every action item has one owner and a due date. Prefer detection and prevention over "be careful".
- If a runbook was wrong or missing, add a runbook upkeep task.
- Customer-facing text never names internal hosts, ids or vendors unless the owner approves it.
