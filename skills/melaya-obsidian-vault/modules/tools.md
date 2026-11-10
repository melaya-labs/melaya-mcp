# Tools: reading sources and writing the vault

> **Use when:** you need to know what this host can do: which connectors are reachable, whether a vault is connected, whether there is a shell, and which write path to use.
> **Inputs:** the host (MCP tools listed, shell or not, files available).
> **Outputs:** a tool status line in the charter: read paths per source, the write path, the scripts available.
> **Next:** [sources.md](sources.md).

## Detect

1. Melaya MCP present (tools named `melaya_*`): call `melaya_setup_status`, then `melaya_connector_list` (connected services and read tool counts). The `melaya` skill covers setup and connecting a service.
2. A vault connected to Melaya: `melaya_connector_tools` with `search` = "obsidian" lists the `obsidian_*` tools when the user has a personal vault.
3. A shell: run `python3 --version` (3.8 or newer runs every script) and check the vault folder is writable.
4. None of these: chat-only mode (end of this page).

## Reading sources through Melaya connectors

- Find tools: `melaya_connector_tools` with `search` (plain words, for example "notion page read") or `service`. Results are marked `[read-only]` or `[write]`; use only `[read-only]` tools. Pass `tool` = an exact name to get its full parameter list before the first call.
- Call: `melaya_connector_call` with `service`, `tool` and `args`. Read-only calls need only the user's `melaya:connectors` permission.
- A service missing from `melaya_connector_list` is not connected: give the user the link from `melaya_connector_connect` and wait. Never look for a workaround.
- Tool names change; the ones below are examples seen in the catalog. Confirm each with `melaya_connector_tools` first.

| Source | Typical read tools (confirm first) |
|---|---|
| Google Drive | `drive_search`, `drive_list`, `drive_export` (Docs, Sheets, Slides to txt, csv, pdf), `drive_download` (PDF, Office, images) |
| Google Docs, Sheets, Slides | `docs_read`, `sheets_list_tabs`, `sheets_read_range`, `slides_read_text` (with speaker notes) |
| Notion | `notion_search`, `notion_get_page`, `notion_get_block_children`, `notion_query_database` |
| Confluence | `confluence_list_spaces`, `confluence_list_pages`, `confluence_get_page`, `confluence_get_page_children`, `confluence_get_page_labels`, `confluence_list_attachments`, `confluence_search` (CQL) |
| OneNote | `outlook_onenote_list_notebooks`, `outlook_onenote_list_pages`, `outlook_onenote_get_page_content` |
| Gmail, Outlook, Zoho Mail | `gmail_search`, `gmail_get_thread`, `gmail_get_attachments`; `outlook_get_conversation`, `outlook_get_message`; the `zoho_mail` read tools |
| Slack, Teams | `slack_list_channels`, `slack_get_messages`; `teams_list_channels`, `teams_read_channel_messages`, `teams_read_chat_messages` |
| Jira, GitHub | `jira_search_issues` (JQL), `jira_get_issue`, `jira_get_comments`; `github_list_repos`, `github_get_file`, `github_list_issues` |
| Local files on the runner | `file_read` (text and PDF) |

Connector reads are bounded (pages, character windows, row ranges). Page through them as [extraction.md](extraction.md) describes.

## Writing the vault through Melaya's vault tools

A vault connected in Melaya (a folder on the user's computer read through the runner, an uploaded copy, or a Git repository) exposes `obsidian_*` tools to agents and, for personal vaults, over MCP through `melaya_connector_call` with `vault` named on every call (`obsidian_vaults` lists them).

| Need | Tools |
|---|---|
| Orient | `obsidian_overview`, `obsidian_folders`, `obsidian_files`, `obsidian_tags`, `obsidian_properties`, `obsidian_aliases` |
| Find and read | `obsidian_search` (Obsidian search syntax), `obsidian_search_context` (path#heading:line), `obsidian_read` (pages of about 9,000 characters with a revision; `section` = "#Heading" or "^block"), `obsidian_document_map`, `obsidian_outline` |
| Graph | `obsidian_links`, `obsidian_backlinks`, `obsidian_orphans`, `obsidian_deadends`, `obsidian_unresolved` |
| Views | `obsidian_bases`, `obsidian_base_views`, `obsidian_base_query`, `obsidian_canvas_read`, `obsidian_dataview_query` (Dataview installed) |
| Change tracking | `obsidian_modified` (since a time), `obsidian_changes` (journal with a cursor) |
| Write (approval per edit) | `obsidian_create` (refuses an existing path unless `overwrite`), `obsidian_patch` (one heading, block or property: append, prepend, replace, delete), `obsidian_append`, `obsidian_prepend`, `obsidian_property_set`, `obsidian_property_remove`, `obsidian_rename` and `obsidian_move` (links updated), `obsidian_base_create`, `obsidian_canvas_write` |

Rules: pass `expected_revision` from your last read on every edit; a `conflict` means re-read and redo, never overwrite. Over MCP each write runs at once with no approval card and needs `melaya:connectors.write`: show the exact change and get the user's yes first. For a large first build, write files on disk (or a copy) and let the user connect or upload the finished vault; use the vault tools for incremental edits afterwards.

## Writing with files (no Melaya, or a first build)

Write UTF-8 Markdown with LF line endings, one file per note, at the path the architecture gives. Never overwrite an existing note without a diff and a yes. The scripts in `../scripts/` need only Python 3.8+:

| Script | Does |
|---|---|
| `scaffold.py` | the vault skeleton that already passes the checker |
| `ledger.py` | the source ledger: plan, next batch, mark, seen, dupes, where, status |
| `build_moc.py` | hub note lists between `%% moc:start %%` and `%% moc:end %%` |
| `autolink.py` | unlinked mentions of titles and aliases, first mention linked |
| `add_contents.py` | `## Contents` outlines on long notes |
| `check_vault.py` | every rule in [validation.md](validation.md) |
| `graph_report.py` | graph metrics and repair suggestions |
| `export_public.py` | the public zone exported and re-checked |

## Chat only (no shell, no vault tools)

Still run the method: write the charter, ask the user to paste or attach sources (or exports), and return notes as complete Markdown blocks with their file paths, plus `Home`, hubs and `_Meta` notes. Walk the manual checklist in [validation.md](validation.md). Never claim a file was written or a check was run.
