# Zones, redaction and publishing

> **Use when:** a vault holds both shareable and internal notes, anything will be published, exported, shared, synced to a site or given to agents, or a note may contain secrets or personal data.
> **Inputs:** the charter's zones; the vault; `_Meta/.publishignore`; `_Meta/vault-config.json`.
> **Outputs:** every note in exactly one zone, a manifest that names the internal paths, redaction applied, and (on request) a checked public export.
> **Next:** [validation.md](validation.md); [agents.md](agents.md) when binding the vault to AI.

## Three zones

| Zone | Marked by | May link to | Leaves the vault |
|---|---|---|---|
| public | no internal flag, path not in the manifest | public notes only | yes, through `export_public.py` |
| internal | `publish: false`, an internal `audience`, `zone/internal` tag, path in `_Meta/.publishignore` | anything | never in a public export, Base or Canvas |
| private | a separate vault | anything in it | never shared |

A vault with no public ambitions sets `"zones": {"default": "internal"}` and stops worrying about leaks; everything else on this page still applies to secrets and personal data.

## The three locks (use all three)

1. **Manifest.** `_Meta/.publishignore` lists internal paths, one per line, a trailing slash for folders (template [../templates/meta/publishignore.txt](../templates/meta/publishignore.txt)). Any export, publish, site build, share, sync or knowledge-base upload skips them.
2. **Properties.** Every internal note carries `publish: false` and an internal `audience` (`internal`, `private`, `confidential`). A tool that cannot read the manifest skips these notes.
3. **Strip markers.** Home may list internal hubs only between `%% private:start %%` and `%% private:end %%`. An export drops those lines, markers included, so the public graph has no dangling link. No other public note is allowed an internal link, even inside markers.

The checker enforces: public notes never link to, embed or list internal notes; public Canvas never shows them; a public Base over the whole vault excludes every internal folder with `not:`; manifest paths carry `publish: false`.

## Keep internal names out of public notes

A public note that names an internal folder, client or project leaks it even without a link. Public conventions say "internal folders are listed in the manifest", never which. Put client code names, unreleased product names and partner names in `denylist_public` (regular expressions, case-insensitive) in `_Meta/vault-config.json`; the checker and the export both refuse them in public notes. `denylist` applies to every zone (for terms that must never appear at all).

## Redaction rules

| Content | Rule |
|---|---|
| Credentials: keys, tokens, passwords, connection strings, private keys, recovery codes | never, in any zone, even partial or as an example; write "stored in the password manager, entry <name>" |
| Personal contact data (emails, phones, home addresses) of anyone | not in the vault; roles and the system of record instead. Allowed exceptions: public role addresses on `example.com` style domains and the organisation's public contact |
| Government ids, bank, card, health, payroll data | never |
| People outside the team | by role and organisation, not by name, unless the owner decides otherwise for an internal vault |
| Team members | name and role in internal notes when the owner agrees; work facts only |
| Customers | organisations in internal notes; in public notes only with permission or when already public |
| Internal hostnames, IPs, ids, file ids, account numbers | internal zone only; never in public notes; examples use `192.0.2.x` and `example.com` |
| Unreleased plans, pricing internals, legal disputes | internal or private zone, per the charter |

How: redact at extraction time ([extraction.md](extraction.md)), replace with a role or a pointer (`[redacted: personal phone]` only where the gap must be visible), and record the excluded pattern in the Source Ledger. The checker's patterns (emails, phones, IBAN and card numbers with checksums, national id shapes, IPs, credential shapes) are a net, not a guarantee: read before you publish.

## Publishing and exporting

1. Get the owner's yes for the destination (static site, Obsidian Publish, public repository, shared folder, knowledge-base upload).
2. `python3 scripts/check_vault.py --vault V` with zero errors.
3. `python3 scripts/export_public.py --vault V --out ../public-export` (outside the vault). It skips manifest paths and internal notes, drops strip-marker blocks, removes internal-only properties (`owner`, `source_of_truth`, `reviewed`, `review_every`, `open_questions`, `publish` by default), copies only attachments, Bases and Canvas that public notes use, prunes canvas nodes and Base filters that point inside, then re-checks: a link to a skipped note is an error (or plain text with `--unlink`), and secrets or deny-listed terms stop it.
4. Run `check_vault.py` on the export folder too, read Home and three random notes in it, then publish.
5. Obsidian Publish users: publish from the export, or select notes with `obsidian_publish_status` and `obsidian_publish_add` only after the same checks.

## Moving a note between zones

- Public to internal: add the flags, add its path to the manifest if it is a folder rule, remove public links to it (the checker lists them), re-export.
- Internal to public: owner's yes, redaction pass, remove the flags, run the checker for leaks of other internal names inside it.
