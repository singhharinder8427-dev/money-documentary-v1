"""Scene drawings for the night sets (run night_look.py, not this file, for the locked look). Originally five busy environments drawn with the aivxer long-form skill's kit (skia): dense props, navy night() lighting,
light pools, glows, grade + bloom, vignette. Characters use our navy + gold brand colours. Losses in orange."""
import os, math, random
import kit
from engine.core import FONT_DIR as _FD; kit.FD = _FD
from kit import *
def _shape(c, path, fill, w=LW, v=INK):   # allow fill=None for outline-only shapes
    if fill is not None: c.drawPath(path, fill if isinstance(fill, skia.Paint) else fp(fill))
    if w: c.drawPath(path, ink(w, v))
kit.shape = _shape; shape = _shape
HAND = skia.Typeface.MakeFromFile(kit.FD + 'CaveatBrush-Regular.ttf')
KAL = skia.Typeface.MakeFromFile(kit.FD + 'Kalam-Bold.ttf')
MRK = skia.Typeface.MakeFromFile(kit.FD + 'PermanentMarker-Regular.ttf')
NAVY, NAVY2, GOLD_, ORNG, WHITE, GREY = '#14213D', '#1E3157', '#FCA311', '#F35B04', '#FFFFFF', '#E5E5E5'

# ---- our cast (navy + gold)
CEO = dict(skin='#EBC9A0', skin_d='#CDA77B', suit=NAVY, suit_d='#0C152B', shirt=WHITE, tie=GOLD_, hair='bald', hair_col='#C9C9CF', glasses=True, moustache=True)
ANALYST = dict(skin='#C8875A', skin_d='#A86C43', suit=GREY, suit_d='#BDBDBD', shirt=WHITE, tie=NAVY, hair='slick', hair_col='#1A1414', glasses=True)
WORKER = dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#6B4A2E', suit_d='#4F3520', shirt='#F4EFE2', tie='#2B4A7A', hair='slick', hair_col='#7A4A26', hat_col='#3A3F4A', hat_band=GOLD_)
BANKER = dict(skin='#E2B48C', skin_d='#C49468', suit='#2E2E38', suit_d='#1E1E26', shirt=WHITE, tie=GOLD_, bowtie=True, hair='slick', hair_col='#3A2A20', moustache=True, hanky=GOLD_)
INVESTOR = dict(skin='#8D5A3B', skin_d='#6F4429', suit=GOLD_, suit_d='#D88A06', shirt=WHITE, tie=NAVY, hair=None)

def bob(c, x, y, s, col='#15110F', front=False):
    cx, cy = x, y + s * HEAD_CY
    if not front:
        p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 118*s, cy - 104*s, cx + 118*s, cy + 92*s), 70*s, 70*s)); shape(c, p, col, 5.5)
def person(c, x, y, s, spec, **kw):
    if spec is INVESTOR: bob(c, x, y, s)
    draw_char(c, x, y, s, spec, light=kw.pop('light', -1), rim=kw.pop('rim', '#9FB8F0'), **kw)

def txt(c, s, x, y, size, color, font=None, align='left', stroke=0, rot=0.0, skew=-0.12, sc=INK):
    return label(c, s, x, y, size, color, font=font or KAL, align=align, stroke=stroke, stroke_col=sc, skew=skew, rot=rot)
def paper(c, x, y, w, h, rot, fill='#FBF8F0', lines=6, title=None, tcol=NAVY):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRect(skia.Rect(-w/2 + 10, -h/2 + 14, w/2 + 10, h/2 + 14), fp((0, 0, 0), 70, blur=10))
    rect(c, -w/2, -h/2, w/2, h/2, fill, 4)
    y0 = -h/2 + (60 if title else 26)
    if title: txt(c, title, -w/2 + 18, -h/2 + 44, 30, tcol, KAL, skew=0)
    for i in range(lines): c.drawRect(skia.Rect(-w/2 + 18, y0 + i * 22, -w/2 + 18 + (w - 36) * (0.55 + 0.45 * ((i * 37) % 10) / 10), y0 + i * 22 + 7), fp('#C9C3B5'))
    c.restore()
def bill(c, x, y, rot, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(c, -80, -36, 80, 36, '#F4F1E8', 4); rect(c, -70, -27, 70, 27, None if False else '#F4F1E8', 2.5, v=NAVY)
    circ(c, 0, 0, 20, GOLD_, 2.5); txt(c, '$', 0, 11, 30, NAVY, MRK, 'center', skew=0)
    txt(c, '100', -64, -10, 16, NAVY, KAL, skew=0); c.restore()
def coin(c, x, y, r=22):
    circ(c, x, y, r, GOLD_, 3.5); circ(c, x, y, r * .72, None if False else GOLD_, 2, v='#B07A0A'); txt(c, '$', x, y + r * .38, r * 1.05, '#9A6A08', MRK, 'center', skew=0)
def lamp(c, x, y, t=0):  # banker lamp: base, stem, green->gold shade
    rect(c, x - 34, y - 10, x + 34, y + 4, '#3A3328', 4, r=4); line(c, x, y - 10, x, y - 92, 6)
    poly(c, [(x - 78, y - 92), (x + 78, y - 92), (x + 58, y - 132), (x - 58, y - 132)], GOLD_, 5)
def clock(c, x, y, r, h=10.1):
    circ(c, x, y, r, '#FBF8F0', 5); [line(c, x + math.sin(a) * r * .8, y - math.cos(a) * r * .8, x + math.sin(a) * r * .92, y - math.cos(a) * r * .92, 4) for a in [i * math.pi / 6 for i in range(12)]]
    line(c, x, y, x + math.sin(h / 12 * 2 * math.pi) * r * .5, y - math.cos(h / 12 * 2 * math.pi) * r * .5, 6); line(c, x, y, x + math.sin(h % 1 * 2 * math.pi) * r * .75, y - math.cos(h % 1 * 2 * math.pi) * r * .75, 4)
def city(c, x0, y0, x1, y1, seed=3, base='#16244A'):
    rnd = random.Random(seed); c.save(); c.clipRect(skia.Rect(x0, y0, x1, y1))
    c.drawRect(skia.Rect(x0, y0, x1, y1), sp(linear(0, y0, 0, y1, [hx('#0A1330'), hx('#253A72')])))
    for _ in range(40): c.drawCircle(rnd.uniform(x0, x1), rnd.uniform(y0, y0 + (y1 - y0) * .4), 1.6, fp('#DCE6FF', 180))
    x = x0 - 20
    while x < x1:
        w = rnd.randint(40, 110); h = rnd.randint(int((y1 - y0) * .25), int((y1 - y0) * .8))
        c.drawRect(skia.Rect(x, y1 - h, x + w, y1), fp(base)); c.drawRect(skia.Rect(x, y1 - h, x + w, y1), ink(2, (10, 14, 30)))
        for wy in range(int(y1 - h + 10), int(y1), 16):
            for wx in range(int(x + 6), int(x + w - 8), 13):
                if rnd.random() < .35: c.drawRect(skia.Rect(wx, wy, wx + 6, wy + 8), fp('#FFD27A', 220))
        x += w + rnd.randint(2, 12)
    c.restore()
def frame_out(surf, path):
    finish(surf); vignette(surf.getCanvas(), 0.62); surf.makeImageSnapshot().save(path, skia.kPNG)

# ============ 1. CEO OFFICE AT NIGHT (the skill's office set, our colours)
def office():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    for i, x in enumerate(range(0, W, 70)): c.drawRect(skia.Rect(x, 0, x + 70, 690), fp('#2A3D68' if i % 2 else '#24365E'))
    rect(c, -10, 690, W + 10, 800, '#3B2A1E'); [line(c, x, 700, x, 790, 4, (30, 20, 14)) for x in range(40, W, 160)]
    rect(c, -10, 800, W + 10, H + 10, '#4A3626'); [line(c, -10, y, W + 10, y, 3, (40, 28, 20), 200) for y in range(840, H, 60)]
    # big window with night skyline + reflections, curtains
    city(c, 1060, 110, 1700, 560, seed=7); [line(c, x, 110, x, 560, 8) for x in (1060, 1380, 1700)]; line(c, 1060, 335, 1700, 335, 8); rect(c, 1060, 110, 1700, 560, None, 8)
    for x0, x1 in ((1060, 1240), (1380, 1520)): poly(c, [(x0 + 30, 120), (x0 + 80, 120), (x1 - 40, 550), (x1 - 90, 550)], (255, 255, 255), 0) if False else c.drawPath((lambda p: (p.moveTo(x0 + 30, 120), p.lineTo(x0 + 70, 120), p.lineTo(x1 - 40, 550), p.lineTo(x1 - 80, 550), p.close(), p)[-1])(skia.Path()), fp((255, 255, 255), 22))
    for cx, d in ((1010, -1), (1750, 1)):
        cp = skia.Path(); cp.moveTo(cx - 70, 80); cp.lineTo(cx + 70, 80); cp.cubicTo(cx + 70 + d * 10, 400, cx + 40, 600, cx + 60 * d, 690); cp.lineTo(cx - 60 * d, 690); cp.cubicTo(cx - 50, 500, cx - 80, 300, cx - 70, 80); cp.close(); shape(c, cp, '#5C1F2A', 5)
    rect(c, 920, 60, 1840, 84, '#3B2A1E', 5, r=8)
    # wall: clock, calendar, framed chart, bookshelf
    clock(c, 760, 210, 70)
    rect(c, 300, 130, 520, 400, '#FBF8F0', 5); rect(c, 300, 130, 520, 190, ORNG, 5); txt(c, 'NOVEMBER', 410, 175, 36, WHITE, KAL, 'center', skew=0)
    for i in range(20): rect(c, 318 + (i % 5) * 40, 205 + (i // 5) * 46, 352 + (i % 5) * 40, 240 + (i // 5) * 46, '#EEE8DA', 2)
    circ(c, 455, 315, 26, None if False else '#FBF8F0', 0); c.drawCircle(455, 314, 26, ink(5, ORNG))
    rect(c, 560, 300, 860, 520, '#7A5A3C', 6); rect(c, 580, 320, 840, 500, '#FBF8F0', 4)
    pl = skia.Path(); pl.moveTo(600, 480); [pl.lineTo(600 + i * 34, 480 - (i * 22 + (12 if i % 2 else 0))) for i in range(1, 7)]; c.drawPath(pl, ink(7, NAVY)); txt(c, 'Q3', 610, 350, 30, NAVY, KAL, skew=0)
    rect(c, 40, 180, 250, 690, '#5A3E2A', 6)
    for sh in range(4):
        y = 230 + sh * 115; line(c, 40, y + 90, 250, y + 90, 6)
        for b in range(7): rect(c, 55 + b * 26, y + 20 + (b % 3) * 6, 77 + b * 26, y + 88, ['#14213D', '#FCA311', '#7A1328', '#2B4A7A', '#E5E5E5'][(b + sh) % 5], 3)
    # plant
    rect(c, 1840, 600, 1910, 700, '#3B2A1E', 5, r=8)
    for a in range(9): oval(c, 1875 + math.cos(a) * 40 - 26, 560 - a * 12 - 14 + math.sin(a * 2) * 10, 1875 + math.cos(a) * 40 + 26, 560 - a * 12 + 14 + math.sin(a * 2) * 10, '#2F5A3A' if a % 2 else '#3C6E48', 4)
    # rug, desk with drawers, items
    oval(c, 360, 900, 1500, 1060, '#5C1F2A', 6); oval(c, 420, 920, 1440, 1040, None if False else '#5C1F2A', 3, v='#C9A060')
    person(c, 930, 950, 1.08, CEO, face=-0.15, eyes='half', mouth='smirk', arms=('hold', 'gesture'), brow=-0.1)
    rect(c, 470, 640, 1390, 690, '#6B4A33', 6, r=6); rect(c, 500, 690, 760, 930, '#5A3E2A', 6); rect(c, 1100, 690, 1360, 930, '#5A3E2A', 6)
    for y in (720, 790, 860): rect(c, 520, y, 740, y + 56, '#6B4A33', 4, r=4); circ(c, 630, y + 28, 7, GOLD_, 3); rect(c, 1120, y, 1340, y + 56, '#6B4A33', 4, r=4); circ(c, 1230, y + 28, 7, GOLD_, 3)
    lamp(c, 560, 640); paper(c, 700, 622, 150, 46, -6, lines=2); paper(c, 1150, 624, 140, 44, 5, lines=2)
    for i in range(4): bill(c, 1230 + i * 6, 616 - i * 9, -0.05, 0.7)
    rect(c, 1300, 590, 1370, 640, '#1E1F2A', 4, r=8); circ(c, 1335, 584, 14, '#1E1F2A', 4)  # phone
    night(c, [('oval', 560, 520, 380, 300, .95), ('oval', 930, 640, 360, 420, .85), ('path', (lambda p: (p.addRect(skia.Rect(1060, 110, 1700, 560)), p)[-1])(skia.Path()), .8, 30),
              ('oval', 1380, 760, 420, 120, .35), ('oval', 760, 220, 140, 140, .4), ('oval', 410, 260, 170, 200, .45)])
    c.drawPath(cone_path(560, 510, 150, 520, 380), fp(GOLD_, 26, blur=30, blend=skia.BlendMode.kPlus)); add_light(c, 560, 505, 110, '#FFE2A0', 150)
    frame_out(surf, 'env1_office.png')

# ============ 2. TRADING FLOOR (screens, ticker board, crowd, falling papers)
def trading():
    surf = skia.Surface(W, H); c = surf.getCanvas(); rnd = random.Random(5)
    c.drawRect(skia.Rect(0, 0, W, H), fp('#101A33'))
    rect(c, 60, 50, 1860, 330, '#0A0F1E', 8, r=10)    # giant ticker board
    ticks = [('ACME', -4.2), ('BOLT', -6.8), ('OPAL', 1.3), ('PIKE', -3.1), ('QUAY', -9.4), ('KITE', -2.2), ('LUME', 0.6), ('NOVA', -5.5), ('RAVN', -7.1), ('SOLA', -1.4)]
    for i, (n, ch) in enumerate(ticks):
        x = 110 + (i % 5) * 350; y = 120 + (i // 5) * 120
        txt(c, n, x, y, 40, WHITE, MRK, skew=0); txt(c, f'{ch:+.1f}%', x + 150, y, 38, ORNG if ch < 0 else GOLD_, MRK, skew=0)
        poly(c, [(x + 295, y - 34), (x + 315, y - 4), (x + 275, y - 4)] if ch >= 0 else [(x + 295, y - 4), (x + 315, y - 34), (x + 275, y - 34)], ORNG if ch < 0 else GOLD_, 2)
    rect(c, 60, 330, 1860, 380, '#1E1F2A', 6); txt(c, 'MARKETS  ·  LIVE', 960, 368, 34, GOLD_, KAL, 'center', skew=0)
    # back rows of desks with monitors (small), then front row (big)
    for row, (y, s, n) in enumerate([(560, .55, 9), (700, .75, 7)]):
        for i in range(n):
            x = 120 + i * (1680 / (n - 1))
            person(c, x + rnd.uniform(-20, 20), y + 70 * s, s, rnd.choice([ANALYST, WORKER, BANKER, INVESTOR, CEO]), face=rnd.uniform(-.5, .5),
                   eyes=rnd.choice(['wide', 'dot']), mouth=rnd.choice(['o', 'open', 'flat']), arms=rnd.choice([('hat', 'down'), ('gesture', 'down'), ('chin', 'hip')]), sweat=rnd.choice([-1, .3]), rim=None)
            rect(c, x - 150 * s, y - 20 * s, x + 150 * s, y + 30 * s, '#2A3A5E', 5)
            for k in (-1, 1):
                mx = x + k * 80 * s; rect(c, mx - 62 * s, y - 120 * s, mx + 62 * s, y - 30 * s, '#05080F', 4)
                g = skia.Path(); g.moveTo(mx - 52 * s, y - 100 * s)
                for j in range(1, 8): g.lineTo(mx - 52 * s + j * 15 * s, y - 100 * s + (j * 7 + (j % 2) * 8) * s)
                c.drawPath(g, ink(4 * s, ORNG))
    # front: a shocked trader with phone, papers flying
    person(c, 760, 1180, 1.35, ANALYST, face=0.3, eyes='wide', mouth='open', brow=0.9, arms=('hat', 'push'), sweat=0.5)
    person(c, 1260, 1150, 1.25, INVESTOR, face=-0.35, eyes='wide', mouth='o', brow=0.7, arms=('chin', 'gesture'))
    for i in range(22): paper(c, rnd.uniform(80, 1840), rnd.uniform(380, 1000), 110, 76, rnd.uniform(-40, 40), lines=3)
    night(c, [('path', (lambda p: (p.addRect(skia.Rect(60, 50, 1860, 380)), p)[-1])(skia.Path()), .9, 40), ('oval', 960, 700, 1100, 260, .55), ('oval', 760, 760, 300, 360, .7), ('oval', 1260, 760, 300, 360, .7)], ambient='#3E4C8A')
    for i in range(5): add_light(c, 200 + i * 380, 200, 260, ORNG, 26)
    frame_out(surf, 'env2_trading.png')

# ============ 3. TOP-DOWN INVESTIGATION DESK (documents, newspaper, cash, hands)
def sleeve(c, x0, y0, x1, y1, w, col):
    a = math.atan2(y1 - y0, x1 - x0); L = math.hypot(x1 - x0, y1 - y0); c.save(); c.translate(x0, y0); c.rotate(math.degrees(a))
    rect(c, 0, -w / 2, L, w / 2, col, 6, r=10); rect(c, L - 26, -w / 2 - 4, L, w / 2 + 4, WHITE, 5, r=6); circ(c, L + 40, 0, w * .55, '#E8B990', 5)
    for k in (-1, 0, 1): line(c, L + 52, k * 14, L + 82, k * 16, 5)
    c.restore()
def desk():
    surf = skia.Surface(W, H); c = surf.getCanvas(); rnd = random.Random(9)
    c.drawRect(skia.Rect(0, 0, W, H), sp(radial(900, 520, 1300, [hx('#2A3D68'), hx('#14213D')])))
    for _ in range(900): c.drawCircle(rnd.uniform(0, W), rnd.uniform(0, H), 1.3, fp('#3A5080', 120))
    rect(c, 140, 70, 1780, 1010, '#1E3157', 8, r=16); rect(c, 170, 100, 1750, 980, '#24365E', 3, r=12)   # navy felt blotter
    # newspaper with orange marker circle
    c.save(); c.translate(560, 420); c.rotate(-7)
    c.drawRect(skia.Rect(-330, -250, 350, 290), fp((0, 0, 0), 80, blur=14)); rect(c, -340, -260, 340, 280, '#EFEADF', 5)
    txt(c, 'THE DAILY LEDGER', 0, -200, 64, NAVY, MRK, 'center', skew=0); line(c, -320, -180, 320, -180, 4); line(c, -320, -170, 320, -170, 2)
    txt(c, 'MARKET LOSES $2 TRILLION', 0, -112, 50, INK, KAL, 'center', skew=0)
    rect(c, -320, -80, -20, 120, '#C9C3B5', 4)
    pl = skia.Path(); pl.moveTo(-300, -60); [pl.lineTo(-300 + i * 45, -60 + (i * i * 4)) for i in range(1, 7)]; c.drawPath(pl, ink(7, ORNG))
    for i in range(9): c.drawRect(skia.Rect(10, -76 + i * 22, 320 - (i % 3) * 40, -68 + i * 22), fp('#B9B2A3'))
    for i in range(5): c.drawRect(skia.Rect(-320, 150 + i * 22, 320 - (i % 2) * 90, 158 + i * 22), fp('#B9B2A3'))
    m = skia.Path(); m.addOval(skia.Rect(-250, -152, 250, -66)); c.drawPath(m, ink(9, ORNG)); c.restore()
    # 401(k) statement with gold highlight
    c.save(); c.translate(1260, 360); c.rotate(5)
    c.drawRect(skia.Rect(-230, -200, 250, 230), fp((0, 0, 0), 80, blur=14)); rect(c, -240, -210, 240, 220, '#FBF8F0', 5); rect(c, -240, -210, 240, -150, NAVY, 5)
    txt(c, '401(k) STATEMENT', -220, -168, 38, WHITE, KAL, skew=0)
    c.drawRect(skia.Rect(-224, -126, 224, -80), fp(GOLD_, 140)); txt(c, 'S&P 500 fund', -214, -92, 34, NAVY, KAL, skew=0); txt(c, '$10,000', 214, -92, 36, NAVY, MRK, 'right', skew=0)
    txt(c, 'Bond fund', -214, -32, 30, '#555555', KAL, skew=0); txt(c, '$4,200', 214, -32, 32, '#555555', MRK, 'right', skew=0)
    txt(c, 'Cash', -214, 20, 30, '#555555', KAL, skew=0); txt(c, '$1,850', 214, 20, 32, '#555555', MRK, 'right', skew=0)
    line(c, -214, 60, 214, 60, 3); txt(c, 'BALANCE', -214, 112, 36, NAVY, KAL, skew=0); txt(c, '$16,050', 214, 116, 46, NAVY, MRK, 'right', skew=0)
    c.restore()
    # sticky notes, polaroid, calculator, coffee, pen, cash, coins
    for (x, y, r, t, col) in [(330, 790, -8, 'RENT DUE', GOLD_), (1520, 700, 9, '-$650', ORNG), (900, 860, 4, 'ASK WHY?', GOLD_)]:
        c.save(); c.translate(x, y); c.rotate(r); rect(c, -95, -70, 95, 70, col, 4); txt(c, t, 0, 16, 40, NAVY if col == GOLD_ else WHITE, MRK, 'center', skew=0); c.restore()
    c.save(); c.translate(1010, 640); c.rotate(-12); rect(c, -110, -120, 110, 130, WHITE, 5); rect(c, -92, -102, 92, 72, '#2A3D68', 3); person(c, 0, 66, 0.3, CEO, eyes='half', mouth='smirk', rim=None); c.restore()
    c.save(); c.translate(1620, 900); c.rotate(14); rect(c, -90, -130, 90, 130, '#2E2E38', 5, r=14); rect(c, -70, -110, 70, -60, '#B8C8A0', 3)
    for i in range(12): rect(c, -70 + (i % 3) * 50, -40 + (i // 3) * 40, -34 + (i % 3) * 50, -10 + (i // 3) * 40, GOLD_ if i % 3 == 2 else GREY, 3, r=5)
    c.restore()
    circ(c, 1700, 250, 80, '#F4EFE2', 6); circ(c, 1700, 250, 62, '#5A3A22', 4); oval(c, 1680, 225, 1720, 240, (255, 255, 255), 0) if False else None
    for i in range(6): bill(c, 760 + i * 10, 850 - i * 12, rnd.uniform(-.2, .2) * 30)
    for (x, y) in [(640, 930), (690, 960), (1180, 860), (1130, 900), (560, 960)]: coin(c, x, y)
    sleeve(c, -40, 1140, 360, 760, 70, NAVY)    # hands sliding the papers in
    sleeve(c, 1960, 1160, 1460, 840, 70, GREY)
    night(c, [('oval', 900, 520, 980, 520, .92), ('oval', 1620, 260, 260, 220, .6)], ambient='#4A5A9A')
    add_light(c, 1720, 80, 380, '#FFE2A0', 60)
    frame_out(surf, 'env3_desk.png')

# ============ 4. MONEY STREET AT NIGHT (bank, cash advance, pawn, billboard, lamp, walker)
STREET_ERA = 'modern'
def street():
    surf = skia.Surface(W, H); c = surf.getCanvas(); rnd = random.Random(2)
    c.drawRect(skia.Rect(0, 0, W, H), sp(linear(0, 0, 0, 700, [hx('#0A1136'), hx('#24338A')])))
    for _ in range(70): c.drawCircle(rnd.uniform(0, W), rnd.uniform(0, 380), 1.8, fp('#E6EEFF', 200))
    circ(c, 1700, 140, 56, '#FFF6DC', 0); add_light(c, 1700, 140, 160, '#FFF6DC', 40)
    blur_begin(c, 5); city(c, 0, 250, W, 640, seed=11, base='#1A2A5C'); c.restore()
    # storefront row
    shops = [(0, 420, 'BANK', NAVY2, GOLD_), (420, 760, 'CASH ADVANCE', '#3A2A4A', ORNG), (760, 1100, 'PAWN', '#4A3626', GOLD_), (1100, 1460, 'DELI', '#2B4A5A', WHITE), (1460, 1920, 'MORTGAGES', '#2A3D68', GOLD_)]
    if STREET_ERA == '1920':   # period version: no modern signs
        shops = [(0, 420, 'BANK', NAVY2, GOLD_), (420, 760, 'TAILOR', '#3A2A4A', WHITE), (760, 1100, 'SECURITIES EXCHANGE CO.', '#4A3626', GOLD_), (1100, 1460, 'DELI', '#2B4A5A', WHITE), (1460, 1920, 'HOTEL', '#2A3D68', GOLD_)]
    for x0, x1, name, body, signc in shops:
        rect(c, x0, 300, x1, 820, body, 6)
        for wy in range(410, 520, 62):
            for wx in range(int(x0 + 30), int(x1 - 60), 80): rect(c, wx, wy, wx + 46, wy + 46, '#FFD27A' if rnd.random() < .55 else '#2B3A66', 4)
        rect(c, x0 + 30, 318, x1 - 30, 388, '#0A0F1E', 5, r=8); txt(c, name, (x0 + x1) / 2, 370, min(52, (x1 - x0 - 80) / (len(name) * 0.62)), signc, MRK, 'center', skew=0)
        rect(c, x0 + 40, 630, x1 - 140, 820, '#FFE7B0', 5); rect(c, x1 - 120, 650, x1 - 40, 820, '#3B2A1E', 5)
    for k in range(4): rect(c, 40 + k * 95, 560, 70 + k * 95, 820, '#E5E5E5', 4)   # bank columns
    if STREET_ERA != '1920': rect(c, 1500, 640, 1760, 760, WHITE, 4); txt(c, 'RATES 7.2%', 1630, 715, 48, ORNG, MRK, 'center', skew=0)
    # billboard on the roof
    if STREET_ERA != '1920': rect(c, 1000, 120, 1600, 290, '#0A0F1E', 6); txt(c, 'YOUR MONEY, EXPLAINED', 1300, 225, 52, GOLD_, MRK, 'center', skew=0); line(c, 1100, 290, 1100, 300, 8); line(c, 1500, 290, 1500, 300, 8)
    # pavement, road, cars
    rect(c, -10, 820, W + 10, 900, '#4A4E5E', 5); [line(c, x, 820, x - 30, 900, 3, (40, 42, 54)) for x in range(0, W, 120)]
    rect(c, -10, 900, W + 10, H + 10, '#22252F', 0)
    for x in range(0, W, 220): rect(c, x, 990, x + 120, 1002, '#E5E5E5', 0)
    for cx, col in ((420, '#7A1328'), (1460, '#2B4A7A')):
        rect(c, cx - 170, 920, cx + 170, 1020, col, 6, r=26); poly(c, [(cx - 100, 920), (cx - 60, 860), (cx + 70, 860), (cx + 110, 920)], col, 6)
        poly(c, [(cx - 84, 916), (cx - 54, 872), (cx - 4, 872), (cx - 4, 916)], '#9FB8F0', 4); circ(c, cx - 100, 1022, 32, '#1E1F2A', 5); circ(c, cx + 100, 1022, 32, '#1E1F2A', 5)
        add_light(c, cx + 170, 975, 60, '#FFF6DC', 160)
    # street lamp + walker + people at the cash advance
    line(c, 980, 900, 980, 470, 10); line(c, 980, 470, 1060, 470, 10); poly(c, [(1030, 470), (1090, 470), (1080, 500), (1040, 500)], '#2E2E38', 5)
    person(c, 900, 905, 0.6, WORKER, face=0.5, eyes='dot', mouth='flat', arms=('pocket', 'pocket'), hat=True, legs=walk_legs(1.2), bob=6)
    person(c, 540, 880, 0.52, INVESTOR, face=-0.4, eyes='half', mouth='flat', arms=('chin', 'down'))
    person(c, 650, 880, 0.52, ANALYST, face=-0.6, eyes='dot', mouth='o', arms=('down', 'hold'), sweat=.3)
    person(c, 220, 880, 0.52, BANKER, face=0.4, eyes='closed', mouth='smile', arms=('present', 'hip'))
    night(c, [('path', cone_path(1060, 500, 50, 520, 400), .85, 26), ('oval', 1060, 900, 300, 60, .8)] +
              [('oval', (x0 + x1) / 2, 720, (x1 - x0) * .55, 160, .55) for x0, x1, *_ in shops] + [('oval', 1300, 205, 340, 110, .7)] + [('oval', (x0 + x1) / 2, 353, (x1 - x0) * .5, 70, .6) for x0, x1, *_ in shops], ambient='#4C5CA0')
    add_light(c, 1060, 498, 90, '#FFE2A0', 200); add_light(c, 590, 353, 200, ORNG, 40)
    frame_out(surf, 'env4_street.png')

# ============ 5. KITCHEN TABLE AT NIGHT (bills, laptop glow, worried couple)
def kitchen():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    c.drawRect(skia.Rect(0, 0, W, H), fp('#2E4470'))
    for y in range(0, 720, 60):
        for x in range((y // 60) % 2 * 60, W, 120): c.drawRect(skia.Rect(x, y, x + 60, y + 60), fp('#34497A'))
    # window with night, cabinets, fridge, pendant lamp, wall calendar
    city(c, 1250, 120, 1650, 430, seed=4); rect(c, 1250, 120, 1650, 430, None, 8); line(c, 1450, 120, 1450, 430, 7); line(c, 1250, 275, 1650, 275, 7)
    for x in range(60, 1100, 210): rect(c, x, 60, x + 190, 300, '#E5E5E5', 6, r=6); circ(c, x + 170, 180, 8, NAVY, 3)
    rect(c, 1700, 140, 1900, 760, '#F4F4F4', 6, r=18); line(c, 1700, 380, 1900, 380, 5); rect(c, 1722, 230, 1736, 320, NAVY, 3, r=6); rect(c, 1722, 420, 1736, 520, NAVY, 3, r=6)
    for (x, y, t, col) in [(1790, 470, 'RENT', GOLD_), (1830, 600, 'BILLS!', ORNG)]:
        c.save(); c.translate(x, y); c.rotate(-6); rect(c, -56, -36, 56, 36, col, 3); txt(c, t, 0, 12, 32, NAVY if col == GOLD_ else WHITE, MRK, 'center', skew=0); c.restore()
    rect(c, 60, 300, 1100, 380, '#3B2A1E', 6); rect(c, 60, 380, 1100, 720, '#4A3626', 6)
    for x in range(60, 1100, 260): rect(c, x + 14, 400, x + 246, 700, '#5A3E2A', 5, r=6); circ(c, x + 230, 550, 8, GOLD_, 3)
    line(c, 860, 0, 860, 300, 4); poly(c, [(780, 300), (940, 300), (900, 250), (820, 250)], GOLD_, 5)
    clock(c, 1180, 180, 52, 11.7)
    rect(c, -10, 720, W + 10, H + 10, '#3A3328', 0); [line(c, -10, y, W + 10, y, 3, (48, 40, 30)) for y in range(760, H, 50)]
    # two people behind the table
    person(c, 640, 1060, 1.05, INVESTOR, face=0.35, eyes='dot', mouth='flat', brow=0.6, brow_tilt=-0.5, arms=('chin', 'hold'))
    person(c, 1180, 1060, 1.05, WORKER, face=-0.35, eyes='wide', mouth='o', brow=0.9, arms=('hold', 'hat'), sweat=.4)
    # table top with bills, laptop, mugs, calculator, piggy bank
    rect(c, 300, 760, 1560, 830, '#7A5A3C', 6, r=10); rect(c, 340, 830, 380, 1090, '#5A3E2A', 5); rect(c, 1480, 830, 1520, 1090, '#5A3E2A', 5)
    rect(c, 760, 640, 1060, 770, '#2E2E38', 6, r=8); rect(c, 780, 655, 1040, 760, '#0A1330', 4)
    g = skia.Path(); g.moveTo(790, 690); [g.lineTo(790 + j * 36, 690 + (j * 9 + (j % 2) * 10)) for j in range(1, 8)]; c.drawPath(g, ink(6, ORNG)); txt(c, '-12%', 1000, 690, 30, ORNG, MRK, 'right', skew=0)
    poly(c, [(720, 770), (1100, 770), (1130, 790), (690, 790)], '#3A3A46', 5)
    for (x, r, t) in [(470, -8, 'CREDIT CARD'), (560, 6, 'RENT DUE'), (1300, -5, 'CAR LOAN'), (1420, 8, 'UTILITIES')]:
        c.save(); c.translate(x, 770); c.rotate(r); rect(c, -80, -40, 80, 40, '#FBF8F0', 4); txt(c, t, 0, 10, 26, ORNG if 'DUE' in t else NAVY, KAL, 'center', skew=0); c.restore()
    for mx in (660, 1200): rect(c, mx - 26, 720, mx + 26, 772, WHITE, 5, r=6); c.drawPath((lambda p: (p.addArc(skia.Rect(mx + 14, 732, mx + 46, 762), -90, 180), p)[-1])(skia.Path()), ink(5))
    oval(c, 1080, 715, 1180, 775, GOLD_, 5); circ(c, 1172, 738, 12, GOLD_, 4); rect(c, 1118, 712, 1146, 718, NAVY, 0); coin(c, 1131, 702, 14)
    night(c, [('oval', 860, 560, 640, 460, .9), ('oval', 910, 720, 260, 120, .9), ('path', (lambda p: (p.addRect(skia.Rect(1250, 120, 1650, 430)), p)[-1])(skia.Path()), .7, 24)], ambient='#4C5CA0')
    add_light(c, 860, 300, 140, '#FFE2A0', 200); c.drawPath(cone_path(860, 300, 160, 900, 470), fp(GOLD_, 22, blur=34, blend=skia.BlendMode.kPlus)); add_light(c, 910, 705, 180, '#7FA6FF', 50)
    frame_out(surf, 'env5_kitchen.png')

if __name__ == '__main__':
    for f in (office, trading, desk, street, kitchen):
        f(); print('done', f.__name__)
