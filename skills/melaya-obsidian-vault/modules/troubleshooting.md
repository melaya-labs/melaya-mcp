# Troubleshooting

> **Use when:** something in the build, the vault, a script or a connector does not behave.
> **Inputs:** the symptom, the checker or script output, the tool reply.
> **Outputs:** the cause and the fix, and the module that owns it.
> **Next:** the owning module, then [validation.md](validation.md).

## Vault and Obsidian

| Symptom | Cause | Fix |
|---|---|---|
| A link opens a new empty note | the name does not match (case, spaces, punctuation) or the note was never created | check the exact file name; fix the link or create the note ([graph.md](graph.md)) |
| A heading link lands at the top | the heading text changed, or contains `: # \| ^ [ ] %` | link without those characters; add a block id for stable targets |
| Properties show as raw text or break | YAML error: unquoted `[[link]]`, a tab, a colon in a value, mixed list styles | quote links and values with colons; use spaces; the checker's property-links finding points at the line |
| A property shows the wrong type | the same name holds different types across notes | fix the odd notes; set the type once in the Properties view |
| Two notes claim the same name | duplicates after import or a synonym note | merge or rename in Obsidian ([maintenance.md](maintenance.md)) |
| Graph view is a hairball | a giant list note or tags shown as nodes | split the list into hubs; hide tags and attachments in graph filters |
| Graph view shows islands | sections not linked from Home or hubs | `build_moc.py --all --apply`; link hubs from Home |
| Base shows no rows | a filter on a missing folder or a property name typo | the checker reports missing folders; compare names in the Properties view |
| Canvas shows "file not found" | a note was renamed outside Obsidian | rename inside Obsidian; fix the `file` path in the canvas |
| Embeds show the whole note | the heading or block in `![[Note#...]]` is gone | fix the anchor (dangling anchors finding) |
| Line endings or odd characters | CRLF or non-UTF-8 import | re-save as UTF-8 with LF; the checker flags CRLF |

## Scripts

| Symptom | Cause | Fix |
|---|---|---|
| `check_vault.py` reports hundreds of taxonomy errors | the taxonomy note does not list the tags used | add the families (with a star for open families) or map old tags to the taxonomy |
| Every note is "unreachable from Home" | `home` in `vault-config.json` does not match the Home file | set `"home": "00 Home.md"` (exact path) |
| Many orphans right after import | hubs not generated yet | `build_moc.py --all --apply`, then re-check |
| A credential finding on a placeholder | the example looks real | use an obvious placeholder (`<your-key>`, `xxxx`), never a realistic value |
| Personal-data warnings on fictional examples | numbers look like phones or IPs | use `example.com`, `192.0.2.x`, `+1 555 0100` style placeholders |
| `autolink.py` links common words | a note is named Plan, Team, Process | `--exclude "Plan,Team"`, or rename the note to something specific |
| `build_moc.py` lists internal notes in a public hub | it never does; check the hub's own zone flags | fix the hub's properties |
| `export_public.py` stops on a link | a public note links to a skipped note | fix the link, move the target to public, or use `--unlink` |
| Scripts fail on Windows paths | backslashes in arguments | quote paths; the scripts normalise separators |

## Sources and connectors

| Symptom | Cause | Fix |
|---|---|---|
| A service is not in `melaya_connector_list` | not connected | `melaya_connector_connect` link to the user, then wait ([tools.md](tools.md)) |
| A tool is refused as a write | it is not read-only, or the user lacks write permission | use read-only tools for sources; vault writes need the user's write permission and yes |
| Results stop at 25 or 100 items | paging not followed | follow cursors and tokens to the end ([extraction.md](extraction.md)) |
| 429 or "rate limited" | too many calls | back off 2, 4, 8 up to 60 s, at most 5 tries, then `failed` and move on |
| A page body is cut off | windowed reads | read with offset or cursor until done |
| Notion page shows only a preview | page tool returns a preview | read children blocks from the page id |
| Drive search misses files | the app sees only files it was granted | ask the owner to share the folder or pick the files; never widen access yourself |
| OCR text has wrong numbers | low-quality scan | verify against the image; mark `(OCR, verify)` until checked |
| Mail import is mostly noise | no label or date scope | narrow by label, participants and date; keep decisions only |
| Refresh re-reads everything | listing without revisions | include `rev` or `modified` in each listing line |
| Items "gone" after a permission change | access lost, not deletion | restore access; never retire notes for a permission change |

## Agents

| Symptom | Cause | Fix |
|---|---|---|
| The agent answers without the vault | it was not told to look | add instruction lines ([agents.md](agents.md)) |
| The agent finds the wrong note | weak title, description or lead | fix the note's title, aliases, description, first lines |
| The agent cites a stale fact | duplicates or no canonical note | one canonical note; mark the old one superseded |
| An edit is refused with a conflict | the note changed since it was read | re-read, redo the edit on the new text |
| A cloud agent cannot read the vault | the vault lives on a computer that is off, cloud reads off | turn the computer on, allow cloud reads or a cloud copy, or run the agent there |
