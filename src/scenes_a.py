"""Cold open through the Kansas and Oregon numbers."""
import math, random
from toon import *
from cast import *
from sets import *
from stage import scene, mouth_at


def rev(t, at_, d=0.7):
    return eout(ramp(t, at_, d))


def host(c, b, t, x=250, y=1050, s=1.08, pose="open", flip=False, mood=None, look_x=0):
    dot(c, x, y, s, t, mouth_at(b.start + t), pose, flip, None, look_x, mood)


def card_in(c, s, x, y, t, t0, size=64, w=1100, fill=PAPER, col=INK):
    k = smooth(ramp(t, t0, 0.8))
    wordcard(c, s, x, y, size, w, k, fill, col, k or 0.01)


def driveway_car(c, t, x, col=TOMATO, s=0.7, y=950, moving=True, driver=None, flip=False):
    car(c, x, y, s, col, -x / 28 if not flip else x / 28, flip, math.sin(t * 9) * 1.2 if moving else 0, driver, t)


@scene("cinema")
def cinema(c, b, t):
    def bg(x):
        sky(x, "night")
        for i, (xx, w, h) in enumerate(((0, 330, 430), (300, 220, 340), (1370, 240, 390), (1600, 360, 460))):
            rr(x, xx, 800 - h, w, h + 40, 4); ink(x, hexc("2a2a6e"), 5)
            for j in range(int(h // 76)):
                for k in range(int(w // 80)):
                    rr(x, xx + 24 + k * 80, 830 - h + j * 76, 36, 46, 3); ink(x, GOLD if (i + j + k * 2) % 3 else hexc("3a3a88"), 0)
        rr(x, -20, 820, W + 40, 300, 0); ink(x, hexc("3a3f6e"), 0)
        rr(x, -20, 880, W + 40, 18, 0); ink(x, hexc("5a5f8e"), 0)
        # the picture house
        rr(x, 520, 300, 880, 560, 8); ink(x, TOMATO, 6)
        rr(x, 600, 590, 720, 270, 6); ink(x, hexc("3a2448"), 6)
        rr(x, 860, 640, 200, 220, 6); ink(x, GOLD, 5)
        line(x, 960, 640, 960, 860, INK, 5)
        for xx in (640, 1110):
            rr(x, xx, 640, 170, 200, 6); ink(x, PAPER, 5)
            star(x, xx + 85, 720, 46, GOLD)
    blit(c, "cinema", bg)
    stars(c, 40, 7, t)
    # marquee
    rr(c, 470, 330, 980, 250, 16); ink(c, CREAM, 7)
    text(c, "NOW SHOWING", 960, 412, 62, TOMATO)
    text(c, "A BASEBALL MOVIE", 960, 510, 84, INK)
    n = 44
    for i in range(n):
        f = i / n * 2 * (980 + 250)
        x = 470 + min(f, 980) - clamp(f - 1230, 0, 980)
        y = 330 + clamp(f - 980, 0, 250) - clamp(f - 2210, 0, 250)
        on = (i + int(t * 7)) % 3 != 0
        ell(c, x, y, 9); ink(c, GOLD if on else hexc("8a6a2a"), 2)
    glow(c, 960, 640, 640, GOLD, 0.22)
    for i in range(8):
        lk = crowd_look(i * 5 + 2)
        x = -260 + i * 150 + t * 62
        if x < 840:
            person(c, x, 950 + (i % 2) * 18, 0.62, lk, t, "idle", walk=t * 1.3 + i * .4, seed=i)
    k = back(ramp(t, 0.2, 0.7))
    with at(c, 250, 200, k, -0.05):
        rr(c, -180, -110, 360, 230, 18); ink(c, PAPER, 6)
        rr(c, -180, -110, 360, 74, 18); ink(c, TOMATO, 6)
        text(c, "APRIL", 0, -52, 54, WHITE)
        text(c, "1989", 0, 80, 118, INK)


@scene("iowa_film")
def iowa_film(c, b, t):
    iowa(c, t)
    # a film crew at the ball field
    x, y = 300, 950
    line(c, x, y, x - 34, y - 150, INK, 8); line(c, x, y, x + 34, y - 150, INK, 8); line(c, x, y - 4, x, y - 150, INK, 8)
    rr(c, x - 64, y - 226, 128, 84, 12); ink(c, hexc("3a3f6e"), 5)
    ell(c, x - 30, y - 248, 30); ink(c, hexc("3a3f6e"), 5); ell(c, x + 30, y - 248, 30); ink(c, hexc("3a3f6e"), 5)
    rr(c, x + 60, y - 204, 56, 42, 6); ink(c, INK, 4)
    person(c, 470, 950, 0.7, crowd_look(12), t, "point_r", seed=2)
    k = ramp((t % 2.2), 0, 0.2)
    with at(c, 660, 900, 0.9):
        rr(c, -90, -40, 180, 110, 8); ink(c, INK, 5)
        text(c, "SCENE 1", 0, 34, 44, WHITE)
        with at(c, -90, -40, 1, -0.5 * (1 - k)):
            rr(c, 0, -26, 180, 28, 6); ink(c, PAPER, 5)
    card_in(c, "A family farm", 1440, 220, t, b.cue("family farm"), 70)
    k2 = back(ramp(t, b.cue("Iowa") - 1.1, 0.7))
    if k2 > 0:
        pin(c, 960, 640 - 90 * 0, k2, TOMATO)
    card_in(c, "Near a small town in Iowa", 840, 410, t, b.cue("near a small"), 60, 1000)


@scene("stranger_arrive")
def stranger_arrive(c, b, t):
    iowa(c, t)
    k = smooth(ramp(t, 0.8, b.dur - 1.4))
    x = lerp(-240, 930, k)
    driveway_car(c, t, x, hexc("c4553a"), 0.85, 1010, k < 1, STRANGER)
    surprised = ramp(t, b.dur - 0.9, 0.3) > 0
    person(c, 1300, 1000, 0.72, FARMER, t, "up_r" if surprised else "idle", flip=True, mood="wow" if surprised else None, seed=3)
    if surprised:
        q = back(ramp(t, b.dur - 0.9, 0.4))
        text(c, "?", 1440, 790, 150 * q, TOMATO, "c", 1, halo=WHITE, halo_w=14)
    card_in(c, "Two weeks later", 480, 200, t, 0.15, 76)


@scene("route_map")
def route_map(c, b, t):
    sky(c, "day")
    usmap(c, 34, 960, 560, IOWA)
    ny, ia, ca = usp(-74, 40.7, 34), usp(-91.2, 42.5, 34), usp(-122.3, 37.8, 34)
    k = smooth(ramp(t, 0.5, b.dur - 0.7))
    def along(f):
        if f < 0.42:
            q = f / 0.42
            return lerp(ny[0], ia[0], q), lerp(ny[1], ia[1], q) + math.sin(q * math.pi) * -24
        q = (f - 0.42) / 0.58
        return lerp(ia[0], ca[0], q), lerp(ia[1], ca[1], q) + math.sin(q * math.pi) * 40
    pts = [along(i / 80 * k) for i in range(81)]
    c.new_path(); c.set_dash([20, 16]); c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    setc(c, TOMATO); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke(); c.set_dash([])
    pin(c, ny[0], ny[1], 0.8, TOMATO); pin(c, ca[0], ca[1], 0.8, SKY); pin(c, ia[0], ia[1], 0.7, GOLD)
    text(c, "New York", ny[0] + 10, ny[1] + 66, 56, INK, "c", 1, halo=PAPER)
    text(c, "California", ca[0] + 130, ca[1] + 66, 56, INK, "c", 1, halo=PAPER)
    text(c, "Iowa", ia[0], ia[1] - 86, 56, INK, "c", 1, halo=PAPER)
    x, y = along(k)
    car(c, x, y + 8, 0.28, hexc("c4553a"), t * 9, flip=True)


@scene("stranger_corn")
def stranger_corn(c, b, t):
    def bg(x):
        sky(x, "day")
        hill(x, [(-60, 560), (900, 520), (1980, 560)], hexc("9cc88a"))
        corn_row(x, -40, 2000, 640, 130, 2); corn_row(x, -40, 2000, 720, 180, 3)
        corn_row(x, -40, 2000, 820, 250, 4)
        hill(x, [(-60, 830), (800, 810), (1980, 830)], DIRT)
    blit(c, "cornwall", bg)
    person(c, 660, 1010, 1.05, STRANGER, t, "think", look_x=9, seed=5)
    car(c, 240, 980, 0.8, hexc("c4553a"))
    k = smooth(ramp(t, b.cue("before somebody") - 0.4, 4))
    tractor(c, lerp(2200, 1460, k), 1000, 1.0, t * 4, True, FARMER)
    for i in range(3):
        f = (t * .6 + i / 3) % 1
        ell(c, lerp(2200, 1460, k) + 110 + f * 90, 830 - f * 90, 14 + f * 26); ink(c, GREY, 0, a=0.4 * (1 - f))
    card_in(c, "Out of his way, to see a cornfield", 960, 200, t, 0.4, 66, 1500)


@scene("stranger_first")
def stranger_first(c, b, t):
    iowa(c, t, "sunset")
    person(c, 560, 930, 0.84, STRANGER, t, "idle", seed=5, look_x=9)
    k = ramp(t, 0.2, 1.1)
    hanging(c, 1360, 300, 1.0, ["Visitor", "No. 1"], t, 0.2, sizes=[66, 120], w=470)


@scene("counter300k")
def counter300k(c, b, t):
    iowa(c, t)
    k = smooth(ramp(t, 0.5, b.dur - 1.9))
    n = int(lerp(2, 30, k))
    for i in range(n):
        lk = crowd_look(i * 3 + 9)
        x = 40 + (i * 271) % 1700
        y = 880 + (i * 37) % 170
        walking = i % 2 == 1
        if walking:
            x = (x + t * 60) % 2200 - 140
        person(c, x, y, 0.5, lk, t, "idle" if walking or i % 4 else "wave", walk=t * 1.3 + i * .3 if walking else None, seed=i)
    val = 300000 * (k ** 2.2)
    panel(c, 410, 90, 1100, 280, PAPER)
    text(c, ("nearly " if k > .55 else "") + counter(val), 960, 216, 124, TOMATO)
    text(c, "visitors by late 1995", 960, 318, 66, INK)


@scene("cars_line")
def cars_line(c, b, t):
    def bg(x):
        sky(x, "day")
        hill(x, [(-60, 620), (700, 570), (1980, 610)], hexc("9cc88a"))
        corn_row(x, 1260, 2000, 720, 120, 2); corn_row(x, 1300, 2000, 800, 150, 3)
        rr(x, -20, 800, 2000, 300, 0); ink(x, hexc("7fbb62"), 0)
        rr(x, -20, 860, 2000, 130, 0); ink(x, ROAD, 5)
        for i in range(12):
            rr(x, i * 180, 918, 100, 12, 5); ink(x, CREAM, 0)
    blit(c, "carline", bg)
    cols = [hexc("c4553a"), SKY, GOLD, LEAF, PLUM, TEAL, TOMATO]
    for i in range(9):
        x = (t * 120 + i * 300) % (W + 700) - 400
        if x < 1560:
            car(c, x, 945, 0.72, cols[i % 7], t * 7 + i)
    cow(c, 500, 800, 0.72, math.sin(t * 1.4))
    sign(c, 1540, 610, 0.9, ["CORN"], post=True, sizes=[78], w=300, rot=-0.02)
    t1 = b.cue("In Iowa")
    card_in(c, "To a cornfield.", 720, 210, t, 0.1, 86)
    card_in(c, "In Iowa.", 1240, 340, t, t1, 86)


@scene("yourfarm_road")
def yourfarm_road(c, b, t):
    longroad(c, t)
    house(c, 460, 770, 0.8); barn(c, 720, 760, 0.62)
    gate(c, 1400, 1010, 0.8)
    host(c, b, t, 150, 1050, 1.0, "point_r")
    # a signpost with nothing on it, by the empty road
    k = rev(t, b.cue("No highway"), 0.5)
    sign(c, 1640, 700, 0.9, [""], post=True, sizes=[60], w=330, h=120, rot=0.02, a=1)
    cross(c, 1640, 700, 0.6, k)
    card_in(c, "Your farm", 960, 150, t, 0.1, 76)
    card_in(c, "A long road in", 1250, 150, t, b.cue("A long road"), 66) if False else None
    if t >= b.cue("A long road"):
        wordcard(c, "A long road in. No highway sign.", 960, 290, 62, 1300, smooth(ramp(t, b.cue("A long road"), .7)), PAPER, INK, 1)


@scene("yourfarm_town")
def yourfarm_town(c, b, t):
    farmland(c, t, "day", 6, (300, 170))
    town(c, 1660, 700, 0.75)
    house(c, 240, 860, 0.72); barn(c, 480, 850, 0.55)
    k = smooth(ramp(t, 0.2, b.dur - 0.5))
    x1 = lerp(620, 1470, k)
    line(c, 620, 900, x1, 900, TOMATO, 12, dash=[6, 26])
    if k > 0.02:
        ell(c, x1, 900, 14); ink(c, TOMATO, 4)
    card_in(c, "The nearest town? A good drive away.", 960, 240, t, 0.6, 62, 1500)


@scene("whisper")
def whisper(c, b, t):
    longroad(c, t, "dusk", None)
    house(c, 620, 860, 1.1, lit=True, porch=True)
    host(c, b, t, 980, 1040, 1.0, "think", mood="sad", look_x=6) if False else person(c, 980, 1040, 1.0, DOT, t, "think", 0, mood="sad", seed=7, look_x=6)
    t0 = b.cue("Who would")
    k = smooth(ramp(t, t0 - 0.2, 0.9))
    if k > 0:
        bubble(c, 1110, 120, 730, 330, (1040, 620), thought=True, a=k)
        para(c, "Who would ever drive all the way out here?", 1475, 230, 66, 640, INK, "c", k)
    # crickets of light
    r = random.Random(3)
    for i in range(14):
        x, y, ph = r.uniform(100, 1800), r.uniform(700, 1000), r.uniform(0, 6)
        glow(c, x + math.sin(t + ph) * 18, y + math.cos(t * .8 + ph) * 12, 12, GOLD, 0.5 + 0.4 * math.sin(t * 3 + ph))


@scene("title")
def title(c, b, t):
    longroad(c, t, "gold", (980, 300))
    gate(c, 1340, 1020, 1.1, smooth(ramp(t, b.cue("Let's find") - .3, 1.2)))
    host(c, b, t, 270, 1050, 1.1, "open")
    hanging(c, 980, 330, 1.0, ["Is your farm too far", "from town for visitors?"], t, 0.05, sizes=[82, 82], w=1170)
    card_in(c, "Let's find out.", 1000, 640, t, b.cue("Let's find"), 74)


def _trail(c, t, active, labels=("How far?", "A real farm", "Three moves")):
    """Three signposts along a road; the current one is lit."""
    for i, l in enumerate(labels):
        x = 400 + i * 560
        on = i == active
        sign(c, x, 300, 1.0 if on else 0.8, [l], sizes=[66], w=480, cols=[INK if on else hexc("5a4a38")], post=False, rot=(-0.02 if i % 2 else 0.02))


@scene("agenda1")
def agenda1(c, b, t):
    farmland(c, t, "day", 2)
    rr(c, -20, 860, W + 40, 120, 0); ink(c, ROAD, 5)
    for i in range(12):
        rr(c, (i * 200 - t * 240) % (W + 200) - 100, 912, 110, 12, 5); ink(c, CREAM, 0)
    car(c, 1020, 900, 0.86, SKY, t * 8, driver=crowd_look(3), bounce=math.sin(t * 9))
    host(c, b, t, 260, 1060, 1.0, "point_r")
    _trail(c, t, 0)
    k = rev(t, b.cue("how far"), 0.8)
    wordcard(c, "How far do farm visitors really travel?", 1120, 580, 62, 1400, k, PAPER, INK, 1)


@scene("agenda2")
def agenda2(c, b, t):
    winter(c, t)
    greenhouse(c, 1120, 900, 1.5, glow_a=1)
    _trail(c, t, 1)
    wordcard(c, "About 60 miles from the capital", 700, 540, 58, 1300, rev(t, b.cue("about 60"), .7), PAPER, INK, 1)
    k = smooth(ramp(t, b.cue("that welcomed"), 2.6))
    if t >= b.cue("that welcomed"):
        panel(c, 150, 660, 800, 240, PAPER)
        text(c, counter(180000 * k), 550, 790, 124, TOMATO)
        text(c, "visitors in one year", 550, 866, 60, INK)


@scene("agenda3")
def agenda3(c, b, t):
    longroad(c, t, "gold", (980, 300))
    _trail(c, t, 2)
    n = [1, 2, 3]
    for i in n:
        k = back(ramp(t, 0.9 + i * 0.5, 0.5))
        x = 520 + (i - 1) * 440
        with at(c, x, 700, k):
            ell(c, 0, 0, 130); ink(c, GOLD, 7)
            text(c, str(i), 0, 62, 180, INK)
    k = smooth(ramp(t, b.cue("worth the drive") - .6, .8))
    wordcard(c, "Worth the drive", 960, 930, 74, 900, k, PAPER, INK, 1)


@scene("stay3")
def stay3(c, b, t):
    longroad(c, t, "day")
    k = back(ramp(t, 0.1, 0.7))
    with at(c, 480, 300, k):
        ell(c, 0, 0, 170); ink(c, GOLD, 8)
        text(c, "Move", 0, -36, 72, INK); text(c, "3", 0, 100, 170, TOMATO)
    t0 = b.cue("found")
    sign(c, 1050, 500, 0.92, ["Found"], sizes=[90], w=430, post=True, rot=-0.05, a=smooth(ramp(t, t0, .6)))
    t1 = b.cue("forgotten")
    sign(c, 1600, 590, 0.92, ["Forgotten"], sizes=[80], w=460, post=True, rot=0.05, a=smooth(ramp(t, t1, .6)))
    host(c, b, t, 250, 1050, 1.05, "point_r")


@scene("stephen")
def stephen(c, b, t):
    def bg(x):
        sky(x, "day")
        hill(x, [(-60, 600), (500, 520), (1100, 580), (1980, 500)], hexc("4f9a5a"))
        hill(x, [(-60, 760), (800, 700), (1980, 740)], hexc("5fae55"))
        for xx, yy, s in ((180, 760, 0.95), (620, 720, 0.8), (1720, 760, 1.05), (1320, 710, 0.75)):
            durian_tree(x, xx, yy, s)
        hill(x, [(-60, 880), (900, 850), (1980, 880)], GRASS)
    blit(c, "durianfarm", bg)
    clouds(c, t, 2, 9, a=0.6, top=60, bottom=140)
    hanging(c, 960, 310, 1.0, ["Bloopy Durians"], t, 0.3, sizes=[94], w=840)
    card_in(c, "Stephen Loke, founder", 960, 520, t, b.cue("Stephen Loke"), 60)
    card_in(c, "A durian farm in Malaysia", 960, 640, t, b.cue("a durian farm"), 60)
    t2 = b.cue("from all over")
    n = int(clamp((t - t2 + 2.4) * 2.6, 0, 8))
    for i in range(n):
        x = (t - t2 + 2.4) * 120 - i * 165 + 60
        person(c, x, 1010 + (i % 2) * 26, 0.6, crowd_look(i * 7 + 31), t, "idle", walk=t * 1.3 + i * .4, seed=i)
    durian(c, 1740, 980, 1.2 + 0.06 * math.sin(t * 3))


def jungle(c, t, shift=0.0):
    def bg(x):
        sky(x, "day")
        hill(x, [(-60, 520), (700, 430), (1400, 500), (1980, 420)], hexc("4f9a5a"))
        hill(x, [(-60, 660), (800, 590), (1980, 640)], hexc("3f8a4a"))
        r = random.Random(4)
        for _ in range(14):
            tree(x, r.uniform(0, W), r.uniform(600, 690), r.uniform(0.6, 1.0), hexc("2f7f3f"), r.randint(0, 9))
    blit(c, "jungle", bg, -((shift * 0.25) % 200) if False else 0)


def dirt_track(c, t, spd=260):
    pts = []
    off = t * spd
    for i in range(-1, 16):
        x = i * 140 - (off % 140)
        k = i + int(off // 140)
        y = 920 + math.sin(k * 1.7) * 26 + math.sin(k * 0.6) * 18
        pts.append((x, y))
    hill(c, pts, DIRT, lw=5)
    r = random.Random(1)
    for i in range(26):
        x = (r.uniform(0, W + 200) - off) % (W + 200) - 100
        ell(c, x, r.uniform(960, 1060), r.uniform(10, 26), r.uniform(5, 11)); ink(c, hexc("8f6238"), 0, a=0.7)
    return lambda x: 920 + math.sin((x + off) / 140 * 1.7) * 26 + math.sin((x + off) / 140 * 0.6) * 18


@scene("stephen4wd")
def stephen4wd(c, b, t):
    jungle(c, t)
    h = dirt_track(c, t)
    x = 900
    y0, y1 = h(x - 110), h(x + 110)
    jeep(c, x, (y0 + y1) / 2 + 2, 1.5, t * 9, math.atan2(y1 - y0, 220), math.sin(t * 11) * 4, t=t)
    for i in range(4):
        f = (t * 1.2 + i / 4) % 1
        ell(c, x - 200 - f * 170, 900 - f * 70, 16 + f * 34); ink(c, WHEAT, 0, a=0.5 * (1 - f))
    card_in(c, "This part matters for you", 960, 170, t, 0.3, 62) if t < b.cue("Visitors reach") else None
    if t >= b.cue("Visitors reach"):
        wordcard(c, "Visitors arrive by four-wheel drive", 960, 170, 66, 1500, smooth(ramp(t, b.cue("Visitors reach"), .7)), PAPER, INK, 1)


@scene("belief")
def belief(c, b, t):
    farmland(c, t, "day", 3, (1600, 170))
    town(c, 1160, 730, 0.9)
    rr(c, -20, 780, W + 40, 90, 0); ink(c, ROAD, 5)
    for i in range(12):
        rr(c, (i * 200 + t * 300) % (W + 200) - 100, 820, 100, 9, 4); ink(c, CREAM, 0)
    for i in range(3):
        x = (i * 680 + t * 280) % (W + 400) - 200
        car(c, x, 846, 0.5, (TOMATO, SKY, GOLD)[i], t * 8)
    t1 = b.cue("close to town")
    k = smooth(ramp(t, t1 - 0.3, 0.8))
    if k > 0:
        barn(c, 1560, 780, 0.62 * k if k > .1 else .1)
    host(c, b, t, 240, 1060, 1.05, "think")
    wordcard(c, "What most farmers believe", 960, 150, 62, 1200, smooth(ramp(t, .1, .7)), PAPER, INK, 1)
    wordcard(c, "Close to town", 620, 340, 62, 700, smooth(ramp(t, t1 - .3, .7)), PAPER, INK, 1)
    wordcard(c, "Near the highway", 1060, 460, 62, 800, smooth(ramp(t, b.cue("Near the highway"), .7)), PAPER, INK, 1)
    wordcard(c, "Near the people", 1490, 340, 62, 760, smooth(ramp(t, b.cue("Near the people"), .7)), PAPER, INK, 1)


def _roadside(c, t, kind="day", seed=7):
    farmland(c, t, kind, seed)
    rr(c, -20, 900, W + 40, 120, 0); ink(c, ROAD, 5)
    for i in range(10):
        rr(c, i * 220 - 60, 952, 120, 11, 5); ink(c, CREAM, 0)


@scene("driveby_intro")
def driveby_intro(c, b, t):
    _roadside(c, t)
    stand(c, 1120, 900, 1.2)
    host(c, b, t, 300, 1050, 1.05, "point_r")
    hanging(c, 980, 300, 1.0, ["The Drive-By Farm"], t, b.cue("Call it"), sizes=[96], w=1000)
    if t < b.cue("Call it"):
        wordcard(c, "One kind of farm", 980, 260, 66, 900, smooth(ramp(t, .2, .7)), PAPER, INK, 1)


@scene("driveby_stand")
def driveby_stand(c, b, t):
    _roadside(c, t)
    k = back(ramp(t, 0.1, 0.8))
    stand(c, 900, 900, 1.3 * max(k, 0.01))
    t1 = b.cue("hand-painted")
    a = back(ramp(t, t1, 0.7))
    if a > 0:
        with at(c, 1450, 620, a, 0.05):
            rr(c, -13, 90, 26, 200, 7); ink(c, WOODD, 5)
            poly(c, [(-190, -110), (180, -124), (196, 90), (-176, 104)]); ink(c, PAPER, 6)
            text(c, "APPLES", 0, -10, 84, TOMATO)
            text(c, "fresh today", 0, 66, 54, INK)


@scene("driveby_car")
def driveby_car(c, b, t):
    _roadside(c, t)
    stand(c, 900, 900, 1.15)
    t1, t2 = b.cue("someone buys"), b.cue("and drives on")
    if t < t1:
        x = lerp(-260, 1150, eout(ramp(t, 0, t1)))
    else:
        x = 1150 + ((max(0, t - t2)) ** 2) * 240
    moving = t < t1 or t > t2
    car(c, x, 975, 0.86, SKY, x / 30, bounce=math.sin(t * 9) if moving else 0, driver=crowd_look(21))
    if t1 <= t <= t2 + .3:
        k = rev(t, t1, .6)
        with at(c, lerp(960, 1150, k), lerp(760, 830, k), 1):
            poly(c, [(-44, -60), (44, -60), (58, 50), (-58, 50)]); ink(c, hexc("d9c79a"), 5)
            apple(c, -12, -70, 18); apple(c, 16, -66, 18, GOLD)
    card_in(c, "A bag of apples. Then gone.", 960, 200, t, t1 + .2, 66, 1200)


@scene("driveby_starve")
def driveby_starve(c, b, t):
    t1 = b.cue("Far from")
    if t < t1:
        _roadside(c, t)
        stand(c, 900, 900, 1.1)
        for i in range(4):
            x = (t * 520 + i * 560) % (W + 500) - 250
            car(c, x, 975, 0.8, (TOMATO, SKY, GOLD, LEAF)[i], t * 12)
        wordcard(c, "It lives on passing traffic", 960, 200, 66, 1200, smooth(ramp(t, .2, .7)), PAPER, INK, 1)
    else:
        q = t - t1
        def bg(x):
            sky(x, "gold")
            hill(x, [(-60, 640), (800, 600), (1980, 640)], hexc("d8c07a"))
            hill(x, [(-60, 760), (800, 730), (1980, 760)], hexc("c3b25e"))
            hill(x, [(-60, 880), (800, 860), (1980, 880)], hexc("b8a858"))
        blit(c, "dryland", bg)
        stand(c, 900, 920, 1.1, faded=1)
        x = (q * 300) % (W + 400) - 200
        with at(c, x, 960 + abs(math.sin(q * 5)) * -30, 1.7, q * 4):
            for a in range(6):
                line(c, 0, 0, math.cos(a) * 42, math.sin(a) * 42, WOODD, 4)
            ell(c, 0, 0, 34); ink(c, None, 4, WOODD)
        wordcard(c, "Far from the traffic, it starves", 960, 200, 66, 1300, smooth(ramp(q, .1, .7)), PAPER, INK, 1)


@scene("notonly")
def notonly(c, b, t):
    longroad(c, t, "day")
    k = smooth(ramp(t, 0.3, b.dur - .6))
    house(c, 1400, 700, 0.5)
    pin(c, 1400, 590, 1 + 0.06 * math.sin(t * 4), TOMATO)
    car(c, lerp(1300, 1240, k), lerp(1060, 900, k), 0.9 - k * .2, GOLD, t * 8, driver=crowd_look(5))
    host(c, b, t, 250, 1050, 1.05, "open")
    wordcard(c, "Traffic is not the only way people find a farm", 960, 200, 62, 1500, smooth(ramp(t, .2, .8)), PAPER, INK, 1)


def odometer(c, x, y, val, digits=4, s=1.0):
    with at(c, x, y, s):
        w = digits * 92 + 28
        rr(c, -w / 2, -80, w, 160, 16); ink(c, INK, 6)
        st = f"{int(val):0{digits}d}"
        for i, ch in enumerate(st):
            xx = -w / 2 + 14 + i * 92
            rr(c, xx + 4, -66, 84, 132, 8); ink(c, PAPER, 0)
            text(c, ch, xx + 46, 40, 112, INK)


@scene("kansas")
def kansas(c, b, t):
    sky(c, "day")
    usmap(c, 30, 480, 520, KANSAS)
    kx, ky = usp(-98.3, 38.5, 30, 480, 520)
    pin(c, kx, ky + 8, 0.8, TOMATO)
    text(c, "Kansas", kx, ky + 60, 58, INK, "c", 1, halo=PAPER)
    k = smooth(ramp(t, b.cue("the average"), b.cue("to get there") - b.cue("the average")))
    panel(c, 1000, 240, 830, 560, PAPER)
    text(c, "Average visitor", 1415, 340, 66, INK)
    odometer(c, 1415, 490, 129 * k, 3, 1.3)
    text(c, "miles to get there", 1415, 690, 66, TOMATO)
    wordcard(c, "A study of agritourism visitors", 960, 140, 60, 1400, smooth(ramp(t, 0.1, .7)), PAPER, INK, 1)


def _carmark(c, x, y, s, col, lit=True):
    car(c, x, y, s, col if lit else hexc("c9c6bb"), 0)


@scene("kansas_fair")
def kansas_fair(c, b, t):
    paper(c)
    text(c, "To be fair", 960, 150, 74, INK, "c", smooth(ramp(t, .1, .6)))
    k = smooth(ramp(t, 0.9, 2.2))
    for i in range(10):
        x, y = 280 + (i % 5) * 340, 450 + (i // 5) * 230
        near = i < 6
        e = back(ramp(t, 0.3 + i * .09, .4))
        if e > 0:
            with at(c, x, y, e):
                car(c, 0, 0, 0.72, mix(hexc("c9c6bb"), LEAF if near else hexc("c9c6bb"), k), 0)
    wordcard(c, "More than half came from under 50 miles away", 960, 880, 60, 1500, smooth(ramp(t, 1.0, .8)), PAPER, INK, 1)


@scene("kansas_avg")
def kansas_avg(c, b, t):
    paper(c)
    x0, x1 = 170, 1760
    y = 700
    line(c, x0, y, x1, y, INK, 12)
    for i, (m, lab) in enumerate(((0, "0"), (50, "50"), (129, "129"))):
        xx = lerp(x0, x1, m / 300)
        line(c, xx, y - 22, xx, y + 22, INK, 8)
        text(c, lab, xx, y + 90, 62, INK)
    text(c, "miles", x1 - 90, y + 90, 56, INK)
    for i in range(6):
        car(c, x0 + 60 + i * 72 + (i % 2) * 8, y - 10 - (i % 2) * 60, 0.32, LEAF, 0)
    t1 = b.cue("pulled that")
    k = smooth(ramp(t, t1 - 1.0, 3.2))
    for i, far in enumerate((0.45, 0.72, 0.96)):
        xx = lerp(x0, x1, lerp(0.25, far, k))
        car(c, xx, y - 12, 0.5, (TOMATO, SKY, GOLD)[i], t * 3)
    mx = lerp(lerp(x0, x1, 0.17), lerp(x0, x1, 129 / 300), k)
    pin(c, mx, y - 100, 1.1, TOMATO)
    text(c, "Average", mx, y - 240, 62, TOMATO, "c", 1, halo=PAPER)
    wordcard(c, "Long drives pulled the average up", 960, 170, 64, 1400, smooth(ramp(t, .1, .7)), PAPER, INK, 1)
    t2 = b.cue("came on purpose")
    if t > t2:
        wordcard(c, "They came on purpose", 1320, 340, 64, 800, smooth(ramp(t, t2, .7)), GOLD, INK, 1)


@scene("oregon")
def oregon(c, b, t):
    sky(c, "day")
    usmap(c, 30, 1130, 480, OREGON)
    ox, oy = usp(-120.5, 44, 30, 1130, 480)
    pin(c, ox, oy + 8, 0.8, TOMATO)
    text(c, "Oregon", ox + 170, oy, 58, INK, "c", 1, halo=PAPER)
    wordcard(c, "A 2018 survey of agritourism farms", 960, 130, 56, 1500, smooth(ramp(t, .2, .7)), PAPER, INK, 1)
    t1 = b.cue("about a quarter")
    panel(c, 100, 780, 1720, 240, PAPER, smooth(ramp(t, t1, .6)))
    if t >= t1:
        for i in range(4):
            x = 240 + i * 245
            e = back(ramp(t, t1 + i * .22, .45))
            with at(c, x, 960, e * .62):
                car(c, 0, 0, 1, GOLD if i == 3 else hexc("c9c6bb"), 0)
        k = smooth(ramp(t, t1 + 1.1, .7))
        text(c, "About a quarter of visits:", 1360, 880, 58, INK, "c", k)
        text(c, "50 miles or more", 1360, 954, 66, TOMATO, "c", k)
    t2 = b.cue("One way")
    if t >= t2:
        stamp(c, "ONE WAY", 1540, 700, 74, -0.1, eout(ramp(t, t2, .35)))


@scene("people_drive")
def people_drive(c, b, t):
    longroad(c, t, "day")
    host(c, b, t, 280, 1050, 1.1, "shrug")
    for i in range(3):
        x = 1250 + i * 18 + (math.sin(t + i) * 14)
        car(c, x - (i * 90), 1000 - i * 90, 0.82 - i * .18, (GOLD, SKY, TOMATO)[i], t * 8)
    t1 = b.cue("How far")
    if t < t1 - .6:
        wordcard(c, "So people do drive", 960, 190, 76, 1100, smooth(ramp(t, .1, .7)), PAPER, INK, 1)
    else:
        hanging(c, 980, 300, 1.0, ["How far is my farm?"], t, t1 - .6, sizes=[92], w=1040)
        cross(c, 980, 300, 1.3, eout(ramp(t, t1 + 1.0, .45)))


@scene("real_question")
def real_question(c, b, t):
    longroad(c, t, "sunset", (960, 470))
    glow(c, 960, 540, 520, GOLD, 0.4 + 0.1 * math.sin(t * 2))
    gate(c, 952, 612, 0.32, smooth(ramp(t, 0.6, 2)))
    q = b.cue("What's")
    hanging(c, 960, 280, 1.0, ["What's waiting at the", "end of the road?"], t, q - .2, sizes=[88, 88], w=1160)
    if t < q - .2:
        wordcard(c, "The real question", 960, 200, 72, 900, smooth(ramp(t, .1, .6)), PAPER, INK, 1)
    host(c, b, t, 220, 1060, 1.05, "point_r")


def half(c, side, fn):
    c.save()
    c.rectangle(0 if side == 0 else 960, 0, 960, H); c.clip()
    fn(c)
    c.restore()


def _split(c, t, left, right, ll, rl, k=1.0):
    half(c, 0, left); half(c, 1, right)
    rr(c, 950, -10, 20, H + 20, 0); ink(c, PAPER, 5)
    sign(c, 480, 120, 0.9, [ll], sizes=[68], w=760, a=k)
    sign(c, 1440, 120, 0.9, [rl], sizes=[68], w=840, a=k)


def driveby_side(c, t, sad=False):
    with at(c, -200, 0, 1):
        _roadside(c, t)
    stand(c, 430, 900, 1.05, faded=0.25)
    person(c, 780, 900, 0.8, FARMER, t, "hips" if sad else "idle", seed=4, mood="sad" if sad else None, flip=True)


def worth_side(c, t):
    farmland(c, t, "gold", 8, (1700, 190))
    barn(c, 1720, 830, 0.9, lit=True)
    gate(c, 1290, 930, 0.8, 1)
    line(c, 1000, 480, 1900, 520, INK, 3);
    for i in range(9):
        ell(c, 1040 + i * 100, 488 + math.sin(i * .9) * 4 + 12, 10); ink(c, GOLD, 3)


@scene("split1")
def split1(c, b, t):
    t1 = b.cue("Worth-the-Drive")
    def L(x):
        driveby_side(x, t)
    def R(x):
        worth_side(x, t)
        if t > t1:
            crowd(x, 1000, 1900, 1020, 0.5, 6, t, 40, walkv=None)
    half(c, 0, L)
    half(c, 1, R)
    rr(c, 950, -10, 20, H + 20, 0); ink(c, PAPER, 5)
    sign(c, 480, 120, 0.9, ["Drive-By Farm"], sizes=[68], w=760, a=smooth(ramp(t, b.cue("Drive-By") - .3, .6)))
    sign(c, 1440, 120, 0.9, ["Worth-the-Drive Farm"], sizes=[68], w=880, a=smooth(ramp(t, t1 - .3, .6)))


@scene("split2")
def split2(c, b, t):
    t1 = b.cue("The other")
    def L(x):
        driveby_side(x, t, True)
        clock(x, 240, 460, 120, t * .3)
    def R(x):
        worth_side(x, t)
        k = smooth(ramp(t, t1, 2.4))
        car(x, lerp(1000, 1200, k), 1000, 0.7, GOLD, t * 8, driver=crowd_look(5))
        if t > t1:
            with at(x, 1450, 460, back(ramp(t, t1 + .2, .6))):
                rr(x, -150, -120, 300, 250, 12); ink(x, PAPER, 6)
                rr(x, -150, -120, 300, 66, 12); ink(x, TOMATO, 6)
                text(x, "SATURDAY", 0, -68, 48, WHITE)
                ell(x, 0, 40, 60); ink(x, None, 8, TOMATO)
                text(x, "Farm", 0, 60, 54, INK)
    half(c, 0, L); half(c, 1, R)
    rr(c, 950, -10, 20, H + 20, 0); ink(c, PAPER, 5)
    sign(c, 480, 120, 0.9, ["Waits for traffic"], sizes=[68], w=780)
    sign(c, 1440, 120, 0.9, ["A reason to plan the trip"], sizes=[60], w=880, a=smooth(ramp(t, t1, .6)))


def _x_card(c, x, y, w, h, t, t0, draw, label=None):
    k = back(ramp(t, t0, .55))
    if k <= 0:
        return
    with at(c, x, y, k):
        panel(c, -w / 2, -h / 2, w, h, PAPER)
        draw(c)
        if label:
            text(c, label, 0, h / 2 - 34, 56, INK)


@scene("notthis1")
def notthis1(c, b, t):
    paper(c)
    host(c, b, t, 250, 1050, 1.05, "open")
    wordcard(c, "What this is not", 1100, 170, 76, 1100, smooth(ramp(t, .1, .6)), PAPER, INK, 1)
    t1 = b.cue("promise")
    _x_card(c, 1150, 620, 900, 500, t, t1 - .4, lambda x: (text(x, "300,000", 0, -30, 150, TOMATO), text(x, "visitors, guaranteed", 0, 80, 66, INK)))
    if t > t1:
        cross(c, 1150, 600, 1.6, eout(ramp(t, b.cue("will pull"), .5)))


@scene("notthis2")
def notthis2(c, b, t):
    paper(c)
    t1, t2 = b.cue("theme park"), b.cue("move closer")
    def park(x):
        with at(x, 0, 60, .9):
            ell(x, 0, -60, 150); ink(x, None, 9, TOMATO)
            for i in range(8):
                a = i * math.pi / 4 + t * .5
                line(x, 0, -60, math.cos(a) * 150, -60 + math.sin(a) * 150, TOMATO, 5)
                ell(x, math.cos(a) * 150, -60 + math.sin(a) * 150, 24); ink(x, (GOLD, SKY)[i % 2], 4)
            line(x, 0, -60, -90, 130, INK, 11); line(x, 0, -60, 90, 130, INK, 11)
    def nearer(x):
        with at(x, 40, 110, .8):
            town(x, 0, 0, .8)
        with at(x, -240, 110, 1):
            barn(x, 0, 0, .52)
        k = (t * .5) % 1
        line(x, -130, -190, 40, -190, TOMATO, 13)
        poly(x, [(30, -222), (84, -190), (30, -158)]); ink(x, TOMATO, 4)
    _x_card(c, 500, 480, 760, 560, t, 0.1, park, "Build a theme park")
    _x_card(c, 1420, 480, 760, 560, t, min(t2 - .3, 1.6), nearer, "Move closer to town")
    cross(c, 500, 440, 1.5, eout(ramp(t, t1 + .35, .5)))
    cross(c, 1420, 440, 1.5, eout(ramp(t, t2 + .9, .5)))


@scene("keepfarming")
def keepfarming(c, b, t):
    farmland(c, t, "day", 5)
    def rows(x):
        for i in range(5):
            corn_row(x, -30, 1980, 790 + i * 56, 80 + i * 8, i + 20, GRASSD)
    blit(c, "lowrows", rows)
    tractor(c, ((t * 70) % 2400) - 300, 1040, 1.0, t * 3, driver=FARMER)
    host(c, b, t, 1560, 1050, 1.1, "wave", True)
    wordcard(c, "Keep farming exactly as you do", 960, 210, 72, 1500, smooth(ramp(t, .2, .7)), PAPER, INK, 1)


@scene("fix")
def fix(c, b, t):
    longroad(c, t, "gold", (980, 300))
    t1, t2 = b.cue("what people find"), b.cue("how they find you")
    k1 = back(ramp(t, t1 - .2, .6)); k2 = back(ramp(t, t2 - .2, .6))
    if k1 > 0:
        with at(c, 520, 560, k1):
            panel(c, -400, -330, 800, 660)
            gate(c, 0, 130, 0.9, smooth(ramp(t, t1 + .4, 1.4)))
            text(c, "What they find", 0, 200, 64, INK); text(c, "when they arrive", 0, 276, 64, INK)
    if k2 > 0:
        with at(c, 1400, 560, k2):
            panel(c, -400, -330, 800, 660)
            with at(c, 0, -92, .42):
                sx, sy, sw, sh = phone(c, 0, 0)
                rr(c, sx + 20, sy + 40, sw - 40, 120, 18); ink(c, CREAM, 5)
                pin(c, 0, 90, 1.2, TOMATO)
            text(c, "How they find you", 0, 200, 64, INK); text(c, "before they leave", 0, 276, 64, INK)
    wordcard(c, "The fix", 960, 120, 74, 600, smooth(ramp(t, .1, .6)), GOLD, INK, 1)
