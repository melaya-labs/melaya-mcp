"""speed-calib / speed-measure: find the fastest pointer settings Paint still draws without missing pixels.

speed-calib writes a standard canvas (540x690, drawing area 450x672) and 6 plans:
  <name>_setup.json   at a slow reference setting: a closed 2 px Pencil box around every test cell (so a leaking
                      fill cannot spread), the 1 px Pencil rings to be filled, and the connectivity probe
                      (a 1 px diagonal diamond: a 4-connected bucket stays inside it, an 8-connected one leaks)
  <name>_s0..s4.json  one row each, SETTINGS[i] = (speed px/s, stepPx, strokeGapMs): the same Brush 6 px and
                      Pencil 2 px pattern (zigzag, short strokes, dots) and one Fill click inside each ring
Run them in order (one batch call each, Paint in front, no window_id) and note each batch's duration.
speed-measure grabs (or reads the saved file), compares every row with row s0 (the slow reference), counts missing
pixels and unfilled rings per tool, reads the probe, and reports for each tool the fastest setting with under 1 %
missing pixels and all fills done; --install writes them into paint_tools.json (brush, pencil, fill) and
fill_conn (4 or 8).
"""
import json
import os

import numpy as np
from scipy import ndimage as ndi

SETTINGS = [(1500, 2, 10), (8000, 16, 2), (12000, 16, 1), (16000, 16, 0), (20000, 16, 0)]
W, H = 450, 672
ROW_H = 112                      # 5 rows of tests + the probe row at the bottom
COLS = [(6, 144), (156, 294), (306, 444)]     # brush, pencil, fill cells (x0, x1) inside the drawing area
BLACK, RED, WHITE = 0, 1, 2


def row_box(i):
    return 6 + i * ROW_H, 6 + i * ROW_H + ROW_H - 12


def pattern(x0, x1, y0, y1):
    """Zigzag, 8 short strokes, 8 dots inside the cell."""
    zz = [[x0 + 8 + j * (x1 - x0 - 16) / 8.0, y0 + 10 if j % 2 == 0 else y0 + 40] for j in range(9)]
    shorts = [[[x0 + 10 + j * 15, y0 + 55], [x0 + 16 + j * 15, y0 + 62]] for j in range(8)]
    dots = [[[x0 + 10 + j * 15, y0 + 80], [x0 + 11 + j * 15, y0 + 80]] for j in range(8)]
    return [zz] + shorts + dots


def rings(x0, y0):
    """Three 1 px squares (closed), returns (ring strokes, seed points)."""
    out, seeds = [], []
    for j in range(3):
        a, b = x0 + 8 + j * 44, y0 + 18
        s = 34
        out.append([[a, b], [a + s, b], [a + s, b + s], [a, b + s], [a, b]])
        seeds.append([a + s / 2, b + s / 2])
    return out, seeds


def box(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]


def generate(job, name, plans_dir, emit_fn, prepare_canvas):
    os.makedirs(job, exist_ok=True)
    pal = np.array([[0, 0, 0], [0.85, 0.1, 0.1], [1, 1, 1]], float)
    layout = prepare_canvas(W, H, pal, os.path.join(job, 'canvas.png'))
    meta = dict(W=W, H=H, layout=layout, palette=pal.tolist(), palette_info={'frame': {}}, frame=False, focus=[], face_box=None,
                speedcalib=dict(settings=SETTINGS, row_h=ROW_H, cols=COLS))
    with open(os.path.join(job, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    ref = dict(speed=SETTINGS[0][0], stepPx=SETTINGS[0][1], strokeGapMs=SETTINGS[0][2])
    boxes, ring_strokes = [], []
    for i in range(len(SETTINGS)):
        y0, y1 = row_box(i)
        for (x0, x1) in COLS:
            boxes.append([BLACK, box(x0 - 3, y0 - 3, x1 + 3, y1 + 3)])
        rs, _ = rings(COLS[2][0], y0)
        ring_strokes += [[BLACK, r] for r in rs]
    py0 = 6 + len(SETTINGS) * ROW_H
    probe_box = box(COLS[2][0] - 3, py0 - 3, COLS[2][0] + 100, py0 + 60)
    boxes.append([BLACK, probe_box])
    cx, cy, r = COLS[2][0] + 40, py0 + 28, 20
    diamond = [[cx, cy - r], [cx + r, cy], [cx, cy + r], [cx - r, cy], [cx, cy - r]]      # pure 45 deg, 1 px
    setup = {'layers': [
        dict(name='boxes', tool='pencil', width=2, opacity=1.0, strokes=boxes, **ref),
        dict(name='rings', tool='pencil', width=1, opacity=1.0, strokes=ring_strokes + [[BLACK, diamond]], **ref),
        dict(name='probe-fill', tool='fill', width=1, opacity=1.0, strokes=[[RED, [[cx, cy], [cx + 0.5, cy]]]], **ref)]}
    out = {'setup': emit_fn(setup, meta, os.path.join(plans_dir, name + '_setup.json'))}
    for i, (sp, st, gap) in enumerate(SETTINGS):
        y0, y1 = row_box(i)
        cfg = dict(speed=sp, stepPx=st, strokeGapMs=gap)
        _, seeds = rings(COLS[2][0], y0)
        plan = {'layers': [
            dict(name='brush', tool='brush', width=6, opacity=1.0, strokes=[[BLACK, s] for s in pattern(COLS[0][0], COLS[0][1], y0, y1)], **cfg),
            dict(name='pencil', tool='pencil', width=2, opacity=1.0, strokes=[[BLACK, s] for s in pattern(COLS[1][0], COLS[1][1], y0, y1)], **cfg),
            dict(name='fills', tool='fill', width=1, opacity=1.0, strokes=[[RED, [s, [s[0] + 0.5, s[1]]]] for s in seeds], **cfg)]}
        out['s%d' % i] = emit_fn(plan, meta, os.path.join(plans_dir, '%s_s%d.json' % (name, i)))
    return out


def measure(drawing, times=None):
    """drawing: HxWx3 drawing-area crop of the finished calibration canvas."""
    dark = drawing.mean(-1) < 0.5
    red = (drawing[..., 0] > 0.6) & (drawing[..., 1] < 0.4) & (drawing[..., 2] < 0.4)
    res = {'settings': [], 'recommended': {}}
    ry0, ry1 = row_box(0)
    refs = {}
    for t, (x0, x1) in zip(('brush', 'pencil'), COLS[:2]):
        refs[t] = ndi.binary_dilation(dark[ry0:ry1, x0:x1], iterations=1)
    for i, s in enumerate(SETTINGS):
        y0, y1 = row_box(i)
        row = {'index': i, 'speed': s[0], 'stepPx': s[1], 'strokeGapMs': s[2]}
        for t, (x0, x1) in zip(('brush', 'pencil'), COLS[:2]):
            test = dark[y0:y1, x0:x1]
            ref = dark[ry0:ry1, x0:x1]
            miss = ref & ~ndi.binary_dilation(test, iterations=1)
            row[t + '_missing'] = round(float(miss.sum()) / max(1, ref.sum()), 4)
        filled = 0
        for j, (sx, sy) in enumerate(rings(COLS[2][0], y0)[1]):
            filled += bool(red[int(sy), int(sx)] and red[int(sy) + 8, int(sx) + 8])
        row['fills_done'] = filled
        if times and i < len(times):
            row['seconds'] = times[i]
        res['settings'].append(row)
    py0 = 6 + len(SETTINGS) * ROW_H
    outside = red[py0 + 2:py0 + 10, COLS[2][0] + 1:COLS[2][0] + 10].mean()
    inside = red[py0 + 26:py0 + 30, COLS[2][0] + 38:COLS[2][0] + 42].mean()
    res['fill_connectivity'] = 8 if outside > 0.5 else (4 if inside > 0.5 else None)
    for t in ('brush', 'pencil'):
        ok = [r for r in res['settings'] if r[t + '_missing'] < 0.01]
        best = max(ok, key=lambda r: (r['speed'] / max(1, r['strokeGapMs'] + 1), r['stepPx'])) if ok else None
        if times:
            ok_t = [r for r in ok if 'seconds' in r]
            best = min(ok_t, key=lambda r: r['seconds']) if ok_t else best
        res['recommended'][t] = best and {k: best[k] for k in ('speed', 'stepPx', 'strokeGapMs')}
    okf = [r for r in res['settings'] if r['fills_done'] == 3]
    bestf = min(okf, key=lambda r: r['strokeGapMs']) if okf else None
    res['recommended']['fill'] = bestf and {'strokeGapMs': bestf['strokeGapMs']}
    return res
