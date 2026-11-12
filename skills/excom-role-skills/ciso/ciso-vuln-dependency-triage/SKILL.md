---
name: ciso-vuln-dependency-triage
description: Turns the flood of CVEs, scanner findings and dependency alerts into a short fix list for your own stack, ranked by evidence of exploitation, exposure and reachability rather than raw CVSS, with owners and due dates from your patch policy. Use when writing the weekly vulnerability brief, when a known-exploited CVE touches your stack, when a container scan, Dependabot or code scanning alert lands, or a release changes a lockfile.
version: 2.0.0
---
# Vulnerability and dependency triage

Produce an ordered, owned fix list where exploited and exposed issues come first. Fixed on time, it keeps releases shippable and questionnaires answerable.

## Look up first

- The patch policy and its fix deadlines per severity: `excom_knowledge_search` for "patching policy", "vulnerability SLA". If none exists, use the default table in references/priority-matrix.md, say so, and ask the owner to confirm deadlines with `excom_propose_task` (needs decision true).
- The stack inventory: components, lockfiles, images and which are internet facing. Search "stack inventory", "architecture", "systems and connectors"; ask the CTO with `excom_send_handoff` (kind question) when it is missing.
- Open items, exceptions and their clocks from last time: `excom_recall`.
- Which repository, scanner and compliance apps you are granted; `excom_request_setup` for a missing one.

## Steps

1. Collect, reads only:
   - Exploited in the wild: `nvd_cve_kev_only`, then `nvd_cve_recent` and `nvd_cve_search_by_product` for each stack component.
   - Dependencies: `osv_batch_query` on every lockfile in one batch, `osv_vuln_details` per hit.
   - Repositories: `github_list_dependabot_alerts`, `github_list_code_scanning_alerts`.
   - Compliance platform: `vanta_list_vulnerabilities` if it is Vanta.
   - Images: `dockerhub_image_manifest` when a floating tag is involved.
2. Score each finding and write the reason: known exploited (strongest), likelihood of exploitation (public exploit, active campaign), CVSS base, exposure (internet facing, internal, build tool, dev only), reachability (is the vulnerable code path used; ask the CTO when unsure).
3. Assign priority and due date from the patch policy (references/priority-matrix.md as fallback). Exploitation outranks CVSS.
4. Group fixes the CTO can ship together (one dependency bump, one image rebuild). Propose each with `excom_propose_task`: package, current and fixed version, priority, due date, covering test. Fixes run in a CTO coding session and deploy through the CTO; the CISO never pushes.
5. No fix available: draft a compensating control (edge rule, feature flag, disable the path) with `excom_save_draft`. Edge rules and flag flips are production class.
6. Record exceptions with owner and expiry; an expired exception re-enters the list. Record deadline misses with `excom_record_measurement`.

## Output

```text
Vulnerability brief <date>: sources read (KEV, NVD, OSV batch, Dependabot, code scanning, scanner log date)
| id | component | exploited | exposure | reachable | CVSS | priority | due | fix | owner | status |
Exceptions: id, compensating control, owner, expiry
Deadline misses since last brief
```

Saved with `excom_save_draft`.

## Approvals

- Any deploy, production image rebuild, edge rule or flag flip (production, through the CTO).
- Accepting a P1 or P2 as an exception (owner decision).
- Paid scanners or feeds (spend, with the cost).

## Example

Acme's weekly brief: 37 OSV hits, 1 known exploited in the reverse proxy (internet facing, P1, due in 48 hours by the policy), 2 high in a build-only tool (P3), 30 dev-only lows grouped into one bump. The P1 goes to the CTO as a coding session task with the fixed version and a covering check.

## References

- references/priority-matrix.md: default priority and deadline table, exposure classes and exception rules. Read at step 3 when your patch policy is missing; load with `excom_skill_load` or by paging.

Adapted from mukul975/Anthropic-Cybersecurity-Skills (skills/performing-cve-prioritization-with-kev-catalog), Apache-2.0. Modified: rewritten generic for EXCOM.
