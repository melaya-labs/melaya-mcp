---
type: source
description: Every system the {{vault}} vault was built from, what was read, when, and what was left out, with the machine ledger behind it.
tags:
  - area/meta
aliases:
  - Sources
related:
  - "[[{{home}}]]"
  - "[[Vault Changelog]]"
audience: internal
publish: false
owner: {{owner}}
status: current
updated: {{date}}
reviewed: {{date}}
review_every: 30d
---

# Source Ledger

The human view of the import. The machine ledger is `_Meta/sources/ledger.jsonl` (one JSON record per item read, newest wins), kept and summarised by `ledger.py`.

## At a glance

- Sources: none read yet.
- Last refresh: not run yet.
- Excluded on purpose: personal data, credentials, drafts marked private.

## Sources

| Source | System | Scope read | Items read | Written | Skipped | Last read | Note |
|---|---|---|---|---|---|---|---|
| <name> | <system> | <space, folder, channel, query> | 0 | 0 | 0 | {{date}} | <link to its source note> |

## Excluded

| What | Why |
|---|---|
| <item or pattern> | <personal data, secret, out of scope, owner said no> |

## Related

- [[{{home}}]]
- [[Vault Changelog]]
