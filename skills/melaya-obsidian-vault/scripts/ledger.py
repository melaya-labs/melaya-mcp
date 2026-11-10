#!/usr/bin/env python3
"""Source ledger: the resumable manifest of what was read from every source, so an import
can stop and resume, refresh only what changed, find duplicates and trace any note back to
the items that fed it. Append-only JSON Lines; the newest record for (source, id) wins.
Standard library only.

Default file: <vault>/_Meta/sources/ledger.jsonl (keep it in the internal zone).

Commands (all take --vault PATH or --ledger FILE):
  plan    --source S --listing FILE.jsonl   record new or changed items as pending; report gone ones
                                            (listing lines: {"id", "title", "rev" or "modified", "url", ...})
          [--mark-gone]                     also record items missing from the listing as state "gone"
  next    --source S [--batch 25]           print the next pending (or failed, with --retry) items as JSONL
  mark    --source S --id ID --state STATE  record a state: read | written | skipped | failed | duplicate | gone
          [--rev R] [--hash H | --text-file F] [--notes "a.md,b.md"] [--reason TEXT] [--batch B] [--title T]
  seen    --source S --id ID [--rev R]      exit 0 when the item is done (read, written, skipped, duplicate)
                                            at this revision, 1 otherwise
  hash    FILE | -                          print sha256 of the normalised text (whitespace collapsed)
  dupes                                     items whose content hash is equal across sources or ids
  where   --note PATH                       items that fed one note (provenance)
  status  [--md]                            counts per source and state; --md prints a Markdown table
"""
import datetime
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib as vl  # noqa: E402

DONE = {"read", "written", "skipped", "duplicate"}
STATES = DONE | {"pending", "failed", "gone"}


def norm_hash(text):
    t = re.sub(r"\s+", " ", text).strip()
    return "sha256:" + hashlib.sha256(t.encode("utf-8")).hexdigest()


def load(path):
    latest, order = {}, []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    print(f"warning: ledger line {i} is not JSON, skipped", file=sys.stderr)
                    continue
                k = (r.get("source"), str(r.get("id")))
                if k not in latest:
                    order.append(k)
                latest[k] = {**latest.get(k, {}), **r}
    return latest, order


def append(path, rec):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    rec = {"ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **rec}
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def rev_of(item):
    return str(item.get("rev") or item.get("revision") or item.get("modified") or item.get("modifiedTime")
               or item.get("updated") or item.get("etag") or "")


def main():
    vl.utf8_stdout()
    o, pos = vl.parse_args(sys.argv[1:], flags=("md", "retry", "mark-gone"))
    if not pos:
        print(__doc__)
        return 2
    cmd = pos[0]
    path = o.get("ledger") or os.path.join(o.get("vault", "."), "_Meta", "sources", "ledger.jsonl")
    latest, order = load(path)
    src = o.get("source")

    if cmd == "hash":
        target = pos[1] if len(pos) > 1 else "-"
        text = sys.stdin.read() if target == "-" else open(target, encoding="utf-8", errors="replace").read()
        print(norm_hash(text))
        return 0

    if cmd == "plan":
        new = changed = same = 0
        seen = set()
        with open(o["listing"], encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                iid = str(item.get("id"))
                seen.add(iid)
                old = latest.get((src, iid))
                rev = rev_of(item)
                if old and old.get("state") in DONE and (not rev or rev == old.get("rev")):
                    same += 1
                    continue
                if old and old.get("state") == "pending" and rev == old.get("rev"):
                    same += 1
                    continue
                kind = "changed" if old else "new"
                new += kind == "new"
                changed += kind == "changed"
                append(path, {"source": src, "id": iid, "state": "pending", "rev": rev, "change": kind,
                              **{k: v for k, v in item.items() if k in ("title", "url", "path", "parent", "type", "size")}})
        gone = [k[1] for k, r in latest.items() if k[0] == src and k[1] not in seen and r.get("state") != "gone"]
        if o.get("mark-gone"):
            for iid in gone:
                append(path, {"source": src, "id": iid, "state": "gone", "reason": "missing from the latest listing"})
        print(f"{src}: {new} new, {changed} changed, {same} unchanged, {len(gone)} gone"
              + (" (recorded)" if o.get("mark-gone") else "") + " -> pending items recorded")
        for iid in gone[:20]:
            r = latest[(src, iid)]
            print(f"  gone: {iid} {r.get('title', '')} -> notes {r.get('notes', [])}")
        return 0

    if cmd == "next":
        want = {"pending"} | ({"failed"} if o.get("retry") else set())
        n = int(o.get("batch", 25))
        for k in order:
            r = latest[k]
            if (not src or k[0] == src) and r.get("state") in want:
                print(json.dumps(r, ensure_ascii=False))
                n -= 1
                if n == 0:
                    break
        return 0

    if cmd == "mark":
        state = o.get("state", "")
        if state not in STATES:
            print(f"state must be one of {sorted(STATES)}", file=sys.stderr)
            return 2
        rec = {"source": src, "id": str(o["id"]), "state": state}
        for k in ("rev", "reason", "batch", "title", "url", "zone", "pii"):
            if o.get(k):
                rec[k] = o[k]
        if o.get("text-file"):
            rec["hash"] = norm_hash(open(o["text-file"], encoding="utf-8", errors="replace").read())
        elif o.get("hash"):
            rec["hash"] = o["hash"]
        if o.get("notes"):
            rec["notes"] = [x.strip() for x in o["notes"].split(",") if x.strip()]
        append(path, rec)
        print(f"recorded {src}:{rec['id']} {state}")
        return 0

    if cmd == "seen":
        r = latest.get((src, str(o.get("id"))))
        ok = bool(r and r.get("state") in DONE and (not o.get("rev") or o["rev"] == r.get("rev")))
        print("seen" if ok else "not seen")
        return 0 if ok else 1

    if cmd == "dupes":
        by = {}
        for k, r in latest.items():
            if r.get("hash") and r.get("state") in DONE:
                by.setdefault(r["hash"], []).append(k)
        groups = [v for v in by.values() if len(v) > 1]
        for g in groups:
            print("same content: " + ", ".join(f"{s}:{i} ({latest[(s, i)].get('title', '')})" for s, i in g))
        print(f"{len(groups)} duplicate groups")
        return 0

    if cmd == "where":
        note = o.get("note", "")
        for k, r in latest.items():
            if note in r.get("notes", []):
                print(f"{k[0]}:{k[1]} rev {r.get('rev', '')} {r.get('title', '')} {r.get('url', '')}")
        return 0

    if cmd == "status":
        table = {}
        for (s, _), r in latest.items():
            table.setdefault(s, {}).setdefault(r.get("state"), 0)
            table[s][r.get("state")] += 1
        cols = ["pending", "read", "written", "skipped", "duplicate", "failed", "gone"]
        if o.get("md"):
            print("| Source | " + " | ".join(c.title() for c in cols) + " |")
            print("|---|" + "---|" * len(cols))
        for s, counts in sorted(table.items(), key=lambda x: str(x[0])):
            if o.get("md"):
                print(f"| {s} | " + " | ".join(str(counts.get(c, 0)) for c in cols) + " |")
            else:
                print(f"{s}: " + ", ".join(f"{c} {counts.get(c, 0)}" for c in cols if counts.get(c)))
        if not table:
            print("ledger is empty: " + path)
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
