"""Living backgrounds (owner, 24 Nov 2026): small moving details drawn every frame ON the set, BEHIND the actors,
so the baked set pictures stop looking frozen. Brand palette only (navy / gold / white; orange only for losses).
Effects run on the ABSOLUTE video clock, so motion carries on across cuts (one continuous film).

Opt-in: old videos render exactly as before. A new video calls `ambience.enable()` in its shots.py.
Per set: AMBIENCE[set_name] = [(effect_name, {params}), ...]; or pass extra layers per shot with shots.wide(..., amb=[...]).
Every effect is fx(c, t, **params) in 1920x1080 world space; randomness is a fixed hash, so frames are repeatable."""
import math, skia
from engine.core import W, H, GOLD, ORANGE, WHITE, F_LABEL
from engine.kit import fp, ink, sp, radial, col

ENABLED = False
def enable(on=True):
    global ENABLED; ENABLED = on

def _r(i, k=0):                      # fixed pseudo-random 0..1 for item i, channel k
    v = math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return v - math.floor(v)
def _glow(c, x, y, r, v, a):
    c.drawCircle(x, y, r, sp(radial(x, y, r, [col(v, a), col(v, a * .35), col(v, 0)], [0, .45, 1]), blend=skia.BlendMode.kPlus))
def _clip(c, rect):
    c.save()
    if rect: c.clipRect(skia.Rect(*rect))

NIGHT_INK = '#0D1630'                # darkest night navy (BRAND.md), silhouettes and birds

# ---------------------------------------------------------------- people
def silhouettes(c, t, y, x0=0, x1=W, n=5, s=1.0, speed=55, clip=None, v=NIGHT_INK, a=200, glass=0):
    """People walking past: behind a glass wall (clip=(l,t,r,b), glass=0..1 frosts them) or along a street.
    y = feet line, s = scale (1.0 ~ 170 px tall). Some carry a briefcase, some look at a glowing phone."""
    _clip(c, clip); span = x1 - x0 + 200 * s
    for i in range(n):
        d = 1 if _r(i) > .45 else -1; sp_ = speed * (.75 + .5 * _r(i, 1)) * s
        x = x0 - 100 * s + ((_r(i, 2) * span + d * sp_ * t) % span); ss = s * (.88 + .22 * _r(i, 3))
        ph = t * sp_ / (38 * ss) + _r(i, 4) * 6; sw = math.sin(ph) * 14 * ss; al = a * (1 - .55 * glass)
        p, k = fp(v, al), ink(9 * ss, v, al)
        c.drawLine(x, y - 70 * ss, x + sw, y, k); c.drawLine(x, y - 70 * ss, x - sw, y, k)           # legs
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 20 * ss, y - 142 * ss, x + 20 * ss, y - 62 * ss), 10 * ss, 10 * ss), p)
        c.drawCircle(x, y - 158 * ss, 15 * ss, p)                                                       # head
        kind = int(_r(i, 5) * 3)
        if kind == 0:                                                                                   # briefcase
            c.drawLine(x, y - 128 * ss, x - d * sw * .6, y - 78 * ss, ink(6 * ss, v, al))
            c.drawRect(skia.Rect(x - d * sw * .6 - 14 * ss, y - 82 * ss, x - d * sw * .6 + 14 * ss, y - 60 * ss), p)
        elif kind == 1:                                                                                 # phone glow at the face
            _glow(c, x + d * 16 * ss, y - 140 * ss, 22 * ss, '#FFD27A', 70 * (1 - .5 * glass))
            c.drawLine(x, y - 128 * ss, x + d * 16 * ss, y - 140 * ss, ink(6 * ss, v, al))
        else: c.drawLine(x, y - 128 * ss, x - sw * .7, y - 80 * ss, ink(6 * ss, v, al))                 # swinging arm
    if glass:                                                                                           # frosted-glass sheen
        c.drawRect(skia.Rect(*clip) if clip else skia.Rect(0, 0, W, H), fp('#9FB3DE', 26 * glass))
    c.restore()

# ---------------------------------------------------------------- sky
def birds(c, t, y=180, n=5, period=16, s=1.0, v=NIGHT_INK, d=1):
    """A small flock crosses the sky once per period (flapping V shapes)."""
    u = (t % period) / period; base = -200 + u * (W + 400)
    for i in range(n):
        x = base - i * 55 * s * (1 + _r(i)) if d > 0 else W - (base - i * 55 * s * (1 + _r(i)))
        yy = y + (_r(i, 1) - .5) * 60 * s + math.sin(t * 1.3 + i) * 6; f = math.sin(t * 9 + i * 1.7) * 9 * s
        p = skia.Path(); p.moveTo(x - 16 * s, yy - f); p.quadTo(x - 7 * s, yy - 4 * s, x, yy); p.quadTo(x + 7 * s, yy - 4 * s, x + 16 * s, yy - f)
        c.drawPath(p, ink(3.2 * s, v, 230))

def clouds(c, t, y=160, n=3, speed=7, v='#1B2A52', a=150, s=1.0):
    """Slow clouds drifting across a night sky (in front of the moon / skyline)."""
    span = W + 700 * s
    for i in range(n):
        x = -350 * s + ((_r(i) * span + speed * t * (.7 + .6 * _r(i, 1))) % span); yy = y + _r(i, 2) * 120
        for j in range(5): c.drawCircle(x + (j - 2) * 55 * s, yy - (25 if j in (1, 3) else 45 if j == 2 else 0) * s, (48 + 14 * (j == 2)) * s, fp(v, a))

def stars(c, t, region=(0, 0, W, 320), n=26, v='#9FB3DE'):
    """Twinkling stars (the real-night look already has a few; this makes them breathe)."""
    l, tp, r, b = region
    for i in range(n):
        x, y = l + _r(i) * (r - l), tp + _r(i, 1) * (b - tp); k = .5 + .5 * math.sin(t * (1.2 + 2 * _r(i, 2)) + i)
        c.drawCircle(x, y, 1.4 + 1.2 * k, fp(v, 90 + 150 * k))

def plane(c, t, y=120, period=45, s=1.0):
    """A distant plane: dark body + blinking white / gold lights, crossing once per period."""
    u = (t % period) / period; x = -120 + u * (W + 240)
    c.drawLine(x - 30 * s, y, x + 30 * s, y - 4 * s, ink(5 * s, NIGHT_INK)); c.drawLine(x - 6 * s, y - 2 * s, x - 18 * s, y + 10 * s, ink(4 * s, NIGHT_INK))
    if (t * 1.3) % 1 < .15: _glow(c, x + 30 * s, y - 4 * s, 14 * s, WHITE, 200)
    if (t * 1.3 + .5) % 1 < .15: _glow(c, x - 30 * s, y, 12 * s, GOLD, 200)

def rain(c, t, a=60, n=140, region=(0, 0, W, H)):
    l, tp, r, b = region; h = b - tp
    for i in range(n):
        x = l + _r(i) * (r - l); y = tp + ((_r(i, 1) * h + t * (900 + 300 * _r(i, 2))) % h)
        c.drawLine(x, y, x - 8, y + 26, ink(1.6, '#9FB3DE', a))

# ---------------------------------------------------------------- street
def cars(c, t, y, n=3, period=8, d=1, s=1.0):
    """Cars driving along a street lane: dark body + cabin, headlights at the front and a light pool on the road
    (no taillights: orange = losses only). y = road line under the wheels."""
    for i in range(n):
        u = ((t + _r(i) * period) % period) / period; x = -260 * s + u * (W + 520 * s)
        if d < 0: x = W - x
        body = skia.RRect.MakeRectXY(skia.Rect(x - 110 * s, y - 52 * s, x + 110 * s, y - 12 * s), 14 * s, 14 * s)
        cab = skia.RRect.MakeRectXY(skia.Rect(x - 62 * s, y - 86 * s, x + 50 * s, y - 46 * s), 16 * s, 16 * s)
        c.drawRRect(cab, fp('#1B2A52')); c.drawRRect(body, fp('#1B2A52')); c.drawRRect(cab, ink(3, NIGHT_INK)); c.drawRRect(body, ink(3, NIGHT_INK))
        for wx in (-62, 62): c.drawCircle(x + wx * s, y - 10 * s, 17 * s, fp(NIGHT_INK))
        _glow(c, x + d * 106 * s, y - 36 * s, 30 * s, '#FFD27A', 230)
        _glow(c, x + d * 230 * s, y - 4 * s, 150 * s, '#FFD27A', 40)

def window_lights(c, t, rects, period=12):
    """Office / apartment windows switching on and off (warm gold), each on its own slow rhythm."""
    for i, (l, tp, r, b) in enumerate(rects):
        on = math.sin(t * 2 * math.pi / (period * (.6 + _r(i))) + _r(i, 1) * 6) > .2
        if on: c.drawRect(skia.Rect(l, tp, r, b), fp('#FFD27A', 120)); _glow(c, (l + r) / 2, (tp + b) / 2, max(r - l, b - tp), '#FFD27A', 30)

def moths(c, t, x, y, n=4, r=34):
    for i in range(n):
        a_ = t * (2.5 + _r(i) * 2) + i * 1.7; c.drawCircle(x + math.cos(a_) * r * (.6 + .5 * _r(i, 1)), y + math.sin(a_ * 1.3) * r * .6, 2.2, fp('#F8EDD3', 200))

def flag(c, t, x, y, w=120, h=70, colors=('#9FB3DE',)):
    """A waving cloth on a pole (pass real flag colours for national flags only)."""
    c.drawLine(x, y, x, y + h * 2.6, ink(5, NIGHT_INK)); p = skia.Path(); p.moveTo(x, y)
    for k in range(11): u = k / 10; p.lineTo(x + u * w, y + math.sin(t * 4 - u * 5) * 8 * u)
    for k in range(10, -1, -1): u = k / 10; p.lineTo(x + u * w, y + h + math.sin(t * 4 - u * 5) * 8 * u)
    p.close(); c.drawPath(p, fp(colors[0], 230)); c.drawPath(p, ink(3, NIGHT_INK))

# ---------------------------------------------------------------- offices and rooms
def screen(c, t, rect, kind='chart', v=GOLD, bg=None):
    """A live screen: 'chart' (line drawing on, scrolling), 'code' (scrolling lines), 'mail' (rows sliding in).
    bg = fill the screen first (hides a static picture already painted in the set)."""
    l, tp, r, b = rect; w, h = r - l, b - tp; _clip(c, rect)
    if bg: c.drawRect(skia.Rect(*rect), fp(bg))
    if kind == 'chart':
        p = skia.Path(); off = t * 40
        for k in range(41):
            xx = l + k / 40 * w; yy = tp + h * (.55 - .25 * math.sin((xx + off) / w * 7) * .8 - .2 * math.sin((xx + off) / w * 17) * .5)
            p.moveTo(xx, yy) if k == 0 else p.lineTo(xx, yy)
        c.drawPath(p, ink(max(2, h / 40), v, 230)); c.drawCircle(r - 4, yy, max(3, h / 30), fp(v))
    else:
        rows = 8; rh = h / rows; sc = (t * (14 if kind == 'code' else 6)) % rh
        for k in range(rows + 1):
            yy = tp + k * rh - sc; ww = w * (.3 + .6 * _r(k + int(t * (14 if kind == 'code' else 6) // rh)))
            c.drawRect(skia.Rect(l + w * .06, yy + rh * .3, l + w * .06 + ww * .85, yy + rh * .62), fp('#9FB3DE' if kind == 'code' else WHITE, 150))
    c.restore()

def ticker(c, t, rect, items=(('ANT', '+17%'), ('NVDA', '+2.1%'), ('S&P 500', '+0.4%')), speed=120, down=()):
    """Scrolling stock ticker strip. Names in `down` are shown in orange with a down arrow (losses only)."""
    l, tp, r, b = rect; h = b - tp; _clip(c, rect); c.drawRect(skia.Rect(*rect), fp('#0D1630', 230))
    f = skia.Font(F_LABEL, h * .62); seg = [(f'{a} {v}', a in down, ORANGE if a in down else (GOLD if i % 2 == 0 else WHITE)) for i, (a, v) in enumerate(items)]
    widths = [f.measureText(s_) + h * 1.9 for s_, _, _ in seg]; total = sum(widths); x = l - (t * speed) % total; a_ = h * .2
    while x < r:
        for (s_, dn, cl), wd in zip(seg, widths):
            c.drawString(s_, x, tp + h * .74, f, fp(cl)); ax = x + f.measureText(s_) + h * .4; ay = tp + h * .5; p = skia.Path()   # arrow drawn as a shape (font has no arrow glyph)
            if dn: p.moveTo(ax - a_, ay - a_); p.lineTo(ax + a_, ay - a_); p.lineTo(ax, ay + a_)
            else: p.moveTo(ax - a_, ay + a_); p.lineTo(ax + a_, ay + a_); p.lineTo(ax, ay - a_)
            p.close(); c.drawPath(p, fp(cl)); x += wd
    c.restore()

def clock(c, t, x, y, r, v=NIGHT_INK):
    """Clock hands moving over a clock face that is already in the set (minute hand visibly turns)."""
    for ang, ln, w in ((t * 6 * 2, r * .78, r * .07), (t * .5 * 2, r * .5, r * .1)):
        a_ = math.radians(ang - 90); c.drawLine(x, y, x + math.cos(a_) * ln, y + math.sin(a_) * ln, ink(w, v))
    c.drawCircle(x, y, r * .08, fp(GOLD))

def steam(c, t, x, y, s=1.0):
    """Coffee steam: three wavy wisps rising and fading."""
    for i in range(3):
        u = ((t * .5 + i / 3) % 1); p = skia.Path(); yy = y - u * 70 * s
        p.moveTo(x + (i - 1) * 10 * s, yy)
        for k in range(1, 6): p.lineTo(x + (i - 1) * 10 * s + math.sin(t * 3 + k + i) * 6 * s, yy - k * 9 * s)
        c.drawPath(p, ink(3 * s, '#F8EDD3', 110 * (1 - u)))

def blinds(c, t, rect, n=6, a=26):
    """Slatted window light drifting slowly across a wall (the sun / street light through blinds)."""
    l, tp, r, b = rect; _clip(c, rect); dx = (t * 6) % ((r - l) / 2)
    for k in range(n):
        yy = tp + k * (b - tp) / n
        c.drawRect(skia.Rect(l + dx, yy, l + dx + (r - l) * .5, yy + (b - tp) / n * .45), fp('#FFD27A', a, blend=skia.BlendMode.kPlus))
    c.restore()

def phone_blink(c, t, x, y, period=3.0):
    if (t % period) < .5: _glow(c, x, y, 26, '#FFD27A', 180 * math.sin((t % period) / .5 * math.pi))

def papers(c, t, n=6, region=(0, 0, W, H), period=6):
    """Loose papers fluttering down (trading floor, newsroom chaos)."""
    l, tp, r, b = region
    for i in range(n):
        u = ((t + _r(i) * period) % period) / period; x = l + _r(i, 1) * (r - l) + math.sin(t * 2 + i) * 40; y = tp + u * (b - tp)
        c.save(); c.translate(x, y); c.rotate(math.sin(t * 3 + i) * 35); c.drawRect(skia.Rect(-22, -15, 22, 15), fp('#F8EDD3', 220)); c.drawRect(skia.Rect(-22, -15, 22, 15), ink(2, NIGHT_INK, 160)); c.restore()

# ---------------------------------------------------------------- data centre
def leds(c, t, rect, cols=6, rows=10):
    l, tp, r, b = rect
    for i in range(cols * rows):
        x = l + (i % cols + .5) * (r - l) / cols; y = tp + (i // cols + .5) * (b - tp) / rows
        if math.sin(t * (2 + 5 * _r(i)) + i * 3) > .3: c.drawCircle(x, y, 3, fp(GOLD if _r(i, 1) > .3 else WHITE))

def fan(c, t, x, y, r, v=NIGHT_INK):
    c.save(); c.translate(x, y); c.rotate(t * 400)
    for k in range(4): c.rotate(90); c.drawOval(skia.Rect(-r * .18, -r, r * .18, 0), fp(v, 200))
    c.restore()

# ---------------------------------------------------------------- mood
def dust(c, t, rect, n=24):
    """Dust floating in a light beam (tension, quiet rooms)."""
    l, tp, r, b = rect
    for i in range(n):
        x = l + ((_r(i) * (r - l) + t * 8 * (_r(i, 1) - .5)) % (r - l)); y = tp + ((_r(i, 2) * (b - tp) - t * 6 * _r(i, 3)) % (b - tp))
        c.drawCircle(x, y, 1.6 + _r(i, 4), fp('#F8EDD3', 80 + 80 * math.sin(t * 2 + i) ** 2))

def flashes(c, t, region=(0, 300, W, 900), rate=1.6):
    """Press / camera flashes popping in a crowd."""
    l, tp, r, b = region; k = int(t * rate); u = t * rate - k
    if u < .12: _glow(c, l + _r(k) * (r - l), tp + _r(k, 1) * (b - tp), 90, WHITE, 230 * (1 - u / .12))

def gold_dust(c, t, n=40, region=(0, 0, W, H)):
    """Gold flakes / confetti falling (big money moments: the bell, the payday)."""
    l, tp, r, b = region
    for i in range(n):
        y = tp + ((_r(i) * (b - tp) + t * (60 + 60 * _r(i, 1))) % (b - tp)); x = l + _r(i, 2) * (r - l) + math.sin(t * 2 + i) * 25
        c.save(); c.translate(x, y); c.rotate(t * 200 * (_r(i, 3) - .5)); c.scale(1, abs(math.sin(t * 4 + i)) + .15)
        c.drawRect(skia.Rect(-7, -4, 7, 4), fp(GOLD if i % 3 else WHITE, 220)); c.restore()

def loss_flicker(c, t, a=40):
    """A slow orange pulse over the whole frame for loss moments (orange = losses only)."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(ORANGE, a * (.5 + .5 * math.sin(t * 4)), blend=skia.BlendMode.kPlus))

FX = {f.__name__: f for f in (silhouettes, birds, clouds, stars, plane, rain, cars, window_lights, moths, flag, screen, ticker,
                              clock, steam, blinds, phone_blink, papers, leds, fan, dust, flashes, gold_dust, loss_flicker)}

# set name -> layers drawn automatically whenever that set is used (filled per set, after the owner approves each one)
AMBIENCE = {}

def draw(c, t, set_name=None, extra=()):
    """Draw the set's ambience layers + any per-shot extras. No-op unless enable() was called."""
    if not ENABLED: return
    for name, kw in list(AMBIENCE.get(set_name, ())) + list(extra):
        kw = dict(kw); within = kw.pop('within', None)          # within=(l,t,r,b): keep the effect inside a window / frame
        _clip(c, within); FX[name](c, t, **kw); c.restore()

if __name__ == '__main__':          # self-check: every effect draws at a few times without error, and stays repeatable
    s = skia.Surface(W, H); cv = s.getCanvas(); enable()
    demo = {'silhouettes': dict(y=900, clip=(200, 300, 1700, 950), glass=.6), 'screen': dict(rect=(100, 100, 500, 350)), 'ticker': dict(rect=(0, 0, W, 60), down=('NVDA',)),
            'clock': dict(x=300, y=300, r=60), 'steam': dict(x=500, y=600), 'blinds': dict(rect=(0, 0, 900, 600)), 'phone_blink': dict(x=10, y=10),
            'cars': dict(y=900), 'window_lights': dict(rects=[(10, 10, 60, 60)]), 'moths': dict(x=400, y=300), 'flag': dict(x=100, y=100),
            'leds': dict(rect=(0, 0, 300, 600)), 'fan': dict(x=200, y=200, r=50), 'dust': dict(rect=(0, 0, 600, 600))}
    def frame(tt):
        cv.clear(skia.ColorBLACK)
        for nm, f in FX.items(): f(cv, tt, **demo.get(nm, {}))
        return s.makeImageSnapshot().toarray()
    a, b, other = frame(1.7), frame(1.7), frame(33.3)
    assert (a == b).all() and a.sum() > 0 and (a != other).any(); print('ambience self-check ok:', len(FX), 'effects, repeatable, animated')
