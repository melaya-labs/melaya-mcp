"""App-agnostic painterly planner.

Input: a prepared job (target.png, meta.json with palette and layout) and a style preset. Output: a plan of
layers, each {tool, width, opacity, strokes:[[k, [[x,y],...]], ...]} in drawing-area pixel coordinates
(k = palette index). Every layer is simulated with the tool model right after it is planned, so the next layer
sees what the canvas really looks like (translucent tools, partial coverage) and the plan is predictable.

Layer types (preset "layers"[].type):
  ground   one serpentine stroke filling the drawing area with one colour (underpainting / toned ground)
  strokes  Hertzmann-style coarse-to-fine strokes: seeds where the canvas differs most from the target,
           traced along a direction field (contour | flow | angle | gradient), stopped when the canvas is
           already closer than the stroke colour would be (unless fixed_len)
  glaze    translucent cell glaze: per cell the palette colour whose blend lowers the Lab error most
  hatch    parallel line hatching per value level (pencil drawing, cross-hatching)
  dots     pointillist dots on a (hex) grid, colours by error diffusion (optical mixing) or one fixed colour
  flat     posterised flat colour regions filled with serpentine strokes inside each region (tip cascade)
  outline  contour lines along region boundaries (labels) or luminance level boundaries
  bokashi  woodblock colour gradient across a band (overlapping translucent horizontal passes)
  cells    partition (voronoi / grid / mondrian) -> colour per cell (nearest / shade / mondrian / dither) -> fill
           (regions / rects) [+ straight split lines]; see cells.py
  ornament decorative motifs in a mask: squares (mosaic), spirals, rings, dots, seal; see cells.py
Masks (layer "mask"): all, focus, primary, fine, detail, finest, paper, skin (face and hands as drawn: light warm
pixels touching the focus), band:<i>, dark:<L>, light:<L>; suffix +N grows a mask by N px, prefix ~ negates, & intersects.
"""
import json
import math
import os

import numpy as np
from scipy import ndimage as ndi

from . import cells as cl
from . import fastpaint as fp
from . import color as col
from . import simulate as sim
from .prepare import ellipse_mask, load_rgb


# ----------------------------------------------------------------------------------------------- context
class Ctx:
    def __init__(self, job, preset, tools, detail=1.0, seed=0):
        self.job = job
        with open(os.path.join(job, 'meta.json')) as f:
            self.meta = json.load(f)
        self.preset, self.tools, self.detail = preset, tools, detail
        self.T = load_rgb(os.path.join(job, 'target.png'))
        self.H, self.W = self.T.shape[:2]
        self.Tl = col.rgb2lab(self.T)
        self.pal = np.array(self.meta['palette'])
        self.pal_lab = col.rgb2lab(self.pal)
        self.pal_lin = col.srgb_to_linear(self.pal)
        self.full = load_rgb(os.path.join(job, 'canvas.png'))
        self.ox, self.oy = self.meta['layout']['draw_origin']
        self.rng = np.random.default_rng(seed)
        self.labels = None
        self._masks()

    @property
    def C(self):
        return self.full[self.oy:self.oy + self.H, self.ox:self.ox + self.W]

    def _masks(self):
        mp = self.preset.get('masks', {})
        H, W = self.H, self.W
        lum = self.Tl[..., 0]
        g = ndi.gaussian_filter(lum, 1.0)
        gm = np.hypot(ndi.sobel(g, 0), ndi.sobel(g, 1))
        self.struct = ndi.gaussian_filter(gm, 3)
        foc = self.meta.get('focus') or []
        self.FOCUS = ellipse_mask(H, W, foc) if foc else np.zeros((H, W), bool)
        self.PRIMARY = ellipse_mask(H, W, foc[:1]) if foc else np.zeros((H, W), bool)
        self.FINE = ndi.binary_dilation(self.FOCUS, iterations=6) if foc else self.FOCUS
        det = self.struct > np.percentile(self.struct, mp.get('detail_pct', 50))
        self.DETAIL = ndi.binary_dilation(det, iterations=2) | self.FINE
        fin = self.struct > np.percentile(self.struct, mp.get('finest_pct', 85))
        self.FINEST = fin | (ndi.binary_dilation(self.PRIMARY, iterations=4) if foc else fin)
        fp = os.path.join(self.job, 'fade.png')
        # paper: where prepare faded the image into bare paper (fade_edges), grown so outlines skip its border
        self.PAPER = (ndi.binary_dilation(load_rgb(fp)[..., 0] < 0.85, iterations=6) if os.path.isfile(fp)
                      else np.zeros((H, W), bool))

    def mask(self, spec):
        if spec in (None, 'all'):
            return None
        out = np.ones((self.H, self.W), bool)
        for part in str(spec).split('&'):
            part = part.strip()
            neg = part.startswith('~')
            name = part.lstrip('~')
            grow = 0
            if '+' in name:                                   # name+N: grow the mask by N px
                name, g = name.rsplit('+', 1)
                grow = int(g)
            if name == 'all':
                m = np.ones((self.H, self.W), bool)
            elif name.startswith('band:'):
                m = self.labels == int(name.split(':')[1]) if self.labels is not None else np.zeros((self.H, self.W), bool)
            elif name.startswith('dark:'):
                m = ndi.gaussian_filter(self.Tl[..., 0], 2) < float(name.split(':')[1])
            elif name.startswith('light:'):
                m = ndi.gaussian_filter(self.Tl[..., 0], 2) > float(name.split(':')[1])
            elif name == 'skin':
                m = self.skin()
            else:
                m = {'focus': self.FOCUS, 'primary': self.PRIMARY, 'fine': self.FINE, 'detail': self.DETAIL,
                     'finest': self.FINEST, 'paper': self.PAPER}[name]
            if grow:
                m = ndi.binary_dilation(m, iterations=grow)
            out &= ~m if neg else m
        return out

    def skin(self):
        """Face and hands as the picture draws them (not an ellipse): light, warm pixels near the focus,
        cleaned up and kept only where they touch the focus ellipses."""
        if getattr(self, '_skin', None) is not None:
            return self._skin
        lab = np.stack([ndi.gaussian_filter(self.Tl[..., c], 1.5) for c in range(3)], -1)
        warm = (lab[..., 0] > self.preset.get('skin', {}).get('min_L', 40)) & (lab[..., 1] > 1) & (lab[..., 2] > 10)
        near = ndi.binary_dilation(self.FOCUS, iterations=20) if self.FOCUS.any() else np.ones_like(warm)
        m = ndi.binary_opening(warm & near, iterations=2)
        m = ndi.binary_closing(m, iterations=4)
        m = ndi.binary_fill_holes(m)
        lab_c, n = ndi.label(m)
        keep = np.unique(lab_c[m & self.FOCUS]) if self.FOCUS.any() else np.arange(1, n + 1)
        self._skin = np.isin(lab_c, keep[keep > 0])
        return self._skin

    def color_index(self, spec):
        """'darkest' | 'lightest' | 'mean' | int | '#hex' / [r,g,b] -> palette index (nearest)."""
        L = self.pal_lab[:, 0]
        if spec == 'darkest':
            return int(L.argmin())
        if spec == 'lightest':
            return int(L.argmax())
        if spec == 'mean':
            return int(col.nearest(col.rgb2lab(self.T.mean((0, 1))), self.pal_lab))
        if isinstance(spec, int):
            return spec
        return int(col.nearest(col.rgb2lab(col.as_rgb(spec)), self.pal_lab))

    def alpha(self, L):
        """Mean coverage of one pass (alpha x opacity x coverage): what a stroke really lays, for colour choice."""
        t = L.get('tool', 'brush')
        return sim.effective_alpha(t, L.get('opacity', 1.0), self.tools) * self.tools[t].get('coverage', 1.0)

    def render(self, L, strokes, seed):
        sim.render(self.full, strokes, L['width'], L['tool'], L.get('opacity', 1.0), self.pal, self.tools,
                   offset=(self.ox, self.oy), seed=seed)


def lab1(rgb):
    return col.rgb2lab(np.asarray(rgb, float)[None, None])[0, 0]


# --------------------------------------------------------------------------------------------- ground
def layer_ground(ctx, L):
    if L.get('color', 'mean') == 'none':
        return []
    k = ctx.color_index(L.get('color', 'mean'))
    w = L.get('width', 64)
    r = w / 2
    sp = L.get('spacing', 0.75) * w
    n = max(1, int(np.ceil((ctx.H - w) / sp)) + 1)
    rows = np.linspace(r, max(r, ctx.H - r), n)          # evenly spaced, first and last row touch the edges
    pts = []
    for j, y in enumerate(rows):
        xs = (r, ctx.W - r) if j % 2 == 0 else (ctx.W - r, r)
        pts += [[xs[0], float(y)], [xs[1], float(y)]]
    return [(k, pts)]


# -------------------------------------------------------------------------------------------- strokes
def flow_field(ctx, sigma=6.0, swirl=0.0, swirl_seed=0, swirl_n=5):
    """Unit tangent field along image structure (structure tensor), blended with vortices where the image is flat."""
    lum = ndi.gaussian_filter(ctx.Tl[..., 0], 1.5)
    gx, gy = ndi.sobel(lum, 1), ndi.sobel(lum, 0)
    jxx, jyy, jxy = (ndi.gaussian_filter(a, sigma) for a in (gx * gx, gy * gy, gx * gy))
    theta = 0.5 * np.arctan2(2 * jxy, jxx - jyy)          # gradient orientation
    tx, ty = -np.sin(theta), np.cos(theta)                  # tangent (along contours)
    lam = np.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2)
    coh = lam / (jxx + jyy + 1e-6)
    if swirl > 0:
        rng = np.random.default_rng(swirl_seed)
        H, W = ctx.H, ctx.W
        yy, xx = np.mgrid[0:H, 0:W].astype(float)
        vx, vy = np.ones((H, W)) * 0.6, np.zeros((H, W))
        flat = ndi.gaussian_filter(1 - coh, 8)
        cand = np.argwhere(flat > np.percentile(flat, 60))
        for _ in range(swirl_n):
            cy, cx = cand[rng.integers(len(cand))] if len(cand) else (rng.uniform(0, H), rng.uniform(0, W))
            rad = rng.uniform(0.08, 0.16) * max(H, W)
            dx, dy = xx - cx, yy - cy
            d = np.hypot(dx, dy) + 1e-6
            s = rng.choice([-1, 1]) * np.exp(-(d / rad) ** 2) * 2.0
            vx += s * (-dy / d)
            vy += s * (dx / d)
        n = np.hypot(vx, vy) + 1e-9
        vx, vy = vx / n, vy / n
        # align sign of the tangent with the swirl, blend by coherence
        sgn = np.sign(tx * vx + ty * vy + 1e-9)
        tx, ty = tx * sgn, ty * sgn
        wgt = np.clip(coh * 1.6, 0, 1) * (1 - swirl) + (1 - swirl) * 0.2
        wgt = np.clip(wgt, 0, 1)
        tx, ty = wgt * tx + (1 - wgt) * vx, wgt * ty + (1 - wgt) * vy
        n = np.hypot(tx, ty) + 1e-9
        tx, ty = tx / n, ty / n
    return tx, ty


def layer_strokes(ctx, L, seed):
    rng = np.random.default_rng(seed)
    R = float(L['width'])
    thresh = L.get('thresh', 0) / ctx.detail
    max_len, min_len, fc = L.get('max_len', 10), L.get('min_len', 2), L.get('fc', 0.6)
    fine_len, fine_scale = L.get('fine_len', 3), L.get('fine_scale', 0.6)
    direction = L.get('direction', 'contour')
    fixed = L.get('fixed_len', False)
    cj = L.get('color_jitter', 0)
    a = ctx.alpha(L)
    only = ctx.mask(L.get('mask'))
    H, W = ctx.H, ctx.W
    sigma = max(0.5, R * L.get('blur', 0.5))
    Tref = np.stack([ndi.gaussian_filter(ctx.T[..., c], sigma) for c in range(3)], -1)
    Tl = col.rgb2lab(Tref)
    C = ctx.C.copy()
    Cl = col.rgb2lab(C)
    err = np.linalg.norm(Tl - Cl, axis=-1)
    if direction == 'flow':
        fx, fy = flow_field(ctx, L.get('flow_sigma', 6), L.get('swirl', 0), L.get('swirl_seed', 7), L.get('swirl_n', 5))
    else:
        lum = Tl[..., 0]
        gy, gx = ndi.sobel(lum, 0), ndi.sobel(lum, 1)
    step = R * L.get('step', 1.0)
    g = max(2, int(round(R * L.get('grid', 1.0) / max(0.2, ctx.detail) ** 0.5)))
    jit = L.get('seed_jitter', 0)
    use_fine = ctx.FINE.any() and L.get('use_fine', True)
    strokes = []
    for y0 in range(0, H, g):
        for x0 in range(0, W, g):
            if only is not None and not only[y0:y0 + g, x0:x0 + g].any():
                continue
            blk = err[y0:y0 + g, x0:x0 + g]
            infine = use_fine and ctx.FINE[y0:y0 + g, x0:x0 + g].any()
            th = thresh * (fine_scale if infine else 1.0)
            if blk.mean() < th:
                continue
            iy, ix = np.unravel_index(blk.argmax(), blk.shape)
            x, y = float(x0 + ix), float(y0 + iy)
            if jit:
                x = float(np.clip(x + rng.uniform(-jit, jit) * g, 0, W - 1))
                y = float(np.clip(y + rng.uniform(-jit, jit) * g, 0, H - 1))
            yi, xi = int(y), int(x)
            if only is not None and not only[yi, xi]:
                continue
            # colour: the palette colour whose blend (tool alpha) over the current canvas lands closest
            if a >= 0.999:
                d = np.linalg.norm(ctx.pal_lab - Tl[yi, xi], axis=1)
            else:
                d = np.linalg.norm(col.rgb2lab(a * ctx.pal + (1 - a) * C[yi, xi]) - Tl[yi, xi], axis=1)
            if cj > 0:
                cand = np.where(d <= d.min() + cj)[0]
                k = int(rng.choice(cand))
            else:
                k = int(d.argmin())
            kl = lab1(a * ctx.pal[k] + (1 - a) * C[yi, xi]) if a < 0.999 else ctx.pal_lab[k]
            pts = [(x, y)]
            lastdx = lastdy = 0.0
            if direction == 'angle':
                ang = math.radians(L.get('angle', 0) + rng.uniform(-1, 1) * L.get('angle_jitter', 0))
                adx, ady = math.cos(ang), math.sin(ang)
            ml = fine_len if (use_fine and ctx.FINE[yi, xi]) else max_len
            if L.get('len_jitter'):
                ml = max(1, int(round(ml * rng.uniform(1 - L['len_jitter'], 1 + L['len_jitter']))))
            for i in range(ml):
                xi, yi = int(round(x)), int(round(y))
                if not (0 <= xi < W and 0 <= yi < H):
                    break
                if not fixed and i >= min_len and np.linalg.norm(Tl[yi, xi] - Cl[yi, xi]) < np.linalg.norm(Tl[yi, xi] - kl):
                    break
                if direction == 'flow':
                    dx, dy = fx[yi, xi], fy[yi, xi]
                elif direction == 'angle':
                    dx, dy = adx, ady
                else:
                    gxv, gyv = gx[yi, xi], gy[yi, xi]
                    if math.hypot(gxv, gyv) < 1e-3:
                        if fixed:
                            dx, dy = (lastdx, lastdy) if (lastdx or lastdy) else (1.0, 0.0)
                        else:
                            break
                    elif direction == 'gradient':
                        dx, dy = gxv, gyv
                    else:
                        dx, dy = -gyv, gxv
                if lastdx * dx + lastdy * dy < 0:
                    dx, dy = -dx, -dy
                dx, dy = fc * dx + (1 - fc) * lastdx, fc * dy + (1 - fc) * lastdy
                n = math.hypot(dx, dy) or 1
                dx, dy = dx / n, dy / n
                x, y = x + step * dx, y + step * dy
                if not (0 <= x < W and 0 <= y < H):
                    break
                if only is not None and L.get('clip_mask', False) and not only[int(y), int(x)]:
                    break
                pts.append((x, y))
                lastdx, lastdy = dx, dy
            strokes.append((k, pts))
    return order_by_colour(ctx, strokes, L.get('color_order', 'index'))


def order_by_colour(ctx, strokes, how):
    if how == 'dark_first':
        key = lambda s: (ctx.pal_lab[s[0], 0], s[0])
    elif how == 'light_first':
        key = lambda s: (-ctx.pal_lab[s[0], 0], s[0])
    else:
        key = lambda s: s[0]
    return sorted(strokes, key=key)


# ---------------------------------------------------------------------------------------------- glaze
def layer_glaze(ctx, L, seed):
    a, cell = ctx.alpha(L), int(L.get('cell', 8))
    H, W = ctx.H, ctx.W
    h, w = H // cell, W // cell
    C, T = ctx.C, ctx.T
    Cc = C[:h * cell, :w * cell].reshape(h, cell, w, cell, 3).mean((1, 3))
    Tc = T[:h * cell, :w * cell].reshape(h, cell, w, cell, 3).mean((1, 3))
    Tl = col.rgb2lab(Tc)
    base = np.linalg.norm(col.rgb2lab(Cc) - Tl, axis=-1)
    best = np.full((h, w), -1)
    gain = np.zeros((h, w))
    for k, c in enumerate(ctx.pal):
        gk = base - np.linalg.norm(col.rgb2lab(a * c + (1 - a) * Cc) - Tl, axis=-1)
        u = gk > gain
        best[u] = k
        gain[u] = gk[u]
    sel = gain > L.get('gain', 3.0) / ctx.detail
    prot = L.get('protect', 'primary')
    if prot and prot != 'none':
        pm = ctx.mask(prot)
        if pm is not None and pm.any():
            sel &= ~ndi.binary_dilation(pm, iterations=2)[::cell, ::cell][:h, :w]
    only = ctx.mask(L.get('mask'))
    if only is not None:
        sel &= only[::cell, ::cell][:h, :w]
    gl = []
    for k in range(len(ctx.pal)):
        m = sel & (best == k)
        for y in range(h):
            x = 0
            while x < w:
                if not m[y, x]:
                    x += 1
                    continue
                x0 = x
                while x < w and m[y, x]:
                    x += 1
                gl.append((k, [((x0 + 0.5) * cell, (y + 0.5) * cell), ((x - 0.5) * cell, (y + 0.5) * cell)]))
    L['width'] = cell
    return sorted(gl, key=lambda s: s[0])


# -------------------------------------------------------------------------------------------- bokashi
def layer_bokashi(ctx, L, seed):
    """Woodblock bokashi: a colour gradient across a band (e.g. the top of the sky), built from overlapping
    passes of horizontal translucent strokes, each pass covering a shorter part of the band."""
    k = ctx.color_index(L.get('color', '#1f3a5f'))
    w = L.get('width', 16)
    y0, y1 = L.get('y0', 0.0) * ctx.H, L.get('y1', 0.18) * ctx.H
    n = L.get('passes', 3)
    out = []
    for i in range(n):
        yb = y0 + (y1 - y0) * (1 - i / n)
        y = y0 + w / 2
        while y <= yb:
            out.append((k, [[w / 2, y], [ctx.W - w / 2, y]]))
            y += w * L.get('spacing', 0.45)
    return out


# ---------------------------------------------------------------------------------------------- hatch
def hatch_lines(region, angle, spacing, min_run, rng, jitter=0.0):
    H, W = region.shape
    th = math.radians(angle)
    ux, uy = math.cos(th), math.sin(th)
    nx, ny = -uy, ux
    corners = np.array([[0, 0], [W, 0], [0, H], [W, H]], float)
    dn = corners @ [nx, ny]
    du = corners @ [ux, uy]
    t = np.arange(du.min(), du.max() + 1, 1.0)
    out = []
    d = dn.min() + rng.uniform(0, spacing)
    while d <= dn.max():
        px, py = d * nx + t * ux, d * ny + t * uy
        ok = (px >= 0) & (px < W - 0.5) & (py >= 0) & (py < H - 0.5)
        xi, yi = np.clip(np.round(px).astype(int), 0, W - 1), np.clip(np.round(py).astype(int), 0, H - 1)
        on = ok & region[yi, xi]
        if on.any():
            e = np.diff(np.concatenate([[0], on.astype(int), [0]]))
            for s, f in zip(np.where(e == 1)[0], np.where(e == -1)[0]):
                if f - s >= min_run:
                    j = lambda: rng.uniform(-jitter, jitter)
                    out.append([(px[s] + j(), py[s] + j()), (px[f - 1] + j(), py[f - 1] + j())])
        d += spacing
    return out


def layer_hatch(ctx, L, seed):
    rng = np.random.default_rng(seed)
    k = ctx.color_index(L.get('color', 'darkest'))
    Ls = ndi.gaussian_filter(ctx.Tl[..., 0], L.get('blur', 1.5))
    only = ctx.mask(L.get('mask'))
    strokes = []
    for lev in L['levels']:
        reg = Ls < lev['L'] * (1 + 0.15 * (ctx.detail - 1))
        if only is not None:
            reg &= only
        for seg in hatch_lines(reg, lev.get('angle', 45), lev.get('spacing', 5), L.get('min_run', 4), rng, L.get('jitter', 0.5)):
            strokes.append((k, [list(p) for p in seg]))
    return strokes


# ----------------------------------------------------------------------------------------------- dots
def layer_dots(ctx, L, seed):
    rng = np.random.default_rng(seed)
    sp = float(L.get('spacing', 6)) / max(0.2, ctx.detail) ** 0.5
    H, W = ctx.H, ctx.W
    only = ctx.mask(L.get('mask'))
    Tb = np.stack([ndi.gaussian_filter(ctx.T[..., c], sp / 2) for c in range(3)], -1)
    err_thr = L.get('thresh', 0) / ctx.detail
    if err_thr:
        Cb = np.stack([ndi.gaussian_filter(ctx.C[..., c], sp / 2) for c in range(3)], -1)
        errmap = np.linalg.norm(col.rgb2lab(Tb) - col.rgb2lab(Cb), axis=-1)
    hexg = L.get('grid', 'hex') == 'hex'
    rows = np.arange(sp / 2, H, sp * (0.866 if hexg else 1))
    cols = np.arange(sp / 2, W, sp)
    fixed = L.get('color', 'fs')
    a = ctx.alpha(L)
    E = np.zeros((len(rows), len(cols) + 2, 3))
    pts_out = []
    comp = L.get('complement', 0.0)
    for r_i, y in enumerate(rows):
        off = (sp / 2 if (hexg and r_i % 2) else 0)
        for c_i, x0 in enumerate(cols):
            x = x0 + off
            if x >= W:
                continue
            jx, jy = rng.uniform(-1, 1, 2) * L.get('jitter', 0.3) * sp
            px, py = float(np.clip(x + jx, 0, W - 1)), float(np.clip(y + jy, 0, H - 1))
            yi, xi = int(py), int(px)
            if only is not None and not only[yi, xi]:
                continue
            if err_thr and errmap[yi, xi] < err_thr:
                continue
            if fixed != 'fs':
                k = ctx.color_index(fixed)
            else:
                want = col.srgb_to_linear(Tb[yi, xi]) + E[r_i, c_i + 1]
                cur = col.srgb_to_linear(ctx.C[yi, xi])
                got_all = a * ctx.pal_lin + (1 - a) * cur
                k = int(np.linalg.norm(got_all - want, axis=1).argmin())
                if comp and rng.random() < comp:
                    tl = col.rgb2lab(Tb[yi, xi])
                    cl = np.array([tl[0], -tl[1], -tl[2]])
                    k = int(np.linalg.norm(ctx.pal_lab - cl, axis=1).argmin())
                e = want - got_all[k]
                E[r_i, c_i + 2] += e * 7 / 16
                if r_i + 1 < len(rows):
                    E[r_i + 1, c_i] += e * 3 / 16
                    E[r_i + 1, c_i + 1] += e * 5 / 16
                    E[r_i + 1, c_i + 2] += e * 1 / 16
            pts_out.append((k, [[px, py], [px + 1, py]]))
    return sorted(pts_out, key=lambda s: s[0])


# ----------------------------------------------------------------------------------------------- flat
def mode_filter(lbl, K, r):
    cnt = np.stack([ndi.uniform_filter((lbl == k).astype(float), 2 * r + 1, mode='nearest') for k in range(K)])
    return cnt.argmax(0)


def despeckle(lbl, K, minsize):
    lbl = lbl.copy()
    for _ in range(3):
        changed = 0
        for k in range(K):
            lab, n = ndi.label(lbl == k)
            if n == 0:
                continue
            sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
            small = np.isin(lab, np.where(sizes < minsize)[0] + 1)
            if small.any():
                l2 = lbl.copy()
                l2[small] = -1
                idx = ndi.distance_transform_edt(l2 == -1, return_distances=False, return_indices=True)
                lbl[small] = l2[tuple(idx)][small]
                changed += small.sum()
        if not changed:
            break
    return lbl


def label_map(ctx, L):
    s = int(L.get('scale', 2))
    Tb = np.stack([ndi.gaussian_filter(ctx.T[..., c], L.get('blur', 1.5)) for c in range(3)], -1)
    small = Tb[s // 2::s, s // 2::s]
    K = len(ctx.pal)
    if L.get('labels', 'nearest') == 'bands':
        nb = ctx.meta['palette_info'].get('band_count') or K
        lum = col.rgb2lab(small)[..., 0]
        edges = L.get('band_edges')
        q = np.quantile(lum, edges if edges else np.linspace(0, 1, nb + 1)[1:-1])
        lbl = np.digitize(lum, q)
    else:
        use = L.get('use_colors')
        pl = ctx.pal_lab if use is None else ctx.pal_lab[use]
        lbl = col.nearest(col.rgb2lab(small), pl)
        if use is not None:
            lbl = np.asarray(use)[lbl]
    if L.get('smooth', 2):
        lbl = mode_filter(lbl, K, L.get('smooth', 2))
    lbl = despeckle(lbl, K, L.get('minsize', 20))
    return lbl, s


def strokes_rows(Eok, need, rows):
    """Serpentine strokes over row runs: each run of `need` inside `Eok`, chained to the nearest run on the next
    row when the connecting segment stays inside Eok."""
    w = Eok.shape[1]
    runs = {}
    for y in rows:
        out, x = [], 0
        while x < w:
            if not Eok[y, x]:
                x += 1
                continue
            x0 = x
            while x < w and Eok[y, x]:
                x += 1
            idx = np.where(need[y, x0:x])[0]
            if len(idx):
                out.append([x0 + idx[0], x0 + idx[-1], False])
        runs[y] = out
    strokes = []
    for k, y in enumerate(rows):
        for r in runs[y]:
            if r[2]:
                continue
            r[2] = True
            pts = [(r[0], y), (r[1], y)]
            j = k
            while j + 1 < len(rows):
                y2 = rows[j + 1]
                xe = pts[-1][0]
                best = None
                for q in runs[y2]:
                    if q[2]:
                        continue
                    for s, e in ((q[0], q[1]), (q[1], q[0])):
                        a, b = min(xe, s), max(xe, s)
                        if Eok[pts[-1][1]:y2 + 1, a:b + 1].all():
                            d = abs(xe - s)
                            if best is None or d < best[0]:
                                best = (d, q, s, e)
                if not best:
                    break
                _, q, s, e = best
                q[2] = True
                j += 1
                pts += [(s, y2)] if s == e else [(s, y2), (e, y2)]
            strokes.append(pts)
    return strokes


def cover(strokes, t, shape):
    m = np.zeros(shape, bool)
    for pts in strokes:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] or pts):
            n = max(abs(x1 - x0), abs(y1 - y0), 1)
            for u in range(n + 1):
                m[round(y0 + (y1 - y0) * u / n), round(x0 + (x1 - x0) * u / n)] = True
    if t > 1:
        r = (t - 1) / 2
        yy, xx = np.mgrid[-int(r):int(r) + 1, -int(r):int(r) + 1]
        m = ndi.binary_dilation(m, (xx ** 2 + yy ** 2) <= (r * r + 0.25))
    return m


def fill_region(R, i, tips):
    """Strokes (tip, [pts]) covering cells R==i without touching cells of earlier ranks (R<i)."""
    h, w = R.shape
    ok, todo, out = R >= i, R == i, []
    for t in tips:
        if not todo.any():
            break
        E = ndi.binary_erosion(ok, np.ones((t, t), bool), border_value=0) if t > 1 else ok
        need = E & (ndi.binary_dilation(todo, np.ones((t, t), bool)) if t > 1 else todo)
        if t > 1:
            need &= ndi.uniform_filter(todo.astype(float), t, mode='constant') >= 0.25
        if not need.any():
            continue
        best = None
        for tr in (False, True):
            Eo, Ne = (E.T, need.T) if tr else (E, need)
            step = max(1, t - 1) if t > 1 else 1
            for off in sorted({0, step // 2}):
                S = strokes_rows(Eo, Ne, list(range(off, Eo.shape[0], step)))
                if tr:
                    S = [[(y, x) for x, y in s] for s in S]
                c = sum(max(2, len(s)) for s in S)
                if best is None or c < best[0]:
                    best = (c, S)
        todo &= ~cover(best[1], t, (h, w))
        out.append((t, best[1]))
    if todo.any():
        out.append((1, strokes_rows(ok, todo, list(range(h)))))
    return out


def layer_flat(ctx, L, seed):
    """Posterised flat colour regions. Returns sub-layers (one per colour and tip) for plan()."""
    lbl, s = label_map(ctx, L)
    full = np.kron(lbl, np.ones((s, s), int))
    pad = np.pad(full, ((0, max(0, ctx.H - full.shape[0])), (0, max(0, ctx.W - full.shape[1]))), mode='edge')
    ctx.labels = pad[:ctx.H, :ctx.W]
    return choose_render(ctx, L, lambda: paint_label_grid(ctx, L, lbl, s), ctx.labels.copy())


def quick_cost(ctx, sublayers):
    """Seconds for a list of (layer, strokes) with the default timing profile: picks, tool switches, strokes,
    ink and fill clicks (the same terms as the emitter's estimate)."""
    import math
    from . import emit_paint as ep
    ui = ep.load_ui()
    tm = ui['timing_profiles'][ui.get('timing_profile', 'recorded')]
    t, tool = 0.0, None
    for L, S in sublayers:
        if L['tool'] != tool:
            t += 0.5
            tool = L['tool']
        last = None
        spec = ctx.tools.get(L['tool'], {})
        step = L.get('stepPx') or spec.get('stepPx', 16)
        for k, pts in S:
            if k != last:
                t += tm['per_pick_s']
                last = k
            if spec.get('flood'):
                t += tm.get('per_fill_s', 0.1)
                continue
            ln = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
            t += tm['per_short_s'] if ln < 4 else tm['per_long_s']
            t += ln / 1000 * (tm['per_kpx16_s'] if step > 4 else tm.get('per_kpx4_s', 0.0))
    return t


def choose_render(ctx, L, stroke_fn, cmap):
    """render: strokes | fill | auto (plan both, keep the cheaper by the timing model)."""
    mode = L.get('render', 'strokes')
    if mode == 'strokes':
        return stroke_fn()
    f = fill_layers(ctx, L, cmap)
    if mode == 'fill':
        return f
    s_ = stroke_fn()
    cf, cs = quick_cost(ctx, f), quick_cost(ctx, s_)
    ctx.render_choice = {'fill_s': round(cf), 'strokes_s': round(cs), 'chosen': 'fill' if cf <= cs else 'strokes'}
    return f if cf <= cs else s_


def fill_layers(ctx, L, cmap):
    """Outline + bucket-fill rendering of a full-resolution palette-index map (see fastpaint.fill_render)."""
    r = fp.fill_render(cmap, L.get('fill_min_area', 12), L.get('fill_conn', ctx.tools.get('fill', {}).get('fill_conn', 'both')))
    name = L.get('name', L.get('type', 'flat'))
    out = []
    if r['outline']:
        out.append(({'tool': 'pencil', 'width': 1, 'opacity': 1.0, 'name': name + '-rings', 'no_merge': True},
                    sorted(r['outline'], key=lambda s: s[0])))
    if r['fills']:
        out.append(({'tool': 'fill', 'width': 1, 'opacity': 1.0, 'name': name + '-fills', 'no_merge': True, 'no_optimise': True},
                    sorted(r['fills'], key=lambda s: s[0])))
    fb = r['fallback_mask']
    if fb.any():                                    # tiny or leaking regions: 1 px pencil rows, exact
        runs = []
        ys, xs = np.nonzero(fb)
        for y in np.unique(ys):
            row = np.where(fb[y])[0]
            for seg in np.split(row, np.where(np.diff(row) > 1)[0] + 1):
                ks = cmap[y, seg]
                for part in np.split(np.arange(len(seg)), np.where(np.diff(ks) != 0)[0] + 1):
                    a, b = seg[part[0]], seg[part[-1]]
                    runs.append((int(ks[part[0]]), [[float(a), float(y)], [float(b), float(y)]]))
        out.append(({'tool': 'pencil', 'width': 1, 'opacity': 1.0, 'name': name + '-small', 'no_merge': True},
                    sorted(runs, key=lambda s: s[0])))
    ctx.fill_stats = r['stats']
    return out


def paint_labels(ctx, L, cmap):
    """Paint a full-resolution palette-index map with region-filling serpentines (used by `cells`)."""
    s = int(L.get('scale', 2))
    return paint_label_grid(ctx, L, cmap[s // 2::s, s // 2::s], s)


def paint_label_grid(ctx, L, lbl, s):
    K = len(ctx.pal)
    area = np.bincount(lbl.ravel(), minlength=K)
    order = [int(k) for k in np.argsort(-area) if area[k] > 0]
    rank = np.full(K, len(order) + 1)
    rank[order] = np.arange(len(order))
    R = rank[lbl]
    tips = L.get('tips', [15, 7, 3, 1])
    ground = L.get('first_is_ground', True)
    subs = {}
    for i, k in enumerate(order):
        if i == 0 and ground:
            continue  # biggest region is laid by the ground serpentine
        for t, S in fill_region(R, i, tips):
            for st in S:
                pts = [[(x + 0.5) * s, (y + 0.5) * s] for x, y in st]
                subs.setdefault(t, []).append((k, pts))
    out = []
    name = L.get('name', L.get('type', 'flat'))
    if ground:
        g = layer_ground(ctx, {'color': order[0], 'width': L.get('ground_width', 64)})
        out.append(({'tool': L.get('tool', 'brush'), 'width': L.get('ground_width', 64), 'name': name + '-base'}, g))
    # paint per colour rank (keeps the occlusion order), coarse tips first inside each colour
    by_k = {}
    for t, S in subs.items():
        for k, pts in S:
            by_k.setdefault(k, {}).setdefault(t, []).append((k, pts))
    for k in order[1:] if ground else order:
        for t in sorted(by_k.get(k, {}), reverse=True):
            out.append(({'tool': L.get('tool', 'brush'), 'width': max(1, t * s), 'name': '%s-c%d-t%d' % (name, k, t)}, by_k[k][t]))
    return out


# -------------------------------------------------------------------------------------------- outline
NB8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def trace_chains(B):
    H, W = B.shape
    nb = ndi.convolve(B.astype(int), np.ones((3, 3), int), mode='constant') - B
    vis = ~B.copy()
    ends = [tuple(p) for p in np.argwhere(B & (nb == 1))]
    rest = [tuple(p) for p in np.argwhere(B)]
    chains = []
    for y, x in ends + rest:
        if vis[y, x]:
            continue
        ch = [(x, y)]
        vis[y, x] = True
        pdx = pdy = 0
        while True:
            best, bs = None, -9
            for dy, dx in NB8:
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and not vis[ny, nx]:
                    s = dx * pdx + dy * pdy - 0.3 * (abs(dx) + abs(dy) - 1)
                    if s > bs:
                        best, bs = (ny, nx, dy, dx), s
            if best is None:
                break
            y, x, pdy, pdx = best
            vis[y, x] = True
            ch.append((x, y))
        chains.append(ch)
    return chains


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    p = np.asarray(pts, float)
    keep = np.zeros(len(p), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(p) - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        d = p[b] - p[a]
        n = math.hypot(*d) or 1
        dist = np.abs((p[a + 1:b, 0] - p[a, 0]) * d[1] - (p[a + 1:b, 1] - p[a, 1]) * d[0]) / n
        i = int(dist.argmax())
        if dist[i] > eps:
            keep[a + 1 + i] = True
            stack += [(a, a + 1 + i), (a + 1 + i, b)]
    return [tuple(q) for q in p[keep]]


def chaikin(pts):
    """One Chaikin corner-cutting pass (keeps the end points): staircase chains become flowing lines."""
    if len(pts) < 3:
        return pts
    p = np.asarray(pts, float)
    q = np.empty((2 * (len(p) - 1), 2))
    q[0::2] = 0.75 * p[:-1] + 0.25 * p[1:]
    q[1::2] = 0.25 * p[:-1] + 0.75 * p[1:]
    return [tuple(p[0])] + [tuple(v) for v in q] + [tuple(p[-1])]


def layer_outline(ctx, L, seed):
    src = L.get('source', 'labels')
    if src == 'labels' and ctx.labels is not None:
        lbl = ctx.labels
    else:
        n = int(str(src).split(':')[1]) if ':' in str(src) else 4
        lum = ndi.gaussian_filter(ctx.Tl[..., 0], L.get('blur', 2.0))
        q = np.quantile(lum, np.linspace(0, 1, n + 1)[1:-1])
        lbl = np.digitize(lum, q)
        lbl = mode_filter(lbl, n, 2)
    B = np.zeros(lbl.shape, bool)
    B[:, :-1] |= lbl[:, :-1] != lbl[:, 1:]
    B[:-1, :] |= lbl[:-1, :] != lbl[1:, :]
    only = ctx.mask(L.get('mask'))
    if only is not None:
        B &= only
    if L.get('edge_pct'):
        B &= ctx.struct > np.percentile(ctx.struct, L['edge_pct'])
    k = ctx.color_index(L.get('color', 'darkest'))
    out = []
    minl = L.get('min_len', 8)
    for ch in trace_chains(B):
        if len(ch) < minl:
            continue
        pts = rdp(ch, L.get('simplify', 0.9))
        for _ in range(int(L.get('smooth', 0))):
            pts = chaikin(pts)
        out.append((k, [[float(x), float(y)] for x, y in pts]))
    return out


# ---------------------------------------------------------------------------------------------- frame
def layer_frame(ctx, F):
    """Picture frame in the canvas margins (drawing coordinates, may be negative): walnut bands, gold fillet,
    dark inner line. Kept 5 px clear of the canvas edges and their resize handles."""
    fi = ctx.meta['palette_info']['frame']
    Wc, Hc = ctx.meta['layout']['canvas']
    ox, oy, W, H = ctx.ox, ctx.oy, ctx.W, ctx.H
    ins = F.get('inset', 14)
    Lx, Rx, Ty, By = 46 - ox, Wc - 5 - ox, 5 - oy, Hc - 5 - oy
    il, ir, it, ib = ins, W - ins, ins, H - ins
    bw = F.get('band_width', 11)
    band = []
    for x in range(Lx + 5, il, 10):
        band.append((fi['walnut'], [[x, Ty], [x, By]]))
    for x in range(ir + 5, Rx + 1, 10):
        band.append((fi['walnut'], [[x, Ty], [x, By]]))
    for y in range(Ty + 3, it, 8):
        band.append((fi['walnut'], [[Lx, y], [Rx, y]]))
    for y in range(ib + 5, By + 1, 8):
        band.append((fi['walnut'], [[Lx, y], [Rx, y]]))
    gold = [(fi['gold'], [[il, it], [ir, it], [ir, ib], [il, ib], [il, it]])]
    dark = [(fi['dark'], [[il + 3, it + 3], [ir - 3, it + 3], [ir - 3, ib - 3], [il + 3, ib - 3], [il + 3, it + 3]])]
    return [({'tool': 'pencil', 'width': bw, 'name': 'frame-walnut', 'speed': 6000}, band),
            ({'tool': 'pencil', 'width': 3, 'name': 'frame-gold', 'speed': 4000}, gold),
            ({'tool': 'pencil', 'width': 2, 'name': 'frame-dark', 'speed': 4000}, dark)]


# ----------------------------------------------------------------------------------------------- plan
def score_view(ctx):
    from .score import scores
    return scores(ctx.C, ctx.T if ctx.preset.get('score_vs', 'target') == 'target' else
                  load_rgb(os.path.join(ctx.job, 'target_raw.png')), ctx.meta.get('face_box'), inset=16)


def plan(job, preset, tools, detail=1.0, seed=0, frame=None, log=print):
    log = log or (lambda *x: None)
    ctx = Ctx(job, preset, tools, detail, seed)
    layers = []

    Wc, Hc = ctx.meta['layout']['canvas']
    strip_x1 = ctx.meta['layout']['strip']['x1']

    def inside(S, w, name):
        """Keep every painting stroke's whole footprint 5 px inside the canvas (and clear of the palette strip),
        so nothing spills above or beside the frame; frame strokes keep the plain 5 px edge rule."""
        if name.startswith('frame'):
            return S
        h = w / 2.0
        x_lo = max(5 + h, strip_x1 + 1 + h + 0.5) - ctx.ox
        x_hi, y_lo, y_hi = Wc - 5 - h - ctx.ox, 5 + h - ctx.oy, Hc - 5 - h - ctx.oy
        if x_hi <= x_lo or y_hi <= y_lo:
            return S
        return [(k, [(min(max(x, x_lo), x_hi), min(max(y, y_lo), y_hi)) for x, y in pts]) for k, pts in S]

    merge_dE = preset.get('colour_merge_dE', 2.0)

    def add(L, S, name=None):
        L = dict(L)
        L.setdefault('opacity', 1.0)
        S = inside(S, L['width'], name or L.get('name') or '')
        if preset.get('optimise', True) and not L.get('no_optimise') and not (name or '').startswith('frame'):
            spec = tools.get(L['tool'], {})
            S, _ = fp.optimise_layer(S, can_reverse=not spec.get('side_ramp') and not spec.get('nib'),
                                     merge_dE=0.0 if L.get('no_merge') else merge_dE, pal_lab=ctx.pal_lab)
        ctx.render(L, S, seed + len(layers))
        sc = score_view(ctx)
        entry = {'name': name or L.get('name') or L.get('type'), 'tool': L['tool'], 'width': L['width'],
                 'opacity': L.get('opacity', 1.0),
                 'strokes': [[int(k), [[round(float(x), 1), round(float(y), 1)] for x, y in pts]] for k, pts in S]}
        for key in ('speed', 'stepPx'):
            if key in L:
                entry[key] = L[key]
        layers.append(entry)
        log('%-20s %-11s w=%-3s n=%5d colours=%2d -> dE %.2f focus %s' % (
            entry['name'][:20], L['tool'], L['width'], len(S), len({s[0] for s in S}), sc['all'],
            '%.2f' % sc['face'] if sc.get('face') is not None else '-'))

    for i, L in enumerate(preset['layers']):
        L = dict(L)
        t = L.get('type', 'strokes')
        L.setdefault('tool', {'glaze': 'watercolour', 'bokashi': 'watercolour', 'hatch': 'pencil', 'outline': 'pencil'}.get(t, 'brush'))
        sd = seed * 1000 + i
        if t == 'ground':
            S = layer_ground(ctx, L)
            if S:
                L.setdefault('width', 64)
                add(L, S, L.get('name', 'ground'))
        elif t == 'strokes':
            add(L, layer_strokes(ctx, L, sd), L.get('name', 'strokes-w%d' % L['width']))
        elif t == 'glaze':
            S = layer_glaze(ctx, L, sd)
            add(L, S, L.get('name', 'glaze'))
        elif t == 'bokashi':
            L.setdefault('tool', 'watercolour')
            L.setdefault('width', 16)
            add(L, layer_bokashi(ctx, L, sd), L.get('name', 'bokashi'))
        elif t == 'hatch':
            L.setdefault('width', 1)
            add(L, layer_hatch(ctx, L, sd), L.get('name', 'hatch'))
        elif t == 'dots':
            L.setdefault('width', 6)
            if ctx.detail < 1:                       # fewer dots -> bigger dots, same coverage
                L['width'] = int(round(L['width'] / ctx.detail ** 0.5))
            add(L, layer_dots(ctx, L, sd), L.get('name', 'dots-w%d' % L['width']))
        elif t == 'flat':
            for sub, S in layer_flat(ctx, L, sd):
                full = dict(L)
                full.update(sub)
                add(full, S, sub['name'])
        elif t == 'outline':
            L.setdefault('width', 2)
            add(L, layer_outline(ctx, L, sd), L.get('name', 'outline'))
        elif t == 'cells':
            for sub, S in cl.layer_cells(ctx, L, sd, paint_labels):
                full = dict(L)
                full.update(sub)
                if S:
                    add(full, S, sub['name'])
        elif t == 'ornament':
            L.setdefault('width', 2)
            S = cl.layer_ornament(ctx, L, sd)
            if S:
                add(L, S, L.get('name', 'ornament-' + L.get('motif', 'squares')))
        else:
            raise ValueError('unknown layer type %r' % t)
    use_frame = ctx.meta.get('frame') if frame is None else frame
    if use_frame:
        for L, S in layer_frame(ctx, preset.get('frame', {})):
            add(L, S, L['name'])
    sc = score_view(ctx)
    out = {'version': 1, 'preset': preset.get('name'), 'job': os.path.abspath(job), 'W': ctx.W, 'H': ctx.H,
           'palette': ctx.meta['palette'], 'layers': layers, 'sim_score': sc, 'sim_vs_target': sc,
           'stats': {'strokes': sum(len(L['strokes']) for L in layers),
                     'colour_groups': sum(len({s[0] for s in L['strokes']}) for L in layers),
                     'layers': len(layers)}}
    return out, ctx.full
