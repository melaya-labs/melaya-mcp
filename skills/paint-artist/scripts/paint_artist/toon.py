"""Toon rendering helpers (manga, anime cel, cartoon, comic): numpy + scipy only.

- kuwahara(): edge-preserving smoothing. Each pixel takes the mean colour of the least varied of the four quadrant
  windows around it, so skin, cloth and sky flatten into cel-like shapes while edges stay sharp. Used as the
  `toon` prefilter (prepare.py).
- line_mask(): ink lines on the dark side of edges, from a difference of Gaussians (the XDoG family of line
  extractors behind photo-to-manga line art), cleaned of specks.
- thin(): Zhang-Suen thinning to one-pixel paths, which planner.trace_chains turns into brush strokes.
"""
import numpy as np
from scipy import ndimage as ndi

LUMA = np.array([0.299, 0.587, 0.114])


def _shift(a, dy, dx, h):
    """a[y + dy, x + dx] with edge clamping (h >= |dy|, |dx|)."""
    pad = ((h, h), (h, h)) + ((0, 0),) * (a.ndim - 2)
    p = np.pad(a, pad, mode='edge')
    H, W = a.shape[:2]
    return p[h + dy:h + dy + H, h + dx:h + dx + W]


def kuwahara(img, radius=4, passes=1, soft=0.0):
    """Edge-preserving smoothing of an RGB float image (H, W, 3) in [0, 1]: Gaussian-weighted quadrant windows
    (no blocky tiles), `passes` times, then an optional light Gaussian `soft` (px) to round the cel edges."""
    r = max(1, int(radius))
    h = (r + 1) // 2
    sg = max(0.8, r / 2.0)
    out = img.astype(float)
    for _ in range(max(1, int(passes))):
        L = out @ LUMA
        mL = ndi.gaussian_filter(L, sg, mode='reflect')
        var = ndi.gaussian_filter(L * L, sg, mode='reflect') - mL * mL
        mC = np.stack([ndi.gaussian_filter(out[..., c], sg, mode='reflect') for c in range(3)], -1)
        best = np.full(L.shape, np.inf)
        res = np.empty_like(out)
        for dy in (-h, h):
            for dx in (-h, h):
                v = _shift(var, dy, dx, h)
                m = _shift(mC, dy, dx, h)
                u = v < best
                best[u] = v[u]
                res[u] = m[u]
        out = res
    if soft:
        out = np.stack([ndi.gaussian_filter(out[..., c], soft) for c in range(3)], -1)
    return np.clip(out, 0, 1)


def line_mask(gray, sigma=1.0, k=1.6, tau=0.02, min_area=12, close=0):
    """Boolean ink-line mask: pixels on the dark side of an edge, where the narrow blur is darker than the wide one
    by more than `tau` (gray in [0, 1]). Specks smaller than `min_area` px are dropped."""
    g1 = ndi.gaussian_filter(gray, sigma)
    g2 = ndi.gaussian_filter(gray, sigma * k)
    B = (g1 - g2) < -abs(tau)
    if close:
        B = ndi.binary_closing(B, iterations=int(close))
    lab, n = ndi.label(B, structure=np.ones((3, 3)))
    if n:
        sizes = ndi.sum(B, lab, index=np.arange(1, n + 1))
        keep = np.zeros(n + 1, bool)
        keep[1:] = sizes >= min_area
        B = keep[lab]
    return B


def thin(B):
    """Zhang-Suen thinning (vectorised): a boolean mask reduced to one-pixel-wide paths."""
    A = np.asarray(B, np.uint8).copy()
    while True:
        changed = False
        for step in (0, 1):
            P = np.pad(A, 1)
            p2, p3, p4 = P[:-2, 1:-1], P[:-2, 2:], P[1:-1, 2:]
            p5, p6, p7 = P[2:, 2:], P[2:, 1:-1], P[2:, :-2]
            p8, p9 = P[1:-1, :-2], P[:-2, :-2]
            nb = [p2, p3, p4, p5, p6, p7, p8, p9]
            cnt = sum(n.astype(int) for n in nb)
            trans = sum(((nb[i] == 0) & (nb[(i + 1) % 8] == 1)).astype(int) for i in range(8))
            if step == 0:
                c = ((p2 * p4 * p6) == 0) & ((p4 * p6 * p8) == 0)
            else:
                c = ((p2 * p4 * p8) == 0) & ((p2 * p6 * p8) == 0)
            m = (A == 1) & (cnt >= 2) & (cnt <= 6) & (trans == 1) & c
            if m.any():
                A[m] = 0
                changed = True
        if not changed:
            return A.astype(bool)
