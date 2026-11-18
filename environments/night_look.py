"""LOCKED night look ("night print"), the night twin of the locked daytime print.
Run: python3 night_look.py [office trading desk street kitchen] -> night1_office.jpg ... night5_kitchen.jpg
Dark areas = navy paper in 4 shades + light-navy ink lines; lamp light reveals the cream/gold print look
(3 tones, small soft navy dots) through a dotted falloff. Locked cast + locked fonts.
Characters are rendered in a separate pass with correct occlusion (things in front of them erase them)."""
import os, sys, numpy as np, skia
from PIL import Image as PI, ImageFilter as PF
import kit
kit.FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts') + '/'
MODE = {'m': 'bg', 'inp': False, 'lights': [], 'glows': [], 'img': None}
_fp, _ink, _sp, _night, _add = kit.fp, kit.ink, kit.sp, kit.night, kit.add_light
def _clear(p, fx=False):
    if MODE['m'] == 'unlit' and fx and not MODE['inp']: p.setAlphaf(0.0); return p   # no glow smudges in the print base
    if MODE['m'] == 'mask' and not MODE['inp']:
        if fx: p.setAlphaf(0.0)                      # glows / blurred shadows never cut characters
        else: p.setBlendMode(skia.BlendMode.kClear)  # solid things in front of a character hide it
    return p
def _fx(a, k, bi, li): return bool((len(a) > bi and a[bi]) or k.get('blur')) or bool((len(a) > li and a[li]) or k.get('blend'))
kit.fp = lambda *a, **k: _clear(_fp(*a, **k), _fx(a, k, 2, 3)); kit.ink = lambda *a, **k: _clear(_ink(*a, **k))
kit.sp = lambda *a, **k: _clear(_sp(*a, **k), _fx(a, k, 2, 1))
def night(c, lights, ambient='#4C5CA0'):
    if MODE['m'] == 'bg': _night(c, lights, ambient)
    elif MODE['m'] == 'unlit': MODE['lights'] = (lights, ambient)
def add_light(c, x, y, r, v, a):
    if MODE['m'] == 'bg': _add(c, x, y, r, v, a)
    elif MODE['m'] == 'unlit': MODE['glows'].append((x, y, r, v, a))
kit.night, kit.add_light = night, add_light
import envs
from kit import W, H, HEAD_CY, head_rrect, draw_char, shape, ink as _i
TF = lambda n: skia.Typeface.MakeFromFile(kit.FD + n)
envs.KAL, envs.MRK, envs.HAND = TF('BarlowCondensed-SemiBold.ttf'), TF('AlfaSlabOne-Regular.ttf'), TF('SpecialElite-Regular.ttf')
_label = kit.label
envs.txt = lambda c, s, x, y, size, color, font=None, align='left', stroke=0, rot=0.0, skew=0, sc=kit.INK: _label(c, s, x, y, size, color, font=font or envs.KAL, align=align, stroke=stroke, stroke_col=sc, skew=0, rot=rot)
envs.night, envs.add_light = night, add_light
FINAL = {
 id(envs.CEO): dict(skin='#F8E2D2', skin_d='#E6C4AE', suit='#14213D', suit_d='#0C152B', shirt='#FFFFFF', tie='#FCA311', hair='silver', hair_col='#ECECF1', glasses=True, moustache=True, moustache_col='#FFFFFF', moustache_outline=True, moustache_dy=10),
 id(envs.ANALYST): dict(skin='#C8875A', skin_d='#A86C43', suit='#E5E5E5', suit_d='#BDBDBD', shirt='#FFFFFF', tie='#14213D', hair='slick', hair_col='#1A1414', glasses=True),
 id(envs.WORKER): dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#6B4A2E', suit_d='#4F3520', shirt='#F4EFE2', tie='#2B4A7A', hair='slick', hair_col='#7A4A26', hat_col='#3A3F4A', hat_band='#FCA311'),
 id(envs.BANKER): dict(skin='#E2B48C', skin_d='#C49468', suit='#2E2E38', suit_d='#1E1E26', shirt='#FFFFFF', tie='#FCA311', bowtie=True, hair='slick', hair_col='#3A2A20', moustache=True, hanky='#FCA311'),
 id(envs.INVESTOR): dict(skin='#8D5A3B', skin_d='#6F4429', suit='#FCA311', suit_d='#D88A06', shirt='#FFFFFF', tie='#14213D', hair=None)}
def person(c, x, y, s, spec, **kw):
    if MODE['m'] != 'mask': return
    MODE['inp'] = True; inv = spec is envs.INVESTOR; sp_ = FINAL[id(spec)]
    kw.pop('light', None); rim = kw.pop('rim', '#9FB8F0')
    hx, hy = x, y + s * HEAD_CY
    if inv:
        p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(hx - 116*s, hy - 106*s, hx + 116*s, hy + 96*s), 40*s, 40*s)); shape(c, p, '#15110F', 5.5)
    draw_char(c, x, y, s, sp_, light=-1, rim=rim, **kw)
    if inv:
        head = skia.Path(); head.addRRect(head_rrect(hx, hy, 100*s)); c.save(); c.clipPath(head, doAntiAlias=True)
        b = skia.Path(); b.moveTo(hx - 110*s, hy - 18*s); b.lineTo(hx - 110*s, hy - 110*s); b.lineTo(hx + 110*s, hy - 110*s); b.lineTo(hx + 110*s, hy - 18*s)
        for i in range(6): b.lineTo(hx + (110 - (i + 0.5) * 36.6) * s, hy - (44 if i % 2 else 30) * s)
        b.close(); c.drawPath(b, kit.fp('#15110F')); c.drawPath(b, kit.ink(5)); c.restore(); c.drawPath(head, kit.ink(5.5))
    MODE['inp'] = False
envs.person = person
def frame_out(surf, path):
    if MODE['m'] == 'bg': kit.finish(surf); kit.vignette(surf.getCanvas(), 0.62)
    MODE['img'] = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).copy()
envs.frame_out = frame_out

def run(fn, mode):
    MODE['m'] = mode; MODE['glows'] = []; getattr(envs, fn)(); return MODE['img']
def grain_arr(rgb):
    r = np.random.default_rng(5); fine = r.normal(0, 1, (H, W))
    soft = np.asarray(PI.fromarray((r.random((54, 96)) * 255).astype(np.uint8)).resize((W, H), PI.BICUBIC).filter(PF.GaussianBlur(18)), float) / 255 - .5
    g = np.clip(232 + fine * 9 + soft * 34, 0, 255) / 255; return rgb * g[..., None]
def over(bg, ch):
    a = ch[..., 3:4].astype(float) / 255; return bg * (1 - a) + ch[..., :3].astype(float) * a  # chars are premultiplied-free RGBA from skia unpremul
def lightmap(lights, ambient, glows):
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.ColorWHITE); _night(c, lights, ambient)
    m = s.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(float).mean(-1) / 255
    amb = np.array(skia.Color4f(kit.hx(ambient)).vec()[:3]).mean(); m = np.clip((m - amb) / (1 - amb), 0, 1)
    s2 = skia.Surface(W, H); c2 = s2.getCanvas(); c2.clear(skia.ColorBLACK)
    for g in glows: _add(c2, *g)
    gm = s2.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(float).mean(-1) / 255
    return np.clip(m + gm * 1.6, 0, 1)
C = lambda h: np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)
def night_print(U, Lm):
    r, g, b = U[..., 0], U[..., 1], U[..., 2]; L = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    sat = (U.max(-1) - U.min(-1)) / np.maximum(U.max(-1), 1)
    gold = (r > 170) & (g > 100) & (b < 110) & (sat > .55); orng = (r > 200) & (g < 120) & (b < 60)
    navyfill = (b > r + 18) & (L < 0.42) & (L > 0.08); lines = np.asarray(PI.fromarray((((L < 0.14) | ((sat < 0.08) & (L < 0.42))) * 255).astype(np.uint8)).filter(PF.MaxFilter(3)), float) > 0
    yy, xx = np.mgrid[0:H, 0:W].astype(float); P = 7.0; a = np.radians(45)
    u = (xx * np.cos(a) + yy * np.sin(a)) * 2 * np.pi / P; v = (-xx * np.sin(a) + yy * np.cos(a)) * 2 * np.pi / P
    scr = (np.cos(u) + np.cos(v) + 2) / 4
    Ld = np.clip(L * 1.9, 0, 1)                                                # night colours are dark: brighten before the day print
    t = np.clip((0.92 - Ld) / 0.7, 0, 1); dots = (np.clip((t - 0.15) / 0.85, 0, 1) * 0.62) > (1 - scr)
    # lit = the locked day print, warmed; objects in 3 tones so desk / floor / wall stay apart; only outlines are dark navy
    day = np.where((t > 0.1)[..., None], C('#E9E0CC'), C('#F8EDD3')); day = np.where((t > 0.55)[..., None], C('#C9C3B8'), day)
    day = np.where(dots[..., None], C('#465C8C'), day)
    day = np.where(navyfill[..., None], np.where((L > 0.2)[..., None], C('#4A6196'), C('#34497A')), day)
    day = np.where(lines[..., None], C('#14213D'), day)
    # dark = navy paper, light-navy ink lines, faint dots
    # dark = navy paper in 4 shades by each object's own brightness (floor, desk, wall stay separate), light-navy ink lines
    step = np.clip(np.floor(np.clip((L - 0.08) / 0.62, 0, 0.999) * 4), 0, 3).astype(int)
    shades = np.array([C('#0D1630'), C('#1B2A52'), C('#2B3F70'), C('#3E5689')])
    dk = shades[step]; dk = np.where((dots & (step < 2))[..., None], dk + 10, dk); dk = np.where(lines[..., None], C('#9FB3DE'), dk)
    dk = np.where(gold[..., None], C('#B9800F'), dk); day = np.where(gold[..., None], np.where((L > .55)[..., None], C('#FCA311'), C('#D68408')), day)
    dk = np.where(orng[..., None], C('#B8470A'), dk); day = np.where(orng[..., None], C('#F35B04'), day)
    Lm2 = np.clip(Lm * 1.35, 0, 1); lit = Lm2 > (0.12 + 0.5 * scr)
    out = np.where(lit[..., None], day, dk)
    return out
if __name__ == '__main__':
    for fn, name in (('office', 'n1_office'), ('trading', 'n2_trading'), ('desk', 'n3_desk'), ('street', 'n4_street'), ('kitchen', 'n5_kitchen')):
        if len(sys.argv) > 1 and fn not in sys.argv[1:]: continue
        ch = run(fn, 'mask'); U = run(fn, 'unlit')[..., :3].astype(float)
        lights, amb = MODE['lights']; MODE['m'] = 'bg'; Lm = lightmap(lights, amb, MODE['glows'])
        out = over(grain_arr(night_print(U, Lm)), ch)
        PI.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(f'night{name[1]}_{name[3:]}.jpg', quality=92); print('done', fn)
