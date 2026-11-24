"""Props for "The $1.7 Trillion Morning" (24 Nov 2026) - LOCKED by the owner 24 Nov 2026. Brand style: flat shapes, one ink outline,
gold = money, orange = losses only. Company marks from engine/logos.py. All draw at (x, y) centre, scale s; u / *_k = 0..1 animation."""
import math
from engine.kit import rect, poly, circ, line, label, fp, ink, skia, ease_out, lerp
from engine.core import NAVY, GOLD, WHITE, ORANGE, F_TITLE, F_TYPE, F_LABEL
from engine import logos

def price_tag(c, x, y, s=1.0, rot=-8, price='$83', old=None, u=1.0):
    """Gold price tag on a string; `old` (e.g. '$70-78') shown crossed out above it; u slides the new price in."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawLine(-210, -20, -300, -120, ink(4, '#C9B995'))
    poly(c, [(-210, -70), (-150, -120), (190, -120), (190, 120), (-150, 120), (-210, 70)], GOLD, 6); circ(c, -165, 0, 14, '#F4EFE2', 4)
    if old:
        label(c, old, 30, -40, 52, NAVY, font=F_LABEL, align='center', skew=0, alpha=.6); c.drawLine(-70, -58, 130, -58, ink(6, ORANGE))
    c.save(); c.translate(0, (1 - ease_out(u)) * 60); label(c, price, 30, 70 if old else 30, 110, NAVY, font=F_TITLE, align='center', skew=0, alpha=min(1, u * 2)); c.restore()
    c.restore()

def investor_list(c, x, y, s=1.0, open_k=1.0, rows=9):
    """'The List': a tall paper with a gold edge, names blurred into bars; open_k 1 = unrolled, 0 = rolled shut to a scroll."""
    h = lerp(40, 520, ease_out(open_k)); c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -170, -h / 2, 170, h / 2, '#FBF8F0', 5, r=6); rect(c, -170, -h / 2, -150, h / 2, GOLD, 0); rect(c, 150, -h / 2, 170, h / 2, GOLD, 0)
    if h > 140:
        label(c, 'ALLOCATION LIST', 0, -h / 2 + 50, 34, NAVY, font=F_TYPE, align='center', skew=0)
        for k in range(rows):
            yy = -h / 2 + 90 + k * 46
            if yy > h / 2 - 30: break
            c.drawRect(skia.Rect(-120, yy, -120 + 160 + 60 * math.sin(k * 2.1), yy + 14), fp('#9DB0DA', 200, blur=3)); circ(c, 118, yy + 7, 9, GOLD, 2)
    for sy in (-1, 1): rect(c, -186, sy * h / 2 - 16, 186, sy * h / 2 + 16, '#E4D9BC', 5, r=16)                    # scroll rods
    c.restore()

def share_certificate(c, x, y, s=1.0, rot=0.0, signed=1.0, name='CO-FOUNDER'):
    """Ivory stock certificate with a gold border, the rough Anthropic mark, and a signature that writes itself (signed 0..1)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-200, -120, 216, 136), fp((0, 0, 0), 70, blur=12)); rect(c, -210, -130, 210, 130, '#FAF9F5', 5, r=6)
    rect(c, -194, -114, 194, 114, None, 4); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-184, -104, 184, 104), 6, 6), ink(3, GOLD))
    logos.anthropic(c, -140, -50, 30); label(c, 'SHARE CERTIFICATE', 40, -56, 26, NAVY, font=F_TITLE, align='center', skew=0)
    label(c, name, 40, -18, 24, NAVY, font=F_TYPE, align='center', skew=0); c.drawLine(-60, 70, 150, 70, ink(2.5, NAVY))
    if signed > 0:
        p = skia.Path(); n = int(28 * min(signed, 1))
        for k in range(n + 1): xx = -50 + k * 7; yy = 58 + math.sin(k * .9) * 12 - k * .4; p.moveTo(xx, yy) if k == 0 else p.lineTo(xx, yy)
        c.drawPath(p, ink(4, NAVY))
    circ(c, 150, 92, 22, GOLD, 3)
    c.restore()

def app_icon(c, x, y, s=1.0, grey=0.0, name='SORA'):
    """A phone app icon (rough OpenAI mark, black/white) that greys out and gets a SHUT DOWN look as grey -> 1."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -90, -90, 90, 90, '#000000', 6, r=34); logos.openai(c, 0, 0, 62)
    if grey > 0: rect(c, -90, -90, 90, 90, None, 0, r=34); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-90, -90, 90, 90), 34, 34), fp('#8A8E9A', 210 * grey))
    label(c, name, 0, 140, 40, WHITE, font=F_LABEL, align='center', skew=0, alpha=1 - .5 * grey)
    c.restore()

def bell(c, x, y, s=1.0, t=0.0, ring=1.0):
    """Gold opening bell swinging, with ring lines while ring > 0."""
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(math.sin(t * 14) * 14 * ring)
    p = skia.Path(); p.moveTo(-70, 60); p.quadTo(-70, -80, 0, -90); p.quadTo(70, -80, 70, 60); p.lineTo(90, 80); p.lineTo(-90, 80); p.close()
    c.drawPath(p, fp(GOLD)); c.drawPath(p, ink(6)); circ(c, 0, 92, 16, '#D68408', 4); circ(c, 0, -96, 12, GOLD, 4); c.restore()
    if ring > 0:
        for k in range(3):
            r_ = 120 + k * 30 + (t * 90) % 30
            for sd in (-1, 1): c.drawArc(skia.Rect(x - r_ * s, y - r_ * s, x + r_ * s, y + r_ * s), -40 if sd > 0 else 140, 80, False, ink(5, GOLD, 200 * ring * (1 - k / 3)))

def fund_box(c, x, y, s=1.0, grab=0.0, title='TOTAL MARKET FUND'):
    """An index-fund box on a conveyor; a mechanical arm pops out and grabs an 'ANT' share card as grab 0 -> 1."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -130, -110, 130, 110, '#C9A96A', 5, r=8); rect(c, -130, -110, 130, -70, NAVY, 5, r=8)
    label(c, title, 0, -82, 20, GOLD, font=F_LABEL, align='center', skew=0)
    k = ease_out(grab); ax = lerp(0, 0, k); ay = lerp(-110, -260, k)
    c.drawLine(0, -110, ax, ay, ink(10, '#8A8E9A')); circ(c, ax, ay, 14, '#8A8E9A', 4)
    if grab > .5: rect(c, ax - 50, ay - 70, ax + 50, ay - 14, '#FAF9F5', 4, r=6); label(c, 'ANT', ax, ay - 30, 30, NAVY, font=F_TITLE, align='center', skew=0)
    c.restore()

def conveyor(c, t, y, x0=0, x1=1920, speed=80):
    """Moving conveyor belt (rollers turn, stripes slide)."""
    rect(c, x0, y, x1, y + 40, '#3A3D4A', 5)
    off = (t * speed) % 60
    for x in range(int(x0 - 60 + off), int(x1), 60): c.drawLine(x, y + 6, x + 20, y + 34, ink(4, '#5A5E6E'))
    for x in range(int(x0 + 30), int(x1), 120): circ(c, x, y + 52, 14, '#5A5E6E', 4)

def subscribe_button(c, x, y, s=1.0, u=1.0, click=0.0):
    """End-of-video subscribe ask in our brand: navy pill + gold bell; a cursor clicks at click 0 -> 1 and it turns SUBSCRIBED."""
    k = ease_out(u); c.save(); c.translate(x, y + (1 - k) * 160); c.scale(s, s)
    done = click >= .5; c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-250, -56, 250, 56), 56, 56), fp(NAVY if not done else '#2B4A7A'))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-250, -56, 250, 56), 56, 56), ink(5, GOLD))
    label(c, 'SUBSCRIBED' if done else 'SUBSCRIBE', 30, 18, 48, WHITE, font=F_TITLE, align='center', skew=0)
    bp = skia.Path(); bp.moveTo(-200, 18); bp.quadTo(-200, -26, -180, -28); bp.quadTo(-160, -26, -160, 18); bp.close(); c.drawPath(bp, fp(GOLD)); circ(c, -180, 24, 6, GOLD, 0)
    if 0 < click < 1:                                                                                                 # cursor arrow pressing
        cx_, cy_ = lerp(200, 120, min(click * 2, 1)), lerp(120, 30, min(click * 2, 1)); sc = .85 if .4 < click < .6 else 1
        c.save(); c.translate(cx_, cy_); c.scale(sc, sc); poly(c, [(0, 0), (0, 56), (14, 44), (26, 70), (36, 66), (24, 40), (44, 40)], WHITE, 4); c.restore()
    c.restore()

if __name__ == '__main__':
    s = skia.Surface(1920, 1080); cv = s.getCanvas()
    for f, kw in ((price_tag, dict(x=300, y=300, old='$70-78', u=.6)), (investor_list, dict(x=700, y=500, open_k=.7)), (share_certificate, dict(x=1200, y=300, signed=.5)),
                  (app_icon, dict(x=1600, y=300, grey=.5)), (bell, dict(x=300, y=800, t=1.2)), (fund_box, dict(x=800, y=900, grab=.8)),
                  (subscribe_button, dict(x=1400, y=900, click=.45))):
        f(cv, **kw)
    conveyor(cv, 1.0, 1000); assert s.makeImageSnapshot().toarray()[..., 3].sum() > 0; print('props_ipo self-check ok')
