---
type: source
description: "<One sentence: which system or collection this is, what the vault took from it, and when.>"
tags:
  - area/meta
  - source/<system>
related:
  - "[[Source Ledger]]"
audience: internal
publish: false
owner: <person who owns the source>
status: current
system: <notion | confluence | google-drive | gmail | slack | jira | github | local-folder | web>
scope: "<space, folder, channel, query or path that was read>"
last_read: {{date}}
source_of_truth:
  - "<connector and tool used, or the local path>"
updated: {{date}}
reviewed: {{date}}
review_every: 30d
---

# {{title}}

<One sentence: what this source holds and why it feeds the vault.>

## At a glance

- Read: <items> items, <items> written to notes, <items> skipped (ledger batch <id>, {{date}}).
- Access: <read-only connector or local folder>. Permission owner: <who>.
- Refresh: every <period>, incremental by <revision or modified time>.

## What was taken

| Area of the source | Notes it fed | Zone |
|---|---|---|
| <space, folder or channel> | [[<Note>]] | <public or internal> |

## What was left out and why

- <Personal data, secrets, drafts, out of scope.>

## Related

- [[Source Ledger]]
- [[<Hub fed by this source>]]

## Changelog

- {{date}} <who>: first import.
