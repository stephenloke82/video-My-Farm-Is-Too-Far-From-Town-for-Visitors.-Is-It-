"""The Fridheimar story, then the mid-roll reminder."""
import math, random
from toon import *
from cast import *
from sets import *
from stage import scene, mouth_at
from scenes_a import rev, host, card_in, odometer


def snowy_gh(c, t, x=1150, y=930, s=1.6, broken=0.0, glow_a=0.0, grow=1.0, n=70):
    winter(c, t, n=n)
    greenhouse(c, x, y, s, broken=broken, glow_a=glow_a, grow=grow)


@scene("iceland_map")
def iceland_map(c, b, t):
    sky(c, "winter")
    rr(c, -20, -20, W + 40, H + 40, 0); ink(c, hexc("7fa4d8"), 0)
    for i in range(6):
        line(c, 0, 180 + i * 160, W, 180 + i * 160 + 20, WHITE, 3, 0.25)
    icemap(c, 170, 1040, 560)
    cap = icep(-21.9, 64.15, 170, 1040, 560); farm = icep(-20.35, 64.17, 170, 1040, 560)
    snowfall(c, t, 40, 5, 30)
    t1 = b.cue("buy a run-down"); t2 = b.cue("about 60 miles")
    pin(c, cap[0], cap[1], 0.7, SKY)
    text(c, "Capital", cap[0] - 40, cap[1] + 62, 56, INK, "c", 1, halo=PAPER)
    k = smooth(ramp(t, t2, 2.2))
    if k > 0:
        line(c, cap[0], cap[1], lerp(cap[0], farm[0], k), lerp(cap[1], farm[1], k), TOMATO, 9, dash=[4, 18])
    if t >= t1:
        with at(c, farm[0], farm[1], back(ramp(t, t1, .6))):
            pin(c, 0, 0, 0.8, TOMATO)
    if t >= t2:
        text(c, "60 miles", (cap[0] + farm[0]) / 2 + 20, farm[1] + 130, 64, TOMATO, "c", smooth(ramp(t, t2, .6)), halo=PAPER)
    k0 = back(ramp(t, 0.1, .6))
    with at(c, 310, 240, k0):
        panel(c, -220, -130, 440, 260)
        text(c, "Iceland", 0, -28, 74, INK); text(c, "1995", 0, 88, 110, TOMATO)
    t3 = b.cue("Two young")
    a = rev(t, t3, .6)
    if a > 0:
        person(c, 170, 1050, 0.82 * a, KNUTUR, t, "idle", seed=2)
        person(c, 400, 1050, 0.78 * a, HELENA, t, "wave", seed=3, flip=True)


@scene("fridheimar_sign")
def fridheimar_sign(c, b, t):
    snowy_gh(c, t, 1240, 930, 1.4, broken=1.0, grow=0.0, n=50)
    k = ramp(t, 0.05, .9)
    sign(c, 640, 640, 1.0, ["Fridheimar"], sizes=[108], w=720, post=True, rot=-0.03 + math.sin(t * 2) * .012)


@scene("grads")
def grads(c, b, t):
    paper(c)
    t1 = b.cue("She studied")
    lk1 = dict(KNUTUR, hat="grad"); lk2 = dict(HELENA, hat="grad")
    person(c, 480, 1000, 1.05, lk1, t, "up_r" if t < t1 else "idle", seed=2, flip=False)
    person(c, 1420, 1000, 1.05, lk2, t, "up_r" if t >= t1 else "idle", seed=3, flip=True)
    k1 = rev(t, .1, .7); k2 = rev(t, t1, .7)
    if k1 > 0:
        wordcard(c, "Agriculture", 480, 230, 72, 800, smooth(ramp(t, .1, .6)), PAPER, LEAF, 1)
        tractor(c, 760, 1000, 0.8 * k1, 0)
    if k2 > 0:
        wordcard(c, "Plants under glass", 1420, 230, 72, 800, smooth(ramp(t, t1, .6)), PAPER, SKY, 1)
        greenhouse(c, 1130, 1000, 0.52 * k2, grow=1)


@scene("repair")
def repair(c, b, t):
    grow = smooth(ramp(t, b.cue("grew tomatoes") - .3, 2.8))
    fixd = smooth(ramp(t, 0.2, 2.6))
    snowy_gh(c, t, 1200, 930, 1.5, broken=1 - fixd, grow=grow, glow_a=grow * .7, n=40)
    t2 = b.cue("heated by")
    # hammering, then the hot spring feeding the house
    if t < t2:
        hit = abs(math.sin(t * 5))
        person(c, 440, 1000, 0.92, KNUTUR, t, "up_r", seed=2)
        with at(c, 548, 690, 1, hit * 1.0 - .4):
            rr(c, -8, -10, 16, 90, 5); ink(c, WOODD, 4); rr(c, -34, -22, 68, 34, 6); ink(c, GREY, 4)
        person(c, 180, 1000, 0.86, HELENA, t, "carry", seed=3)
    else:
        k = rev(t, t2, .8)
        ell(c, 330, 950, 170, 52); ink(c, hexc("7fd0d8"), 5)
        for i in range(5):
            f = (t * .4 + i / 5) % 1
            ell(c, 240 + i * 45 + math.sin(t + i) * 14, 920 - f * 300, 20 + f * 36); ink(c, WHITE, 0, a=.55 * (1 - f))
        line(c, 480, 950, lerp(480, 800, k), 950, TOMATO, 16)
        r = (t * 1.3) % 1
        ell(c, lerp(480, 800, r * k), 950, 7); ink(c, GOLD, 0)
        wordcard(c, "Heated by hot springs", 480, 200, 62, 800, smooth(ramp(t, t2, .6)), PAPER, INK, 1)
    if t < t2:
        wordcard(c, "Year-round tomatoes", 480, 200, 62, 800, smooth(ramp(t, b.cue("grew tomatoes") - .2, .6)), PAPER, INK, 1)


@scene("crates")
def crates(c, b, t):
    winter(c, t, n=30)
    rr(c, -20, 920, W + 40, 60, 0); ink(c, WOODD, 5)
    gate(c, 1540, 930, 1.0, 1)
    for i in range(9):
        x = (t * 150 + i * 280) % 2500 - 420
        crate(c, x, 918, 0.9)
    hanging(c, 960, 300, 1.0, ["A tomato is a tomato"], t, 0.15, sizes=[92], w=1100)
    t1 = b.cue("Theirs went")
    wordcard(c, "Out the gate, like everyone else's", 960, 560, 62, 1400, smooth(ramp(t, t1, .7)), PAPER, INK, 1)


@scene("gate2008")
def gate2008(c, b, t):
    winter(c, t, n=40)
    greenhouse(c, 1490, 900, 1.05, glow_a=.7)
    horse(c, 1000, 940, 0.62, t, walk=None)
    t1 = b.cue("opened the gate")
    gate(c, 560, 1000, 1.25, smooth(ramp(t, t1 - .2, 1.3)))
    k0 = back(ramp(t, .15, .6))
    with at(c, 300, 230, k0):
        panel(c, -170, -90, 340, 180); text(c, "2008", 0, 44, 112, TOMATO)
    t2 = b.cue("Visitors could")
    if t > t2:
        q = t - t2
        for i in range(4):
            x = -120 + q * 190 - i * 150
            if x > -200:
                person(c, x, 1030 + i % 2 * 16, 0.6, crowd_look(i * 5 + 3), t, "idle", walk=t * 1.3 + i * .4, seed=i)
    wordcard(c, "Watch them breed horses and grow tomatoes", 1100, 200, 56, 1400, smooth(ramp(t, t2, .6)), PAPER, INK, 1)


@scene("nine_hundred")
def nine_hundred(c, b, t):
    snowy_gh(c, t, 1300, 900, 1.2, glow_a=.6, n=40)
    k = smooth(ramp(t, 0.3, b.dur - 1.0))
    panel(c, 170, 210, 760, 400)
    text(c, "First year", 550, 320, 66, INK)
    text(c, counter(900 * k), 550, 470, 150, TOMATO)
    text(c, "people", 550, 556, 62, INK)
    crowd(c, 170, 880, 1030, 0.52, 7, t, 50)


@scene("noticed")
def noticed(c, b, t):
    snowy_gh(c, t, 1420, 900, 1.05, glow_a=.7, n=40)
    t1 = b.cue("But they")
    person(c, 480, 1040, 1.0, KNUTUR, t, "think", seed=2, look_x=8)
    person(c, 780, 1040, 0.96, HELENA, t, "look", seed=3, look_x=8)
    wordcard(c, "Not a crowd.", 640, 200, 80, 800, smooth(ramp(t, .05, .6)), PAPER, INK, 1)
    if t > t1:
        k = back(ramp(t, t1, .6))
        with at(c, 660, 500, k):
            glow(c, 0, 0, 170, GOLD, .55)
            ell(c, 0, -14, 62, 66); ink(c, GOLD, 6); rr(c, -26, 46, 52, 34, 7); ink(c, GREY, 5)


def cutaway(c, t, w=0.46):
    """Blizzard on the left of the glass, warm greenhouse on the right."""
    greenhouse_in(c, t)
    c.save()
    c.rectangle(0, 0, W * w, H); c.clip()
    def cold(x):
        sky(x, "storm")
        hill(x, [(-60, 720), (500, 680), (1000, 730)], hexc("c6d3e6"))
        hill(x, [(-60, 840), (500, 820), (1000, 840)], SNOW)
        for i in range(5):
            tree(x, 60 + i * 170, 800 - (i % 2) * 40, .8, bare=True)
    blit(c, "cold", cold)
    snowfall(c, t, 120, 3, 340, speed=1.9)
    c.restore()
    rr(c, W * w - 12, -10, 24, H + 20, 0); ink(c, PAPER, 5)


@scene("warm_inside")
def warm_inside(c, b, t):
    cutaway(c, t)
    for i, x in enumerate((1060, 1270, 1480, 1700)):
        person(c, x, 1010 + (i % 2) * 20, 0.82, crowd_look(i * 4 + 6), t, "cheer" if i % 2 else "open", seed=i, mood="happy")
    wordcard(c, "Warm, bright, inside", 1380, 200, 66, 900, smooth(ramp(t, b.cue("warm") - .4, .6)), PAPER, INK, 1)
    wordcard(c, "Icelandic winter", 440, 200, 66, 800, smooth(ramp(t, b.cue("while the Icelandic") - .2, .6)), PAPER, SKY, 1)


def table(c, x, y, s=1.0, soup=True, cloth=TOMATO):
    with at(c, x, y, s):
        for xx in (-120, 120):
            rr(c, xx - 8, -100, 16, 100, 4); ink(c, WOODD, 4)
        rr(c, -160, -118, 320, 24, 8); ink(c, CREAM, 5)
        for i in range(6):
            rr(c, -160 + i * 53.4, -112, 26, 18, 2); ink(c, cloth, 0)
        if soup:
            bowl(c, -64, -120, .5); bowl(c, 64, -120, .5)


def bowl(c, x, y, s=1.0, t=0.0, col=TOMATO, steam=False):
    with at(c, x, y, s):
        ell(c, 0, -62, 100, 26); ink(c, col, 5)
        c.new_path(); c.move_to(-100, -62); c.curve_to(-92, 10, 92, 10, 100, -62); c.curve_to(60, -44, -60, -44, -100, -62)
        c.close_path(); ink(c, CREAM, 5)
        if steam:
            for i in range(3):
                f = (t * .5 + i / 3) % 1
                xx = -50 + i * 50 + math.sin(f * 7) * 12
                ell(c, xx, -96 - f * 150, 12 + f * 24); ink(c, WHITE, 0, a=.6 * (1 - f))


@scene("restaurant")
def restaurant(c, b, t):
    greenhouse_in(c, t)
    k0 = back(ramp(t, .2, .6))
    with at(c, 280, 170, k0):
        panel(c, -170, -90, 340, 180); text(c, "2012", 0, 44, 112, TOMATO)
    t1 = b.cue("a restaurant")
    for i, (x, y, s) in enumerate(((560, 860, .85), (1010, 860, .85), (1450, 860, .85), (780, 1000, 1.05), (1290, 1000, 1.05))):
        k = eout(ramp(t, t1 + i * .28, .55))
        if k > 0:
            with at(c, 0, (1 - k) * -860, 1):
                table(c, x, y, s)
    wordcard(c, "A restaurant in the middle of the greenhouse", 1120, 170, 56, 1300, smooth(ramp(t, t1, .7)), PAPER, INK, 1)


@scene("menu")
def menu(c, b, t):
    greenhouse_in(c, t)
    rr(c, -30, 800, W + 60, 44, 10); ink(c, CREAM, 5)
    for i in range(20):
        rr(c, i * 100, 812, 50, 26, 2); ink(c, TOMATO, 0)
    for x in (260, 960, 1660):
        rr(c, x - 14, 844, 28, 240, 6); ink(c, WOODD, 5)
    wordcard(c, "Tables between the tomato vines", 960, 150, 62, 1300, smooth(ramp(t, .1, .6)), PAPER, INK, 1) if t < b.cue("Tomato soup") else None
    items = [("Tomato soup", 400, b.cue("Tomato soup")), ("Tomato ice cream", 960, b.cue("Tomato ice cream")), ("Tomato beer", 1520, b.cue("Even tomato beer"))]
    for i, (lab, x, t0) in enumerate(items):
        k = back(ramp(t, t0, .55))
        if k <= 0:
            continue
        with at(c, x, 802, k):
            if i == 0:
                bowl(c, 0, 0, 1.3, t, steam=True)
                c.save(); c.translate(150, 10); ell(c, 0, -30, 76, 44); ink(c, hexc("d9a65e"), 5); c.restore()
            elif i == 1:
                poly(c, [(-54, -60), (54, -60), (0, 80)]); ink(c, hexc("d9a65e"), 5)
                ell(c, 0, -96, 62); ink(c, hexc("f07f6a"), 5); tomato(c, 0, -164, 26)
            else:
                rr(c, -56, -160, 112, 190, 12); ink(c, hexc("e8944a"), 5)
                c.new_path(); ell(c, 0, -160, 66, 26); ink(c, WHITE, 5)
                c.new_path(); c.arc(68, -70, 38, -1.4, 1.4); setc(c, INK); c.set_line_width(14); c.stroke()
        wordcard(c, lab, x, 520, 58, 560, smooth(ramp(t, t0, .5)), PAPER, TOMATO, 1)


@scene("picture")
def picture(c, b, t):
    greenhouse_in(c, t)
    # the glass wall beside the table, snow beyond it
    t1 = b.cue("Snow outside")
    panel(c, 90, 70, 760, 560, hexc("a9c3e4"), lw=9)
    c.save(); rr(c, 96, 76, 748, 548, 22); c.clip()
    blit(c, "cold", lambda x: None) if False else None
    sky(c, "winter")
    hill(c, [(0, 500), (500, 450), (900, 500)], SNOW)
    if t >= t1:
        snowfall(c, t, 80, 8, 60)
    c.restore()
    line(c, 470, 70, 470, 630, PAPER, 10); line(c, 90, 340, 850, 340, PAPER, 10)
    table(c, 760, 1090, 3.0, soup=False)
    t2 = b.cue("eating soup")
    bowl(c, 760, 760, 2.0, t, steam=True)
    t3 = b.cue("growing a few")
    # spoon dips
    s = (math.sin(t * 1.6) + 1) / 2
    with at(c, 1000, 660 + s * 40, 1, .7):
        rr(c, -11, -220, 22, 220, 9); ink(c, GREY, 5); ell(c, 0, 8, 34, 42); ink(c, GREY, 5)
    # a vine right beside us
    line(c, 1500, -10, 1500, 900, mix(LEAF, INK, .1), 14)
    for j in range(7):
        yy = 80 + j * 125; side = (-1) ** j
        ell(c, 1500 + side * 56, yy, 74, 40); ink(c, GRASSD, 4)
        tomato(c, 1500 - side * 52, yy + 46, 46)
    if t >= t3:
        k = rev(t, t3, .7)
        line(c, 1000, 480, lerp(1000, 1400, k), lerp(480, 420, k), TOMATO, 12, dash=[4, 22])
        wordcard(c, "A few feet from your table", 1180, 230, 60, 900, smooth(ramp(t, t3, .6)), PAPER, INK, 1)
    wordcard(c, "Picture it", 470, 960, 62, 500, smooth(ramp(t, 0, .6)) * (1 - smooth(ramp(t, 2.4, .5))), PAPER, INK, 1)


@scene("count180")
def count180(c, b, t):
    snowy_gh(c, t, 1500, 880, 1.1, glow_a=1, n=40)
    k = smooth(ramp(t, 0.2, b.dur - 1.2))
    panel(c, 110, 130, 1060, 700)
    text(c, "By 2019", 640, 240, 72, INK)
    text(c, counter(180000 * k), 640, 410, 160, TOMATO)
    text(c, "visitors in one year", 640, 510, 64, INK)
    x0 = 200; xw = 880
    rr(c, x0, 600, max(16, xw * (900 / 180000)), 60, 8); ink(c, GOLD, 4)
    text(c, "900", x0 + 40, 650, 56, INK, "l")
    rr(c, x0, 700, max(16, xw * k), 60, 8); ink(c, TOMATO, 4)


def _ring(c, x, y, r, frac, col=TOMATO, bg=hexc("e3dcc8"), lw=52):
    c.new_path(); c.arc(x, y, r, 0, 7); setc(c, bg); c.set_line_width(lw); c.stroke()
    c.new_path(); c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac)
    setc(c, col); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_BUTT); c.stroke()


@scene("pct85")
def pct85(c, b, t):
    winter(c, t, n=30)
    k = smooth(ramp(t, 0.2, 1.9))
    t1 = b.cue("Today")
    panel(c, 110, 180, 780, 720)
    _ring(c, 500, 480, 200, .85 * k)
    text(c, f"{int(85 * k)}%", 500, 530, 124, TOMATO)
    text(c, "from outside Iceland", 500, 800, 62, INK)
    panel(c, 1000, 180, 810, 720, PAPER, smooth(ramp(t, t1, .6)))
    if t >= t1:
        text(c, "Dozens of people", 1405, 290, 74, INK)
        for i in range(16):
            e = back(ramp(t, t1 + .1 + i * .05, .4))
            if e > 0:
                person(c, 1090 + (i % 6) * 122 + (i // 6) * 30, 490 + (i // 6) * 135, .34 * e, crowd_look(i * 3 + 11), t, "idle", seed=i)
        text(c, "employed on the farm", 1405, 860, 62, TOMATO)


@scene("quote")
def quote(c, b, t):
    greenhouse_in(c, t)
    t1 = b.cue("It turned")
    person(c, 300, 1040, 1.05, KNUTUR, t, "open", seed=2, mouth=0)
    sc = smooth(ramp(t, t1 + .2, 1.2))
    wordcard(c, "Tourism: the side business", 1160, 300, 66, 1200, smooth(ramp(t, .3, .6)) * (1 - sc * .55), PAPER, INK, 1)
    k = back(ramp(t, t1 + .2, .7))
    if k > 0:
        with at(c, 1160, 620, k):
            panel(c, -540, -130, 1080, 260, GOLD)
            text(c, "One of their", 0, -24, 76, INK); text(c, "main businesses", 0, 72, 76, INK)


@scene("same")
def same(c, b, t):
    winter(c, t, n=40)
    wordcard(c, "Did they move closer to the city?", 960, 150, 62, 1500, smooth(ramp(t, .05, .6)), PAPER, INK, 1)
    t0 = b.cue("No.")
    if t >= t0:
        stamp(c, "NO", 520, 520, 200, -.1, eout(ramp(t, t0, .35)))
    rows = [("Same farm.", "Same farm"), ("Same village.", "Same village"), ("Same road.", "Same road")]
    panel(c, 960, 300, 760, 560, PAPER, smooth(ramp(t, t0, .5)))
    for i, (cue, lab) in enumerate(rows):
        t1 = b.cue(cue)
        k = smooth(ramp(t, t1 - .1, .4))
        tick(c, 1060, 400 + i * 180, 1.1, LEAF, k)
        text(c, lab, 1130, 425 + i * 180, 84, INK, "l", k)


@scene("fixed")
def fixed(c, b, t):
    longroad(c, t, "gold", (980, 300))
    greenhouse(c, 960, 640, .55, glow_a=1)
    t1 = b.cue("They made")
    wordcard(c, "They didn't fix the distance.", 960, 230, 80, 1500, smooth(ramp(t, .05, .7)), PAPER, INK, 1)
    k = back(ramp(t, t1, .6))
    if k > 0:
        with at(c, 960, 840, k):
            panel(c, -660, -90, 1320, 180, GOLD)
            text(c, "They made the trip worth it.", 0, 30, 84, INK)


def guide_book(c, x, y, s=1.0, rot=0.0):
    with at(c, x, y, s, rot):
        rr(c, -196, -262, 400, 540, 12); ink(c, hexc("10205f"), 6)
        rr(c, -210, -274, 400, 540, 12); ink(c, SKY, 6)
        rr(c, -210, -274, 32, 540, 8); ink(c, hexc("16298a"), 5)
        for i, l in enumerate(("Stop Being", "the Best-Kept", "Secret in", "Your County")):
            text(c, l, 12, -170 + i * 72, 52, WHITE if i != 1 else GOLD)
        pin(c, 12, 190, 1.0, TOMATO)
        text(c, "Google guide for farms", 12, 240, 30, CREAM)


@scene("cta_guide")
def cta_guide(c, b, t):
    paper(c)
    t1, t2, t3 = b.cue("Stephen wrote"), b.cue("The link"), b.cue("More about")
    host(c, b, t, 240, 1050, 1.05, "point_r")
    bubble(c, 90, 90, 760, 230, (300, 600), thought=True, a=smooth(ramp(t, .2, .6)))
    text(c, "My farm has to", 470, 186, 66, INK, "c", smooth(ramp(t, .2, .6)))
    text(c, "be found first", 470, 266, 66, INK, "c", smooth(ramp(t, .2, .6)))
    k = back(ramp(t, t1, .6))
    if k > 0:
        guide_book(c, 1040, 590, .95 * k, -.05)
    if t >= t2:
        y = 830 + math.sin(t * 3) * 10
        wordcard(c, "Link in the description", 1430, 300, 60, 800, smooth(ramp(t, t2, .6)), GOLD, INK, 1)
        line(c, 1560, 640, 1560, y + 70, TOMATO, 26)
        poly(c, [(1490, y + 60), (1630, y + 60), (1560, y + 160)]); ink(c, TOMATO, 6)
    if t >= t3:
        wordcard(c, "More at the end", 1430, 180, 56, 700, smooth(ramp(t, t3, .6)), PAPER, INK, 1)


@scene("subscribe")
def subscribe(c, b, t):
    farmland(c, t, "day", 2)
    host(c, b, t, 340, 1050, 1.15, "point_r")
    t1 = b.cue("subscribe")
    press = ramp(t, t1 + .1, .15) * (1 - ramp(t, t1 + .35, .2))
    done = t > t1 + .25
    k = back(ramp(t, t1 - .4, .5))
    with at(c, 1120, 500, k * (1 - press * .08)):
        panel(c, -360, -100, 720, 200, CREAM if done else TOMATO, r=40)
        text(c, "Subscribed" if done else "SUBSCRIBE", 0, 34, 94, INK if done else WHITE)
    if done:
        sw = math.sin((t - t1) * 8) * .3 * max(0, 1 - (t - t1) / 2)
        with at(c, 1600, 500, 1, sw):
            c.new_path(); c.move_to(-70, 54); c.curve_to(-48, 30, -56, -74, 0, -78); c.curve_to(56, -74, 48, 30, 70, 54)
            c.close_path(); ink(c, GOLD, 6)
            ell(c, 0, 66, 18); ink(c, GOLD, 5)
    wordcard(c, "So the next farm lesson finds you", 1120, 780, 62, 1300, smooth(ramp(t, b.cue("so the next"), .6)), PAPER, INK, 1)
