"""Cell-based layers: partition the picture into cells, colour each cell, fill it with paintable strokes.

layer "cells" (preset):
  partition  voronoi | grid | mondrian
    voronoi:  n (cells), edge_bias (share of seeds placed on strong structure), density_gamma (>0: the other seeds
              follow local detail too, so the face gets small cells), focus_density (seed density multiplier on
              the focus), split (edge_line: straight cut where the value changes most, angular edge-aligned shards
              for cubism; value: split by the cell's own value threshold, pieces follow the contour, for
              stained glass), split_depth, split_min_dL (cells with less contrast stay whole)
    grid:     cols, rows (rows default: square blocks)
    mondrian: n (cells), min_frac (smallest split position as a share of the side), min_px (smallest cell
              side), detail_power (0: biggest cells split first; up to 1: cells with more value variation first,
              so rectangles get small on the face); every split runs along the cell's strongest straight edge
  color      nearest | shade | mondrian | dither   (+ match: {paint: proxy colour} chooses each paint where the
             picture looks like its proxy; colors: restrict to these palette colours; jitter: dE
             window for a random pick among near colours, per cell; value_weight: weight of L in the colour match,
             >1 keeps the picture's light and dark structure readable with a stylised palette)
    nearest:  palette colour nearest the cell's mean Lab
    shade:    bands (n), shade_step (L per band), shade_dir (degrees, 'edge' = across the cell's dominant edge,
              'random'): each cell graded light to dark in parallel bands
    mondrian: primary_share (share of cells, the most saturated, coloured with the nearest of the palette's
              saturated colours by hue), black_share (darkest cells -> darkest colour), the rest white or light
              grey by value
    dither:   ordered 4x4 Bayer dithering on the cell grid, dither (L units of spread)
  fill       regions (posterised-region serpentines, tip cascade: any cell shape) | rects (horizontal lines inside
             each rectangle, crisp corners: grid and mondrian), rect_width (line width for rects), rect_overlap
             (px each line runs past its rectangle, default 1: no 1-px seams live)
  lines      (mondrian) {color, width, thick_width, thick_levels}: the split lines drawn straight, full length
After the layer, ctx.labels holds the CELL ids, so an `outline` layer with source labels draws every cell boundary
(stained-glass leading, cubist facet edges).
"""
import math

import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

from . import color as col

BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0 - 0.5


# ------------------------------------------------------------------------------------------ partitions
def part_voronoi(ctx, L, rng):
    H, W = ctx.H, ctx.W
    n = int(L.get('n', 150) * ctx.detail)
    st = ctx.struct / (ctx.struct.max() + 1e-9)
    w_edge = st ** 2
    dens = np.ones((H, W))
    if ctx.FOCUS.any():
        dens[ctx.FOCUS] *= L.get('focus_density', 1.0)
    ne = int(n * L.get('edge_bias', 0.5))
    p1 = (w_edge * dens).ravel()
    p2 = (dens * (st + 0.06) ** L.get('density_gamma', 0.0)).ravel()   # >0: more, smaller cells where there is detail
    i1 = rng.choice(H * W, ne, replace=False, p=p1 / p1.sum())
    i2 = rng.choice(H * W, n - ne, replace=False, p=p2 / p2.sum())
    idx = np.concatenate([i1, i2])
    seeds = np.stack([idx % W, idx // W], 1).astype(float) + rng.uniform(-0.5, 0.5, (len(idx), 2))
    yy, xx = np.mgrid[0:H, 0:W]
    pts = np.stack([xx.ravel(), yy.ravel()], 1)
    _, lab = cKDTree(seeds).query(pts)
    lab = lab.reshape(H, W)
    split = L.get('split') or ('edge_line' if L.get('split_along_edges') else None)
    for _ in range(int(L.get('split_depth', 1)) if split else 0):
        lab = split_cells(ctx, lab, split, L.get('split_min_dL', 8))
    return lab, None, None


def _otsu_cut(vals):
    """Best two-way split of an ordered value sequence: index and between-class contrast (|mean1 - mean2|)."""
    n = len(vals)
    c = np.cumsum(vals)
    i = np.arange(1, n)
    m1 = c[:-1] / i
    m2 = (c[-1] - c[:-1]) / (n - i)
    score = i * (n - i) * (m1 - m2) ** 2
    k = int(np.argmax(score))
    return k + 1, abs(m1[k] - m2[k])


def split_cells(ctx, lab, how='edge_line', min_dL=8):
    """Split cells where the picture has an edge inside them, so the subject's silhouette survives.
    edge_line: one straight cut, perpendicular to the cell's dominant gradient, placed where the value changes most
               (angular shards that follow the edges: cubism)
    value:     split by the cell's own value threshold (pieces follow the actual contour: stained-glass panes)
    Cells whose two sides differ by less than min_dL (L units) stay whole."""
    lum = ndi.gaussian_filter(ctx.Tl[..., 0], 1.5)
    gx, gy = ndi.sobel(lum, 1), ndi.sobel(lum, 0)
    yy, xx = np.mgrid[0:ctx.H, 0:ctx.W]
    out = lab * 2
    n = lab.max() + 1
    sl = ndi.find_objects(lab + 1)
    for c in range(n):
        if sl[c] is None:
            continue
        m = lab[sl[c]] == c
        if m.sum() < 40:
            continue
        lv = lum[sl[c]][m]
        if how == 'value':
            order = np.argsort(lv)
            k, dl = _otsu_cut(lv[order])
            if dl < min_dL:
                continue
            side = lv > lv[order][k - 1]
        else:
            jxx, jyy, jxy = (v[sl[c]][m].sum() for v in (gx * gx, gy * gy, gx * gy))
            th = 0.5 * math.atan2(2 * jxy, jxx - jyy)      # gradient direction: the cut runs perpendicular to it
            ys, xs = yy[sl[c]][m], xx[sl[c]][m]
            proj = xs * math.cos(th) + ys * math.sin(th)
            order = np.argsort(proj)
            k, dl = _otsu_cut(lv[order])
            if dl < min_dL:
                continue
            side = proj > proj[order][k - 1]
        sub = out[sl[c]]
        sub[m] = c * 2 + side.astype(int)
    # give every connected piece its own id (value splits can produce several islands), absorb tiny islands
    ids = np.zeros_like(out)
    nxt = 0
    for v in np.unique(out):
        comp, k = ndi.label(out == v)
        for j in range(1, k + 1):
            ids[comp == j] = nxt
            nxt += 1
    sizes = np.bincount(ids.ravel())
    small = sizes[ids] < 25
    if small.any():
        idx = ndi.distance_transform_edt(small, return_distances=False, return_indices=True)
        ids = ids[tuple(idx)]
    _, inv = np.unique(ids, return_inverse=True)
    return inv.reshape(lab.shape)


def part_grid(ctx, L):
    H, W = ctx.H, ctx.W
    cols = int(L.get('cols', 36))
    rows = int(L.get('rows') or round(H / (W / cols)))
    xb = np.linspace(0, W, cols + 1)
    yb = np.linspace(0, H, rows + 1)
    cx = np.minimum(np.searchsorted(xb, np.arange(W) + 0.5) - 1, cols - 1)
    cy = np.minimum(np.searchsorted(yb, np.arange(H) + 0.5) - 1, rows - 1)
    lab = cy[:, None] * cols + cx[None, :]
    rects = [(xb[c], yb[r], xb[c + 1], yb[r + 1]) for r in range(rows) for c in range(cols)]
    return lab, rects, (rows, cols)


def part_mondrian(ctx, L, rng):
    """Guillotine partition: repeatedly split the cell with the most (area x value variation) along its strongest
    straight edge (full-length vertical or horizontal line), until n cells. Returns cell ids, rects, lines."""
    import heapq
    H, W = ctx.H, ctx.W
    lum = ndi.gaussian_filter(ctx.Tl[..., 0], 2)
    gx, gy = np.abs(ndi.sobel(lum, 1)), np.abs(ndi.sobel(lum, 0))
    min_px, min_frac = L.get('min_px', 40), L.get('min_frac', 0.12)
    n_target = int(L.get('n', 16) * max(0.5, ctx.detail))

    dp = L.get('detail_power', 0.0)    # 0: biggest cells first (classic); >0: cells with more value variation first

    def prio(x0, y0, x1, y1):
        reg = lum[int(y0):int(y1), int(x0):int(x1)]
        return -((x1 - x0) * (y1 - y0)) ** (1 - 0.5 * min(1, dp)) * (1 + reg.std() / 10) ** (1 + 2 * dp) * rng.uniform(0.85, 1.15)

    def best_split(x0, y0, x1, y1):
        w, h = x1 - x0, y1 - y0
        cands = []
        for kind, length, a0, a1, prof_fn in (
                ('v', w, x0, x1, lambda lo, hi: gx[int(y0):int(y1), lo:hi].mean(0)),
                ('h', h, y0, y1, lambda lo, hi: gy[lo:hi, int(x0):int(x1)].mean(1))):
            if length < 2 * min_px:
                continue
            lo, hi = int(a0 + max(min_px, length * min_frac)), int(a1 - max(min_px, length * min_frac))
            if hi <= lo:
                continue
            prof = prof_fn(lo, hi)
            prof = ndi.uniform_filter1d(prof, 5)
            i = int(np.argmax(prof + rng.uniform(0, prof.max() * 0.25 + 1e-6, prof.shape)))
            cands.append((kind, lo + i, length * (1 + prof[i] / (prof.mean() + 1e-6) * 0.15)))
        return max(cands, key=lambda c: c[2]) if cands else None

    heap = [(prio(0, 0, W, H), 0, (0, 0, W, H), 0)]
    rects, lines, cnt = [], [], 1
    while heap and len(heap) + len(rects) < n_target:
        _, _, (x0, y0, x1, y1), d = heapq.heappop(heap)
        sp = best_split(x0, y0, x1, y1)
        if sp is None:
            rects.append((x0, y0, x1, y1))
            continue
        kind, pos, _ = sp
        if kind == 'v':
            lines.append(((pos, y0), (pos, y1), d))
            kids = [(x0, y0, pos, y1), (pos, y0, x1, y1)]
        else:
            lines.append(((x0, pos), (x1, pos), d))
            kids = [(x0, y0, x1, pos), (x0, pos, x1, y1)]
        for r in kids:
            cnt += 1
            heapq.heappush(heap, (prio(*r), cnt, r, d + 1))
    rects += [r for _, _, r, _ in heap]
    lab = np.zeros((H, W), int)
    for i, (x0, y0, x1, y1) in enumerate(rects):
        lab[int(y0):int(y1), int(x0):int(x1)] = i
    return lab, rects, lines


# ------------------------------------------------------------------------------------------ colouring
def cell_means(ctx, lab):
    n = lab.max() + 1
    cnt = np.bincount(lab.ravel(), minlength=n).astype(float) + 1e-9
    return np.stack([np.bincount(lab.ravel(), ctx.Tl[..., c].ravel(), n) / cnt for c in range(3)], 1)


def colour_cells(ctx, L, lab, grid, rng):
    """Return a per-pixel palette-index map."""
    mode = L.get('color', 'nearest')
    means = cell_means(ctx, lab)
    use = np.array([ctx.color_index(c) for c in L['colors']]) if L.get('colors') else np.arange(len(ctx.pal))
    pal_use = ctx.pal_lab[use].copy()
    # match: {paint: proxy} -> the paint is chosen where the picture looks like the proxy colour (a stylised
    # palette that still traces the subject: yellow where the skin is light, blue/black where it is dark ...)
    for paint, proxy in (L.get('match') or {}).items():
        k = ctx.color_index(paint)
        hit = np.where(use == k)[0]
        if len(hit):
            pal_use[hit[0]] = col.rgb2lab(col.as_rgb(proxy)[None])[0]

    wv = np.array([L.get('value_weight', 1.0), 1.0, 1.0])

    def near(labs, jit=True):
        labs = np.asarray(labs, float)
        d = np.linalg.norm((labs[..., None, :] - pal_use) * wv, axis=-1)
        j = L.get('jitter', 0)
        if j and jit and d.ndim == 2:
            pick = np.empty(len(d), int)
            for i, row in enumerate(d):
                cand = np.where(row <= row.min() + j)[0]
                pick[i] = rng.choice(cand)
            return use[pick]
        return use[d.argmin(-1)]
    if mode == 'nearest':
        return near(means)[lab]
    if mode == 'dither':
        rows, cols = grid
        r, c = np.divmod(np.arange(len(means)), cols)
        m = means.copy()
        m[:, 0] += BAYER4[r % 4, c % 4] * L.get('dither', 8) * 2
        return near(m)[lab]
    if mode == 'mondrian':
        pal = ctx.pal_lab
        chroma_p = np.hypot(pal[:, 1], pal[:, 2])
        prim = np.where(chroma_p > 30)[0]
        neutral = np.where(chroma_p <= 30)[0]
        neutral = neutral[np.argsort(pal[neutral, 0])]           # dark .. light
        n = len(means)
        idx = np.empty(n, int)
        chroma = np.hypot(means[:, 1], means[:, 2])
        size = np.bincount(lab.ravel(), minlength=n)
        score = chroma + 0.15 * (means[:, 0] - 50) * 0          # saturation ranks the colour cells
        order = np.argsort(-score)
        n_prim = max(1, int(round(n * L.get('primary_share', 0.3))))
        n_black = int(round(n * L.get('black_share', 0.05)))
        idx[:] = -1
        darkest = np.argsort(means[:, 0])
        for c in darkest[:n_black]:
            if size[c] < np.median(size):                        # black only on small cells
                idx[c] = neutral[0]
        hue_p = np.arctan2(pal[prim, 2], pal[prim, 1])
        used = 0
        for c in order:
            if used >= n_prim:
                break
            if idx[c] >= 0:
                continue
            h = math.atan2(means[c, 2], means[c, 1]) + rng.normal(0, 0.6)
            d = np.abs(np.angle(np.exp(1j * (hue_p - h))))
            idx[c] = prim[int(d.argmin())]
            used += 1
        light = neutral[-1]
        grey = neutral[-2] if len(neutral) > 2 else light
        for c in range(n):
            if idx[c] < 0:
                idx[c] = light if means[c, 0] > L.get('grey_below', 45) else grey
        return idx[lab]
    if mode == 'shade':
        H, W = ctx.H, ctx.W
        yy, xx = np.mgrid[0:H, 0:W]
        nb, step = int(L.get('bands', 3)), float(L.get('shade_step', 12))
        out = np.empty((H, W), int)
        sl = ndi.find_objects(lab + 1)
        lum = ndi.gaussian_filter(ctx.Tl[..., 0], 1.5)
        gx, gy = ndi.sobel(lum, 1), ndi.sobel(lum, 0)
        sd = L.get('shade_dir', 'random')
        for c in range(len(means)):
            if sl[c] is None:
                continue
            m = lab[sl[c]] == c
            ys, xs = yy[sl[c]][m], xx[sl[c]][m]
            if sd == 'random':
                th = rng.uniform(0, 2 * math.pi)
            elif sd == 'edge':
                th = math.atan2(gy[sl[c]][m].sum(), gx[sl[c]][m].sum())
            else:
                th = math.radians(float(sd))
            proj = (xs - xs.mean()) * math.cos(th) + (ys - ys.mean()) * math.sin(th)
            if len(proj) > nb and proj.max() > proj.min():
                band = np.minimum((np.argsort(np.argsort(proj)) * nb) // len(proj), nb - 1)
            else:
                band = np.zeros(len(proj), int)
            off = (band - (nb - 1) / 2) * -step                 # band 0 = light side
            lab_c = np.repeat(means[c][None], len(proj), 0)
            lab_c[:, 0] = np.clip(lab_c[:, 0] + off, 0, 100)
            sub = out[sl[c]]
            k0 = near(means[c][None])[0]                         # the cell's paint (jitter applies per cell)
            shift = ctx.pal_lab[k0] - means[c]
            sub[m] = near(lab_c + shift * np.array([0, 1, 1]), jit=False)   # bands keep the chosen hue, vary the value
        return out
    raise ValueError('unknown cells color %r' % mode)


# ------------------------------------------------------------------------------------------ fills
def rect_fill(rects, colours, width, merge_rows=False, overlap=1.0):
    """Horizontal lines inside each rectangle, ends inset by width/2 so corners stay square.
    rects: [(x0,y0,x1,y1)], colours: palette index per rect. Returns [(k, pts)]."""
    items = list(zip(rects, colours))
    if merge_rows:   # merge horizontally adjacent rectangles of the same colour and the same row
        items.sort(key=lambda it: (round(it[0][1], 3), it[0][0]))
        merged = []
        for (x0, y0, x1, y1), k in items:
            if merged and merged[-1][1] == k and abs(merged[-1][0][1] - y0) < 1e-6 and abs(merged[-1][0][2] - x0) < 1e-6:
                (a0, b0, a1, b1), _ = merged[-1]
                merged[-1] = ((a0, b0, x1, b1), k)
            else:
                merged.append(((x0, y0, x1, y1), k))
        items = merged
    out = []
    for (x0, y0, x1, y1), k in items:
        h, w = y1 - y0, x1 - x0
        n = max(1, math.ceil((h - width) / (width * 0.8)) + 1)
        ov = overlap                                     # px past each edge: no seams when Paint rounds positions
        ys = [y0 + h / 2] if n == 1 else list(np.linspace(y0 + width / 2 - ov, y1 - width / 2 + ov, n))
        xa, xb = x0 + width / 2 - ov, x1 - width / 2 + ov
        if xb <= xa:
            xa = xb = (x0 + x1) / 2
        for y in ys:
            out.append((int(k), [[float(xa), float(y)], [float(xb) + (0.01 if xb == xa else 0), float(y)]]))
    out.sort(key=lambda s: s[0])
    return out


def layer_cells(ctx, L, seed, paint_labels):
    """Returns [(layer_dict, strokes)] sub-layers. paint_labels = planner's region painter for 'regions' fills."""
    rng = np.random.default_rng(seed)
    part = L.get('partition', 'voronoi')
    lines = None
    if part == 'voronoi':
        lab, rects, grid = part_voronoi(ctx, L, rng)
    elif part == 'grid':
        lab, rects, grid = part_grid(ctx, L)
    elif part == 'mondrian':
        lab, rects, lines = part_mondrian(ctx, L, rng)
        grid = None
    else:
        raise ValueError('unknown partition %r' % part)
    cmap = colour_cells(ctx, L, lab, grid, rng)
    out = []
    tool = L.get('tool', 'brush')
    if L.get('fill', 'regions') == 'rects' and rects is not None:
        k_of = [int(np.bincount(cmap[int(y0):max(int(y0) + 1, int(y1)), int(x0):max(int(x0) + 1, int(x1))].ravel()).argmax())
                for x0, y0, x1, y1 in rects]
        w = L.get('rect_width', 8)
        S = rect_fill(rects, k_of, w, merge_rows=(part == 'grid'), overlap=L.get('rect_overlap', 1.0))
        if L.get('first_is_ground', False):
            pass
        out.append(({'tool': tool, 'width': w, 'name': L.get('name', 'cells') + '-rects'}, S))
    else:
        out += paint_labels(ctx, L, cmap)
    ctx.labels = lab
    if lines:
        ln = L.get('lines', {})
        k = ctx.color_index(ln.get('color', 'darkest'))
        thick = [(k, [list(a), list(b)]) for a, b, d in lines if d < ln.get('thick_levels', 1)]
        thin = [(k, [list(a), list(b)]) for a, b, d in lines if d >= ln.get('thick_levels', 1)]
        if thin:
            out.append(({'tool': ln.get('tool', 'brush'), 'width': ln.get('width', 7), 'name': 'cells-lines'}, thin))
        if thick:
            out.append(({'tool': ln.get('tool', 'brush'), 'width': ln.get('thick_width', 12), 'name': 'cells-lines-thick'}, thick))
    return out


# ------------------------------------------------------------------------------------------ ornaments
def _square(x, y, s, lw):
    n = max(1, math.ceil((s - lw) / (lw * 0.8)) + 1)
    out = []
    for i in range(n):
        yy = y - s / 2 + lw / 2 + i * (s - lw) / max(1, n - 1) if n > 1 else y
        out.append([[x - (s - lw) / 2, yy], [x + (s - lw) / 2 + 0.01, yy]])
    return out


def _spiral(x, y, r, turns, rng):
    a0 = rng.uniform(0, 2 * math.pi)
    t = np.linspace(0, turns * 2 * math.pi, int(turns * 18) + 2)
    rr = r * t / t[-1]
    return [[[float(x + q * math.cos(a0 + u)), float(y + q * math.sin(a0 + u))] for u, q in zip(t, rr)]]


def _ring(x, y, r):
    t = np.linspace(0, 2 * math.pi, max(10, int(r * 1.5)))
    return [[[float(x + r * math.cos(u)), float(y + r * math.sin(u))] for u in t]]


def layer_ornament(ctx, L, seed):
    """Decorative motifs on a grid inside a mask: squares (mosaic tesserae), spirals, rings, dots, seal (one
    filled square stamp at `at`, e.g. the red hanko of an ink painting). Colour by target value (`colors` listed
    dark to light) or random."""
    rng = np.random.default_rng(seed)
    motif = L.get('motif', 'squares')
    cols = [ctx.color_index(c) for c in L.get('colors', ['darkest'])]
    s = float(L.get('size', 8))
    lw = float(L.get('width', 2))
    out = []
    if motif == 'seal':
        x, y = L.get('at', [0.88, 0.9])
        for p in _square(x * ctx.W, y * ctx.H, s, lw):
            out.append((cols[0], p))
        return out
    sp = float(L.get('spacing', s * 1.5)) / max(0.2, ctx.detail) ** 0.5
    only = ctx.mask(L.get('mask'))
    Lv = ndi.gaussian_filter(ctx.Tl[..., 0], 2)
    rows = np.arange(sp / 2, ctx.H, sp)
    for ri, y in enumerate(rows):
        off = sp / 2 if (L.get('grid', 'square') == 'hex' and ri % 2) else 0
        for x in np.arange(sp / 2 + off, ctx.W, sp):
            j = L.get('jitter', 0.15) * sp
            px, py = x + rng.uniform(-j, j), y + rng.uniform(-j, j)
            if not (s / 2 <= px < ctx.W - s / 2 and s / 2 <= py < ctx.H - s / 2):
                continue
            if only is not None and not only[int(py), int(px)]:
                continue
            if rng.random() > L.get('density', 1.0):
                continue
            if L.get('color_by', 'luminance') == 'luminance' and len(cols) > 1:
                k = cols[min(len(cols) - 1, int(Lv[int(py), int(px)] / 100 * len(cols) + rng.normal(0, 0.35)))]
            else:
                k = cols[int(rng.integers(len(cols)))]
            sz = s * rng.uniform(1 - L.get('size_jitter', 0.2), 1 + L.get('size_jitter', 0.2))
            if motif == 'squares':
                ps = _square(px, py, sz, lw)
            elif motif == 'spirals':
                ps = _spiral(px, py, sz / 2, L.get('turns', 2.5), rng)
            elif motif == 'rings':
                ps = _ring(px, py, sz / 2)
            elif motif == 'dots':
                ps = [[[px, py], [px + 0.5, py]]]
            else:
                raise ValueError('unknown motif %r' % motif)
            out += [(k, p) for p in ps]
    out.sort(key=lambda t: t[0])
    return out
