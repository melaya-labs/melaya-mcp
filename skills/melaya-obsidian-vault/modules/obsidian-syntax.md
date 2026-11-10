# Obsidian syntax that matters for a vault

> **Use when:** writing links, embeds, callouts, diagrams, comments or HTML in notes, or checking that Markdown renders the way Obsidian expects.
> **Inputs:** a note being written ([writing.md](writing.md)).
> **Outputs:** Obsidian-correct Markdown that resolves, renders and survives export.
> **Next:** [views.md](views.md) for Bases and Canvas, [graph.md](graph.md) for link strategy.

## Links

| Form | Use |
|---|---|
| `[[Note]]` | link by name (names are unique in the vault) |
| `[[Note\|text]]` | different display text; inside a table cell escape the pipe as `\|` |
| `[[Note#Heading]]`, `[[Note#Heading#Sub]]` | deep link to a section |
| `[[Note#^block-id]]` | deep link to one paragraph, list item or table |
| `[[#Heading]]` | a section of the same note (the Contents outline uses this) |
| `[text](https://...)` | external URL; always with readable text |
| `[[Folder/Note]]` | only to break a name clash; better rename one note |

- Heading links drop the characters `: # | ^ [ ] %`: the heading `Part 1: Setup` is linked as `[[Note#Part 1 Setup]]`.
- Block ids: append ` ^id` at the end of the paragraph or list item (letters, digits, hyphens). On a table or callout, put `^id` on its own line right after it.
- Wikilinks are the default (`newLinkFormat: shortest`, `useMarkdownLinks: false`, which `scaffold.py` sets). They keep working when notes move, because Obsidian resolves by name.
- Never link to a note that does not exist. When a link must wait, write the plain name and an open question.

## Embeds (transclusion)

| Form | Shows |
|---|---|
| `![[Note]]` | the whole note inline (use sparingly) |
| `![[Note#Heading]]` | one section: reuse a procedure step or a definition |
| `![[Term#^definition]]` | one block: the canonical definition, never retyped |
| `![[diagram.png\|600]]` | an image at a width |
| `![[file.pdf#page=3]]` | a PDF at a page |
| `![[View.base]]`, `![[View.base#View name]]` | a Bases view inside a note |

Embed instead of copying: the source note stays the single place to edit.

## Callouts

```markdown
> [!note] Title
> Body text, can hold lists, links and code.

> [!faq]- Folded by default (minus) or open (plus)?
> Answer.
```

Types: `note`, `abstract` (summary, tldr), `info`, `todo`, `tip` (hint, important), `success` (check, done), `question` (help, faq), `warning` (caution, attention), `failure` (fail, missing), `danger` (error), `bug`, `example`, `quote` (cite). Use them with intent: `warning` for safety and irreversible steps, `tip` for the shortcut, `example` for worked cases, `faq` folded for Q and A, `info` for context, `quote` for verbatim source text with its citation. Callouts nest with `> >`.

## Diagrams and math

- Mermaid in a fenced block (`mermaid`): `flowchart LR` for processes, `sequenceDiagram` for exchanges, `timeline`, `gantt` for plans, `mindmap` for overviews. Quote labels with spaces or punctuation: `A["Order received"]`. Keep under about 15 nodes; split otherwise.
- LaTeX: `$inline$` and `$$block$$` for research vaults.

## Structure and text

- Headings: one `#` title per note, then `##` sections, `###` inside; never skip levels. Stable headings are citation targets: rename them only with a search for links to them.
- Lists, numbered steps, task lists `- [ ]` and `- [x]`.
- Tables need a header row and `|---|` separator; keep under about 8 columns.
- Footnotes `[^1]` for citations in long prose; inline `(source, date)` elsewhere.
- Comments `%% hidden %%` are not rendered and not exported; the strip markers (`%% private:start %%`) and generated-list markers (`%% moc:start %%`) are comments.
- Highlights `==text==`, strikethrough `~~text~~`.
- Tags in the body (`#topic/x`) are allowed but the taxonomy prefers the `tags` property.

## HTML and folding

- Obsidian renders a safe subset of HTML (`<details>`, `<sub>`, `<sup>`, `<kbd>`, `<br>`, simple tables); Markdown inside HTML blocks is not rendered. Prefer callouts and Markdown.
- Headings and list items fold in the editor; folding is not saved in the file, so never rely on it to hide content.
- Web pages can be embedded with an HTML iframe element (some sites refuse); prefer a link plus a summary.

## Files Obsidian reads

- Notes `.md`, Bases `.base` (YAML), Canvas `.canvas` (JSON Canvas), attachments (images, PDF, audio, video).
- `.obsidian/` holds settings; never put knowledge there, and leave it out of exports and Git when it holds personal workspace state (`workspace.json`).
