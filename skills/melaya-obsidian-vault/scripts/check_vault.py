#!/usr/bin/env python3
"""Check an Obsidian vault against its conventions. Standard library only; read-only.

Usage:
  python3 check_vault.py --vault PATH [--config FILE] [--scope=FOLDER/] [--today=YYYY-MM-DD]
                         [--all] [--quiet] [--json=REPORT.json] [--strict]

Checks (each finding is ERROR or WARN; exit code 1 when any ERROR, or any WARN with --strict):
  links       dangling links and embeds, dangling #heading and #^block anchors, ambiguous names,
              unquoted links in properties, duplicate note names
  graph       orphans (nothing links in), notes unreachable from Home or more than max_hops away
  properties  required keys (global and per zone), type / status / audience values, dates,
              review_every format, stale reviews, one-sentence description, tags as a list,
              tags present in the taxonomy note or tag_patterns
  structure   H1 title, required sections per type, At a glance bullet count, Changelog last and
              well formed, Contents outline on notes over the size budget, open_questions flag
  zones       public notes linking, embedding or listing internal notes (outside strip markers),
              public notes carrying internal flags, manifest paths without publish: false,
              public Bases and Canvas that reach the internal zone
  content     credential-like strings, emails outside the allow list, phone numbers, IBANs and
              card numbers (checksummed), national ids, IP addresses, deny-list patterns,
              banned punctuation, CRLF line endings
  files       invalid Canvas JSON, Canvas nodes to missing files, Bases on missing folders,
              unused or oversized attachments, attachments outside the attachments folder

Configuration: <vault>/_Meta/vault-config.json (see vaultlib.DEFAULTS for every key).
"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vaultlib as vl  # noqa: E402

SECRET_RE = re.compile(
    r"(AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|AIza[0-9A-Za-z_\-]{35}|xox[abposr]-[A-Za-z0-9-]{10,}"
    r"|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|glpat-[A-Za-z0-9_\-]{20,}"
    r"|sk-(?:live|proj|ant)?[-_]?[A-Za-z0-9_\-]{20,}|[rs]k_live_[A-Za-z0-9]{16,}"
    r"|eyJ[A-Za-z0-9_\-]{15,}\.[A-Za-z0-9_\-]{15,}\.[A-Za-z0-9_\-]{10,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._\-]{24,}"
    r"|(?i:\b(?:api[_-]?key|secret|passw(?:or)?d|token|client[_-]?secret)\b\s*[:=]\s*[\"']?[A-Za-z0-9_\-/+=.]{12,}))")
PLACEHOLDER_RE = re.compile(r"(?i)your|example|placeholder|redacted|dummy|xxxx|<|\.\.\.|\*{4}")
EMAIL_RE = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)")
PHONE_RE = re.compile(r"(?<![\w+])\+\d{1,3}[ .\-]?\(?\d{1,4}\)?(?:[ .\-]?\d{2,4}){2,4}(?!\w)")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,3})?\b")
CARD_RE = re.compile(r"(?<!\d)(?:\d[ \-]?){12,18}\d(?!\d)")
SSN_RE = re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")
IP_RE = re.compile(r"(?<![\d.])(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?![\d.])")
DOC_IPS = ("192.0.2.", "198.51.100.", "203.0.113.", "127.0.0.1", "0.0.0.0")
ATTACH_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".mp3", ".wav", ".m4a", ".ogg",
              ".mp4", ".mov", ".webm", ".docx", ".xlsx", ".pptx", ".csv", ".zip", ".avif", ".bmp")
CHECKS = ["dangling links", "dangling anchors", "ambiguous links", "duplicate names", "property links",
          "orphans", "hops from Home", "missing properties", "invalid properties", "taxonomy", "stale notes",
          "structure", "size without outline", "zone leaks", "secrets", "personal data", "deny list",
          "punctuation", "line endings", "files", "attachments"]


def luhn(digits):
    s, alt = 0, False
    for d in reversed(digits):
        d = int(d)
        if alt:
            d = d * 2 - 9 if d > 4 else d * 2
        s += d
        alt = not alt
    return s % 10 == 0


def iban_ok(raw):
    s = raw.replace(" ", "")
    if not 15 <= len(s) <= 34:
        return False
    num = "".join(str(int(c, 36)) for c in s[4:] + s[:4])
    return int(num) % 97 == 1


def main():
    vl.utf8_stdout()
    opts, pos = vl.parse_args(sys.argv[1:], flags=("all", "quiet", "strict"))
    root = opts.get("vault") or (pos[0] if pos else ".")
    cfg = vl.load_config(root, opts.get("config"))
    vault = vl.Vault(root, cfg)
    scope = opts.get("scope", "").strip('"')
    today = datetime.date.fromisoformat(opts["today"]) if opts.get("today") else datetime.date.today()
    findings = {}

    def report(check, level, rel, msg):
        if scope and not rel.startswith(scope):
            return
        findings.setdefault(check, []).append((level, rel, msg))

    notes = {r: n for r, n in vault.notes.items() if not vault.is_template(r)}
    zones_on = bool(vault.manifest) or cfg["zones"]["default"] != "public" or any(
        n.zone == "internal" for n in notes.values())

    # ------------------------------------------------------------ links and anchors
    out, inn, problems = vault.graph()
    for rel, ln, kind in problems:
        if ln["kind"] == "md" and not ln["target"].lower().endswith((".md",) + ATTACH_EXT + (".canvas", ".base")):
            continue  # a Markdown link to something that is not a vault file type (left to the author)
        report("ambiguous links" if kind == "ambiguous" else "dangling links", "ERROR", rel,
               f"line {ln['line']}: {ln['raw']}" + (" (several notes have this name: qualify the path or rename)"
                                                   if kind == "ambiguous" else ""))
    leak_allowed = set(cfg["zones"]["leak_allowed"])
    for rel, n in notes.items():
        for ln in vault.links(n):
            if ln["target"] == "":
                a = ln["anchor"] or ""
                ok = a[1:] in n.blocks if a.startswith("^") else vl.norm_heading(a) in n.headings
                if a and not ok:
                    report("dangling anchors", "ERROR", rel, f"line {ln['line']}: {ln['raw']} (not in this note)")
                continue
            dest, _ = vault.resolve(ln["target"], rel)
            if not dest:
                continue
            if ln["anchor"] and dest in vault.notes:
                d, a = vault.notes[dest], ln["anchor"]
                parts = [p for p in a.split("#") if p]
                ok = (parts and parts[-1].startswith("^") and parts[-1][1:] in d.blocks) or \
                     all(vl.norm_heading(p) in d.headings for p in parts)
                if not ok:
                    report("dangling anchors", "ERROR", rel, f"line {ln['line']}: {ln['raw']} (no '{a}' in {d.stem})")
            if zones_on and n.zone == "public" and vault.zone_of(dest, vault.notes[dest].props if dest in vault.notes else None) == "internal":
                if not (rel in leak_allowed and ln["private"]):
                    report("zone leaks", "ERROR", rel, f"line {ln['line']}: public note links to internal {dest}")
        for i, line in enumerate(n.fm_text.splitlines(), 2):
            if "[[" in line and not re.search(r"(:\s*|-\s*)[\"']\[\[", line) and not re.search(r"\[\s*[\"']\[\[", line):
                report("property links", "ERROR", rel, f"line {i}: links in properties must be quoted: {line.strip()}")

    for name, rels in vault.by_name.items():
        md = [r for r in rels if r.endswith(".md") and not vault.is_template(r)]
        if len(md) > 1:
            for r in md:
                report("duplicate names", "ERROR", r, f"'{name}' also at {[x for x in md if x != r]}")

    # ------------------------------------------------------------ graph reach
    home = cfg["home"]
    dist = vault.hops(out)
    exempt = tuple(cfg["orphan_exempt"])
    if home not in vault.notes:
        report("hops from Home", "ERROR", home, "home note not found (set 'home' in vault-config.json)")
    for rel in notes:
        if rel == home or (exempt and rel.startswith(exempt)):
            continue
        if not (inn.get(rel, set()) - {rel}):
            report("orphans", "ERROR", rel, "nothing links here (add it to its hub and to related notes)")
        if home in vault.notes:
            if rel not in dist:
                report("hops from Home", "ERROR", rel, "no link path from Home")
            elif dist[rel] > cfg["max_hops"]:
                report("hops from Home", "ERROR", rel, f"{dist[rel]} hops from Home (max {cfg['max_hops']})")

    # ------------------------------------------------------------ properties
    allowed_tags = vl.taxonomy_tags(vault)
    patterns = cfg["tag_patterns"]
    types, statuses, audiences = set(cfg["types"]), set(cfg["statuses"]), set(cfg["audiences"])
    for rel, n in notes.items():
        p = n.props
        if not n.has_fm:
            report("missing properties", "ERROR", rel, "no properties (frontmatter) block")
            continue
        need = list(cfg["required_properties"]) + list(cfg["required_by_zone"].get(n.zone, []))
        for k in need:
            if vl.as_list(p.get(k)) == []:
                report("missing properties", "ERROR", rel, f"missing '{k}'")
        if "tags" in p and not isinstance(p["tags"], list):
            report("invalid properties", "ERROR", rel, "tags must be a YAML list")
        t = n.type
        if t and types and t not in types:
            report("invalid properties", "ERROR", rel, f"type '{t}' not in {sorted(types)}")
        st = str(p.get("status", "")).strip()
        if st and statuses and st not in statuses:
            report("invalid properties", "ERROR", rel, f"status '{st}' not in {sorted(statuses)}")
        au = str(p.get("audience", "")).strip()
        if au and audiences and au not in audiences:
            report("invalid properties", "ERROR", rel, f"audience '{au}' not in {sorted(audiences)}")
        if st == "superseded":
            sb = str(vl.as_list(p.get("superseded_by"))[0] if vl.as_list(p.get("superseded_by")) else "")
            m = re.search(r"\[\[([^\]|#]+)", sb)
            if not m or not vault.resolve(m.group(1), rel)[0]:
                report("invalid properties", "ERROR", rel, "status superseded needs superseded_by: \"[[New Note]]\"")
        for k in ("updated", "reviewed", "created"):
            if p.get(k) not in (None, "", []) and not vl.to_date(p.get(k)):
                report("invalid properties", "ERROR", rel, f"{k} is not a YYYY-MM-DD date: {p.get(k)}")
        up = vl.to_date(p.get("updated", ""))
        if up and up > today:
            report("invalid properties", "ERROR", rel, f"updated {up} is in the future")
        if p.get("review_every") not in (None, "", []) and vl.period_days(p.get("review_every")) is None:
            report("invalid properties", "ERROR", rel, "review_every must look like 14d, 6w, 3m or 1y")
        rv, every = vl.to_date(p.get("reviewed", "")), vl.period_days(p.get("review_every", ""))
        if rv and every and rv + datetime.timedelta(days=every) < today and st in ("", "current"):
            report("stale notes", "WARN", rel, f"review due since {rv + datetime.timedelta(days=every)}")
        desc = str(p.get("description", "") or "")
        if desc and (len(desc) > cfg["description_max"] or re.search(r"[.?!]\s+[A-Z]", desc)):
            report("invalid properties", "WARN", rel, f"description should be one sentence of at most {cfg['description_max']} characters")
        if allowed_tags is not None or patterns:
            for tag in set(n.tags()):
                if not vl.tag_allowed(tag, allowed_tags, patterns):
                    report("taxonomy", "ERROR", rel, f"tag '{tag}' is not in the taxonomy")
        if vault.in_manifest(rel) and str(p.get("publish", "")).lower() != "false":
            report("zone leaks", "WARN", rel, "manifest path without publish: false (tools that cannot read the manifest would publish it)")

    # ------------------------------------------------------------ structure
    lo, hi = cfg["glance_bullets"]
    budget = int(cfg["size_budget_kb"]) * 1024
    for rel, n in notes.items():
        if not n.has_fm:
            continue
        body, h2 = n.body, vl.h2_list(n.body)
        if not re.search(r"^# \S", vl.strip_code(body, False), re.M):
            report("structure", "WARN", rel, "no H1 title")
        need = cfg["sections"].get(n.type, cfg["sections"].get("*", []))
        for h in need:
            if h not in h2:
                report("structure", "ERROR", rel, f"missing '## {h}' (required for type '{n.type or '*'}')")
        if "At a glance" in h2:
            seg = vl.section_text(body, "At a glance") or ""
            b = len(re.findall(r"^\s{0,1}[-*] ", seg, re.M))
            if not lo <= b <= hi:
                report("structure", "WARN", rel, f"At a glance has {b} bullets ({lo} to {hi})")
            if h2.index("At a glance") > 0:
                report("structure", "WARN", rel, "At a glance should be the first section")
        if "Changelog" in h2:
            if h2[-1] != "Changelog":
                report("structure", "ERROR", rel, "Changelog must be the last section")
            seg = vl.section_text(body, "Changelog") or ""
            dates = re.findall(r"^- (\d{4}-\d{2}-\d{2}) [^:\n]+: .+", seg, re.M)
            if not dates:
                report("structure", "ERROR", rel, "Changelog lines look like '- 2026-01-31 who: what changed (source).'")
            up = vl.to_date(n.props.get("updated", ""))
            if dates and up and max(dates) > up.isoformat():
                report("invalid properties", "ERROR", rel, f"updated {up} is older than the newest changelog line {max(dates)}")
        oq = "Open questions" in h2
        if vl.truthy(n.props.get("open_questions", "")) and not oq:
            report("structure", "WARN", rel, "open_questions: true but no '## Open questions' section")
        size = len(n.raw.encode("utf-8"))
        if size > budget and n.type not in ("log",):
            seg = vl.section_text(body, "Contents")
            listed = {vl.norm_heading(a) for a in re.findall(r"\[\[#([^\]|]+)", seg or "")}
            missing = [h for h in h2 if h not in ("Contents", "At a glance") and vl.norm_heading(h) not in listed]
            if seg is None or missing:
                report("size without outline", cfg["contents_level"], rel,
                       f"{size // 1024} KB: add '## Contents' linking every H2 (scripts/add_contents.py)"
                       + (f", missing {missing[:3]}" if seg is not None else ""))

    # ------------------------------------------------------------ content scans
    allow = tuple("@" + d.lower() for d in cfg["pii"]["email_allow"]) + tuple("." + d.lower() for d in cfg["pii"]["email_allow"])
    deny = [re.compile(x, re.I) for x in cfg["denylist"]]
    deny_pub = [re.compile(x, re.I) for x in cfg["denylist_public"]]
    banned = cfg["banned"]
    custom_banned = [re.compile(x) for x in banned.get("custom", [])]
    pii = cfg["pii"]
    for rel, n in notes.items():
        raw = n.raw
        if "\r\n" in raw:
            report("line endings", "WARN", rel, "CRLF line endings (save as LF)")
        for m in SECRET_RE.finditer(raw):
            if not PLACEHOLDER_RE.search(m.group(0)):
                report("secrets", "ERROR", rel, f"credential-like string: {m.group(0)[:16]}...")
        for m in EMAIL_RE.finditer(raw):
            addr = m.group(0).lower()
            if not addr.endswith(allow):
                report("personal data", "ERROR" if n.zone == "public" else "WARN", rel, f"email address: {m.group(0)}")
        text = vl.strip_code(raw, comments=False)
        if pii.get("phone"):
            for m in PHONE_RE.finditer(text):
                digits = re.sub(r"\D", "", m.group(0))
                if 8 <= len(digits) <= 15 and "555" not in digits[:7]:  # 555 numbers are fictional
                    report("personal data", pii["phone"], rel, f"phone number: {m.group(0)}")
        for m in IBAN_RE.finditer(text):
            if iban_ok(m.group(0)):
                report("personal data", "ERROR", rel, f"IBAN: {m.group(0)[:8]}...")
        for m in CARD_RE.finditer(text):
            d = re.sub(r"\D", "", m.group(0))
            if 13 <= len(d) <= 19 and luhn(d) and not vl.DATE_RE.match(m.group(0)[:10]):
                report("personal data", "ERROR", rel, f"card-like number: {d[:4]}...")
        if pii.get("national_id"):
            for m in SSN_RE.finditer(text):
                report("personal data", pii["national_id"], rel, f"national id pattern: {m.group(0)[:3]}-..")
        if pii.get("ip"):
            for m in IP_RE.finditer(text):
                ip = m.group(0)
                if all(0 <= int(x) <= 255 for x in m.groups()) and not ip.startswith(DOC_IPS):
                    report("personal data", pii["ip"], rel, f"IP address: {ip} (use 192.0.2.x in examples)")
        for rx in deny + (deny_pub if n.zone == "public" else []):
            for m in rx.finditer(raw):
                report("deny list", "ERROR", rel, f"deny-listed term: {m.group(0)}")
        if n.type == "meta":
            continue  # rule notes quote the banned characters
        for i, line in enumerate(vl.strip_code(n.body).splitlines(), n.fm_lines + 1):
            if banned.get("em_dash") and "\u2014" in line:
                report("punctuation", "ERROR", rel, f"line {i}: em dash")
            if banned.get("en_dash_separator") and re.search(r"\s\u2013\s", line):
                report("punctuation", "ERROR", rel, f"line {i}: en dash used as a separator")
            if banned.get("semicolon") and ";" in re.sub(r"&#?\w+;", "", line):
                report("punctuation", "ERROR", rel, f"line {i}: semicolon")
            if banned.get("exclamation") and re.search(r"[A-Za-z)]!(\s|$)", line) and not line.lstrip().startswith((">", "![")):
                report("punctuation", "ERROR", rel, f"line {i}: exclamation mark")
            for rx in custom_banned:
                if rx.search(line):
                    report("punctuation", "ERROR", rel, f"line {i}: matches banned pattern {rx.pattern}")

    # ------------------------------------------------------------ canvas, bases, attachments
    internal_folders = [p.rstrip("/") for p in vault.manifest if p.endswith("/")]
    for rel in vault.files:
        if vault.is_template(rel):
            continue
        full = os.path.join(vault.root, rel)
        public = vault.zone_of(rel) == "public"
        if rel.endswith(".canvas"):
            try:
                data = vault.canvas(rel)
            except Exception as e:  # noqa: BLE001
                report("files", "ERROR", rel, f"canvas is not valid JSON: {e}")
                continue
            ids = {nd.get("id") for nd in data.get("nodes", [])}
            for nd in data.get("nodes", []):
                if nd.get("type") == "file":
                    dest = vault.by_path.get(str(nd.get("file", "")).lower())
                    if not dest:
                        report("files", "ERROR", rel, f"canvas node points to missing file {nd.get('file')}")
                    elif zones_on and public and vault.zone_of(dest, vault.notes[dest].props if dest in vault.notes else None) == "internal":
                        report("zone leaks", "ERROR", rel, f"public canvas shows internal {dest}")
            for ed in data.get("edges", []):
                if ed.get("fromNode") not in ids or ed.get("toNode") not in ids:
                    report("files", "ERROR", rel, f"canvas edge {ed.get('id')} points to a missing node")
        elif rel.endswith(".base"):
            with open(full, encoding="utf-8") as f:
                text = f.read()
            not_indent = None
            for line in text.splitlines():
                ind = len(line) - len(line.lstrip())
                if not_indent is not None and line.strip() and ind <= not_indent:
                    not_indent = None
                if re.match(r"^\s*-?\s*not:\s*$", line):
                    not_indent = ind
                    continue
                for folder in re.findall(r'inFolder\(\s*"([^"]+)"\s*\)', line):
                    if not_indent is None and not os.path.isdir(os.path.join(vault.root, folder)):
                        report("files", "ERROR", rel, f'base filters on missing folder "{folder}"')
            if zones_on and public and internal_folders:
                top = text.split("views:")[0]
                scoped = re.findall(r'inFolder\(\s*"([^"]+)"\s*\)', top)
                positive = [x for x in scoped if x not in internal_folders]
                excluded = "not:" in top and all(any(x == e or x.startswith(e + "/") for e in scoped) for x in internal_folders)
                if not positive and not excluded:
                    report("zone leaks", "ERROR", rel, "public base over the whole vault must exclude every internal folder with not:")
        elif rel.lower().endswith(ATTACH_EXT):
            if not inn.get(rel):
                report("attachments", "WARN", rel, "attachment not used by any note")
            att = cfg["attachments_folder"].strip("/")
            if att and not rel.startswith(att + "/") and "/" + att + "/" not in rel:
                report("attachments", "WARN", rel, f"attachment outside the '{att}' folder")
            if os.path.getsize(full) > cfg["attachment_max_mb"] * 1024 * 1024:
                report("attachments", "WARN", rel, f"larger than {cfg['attachment_max_mb']} MB")

    # ------------------------------------------------------------ output
    errors = sum(1 for v in findings.values() for f in v if f[0] == "ERROR")
    warns = sum(1 for v in findings.values() for f in v if f[0] == "WARN")
    internal_n = sum(1 for n in notes.values() if n.zone == "internal")
    print(f"Vault: {vault.root}")
    print(f"Notes: {len(notes)} ({internal_n} internal), other files: {len(vault.files)}, "
          f"max hops from Home: {max(dist.values()) if dist else 'n/a'}, today: {today}")
    limit = None if opts.get("all") else 25
    for c in CHECKS + sorted(set(findings) - set(CHECKS)):
        items = findings.get(c, [])
        e = sum(1 for f in items if f[0] == "ERROR")
        print(f"  {c:<22} errors {e:>4}   warnings {len(items) - e:>4}")
    if not opts.get("quiet"):
        for c in CHECKS + sorted(set(findings) - set(CHECKS)):
            items = sorted(findings.get(c, []), key=lambda f: (f[0] != "ERROR", f[1]))
            if items:
                print(f"\n== {c} ({len(items)})")
                for level, rel, msg in items[:limit]:
                    print(f"  {level:<5} {rel}: {msg}")
                if limit and len(items) > limit:
                    print(f"  ... {len(items) - limit} more (use --all)")
    if opts.get("json"):
        with open(opts["json"], "w", encoding="utf-8") as f:
            json.dump({"vault": vault.root, "today": today.isoformat(), "errors": errors, "warnings": warns,
                       "findings": [{"check": c, "level": l, "path": r, "message": m}
                                    for c, items in findings.items() for (l, r, m) in items]}, f, indent=1)
    print(f"\nRESULT: {errors} errors, {warns} warnings")
    return 1 if errors or (opts.get("strict") and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
