"""Tool-accurate compositing simulator.

Every stroke is rasterised as a mask on its own bounding box (supersampled for antialiased tools), then
alpha-composited onto the float canvas with alpha = tool coverage x opacity. One stroke never darkens itself
(Paint renders a stroke as one unit). The coverage numbers come from the app adapter's tool model
(paint_tools.json, measured live 2026-10-24: Brush 1.00, Oil 0.81 streaky, Watercolour 0.70 per pass and 12 px wide at
size 16, Pencil = opacity, Calligraphy nib 135 deg; see references/paint-win11.md).
"""
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))


def load_tools(path=None):
    p = path or os.path.join(HERE, 'paint_tools.json')
    with open(p) as f:
        return json.load(f)['tools']


def effective_alpha(tool, opacity, tools):
    t = tools[tool]
    a = t['alpha']
    if t.get('opacity_setting'):
        a *= opacity
    return min(1.0, a)


def _normals(pts):
    p = np.asarray(pts, float)
    if len(p) < 2:
        return np.tile([[0.0, 1.0]], (len(p), 1))
    seg = np.diff(p, axis=0)
    n = np.stack([-seg[:, 1], seg[:, 0]], 1)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
    out = np.zeros_like(p)
    out[:-1] += n
    out[1:] += n
    out /= np.maximum(np.linalg.norm(out, axis=1, keepdims=True), 1e-9)
    return out


def stroke_mask(pts, width, spec, rng):
    """Return (mask float32 HxW in 0..1, x0, y0) for one stroke in canvas pixel coordinates."""
    pts = [(float(x), float(y)) for x, y in pts]
    r = width / 2.0
    pad = int(math.ceil(r + 2 + spec.get('soft', 0) * width))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, y0 = int(math.floor(min(xs))) - pad, int(math.floor(min(ys))) - pad
    x1, y1 = int(math.ceil(max(xs))) + pad, int(math.ceil(max(ys))) + pad
    w, h = x1 - x0 + 1, y1 - y0 + 1
    ss = 2 if spec.get('aa', True) else 1
    m = Image.new('L', (w * ss, h * ss), 0)
    d = ImageDraw.Draw(m)
    q = [((x - x0) * ss, (y - y0) * ss) for x, y in pts]
    nb = int(spec.get('bristles', 0) and max(3, round(width / spec.get('bristle_px', 2.5))))
    if spec.get('nib') is not None and width >= 3:
        # calligraphy: a flat nib held at a fixed angle -> thick-thin strokes depending on direction
        a = math.radians(spec['nib'])
        nx, ny = math.cos(a), math.sin(a)
        for j in range(max(3, int(width * ss))):
            off = (j / max(1, int(width * ss) - 1) - 0.5) * width
            qq = [((x + off * nx - x0) * ss, (y + off * ny - y0) * ss) for x, y in pts]
            if len(qq) > 1:
                d.line(qq, fill=255, width=max(1, int(ss * 1.5)))
            else:
                d.point(qq[0], fill=255)
    elif nb and width >= 4:
        # oil brush: parallel bristle tracks of varying load -> streaky texture, mean coverage ~ alpha
        nrm = _normals(pts)
        bw = max(1.0, width / nb * 1.6)
        for j in range(nb):
            off = (-r + bw / 2) + (width - bw) * j / max(1, nb - 1)
            v = rng.uniform(spec.get('bristle_lo', 0.62), spec.get('bristle_hi', 1.0))
            if spec.get('side_ramp'):     # wet edge: coverage ramps up across the stroke (from the -normal side)
                t = (j + 0.5) / nb
                v *= min(1.0, (1 - t if spec.get('side_flip') else t) / spec['side_ramp'])
            val = int(255 * v)
            qq = [((x + off * nx - x0) * ss, (y + off * ny - y0) * ss) for (x, y), (nx, ny) in zip(pts, nrm)]
            if len(qq) > 1:
                d.line(qq, fill=val, width=max(1, int(round(bw * ss))), joint='curve')
            for X, Y in (qq[0], qq[-1]):
                rr = bw * ss / 2
                d.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=val)
    else:
        rr = r * ss
        if len(q) > 1:
            d.line(q, fill=255, width=max(1, int(round(width * ss))), joint='curve')
        for X, Y in (q[0], q[-1]):
            if width <= 1.01 and ss == 1:
                d.point((X, Y), fill=255)
            else:
                d.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=255)
    if ss > 1:
        m = m.resize((w, h), Image.BILINEAR)
    if spec.get('soft'):
        m = m.filter(ImageFilter.GaussianBlur(max(0.6, spec['soft'] * width)))
    mm = np.asarray(m, np.float32) / 255.0
    if nb and width >= 4 and spec.get('bristle_renorm', True):
        mm = mm / 0.81  # bristle mask mean is ~0.81 of full; renormalise so mean coverage == alpha
    return np.clip(mm, 0, 1), x0, y0


def render(canvas, strokes, width, tool, opacity, palette, tools, offset=(0, 0), seed=0):
    """Composite strokes [(k, pts)] onto canvas (HxWx3 float, modified in place). offset: added to pts."""
    spec = tools[tool]
    a = effective_alpha(tool, opacity, tools)
    width = width * spec.get('width_scale', 1.0)          # measured ink thickness / nominal size
    rng = np.random.default_rng(seed)
    H, W = canvas.shape[:2]
    ox, oy = offset
    for k, pts in strokes:
        col = np.asarray(palette[k], np.float32)
        mm, x0, y0 = stroke_mask([(x + ox, y + oy) for x, y in pts], width, spec, rng)
        h, w = mm.shape
        cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
        if cx0 >= cx1 or cy0 >= cy1:
            continue
        sub = mm[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0, None] * a
        reg = canvas[cy0:cy1, cx0:cx1]
        reg += sub * (col - reg)
    return canvas
