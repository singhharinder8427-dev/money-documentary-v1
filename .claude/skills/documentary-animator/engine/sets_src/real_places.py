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
