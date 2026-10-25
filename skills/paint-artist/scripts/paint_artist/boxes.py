"""Boxes: one picture split into R x C boxes, each painted as its OWN full painting on a standard canvas (540x690,
drawing area 450x672, same screen position for every box), then assembled into one big image.

prepare: the source (optionally cut to --crop x0,y0,x1,y1 source px) is fitted to the assembled aspect
         (C*450 : R*672): --fit crop takes the largest window of that aspect, centred, or placed so that the source
         point --split-at x,y lands exactly on the middle vertical / horizontal divider (the window shrinks if it has
         to); --fit stretch keeps the whole region. For each box, the box's part of the window plus `bleed` drawing
         px of the neighbouring area on every interior side is resized to the 450x672 drawing area (no frame) and
         prepared with the box's style. Focus ellipses (fractions of the window, i.e. of the assembled picture) go
         into EVERY box they overlap, so a face on the split gets detail on both sides. boxes.json records the
         window, the tile rectangle (the box without the bleed) inside the drawing area and the file names
         pa_<name>_<style>[_<index>].png / .json.
plan:    each box is planned as a normal job, capped by the corrected time model (default 480 s per box); per-box
         detail and seconds from the overrides ("plan": {"detail", "seconds"}) or --box-detail / --box-seconds.
emit:    one plan per box (pa_<name>_<style>.json), a canvas copy per box to open in Paint (pa_<name>_<style>.png),
         boxes.json and job_card.json (the canonical card the video and batch scripts read).
assemble: the saved box PNGs (or the simulations with --sim) -> drawing areas -> tiles (bleed cropped, resized to
         exact box size) -> one C*450 x R*672 image, + dark dividers + the frame: assembled.png and
         assembled_nodividers.png.
"""
import json
import os
import re

from PIL import Image, ImageDraw

from . import prepare as pr

BOX_W, BOX_H = 450, 672


def norm_prefix(name):
    """--name ermine / pa_ermine / 'pa_ermine_' -> 'ermine' (files are pa_<prefix>_<style>)."""
    p = re.sub(r'[^A-Za-z0-9_-]+', '_', str(name or 'box').strip()).strip('_')
    if p.startswith('pa_'):
        p = p[3:]
    return p or 'box'


def assign_names(boxes, prefix):
    """plan_file / canvas_file / window_title per box: pa_<prefix>_<style>, + _<index> when a style repeats."""
    prefix = norm_prefix(prefix)
    keys = [b.get('name_key') or b['style'] for b in boxes]
    for b, k in zip(boxes, keys):
        stem = 'pa_%s_%s' % (prefix, k) + ('_%d' % b['index'] if keys.count(k) > 1 else '')
        b.update(plan_file=stem + '.json', canvas_file=stem + '.png', window_title=stem + '.png - Paint')
    return boxes


def fit_window(size, rows, cols, fit='crop', crop=None, split_at=None):
    """The source window (x0, y0, x1, y1, source px) painted by the boxes. crop: region of the source to use;
    fit crop: the largest window of the assembled aspect inside it, centred, or with the source point split_at
    (x, y; either may be None) exactly on the middle divider (column cols//2, row rows//2); stretch: the region."""
    SW, SH = size
    R = [0.0, 0.0, float(SW), float(SH)] if not crop else [float(v) for v in crop]
    R = [max(0.0, R[0]), max(0.0, R[1]), min(float(SW), R[2]), min(float(SH), R[3])]
    if R[2] - R[0] < 8 or R[3] - R[1] < 8:
        raise SystemExit('--crop %s leaves no source area (source is %dx%d)' % (crop, SW, SH))
    sx, sy = (list(split_at) + [None, None])[:2] if split_at else (None, None)
    if fit == 'stretch' and sx is None and sy is None:
        return R
    A = cols * BOX_W / (rows * BOX_H)
    Rw, Rh = R[2] - R[0], R[3] - R[1]
    fx = (cols // 2) / cols if cols > 1 else None
    fy = (rows // 2) / rows if rows > 1 else None
    Wd = min(Rw, Rh * A)
    for v, f, lo, hi, k in ((sx, fx, R[0], R[2], 1.0), (sy, fy, R[1], R[3], A)):
        if v is None or f is None:
            continue
        if not lo < v < hi:
            raise SystemExit('--split-at point %.0f is outside the source region %.0f..%.0f' % (v, lo, hi))
        Wd = min(Wd, (v - lo) / f * k, (hi - v) / (1 - f) * k)
    Hd = Wd / A
    x0 = sx - fx * Wd if (sx is not None and fx is not None) else R[0] + (Rw - Wd) / 2
    y0 = sy - fy * Hd if (sy is not None and fy is not None) else R[1] + (Rh - Hd) / 2
    return [x0, y0, x0 + Wd, y0 + Hd]


def focus_for_box(focus, win_w, win_h, crop, box=None):
    """Focus ellipses (fractions of the window) that overlap the box (window px; default the crop), in fractions of
    the box crop (window px, the box plus its bleed), in their original order (the first one is the box's face:
    finest detail, score box)."""
    out = []
    cx0, cy0, cx1, cy1 = crop
    bx0, by0, bx1, by1 = box or crop
    cw, ch = cx1 - cx0, cy1 - cy0
    for fx, fy, rx, ry in (focus or []):
        px, py, qx, qy = fx * win_w, fy * win_h, max(1e-6, rx * win_w), max(1e-6, ry * win_h)
        dx = max(bx0 - px, 0.0, px - bx1) / qx
        dy = max(by0 - py, 0.0, py - by1) / qy
        if dx * dx + dy * dy < 1:                  # the ellipse reaches into the box
            out.append([round((px - cx0) / cw, 5), round((py - cy0) / ch, 5), round(qx / cw, 5), round(qy / ch, 5)])
    return out


def prepare_boxes(src, job, styles, rows, cols, load_style, bleed=8, overrides=None, focus=None, fit='crop',
                  crop=None, split_at=None, name='box'):
    """bleed: drawing px planned past every interior box edge. focus: [cx, cy, rx, ry] fractions of the window."""
    from .grid import deep_update
    os.makedirs(job, exist_ok=True)
    im = Image.open(src).convert('RGB')
    win = fit_window(im.size, rows, cols, fit, crop, split_at)
    WX0, WY0, WX1, WY1 = win
    Wd, Hd = WX1 - WX0, WY1 - WY0
    bw, bh = Wd / cols, Hd / rows                                    # one box in source px
    bx_, by_ = bleed * bw / BOX_W, bleed * bh / BOX_H                # the bleed in source px
    boxes = []
    for i, st in enumerate(styles):
        r, c = divmod(i, cols)
        x0, x1 = WX0 + c * bw, WX0 + (c + 1) * bw
        y0, y1 = WY0 + r * bh, WY0 + (r + 1) * bh
        bl = bx_ if c > 0 else 0
        br = bx_ if c < cols - 1 else 0
        bt = by_ if r > 0 else 0
        bb = by_ if r < rows - 1 else 0
        cr = (x0 - bl, y0 - bt, x1 + br, y1 + bb)
        cw, ch = cr[2] - cr[0], cr[3] - cr[1]
        sx, sy = BOX_W / cw, BOX_H / ch
        tile = [bl * sx, bt * sy, BOX_W - br * sx, BOX_H - bb * sy]           # the box itself, in drawing px
        key = os.path.splitext(os.path.basename(st))[0]
        sub = os.path.join(job, 'box%d_%s' % (i, key))
        os.makedirs(sub, exist_ok=True)
        src_crop = os.path.join(sub, 'box_source.png')
        im.resize((max(1, int(round(cw))), max(1, int(round(ch)))), Image.LANCZOS, box=cr).save(src_crop)
        preset = load_style(st)
        ov = dict((overrides or {}).get(str(i)) or {})
        plan_opts = ov.pop('plan', None) or {}
        if ov:
            preset = deep_update(preset, ov)
        bfocus = focus_for_box(focus, Wd, Hd, (cr[0] - WX0, cr[1] - WY0, cr[2] - WX0, cr[3] - WY0),
                               (x0 - WX0, y0 - WY0, x1 - WX0, y1 - WY0))
        face_box = None
        if bfocus:                                  # the face box of the first focus, clamped to the box
            fcx, fcy, frx, fry = bfocus[0]
            face_box = [round(min(1.0, max(0.0, v)), 5) for v in
                        (fcx - frx * 1.15, fcy - fry * 1.15, fcx + frx * 1.15, fcy + fry * 1.15)]
            if face_box[2] - face_box[0] < 0.02 or face_box[3] - face_box[1] < 0.02:
                face_box = None
        pr.prepare(src_crop, sub, preset, BOX_W, BOX_H, 'stretch', bfocus or None, face_box, None, False, False)
        b = {'index': i, 'row': r, 'col': c, 'style': preset.get('name', key), 'name_key': key,
             'job': os.path.relpath(sub, job),
             'source_rect': [round(v, 2) for v in (x0, y0, x1, y1)], 'crop_with_bleed': [round(v, 2) for v in cr],
             'tile_in_drawing_px': [round(v, 2) for v in tile], 'focus': bfocus}
        if plan_opts:
            b['plan_opts'] = {k: plan_opts[k] for k in ('detail', 'seconds') if k in plan_opts}
        boxes.append(b)
    assign_names(boxes, name)
    meta = {'boxes': boxes, 'rows': rows, 'cols': cols, 'bleed': bleed, 'source': os.path.abspath(src),
            'source_size': list(im.size), 'name': norm_prefix(name), 'fit': fit,
            'crop_src_px': [round(float(v), 2) for v in crop] if crop else None,
            'window_src_px': [round(v, 2) for v in win], 'focus': focus or [],
            'assembled_size': [cols * BOX_W, rows * BOX_H]}
    if split_at:
        sx, sy = (list(split_at) + [None, None])[:2]
        meta['split_at_src_px'] = [sx, sy]
        meta['split_at_window_frac'] = [None if sx is None else round((sx - WX0) / Wd, 4),
                                        None if sy is None else round((sy - WY0) / Hd, 4)]
    with open(os.path.join(job, 'boxes.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    return meta


# ------------------------------------------------------------------------------------------- job card
POS2 = {(0, 0): 'TL', (0, 1): 'TR', (1, 0): 'BL', (1, 1): 'BR'}
PRETTY = {'master': 'Master', 'pop-art': 'Pop art', 'van-gogh': 'Van Gogh', 'ukiyo-e': 'Ukiyo-e',
          'pencil-sketch': 'Pencil', 'stained-glass': 'Stained glass', 'pixel-art': 'Pixel art', 'sumi-e': 'Sumi-e'}


def card_labels(card, boxes):
    """Box labels from a job card: canonical boxes[].label, else the older shapes agents wrote by hand
    (plans[].label in box order, or styles{TL,TR,BL,BR}.label for 2x2). Returns {index: label}."""
    out = {}
    if not isinstance(card, dict):
        return out
    if isinstance(card.get('boxes'), list):
        for j, e in enumerate(card['boxes']):
            if isinstance(e, dict) and e.get('label'):
                out[int(e.get('index', j))] = e['label']
    if not out and isinstance(card.get('plans'), list):
        for j, e in enumerate(card['plans']):
            if isinstance(e, dict) and e.get('label'):
                out[e['box'] if isinstance(e.get('box'), int) else int(e.get('index', j))] = e['label']
    if not out and isinstance(card.get('styles'), dict):
        for b in boxes:
            e = card['styles'].get(POS2.get((b['row'], b['col']), ''))
            if isinstance(e, dict) and e.get('label'):
                out[b['index']] = e['label']
    return out


def default_label(style, artist=None):
    if style == 'master' and artist:
        return artist
    return PRETTY.get(style, style.replace('-', ' ').capitalize())


def job_card(job, B, prev=None, slug=None, title=None, artist=None, year=None, source_url=None, labels=None):
    """The canonical job card of a boxes job, written by emit (schema in references/grid.md). Values not given
    are kept from the previous card (any older shape), so re-emitting after locate keeps title and labels."""
    prev = prev if isinstance(prev, dict) else {}
    old = card_labels(prev, B['boxes'])
    artist = artist or prev.get('artist')
    boxes = []
    for b in B['boxes']:
        i = b['index']
        lab = (labels[i] if labels and i < len(labels) and labels[i] else None) or old.get(i) or default_label(b['style'], artist)
        boxes.append({'index': i, 'row': b['row'], 'col': b['col'], 'style': b['style'], 'label': lab,
                      'plan_file': b['plan_file'], 'canvas_file': b['canvas_file'],
                      'window_title': b.get('window_title') or b['canvas_file'] + ' - Paint',
                      'est_seconds': b.get('est_seconds'), 'est_seconds_unrecorded': b.get('est_seconds_unrecorded'),
                      'strokes': b.get('strokes'), 'steps': b.get('batch_steps'), 'detail': b.get('detail')})
    card = {'version': 1, 'slug': slug or prev.get('slug') or B.get('name'),
            'title': title or prev.get('title'), 'artist': artist, 'year': year or prev.get('year'),
            'source_url': source_url or prev.get('source_url'),
            'mode': 'boxes %dx%d' % (B['rows'], B['cols']), 'rows': B['rows'], 'cols': B['cols'],
            'source': B.get('source'), 'window_src_px': B.get('window_src_px'),
            'boxes': boxes,
            'est_total_seconds': sum(x['est_seconds'] or 0 for x in boxes),
            'est_total_seconds_unrecorded': sum(x['est_seconds_unrecorded'] or 0 for x in boxes),
            'total_strokes': sum(x['strokes'] or 0 for x in boxes),
            'total_steps': sum(x['steps'] or 0 for x in boxes),
            'timing_profile': B.get('timing_profile'),
            'canvas_origin': B['boxes'][0].get('canvas_origin') if B['boxes'] else None,
            'plans_dir': B.get('plans_dir'),
            'preview': os.path.join(job, 'assembled_sim.png'),
            'preview_nodividers': os.path.join(job, 'assembled_nodividers_sim.png')}
    if prev.get('notes'):
        card['notes'] = prev['notes']
    return card


# ------------------------------------------------------------------------------------------- assemble
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
