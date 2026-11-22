"""REAL PLACES - drawn in flat 2D with their REAL colours, then given our brand by looks.real_night (owner-locked
22 Nov 2026). Each place = draw_<name>(c) on a 1920x1080 canvas + a NIGHT dict with the light pools / glows / colours
for the night pass. Coordinates may come from a reference photo (P() maps photo pixels to the frame); everything is
drawn fresh in code - shapes only, never a traced or pasted photo."""
import numpy as np, skia
from engine.core import W, H

def col(h, a=255): h = h.lstrip('#'); return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
INK = '#1E2622'

# ============ NVIDIA HQ (Endeavor building, Santa Clara) - exterior at dusk/night, sign wall with the rough eye logo
# Reference: Nvidia press photo of the Endeavor entrance (layout + colours only). Spots: walkway, stairs, sign.
def _P_hq(x, y): return (x * .96, (y - 173) * .96)          # reference photo (2000x1334) -> frame
def draw_nvidia_hq(c):
    P = _P_hq
    def poly(c, pts, fill, line=None, lw=3):
        p = skia.Path(); p.moveTo(*P(*pts[0]))
        for q in pts[1:]: p.lineTo(*P(*q))
        p.close(); c.drawPath(p, skia.Paint(Color=col(fill), AntiAlias=True))
        if line: c.drawPath(p, skia.Paint(Color=col(line), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=lw, StrokeJoin=skia.Paint.kRound_Join))
    def ln(c, a, b, color, w=3): c.drawLine(*P(*a), *P(*b), skia.Paint(Color=col(color), AntiAlias=True, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap))

    # --- sky: dusk lavender, 3 flat bands
    for y0, y1, h in [(0, 260, '#7E6FAE'), (260, 520, '#9384BC'), (520, 1100, '#AE9CC9')]:
        c.drawRect(skia.Rect(0, y0, W, y1), skia.Paint(Color=col(h)))

    poly(c, [(0, 520), (2000, 520), (2000, 920), (0, 920)], '#55634F')        # distant ground / back wall
    poly(c, [(0, 540), (205, 660), (205, 790), (0, 790)], '#A39D90')
    # --- back right glass block (lighter, lit offices)
    poly(c, [(1400, 400), (2000, 380), (2000, 800), (1400, 800)], '#5E7466', INK)
    for i in range(1, 7): y = 395 + i * 52; ln(c, (1500, y), (2000, y - 4), '#8FA493', 3)
    for x in range(1560, 2000, 75): ln(c, (x, 393), (x, 760), '#8FA493', 2)
    for x, y in [(1640, 440), (1790, 440), (1715, 545), (1865, 600)]:
        poly(c, [(x, y), (x + 70, y), (x + 70, y + 46), (x, y + 46)], '#D9E7B8')           # lit windows
    poly(c, [(1400, 372), (2000, 300), (2000, 395), (1400, 400)], '#B9BDC2', INK)            # back roof

    # --- main glass volume (angular)
    glass = [(0, 425), (850, 262), (2000, 390), (1640, 400), (1185, 660), (205, 660), (0, 540)]
    poly(c, glass, '#26372F')
    # lit clerestory band under the roof
    poly(c, [(0, 470), (850, 300), (1640, 405), (1640, 440), (850, 345), (0, 510)], '#C9DDA6')
    # mullion grid: rows follow the facade, columns vertical
    for i in range(1, 9):
        t = i / 9; a = lerp((0, 510), (205, 660), t); b = lerp((850, 345), (1185, 660), t)
        ln(c, a, b, '#4F6B58', 3); ln(c, b, lerp((1640, 440), (1185, 660), t), '#4F6B58', 3)
    for x in range(60, 1640, 82):
        top = 510 - x * (165 / 850) if x < 850 else 345 + (x - 850) * (95 / 790)
        bot = 660 if x < 1185 else 660 - (x - 1185) * (260 / 455)
        if bot > top + 10: ln(c, (x, top), (x, bot), '#4F6B58', 2)
    ln(c, (930, 330), (1100, 650), '#6E8C75', 4)                                          # diagonal brace
    # roof edge: thin aluminium fascia
    poly(c, [(0, 410), (850, 248), (2000, 372), (2000, 392), (850, 266), (0, 432)], '#CDD0D4', INK)
    # glass outline
    p = skia.Path(); p.moveTo(*P(*glass[0])); [p.lineTo(*P(*q)) for q in glass[1:]]; p.close()
    c.drawPath(p, skia.Paint(Color=col(INK), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3))

    # --- concrete base + lit entrance
    poly(c, [(205, 660), (1185, 660), (1185, 790), (205, 790)], '#C2BBAC', INK)
    poly(c, [(205, 660), (430, 660), (450, 790), (205, 790)], '#A39D90')                      # shaded wedge
    poly(c, [(735, 662), (990, 662), (990, 785), (735, 785)], '#F3D9A0', INK)                   # warm lobby light
    for x in (790, 850, 910): ln(c, (x, 690), (x, 785), '#B98F4A', 3)
    poly(c, [(750, 668), (975, 668), (975, 682), (750, 682)], '#FFF1C9')

    # --- lawn slope left
    poly(c, [(0, 730), (300, 755), (660, 805), (660, 915), (0, 915)], '#5E9A3C', INK)
    poly(c, [(0, 810), (660, 860), (660, 915), (0, 915)], '#4E8732')

    # --- dark bushes right of the walkway + trees
    rb = np.random.default_rng(9)
    poly(c, [(930, 760), (1200, 700), (1500, 715), (1760, 760), (1760, 900), (930, 900)], '#4A3A40')
    for _ in range(70):
        cx = rb.uniform(940, 1750); top = 700 + abs(cx - 1250) * .08
        cy = rb.uniform(top + 10, 880); r = rb.uniform(28, 55)
        c.drawCircle(*P(cx, cy), r * .96, skia.Paint(Color=col(rb.choice(['#4A3A40', '#5A4650', '#3E3035'])), AntiAlias=True))
    for _ in range(120):                                           # reed tips
        x = rb.uniform(940, 1750); y = rb.uniform(720, 860)
        ln(c, (x, y), (x + rb.uniform(-10, 10), y - rb.uniform(25, 60)), rb.choice(['#6A5560', '#3E3035']), 3)
    for cx, cy, r in [(1720, 610, 70), (1850, 590, 85), (1960, 560, 70)]:
        ln(c, (cx, cy + r * .4), (cx, 790), '#5B4636', 6)
        c.drawCircle(*P(cx, cy), r * .96, skia.Paint(Color=col('#3F6A3A'), AntiAlias=True))
        c.drawCircle(*P(cx - r * .3, cy - r * .3), r * .45, skia.Paint(Color=col('#558A48'), AntiAlias=True))
    poly(c, [(930, 880), (1760, 880), (1840, 915), (930, 915)], '#3A6B32')                       # hedge strip

    # --- walkway (perspective, striped pavers)
    poly(c, [(775, 780), (905, 780), (935, 915), (330, 915)], '#8E8E8C', INK)
    for t in (.18, .42, .62, .82):
        a = lerp((775, 780), (905, 780), t); b = lerp((330, 915), (935, 915), t)
        ln(c, a, b, '#D6D3CA', 14)

    # --- retaining walls + stairs
    poly(c, [(0, 915), (330, 915), (330, 1135), (0, 1135)], '#B5AFA2', INK)
    poly(c, [(930, 905), (1205, 905), (1205, 1135), (1080, 1135)], '#A8A296', INK)
    for i in range(8):
        y = 915 + i * 27.5; x0 = 335 - i * 8; x1 = 990 + i * 22
        poly(c, [(x0, y), (x1, y), (x1, y + 27.5), (x0, y + 27.5)], '#CFC8B9' if i % 2 == 0 else '#C6BFAF')
        ln(c, (x0, y + 26), (x1, y + 26), '#8F897D', 3)
    # rails
    for pts in ([(360, 780), (330, 915), (275, 1130)], [(925, 785), (1000, 905), (1090, 1000), (1195, 1135)]):
        for a, b in zip(pts, pts[1:]): ln(c, a, b, '#E3E6E9', 5)
        for q in pts: ln(c, q, (q[0], q[1] + 120 if q[1] < 1050 else q[1]), '#C9CCD0', 4)

    poly(c, [(1835, 880), (2000, 860), (2000, 1140), (1835, 1140)], '#3F5A35')
    for cx, cy, r in [(1900, 900, 70), (1990, 880, 80)]: c.drawCircle(*P(cx, cy), r * .96, skia.Paint(Color=col('#4A3A40'), AntiAlias=True))
    # --- sign wall with rough Nvidia logo (drawn fresh, not traced)
    poly(c, [(1205, 910), (1840, 910), (1840, 1140), (1205, 1140)], '#9C978B', INK)
    poly(c, [(1205, 910), (1840, 910), (1840, 925), (1205, 925)], '#B7B2A5')
    lx, ly = P(1355, 948); sz = 118 * .96
    box = skia.Rect(lx + sz * .4, ly, lx + sz, ly + sz * .7)
    c.drawRect(box, skia.Paint(Color=col('#76B900'), AntiAlias=True))
    def eye_paths():
        out = []
        cx, cy = lx + sz * .5, ly + sz * .37
        for k, w_ in [(1.0, 10), (.62, 8)]:
            p = skia.Path(); p.moveTo(cx - sz * .5 * k, cy)
            p.quadTo(cx, cy - sz * .42 * k, cx + sz * .48 * k, cy + sz * .02)
            p.quadTo(cx, cy + sz * .42 * k, cx - sz * .5 * k, cy); out.append((p, w_))
        p = skia.Path(); p.addArc(skia.Rect(cx - sz * .17, cy - sz * .15, cx + sz * .13, cy + sz * .15), 120, 260); out.append((p, 7))
        return out
    for clip_in, colr in [(False, '#76B900'), (True, '#9C978B')]:
        c.save()
        if clip_in: c.clipRect(box)
        else: c.clipRect(box, skia.ClipOp.kDifference)
        for p, w_ in eye_paths():
            c.drawPath(p, skia.Paint(Color=col(colr), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w_, StrokeCap=skia.Paint.kRound_Cap))
        c.restore()
    font = skia.Font(skia.Typeface('DejaVu Sans', skia.FontStyle.Bold()), 66)
    tx, ty = P(1490, 1018)
    c.drawString('NVIDIA', tx + 4, ty + 4, font, skia.Paint(Color=col('#5E5A52'), AntiAlias=True))
    c.drawString('NVIDIA', tx, ty, font, skia.Paint(Color=col('#F2E9D6'), AntiAlias=True))

    # --- lamp posts (glowing disc heads)
    for x, top, base, r in [(255, 150, 900, 60), (450, 330, 850, 44), (555, 428, 820, 34), (625, 485, 800, 28)]:
        ln(c, (x, top + 10), (x, base), '#3A3F44', 10 if r > 40 else 7)
        gx, gy = P(x, top)
        pass
        c.drawOval(skia.Rect(gx - r, gy - r * .22, gx + r, gy + r * .22), skia.Paint(Color=col('#F6D46A'), AntiAlias=True))
        c.drawOval(skia.Rect(gx - r, gy - r * .22, gx + r, gy + r * .22), skia.Paint(Color=col('#6B6450'), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2))

    # --- foreground: path + tall grass
    poly(c, [(0, 1135), (2000, 1135), (2000, 1175), (0, 1175)], '#BDB8AD')
    poly(c, [(0, 1175), (2000, 1175), (2000, 1340), (0, 1340)], '#5E9440')
    rng = np.random.default_rng(4)
    for _ in range(260):
        x = rng.uniform(0, 2000); y = rng.uniform(1150, 1340); hgt = rng.uniform(30, 90)
        ln(c, (x, y), (x + rng.uniform(-18, 18), y - hgt), rng.choice(['#4C7F33', '#6EA64B', '#7A8F55', '#3F6C2A']), 3)


NVIDIA_HQ_SKY = ('#7E6FAE', '#9384BC', '#AE9CC9')
def nvidia_hq_night():
    P = _P_hq; lamps = [(255, 150, 60), (450, 330, 44), (555, 428, 34), (625, 485, 28)]
    pools = [(*P(x, t), r * 5.5, .9, .8) for x, t, r in lamps]
    pools += [(*P(862, 720), 420, 1.1, 1.3)]                       # lobby spill on walkway + stairs
    pools += [(P(1520, 1120)[0], P(1520, 1120)[1], 330, 1.2, 1.4)] # uplight on the sign wall (x squash handled by radius)
    glows = [(*P(x, t), r) for x, t, r in lamps]
    return dict(sky=NVIDIA_HQ_SKY, pools=pools, glows=glows, spot_gold=('#F6D46A',), keep=('#76B900',))


# =====================================================================================================================
# THE NVIDIA FILES sets, redrawn in REAL colours (22 Nov 2026; the old navy versions were deleted). Same layout as
# before, so actor spots and the blank frames the shots draw into (sign frame, wall panel, calendar, wall screen)
# stay exactly where they were.
# =====================================================================================================================
import math, random
from engine.sets_src.night_scenes import rect, line, poly, circ, oval, shape, fp, ink, city, clock, txt, MRK
LIT = '#FFD27A'; BULB = '#FFE2A0'; LAMP = '#F6D46A'; SCREEN = '#5B9BE8'
LIGHTS = (LIT, BULB, LAMP, SCREEN, '#FF5A6E')
def _ov(x, y, rx, ry, k): return (x, y, rx, k, rx / ry)       # old NS.night oval -> real_night pool
def _pl(x, y, r, k=.9): return (x, y, r, k, 1.0)
def _night(pools, glows=(), keep=(), src=LIGHTS, sky=()):
    return dict(pools=pools, glows=glows, spot_gold=(LAMP,), keep=keep, src_cols=src, sky=sky)

def _desk(c, x, floor_y, s=1.0, screen=True):
    """Office workstation in real colours: chair, metal legs, drawer unit, wood top, monitor on a stand, keyboard, mug."""
    top = floor_y - 150 * s
    rect(c, x + 40 * s, top - 110 * s, x + 150 * s, top - 10 * s, '#2B2F38', 5, r=14)                      # chair back
    for lx in (x - 160 * s, x + 150 * s): rect(c, lx, top + 10 * s, lx + 12 * s, floor_y, '#8A8F98', 4)   # metal legs
    rect(c, x + 60 * s, top + 16 * s, x + 150 * s, floor_y - 6 * s, '#D9D6CF', 4)                          # drawer unit
    for k in range(2): rect(c, x + 72 * s, top + 30 * s + k * 50 * s, x + 138 * s, top + 70 * s + k * 50 * s, None, 3, v='#A9A59C'); circ(c, x + 105 * s, top + 50 * s + k * 50 * s, 4 * s, '#8A8F98', 2)
    p = skia.Path(); p.moveTo(x - 180 * s, top); p.lineTo(x + 180 * s, top); p.lineTo(x + 170 * s, top - 24 * s); p.lineTo(x - 170 * s, top - 24 * s); p.close()
    c.drawPath(p, fp('#C9A273')); c.drawPath(p, ink(5)); rect(c, x - 180 * s, top, x + 180 * s, top + 16 * s, '#A9814F', 5)
    rect(c, x - 70 * s, top - 34 * s, x - 10 * s, top - 26 * s, '#2E2E38', 3); rect(c, x - 46 * s, top - 64 * s, x - 34 * s, top - 30 * s, '#2E2E38', 3)
    rect(c, x - 130 * s, top - 190 * s, x + 50 * s, top - 60 * s, '#1E2026', 5, r=6); rect(c, x - 120 * s, top - 180 * s, x + 40 * s, top - 70 * s, SCREEN if screen else '#0A1330', 3)
    if screen:
        g = skia.Path(); g.moveTo(x - 110 * s, top - 90 * s)
        for j in range(1, 7): g.lineTo(x - 110 * s + j * 24 * s, top - 90 * s - (j * 11 + (10 if j % 2 else 0)) * s)
        c.drawPath(g, ink(5, '#FFFFFF'))
    rect(c, x - 120 * s, top - 20 * s, x + 20 * s, top - 8 * s, '#3A3F4F', 3, r=3)
    rect(c, x + 90 * s, top - 46 * s, x + 120 * s, top - 14 * s, '#FBF8F0', 3, r=4)

def _plant(c, px, base=720, s=1.0):
    rect(c, px - 34 * s, base - 80 * s, px + 34 * s, base, '#C9B79A', 5, r=8)
    for k in range(5): oval(c, px + (-60 + k * 24) * s, base - (200 - (k % 2) * 30) * s, px + (-20 + k * 24) * s, base - 70 * s, ('#3E8A3E', '#2F6F33')[k % 2], 4)

# ---------- 1. Singapore shophouse street
def draw_sg_street(c):
    city(c, 0, 0, W, 600, seed=21)
    for x in (740, 900, 1060):                                     # three towers + sky deck (bay-front silhouette)
        poly(c, [(x, 150), (x + 62, 150), (x + 92, 610), (x - 30, 610)], '#B9BEC6', 5)
        for k in range(8): c.drawLine(x + 6 + k * 3, 170, x + 24 + k * 10, 600, ink(2, (120, 128, 140), 150))
    rect(c, 690, 118, 1190, 156, '#C9CDD3', 5, r=20); rect(c, 1130, 110, 1230, 126, '#A9AEB6', 3, r=8)
    rect(c, -10, 760, W + 10, H + 10, '#4A4A4F', 0); [line(c, -10, y, W + 10, y, 3, (66, 66, 72)) for y in range(800, H, 46)]
    rect(c, -10, 740, W + 10, 790, '#A39886', 4)                                                         # five-foot way
    for x in range(0, W, 220): c.drawRect(skia.Rect(x + 40, 930, x + 150, 944), fp('#F2EFE6', 230))
    for (x0, w, col, trim) in [(-20, 520, '#9FD3C0', '#6FB09A'), (520, 700, '#F2D48A', '#D9B562'), (1220, 720, '#E8A9B5', '#C9828F')]:
        x1 = x0 + w; rect(c, x0, 250, x1, 760, col, 6)
        rect(c, x0, 228, x1, 258, '#B5523B', 5)                                                          # terracotta roof edge
        rect(c, x0, 258, x1, 286, trim, 5)
        for wx in range(int(x0 + 50), int(x1 - 80), 130):
            for wy in (320, 470):
                p = skia.Path(); p.moveTo(wx, wy + 100); p.lineTo(wx, wy + 30); p.arcTo(skia.Rect(wx, wy - 20, wx + 80, wy + 80), 180, 180, False); p.lineTo(wx + 80, wy + 100); p.close()
                shape(c, p, LIT if (wx + wy) % 3 else '#3E7D6B', 5)                                       # lit / teal shutters
                for sx in (wx + 20, wx + 40, wx + 60): c.drawLine(sx, wy + 8, sx, wy + 100, ink(2.5, (40, 60, 52), 180))
        for ax in range(int(x0 + 30), int(x1 - 60), 170):
            rect(c, ax, 640, ax + 120, 760, '#5C4A3A' if ax % 3 else '#3A2E26', 5, r=6)                   # arcade openings
    rect(c, 700, 322, 1220, 438, '#1A1F2B', 8, r=10); rect(c, 712, 334, 1208, 426, None, 3, r=6, v='#5A6478')   # BLANK sign frame
    rect(c, 880, 560, 1040, 760, LIT, 7, r=6); line(c, 960, 560, 960, 760, 5); circ(c, 944, 670, 6, '#2E2E38', 3); circ(c, 976, 670, 6, '#2E2E38', 3)
    rect(c, 860, 540, 1060, 566, '#7A4A2E', 5)
    for lx in (330, 1610):
        line(c, lx, 330, lx, 800, 9); poly(c, [(lx - 36, 330), (lx + 36, 330), (lx + 22, 304), (lx - 22, 304)], LAMP, 5)
    for lx in (500, 1420): circ(c, lx, 560, 22, '#E0453A', 4); line(c, lx, 500, lx, 538, 4)                # red lanterns
def sg_street_night():
    return _night([_pl(330, 360, 330), _pl(1610, 360, 330), _ov(960, 380, 380, 140, .9), _ov(960, 700, 300, 160, .8), _ov(960, 880, 700, 90, .35)],
                  glows=[(330, 318, 60), (1610, 318, 60)], src=(LIT, LAMP))

# ---------- 2. Megaspeed office
def draw_megaspeed(c):
    for i, x in enumerate(range(0, W, 80)): c.drawRect(skia.Rect(x, 0, x + 80, 700), fp('#E8E6E1' if i % 2 else '#DEDBD4'))
    rect(c, -10, 700, W + 10, H + 10, '#6B7280', 0); [line(c, -10, y, W + 10, y, 3, (92, 98, 110)) for y in range(760, H, 56)]
    city(c, 90, 120, 620, 520, seed=33); [line(c, 90 + 530 * b, 120, 90 + 530 * b, 520, 7) for b in (.33, .66)]; line(c, 90, 320, 620, 320, 7); rect(c, 90, 120, 620, 520, None, 8)
    rect(c, 700, 150, 1220, 330, '#1F2430', 8, r=8)                                                       # blank wall panel
    rect(c, 1330, 150, 1850, 720, '#2A3140', 8)
    for k, x in enumerate(range(1370, 1830, 100)):
        rect(c, x, 190, x + 80, 700, '#1C1F25', 5, r=6)
        for yy in range(210, 690, 46):
            rect(c, x + 8, yy, x + 72, yy + 34, '#2C3038', 2, r=3)
            for j in range(4): c.drawCircle(x + 20 + j * 14, yy + 17, 4, fp(SCREEN if (yy // 46 + j + k) % 3 else '#F2A23A'))
    c.drawRect(skia.Rect(1330, 150, 1850, 720), fp((220, 235, 255), 26)); rect(c, 1330, 150, 1850, 720, None, 8); line(c, 1590, 150, 1590, 720, 6)
    for (dx, fy, sc) in ((300, 840, .85), (700, 840, .85), (1100, 840, .85), (250, 1010, 1.05), (820, 1010, 1.05)): _desk(c, dx, fy, sc)
def megaspeed_night():
    return _night([_ov(360, 330, 340, 260, .85), _ov(1590, 420, 360, 340, .9), _ov(960, 240, 300, 120, .7), _ov(700, 850, 700, 160, .7)])

# ---------- 3. 1993 roadside diner (booth table in FRONT of the actors = fg)
def _diner_table(c):
    rect(c, 560, 850, 1540, 920, '#E9DCC0', 6, r=10); rect(c, 560, 906, 1540, 920, '#B9BEC6', 3)        # formica top, chrome edge
    rect(c, 1010, 920, 1090, 1100, '#9AA0A8', 5)
    for (mx, my) in ((780, 820), (1300, 822)): rect(c, mx - 24, my, mx + 24, 856, '#FFFFFF', 5, r=6)
    rect(c, 1010, 806, 1070, 850, '#E0453A', 4, r=5)                                                       # ketchup-red napkin box
def draw_diner93(c, table=True):
    c.drawRect(skia.Rect(0, 0, W, 700), fp('#F1E3C6'))
    c.drawRect(skia.Rect(0, 520, W, 560), fp('#C0392B'))                                                   # red wall stripe
    for x in range(0, W, 120): c.drawRect(skia.Rect(x, 560, x + 60, 700), fp('#E6D3AE'))
    rect(c, -10, 700, W + 10, H + 10, '#EDE8DC', 0)
    for y in range(700, H, 70):
        for x in range(((y // 70) % 2) * 70, W, 140): c.drawRect(skia.Rect(x, y, x + 70, y + 70), fp('#2A2A2E'))
    city(c, 1120, 130, 1800, 520, seed=47); rect(c, 1120, 130, 1800, 520, None, 8); line(c, 1460, 130, 1460, 520, 8); line(c, 1120, 330, 1800, 330, 8)
    for hx_ in (1180, 1300, 1700): c.drawCircle(hx_, 470, 9, fp(BULB, 230))
    c.drawRect(skia.Rect(1120, 470, 1800, 520), fp('#3A3A40'))
    rect(c, 160, 110, 560, 230, '#1A1F2B', 7, r=14); txt(c, 'DINER', 360, 205, 96, '#FF5A6E', MRK, 'center', skew=0)   # red neon
    rect(c, 640, 120, 860, 400, '#FBF8F0', 5); rect(c, 640, 120, 860, 180, '#C0392B', 5)                  # calendar frame
    clock(c, 960, 210, 60, 11.3)
    rect(c, 60, 430, 520, 560, '#D7DCE2', 6, r=8); rect(c, 74, 444, 506, 520, '#EEF2F6', 3)
    for k in range(3): circ(c, 140 + k * 140, 482, 34, '#E8C77A', 4); circ(c, 140 + k * 140, 482, 16, '#B5523B', 2)
    rect(c, 80, 580, 900, 640, '#C0392B', 6); rect(c, 80, 640, 900, 760, '#C9CDD3', 5)                     # red counter, chrome front
    for x in (200, 360, 520, 680, 820): line(c, x, 640, x, 770, 8); oval(c, x - 40, 600, x + 40, 650, '#C0392B', 5)
    rect(c, 600, 540, 1020, 960, '#B83227', 6, r=26); rect(c, 1060, 540, 1480, 960, '#B83227', 6, r=26)    # red vinyl booths
    if table: _diner_table(c)
def diner93_night():
    return _night([_ov(360, 160, 260, 120, .95), _ov(960, 700, 800, 380, .75), _ov(1460, 330, 380, 230, .8), _ov(1040, 840, 500, 120, .8)],
                  glows=[(360, 170, 90)], src=(LIT, BULB, '#FF5A6E'))

# ---------- 4. Singapore Italian restaurant (candle table in FRONT = fg)
def _rest_table(c):
    poly(c, [(520, 830), (1400, 830), (1490, 1090), (430, 1090)], '#F7F3EA', 7)
    for xx in (620, 800, 960, 1120, 1300): c.drawLine(xx, 840, xx - (960 - xx) * .12, 1086, ink(2.5, (210, 204, 190), 200))
    rect(c, 940, 760, 980, 840, '#FBF8F0', 4, r=4)
    for (gx, gy) in ((780, 820), (1130, 822)):
        g = skia.Path(); g.moveTo(gx - 20, gy - 70); g.lineTo(gx + 20, gy - 70); g.quadTo(gx + 20, gy - 20, gx, gy - 12); g.quadTo(gx - 20, gy - 20, gx - 20, gy - 70)
        c.drawPath(g, fp((150, 30, 50), 200)); c.drawLine(gx, gy - 12, gx, gy + 10, ink(5)); c.drawLine(gx - 16, gy + 10, gx + 16, gy + 10, ink(5))   # red wine
        oval(c, gx - 30, gy + 14, gx + 30, gy + 34, '#FBF8F0', 4)
    f = skia.Path(); f.moveTo(960, 740); f.cubicTo(950, 710, 970, 700, 960, 672); f.cubicTo(985, 700, 985, 722, 960, 740); c.drawPath(f, fp(LAMP))
def draw_restaurant(c, table=True):
    c.drawRect(skia.Rect(0, 0, W, 720), fp('#B86B45'))
    for x in range(0, W, 60): c.drawRect(skia.Rect(x, 0, x + 30, 720), fp('#A85E3B'))
    rect(c, -10, 720, W + 10, H + 10, '#5A3A26', 0); [line(c, -10, y, W + 10, y, 3, (74, 48, 32)) for y in range(760, H, 60)]
    for (x0, x1) in ((140, 560), (1360, 1780)):
        p = skia.Path(); p.moveTo(x0, 520); p.lineTo(x0, 260); p.arcTo(skia.Rect(x0, 120, x1, 400), 180, 180, False); p.lineTo(x1, 520); p.close()
        c.save(); c.clipPath(p, doAntiAlias=True); city(c, x0, 120, x1, 520, seed=60 + x0 // 100); c.restore(); shape(c, p, None, 9); line(c, (x0 + x1) / 2, 120, (x0 + x1) / 2, 520, 6)
    rect(c, 640, 190, 1280, 500, '#6B4429', 7, r=6)
    for sy in (260, 340, 420): line(c, 650, sy + 40, 1270, sy + 40, 7)
    for sy in (260, 340, 420):
        for bx in range(676, 1250, 52):
            rect(c, bx, sy - 18, bx + 24, sy + 40, '#2F4A2F' if (bx // 52) % 3 else '#5C1F2A', 3, r=7); rect(c, bx + 7, sy - 38, bx + 17, sy - 16, '#2F4A2F', 3, r=3); c.drawRect(skia.Rect(bx + 3, sy + 8, bx + 21, sy + 26), fp('#F2E9D6'))
    for lx in (420, 960, 1500): line(c, lx, 0, lx, 110, 4); poly(c, [(lx - 62, 150), (lx + 62, 150), (lx + 34, 108), (lx - 34, 108)], LAMP, 5)
    for (tx, ty) in ((260, 660), (1660, 660)):
        oval(c, tx - 120, ty, tx + 120, ty + 40, '#F7F3EA', 5); line(c, tx, ty + 40, tx, ty + 200, 8); rect(c, tx - 10, ty - 22, tx + 10, ty, '#FBF8F0', 3, r=3)
    if table: _rest_table(c)
def restaurant_night():
    return _night([_ov(960, 860, 560, 220, 1.0), _pl(420, 220, 360, .95), _pl(960, 220, 380, .95), _pl(1500, 220, 360, .95), _ov(960, 600, 900, 260, .45)],
                  glows=[(960, 710, 60), (420, 135, 60), (960, 135, 60), (1500, 135, 60)], src=(LIT, LAMP))

# ---------- 5. Malaysian data-center aisle
def draw_datacenter(c):
    VX, VY = 960, 440
    c.drawRect(skia.Rect(0, 0, W, H), fp('#3A3F48'))
    ceil = skia.Path(); ceil.moveTo(0, 0); ceil.lineTo(W, 0); ceil.lineTo(VX + 120, VY - 70); ceil.lineTo(VX - 120, VY - 70); ceil.close(); shape(c, ceil, '#4A505A', 5)
    flr = skia.Path(); flr.moveTo(0, H); flr.lineTo(W, H); flr.lineTo(VX + 120, VY + 60); flr.lineTo(VX - 120, VY + 60); flr.close(); shape(c, flr, '#8E949C', 5)
    for k in range(-5, 6): line(c, VX + k * 22, VY + 60, VX + k * 230, H, 3, (110, 116, 124), 200)
    for z in (1.15, 1.5, 2.0, 2.8, 4.0): y = VY + 470 / z; line(c, VX - 1100 / z, y, VX + 1100 / z, y, 3, (110, 116, 124), 200)   # raised-floor tiles
    rect(c, VX - 120, VY - 70, VX + 120, VY + 60, '#2A2E36', 6)
    X = lambda side, z: VX + side * 1100 / z; T = lambda z: VY - 520 / z; B = lambda z: VY + 470 / z
    zs = [1.0, 1.28, 1.64, 2.1, 2.7, 3.45, 4.4, 5.6]
    for side in (-1, 1):
        for i in range(len(zs) - 1):
            za, zb = zs[i], zs[i + 1]
            p = skia.Path(); p.moveTo(X(side, za), T(za)); p.lineTo(X(side, zb), T(zb)); p.lineTo(X(side, zb), B(zb)); p.lineTo(X(side, za), B(za)); p.close()
            if i % 4 != 3:
                shape(c, p, '#1C1F25', 6)
                for k in range(1, 9):
                    ya, yb = T(za) + (B(za) - T(za)) * k / 9, T(zb) + (B(zb) - T(zb)) * k / 9
                    line(c, X(side, za), ya, X(side, zb), yb, 3, (44, 48, 56))
                    for j in range(4):
                        tt = (j + .5) / 4; lx = X(side, za) + (X(side, zb) - X(side, za)) * tt; ly = ya + (yb - ya) * tt + (B(zb) - T(zb)) / 22
                        c.drawCircle(lx, ly, max(2.2, 5.5 / ((za + zb) / 2)), fp(SCREEN if (i + j + k) % 3 else '#F2A23A'))
            else: shape(c, p, '#2A2E36', 5)
    for z in (1.3, 2.3, 3.6, 5.2): y0 = VY - 520 / z - 4; c.drawRect(skia.Rect(VX - 300 / z, y0 - 22 / z, VX + 300 / z, y0), fp(BULB))
    def box(cx, base, w, h):
        d = w * .28; rect(c, cx - w / 2, base - h, cx + w / 2, base, '#C49A62', 6, r=3)
        tp = skia.Path(); tp.moveTo(cx - w / 2, base - h); tp.lineTo(cx - w / 2 + d, base - h - d * .7); tp.lineTo(cx + w / 2 + d, base - h - d * .7); tp.lineTo(cx + w / 2, base - h); tp.close(); shape(c, tp, '#D9B37C', 5)
        sd = skia.Path(); sd.moveTo(cx + w / 2, base - h); sd.lineTo(cx + w / 2 + d, base - h - d * .7); sd.lineTo(cx + w / 2 + d, base - d * .7); sd.lineTo(cx + w / 2, base); sd.close(); shape(c, sd, '#A57E4C', 5)
        c.drawRect(skia.Rect(cx - 6, base - h, cx + 6, base), fp('#3A2E22', 220)); c.drawRect(skia.Rect(cx - w / 2, base - h * .5 - 8, cx + w / 2, base - h * .5 + 8), fp('#3A2E22', 220))
        txt(c, 'SERVERS', cx, base - h * .74, max(14, w * .13), '#2A2018', MRK, 'center', skew=0)
    box(520, 960, 260, 200); box(760, 880, 170, 140); box(1360, 940, 250, 190); box(1580, 1010, 300, 230); box(1160, 800, 110, 90)
def datacenter_night():
    return _night([_ov(960, 520, 640, 380, .6), _ov(960, 160, 540, 90, .85), _ov(960, 900, 800, 160, .45)], src=(BULB,))

# ---------- 6. Nvidia office (green accents = company colour, CLAUDE.md 3b)
def draw_nvidia_office(c):
    c.drawRect(skia.Rect(0, 0, W, 720), fp('#E9E7E2'))
    for x in range(0, W, 240): c.drawRect(skia.Rect(x, 0, x + 6, 720), fp('#D3D0C8'))
    c.drawRect(skia.Rect(0, 640, W, 652), fp('#76B900'))                                                   # Nvidia green wall band
    rect(c, -10, 720, W + 10, H + 10, '#B88A5E', 0); [line(c, -10, y, W + 10, y, 3, (160, 118, 80)) for y in range(780, H, 60)]
    city(c, 60, 110, 520, 560, seed=81); rect(c, 60, 110, 520, 560, None, 8); line(c, 290, 110, 290, 560, 7)
    rect(c, 640, 110, 1280, 520, '#0A1330', 9, r=10); rect(c, 662, 132, 1258, 498, '#0F1E44', 3, r=6)   # big wall screen (blank)
    rect(c, 940, 520, 980, 600, '#2E2E38', 4)
    rect(c, 1400, 110, 1860, 560, '#BFD3DE', 8); c.drawRect(skia.Rect(1400, 110, 1860, 560), fp((255, 255, 255), 40))
    for xx in (1550, 1710): line(c, xx, 110, xx, 560, 5)
    rect(c, 1430, 400, 1830, 430, '#76B900', 0)                                                          # green stripe on the glass
    for px in (590, 1330): _plant(c, px)
    for (dx, fy, sc) in ((380, 880, .8), (1540, 880, .8), (300, 1050, 1.0), (1620, 1050, 1.0)): _desk(c, dx, fy, sc)
def nvidia_office_night():
    return _night([_ov(960, 320, 420, 260, .9), _ov(300, 340, 300, 260, .8), _ov(960, 900, 800, 200, .7), _ov(1630, 330, 300, 260, .7)], keep=('#76B900',))

# ---------- 7. Newsroom
def draw_newsroom(c):
    c.drawRect(skia.Rect(0, 0, W, 700), fp('#5B6B82'))
    rect(c, -10, 700, W + 10, H + 10, '#4A4F5A', 0); [line(c, -10, y, W + 10, y, 3, (66, 72, 84)) for y in range(760, H, 56)]
    for i in range(6):
        x0, y0 = 160 + (i % 3) * 300, 110 + (i // 3) * 200; rect(c, x0, y0, x0 + 270, y0 + 170, '#16181E', 6, r=6); rect(c, x0 + 12, y0 + 12, x0 + 258, y0 + 158, SCREEN, 2, r=4)
        c.drawRect(skia.Rect(x0 + 12, y0 + 120, x0 + 258, y0 + 158), fp('#C0392B')); c.drawRect(skia.Rect(x0 + 20, y0 + 128, x0 + 160, y0 + 140), fp('#FFFFFF'))
    for k, (cx, nm) in enumerate(((1250, 'NEW YORK'), (1480, 'LONDON'), (1710, 'SINGAPORE'))):
        circ(c, cx, 220, 80, '#FBF8F0', 6); line(c, cx, 220, cx + 30 * math.cos(k), 220 - 50, 6); line(c, cx, 220, cx + 40, 220 + 10 * k, 5)
        txt(c, nm, cx, 340, 28, '#E9EDF2', align='center')
    for (dx, fy, sc) in ((260, 860, .8), (700, 860, .8), (1140, 860, .8), (1580, 860, .8)): _desk(c, dx, fy, sc)
def newsroom_night():
    return _night([_ov(610, 310, 520, 260, .9), _ov(1480, 230, 360, 160, .75), _ov(960, 900, 900, 200, .7)], src=(SCREEN, '#FBF8F0'))

# ---------- 8. Clean top-down desk (warm wood, lamp pool top-left, empty centre for documents)
def draw_desk_clean(c):
    c.drawRect(skia.Rect(0, 0, W, H), fp('#8A5E3C'))
    rnd = random.Random(7)
    for i in range(0, H, 14):
        y = i + rnd.uniform(-2, 2); c.drawLine(0, y, W, y + rnd.uniform(-6, 6), ink(rnd.choice((2, 3, 4)), rnd.choice(('#7A5234', '#9A6C48', '#835838')), 160))
    for k in range(6):
        cx, cy = rnd.uniform(200, W - 200), rnd.uniform(150, H - 150); c.drawOval(skia.Rect(cx - 90, cy - 18, cx + 90, cy + 18), ink(3, '#6A462C', 130))
    c.drawCircle(170, 930, 64, ink(9, '#5A3A24', 150)); c.drawCircle(170, 930, 52, ink(3, '#5A3A24', 100))
    rect(c, 1560, 930, 1800, 952, '#FCA311', 4, r=10); poly(c, [(1800, 930), (1836, 941), (1800, 952)], '#F4EFE2', 3)
def desk_clean_night():
    return dict(pools=[(820, 460, 900, .75, 1.15), (1680, 940, 260, .8, 1.0)], glows=(), spot_gold=(), keep=('#FCA311',), src_cols=())
