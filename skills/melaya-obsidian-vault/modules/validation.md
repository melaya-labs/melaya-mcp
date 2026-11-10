# Validation: the checker and the helper scripts

> **Use when:** after every batch, before a handover, review, export or publish, and whenever something looks broken.
> **Inputs:** the vault folder (or an export); `_Meta/vault-config.json`; a shell with Python 3.8+ (or the manual checklist below).
> **Outputs:** a findings report with zero errors, and the fixes made.
> **Next:** [graph.md](graph.md) for link fixes, [zones.md](zones.md) for leaks, [troubleshooting.md](troubleshooting.md).

All scripts are in `../scripts/`, standard library only, and read `_Meta/vault-config.json`. Run them on the vault folder (or a copy); every writing script is a dry run unless `--apply`.

## The checker

```bash
python3 scripts/check_vault.py --vault "/path/to/vault" [--scope "20 Product/"] [--today 2026-11-10] [--all] [--json report.json] [--strict]
```

Exit code 1 on any error (or any warning with `--strict`). The summary lists every check with its counts, then the findings (first 25 per check unless `--all`).

| Check | Finds | Level |
|---|---|---|
| dangling links | `[[Name]]`, embeds, Markdown links to vault files that do not resolve | error |
| dangling anchors | `#Heading` or `#^block` missing in the target | error |
| ambiguous links, duplicate names | two notes share a name | error |
| property links | unquoted `[[...]]` in properties | error |
| orphans | nothing links in (notes, Canvas count) | error |
| hops from Home | unreachable, or over `max_hops` | error |
| missing properties | `required_properties`, plus `required_by_zone` for internal notes | error |
| invalid properties | type, status, audience outside their lists; bad dates; future `updated`; `review_every` format; `superseded` without a valid `superseded_by`; `updated` older than the newest Changelog line; long description (warning) | error |
| taxonomy | a tag not in the taxonomy note or `tag_patterns` | error |
| stale notes | `reviewed + review_every` passed and status current | warning |
| structure | required H2 per type, At a glance bullets, Changelog last and well formed, H1 missing (warning), `open_questions` flag without the section (warning) | error |
| size without outline | over the size budget without a complete `## Contents` | warning (configurable) |
| zone leaks | public to internal links, embeds, Canvas, Bases; manifest path without `publish: false` (warning) | error |
| secrets | credential-shaped strings (cloud keys, tokens, private keys, assignments like `password: ...`) | error |
| personal data | emails outside `pii.email_allow` (error in public notes), IBAN and card numbers that pass their checksums, phones, national id shapes, IPs (warning) | error or warning |
| deny list | `denylist` everywhere, `denylist_public` in public notes | error |
| punctuation | em dash, en-dash separator, and optionally semicolons, exclamation marks, custom patterns (meta notes exempt) | error |
| files | invalid Canvas JSON, Canvas nodes or edges to missing items, Bases filtering on missing folders | error |
| attachments | unused, outside the attachments folder, oversized | warning |

Templates (`_Templates/`) and `_Meta/sources/` are not checked as notes.

## The other scripts

| Script | Use |
|---|---|
| `scaffold.py --vault V --name N --sections "10 A,20 B" [--internal "80 C"] [--languages en,fr]` | new vault skeleton that passes the checker; never overwrites without `--force` |
| `ledger.py plan|next|mark|seen|hash|dupes|where|status` | the source ledger ([extraction.md](extraction.md)) |
| `build_moc.py --all --apply` | refresh every hub's generated list |
| `autolink.py [--types term,concept] [--exclude "Plan,Team"] [--apply]` | link first unlinked mentions of titles and aliases |
| `add_contents.py [--budget-kb 8] [--min-h2 6] --apply` | Contents outlines on long notes |
| `graph_report.py [--json r.json] [--md r.md]` | graph metrics and repair lists ([graph.md](graph.md)) |
| `export_public.py --out DIR [--unlink]` | public export with re-check ([zones.md](zones.md)) |

## After every batch

```bash
python3 scripts/build_moc.py --vault V --all --apply
python3 scripts/autolink.py --vault V            # review, then --apply
python3 scripts/add_contents.py --vault V --apply
python3 scripts/check_vault.py --vault V
python3 scripts/graph_report.py --vault V | head -20
```

Fix every error before the next batch; list warnings in the batch report.

## Through Melaya's vault tools (no shell on the vault's machine)

`obsidian_unresolved` (dead links), `obsidian_orphans`, `obsidian_deadends`, `obsidian_properties` (property names and counts), `obsidian_tags` (tags with counts against the taxonomy), `obsidian_search` with `[status:stale]` or `-[description]`, and `obsidian_backlinks` on hubs cover most checks. Or ask the user to run the checker on their computer and paste the summary.

## Manual checklist (chat only)

- [ ] Every note has type, description, tags (from the taxonomy), updated; internal notes have owner, status, reviewed, review_every, publish: false.
- [ ] Every link points at a note in the file list; every heading link at an existing heading.
- [ ] Every note is listed in its hub; every hub is listed in Home; nothing is more than three links from Home.
- [ ] No public note links to an internal one; Home's internal links sit between the strip markers.
- [ ] No credential, personal contact data, id or account number anywhere.
- [ ] Every fact has a source and a date; unknowns are open questions.

## Reading the result

Report to the user: the RESULT line, counts per check that is not zero, what you fixed, and what needs them (an open question, a missing permission, a decision on a conflict). Never say "clean" when only part of the vault was checked; say which `--scope`.
