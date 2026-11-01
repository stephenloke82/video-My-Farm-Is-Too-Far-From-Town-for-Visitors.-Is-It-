"""People, animals, vehicles and farm props. Everything stands on its origin point."""
import math, random
import cairo
from toon import *

SKINS = [hexc(h) for h in ("f4c9a0", "e5ae82", "c98a5e", "a06a44", "7a4e30", "f7d7b5")]
HAIRS = [hexc(h) for h in ("3a2a20", "6b4426", "b5763a", "1f1b2a", "8c8c94", "d8a84e")]
SHIRTS = [TOMATO, SKY, LEAF, GOLD, PLUM, TEAL, hexc("e77fa8"), hexc("3e7fd1")]
PANTS = [hexc("33427a"), hexc("5a4632"), hexc("3f6a5a"), hexc("6b5a8c")]

DOT = dict(skin=hexc("f4c9a0"), hair=hexc("8a4f2a"), shirt=CREAM, pants=hexc("3560c0"),
           hat="straw", overalls=True, boots=hexc("7a4a28"), hairstyle="bob")
STRANGER = dict(skin=hexc("e5ae82"), hair=hexc("3a2a20"), shirt=hexc("c4553a"), pants=hexc("33427a"),
                hat="cap", capcol=SKY, boots=hexc("5a4632"), hairstyle="short")
FARMER = dict(skin=hexc("f0c098"), hair=hexc("8c8c94"), shirt=hexc("6d8fbe"), pants=hexc("5a4632"),
              hat="cap", capcol=LEAF, boots=hexc("5a4632"), hairstyle="short")
KNUTUR = dict(skin=hexc("f4d2b4"), hair=hexc("b5763a"), shirt=hexc("3e7fd1"), pants=hexc("33427a"),
              hat=None, boots=hexc("5a4632"), hairstyle="short", beard=True)
HELENA = dict(skin=hexc("f7d7b5"), hair=hexc("d8a84e"), shirt=LEAF, pants=hexc("5a4632"),
              hat=None, boots=hexc("5a4632"), hairstyle="long")

POSES = {  # shoulder and elbow angles for left and right, degrees from hanging straight down
    "idle": (12, 8, 12, 8), "wave": (14, 8, 150, 24), "open": (58, 28, 58, 28),
    "point_r": (12, 8, 98, 6), "point_l": (98, 6, 12, 8), "hips": (42, -105, 42, -105),
    "think": (12, 8, 42, 118), "cheer": (150, 16, 150, 16), "shrug": (52, 74, 52, 74),
    "carry": (62, 32, 62, 32), "up_r": (12, 8, 135, 10), "look": (12, 8, 118, 92),
}


def crowd_look(seed):
    r = random.Random(seed)
    return dict(skin=r.choice(SKINS), hair=r.choice(HAIRS), shirt=r.choice(SHIRTS), pants=r.choice(PANTS),
                hat=r.choice([None, None, "beanie", "cap", "sun"]), capcol=r.choice(SHIRTS),
                boots=hexc("4a3a30"), hairstyle=r.choice(["short", "long", "bun"]))


def _limb(c, pts, col, w):
    for colr, lw in ((INK, w + 8), (col, w)):
        c.new_path(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        setc(c, colr); c.set_line_width(lw); c.stroke()


def _arm(c, sx, sy, side, sh, el, col, skin, length=62):
    a = math.radians(sh) * side
    ex, ey = sx + math.sin(a) * length, sy + math.cos(a) * length
    b = a + math.radians(el) * side
    hx, hy = ex + math.sin(b) * length * 0.9, ey + math.cos(b) * length * 0.9
    _limb(c, [(sx, sy), (ex, ey), (hx, hy)], col, 22)
    ell(c, hx, hy, 15); ink(c, skin, 4)
    return hx, hy


def face(c, look, t, seed, mouth, look_x, mood):
    eye_y = -6
    blink = (t * 0.31 + seed * 0.37) % 1.0 < 0.035
    for side in (-1, 1):
        ex = side * 24 + look_x
        if blink or mood == "happy":
            c.new_path()
            c.arc(ex, eye_y + 3, 8.5, math.pi * 1.1, math.pi * 1.9)
            setc(c, INK); c.set_line_width(4.5); c.stroke()
        else:
            ell(c, ex, eye_y, 7.5, 9); ink(c, INK, 0)
            ell(c, ex + 2.5, eye_y - 3, 2.6); ink(c, WHITE, 0)
        if mood == "sad":
            line(c, ex - 11, eye_y - 16 - side * -4, ex + 11, eye_y - 16 + side * -4, INK, 4)
        elif mood == "wow":
            line(c, ex - 9, eye_y - 22, ex + 9, eye_y - 22, INK, 4)
        else:
            line(c, ex - 9, eye_y - 17, ex + 9, eye_y - 18, INK, 3.5, 0.75)
    ell(c, -36 + look_x, 14, 13, 8); ink(c, TOMATO, 0, a=0.28)
    ell(c, 36 + look_x, 14, 13, 8); ink(c, TOMATO, 0, a=0.28)
    mx, my = look_x * 1.2, 26
    if mouth > 0.08:
        o = 4 + 17 * mouth
        wd = 15 - 3 * mouth
        ell(c, mx, my + o * 0.3, wd, o); ink(c, hexc("7a2432"), 3.5)
        ell(c, mx, my + o * 1.0, wd * 0.6, o * 0.32); ink(c, TOMATO, 0)
    elif mood == "sad":
        c.new_path(); c.arc(mx, my + 14, 13, math.pi * 1.2, math.pi * 1.8)
        setc(c, INK); c.set_line_width(4.5); c.stroke()
    elif mood == "wow":
        ell(c, mx, my + 3, 9, 11); ink(c, hexc("7a2432"), 3.5)
    else:
        c.new_path(); c.arc(mx, my - 3, 15, math.pi * 0.14, math.pi * 0.86)
        setc(c, INK); c.set_line_width(4.5); c.stroke()


def hat(c, look):
    h = look.get("hat")
    if h == "straw":
        ell(c, 0, -46, 96, 20); ink(c, GOLD, 5)
        c.new_path()
        c.move_to(-54, -48); c.curve_to(-54, -118, 54, -118, 54, -48); c.close_path(); ink(c, GOLD, 5)
        c.new_path()
        c.move_to(-54, -48); c.curve_to(-50, -60, 50, -60, 54, -48)
        c.line_to(53, -66); c.curve_to(46, -80, -46, -80, -53, -66); c.close_path(); ink(c, TOMATO, 4)
        for i in range(-3, 4):
            line(c, i * 21, -39 + abs(i) * 1.5, i * 25, -33 + abs(i), WOODD, 2, 0.45)
    elif h == "sun":
        ell(c, 0, -44, 82, 15); ink(c, WHEAT, 4)
        c.new_path(); c.move_to(-46, -46); c.curve_to(-46, -96, 46, -96, 46, -46); c.close_path(); ink(c, WHEAT, 4)
    elif h == "cap":
        col = look.get("capcol", SKY)
        c.new_path(); c.move_to(-60, -30); c.curve_to(-60, -104, 60, -104, 60, -30); c.close_path(); ink(c, col, 5)
        c.new_path(); c.move_to(30, -36); c.curve_to(60, -44, 92, -40, 96, -28); c.curve_to(80, -24, 50, -24, 30, -28); c.close_path()
        ink(c, mix(col, INK, 0.25), 4)
    elif h == "beanie":
        col = look.get("capcol", TOMATO)
        c.new_path(); c.move_to(-60, -26); c.curve_to(-60, -102, 60, -102, 60, -26); c.close_path(); ink(c, col, 5)
        rr(c, -64, -40, 128, 24, 11); ink(c, mix(col, WHITE, 0.35), 4)
        ell(c, 0, -98, 13); ink(c, CREAM, 4)
    elif h == "grad":
        rr(c, -48, -66, 96, 34, 6); ink(c, INK, 4)
        poly(c, [(0, -102), (88, -72), (0, -44), (-88, -72)]); ink(c, hexc("2a2f55"), 5)
        line(c, 0, -74, 74, -60, GOLD, 5); ell(c, 76, -46, 7, 14); ink(c, GOLD, 3)


def person(c, x, y, s, look, t=0.0, pose="idle", mouth=0.0, flip=False, walk=None, seed=1,
           look_x=0, mood=None, bob=True, sit=False, gest=0.0, carry=None):
    """Full figure, about 380 units tall at s=1, standing on (x, y)."""
    sx, sy = 12 if False else 0, 0
    with at(c, x, y, s, sx=-s if flip else s):
        if not sit:
            ell(c, 0, 4, 78, 13); ink(c, INK, 0, a=0.18)
        bounce = -abs(math.sin(walk * math.pi)) * 8 if walk is not None else (math.sin(t * 2.1 + seed) * 2.5 if bob else 0)
        # legs
        ph = math.sin(walk * math.pi * 2) if walk is not None else 0
        for side in (-1, 1):
            swing = ph * side * 26
            if sit:
                continue
            hipx, footx = side * 22, side * 26 + swing
            lift = max(0, ph * side) * 12
            _limb(c, [(hipx, -128 + bounce), (footx, -22 - lift)], look["pants"], 30)
            rr(c, footx - 22, -24 - lift, 58, 25, 11); ink(c, look.get("boots", SOIL), 4)
        c.translate(0, bounce)
        p = POSES[pose]
        wig = math.sin(t * 3.1 + seed) * 9 * gest
        wig2 = math.sin(t * 2.3 + seed + 1) * 9 * gest
        # back arm
        swing_a = ph * 16 if walk is not None else 0
        _arm(c, -40, -222, -1, p[0] + wig + swing_a, p[1], look["shirt"], look["skin"])
        # torso
        rr(c, -48, -244, 96, 132, 30); ink(c, look["shirt"], 5)
        if look.get("overalls"):
            rr(c, -42, -188, 84, 80, 14); ink(c, look["pants"], 4.5)
            rr(c, -34, -232, 16, 50, 6); ink(c, look["pants"], 3.5)
            rr(c, 18, -232, 16, 50, 6); ink(c, look["pants"], 3.5)
            ell(c, -26, -186, 6); ink(c, GOLD, 2.5); ell(c, 26, -186, 6); ink(c, GOLD, 2.5)
            rr(c, -21, -170, 42, 30, 7); ink(c, mix(look["pants"], WHITE, 0.14), 3)
        # neck and head
        rr(c, -15, -262, 30, 28, 8); ink(c, look["skin"], 4)
        with at(c, 0, -320, 1):
            hs = look.get("hairstyle", "short")
            if hs in ("long", "bob") and look.get("hair"):
                n = 84 if hs == "long" else 44
                rr(c, -68, -30, 136, n + 30, 34); ink(c, look["hair"], 5)
            if hs == "bun":
                ell(c, 0, -72, 26); ink(c, look["hair"], 5)
            ell(c, 0, 0, 62, 60); ink(c, look["skin"], 5.5)
            if look.get("beard"):
                c.new_path(); c.move_to(-60, 8); c.curve_to(-54, 76, 54, 76, 60, 8)
                c.curve_to(40, 26, -40, 26, -60, 8); c.close_path(); ink(c, look["hair"], 4)
            if not look.get("hat"):
                c.new_path(); c.move_to(-62, -6); c.curve_to(-66, -82, 66, -82, 62, -6)
                c.curve_to(40, -38, -30, -44, -62, -6); c.close_path(); ink(c, look["hair"], 4.5)
            face(c, look, t, seed, mouth, look_x, mood)
            hat(c, look)
        # front arm
        hand = _arm(c, 40, -222, 1, p[2] + wig2 - swing_a, p[3], look["shirt"], look["skin"])
        if carry:
            carry(c, *hand)


def dot(c, x, y, s, t, mouth, pose="open", flip=False, walk=None, look_x=0, mood=None):
    person(c, x, y, s, DOT, t, pose, mouth, flip, walk, 7, look_x, mood, gest=clamp(mouth * 1.6))


def crowd(c, x0, x1, y, s, n, t, seed=0, walkv=None, pose=None, dy=26):
    """A row of visitors. With walkv they stroll to the right at that speed."""
    for i in range(n):
        lk = crowd_look(seed + i * 3 + 1)
        f = (i + 0.5) / n
        x = lerp(x0, x1, f)
        yy = y + (i % 3) * dy - dy
        sc = s * (0.9 + 0.1 * ((i * 7) % 3))
        p = pose or ["idle", "wave", "point_r", "open"][(seed + i) % 4]
        if walkv is not None:
            person(c, x, yy, sc, lk, t, "idle", walk=(t * 1.4 + i * 0.37), seed=i)
        else:
            person(c, x, yy, sc, lk, t, p, seed=i)


# Vehicles
def wheel(c, x, y, r, spin, tyre=INK):
    ell(c, x, y, r); ink(c, tyre, 0)
    ell(c, x, y, r * 0.58); ink(c, CREAM, 3)
    for i in range(4):
        a = spin + i * math.pi / 2
        line(c, x, y, x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.5, GREY, 3.5)


def car(c, x, y, s, col=TOMATO, spin=0.0, flip=False, bounce=0.0, driver=None, t=0.0, wave=False):
    """A boxy sedan, facing right. Origin on the road between its wheels."""
    with at(c, x, y, s, sx=-s if flip else s):
        ell(c, 0, 2, 150, 12); ink(c, INK, 0, a=0.18)
        with at(c, 0, bounce, 1):
            c.new_path()
            c.move_to(-146, -30); c.line_to(-140, -74); c.line_to(-90, -80); c.line_to(-52, -132)
            c.line_to(58, -132); c.line_to(98, -82); c.line_to(150, -70); c.line_to(156, -30); c.close_path()
            ink(c, col, 5.5)
            poly(c, [(-44, -122), (-4, -122), (-4, -82), (-78, -82)]); ink(c, hexc("cfe6f5"), 4)
            poly(c, [(6, -122), (52, -122), (82, -82), (6, -82)]); ink(c, hexc("cfe6f5"), 4)
            if driver:
                with at(c, 30, -74, 0.44):
                    ell(c, 0, -30, 60); ink(c, driver["skin"], 5)
                    ell(c, 24, -38, 7, 9); ink(c, INK, 0)
                    hat(c, driver)
            rr(c, -150, -46, 306, 10, 4); ink(c, mix(col, WHITE, 0.3), 0)
            rr(c, 142, -64, 16, 16, 5); ink(c, GOLD, 3)
            rr(c, -152, -62, 12, 16, 4); ink(c, TOMATO, 3)
        wheel(c, -88, -24 + bounce * 0.3, 30, spin)
        wheel(c, 92, -24 + bounce * 0.3, 30, spin)


def jeep(c, x, y, s, spin=0.0, tilt=0.0, bounce=0.0, flip=False, t=0.0, riders=2, col=LEAF):
    """Four-wheel drive with a canvas roof, big tyres and waving passengers."""
    with at(c, x, y, s, sx=-s if flip else s):
        ell(c, 0, 2, 175, 12); ink(c, INK, 0, a=0.18)
        with at(c, 0, bounce, 1, tilt):
            rr(c, -176, -128, 36, 64, 18)
            ink(c, INK, 0)
            ell(c, -170, -96, 34); ink(c, INK, 4); ell(c, -170, -96, 18); ink(c, GREY, 3)
            for i in range(riders):
                xx = -60 + i * 76
                with at(c, xx, -130, 0.42):
                    lk = crowd_look(40 + i)
                    ell(c, 0, -30, 60); ink(c, lk["skin"], 5)
                    ell(c, 22, -38, 7, 9); ink(c, INK, 0)
                    c.new_path(); c.arc(22, -6, 14, 0.3, 2.8); setc(c, INK); c.set_line_width(4.5); c.stroke()
                    if lk.get("hat"):
                        hat(c, lk)
                if i == 1:
                    wv = math.sin(t * 8) * 8
                    _limb(c, [(xx + 22, -112), (xx + 44 + wv, -168)], crowd_look(41)["shirt"], 12)
            c.new_path()
            c.move_to(-158, -60); c.line_to(-150, -118); c.line_to(70, -118); c.line_to(110, -74)
            c.line_to(168, -66); c.line_to(174, -32); c.line_to(-158, -32); c.close_path(); ink(c, col, 5.5)
            poly(c, [(46, -112), (68, -112), (98, -76), (46, -76)]); ink(c, hexc("cfe6f5"), 4)
            rr(c, -170, -176, 262, 16, 8); ink(c, hexc("d9c79a"), 4)
            for xx in (-150, 62):
                line(c, xx, -162, xx, -112, INK, 7)
            rr(c, 166, -60, 14, 18, 5); ink(c, GOLD, 3)
        wheel(c, -96, -36 + bounce * 0.2, 42, spin)
        wheel(c, 108, -36 + bounce * 0.2, 42, spin)


def tractor(c, x, y, s, spin=0.0, flip=False, driver=None):
    with at(c, x, y, s, sx=-s if flip else s):
        ell(c, 0, 2, 150, 12); ink(c, INK, 0, a=0.18)
        rr(c, -40, -124, 170, 66, 12); ink(c, TOMATO, 5)
        rr(c, 112, -158, 12, 40, 4); ink(c, GREY, 4)
        rr(c, -96, -176, 90, 112, 12); ink(c, hexc("cfe6f5"), 5)
        if driver:
            with at(c, -52, -112, 0.46):
                ell(c, 0, -30, 60); ink(c, driver["skin"], 5)
                ell(c, 24, -38, 7, 9); ink(c, INK, 0); hat(c, driver)
        wheel(c, -74, -62, 62, spin)
        wheel(c, 100, -34, 34, spin * 1.8)


# Farm buildings and things
def barn(c, x, y, s=1.0, col=TOMATO, lit=False):
    with at(c, x, y, s):
        poly(c, [(-130, 0), (-130, -150), (-82, -214), (0, -258), (82, -214), (130, -150), (130, 0)]); ink(c, col, 6)
        poly(c, [(-142, -146), (-88, -220), (0, -270), (88, -220), (142, -146), (130, -150), (82, -214), (0, -258), (-82, -214), (-130, -150)])
        ink(c, CREAM, 4)
        rr(c, -60, -118, 120, 118, 4); ink(c, GOLD if lit else CREAM, 5)
        for a, b in (((-60, -118), (60, 0)), ((60, -118), (-60, 0))):
            line(c, a[0], a[1], b[0], b[1], col, 7)
        rr(c, -24, -206, 48, 44, 4); ink(c, GOLD if lit else hexc("cfe6f5"), 4)


def house(c, x, y, s=1.0, wall=PAPER, roof=hexc("6d5a8c"), lit=False, porch=True):
    with at(c, x, y, s):
        rr(c, -120, -150, 240, 150, 4); ink(c, wall, 6)
        poly(c, [(-146, -146), (0, -258), (146, -146)]); ink(c, roof, 6)
        rr(c, 62, -252, 34, 74, 3); ink(c, TOMATO, 5)
        glass = GOLD if lit else hexc("cfe6f5")
        for xx in (-82, 44):
            rr(c, xx, -116, 56, 56, 4); ink(c, glass, 5)
            line(c, xx + 28, -116, xx + 28, -60, INK, 3); line(c, xx, -88, xx + 56, -88, INK, 3)
        rr(c, -22, -96, 46, 96, 4); ink(c, TOMATO, 5)
        if porch:
            rr(c, -136, -8, 272, 14, 4); ink(c, WOOD, 4)


def gate(c, x, y, s=1.0, opn=0.0, col=WOOD):
    """Five-bar farm gate. opn 0 is shut, 1 swung open towards us."""
    w = 300
    with at(c, x, y, s):
        rr(c, -w / 2 - 28, -196, 28, 200, 6); ink(c, WOODD, 5)
        rr(c, w / 2, -196, 28, 200, 6); ink(c, WOODD, 5)
        k = math.cos(smooth(opn) * math.pi * 0.36)
        with at(c, -w / 2, 0, 1, sx=k):
            for i in range(5):
                rr(c, 0, -168 + i * 34, w, 16, 5); ink(c, col, 3.5)
            for xx in (6, w - 22):
                rr(c, xx, -176, 16, 164, 4); ink(c, mix(col, WOODD, 0.5), 3.5)
            c.new_path(); c.set_line_cap(cairo.LINE_CAP_ROUND)
            for clr, lw in ((INK, 21), (col, 13)):
                c.move_to(14, -22); c.line_to(w - 14, -160); setc(c, clr); c.set_line_width(lw); c.stroke()


def greenhouse(c, x, y, s=1.0, w=520, h=200, broken=0.0, glow_a=0.0, grow=1.0):
    """Peaked glasshouse. broken lifts panes out, grow fills it with vines."""
    with at(c, x, y, s):
        if glow_a:
            glow(c, 0, -h * 0.7, w * 0.95, GOLD, 0.55 * glow_a)
        glass = mix(hexc("d6efe6"), hexc("9fb3ab"), broken)
        c.new_path(); poly(c, [(-w / 2, 0), (-w / 2, -h * 0.62), (0, -h), (w / 2, -h * 0.62), (w / 2, 0)])
        ink(c, mix(glass, GOLD, 0.55 * glow_a), 6)
        rng = random.Random(4)
        if grow > 0:
            for i in range(7):
                xx = -w / 2 + (i + 0.5) * w / 7
                top = -h * 0.5 * grow
                line(c, xx, 0, xx, top, LEAF, 7)
                for j in range(3):
                    yy = top * (0.3 + j * 0.3)
                    ell(c, xx + (-1) ** j * 12, yy, 12, 9); ink(c, GRASSD, 2.5)
                    if grow > 0.6:
                        tomato(c, xx - (-1) ** j * 11, yy + 8, 9)
        n = 8
        for i in range(n + 1):
            xx = -w / 2 + i * w / n
            yt = -h + abs(xx) / (w / 2) * h * 0.38
            line(c, xx, 0, xx, yt, PAPER if not broken else WOODD, 5)
        line(c, -w / 2, -h * 0.3, w / 2, -h * 0.3, PAPER if not broken else WOODD, 4)
        poly(c, [(-w / 2, 0), (-w / 2, -h * 0.62), (0, -h), (w / 2, -h * 0.62), (w / 2, 0)])
        ink(c, None, 6)
        if broken > 0.1:
            for (px, py) in ((-120, -120), (60, -150), (150, -80), (-40, -60)):
                poly(c, [(px, py), (px + 34, py - 18), (px + 20, py + 26)]); ink(c, hexc("4d5a58"), 3, a=broken)
        rr(c, -36, -92, 72, 92, 4); ink(c, WOOD, 5)


def corn_row(c, x0, x1, y, h, seed, col=hexc("5aa04a")):
    rng = random.Random(seed)
    x = x0
    while x < x1:
        hh = h * rng.uniform(0.85, 1.1)
        line(c, x, y, x, y - hh, mix(col, INK, 0.2), 5)
        for k in range(3):
            yy = y - hh * (0.35 + k * 0.24)
            side = 1 if k % 2 else -1
            c.new_path(); c.move_to(x, yy)
            c.curve_to(x + side * h * .2, yy - h * .17, x + side * h * .33, yy - h * .1, x + side * h * .42, yy + h * .08)
            c.curve_to(x + side * h * .28, yy - h * .02, x + side * h * .14, yy + h * .03, x, yy + h * .05); c.close_path()
            ink(c, col, 2.5)
        if rng.random() < 0.6:
            ell(c, x + 7, y - hh * 0.55, 8, 20); ink(c, GOLD, 2.5)
        x += h * rng.uniform(0.48, 0.62)


def chicken(c, x, y, s, t, seed=0, flip=False, col=CREAM):
    peck = max(0, math.sin(t * 2.5 + seed)) ** 6
    with at(c, x, y, s, sx=-s if flip else s):
        ell(c, 0, 2, 50, 7); ink(c, INK, 0, a=0.16)
        line(c, -10, -28, -10, 0, GOLD, 6); line(c, 10, -28, 10, 0, GOLD, 6)
        ell(c, 0, -56, 46, 36); ink(c, col, 5)
        poly(c, [(-44, -66), (-74, -96), (-30, -82)]); ink(c, col, 4)
        with at(c, 38, -88 + peck * 40, 1, peck * 0.7):
            ell(c, 0, 0, 22); ink(c, col, 5)
            poly(c, [(20, -4), (42, 3), (20, 10)]); ink(c, GOLD, 3.5)
            ell(c, -2, -26, 8, 10); ink(c, TOMATO, 3); ell(c, 8, -24, 7, 8); ink(c, TOMATO, 3)
            ell(c, 7, -5, 3.5); ink(c, INK, 0)


def horse(c, x, y, s, t, walk=None, flip=False, col=hexc("a8683a")):
    ph = math.sin((walk or 0) * math.pi * 2)
    with at(c, x, y, s, sx=-s if flip else s):
        ell(c, 0, 3, 150, 12); ink(c, INK, 0, a=0.16)
        for lx, off in ((-92, 1), (-68, -1), (72, -1), (98, 1)):
            d = off * ph * 24 if walk is not None else 0
            _limb(c, [(lx, -130), (lx + d, -14)], col, 26)
            rr(c, lx + d - 15, -18, 30, 18, 5); ink(c, INK, 0)
        c.new_path(); c.move_to(-120, -112); c.curve_to(-136, -40, -150, -50, -158, -24)
        line(c, -116, -180, -152, -60, hexc("4a2c18"), 22)
        rr(c, -126, -206, 248, 106, 50); ink(c, col, 5.5)
        c.new_path()
        poly(c, [(82, -190), (120, -280), (168, -278), (130, -160)]); ink(c, col, 5.5)
        rr(c, 112, -300, 104, 60, 24); ink(c, col, 5.5)
        poly(c, [(118, -296), (126, -330), (140, -298)]); ink(c, col, 4.5)
        ell(c, 156, -282, 6.5); ink(c, INK, 0)
        ell(c, 198, -264, 4); ink(c, INK, 0)
        line(c, 112, -296, 74, -196, hexc("4a2c18"), 18)


def cow(c, x, y, s, t, turn=0.0, flip=False):
    with at(c, x, y, s, sx=-s if flip else s):
        ell(c, 0, 3, 130, 12); ink(c, INK, 0, a=0.16)
        for lx in (-84, -56, 62, 88):
            _limb(c, [(lx, -96), (lx, -12)], WHITE, 22)
            rr(c, lx - 13, -14, 26, 15, 4); ink(c, INK, 0)
        rr(c, -116, -174, 224, 104, 44); ink(c, WHITE, 5.5)
        ell(c, -50, -128, 34, 26); ink(c, INK, 0); ell(c, 40, -148, 24, 18); ink(c, INK, 0)
        with at(c, 108, -168, 1, 0):
            for sd in (-1, 1):
                ell(c, sd * 52, -22, 18, 10); ink(c, hexc("f0b8b0"), 4)
            rr(c, -44, -44, 88, 96, 36); ink(c, WHITE, 5.5)
            rr(c, -36, 16, 72, 42, 18); ink(c, hexc("f0b8b0"), 4.5)
            lk = turn * 7
            ell(c, -18 + lk, -12, 7, 9); ink(c, INK, 0); ell(c, 18 + lk, -12, 7, 9); ink(c, INK, 0)


def crate(c, x, y, s=1.0, n=6, ripe=1.0):
    with at(c, x, y, s):
        for i in range(n):
            tomato(c, -56 + (i % 3) * 56, -74 + (i // 3) * -22, 26, ripe)
        rr(c, -86, -70, 172, 70, 6); ink(c, WOOD, 5)
        line(c, -80, -36, 80, -36, WOODD, 3.5, 0.6)


def stand(c, x, y, s=1.0, faded=0.0):
    """Roadside fruit stand with an awning."""
    with at(c, x, y, s):
        for xx in (-166, 150):
            rr(c, xx, -226, 16, 226, 4); ink(c, WOODD, 5)
        rr(c, -180, -106, 360, 106, 8); ink(c, mix(WOOD, GREY, faded * 0.5), 5)
        for i in range(8):
            xx = -180 + i * 45
            colr = mix(TOMATO if i % 2 else CREAM, GREY, faded * 0.6)
            c.new_path(); c.move_to(xx, -262); c.line_to(xx + 45, -262); c.line_to(xx + 45, -216)
            c.curve_to(xx + 34, -198, xx + 11, -198, xx, -216); c.close_path(); ink(c, colr, 4.5)
        rng = random.Random(9)
        for i in range(10):
            ell(c, -130 + i * 29 + rng.uniform(-3, 3), -118 - (i % 2) * 16, 20, 19)
            ink(c, mix(TOMATO if i % 3 else GOLD, GREY, faded * 0.7), 3.5)


def apple(c, x, y, r=18, col=TOMATO):
    ell(c, x, y, r, r * .95); ink(c, col, 3.5)
    line(c, x, y - r * .8, x + 3, y - r * 1.25, WOODD, 3.5)


def durian(c, x, y, s=1.0):
    with at(c, x, y, s):
        pts = []
        for i in range(20):
            a = i * math.pi / 10
            q = 44 if i % 2 else 53
            pts.append((math.cos(a) * q * 0.86, math.sin(a) * q * 1.1))
        poly(c, pts); ink(c, hexc("9db84a"), 4.5)
        for (dx, dy) in ((-14, -18), (14, -6), (-8, 18), (18, 22)):
            ell(c, dx, dy, 3.5); ink(c, GRASSD, 0)
        line(c, 0, -58, 2, -76, WOODD, 7)


def durian_tree(c, x, y, s=1.0):
    with at(c, x, y, s):
        poly(c, [(-20, 0), (-12, -220), (12, -220), (20, 0)]); ink(c, WOODD, 5)
        c.new_path()
        for dx, dy, q in ((-88, -230, 76), (84, -236, 80), (0, -300, 94), (-40, -180, 56), (54, -176, 56)):
            ell(c, dx, dy, q)
        setc(c, INK); c.set_line_width(10); c.stroke_preserve(); setc(c, hexc("3a8a44")); c.fill()
        ell(c, -24, -320, 44, 26); ink(c, GRASS, 0, a=0.5)
        for dx, dy in ((-92, -176), (68, -170), (6, -220)):
            durian(c, dx, dy, 0.55)


def tent(c, x, y, s=1.0, col=GOLD, lit=False):
    with at(c, x, y, s):
        if lit:
            glow(c, 0, -60, 170, GOLD, 0.5)
        poly(c, [(-120, 0), (0, -150), (120, 0)]); ink(c, col, 6)
        poly(c, [(-34, 0), (0, -92), (34, 0)]); ink(c, hexc("7a4a28") if not lit else hexc("ffe9a8"), 5)


def cabin(c, x, y, s=1.0, lit=True):
    with at(c, x, y, s):
        if lit:
            glow(c, 0, -80, 260, GOLD, 0.5)
        rr(c, -130, -130, 260, 130, 6); ink(c, WOOD, 6)
        for i in range(1, 5):
            line(c, -126, -130 + i * 26, 126, -130 + i * 26, WOODD, 3.5)
        poly(c, [(-156, -124), (0, -226), (156, -124)]); ink(c, hexc("6a4a3a"), 6)
        rr(c, -96, -100, 62, 58, 4); ink(c, GOLD if lit else hexc("cfe6f5"), 5)
        rr(c, 30, -100, 56, 100, 4); ink(c, TOMATO, 5)
        rr(c, 62, -214, 30, 62, 4); ink(c, GREY, 5)


def phone(c, x, y, s=1.0):
    """Blank phone; returns screen rect in parent coordinates for scale s."""
    w, h = 340, 620
    with at(c, x, y, s):
        rr(c, -w / 2, -h / 2, w, h, 44); ink(c, INK, 6)
        rr(c, -w / 2 + 16, -h / 2 + 18, w - 32, h - 36, 28); ink(c, PAPER, 0)
    return x - (w / 2 - 16) * s, y - (h / 2 - 18) * s, (w - 32) * s, (h - 36) * s


def clock(c, x, y, r, frac, col=CREAM):
    """Round clock face, hand at frac of a turn."""
    ell(c, x, y, r); ink(c, col, 6)
    for i in range(12):
        a = i * math.pi / 6
        line(c, x + math.cos(a) * r * .8, y + math.sin(a) * r * .8, x + math.cos(a) * r * .9, y + math.sin(a) * r * .9, INK, 4)
    a = frac * 2 * math.pi - math.pi / 2
    line(c, x, y, x + math.cos(a) * r * .68, y + math.sin(a) * r * .68, TOMATO, 8)
    line(c, x, y, x + math.cos(a / 12) * r * .45, y + math.sin(a / 12) * r * .45, INK, 8)
    ell(c, x, y, 8); ink(c, INK, 0)


def bubble(c, x, y, w, h, tail=None, fill=PAPER, thought=False, a=1.0):
    """Speech or thought bubble. tail is the point it aims at."""
    panel(c, x, y, w, h, fill, a, r=46)
    if tail:
        tx, ty = tail
        bx = clamp(tx, x + 60, x + w - 60)
        by = y + h if ty > y + h else y
        if thought:
            for i, f in enumerate((0.3, 0.58, 0.82)):
                ell(c, lerp(bx, tx, f), lerp(by, ty, f), 20 - i * 5); ink(c, fill, 4.5, INK, a)
        else:
            poly(c, [(bx - 26, by - 5), (tx, ty), (bx + 26, by - 5)]); setc(c, fill, a); c.fill()
            c.new_path(); c.move_to(bx - 26, by); c.line_to(tx, ty); c.line_to(bx + 26, by)
            setc(c, INK, a); c.set_line_width(6); c.stroke()
