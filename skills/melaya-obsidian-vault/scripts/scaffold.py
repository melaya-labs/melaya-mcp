#!/usr/bin/env python3
"""Create the skeleton of a new Obsidian vault that already passes check_vault.py:
Home, one hub per section, the _Meta notes (conventions, tag taxonomy, editing protocol,
changelog, source ledger, charter), vault-config.json, the .publishignore manifest, the
note templates in _Templates/, two Bases, a Canvas map, an Attachments folder and a
minimal .obsidian config (only when the vault has none). Existing files are never
overwritten unless --force. Standard library only.

Usage:
  python3 scaffold.py --vault PATH --name "Vault name" --sections "10 Company,20 Product,90 Reference"
                      [--internal "80 Operations"] [--owner "vault owner"] [--languages en,fr]
                      [--today YYYY-MM-DD] [--force] [--dry-run]

Sections are "NN Name" (numbered folders sort in reading order); a name without a number is
numbered 10, 20, 30... Internal sections get publish: false, audience: internal, and their
folders go in the manifest; Home links them only between the private strip markers.
"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib as vl  # noqa: E402

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(SKILL, "templates")


def read_tpl(*parts):
    with open(os.path.join(TPL, *parts), encoding="utf-8") as f:
        return f.read()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def parse_sections(spec, start=10):
    out, n = [], start
    for raw in [s.strip() for s in spec.split(",") if s.strip()]:
        m = re.match(r"^(\d{2})\s+(.+)$", raw)
        num, name = (m.group(1), m.group(2)) if m else ("%02d" % n, raw)
        n = int(num) + 10
        out.append({"num": num, "name": name, "folder": f"{num} {name}", "slug": slug(name)})
    return out


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def main():
    vl.utf8_stdout()
    o, pos = vl.parse_args(sys.argv[1:], flags=("force", "dry-run"))
    root = o.get("vault") or (pos[0] if pos else "")
    if not root or not o.get("sections"):
        print(__doc__)
        return 2
    name = o.get("name") or os.path.basename(os.path.abspath(root))
    owner = o.get("owner", "vault owner")
    today = o.get("today") or datetime.date.today().isoformat()
    langs = [x.strip() for x in o.get("languages", "en").split(",") if x.strip()]
    public = parse_sections(o["sections"])
    internal = parse_sections(o.get("internal", ""), start=80) if o.get("internal") else []
    for s in public:
        s["internal"] = False
    for s in internal:
        s["internal"] = True
    sections = sorted(public + internal, key=lambda s: s["num"])
    home_stem = "00 Home"
    files = {}

    # ---------------------------------------------------------------- Home
    rows = "\n".join(f"| **{s['name']}** | <one line: what it holds> | [[{s['name']}]] |" for s in public)
    priv = ", ".join([f"[[{s['name']}]]" for s in internal] + ["[[Source Ledger]]", "[[Review Queue.base|Review queue]]"])
    files[home_stem + ".md"] = f"""---
type: moc
description: The entry point of the {name} vault, linking every section, the shared views and the rules of the vault.
tags:
  - area/home
aliases:
  - Home
  - Start here
related:
  - "[[Vault Conventions]]"
audience: everyone
owner: {owner}
status: current
updated: {today}
---

# {name}

<Two sentences: what this vault is, who it is for, and the first note to read.>

> [!tip] New here?
> Pick a section below. Every note is at most three links from this page, and [[Vault Conventions]] explains how the vault works.

## At a glance

- <What the organisation, project or research is, in one line.>
- Sections: {", ".join(f"[[{s['name']}]]" for s in public)}.
- Change something: follow [[Editing Protocol]], log it in [[Vault Changelog]].

## Sections

| Section | What it holds | Start at |
|---|---|---|
{rows}

## Views

- [[All Notes.base|All notes]] (by section, by kind, recently updated)
- [[Home Map.canvas|Vault map]]

## About this vault

- [[Vault Charter]], [[Vault Conventions]], [[Tag Taxonomy]], [[Editing Protocol]], [[Vault Changelog]]

%% private:start %%
## Internal

- {priv}
%% private:end %%
"""

    # ---------------------------------------------------------------- hubs
    for i, s in enumerate(sections):
        peers = [p for p in sections if p is not s and p["internal"] == s["internal"]][:2]
        zone = ("audience: internal\npublish: false\n" if s["internal"] else "audience: everyone\n")
        tags = ("  - area/internal\n  - zone/internal\n" if s["internal"] else f"  - area/{s['slug']}\n")
        review = f"reviewed: {today}\nreview_every: 90d\n"
        related = "\n".join(f"- [[{p['name']}]]" for p in peers)
        files[f"{s['folder']}/{s['name']}.md"] = f"""---
type: moc
description: The hub of the {s['name']} section, linking every note in it, grouped by kind.
tags:
{tags}related:
  - "[[{home_stem}]]"
{zone}owner: {owner}
status: current
updated: {today}
{review}---

# {s['name']}

<One or two sentences: what lives in this section and how it is organised.>

## At a glance

- <The note most readers need first.>
- <How the section is split: by product, client, process or topic.>
- Back to [[{home_stem}]].

## Notes in this section

%% moc:start %%
_No notes yet._
%% moc:end %%

## Related

- [[{home_stem}]]
{related}
"""

    # ---------------------------------------------------------------- _Meta
    def hub_ref(s):  # public notes never link into the internal zone
        return s["name"] + " (internal)" if s["internal"] else "[[" + s["name"] + "]]"

    sec_table = "| Folder | Holds | Hub | Zone |\n|---|---|---|---|\n" + "\n".join(
        f"| `{s['folder']}/` | <what it holds> | {hub_ref(s)} | {'internal' if s['internal'] else 'public'} |"
        for s in public) + ("\n| Internal folders | Listed in `_Meta/.publishignore`, never named in public notes | the internal hubs | internal |" if internal else "") + "\n| `_Meta/` | Conventions, taxonomy, protocol, changelog, sources, config | [[Vault Conventions]] | public, sources internal |" \
        "\n| `_Templates/` | One template per note type | none | not a note folder |" \
        "\n| `Bases/`, `Canvas/`, `Attachments/` | Views, maps, files embedded by notes | [[" + home_stem + "]] | follows the notes |"
    area_rows = "| Tag | Section |\n|---|---|\n| `area/home` | Home |\n| `area/meta` | `_Meta/` |\n" + "\n".join(
        f"| `area/{s['slug']}` | {hub_ref(s)} |" for s in public) + \
        ("\n| `area/internal` | Every note in an internal folder |" if internal else "") + \
        "\n| `area/people` | People and team notes, wherever they live |\n| `area/reference` | Glossary, terms and fact sheets, wherever they live |"
    if len(langs) == 1:
        lang_line = f"Language: `{langs[0]}` for every note."
    else:
        lang_line = (f"Primary language `{langs[0]}`; other languages {', '.join('`' + x + '`' for x in langs[1:])}. "
                     "Each translated note carries `lang` and `translation_of` properties and a language tag.")
    values = {"vault": name, "home": home_stem, "owner": owner, "date": today, "max_hops": "3",
              "sections_table": sec_table, "area_tags": area_rows, "languages": lang_line,
              "write_folders": ", ".join(f"`{s['folder']}/`" for s in public) + (", and the internal folders" if internal else "")}
    for src, dst in (("conventions.md", "Vault Conventions.md"), ("tag-taxonomy.md", "Tag Taxonomy.md"),
                     ("editing-protocol.md", "Editing Protocol.md"), ("changelog.md", "Vault Changelog.md"),
                     ("source-ledger.md", "Source Ledger.md")):
        files["_Meta/" + dst] = fill(read_tpl("meta", src), values)
    charter = read_tpl("vault-charter.md").replace("<Home note>", home_stem).replace("<YYYY-MM-DD>", today)
    files["_Meta/Vault Charter.md"] = charter.replace("<vault owner>", owner)

    cfg = json.loads(read_tpl("meta", "vault-config.json"))
    cfg["home"] = home_stem + ".md"
    cfg["zones"]["leak_allowed"] = [home_stem + ".md"]
    files["_Meta/vault-config.json"] = json.dumps(cfg, indent=2) + "\n"
    manifest_paths = "\n".join(s["folder"] + "/" for s in internal)
    files["_Meta/.publishignore"] = fill(read_tpl("meta", "publishignore.txt"), {"internal_paths": manifest_paths}).rstrip() + "\n"
    files["_Meta/sources/ledger.jsonl"] = ""

    # ---------------------------------------------------------------- templates, bases, canvas
    for f in sorted(os.listdir(os.path.join(TPL, "notes"))):
        if f.endswith(".md"):
            files["_Templates/" + f[:-3].replace("-", " ").title() + " Template.md"] = read_tpl("notes", f)
    excl = "\n".join(f'        - file.inFolder("{s["folder"]}")' for s in internal)
    files["Bases/All Notes.base"] = read_tpl("bases", "all-notes.base").replace("{{exclude}}\n", excl + "\n" if excl else "")
    files["Bases/Review Queue.base"] = read_tpl("bases", "review-queue.base")
    nodes = [{"id": "home", "type": "file", "file": home_stem + ".md", "x": 0, "y": 0, "width": 400, "height": 100, "color": "6"},
             {"id": "title", "type": "text", "text": f"# {name} map\nEvery public hub, one click from Home.",
              "x": -480, "y": 0, "width": 420, "height": 100}]
    edges = []
    w = 420
    x0 = -((len(public) - 1) * w) // 2
    for i, s in enumerate(public):
        nid = "hub" + s["num"]
        nodes.append({"id": nid, "type": "file", "file": f"{s['folder']}/{s['name']}.md",
                      "x": x0 + i * w - 190, "y": 220, "width": 380, "height": 90, "color": "4"})
        edges.append({"id": "e" + s["num"], "fromNode": "home", "fromSide": "bottom", "toNode": nid, "toSide": "top"})
    files["Canvas/Home Map.canvas"] = json.dumps({"nodes": nodes, "edges": edges}, indent=1) + "\n"
    if not os.path.isdir(os.path.join(root, ".obsidian")):
        files[".obsidian/app.json"] = json.dumps({"attachmentFolderPath": "Attachments", "newLinkFormat": "shortest",
                                                  "useMarkdownLinks": False, "alwaysUpdateLinks": True,
                                                  "showUnsupportedFiles": False}, indent=2) + "\n"
        files[".obsidian/templates.json"] = json.dumps({"folder": "_Templates", "dateFormat": "YYYY-MM-DD"}, indent=2) + "\n"

    # ---------------------------------------------------------------- write
    made, kept = [], []
    for rel, text in files.items():
        p = os.path.join(root, rel)
        if os.path.exists(p) and not o.get("force"):
            kept.append(rel)
            continue
        made.append(rel)
        if not o.get("dry-run"):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    if not o.get("dry-run"):
        os.makedirs(os.path.join(root, "Attachments"), exist_ok=True)
    print(("Would create" if o.get("dry-run") else "Created") + f" {len(made)} files in {os.path.abspath(root)}")
    for r in made:
        print("  + " + r)
    for r in kept:
        print("  = kept existing " + r)
    print("Next: fill the charter and hubs, then run check_vault.py --vault " + root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
