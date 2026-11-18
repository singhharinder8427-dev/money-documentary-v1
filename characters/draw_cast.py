from kit import *
LBL = skia.Typeface.MakeFromFile('/usr/share/fonts/opentype/inter/Inter-Black.otf') or skia.Typeface.MakeDefault()
surf = skia.Surface(W, H); c = surf.getCanvas()
# stage: navy wall with panels, wainscot, wood floor
c.drawRect(skia.Rect(0, 0, W, H), fp('#22355E'))
for x in range(0, W, 96): c.drawRect(skia.Rect(x, 0, x + 48, 760), fp('#29406E'))
rect(c, -10, 700, W + 10, 780, '#18284A'); rect(c, -10, 780, W + 10, H + 10, '#3A3328')
for x in range(-40, W, 160): line(c, x, 780, x - 120, H, 3, (40, 34, 26), 160)

def bob_hair_back(cx, cy, s, col):   # woman's bob: back part behind the head
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 116*s, cy - 106*s, cx + 116*s, cy + 96*s), 40*s, 40*s)); shape(c, p, col, 5.5)
def bob_hair_front(cx, cy, s, col):  # bangs, clipped to the head circle
    head = skia.Path(); head.addRRect(head_rrect(cx, cy, 100*s))
    c.save(); c.clipPath(head, doAntiAlias=True)
    b = skia.Path(); b.moveTo(cx - 110*s, cy - 18*s); b.lineTo(cx - 110*s, cy - 110*s); b.lineTo(cx + 110*s, cy - 110*s); b.lineTo(cx + 110*s, cy - 18*s)
    for i in range(6): b.lineTo(cx + (110 - (i + 0.5) * 36.6) * s, cy - (44 if i % 2 else 30) * s)
    b.close(); c.drawPath(b, fp(col)); c.drawPath(b, ink(5)); c.restore(); c.drawPath(head, ink(5.5))

S = 0.95; Y = 1000
CAST = [
  ('THE CEO', 230, dict(skin='#F8E2D2', skin_d='#E6C4AE', suit='#14213D', suit_d='#0C152B', shirt='#FFFFFF', tie='#FCA311', hair='silver', hair_col='#ECECF1', glasses=True, moustache=True, moustache_col='#FFFFFF', moustache_outline=True, moustache_dy=10),
     dict(face=0.25, eyes='half', mouth='smirk', brow=-0.2, arms=('pocket', 'hip'))),
  ('THE ANALYST', 595, dict(skin='#C8875A', skin_d='#A86C43', suit='#E5E5E5', suit_d='#BDBDBD', shirt='#FFFFFF', tie='#14213D', hair='slick', hair_col='#1A1414', glasses=True),
     dict(face=-0.2, eyes='dot', mouth='open', brow=0.5, arms=('down', 'gesture'))),
  ('THE WORKER', 960, dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#6B4A2E', suit_d='#4F3520', shirt='#F4EFE2', tie='#2B4A7A', hair='slick', hair_col='#7A4A26', hat_col='#3A3F4A', hat_band='#FCA311'),
     dict(face=0.0, eyes='wide', mouth='o', brow=0.8, brow_tilt=-0.6, arms=('chin', 'down'), sweat=0.3, hat=True)),
  ('THE BANKER', 1325, dict(skin='#E2B48C', skin_d='#C49468', suit='#2E2E38', suit_d='#1E1E26', shirt='#FFFFFF', tie='#FCA311', bowtie=True, hair='slick', hair_col='#3A2A20', moustache=True, hanky='#FCA311'),
     dict(face=0.3, eyes='closed', mouth='smile', brow=0.2, arms=('present', 'hip'))),
  ('THE INVESTOR', 1690, dict(skin='#8D5A3B', skin_d='#6F4429', suit='#FCA311', suit_d='#D88A06', shirt='#FFFFFF', tie='#14213D', hair=None),
     dict(face=-0.3, eyes='dot', mouth='smile', brow=0.3, arms=('hold', 'gesture'))),
]
night(c, [('oval', x, 640, 230, 560, 0.92) for _, x, _, _ in CAST] + [('oval', x, 1000, 200, 60, 0.8) for _, x, _, _ in CAST])
for _, x, _, _ in CAST: add_light(c, x, 160, 170, '#FCA311', 45)
finish(surf); vignette(c, 0.5)
import numpy as np
from PIL import Image as _PI, ImageFilter as _PF
_r = np.random.default_rng(5)
_fine = _r.normal(0, 1, (H, W))                                                     # fine paper tooth
_soft = np.asarray(_PI.fromarray((_r.random((54, 96)) * 255).astype(np.uint8)).resize((W, H), _PI.BICUBIC).filter(_PF.GaussianBlur(18)), dtype=float) / 255 - .5   # soft fibre blotches
_g = np.clip(232 + _fine * 9 + _soft * 34, 0, 255).astype(np.uint8)
_img = skia.Image.fromarray(np.dstack([_g, _g, _g, np.full_like(_g, 255)]))
gp = skia.Paint(); gp.setShader(_img.makeShader(skia.TileMode.kClamp, skia.TileMode.kClamp)); gp.setBlendMode(skia.BlendMode.kMultiply); c.drawPaint(gp)
# characters drawn last: no grain, no darkening, crisp and glossy
for _, x, _, _ in CAST: c.drawOval(skia.Rect(x - 120, 975, x + 120, 1010), fp((0, 0, 0), 120, blur=10))
for name, x, spec, pose in CAST:
    hx, hy = x, Y + S * HEAD_CY
    if name == 'THE INVESTOR': bob_hair_back(hx, hy, S, '#15110F')
    draw_char(c, x, Y, S, spec, light=-1, rim='#9FB8F0', **pose)
    if name == 'THE INVESTOR': bob_hair_front(hx, hy, S, '#15110F')

# name tags (navy box, gold bar), drawn after the grade so they stay crisp
f = skia.Font(LBL, 34)
for name, x, _, _ in CAST:
    w = f.measureText(name) + 46; rect(c, x - w/2, 1022, x + w/2, 1070, '#14213D', 4, r=6); c.drawRect(skia.Rect(x - w/2 + 2, 1024, x - w/2 + 12, 1068), fp('#FCA311'))
    c.drawString(name, x - w/2 + 28, 1058, f, fp('#FFFFFF'))
surf.makeImageSnapshot().save('five_v3.png', skia.kPNG); print('saved')
