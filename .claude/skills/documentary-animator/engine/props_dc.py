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


# ---- added 23 Nov 2026 for Part 2 shots (PENDING owner approval in ASSET_LIBRARY.md)
def hand_mic(c, x, y, s=1.0, rot=0.0, arm=True):
    """Reporter's hand-held microphone: dark foam head, gold band, handle, sleeve + hand. Anchor = top of the handle; pointing up-left at rot 0."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if arm:
        poly(c, [(20, 120), (90, 120), (170, 420), (60, 420)], '#2B3A55', 5)                         # sleeve
        circ(c, 6, 96, 40, '#E9B98F', 5)                                                              # hand
    rect(c, -16, -20, 16, 110, '#2E2E38', 5, r=8)                                                      # handle
    rect(c, -20, -34, 20, -14, GOLD, 4, r=4)                                                           # band
    circ(c, 0, -86, 52, '#1B1D26', 5)                                                                  # foam head
    for k in range(-2, 3): c.drawLine(-40, -86 + k * 14, 40, -86 + k * 14, ink(2, '#3A3F4F', 180))    # mesh lines
    c.restore()

def passport(c, x, y, s=1.0, rot=0.0, open_k=0.0, tag='PASSPORT'):
    """Simple passport: navy cover, gold crest + word; open_k 1 shows a blank photo page. No real country marks."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-130, -170, 150, 190), fp((0, 0, 0), 70, blur=12))
    if open_k < .5:
        rect(c, -140, -180, 140, 180, '#1E3A6E', 6, r=10); circ(c, 0, -60, 52, None, 6, v=GOLD)
        label(c, tag, 0, 70, 38, GOLD, font=F_LABEL, align='center', skew=0)
    else:
        rect(c, -280, -180, 0, 180, '#F4EFE2', 6, r=8); rect(c, 0, -180, 280, 180, '#F4EFE2', 6, r=8)
        rect(c, -240, -120, -80, 40, '#C9D3EA', 4, r=6); circ(c, -160, -60, 34, '#9DB0DA', 4)
        for k in range(4): c.drawLine(-60 + 0, -110 + k * 34, 240, -110 + k * 34, ink(3, '#6B7390', 200))
    c.restore()


# ---------------- 24 Nov 2026, chapter 5 props (PENDING owner approval) ----------------
def fund_screen(c, x, y, s=1.0, t=0.0, title='YOUR 401(k)', share=6.0, grid=True):
    """Desk monitor facing the viewer showing a fund: header + a 10x10 waffle (100 squares = $10,000); `share` squares glow Nvidia green
    (brand colour exception, company element). t = seconds in: squares fill in over ~1 s. Anchor = screen centre; ~560*s wide."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -60, 238, 60, 270, '#3A3F4F', 5, r=6); rect(c, -140, 262, 140, 282, '#2E2E38', 5, r=8)               # stand + foot
    rect(c, -290, -230, 290, 240, '#1E2026', 6, r=18); rect(c, -268, -208, 268, 218, '#0F1A38', 3, r=8)         # bezel + screen
    label(c, title, 0, -150, 52, WHITE, font=F_TITLE, align='center', skew=0)
    label(c, 'S&P 500 INDEX FUND', 0, -112, 26, '#9DB0DA', font=F_LABEL, align='center', skew=0)
    if grid:
        n = int(min(1.0, max(0.0, t / 1.0)) * 100);
        for i in range(100):
            col, row = i % 10, i // 10; cx = -135 + col * 30; cy = -86 + row * 24
            lit = i < share
            if i < n or lit and t > .2:
                rect(c, cx - 12, cy, cx + 12, cy + 18, '#76B900' if lit else '#2B4A7A', 2.5, r=3)
        if share and t > 1.0:
            pulse = 1 + .06 * math.sin(t * 6); rect(c, -149, -90, -149 + 30 * share * pulse + 6, -64, None, 5, r=6, v=GOLD)
    c.restore()

def chip_box(c, x, y, s=1.0, rot=0.0, label_text='H200'):
    """Chip package on a small pallet: dark square die, gold pins, Nvidia-green corner mark. Anchor = centre; ~220*s wide."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for k in range(-4, 5):
        rect(c, -120, k * 24 - 5, -100, k * 24 + 5, '#C9A227', 2); rect(c, 100, k * 24 - 5, 120, k * 24 + 5, '#C9A227', 2)
        rect(c, k * 24 - 5, -120, k * 24 + 5, -100, '#C9A227', 2); rect(c, k * 24 - 5, 100, k * 24 + 5, 120, '#C9A227', 2)
    rect(c, -104, -104, 104, 104, '#2B2F38', 6, r=14); rect(c, -64, -64, 64, 64, '#1B1D26', 4, r=8)
    poly(c, [(-92, -92), (-62, -92), (-92, -62)], '#76B900', 3)
    label(c, label_text, 0, 14, 44, WHITE, font=F_TITLE, align='center', skew=0)
    c.restore()

def question_card(c, x, y, s=1.0, rot=0.0, n=1, line1='', line2='', u=1.0):
    """Index card with a gold number tab; u 0..1 pops it in (scale + settle). Anchor = centre; 460*s wide."""
    k = 0 if u <= 0 else min(1.0, u); sc = s * (0.4 + 0.6 * ease_out(k)) * (1 + .06 * math.sin(k * math.pi))
    if u <= 0: return
    c.save(); c.translate(x, y + (1 - ease_out(k)) * 60); c.rotate(rot); c.scale(sc, sc)
    c.drawRect(skia.Rect(-226, -146, 246, 166), fp((0, 0, 0), 70, blur=12))
    rect(c, -230, -150, 230, 150, '#FBF8F0', 6, r=10); circ(c, -190, -110, 34, GOLD, 5); label(c, str(n), -190, -92, 52, NAVY, font=F_TITLE, align='center', skew=0)
    label(c, line1, 0, -10, 38, NAVY, font=F_TITLE, align='center', skew=0); label(c, line2, 0, 50, 38, NAVY, font=F_TITLE, align='center', skew=0)
    c.restore()
