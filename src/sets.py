"""Painted backgrounds, cached once per worker, with moving skies on top."""
import math, random
from toon import *
from cast import *

SEASON_LAND = {
    "day": (hexc("9cc88a"), hexc("7fbb62"), hexc("6fb04d")),
    "sunset": (hexc("a46a7e"), hexc("b07a4e"), hexc("8c7a3e")),
    "gold": (hexc("d8c07a"), hexc("c3b25e"), hexc("a9a448")),
    "dusk": (hexc("4a3a78"), hexc("3f4a6e"), hexc("34506a")),
    "night": (hexc("1e2f78"), hexc("1a3a68"), hexc("173f58")),
}


def _rolling(c, kind):
    a, b, d = SEASON_LAND[kind]
    hill(c, [(-60, 640), (300, 560), (760, 620), (1200, 540), (1980, 620)], a)
    hill(c, [(-60, 720), (420, 660), (900, 720), (1400, 650), (1980, 700)], b)
    hill(c, [(-60, 830), (500, 770), (1100, 820), (1980, 770)], d)


def farmland(c, t, kind="day", seed=1, sunxy=(1560, 200), trees=True):
    """Rolling country with drifting clouds."""
    key = f"sky-{kind}"
    def s(x):
        sky(x, kind)
        if kind in ("night",):
            stars(x)
    blit(c, key, s)
    if kind in ("night", "dusk"):
        stars(c, 60, seed, t)
    elif sunxy:
        sun(c, *sunxy)
    if kind != "night":
        clouds(c, t, 4, seed, a=0.75 if kind != "day" else 0.92)
    def land(x):
        _rolling(x, kind)
        if trees:
            r = random.Random(seed)
            for _ in range(11):
                tree(x, r.uniform(0, W), r.uniform(600, 690), r.uniform(0.32, 0.5),
                     mix(LEAF, SEASON_LAND[kind][2], 0.35), r.randint(0, 99))
    blit(c, f"land-{kind}-{seed}", land)


def _iowa_land(x, kind):
    a, b, d = SEASON_LAND[kind]
    hill(x, [(-60, 610), (380, 560), (900, 600), (1400, 545), (1980, 590)], a)
    for i in range(9):
        tree(x, 40 + i * 215, 590 - (i % 3) * 16, 0.42, mix(LEAF, d, 0.3), i)
    house(x, 1320, 660, 0.72)
    barn(x, 1610, 668, 0.82)
    hill(x, [(-60, 660), (500, 640), (1100, 660), (1980, 650)], b)
    # the ball field cut out of the corn
    ell(x, 560, 790, 470, 150); ink(x, GRASS if kind == "day" else d, 5)
    poly(x, [(560, 690), (800, 790), (560, 880), (320, 790)]); ink(x, DIRT, 4)
    poly(x, [(560, 720), (720, 790), (560, 850), (400, 790)]); ink(x, GRASS if kind == "day" else d, 3)
    for (px, py) in ((560, 690), (800, 790), (560, 880), (320, 790)):
        rr(x, px - 12, py - 8, 24, 16, 3); ink(x, WHITE, 3)
    corn_row(x, 1040, 2000, 720, 66, 2)
    corn_row(x, 1080, 2000, 790, 86, 3)
    corn_row(x, 1120, 2000, 880, 112, 4)
    corn_row(x, 1160, 2000, 1000, 150, 5)
    hill(x, [(-60, 980), (600, 960), (1200, 1000), (1980, 985)], mix(d, INK, 0.08))


def iowa(c, t, kind="day"):
    blit(c, f"sky-{kind}", lambda x: sky(x, kind))
    if kind == "sunset":
        sun(c, 900, 500, 90, hexc("ffd27a"))
    else:
        sun(c, 330, 170)
    clouds(c, t, 4, 8, a=0.9)
    blit(c, f"iowa-{kind}", lambda x: _iowa_land(x, kind))


def _road_land(x, kind):
    a, b, d = SEASON_LAND[kind]
    hill(x, [(-60, 560), (420, 500), (980, 540), (1500, 490), (1980, 540)], a)
    hill(x, [(-60, 620), (500, 570), (1200, 610), (1980, 570)], b)
    hill(x, [(-60, 690), (700, 650), (1980, 680)], d)
    # a road winding from our feet to the far hills
    left = [(1040, 1100), (1120, 960), (1000, 840), (880, 760), (940, 700), (1010, 660), (970, 625), (940, 600)]
    right = [(1560, 1100), (1440, 960), (1160, 840), (960, 760), (985, 700), (1035, 660), (982, 625), (948, 600)]
    curve(x, left)
    pts = list(reversed(right))
    for p in pts:
        x.line_to(*p)
    x.close_path(); ink(x, DIRT, 4)
    for f in (0.0, 0.14, 0.3, 0.46):
        pass
    r = random.Random(11)
    for _ in range(16):
        side = r.choice((-1, 1))
        tree(x, 1000 + side * r.uniform(280, 980), r.uniform(640, 760), r.uniform(0.4, 0.8),
             mix(LEAF, d, 0.25), r.randint(0, 99))


def longroad(c, t, kind="day", sunxy=(980, 260)):
    blit(c, f"sky-{kind}", lambda x: sky(x, kind))
    if sunxy:
        sun(c, *sunxy)
    clouds(c, t, 4, 5, a=0.85)
    blit(c, f"road-{kind}", lambda x: _road_land(x, kind))


def _winter_land(x):
    poly(x, [(-60, 640), (220, 400), (420, 540), (640, 360), (880, 560), (1120, 430), (1400, 580), (1680, 420), (1980, 620), (1980, 760), (-60, 760)])
    ink(x, hexc("5e6f95"), 0)
    for (px, py, w) in ((220, 400, 70), (640, 360, 80), (1120, 430, 60), (1680, 420, 74)):
        poly(x, [(px - w, py + w * .9), (px, py), (px + w, py + w * .9), (px + w * .4, py + w * .66), (px, py + w), (px - w * .4, py + w * .66)])
        ink(x, SNOW, 0)
    hill(x, [(-60, 720), (500, 660), (1100, 710), (1980, 650)], hexc("dfe8f5"))
    hill(x, [(-60, 840), (700, 790), (1980, 830)], SNOW)


def winter(c, t, kind="winter", fall=True, n=70, speed=1.0, wind=30):
    blit(c, f"sky-{kind}", lambda x: sky(x, kind))
    blit(c, "winter-land", _winter_land)
    if fall:
        snowfall(c, t, n, 5, wind, speed=speed)


def _gh_inside(x):
    # glass roof with a cold blue sky beyond it, warm light inside
    fill_bg(x, [(0, hexc("9fc0e4")), (0.42, hexc("f6e3a8")), (0.75, hexc("f9d88c")), (1, hexc("e7b866"))])
    for (px, py, s) in ((360, 80, 0.9), (1240, 60, 1.0)):
        cloud(x, px, py, s, WHITE, 0.6)
    for i in range(-5, 7):
        xx = 960 + i * 330
        line(x, xx, -10, 960 + i * 190, 430, PAPER, 11, 0.95)
    for yy in (150, 300):
        line(x, 0, yy, W, yy, PAPER, 8, 0.95)
    line(x, 0, 430, W, 430, PAPER, 12, 0.95)
    # rows of tomato vines running away from us
    for layer, (y0, h, n, sc) in enumerate(((430, 260, 15, 0.8), (430, 330, 8, 1.15))):
        for i in range(n):
            xx = (i + 0.5) * W / n
            if 620 < xx < 1300 and layer == 1:
                continue
            line(x, xx, y0 - 30, xx, y0 + h, mix(LEAF, INK, 0.1), 7 * sc)
            r = random.Random(i * 7 + layer)
            for j in range(9):
                yy = y0 + j * h / 9
                side = (-1) ** j
                ell(x, xx + side * 19 * sc, yy, 27 * sc, 16 * sc); ink(x, mix(LEAF, GRASS, r.random()), 3)
                if j % 2:
                    tomato(x, xx - side * 15 * sc, yy + 12, 15 * sc)
    rr(x, -20, 790, W + 40, 300, 0); ink(x, hexc("d3b07e"), 0)
    hill(x, [(-60, 800), (960, 786), (1980, 800)], hexc("cfa873"))


def greenhouse_in(c, t):
    blit(c, "gh-in", _gh_inside)
    # dust motes in the warm air
    r = random.Random(4)
    for _ in range(26):
        x0, y0, v, ph = r.uniform(0, W), r.uniform(300, 900), r.uniform(4, 12), r.uniform(0, 6)
        setc(c, WHITE, 0.3 + 0.2 * math.sin(t + ph))
        c.arc((x0 + t * v) % W, y0 + math.sin(t * .6 + ph) * 16, 3, 0, 7); c.fill()


def paper(c, kind="day", seed=4):
    """Quiet backdrop for numbers and diagrams."""
    def d(x):
        sky(x, "gold")
        mix_a = 0.55
        hill(x, [(-60, 930), (500, 880), (1200, 930), (1980, 880)], hexc("e3c98a"))
        hill(x, [(-60, 1010), (760, 970), (1980, 1000)], hexc("c9b268"))
    blit(c, "paper", d)


def _town(x, s=1.0, cx=0, cy=0, col=hexc("7d87b5")):
    r = random.Random(3)
    with at(x, cx, cy, s):
        xx = -200
        while xx < 200:
            w, h = r.uniform(34, 62), r.uniform(70, 190)
            rr(x, xx, -h, w, h, 3); ink(x, col, 3.5)
            for i in range(int(h // 28)):
                rr(x, xx + 8, -h + 10 + i * 28, 9, 12, 1); ink(x, GOLD, 0)
                rr(x, xx + w - 18, -h + 10 + i * 28, 9, 12, 1); ink(x, GOLD, 0)
            xx += w + 4


def town(c, x, y, s=1.0, col=hexc("7d87b5")):
    _town(c, s, x, y, col)


# Maps
_K38 = math.cos(math.radians(38))
US = [(-124.7, 48.4), (-122.8, 49), (-95.2, 49), (-94.6, 48.7), (-91.5, 48.1), (-89.5, 48), (-84.8, 46.6), (-83.5, 45.8),
      (-82.5, 45.3), (-82.4, 43), (-83, 42), (-79, 42.7), (-79, 43.3), (-76.5, 43.5), (-75, 45), (-71.5, 45), (-70, 46.7),
      (-68.3, 47.3), (-67, 45.2), (-70.2, 43.6), (-70.7, 41.7), (-74, 40.6), (-75.5, 38.5), (-76, 35.6), (-78, 33.9),
      (-81, 32), (-81.4, 30.4), (-80, 26.8), (-80.4, 25.2), (-81.8, 26), (-82.8, 28), (-84, 30), (-86, 30.4), (-89, 30.3),
      (-89.3, 29.2), (-91.5, 29.5), (-94, 29.6), (-97, 27.8), (-97.3, 26), (-99.2, 26.6), (-101.4, 29.8), (-103, 29),
      (-104.8, 30.3), (-106.5, 31.8), (-108.2, 31.4), (-111, 31.3), (-114.8, 32.5), (-117.1, 32.5), (-118.5, 34),
      (-120.6, 34.6), (-122.4, 37.5), (-124.3, 40.3), (-124, 43), (-124, 46.2)]
IOWA = [(-96.5, 43.5), (-91.2, 43.5), (-90.2, 41.8), (-91.4, 40.4), (-95.8, 40.6)]
KANSAS = [(-102, 40), (-94.6, 40), (-94.6, 37), (-102, 37)]
OREGON = [(-124.3, 46.2), (-122.5, 45.6), (-119, 45.9), (-117, 46), (-117, 42), (-124.2, 42), (-124, 43)]
ICELAND = [(-24.3, 65.5), (-23, 66.4), (-22.4, 66.4), (-21.3, 65.4), (-20.3, 65.7), (-19.5, 66.1), (-18.2, 66.0), (-16.2, 66.5),
           (-14.8, 66.3), (-14.6, 65.6), (-13.6, 65.1), (-14.6, 64.4), (-15.9, 64.2), (-17.5, 63.75), (-19, 63.4), (-20.4, 63.7),
           (-22.6, 63.85), (-22.7, 64.1), (-21.9, 64.3), (-22.3, 64.75), (-24, 64.85), (-22.4, 65.1), (-22.2, 65.4)]


def usp(lon, lat, k=38.0, cx=960, cy=560):
    return (cx + (lon + 96) * _K38 * k, cy - (lat - 38) * k)


def usmap(c, k=38.0, cx=960, cy=560, hi=None, hicol=GOLD):
    p = lambda ll: usp(ll[0], ll[1], k, cx, cy)
    curve(c, [p(q) for q in US], close=True)
    ink(c, hexc("a9cf8e"), 6)
    if hi:
        poly(c, [p(q) for q in hi]); ink(c, hicol, 5)


def icep(lon, lat, k=150.0, cx=960, cy=560):
    return (cx + (lon + 19) * 0.426 * k, cy - (lat - 65) * k)


def icemap(c, k=150.0, cx=960, cy=560):
    curve(c, [icep(a, b, k, cx, cy) for a, b in ICELAND], close=True)
    ink(c, hexc("e6eefa"), 6)
