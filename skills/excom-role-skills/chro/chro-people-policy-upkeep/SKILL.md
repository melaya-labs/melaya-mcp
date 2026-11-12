---
name: chro-people-policy-upkeep
description: Reviews people and security policies against current practice, drafts revisions as redlines, runs fairness and privacy checks, plans re-acknowledgement, and answers policy questions with the clause cited. Use when a policy is past its review date, when practice has changed (remote work, new tools, a new product surface), before a new hire acknowledges the policy set, or when someone asks "what is our policy on".
version: 2.0.0
---
# People policy upkeep

Keeps policies true, dated and acknowledged, and answers questions from the text rather than memory. Stale policies are what an auditor or a new hire finds first.

## Look up first

- The policy set with versions and review dates: `excom_knowledge_search` "people policies", "information security policy", "acceptable use", "remote working", then `excom_knowledge_read`. Never reconstruct a policy you were not given; if one is missing, say so and propose drafting it with `excom_save_draft`.
- Who owns and approves each policy: from the policy text, or ask the owner with `excom_propose_task` (needs_decision true).
- The data retention rules for any data a policy collects: `excom_knowledge_search` "data retention".
- `excom_recall` for earlier policy decisions.

## Steps

1. List policies whose review date has passed and record each with `excom_record_fact`.
2. Question mode: find the clause, quote it, explain it in plain words, name exceptions and who to ask, cite note and section. If nothing covers it, say so and propose a task; never guess.
3. Review mode: write the purpose line ("this policy exists so that"), then mark each clause still true, drifted, missing or contradicted, with the practice evidence.
4. Separate policy (rules with consequences) from procedure (steps that change often); move procedure to its runbook so the policy stays stable.
5. Draft the redline with the drafting rules in `references/policy-drafting.md`: one obligation per clause, "must" for requirements, named actor and timeframe. Flag clauses that read as contractual for the CLO.
6. Run the fairness and privacy checks from the reference.
7. Ask the CLO and CISO for review of legal and security clauses with `excom_send_handoff` (kind request). Save the redline with `excom_save_draft`; a Docs copy with `docs_create` is a record write.
8. After the owner approves, propose the acknowledgement round and the next review date with `excom_propose_task`. Do not edit source notes yourself; findings go to the note owner.

## Output

```text
Policy review: <policy>  version <n>  last review <date>  next review <date>
Purpose | Clause | status | evidence
Redline: clause | current | proposed | reason
Questions for CLO / CISO | Acknowledgement plan: who | by when
Question answer: quick answer | details | exceptions | contact | source (note, clause)
```

## Approvals

- Publishing or changing an approved policy: the owner (security policies with the CISO).
- Change notices to people: send.
- Changes that alter contract terms: legal or people, through the CLO.

## Example

Acme's remote working policy is 4 months past review. The review finds two drifted clauses (a VPN rule replaced by an access proxy) and one missing clause (agents running on personal laptops). The redline proposes three changes with evidence; the CISO confirms; the owner approves and a re-acknowledgement round is proposed.

## References

- `references/policy-drafting.md`: clause drafting rules, fairness and privacy checks, revision table; read at steps 5 and 6.

Adapted from sara-hamza/people-ops-claude (plugins/people-ops/skills/policy-drafter), MIT, and anthropics/knowledge-work-plugins (human-resources/skills/policy-lookup), Apache-2.0. Modified: rewritten generic for EXCOM.
