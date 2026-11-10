#!/usr/bin/env python3
"""Add or refresh a '## Contents' outline (one [[#Heading]] link per H2) in long notes.
Placed right after '## At a glance' (or before the first H2 when there is none).
Idempotent, LF output, standard library only. Dry run unless --apply.

Usage:
  python3 add_contents.py --vault PATH [--budget-kb=8] [--min-h2=0] [--scope=FOLDER/] [--apply]

A note gets an outline when it is larger than the budget, or has at least --min-h2 H2
sections when --min-h2 is above 0. An existing outline is refreshed or, when the note no
longer qualifies, left alone (remove it by hand if you want it gone).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib as vl  # noqa: E402


def outline_for(body):
    """Return the body with a fresh Contents block, or None when there is nothing to outline."""
    base = re.sub(r"^## Contents[ \t]*\n.*?(?=^## |\Z)", "", body, count=1, flags=re.S | re.M)
    heads = [h for h in vl.h2_list(base) if h not in ("At a glance", "Contents")]
    if not heads:
        return None, base
    block = "## Contents\n\n" + "\n".join(f"- [[#{vl.heading_anchor_text(h)}]]" for h in heads) + "\n\n"
    m = re.search(r"^## At a glance[ \t]*\n.*?(?=^## |\Z)", base, re.S | re.M)
    if m:
        seg = m.group(0)
        if not seg.endswith("\n\n"):
            seg = seg.rstrip("\n") + "\n\n"
        return base[:m.start()] + seg + block + base[m.end():], base
    first = re.search(r"^## ", vl.strip_code(base, False), re.M)
    if not first:
        return None, base
    return base[:first.start()] + block + base[first.start():], base


def main():
    vl.utf8_stdout()
    o, pos = vl.parse_args(sys.argv[1:], flags=("apply",))
    root = o.get("vault") or (pos[0] if pos else ".")
    vault = vl.Vault(root)
    budget = int(o.get("budget-kb", vault.cfg["size_budget_kb"])) * 1024
    min_h2 = int(o.get("min-h2", 0))
    scope = o.get("scope", "")
    changed = 0
    for rel, n in sorted(vault.notes.items()):
        if vault.is_template(rel) or (scope and not rel.startswith(scope)) or n.type == "log":
            continue
        has = vl.section_text(n.body, "Contents") is not None
        big = len(n.raw.encode("utf-8")) > budget
        many = min_h2 and len(vl.h2_list(n.body)) >= min_h2
        if not (big or many or has):
            continue
        new_body, _ = outline_for(n.body.replace("\r\n", "\n"))
        if new_body is None or new_body == n.body:
            continue
        changed += 1
        print(("updated: " if o.get("apply") else "would update: ") + rel)
        if o.get("apply"):
            vault.write(rel, n.raw[: len(n.raw) - len(n.body)] + new_body)
    print(f"{changed} notes {'updated' if o.get('apply') else 'to update (dry run, add --apply)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
