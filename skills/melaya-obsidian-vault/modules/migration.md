# Migration recipes

> **Use when:** moving a knowledge base from Notion, Confluence, Google Drive or Docs, OneNote, Evernote or a Markdown dump (Logseq, Roam, Bear, Joplin, a Git wiki, a docs site) into Obsidian.
> **Inputs:** an export file or connector access ([tools.md](tools.md)); the charter; the target sections.
> **Outputs:** the old structure mapped to sections and hubs, notes with properties and wikilinks, attachments in place, a ledger of every page, and a checker at zero errors.
> **Next:** [architecture.md](architecture.md), [graph.md](graph.md), [validation.md](validation.md); [maintenance.md](maintenance.md) when both systems stay live for a while.

## The common pipeline

1. **Freeze or date the source**: agree a cut-over date; later changes go through a refresh ([maintenance.md](maintenance.md)).
2. **Get the content**: a full export when the system offers one (faster, complete, offline), connector reads otherwise or for incremental updates. Obsidian's official Importer plugin converts several formats (Notion, Evernote, OneNote, Apple Notes, Google Keep, Bear, Roam, HTML, Markdown); use it for the raw conversion when available, then apply the rest of this pipeline.
3. **Unpack into a work folder outside the vault** and list every page into the ledger (`ledger.py plan`).
4. **Map the structure**: old spaces, notebooks, top pages or folders become sections; their children become sub-hubs or notes. Write the mapping table in the Source note before converting.
5. **Convert** (recipes below), then **normalise**: names (Title Case, unique, no ids), properties from old metadata, wikilinks from old links, attachments to `Attachments/`, callouts from panels.
6. **Clean**: drop empty and duplicate pages, archive pages older than the charter's horizon, merge stubs ([maintenance.md](maintenance.md)).
7. **Rebuild the spine**: hubs (`build_moc.py --all --apply`), Home, `autolink.py`, the checker, the graph report.
8. **Redirects**: a table in the Source note (old URL or title to new note) so people can find moved pages; aliases for old titles.

## Notion

- Export: Markdown and CSV, include subpages, "create folders for subpages". Files are named `Page Title <32 hex id>.md`; databases are a CSV plus a folder of row pages.
- Strip the id suffix from file and folder names (keep it in the ledger as the item id); resolve name clashes by qualifying titles.
- Links are URL-encoded relative paths (`Page%20Title%20<id>.md`): decode, map to the new note name, rewrite as `[[New Name]]`.
- Database columns become properties: Select and Multi-select to tags (mapped to the taxonomy) or text properties, Date to dates, Person to `owner` (role), Relation to quoted wikilinks, Status to `status` (mapped to the vault's values). Each database becomes a folder with a Base that recreates the main views.
- Callout blocks become `> [!note]`; toggles become folded callouts `> [!note]-`; synced blocks become one canonical note embedded where reused; inline databases become a Base embed.
- Connector route: `notion_search`, `notion_get_block_children` (page_id as the root block), `notion_query_database` with paging.

## Confluence

- Export: space export to HTML (or read through the API in storage format). Page tree from ancestors; labels; attachments per page.
- Each space becomes a section (or sub-section); the space home page becomes the hub; the page tree becomes folders only to the depth that helps (usually two levels), with hubs per folder.
- Macros: info, note, warning and tip panels to the matching callouts; expand to a folded callout; code to fenced blocks with the language; status lozenges to text or a property; Jira issue macros to links with the key; page-tree and children macros to the generated hub list; include-page to an embed `![[Page]]`; draw.io or Gliffy diagrams to an image plus a Mermaid redraw when they matter.
- Labels to tags through the taxonomy; page owner and last editor to `owner` (role) and `updated`.
- Comments: keep only those that record decisions, as a Decisions section with the date.
- Connector route: `confluence_list_spaces`, `confluence_list_pages` (space id), `confluence_get_page`, `confluence_get_page_children`, `confluence_get_page_labels`, `confluence_list_attachments`, `confluence_get_page_versions` for revision ids.

## Google Drive and Google Docs

- Export Docs to Markdown (or `.docx` then `pandoc -t gfm`); through the connector, `drive_export` to text or `docs_read`. Sheets to CSV per tab; Slides through `slides_read_text` with speaker notes.
- Resolve open suggestions and comments with the owner first, or note them as open questions.
- Folder tree to sections; shared drives map to sections by owner team. Shortcuts and duplicates across folders become one note.
- Heading styles must be real headings (Title, Heading 1 to 3); fake headings (bold lines) are converted by hand.
- Files that are records (contracts, invoices, signed PDFs) stay in Drive; the note links to them.

## OneNote

- No native Markdown export: use Obsidian's Importer, or read pages with the OneNote connector (`outlook_onenote_list_notebooks`, `outlook_onenote_list_pages`, `outlook_onenote_get_page_content` in HTML) and convert HTML to Markdown.
- Notebook to section, section group and section to sub-hubs, page and subpages to notes (subpages fold into their parent when short).
- Free-floating layout is flattened in reading order; ink and handwriting become an image plus OCR text marked `(OCR, verify)`; embedded files go to attachments.

## Evernote

- Export notebooks as `.enex` (XML with ENML bodies and base64 resources), or use the Importer plugin.
- Notebook and stack to sections; tags to the taxonomy (merge the long tail); created and updated dates to properties; source URL of web clips to `source_of_truth`.
- Web clips become literature or reference notes trimmed to the content; to-do checkboxes become task lists; encrypted text blocks are not imported.

## Markdown dumps (Logseq, Roam, Bear, Joplin, Git wikis, docs sites)

- Already Markdown: check link style (`[[...]]` or relative `.md` links), front matter keys, and attachment paths; normalise to this vault's properties.
- Logseq and Roam: block references `((uuid))` become block ids `^id` on the target plus `[[Note#^id]]` links; page properties `key:: value` become YAML properties; daily journal pages become a Journal folder or are mined for decisions and dropped.
- Docs sites (Docusaurus, MkDocs, GitBook): front matter `title` and `sidebar_position` to name and `order`; admonitions (`:::note`, `!!! note`) to callouts; the sidebar or nav file to hubs.
- Git wikis: `_Sidebar` to the hub; `[[Page Name]]` already compatible; images to `Attachments/`.

## Running both systems for a while

Keep the old system read-only after cut-over, or refresh from it with the ledger until it is retired. Write the cut-over date and the redirect table in the Source note; tell the team where new notes go.
