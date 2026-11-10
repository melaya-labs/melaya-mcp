"""Shared helpers for the melaya-obsidian-vault scripts. Python 3.8+, standard library only.

Reads an Obsidian vault the way Obsidian resolves it: notes (.md), wikilinks and embeds
([[Note]], [[Note#Heading]], [[Note#^block]], [[Note|text]], ![[Note]]), Markdown links to
local files, links inside properties, headings, block ids, tags, aliases, Canvas and Bases.
Configuration comes from <vault>/_Meta/vault-config.json (every key optional, see DEFAULTS).
"""
import datetime
import json
import os
import re
import sys
import urllib.parse

DEFAULTS = {
    "home": "00 Home.md",
    "max_hops": 3,
    "meta_folder": "_Meta",
    "templates_folder": "_Templates",
    "attachments_folder": "Attachments",
    "ignore_dirs": [".obsidian", ".git", ".trash", "node_modules", ".venv"],
    "ignore_paths": ["_Meta/sources/"],
    "required_properties": ["type", "description", "tags", "updated"],
    "required_by_zone": {"internal": ["owner", "status", "reviewed", "review_every"]},
    "types": ["moc", "concept", "process", "reference", "decision", "person", "team", "project",
              "glossary", "term", "faq", "meeting", "source", "log", "meta"],
    "statuses": ["draft", "current", "stale", "superseded", "archived"],
    "audiences": [],
    "sections": {
        "*": ["At a glance", "Related"],
        "moc": ["At a glance"],
        "decision": ["At a glance", "Context", "Decision", "Consequences", "Related"],
        "process": ["At a glance", "Steps", "Related"],
        "meeting": ["At a glance", "Decisions", "Actions", "Related"],
        "glossary": ["Terms"],
        "log": ["Log"],
        "meta": [],
    },
    "glance_bullets": [3, 7],
    "description_max": 200,
    "size_budget_kb": 8,
    "contents_level": "WARN",
    "taxonomy_note": "_Meta/Tag Taxonomy.md",
    "tag_patterns": [],
    "banned": {"em_dash": True, "en_dash_separator": True, "semicolon": False, "exclamation": False,
               "custom": []},
    "zones": {
        "default": "public",
        "manifest": "_Meta/.publishignore",
        "private_values": {"publish": ["false"], "audience": ["internal", "private", "confidential"]},
        "strip_start": "%% private:start %%",
        "strip_end": "%% private:end %%",
        "leak_allowed": ["00 Home.md"],
    },
    "pii": {"email_allow": ["example.com", "example.org", "example.net"], "phone": "WARN", "ip": "WARN",
            "national_id": "WARN"},
    "denylist": [],
    "denylist_public": [],
    "orphan_exempt": [],
    "attachment_max_mb": 20,
}

FENCE_RE = re.compile(r"^[ \t]*(```+|~~~+)[^\n]*\n.*?^[ \t]*\1[ \t]*$", re.S | re.M)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
COMMENT_RE = re.compile(r"%%.*?%%", re.S)
WIKI_RE = re.compile(r"(!?)\[\[([^\[\]\n]+?)\]\]")
MD_LINK_RE = re.compile(r"(!?)\[([^\]\n]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
BLOCK_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9-]+)\s*$")
TAG_RE = re.compile(r"(?<![\w/#&\[(])#([A-Za-z0-9_\-/]*[A-Za-z_\-/][A-Za-z0-9_\-/]*)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def merge(base, over):
    out = dict(base)
    for k, v in (over or {}).items():
        out[k] = merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out


def load_config(vault, path=None):
    path = path or os.path.join(vault, "_Meta", "vault-config.json")
    cfg = DEFAULTS
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            cfg = merge(DEFAULTS, json.load(f))
    return cfg


def parse_args(argv, flags=()):
    """--key=value and --flag arguments, plus positionals. Returns (opts, positionals)."""
    opts, pos = {}, []
    it = iter(argv)
    for a in it:
        if a.startswith("--"):
            if "=" in a:
                k, v = a[2:].split("=", 1)
                opts[k] = v
            elif a[2:] in flags:
                opts[a[2:]] = True
            else:
                opts[a[2:]] = next(it, "")
        else:
            pos.append(a)
    return opts, pos


def utf8_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


# ---------------------------------------------------------------- frontmatter

def _scalar(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def _inline_list(v):
    inner = v.strip()[1:-1]
    items, cur, q = [], "", None
    for ch in inner:
        if q:
            cur += ch
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            cur += ch
        elif ch == ",":
            items.append(_scalar(cur))
            cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(_scalar(cur))
    return [i for i in items if i != ""]


def split_frontmatter(text):
    """Return (frontmatter_text or None, body, frontmatter_line_count)."""
    m = re.match(r"---[ \t]*\r?\n(.*?\r?\n)?---[ \t]*(\r?\n|$)", text, re.S)
    if not m:
        return None, text, 0
    fm = m.group(1) or ""
    return fm, text[m.end():], text[:m.end()].count("\n")


def parse_frontmatter(fm):
    """Small YAML subset: scalars, quoted strings, inline [a, b] lists, block lists, block scalars.
    Nested maps are kept as their raw text. Values are strings or lists of strings."""
    props, key, block = {}, None, False
    for line in (fm or "").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        km = re.match(r"^([^\s:#][^:]*?):(?:\s+(.*))?$", line)
        if km and not line.startswith((" ", "\t")):
            key, val = km.group(1).strip(), (km.group(2) or "").strip()
            block = val in ("|", ">", "|-", ">-")
            if block:
                props[key] = ""
            elif val.startswith("[") and val.endswith("]"):
                props[key] = _inline_list(val)
            else:
                props[key] = _scalar(val) if val else []
            continue
        if key is None:
            continue
        lm = re.match(r"^\s+-\s*(.*)$", line)
        if lm and not block:
            if not isinstance(props[key], list):
                props[key] = [] if props[key] in ("", []) else [props[key]]
            props[key].append(_scalar(lm.group(1)))
        elif block or line.startswith((" ", "\t")):
            prev = props[key] if isinstance(props[key], str) else ""
            props[key] = (prev + "\n" + line.strip()).strip()
    return props


def as_list(v):
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def truthy(v):
    return str(v).strip().lower() in ("true", "yes", "1")


def to_date(v):
    try:
        return datetime.date.fromisoformat(str(v).strip()[:10]) if DATE_RE.match(str(v).strip()[:10]) else None
    except ValueError:
        return None


def period_days(v):
    m = re.fullmatch(r"(\d+)\s*([dwmy])", str(v).strip().lower())
    return int(m.group(1)) * {"d": 1, "w": 7, "m": 30, "y": 365}[m.group(2)] if m else None


# ---------------------------------------------------------------- text helpers

def blank_keep_lines(m):
    return "\n" * m.group(0).count("\n")


def strip_code(text, comments=True):
    """Remove fenced code, inline code and (optionally) %% comments %%, keeping line numbers."""
    text = FENCE_RE.sub(blank_keep_lines, text)
    text = INLINE_CODE_RE.sub("``", text)
    if comments:
        text = COMMENT_RE.sub(blank_keep_lines, text)
    return text


CODE_SPAN_RE = re.compile(FENCE_RE.pattern + r"|`[^`\n]*`", re.S | re.M)


def sub_outside_code(text, rx, fn):
    """rx.sub(fn) applied only outside fenced and inline code."""
    out, last = [], 0
    for m in CODE_SPAN_RE.finditer(text):
        out.append(rx.sub(fn, text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(rx.sub(fn, text[last:]))
    return "".join(out)


def norm_heading(h):
    h = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", h)
    h = re.sub(r"[*_`=~]", "", h)
    h = re.sub(r"[:#|^\[\]%\\]", " ", h)
    return re.sub(r"\s+", " ", h).strip().lower()


def heading_anchor_text(h):
    """The text to put after # in a [[#Heading]] link (Obsidian drops : # | ^ [ ] %)."""
    return re.sub(r"\s+", " ", re.sub(r"[:#|^\[\]%\\]", " ", h)).strip()


def h2_list(body):
    return [m.group(1).strip() for m in re.finditer(r"^## (.+?)\s*#*\s*$", strip_code(body, False), re.M)]


def section_text(body, heading):
    m = re.search(r"^## " + re.escape(heading) + r"\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1) if m else None


# ---------------------------------------------------------------- vault model

class Note:
    def __init__(self, rel, raw):
        self.rel = rel
        self.raw = raw
        self.stem = os.path.basename(rel)[:-3]
        fm, body, self.fm_lines = split_frontmatter(raw)
        self.has_fm = fm is not None
        self.fm_text = fm or ""
        self.props = parse_frontmatter(fm) if fm is not None else {}
        self.body = body
        self.headings, self.blocks, self.heading_list = set(), set(), []
        for line in strip_code(body, False).splitlines():
            hm = HEADING_RE.match(line)
            if hm:
                self.headings.add(norm_heading(hm.group(2)))
                self.heading_list.append((len(hm.group(1)), hm.group(2)))
            bm = BLOCK_RE.search(line)
            if bm:
                self.blocks.add(bm.group(1))
        self.zone = "public"

    @property
    def type(self):
        return str(self.props.get("type", "")).strip()

    def aliases(self):
        return [a for a in as_list(self.props.get("aliases")) if a]

    def tags(self):
        tags = [t.lstrip("#") for t in as_list(self.props.get("tags")) if t]
        clean = strip_code(self.body)
        clean = MD_LINK_RE.sub(" ", clean)
        for line in clean.splitlines():
            if HEADING_RE.match(line):
                continue
            tags += TAG_RE.findall(line)
        return tags


class Vault:
    def __init__(self, root, cfg=None):
        self.root = os.path.abspath(root)
        self.cfg = cfg or load_config(self.root)
        self.notes, self.files = {}, {}
        self.by_name, self.by_path = {}, {}
        ign_dirs = set(self.cfg["ignore_dirs"])
        ign_paths = tuple(self.cfg["ignore_paths"])
        for dp, dn, fn in os.walk(self.root):
            dn[:] = sorted(d for d in dn if d not in ign_dirs)
            for f in sorted(fn):
                rel = os.path.relpath(os.path.join(dp, f), self.root).replace(os.sep, "/")
                if rel.startswith(ign_paths) or f in (".DS_Store",):
                    continue
                if f.endswith(".md"):
                    with open(os.path.join(dp, f), encoding="utf-8", errors="replace", newline="") as fh:
                        self.notes[rel] = Note(rel, fh.read())
                    self.by_name.setdefault(f[:-3].lower(), []).append(rel)
                    self.by_path[rel[:-3].lower()] = rel
                else:
                    self.files[rel] = f
                    self.by_name.setdefault(f.lower(), []).append(rel)
                self.by_path[rel.lower()] = rel
        self.manifest = self._load_manifest()
        for n in self.notes.values():
            n.zone = self.zone_of(n.rel, n.props)

    # ---- zones
    def _load_manifest(self):
        p = os.path.join(self.root, self.cfg["zones"]["manifest"])
        pats = []
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        pats.append(line.rstrip("*"))
        return pats

    def in_manifest(self, rel):
        for p in self.manifest:
            if p.endswith("/"):
                if rel.startswith(p) or rel == p.rstrip("/"):
                    return True
            elif rel == p or rel.startswith(p + "/"):
                return True
        return False

    def zone_of(self, rel, props=None):
        z = self.cfg["zones"]
        if self.in_manifest(rel):
            return "internal"
        for k, vals in z["private_values"].items():
            if props and str(props.get(k, "")).strip().lower() in vals:
                return "internal"
        return "internal" if z["default"] != "public" else "public"

    def is_template(self, rel):
        t = self.cfg["templates_folder"].strip("/") + "/"
        return rel.startswith(t) or ("/" + t) in rel

    # ---- resolution
    def resolve(self, target, src_rel=""):
        """Return (rel or None, ambiguous)."""
        t = urllib.parse.unquote(target.strip()).replace("\\", "/").lstrip("/")
        if not t:
            return None, False
        low = t.lower()
        if low.startswith("./") or low.startswith("../"):
            joined = os.path.normpath(os.path.join(os.path.dirname(src_rel), t)).replace(os.sep, "/")
            low = joined.lower()
        for cand in (low, low + ".md"):
            if cand in self.by_path:
                return self.by_path[cand], False
        if "/" in low:
            tail = low.rsplit("/", 1)[1]
            cands = [r for r in self.by_name.get(tail, []) + self.by_name.get(tail[:-3] if tail.endswith(".md") else tail, [])
                     if r.lower().endswith(low) or r.lower().endswith(low + ".md")]
            cands = sorted(set(cands))
            return (cands[0], False) if len(cands) == 1 else (None, len(cands) > 1)
        name = low[:-3] if low.endswith(".md") else low
        cands = self.by_name.get(name, []) or self.by_name.get(low, [])
        if len(cands) > 1 and not self.is_template(src_rel):
            cands = [c for c in cands if not self.is_template(c)] or cands
        if len(cands) == 1:
            return cands[0], False
        if len(cands) > 1:
            same = [c for c in cands if os.path.dirname(c) == os.path.dirname(src_rel)]
            return (same[0], False) if len(same) == 1 else (None, True)
        return None, False

    # ---- links
    def links(self, note, include_props=True, keep_private_blocks=True):
        """Yield dicts: line, target, anchor, raw, embed, kind ('wiki'|'md'|'prop'), private (inside strip markers)."""
        out = []
        z = self.cfg["zones"]
        if include_props and note.fm_text:
            for i, line in enumerate(note.fm_text.splitlines(), 2):
                for m in WIKI_RE.finditer(line):
                    out.append(self._wiki(m, i, "prop", False))
        text = strip_code(note.body, comments=False)
        inside = False
        offset = note.fm_lines
        for i, line in enumerate(text.splitlines(), 1):
            if z["strip_start"] in line:
                inside = True
            scan = COMMENT_RE.sub("", line)
            for m in WIKI_RE.finditer(scan):
                out.append(self._wiki(m, i + offset, "wiki", inside))
            for m in MD_LINK_RE.finditer(scan):
                href = m.group(3)
                if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) or href.startswith("//"):
                    continue  # external URL, mailto:, obsidian:// and other schemes
                tgt, _, anchor = href.partition("#")
                out.append({"line": i + offset, "target": urllib.parse.unquote(tgt), "anchor": anchor or None,
                            "raw": m.group(0), "embed": bool(m.group(1)), "kind": "md", "private": inside})
            if z["strip_end"] in line:
                inside = False
        return out

    @staticmethod
    def _wiki(m, line, kind, private):
        inner = m.group(2)
        head = re.split(r"\\?\|", inner, maxsplit=1)[0].rstrip("\\")
        tgt, anchor = (head.split("#", 1) + [None])[:2] if "#" in head else (head, None)
        return {"line": line, "target": tgt.strip(), "anchor": anchor, "raw": m.group(0), "embed": bool(m.group(1)),
                "kind": kind, "private": private}

    def canvas(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as f:
            return json.load(f)

    def graph(self):
        """Directed edges between vault files (notes, canvases, other files).
        Returns (out_links, in_links, problems) where problems are (rel, link, kind) for unresolved links."""
        out, inn, problems = {}, {}, []
        for rel, n in self.notes.items():
            if self.is_template(rel):
                continue
            for ln in self.links(n):
                if not ln["target"]:
                    continue
                dest, amb = self.resolve(ln["target"], rel)
                if dest is None:
                    problems.append((rel, ln, "ambiguous" if amb else "dangling"))
                    continue
                out.setdefault(rel, set()).add(dest)
                inn.setdefault(dest, set()).add(rel)
        for rel in self.files:
            if rel.endswith(".canvas"):
                try:
                    data = self.canvas(rel)
                except Exception:
                    continue
                for nd in data.get("nodes", []):
                    if nd.get("type") == "file" and nd.get("file"):
                        dest = self.by_path.get(nd["file"].lower())
                        if dest:
                            out.setdefault(rel, set()).add(dest)
                            inn.setdefault(dest, set()).add(rel)
                    for m in WIKI_RE.finditer(nd.get("text", "") or ""):
                        dest, _ = self.resolve(self._wiki(m, 0, "wiki", False)["target"], rel)
                        if dest:
                            out.setdefault(rel, set()).add(dest)
                            inn.setdefault(dest, set()).add(rel)
        return out, inn, problems

    def hops(self, out):
        home = self.cfg["home"]
        if home not in self.notes:
            return {}
        dist, frontier = {home: 0}, [home]
        while frontier:
            nxt = []
            for r in frontier:
                for d in sorted(out.get(r, ())):
                    if d not in dist:
                        dist[d] = dist[r] + 1
                        nxt.append(d)
            frontier = nxt
        return dist

    def write(self, rel, text):
        p = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)


def taxonomy_tags(vault):
    """Tags declared in the taxonomy note: every `backticked` token that looks like a tag."""
    rel = vault.cfg.get("taxonomy_note")
    n = vault.notes.get(rel) if rel else None
    if not n:
        return None
    found = set()
    for tok in re.findall(r"`#?([A-Za-z0-9_\-]+(?:/[A-Za-z0-9_\-*]+)*)`", n.body):
        found.add(tok)
    return found


def tag_allowed(tag, allowed, patterns):
    if allowed is None and not patterns:
        return True
    if allowed and tag in allowed:
        return True
    if allowed:
        for a in allowed:
            if a.endswith("/*") and tag.startswith(a[:-1]):
                return True
    return any(re.fullmatch(p, tag) for p in patterns)
