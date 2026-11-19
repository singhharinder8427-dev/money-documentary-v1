"""Thumbnail B - "$20 MILLION GONE" - drawn with the channel engine (same Ponzi as the video)."""
import sys, os, math, random, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / '.claude' / 'skills' / 'documentary-animator'))
import skia
from engine.core import W, H, NAVY, GOLD, ORANGE, WHITE, F_TITLE
from engine import kit, widgets as Wd, anim as A
from engine.kit import fp, ink, draw_char, hand_pos, poly, rect, circ, vignette
from engine.cast import CAST
from engine.sets import get_set

def thumb(path):
    s = skia.Surface(W, H); c = s.getCanvas()
    # background: the 1920s night street, zoomed + blurred, darkened
    st = get_set('night/street1920'); p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(10, 10))
    c.save(); c.translate(W / 2, H / 2); c.scale(1.6, 1.6); c.translate(-1100, -560); c.drawImage(st.base, 0, 0, skia.SamplingOptions(), p); c.restore()
    c.drawRect(skia.Rect(0, 0, W, H), fp((6, 10, 28), 120)); vignette(c, .75, .45)
    # police car on the right + spotlight onto Ponzi
    A.police_car(c, 1560, 990, 2.0, .9, spot_target=None)
    beam = skia.Path(); beam.moveTo(1500, 735); beam.lineTo(380, 200); beam.lineTo(380, 860); beam.close()
    c.drawPath(beam, fp('#FFF2C8', 150, blur=24, blend=skia.BlendMode.kPlus)); c.drawCircle(1500, 735, 60, fp('#FFF6DC', 230, blur=14))
    c.drawCircle(600, 500, 400, fp('#FFE9B0', 95, blur=60, blend=skia.BlendMode.kPlus))
    for x, y, col in ((1700, 650, '#6F8FE0'), (1640, 640, ORANGE)): c.drawCircle(x, y, 200, fp(col, 55, blur=60, blend=skia.BlendMode.kPlus))
    # orange crash arrow zig-zag down (right)
    pts = [(1180, 250), (1290, 360), (1240, 400), (1400, 560)]
    pa = skia.Path(); pa.moveTo(*pts[0]); [pa.lineTo(*q) for q in pts[1:]]
    c.drawPath(pa, ink(48, (10, 17, 36))); c.drawPath(pa, ink(32, ORANGE))
    poly(c, [(1335, 600), (1450, 515), (1458, 612)], ORANGE, 8)
    # Ponzi close-up: shocked, gritted teeth, sweat, hat knocked crooked, hands cuffed in front
    spec = dict(CAST['ponzi']); X, FEET, S = 610, 1420, 2.05
    draw_char(c, X, FEET, S, spec, face=.15, eyes='wide', mouth='grit', brow=1.0, brow_tilt=-.8, arms=('chin', 'chin'), tilt=-7,
              sweat=.35, light=-1, rim='#FFB070', hat=True)
    r = random.Random(3)
    for k in range(2): c.drawCircle(X + (-150 if k else 175), FEET + S * kit.HEAD_CY - 60 + k * 40, 0, fp(WHITE))
    # handcuffs on the wrists
    lx, ly = hand_pos(X, FEET, S, ('chin', 'chin'), -1); rx, ry = hand_pos(X, FEET, S, ('chin', 'chin'), 1); cy = (ly + ry) / 2 + 38
    for hx in (lx, rx):                                                        # cuff rings around each wrist
        c.drawCircle(hx, cy, 40, ink(26, (10, 17, 36))); c.drawCircle(hx, cy, 40, ink(15, '#D7DCE6'))
        c.drawArc(skia.Rect(hx - 40, cy - 40, hx + 40, cy + 40), 200, 70, False, ink(6, WHITE))
    for k in range(4):                                                         # short chain between the cuffs
        t_ = (k + .5) / 4; x_ = lx + 40 + (rx - lx - 80) * t_
        c.drawOval(skia.Rect(x_ - 16, cy + 6 - 9, x_ + 16, cy + 6 + 9), ink(12, (10, 17, 36))); c.drawOval(skia.Rect(x_ - 16, cy + 6 - 9, x_ + 16, cy + 6 + 9), ink(6, '#9AA3B5'))
    for k in range(18):                                                           # orange sparks off the cuffs
        a = r.uniform(0, 2 * math.pi); d = r.uniform(60, 170); x0, y0 = (lx + rx) / 2 + math.cos(a) * d, cy + 30 + abs(math.sin(a)) * d * .6
        c.drawCircle(x0, y0, r.uniform(4, 9), fp('#FFB070')); c.drawCircle(x0, y0, 22, fp(ORANGE, 70, blur=10))
    # gold coins falling / scattered at the bottom
    for k in range(16):
        x0 = r.uniform(60, 1300); y0 = r.uniform(930, 1070); c.save(); c.translate(x0, y0); c.scale(abs(math.cos(k)) * .7 + .35, 1); Wd.coin(c, 0, 0, r.uniform(34, 52)); c.restore()
    for k in range(7):                                                        # coins flying at the sides only (never over the face)
        x0 = r.choice([r.uniform(60, 200), r.uniform(980, 1180)]); y0 = r.uniform(380, 760); c.save(); c.translate(x0, y0); c.rotate(r.uniform(-40, 40)); c.scale(abs(math.sin(k * 1.7)) * .6 + .4, 1); Wd.coin(c, 0, 0, 30); c.restore()
    # headline: "$20 MILLION" orange + "GONE" white, Alfa Slab, thick outline + shadow
    f = skia.Font(F_TITLE, 168); a_, b_ = '$20 MILLION ', 'GONE'; wa = f.measureText(a_); wt = wa + f.measureText(b_); x0 = (W - wt) / 2; y0 = 190
    for txt, col, xx in ((a_, ORANGE, x0), (b_, WHITE, x0 + wa)):
        c.drawString(txt, xx + 12, y0 + 14, f, fp((0, 0, 0), 170, blur=8)); c.drawString(txt, xx, y0, f, ink(30, (10, 17, 36))); c.drawString(txt, xx, y0, f, fp(col))
    img = s.makeImageSnapshot(); img.save(str(path).replace('.jpg', '_1920.png'), skia.kPNG)
    from PIL import Image
    Image.open(str(path).replace('.jpg', '_1920.png')).convert('RGB').resize((1280, 720), Image.LANCZOS).save(path, quality=92)

if __name__ == '__main__':
    thumb(HERE / 'thumb_B_20M_gone.jpg'); print('saved')
