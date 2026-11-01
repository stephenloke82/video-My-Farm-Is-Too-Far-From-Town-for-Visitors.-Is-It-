"""Storybook drawing kit: colour, type, shapes, and a per-process surface cache."""
import math, os, random
import cairo
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

W, H = 1920, 1080
FONT_DIR = os.path.join(os.environ["LOCALAPPDATA"], "farvid", "fonts")


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


SKY = hexc("1b36a8"); GOLD = hexc("f2b632"); TOMATO = hexc("e2452f"); LEAF = hexc("3f8f3a")
CREAM = hexc("fbf1d9"); PAPER = hexc("fff8e8"); INK = hexc("1b1f3a"); WOOD = hexc("c8955a")
WOODD = hexc("8f6238"); WOODL = hexc("e0b57e"); SOIL = hexc("7a5230"); GRASS = hexc("6fb04d")
GRASSD = hexc("4f9440"); WHEAT = hexc("e9cf7a"); DUSK = hexc("6a3f8f"); SNOW = hexc("eef3fb")
ICE = hexc("bcd3ee"); PLUM = hexc("5a3a8c"); TEAL = hexc("2f9e9a"); ROAD = hexc("8d8679")
GREY = hexc("8a8fa3"); WHITE = (1, 1, 1); DIRT = hexc("b98a58")


def mix(a, b, f):
    return tuple(a[i] + (b[i] - a[i]) * f for i in range(3))


# Timing helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def eout(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def back(x, s=1.5):
    x = clamp(x) - 1
    return x * x * ((s + 1) * x + s) + 1


def ramp(t, a, d=0.6):
    return clamp((t - a) / d) if d > 0 else float(t >= a)


def lerp(a, b, f):
    return a + (b - a) * f


# Type: glyph outlines from the font file, so cairo draws crisp vector text
class _Pen(BasePen):
    def __init__(self, gs):
        super().__init__(gs); self.ops = []
    def _moveTo(self, p): self.ops.append(("m", p))
    def _lineTo(self, p): self.ops.append(("l", p))
    def _curveToOne(self, a, b, p): self.ops.append(("c", a, b, p))
    def _closePath(self): self.ops.append(("z",))
    def _endPath(self): self.ops.append(("z",))


class Font:
    def __init__(self, path):
        self.f = TTFont(path)
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.cache = {}
        self.adv = self.f["hmtx"].metrics

    def glyph(self, ch):
        g = self.cache.get(ch)
        if g is None:
            name = self.cmap.get(ord(ch), ".notdef")
            pen = _Pen(self.gs)
            self.gs[name].draw(pen)
            g = self.cache[ch] = (pen.ops, self.adv[name][0])
        return g

    def width(self, s, size):
        return sum(self.glyph(ch)[1] for ch in s) * size / self.upm

    def path(self, c, s, x, y, size):
        k = size / self.upm
        for ch in s:
            ops, adv = self.glyph(ch)
            for op in ops:
                if op[0] == "m":
                    c.move_to(x + op[1][0] * k, y - op[1][1] * k)
                elif op[0] == "l":
                    c.line_to(x + op[1][0] * k, y - op[1][1] * k)
                elif op[0] == "c":
                    c.curve_to(x + op[1][0] * k, y - op[1][1] * k, x + op[2][0] * k,
                               y - op[2][1] * k, x + op[3][0] * k, y - op[3][1] * k)
                else:
                    c.close_path()
            x += adv * k


_fonts = {}


def font(name="bold"):
    if name not in _fonts:
        _fonts[name] = Font(os.path.join(FONT_DIR, f"Fredoka-{name}.ttf"))
    return _fonts[name]


def text(c, s, x, y, size=60, col=INK, align="c", a=1.0, weight="bold", halo=None, halo_w=10):
    """Draw one line with its baseline at y. align is l, c or r."""
    if a <= 0 or not s:
        return
    f = font(weight)
    w = f.width(s, size)
    x0 = x - (w / 2 if align == "c" else w if align == "r" else 0)
    c.new_path()
    f.path(c, s, x0, y, size)
    if halo:
        c.set_source_rgba(*halo, a)
        c.set_line_width(halo_w)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke_preserve()
    c.set_source_rgba(*col, a)
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.fill()


def wrap(s, size, width, weight="bold"):
    f = font(weight)
    out, line = [], ""
    for word in s.split():
        t = (line + " " + word).strip()
        if f.width(t, size) > width and line:
            out.append(line); line = word
        else:
            line = t
    if line:
        out.append(line)
    return out


def para(c, s, x, y, size, width, col=INK, align="c", a=1.0, lead=1.22, weight="bold", halo=None):
    lines = wrap(s, size, width, weight)
    for i, l in enumerate(lines):
        text(c, l, x, y + i * size * lead, size, col, align, a, weight, halo)
    return len(lines) * size * lead


# Shapes. Soft ink outlines, flat colour.
def setc(c, col, a=1.0):
    c.set_source_rgba(*col, a)


def ink(c, fill=None, lw=5.0, stroke=INK, a=1.0):
    if fill is not None:
        setc(c, fill, a)
        if lw:
            c.fill_preserve()
        else:
            c.fill()
    if lw:
        setc(c, stroke, a)
        c.set_line_width(lw)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.stroke()
    else:
        c.new_path()


def rr(c, x, y, w, h, r=14):
    r = min(r, w / 2, h / 2)
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


def ell(c, x, y, rx, ry=None):
    ry = rx if ry is None else ry
    c.save(); c.translate(x, y); c.scale(max(abs(rx), 1e-3), max(abs(ry), 1e-3))
    c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi)
    c.restore()


def poly(c, pts, close=True):
    c.new_sub_path()
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    if close:
        c.close_path()


def curve(c, pts, close=False):
    """Catmull-Rom through points."""
    n = len(pts)
    c.new_sub_path()
    c.move_to(*pts[0])
    rng = range(n if close else n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (close or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (close or i < n - 2) else p2
        c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                   p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    if close:
        c.close_path()


def line(c, x0, y0, x1, y1, col=INK, lw=5, a=1.0, dash=None):
    c.new_path()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    if dash:
        c.set_dash(dash)
    setc(c, col, a); c.set_line_width(lw)
    c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
    c.set_dash([])


def vgrad(c, y0, y1, stops):
    g = cairo.LinearGradient(0, y0, 0, y1)
    for p, col in stops:
        g.add_color_stop_rgba(p, *col, 1)
    c.set_source(g)


def fill_bg(c, stops):
    vgrad(c, 0, H, stops)
    c.rectangle(-60, -60, W + 120, H + 120); c.fill()


def glow(c, x, y, r, col, a=0.5):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a)
    g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g)
    c.arc(x, y, r, 0, 2 * math.pi); c.fill()


class at:
    """with at(c, x, y, s, rot): draw in local coordinates."""
    def __init__(self, c, x=0, y=0, s=1, rot=0, sx=None, a=None):
        self.c, self.x, self.y, self.s, self.rot, self.sx = c, x, y, s, rot, sx
    def __enter__(self):
        c = self.c
        c.save(); c.translate(self.x, self.y)
        if self.rot:
            c.rotate(self.rot)
        sy = self.s if abs(self.s) > 1e-3 else 1e-3
        sx = self.s if self.sx is None else self.sx
        c.scale(sx if abs(sx) > 1e-3 else 1e-3, sy)
        return c
    def __exit__(self, *e):
        self.c.restore()


_surfaces = {}


def cached(key, draw, w=W, h=H):
    """Paintings that do not change are drawn once per worker and reused."""
    s = _surfaces.get(key)
    if s is None:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(s)
        draw(ctx)
        _surfaces[key] = s
    return s


def blit(c, key, draw, x=0, y=0, a=1.0, w=W, h=H):
    s = cached(key, draw, w, h)
    c.set_source_surface(s, x, y)
    if a >= 1:
        c.paint()
    else:
        c.paint_with_alpha(a)


# Skies and land
SKIES = {
    "day": [(0, hexc("5fa8e8")), (0.45, hexc("a8d8f0")), (0.7, hexc("fdf0c8"))],
    "sunset": [(0, hexc("3b3a9c")), (0.32, hexc("c1608e")), (0.55, hexc("f39a4f")), (0.72, hexc("fbd67e"))],
    "dusk": [(0, hexc("1b2a78")), (0.4, hexc("5a3a8c")), (0.72, hexc("d97f6a"))],
    "night": [(0, hexc("121a55")), (0.55, hexc("1b36a8")), (0.8, hexc("3a4fb8"))],
    "gold": [(0, hexc("f6c56f")), (0.5, hexc("fbe0a8")), (0.75, hexc("fff3d6"))],
    "winter": [(0, hexc("4d6fb5")), (0.5, hexc("a9c3e4")), (0.75, hexc("e6edf7"))],
    "storm": [(0, hexc("3a4a78")), (0.5, hexc("6f83a8")), (0.75, hexc("b8c6dc"))],
}


def sky(c, kind="day"):
    fill_bg(c, SKIES[kind])


def sun(c, x, y, r=70, col=hexc("ffe27a")):
    glow(c, x, y, r * 3.2, col, 0.55)
    ell(c, x, y, r); ink(c, col, 0)


def cloud(c, x, y, s=1.0, col=WHITE, a=0.92):
    with at(c, x, y, s):
        c.new_path()
        for dx, dy, r in ((-80, 8, 42), (-30, -14, 58), (34, -6, 50), (84, 12, 34)):
            ell(c, dx, dy, r)
        rr(c, -115, 6, 230, 44, 22)
        setc(c, col, a); c.set_fill_rule(cairo.FILL_RULE_WINDING); c.fill()


def clouds(c, t, n=4, seed=3, col=WHITE, a=0.9, top=70, bottom=320):
    r = random.Random(seed)
    for i in range(n):
        x0, y, s, v = r.uniform(0, W + 300), r.uniform(top, bottom), r.uniform(0.6, 1.25), r.uniform(4, 11)
        x = (x0 + t * v) % (W + 400) - 200
        cloud(c, x, y, s, col, a)


def hill(c, pts, col, base=H + 40, lw=0):
    curve(c, pts)
    c.line_to(pts[-1][0], base); c.line_to(pts[0][0], base); c.close_path()
    ink(c, col, lw)


def tree(c, x, y, s=1.0, col=LEAF, seed=0, bare=False):
    with at(c, x, y, s):
        c.new_path()
        poly(c, [(-11, 0), (-7, -70), (7, -70), (11, 0)]); ink(c, WOODD, 4)
        if bare:
            for a, l in ((-0.6, 56), (0.5, 62), (-0.1, 78)):
                line(c, 0, -60, math.sin(a) * l, -60 - math.cos(a) * l, WOODD, 7)
            return
        r = random.Random(seed)
        c.new_path()
        for dx, dy, q in ((-34, -96, 42), (32, -98, 44), (0, -136, 50)):
            ell(c, dx + r.uniform(-4, 4), dy + r.uniform(-4, 4), q)
        setc(c, INK); c.set_line_width(9); c.stroke_preserve()
        setc(c, col); c.fill()
        ell(c, -14, -132, 24, 16); ink(c, mix(col, WHITE, 0.25), 0)


def pine(c, x, y, s=1.0, col=hexc("2f7a4a"), snow=False):
    with at(c, x, y, s):
        poly(c, [(-8, 0), (-8, -26), (8, -26), (8, 0)]); ink(c, WOODD, 4)
        for i in range(3):
            yy = -24 - i * 40; w = 58 - i * 12
            poly(c, [(-w, yy), (0, yy - 68), (w, yy)]); ink(c, SNOW if snow else col, 4)


def fence(c, x0, x1, y, s=1.0, col=WOOD):
    n = int((x1 - x0) / (90 * s))
    for k in (-34, -14):
        rr(c, x0, y + k * s, x1 - x0, 11 * s, 4); ink(c, col, 3)
    for i in range(n + 1):
        x = x0 + i * 90 * s
        rr(c, x - 8 * s, y - 52 * s, 16 * s, 56 * s, 5); ink(c, mix(col, WOODD, 0.4), 3.5)


def scatter(c, n, seed, x0, x1, y0, y1, r0, r1, col, a=1.0):
    rng = random.Random(seed)
    setc(c, col, a)
    for _ in range(n):
        c.arc(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(r0, r1), 0, 7); c.fill()


def snowfall(c, t, n=70, seed=5, wind=30, a=0.9, speed=1.0):
    rng = random.Random(seed)
    setc(c, WHITE, a)
    for _ in range(n):
        x0, y0, r, v, ph = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2.5, 7), rng.uniform(70, 150), rng.uniform(0, 6)
        x = (x0 + t * wind * speed + math.sin(t + ph) * 18) % W
        y = (y0 + t * v * speed) % H
        c.arc(x, y, r, 0, 7); c.fill()


def stars(c, n=90, seed=2, t=0):
    rng = random.Random(seed)
    for _ in range(n):
        x, y, r, ph = rng.uniform(0, W), rng.uniform(0, 620), rng.uniform(1, 3), rng.uniform(0, 6)
        setc(c, WHITE, 0.5 + 0.4 * math.sin(t * 2 + ph))
        c.arc(x, y, r, 0, 7); c.fill()


# Words on screen
def panel(c, x, y, w, h, fill=PAPER, a=1.0, r=26, lw=6):
    rr(c, x + 6, y + 9, w, h, r); setc(c, INK, 0.16 * a); c.fill()
    rr(c, x, y, w, h, r); ink(c, fill, lw, INK, a)


def wordcard(c, s, cx, cy, size=64, w=1100, a=1.0, fill=PAPER, col=INK, slide=0.0):
    """A paper card holding one thought. a and slide ease it in."""
    if a <= 0:
        return
    lines = wrap(s, size, w - 80)
    h = len(lines) * size * 1.2 + 58
    tw = max(font().width(l, size) for l in lines) + 90
    y = cy - h / 2 + (1 - slide) * 26 if slide else cy - h / 2
    panel(c, cx - tw / 2, y, tw, h, fill, a)
    for i, l in enumerate(lines):
        text(c, l, cx, y + 26 + size * 0.92 + i * size * 1.2, size, col, "c", a)


def sign(c, x, y, s, lines, rot=0.0, sizes=None, w=520, h=None, post=False, cols=None, a=1.0):
    """Wooden sign with ink lettering, hanging or on a post."""
    sizes = sizes or [64] * len(lines)
    h = h or sum(z * 1.22 for z in sizes) + 56
    with at(c, x, y, s, rot):
        if post:
            rr(c, -13, h / 2 - 8, 26, 240, 7); ink(c, WOODD, 5, INK, a)
        rr(c, -w / 2 + 6, -h / 2 + 9, w, h, 20); setc(c, INK, 0.2 * a); c.fill()
        rr(c, -w / 2, -h / 2, w, h, 20); ink(c, WOOD, 6, INK, a)
        for i in range(1, 4):
            yy = -h / 2 + h * i / 4
            line(c, -w / 2 + 18, yy, w / 2 - 18, yy + (i - 2) * 2, WOODD, 2.5, 0.35 * a)
        for dx in (-1, 1):
            for dy in (-1, 1):
                ell(c, dx * (w / 2 - 20), dy * (h / 2 - 18), 6); ink(c, WOODD, 2, INK, a)
        yy = -h / 2 + 22
        for i, l in enumerate(lines):
            yy += sizes[i] * 1.08
            text(c, l, 0, yy, sizes[i], (cols[i] if cols else INK), "c", a)
            yy += sizes[i] * 0.14


def hanging(c, x, y, s, lines, t, t0=0.0, **kw):
    """A sign swinging in on two ropes; settles over about a second."""
    k = ramp(t, t0, 1.1)
    drop = (1 - eout(k)) * -520
    swing = math.sin((t - t0) * 5.2) * 0.13 * (1 - smooth(ramp(t, t0, 1.9))) if t >= t0 else 0
    if t < t0:
        return
    h = kw.get("h") or sum(z * 1.22 for z in kw.get("sizes", [64] * len(lines))) + 56
    with at(c, x, y + drop, 1, swing):
        for dx in (-0.32, 0.32):
            line(c, dx * kw.get("w", 520) * s, -1200, dx * kw.get("w", 520) * s, -h / 2 * s, INK, 6)
        sign(c, 0, 0, s, lines, **kw)


def tick(c, x, y, s=1.0, col=LEAF, k=1.0):
    if k <= 0:
        return
    with at(c, x, y, s):
        ell(c, 0, 0, 34); ink(c, col, 5)
        pts = [(-16, 2), (-5, 14), (17, -12)]
        c.new_path(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.move_to(*pts[0])
        if k < 0.5:
            f = k * 2
            c.line_to(lerp(pts[0][0], pts[1][0], f), lerp(pts[0][1], pts[1][1], f))
        else:
            f = (k - 0.5) * 2
            c.line_to(*pts[1]); c.line_to(lerp(pts[1][0], pts[2][0], f), lerp(pts[1][1], pts[2][1], f))
        setc(c, WHITE); c.set_line_width(9); c.stroke()


def cross(c, x, y, s=1.0, k=1.0, col=TOMATO, lw=26):
    """A big painted X that sweeps across."""
    if k <= 0:
        return
    f1, f2 = clamp(k * 2), clamp(k * 2 - 1)
    with at(c, x, y, s):
        for (a, b, f) in (((-100, -100), (100, 100), f1), ((100, -100), (-100, 100), f2)):
            if f <= 0:
                continue
            bx, by = lerp(a[0], b[0], f), lerp(a[1], b[1], f)
            line(c, a[0], a[1], bx, by, INK, lw + 10)
            line(c, a[0], a[1], bx, by, col, lw)


def stamp(c, s, x, y, size=84, rot=-0.12, k=1.0, col=TOMATO):
    if k <= 0:
        return
    z = lerp(1.7, 1.0, eout(k))
    w = font().width(s, size) + 70
    with at(c, x, y, z, rot):
        rr(c, -w / 2, -size * 0.85, w, size * 1.5, 14)
        setc(c, PAPER, 0.92 * min(1, k * 2)); c.fill_preserve()
        setc(c, col, min(1, k * 2)); c.set_line_width(9); c.stroke()
        text(c, s, 0, size * 0.3, size, col, "c", min(1, k * 2))


def pin(c, x, y, s=1.0, col=TOMATO):
    with at(c, x, y, s):
        c.new_path(); c.move_to(0, 0)
        c.curve_to(-14, -26, -36, -40, -36, -66)
        c.curve_to(-36, -112, 36, -112, 36, -66)
        c.curve_to(36, -40, 14, -26, 0, 0); c.close_path()
        ink(c, col, 5)
        ell(c, 0, -68, 13); ink(c, CREAM, 3)


def tomato(c, x, y, r=30, ripe=1.0):
    with at(c, x, y, r / 30):
        ell(c, 0, 0, 30, 27); ink(c, mix(LEAF, TOMATO, ripe), 3.5)
        ell(c, -11, -9, 7, 5); ink(c, WHITE, 0, a=0.45)
        for a in (0, 1.25, 2.5, 3.75, 5):
            poly(c, [(0, -27), (math.cos(a) * 15, -27 + math.sin(a) * 7), (math.cos(a + .3) * 5, -24 + math.sin(a) * 2)])
            ink(c, LEAF, 2)


def coin(c, x, y, r=26):
    ell(c, x, y, r); ink(c, GOLD, 4)
    text(c, "$", x, y + r * 0.42, r * 1.2, WOODD, "c")


def star(c, x, y, r=40, col=GOLD, rot=0.0, lw=4):
    pts = []
    for i in range(10):
        q = r if i % 2 == 0 else r * 0.46
        a = -math.pi / 2 + i * math.pi / 5 + rot
        pts.append((x + math.cos(a) * q, y + math.sin(a) * q))
    poly(c, pts); ink(c, col, lw)


def counter(v):
    return f"{int(round(v)):,}"
