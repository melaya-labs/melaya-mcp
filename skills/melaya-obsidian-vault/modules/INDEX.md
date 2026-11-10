# Module graph

Every module is a node with typed inputs and outputs; an edge means "the output of A is the input of B". Load the node you need and follow its Next line; never load the whole graph of modules. Artifacts named here live in the vault (`_Meta/...`) or in a work folder outside it.

## Nodes

| Module | Inputs | Outputs | Next |
|---|---|---|---|
| [intake](intake.md) | request, existing vault | `_Meta/Vault Charter.md` (test questions, zones, languages, sources, defaults) | sources, scaffold, architecture |
| [tools](tools.md) | the host | tool status: read paths, write path, scripts | sources |
| [sources](sources.md) | charter, connectors, folders | inventory, sensitivity levels, listings, `ledger.py plan`, owner's yes | extraction |
| [extraction](extraction.md) | pending ledger items | normalised text, ledger states, candidate facts | extract-types, architecture, writing |
| [extract-types](extract-types.md) | one batch of one source type | per-type recipe applied, candidate notes | architecture, writing |
| [architecture](architecture.md) | charter, inventory, candidates | sections, hubs, note types, names, paths, attachments policy | properties, writing |
| [properties](properties.md) | note type and zone | frontmatter, taxonomy, `vault-config.json` | writing |
| [obsidian-syntax](obsidian-syntax.md) | a note in progress | correct links, embeds, callouts, diagrams | views, graph |
| [views](views.md) | consistent properties | `.base` views, Dataview blocks, `.canvas` maps | graph, zones |
| [writing](writing.md) | facts with citations, type, voice | finished notes, Changelog lines | graph, validation |
| [graph](graph.md) | the vault, graph report | hubs, cross-links, glossary links, 3-hop reach | validation |
| [zones](zones.md) | charter zones, the vault | manifest, flags, redaction, public export | validation, agents |
| [multilingual](multilingual.md) | languages, mixed sources | layout, `lang` properties, translation links, voice cards | writing, graph |
| [validation](validation.md) | the vault | checker report at zero errors, fixes | graph, zones, troubleshooting |
| [maintenance](maintenance.md) | ledger, fresh listings, review queue | refreshed notes, reviews, merges and splits, refresh report | validation |
| [migration](migration.md) | an export or connector access | mapped structure, converted notes, redirect table | architecture, graph, validation |
| [agents](agents.md) | a checked vault | retrieval-friendly notes, binding and scopes, editing protocol, instruction lines | maintenance |
| [scenarios](scenarios.md) | the scenario | the module path and defaults | first module of the path |
| [troubleshooting](troubleshooting.md) | a symptom | cause and fix | the owning module |

## Standard flows

| Goal | Path through the graph |
|---|---|
| New vault from scattered sources | intake, tools, sources, scaffold, then per batch: extraction, extract-types, architecture, properties, writing, graph, validation; then zones (if shared), agents (if bound), report |
| Migration | intake, tools, sources, migration, extraction, architecture, properties, writing, graph, validation, maintenance |
| Add one source to an existing vault | sources, extraction, extract-types, writing, graph, validation |
| Monthly refresh | maintenance, extraction, writing, validation |
| Publish the public part | zones, validation (vault and export) |
| Make agents use it | agents, validation, then the charter's test questions |
| Rescue a messy vault | intake, validation (baseline), graph, architecture, properties, maintenance, validation |

## Resources

| Folder | What is there | When to read it |
|---|---|---|
| [../templates/](../templates/) | `vault-charter.md`, `home.md`, `moc.md`; `notes/` (concept, process, runbook, reference, decision, person, team, project, glossary, term, faq, meeting, source); `meta/` (conventions, tag taxonomy, editing protocol, changelog, source ledger, `vault-config.json`, `publishignore.txt`); `bases/`; `canvas/` | copy the one you are filling; `scaffold.py` copies them for you |
| [../examples/](../examples/) | a fictional company vault built from Drive, Notion, Slack and mail; a fictional research vault | when you want a finished reference of the same kind |
| [../scripts/](../scripts/) | `scaffold.py`, `ledger.py`, `build_moc.py`, `autolink.py`, `add_contents.py`, `check_vault.py`, `graph_report.py`, `export_public.py`, shared `vaultlib.py` | whenever a shell is available ([validation.md](validation.md)) |

## Adding a node

A new module is one file in `modules/` that opens with a title and the four-line front block (Use when, Inputs, Outputs, Next), plus one row in the router's intent table and one in the node table above. Keep modules generic: no real organisation, product or person names, fictional examples only, plain ASCII, numbers over adjectives.
