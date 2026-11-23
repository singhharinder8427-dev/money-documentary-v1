"""Props for The Nvidia Files Part 2 (23 Nov 2026), LOCKED by the owner (23 Nov) - do not change without asking. Same rules as props.py: brand kit, thick ink outline,
real colours only for real objects (plane livery = flag colours), gold stamps. Signature: prop(c, x, y, s=1.0, ...).
Stamps on props (REPORTED / ONE SOURCE / NOT CONFIRMED / TOP SECRET): use prop_stamp (gold + thick navy stroke, owner rule 23 Nov).
widgets.stamp stays as-is for full-screen stamps in older videos."""
import math
from engine.kit import rect, poly, circ, oval, line, label, fp, ink, skia
from engine.core import NAVY, GOLD, WHITE, F_TITLE, F_TYPE, F_LABEL
from engine.kit import lerp, ease_out, INK
from engine.widgets import _font
import random

def af1_plane(c, x, y, s=1.0, rot=0.0, lights=1.0):
    """Air Force One, side view, flying right: white fuselage, light-blue + dark-blue cheat line, blue tail, engines, window row,
    blinking wing-tip lights. Anchor = centre of the fuselage; width ~ 600*s."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    poly(c, [(-60, 6), (-180, 90), (-120, 96), (40, 12)], '#E6E9EE', 5)                                 # far wing
    poly(c, [(-300, -20), (-380, -150), (-330, -150), (-250, -24)], '#1F4E8C', 5)                       # tail fin (blue)
    poly(c, [(-300, -12), (-370, -22), (-372, -6), (-300, 8)], '#E6E9EE', 4)                            # tail plane
    fus = skia.Path(); fus.moveTo(-320, -26); fus.lineTo(220, -26); fus.cubicTo(300, -24, 330, -4, 340, 10); fus.cubicTo(330, 30, 290, 36, 220, 36)
    fus.lineTo(-320, 36); fus.close(); c.drawPath(fus, fp('#F4F6F9')); c.save(); c.clipPath(fus, doAntiAlias=True)
    c.drawRect(skia.Rect(-330, 14, 350, 40), fp('#7FB2E5')); c.drawRect(skia.Rect(-330, 4, 350, 14), fp('#1F4E8C')); c.restore(); c.drawPath(fus, ink(5))
    for wx in range(-240, 180, 36): c.drawRoundRect(skia.Rect(wx, -14, wx + 14, 2), 5, 5, fp('#2B3A5C'))
    poly(c, [(-70, 8), (-210, 110), (-150, 116), (30, 20)], '#F4F6F9', 5)                               # near wing
    rect(c, -150, 86, -90, 112, '#D9DDE3', 4, r=10)                                                      # engine
    c.drawCircle(-196, 108, 5 + 3 * lights, fp('#FF5A6E', int(200 * lights), blur=3)); c.drawCircle(-384, -148, 4 + 2 * lights, fp('#FFFFFF', int(220 * lights), blur=3))
    c.restore()

def memo_folder(c, x, y, s=1.0, rot=0.0, open_k=0.0, label_text='TOP SECRET'):
    """Classified memo: manila folder, navy band with a gold typewriter label, a few pages peeking out; open_k 0..1 lifts the cover.
    Draw the gold stamp (widgets.stamp) separately when it should slam on."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-150, -100, 170, 120), fp((0, 0, 0), 70, blur=12))                              # soft shadow
    rect(c, -160, -110, 160, 110, '#D9B877', 5, r=6)                                                      # back flap
    for k in range(3): rect(c, -140 + k * 6, -118 - k * 4 - 10 * open_k, 140 + k * 6, 96, '#FBF8F0', 3, r=2)   # pages
    c.save(); c.translate(-160, 110); c.rotate(-open_k * 38)
    rect(c, 0, -216, 320, 0, '#E6C98A', 5, r=6); rect(c, 0, -216, 320, -170, NAVY, 5, r=6)
    label(c, label_text, 160, -184, 30, GOLD, font=F_TYPE, align='center', skew=0)
    rect(c, 30, -150, 290, -130, '#C9A96A', 2, r=3); rect(c, 30, -118, 210, -102, '#C9A96A', 2, r=3); c.restore()
    c.restore()


def prop_stamp(c, s, x, y, t, color=GOLD, rot=-8, size=110, stroke=8):
    """Stamp slam for use ON a prop: same motion as widgets.stamp (scale 2.6 -> 1 in 0.2 s, shake returned) but gold with a thick
    navy ink stroke on the border and the letters, plus a soft shadow, so it stays readable on light paper/folders. t = seconds since the hit."""
    if t < 0: return (0, 0)
    k = lerp(2.6, 1.0, ease_out(min(t / .2, 1))); a = int(255 * min(t / .08, 1))
    f = _font(F_TITLE, size); tw = f.measureText(s.upper())
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    boxes = [skia.RRect.MakeRectXY(skia.Rect(-tw / 2 - 46 + i, -size * .78 + i, tw / 2 + 46 - i, size * .52 - i), 18, 18) for i in (0, 22)]
    for rr, w in zip(boxes, (12, 5)):
        c.drawRRect(rr, ink(w + stroke, INK, a))                                                         # navy stroke under the gold line
    for rr, w in zip(boxes, (12, 5)):
        c.drawRRect(rr, ink(w, color, a))
    c.drawString(s.upper(), -tw / 2 + 4, size * .3 + 6, f, fp((0, 0, 0), int(a * .35), blur=5))          # soft shadow
    c.drawString(s.upper(), -tw / 2, size * .3, f, ink(stroke, INK, a))                                  # navy letter stroke
    c.drawString(s.upper(), -tw / 2, size * .3, f, fp(color, a)); c.restore()
    if t < .35: r = random.Random(int(t * 100)); amp = 14 * (1 - t / .35); return (r.uniform(-amp, amp), r.uniform(-amp, amp))
    return (0, 0)
