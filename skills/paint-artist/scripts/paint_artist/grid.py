"""Grid composite: one picture split into N x M cells by straight dividers, each cell painted in its own style.

prepare: one sub-job per cell in JOB/cells/<i>_<style>/ (the style prepared on the WHOLE image, so its look is right).
plan:    each style is planned on the whole image, then its strokes are clipped to its cell: the painted footprint
         (centreline +- width/2) stays `inset` px clear of every internal divider; pieces shorter than 2 px are
         dropped (dots are kept when inside). Only the colours a cell really uses go into ONE combined palette strip
         (exact duplicates merged); canvas.png is (re)written here, so open it in Paint AFTER plan. Layers are
         ordered cell by cell (a cell is finished before the next one starts), then the dividers (Pencil, dark),
         then the frame. The whole grid is simulated.
emit:    ONE stored plan if the estimate fits the time cap (500 s), else one plan per cell (dividers and frame go
         with the last); JOB/cells.json gives each cell's rectangle (drawing, canvas and screen px), style, plan
         file, step range and estimated start / end seconds from the batch start.
"""
import json
import math
import os
import shutil

import numpy as np
from PIL import Image, ImageDraw

from . import color as col
from . import planner as pl
from . import prepare as pr
from . import simulate as sim

MIN_SWATCH = 6
_DRY = [False]


# ------------------------------------------------------------------------------------------- geometry
def parse_grid(spec):
    r, c = spec.lower().split('x') if 'x' in spec.lower() else (spec, spec)
    return int(r), int(c)


def cell_rects(W, H, rows, cols, split_x=None, split_y=None):
    """Cells in reading order. split_x / split_y: interior divider positions as fractions of the drawing area
    (cols - 1 and rows - 1 values, increasing); default uniform."""
    def bounds(n, split, size):
        if not split:
            return np.linspace(0, size, n + 1)
        if len(split) != n - 1 or any(not 0 < v < 1 for v in split) or list(split) != sorted(split):
            raise SystemExit('split positions must be %d increasing fractions in (0, 1), got %s' % (n - 1, split))
        return np.array([0.0] + [v * size for v in split] + [float(size)])
    xs = bounds(cols, split_x, W)
    ys = bounds(rows, split_y, H)
    return [(float(xs[c]), float(ys[r]), float(xs[c + 1]), float(ys[r + 1])) for r in range(rows) for c in range(cols)]


def clip_segment(p, q, box):
    """Liang-Barsky: clip segment p-q to box (x0, y0, x1, y1); returns (p', q') or None."""
    x0, y0, x1, y1 = box
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return None
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
    if t0 > t1:
        return None
    return (p[0] + t0 * dx, p[1] + t0 * dy), (p[0] + t1 * dx, p[1] + t1 * dy)


def clip_polyline(pts, box, min_len=2.0):
    pts = [tuple(p) for p in pts]
    total = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    if total < 1.5:                                   # a dot: keep it if inside
        x, y = pts[0]
        return [pts] if box[0] <= x <= box[2] and box[1] <= y <= box[3] else []
    out, cur = [], []
    for a, b in zip(pts, pts[1:]):
        c = clip_segment(a, b, box)
        if c is None:
            if cur:
                out.append(cur)
                cur = []
            continue
        s, e = c
        if cur and math.dist(cur[-1], s) < 1e-6:
            cur.append(e)
        else:
            if cur:
                out.append(cur)
            cur = [s, e]
        if math.dist(e, b) > 1e-6:                    # left the box inside this segment
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [p for p in out if sum(math.dist(a, b) for a, b in zip(p, p[1:])) >= min_len]


def serpentine(box, rect, w, W, H):
    """Ground serpentine covering the cell: rows evenly spaced inside the centreline box (clamped to the image)."""
    x0, y0 = max(box[0], w / 2), max(box[1], w / 2)
    x1, y1 = min(box[2], W - w / 2), min(box[3], H - w / 2)
    if x1 < x0:
        x0 = x1 = (rect[0] + rect[2]) / 2
    if y1 < y0:
        y0 = y1 = (rect[1] + rect[3]) / 2
    n = max(1, int(math.ceil((y1 - y0) / (0.75 * w))) + 1)
    pts = []
    for j, y in enumerate(np.linspace(y0, y1, n)):
        xs = (x0, x1) if j % 2 == 0 else (x1, x0)
        pts += [[round(xs[0], 1), round(float(y), 1)], [round(xs[1], 1), round(float(y), 1)]]
    return pts


def footprint_box(rect, W, H, w, inset):
    """Box for stroke CENTRELINES so the footprint stays `inset` px clear of internal dividers."""
    x0, y0, x1, y1 = rect
    h = w / 2.0
    bx0 = x0 + inset + h if x0 > 0.5 else -1e9
    by0 = y0 + inset + h if y0 > 0.5 else -1e9
    bx1 = x1 - inset - h if x1 < W - 0.5 else 1e9
    by1 = y1 - inset - h if y1 < H - 0.5 else 1e9
    return bx0, by0, bx1, by1


# ------------------------------------------------------------------------------------------- prepare
def prepare_grid(src, job, styles, grid, load_style, width=None, height=672, fit='crop', focus=None, face_box=None,
                 order=None, divider_width=5, inset=2, divider_color='#1a1a1a', frame=True, cell_overrides=None,
                 split_x=None, split_y=None):
    rows, cols = parse_grid(grid)
    if len(styles) != rows * cols:
        raise SystemExit('--styles needs %d names for a %s grid, got %d' % (rows * cols, grid, len(styles)))
    os.makedirs(job, exist_ok=True)
    cells = []
    for i, st in enumerate(styles):
        sub = os.path.join(job, 'cells', '%d_%s' % (i, os.path.splitext(os.path.basename(st))[0]))
        preset = load_style(st)
        if cell_overrides and str(i) in cell_overrides:
            preset = deep_update(preset, cell_overrides[str(i)])
        meta = pr.prepare(src, sub, preset, width, height, fit, focus, face_box, None, False, False)
        cells.append({'index': i, 'style': preset.get('name', st), 'job': os.path.relpath(sub, job)})
    W, H = meta['W'], meta['H']
    rects = cell_rects(W, H, rows, cols, split_x, split_y)
    for c, r in zip(cells, rects):
        c['rect'] = [round(v, 2) for v in r]
    order = order or list(range(rows * cols))
    shutil.copy(os.path.join(job, cells[0]['job'], 'target_raw.png'), os.path.join(job, 'target_raw.png'))
    shutil.copy(os.path.join(job, cells[0]['job'], 'target_raw.png'), os.path.join(job, 'target.png'))
    gmeta = dict(source=meta['source'], W=W, H=H, preset='grid', focus=meta['focus'], face_box=meta['face_box'], frame=frame,
                 grid=dict(rows=rows, cols=cols, order=order, cells=cells, divider_width=divider_width, inset=inset,
                           divider_color=divider_color, split_x=split_x, split_y=split_y))
    with open(os.path.join(job, 'meta.json'), 'w') as f:
        json.dump(gmeta, f, indent=1)
    return gmeta


def deep_update(a, b):
    a = json.loads(json.dumps(a))
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            a[k] = deep_update(a[k], v)
        else:
            a[k] = v
    return a


# ------------------------------------------------------------------------------------------- plan
class _FrameCtx:
    """Minimal context for planner.layer_frame on the combined canvas."""
    def __init__(self, meta):
        self.meta = meta
        self.ox, self.oy = meta['layout']['draw_origin']
        self.W, self.H = meta['W'], meta['H']


def plan_grid(job, tools, detail=1.0, seed=0, log=None):
    log = log or (lambda *x: None)
    with open(os.path.join(job, 'meta.json')) as f:
        gmeta = json.load(f)
    G = gmeta['grid']
    W, H = gmeta['W'], gmeta['H']
    inset = G['inset']
    combined, cell_layers, cell_stats, sub_sims = [], {}, {}, {}

    def cidx(rgb):
        rgb = [round(float(v), 4) for v in rgb]
        for i, c in enumerate(combined):
            if np.abs(np.array(c) - rgb).max() < 1.5 / 255:
                return i
        combined.append(rgb)
        return len(combined) - 1

    for cell in G['cells']:
        sub = os.path.join(job, cell['job'])
        with open(os.path.join(sub, 'preset.json')) as f:
            preset = json.load(f)
        log('cell %d (%s): planning on the whole image' % (cell['index'], cell['style']))
        plan, subfull = pl.plan(sub, preset, tools, detail, seed, frame=False, log=lambda *x: None)
        sox, soy = json.load(open(os.path.join(sub, 'meta.json')))['layout']['draw_origin']
        sub_sims[cell['index']] = subfull[soy:soy + H, sox:sox + W]
        pal = plan['palette']
        layers, n_in, n_out = [], 0, 0
        for L in plan['layers']:
            box = footprint_box(cell['rect'], W, H, L['width'], inset)
            S = []
            nm = L.get('name', '')
            if (nm.startswith('ground') or nm.endswith('-base')) and L['strokes']:
                # a ground fill: re-lay its serpentine inside the cell (clipping the whole-image one leaves bands)
                n_in += 1
                S.append([cidx(pal[L['strokes'][0][0]]), serpentine(box, cell['rect'], L['width'], W, H)])
            for k, pts in (L['strokes'] if not S else []):
                n_in += 1
                for piece in clip_polyline(pts, box):
                    S.append([cidx(pal[k]), [[round(x, 1), round(y, 1)] for x, y in piece]])
            n_out += len(S)
            if S:
                S.sort(key=lambda s: s[0])
                e = dict(L, strokes=S, name='cell%d-%s' % (cell['index'], L['name']), cell=cell['index'])
                layers.append(e)
            if (nm.startswith('ground') or nm.endswith('-base')) and S:
                # the wide serpentine's round caps cannot reach the cell's square corners: a thin loop of the same
                # colour along the cell's inner edges fills them (corners left are smaller than the divider)
                ew = 8
                b = footprint_box(cell['rect'], W, H, ew, inset)
                x0, y0 = max(b[0], ew / 2), max(b[1], ew / 2)
                x1, y1 = min(b[2], W - ew / 2), min(b[3], H - ew / 2)
                loop = [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]
                layers.append(dict(L, width=ew, name='cell%d-%s-edges' % (cell['index'], L['name']), cell=cell['index'],
                                   strokes=[[S[0][0], [[round(x, 1), round(y, 1)] for x, y in loop]]]))
        cell_layers[cell['index']] = layers
        cell_stats[cell['index']] = {'full_plan_strokes': n_in, 'cell_strokes': n_out}
        log('   %d of %d strokes kept in the cell' % (n_out, n_in))
    # dividers + frame colours, then the combined canvas
    div_k = cidx(col.as_rgb(G['divider_color']).tolist())
    fr = {}
    if gmeta.get('frame'):
        for name, c in pr.FRAME_COLOURS.items():
            fr[name] = cidx(list(c))
    pal = np.array(combined)
    order = np.argsort(col.rgb2lab(pal)[:, 0], kind='stable')          # strip dark to light
    inv = np.empty(len(order), int)
    inv[order] = np.arange(len(order))
    pal = pal[order]
    Hc = pr.DRAW_Y0 + H + pr.MARGIN_B
    max_k = (Hc - pr.DRAW_Y0 - 1) // MIN_SWATCH
    if len(pal) > max_k:
        raise SystemExit('the grid needs %d colours; the %d px canvas strip holds at most %d (swatch >= %d px): '
                         'use fewer cells, smaller palettes (k) or a taller canvas' % (len(pal), Hc, max_k, MIN_SWATCH))
    layout = make_canvas_any(W, H, pal, os.path.join(job, 'canvas.png'))
    remap = lambda S: [[int(inv[k]), pts] for k, pts in S]
    all_layers = []
    for i in G['order']:
        for L in cell_layers[i]:
            all_layers.append(dict(L, strokes=sorted(remap(L['strokes']), key=lambda s: s[0])))
    dw = G['divider_width']
    dk = int(inv[div_k])
    xs = sorted({c['rect'][0] for c in G['cells']} - {0.0})
    ys = sorted({c['rect'][1] for c in G['cells']} - {0.0})
    div = [[dk, [[x, 0.0], [x, float(H)]]] for x in xs] + [[dk, [[0.0, y], [float(W), y]]] for y in ys]
    if div:
        all_layers.append({'name': 'grid-dividers', 'tool': 'pencil', 'width': dw, 'opacity': 1.0, 'strokes': div, 'cell': 'grid', 'speed': 4000})
    meta = dict(gmeta, layout=layout, palette=[[round(float(v), 5) for v in c] for c in pal],
                palette_info={'mode': 'grid', 'frame': {n: int(inv[k]) for n, k in fr.items()}})
    if gmeta.get('frame'):
        for L, S in pl.layer_frame(_FrameCtx(meta), {}):
            all_layers.append(dict(L, opacity=1.0, strokes=[[int(k), [list(p) for p in pts]] for k, pts in S], cell='grid'))
    with open(os.path.join(job, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    # simulate the whole grid
    full = pr.load_rgb(os.path.join(job, 'canvas.png'))
    ox, oy = layout['draw_origin']
    for li, L in enumerate(all_layers):
        sim.render(full, [(k, pts) for k, pts in L['strokes']], L['width'], L['tool'], L.get('opacity', 1.0), pal, tools,
                   offset=(ox, oy), seed=seed + li)
    drawing = full[oy:oy + H, ox:ox + W]
    per_cell = {}
    for cell in G['cells']:
        x0, y0, x1, y1 = [int(round(v)) for v in cell['rect']]
        t = sub_sims[cell['index']]
        a, b = drawing[y0 + 6:y1 - 6, x0 + 6:x1 - 6], t[y0 + 6:y1 - 6, x0 + 6:x1 - 6]
        per_cell[cell['index']] = dict(cell_stats[cell['index']], cell_vs_full_style_sim=round(col.delta_e(a, b), 2))
    from .score import scores
    sc = scores(drawing, pr.load_rgb(os.path.join(job, 'target_raw.png')), meta.get('face_box'))
    plan = {'version': 1, 'preset': 'grid', 'job': os.path.abspath(job), 'W': W, 'H': H, 'palette': meta['palette'],
            'layers': all_layers, 'grid': G, 'cells': per_cell, 'sim_score': sc,
            'stats': {'strokes': sum(len(L['strokes']) for L in all_layers), 'layers': len(all_layers),
                      'colour_groups': sum(len({s[0] for s in L['strokes']}) for L in all_layers), 'colours': len(pal)}}
    return plan, full


def make_canvas_any(W, H, pal, path):
    """Like prepare.make_canvas, for up to (Hc - 10) // 6 swatches (smaller swatches when needed)."""
    K = len(pal)
    Wc, Hc = pr.DRAW_X0 + W + pr.MARGIN_R, pr.DRAW_Y0 + H + pr.MARGIN_B
    swh = min(17, (Hc - pr.DRAW_Y0 - 1) // K)
    img = np.ones((Hc, Wc, 3))
    for i, c in enumerate(pal):
        y0 = pr.DRAW_Y0 + swh * i
        img[y0:y0 + swh - 1, pr.STRIP_X0:pr.STRIP_X1 + 1] = np.round(np.asarray(c) * 255) / 255
    pr.save_rgb(img, path)
    return dict(canvas=[Wc, Hc], draw_origin=[pr.DRAW_X0, pr.DRAW_Y0], strip=dict(x0=pr.STRIP_X0, x1=pr.STRIP_X1, y0=pr.DRAW_Y0, swh=swh))


# ------------------------------------------------------------------------------------------- emit
def emit_grid(plan, meta, ui, tools, plans_dir, name, cap=500.0, dry=False):
    from . import emit_paint as ep
    G = meta['grid']
    groups = []                                       # (cell index or 'grid', [layers]) in paint order
    for L in plan['layers']:
        c = L.get('cell')
        if not groups or groups[-1][0] != c:
            groups.append((c, []))
        groups[-1][1].append(L)

    def run(groups_subset):
        em = ep.Emitter(meta, ui, tools)
        em.steps.append({'kind': 'set_value', 'target': dict(ui['opacity_slider']), 'value': '100', 'onError': 'continue'})
        marks = []
        for c, Ls in groups_subset:
            s0, t0 = len(em.steps), em.estimate()
            for L in Ls:
                if L['strokes']:
                    em.layer(L)
            marks.append((c, s0, len(em.steps) - 1, t0, em.estimate()))
        return em, marks

    _DRY[0] = dry
    em, marks = run(groups)
    total = em.estimate()
    if not dry:
        os.makedirs(plans_dir, exist_ok=True)
    files, cell_info = [], {}
    if total <= cap:
        path = os.path.join(plans_dir or '.', name + '.json')
        _write(path, em.steps)
        files.append({'file': os.path.basename(path), 'steps': len(em.steps), 'est_seconds': round(total)})
        for c, s0, s1, t0, t1 in marks:
            cell_info.setdefault(c, []).append({'plan': os.path.basename(path), 'steps': [s0, s1], 'est_start_s': round(t0, 1), 'est_end_s': round(t1, 1)})
    else:                                             # one plan per cell; dividers and frame ride with the last
        cells_groups = [g for g in groups if g[0] != 'grid']
        tail = [g for g in groups if g[0] == 'grid']
        t_offset = 0.0
        for gi, g in enumerate(cells_groups):
            part = [g] + (tail if gi == len(cells_groups) - 1 else [])
            emp, mk = run(part)
            path = os.path.join(plans_dir or '.', '%s_cell%d.json' % (name, g[0]))
            _write(path, emp.steps)
            files.append({'file': os.path.basename(path), 'steps': len(emp.steps), 'est_seconds': round(emp.estimate())})
            for c, s0, s1, t0, t1 in mk:
                cell_info.setdefault(c, []).append({'plan': os.path.basename(path), 'steps': [s0, s1],
                                                    'est_start_s': round(t_offset + t0, 1), 'est_end_s': round(t_offset + t1, 1)})
            t_offset += emp.estimate() + 8.0          # + call latency and collecting between plans
    org = em.org
    s = em.s
    ox, oy = meta['layout']['draw_origin']
    cells_out = []
    for cell in G['cells']:
        x0, y0, x1, y1 = cell['rect']
        cx0, cy0, cx1, cy1 = ox + x0, oy + y0, ox + x1, oy + y1
        cells_out.append({'index': cell['index'], 'style': cell['style'],
                          'rect_drawing_px': [round(v, 1) for v in (x0, y0, x1, y1)],
                          'rect_canvas_px': [round(v, 1) for v in (cx0, cy0, cx1, cy1)],
                          'rect_screen_px': [round(org[0] + v * s, 1) for v in (cx0,)] + [round(org[1] + cy0 * s, 1)] +
                                            [round(org[0] + cx1 * s, 1), round(org[1] + cy1 * s, 1)],
                          'paint_order': G['order'].index(cell['index']), 'segments': cell_info.get(cell['index'], [])})
    out = {'canvas_origin_screen': list(org), 'scale': s, 'one_plan': total <= cap, 'plans': files,
           'est_total_seconds': round(total if total <= cap else sum(f['est_seconds'] for f in files)),
           'cells': sorted(cells_out, key=lambda c: c['paint_order']),
           'finish': cell_info.get('grid', []),
           'note': 'step indexes are 0-based positions in the plan file steps; times are estimates from the batch start '
                   '(add about 3 s of call latency); screen rects are valid for the canvas origin above (re-run emit after locate)'}
    return out


def _write(path, steps):
    if _DRY[0]:
        return
    with open(path, 'w') as f:
        json.dump({'surface': 'computer', 'kind': 'batch', 'steps': steps}, f, separators=(',', ':'))
