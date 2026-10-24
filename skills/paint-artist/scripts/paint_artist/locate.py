"""Calibration helpers that work from a screen grab (no app API needed).

locate_canvas: find the canvas on screen. Primary method: match the palette strip (the swatch colours at their
exact spacing, never painted over) at each candidate display scale, which works on a blank or a finished canvas.
Fallback (blank canvas only): the largest near-white region with the canvas aspect. Returns origin (screen
top-left of the canvas), scale (= display scale at 100 % zoom) and swatch_err (mean RGB error 0..255 at the
swatch centres; under 3 = every colour pick will land).

Tool darkness calibration: calib_layout() builds a tiny canvas + plan that paints one black stroke per tool;
measure_tools() reads the grab and returns the coverage of each stroke (1 - stroke luminance / paper).
"""
import json
import math

import numpy as np
from scipy import ndimage as ndi


def locate_canvas(grab, meta, white=235, scales=(1.0, 1.25, 1.5, 1.75, 2.0)):
    """Find the canvas on a full-screen grab. Primary: match the palette strip (never painted over) at each
    candidate display scale; fallback: the largest near-white region with the canvas aspect (blank canvas)."""
    best = strip_search(grab, meta, scales)
    if best and best['swatch_err'] < 2.5:
        return best
    return white_region(grab, meta, white) or best or {'error': 'canvas not found'}


def strip_search(grab, meta, scales):
    st = meta['layout']['strip']
    pal = np.asarray(meta['palette']) * 255
    g = grab * 255
    H, W = g.shape[:2]
    out = None
    for s in scales:
        offs = [int(round((st['y0'] + st['swh'] * i + st['swh'] // 2 - (st['y0'] + st['swh'] // 2)) * s)) for i in range(len(pal))]
        span = offs[-1]
        if span >= H:
            continue
        E = np.zeros((H - span, W))
        lm = int(round((st['x0'] - 4) * s))                  # never-painted white margin left of the strip
        gp = int(round((st['swh'] - 1) * s))                  # 1 px white gap under each swatch
        for i, dy in enumerate(offs):
            E += np.abs(g[dy:dy + H - span] - pal[i]).mean(-1)
            shifted = np.full((H - span, W), 255.0)
            shifted[:, lm:] = np.abs(g[dy:dy + H - span, :W - lm] - 255).mean(-1)
            E += shifted * 0.5
            if dy + gp < H:
                rows = g[dy + gp:dy + gp + H - span]
                gap = np.full((H - span, W), 255.0)
                gap[:len(rows)] = np.abs(rows - 255).mean(-1)
                E += gap * 0.5
        E /= len(pal) * 2
        y, x = np.unravel_index(E.argmin(), E.shape)
        err = float(E[y, x])
        # each swatch is a flat block: the minimum is a plateau; its centre is the swatch-column centre
        lab, _ = ndi.label(E <= err + 2.0)
        ys, xs = np.nonzero(lab == lab[y, x])
        if out is None or err < out['swatch_err']:
            # the plateau's top-left = the top-left pixel of the swatch column (x0, y0) on screen
            ox, oy = xs.min() - st['x0'] * s, ys.min() - st['y0'] * s
            out = {'origin': [int(round(ox)), int(round(oy))], 'scale': s, 'swatch_err': round(err, 2), 'method': 'strip'}
    return out


def white_region(grab, meta, white=235):
    Wc, Hc = meta['layout']['canvas']
    m = (grab * 255 >= white).all(-1)
    lab, n = ndi.label(m)
    best = None
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if w < 50 or h < 50:
            continue
        err = abs((w / h) - (Wc / Hc))
        if err < 0.03 and (best is None or w * h > best[0]):
            best = (w * h, sl, err)
    if best is None:
        return None
    _, sl, err = best
    y0, x0 = sl[0].start, sl[1].start
    scale = (sl[1].stop - sl[1].start) / Wc
    res = {'origin': [int(x0), int(y0)], 'scale': round(float(scale), 4), 'aspect_err': round(float(err), 4), 'method': 'white'}
    res['swatch_err'] = swatch_error(grab, meta, res['origin'], scale)
    return res


def swatch_error(grab, meta, origin, scale=1.0):
    st = meta['layout']['strip']
    errs = []
    for i, c in enumerate(meta['palette']):
        x = origin[0] + ((st['x0'] + st['x1']) / 2) * scale
        y = origin[1] + (st['y0'] + st['swh'] * i + st['swh'] // 2) * scale
        px = grab[int(round(y)), int(round(x))]
        errs.append(np.abs(px * 255 - np.array(c) * 255).mean())
    return round(float(np.mean(errs)), 2)


# (tool, opacity, passes, direction). Every tool once, horizontally; the calligraphy brush also vertically and on
# both diagonals so its nib angle can be fitted; watercolour twice to check that passes stack.
CALIB_TOOLS = [('brush', 1.0, 1, 0), ('oil', 1.0, 1, 0), ('watercolour', 1.0, 1, 0), ('watercolour', 1.0, 2, 0),
               ('pencil', 0.35, 1, 0), ('pencil', 1.0, 1, 0), ('calligraphy', 1.0, 1, 0), ('airbrush', 1.0, 1, 0),
               ('crayon', 1.0, 1, 0), ('marker', 1.0, 1, 0), ('natural_pencil', 1.0, 1, 0),
               ('calligraphy', 1.0, 1, 90), ('calligraphy', 1.0, 1, 45), ('calligraphy', 1.0, 1, 135)]
CALIB_W, CALIB_WIDTH = 16, 16


def calib_size():
    nh = sum(1 for t in CALIB_TOOLS if t[3] == 0)
    return 460, 40 + nh * 40


def calib_strokes():
    """Black strokes, width 16: horizontals 40 px apart on the left, the angled calligraphy strokes on the right."""
    W, H = calib_size()
    out, i = [], 0
    xr = W - 90                                  # right column for the angled strokes
    ang = [t for t in CALIB_TOOLS if t[3] != 0]
    for tool, op, passes, d in CALIB_TOOLS:
        if d == 0:
            y = 30 + i * 40
            i += 1
            pts = [[30, y], [xr - 40, y]]
        else:
            j = ang.index((tool, op, passes, d))
            cy = 70 + j * ((H - 100) / max(1, len(ang) - 1)) if len(ang) > 1 else H / 2
            r = 30
            dx, dy = math.cos(math.radians(d)) * r, math.sin(math.radians(d)) * r
            pts = [[xr + 30 - dx, cy - dy], [xr + 30 + dx, cy + dy]]
        out.append({'tool': tool, 'opacity': op, 'passes': passes, 'dir': d, 'width': CALIB_WIDTH, 'pts': pts})
    return out


def _profile(dark, s):
    """Darkness along the stroke's normal, averaged along its middle 60 %, and ink area per unit length."""
    (x0, y0), (x1, y1) = s['pts']
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    ts = np.linspace(0.2 * L, 0.8 * L, 60)
    offs = np.arange(-20, 20.5, 0.5)
    H, W = dark.shape
    prof = []
    for o in offs:
        xs = x0 + ts * ux + o * nx
        ys = y0 + ts * uy + o * ny
        xi, yi = np.clip(np.round(xs).astype(int), 0, W - 1), np.clip(np.round(ys).astype(int), 0, H - 1)
        prof.append(dark[yi, xi].mean())
    prof = np.array(prof)
    return offs, prof


def measure_tools(drawing, strokes):
    """drawing: HxWx3 crop of the drawing area. Per stroke, from the darkness profile across it (averaged along
    its middle 60 %): alpha = mean of the stroke core (profile >= 75 % of its peak), peak, thickness_px = ink area /
    peak; for the calligraphy brush the nib angle and length fitted on four directions."""
    dark = 1 - drawing.mean(-1)
    res = {}
    cal = []
    for s in strokes:
        offs, prof = _profile(dark, s)
        peak = prof.max()
        core = prof[prof >= 0.75 * peak]
        centre = core.mean() if len(core) else 0.0          # coverage of the stroke body (textured tools vary)
        thick = float(prof.sum() * 0.5 / max(peak, 1e-6))   # ink area / peak = effective width
        key = '%s%s@%d%s' % (s['tool'], '_x2' if s['passes'] == 2 else '', round(s['opacity'] * 100), '' if s['dir'] == 0 else '/%d' % s['dir'])
        res[key] = {'alpha': round(float(centre), 3), 'peak': round(float(peak), 3), 'thickness_px': round(thick, 1)}
        if s['tool'] == 'calligraphy':
            cal.append((s['dir'], thick))
    if len(cal) >= 3:
        best = None
        for a in range(0, 180):
            for wv in np.arange(4, 24, 0.5):
                for pen in np.arange(0, 6, 0.5):
                    e = sum((wv * abs(math.sin(math.radians(d - a))) + pen - t) ** 2 for d, t in cal)
                    if best is None or e < best[0]:
                        best = (e, a, wv, pen)
        res['calligraphy_nib'] = {'angle_deg': best[1], 'nib_px_at_16': float(best[2]), 'min_px': float(best[3]),
                                  'fit_rms': round(math.sqrt(best[0] / len(cal)), 2)}
    return res


def tools_from_measure(tools, res, width=CALIB_WIDTH):
    """Fold measured numbers into a paint_tools.json dict (alpha, width_scale, nib) and mark them measured."""
    t = tools['tools']
    for name in t:
        k = '%s@100' % name
        if name == 'pencil':
            k = 'pencil@100'
        if k not in res:
            continue
        m = res[k]
        t[name]['alpha'] = round(min(1.0, m['alpha']), 3)
        if name not in ('calligraphy',):
            t[name]['width_scale'] = round(m['thickness_px'] / width, 2)
        t[name]['measured'] = True
    if 'calligraphy_nib' in res:
        n = res['calligraphy_nib']
        t['calligraphy']['nib'] = n['angle_deg']
        t['calligraphy']['width_scale'] = round(n['nib_px_at_16'] / width, 2)
        t['calligraphy']['nib_min_px'] = n['min_px']
    if 'watercolour_x2@100' in res:
        t['watercolour']['alpha_two_passes'] = res['watercolour_x2@100']['alpha']
    if 'pencil@35' in res:
        t['pencil']['alpha_at_35'] = res['pencil@35']['alpha']
    return tools
