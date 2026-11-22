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


# ---- added 22 Nov 2026 (Nvidia Files QA fixes). PENDING owner approval -> ASSET_LIBRARY.md ----
NV_GREEN = '#76B900'
def nvidia_logo(c, x, y, s=1.0, word=True, on_dark=True):
    """Simple ROUGH 2D Nvidia-style mark (rule 3b): a green square with a white eye-like swirl, + the name. Drawn fresh, not traced."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -60, -50, 60, 50, NV_GREEN, 5, r=6)
    p = skia.Path(); p.moveTo(-54, 0); p.cubicTo(-30, -36, 30, -36, 54, 0); p.cubicTo(30, 36, -30, 36, -54, 0); p.close()
    c.drawPath(p, fp(WHITE)); circ(c, 4, 0, 20, NV_GREEN, 0); circ(c, 4, 0, 9, WHITE, 0)
    q = skia.Path(); q.moveTo(-60, 22); q.quadTo(-10, 4, 20, -50); c.drawPath(q, ink(6, NV_GREEN))
    if word: label(c, 'NVIDIA', 78, 22, 64, WHITE if on_dark else NAVY, F_TITLE, 'left')
    c.restore()

def phone_flat(c, x, y, s=1.0, lit=0.0, t=0.0):
    """Phone lying FLAT on a table (perspective), screen lights up when lit > 0, buzzes when lit pulses."""
    bz = math.sin(t * 70) * 3 * lit
    c.save(); c.translate(x + bz, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-70, -22); p.lineTo(70, -22); p.lineTo(90, 22); p.lineTo(-90, 22); p.close()
    c.drawPath(p, fp('#1B1D26')); c.drawPath(p, ink(5))
    q = skia.Path(); q.moveTo(-60, -16); q.lineTo(60, -16); q.lineTo(76, 16); q.lineTo(-76, 16); q.close()
    c.drawPath(q, fp('#FFE2A0' if lit > .5 else '#24365E'))
    if lit > 0: c.drawOval(skia.Rect(-160, -70, 160, 60), fp(GOLD, int(80 * lit), blur=24))
    c.restore()

def hair_dryer(c, x, y, s=1.0, ang=0.0, t=0.0, hand=True, sleeve='#6B4A2E', skin='#F0CDA4', blowing=True):
    """Hair dryer HELD by a hand + sleeve (never floating). Hot-air lines when blowing."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    if hand:
        rect(c, -30, 150, 30, 420, sleeve, 6, r=14); rect(c, -34, 140, 34, 168, WHITE, 5, r=6)
    rect(c, -40, -10, 40, 170, '#2E2E38', 6, r=16); rect(c, -150, -60, 60, 60, '#3A3F4F', 7, r=50); circ(c, -150, 0, 56, '#2E2E38', 6)
    if hand:
        oval(c, -48, 40, 48, 140, skin, 6)
        for i in range(3): rect(c, -56, 54 + i * 26, 2, 74 + i * 26, skin, 4, r=9)
    if blowing:
        for i in range(4): c.drawLine(-210, -30 + i * 20, -330 - 20 * math.sin(t * 20 + i), -40 + i * 26, ink(6, GOLD, 160))
    c.restore()

def handcuffs(c, x, y, s=1.0, close_k=1.0, rot=0.0):
    """Proper handcuffs: two thick cuffs with a ratchet block each and a 3-link chain; they snap shut as close_k goes 0 -> 1."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for sx in (-1, 1):
        cx = sx * 170; c.save(); c.translate(cx, 0); c.rotate(sx * (1 - close_k) * 30)
        p = skia.Path(); p.addArc(skia.Rect(-110, -110, 110, 110), 200, 300 - 60 * (1 - close_k)); c.drawPath(p, ink(44, '#14141A')); c.drawPath(p, ink(30, '#C9CFDB'))
        c.drawPath(p, ink(6, WHITE, 120)); rect(c, -40 * sx - 40, -150, -40 * sx + 40, -70, '#AEB4C2', 6, r=10); circ(c, -40 * sx, -110, 10, '#14141A', 0)
        c.restore()
    for i in range(3):
        cx = -70 + i * 70; oval(c, cx - 36, -126, cx + 36, -94, None, 0); c.drawOval(skia.Rect(cx - 36, -126, cx + 36, -94), ink(16, '#14141A')); c.drawOval(skia.Rect(cx - 36, -126, cx + 36, -94), ink(9, '#C9CFDB'))
    c.restore()

def scooter_rider(c, x, y, s=1.0, t=0.0, skin='#C98E62', jacket='#2B4A7A', box='#C9A26A'):
    """Delivery scooter WITH a rider (helmet, jacket) and a pizza box on the back."""
    c.save(); c.translate(x, y + 4 * math.sin(t * 25)); c.scale(s, s)
    circ(c, -110, 60, 50, '#2E2E38', 6); circ(c, 110, 60, 50, '#2E2E38', 6); circ(c, -110, 60, 18, '#9DB0DA', 4); circ(c, 110, 60, 18, '#9DB0DA', 4)
    rect(c, -150, -20, 150, 40, '#2B4A7A', 6, r=20); line(c, 120, -20, 160, -140, 10); line(c, 140, -140, 190, -140, 10)
    rect(c, -200, -150, -70, -20, box, 5, r=4); label(c, 'PIZZA', -135, -76, 30, NAVY, F_LABEL, 'center')
    rect(c, -40, -200, 50, -20, jacket, 6, r=24); line(c, 40, -150, 150, -135, 14, jacket); circ(c, 150, -135, 14, skin, 4)
    line(c, 10, -20, 70, 40, 16, '#1E2A40'); circ(c, 5, -250, 52, skin, 6)
    p = skia.Path(); p.addArc(skia.Rect(-55, -310, 65, -190), 180, 180); c.drawPath(p, fp(GOLD)); c.drawPath(p, ink(6)); rect(c, 20, -262, 62, -240, '#24365E', 4, r=6)
    c.restore()

def paper_in_hand(c, hx, hy, s=1.0, title='STATEMENT', lines=('S&P 500 index fund',), rot=6.0):
    """A sheet held at a character's hand position (kit.hand_pos), so documents are never floating."""
    c.save(); c.translate(hx, hy); c.rotate(rot); c.scale(s, s)
    rect(c, -20, -240, 300, 160, PAPER, 5); label(c, title, 0, -190, 38, NAVY, F_LABEL)
    for i, ln in enumerate(lines): label(c, ln, 0, -130 + i * 46, 30, NAVY, F_TYPE)
    circ(c, 0, 0, 22, '#E9B98F', 5); c.restore()

def phone_in_hand(c, hx, hy, s=1.0, lit=True):
    """Phone held at a hand position (for poses other than 'phone')."""
    c.save(); c.translate(hx, hy - 30 * s); c.scale(s, s)
    rect(c, -26, -50, 26, 50, '#1B1D26', 5, r=8); c.drawRect(skia.Rect(-20, -42, 20, 40), fp('#FFE2A0' if lit else '#24365E'))
    if lit: c.drawCircle(0, 0, 60, fp(GOLD, 50, blur=18))
    c.restore()
