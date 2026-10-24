"""Paint adapter: app-agnostic plan -> Melaya Computer Control batch plan JSON (one melaya_computer_batch call).

Step kinds produced (exactly the ones the live Mona Lisa run used):
  set_value  {target:{label,role:"slider"}, value, onError:"continue"}      Size / Opacity sliders
  click      {target:{x,y}, onError:"continue"[, delivery:"foreground"]}  Pencil, Brushes dropdown + item
  wait       {ms}
  mouse      {target:{x,y}, state:"down"|"up"}                           colour picker press, swatch press
  move       {x, y}                                                       travel to the swatch
  path       {strokes:[[[x,y],...],...], speed, stepPx, strokeGapMs}      <=200 strokes per step, camelCase keys
Colours come from the palette strip painted into the canvas image, picked with the colour picker (Paint's Edit
Colours dialog hangs Paint: never used). The picker returns to the previous tool after one pick.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_ui(path=None):
    """ui.default.json, overridden by a job's ui.json (normally just canvas_origin and scale from locate). The
    timing model always comes from the defaults unless the override sets timing_model_override: true."""
    with open(os.path.join(HERE, 'ui.default.json')) as f:
        ui = json.load(f)
    if path and os.path.abspath(path) != os.path.abspath(os.path.join(HERE, 'ui.default.json')):
        with open(path) as f:
            over = json.load(f)
        if not over.get('timing_model_override'):
            over.pop('timing_model', None)
        ui.update(over)
    return ui


def size_value(px):
    px = int(round(px))
    return px - 1 if px <= 22 else (px + 1 + 22) // 2


class Emitter:
    def __init__(self, meta, ui, tools):
        self.meta, self.ui, self.tools = meta, ui, tools
        self.s = float(ui.get('scale', 1.0))
        Wc, Hc = meta['layout']['canvas']
        if ui.get('canvas_origin'):
            self.org = tuple(ui['canvas_origin'])
        else:
            cx, cy = ui['canvas_center']
            self.org = (int(round(cx - Wc * self.s / 2)), int(round(cy - Hc * self.s / 2)))
        vp = ui.get('viewport')
        if vp and (self.org[0] < vp[0] or self.org[1] < vp[1] or self.org[0] + Wc * self.s > vp[2] or self.org[1] + Hc * self.s > vp[3]):
            raise SystemExit('canvas %dx%d does not fit the Paint viewport at 100%% zoom; lower --height' % (Wc, Hc))
        self.Wc, self.Hc = Wc, Hc
        self.steps = []
        self.cur_tool = None
        self.cur_size = None
        self.cur_opacity = None
        self.n_strokes = self.n_picks = self.n_switch = 0
        self.ink = 0.0
        self.ink_time = 0.0
        self.ink16 = 0.0
        self.ink4 = 0.0
        self.n_points = 0
        self.n_long = self.n_short = self.n_fill = 0
        self.clamped = 0

    # --- coordinates
    def scr(self, cx, cy):
        return [int(round(self.org[0] + cx * self.s)), int(round(self.org[1] + cy * self.s))]

    def canvas_pt(self, x, y, width, frame=False):
        """drawing coords -> clamped canvas coords: inside the canvas and clear of the resize handles and the strip;
        painting strokes (not the frame) keep their whole footprint (width/2) 5 px inside the canvas edge."""
        ox, oy = self.meta['layout']['draw_origin']
        e = self.ui.get('edge_clear_px', 5)
        h = 0 if frame else width / 2
        xmin = max(e + h, self.meta['layout']['strip']['x1'] + 1 + width / 2 + 0.5)
        cx, cy = ox + x, oy + y
        nx = min(max(cx, xmin), self.Wc - 1 - e - h)
        ny = min(max(cy, e + h), self.Hc - 1 - e - h)
        if (nx, ny) != (cx, cy):
            self.clamped += 1
        return nx, ny

    def swatch(self, i):
        st = self.meta['layout']['strip']
        return self.scr((st['x0'] + st['x1']) / 2, st['y0'] + st['swh'] * i + st['swh'] // 2)

    # --- UI steps
    def wait(self, ms):
        self.steps.append({'kind': 'wait', 'ms': int(ms)})

    def set_slider(self, which, value):
        self.steps.append({'kind': 'set_value', 'target': dict(self.ui[which]), 'value': str(value), 'onError': 'continue'})

    def tool(self, t):
        if t == self.cur_tool:
            return
        w = self.ui.get('waits_ms', {})
        if t in ('pencil', 'fill'):
            x, y = self.ui[t]
            self.steps.append({'kind': 'click', 'target': {'x': x, 'y': y}, 'onError': 'continue'})
            self.wait(w.get('after_pencil', 200))
        else:
            x, y = self.ui['brushes']
            self.steps.append({'kind': 'click', 'target': {'x': x, 'y': y}, 'delivery': 'foreground', 'onError': 'continue'})
            self.wait(w.get('after_brushes_open', 450))
            ix, iy = self.ui['brush_items'][t]
            self.steps.append({'kind': 'click', 'target': {'x': ix, 'y': iy}, 'onError': 'continue'})
            self.wait(w.get('after_brush_item', 300))
        self.cur_tool = t
        self.cur_size = None
        self.cur_opacity = None
        self.n_switch += 1

    def opacity(self, op):
        if not self.tools[self.cur_tool].get('opacity_setting'):
            return
        v = int(round(op * 100))
        if v != self.cur_opacity:
            self.set_slider('opacity_slider', v)
            self.cur_opacity = v

    def size(self, px):
        px = min(int(round(px)), self.ui.get('max_px', 64))
        if px != self.cur_size:
            self.set_slider('size_slider', size_value(px))
            self.cur_size = px

    def pick(self, i):
        px, py = self.ui['picker']
        x, y = self.swatch(i)
        self.steps += [{'kind': 'mouse', 'target': {'x': px, 'y': py}, 'state': 'down'},
                       {'kind': 'mouse', 'target': {'x': px, 'y': py}, 'state': 'up'},
                       {'kind': 'move', 'x': x, 'y': y},
                       {'kind': 'mouse', 'target': {'x': x, 'y': y}, 'state': 'down'},
                       {'kind': 'mouse', 'target': {'x': x, 'y': y}, 'state': 'up'}]
        self.n_picks += 1

    def paths(self, strokes, speed, step_px, gap_ms=None, fill=False):
        p = self.ui.get('path', {})
        n = p.get('max_strokes_per_step', 200)
        v_eff = min(speed, step_px * 1000.0)
        for st in strokes:
            L = sum(math.dist(a, b) for a, b in zip(st, st[1:]))
            self.ink += L
            self.ink_time += L / v_eff
            self.n_points += len(st)
            if fill:
                self.n_fill += 1
                continue
            if L < 4:
                self.n_short += 1
            else:
                self.n_long += 1
            if step_px > 4:
                self.ink16 += L
            else:
                self.ink4 += L
        gap = p.get('strokeGapMs', 2) if gap_ms is None else gap_ms
        for k in range(0, len(strokes), n):
            self.steps.append({'kind': 'path', 'strokes': strokes[k:k + n], 'speed': speed, 'stepPx': step_px,
                               'strokeGapMs': gap})
        self.n_strokes += len(strokes)

    # --- layers
    def layer(self, L):
        t = L['tool']
        spec = self.tools[t]
        self.tool(t)
        if t != 'fill':                                   # the Fill tool has no size or opacity
            self.opacity(L.get('opacity', 1.0))
            self.size(L['width'])
        p = self.ui.get('path', {})
        nm = L.get('name', '')
        is_ground = nm.startswith('ground') or '-ground' in nm or nm.endswith('-base')
        speed = L.get('speed') or spec.get('speed') or (p.get('ground_speed', 6000) if is_ground else p.get('speed', 8000))
        step_px = L.get('stepPx') or spec.get('stepPx', 16)
        gap_ms = L.get('strokeGapMs', spec.get('strokeGapMs'))
        group, ck = [], None
        for k, pts in L['strokes']:
            if k != ck:
                if group:
                    self.paths(group, speed, step_px, gap_ms, t == 'fill')
                group, ck = [], k
                self.pick(k)
            q = [self.scr(*self.canvas_pt(x, y, L['width'], L.get('name', '').startswith('frame'))) for x, y in pts]
            q = [q[0]] + [b for a, b in zip(q, q[1:]) if b != a]
            if len(q) == 1:
                q.append([q[0][0] + 1, q[0][1]])
            group.append(q)
        if group:
            self.paths(group, speed, step_px, gap_ms, t == 'fill')

    def emit(self, plan):
        self.steps.append({'kind': 'set_value', 'target': dict(self.ui['opacity_slider']), 'value': '100', 'onError': 'continue'})
        for L in plan['layers']:
            if L['strokes']:
                self.layer(L)
        return {'surface': 'computer', 'kind': 'batch', 'steps': self.steps}

    def estimate(self, profile=None):
        """Seconds for the steps emitted so far, with a timing profile from ui['timing_profiles'] ('recorded', the
        default and conservative one, or 'unrecorded')."""
        profs = self.ui.get('timing_profiles') or {}
        name = profile or self.ui.get('timing_profile', 'recorded')
        tm = profs.get(name) or next(iter(profs.values()), {})
        waits = sum(s['ms'] for s in self.steps if s['kind'] == 'wait') / 1000
        nset = sum(1 for s in self.steps if s['kind'] == 'set_value')
        return (self.n_long * tm.get('per_long_s', 0.016) + self.n_short * tm.get('per_short_s', 0.036)
                + self.n_points * tm.get('per_point_s', 0.0) + self.n_picks * tm.get('per_pick_s', 0.28)
                + self.ink16 / 1000 * tm.get('per_kpx16_s', 0.55) + self.ink4 / 1000 * tm.get('per_kpx4_s', 0.0)
                + self.n_fill * tm.get('per_fill_s', 0.30) + nset * tm.get('per_set_value_s', 0.0) + waits)


def emit(plan, meta, ui, tools, out_path):
    em = Emitter(meta, ui, tools)
    doc = em.emit(plan)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(doc, f, separators=(',', ':'))
    kinds = {}
    for s in doc['steps']:
        kinds[s['kind']] = kinds.get(s['kind'], 0) + 1
    summary = {'file': out_path, 'steps': len(doc['steps']), 'kinds': kinds, 'strokes': em.n_strokes,
               'picks': em.n_picks, 'tool_switches': em.n_switch, 'ink_px': int(em.ink), 'clamped_points': em.clamped,
               'canvas_origin': list(em.org), 'bytes': os.path.getsize(out_path), 'est_seconds': round(em.estimate()),
               'est_seconds_unrecorded': round(em.estimate('unrecorded')), 'timing_profile': ui.get('timing_profile', 'recorded'),
               'max_steps_ok': len(doc['steps']) <= 5000, 'size_ok': os.path.getsize(out_path) <= 2 * 1024 * 1024}
    return summary
