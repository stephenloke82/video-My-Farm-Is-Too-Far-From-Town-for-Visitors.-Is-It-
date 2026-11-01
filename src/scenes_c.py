"""The three moves, the objection, the close and the end screen."""
import math, random
from toon import *
from cast import *
from sets import *
from stage import scene, mouth_at
from scenes_a import rev, host, card_in, dirt_track, jungle, half, _roadside
from scenes_b import bowl, table, cutaway, guide_book


def chapter(c, b, t, n, line1, col, sub=None):
    fill_bg(c, [(0, mix(col, WHITE, .12)), (1, mix(col, INK, .12))])
    hill(c, [(-60, 860), (700, 800), (1980, 860)], mix(col, INK, .22))
    k = back(ramp(t, .05, .55))
    with at(c, 960, 280, k):
        ell(c, 0, 0, 190); ink(c, PAPER, 8)
        text(c, "Move", 0, -44, 76, INK); text(c, n, 0, 118, 200, col if col != GOLD else TOMATO)
    gate(c, 1690, 880, .9, smooth(ramp(t, .4, 1.3)))
    host(c, b, t, 270, 1050, 1.05, "cheer" if t < 1.4 else "open")
    t0 = b.cue(line1[0])
    y = 590
    for l in line1[1]:
        text(c, l, 960, y, 76, WHITE, "c", smooth(ramp(t, t0, .7)), halo=INK, halo_w=9)
        y += 92


@scene("move1card")
def move1card(c, b, t):
    chapter(c, b, t, "1", ("Give them", ["One thing they cannot", "get in town"]), GOLD)


@scene("move1_examples")
def move1_examples(c, b, t):
    paper(c)
    t2 = b.cue("The Iowa farm")
    def a(x):
        greenhouse_in(x, t)
        table(x, 960, 880, 1.9)
    def d(x):
        iowa(x, t)
        k = (t * .22) % 1
        pts = [(560, 690), (800, 790), (560, 880), (320, 790), (560, 690)]
        q = k * 4; i = int(q); f = q - i
        px = lerp(pts[i][0], pts[i + 1][0], f); py = lerp(pts[i][1], pts[i + 1][1], f)
        person(x, px, py, .5, crowd_look(4), t, "idle", walk=t * 1.8, seed=3, flip=f < 0 and False or i in (1, 2))
    panes = [(70, a, "Lunch inside a greenhouse", .1), (990, d, "A walk around the bases", t2)]
    for (x, fn, lab, t0) in panes:
        k = smooth(ramp(t, t0, .6))
        if k <= 0:
            continue
        w, h = 860, 620
        panel(c, x, 170, w, h, PAPER, k, r=30)
        c.save(); rr(c, x + 8, 178, w - 16, h - 16, 24); c.clip()
        if fn is d:
            with at(c, x - 60, 170 - 100, .6 + .0):
                d(c)
        else:
            with at(c, x - 60, 170, .55):
                a(c)
        c.restore()
        text(c, lab, x + w / 2, 900, 58, INK, "c", k, halo=PAPER)


@scene("sold_one")
def sold_one(c, b, t):
    paper(c)
    t1 = b.cue("They sold")
    # a shelf of more stuff, struck out
    x0 = 540
    panel(c, 110, 210, 800, 600)
    text(c, "More stuff", x0 - 30, 300, 72, INK)
    for i in range(3):
        rr(c, 170, 470 + i * 110, 680, 18, 6); ink(c, WOOD, 4)
        for j in range(6):
            x = 210 + j * 108
            if (i + j) % 2:
                apple(c, x, 440 + i * 110, 22, (TOMATO, GOLD, LEAF)[j % 3])
            else:
                rr(c, x - 24, 410 + i * 110, 48, 60, 7); ink(c, (TEAL, PLUM, SKY)[j % 3], 4)
    cross(c, 510, 590, 1.55, eout(ramp(t, b.cue("Neither") + .6, .5)))
    k = back(ramp(t, t1, .7))
    if k > 0:
        with at(c, 1400, 500, k):
            glow(c, 0, 0, 400, GOLD, .65)
            star(c, 0, -30, 170, GOLD, math.sin(t) * .05, 7)
            text(c, "1", 0, 30, 150, TOMATO)
        wordcard(c, "One experience, only here", 1400, 860, 60, 900, smooth(ramp(t, t1, .7)), PAPER, INK, 1)


@scene("eggs")
def eggs(c, b, t):
    farmland(c, t, "day", 3)
    def coop(x):
        rr(x, 1270, 560, 470, 340, 6); ink(x, WOOD, 6)
        poly(x, [(1240, 570), (1505, 430), (1770, 570)]); ink(x, TOMATO, 6)
        for i in range(3):
            rr(x, 1305 + i * 140, 700, 120, 96, 8); ink(x, hexc("5a3a2a"), 5)
            ell(x, 1365 + i * 140, 790, 50, 13); ink(x, WHEAT, 3)
    blit(c, "coop", coop)
    for i, x in enumerate((1060, 780, 1600)):
        chicken(c, x, 1000 + i * 14, .9, t, i, i == 2)
    person(c, 420 + t * 34, 1020, .7, crowd_look(70), t, "carry", seed=2, walk=t * 1.2, carry=lambda x, hx, hy: _basket(x, hx, hy))
    person(c, 300, 1040, .62, crowd_look(73), t, "up_r", seed=4)
    t1 = b.cue("eggs the children")
    k = back(ramp(t, t1 + .8, .6))
    if k > 0:
        with at(c, 1490, 330, k):
            panel(c, -270, -180, 540, 340)
            ell(c, 0, 40, 210, 80); ink(c, GREY, 5)
            for dx in (-80, 80):
                ell(c, dx, 34, 74, 50); ink(c, WHITE, 3.5); ell(c, dx, 32, 28); ink(c, GOLD, 3)
    wordcard(c, "Breakfast with eggs they collected", 780, 200, 62, 1100, smooth(ramp(t, .3, .7)), PAPER, INK, 1)


def _basket(c, x, y):
    c.new_path(); c.arc(x, y + 8, 34, math.pi, 0); setc(c, INK); c.set_line_width(6); c.stroke()
    rr(c, x - 44, y + 6, 88, 56, 12); ink(c, WOOD, 5)
    for dx in (-20, 0, 20):
        ell(c, x + dx, y + 2, 15, 18); ink(c, CREAM, 3)


@scene("fruit")
def fruit(c, b, t):
    farmland(c, t, "day", 4)
    def orch(x):
        with at(x, 1100, 1020, 2.4):
            poly(x, [(-18, 0), (-12, -80), (12, -80), (18, 0)]); ink(x, WOODD, 2.5)
            x.new_path()
            for dx, dy, q in ((-60, -120, 74), (60, -120, 74), (0, -176, 86), (-104, -86, 50), (104, -86, 50)):
                ell(x, dx, dy, q)
            setc(x, INK); x.set_line_width(5); x.stroke_preserve(); setc(x, LEAF); x.fill()
    blit(c, "orchard", orch)
    for (x, y) in ((820, 540), (1010, 420), (1240, 500), (1400, 640), (900, 700), (1160, 680)):
        apple(c, x, y + math.sin(t * 1.5 + x) * 3, 34)
    k = smooth(ramp(t, .1, b.dur - .3))
    person(c, 560, 1040, 1.15, crowd_look(70), t, "up_r", seed=2, mood="happy", look_x=8)
    apple(c, lerp(760, 690, k), lerp(610, 560, k), 34)
    wordcard(c, "Straight from the tree", 620, 200, 72, 1000, smooth(ramp(t, .2, .7)), PAPER, INK, 1)


@scene("sunset")
def sunset(c, b, t):
    farmland(c, t, "sunset", 6, (1400, 520), trees=False)
    x = 620 + t * 95
    # a hay wagon behind a tractor
    y = 900
    rr(c, x - 330, y - 96, 320, 50, 6); ink(c, WOOD, 5)
    for i in range(4):
        person(c, x - 300 + i * 90, y - 96, .34, crowd_look(i * 3 + 80), t, "wave" if i % 2 else "idle", seed=i)
    rr(c, x - 330, y - 104, 320, 44, 8); ink(c, WHEAT, 4)
    wheel(c, x - 270, y - 26, 28, t * 3); wheel(c, x - 80, y - 26, 28, t * 3)
    line(c, x - 10, y - 60, x + 60, y - 60, INK, 8)
    tractor(c, x + 150, y, .8, t * 3, driver=FARMER)
    wordcard(c, "A ride across the fields at sunset", 960, 190, 66, 1300, smooth(ramp(t, .2, .7)), PAPER, INK, 1)


def supermarket(c, x, y, s=1.0):
    with at(c, x, y, s):
        rr(c, -210, -190, 420, 190, 6); ink(c, CREAM, 6)
        rr(c, -226, -226, 452, 56, 8); ink(c, TOMATO, 6)
        text(c, "SUPERMARKET", 0, -182, 40, WHITE)
        for i in range(3):
            rr(c, -180 + i * 126, -146, 108, 146, 4); ink(c, hexc("cfe6f5"), 5)


@scene("test")
def test(c, b, t):
    farmland(c, t, "day", 7)
    wordcard(c, "The test", 960, 130, 74, 600, smooth(ramp(t, .05, .6)), GOLD, INK, 1)
    t1, t2 = b.cue("If they can get"), b.cue("it will not")
    house(c, 960, 830, .6)
    k1 = back(ramp(t, t1, .6))
    if k1 > 0:
        supermarket(c, 300, 830, .8 * k1)
        line(c, 480, 860, 820, 860, GOLD, 10, dash=[4, 20])
        text(c, "10 minutes", 640, 800, 62, INK, "c", 1, halo=PAPER)
    k2 = back(ramp(t, t2, .6))
    if k2 > 0:
        barn(c, 1700, 830, .62 * k2)
        line(c, 1100, 860, 1570, 860, TOMATO, 10, dash=[4, 20])
        text(c, "60 miles", 1330, 800, 62, INK, "c", 1, halo=PAPER)
        cross(c, 1330, 860, .55, eout(ramp(t, t2 + 1.0, .5)))
    t3 = b.cue("supermarket")
    wordcard(c, "Same thing as the shop? They stay home.", 960, 300, 62, 1500, smooth(ramp(t, t2 + .7, .6)), PAPER, INK, 1)


def sentence_sign(c, t, t0, x=960, y=420, s=1.0, typed=None):
    k = t >= t0
    hanging(c, x, y, s, ["Only at our farm", "can you ______"], t, t0, sizes=[96, 96], w=1120)


@scene("sentence")
def sentence(c, b, t):
    longroad(c, t, "gold", (980, 300))
    t0 = b.cue("Only at")
    wordcard(c, "Finish this sentence", 960, 170, 68, 1000, smooth(ramp(t, .05, .6)) * (1 - smooth(ramp(t, t0 - .3, .4))), PAPER, INK, 1)
    sentence_sign(c, t, t0 - .2)
    t1 = b.cue("Whatever")
    host(c, b, t, 250, 1050, 1.05, "open")
    if t > t1:
        wordcard(c, "That blank is your reason for the drive", 1060, 790, 62, 1400, smooth(ramp(t, t1, .7)), GOLD, INK, 1)


@scene("move2card")
def move2card(c, b, t):
    chapter(c, b, t, "2", ("Make the road", ["Make the road part of the", "adventure"]), LEAF)
    t1 = b.cue("and make")
    wordcard(c, "A visit long enough to be worth it", 960, 790, 60, 1000, smooth(ramp(t, t1, .7)), PAPER, INK, 1)


@scene("bumpy")
def bumpy(c, b, t):
    t1, t2 = b.cue("A bumpy road"), b.cue("becomes the first")
    if t < t2:
        jungle(c, t)
        h = dirt_track(c, t)
        x = 980
        y0, y1 = h(x - 110), h(x + 110)
        jeep(c, x, (y0 + y1) / 2 + 2, 1.05, t * 9, math.atan2(y1 - y0, 220), math.sin(t * 11) * 4, t=t)
        if t < t1:
            wordcard(c, "By four-wheel drive", 960, 170, 66, 1000, smooth(ramp(t, .1, .6)), PAPER, INK, 1)
        if t > t1:
            k = rev(t, t1, .6)
            person(c, lerp(-140, 250, k) if t < t1 + 2 else lerp(250, -300, smooth(ramp(t, t1 + 2, 1.2))), 1020, .84,
                   crowd_look(14), t, "carry", mood="wow", flip=t > t1 + 2, walk=t * 1.3,
                   carry=lambda x, hx, hy: _cart(x, hx, hy))
            wordcard(c, "It scares off a shopper", 960, 170, 66, 1000, smooth(ramp(t, t1, .6)), PAPER, INK, 1)
    else:
        q = t - t2
        farmland(c, t, "gold", 3)
        person(c, 460, 1030, 1.05, crowd_look(14), t, "open", mouth=abs(math.sin(t * 7)) * .8, seed=2, look_x=8)
        person(c, 1130, 1030, .98, crowd_look(16), t, "idle", flip=True, mood="wow", seed=3)
        person(c, 1400, 1040, .94, crowd_look(19), t, "hips", flip=True, mood="happy", seed=4)
        bubble(c, 300, 130, 780, 390, (500, 640), a=smooth(ramp(q, 0, .5)))
        with at(c, 690, 370, .74):
            hill(c, [(-420, 110), (-200, 60), (0, 100), (200, 50), (420, 100)], DIRT, base=150)
            jeep(c, 0, 92, .9, t * 8, math.sin(t * 7) * .08, math.sin(t * 11) * 4, t=t)
        wordcard(c, "The first story they tell", 1400, 300, 60, 700, smooth(ramp(q, .4, .6)), GOLD, INK, 1)


def _cart(c, x, y):
    poly(c, [(x + 6, y + 4), (x + 124, y + 4), (x + 106, y + 72), (x + 26, y + 72)]); ink(c, GREY, 4.5)
    ell(c, x + 42, y + 92, 12); ink(c, INK, 0); ell(c, x + 96, y + 92, 12); ink(c, INK, 0)


@scene("hour20")
def hour20(c, b, t):
    paper(c)
    t1 = b.cue("But they")
    # left: long way for short stop. Right: the same drive, a whole day.
    def bars(x, y, lab, frac, col):
        rr(c, x, y, 780 * frac, 64, 12); ink(c, col, 4)
        text(c, lab, x, y - 16, 56, INK, "l")
    panel(c, 100, 150, 830, 700)
    k1 = smooth(ramp(t, .2, .6))
    text(c, "No", 515, 250, 74, TOMATO, "c", k1)
    if k1:
        clock(c, 515, 410, 100, t * .3)
        bars(150, 610, "1 hour drive", .95, hexc("c9c6bb"))
        bars(150, 760, "20-minute stop", .32 * k1, TOMATO)
    k2 = back(ramp(t, t1, .6))
    if k2 > 0:
        with at(c, 1405, 500, k2):
            with at(c, -1405, -500, 1):
                panel(c, 990, 150, 830, 700)
                text(c, "Yes", 1405, 250, 74, LEAF)
                sun(c, 1405, 410, 76)
                bars(1040, 610, "1 hour drive", .95, hexc("c9c6bb"))
                bars(1040, 760, "A half-day out", .95 * smooth(ramp(t, b.cue("half-day") - .4, .9)) + .05, LEAF)


@scene("dotoeat")
def dotoeat(c, b, t):
    farmland(c, t, "day", 8)
    items = [("Something to do.", "To do", 340), ("Something to eat.", "To eat", 960), ("Something to take home.", "To take home", 1580)]
    for i, (cue, lab, x) in enumerate(items):
        k = back(ramp(t, b.cue(cue) - .1, .55))
        if k <= 0:
            continue
        with at(c, x, 500, k):
            panel(c, -270, -280, 540, 560)
            if i == 0:
                horse(c, 0, 90, .54, t)
            elif i == 1:
                bowl(c, 0, 70, 1.3, t, steam=True)
            else:
                c.new_path()
                poly(c, [(-90, -100), (90, -100), (112, 80), (-112, 80)]); ink(c, hexc("d9c79a"), 5)
                c.new_path(); c.arc(0, -100, 52, math.pi, 0); setc(c, INK); c.set_line_width(7); c.stroke()
                tomato(c, -40, 0, 40); apple(c, 44, 0, 36, GOLD)
            text(c, lab, 0, 220, 66, INK)


def _stop(c, x, y, s, kind, t):
    with at(c, x, y, s):
        panel(c, -180, -190, 360, 310)
        if kind == 0:
            horse(c, 0, 70, .46, t)
        elif kind == 1:
            greenhouse(c, 0, 70, .54, h=210, glow_a=.4)
        elif kind == 2:
            bowl(c, 0, 60, 1.05, t, steam=True)
        else:
            stand(c, 0, 80, .72)


@scene("iceland_path")
def iceland_path(c, b, t):
    winter(c, t, n=40, fall=True)
    stops = [("A horse show.", "Horse show", 250), ("A walk through", "Greenhouse", 730), ("Lunch.", "Lunch", 1210), ("A little farm shop.", "Farm shop", 1680)]
    path = [(70, 960), (500, 930), (980, 960), (1460, 930), (1860, 960)]
    curve(c, path); setc(c, DIRT); c.set_line_width(46); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    done = 0
    for i, (cue, lab, x) in enumerate(stops):
        t0 = b.cue(cue)
        k = back(ramp(t, t0, .5))
        if k > 0:
            _stop(c, x, 520, .95 * k, i, t)
            text(c, lab, x, 720, 58, INK, "c", 1, halo=PAPER)
            done = i + 1
    t0 = b.cue("A horse show.")
    t3 = b.cue("A little farm shop.")
    f = smooth(ramp(t, t0, max(.1, b.dur - t0 - .4)))
    person(c, lerp(70, 1780, f), 960, .58, crowd_look(4), t, "idle", walk=t * 1.4, seed=2)
    wordcard(c, "How the Iceland farm grew", 960, 130, 62, 1100, smooth(ramp(t, .05, .6)), PAPER, INK, 1)


@scene("earn")
def earn(c, b, t):
    paper(c)
    t1 = b.cue("and another way")
    host(c, b, t, 240, 1050, 1.05, "open")
    labels = ("Horse show", "Greenhouse", "Lunch", "Farm shop")
    for i, lab in enumerate(labels):
        k = eout(ramp(t, .3 + i * .55, .5))
        if k <= 0:
            continue
        x = 600 + i * 340
        panel(c, x - 158, 820, 316, 96, PAPER, k, r=20)
        text(c, lab, x, 886, 54, INK, "c", k)
        hh = 90 + i * 74
        rr(c, x - 70, 790 - hh * k, 140, hh * k, 10); ink(c, LEAF, 4, INK, k)
    k = smooth(ramp(t, t1, .6))
    if k > 0:
        for i in range(4):
            q = (t - t1 - i * .25)
            if q > 0:
                y = 720 - (90 + i * 74) - 54 + 70 - (1 - eout(ramp(q, 0, .5))) * 200
                for j in range(i + 1):
                    coin(c, 600 + i * 340 - 26 * j + 13 * i, y - (j % 2) * 8, 36)
    wordcard(c, "Another reason to stay", 700, 180, 64, 1000, smooth(ramp(t, .2, .6)), PAPER, INK, 1)
    wordcard(c, "Another way to earn", 1360, 310, 64, 900, k, GOLD, INK, 1)


@scene("tell_drive")
def tell_drive(c, b, t):
    longroad(c, t, "day")
    t1 = b.cue("Forty-five")
    wordcard(c, "Tell people before they ask", 960, 170, 68, 1200, smooth(ramp(t, .05, .6)) * (1 - smooth(ramp(t, t1, .4))), PAPER, INK, 1)
    host(c, b, t, 250, 1050, 1.05, "point_r")
    k = t >= t1 - .3
    if k:
        with at(c, 1180, 470, back(ramp(t, t1 - .3, .6))):
            sx, sy, sw, sh = 0, 0, 0, 0
            panel(c, -620, -300, 1240, 560)
            rr(c, -620, -300, 1240, 92, 26); ink(c, SKY, 6)
            text(c, "Getting here", 0, -236, 60, WHITE)
            text(c, "Forty-five minutes from town,", 0, -100, 72, INK)
            text(c, "and the last stretch", 0, 8, 72, INK, "c", smooth(ramp(t, b.cue("and the last"), .5)))
            text(c, "is a farm track.", 0, 116, 72, TOMATO, "c", smooth(ramp(t, b.cue("and the last") + .5, .5)))


@scene("expected")
def expected(c, b, t):
    t1 = b.cue("A long drive that is a surprise")
    def L(x):
        longroad(x, t, "day")
        car(x, 500, 960, 1.1, SKY, t * 8, driver=crowd_look(5), bounce=math.sin(t * 9) * 1.5)
        person(x, 760, 1040, .7, crowd_look(21), t, "cheer", mood="happy", seed=3)
    def R(x):
        c2 = x
        fill_bg(x, SKIES["storm"])
        hill(x, [(960, 640), (1400, 600), (1980, 640)], hexc("7f8aa3"))
        hill(x, [(960, 760), (1400, 730), (1980, 760)], hexc("66708f"))
        car(x, 1500, 980, 1.0, SKY, 0, driver=crowd_look(5))
        person(x, 1220, 1040, .86, crowd_look(21), t, "shrug", mood="sad", seed=3, look_x=-6)
        text(x, "?", 1660, 660, 170, TOMATO, "c", abs(math.sin(t * 2)) * .5 + .5, halo=WHITE)
    if t < t1 - .2:
        L(c)
        sign(c, 960, 130, .9, ["Expected = part of the trip"], sizes=[64], w=1000)
        return
    half(c, 0, L)
    half(c, 1, R)
    rr(c, 950, -10, 20, H + 20, 0); ink(c, PAPER, 5)
    sign(c, 480, 130, .9, ["Expected = part of the trip"], sizes=[56], w=860)
    sign(c, 1440, 130, .9, ["Surprise = a mistake"], sizes=[56], w=760, a=smooth(ramp(t, t1, .5)))


@scene("move3card")
def move3card(c, b, t):
    chapter(c, b, t, "3", ("The one", ["The one that decides", "found or forgotten"]), TOMATO)


@scene("phone_home")
def phone_home(c, b, t):
    def room(x):
        fill_bg(x, [(0, hexc("f6e0b0")), (1, hexc("eccf95"))])
        rr(x, -20, 860, W + 40, 240, 0); ink(x, hexc("b58a5a"), 5)
        rr(x, 1180, 150, 620, 430, 10); ink(x, hexc("a8d8f0"), 8)
        hill(x, [(1190, 480), (1500, 450), (1790, 480)], GRASS, base=572)
        car(x, 1480, 560, .66, GOLD, 0)
        rr(x, 1180, 150, 620, 430, 10); ink(x, None, 8)
        line(x, 1490, 150, 1490, 580, PAPER, 9)
        rr(x, 170, 620, 860, 300, 44); ink(x, hexc("5a7fbe"), 6)
        rr(x, 140, 760, 920, 170, 36); ink(x, hexc("6a90d0"), 6)
    blit(c, "livingroom", room)
    person(c, 450, 880, .9, crowd_look(4), t, "carry", seed=2, mood="happy", sit=True, look_x=8,
           carry=lambda x, hx, hy: (rr(x, hx - 14, hy - 46, 44, 74, 8), ink(x, INK, 3)))
    person(c, 730, 874, .84, crowd_look(16), t, "idle", seed=3, sit=True, flip=True, look_x=8)
    t1 = b.cue("Every visitor")
    if t < t1:
        wordcard(c, "Nobody stumbles across a remote farm", 960, 90, 60, 1500, smooth(ramp(t, .1, .6)), PAPER, INK, 1)
    else:
        wordcard(c, "They decide at home, on a phone", 960, 90, 60, 1500, smooth(ramp(t, t1, .6)), PAPER, INK, 1)
    t2 = b.cue("before the car")
    if t > t2:
        with at(c, 1490, 760, back(ramp(t, t2, .5))):
            panel(c, -330, -80, 660, 160, GOLD)
            text(c, "Before the car leaves", 0, 22, 52, INK)


def tile(c, x, y, lab, k=1.0, lit=1.0, s=1.0, col=None):
    if k <= 0:
        return
    with at(c, x, y, s * k):
        panel(c, -270, -130, 540, 260, mix(hexc("d9d4c6"), col or GOLD, lit), r=30)
        text(c, lab, 0, 28, 74, mix(hexc("7a7468"), INK, lit))


TILES = (("Relevance", 400), ("Distance", 960), ("Prominence", 1520))


@scene("three")
def three(c, b, t):
    paper(c)
    wordcard(c, "Google's local results rest mainly on three things", 960, 170, 58, 1600, smooth(ramp(t, .1, .7)), PAPER, INK, 1)
    for i, (lab, x) in enumerate(TILES):
        if t < b.cue(lab) - .1:
            tile(c, x, 560, "?", back(ramp(t, .5 + i * .22, .45)), .35)
        else:
            tile(c, x, 560, lab, back(ramp(t, b.cue(lab) - .1, .4)), 1)


@scene("lock")
def lock(c, b, t):
    paper(c)
    t1 = b.cue("But the other")
    l = smooth(ramp(t, .4, .8))
    tile(c, 400, 560, "Relevance", 1, 1 if t > t1 else .3)
    tile(c, 1520, 560, "Prominence", 1, 1 if t > t1 else .3)
    tile(c, 960, 560, "Distance", 1, 1 - l * .8)
    k = back(ramp(t, .4, .5))
    if k > 0:
        with at(c, 960, 420, k):
            c.new_path(); c.arc(0, -36, 44, math.pi, 0); setc(c, INK); c.set_line_width(26); c.stroke()
            c.new_path(); c.arc(0, -36, 44, math.pi, 0); setc(c, GREY); c.set_line_width(14); c.stroke()
            rr(c, -68, -36, 136, 104, 14); ink(c, GOLD, 6); ell(c, 0, 8, 12); ink(c, INK, 0)
    wordcard(c, "Distance, you cannot change", 960, 170, 66, 1200, smooth(ramp(t, .2, .6)), PAPER, INK, 1) if t < t1 else None
    if t >= t1:
        wordcard(c, "The other two, you can", 960, 170, 72, 1200, smooth(ramp(t, t1, .6)), GOLD, INK, 1)
        for x in (400, 1520):
            with at(c, x, 800, back(ramp(t, t1 + .3, .5))):
                poly(c, [(-36, 40), (-36, -10), (-66, -10), (0, -76), (66, -10), (36, -10), (36, 40)]); ink(c, LEAF, 5)


def listing(c, x, y, s, t, k1=1.0, stars=0.0):
    """A local listing card on a phone."""
    with at(c, x, y, s):
        sx, sy, sw, sh = phone(c, 0, 0)
        def farm(x2):
            pass
        rr(c, sx, sy, sw, 190, 28); ink(c, hexc("a8d8f0"), 0)
        hill(c, [(sx, sy + 150), (0, sy + 120), (sx + sw, sy + 150)], GRASS, base=sy + 190)
        barn(c, 40, sy + 170, .34)
        text(c, "Your Farm", 0, sy + 250, 46, INK)


@scene("relevance")
def relevance(c, b, t):
    paper(c)
    listing(c, 390, 560, 1.3, t)
    text(c, "Relevance", 1290, 190, 86, TOMATO)
    wordcard(c, "Does your listing match the search?", 1270, 310, 54, 1100, smooth(ramp(t, .4, .6)), PAPER, INK, 1)
    rows = [("A complete profile", "A complete profile"), ("The right category", "the right category"),
            ("Real photos", "real photos"), ("Your opening hours", "your opening hours")]
    for i, (lab, cue) in enumerate(rows):
        t0 = b.cue(cue)
        k = smooth(ramp(t, t0, .45))
        y = 460 + i * 130
        tick(c, 900, y, 1.1, LEAF, k)
        text(c, lab, 970, y + 26, 72, INK, "l", k)
        # the same line fills in on the phone
        with at(c, 390, 560, 1.3):
            rr(c, -120, -28 + i * 60, 240 * k, 34, 8); ink(c, (LEAF, GOLD, SKY, TOMATO)[i], 0, a=k)


@scene("prominence")
def prominence(c, b, t):
    paper(c)
    text(c, "Prominence", 500, 170, 86, TOMATO)
    wordcard(c, "How well known you are", 500, 290, 58, 800, smooth(ramp(t, .4, .6)), PAPER, INK, 1)
    t1 = b.cue("reviews"); t2 = b.cue("and links")
    panel(c, 100, 420, 800, 410, PAPER, smooth(ramp(t, t1, .5)))
    if t >= t1:
        text(c, "Reviews", 500, 530, 74, INK)
        for i in range(5):
            e = back(ramp(t, t1 + i * .2, .4))
            if e > 0:
                star(c, 200 + i * 150, 680, 62 * e, GOLD, 0, 5)
    # links from other sites point at the farm
    cx, cy = 1420, 590
    k = t >= t2
    barn(c, cx, cy + 130, .8)
    if k:
        pos = [(1060, 280), (1770, 300), (1040, 790), (1770, 800), (1420, 180)]
        labels = ("Blog", "News", "Guide", "Tours", "Town")
        text(c, "Links", 1700, 190, 74, INK, "c", smooth(ramp(t, t2, .5)))
        for i, (x, y) in enumerate(pos):
            e = eout(ramp(t, t2 + i * .22, .4))
            if e <= 0:
                continue
            line(c, x, y, lerp(x, cx, e * .82), lerp(y, cy, e * .82), SKY, 8, dash=[4, 16])
            with at(c, x, y, e):
                panel(c, -105, -56, 210, 112, CREAM)
                text(c, labels[i], 0, 20, 54, INK)


@scene("nopay")
def nopay(c, b, t):
    paper(c)
    t1 = b.cue("Google says")
    host(c, b, t, 240, 1050, 1.05, "cheer" if t < 1.4 else "open", mood="happy" if t < t1 else None)
    wordcard(c, "Good news for a small budget", 1120, 170, 66, 1200, smooth(ramp(t, .1, .6)), GOLD, INK, 1)
    if t >= t1:
        # a money bag tries to buy its way up and bounces back
        q = (t - t1)
        rr(c, 1460, 330, 40, 620, 14); ink(c, GREY, 5)
        f = abs(math.sin(q * 2.2))
        x = lerp(880, 1360, f)
        with at(c, x, 800, 1, f * .2):
            c.new_path(); c.move_to(-34, -92); c.line_to(34, -92); c.line_to(76, 60); c.curve_to(60, 106, -60, 106, -76, 60); c.close_path(); ink(c, hexc("d9c79a"), 6)
            text(c, "$", 0, 44, 110, LEAF)
        k = smooth(ramp(t, t1 + .4, .6))
        wordcard(c, "No way to pay for a better local ranking", 1120, 460, 62, 1300, k, PAPER, TOMATO, 1)


@scene("found_forgot")
def found_forgot(c, b, t):
    t1, t2 = b.cue("The Worth-the-Drive"), b.cue("That is the difference")
    if t < t2:
        def L(x):
            with at(x, -200, 0, 1):
                _roadside(x, t)
            stand(x, 480, 900, 1.05)
            car(x, (t * 180) % 1300 - 200, 975, .78, SKY, t * 6)
        def R(x):
            longroad(x, t, "gold", (1460, 320))
            with at(x, 1440, 700, .9):
                pin(x, 0, 0, 1.5 + .08 * math.sin(t * 4), TOMATO)
            car(x, 1270, 950, .9, GOLD, t * 8, driver=crowd_look(5))
        if t < t1 - .2:
            _roadside(c, t)
            stand(c, 900, 900, 1.15)
            car(c, (t * 240) % 2300 - 200, 975, .84, SKY, t * 6)
            sign(c, 960, 130, .9, ["Found by accident"], sizes=[72], w=840)
            return
        half(c, 0, L); half(c, 1, R)
        rr(c, 950, -10, 20, H + 20, 0); ink(c, PAPER, 5)
        sign(c, 480, 130, .9, ["Found by accident"], sizes=[66], w=760)
        sign(c, 1440, 130, .9, ["Found on purpose"], sizes=[66], w=760, a=smooth(ramp(t, t1, .5)))
    else:
        q = t - t2
        t3 = b.cue("one that gets forgotten")
        def L(x):
            longroad(x, t, "day", (460, 240))
            gate(x, 500, 1000, 1.0, 1)
            crowd(x, 60, 900, 1040, .52, 5, t, 22)
        def R(x):
            fill_bg(x, SKIES["storm"])
            hill(x, [(960, 700), (1400, 660), (1980, 700)], hexc("9aa2b4"))
            hill(x, [(960, 820), (1400, 800), (1980, 820)], hexc("8a90a4"))
            gate(x, 1440, 1000, 1.0, 0, hexc("9a9486"))
        half(c, 0, L); half(c, 1, R)
        rr(c, 950, -10, 20, H + 20, 0); ink(c, PAPER, 5)
        sign(c, 480, 130, .9, ["Gets found"], sizes=[72], w=560)
        sign(c, 1440, 130, .9, ["Gets forgotten"], sizes=[72], w=640, a=smooth(ramp(t, t3 - .2, .5)))


@scene("hours")
def hours(c, b, t):
    longroad(c, t, "day")
    host(c, b, t, 270, 1050, 1.05, "think", look_x=7)
    t1 = b.cue("It is hours")
    bubble(c, 520, 110, 980, 280, (330, 640), thought=True, a=smooth(ramp(t, .1, .6)))
    text(c, "My farm is not 60 miles out.", 1010, 230, 62, INK, "c", smooth(ramp(t, .2, .6)))
    text(c, "It is hours out.", 1010, 330, 78, TOMATO, "c", smooth(ramp(t, t1, .4)))
    if t >= t1:
        clock(c, 1500, 720, 170 * back(ramp(t, t1, .5)), t * 1.6)


@scene("honest")
def honest(c, b, t):
    paper(c)
    wordcard(c, "The honest answer", 960, 140, 72, 900, smooth(ramp(t, .1, .6)), GOLD, INK, 1)
    t1 = b.cue("The further")
    k = smooth(ramp(t, t1, b.dur - t1 - .4))
    if t > t1 - .1:
        y = 860
        x1 = lerp(420, 1340, k)
        rr(c, 200, y - 26, x1 - 200, 52, 26); ink(c, DIRT, 5)
        barn(c, 260, y - 20, .46)
        star(c, x1 + 90, y - 60 - k * 240, 80 + k * 240, GOLD, math.sin(t) * .06, 6)
        text(c, "Reason", x1 + 90, y - 28 - k * 240, 40 + k * 44, INK)
        text(c, "Distance", 640, y + 100, 62, INK)


@scene("halfday")
def halfday(c, b, t):
    farmland(c, t, "gold", 6)
    host(c, b, t, 250, 1050, 1.05, "open")
    with at(c, 800, 620, back(ramp(t, .1, .5))):
        panel(c, -280, -210, 560, 420)
        clock(c, 0, -30, 130, t * .4)
        text(c, "An hour out", 0, 170, 66, INK)
    k = back(ramp(t, b.cue("a half-day") - .1, .5))
    if k > 0:
        line(c, 1100, 620, 1190, 620, TOMATO, 16)
        poly(c, [(1180, 590), (1236, 620), (1180, 650)]); ink(c, TOMATO, 4)
        with at(c, 1540, 620, k):
            panel(c, -280, -210, 560, 420, GOLD)
            sun(c, 0, -40, 86)
            text(c, "A half-day", 0, 170, 66, INK)


@scene("cabin")
def cabin_s(c, b, t):
    farmland(c, t, "night", 3, None, False)
    t1, t2, t3, t4 = b.cue("Tents."), b.cue("A cabin."), b.cue("A farm stay."), b.cue("Then the distance")
    k1, k2, k3 = back(ramp(t, t1, .5)), back(ramp(t, t2, .5)), back(ramp(t, t3, .5))
    if k1 > 0:
        tent(c, 330, 920, 1.25 * k1, GOLD, True); text(c, "Tents", 330, 1020, 60, WHITE)
    if k2 > 0:
        cabin(c, 960, 900, 1.25 * k2); text(c, "A cabin", 960, 1000, 60, WHITE)
    if k3 > 0:
        house(c, 1590, 900, 1.1 * k3, lit=True); text(c, "A farm stay", 1590, 1000, 60, WHITE)
    wordcard(c, "Somewhere to sleep", 960, 180, 70, 900, smooth(ramp(t, .2, .6)) * (1 - smooth(ramp(t, t4 - .2, .4))), PAPER, INK, 1)
    if t > t4 - .2:
        f = math.cos(clamp((t - t4 - 1.4) / .6) * math.pi)
        if t < t4 + 1.7:
            with at(c, 960, 240, 1, sx=1):
                sign(c, 0, 0, 1, ["A drive"], sizes=[100], w=620, a=smooth(ramp(t, t4 - .2, .4)))
        else:
            with at(c, 960, 240, back(ramp(t, t4 + 1.7, .5))):
                sign(c, 0, 0, 1, ["A getaway"], sizes=[100], w=660)


@scene("bar_gate")
def bar_gate(c, b, t):
    longroad(c, t, "gold", (980, 300))
    gate(c, 960, 960, 1.3, 1)
    k = smooth(ramp(t, .4, 1.4))
    y = lerp(640, 420, k)
    for x in (620, 1300):
        rr(c, x - 12, 340, 24, 620, 6); ink(c, GREY, 5)
    rr(c, 620, y - 14, 680, 28, 12); ink(c, TOMATO, 5)
    t1 = b.cue("It does not")
    wordcard(c, "Distance raises the bar", 960, 170, 76, 1200, smooth(ramp(t, .1, .6)), PAPER, INK, 1)
    if t > t1:
        wordcard(c, "It does not close the gate", 960, 300, 72, 1200, smooth(ramp(t, t1, .6)), GOLD, INK, 1)
    host(c, b, t, 230, 1050, 1.0, "point_r")


@scene("back1989")
def back1989(c, b, t):
    iowa(c, t, "sunset")
    t1, t2 = b.cue("He didn't"), b.cue("He cared")
    k = smooth(ramp(t, .2, b.dur))
    person(c, lerp(240, 560, k), 930, .84, STRANGER, t, "idle", walk=t * 1.1, seed=5)
    car(c, 150, 1000, .8, hexc("c4553a"))
    if t < t1:
        wordcard(c, "That stranger, 1989", 960, 170, 68, 900, smooth(ramp(t, .1, .6)), PAPER, INK, 1)
    elif t < t2:
        wordcard(c, "He didn't care how far", 960, 170, 68, 1000, smooth(ramp(t, t1, .6)), PAPER, INK, 1)
    else:
        wordcard(c, "He cared what was waiting", 960, 170, 68, 1200, smooth(ramp(t, t2, .6)), GOLD, INK, 1)


@scene("doing")
def doing(c, b, t):
    t1 = b.cue("Doing will")
    if t < t1 - .1:
        def room(x):
            fill_bg(x, [(0, hexc("f6e0b0")), (1, hexc("eccf95"))])
            rr(x, -20, 900, W + 40, 240, 0); ink(x, hexc("b58a5a"), 5)
        blit(c, "room2", room)
        rr(c, 560, 200, 800, 520, 24); ink(c, INK, 8)
        rr(c, 590, 228, 740, 464, 12); ink(c, hexc("a8d8f0"), 0)
        c.save(); rr(c, 590, 228, 740, 464, 12); c.clip()
        hill(c, [(590, 560), (960, 530), (1330, 560)], GRASS, base=700)
        gate(c, 960, 680, .8, 0)
        c.restore()
        rr(c, 900, 720, 120, 170, 6); ink(c, WOOD, 5)
        wordcard(c, "Watching won't change anything", 960, 110, 66, 1400, smooth(ramp(t, .1, .6)), PAPER, INK, 1)
    else:
        q = t - t1
        longroad(c, t, "gold", (980, 300))
        gate(c, 1150, 1020, 1.25, smooth(ramp(q, 0, 1)))
        dot(c, 620, 1050, 1.15, t, mouth_at(b.start + t), "cheer", mood="happy")
        stamp(c, "DOING WILL", 960, 240, 110, -.05, eout(ramp(q, 0, .35)), LEAF)


@scene("homework")
def homework(c, b, t):
    paper(c)
    t1, t2 = b.cue("Only at"), b.cue("how far you are")
    host(c, b, t, 230, 1050, 1.0, "point_r")
    panel(c, 470, 180, 1340, 720)
    ell(c, 570, 280, 44); ink(c, GOLD, 5)
    text(c, "Your comment", 640, 300, 62, INK, "l")
    s1 = "Only at our farm can you..."
    if t >= t1:
        n = int(len(s1) * clamp((t - t1) / 1.6))
        text(c, s1[:n], 540, 460, 76, INK, "l")
    if t >= t2:
        text(c, "We are ___ miles from town.", 540, 610, 74, TOMATO, "l", smooth(ramp(t, t2, .6)))
    wordcard(c, "Your homework", 960, 110, 68, 800, smooth(ramp(t, .1, .6)), GOLD, INK, 1)
    if t >= t2:
        wordcard(c, "In the comments", 1200, 790, 60, 800, smooth(ramp(t, t2 + .4, .6)), PAPER, SKY, 1)


@scene("guide")
def guide(c, b, t):
    farmland(c, t, "gold", 2)
    k = back(ramp(t, .4, .7))
    guide_book(c, 600, 550, 1.3 * max(k, .01), -.04)
    t1 = b.cue("Stop Being")
    wordcard(c, "Be found before they leave home", 1360, 300, 60, 800, smooth(ramp(t, .2, .6)), PAPER, INK, 1)
    if t >= t1:
        panel(c, 1000, 480, 800, 360, GOLD, smooth(ramp(t, t1, .5)))
        for i, l in enumerate(("Stop Being the", "Best-Kept Secret", "in Your County")):
            text(c, l, 1400, 590 + i * 96, 72, INK, "c", smooth(ramp(t, t1 + i * .25, .5)))


@scene("inside")
def inside(c, b, t):
    paper(c)
    guide_book(c, 300, 560, .92, -.04)
    rows = [("The three farms Google shows first", "the three farms"), ("A farm category guide", "a farm category"), ("A fifteen-shot photo list", "a fifteen-shot"),
            ("Scripts for asking for reviews", "scripts for"), ("Reply templates", "reply templates"), ("A thirty-day plan", "a thirty-day plan")]
    panel(c, 610, 100, 1230, 880)
    for i, (lab, cue) in enumerate(rows):
        t0 = b.cue(cue)
        k = smooth(ramp(t, t0, .45))
        y = 220 + i * 140
        tick(c, 700, y, 1.05, LEAF, k)
        text(c, lab, 770, y + 22, 60, INK, "l", k)


@scene("guarantee")
def guarantee(c, b, t):
    farmland(c, t, "day", 6)
    k = back(ramp(t, .2, .6))
    with at(c, 520, 560, k):
        pts = []
        for i in range(32):
            a = i * math.pi / 16
            q = 330 if i % 2 else 296
            pts.append((math.cos(a + t * .1) * q, math.sin(a + t * .1) * q))
        poly(c, pts); ink(c, GOLD, 7)
        ell(c, 0, 0, 250); ink(c, PAPER, 5)
        text(c, "30-day", 0, -56, 92, TOMATO); text(c, "money-back", 0, 34, 70, INK); text(c, "guarantee", 0, 116, 70, INK)
    t1 = b.cue("Click the link"); t2 = b.cue("and the guide")
    wordcard(c, "Link in the description", 1360, 300, 62, 900, smooth(ramp(t, t1, .6)), GOLD, INK, 1)
    if t >= t2:
        k2 = (t - t2) % 1.4 / 1.4
        y = 500 + k2 * 170
        line(c, 1360, 470, 1360, y, TOMATO, 26)
        poly(c, [(1296, y - 10), (1424, y - 10), (1360, y + 76)]); ink(c, TOMATO, 6)
        rr(c, 1190, 790, 340, 30, 12); ink(c, INK, 5)
        wordcard(c, "Downloads straight away", 1360, 910, 58, 900, smooth(ramp(t, t2, .6)), PAPER, INK, 1)


@scene("next")
def next_(c, b, t):
    paper(c)
    host(c, b, t, 240, 1050, 1.05, "point_r")
    with at(c, 1170, 450, back(ramp(t, .2, .6))):
        panel(c, -560, -320, 1120, 640)
        c.save(); rr(c, -552, -312, 1104, 624, 20); c.clip()
        with at(c, -552, -312, .575):
            longroad(c, t, "gold", (980, 300))
        gate(c, 300, 270, .8, smooth(ramp(t, 1.0, 1.4)))
        c.restore()
        text(c, "Start Agritourism With", 0, -176, 70, INK, "c", 1, halo=PAPER, halo_w=12)
        text(c, "What You Already Own", 0, -90, 70, INK, "c", 1, halo=PAPER, halo_w=12)
    t1 = b.cue("It shows")
    wordcard(c, "Open the gate without a loan", 1170, 900, 62, 1200, smooth(ramp(t, t1, .6)), GOLD, INK, 1)


@scene("final")
def final(c, b, t):
    longroad(c, t, "sunset", (960, 470))
    glow(c, 960, 520, 620, GOLD, .4)
    gate(c, 952, 612, .32, smooth(ramp(t, .4, 2)))
    t1 = b.cue("Make it")
    wordcard(c, "Don't fix the distance.", 960, 220, 86, 1400, smooth(ramp(t, .05, .6)), PAPER, INK, 1)
    wordcard(c, "Make it worth the drive.", 960, 390, 86, 1400, smooth(ramp(t, t1, .6)), GOLD, INK, 1)
    host(c, b, t, 250, 1060, 1.05, "wave")


@scene("endscreen")
def endscreen(c, b, t):
    # Dot waves at the open gate. Upper right stays clear for YouTube's end cards.
    longroad(c, t, "gold", (1000, 300))
    gate(c, 700, 1030, 1.05, 1)
    person(c, 240, 1050, 1.15, DOT, t, "wave", seed=7, mood="happy")
    text(c, "Agritourism Success", 480, 120, 62, INK, "c", 1, halo=PAPER)
    text(c, "AgritourismSuccess.com", 1440, 960, 56, INK, "c", 1, halo=PAPER)
    text(c, "Narration and animation are AI-generated.", 1440, 1030, 34, INK, "c", .9, weight="reg", halo=PAPER, halo_w=6)
