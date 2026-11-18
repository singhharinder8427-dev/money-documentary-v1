"""LOCKED daytime look (style A, printed illustration). Run: python3 print_look.py [scene ...]
Scenes: living_room kitchen bank street lesson -> day1_living.png ... day5_lesson.png.
Our own daytime look: the world is a 2-colour print (navy ink on cream paper, navy halftone dots for shade,
gold as the only spot colour). Characters stay full-colour and glossy on top. Runs the same scenes as day_envs."""
import numpy as np, skia, day_envs as D
NAVY = np.array([20, 33, 61], float); PAPER = np.array([246, 239, 226], float); TINT = np.array([214, 222, 236], float); DOT = np.array([70, 92, 140], float)

def to_print(surf):
    img = surf.makeImageSnapshot()
    arr = img.toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(float)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    L = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    mx, mn = arr.max(-1), arr.min(-1); sat = (mx - mn) / np.maximum(mx, 1)
    gold = (r > 180) & (g > 110) & (b < 110) & (sat > .55)               # gold spot colour survives
    t = np.clip((0.86 - L) / 0.62, 0, 1)                                 # 0 = paper, 1 = solid ink
    H, W = L.shape; yy, xx = np.mgrid[0:H, 0:W].astype(float); P = 7.0; ang = np.radians(45)
    u = (xx * np.cos(ang) + yy * np.sin(ang)) * 2 * np.pi / P; v = (-xx * np.sin(ang) + yy * np.cos(ang)) * 2 * np.pi / P
    screen = (np.cos(u) + np.cos(v) + 2) / 4                             # 0..1 dot screen
    t2 = np.clip((t - 0.18) / 0.82, 0, 1) * 0.62; ink = t2 > (1 - screen)          # smaller, lighter dots
    base = np.where((t > 0.08)[..., None], TINT, PAPER)                  # light tint under shaded areas
    out = np.where(ink[..., None], DOT, base)
    out = np.where((t > 0.82)[..., None], NAVY, out)                     # solid ink lines / darks
    navyfill = (b > r + 18) & (L < 0.42) & (L > 0.08)                   # navy objects keep their shape: solid mid-navy
    out = np.where(navyfill[..., None], np.where((L > 0.2)[..., None], np.array([52, 74, 122], float), np.array([38, 56, 98], float)), out)
    gold_col = np.where((L > 0.55)[..., None], np.array([252, 163, 17], float), np.array([214, 132, 8], float))
    out = np.where(gold[..., None], gold_col, out)
    o = np.dstack([out.astype(np.uint8), np.full((H, W), 255, np.uint8)])
    c = surf.getCanvas(); c.clear(skia.ColorWHITE); c.drawImage(skia.Image.fromarray(o, colorType=skia.kRGBA_8888_ColorType), 0, 0)
    D.grain(c); return c

D.finish_bg = to_print
import sys
for n in (sys.argv[1:] or ['living_room', 'kitchen', 'bank', 'street', 'lesson']):
    getattr(D, n)()
