"""plankit: build, size, preview, store and verify one-call Melaya device plans.

Generic helper for the method in ../GUIDE.md (read, plan offline, preview, store and run in ONE call, verify, recover).
Python 3.9+, standard library only. Copy it next to your job script or run it from here.

    from plankit import *
    rows = [{"name": "Ada", "city": "London"}, ...]
    steps = [c_type("\t".join(r.values()) + "\n", target=T(label="Text editor"), delivery="background") for r in rows]
    print(preview(steps, "computer", "batch"))
    path = write_plan("crm_rows", steps, "computer", "batch")   # ~/.melaya/plans/crm_rows.json
    # then call melaya_computer_batch {"steps": [], "plan": {"file": "crm_rows.json"}}
    # read back (get_text / read_table / browser_get_text) and check:
    print(diff_lines(expected_lines, text_read_back))

CLI:  python plankit.py preview FILE.json   (counts, caps, time estimate of an existing plan)
      python plankit.py selftest            (builds and checks one plan per surface, writes nothing)

Step shapes follow the live tool schemas (2026-10-24):
  computer batch : contract actions {kind, target?, ..., delivery?, expect?, onError?}; camelCase keys
  computer fast / browser fast / phone fast : plain-word steps {do, target|into|text|option|key|ms ...}
  browser batch  : {do, args}; refs (@eN) from melaya_browser_screen; max 20 steps per call
  phone batch    : {do, args, expect?, settle_ms?}; max 25 steps per call; expect is checked before settle_ms and
                   text_visible matches substrings (p_input_checked, expect_collisions)
"""
import csv
import json
import os
import re
import sys

PLAN_DIR = os.path.join(os.path.expanduser("~"), ".melaya", "plans")
PLAN_FILE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}\.json$")
PLAN_MAX_BYTES = 2 * 1024 * 1024

# Hard caps per (surface, kind): steps per call and wall time (s) per call. A plan over a cap is split.
CAPS = {
    ("computer", "batch"): {"steps": 5000, "seconds": 600},
    ("computer", "fast"): {"steps": 500, "seconds": 900},
    ("computer", "path"): {"strokes": 200, "points": 20000, "seconds": 540},
    ("browser", "batch"): {"steps": 20, "seconds": 60},
    ("browser", "fast"): {"steps": 100, "seconds": 900},
    ("phone", "batch"): {"steps": 25, "seconds": 60},
    ("phone", "fast"): {"steps": 100, "seconds": 900},
}

# Seconds per step, by step kind, measured on live runs 2026-10-24 (see ../GUIDE.md "Time model"); the defaults are
# deliberately a little high. Pass your own to estimate() once you have timed a run of your app.
#   computer batch: 35 background type / expect steps in 2.8 s (Notepad); Paint: 1786 steps, 17,386 strokes in 512 s
#   browser fast: open 4.6-5.2 s, type 1.0-2.0 s, select 2.0-2.7 s, click that changes the page 3.0 s, read 1.2-1.4 s
COSTS = {
    "computer": {"type": 0.08, "type_per_char": 0.0, "press": 0.08, "click": 0.15, "set_value": 0.1, "select": 0.4,
                 "mouse": 0.03, "move": 0.03, "expect": 0.02, "get_text": 0.15, "read_table": 0.5, "scroll": 0.15,
                 "path_per_stroke": 0.0245, "default": 0.15},
    "browser": {"input_text": 1.0, "click": 1.5, "select_option": 1.0, "navigate": 4.0, "get_text": 1.0,
                "get_screen_tree": 1.0, "press_key": 0.5, "type": 1.5, "select": 2.5, "pick": 3.0, "open": 5.0,
                "read": 1.4, "expect": 0.05, "back": 2.0, "default": 1.5},
    # phone batch: 21 steps (click_id + 20 input_text, 10 of them with settle_ms 1200) in 20.8 s wall;
    # phone fast: type 0.5-1.4 s, wait N ms = N + 0.3 s, read 0.25-0.45 s, expect and collect about 0 s
    "phone": {"click_text": 0.8, "click_id": 0.8, "input_text": 0.3, "clear_text": 0.3, "paste": 0.3, "open_app": 2.5,
              "tap": 0.6, "type": 1.2, "read": 0.4, "expect": 0.05, "collect": 0.3, "click": 1.5, "back": 1.0,
              "wait_overhead": 0.3, "default": 1.5},
}


# ---------------------------------------------------------------- targets


def T(ref=None, label=None, role=None, near=None, nth=None, x=None, y=None):
    """A computer target: ref first, else label (+ role / near / nth), else x, y (last resort)."""
    if ref:
        return {"ref": ref if ref.startswith("@") else "@" + ref}
    if label:
        t = {"label": label}
        if role:
            t["role"] = role
        if near:
            t["near"] = near
        if nth is not None:
            t["nth"] = int(nth)
        return t
    if x is not None and y is not None:
        return {"x": int(round(x)), "y": int(round(y))}
    raise ValueError("target needs ref, label or x and y")


def _c(kind, delivery=None, expect=None, on_error=None, **kw):
    s = {"kind": kind}
    s.update({k: v for k, v in kw.items() if v is not None})
    if delivery:
        s["delivery"] = delivery                     # "auto" | "background" | "foreground"
    if expect:
        s["expect"] = expect                         # {appears|disappears|value:{target,equals|contains}|windowTitleContains|idle}
    if on_error:
        s["onError"] = on_error                      # "stop" (default) | "continue"
    return s


# ---------------------------------------------------------------- computer batch steps (melaya_computer_batch)


def c_click(target, button=None, count=None, modifiers=None, **o):
    return _c("click", target=target, button=button, count=count, modifiers=modifiers, **o)


def c_type(text, target=None, clear=None, **o):
    """Type text (max 20000 chars). Put line breaks in the text ("\\n") rather than pressing Enter: Enter is a commit
    key that raises an approval card in safe mode. Never use submit: true in a bulk plan."""
    return _c("type", target=target, text=text, clear=clear, **o)


def c_press(keys, repeat=None, **o):
    return _c("press", keys=keys, repeat=repeat, **o)


def c_set_value(target, value, **o):
    return _c("set_value", target=target, value=str(value), **o)


def c_select(target=None, option=None, menu_path=None, **o):
    return _c("select", target=target, option=option, menuPath=menu_path, **o)


def c_toggle(target, state=None, **o):
    return _c("toggle", target=target, state=state, **o)


def c_wait(ms=None, appears=None, disappears=None, timeout_ms=None, **o):
    until = {k: v for k, v in (("appears", appears), ("disappears", disappears)) if v}
    return _c("wait", ms=ms, until=until or None, timeoutMs=timeout_ms, **o)


def c_expect(timeout_ms=None, **condition):
    return {"kind": "expect", "condition": condition, **({"timeoutMs": timeout_ms} if timeout_ms else {})}


def c_scroll(direction, amount=None, target=None, **o):
    return _c("scroll", direction=direction, amount=amount, target=target, **o)


def c_path(strokes, speed=None, step_px=None, stroke_gap_ms=None, curve=None, **o):
    """Pointer strokes inside a batch. camelCase keys only (stepPx, strokeGapMs): snake_case is rejected in a batch."""
    return _c("path", strokes=strokes, speed=speed, stepPx=step_px, strokeGapMs=stroke_gap_ms, curve=curve, **o)


def c_mouse(x, y, state, **o):
    return _c("mouse", target={"x": int(x), "y": int(y)}, state=state, **o)


def c_move(x, y, **o):
    return _c("move", x=int(x), y=int(y), **o)


# ---------------------------------------------------------------- browser batch steps (melaya_browser_batch, max 20)


def b(do, **args):
    """{do, args}: navigate(url) click(ref) tap(x,y) input_text(ref,text,submit?) press_key(key) scroll(direction,
    amount_px?) select_option(ref, values) submit(ref) get_screen_tree get_text(ref?) screenshot back forward wait(ms)."""
    return {"do": do, "args": {k: v for k, v in args.items() if v is not None}} if args else {"do": do}


# ---------------------------------------------------------------- fast steps (computer / browser / phone fast)


def f(do, **kw):
    """Plain-word fast step: f("type", into="Email", text="a@b.c"), f("click", target="Save"), f("select", into="Country",
    option="France"), f("pick", into="Tags", options=[...]), f("press", key="Tab"), f("expect", text="Saved"),
    f("wait", ms=500), f("read"), f("collect", ...), f("for_each", ...)."""
    s = {"do": do}
    s.update({k: v for k, v in kw.items() if v is not None})
    return s


# ---------------------------------------------------------------- phone batch steps (melaya_phone_batch, max 25)


def p(do, expect=None, settle_ms=None, **args):
    """{do, args, expect?, settle_ms?}: open_app(app) click_text(text) click_id(id) input_text(text) paste(text)
    clear_text press_enter tap / double_tap (x,y) long_press(x,y,duration_ms?) scroll(direction,amount?)
    swipe(x1,y1,x2,y2,duration_ms?) back home. No wait step: settle_ms (0-3000, default 300) waits after the step.
    expect holds ONE of {app}|{text_visible}|{editable_focused: True}. It is checked right after the action, BEFORE
    settle_ms, and text_visible is a substring match ("= 10" passes on "= 1000"): see p_input_checked()."""
    s = {"do": do}
    if args:
        s["args"] = {k: v for k, v in args.items() if v is not None}
    if expect:
        if len(expect) != 1:
            raise ValueError("a phone batch expect takes exactly one of app, text_visible, editable_focused")
        s["expect"] = expect
    if settle_ms is not None:
        s["settle_ms"] = max(0, min(3000, int(settle_ms)))
    return s


def p_input_checked(text, text_visible, settle_ms=1200):
    """Type into the focused field, then check a value that appears only after a moment (suggestions, a computed
    result, a search count). The batch checks expect before settle_ms, so a late value fails on the typing step itself:
    type with a settle, then set the SAME text again (no visible change) and check on that second step."""
    return [p("input_text", text=text, settle_ms=settle_ms), p("input_text", text=text, expect={"text_visible": text_visible})]


def expect_collisions(texts):
    """Pairs (a, b) where expected text a is contained in another expected text b. Phone text_visible and fast expect
    text match substrings, so such a check can pass on the wrong value: make those texts longer or verify by read."""
    t = [str(x) for x in texts]
    return [(a, b) for a in t for b in t if a != b and a in b]


# ---------------------------------------------------------------- data in


def read_records(path, delimiter=None):
    """CSV / TSV / JSON list -> list of dicts."""
    if path.lower().endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    with open(path, encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        d = delimiter or ("\t" if sample.count("\t") > sample.count(",") else ",")
        return list(csv.DictReader(fh, delimiter=d))


# ---------------------------------------------------------------- sizing, time, chunking


def _kind_of(step):
    return step.get("kind") or step.get("do") or "default"


def estimate(steps, surface, costs=None, kind=None):
    """Seconds for a step list from per-kind costs plus explicit waits (and path strokes / typed characters).
    Phone batch steps also wait settle_ms after each step (300 ms when not given): pass kind="batch" to count it."""
    c = dict(COSTS.get(surface, {}))
    c.update(costs or {})
    default_settle = 300 if (surface, kind) == ("phone", "batch") else 0
    t = 0.0
    for s in steps:
        k = _kind_of(s)
        if k == "wait":
            t += (s.get("ms") or (s.get("args") or {}).get("ms") or 0) / 1000.0 + c.get("wait_overhead", 0.0)
            continue
        if k == "path":
            t += len(s.get("strokes", [])) * c.get("path_per_stroke", 0.0245)
            continue
        t += c.get(k, c.get("default", 0.3))
        if k in ("type", "input_text"):
            t += len(s.get("text") or (s.get("args") or {}).get("text") or "") * c.get("type_per_char", 0.0)
        settle = s.get("settle_ms")
        t += (default_settle if settle is None else settle) / 1000.0
    return t


def chunk(steps, surface, kind, max_steps=None, max_seconds=None, costs=None, margin=0.9):
    """Split a step list into calls that each respect the step cap and the time cap (with a safety margin).
    Never splits inside a group you mark with {"_group": id} on consecutive steps (e.g. one record's fields)."""
    cap = CAPS[(surface, kind)]
    ms = max_steps or cap.get("steps", 10 ** 9)
    mt = (max_seconds or cap.get("seconds", 10 ** 9)) * margin
    groups, cur, gid = [], [], object()
    for s in steps:
        g = s.get("_group", id(s))
        if cur and g != gid:
            groups.append(cur)
            cur = []
        cur.append(s)
        gid = g
    if cur:
        groups.append(cur)
    out, part = [], []
    for g in groups:
        if part and (len(part) + len(g) > ms or estimate(part + g, surface, costs, kind) > mt):
            out.append(part)
            part = []
        if len(g) > ms:
            raise ValueError("one group has %d steps, over the %d-step cap" % (len(g), ms))
        part += g
    if part:
        out.append(part)
    return [[{k: v for k, v in s.items() if k != "_group"} for s in c] for c in out]


def preview(steps, surface, kind, costs=None):
    """Counts by kind, estimate, bytes and cap checks: show this to the user before running."""
    kinds = {}
    for s in steps:
        kinds[_kind_of(s)] = kinds.get(_kind_of(s), 0) + 1
    cap = CAPS[(surface, kind)]
    est = estimate(steps, surface, costs, kind)
    size = len(json.dumps({"surface": surface, "kind": kind, "steps": steps}, separators=(",", ":")).encode())
    calls = len(chunk(steps, surface, kind, costs=costs)) if steps else 0
    bg = sum(1 for s in steps if s.get("delivery") == "background")
    return {"surface": surface, "kind": kind, "steps": len(steps), "kinds": kinds, "est_seconds": round(est, 1),
            "bytes": size, "calls_needed": calls, "fits_one_call": calls == 1 and size <= PLAN_MAX_BYTES,
            "step_cap": cap.get("steps"), "time_cap_s": cap.get("seconds"), "background_steps": bg}


# ---------------------------------------------------------------- store


def write_plan(name, steps, surface, kind, args=None, folder=None):
    """Write ~/.melaya/plans/<name>.json as {surface, kind, steps, ...args}; returns the path. Run it with
    plan: {"file": "<name>.json"} (or promote it with melaya_<surface>_plan save source {file})."""
    fname = name if name.endswith(".json") else name + ".json"
    if not PLAN_FILE_RE.match(fname):
        raise ValueError("plan file name: letters, digits, . _ - only, no folders")
    cap = CAPS[(surface, kind)]
    if "steps" in cap and len(steps) > cap["steps"]:
        raise ValueError("%d steps > %d cap for %s %s: use chunk()" % (len(steps), cap["steps"], surface, kind))
    doc = {"surface": surface, "kind": kind, "steps": steps}
    doc.update(args or {})
    folder = folder or PLAN_DIR
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, fname)
    data = json.dumps(doc, separators=(",", ":"), ensure_ascii=False)
    if len(data.encode()) > PLAN_MAX_BYTES:
        raise ValueError("plan is over 2 MB: split it with chunk()")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(data)
    return path


def write_plans(name, steps, surface, kind, args=None, folder=None, costs=None):
    """chunk() + write_plan() -> list of paths name_1.json, name_2.json ... (one call each, in order)."""
    parts = chunk(steps, surface, kind, costs=costs)
    if len(parts) == 1:
        return [write_plan(name, parts[0], surface, kind, args, folder)]
    return [write_plan("%s_%d" % (name, i + 1), c, surface, kind, args, folder) for i, c in enumerate(parts)]


# ---------------------------------------------------------------- verify


def norm(s):
    return re.sub(r"\s+", " ", str(s if s is not None else "")).strip()


def diff_lines(expected, actual_text, strip_empty=True):
    """Compare expected lines with text read back (get_text / browser_get_text). Returns ok, counts and the first
    mismatches with their line numbers (1-based), so the fix can resume at the first bad row."""
    got = actual_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if strip_empty:
        got = [g for g in got if g.strip()]
    exp = [e for e in expected if (e.strip() or not strip_empty)]
    bad = [(i + 1, e, got[i] if i < len(got) else None) for i, e in enumerate(exp) if i >= len(got) or norm(got[i]) != norm(e)]
    return {"ok": not bad and len(got) == len(exp), "expected": len(exp), "got": len(got),
            "first_bad_line": bad[0][0] if bad else None, "mismatches": bad[:10], "extra": got[len(exp):][:5]}


def diff_flat(expected_lines, actual_text, reported_chars=None):
    """For read-backs that drop line breaks (some editors return a document's value without them): compare the text
    with every line break removed, and the reported character count with expected characters + one per line break."""
    exp = "".join(expected_lines)
    got = actual_text.replace(chr(13), "").replace(chr(10), "")
    want_chars = sum(len(l) for l in expected_lines) + len(expected_lines)
    i = next((k for k in range(min(len(exp), len(got))) if exp[k] != got[k]), None)
    if i is None and len(exp) != len(got):
        i = min(len(exp), len(got))
    return {"ok": i is None and (reported_chars is None or int(reported_chars) == want_chars),
            "first_diff_at": i, "expected_chars": want_chars, "reported_chars": reported_chars,
            "context": (exp[max(0, (i or 0) - 20):(i or 0) + 20], got[max(0, (i or 0) - 20):(i or 0) + 20]) if i is not None else None}


def diff_rows(expected_rows, actual_rows, key=None, columns=None):
    """Compare records (list of dicts) with rows read back (read_table / collect). Match by key column or position."""
    cols = columns or (list(expected_rows[0].keys()) if expected_rows else [])
    idx = {norm(r.get(key)): r for r in actual_rows} if key else None
    bad, missing = [], []
    for i, e in enumerate(expected_rows):
        a = idx.get(norm(e.get(key))) if key else (actual_rows[i] if i < len(actual_rows) else None)
        if a is None:
            missing.append(i)
            continue
        d = {c: (e.get(c), a.get(c)) for c in cols if norm(e.get(c)) != norm(a.get(c))}
        if d:
            bad.append((i, d))
    return {"ok": not bad and not missing, "expected": len(expected_rows), "got": len(actual_rows),
            "missing": missing[:20], "mismatches": bad[:10]}


def diff_fields(expected, actual):
    """Form check: {field: value} expected vs read back."""
    d = {k: (v, actual.get(k)) for k, v in expected.items() if norm(v) != norm(actual.get(k))}
    return {"ok": not d, "checked": len(expected), "mismatches": d}


def first_unfinished(steps, done_count):
    """The 0-based step a resume should start at, from a result's resume_from.step or its count of done steps."""
    return max(0, min(int(done_count), len(steps)))


# ---------------------------------------------------------------- CLI


def _selftest():
    rows = [{"id": str(i), "name": "Item %02d" % i, "qty": str(i * 3)} for i in range(1, 31)]
    cs = [c_type("\t".join(r.values()) + "\n", target=T(label="Text editor"), delivery="background") for r in rows]
    pv = preview(cs, "computer", "batch")
    assert pv["steps"] == 30 and pv["fits_one_call"] and pv["background_steps"] == 30, pv
    bs = [b("input_text", ref="@e%d" % (i + 3), text=r["name"]) for i, r in enumerate(rows)]
    parts = chunk(bs, "browser", "batch")
    assert len(parts) == 2 and len(parts[0]) == 20, [len(x) for x in parts]
    grouped = []
    for i, r in enumerate(rows):
        grouped += [dict(f("type", into="Name", text=r["name"]), _group=i), dict(f("type", into="Qty", text=r["qty"]), _group=i),
                    dict(f("click", target="Add"), _group=i)]
    gp = chunk(grouped, "browser", "fast")
    assert all(len(x) % 3 == 0 for x in gp) and sum(len(x) for x in gp) == 90, [len(x) for x in gp]
    ps = [p("click_text", text="New"), p("input_text", text="x", expect={"editable_focused": True})]
    assert estimate(ps, "phone") > 0 and estimate(ps, "phone", kind="batch") > estimate(ps, "phone")
    pc = p_input_checked("12*7+3", "= 87")
    assert len(pc) == 2 and "expect" not in pc[0] and pc[1]["expect"] == {"text_visible": "= 87"}, pc
    assert expect_collisions(["= 100", "= 1000", "= 87"]) == [("= 100", "= 1000")]
    try:
        p("input_text", text="x", expect={"app": "a", "text_visible": "b"})
        raise AssertionError("two expect fields accepted")
    except ValueError:
        pass
    exp = ["\t".join(r.values()) for r in rows]
    assert diff_lines(exp, "\r\n".join(exp) + "\r\n")["ok"]
    assert diff_lines(exp, "\n".join(exp[:29]))["first_bad_line"] == 30
    assert diff_rows(rows, [dict(r) for r in rows], key="id")["ok"]
    assert not diff_fields({"a": "1"}, {"a": "2"})["ok"]
    assert diff_flat(exp, "".join(exp), sum(map(len, exp)) + len(exp))["ok"]
    assert diff_flat(exp, "".join(exp)[:-1])["first_diff_at"] is not None
    print("selftest ok:", json.dumps(pv))


def _main(argv):
    if len(argv) >= 1 and argv[0] == "selftest":
        return _selftest()
    if len(argv) >= 2 and argv[0] == "preview":
        with open(argv[1], encoding="utf-8") as fh:
            doc = json.load(fh)
        steps = doc if isinstance(doc, list) else doc.get("steps", [])
        surface = (doc.get("surface") if isinstance(doc, dict) else None) or (argv[2] if len(argv) > 2 else "computer")
        kind = (doc.get("kind") if isinstance(doc, dict) else None) or (argv[3] if len(argv) > 3 else "batch")
        print(json.dumps(preview(steps, surface, kind), indent=1))
        return
    print(__doc__)


if __name__ == "__main__":
    _main(sys.argv[1:])
