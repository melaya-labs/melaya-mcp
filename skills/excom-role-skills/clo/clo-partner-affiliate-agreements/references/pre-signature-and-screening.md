# Pre-signature checklist, screening and filing

## Pre-signature checklist
- Document is final: no open redlines or comments.
- All exhibits and schedules attached (tier schedule, DPA if the partner processes data, brand guidelines).
- Correct legal entity names on every signature block, matching the registry check.
- Signers have authority to bind their organisation.
- Dates correct, or left for the execution date.
- Internal approvals recorded (owner; counsel where a clause carries risk).
- Tier and terms match the published programme exactly, or the owner approved the difference in writing.
- Signing order set (counterparty first or company first) and copy recipients listed.

## Screening layers (run in order; stop and escalate on a possible match)
1. Sanctions: `sanctions_screen` on the legal name (several lists in one verdict); `sanctions_screen_batch` for many names.
2. Legal entity: `gleif_get_lei`, or the national registry tool for the country.
3. Tax number: `vies_check_vat` for EU VAT numbers.
4. Domain and identity: `rdap_domain` for the website's registration; compare names and countries.
5. Record: date, tools, results, verdict. A hit is a signal, not a conclusion; the owner and counsel decide.

## Filing convention
- The team's partner agreements folder location comes from the knowledge base.
- One folder per partner, named with the partner's legal name.
- File name: <partner legal name> - <agreement type> - signed <date>.pdf (use a hyphen, not a dash character).
- A partner is SIGNED only when the executed agreement is in that folder.
- Keep the envelope id in the status line so the copy can be re-downloaded.
