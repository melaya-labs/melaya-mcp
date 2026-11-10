"""Kleki adapter (https://kleki.com in a browser window, macOS or any OS): app-agnostic plan -> Melaya batch plan JSON.

Same plan, layout and path steps as the Paint adapter (emit_paint.py); only the UI differs:
  tools    brush / oil / watercolour -> Kleki's Pen brush (oil and watercolour as a lower pen opacity, see the tool
           model), pencil -> the Pixel brush (aliased), fill -> the Paint Bucket (key G, tolerance 0 set once).
           Brushes are chosen by clicking their icon in the brush row; G is pressed only when the bucket is not
           already active (G toggles bucket <-> gradient) and B returns from the bucket to the last brush (B pressed
           in brush mode would cycle to the next brush, so it is never sent then).
  size     Kleki's sliders are custom elements (no AX slider): a left press on the bar sets the value at that x.
           Size is a diameter: radius = 0.5 + 99.5 t^2 (t = x along the bar), so one click lands any size.
  opacity  Pen: 0.01 + 0.99 t^1.7, Pixel: linear. 100 % is a short drag past the right end (the value clamps).
  colour   right-click on the palette strip swatch (Kleki's temporary eyedropper): one step per pick.
Coordinates are screen points (macOS); ui.kleki.json holds the bars and icons for a fixed window, `locate` the
canvas origin.
"""
import math

from .emit_paint import Emitter


class KlekiEmitter(Emitter):
    """Overrides the UI steps of the Paint Emitter; the stroke, clamping and estimate logic is shared."""

    def __init__(self, meta, ui, tools):
        super().__init__(meta, ui, tools)
        self.mode = None                     # 'brush' | 'bucket'
        self.brush = None                    # 'pen' | 'pixel'

    # --- sliders: one press at the x of the wanted value (or a drag past the end for the maximum)
    def _bar_x(self, bar, t):
        return round(bar['x0'] + max(0.0, min(1.0, t)) * (bar['x1'] - bar['x0']), 2)

    def _set_bar(self, bar, t):
        y = bar['y']
        if t >= 0.999:
            x0 = bar['x1'] - 6
            self.steps.append({'kind': 'path', 'strokes': [[[x0, y], [bar['x1'] + 24, y]]], 'speed': 800, 'stepPx': 4,
                               'strokeGapMs': 10, 'settleMs': self.ui.get('path', {}).get('settleMs', 12)})
        else:                                # a press, not a path: a zero-length path sends no pointer event at all
            x = self._bar_x(bar, t)
            self.steps += [{'kind': 'mouse', 'target': {'x': x, 'y': y}, 'state': 'down'},
                           {'kind': 'mouse', 'target': {'x': x, 'y': y}, 'state': 'up'}]
        self.wait(self.ui.get('waits_ms', {}).get('after_slider', 40))

    def size(self, px):
        px = min(max(float(px), 1.0), self.ui.get('max_px', 64))
        px = round(px * self.tools[self.cur_tool].get('size_factor', 1.0), 1)
        if px == self.cur_size:
            return
        r = px / 2
        t = math.sqrt(max(r - 0.5, 0.0) / 99.5)
        self._set_bar(self.ui['size_bar'], t)
        self.cur_size = px

    def opacity(self, op):
        spec = self.tools[self.cur_tool]
        v = max(0.01, min(1.0, op * spec.get('kleki_opacity', 1.0)))
        v = round(v, 2)
        if v == self.cur_opacity:
            return
        if v >= 0.999:
            t = 1.0
        elif self.brush == 'pixel':
            t = (v - 0.01) / 0.99
        else:
            t = ((v - 0.01) / 0.99) ** (1 / 1.7)
        self._set_bar(self.ui['opacity_bar'], t)
        self.cur_opacity = v

    # --- tools
    def tool(self, t):
        if t == self.cur_tool:
            return
        w = self.ui.get('waits_ms', {})
        if t == 'fill':
            if self.mode != 'bucket':
                self.steps.append({'kind': 'press', 'keys': 'g', 'onError': 'continue'})
                self.wait(w.get('after_key', 120))
            self.mode = 'bucket'
        else:
            want = 'pixel' if t == 'pencil' else 'pen'
            if self.mode == 'bucket':
                self.steps.append({'kind': 'press', 'keys': 'b', 'onError': 'continue'})
                self.wait(w.get('after_key', 120))
            if want != self.brush or self.mode != 'brush':
                x, y = self.ui['brush_icons'][want]       # mouse steps: a click step waits ~0.65 s for an AX change Kleki never shows
                self.steps += [{'kind': 'mouse', 'target': {'x': x, 'y': y}, 'state': 'down'},
                               {'kind': 'mouse', 'target': {'x': x, 'y': y}, 'state': 'up'}]
                self.wait(w.get('after_brush_icon', 150))
                self.cur_size = self.cur_opacity = None        # each Kleki brush keeps its own size and opacity
            self.mode, self.brush = 'brush', want
        self.cur_tool = t
        self.n_switch += 1

    def paths(self, strokes, speed, step_px, gap_ms=None, fill=False):
        """As Paint, plus settleMs on every path step: macOS delivers drag events once per display frame and Kleki
        draws only up to the last move it received (not to the release point), so without a still frame on the last
        point a stroke loses up to one frame of travel (a whole 40 px edge at 8000 px/s), and a press released in
        the same frame (bucket clicks, dots) is dropped."""
        n0 = len(self.steps)
        super().paths(strokes, speed, step_px, gap_ms, fill)
        settle = self.ui.get('path', {}).get('settleMs', 12)
        for s in self.steps[n0:]:
            if s['kind'] == 'path':
                s['settleMs'] = settle

    def pick(self, i):
        x, y = self.swatch(i)
        self.steps += [{'kind': 'mouse', 'target': {'x': x, 'y': y}, 'state': 'down', 'button': 'right'},
                       {'kind': 'mouse', 'target': {'x': x, 'y': y}, 'state': 'up', 'button': 'right'}]
        self.n_picks += 1

    def emit(self, plan):
        self.start()
        for L in plan['layers']:
            if L['strokes']:
                self.layer(L)
        return {'surface': 'computer', 'kind': 'batch', 'steps': self.steps}

    def start(self):
        """Known state: the Pen brush at 100 % opacity (the app may have been left on any tool)."""
        self.mode = 'bucket'                 # forces B, then the Pen icon
        self.tool('brush')
        self.opacity(1.0)
        self.n_switch = 0
