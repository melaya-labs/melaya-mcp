# Rating matrix and evidence list

## Evidence per supplier
- Live use confirmed (tool and date).
- Security attestation on file (SOC 2 Type II report, ISO 27001 certificate) or "not on file".
- DPA and transfer mechanism executed, or "verify".
- Contracting legal entity confirmed.
- Data residency matches what the public subprocessor list says.
- Incidents in the last 90 days (status page, notices).
- Concentration: single point of failure yes or no.
- Fallback documented, and whether it was ever tested.
- Screening result from the CLO (date).

## Rating matrix
| | Low impact | Medium impact | High impact |
|---|---|---|---|
| High likelihood | Medium | High | Critical |
| Medium likelihood | Low | Medium | High |
| Low likelihood | Low | Low | Medium |

## Categories
- Operational: outage, capacity, support failure.
- Financial: price rise, lock-in, supplier instability.
- Compliance: no DPA, wrong residency, missing attestation.
- Security: breach, weak access controls, sub-supplier risk.
- Strategic: supplier exits a market, product discontinued, acquisition.

## Rules
- Unknown is a gap, not a pass.
- Never claim an attestation that is not on file.
- Customer-selected providers are rated as the customer's choice, not as your subprocessors.
- No ids, addresses or credentials in the memo.
