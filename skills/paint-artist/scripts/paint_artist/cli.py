"""paint-artist command line. Run from the skill's scripts/ folder:  python -m paint_artist <command> ...

  compose  SCENE|scene.json --out ref.png            render a fresh composition (landscape, still_life, portrait)
  analyse  REF.png --out style.json [--base STYLE]    derive a style preset from a reference painting
  prepare  SRC|--subject mona_lisa --job DIR --style STYLE|preset.json   target.png, palette, canvas.png, meta.json
           [--height 672] [--width W] [--fit crop|stretch] [--focus cx,cy,rx,ry ...] [--face-box x0,y0,x1,y1]
           [--reference REF --transfer] [--no-frame]
  plan     --job DIR [--detail 1.0] [--budget N] [--seconds 480] [--profile recorded|unrecorded] [--seed 0]   plan.json + sim + preview
  preview  --job DIR [--ui ui.json]                   estimate (time, steps) and preview.png without emitting
  emit     --job DIR --name NAME [--ui ui.json]       write ~/.melaya/plans/NAME.json (the one batch call)
  locate   --job DIR --grab grab.png [--write-ui]     find the canvas on a screenshot (origin, DPI scale, swatch check)
  score    --job DIR [--file saved.png | --grab grab.png | --take]   live vs sim and vs source, Lab dE all/face/rest
  calib-plan --job DIR --name NAME / calib-measure --job DIR --grab grab.png      re-measure tool darkness
  speed-calib --job DIR [--name pa_speed] / speed-measure --job DIR --take --times t0,..,t4 [--install]   fastest safe speeds
  make     SRC --job DIR --style STYLE --name NAME    prepare + plan + emit in one go
  assemble --job DIR [--sim] [--file 0=box0.png ...]  boxes: tile the saved boxes (+ dividers, frame)
  contact  --out sheet.png JOB [JOB ...]              contact sheet of sim previews (labels = style names)
"""
import argparse
import shutil
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import analyse as an
from . import compose as cp
from . import emit_paint as ep
from . import grid as gr
from . import boxes as bx
from . import speedcalib as spc
from . import planner as pl
from . import prepare as pr
from . import score as sc
from . import simulate as sim
from .locate import calib_size, calib_strokes, locate_canvas, measure_tools, tools_from_measure

PKG = os.path.dirname(os.path.abspath(__file__))


def winpath(p):
    """Accept Git Bash paths (/c/Users/...) as well as Windows ones; Windows Python cannot open /c/... ."""
    if isinstance(p, str) and os.name == 'nt' and len(p) > 2 and p[0] == '/' and p[2] == '/' and p[1].isalpha():
        return p[1].upper() + ':' + p[2:]
    return p


def hint(msg):
    """Human hints go to stderr, so stdout stays parseable JSON."""
    print(msg, file=sys.stderr)
SKILL = os.path.abspath(os.path.join(PKG, '..', '..'))
STYLES = os.path.join(SKILL, 'styles')
PLANS = os.path.expanduser('~/.melaya/plans')


def load_style(s):
    p = s if os.path.isfile(s) else os.path.join(STYLES, s + '.json')
    with open(p) as f:
        return json.load(f)


def floats(s):
    return [float(v) for v in s.split(',')]


def jload(p):
    with open(p) as f:
        return json.load(f)


def jsave(o, p, compact=False):
    with open(p, 'w') as f:
        json.dump(o, f, separators=(',', ':')) if compact else json.dump(o, f, indent=1)


def tools_for(job, path=None):
    for p in (path, os.path.join(job, 'tools.json')):
        if p and os.path.isfile(p):
            return sim.load_tools(p)
    return sim.load_tools()


PROFILE = [None]


def ui_for(job, path=None):
    ui = None
    for p in (path, os.path.join(job, 'ui.json')):
        if p and os.path.isfile(p):
            ui = ep.load_ui(p)
            break
    ui = ui or ep.load_ui()
    if PROFILE[0]:
        ui['timing_profile'] = PROFILE[0]
    return ui


# ------------------------------------------------------------------------------------------- commands
def cmd_compose(a):
    focus = cp.compose(a.scene, a.out, a.width, a.height)
    print(json.dumps({'out': a.out, 'focus': focus}))


def cmd_analyse(a):
    P, f = an.derive(a.ref, a.base, a.out)
    print(json.dumps({'base': P['derived_from']['base'], 'features': f, 'out': a.out}, indent=1))


def apply_subject(a):
    """--subject NAME: source, size, fit, focus and face box from assets/subjects/subjects.json (explicit flags win)."""
    if not getattr(a, 'subject', None):
        if not a.src:
            raise SystemExit('give a source image or --subject NAME')
        return
    subs = jload(os.path.join(SKILL, 'assets', 'subjects', 'subjects.json'))
    if a.subject not in subs:
        raise SystemExit('unknown subject %r; known: %s' % (a.subject, ', '.join(subs)))
    d = subs[a.subject]
    a.src = a.src or os.path.join(SKILL, d['file'])
    a.width = a.width or d.get('width')
    if a.height == 672 and d.get('height'):
        a.height = d['height']
    if d.get('fit') and a.fit == 'crop':
        a.fit = d['fit']
    if not a.focus and d.get('focus'):
        a.focus = [','.join(str(v) for v in f) for f in d['focus']]
    if not a.face_box and d.get('face_box'):
        a.face_box = ','.join(str(v) for v in d['face_box'])


def cmd_prepare(a):
    if getattr(a, 'boxes', None):
        rows, cols = gr.parse_grid(a.boxes)
        src = a.src
        focus = [floats(s) for s in a.focus] if a.focus else None
        if getattr(a, 'subject', None):
            subs = jload(os.path.join(SKILL, 'assets', 'subjects', 'subjects.json'))
            d = subs[a.subject]
            src = src or os.path.join(SKILL, d.get('file_hires') or d['file'])
            focus = focus or d.get('focus')
        styles = [winpath(s.strip()) for s in a.styles.split(',')]
        if len(styles) != rows * cols:
            raise SystemExit('--styles needs %d names for %s boxes' % (rows * cols, a.boxes))
        over = json.loads(a.cell_override) if a.cell_override else None
        m = bx.prepare_boxes(src, a.job, styles, rows, cols, load_style, a.bleed, over, focus)
        print(json.dumps({'job': a.job, 'boxes': [(b['index'], b['style'], b['job'], b['tile_in_drawing_px']) for b in m['boxes']],
                          'assembled_size': m['assembled_size']}))
        return
    apply_subject(a)
    if getattr(a, 'grid', None):
        styles = [winpath(s.strip()) for s in a.styles.split(',')]
        order = [int(v) for v in a.order.split(',')] if a.order else None
        over = json.loads(a.cell_override) if a.cell_override else None
        m = gr.prepare_grid(a.src, a.job, styles, a.grid, load_style, a.width, a.height, a.fit,
                            [floats(s) for s in a.focus] if a.focus else None, floats(a.face_box) if a.face_box else None,
                            order, a.divider_width, a.inset, a.divider_color, not a.no_frame, over,
                            floats(a.split_x) if a.split_x else None, floats(a.split_y) if a.split_y else None)
        print(json.dumps({'job': a.job, 'grid': '%dx%d' % (m['grid']['rows'], m['grid']['cols']), 'W': m['W'], 'H': m['H'],
                          'cells': [(c['index'], c['style'], c['rect']) for c in m['grid']['cells']],
                          'order': m['grid']['order'], 'note': 'canvas.png is written by plan'}))
        return
    preset = load_style(a.style)
    focus = [floats(s) for s in a.focus] if a.focus else None
    if focus is None and a.focus_from:
        focus = a.focus_from
    meta = pr.prepare(a.src, a.job, preset, a.width, a.height, a.fit, focus,
                      floats(a.face_box) if a.face_box else None, a.reference, not a.no_frame, a.transfer)
    print(json.dumps({'job': a.job, 'W': meta['W'], 'H': meta['H'], 'canvas': meta['layout']['canvas'],
                      'colours': len(meta['palette']), 'swatch_px': meta['layout']['strip']['swh'], 'frame': meta['frame']}))


def run_plan(job, detail, seed, log=None):
    preset = jload(os.path.join(job, 'preset.json'))
    return pl.plan(job, preset, tools_for(job), detail, seed, log=log)


def estimate(job, plan, ui=None):
    meta = jload(os.path.join(job, 'meta.json'))
    em = ep.Emitter(meta, ui or ui_for(job), tools_for(job))
    em.emit(plan)
    return em.estimate(), len(em.steps), em


def cmd_plan_grid(a):
    plan, full = gr.plan_grid(a.job, tools_for(a.job), a.detail, a.seed, log=hint)
    meta = jload(os.path.join(a.job, 'meta.json'))
    dry = gr.emit_grid(plan, meta, ui_for(a.job), tools_for(a.job), None, 'dry', a.seconds or 1e9, dry=True)
    _, nsteps, em = estimate(a.job, plan)
    plan['stats'].update({'est_seconds': dry['est_total_seconds'], 'batch_steps': nsteps, 'picks': em.n_picks})
    jsave(plan, os.path.join(a.job, 'plan.json'), compact=True)
    write_previews(a.job, full, plan)
    print(json.dumps({'strokes': plan['stats']['strokes'], 'batch_steps': nsteps, 'picks': em.n_picks,
                      'colours': plan['stats']['colours'], 'swatch_px': meta['layout']['strip']['swh'],
                      'est_total_seconds': dry['est_total_seconds'], 'one_plan': dry['one_plan'],
                      'cells': [{'index': c['index'], 'style': c['style'], 'est_start_s': c['segments'][0]['est_start_s'],
                                 'est_end_s': c['segments'][-1]['est_end_s'], **plan['cells'][c['index']]} for c in dry['cells']],
                      'preview': os.path.join(a.job, 'preview.png')}, indent=1))
    hint('grid: canvas.png was (re)written by plan: open THAT file in Paint. cell_vs_full_style_sim = each cell vs the '
         'same style simulated on the whole image (what clipping to the cell changed).')


def cmd_plan(a):
    if os.path.isfile(os.path.join(a.job, 'boxes.json')) and not os.path.isfile(os.path.join(a.job, 'meta.json')):
        B = jload(os.path.join(a.job, 'boxes.json'))
        summary = []
        for b in B['boxes']:
            a2 = argparse.Namespace(**vars(a))
            a2.job = os.path.join(a.job, b['job'])
            hint('box %d (%s): planning' % (b['index'], b['style']))
            import contextlib, io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                cmd_plan(a2)
            r = json.loads(buf.getvalue())
            b.update(strokes=r['strokes'], batch_steps=r['batch_steps'], est_seconds=r['est_seconds'],
                     detail=jload(os.path.join(a2.job, 'plan.json'))['stats'].get('detail'))
            summary.append({k: b[k] for k in ('index', 'style', 'strokes', 'batch_steps', 'est_seconds', 'detail')})
        jsave(B, os.path.join(a.job, 'boxes.json'))
        out = bx.assemble(a.job, sim=True)
        print(json.dumps({'boxes': summary, 'assembled_preview': out}, indent=1))
        return
    if jload(os.path.join(a.job, 'meta.json')).get('grid'):
        return cmd_plan_grid(a)
    detail = a.detail
    for attempt in range(5):
        plan, full = run_plan(a.job, detail, a.seed, log=hint if attempt == 0 and not a.quiet else (lambda *x: None))
        est, nsteps, _ = estimate(a.job, plan)
        n = plan['stats']['strokes']
        over = []
        if a.budget and n > a.budget * 1.05:
            over.append((a.budget / n) ** 0.5)
        if a.seconds and est > a.seconds:
            over.append((a.seconds / est) ** 0.6)
        if nsteps > 4900:
            over.append((4900 / nsteps) ** 0.6)
        if not over:
            break
        if attempt == 4:
            raise SystemExit('plan still estimates %.0f s (%s profile) after lowering detail to %.2f: above the %.0f s cap; '
                             'use a smaller canvas, a lower --detail, or split the work' % (est, ui_for(a.job).get('timing_profile'), detail, a.seconds))
        detail *= min(over) * 0.97
        hint('-> over budget (%d strokes, %.0f s, %d steps): retry with detail %.3f' % (n, est, nsteps, detail))
    plan['stats'].update({'detail': round(detail, 3), 'est_seconds': round(est), 'batch_steps': nsteps})
    jsave(plan, os.path.join(a.job, 'plan.json'), compact=True)
    write_previews(a.job, full, plan)
    print(json.dumps({'strokes': plan['stats']['strokes'], 'layers': plan['stats']['layers'],
                      'colour_groups': plan['stats']['colour_groups'], 'batch_steps': nsteps,
                      'est_seconds': round(est), 'sim_vs_target': plan['sim_score']}, indent=1))
    hint('sim_vs_target = simulation vs the STYLE-FILTERED target (target.png); score reports sim_vs_raw / live_vs_raw '
         'against the unfiltered source and live_vs_sim (execution fidelity).')


def write_previews(job, full, plan):
    meta = jload(os.path.join(job, 'meta.json'))
    ox, oy = meta['layout']['draw_origin']
    pr.save_rgb(full, os.path.join(job, 'sim_canvas.png'))
    pr.save_rgb(full[oy:oy + meta['H'], ox:ox + meta['W']], os.path.join(job, 'sim.png'))
    tgt = Image.open(os.path.join(job, 'target_raw.png'))
    can = Image.open(os.path.join(job, 'sim_canvas.png'))
    gap = 12
    out = Image.new('RGB', (tgt.width + can.width + 3 * gap, max(tgt.height, can.height) + 2 * gap + 22), (24, 24, 24))
    out.paste(tgt, (gap, gap + 22 + (can.height - tgt.height) // 2))
    out.paste(can, (2 * gap + tgt.width, gap + 22))
    d = ImageDraw.Draw(out)
    d.text((gap, 6), 'source', fill=(220, 220, 220))
    s = plan['sim_score']
    d.text((2 * gap + tgt.width, 6), 'simulation (%s): %d strokes, dE %.2f' % (plan.get('preset'), plan['stats']['strokes'], s['all']),
           fill=(220, 220, 220))
    out.save(os.path.join(job, 'preview.png'))


def cmd_preview(a):
    plan = jload(os.path.join(a.job, 'plan.json'))
    est, nsteps, em = estimate(a.job, plan, ui_for(a.job, a.ui))
    print(json.dumps({'preview': os.path.join(a.job, 'preview.png'), 'sim': os.path.join(a.job, 'sim_canvas.png'),
                      'strokes': em.n_strokes, 'picks': em.n_picks, 'batch_steps': nsteps, 'est_seconds': round(est),
                      'est_minutes': round(est / 60, 1), 'sim_vs_target': plan['sim_score'], 'canvas_origin': list(em.org)}, indent=1))


def cmd_emit(a):
    if os.path.isfile(os.path.join(a.job, 'boxes.json')) and not os.path.isfile(os.path.join(a.job, 'meta.json')):
        B = jload(os.path.join(a.job, 'boxes.json'))
        for b in B['boxes']:
            sub = os.path.join(a.job, b['job'])
            if os.path.isfile(os.path.join(a.job, 'ui.json')) and not os.path.isfile(os.path.join(sub, 'ui.json')):
                shutil.copy(os.path.join(a.job, 'ui.json'), os.path.join(sub, 'ui.json'))
            elif os.path.isfile(os.path.join(a.job, 'ui.json')):
                shutil.copy(os.path.join(a.job, 'ui.json'), os.path.join(sub, 'ui.json'))
            plan = jload(os.path.join(sub, 'plan.json'))
            meta = jload(os.path.join(sub, 'meta.json'))
            out = os.path.join(a.plans or PLANS, b['plan_file'])
            est0 = estimate(sub, plan, ui_for(sub, a.ui))[0]
            if a.seconds and est0 > a.seconds and not a.force:
                raise SystemExit('refusing to emit box %d: estimate %.0f s exceeds %.0f s' % (b['index'], est0, a.seconds))
            s = ep.emit(plan, meta, ui_for(sub, a.ui), tools_for(sub), out)
            dst = os.path.join(a.job, b['canvas_file'])
            if not os.path.isfile(dst) or getattr(a, 'recopy', False):     # never overwrite a painted, saved box
                shutil.copy(os.path.join(sub, 'canvas.png'), dst)
            b.update(plan_path=out, canvas_path=os.path.join(a.job, b['canvas_file']), batch_steps=s['steps'],
                     est_seconds=s['est_seconds'], est_seconds_unrecorded=s['est_seconds_unrecorded'],
                     canvas_origin=s['canvas_origin'])
        B['est_total_seconds'] = sum(b['est_seconds'] for b in B['boxes'])
        jsave(B, os.path.join(a.job, 'boxes.json'))
        print(json.dumps(B, indent=1))
        hint('Open each canvas (pa_box_*.png) in Paint; paint them in order, one batch call per plan, the right window in front '
             'before each; save each with Ctrl+S; then assemble --job %s' % a.job)
        return
    plan = jload(os.path.join(a.job, 'plan.json'))
    meta = jload(os.path.join(a.job, 'meta.json'))
    if meta.get('grid'):
        out = gr.emit_grid(plan, meta, ui_for(a.job, a.ui), tools_for(a.job), a.plans or PLANS, a.name, a.seconds or 1e9)
        jsave(out, os.path.join(a.job, 'cells.json'))
        print(json.dumps(out, indent=1))
        hint('Run %s: melaya_computer_batch {"steps": [], "plan": {"file": "<plan>"}} per plan, in order (no window_id). '
             'Cell rectangles, step ranges and times: %s' % ('ONE call' if out['one_plan'] else '%d calls' % len(out['plans']),
                                                             os.path.join(a.job, 'cells.json')))
        return
    out = os.path.join(a.plans or PLANS, a.name + '.json')
    est0 = estimate(a.job, plan, ui_for(a.job, a.ui))[0]
    if a.seconds and est0 > a.seconds and not a.force:
        raise SystemExit('refusing to emit: estimate %.0f s (%s profile) exceeds --seconds %.0f (the batch stops at 10 '
                         'minutes). Re-plan with --seconds, or --force.' % (est0, ui_for(a.job, a.ui).get('timing_profile'), a.seconds))
    s = ep.emit(plan, meta, ui_for(a.job, a.ui), tools_for(a.job), out)
    jsave(s, os.path.join(a.job, 'emit.json'))
    print(json.dumps(s, indent=1))
    hint('Run it in ONE call: melaya_computer_batch {"steps": [], "plan": {"file": "%s.json"}}  (no window_id). '
         'The same summary is in JOB/emit.json.' % a.name)


def col_de(a, b):
    from .color import delta_e
    return delta_e(a, b)


def load_grab(a):
    if getattr(a, 'take', False):
        g = sc.grab(os.path.join(a.job, 'grab_%s.png' % a.f.__name__.replace('cmd_', '')))
    else:
        g = a.grab
    return np.asarray(Image.open(g).convert('RGB')).astype(float) / 255


def located(g, meta):
    res = locate_canvas(g, meta)
    if 'origin' not in res or res.get('swatch_err', 99) > 2.5:
        raise SystemExit('canvas not found on screen (%s): bring the Paint window to the front, maximised, zoom 100 %%, '
                         'nothing covering the palette strip, then retry' % json.dumps(res))
    return res


def cmd_locate(a):
    meta = jload(os.path.join(a.job, 'meta.json'))
    res = located(load_grab(a), meta)
    if a.write_ui:
        p = os.path.join(a.job, 'ui.json')
        over = jload(p) if os.path.isfile(p) else {}
        over.update({'canvas_origin': res['origin'], 'scale': res['scale']})
        jsave(over, p)
        res['ui'] = os.path.join(a.job, 'ui.json')
    print(json.dumps(res))


def cmd_score(a):
    meta = jload(os.path.join(a.job, 'meta.json'))
    if getattr(a, 'file', None):
        # the saved Paint file IS the canvas: exact pixels, no screen grab, no resize-handle dots
        g = np.asarray(Image.open(winpath(a.file)).convert('RGB')).astype(float) / 255
        Wc0, Hc0 = meta['layout']['canvas']
        if g.shape[:2] != (Hc0, Wc0):
            raise SystemExit('saved file is %dx%d, expected the %dx%d canvas' % (g.shape[1], g.shape[0], Wc0, Hc0))
        loc = {'origin': [0, 0], 'scale': 1.0, 'swatch_err': 0.0, 'method': 'file'}
    else:
        g = load_grab(a)
        loc = located(g, meta)
    live = sc.crop_drawing(g, loc['origin'], meta, loc['scale'])
    pr.save_rgb(live, os.path.join(a.job, 'live.png'))
    # gallery crop: the canvas without the palette strip, frame included (canvas x 41.., full height)
    Wc, Hc = meta['layout']['canvas']
    ox, oy, s_ = loc['origin'][0], loc['origin'][1], loc['scale']
    x0, y0 = int(round(ox + 41 * s_)), int(round(oy))
    lc = g[y0:y0 + int(round(Hc * s_)), x0:x0 + int(round((Wc - 41) * s_))]
    if abs(s_ - 1) > 1e-6:
        lc = np.asarray(Image.fromarray((lc * 255).astype(np.uint8)).resize((Wc - 41, Hc), Image.LANCZOS)).astype(float) / 255
    pr.save_rgb(lc, os.path.join(a.job, 'live_canvas.png'))
    res = {'locate': loc, 'live_vs_' + a.vs: sc.score_job(a.job, live, a.vs)}
    if os.path.isfile(os.path.join(a.job, 'sim.png')):
        simg = pr.load_rgb(os.path.join(a.job, 'sim.png'))
        res['sim_vs_' + a.vs] = sc.score_job(a.job, simg, a.vs)
        res['live_vs_sim'] = sc.scores(live, simg, meta.get('face_box'))
        tgt = Image.open(os.path.join(a.job, 'target_raw.png'))
        row = [tgt, Image.open(os.path.join(a.job, 'sim.png')), Image.open(os.path.join(a.job, 'live.png'))]
        out = Image.new('RGB', (sum(i.width for i in row) + 40, row[0].height + 30), (24, 24, 24))
        x = 10
        d = ImageDraw.Draw(out)
        for lab, im in zip(('target', 'simulation', 'live'), row):
            out.paste(im, (x, 25))
            d.text((x, 6), lab, fill=(220, 220, 220))
            x += im.width + 10
        out.save(os.path.join(a.job, 'compare.png'))
    if meta.get('grid') and os.path.isfile(os.path.join(a.job, 'sim.png')):
        simg = pr.load_rgb(os.path.join(a.job, 'sim.png'))
        res['cells'] = []
        for c in meta['grid']['cells']:
            x0, y0, x1, y1 = [int(round(v)) for v in c['rect']]
            res['cells'].append({'index': c['index'], 'style': c['style'],
                                 'live_vs_sim': round(col_de(live[y0 + 6:y1 - 6, x0 + 6:x1 - 6], simg[y0 + 6:y1 - 6, x0 + 6:x1 - 6]), 2)})
    jsave(res, os.path.join(a.job, 'score.json'))
    print(json.dumps(res, indent=1))


def cmd_calib_plan(a):
    """A calibration job: blank drawing with a black swatch; one black stroke per tool (see locate.CALIB_TOOLS)."""
    os.makedirs(a.job, exist_ok=True)
    W, H = calib_size()
    pal = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
    layout = pr.make_canvas(W, H, pal, os.path.join(a.job, 'canvas.png'))
    meta = dict(W=W, H=H, layout=layout, palette=pal.tolist(), palette_info={'frame': {}}, frame=False, focus=[], face_box=None)
    jsave(meta, os.path.join(a.job, 'meta.json'))
    strokes = calib_strokes()
    layers = []
    for s in strokes:
        for _ in range(s['passes']):
            layers.append({'name': 'calib-%s' % s['tool'], 'tool': s['tool'], 'width': s['width'], 'opacity': s['opacity'],
                           'strokes': [[0, s['pts']]]})
    jsave({'layers': layers}, os.path.join(a.job, 'calib_plan.json'))
    jsave(strokes, os.path.join(a.job, 'calib_strokes.json'))
    s = ep.emit({'layers': layers}, meta, ui_for(a.job, a.ui), tools_for(a.job), os.path.join(a.plans or PLANS, a.name + '.json'))
    print(json.dumps(s, indent=1))
    hint('Open %s in Paint (maximised, 100%%), locate --write-ui, run calib-plan again, run plan file %s.json in one '
         'batch call, then: calib-measure --job %s --take' % (os.path.join(a.job, 'canvas.png'), a.name, a.job))


def cmd_calib_measure(a):
    meta = jload(os.path.join(a.job, 'meta.json'))
    g = load_grab(a)
    loc = located(g, meta)
    d = sc.crop_drawing(g, loc['origin'], meta, loc['scale'])
    pr.save_rgb(d, os.path.join(a.job, 'calib_live.png'))
    res = measure_tools(d, jload(os.path.join(a.job, 'calib_strokes.json')))
    tools = tools_from_measure(json.load(open(os.path.join(PKG, 'paint_tools.json'))), res)
    jsave(tools, os.path.join(a.job, 'tools.json'))
    if a.install:
        jsave(tools, os.path.join(PKG, 'paint_tools.json'))
    jsave(res, os.path.join(a.job, 'calib_measured.json'))
    print(json.dumps({'measured': res, 'tools_json': os.path.join(a.job, 'tools.json'),
                      'installed': bool(a.install)}, indent=1))


def cmd_speed_calib(a):
    ui, tools = ui_for(a.job, a.ui), tools_for(a.job)

    def emit_fn(plan, meta, out):
        return {k: v for k, v in ep.emit(plan, meta, ui, tools, out).items() if k in ('file', 'steps', 'est_seconds')}
    out = spc.generate(a.job, a.name, a.plans or PLANS, emit_fn, pr.make_canvas)
    print(json.dumps(out, indent=1))
    hint('Open %s in Paint, pre-flight, locate --write-ui, re-run speed-calib (re-emits with the measured origin), then run '
         '%s_setup, %s_s0 .. _s4 in order, one batch call each; note each duration; then speed-measure --job %s --take '
         '--times t0,t1,t2,t3,t4' % (os.path.join(a.job, 'canvas.png'), a.name, a.name, a.job))


def cmd_speed_measure(a):
    meta = jload(os.path.join(a.job, 'meta.json'))
    if getattr(a, 'file', None):
        g = np.asarray(Image.open(winpath(a.file)).convert('RGB')).astype(float) / 255
        loc = {'origin': [0, 0], 'scale': 1.0}
    else:
        g = load_grab(a)
        loc = located(g, meta)
    d = sc.crop_drawing(g, loc['origin'], meta, loc['scale'])
    pr.save_rgb(d, os.path.join(a.job, 'speed_live.png'))
    times = [float(v) for v in a.times.split(',')] if a.times else None
    res = spc.measure(d, times)
    if a.install:
        p = os.path.join(PKG, 'paint_tools.json')
        tools = jload(p)
        for t in ('brush', 'pencil'):
            r = res['recommended'].get(t)
            if r:
                tools['tools'][t].update(speed=r['speed'], stepPx=r['stepPx'], strokeGapMs=r['strokeGapMs'])
        if res['recommended'].get('fill'):
            tools['tools']['fill']['strokeGapMs'] = res['recommended']['fill']['strokeGapMs']
        if res.get('fill_connectivity'):
            tools['tools']['fill'].update(connectivity=res['fill_connectivity'], fill_conn=res['fill_connectivity'], measured=True)
        jsave(tools, p)
        res['installed'] = p
    jsave(res, os.path.join(a.job, 'speed_measured.json'))
    print(json.dumps(res, indent=1))


def cmd_assemble(a):
    files = {}
    for kv in (a.file or []):
        k, v = kv.split('=', 1)
        files[k] = winpath(v)
    out = bx.assemble(a.job, files, sim=a.sim, divider=a.divider_width)
    print(json.dumps(out, indent=1))


def cmd_make(a):
    a2 = argparse.Namespace(**vars(a))
    cmd_prepare(a2)
    a2.detail, a2.budget, a2.seconds, a2.seed, a2.quiet = a.detail, a.budget, a.seconds, a.seed, True
    cmd_plan(a2)
    if a.name:
        a2.ui, a2.plans = a.ui, None
        cmd_emit(a2)


def cmd_contact(a):
    tiles = []
    for job in a.jobs:
        im = Image.open(os.path.join(job, 'sim.png' if a.drawing else 'sim_canvas.png')).convert('RGB')
        im.thumbnail((a.tile, a.tile * 2))
        p = jload(os.path.join(job, 'plan.json'))
        try:
            est = estimate(job, p)[0]
        except SystemExit:
            est = p['stats'].get('est_seconds', 0)
        label = a.labels[len(tiles)] if a.labels and len(a.labels) > len(tiles) else p.get('preset')
        tiles.append((im, '%s  %d strokes  ~%ds' % (label, p['stats']['strokes'], est)))
    cols = a.cols
    rows = (len(tiles) + cols - 1) // cols
    tw = max(t[0].width for t in tiles)
    th = max(t[0].height for t in tiles) + 22
    sheet = Image.new('RGB', (cols * (tw + 10) + 10, rows * (th + 10) + 10), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(tiles):
        x, y = 10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)
        sheet.paste(im, (x, y + 20))
        d.text((x, y + 4), lab, fill=(225, 225, 225))
    if a.out.endswith('.png') and a.colors:
        sheet = sheet.quantize(a.colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    sheet.save(a.out, optimize=True)
    print(json.dumps({'out': a.out, 'size': list(sheet.size)}))


def main(argv=None):
    ap = argparse.ArgumentParser(prog='paint_artist', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('compose'); p.add_argument('scene'); p.add_argument('--out', required=True)
    p.add_argument('--width', type=int); p.add_argument('--height', type=int); p.set_defaults(f=cmd_compose)
    p = sp.add_parser('analyse'); p.add_argument('ref'); p.add_argument('--out', required=True); p.add_argument('--base')
    p.set_defaults(f=cmd_analyse)

    def prep_args(p):
        p.add_argument('src', nargs='?'); p.add_argument('--subject', help='bundled subject, e.g. mona_lisa')
        p.add_argument('--job', required=True); p.add_argument('--style', default='master')
        p.add_argument('--width', type=int); p.add_argument('--height', type=int, default=672)
        p.add_argument('--fit', default='crop', choices=['crop', 'stretch']); p.add_argument('--focus', action='append')
        p.add_argument('--face-box'); p.add_argument('--reference'); p.add_argument('--transfer', action='store_true')
        p.add_argument('--no-frame', action='store_true'); p.set_defaults(focus_from=None)
        p.add_argument('--grid', help='composite: RxC cells, e.g. 2x2 (with --styles)')
        p.add_argument('--boxes', help='RxC boxes, each painted as its own full painting on a standard canvas (with --styles)')
        p.add_argument('--bleed', type=float, default=8, help='boxes: source px of the neighbouring area planned past each interior edge')
        p.add_argument('--styles', help='grid: comma-separated styles (or preset files), reading order')
        p.add_argument('--order', help='grid: paint order of the cells, e.g. 0,1,2,3 (default reading order)')
        p.add_argument('--divider-width', type=int, default=5); p.add_argument('--inset', type=float, default=2,
                                                                                help='grid: footprint clearance from the divider centre line; keep it <= divider width / 2 so the divider hides the seam')
        p.add_argument('--divider-color', default='#1a1a1a')
        p.add_argument('--split-x', help='grid: vertical divider positions, fractions of the width (cols-1 values), e.g. 0.45')
        p.add_argument('--split-y', help='grid: horizontal divider positions, fractions of the height (rows-1 values), e.g. 0.37')
        p.add_argument('--cell-override', help='grid: JSON {"<cell index>": {preset keys}} merged into that cell\'s style')
    p = sp.add_parser('prepare'); prep_args(p); p.set_defaults(f=cmd_prepare)
    p = sp.add_parser('plan'); p.add_argument('--job', required=True); p.add_argument('--detail', type=float, default=1.0)
    p.add_argument('--budget', type=int); p.add_argument('--seconds', type=float, default=480, help='time cap in seconds with the timing profile (the batch runs up to 10 min); 0 = none'); p.add_argument('--seed', type=int, default=0)
    p.add_argument('--quiet', action='store_true'); p.set_defaults(f=cmd_plan)
    p = sp.add_parser('preview'); p.add_argument('--job', required=True); p.add_argument('--ui'); p.set_defaults(f=cmd_preview)
    p = sp.add_parser('emit'); p.add_argument('--job', required=True); p.add_argument('--name', required=True)
    p.add_argument('--ui'); p.add_argument('--plans')
    p.add_argument('--seconds', type=float, default=480, help='refuse a single plan above this estimate (grid: split per cell instead)')
    p.add_argument('--force', action='store_true', help='emit even above --seconds')
    p.add_argument('--recopy', action='store_true', help='boxes: overwrite the box canvases with blank ones')
    p.set_defaults(f=cmd_emit)
    for name, fn in (('locate', cmd_locate), ('score', cmd_score), ('calib-measure', cmd_calib_measure)):
        p = sp.add_parser(name); p.add_argument('--job', required=True); p.add_argument('--grab'); p.add_argument('--take', action='store_true')
        if name == 'locate':
            p.add_argument('--write-ui', action='store_true')
        if name == 'score':
            p.add_argument('--vs', default='raw', choices=['raw', 'target'])
            p.add_argument('--file', help='score the saved canvas PNG instead of a screen grab (exact, preferred)')
        if name == 'calib-measure':
            p.add_argument('--install', action='store_true', help='also write the result into paint_tools.json')
        p.set_defaults(f=fn)
    p = sp.add_parser('calib-plan'); p.add_argument('--job', required=True); p.add_argument('--name', default='paint_calib'); p.add_argument('--plans')
    p.add_argument('--ui'); p.set_defaults(f=cmd_calib_plan)
    p = sp.add_parser('assemble'); p.add_argument('--job', required=True); p.add_argument('--sim', action='store_true')
    p.add_argument('--file', action='append', help='INDEX=saved_box.png (default JOB/pa_box_<style>.png)')
    p.add_argument('--divider-width', type=int, default=5); p.set_defaults(f=cmd_assemble)
    p = sp.add_parser('speed-calib'); p.add_argument('--job', required=True); p.add_argument('--name', default='pa_speed')
    p.add_argument('--ui'); p.add_argument('--plans'); p.set_defaults(f=cmd_speed_calib)
    p = sp.add_parser('speed-measure'); p.add_argument('--job', required=True); p.add_argument('--grab'); p.add_argument('--take', action='store_true')
    p.add_argument('--file'); p.add_argument('--times', help='batch durations of s0..s4, comma separated')
    p.add_argument('--install', action='store_true'); p.set_defaults(f=cmd_speed_measure)
    p = sp.add_parser('make'); prep_args(p); p.add_argument('--name'); p.add_argument('--detail', type=float, default=1.0)
    p.add_argument('--budget', type=int); p.add_argument('--seconds', type=float, default=480, help='time cap in seconds with the timing profile (the batch runs up to 10 min); 0 = none'); p.add_argument('--seed', type=int, default=0)
    p.add_argument('--ui'); p.set_defaults(f=cmd_make)
    p = sp.add_parser('contact'); p.add_argument('jobs', nargs='+'); p.add_argument('--out', required=True)
    p.add_argument('--cols', type=int, default=4); p.add_argument('--tile', type=int, default=300)
    p.add_argument('--drawing', action='store_true'); p.add_argument('--labels', nargs='*')
    p.add_argument('--colors', type=int, default=0, help='quantise the sheet to N colours (smaller PNG)'); p.set_defaults(f=cmd_contact)
    for sp_ in sp.choices.values():
        if not any(x.dest == 'profile' for x in sp_._actions):
            sp_.add_argument('--profile', choices=['recorded', 'unrecorded'], help='timing profile (default recorded)')
    a = ap.parse_args(argv)
    PROFILE[0] = getattr(a, 'profile', None)
    for k in ('job', 'src', 'out', 'grab', 'ui', 'plans', 'reference', 'scene', 'ref'):
        if getattr(a, k, None):
            setattr(a, k, winpath(getattr(a, k)))
    if getattr(a, 'jobs', None):
        a.jobs = [winpath(j) for j in a.jobs]
    if getattr(a, 'style', None):
        a.style = winpath(a.style)
    a.f(a)


if __name__ == '__main__':
    main()
