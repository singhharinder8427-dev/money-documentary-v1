"""Night sets for The Nvidia Files, Part 1 chapter 1 (n011-n025). Same recipe as night_scenes.py: draw the room FLAT in navy/gold/cream,
call NS.night() for the light map, NS.frame_out() to finish. sets.py turns each into the locked night print look.
NO green, orange only for losses. Real company names appear only as typographic signs added in the shot (engine/props.py).
Functions look up NS.person / NS.night / NS.add_light / NS.frame_out / NS.txt at CALL time, because sets.py patches them."""
import math, random
from engine.sets_src import night_scenes as NS
from engine.sets_src.night_scenes import (rect, line, poly, circ, oval, shape, fp, ink, sp, linear, radial, hx, C, skia, W, H,
                                          cone_path, city, clock, coin, NAVY, NAVY2, GOLD_, ORNG, WHITE, GREY, MRK, KAL)
from engine.sets_src.night_scenes import INVESTOR   # placeholder spec for seated people (the real actor is drawn by the shot)

FLOOR, WOOD, WOOD_D = '#3A3328', '#7A5A3C', '#5A3E2A'


def _pool(x, y, r, a=.9): return ('pool', x, y, r, a)


def _win(c, x0, y0, x1, y1, seed, bars=(0.5,)):
    city(c, x0, y0, x1, y1, seed=seed)
    for b in bars: line(c, x0 + (x1 - x0) * b, y0, x0 + (x1 - x0) * b, y1, 7)
    line(c, x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, 7); rect(c, x0, y0, x1, y1, None, 8)


# ============ 1. SINGAPORE STREET AT NIGHT (shophouse row, blank sign frame for MEGASPEED / the old sign)
def sg_street():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    city(c, 0, 0, W, 600, seed=21)
    for x in (740, 900, 1060):   # three leaning towers + a sky deck (generic bay-front silhouette)
        poly(c, [(x, 150), (x + 62, 150), (x + 92, 610), (x - 30, 610)], '#1B2C57', 5)
        for k in range(8): c.drawLine(x + 6 + k * 3, 170, x + 24 + k * 10, 600, ink(2, (10, 14, 30), 150))
    rect(c, 690, 118, 1190, 156, '#1B2C57', 5, r=20)
    rect(c, 1130, 110, 1230, 126, '#24365E', 3, r=8)
    rect(c, -10, 760, W + 10, H + 10, FLOOR, 0); [line(c, -10, y, W + 10, y, 3, (48, 40, 30)) for y in range(800, H, 46)]
    rect(c, -10, 740, W + 10, 790, '#4A3626', 4)
    for x in range(0, W, 220): c.drawRect(skia.Rect(x + 40, 930, x + 150, 944), fp('#E8D9B0', 210))   # road dashes
    # shophouse row: three storeys, arched shuttered windows, five-foot-way arcade
    houses = [(-20, 520, '#2E4470'), (520, 700, '#34497A'), (1220, 720, '#4A3626')]
    for (x0, w, col) in houses:
        x1 = x0 + w; rect(c, x0, 250, x1, 760, col, 6)
        rect(c, x0, 250, x1, 286, '#1E3157', 5)
        for wx in range(int(x0 + 50), int(x1 - 80), 130):
            for wy in (320, 470):
                p = skia.Path(); p.moveTo(wx, wy + 100); p.lineTo(wx, wy + 30); p.arcTo(skia.Rect(wx, wy - 20, wx + 80, wy + 80), 180, 180, False); p.lineTo(wx + 80, wy + 100); p.close()
                shape(c, p, '#FFD27A' if (wx + wy) % 3 else '#1B2A52', 5)
                for sx in (wx + 20, wx + 40, wx + 60): c.drawLine(sx, wy + 8, sx, wy + 100, ink(2.5, (24, 22, 27), 180))
        for ax in range(int(x0 + 30), int(x1 - 60), 170):
            rect(c, ax, 640, ax + 120, 760, '#0F1A38' if ax % 3 else '#2B1E14', 5, r=6)
    # centre shophouse: BLANK sign frame (the shot draws OLD sign / MEGASPEED here) and a glass door
    rect(c, 700, 322, 1220, 438, '#0F1A38', 8, r=10); rect(c, 712, 334, 1208, 426, None, 3, r=6, v='#4A62A0')
    rect(c, 880, 560, 1040, 760, '#FFD27A', 7, r=6); line(c, 960, 560, 960, 760, 5); circ(c, 944, 670, 6, '#2E2E38', 3); circ(c, 976, 670, 6, '#2E2E38', 3)
    rect(c, 860, 540, 1060, 566, '#1E3157', 5)
    for lx in (330, 1610):   # street lamps
        line(c, lx, 330, lx, 800, 9); poly(c, [(lx - 36, 330), (lx + 36, 330), (lx + 22, 304), (lx - 22, 304)], GOLD_, 5)
    for lx in (500, 1420): circ(c, lx, 560, 22, ORNG if False else '#FFD27A', 4); line(c, lx, 500, lx, 538, 4)   # lanterns
    NS.night(c, [_pool(330, 360, 330), _pool(1610, 360, 330), ('oval', 960, 380, 380, 140, .9), ('oval', 960, 700, 300, 160, .8),
                 ('oval', 960, 880, 700, 90, .35)], ambient='#4C5CA0')
    NS.add_light(c, 330, 320, 150, '#FFE2A0', 200); NS.add_light(c, 1610, 320, 150, '#FFE2A0', 200); NS.add_light(c, 960, 380, 260, '#FFD27A', 90)
    NS.frame_out(surf, 'ng_sg_street.png')


# ============ 2. MEGASPEED OFFICE (open-plan, glass server room, blank wall panel for the wordmark)
def megaspeed_office():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    for i, x in enumerate(range(0, W, 80)): c.drawRect(skia.Rect(x, 0, x + 80, 700), fp('#2A3D68' if i % 2 else '#263862'))
    rect(c, -10, 700, W + 10, H + 10, '#34304A', 0); [line(c, -10, y, W + 10, y, 3, (30, 28, 44)) for y in range(760, H, 56)]
    _win(c, 90, 120, 620, 520, seed=33, bars=(0.33, 0.66))
    rect(c, 700, 150, 1220, 330, '#0F1A38', 8, r=8)   # blank wall panel (shot draws MEGASPEED here)
    # glass server room on the right: racks glowing gold
    rect(c, 1330, 150, 1850, 720, '#16244A', 8)
    for k, x in enumerate(range(1370, 1830, 100)):
        rect(c, x, 190, x + 80, 700, '#2B2F3C', 5, r=6)
        for yy in range(210, 690, 46):
            rect(c, x + 8, yy, x + 72, yy + 34, '#3A3F4F', 2, r=3)
            for j in range(4): c.drawCircle(x + 20 + j * 14, yy + 17, 4, fp(GOLD_ if (yy // 46 + j + k) % 3 else '#5A6076'))
    c.drawRect(skia.Rect(1330, 150, 1850, 720), fp((255, 255, 255), 18)); rect(c, 1330, 150, 1850, 720, None, 8)
    for x in (1590,): line(c, x, 150, x, 720, 6)
    # desks + monitors in two rows
    for (dx, dy, sc) in ((250, 850, 1.0), (650, 850, 1.0), (1050, 850, 1.0), (200, 980, 1.2), (780, 980, 1.2)):
        s = sc; rect(c, dx - 150 * s, dy, dx + 150 * s, dy + 22 * s, WOOD, 5)
        rect(c, dx - 120 * s, dy - 120 * s, dx + 10 * s, dy - 14 * s, '#2E2E38', 5, r=6); rect(c, dx - 110 * s, dy - 110 * s, dx, dy - 24 * s, '#0A1330', 3)
        g = skia.Path(); g.moveTo(dx - 100 * s, dy - 44 * s)
        for j in range(1, 6): g.lineTo(dx - 100 * s + j * 18 * s, dy - 44 * s - (j * 9 + (8 if j % 2 else 0)) * s)
        c.drawPath(g, ink(5, GOLD_)); line(c, dx - 55 * s, dy - 14 * s, dx - 55 * s, dy, 6)
        rect(c, dx + 50 * s, dy - 18 * s, dx + 100 * s, dy, '#FBF8F0', 3, r=3)
    NS.night(c, [('oval', 360, 330, 340, 260, .85), ('oval', 1590, 420, 360, 340, .9), ('oval', 960, 240, 300, 120, .7),
                 ('oval', 700, 850, 700, 160, .7)], ambient='#4C5CA0')
    NS.add_light(c, 1590, 420, 300, '#FFB93C', 110); NS.add_light(c, 360, 320, 220, '#7FA6FF', 70)
    NS.frame_out(surf, 'ng_megaspeed_office.png')


# ============ 3. 1993 ROADSIDE DINER (booth at the window, counter + stools behind, neon, wall calendar frame)
def diner93():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    c.drawRect(skia.Rect(0, 0, W, 700), fp('#2E4470'))
    for x in range(0, W, 120): c.drawRect(skia.Rect(x, 0, x + 60, 700), fp('#34497A'))   # panelled wall stripes
    rect(c, -10, 700, W + 10, H + 10, '#2B2B36', 0)
    for y in range(700, H, 70):   # checker floor
        for x in range(((y // 70) % 2) * 70, W, 140): c.drawRect(skia.Rect(x, y, x + 70, y + 70), fp('#3A3F4F'))
    # big window: night highway with headlights, neon sign reflected
    city(c, 1120, 130, 1800, 520, seed=47); rect(c, 1120, 130, 1800, 520, None, 8); line(c, 1460, 130, 1460, 520, 8); line(c, 1120, 330, 1800, 330, 8)
    for hx_ in (1180, 1300, 1700): c.drawCircle(hx_, 470, 9, fp('#FFE2A0', 230))
    c.drawRect(skia.Rect(1120, 470, 1800, 520), fp('#14213D'))
    # neon DINER sign on the wall, wall calendar frame, clock, pie case
    rect(c, 160, 110, 560, 230, '#0F1A38', 7, r=14); NS.txt(c, 'DINER', 360, 205, 96, GOLD_, MRK, 'center', skew=0)
    rect(c, 640, 120, 860, 400, '#FBF8F0', 5); rect(c, 640, 120, 860, 180, NAVY2, 5)   # calendar page frame (shot flips the year)
    clock(c, 960, 210, 60, 11.3)
    rect(c, 60, 430, 520, 560, '#E5E5E5', 6, r=8); rect(c, 74, 444, 506, 520, '#C9C3B8', 3)
    for k in range(3): circ(c, 140 + k * 140, 482, 34, '#E8C77A', 4); circ(c, 140 + k * 140, 482, 16, '#B07A0A', 2)
    # counter + stools behind the booth
    rect(c, 80, 580, 900, 640, '#7A5A3C', 6); rect(c, 80, 640, 900, 760, '#4A3626', 5)
    for x in (200, 360, 520, 680, 820):
        line(c, x, 640, x, 770, 8); oval(c, x - 40, 600, x + 40, 650, '#5C1F2A', 5)
    # booth seats behind the two diners (benches), TABLE drawn in front after the people
    rect(c, 600, 540, 1020, 960, '#5C1F2A', 6, r=26)     # back bench
    rect(c, 1060, 540, 1480, 960, '#5C1F2A', 6, r=26)
    NS.person(c, 800, 1010, 1.1, INVESTOR, face=0.3)       # placeholder seats (the shot draws the real actors here)
    NS.person(c, 1280, 1010, 1.1, INVESTOR, face=-0.3)
    rect(c, 560, 850, 1540, 920, WOOD, 6, r=10); rect(c, 1010, 920, 1090, 1100, WOOD_D, 5)
    for (mx, my) in ((780, 820), (1300, 822)): rect(c, mx - 24, my, mx + 24, 856, WHITE, 5, r=6)   # two mugs
    rect(c, 1010, 806, 1070, 850, '#E8D9B0', 4, r=5)
    NS.night(c, [('oval', 360, 160, 260, 120, .95), ('oval', 960, 700, 800, 380, .75), ('oval', 1460, 330, 380, 230, .8), ('oval', 1040, 840, 500, 120, .8)], ambient='#4C5CA0')
    NS.add_light(c, 360, 170, 220, '#FFB93C', 130); NS.add_light(c, 1040, 820, 220, '#FFE2A0', 80)
    NS.frame_out(surf, 'ng_diner93.png')


# ============ 4. SINGAPORE ITALIAN RESTAURANT (Dec 2023): candle table in front, arched windows, wine shelf
def restaurant():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    c.drawRect(skia.Rect(0, 0, W, 720), fp('#3A2A22'))
    for x in range(0, W, 60): c.drawRect(skia.Rect(x, 0, x + 30, 720), fp('#432F26'))
    rect(c, -10, 720, W + 10, H + 10, '#2A1E14', 0); [line(c, -10, y, W + 10, y, 3, (40, 28, 20)) for y in range(760, H, 60)]
    for (x0, x1) in ((140, 560), (1360, 1780)):   # arched windows over a night skyline
        p = skia.Path(); p.moveTo(x0, 520); p.lineTo(x0, 260); p.arcTo(skia.Rect(x0, 120, x1, 400), 180, 180, False); p.lineTo(x1, 520); p.close()
        c.save(); c.clipPath(p, doAntiAlias=True); city(c, x0, 120, x1, 520, seed=60 + x0 // 100); c.restore(); shape(c, p, None, 9); line(c, (x0 + x1) / 2, 120, (x0 + x1) / 2, 520, 6)
    rect(c, 640, 190, 1280, 500, '#2A1E14', 7, r=6)   # wine shelf
    for sy in (260, 340, 420): line(c, 650, sy + 40, 1270, sy + 40, 7)
    for sy in (260, 340, 420):
        for bx in range(676, 1250, 52):
            rect(c, bx, sy - 18, bx + 24, sy + 40, '#14213D', 3, r=7); rect(c, bx + 7, sy - 38, bx + 17, sy - 16, '#14213D', 3, r=3); c.drawRect(skia.Rect(bx + 3, sy + 8, bx + 21, sy + 26), fp('#E8D9B0'))
    for lx in (420, 960, 1500):   # pendant lamps
        line(c, lx, 0, lx, 110, 4); poly(c, [(lx - 62, 150), (lx + 62, 150), (lx + 34, 108), (lx - 34, 108)], GOLD_, 5)
    # back tables with tiny candles
    for (tx, ty) in ((260, 660), (1660, 660)):
        oval(c, tx - 120, ty, tx + 120, ty + 40, '#E5E5E5', 5); line(c, tx, ty + 40, tx, ty + 200, 8); rect(c, tx - 10, ty - 22, tx + 10, ty, '#FBF8F0', 3, r=3)
    NS.person(c, 760, 1060, 1.18, INVESTOR, face=0.3)      # placeholders: seated guests (the shot draws the real actors)
    NS.person(c, 1160, 1060, 1.18, INVESTOR, face=-0.3)
    # front table with cloth, candle, glasses, plates
    poly(c, [(520, 830), (1400, 830), (1490, 1090), (430, 1090)], '#F4EFE2', 7)
    for xx in (620, 800, 960, 1120, 1300): c.drawLine(xx, 840, xx - (960 - xx) * .12, 1086, ink(2.5, (200, 194, 180), 200))
    rect(c, 940, 760, 980, 840, '#FBF8F0', 4, r=4)
    for (gx, gy) in ((780, 820), (1130, 822)):
        c.drawPath((lambda p: (p.moveTo(gx - 20, gy - 70), p.lineTo(gx + 20, gy - 70), p.quadTo(gx + 20, gy - 20, gx, gy - 12), p.quadTo(gx - 20, gy - 20, gx - 20, gy - 70), p)[-1])(skia.Path()), fp((225, 240, 255), 70)); c.drawLine(gx, gy - 12, gx, gy + 10, ink(5)); c.drawLine(gx - 16, gy + 10, gx + 16, gy + 10, ink(5))
        oval(c, gx - 30, gy + 14, gx + 30, gy + 34, '#FBF8F0', 4)
    c.drawPath((lambda p: (p.moveTo(960, 740), p.cubicTo(950, 710, 970, 700, 960, 672), p.cubicTo(985, 700, 985, 722, 960, 740), p)[-1])(skia.Path()), fp(GOLD_))
    NS.night(c, [('oval', 960, 860, 520, 200, .95), _pool(420, 170, 240, .7), _pool(960, 170, 240, .7), _pool(1500, 170, 240, .7), ('oval', 960, 330, 340, 160, .6),
                 ('oval', 350, 330, 260, 200, .6), ('oval', 1570, 330, 260, 200, .6)], ambient='#4C5CA0')
    NS.add_light(c, 960, 710, 180, '#FFB93C', 180); NS.add_light(c, 420, 140, 150, '#FFE2A0', 170); NS.add_light(c, 960, 140, 150, '#FFE2A0', 170); NS.add_light(c, 1500, 140, 150, '#FFE2A0', 170)
    NS.frame_out(surf, 'ng_restaurant.png')


# ============ 5. MALAYSIAN DATA-CENTER AISLE (one-point perspective, racks both sides, sealed crates on the floor)
def datacenter():
    surf = skia.Surface(W, H); c = surf.getCanvas(); VX, VY = 960, 440
    c.drawRect(skia.Rect(0, 0, W, H), fp('#1B2A52'))
    ceil = skia.Path(); ceil.moveTo(0, 0); ceil.lineTo(W, 0); ceil.lineTo(VX + 120, VY - 70); ceil.lineTo(VX - 120, VY - 70); ceil.close(); shape(c, ceil, '#24365E', 5)
    flr = skia.Path(); flr.moveTo(0, H); flr.lineTo(W, H); flr.lineTo(VX + 120, VY + 60); flr.lineTo(VX - 120, VY + 60); flr.close(); shape(c, flr, '#34304A', 5)
    for k in range(-5, 6): line(c, VX + k * 22, VY + 60, VX + k * 230, H, 3, (24, 22, 40), 160)
    rect(c, VX - 120, VY - 70, VX + 120, VY + 60, '#0F1A38', 6)   # far end wall
    X = lambda side, z: VX + side * 1100 / z; T = lambda z: VY - 520 / z; B = lambda z: VY + 470 / z
    zs = [1.0, 1.28, 1.64, 2.1, 2.7, 3.45, 4.4, 5.6]
    for side in (-1, 1):
        for i in range(len(zs) - 1):
            za, zb = zs[i], zs[i + 1]
            if i % 4 != 3:    # rack faces
                p = skia.Path(); p.moveTo(X(side, za), T(za)); p.lineTo(X(side, zb), T(zb)); p.lineTo(X(side, zb), B(zb)); p.lineTo(X(side, za), B(za)); p.close()
                shape(c, p, '#2B2F3C', 6)
                for k in range(1, 9):
                    ya, yb = T(za) + (B(za) - T(za)) * k / 9, T(zb) + (B(zb) - T(zb)) * k / 9
                    line(c, X(side, za), ya, X(side, zb), yb, 3, (20, 22, 34))
                    for j in range(4):
                        tt = (j + .5) / 4; lx = X(side, za) + (X(side, zb) - X(side, za)) * tt; ly = ya + (yb - ya) * tt + (B(zb) - T(zb)) / 22
                        c.drawCircle(lx, ly, max(2.2, 5.5 / ((za + zb) / 2)), fp(GOLD_ if (i + j + k) % 3 else '#5A6076'))
            else:             # cross-aisle gap
                p = skia.Path(); p.moveTo(X(side, za), T(za)); p.lineTo(X(side, zb), T(zb)); p.lineTo(X(side, zb), B(zb)); p.lineTo(X(side, za), B(za)); p.close(); shape(c, p, '#0F1A38', 5)
    for z in (1.3, 2.3, 3.6, 5.2):   # ceiling light strips
        y0 = VY - 520 / z - 4; c.drawRect(skia.Rect(VX - 300 / z, y0 - 22 / z, VX + 300 / z, y0), fp('#FFE2A0'))
    # sealed crates on the floor (generic stencil; shot can add gold glow with props.crate)
    def box(cx, base, w, h, tilt=0.0):
        d = w * .28; rect(c, cx - w / 2, base - h, cx + w / 2, base, '#8A6540', 6, r=3)
        top = skia.Path(); top.moveTo(cx - w / 2, base - h); top.lineTo(cx - w / 2 + d, base - h - d * .7); top.lineTo(cx + w / 2 + d, base - h - d * .7); top.lineTo(cx + w / 2, base - h); top.close(); shape(c, top, '#6B4A2E', 5)
        sd = skia.Path(); sd.moveTo(cx + w / 2, base - h); sd.lineTo(cx + w / 2 + d, base - h - d * .7); sd.lineTo(cx + w / 2 + d, base - d * .7); sd.lineTo(cx + w / 2, base); sd.close(); shape(c, sd, '#4F3520', 5)
        c.drawRect(skia.Rect(cx - 6, base - h, cx + 6, base), fp('#E8D9B0', 235)); c.drawRect(skia.Rect(cx - w / 2, base - h * .5 - 8, cx + w / 2, base - h * .5 + 8), fp('#E8D9B0', 235))
        NS.txt(c, 'SERVERS', cx, base - h * .74, max(14, w * .13), '#E8D9B0', MRK, 'center', skew=0, stroke=3)
    box(520, 960, 260, 200); box(760, 880, 170, 140); box(1360, 940, 250, 190); box(1580, 1010, 300, 230); box(1160, 800, 110, 90)
    NS.night(c, [('oval', 960, 520, 640, 380, .6), ('oval', 960, 160, 540, 90, .85), ('oval', 960, 900, 800, 160, .45)], ambient='#4C5CA0')
    NS.add_light(c, 960, 140, 240, '#FFE2A0', 120); NS.add_light(c, 960, 470, 200, '#7FA6FF', 70)
    NS.frame_out(surf, 'ng_datacenter.png')
