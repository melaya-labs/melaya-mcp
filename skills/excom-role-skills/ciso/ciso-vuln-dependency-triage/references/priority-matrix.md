# Default priority matrix and exception rules

Use only when your patch policy sets no deadlines. Say so in the brief and ask the owner to confirm.

## Priority

| Known exploited | Severity | Exposure | Priority | Default fix within |
|---|---|---|---|---|
| Yes | Any | Internet facing | P1 | 48 hours |
| Yes | Any | Internal | P1 | 48 hours |
| No | Critical | Internet facing | P2 | 7 days |
| No | High | Any | P3 | 7 days |
| No | Critical | Build or dev only | P3 | 14 days |
| No | Medium or lower | Any | P4 | Next release |

Raise one level when a public exploit or an active campaign is named in the advisory. Lower one level only when the CTO confirms the vulnerable path is unreachable, and write that confirmation down.

## Exposure classes

- Internet facing: edge, public API, web app, browser extension, anything a stranger can send input to.
- Internal: services reachable only from inside the network or by authenticated staff.
- Build tool: used only at build time, not shipped.
- Dev only: test and development dependencies, never deployed.

## Signals, strongest first

1. Listed in the known exploited vulnerabilities catalogue.
2. Public exploit code or an active campaign.
3. Exploit prediction score, when available in the advisory.
4. CVSS base score.
5. Asset criticality and exposure.

## Exceptions

- Every exception has an owner, a compensating control, a reason and an expiry date.
- P1 and P2 exceptions need the owner's decision.
- An expired exception re-enters the list automatically with its original due date passed.

## Closing a finding

A finding closes only when the deployed version is read back (package version in the running build or image digest), not when the fix is merged.
