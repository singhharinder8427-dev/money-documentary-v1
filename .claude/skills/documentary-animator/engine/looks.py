"""The two LOCKED looks as image passes (numpy): day print (style A) and night print, plus paper grain.
Characters are never passed through these - they are drawn crisp on top."""
import numpy as np
from PIL import Image as PI, ImageFilter as PF
from engine.core import W, H

def C(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)
def _screen(P=7.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(float); a = np.radians(45)
    u = (xx * np.cos(a) + yy * np.sin(a)) * 2 * np.pi / P; v = (-xx * np.sin(a) + yy * np.cos(a)) * 2 * np.pi / P
    return (np.cos(u) + np.cos(v) + 2) / 4
_SCR = None
def screen():
    global _SCR
    if _SCR is None: _SCR = _screen()
    return _SCR
def _parts(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]; L = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    sat = (a.max(-1) - a.min(-1)) / np.maximum(a.max(-1), 1)
    gold = (r > 170) & (g > 100) & (b < 110) & (sat > .55); orng = (r > 200) & (g < 120) & (b < 60)
    return r, g, b, L, sat, gold, orng

def day_print(a):
    """Locked daytime look: navy ink on cream paper, light navy tint in shade, small soft navy dots, gold spot colour."""
    r, g, b, L, sat, gold, _ = _parts(a); scr = screen()
    t = np.clip((0.86 - L) / 0.62, 0, 1); dots = (np.clip((t - 0.18) / 0.82, 0, 1) * 0.42) > (1 - scr)   # owner: dots subtler
    out = np.where((t > 0.08)[..., None], C('#D6DEEC'), C('#F6EFE2'))
    out = np.where(dots[..., None], C('#8193BC'), out)
    out = np.where((t > 0.82)[..., None], C('#14213D'), out)
    navyfill = (b > r + 18) & (L < 0.42) & (L > 0.08)
    out = np.where(navyfill[..., None], np.where((L > 0.2)[..., None], C('#34497A'), C('#263862')), out)
    out = np.where(gold[..., None], np.where((L > 0.55)[..., None], C('#FCA311'), C('#D68408')), out)
    return out

def night_print(U, Lm):
    """Locked night look. U = the set drawn flat (unlit), Lm = light map 0..1 (lamps, windows)."""
    r, g, b, L, sat, gold, orng = _parts(U); scr = screen()
    navyfill = (b > r + 18) & (L < 0.42) & (L > 0.03)
    ink_px = ((L < 0.14) & (sat < 0.35)) | ((sat < 0.08) & (L < 0.42))     # real ink is near-black grey; dark navy fills are strongly blue
    lines = np.asarray(PI.fromarray((ink_px * 255).astype(np.uint8)).filter(PF.MaxFilter(3)), float) > 0
    Ld = np.clip(L * 1.9, 0, 1)
    t = np.clip((0.92 - Ld) / 0.7, 0, 1); dots = (np.clip((t - 0.15) / 0.85, 0, 1) * 0.42) > (1 - scr)   # owner: dots subtler
    day = np.where((t > 0.1)[..., None], C('#E9E0CC'), C('#F8EDD3')); day = np.where((t > 0.55)[..., None], C('#C9C3B8'), day)
    day = np.where(dots[..., None] & (t > 0.55)[..., None], C('#8193BC'), day)                    # lit areas: dots only in deep shade
    day = np.where(navyfill[..., None], np.where((L > 0.2)[..., None], C('#4A6196'), C('#34497A')), day)
    day = np.where(lines[..., None], C('#14213D'), day)
    step = np.clip(np.floor(np.clip((L - 0.08) / 0.62, 0, 0.999) * 4), 0, 3).astype(int)
    shades = np.array([C('#0D1630'), C('#1B2A52'), C('#2E4374'), C('#4A62A0')])   # brightest step lifted: tables / paper stay readable in the dark
    dk = shades[step]; dk = np.where((dots & (step < 2))[..., None], dk + 6, dk)
    near = np.asarray(PI.fromarray((np.clip(L, 0, 1) * 255).astype(np.uint8)).filter(PF.GaussianBlur(5)), float) / 255
    dk = np.where(lines[..., None], np.where((near > 0.5)[..., None], C('#0D1630'), C('#9FB3DE')), dk)   # ink: dark on light objects, light on dark
    dk = np.where(gold[..., None], C('#B9800F'), dk); day = np.where(gold[..., None], np.where((L > .55)[..., None], C('#FCA311'), C('#D68408')), day)
    dk = np.where(orng[..., None], C('#B8470A'), dk); day = np.where(orng[..., None], C('#F35B04'), day)
    Le = np.clip((Lm - 0.18) / 0.55, 0, 1)                          # weak spill stays dark navy; lamps / windows light up
    lit = Le > (0.12 + 0.55 * scr)                                   # dotted halftone edge where the light fades (vignette feel)
    return np.where(lit[..., None], day, dk)

def grain(rgb, base=232, fine=9, soft=34, seed=5):
    """Paper grain, multiplied. Backgrounds only."""
    r = np.random.default_rng(seed); f = r.normal(0, 1, (H, W))
    s = np.asarray(PI.fromarray((r.random((54, 96)) * 255).astype(np.uint8)).resize((W, H), PI.BICUBIC).filter(PF.GaussianBlur(18)), float) / 255 - .5
    g = np.clip(base + f * fine + s * soft, 0, 255) / 255; return rgb * g[..., None]

# ---------- REAL-COLOUR NIGHT LOOK (owner-locked 22 Nov 2026) ----------
# Every NEW place / office / street / company location / prop scene is made in two steps:
#   1. draw it in flat 2D with its REAL colours (green grass stays green, a company's own colours stay) -
#      simple flat shapes, thin dark outlines, matching the real place (sets_src/real_places.py);
#   2. this pass puts our brand on it: unlit parts go onto our 4 night navies with a hint of the real colour,
#      only real light sources keep full colour, halftone dots in shadows, navy sky with dots + stars,
#      gold lamp heads, company logo colours stay true, dark-navy dotted vignette, paper grain.
REAL_VIGNETTE = 'bottom'      # LOCKED 22 Nov 2026: 'bottom' (dark navy rises from the bottom edge only). 'circle' = round, all edges
def real_night(a, sky=None, pools=(), glows=(), spot_gold=(), keep=(), src_level=.72, src_cols=None, vignette=None):
    """a: HxWx3 float flat drawing in real colours. sky: bool mask of sky pixels (or None).
    pools: [(x, y, radius, strength, squash)] light pools (lamp spill, lobby spill, sign uplight).
    glows: [(x, y, radius)] warm glow around lamp heads. spot_gold: hex colours turned into brand gold (lamp heads).
    keep: hex colours kept exactly (company logo colours, e.g. Nvidia #76B900).
    src_cols: hex colours that ARE light sources (lit windows, screens, bulbs). Use it for rooms with white walls, so walls
    are not mistaken for lights; without it, every pixel brighter than src_level counts as a light source."""
    def near(h, tol): return np.abs(a - C(h)).sum(-1) < tol
    yy, xx = np.mgrid[0:H, 0:W].astype(float); scr = screen()
    sky = np.zeros((H, W), bool) if sky is None else sky
    Lum = a.mean(-1) / 255
    if src_cols is None: src = ((Lum > src_level) & ~sky).astype(float)   # bright real colours = light sources (windows, lobby)
    else:
        src = np.zeros((H, W))
        for h in src_cols: src = np.maximum(src, near(h, 30).astype(float))
    lm = np.asarray(PI.fromarray((np.clip(src, 0, 1) * 255).astype(np.uint8)).filter(PF.GaussianBlur(28)), float) / 255 * 3.0
    for x, y, r, k, sq in pools: lm += np.clip(1 - np.hypot(xx - x, (yy - y) * sq) / r, 0, 1) * k
    lm = np.clip(lm, 0, 1)
    ramp = np.array([C('#0D1630'), C('#1B2A52'), C('#2E4374'), C('#4A62A0')])      # our 4 night navies
    tt = np.clip((Lum - .05) / .8, 0, .999) * 3; i0 = np.floor(tt).astype(int); f = (tt - i0)[..., None]
    dark = (ramp[i0] * (1 - f) + ramp[np.minimum(i0 + 1, 3)] * f) * .8 + a * .2
    k = lm[..., None] ** .8; out = dark * (1 - k) + a * k
    shade = np.clip((.55 - out.mean(-1) / 255) / .45, 0, 1)        # halftone dots in the shadows
    out = np.where(((shade * .38) > (1 - scr))[..., None], out * .78 + C('#2B3F70') * .22 + 10, out)
    sv = np.clip(yy / (H * .42), 0, 1)                               # night sky
    skyc = np.where(((sv ** 1.6) * .6 > (1 - scr))[..., None], C('#1B2A52'), C('#0D1630'))
    rng = np.random.default_rng(3); st = np.zeros((H, W), bool)
    for _ in range(80):
        x, y = rng.integers(0, W), rng.integers(0, int(H * .28)); st[y:y + 2, x:x + 2] = True
    out = np.where(sky[..., None], np.where(st[..., None], C('#9FB3DE'), skyc), out)
    lamp = np.zeros((H, W), bool)
    for h in spot_gold: lamp |= near(h, 20)
    out = np.where(lamp[..., None], C('#FCA311'), out)
    g = np.zeros((H, W))
    for x, y, r in glows: g += np.clip(1 - np.hypot(xx - x, (yy - y) * 1.6) / (r * 2.2), 0, 1) ** 2
    g = np.clip(g, 0, 1)[..., None] * (~lamp)[..., None]; out = out * (1 - g * .55) + C('#FFD27A') * g * .55
    for h in keep: out = np.where(near(h, 12)[..., None], C(h), out)
    if (vignette or REAL_VIGNETTE) == 'bottom':                       # bottom-only: navy rises from the lower edge
        v = np.clip((yy / H - .74) / .26, 0, 1) ** 1.4
    else:                                                            # round: all edges
        d = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)); v = np.clip((d - .72) / .5, 0, 1) ** 1.2
    out = out * (1 - v[..., None] * .9) + C('#0D1630') * (v[..., None] * .9)
    out = np.where((((v * .9) > (1 - scr)) & (v > .08))[..., None], C('#0D1630'), out)
    return np.clip(grain(out, base=240, fine=7, soft=24), 0, 255)
