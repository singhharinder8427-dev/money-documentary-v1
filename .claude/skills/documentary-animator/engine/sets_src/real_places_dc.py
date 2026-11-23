"""REAL PLACES, Washington set for The Nvidia Files Part 2 (23 Nov 2026). Same method as real_places.py (CLAUDE.md 3d):
draw the real place flat 2D in REAL colours (layout + colours from memory of the public buildings; fresh shapes, never traced),
then looks.real_night puts our brand on it. Sets: white_house (exterior), oval_office, af1_cabin, commerce_hq (exterior), commerce_room.
Status: LOCKED by the owner (23 Nov 2026), do not change without asking."""
import math, skia
from engine.core import W, H
from engine.sets_src.night_scenes import rect, line, poly, circ, oval, shape, fp, ink, txt, MRK
from engine.sets_src.real_places import _night, _pl, _ov, LIT, BULB, LAMP, SCREEN

DC_SKY = ('#7E6FAE', '#9384BC', '#AE9CC9')
FLAG_RED, FLAG_BLUE, FLAG_WHITE = '#B22234', '#3C3B6E', '#FFFFFF'
FLAGS = (FLAG_RED, FLAG_BLUE)

def _sky(c, horizon):
    for k, (y0, y1) in enumerate(((0, horizon * .45), (horizon * .45, horizon * .75), (horizon * .75, horizon))):
        c.drawRect(skia.Rect(0, y0, W, y1 + 1), fp(DC_SKY[k]))

def _flag(c, px, top, w=170, h=100):
    """US flag on a pole: 13 stripes + blue canton (true flag colours, owner exception 1)."""
    line(c, px, top - 20, px, top + 420, 9); circ(c, px, top - 24, 8, '#C9A227', 3)
    sh = h / 13
    for i in range(13): c.drawRect(skia.Rect(px, top + i * sh, px + w, top + (i + 1) * sh + .5), fp(FLAG_RED if i % 2 == 0 else FLAG_WHITE))
    c.drawRect(skia.Rect(px, top, px + w * .42, top + sh * 7), fp(FLAG_BLUE)); rect(c, px, top, px + w, top + h, None, 4)
    for r_ in range(3):
        for k in range(4): c.drawCircle(px + 14 + k * 20, top + 12 + r_ * 20, 2.4, fp(FLAG_WHITE))

def _column(c, x, y0, y1, w=34):
    rect(c, x - w / 2, y0, x + w / 2, y1, '#F1EEE6', 4); rect(c, x - w / 2 - 6, y0 - 12, x + w / 2 + 6, y0, '#E4E0D4', 4); rect(c, x - w / 2 - 6, y1, x + w / 2 + 6, y1 + 12, '#E4E0D4', 4)
    for k in (-1, 0, 1): line(c, x + k * 9, y0 + 4, x + k * 9, y1 - 2, 2, (170, 165, 150), 160)

# ---------- 1. White House, north front at night (columns, portico, lawn, flag, railing)
def draw_white_house(c):
    _sky(c, 700)
    rect(c, -10, 760, W + 10, H + 10, '#4E8A3A', 0)                                                    # lawn
    for x in range(-100, W + 100, 150): c.drawLine(x + 60, 770, x - 100, H, ink(3, '#427A32', 120))
    poly(c, [(740, 770), (1180, 770), (1500, H), (420, H)], '#B9B2A2', 4)                              # drive
    for (x0, x1) in ((260, 700), (1220, 1660)):                                                        # white wings
        rect(c, x0, 470, x1, 770, '#F3F1EA', 5); rect(c, x0 - 10, 452, x1 + 10, 480, '#E4E0D4', 5)
        for k in range(14): line(c, x0 - 4 + k * (x1 - x0 + 8) / 13, 424, x0 - 4 + k * (x1 - x0 + 8) / 13, 452, 3)
        rect(c, x0 - 10, 424, x1 + 10, 432, '#E4E0D4', 3)
        for row, wy in enumerate((520, 650)):
            for wx in range(int(x0 + 34), int(x1 - 60), 84):
                lit = (wx // 84 + row) % 3 != 0
                rect(c, wx, wy, wx + 46, wy + 74, LIT if lit else '#59688A', 4); rect(c, wx - 5, wy - 9, wx + 51, wy, '#E4E0D4', 3)
                line(c, wx + 23, wy, wx + 23, wy + 74, 2.5)
    for cx_ in (420, 1500): rect(c, cx_, 390, cx_ + 34, 440, '#B5523B', 4)                              # chimneys (brick)
    rect(c, 690, 566, 1230, 600, '#EDEAE0', 5)                                                           # portico entablature
    poly(c, [(660, 566), (960, 450), (1260, 566)], '#F3F1EA', 5); poly(c, [(720, 560), (960, 470), (1200, 560)], None, 3, '#BDB8A8')
    rect(c, 700, 600, 1220, 770, '#E9E6DB', 4)
    rect(c, 900, 640, 1020, 770, LIT, 5, r=4); line(c, 960, 640, 960, 770, 4); poly(c, [(890, 640), (960, 604), (1030, 640)], '#EDEAE0', 4)   # lit door
    for x in (735, 860, 1060, 1185): _column(c, x, 604, 758)
    for x in range(690, 1240, 40): rect(c, x, 760, x + 28, 770, '#E4E0D4', 2)
    for k in range(4): rect(c, 690 - k * 14, 770 + k * 11, 1230 + k * 14, 782 + k * 11, '#D8D4C6', 4)  # steps
    for fx in (1496,): _flag(c, fx + 200, 320)                                                          # flag on a pole to the right
    for lx in (430, 1490): line(c, lx, 700, lx, 900, 8); poly(c, [(lx - 28, 700), (lx + 28, 700), (lx + 18, 674), (lx - 18, 674)], LAMP, 5)   # lamp posts
    line(c, -10, 905, W + 10, 905, 6); line(c, -10, 935, W + 10, 935, 4)                              # black railing
    for x in range(10, W, 70): line(c, x, 905, x, 935, 5)
def white_house_night():
    return _night([_pl(960, 640, 520, 1.0), _pl(480, 640, 360, .7), _pl(1440, 640, 360, .7), _pl(960, 840, 700, .5), _pl(430, 690, 260, .8), _pl(1490, 690, 260, .8)],
                  glows=[(430, 674, 60), (1490, 674, 60)], sky=DC_SKY, keep=FLAGS, src=(LIT, LAMP))

# ---------- 2. Oval Office (cream walls, gold drapes, flags, dark wood desk in FRONT of an actor at 'desk')
def draw_oval_office(c):
    c.drawRect(skia.Rect(0, 0, W, 760), fp('#EADFC0'))
    for x in range(0, W, 160): c.drawRect(skia.Rect(x, 0, x + 6, 760), fp('#DDD0AC'))
    rect(c, -10, 590, W + 10, 760, '#D8CAA3', 0); line(c, -10, 590, W + 10, 590, 4)                       # wainscot
    rect(c, -10, 760, W + 10, H + 10, '#B8A77C', 0)                                                       # floor
    c.save(); c.translate(960, 900)                                                                       # oval rug (blue + gold ring)
    c.drawOval(skia.Rect(-640, -150, 640, 150), fp('#2B4A7A')); c.drawOval(skia.Rect(-640, -150, 640, 150), ink(5)); c.drawOval(skia.Rect(-560, -118, 560, 118), ink(10, '#C9A227')); c.restore()
    for wx in (580, 960, 1340):                                                                           # three tall windows + gold drapes
        rect(c, wx - 90, 150, wx + 90, 590, '#59688A', 6); line(c, wx, 150, wx, 590, 5); line(c, wx - 90, 370, wx + 90, 370, 5)
        for sx in (-1, 1):
            poly(c, [(wx + sx * 90, 130), (wx + sx * 150, 150), (wx + sx * 160, 620), (wx + sx * 96, 600)], '#C99A2E', 5)
            for k in range(3): line(c, wx + sx * (104 + k * 18), 160, wx + sx * (112 + k * 18), 590, 2, (150, 110, 30), 170)
        rect(c, wx - 110, 118, wx + 110, 150, '#B8861E', 5)
    for (fx, col, canton) in ((300, FLAG_BLUE, True), (1560, None, False)):                              # presidential flag + US flag
        line(c, fx + 40, 160, fx + 40, 780, 10); circ(c, fx + 40, 150, 10, '#C9A227', 3)
        if canton:
            poly(c, [(fx + 40, 190), (fx + 240, 190), (fx + 230, 520), (fx + 40, 520)], FLAG_BLUE, 5); circ(c, fx + 134, 340, 42, '#C9A227', 4)
        else:
            sh = 25
            for i in range(13): c.drawRect(skia.Rect(fx + 40, 190 + i * sh, fx + 250, 190 + (i + 1) * sh + .5), fp(FLAG_RED if i % 2 == 0 else FLAG_WHITE))
            c.drawRect(skia.Rect(fx + 40, 190, fx + 140, 190 + sh * 7), fp(FLAG_BLUE)); rect(c, fx + 40, 190, fx + 250, 190 + sh * 13, None, 4)
    for sx in (-1, 1): rect(c, 960 + sx * 700 - 60, 560, 960 + sx * 700 + 60, 760, '#5B4631', 5)          # side tables
    _oval_desk(c)                                                                                         # base layer carries the desk too (fg reuses these pixels)
def _oval_desk(c):   # the Resolute-style desk, in FRONT of the actor at 'desk'
    rect(c, 690, 840, 1230, 880, '#9A6A3E', 6, r=6); rect(c, 710, 880, 1210, 1040, '#82552F', 6); rect(c, 740, 900, 1180, 1020, None, 4, r=6, v='#B88650')
    rect(c, 706, 1040, 760, 1060, '#4A2F1B', 4); rect(c, 1160, 1040, 1214, 1060, '#4A2F1B', 4)
def oval_office_night():
    return _night([_pl(960, 420, 560, .9), _pl(560, 330, 300, .6), _pl(1360, 330, 300, .6), _ov(960, 900, 700, 200, .55), _pl(960, 940, 380, 1.0)], glows=[], keep=FLAGS, src=(LIT, LAMP, '#59688A'))

# ---------- 3. Air Force One cabin (cream walls, blue seats + carpet, oval windows, wood table in FRONT)
def draw_af1_cabin(c):
    c.drawRect(skia.Rect(0, 0, W, 740), fp('#EFE7D4'))
    rect(c, -10, 120, W + 10, 200, '#D9D2C0', 4)                                                          # overhead bins
    for x in range(40, W, 240): c.drawRect(skia.Rect(x, 138, x + 160, 176), fp(LAMP))                     # cabin lights
    c.drawRect(skia.Rect(0, 330, W, 352), fp('#4B8FD1')); c.drawRect(skia.Rect(0, 352, W, 364), fp('#C9A227'))   # light-blue cheat stripe + gold line
    for wx in range(150, W, 300):                                                                         # oval windows, dark sky outside
        c.drawRoundRect(skia.Rect(wx - 62, 230, wx + 62, 400), 60, 80, fp(DC_SKY[0])); c.drawRoundRect(skia.Rect(wx - 62, 230, wx + 62, 400), 60, 80, ink(6, '#CFC8B6'))
        c.drawRoundRect(skia.Rect(wx - 62, 230, wx + 62, 400), 60, 80, ink(2, '#1E2622'))
    rect(c, -10, 740, W + 10, H + 10, '#2D4F7C', 0)                                                       # blue carpet
    for y in range(780, H, 60): line(c, -10, y, W + 10, y, 2, (30, 60, 100), 150)
    for sx in (-1, 1):                                                                                    # blue leather seats along both sides
        for k in range(2):
            x = 960 + sx * (690 + k * 150)
            rect(c, x - 70, 520, x + 70, 740, '#3A62A0', 5, r=24); rect(c, x - 54, 500, x + 54, 560, '#F4F1E8', 5, r=14)   # seat + headrest
            rect(c, x - 76, 640, x + 76, 700, '#2F528A', 5, r=14)
    rect(c, 880, 400, 1040, 470, '#E8DFC8', 4); line(c, 880, 436, 1040, 436, 3)                           # galley door
    _af1_table(c)
def _af1_table(c):
    rect(c, 640, 860, 1280, 900, '#B08A5C', 6, r=10); rect(c, 640, 896, 1280, 908, '#9A7548', 4)
    rect(c, 940, 908, 980, 1060, '#C9C3B5', 4)
    for (mx, my) in ((780, 836), (1130, 836)): rect(c, mx - 22, my, mx + 22, 862, '#FFFFFF', 5, r=6)    # two cups
def af1_cabin_night():
    return _night([_pl(300, 160, 360, .7), _pl(960, 160, 420, .8), _pl(1620, 160, 360, .7), _ov(960, 860, 700, 170, .5), _pl(960, 920, 460, 1.0)], sky=(DC_SKY[0],), keep=('#4B8FD1',), src=(LAMP,))

# ---------- 4. US Department of Commerce, Herbert C. Hoover Building, exterior (limestone colonnade, flags, steps)
def draw_commerce_hq(c):
    _sky(c, 640)
    rect(c, -10, 780, W + 10, H + 10, '#4A4A52', 0); rect(c, -10, 780, W + 10, 830, '#A39E94', 4)        # street + sidewalk
    for x in range(0, W, 220): c.drawRect(skia.Rect(x + 40, 960, x + 150, 974), fp('#F2EFE6', 230))
    rect(c, 100, 330, 1820, 780, '#D9D3C2', 6); rect(c, 80, 312, 1840, 346, '#C9C3B1', 5)                 # limestone block + cornice
    for k in range(20): line(c, 90 + k * 88, 346, 90 + k * 88, 366, 3)
    for x in range(160, 1780, 100): _column(c, x, 540, 760, 36)                                           # colonnade
    for wx in range(150, 1780, 100):
        for wy in (380,):
            rect(c, wx, wy, wx + 50, wy + 120, LIT if (wx // 100) % 3 else '#59688A', 4)                 # upper-floor windows
    rect(c, 80, 520, 1840, 546, '#C9C3B1', 4)
    rect(c, 860, 600, 1060, 780, '#3A3A44', 6, r=6); rect(c, 872, 612, 1048, 776, LIT, 4, r=4); line(c, 960, 612, 960, 776, 4)   # lit entrance
    circ(c, 960, 570, 26, '#C9A227', 5); circ(c, 960, 570, 14, '#E8D48A', 3)                              # gold department seal
    for k in range(5): rect(c, 800 - k * 12, 780 + k * 9, 1120 + k * 12, 790 + k * 9, '#CFC9B8', 3)       # steps
    _flag(c, 330, 560, 150, 90); _flag(c, 1540, 560, 150, 90)
    for lx in (520, 1400): line(c, lx, 700, lx, 900, 8); poly(c, [(lx - 26, 700), (lx + 26, 700), (lx + 16, 676), (lx - 16, 676)], LAMP, 5)
def commerce_hq_night():
    return _night([_pl(960, 650, 520, 1.0), _pl(520, 700, 260, .8), _pl(1400, 700, 260, .8), _ov(960, 520, 900, 220, .6), _ov(960, 880, 800, 110, .35)],
                  glows=[(520, 676, 60), (1400, 676, 60)], sky=DC_SKY, keep=FLAGS + ('#C9A227',), src=(LIT, LAMP))

# ---------- 5. Commerce conference room (long walnut table in FRONT, flags, one empty chair pulled out)
def draw_commerce_room(c):
    c.drawRect(skia.Rect(0, 0, W, 740), fp('#D9D1BC'))
    for x in range(0, W, 200): c.drawRect(skia.Rect(x, 0, x + 8, 740), fp('#C7BEA5'))
    rect(c, -10, 740, W + 10, H + 10, '#7A6A55', 0); [line(c, -10, y, W + 10, y, 3, (100, 86, 68)) for y in range(790, H, 56)]
    rect(c, 140, 120, 760, 470, '#1F2430', 8, r=8); rect(c, 160, 140, 740, 450, '#2B3A5C', 3, r=6)         # wall screen (blank)
    rect(c, 1160, 120, 1780, 470, '#59688A', 8); line(c, 1470, 120, 1470, 470, 5)                         # window
    for (fx, who) in ((880, 'us'), (1040, 'dept')):
        line(c, fx, 260, fx, 740, 8)
        poly(c, [(fx, 280), (fx + 110, 292), (fx + 110, 400), (fx, 388)], FLAG_BLUE if who == 'dept' else FLAG_RED, 4)
    for x in (470, 780, 1090, 1400):                                                                      # chairs behind the table
        rect(c, x - 60, 560, x + 60, 760, '#2B2F38', 5, r=22)
    rect(c, 1090 - 60, 560, 1090 + 60, 760, '#2B2F38', 5, r=22)
    _commerce_table(c)
def _commerce_table(c):
    rect(c, 200, 840, 1720, 900, '#9A6A3E', 6, r=10); rect(c, 200, 896, 1720, 912, '#82552F', 4)
    for x in (360, 1560): rect(c, x - 22, 912, x + 22, 1070, '#4A2F1B', 4)
    for (mx, my, rot) in ((520, 850, -4), (980, 846, 3), (1380, 850, -2)): c.save(); c.translate(mx, my); c.rotate(rot); rect(c, -70, -10, 70, 14, '#FBF8F0', 3); c.restore()
def commerce_room_night():
    return _night([_ov(450, 300, 380, 200, .8), _ov(1470, 300, 420, 200, .7), _pl(960, 120, 600, .6), _ov(960, 880, 800, 180, .55), _pl(960, 920, 760, 1.0)], src=(SCREEN, LAMP, '#59688A'))
