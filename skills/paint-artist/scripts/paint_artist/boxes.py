"""Boxes: one picture split into R x C boxes, each painted as its OWN full painting on a standard canvas (540x690,
drawing area 450x672, same screen position for every box), then assembled into one big image.

prepare: for each box, the box's region of the high-resolution source plus `bleed` source pixels of the
         neighbouring area on every interior side is resized to the 450x672 drawing area (no frame) and prepared
         with the box's style; boxes.json records the tile rectangle (the box without the bleed) inside the drawing
         area. Planning on the bleed means the strokes run past the box edge, so the tile edges are fully painted.
plan:    each box is planned as a normal job, capped by the corrected time model (default 480 s per box).
emit:    one plan per box (pa_box_<style>.json), a canvas copy per box to open in Paint (pa_box_<style>.png).
assemble: the saved box PNGs (or the simulations with --sim) -> drawing areas -> tiles (bleed cropped, resized to
         exact box size) -> one R*450 x C*672 image, + dark dividers + the frame: assembled.png and
         assembled_nodividers.png.
"""
import json
import os
import shutil

import numpy as np
from PIL import Image, ImageDraw

from . import prepare as pr

BOX_W, BOX_H = 450, 672


def prepare_boxes(src, job, styles, rows, cols, load_style, bleed=8, overrides=None, focus=None):
    os.makedirs(job, exist_ok=True)
    im = Image.open(src).convert('RGB')
    SW, SH = im.size
    boxes = []
    for i, st in enumerate(styles):
        r, c = divmod(i, cols)
        x0, x1 = c * SW / cols, (c + 1) * SW / cols
        y0, y1 = r * SH / rows, (r + 1) * SH / rows
        bl = bleed if c > 0 else 0
        br = bleed if c < cols - 1 else 0
        bt = bleed if r > 0 else 0
        bb = bleed if r < rows - 1 else 0
        crop = (x0 - bl, y0 - bt, x1 + br, y1 + bb)
        sx, sy = BOX_W / (crop[2] - crop[0]), BOX_H / (crop[3] - crop[1])
        tile = [bl * sx, bt * sy, BOX_W - br * sx, BOX_H - bb * sy]           # the box itself, in drawing px
        name = os.path.splitext(os.path.basename(st))[0]
        sub = os.path.join(job, 'box%d_%s' % (i, name))
        os.makedirs(sub, exist_ok=True)
        src_crop = os.path.join(sub, 'box_source.png')
        im.crop(tuple(int(round(v)) for v in crop)).save(src_crop)
        preset = load_style(st)
        if overrides and str(i) in overrides:
            from .grid import deep_update
            preset = deep_update(preset, overrides[str(i)])
        # focus ellipses in box coordinates (only those whose centre falls in the box crop)
        bfocus = []
        for fx, fy, rx, ry in (focus or []):
            px, py = fx * SW, fy * SH
            if crop[0] <= px <= crop[2] and crop[1] <= py <= crop[3]:
                bfocus.append([(px - crop[0]) / (crop[2] - crop[0]), (py - crop[1]) / (crop[3] - crop[1]),
                               rx * SW / (crop[2] - crop[0]), ry * SH / (crop[3] - crop[1])])
        pr.prepare(src_crop, sub, preset, BOX_W, BOX_H, 'stretch', bfocus or None, None, None, False, False)
        boxes.append({'index': i, 'row': r, 'col': c, 'style': preset.get('name', name), 'job': os.path.relpath(sub, job),
                      'source_rect': [round(v, 2) for v in (x0, y0, x1, y1)], 'crop_with_bleed': [round(v, 2) for v in crop],
                      'tile_in_drawing_px': [round(v, 2) for v in tile], 'canvas_file': 'pa_box_%s.png' % name,
                      'plan_file': 'pa_box_%s.json' % name})
    meta = {'boxes': boxes, 'rows': rows, 'cols': cols, 'bleed': bleed, 'source': os.path.abspath(src),
            'assembled_size': [cols * BOX_W, rows * BOX_H]}
    with open(os.path.join(job, 'boxes.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    return meta


def tile_from_canvas(img, box, layout):
    """Crop the drawing area of a saved / simulated box canvas, then the tile (bleed removed), resize to box size."""
    ox, oy = layout['draw_origin']
    a = img.crop((ox, oy, ox + BOX_W, oy + BOX_H))
    t = box['tile_in_drawing_px']
    a = a.crop((t[0], t[1], t[2], t[3]))
    return a.resize((BOX_W, BOX_H), Image.LANCZOS)


def assemble(job, files=None, sim=False, divider=5, divider_color=(26, 26, 26), margin=34):
    with open(os.path.join(job, 'boxes.json')) as f:
        B = json.load(f)
    W, H = B['assembled_size']
    big = Image.new('RGB', (W, H), 'white')
    for b in B['boxes']:
        sub = os.path.join(job, b['job'])
        with open(os.path.join(sub, 'meta.json')) as f:
            layout = json.load(f)['layout']
        if sim:
            path = os.path.join(sub, 'sim_canvas.png')
        else:
            path = (files or {}).get(str(b['index'])) or os.path.join(job, b['canvas_file'])
        tile = tile_from_canvas(Image.open(path).convert('RGB'), b, layout)
        big.paste(tile, (b['col'] * BOX_W, b['row'] * BOX_H))
    out = {}
    for name, with_div in (('assembled_nodividers', False), ('assembled', True)):
        img = big.copy()
        d = ImageDraw.Draw(img)
        if with_div:
            for c in range(1, B['cols']):
                x = c * BOX_W
                d.rectangle([x - divider // 2, 0, x - divider // 2 + divider - 1, H], fill=divider_color)
            for r in range(1, B['rows']):
                y = r * BOX_H
                d.rectangle([0, y - divider // 2, W, y - divider // 2 + divider - 1], fill=divider_color)
        framed = frame(img, margin)
        p = os.path.join(job, name + ('_sim' if sim else '') + '.png')
        framed.save(p)
        out[name] = p
    return out


def frame(img, m):
    """A painted-look frame like the canvas runs: walnut band, gold fillet, dark inner line."""
    W, H = img.size
    out = Image.new('RGB', (W + 2 * m, H + 2 * m), (61, 38, 26))
    out.paste(img, (m, m))
    d = ImageDraw.Draw(out)
    walnut, gold, dark = (61, 38, 26), (204, 163, 82), (13, 8, 20)
    d.rectangle([m - 4, m - 4, W + m + 3, H + m + 3], outline=gold, width=3)
    d.rectangle([m - 1, m - 1, W + m, H + m], outline=dark, width=2)
    return out
