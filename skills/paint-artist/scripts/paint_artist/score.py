"""Honest scoring: crop the painted drawing area and the full-size target IDENTICALLY (inset inside the frame),
then mean CIE76 Lab dE overall / focus (face box) / rest. Never resize the whole source to a crop's size: that
misaligns everything by the crop offset.

Screen grab: ffmpeg -f gdigrab -draw_mouse 0 -i desktop -frames:v 1 grab.png   (option order matters: input options before -i; Windows)
"""
import json
import os
import subprocess

import numpy as np

from . import color as col
from .prepare import load_rgb


def scores(img, target, face_box=None, inset=16):
    """img, target: HxWx3 drawing-area arrays of the same size. face_box: [x0,y0,x1,y1] fractions or None."""
    H, W = target.shape[:2]
    assert img.shape[:2] == (H, W), (img.shape, target.shape)
    d = np.linalg.norm(col.rgb2lab(img) - col.rgb2lab(target), axis=-1)
    m = np.zeros((H, W), bool)
    m[inset:H - inset, inset:W - inset] = True
    out = {'all': float(d[m].mean()), 'inset': inset}
    if face_box:
        f = np.zeros((H, W), bool)
        x0, y0, x1, y1 = face_box
        f[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = True
        out['face'] = float(d[f & m].mean()) if (f & m).any() else None
        out['rest'] = float(d[~f & m].mean())
    else:
        out['face'] = None
    return out


def grab(path):
    """Full-desktop screenshot with ffmpeg gdigrab (Windows). Returns path."""
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'gdigrab', '-draw_mouse', '0', '-i', 'desktop', '-frames:v', '1', path], check=True)
    return path


def crop_drawing(grab_rgb, origin, meta, scale=1.0):
    """Cut the drawing area out of a screen grab, given the canvas origin on screen (top-left of the canvas)."""
    from PIL import Image
    ox, oy = meta['layout']['draw_origin']
    W, H = meta['W'], meta['H']
    x0, y0 = origin[0] + ox * scale, origin[1] + oy * scale
    if abs(scale - 1) < 1e-6:
        return grab_rgb[int(round(y0)):int(round(y0)) + H, int(round(x0)):int(round(x0)) + W]
    im = Image.fromarray((grab_rgb * 255).astype(np.uint8)).crop((x0, y0, x0 + W * scale, y0 + H * scale))
    return np.asarray(im.resize((W, H), Image.LANCZOS)).astype(float) / 255


def score_job(job, painted, vs='raw'):
    with open(os.path.join(job, 'meta.json')) as f:
        meta = json.load(f)
    tgt = load_rgb(os.path.join(job, 'target_raw.png' if vs == 'raw' else 'target.png'))
    return scores(painted, tgt, meta.get('face_box'))
