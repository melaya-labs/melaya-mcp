"""Speed-ups that keep the painted result identical (or within the colour-merge threshold).

optimise_layer(S, tool, merge_dE, pal_lab, can_reverse)
    - colour merge: colours of one layer closer than merge_dE (Lab) become the most used one (fewer picks)
    - per colour: drop exactly collinear points, chain strokes whose ends touch (no extra paint), order strokes
      by nearest neighbour + 2-opt on pen-up travel (reversing a stroke only when the tool is direction-free)

fill_render(ctx, cmap, outline_tool_width=1)
    Outline + bucket fill for flat colour regions: each connected region of one colour gets a 1 px ring in its own
    colour along its inner border (every region pixel with a 4-neighbour outside the region or the image; with an
    8-neighbour when the bucket floods 8-connected), then one Fill click on a guaranteed interior pixel of each
    interior component, so a flood from the interior cannot leak. The result is
    verified by simulation (pencil rasterisation + flood fill on a label canvas); a region that leaks or misses
    pixels falls back to ordinary strokes (returned in 'fallback').
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

from . import color as col


# ------------------------------------------------------------------------------------------ strokes
def _collinear_prune(pts):
    if len(pts) < 3:
        return pts
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = out[-1], pts[i], pts[i + 1]
        cross = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        dot = (b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1])
        if abs(cross) < 1e-9 and dot > 0:
            continue
        out.append(b)
    out.append(pts[-1])
    return out


def _chain(strokes, can_reverse, tol=0.6):
    """Join strokes whose ends touch (within tol px): the joined stroke paints exactly the same pixels."""
    strokes = [list(map(tuple, s)) for s in strokes]
    if len(strokes) > 3000:                      # keep it linear-time for huge dot layers (dots never touch)
        return strokes
    ends = {}
    for i, s in enumerate(strokes):
        ends.setdefault((round(s[0][0]), round(s[0][1])), []).append((i, 0))
        ends.setdefault((round(s[-1][0]), round(s[-1][1])), []).append((i, 1))
    used = [False] * len(strokes)
    out = []
    for i in range(len(strokes)):
        if used[i]:
            continue
        used[i] = True
        cur = strokes[i]
        grown = True
        while grown:
            grown = False
            key = (round(cur[-1][0]), round(cur[-1][1]))
            for j, side in ends.get(key, []):
                if used[j]:
                    continue
                s = strokes[j]
                if side == 0 and math.dist(cur[-1], s[0]) <= tol:
                    cur = cur + s[1:]
                elif side == 1 and can_reverse and math.dist(cur[-1], s[-1]) <= tol:
                    cur = cur + s[::-1][1:]
                else:
                    continue
                used[j] = True
                grown = True
                break
        out.append(cur)
    return out


def _order(strokes, can_reverse):
    """Nearest-neighbour tour over stroke ends, then 2-opt on the stroke sequence (small groups)."""
    n = len(strokes)
    if n < 3:
        return strokes
    starts = np.array([s[0] for s in strokes], float)
    endsa = np.array([s[-1] for s in strokes], float)
    left = np.ones(n, bool)
    cur = 0
    left[0] = False
    order, rev = [0], [False]
    pos = endsa[0]
    for _ in range(n - 1):
        d0 = np.where(left, np.hypot(*(starts - pos).T), np.inf)
        j0 = int(d0.argmin())
        if can_reverse:
            d1 = np.where(left, np.hypot(*(endsa - pos).T), np.inf)
            j1 = int(d1.argmin())
            if d1[j1] < d0[j0]:
                left[j1] = False
                order.append(j1)
                rev.append(True)
                pos = starts[j1]
                continue
        left[j0] = False
        order.append(j0)
        rev.append(False)
        pos = endsa[j0]
    seq = [strokes[i][::-1] if r else strokes[i] for i, r in zip(order, rev)]
    if len(seq) <= 300:                          # 2-opt on segment order (no reversal of the strokes themselves)
        def gap(a, b):
            return math.dist(a[-1], b[0])
        improved, it = True, 0
        while improved and it < 4:
            improved, it = False, it + 1
            for i in range(1, len(seq) - 2):
                for k in range(i + 1, len(seq) - 1):
                    if k - i > 60:
                        break
                    d_old = gap(seq[i - 1], seq[i]) + gap(seq[k], seq[k + 1])
                    d_new = gap(seq[i - 1], seq[k]) + gap(seq[i], seq[k + 1])
                    if d_new + 1e-9 < d_old and can_reverse:
                        seq[i:k + 1] = [s[::-1] for s in seq[i:k + 1][::-1]]
                        improved = True
    return seq


def optimise_layer(S, can_reverse=True, merge_dE=0.0, pal_lab=None):
    """S: [(k, pts)] grouped by colour. Returns (S', stats)."""
    n0 = len(S)
    if merge_dE and pal_lab is not None and S:
        used = {}
        for k, _ in S:
            used[k] = used.get(k, 0) + 1
        ks = sorted(used, key=lambda k: -used[k])
        rep = {}
        for k in ks:
            if k in rep:
                continue
            rep[k] = k
            for j in ks:
                if j not in rep and np.linalg.norm(pal_lab[k] - pal_lab[j]) < merge_dE:
                    rep[j] = k
        S = [(rep[k], pts) for k, pts in S]
    groups, order = {}, []
    for k, pts in S:
        if k not in groups:
            groups[k] = []
            order.append(k)
        groups[k].append([tuple(p) for p in pts])
    out = []
    for k in order:
        g = [_collinear_prune(s) for s in groups[k]]
        g = _chain(g, can_reverse)
        g = _order(g, can_reverse)
        out += [(k, [list(p) for p in s]) for s in g]
    return out, {'strokes_in': n0, 'strokes_out': len(out), 'colours': len(order)}


# ------------------------------------------------------------------------------------------ outline + fill
NB8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def _trace(B):
    """Cover every pixel of the boolean mask B with 8-connected chains (lists of (x, y))."""
    H, W = B.shape
    vis = ~B.copy()
    pts = np.argwhere(B)
    nb = ndi.convolve(B.astype(int), np.ones((3, 3), int), mode='constant') - B
    order = sorted(map(tuple, pts), key=lambda p: nb[p])     # start at ends
    chains = []
    for y, x in order:
        if vis[y, x]:
            continue
        ch = [(x, y)]
        vis[y, x] = True
        pdx = pdy = 0
        while True:
            best, bs = None, -99
            for dy, dx in NB8:
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and not vis[ny, nx]:
                    # Warnsdorff: go first to the pixel with the fewest unvisited neighbours (clears 2 px wide
                    # rings in one pass), then keep the direction, then prefer 4-neighbours
                    free = sum(1 for ey, ex in NB8 if 0 <= ny + ey < H and 0 <= nx + ex < W and not vis[ny + ey, nx + ex])
                    s = -2.0 * free + dx * pdx + dy * pdy - 0.3 * (abs(dx) + abs(dy) - 1)
                    if s > bs:
                        best, bs = (ny, nx, dy, dx), s
            if best is None:
                break
            y, x, pdy, pdx = best
            vis[y, x] = True
            ch.append((x, y))
        chains.append(ch)
    return chains


def raster_pencil(lab, strokes, value):
    """Rasterise 1 px pencil polylines (aliased, Bresenham) into the int label image lab (in place)."""
    img = Image.fromarray(lab.astype(np.int32), mode='I')
    d = ImageDraw.Draw(img)
    for pts in strokes:
        q = [(float(x), float(y)) for x, y in pts]
        if len(q) == 1:
            d.point(q[0], fill=int(value))
        else:
            d.line(q, fill=int(value), width=1)
    lab[:] = np.asarray(img)


def flood(lab, x, y, conn=4):
    """Pixels flooded by a Fill click at (x, y): the connected area of exactly lab[y, x]."""
    m = lab == lab[y, x]
    st = ndi.generate_binary_structure(2, 1 if conn == 4 else 2)
    comp, _ = ndi.label(m, st)
    return comp == comp[y, x]


def fill_render(cmap, min_area=12, fill_conn='both'):
    """cmap: HxW palette-index map. Returns dict(outline=[(k, pts)], fills=[(k, [[x, y], [x + 0.5, y]])],
    fallback_mask=bool HxW (pixels to paint with ordinary strokes), stats). fill_conn = the connectivity of Paint's
    bucket: 'both' (default, safe for either: 8-neighbour ring, one seed per 4-connected interior part, verified with
    the 8 flood for leaks and the 4 flood for coverage), 4 or 8 once speed-calib has measured it (4 is leanest)."""
    H, W = cmap.shape
    WHITE = -1
    canvas = np.full((H, W), WHITE, np.int32)
    outline, fills = [], []
    fallback = np.zeros((H, W), bool)
    n_regions = n_fill = 0
    st8 = ndi.generate_binary_structure(2, 2)
    for k in np.unique(cmap):
        comp, n = ndi.label(cmap == k, st8)
        sl = ndi.find_objects(comp)
        for r in range(1, n + 1):
            s = sl[r - 1]
            y0, y1 = max(0, s[0].start - 1), min(H, s[0].stop + 1)
            x0, x1 = max(0, s[1].start - 1), min(W, s[1].stop + 1)
            R = comp[y0:y1, x0:x1] == r
            n_regions += 1
            # border: region pixels with any 8-neighbour outside the region or outside the image
            pad = np.pad(R, 1, constant_values=False)
            # the ring needed against a 4-connected flood is the 4-neighbour border (a thin closed curve); against an
            # 8-connected flood it is the 8-neighbour border (thicker at concave corners)
            st_b = ndi.generate_binary_structure(2, 1) if fill_conn == 4 else st8
            inner = ndi.binary_erosion(pad, st_b, border_value=0)[1:-1, 1:-1]
            touch_img = np.zeros_like(R)
            if y0 == 0: touch_img[0, :] = True
            if y1 == H: touch_img[-1, :] = True
            if x0 == 0: touch_img[:, 0] = True
            if x1 == W: touch_img[:, -1] = True
            inner &= ~touch_img
            B = R & ~inner
            if R.sum() < min_area:
                fallback[y0:y1, x0:x1] |= R
                continue
            for ch in _trace(B):
                pts = [(x + x0, y + y0) for x, y in ch]
                if len(pts) == 1:          # a lone border pixel: draw it as a 2-point stroke toward a region pixel
                    px, py = pts[0]
                    for dx, dy in NB8:
                        qx, qy = px + dx, py + dy
                        if 0 <= qy - y0 < R.shape[0] and 0 <= qx - x0 < R.shape[1] and R[qy - y0, qx - x0]:
                            pts.append((qx, qy))
                            break
                pts = _collinear_prune(pts)
                outline.append((int(k), [[float(x), float(y)] for x, y in pts]))
            ic, ni = ndi.label(inner, st8 if fill_conn == 8 else ndi.generate_binary_structure(2, 1))   # 'both': per 4-part
            if ni:
                dist = ndi.distance_transform_edt(inner)
                for c in range(1, ni + 1):
                    m = ic == c
                    yy, xx = np.unravel_index(np.argmax(np.where(m, dist, -1)), m.shape)
                    fills.append((int(k), (int(xx + x0), int(yy + y0))))
                    n_fill += 1
    # ---- verify by simulation: outlines then fills, flood with the chosen connectivity
    by_k = {}
    for k, pts in outline:
        by_k.setdefault(k, []).append(pts)
    for k, ss in by_k.items():
        raster_pencil(canvas, ss, k)
    bad = np.zeros((H, W), bool)
    ok_fills = []
    for k, (x, y) in fills:
        if canvas[y, x] != WHITE:
            bad |= cmap == k
            continue
        f = flood(canvas, x, y, 8 if fill_conn in (8, 'both') else 4)     # leak check with the wider flood
        if (cmap[f] != k).any():       # leak: do not click it, paint the region with strokes
            bad |= f & (cmap == k)
            continue
        if fill_conn == 'both':
            f = flood(canvas, x, y, 4)                                    # coverage with the narrower flood
        canvas[f] = k
        ok_fills.append((k, [[float(x), float(y)], [float(x) + 0.5, float(y)]]))
    miss = (canvas != cmap) & (canvas == WHITE)
    fallback |= miss | bad
    wrong = int(((canvas != cmap) & (canvas != WHITE)).sum())
    return dict(outline=outline, fills=ok_fills, fallback_mask=fallback,
                stats={'regions': n_regions, 'outline_strokes': len(outline), 'fills': len(ok_fills),
                       'fills_rejected': n_fill - len(ok_fills), 'fallback_px': int(fallback.sum()),
                       'wrong_px': wrong})
