"""Two 1280x720 thumbnails, drawn with the same kit as the film."""
import os
import cairo
from toon import *
from cast import *
from sets import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")


def shoot(name, fn):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1280, 720)
    c = cairo.Context(s)
    c.scale(2 / 3, 2 / 3)
    fn(c)
    s.write_to_png(os.path.join(OUT, name))


def big(c, s, x, y, size, col=WHITE):
    text(c, s, x, y, size, col, "c", 1, halo=INK, halo_w=26)


def a(c):
    longroad(c, 3, "sunset", (960, 470))
    glow(c, 960, 520, 620, GOLD, .45)
    gate(c, 952, 612, .34, 1)
    big(c, "TOO FAR", 1330, 300, 230, GOLD)
    big(c, "FROM TOWN?", 1290, 520, 170)
    person(c, 330, 1090, 1.9, DOT, 0, "point_r", mood="wow", seed=7, look_x=8)


def b(c):
    winter(c, 2, n=60)
    greenhouse(c, 1330, 1000, 1.7, glow_a=1)
    big(c, "60 MILES OUT", 700, 210, 150)
    big(c, "180,000", 700, 430, 210, GOLD)
    big(c, "VISITORS", 700, 590, 130)
    person(c, 270, 1090, 1.4, DOT, 0, "cheer", mood="happy", seed=7)


def main():
    os.makedirs(OUT, exist_ok=True)
    shoot("thumbnail-a.png", a)
    shoot("thumbnail-b.png", b)
