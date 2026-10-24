"""Fresh compositions without a source image: a tiny scene language rendered with numpy/PIL into a reference
PNG (shapes, gradients, sphere lighting, reflections, texture), which then goes through a style preset.

Scene JSON:
{ "size": [W, H],
  "background": {"stops": [[0, "#1b2a4a"], [0.55, "#f2a65a"], [1, "#2d3b2f"]]},      vertical gradient
  "shapes": [ {"type": "ellipse"|"rect"|"polygon", "box": [x0,y0,x1,y1] | "points": [[x,y],...]  (0..1 fractions),
               "fill": "#hex", "to": "#hex" (optional linear gradient), "dir": [dx,dy],
               "sphere": {"light": [lx,ly,lz], "ambient": 0.35, "spec": 0.4}  (shaded volume),
               "glow": 0.0 (soft halo radius as fraction), "blur": 0 (px), "alpha": 1.0 },
              {"type": "reflection", "y": 0.62, "strength": 0.55, "ripple": 3},
              {"type": "noise", "amount": 0.025, "scale": 2} ] }
Built-in scenes: landscape, still_life, portrait. Write your own JSON for anything else.
"""
import json
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi

from .color import as_rgb


def _grad_bg(W, H, stops):
    ys = np.linspace(0, 1, H)
    pos = [s[0] for s in stops]
    cols = np.array([as_rgb(s[1]) for s in stops])
    out = np.stack([np.interp(ys, pos, cols[:, c]) for c in range(3)], -1)
    return np.repeat(out[:, None, :], W, 1)


def _mask(W, H, sh):
    m = Image.new('L', (W * 2, H * 2), 0)
    d = ImageDraw.Draw(m)
    if sh['type'] in ('ellipse', 'rect'):
        x0, y0, x1, y1 = sh['box']
        box = [x0 * W * 2, y0 * H * 2, x1 * W * 2, y1 * H * 2]
        (d.ellipse if sh['type'] == 'ellipse' else d.rectangle)(box, fill=255)
    else:
        d.polygon([(x * W * 2, y * H * 2) for x, y in sh['points']], fill=255)
    m = m.resize((W, H), Image.LANCZOS)
    if sh.get('blur'):
        m = m.filter(ImageFilter.GaussianBlur(sh['blur']))
    return np.asarray(m).astype(float) / 255


def render_scene(scene):
    W, H = scene['size']
    img = _grad_bg(W, H, scene['background']['stops'])
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    for sh in scene['shapes']:
        t = sh['type']
        if t == 'reflection':
            y0 = int(sh['y'] * H)
            n = H - y0
            src = img[max(0, y0 - n):y0][::-1]
            ripple = sh.get('ripple', 3)
            rows = np.arange(len(src))
            shift = (np.sin(rows / 2.3) * ripple * (rows / max(1, len(src)) + 0.2)).astype(int)
            ref = np.stack([np.roll(src[i], shift[i], axis=0) for i in range(len(src))])
            k = sh.get('strength', 0.55)
            water = np.asarray(as_rgb(sh.get('water', '#2b4f6e')))
            ref = (1 - sh.get('water_mix', 0.3)) * ref * sh.get('tint', 0.9) + sh.get('water_mix', 0.3) * water
            img[y0:y0 + len(ref)] = k * ref + (1 - k) * img[y0:y0 + len(ref)]
            continue
        if t == 'noise':
            rng = np.random.default_rng(sh.get('seed', 0))
            nz = ndi.gaussian_filter(rng.normal(0, 1, (H, W)), sh.get('scale', 2))
            nz /= nz.std() + 1e-9
            img = np.clip(img + nz[..., None] * sh.get('amount', 0.025), 0, 1)
            continue
        m = _mask(W, H, sh)
        c0 = as_rgb(sh['fill'])
        col = np.ones((H, W, 3)) * c0
        if sh.get('to'):
            dx, dy = sh.get('dir', [0, 1])
            ys, xs = np.nonzero(m > 0.5)
            if len(xs):
                p = (xx * dx + yy * dy)
                lo, hi = (xs * dx + ys * dy).min(), (xs * dx + ys * dy).max()
                tt = np.clip((p - lo) / max(1e-6, hi - lo), 0, 1)[..., None]
                col = (1 - tt) * c0 + tt * as_rgb(sh['to'])
        if sh.get('sphere') and t != 'polygon':
            x0, y0, x1, y1 = sh['box']
            cx, cy, rx, ry = (x0 + x1) / 2 * W, (y0 + y1) / 2 * H, (x1 - x0) / 2 * W, (y1 - y0) / 2 * H
            u, v = (xx - cx) / rx, (yy - cy) / ry
            r2 = np.clip(u * u + v * v, 0, 1)
            nz_ = np.sqrt(1 - r2)
            L = np.array(sh['sphere'].get('light', [-0.5, -0.6, 0.65]), float)
            L /= np.linalg.norm(L)
            diff = np.clip(u * L[0] + v * L[1] + nz_ * L[2], 0, 1)
            amb = sh['sphere'].get('ambient', 0.35)
            spec = sh['sphere'].get('spec', 0.35) * diff ** 24
            col = col * (amb + (1 - amb) * diff)[..., None] + spec[..., None]
        if sh.get('glow'):
            g = ndi.gaussian_filter(m, sh['glow'] * max(W, H))
            img = img + (1 - img) * (g[..., None] * np.asarray(c0)) * 0.9
        a = m[..., None] * sh.get('alpha', 1.0)
        img = a * np.clip(col, 0, 1) + (1 - a) * img
    return np.clip(img, 0, 1)


SCENES = {
    'landscape': {
        'size': [450, 600],
        'background': {'stops': [[0, '#24315e'], [0.30, '#7d5a8c'], [0.50, '#f2a65a'], [0.60, '#f7d08a'], [1.0, '#2c4a5a']]},
        'shapes': [
            {'type': 'ellipse', 'box': [0.56, 0.40, 0.76, 0.55], 'fill': '#fff1c4', 'glow': 0.06},
            {'type': 'polygon', 'points': [[0, 0.60], [0.10, 0.42], [0.22, 0.50], [0.36, 0.36], [0.52, 0.52], [0.62, 0.46], [0.80, 0.55], [1, 0.44], [1, 0.60]],
             'fill': '#4a4f7a', 'to': '#2e3352', 'dir': [0, 1]},
            {'type': 'polygon', 'points': [[0, 0.60], [0.15, 0.52], [0.30, 0.57], [0.45, 0.53], [0.70, 0.59], [0.85, 0.55], [1, 0.58], [1, 0.62], [0, 0.62]],
             'fill': '#2f3d3a'},
            {'type': 'reflection', 'y': 0.62, 'strength': 0.85, 'ripple': 4, 'water_mix': 0.25},
            {'type': 'polygon', 'points': [[0, 0.78], [0.20, 0.74], [0.45, 0.80], [0.70, 0.76], [1, 0.82], [1, 1], [0, 1]],
             'fill': '#3f5a2c', 'to': '#1f2e17', 'dir': [0, 1]},
            {'type': 'ellipse', 'box': [0.03, 0.55, 0.23, 0.80], 'fill': '#2d4a22', 'sphere': {'light': [0.6, -0.6, 0.5], 'ambient': 0.45}},
            {'type': 'rect', 'box': [0.12, 0.76, 0.14, 0.86], 'fill': '#3b2a1c'},
            {'type': 'ellipse', 'box': [0.80, 0.62, 0.98, 0.86], 'fill': '#35552a', 'sphere': {'light': [-0.6, -0.6, 0.5], 'ambient': 0.45}},
            {'type': 'rect', 'box': [0.885, 0.84, 0.905, 0.92], 'fill': '#3b2a1c'},
            {'type': 'noise', 'amount': 0.02, 'scale': 1.5},
        ]},
    'still_life': {
        'size': [450, 560],
        'background': {'stops': [[0, '#3b2f2a'], [0.62, '#5a4636'], [0.63, '#7a5636'], [1, '#4a3322']]},
        'shapes': [
            {'type': 'rect', 'box': [0.0, 0.63, 1.0, 1.0], 'fill': '#8a6a48', 'to': '#4a3322', 'dir': [0, 1]},
            {'type': 'ellipse', 'box': [0.30, 0.22, 0.62, 0.70], 'fill': '#3d6e9e', 'sphere': {'light': [-0.6, -0.5, 0.6], 'ambient': 0.25, 'spec': 0.6}},
            {'type': 'rect', 'box': [0.40, 0.12, 0.52, 0.26], 'fill': '#35628c', 'to': '#1d3a57', 'dir': [1, 0]},
            {'type': 'ellipse', 'box': [0.10, 0.58, 0.32, 0.76], 'fill': '#d8452c', 'sphere': {'light': [-0.6, -0.5, 0.6], 'ambient': 0.25, 'spec': 0.5}},
            {'type': 'ellipse', 'box': [0.58, 0.60, 0.78, 0.77], 'fill': '#e3b23c', 'sphere': {'light': [-0.6, -0.5, 0.6], 'ambient': 0.25, 'spec': 0.5}},
            {'type': 'ellipse', 'box': [0.72, 0.64, 0.90, 0.79], 'fill': '#6f9a3a', 'sphere': {'light': [-0.6, -0.5, 0.6], 'ambient': 0.25, 'spec': 0.4}},
            {'type': 'polygon', 'points': [[0.05, 0.80], [0.95, 0.80], [0.92, 0.86], [0.08, 0.86]], 'fill': '#efe6d6', 'alpha': 0.85},
            {'type': 'noise', 'amount': 0.02, 'scale': 1.5},
        ]},
    'portrait': {
        'size': [450, 600],
        'background': {'stops': [[0, '#2e3d4f'], [1, '#141a22']]},
        'shapes': [
            {'type': 'ellipse', 'box': [0.10, 0.66, 0.90, 1.25], 'fill': '#7a2d2d', 'sphere': {'light': [-0.5, -0.6, 0.6], 'ambient': 0.3}},
            {'type': 'rect', 'box': [0.42, 0.52, 0.58, 0.70], 'fill': '#d9a27e', 'to': '#a8705a', 'dir': [1, 0]},
            {'type': 'ellipse', 'box': [0.31, 0.20, 0.69, 0.60], 'fill': '#e6b494', 'sphere': {'light': [-0.55, -0.45, 0.7], 'ambient': 0.35, 'spec': 0.2}},
            {'type': 'ellipse', 'box': [0.27, 0.12, 0.73, 0.40], 'fill': '#3a2418', 'alpha': 0.95},
            {'type': 'ellipse', 'box': [0.39, 0.36, 0.46, 0.40], 'fill': '#2a1c16'},
            {'type': 'ellipse', 'box': [0.54, 0.36, 0.61, 0.40], 'fill': '#2a1c16'},
            {'type': 'ellipse', 'box': [0.44, 0.49, 0.56, 0.52], 'fill': '#a8524a'},
            {'type': 'noise', 'amount': 0.015, 'scale': 1.5},
        ],
        'focus': [[0.5, 0.40, 0.17, 0.19]]},
}


def compose(scene, out, width=None, height=None):
    if isinstance(scene, str):
        if scene in SCENES:
            scene = json.loads(json.dumps(SCENES[scene]))
        else:
            with open(scene) as f:
                scene = json.load(f)
    if width or height:
        W0, H0 = scene['size']
        W = int(width or round(W0 * height / H0))
        H = int(height or round(H0 * width / W0))
        scene['size'] = [W, H]
    img = render_scene(scene)
    Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(out)
    return scene.get('focus')
