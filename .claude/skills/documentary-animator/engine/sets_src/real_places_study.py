"""REAL PLACE, The Analyst's Study at night (24 Nov 2026), for The Nvidia Files Part 2, chapter 5 "Why It's a Big Deal for Your 401(k)".
Same method as real_places.py (CLAUDE.md 3d): flat 2D in REAL colours (cream wall, walnut panelling + desk, burgundy curtains, bookshelf,
night city in the window, green banker's lamp), then looks.real_night puts our brand on it. Status: PENDING owner approval."""
import math, skia
from engine.core import W, H
from engine.sets_src.night_scenes import rect, line, poly, circ, oval
from engine.sets_src.real_places import _night, _pl, _ov, LIT, BULB, LAMP, SCREEN

WIN = '#2B3F73'
BOOKS = ('#8E3B46', '#2F5D8C', '#C9A227', '#3E7D6B', '#D9D3C2', '#5B4A8A', '#B8643A', '#27408B')

def draw_study(c):
    rect(c, -10, -10, W + 10, 760, '#C9B995', 0)                                                           # cream wall
    rect(c, -10, 500, W + 10, 760, '#8A6644', 0); rect(c, -10, 492, W + 10, 516, '#6E4E31', 5)             # walnut panelling + rail
    for x in range(40, W, 200): rect(c, x, 546, x + 150, 716, None, 3, v='#6E4E31')
    rect(c, -10, 760, W + 10, H + 10, '#5C4430', 0)                                                        # floor
    for y in range(806, H, 54): line(c, -10, y, W + 10, y, 3, (60, 44, 28), 200)
    rect(c, 130, 96, 710, 500, '#E9E2D0', 8, r=6); rect(c, 152, 118, 688, 478, WIN, 4)                    # window, night glass
    for i in range(9):                                                                                     # city skyline + lit windows
        bx = 152 + i * 60; bh = 90 + (i * 53 % 150); rect(c, bx, 478 - bh, bx + 56, 478, '#1B2340', 3)
        for k in range(int(bh // 30)):
            for j in (0, 1):
                if (i + k + j) % 2 == 0: c.drawRect(skia.Rect(bx + 10 + j * 22, 478 - bh + 10 + k * 28, bx + 22 + j * 22, 478 - bh + 22 + k * 28), skia.Paint(Color=skia.Color(255, 210, 122)))
    line(c, 420, 118, 420, 478, 6); line(c, 152, 298, 688, 298, 6)
    rect(c, 96, 80, 170, 500, '#7A2E3C', 5, r=10); rect(c, 672, 80, 746, 500, '#7A2E3C', 5, r=10)         # curtains
    circ(c, 960, 220, 74, '#F4EFE2', 7); circ(c, 960, 220, 6, '#2E2E38', 2); line(c, 960, 220, 960, 168, 5); line(c, 960, 220, 998, 236, 5)   # wall clock
    for k in range(12):
        a = math.radians(k * 30); line(c, 960 + 60 * math.sin(a), 220 - 60 * math.cos(a), 960 + 68 * math.sin(a), 220 - 68 * math.cos(a), 3)
    rect(c, 1190, 90, 1810, 740, '#6B4A2E', 7)                                                             # bookshelf
    for r_ in range(5):
        y = 96 + r_ * 128; rect(c, 1200, y + 116, 1800, y + 128, '#8A6644', 4)
        x = 1210; k = 0
        while x < 1770:
            w = 22 + (k * 7 % 14); h = 70 + (k * 11 % 34); rect(c, x, y + 116 - h, x + w, y + 116, BOOKS[(k + r_) % len(BOOKS)], 3); x += w + 2; k += 1
    oval(c, 1000, 560, 1100, 700, '#3E8A3E', 5); rect(c, 1018, 700, 1082, 740, '#B8643A', 5, r=6)              # floor plant
    _credenza(c)

def _credenza(c):
    """Low credenza against the right-hand wall (BACKGROUND, behind the actors; the full body of the analyst always shows). Lamp + mug stand on it."""
    rect(c, 1190, 744, 1830, 770, '#B07A45', 6, r=8); rect(c, 1200, 770, 1820, 900, '#6B4627', 5)
    for x in (1220, 1520): rect(c, x, 788, x + 280, 884, None, 4, v='#4A2F1B'); circ(c, x + 140, 836, 8, '#C9A227', 3)
    rect(c, 1690, 728, 1790, 746, '#2E4A3A', 4, r=6); line(c, 1740, 728, 1740, 650, 8)                      # banker's lamp, green glass shade
    poly(c, [(1666, 650), (1814, 650), (1790, 602), (1690, 602)], '#1F6B4C', 5); circ(c, 1740, 664, 10, BULB, 2)
    rect(c, 1230, 704, 1276, 744, '#F4EFE2', 4, r=8); line(c, 1276, 716, 1292, 716, 4)                     # mug

def study_night():
    return _night([_ov(420, 300, 440, 260, .8), _pl(1740, 664, 360, 1.0), _ov(960, 940, 900, 190, .6), _ov(1500, 420, 360, 300, .3)],
                  glows=[(1740, 662, 70)], keep=('#7A2E3C', '#1F6B4C'), src=(LIT, LAMP, BULB, WIN))
