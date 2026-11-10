#!/usr/bin/env python3
"""Graph metrics and repair suggestions for an Obsidian vault. Read-only, standard library only.

Usage:
  python3 graph_report.py --vault PATH [--min-links 3] [--json=REPORT.json] [--md=REPORT.md] [--top 15]

Reports: notes, links, average links per note, connected components, hop histogram from
Home, orphans (no inbound link), dead ends (no outbound link), weakly linked notes (fewer
than --min-links distinct links in and out), top hubs by inbound links, notes that do not
link up to the hub of their folder, hubs that do not list every note of their folder,
and the section-to-section link matrix (which sections never talk to each other).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib as vl  # noqa: E402


def top_section(rel):
    return rel.split("/", 1)[0] if "/" in rel else "(root)"


def main():
    vl.utf8_stdout()
    o, pos = vl.parse_args(sys.argv[1:])
    root = o.get("vault") or (pos[0] if pos else ".")
    vault = vl.Vault(root)
    min_links = int(o.get("min-links", 3))
    top = int(o.get("top", 15))
    out, inn, problems = vault.graph()
    notes = [r for r in vault.notes if not vault.is_template(r)]
    note_set = set(notes)
    edges = sum(len([d for d in out.get(r, ()) if d in note_set]) for r in notes)
    dist = vault.hops(out)

    # undirected components over notes
    adj = {r: set() for r in notes}
    for r in notes:
        for d in out.get(r, ()):
            if d in note_set:
                adj[r].add(d)
                adj[d].add(r)
    seen, comps = set(), []
    for r in notes:
        if r in seen:
            continue
        stack, comp = [r], []
        seen.add(r)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(comp)
    comps.sort(key=len, reverse=True)

    hist = {}
    for r in notes:
        h = dist.get(r, "unreachable")
        hist[h] = hist.get(h, 0) + 1
    orphans = [r for r in notes if r != vault.cfg["home"] and not (inn.get(r, set()) - {r})]
    dead_ends = [r for r in notes if not [d for d in out.get(r, ()) if d != r]]
    weak = [r for r in notes if len((out.get(r, set()) | inn.get(r, set())) - {r}) < min_links]
    hubs = sorted(notes, key=lambda r: -len(inn.get(r, ())))[:top]

    # hub coverage: each folder's hub (type moc in that folder)
    hub_of = {}
    for r in notes:
        if vault.notes[r].type == "moc":
            hub_of.setdefault(os.path.dirname(r), r)
    no_uplink, not_listed = [], []
    for r in notes:
        folder = os.path.dirname(r)
        h = hub_of.get(folder)
        if not h or h == r:
            continue
        if h not in out.get(r, set()):
            no_uplink.append((r, h))
        if r not in out.get(h, set()) and not (vault.notes[h].zone == "public" and vault.notes[r].zone == "internal"):
            not_listed.append((h, r))

    sections = sorted({top_section(r) for r in notes})
    matrix = {a: {b: 0 for b in sections} for a in sections}
    for r in notes:
        for d in out.get(r, ()):
            if d in note_set:
                matrix[top_section(r)][top_section(d)] += 1
    internal_sections = {s for s in sections if all(vault.notes[r].zone == "internal" for r in notes if top_section(r) == s)}
    skip = {"(root)", vault.cfg["meta_folder"]} | internal_sections  # public notes never link into internal sections
    silent = [(a, b) for a in sections for b in sections
              if a < b and not matrix[a][b] and not matrix[b][a] and a not in skip and b not in skip]

    rep = {
        "notes": len(notes), "links": edges, "avg_links_per_note": round(edges / max(1, len(notes)), 2),
        "components": len(comps), "largest_component": len(comps[0]) if comps else 0,
        "isolated_groups": [c for c in comps[1:6]],
        "hops_from_home": {str(k): v for k, v in sorted(hist.items(), key=lambda kv: (isinstance(kv[0], str), kv[0]))},
        "max_hops": max(dist.values()) if dist else None,
        "orphans": orphans, "dead_ends": dead_ends, "weakly_linked": weak,
        "top_hubs": [{"note": r, "inbound": len(inn.get(r, ()))} for r in hubs],
        "missing_uplink": [{"note": r, "hub": h} for r, h in no_uplink],
        "hub_missing_note": [{"hub": h, "note": r} for h, r in not_listed],
        "unresolved_links": len(problems),
        "sections_never_linked": [f"{a} <-> {b}" for a, b in silent],
        "section_matrix": matrix,
    }
    lines = [
        "# Graph report", "",
        f"- Notes {rep['notes']}, links {rep['links']}, {rep['avg_links_per_note']} links per note on average.",
        f"- Components {rep['components']} (largest {rep['largest_component']}). Max hops from Home {rep['max_hops']}.",
        f"- Hops from Home: " + ", ".join(f"{k}: {v}" for k, v in rep["hops_from_home"].items()),
        f"- Orphans {len(orphans)}, dead ends {len(dead_ends)}, weakly linked (<{min_links}) {len(weak)}, unresolved links {len(problems)}.",
        f"- Notes not linking up to their hub {len(no_uplink)}, notes missing from their hub {len(not_listed)}.",
        "", "## Top hubs", ""] + [f"- {h['note']}: {h['inbound']} inbound" for h in rep["top_hubs"]]
    for title, items in (("Orphans", orphans), ("Dead ends", dead_ends), ("Weakly linked", weak),
                         ("Missing up-link to hub", [f"{x['note']} -> {x['hub']}" for x in rep["missing_uplink"]]),
                         ("Hub does not list", [f"{x['hub']} misses {x['note']}" for x in rep["hub_missing_note"]]),
                         ("Sections that never link to each other", rep["sections_never_linked"])):
        if items:
            lines += ["", f"## {title} ({len(items)})", ""] + [f"- {x}" for x in items[:50]]
    lines += ["", "## Section link matrix (rows link to columns)", "",
              "| from \\ to | " + " | ".join(sections) + " |", "|---|" + "---|" * len(sections)]
    for a in sections:
        lines.append(f"| {a} | " + " | ".join(str(matrix[a][b]) for b in sections) + " |")
    text = "\n".join(lines) + "\n"
    print(text)
    if o.get("json"):
        with open(o["json"], "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=1)
    if o.get("md"):
        with open(o["md"], "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
