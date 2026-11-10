#!/usr/bin/env python3
"""Find unlinked mentions of note titles and aliases (glossary auto-linking) and, with
--apply, link the first mention in each note. Skips properties, headings, code, comments,
existing links, URLs, tags, generated hub lists, meta and log notes (unless --include-meta)
and the target note itself. A public note is never linked to
an internal note. Dry run unless --apply. Standard library only.

Usage:
  python3 autolink.py --vault PATH [--types term,concept,person,project] [--folder "90 Reference"]
                      [--min-len 4] [--scope FOLDER/] [--max 200] [--apply]

--types / --folder choose which notes are link targets (default: term, concept, glossary,
person, team, project). Matching is case-insensitive on whole words; an alias or a
different case is linked as [[Title|text as written]]. Review the dry run first: common
words used as titles (Plan, Team) are better added to --exclude "Plan,Team".
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib as vl  # noqa: E402

PROTECT = re.compile(r"(!?\[\[[^\]]*\]\]|\[[^\]]*\]\([^)]*\)|https?://\S+|`[^`]*`|%%.*?%%|(?<![\w])#[\w/-]+|<[^>]+>)")


def protected_spans(line):
    return [(m.start(), m.end()) for m in PROTECT.finditer(line)]


def main():
    vl.utf8_stdout()
    o, pos = vl.parse_args(sys.argv[1:], flags=("apply", "include-meta"))
    root = o.get("vault") or (pos[0] if pos else ".")
    vault = vl.Vault(root)
    types = set((o.get("types") or "term,concept,glossary,person,team,project").split(","))
    folder = o.get("folder", "")
    min_len = int(o.get("min-len", 4))
    exclude = {x.strip().lower() for x in o.get("exclude", "").split(",") if x.strip()}
    scope = o.get("scope", "")
    cap = int(o.get("max", 200))

    terms = []  # (term, target stem, target rel)
    for rel, n in vault.notes.items():
        if vault.is_template(rel):
            continue
        if (folder and rel.startswith(folder)) or (not folder and n.type in types):
            for t in [n.stem] + n.aliases():
                if len(t) >= min_len and t.lower() not in exclude:
                    terms.append((t, n.stem, rel))
    terms.sort(key=lambda x: -len(x[0]))
    if not terms:
        print("no link targets found (check --types or --folder)")
        return 0
    rx = re.compile(r"(?<![\w\[|#/])(" + "|".join(re.escape(t[0]) for t in terms) + r")(?![\w\]])", re.I)
    lookup = {t[0].lower(): t for t in terms}

    total, changed_notes = 0, 0
    for rel, n in sorted(vault.notes.items()):
        if vault.is_template(rel) or (scope and not rel.startswith(scope)):
            continue
        if n.type in ("meta", "log") and not o.get("include-meta"):
            continue
        linked = {vault.resolve(ln["target"], rel)[0] for ln in vault.links(n)}
        done = set()
        lines = n.body.split("\n")
        fence = generated = False
        edits = 0
        for i, line in enumerate(lines):
            if re.match(r"^\s*(```|~~~)", line):
                fence = not fence
                continue
            if "%% moc:start %%" in line:
                generated = True
            if "%% moc:end %%" in line:
                generated = False
                continue
            if fence or generated or re.match(r"^\s*#{1,6}\s", line) or line.lstrip().startswith(("|---", "> [!")):
                continue
            spans = protected_spans(line)
            out, last = [], 0
            for m in rx.finditer(line):
                if any(a <= m.start() < b for a, b in spans):
                    continue
                term, stem, trel = lookup[m.group(1).lower()]
                if trel == rel or trel in linked or trel in done:
                    continue
                if n.zone == "public" and vault.notes[trel].zone == "internal":
                    continue
                text = m.group(1)
                link = f"[[{stem}]]" if text == stem else f"[[{stem}|{text}]]"
                print(f"{rel}:{i + 1 + n.fm_lines}: {text} -> {link}")
                done.add(trel)
                total += 1
                edits += 1
                out.append(line[last:m.start()] + link)
                last = m.end()
                if total >= cap:
                    break
            if out:
                lines[i] = "".join(out) + line[last:]
            if total >= cap:
                break
        if edits and o.get("apply"):
            vault.write(rel, n.raw[: len(n.raw) - len(n.body)] + "\n".join(lines))
            changed_notes += 1
        if total >= cap:
            print(f"stopped at --max {cap}")
            break
    print(f"{total} links {'added in ' + str(changed_notes) + ' notes' if o.get('apply') else 'suggested (dry run, add --apply)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
