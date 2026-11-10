#!/usr/bin/env python3
"""Generate or refresh the note list of a hub (map of content) from the notes in its folder.
The list lives between '%% moc:start %%' and '%% moc:end %%' in the hub, so hand-written
text around it is kept. One line per note: [[Note]] and its description, grouped by type
(or by any property), sub-hubs first. Dry run unless --apply. Standard library only.

Usage:
  python3 build_moc.py --vault PATH --moc "10 Company/Company.md" [--folder "10 Company"]
                       [--group-by type] [--recursive] [--apply]
  python3 build_moc.py --vault PATH --all [--recursive] [--apply]     every note with type: moc,
                                                                      over its own folder

Hubs of direct subfolders are always listed (sub-hubs first); --recursive also lists deeper
notes that have no hub of their own. Without markers the block is added as
'## Notes in this section' before '## Related'.
Internal notes are listed only in internal hubs, so a public hub never links into the
internal zone.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib as vl  # noqa: E402

START, END = "%% moc:start %%", "%% moc:end %%"
LABELS = {"moc": "Hubs", "concept": "Concepts", "process": "Processes and runbooks", "reference": "Reference",
          "decision": "Decisions", "person": "People", "team": "Teams", "project": "Projects",
          "glossary": "Glossary", "term": "Terms", "faq": "FAQ", "meeting": "Meetings", "source": "Sources",
          "log": "Logs", "meta": "About the vault", "": "Other"}


def build(vault, moc_rel, folder, group_by, recursive):
    moc = vault.notes[moc_rel]
    rows = []
    for rel, n in vault.notes.items():
        if rel == moc_rel or vault.is_template(rel):
            continue
        parent = os.path.dirname(rel)
        sub_hub = n.type == "moc" and os.path.dirname(parent) == folder  # hubs of direct subfolders, always
        if not (parent == folder or sub_hub or (recursive and rel.startswith(folder + "/"))):
            continue
        if recursive and parent != folder and n.type != "moc":
            # in recursive mode, a note under a sub-hub is listed by that sub-hub, not here
            sub_hubs = [r for r, m in vault.notes.items() if m.type == "moc" and os.path.dirname(r) == parent]
            if sub_hubs:
                continue
        if moc.zone == "public" and n.zone == "internal":
            continue
        key = str(n.props.get(group_by, "") or "")
        order = n.props.get("order", "")
        rows.append((key, int(order) if str(order).isdigit() else 9999, n.stem, n))
    if not rows:
        return "_No notes yet._"
    groups = {}
    for key, order, stem, n in rows:
        groups.setdefault(key, []).append((order, stem.lower(), n))
    keys = sorted(groups, key=lambda k: (k != "moc", LABELS.get(k, k or "~")))
    out = []
    for k in keys:
        label = LABELS.get(k, k.replace("-", " ").title()) if group_by == "type" else (k or "Other")
        out.append(f"### {label}\n")
        for _, _, n in sorted(groups[k], key=lambda x: (x[0], x[1])):
            desc = str(n.props.get("description", "") or "").strip()
            out.append(f"- [[{n.stem}]]" + (f": {desc}" if desc else ""))
        out.append("")
    return "\n".join(out).rstrip()


def apply_block(body, block):
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    new = f"{START}\n{block}\n{END}"
    if pat.search(body):
        return pat.sub(lambda m: new, body, count=1)
    section = f"## Notes in this section\n\n{new}\n\n"
    m = re.search(r"^## Related", body, re.M)
    return body[:m.start()] + section + body[m.start():] if m else body.rstrip("\n") + "\n\n" + section


def main():
    vl.utf8_stdout()
    o, pos = vl.parse_args(sys.argv[1:], flags=("apply", "all", "recursive"))
    root = o.get("vault") or (pos[0] if pos else ".")
    vault = vl.Vault(root)
    group_by = o.get("group-by", "type")
    if o.get("all"):
        targets = [(r, os.path.dirname(r)) for r, n in sorted(vault.notes.items())
                   if n.type == "moc" and not vault.is_template(r) and r != vault.cfg["home"]]
    else:
        moc = o.get("moc", "")
        if moc not in vault.notes:
            print(f"hub not found: {moc}")
            return 2
        targets = [(moc, o.get("folder", os.path.dirname(moc)))]
    changed = 0
    for moc_rel, folder in targets:
        n = vault.notes[moc_rel]
        block = build(vault, moc_rel, folder, group_by, o.get("recursive"))
        body = apply_block(n.body, block)
        if body != n.body:
            changed += 1
            print(("updated: " if o.get("apply") else "would update: ") + moc_rel)
            if o.get("apply"):
                vault.write(moc_rel, n.raw[: len(n.raw) - len(n.body)] + body)
            else:
                print("\n".join("    " + line for line in block.splitlines()[:30]))
    print(f"{changed} hubs {'updated' if o.get('apply') else 'to update (dry run, add --apply)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
