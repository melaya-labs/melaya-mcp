"""analyse: measure a reference painting's style and derive a preset JSON (mode 2: "paint X in the style of Y").

Measured features (on the reference, at most 700 px tall):
  palette_k        smallest k whose k-means quantisation stays under 6 dE (how many distinct paints)
  chroma           mean Lab chroma (saturation of the paint)
  L_mean, L_p5/p95 value key and range (dark chiaroscuro vs high-key watercolour)
  coherence        structure-tensor coherence at 2 px (directional brushwork vs dots / hatching mesh)
  swirl            coherence at 2 px minus at 12 px (locally directional, regionally turning: swirls)
  stroke_len_px    autocorrelation length of the texture along the local stroke direction
  stroke_w_px      autocorrelation length across it
  flatness         share of pixels in near-uniform areas (flat colour fields, washes)
  outline          share of edges that are thin dark lines (contour drawing: ukiyo-e, pop art, comics)
  texture          std of the high-pass luminance (impasto, broken colour)
The base style is picked by rules from these numbers, then tuned (palette size and colours from the
reference, saturation, stroke lengths and widths). Always look at the reference yourself and adjust the JSON.
"""
import json
import math
import os

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

from . import color as col

STYLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'styles')


def features(path):
    im = Image.open(path).convert('RGB')
    s = min(1.0, 700 / im.size[1])
    im = im.resize((max(8, int(im.size[0] * s)), max(8, int(im.size[1] * s))), Image.LANCZOS)
    a = np.asarray(im).astype(float) / 255
    lab = col.rgb2lab(a)
    L = lab[..., 0]
    H, W = L.shape
    f = {}
    small = lab[::3, ::3].reshape(-1, 3)
    f['palette_k'] = 40
    for k in (4, 6, 8, 12, 16, 24, 32):
        C, lbl = col.kmeans_lab(small, k, iters=12)
        if np.linalg.norm(small - C[lbl], axis=1).mean() < 6:
            f['palette_k'] = k
            break
    f['chroma'] = float(np.hypot(lab[..., 1], lab[..., 2]).mean())
    f['L_mean'] = float(L.mean())
    f['L_p5'], f['L_p95'] = float(np.percentile(L, 5)), float(np.percentile(L, 95))
    gx, gy = ndi.sobel(ndi.gaussian_filter(L, 0.8), 1), ndi.sobel(ndi.gaussian_filter(L, 0.8), 0)

    def tensor(sig):
        jxx, jyy, jxy = (ndi.gaussian_filter(v, sig) for v in (gx * gx, gy * gy, gx * gy))
        return np.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2) / (jxx + jyy + 1e-6), jxx + jyy, jxx, jyy, jxy
    c2, e2, jxx, jyy, jxy = tensor(2)
    c12 = tensor(12)[0]
    tex = e2 > np.percentile(e2, 40)
    f['coherence'] = float(c2[tex].mean())          # directional brushwork (high) vs dots / hatching mesh (low)
    f['swirl'] = float((c2[tex] - c12[tex]).mean())   # locally directional, regionally turning
    Ls = ndi.gaussian_filter(L, 1.2)
    sd = np.sqrt(np.maximum(ndi.uniform_filter(Ls * Ls, 7) - ndi.uniform_filter(Ls, 7) ** 2, 0))
    f['flatness'] = float((sd < 1.5).mean())
    gm = np.hypot(gx, gy)
    edges = gm > np.percentile(gm, 85)
    f['outline'] = float(((ndi.grey_closing(L, size=5) - L)[edges] > 12).mean())
    hp = L - ndi.gaussian_filter(L, 2)
    f['texture'] = float(hp.std())
    theta = 0.5 * np.arctan2(2 * jxy, jxx - jyy)
    tx, ty = -np.sin(theta), np.cos(theta)
    rng = np.random.default_rng(0)
    m = tex.copy()
    m[:20], m[-20:], m[:, :20], m[:, -20:] = False, False, False, False
    ys, xs = np.nonzero(m)
    sel = rng.choice(len(ys), min(4000, len(ys)), replace=False)
    ys, xs = ys[sel], xs[sel]
    h0 = hp[ys, xs]

    def corr_len(dx, dy):
        for d in range(1, 40):
            v = ndi.map_coordinates(hp, [np.clip(ys + d * dy, 0, H - 1), np.clip(xs + d * dx, 0, W - 1)], order=1)
            if np.corrcoef(h0, v)[0, 1] < 0.3:
                return d
        return 40
    f['stroke_len_px'] = corr_len(tx[ys, xs], ty[ys, xs])
    f['stroke_w_px'] = corr_len(-ty[ys, xs], tx[ys, xs])
    f['size'] = [W, H]
    return {k: (round(v, 3) if isinstance(v, float) else v) for k, v in f.items()}


def pick_base(f):
    """Heuristic first guess (calibrated on Starry Night, The Great Wave, La Grande Jatte, the Mona Lisa and the
    skill's own style renders). Always confirm by looking at the reference; pass --base to override."""
    if f['chroma'] < 6:
        return 'chiaroscuro' if f['L_mean'] < 40 else 'pencil-sketch'
    if f['chroma'] > 40 and f['outline'] > 0.3:
        return 'pop-art'
    if f['outline'] > 0.38 and f['flatness'] > 0.4:
        return 'ukiyo-e'
    if f['coherence'] < 0.56 and f['flatness'] < 0.3:
        return 'pointillism'
    if f['coherence'] > 0.62 and f['flatness'] < 0.35 and f['texture'] > 7:
        return 'van-gogh'
    if f['L_mean'] < 35 and f['flatness'] > 0.4:
        return 'chiaroscuro'
    if f['L_mean'] > 55 and f['flatness'] > 0.4 and f['chroma'] < 25:
        return 'watercolour'
    if f['texture'] > 5 and f['flatness'] < 0.6:
        return 'impressionist'
    return 'master'


def derive(ref, base=None, out=None):
    f = features(ref)
    name = base or pick_base(f)
    with open(os.path.join(STYLES_DIR, name + '.json')) as fh:
        P = json.load(fh)
    P['name'] = 'from-' + os.path.splitext(os.path.basename(ref))[0]
    P['description'] = 'Derived from %s (base %s). Edit after looking at the reference.' % (os.path.basename(ref), name)
    P['derived_from'] = {'reference': os.path.abspath(ref), 'base': name, 'features': f}
    pal = P.setdefault('palette', {})
    if pal.get('mode', 'kmeans') == 'kmeans':
        pal['mode'] = 'reference'
        pal['k'] = int(min(36, max(pal.get('k', 16) // 2, f['palette_k'])))
    # stroke geometry: elongation of the reference's marks (length / width) scales the base style's stroke length
    ratio = f['stroke_len_px'] / max(1, f['stroke_w_px'])
    k_len = float(np.clip(ratio / 3.0, 0.6, 1.6))
    for L in P.get('layers', []):
        if L.get('type', 'strokes') == 'strokes' and 'max_len' in L and L.get('width', 0) >= 4:
            L['max_len'] = int(min(24, max(1, round(L['max_len'] * k_len))))
    # saturation: keep the style's character, nudged toward the reference's chroma
    P['prefilter'] = dict(P.get('prefilter', {}))
    P['prefilter']['saturation'] = round(P['prefilter'].get('saturation', 1.0) * float(np.clip(f['chroma'] / 22, 0.75, 1.25)), 2)
    P['derived_from']['stroke_len_scale'] = round(k_len, 2)
    if out:
        with open(out, 'w') as fh:
            json.dump(P, fh, indent=1)
    return P, f
