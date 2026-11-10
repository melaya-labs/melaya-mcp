# Views: Bases, Dataview and Canvas

> **Use when:** the vault needs tables or cards over its notes (review queues, project lists, glossaries, decision logs), or a visual map.
> **Inputs:** notes with consistent properties ([properties.md](properties.md)).
> **Outputs:** `.base` files in `Bases/`, optional Dataview blocks, `.canvas` maps in `Canvas/`, each linked from Home or a hub.
> **Next:** [graph.md](graph.md); [zones.md](zones.md) before any view is shared.

Views are only as good as the properties under them: one name, one type, everywhere.

## Bases (core plugin, `.base` files)

A Base is YAML: global `filters`, optional `formulas`, display names in `properties`, and one or more `views` (table, cards, list).

```yaml
filters:
  and:
    - file.ext == "md"
    - file.inFolder("50 Decisions")
    - not:
        - file.inFolder("_Templates")
properties:
  note.owner:
    displayName: Owner
views:
  - type: table
    name: Decisions by date
    filters:
      and:
        - type == "decision"
    order:
      - file.name
      - decided
      - owner
      - description
    sort:
      - property: decided
        direction: DESC
  - type: cards
    name: Open questions
    filters:
      and:
        - open_questions == true
    groupBy:
      property: note.owner
      direction: ASC
```

- Filters combine `and`, `or`, `not` over expressions: `type == "process"`, `status != "current"`, `file.hasTag("topic/onboarding")`, `file.inFolder("20 Product")`, `file.hasLink("Refill Kit")`, `file.hasProperty("review_every")`.
- `file.*` gives name, path, folder, ext, size, ctime, mtime, tags, links; `note.*` (or the bare name) is a property.
- Formulas compute columns, for example `formulas:` then `needs_review: 'if(status == "stale", "review", "")'`.
- Embed a view in a note: `![[Decisions.base#Decisions by date]]`.
- Ready-made: [../templates/bases/all-notes.base](../templates/bases/all-notes.base) (by section, by kind, hubs, recently updated) and [../templates/bases/review-queue.base](../templates/bases/review-queue.base) (oldest review first, not current, by owner, open questions).
- A public Base over the whole vault must exclude every internal folder with `not:` (the checker enforces it); a Base that lists internal notes is itself internal and goes in the manifest.
- With Melaya's vault tools, agents read rows with `obsidian_base_query` and create views with `obsidian_base_create`.

## Dataview (community plugin)

Use when the vault already relies on it or a query needs grouping Bases lacks. It renders only inside Obsidian with the plugin; exports and agents see the query text, not the result, so never put the only copy of a fact in a query.

````markdown
```dataview
TABLE owner, reviewed, status
FROM -"_Templates"
WHERE review_every AND reviewed < date(today) - dur(90 days)
SORT reviewed ASC
```
````

- `LIST`, `TABLE`, `TASK`; `FROM "folder"` or `FROM #tag`; `WHERE`, `SORT`, `GROUP BY`, `LIMIT`.
- Inline fields (`key:: value`) are Dataview-only; prefer properties so Bases, the checker and agents read the same data.
- Agents run queries with `obsidian_dataview_query` when the plugin is installed.

## Canvas (`.canvas`, JSON Canvas)

A map of the vault or of one topic: file nodes (notes, images, PDFs, Bases), text nodes, link nodes (URLs), groups and labelled edges.

```json
{
  "nodes": [
    {"id": "home", "type": "file", "file": "00 Home.md", "x": 0, "y": 0, "width": 400, "height": 100, "color": "6"},
    {"id": "g1", "type": "group", "label": "Product", "x": -460, "y": 180, "width": 900, "height": 160},
    {"id": "kit", "type": "file", "file": "20 Product/Refill Kit.md", "x": -420, "y": 220, "width": 380, "height": 90},
    {"id": "note1", "type": "text", "text": "Start with the kit.", "x": 20, "y": 220, "width": 300, "height": 90}
  ],
  "edges": [
    {"id": "e1", "fromNode": "home", "fromSide": "bottom", "toNode": "kit", "toSide": "top", "label": "main product"}
  ]
}
```

- Ids unique; every edge's `fromNode` and `toNode` exist; `file` paths are vault-relative and exact (the checker verifies all three).
- Colors: `"1"` to `"6"` (red, orange, yellow, green, cyan, purple) or a hex value.
- One global map (Home and every public hub, [../templates/canvas/home-map.canvas](../templates/canvas/home-map.canvas)) plus one map per large section. Keep 10 to 40 nodes per canvas; link canvases from their hub.
- Canvas file nodes count as links for orphans, and a public canvas never shows an internal note.
- Lay out deliberately: hub top centre, groups by section in a row, edges only where the relation is worth reading.

## Properties view and search

- The core Properties view lists every property name with its type and count: run through it after each batch to catch near-duplicates (`owner` and `owners`).
- Obsidian search understands properties: `[status:stale]`, `[type:decision] tag:#topic/pricing`, `path:"20 Product" -[audience:everyone]`.
