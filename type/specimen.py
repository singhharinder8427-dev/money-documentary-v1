import skia, numpy as np
W, H = 1920, 1080
NAVY, NAVY2, GOLD, ORANGE, WHITE, GREY, INK = '#14213D', '#1E3157', '#FCA311', '#F35B04', '#FFFFFF', '#E5E5E5', '#18161B'
def hx(h, a=255): h = h.lstrip('#'); return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(a))
def P(c, a=255, blur=0):
    p = skia.Paint(AntiAlias=True, Color=hx(c, a))
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p
TF = lambda f: skia.Typeface.MakeFromFile('../fonts/' + f)
SLAB, TYPE, BAR, BARS, SEG = TF('AlfaSlabOne-Regular.ttf'), TF('SpecialElite-Regular.ttf'), TF('BarlowCondensed-Bold.ttf'), TF('BarlowCondensed-SemiBold.ttf'), TF('DSEG7Classic-Bold.ttf')
def T(c, s, x, y, size, col, tf, align='left', stroke=0, scol=INK):
    f = skia.Font(tf, size); w = f.measureText(s); ox = {'left': 0, 'center': -w / 2, 'right': -w}[align]
    if stroke:
        sp = skia.Paint(AntiAlias=True, Color=hx(scol)); sp.setStyle(skia.Paint.kStroke_Style); sp.setStrokeWidth(stroke); sp.setStrokeJoin(skia.Paint.kRound_Join); c.drawString(s, x + ox, y, f, sp)
    c.drawString(s, x + ox, y, f, P(col)); return w
def counter(c, s, x, y, size, col):
    """digital counter: digits in the seven-segment font, other characters ($ , - B) in Barlow"""
    cx = x
    for ch in s:
        if ch.isdigit():
            f = skia.Font(SEG, size); ghost = skia.Font(SEG, size)
            c.drawString('8', cx, y, ghost, P(col, 14)); c.drawString(ch, cx, y, f, P(col)); c.drawString(ch, cx, y, f, P(col, 120, blur=8)); cx += f.measureText('8') + size * .06
        else:
            f = skia.Font(BAR, size * 1.15); c.drawString(ch, cx, y, f, P(col)); cx += f.measureText(ch) + size * .04
    return cx - x
def panel(c, x0, y0, x1, y1, col, r=18):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 + 8, y0 + 12, x1 + 8, y1 + 12), r, r), P('#000000', 110, blur=12))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r), P(col))
def tag(c, s, x, y): T(c, s, x, y, 26, GREY, BARS)

surf = skia.Surface(W, H); c = surf.getCanvas()
c.drawPaint(P(NAVY))
r = np.random.default_rng(4); g = np.clip(232 + r.normal(0, 1, (H, W)) * 9, 0, 255).astype(np.uint8)
gp = skia.Paint(); gp.setShader(skia.Image.fromarray(np.dstack([g, g, g, np.full_like(g, 255)])).makeShader(skia.TileMode.kClamp, skia.TileMode.kClamp)); gp.setBlendMode(skia.BlendMode.kMultiply)
T(c, 'TYPE SYSTEM', 70, 90, 54, GOLD, SLAB); T(c, 'money channel  ·  navy / gold', 560, 88, 34, GREY, BARS)

# 1 title (Alfa Slab One)
panel(c, 70, 140, 1000, 470, NAVY2); tag(c, 'TITLES + CHAPTER NAMES  ·  Alfa Slab One', 100, 185)
w = T(c, 'WHY YOUR ', 100, 290, 74, WHITE, SLAB)
wk = T(c, '401(k)', 100 + w, 290, 74, GOLD, SLAB)
T(c, 'IS A BET ON ONE MAN', 100, 395, 64, WHITE, SLAB)
c.drawRect(skia.Rect(100 + w, 304, 100 + w + wk, 316), P(GOLD))

# 2 chapter card (black)
panel(c, 1040, 140, 1850, 470, '#000000'); tag(c, 'CHAPTER CARD', 1070, 185)
T(c, 'CHAPTER 2', 1445, 290, 44, GOLD, BAR, 'center'); T(c, 'THE LOCKED DOOR', 1445, 380, 66, WHITE, SLAB, 'center')

# 3 typewriter text card (Special Elite) - words typed in with the voice
panel(c, 70, 510, 1000, 770, '#000000'); tag(c, 'TEXT CARDS + DOCUMENTS + QUOTES  ·  Special Elite (typewriter)', 100, 555)
T(c, 'Nobody told the man', 120, 650, 70, WHITE, TYPE); T(c, 'at the table.', 120, 730, 70, WHITE, TYPE); c.drawRect(skia.Rect(560, 680, 596, 736), P(GOLD))

# 4 lower third + sticky + location tag (Barlow Condensed)
panel(c, 1040, 510, 1850, 770, NAVY2); tag(c, 'LABELS, NAME TAGS, STICKY NOTES  ·  Barlow Condensed', 1070, 555)
panel(c, 1070, 590, 1450, 690, NAVY, 10); c.drawRect(skia.Rect(1070, 590, 1084, 690), P(GOLD))
T(c, 'J. CARTER', 1104, 640, 50, WHITE, BAR); T(c, 'FUND MANAGER', 1104, 676, 30, GOLD, BARS)
c.save(); c.translate(1620, 650); c.rotate(-5); panel(c, -150, -70, 150, 70, GOLD, 6); T(c, 'RENT DUE', 0, 22, 64, NAVY, BAR, 'center'); c.restore()
panel(c, 1070, 710, 1460, 752, '#0A0F1E', 6); T(c, 'WALL STREET  ·  NOV 2026', 1090, 742, 32, WHITE, BARS)

# 5 digital counters (DSEG7)
panel(c, 70, 810, 1850, 1040, '#05070D'); tag(c, 'NUMBER COUNTERS  ·  DSEG7 digital (seven-segment)', 100, 855)
counter(c, '$16,050', 110, 990, 110, GOLD); T(c, 'BALANCE', 110, 1022, 28, GREY, BARS)
counter(c, '-$589B', 760, 990, 110, ORANGE); T(c, 'ONE-DAY LOSS', 760, 1022, 28, GREY, BARS)
counter(c, '1,700', 1380, 990, 110, GOLD); T(c, 'PER AMERICAN', 1380, 1022, 28, GREY, BARS)
c.drawPaint(gp)
surf.makeImageSnapshot().save('type_system.png', skia.kPNG); print('saved')
