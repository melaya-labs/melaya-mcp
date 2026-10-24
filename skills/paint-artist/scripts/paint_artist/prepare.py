"""prepare: source image (or composed scene) -> job folder with target.png, palette, canvas.png, meta.json.

Canvas layout (all apps): a white image whose left strip holds the palette swatches (x 10..40, one swatch per
colour, `swh` px high, 1 px white gap), and the drawing area at (60, 9) of size W x H, 30 px right margin and
9 px bottom margin. The frame (optional) is painted in those margins. In Paint the colours are taken from this
strip with the colour picker, so the strip IS the palette: never paint over x < 44.
"""
import json
import os
import shutil

import numpy as np
from PIL import Image

from . import color as col

STRIP_X0, STRIP_X1, DRAW_X0, DRAW_Y0, MARGIN_R, MARGIN_B = 10, 40, 60, 9, 30, 9
MAX_SWATCHES = 40
FRAME_COLOURS = {'walnut': (0.24, 0.15, 0.10), 'gold': (0.80, 0.64, 0.32), 'dark': (0.05, 0.03, 0.08)}


def load_rgb(path):
    return np.asarray(Image.open(path).convert('RGB')).astype(float) / 255


def save_rgb(a, path):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)


def fit(img, W, H, mode='crop'):
    """Resize a PIL image to W x H. crop = centre-crop to the aspect first; stretch = plain resize."""
    if mode == 'crop':
        w, h = img.size
        a = W / H
        if w / h > a:
            nw = round(h * a)
            img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = round(w / a)
            img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return img.resize((W, H), Image.LANCZOS)


def ellipse_mask(H, W, ells, scale=1.0):
    yy, xx = np.mgrid[0:H, 0:W] / np.array([H, W])[:, None, None]
    m = np.zeros((H, W), bool)
    for cx, cy, rx, ry in ells:
        m |= ((xx - cx) / (rx * scale)) ** 2 + ((yy - cy) / (ry * scale)) ** 2 < 1
    return m


def vignette(T, v, focus=None):
    """Tenebrism: darken L away from the lit centre (first focus ellipse, else v['center'])."""
    H, W = T.shape[:2]
    cx, cy = (focus[0][0], focus[0][1]) if focus else tuple(v.get('center', [0.5, 0.42]))
    yy, xx = np.mgrid[0:H, 0:W] / np.array([H, W])[:, None, None]
    d = np.hypot((xx - cx) * W / max(W, H), (yy - cy) * H / max(W, H))
    r0, r1 = v.get('inner', 0.18), v.get('outer', 0.65)
    t = np.clip((d - r0) / (r1 - r0), 0, 1)
    k = 1 - v.get('strength', 0.6) * t * t * (3 - 2 * t)
    lab = col.rgb2lab(T)
    lab[..., 0] *= k
    lab[..., 1:] *= (0.5 + 0.5 * k)[..., None]
    return col.lab2rgb(lab)


def complement_shadows(T, v):
    """Fauve shadows: below an L threshold, push the colour toward the complement family (green for warm
    shadows, violet for cool ones), keeping the value."""
    lab = col.rgb2lab(T)
    thr, k = v.get('L', 50), v.get('strength', 0.7)
    w = np.clip((thr - lab[..., 0]) / v.get('soft', 15), 0, 1)[..., None] * k
    warm = (lab[..., 1] + lab[..., 2] > 0)[..., None]
    green, violet = np.array(v.get('warm_to', [-45, 25])), np.array(v.get('cool_to', [35, -45]))
    tgt = np.where(warm, green, violet)
    lab[..., 1:] = (1 - w) * lab[..., 1:] + w * tgt
    return col.lab2rgb(lab)


def warp(T, v):
    """Expressionist distortion: displace the image with smooth low-frequency waves (amp px, wavelength px)."""
    from scipy import ndimage as ndi
    H, W = T.shape[:2]
    rng = np.random.default_rng(v.get('seed', 5))
    amp, wl = v.get('amp', 10), v.get('wavelength', 140)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    dx = np.zeros((H, W))
    dy = np.zeros((H, W))
    for _ in range(3):
        f, ph, an = 2 * np.pi / (wl * rng.uniform(0.7, 1.4)), rng.uniform(0, 6.3), rng.uniform(0, np.pi)
        dx += amp / 3 * np.sin(f * (xx * np.cos(an) + yy * np.sin(an)) + ph)
        f, ph, an = 2 * np.pi / (wl * rng.uniform(0.7, 1.4)), rng.uniform(0, 6.3), rng.uniform(0, np.pi)
        dy += amp / 3 * np.sin(f * (xx * np.cos(an) + yy * np.sin(an)) + ph)
    return np.stack([ndi.map_coordinates(T[..., c], [yy + dy, xx + dx], order=1, mode='nearest') for c in range(3)], -1)


def fade_edges(T, v):
    """Let the image dissolve into bare paper toward the borders with an irregular edge (watercolour, sketch)."""
    from scipy import ndimage as ndi
    H, W = T.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    # rounded-rectangle (superellipse) distance: a soft vignette of bare paper, slightly irregular
    u, w_ = np.abs(xx / (W - 1) * 2 - 1), np.abs(yy / (H - 1) * 2 - 1)
    p = v.get('roundness', 5.0)
    r = (u ** p + w_ ** p) ** (1 / p)
    rng = np.random.default_rng(v.get('seed', 3))
    nz = ndi.gaussian_filter(rng.normal(0, 1, (H, W)), max(H, W) * v.get('noise_scale', 0.06))
    nz /= np.abs(nz).max() + 1e-9
    w0 = v.get('width', 0.1) * 2
    t = np.clip((1 - r - w0 * 0.15 + nz * w0 * v.get('noise', 0.35)) / w0, 0, 1)
    t = (t * t * (3 - 2 * t))[..., None]
    paper = np.array(v.get('paper', [1.0, 1.0, 1.0]))
    return t * T + (1 - t) * paper, t[..., 0]


def build_palette(T, preset, focus, reference=None, frame=True):
    """Return palette (n,3) 0..1, info dict. Modes: kmeans (from the target), reference (k-means on a reference
    painting), fixed (preset colours), bands (luminance bands -> fixed colours, pop art)."""
    P = preset.get('palette', {})
    mode = P.get('mode', 'kmeans')
    include = [col.as_rgb(c) for c in P.get('include', [])]
    frame_cols = list(FRAME_COLOURS.values()) if frame else []
    budget = MAX_SWATCHES - len(include) - len(frame_cols)
    k = min(P.get('k', 24), budget)
    info = {'mode': mode}
    if mode in ('fixed', 'bands'):
        pal = np.array([col.as_rgb(c) for c in P['colors']])
    else:
        src = reference if (mode == 'reference' and reference is not None) else T
        s = 2 if src.shape[0] > 300 else 1
        small = src[::s, ::s]
        lab = col.rgb2lab(small)
        wts = None
        if focus and src is T and P.get('focus_weight', 1) != 1:
            fm = ellipse_mask(small.shape[0], small.shape[1], focus, 1.1)
            wts = np.where(fm, P['focus_weight'], 1.0).ravel()
        C, lbl = col.kmeans_lab(lab, k, wts, seed=P.get('seed', 0))
        flat = small.reshape(-1, 3)
        pal = np.array([flat[lbl == j].mean(0) if (lbl == j).any() else col.lab2rgb(C[j]) for j in range(len(C))])
        if P.get('snap'):
            pal = col.snap_palette(pal, [col.as_rgb(c) for c in P['snap']['colors']], P['snap'].get('amount', 0.7))
        if P.get('saturation', 1) != 1 or P.get('value', 0):
            pal = col.adjust(pal[None], saturation=P.get('saturation', 1), brightness=P.get('value', 0))[0]
        if P.get('min_L') is not None:  # impressionists: no black; lift the darkest colours into deep blue-violet
            lab_p = col.rgb2lab(pal)
            low = lab_p[:, 0] < P['min_L']
            lab_p[low, 0] = P['min_L']
            lab_p[low, 2] = np.minimum(lab_p[low, 2], -18)
            lab_p[low, 1] = np.maximum(lab_p[low, 1], 8)
            pal = col.lab2rgb(lab_p)
    pal = list(np.clip(pal, 0, 1))
    pal += include
    frame_idx = {}
    for name, c in zip(FRAME_COLOURS, frame_cols):
        pl = col.rgb2lab(np.array(pal))
        d = np.linalg.norm(pl - col.rgb2lab(np.array(c)), axis=1)
        if d.min() < 6:
            frame_idx[name] = int(d.argmin())
        else:
            pal.append(np.array(c))
            frame_idx[name] = len(pal) - 1
    pal = np.array(pal)
    if mode != 'bands':  # swatch order: dark to light (bands keep their band order)
        order = np.argsort(col.rgb2lab(pal)[:, 0], kind='stable')
        inv = np.empty(len(order), int)
        inv[order] = np.arange(len(order))
        pal = pal[order]
        frame_idx = {n: int(inv[i]) for n, i in frame_idx.items()}
        info['band_count'] = None
    else:
        info['band_count'] = len(P['colors'])
    info['frame'] = frame_idx
    return pal, info


def make_canvas(W, H, pal, path):
    K = len(pal)
    Wc, Hc = DRAW_X0 + W + MARGIN_R, DRAW_Y0 + H + MARGIN_B
    swh = min(17, (Hc - DRAW_Y0 - 1) // K)
    if swh < 6:
        raise SystemExit('palette of %d colours does not fit a %d px tall canvas (swatch %d px < 6): lower k or raise height' % (K, Hc, swh))
    img = np.ones((Hc, Wc, 3))
    for i, c in enumerate(pal):
        y0 = DRAW_Y0 + swh * i
        img[y0:y0 + swh - 1, STRIP_X0:STRIP_X1 + 1] = np.round(c * 255) / 255
    save_rgb(img, path)
    return dict(canvas=[Wc, Hc], draw_origin=[DRAW_X0, DRAW_Y0], strip=dict(x0=STRIP_X0, x1=STRIP_X1, y0=DRAW_Y0, swh=swh))


def prepare(source, out, preset, width=None, height=672, fit_mode='crop', focus=None, face_box=None,
            reference=None, frame=True, transfer=False):
    os.makedirs(out, exist_ok=True)
    src = Image.open(source).convert('RGB')
    H = int(height)
    W = int(width) if width else int(round(H * src.size[0] / src.size[1]))
    raw = np.asarray(fit(src, W, H, fit_mode)).astype(float) / 255
    ref = None
    if reference:
        ref = np.asarray(fit(Image.open(reference).convert('RGB'), W, H, 'crop')).astype(float) / 255
    T = raw
    pf = preset.get('prefilter', {})
    if transfer and ref is not None:
        T = col.reinhard_transfer(T, ref)
    T = col.adjust(T, pf.get('saturation', 1), pf.get('contrast', 1), pf.get('gamma', 1), pf.get('brightness', 0))
    if pf.get('complement_shadows'):
        T = complement_shadows(T, pf['complement_shadows'])
    if pf.get('warp'):
        T = warp(T, pf['warp'])
    if pf.get('vignette'):
        T = vignette(T, pf['vignette'], focus)
    if pf.get('fade_edges'):
        T, wfade = fade_edges(T, pf['fade_edges'])
        save_rgb(np.repeat(wfade[..., None], 3, -1), os.path.join(out, 'fade.png'))
    elif os.path.isfile(os.path.join(out, 'fade.png')):
        os.remove(os.path.join(out, 'fade.png'))
    save_rgb(raw, os.path.join(out, 'target_raw.png'))
    save_rgb(T, os.path.join(out, 'target.png'))
    pal, info = build_palette(T, preset, focus, ref, frame)
    layout = make_canvas(W, H, pal, os.path.join(out, 'canvas.png'))
    if face_box is None and focus:
        cx, cy, rx, ry = focus[0]
        face_box = [cx - rx * 1.15, cy - ry * 1.15, cx + rx * 1.15, cy + ry * 1.15]
    meta = dict(source=os.path.abspath(source), W=W, H=H, preset=preset.get('name'), layout=layout,
                palette=[[round(float(v), 5) for v in c] for c in pal], palette_info=info, frame=bool(frame),
                focus=focus or [], face_box=face_box, reference=os.path.abspath(reference) if reference else None)
    with open(os.path.join(out, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    with open(os.path.join(out, 'preset.json'), 'w') as f:
        json.dump(preset, f, indent=1)
    if os.path.abspath(source) != os.path.abspath(os.path.join(out, os.path.basename(source))):
        shutil.copy(source, os.path.join(out, 'source' + os.path.splitext(source)[1]))
    return meta
