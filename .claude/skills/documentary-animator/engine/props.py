"""Props for The Nvidia Files (Part 1, chapter 1). Every prop is drawn in the brand kit: thick ink outline, navy / gold / cream,
NO green anywhere, orange only for losses. All functions draw into a skia canvas: prop(c, x, y, s=1.0, ...).
Company names appear as plain typographic signs (no real logos); the chip is a generic navy-and-gold die."""
import math
from engine.kit import rect, poly, circ, oval, line, label, fp, ink, sp, linear, hx, C, skia, W, H
from engine.core import NAVY, NAVY2, NAVY3, GOLD, GOLD_D, WHITE, GREY, PAPER, F_TITLE, F_TYPE, F_LABEL, F_LABEL2

CREAM = '#F8EDD3'
BRAND = {'nvidia': '#76B900'}   # owner rule (CLAUDE.md 3b): real companies keep their original brand colours; verify before adding more


def sign_megaspeed(c, x, y, s=1.0, glow=1.0):
    """Shop-front sign, centre (x, y): MEGASPEED wordmark + three speed lines. glow 0..1 = lit-up amount."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect(-290, -66, 290, 66), fp(GOLD, int(90 * glow), blur=26))
    rect(c, -270, -56, 270, 56, NAVY, 7, r=10); rect(c, -258, -44, 258, 44, None, 3, r=6, v=GOLD)
    for i, w in enumerate((70, 52, 34)): c.drawRoundRect(skia.Rect(-246, -26 + i * 22, -246 + w, -18 + i * 22), 4, 4, fp(GOLD))
    label(c, 'MEGASPEED', 40, 20, 62, GOLD, font=F_TITLE, align='center', skew=0, stroke=0)
    c.restore()


def sign_old_arcade(c, x, y, s=1.0, hanging=0.0):
    """The OLD sign (invented name - the real game company is never shown): dull, chipped, tilted by `hanging` degrees."""
    c.save(); c.translate(x, y); c.rotate(hanging); c.scale(s, s)
    rect(c, -250, -50, 250, 50, '#3A3F4A', 6, r=8); rect(c, -238, -38, 238, 38, None, 3, r=5, v='#8C93A6')
    label(c, 'GAME PALACE', 0, 16, 56, '#B9BFCF', font=F_TITLE, align='center', skew=0)
    for px in (-150, 90): c.drawLine(px, -50, px + 18, 50, ink(3, (24, 22, 27), 200))   # cracks
    c.restore()


def chip(c, x, y, s=1.0, rot=0.0, glow=0.0, accent=GOLD):
    """Generic AI chip: navy package, `accent` die + pins (default gold; BRAND['nvidia'] for Nvidia chips). No traced logo."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if glow: c.drawCircle(0, 0, 150, fp(accent, int(80 * glow), blur=30))
    for k in range(-3, 4):
        for (ax, ay, bx, by) in ((-70, k * 20, -92, k * 20), (70, k * 20, 92, k * 20), (k * 20, -70, k * 20, -92), (k * 20, 70, k * 20, 92)):
            c.drawLine(ax, ay, bx, by, ink(7, (24, 22, 27))); c.drawLine(ax, ay, bx, by, ink(3.5, accent))
    rect(c, -72, -72, 72, 72, NAVY, 6, r=10); rect(c, -44, -44, 44, 44, accent, 5, r=5)
    for k in (-24, 0, 24): c.drawLine(-44, k, 44, k, ink(2.5, GOLD_D)); c.drawLine(k, -44, k, 44, ink(2.5, GOLD_D))
    rect(c, -22, -22, 22, 22, NAVY, 4, r=3)
    c.restore()


def certificate(c, x, y, s=1.0, rot=0.0, text='NVIDIA CLOUD PARTNER', k=1.0):
    """Certificate sliding onto a desk. Text only + the generic chip mark (never the real logo)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * k, s * k)
    c.drawRect(skia.Rect(-250, -170, 266, 188), fp((0, 0, 0), 80, blur=14))
    rect(c, -260, -180, 260, 180, CREAM, 6); rect(c, -244, -164, 244, 164, None, 3, v=GOLD_D)
    label(c, 'CERTIFICATE', 0, -118, 34, NAVY, font=F_TITLE, align='center', skew=0)
    label(c, text, 0, -52, min(40, 440 // max(len(text), 1) * 1.55), NAVY, font=F_TITLE, align='center', skew=0)
    c.drawLine(-170, -30, 170, -30, ink(3, GOLD_D))
    for i, w in enumerate((330, 280, 300)): c.drawRect(skia.Rect(-165, -4 + i * 22, -165 + w, 6 + i * 22), fp('#C9C3B5'))
    chip(c, -150, 118, .32, accent=BRAND['nvidia'])
    circ(c, 150, 112, 38, GOLD, 5); circ(c, 150, 112, 26, None, 2.5, v=GOLD_D)
    for a in (-18, 0, 18): c.drawLine(150 + a, 148, 150 + a * 1.4, 186, ink(7, GOLD_D))
    c.restore()


def server_rack(c, x, y, s=1.0, lit=1.0, phase=0.0):
    """Tall server rack, feet at (x, y). Gold status lights blink with `phase` (seconds)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -78, -420, 78, 0, '#2B2F3C', 7, r=8)
    for i in range(10):
        yy = -400 + i * 38
        rect(c, -66, yy, 66, yy + 30, '#3A3F4F', 3, r=4)
        for j in range(5):
            on = math.sin(phase * 3 + i * 1.7 + j * 2.3) > -0.2
            c.drawCircle(-48 + j * 14, yy + 15, 4.5, fp(GOLD if on else '#5A6076'))
        c.drawLine(10, yy + 15, 58, yy + 15, ink(3, '#14213D'))
    if lit: c.drawRect(skia.Rect(-90, -430, 90, 10), fp(GOLD, int(26 * lit), blur=24))
    c.restore()


def crate(c, x, y, s=1.0, label_text='SERVERS', open_k=0.0, glow=0.0):
    """Sealed shipping crate, front-bottom-centre at (x, y): wood, tape cross, stencil. glow lights the stencil gold."""
    c.save(); c.translate(x, y); c.scale(s, s)
    top = skia.Path(); top.moveTo(-120, -160); top.lineTo(-70, -205); top.lineTo(150, -205); top.lineTo(120, -160); top.close()
    side = skia.Path(); side.moveTo(120, -160); side.lineTo(150, -205); side.lineTo(150, -48); side.lineTo(120, 0); side.close()
    c.drawPath(top, fp('#6B4A2E')); c.drawPath(top, ink(5))
    c.drawPath(side, fp('#4F3520')); c.drawPath(side, ink(5))
    rect(c, -120, -160, 120, 0, '#8A6540', 6, r=3)
    for xx in (-120, -50, 20, 90): c.drawLine(xx, -160, xx, 0, ink(3, '#5B4128'))
    c.drawRect(skia.Rect(-14, -160, 14, 0), fp('#E8D9B0', 235)); c.drawRect(skia.Rect(-120, -92, 120, -66), fp('#E8D9B0', 235))   # sealing tape
    if glow: c.drawRect(skia.Rect(-100, -150, 100, -100), fp(GOLD, int(110 * glow), blur=16))
    label(c, label_text, 0, -118, 30, GOLD if glow > .3 else '#E8D9B0', font=F_TITLE, align='center', skew=0, stroke=3)
    chip(c, 80, -34, .17)
    if open_k > 0:
        c.drawRect(skia.Rect(-120, -160, 120, -160 + 8), fp((0, 0, 0), 120))
    c.restore()


def velvet_display(c, x, y, s=1.0, hand_k=0.0, glow=1.0):
    """Chip on a navy velvet cushion on a pedestal, gold rope between two posts. hand_k 0..1: a hand reaches, rope stops it."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -90, -250, 90, 0, '#2E2E38', 7, r=6); rect(c, -110, -270, 110, -240, '#3A3F4F', 6, r=6)
    oval(c, -80, -330, 80, -250, NAVY3, 6)
    chip(c, 0, -300, .46, glow=glow)
    for sx in (-300, 300):   # rope posts
        c.drawRect(skia.Rect(sx - 8, -250, sx + 8, 0), fp('#D6D9E2')); c.drawRect(skia.Rect(sx - 8, -250, sx + 8, 0), ink(5))
        circ(c, sx, -262, 20, GOLD, 5); rect(c, sx - 28, -8, sx + 28, 6, '#2E2E38', 5, r=4)
    rp = skia.Path(); rp.moveTo(-300, -240); rp.quadTo(0, -130, 300, -240); c.drawPath(rp, ink(16, (24, 22, 27))); c.drawPath(rp, ink(9, GOLD))
    if hand_k > 0:   # a real arm: navy suit sleeve, white cuff, hand with fingers reaching for the chip
        k = min(hand_k, 1); hx_, hy_ = 330 - 300 * k, -560 + 230 * k
        a = math.atan2(hy_ - (-640), hx_ - 620); L = math.hypot(hx_ - 620, hy_ + 640)
        c.save(); c.translate(620, -640); c.rotate(math.degrees(a))
        rect(c, -60, -52, L - 70, 52, NAVY2, 6, r=22); c.drawLine(0, 0, L - 80, 0, ink(3, '#2E4A7E'))
        rect(c, L - 96, -56, L - 58, 56, WHITE, 5, r=8)
        oval(c, L - 66, -40, L + 20, 40, '#E9B98F', 6)                                   # palm
        for i, fy in enumerate((-30, -10, 10, 30)): rect(c, L + 4, fy - 9, L + 62 - abs(i - 1.5) * 8, fy + 9, '#E9B98F', 4.5, r=9)   # fingers
        rect(c, L - 40, -58, L + 6, -36, '#E9B98F', 4.5, r=10)                            # thumb
        c.restore()
    c.restore()


def flashlight(c, x, y, angle_deg, length=700, spread=260, power=1.0):
    """Soft additive flashlight cone from (x, y). angle 0 = pointing right, 90 = down."""
    c.save(); c.translate(x, y); c.rotate(angle_deg)
    cone = skia.Path(); cone.moveTo(0, -10); cone.lineTo(length, -spread / 2); cone.lineTo(length, spread / 2); cone.lineTo(0, 10); cone.close()
    c.drawPath(cone, fp('#FFE9B0', int(95 * power), blur=18, blend=skia.BlendMode.kPlus))
    c.drawCircle(length, 0, spread * .42, fp('#FFE9B0', int(80 * power), blur=30, blend=skia.BlendMode.kPlus))
    rect(c, -44, -14, 6, 14, '#2E2E38', 5, r=5); rect(c, 6, -20, 24, 20, GOLD, 4, r=4)
    c.restore()


def tag_pair(c, x, y, k=1.0, cross_k=0.0):
    """Two identical name tags 'HUANG' joined by an equals sign that gets crossed out (No relation. Same last name.)"""
    def tag(cx, role):
        rect(c, cx - 190, y - 70, cx + 190, y + 70, '#F4EFE2', 6, r=10); c.drawRect(skia.Rect(cx - 190, y - 70, cx + 190, y - 26), fp(NAVY)); c.drawRect(skia.Rect(cx - 190, y - 70, cx + 190, y - 26), ink(6))
        label(c, 'HELLO MY NAME IS', cx, y - 38, 26, WHITE, font=F_LABEL, align='center', skew=0)
        label(c, 'HUANG', cx, y + 40, 62, NAVY, font=F_TITLE, align='center', skew=0)
        label(c, role, cx, y + 62, 22, '#6B7390', font=F_LABEL2, align='center', skew=0)
    c.save(); c.translate(0, (1 - min(k, 1)) * -40); tag(x - 330, 'NVIDIA'); tag(x + 330, 'MEGASPEED')
    c.drawRect(skia.Rect(x - 46, y - 30, x + 46, y - 12), fp(GOLD)); c.drawRect(skia.Rect(x - 46, y + 12, x + 46, y + 30), fp(GOLD))
    if cross_k > 0:   # slash through the equals sign (ink on a cream under-stroke; orange is for losses only)
        e = min(cross_k, 1); x0, y0 = x - 70, y + 52; x1, y1 = x0 + 140 * e, y0 - 104 * e
        c.drawLine(x0, y0, x1, y1, ink(22, '#F4EFE2')); c.drawLine(x0, y0, x1, y1, ink(12, (24, 22, 27)))
    c.restore()
