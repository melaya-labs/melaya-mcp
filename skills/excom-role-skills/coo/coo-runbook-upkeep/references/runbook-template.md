# Runbook template

```text
Runbook: <task name>
Owner: <role> | Collaborators: <roles> | Frequency: <daily / weekly / as needed>
Updated: <date> | Reviewed: <date> | Review every: <interval> | Source of truth: <engineering source, if any>

Purpose: what this achieves and when to run it
Prerequisites: access, apps granted, inputs needed

Steps
| Step | Action | Tool or file | Approval |
| 1 | <exact action> | <tool id or file> | none / ask (send, spend, production, record write) / operator only |
| 2 | ... | ... | ... |
Each step also states the expected result and what to do if it fails.

Verification: how to confirm it worked (what was verified live, what was not)
Rollback: how to undo it
Escalation: situation | role to contact | channel
History: date | run by | evidence (task or run) | notes
```

## Rules for good steps

- Be painfully specific. "Run the deploy" is not a step. Name the tool, the target and the expected result.
- Mark every step that sends, spends, touches production or needs a secret. Operator-only steps name the section of the operator's notes, never the value.
- Put failure modes next to the step where they happen.
- Test the runbook by having someone who has never run it follow it, then fix where they got stuck.
- When the engineering source and this copy disagree, the engineering source wins, and the owner updates the copy.

## Drift signals to look for

| Signal | Where you see it |
|---|---|
| Step skipped or reordered | Task notes, pipeline run steps |
| Extra manual step | Task notes saying "also had to..." |
| Tool or file no longer exists | Grants, release notes, commits |
| Check failed but waved through | Task verification notes |
| Approval asked where none is marked, or the reverse | Approval history |
| Owner changed | Team roles, handoffs |
