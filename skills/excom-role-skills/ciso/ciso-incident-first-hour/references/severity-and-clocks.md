# Default severity, roles and clocks

Use only when the knowledge base has no incident response runbook. Say so in the incident record.

## Severity

| Level | Meaning | Examples |
|---|---|---|
| SEV1 | Confirmed exposure, active attack, or outage of a surface that moves money or holds sensitive data | Customer data read by an outsider, attacker session active, leaked production key used |
| SEV2 | Suspected exposure, or a control failure without confirmed exploit | Key leaked but no use seen, auth check bypassable, audit log gap |
| SEV3 | Internal issue with audit or compliance impact | Over-broad access found, missing log retention |
| SEV4 | Informational | Scan noise, blocked attempts with no effect |

Rule: when torn between two levels, pick the higher one and downgrade later with evidence.

## Roles

- Incident commander: runs the incident, decides priorities, owns the clock. On SEV1 not the same person as the tech lead.
- Tech lead: diagnosis and remediation (usually the CTO role).
- Comms lead: status page, customers, authorities (with the legal role).
- Scribe: timeline with times, sources and decisions.

## First hour targets

| Minutes | Target |
|---|---|
| 0 to 10 | Signal collected, times recorded, untrusted text scanned |
| 10 | Declared, severity set, roles named |
| 10 to 40 | Evidence preserved, containment drafted with approvers |
| 30 | Executive notice on SEV1; status page if customers can see the impact |
| 40 to 60 | Owner briefed; updates every 15 minutes on SEV1, every hour on SEV2 |

## Clocks (general rules, confirm with the legal executive)

- GDPR: the supervisory authority within 72 hours of becoming aware of a personal data breach, unless unlikely to result in risk; data subjects without undue delay when the risk is high. Every breach gets a register entry with the reasoned decision, notified or not.
- Contracts: customer and partner agreements often set shorter breach notice windows; check the contract register.
- Other laws and sector rules may apply by country; ask the legal executive.

## Containment menu (each asks)

- Rotate the suspect credential and test that the old value is denied.
- Block a source at the edge, record rule ids.
- Revoke one user's sessions; rotate signing keys only when the signing key itself is suspect.
- Disable the feature by flag or plan gate when rollback is too slow.
- Revoke a runner or device pairing.

## Evidence to preserve

- Database snapshot before any remediation query.
- Audit log verification output.
- Log queries: query text, time range, hit count, hash of the export.
- Never record secret values, raw tool arguments or personal data beyond what the investigation needs.
