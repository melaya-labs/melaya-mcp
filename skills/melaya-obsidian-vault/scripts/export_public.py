#!/usr/bin/env python3
"""Export the public zone of a vault to a separate folder (for a static site, Obsidian
Publish, a shared copy, a public Git repository or a knowledge-base upload). Standard
library only. The source vault is never modified.

Usage:
  python3 export_public.py --vault PATH --out DIR [--unlink] [--drop-props owner,source_of_truth,reviewed,review_every]
                           [--no-meta] [--force]

Rules applied, in order:
  1. Skip every path in the manifest (_Meta/.publishignore) and every note whose properties
     mark it internal (publish: false, or an audience listed in zones.private_values).
  2. Drop every line between the private strip markers (markers included).
  3. Drop the listed properties (default: owner, source_of_truth, reviewed, review_every,
     open_questions, publish).
  4. Copy attachments, Canvas and Bases only when a public note uses them; a Canvas loses
     nodes that point to skipped files; _Templates always stays behind, and public _Meta notes
     (conventions, taxonomy) are exported unless --no-meta.
  5. Re-check the exported copy: a link to a note that was not exported is an error, or,
     with --unlink, becomes its plain display text. Then a secrets and deny-list scan.
Exit code 1 when the exported copy still has a dangling link or a finding.
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib as vl  # noqa: E402
from check_vault import SECRET_RE, PLACEHOLDER_RE  # noqa: E402

DEFAULT_DROP = "owner,source_of_truth,reviewed,review_every,open_questions,publish"


def drop_props(fm, keys):
    out, skip = [], False
    for line in fm.splitlines():
        m = re.match(r"^([^\s:#][^:]*?):", line)
        if m and not line.startswith((" ", "\t")):
            skip = m.group(1).strip() in keys
        if not skip:
            out.append(line)
    return "\n".join(out)


def strip_private(body, start, end):
    out, inside = [], False
    for line in body.split("\n"):
        if start in line:
            inside = True
        if not inside:
            out.append(line)
        if end in line:
            inside = False
    return "\n".join(out)


def main():
    vl.utf8_stdout()
    o, pos = vl.parse_args(sys.argv[1:], flags=("unlink", "no-meta", "force"))
    root, dest = o.get("vault"), o.get("out")
    if not root or not dest:
        print(__doc__)
        return 2
    vault = vl.Vault(root)
    z = vault.cfg["zones"]
    dest = os.path.abspath(dest)
    if dest.startswith(vault.root + os.sep) or dest == vault.root:
        print("--out must be outside the vault")
        return 2
    if os.path.exists(dest) and os.listdir(dest) and not o.get("force"):
        print(f"{dest} is not empty (add --force to write into it)")
        return 2
    keys = {k.strip() for k in o.get("drop-props", DEFAULT_DROP).split(",") if k.strip()}
    meta = (vault.cfg["meta_folder"].strip("/") + "/", vault.cfg["templates_folder"].strip("/") + "/")

    public = {r: n for r, n in vault.notes.items()
              if n.zone == "public" and not vault.is_template(r) and not (o.get("no-meta") and r.startswith(meta))}
    exported = set(public)
    used = set()
    for r, n in public.items():
        body = strip_private(n.body, z["strip_start"], z["strip_end"])
        tmp = vl.Note(r, (("---\n" + n.fm_text + "---\n") if n.has_fm else "") + body)
        for ln in vault.links(tmp):
            d, _ = vault.resolve(ln["target"], r) if ln["target"] else (None, False)
            if d and d not in vault.notes:
                used.add(d)
    for rel in vault.files:
        if rel.endswith((".canvas", ".base")) and vault.zone_of(rel) == "public" and not vault.is_template(rel):
            used.add(rel)
    files = {r for r in used if vault.zone_of(r) == "public"}
    exported |= files

    problems, written = [], 0
    for r, n in sorted(public.items()):
        body = strip_private(n.body, z["strip_start"], z["strip_end"])
        fm = drop_props(n.fm_text, keys) if n.has_fm else ""

        def fix(m, rel=r):
            inner = m.group(2)
            head, _, alias = inner.partition("|")
            tgt = head.split("#", 1)[0].rstrip("\\")
            if not tgt:
                return m.group(0)
            d, _ = vault.resolve(tgt, rel)
            if d and d in exported:
                return m.group(0)
            if o.get("unlink") and not m.group(1):
                return alias or head.split("#")[-1] or tgt
            problems.append(f"{rel}: link to a note that is not exported: {m.group(0)}")
            return m.group(0)

        body = vl.sub_outside_code(body, vl.WIKI_RE, fix)
        fm = vl.WIKI_RE.sub(fix, fm) if fm else fm
        text = (f"---\n{fm.rstrip()}\n---\n" if n.has_fm else "") + body
        for m in SECRET_RE.finditer(text):
            if not PLACEHOLDER_RE.search(m.group(0)):
                problems.append(f"{r}: credential-like string {m.group(0)[:12]}...")
        for rx in vault.cfg["denylist"] + vault.cfg["denylist_public"]:
            for m in re.finditer(rx, text, re.I):
                problems.append(f"{r}: deny-listed term {m.group(0)}")
        p = os.path.join(dest, r)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        written += 1
    for r in sorted(files):
        p = os.path.join(dest, r)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if r.endswith(".canvas"):
            data = vault.canvas(r)
            keep = [nd for nd in data.get("nodes", []) if nd.get("type") != "file"
                    or vault.by_path.get(str(nd.get("file", "")).lower()) in exported]
            ids = {nd.get("id") for nd in keep}
            data["nodes"] = keep
            data["edges"] = [e for e in data.get("edges", []) if e.get("fromNode") in ids and e.get("toNode") in ids]
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                json.dump(data, f, indent=1)
        elif r.endswith(".base"):
            internal_dirs = [x.rstrip("/") for x in vault.manifest if x.endswith("/")]
            with open(os.path.join(vault.root, r), encoding="utf-8") as f:
                lines = [ln for ln in f.read().split("\n")
                         if not ("inFolder" in ln and any(f'"{d}"' in ln for d in internal_dirs))]
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lines))  # exclusions of internal folders are dropped with the folders
        else:
            shutil.copy2(os.path.join(vault.root, r), p)
    skipped = len([r for r in vault.notes if r not in public and not vault.is_template(r)])
    print(f"Exported {written} notes and {len(files)} files to {dest}; skipped {skipped} internal or meta notes.")
    for p in problems[:50]:
        print("  ERROR " + p)
    print(f"RESULT: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
