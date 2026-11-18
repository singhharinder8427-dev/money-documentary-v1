"""On-screen graphics in the locked style. Every function draws onto a skia canvas at time u.
Colour rules: gold = money / brand, orange = losses ONLY and always with a minus sign or a down arrow,
gains in navy (on paper) or white (on dark) with an up arrow, never green. Fonts: DSEG counters, Alfa Slab
titles/stamps, Special Elite typed text, Barlow labels."""
import math, random
import skia
from engine.core import W, H, NAVY, NAVY2, NAVY3, BLACK, WHITE, GREY, GOLD, GOLD_D, ORANGE, PAPER, F_COUNTER, F_TITLE, F_TYPE, F_LABEL, F_LABEL2
from engine.kit import fp, ink, hx, rect, circ, poly, shape, pop, back, ease, ease_out, lerp, K, INK

def _font(tf, size): return skia.Font(tf, size)
def text(c, s, x, y, size, color, tf=F_LABEL, align='left', stroke=0, stroke_col=INK, alpha=255):
    f = _font(tf, size); w = f.measureText(s); ox = {'left': 0, 'center': -w / 2, 'right': -w}[align]
    if stroke: c.drawString(s, x + ox, y, f, ink(stroke, stroke_col, alpha))
    c.drawString(s, x + ox, y, f, fp(color, alpha)); return w
def wrap(words, tf, size, maxw):
    f = _font(tf, size); lines, cur = [], []
    for w in words:
        if cur and f.measureText(' '.join(cur + [w])) > maxw: lines.append(cur); cur = [w]
        else: cur.append(w)
    if cur: lines.append(cur)
    return lines

# ---------------- cards (full screen)
def text_card(c, s, u, gold_words=(), bg=BLACK, size=78, color=WHITE):
    """Typed text card: Special Elite, revealed word by word over u 0..1, gold block cursor. Max ~12 words."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(bg)); words = s.split(); lines = wrap(words, F_TYPE, size, 1500)
    n = len(words); shown = int(round(min(max(u, 0), 1) * n)); f = _font(F_TYPE, size); lh = size * 1.35
    y0 = H / 2 - (len(lines) - 1) * lh / 2 + size * .3; k = 0; cx = cy = None
    gw = {g.lower().strip('.,!?') for g in gold_words}
    for i, ln in enumerate(lines):
        x = W / 2 - f.measureText(' '.join(ln)) / 2; y = y0 + i * lh
        for w in ln:
            if k < shown:
                col = GOLD if w.lower().strip('.,!?') in gw else color
                c.drawString(w, x, y, f, fp(col)); cx, cy = x + f.measureText(w) + 10, y
            x += f.measureText(w + ' '); k += 1
    if cx is None: cx, cy = W / 2 - f.measureText(' '.join(lines[0])) / 2, y0
    if (u < 1) or (int(u * 8) % 2 == 0): c.drawRect(skia.Rect(cx, cy - size * .78, cx + size * .45, cy + size * .08), fp(GOLD))

def chapter_card(c, n, title, u):
    """Navy chapter card: 'CHAPTER n' in gold Barlow, title in Alfa Slab popping in, gold rule growing."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(NAVY))
    a = ease(K(u, 0, .25)); text(c, f'CHAPTER {n}', W / 2, 420, 52, GOLD, F_LABEL, 'center', alpha=int(255 * a))
    k = pop(K(u, .08, .35)); c.save(); c.translate(W / 2, 560); c.scale(k, k); text(c, title.upper(), 0, 0, 120, WHITE, F_TITLE, 'center', stroke=0); c.restore()
    wl = 520 * ease_out(K(u, .25, .4)); c.drawRect(skia.Rect(W / 2 - wl, 618, W / 2 + wl, 628), fp(GOLD))

def title_card(c, title, u, gold_word=None, sub=None):
    """Black title card after the hook: Alfa Slab title, one gold word, optional Barlow subtitle."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(BLACK)); k = pop(K(u, 0, .4)); f = _font(F_TITLE, 130)
    words = title.upper().split(); tw = f.measureText(' '.join(words)); c.save(); c.translate(W / 2, H / 2 + 30); c.scale(k, k); x = -tw / 2
    for w in words:
        c.drawString(w, x, 0, f, fp(GOLD if gold_word and w.strip('.,!?') == gold_word.upper() else WHITE)); x += f.measureText(w + ' ')
    c.restore()
    if sub: text(c, sub.upper(), W / 2, H / 2 + 120, 44, GREY, F_LABEL2, 'center', alpha=int(255 * ease(K(u, .3, .3))))

# ---------------- counters
def money_str(v, unit='$', decimals=0):
    s = f'{abs(v):,.{decimals}f}'; return s
def counter(c, x, y, v0, v1, u, unit='$', loss=False, size=96, label=None, panel=True, suffix='', decimals=0):
    """Digital counter (DSEG digits, Barlow $ , and commas). Gold for money; loss=True -> orange with a minus and
    a down arrow. (x, y) = centre of the panel. u 0..1 counts with ease-out."""
    v = lerp(v0, v1, ease_out(min(max(u, 0), 1))); col = ORANGE if loss else GOLD
    groups = money_str(v, unit, decimals).split(','); fd = _font(F_COUNTER, size); fb = _font(F_LABEL, size * 1.12)
    parts = ([('-', fb)] if loss else []) + ([(unit, fb)] if unit else [])
    for i, g in enumerate(groups): parts += [(g, fd)] + ([(',', fb)] if i < len(groups) - 1 else [])
    if suffix: parts.append((suffix, fb))
    gap = size * .06; tw = sum(f.measureText(t) for t, f in parts) + gap * (len(parts) - 1); aw = size * .7 if loss else 0
    if panel:
        pw, ph = tw + aw + size * .9, size * 1.45
        rect(c, x - pw / 2, y - ph / 2, x + pw / 2, y + ph / 2, NAVY, 6, r=14); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - pw / 2 + 8, y - ph / 2 + 8, x + pw / 2 - 8, y + ph / 2 - 8), 10, 10), ink(3, col))
    xx = x - (tw + aw) / 2; yy = y + size * .38
    for t, f in parts: c.drawString(t, xx, yy, f, fp(col)); xx += f.measureText(t) + gap
    if loss: ax = xx + aw * .45; poly(c, [(ax - aw * .35, y - size * .2), (ax + aw * .35, y - size * .2), (ax, y + size * .32)], ORANGE, 0)
    if label: text(c, label.upper(), x, y + size * 1.25, size * .42, WHITE, F_LABEL, 'center')

# ---------------- stamps, labels, tags
def stamp(c, s, x, y, t, color=GOLD, rot=-8, size=110):
    """Stamp slam: t = seconds since the hit. Scale 2.6 -> 1 in 0.2 s. Returns camera shake (dx, dy)."""
    if t < 0: return (0, 0)
    k = lerp(2.6, 1.0, ease_out(min(t / .2, 1))); a = min(t / .08, 1)
    f = _font(F_TITLE, size); tw = f.measureText(s.upper())
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    for inset, w in ((0, 12), (22, 5)):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-tw / 2 - 46 + inset, -size * .78 + inset, tw / 2 + 46 - inset, size * .52 - inset), 18, 18), ink(w, color, int(255 * a)))
    c.drawString(s.upper(), -tw / 2, size * .3, f, fp(color, int(255 * a))); c.restore()
    if t < .35: r = random.Random(int(t * 100)); amp = 14 * (1 - t / .35); return (r.uniform(-amp, amp), r.uniform(-amp, amp))
    return (0, 0)

def pop_label(c, s, x, y, u, color=WHITE, size=66, rot=-4, stroke=14):
    """Barlow label with a thick ink stroke that pops in with overshoot."""
    k = pop(u)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); text(c, s.upper(), 0, 0, size, color, F_LABEL, 'center', stroke=stroke); c.restore()

def lower_third(c, name, role, u, x=90, y=900):
    """Name tag: navy box, gold bar, Barlow name + gold role. Scales in with back()."""
    k = back(min(max(u / .4, 0), 1)); fn, fr = _font(F_LABEL, 62), _font(F_LABEL2, 36)
    w = max(fn.measureText(name.upper()), fr.measureText(role.upper())) + 90
    c.save(); c.translate(x, y); c.scale(k, 1)
    rect(c, 0, 0, w, 130, NAVY, 5, r=8); c.drawRect(skia.Rect(4, 4, 22, 126), fp(GOLD))
    c.drawString(name.upper(), 46, 64, fn, fp(WHITE)); c.drawString(role.upper(), 46, 108, fr, fp(GOLD)); c.restore()

def place_tag(c, place, u, sub=None):
    """Location tag top-left: gold pin + Barlow place name (+ date)."""
    a = int(255 * ease(K(u, 0, .3))); x, y = 80, 120
    circ(c, x, y - 34, 16, GOLD, 4); poly(c, [(x - 12, y - 26), (x + 12, y - 26), (x, y - 2)], GOLD, 0)
    text(c, place.upper(), x + 34, y - 18, 46, WHITE, F_LABEL, stroke=8, alpha=a)
    if sub: text(c, sub.upper(), x + 34, y + 22, 32, GOLD, F_LABEL2, stroke=6, alpha=a)

def sticky(c, s, x, y, u, rot=-5, w=220):
    """Gold-paper sticky note with navy Barlow text."""
    k = pop(u)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    c.drawRect(skia.Rect(-w / 2 + 8, -w / 2 + 12, w / 2 + 8, w / 2 + 12), fp((0, 0, 0), 70, blur=8)); rect(c, -w / 2, -w / 2, w / 2, w / 2, '#FFE2A0', 4)
    lines = wrap(s.upper().split(), F_LABEL, 44, w - 30)
    for i, ln in enumerate(lines): text(c, ' '.join(ln), 0, -len(lines) * 24 + 40 + i * 48, 44, NAVY, F_LABEL, 'center')
    c.restore()

def document(c, x, y, title, lines, u, w=560, h=700, rot=-3, stamp_txt=None, stamp_t=-1):
    """Paper document sliding in; title in Barlow, lines typed in Special Elite (navy on paper)."""
    k = back(min(max(u / .35, 0), 1)); c.save(); c.translate(x, y + (1 - k) * 500); c.rotate(rot)
    c.drawRect(skia.Rect(-w / 2 + 14, -h / 2 + 18, w / 2 + 14, h / 2 + 18), fp((0, 0, 0), 80, blur=12)); rect(c, -w / 2, -h / 2, w / 2, h / 2, PAPER, 5)
    text(c, title.upper(), -w / 2 + 36, -h / 2 + 70, 48, NAVY, F_LABEL); c.drawRect(skia.Rect(-w / 2 + 36, -h / 2 + 92, w / 2 - 36, -h / 2 + 97), fp(NAVY))
    total = sum(len(l) for l in lines); shown = int(max(u - .2, 0) / .8 * total); k2 = 0
    for i, ln in enumerate(lines):
        vis = ln[:max(0, min(len(ln), shown - k2))]; k2 += len(ln)
        text(c, vis, -w / 2 + 36, -h / 2 + 160 + i * 56, 34, NAVY, F_TYPE)
    if stamp_txt and stamp_t >= 0: stamp(c, stamp_txt, w * .12, h * .22, stamp_t, ORANGE if stamp_txt.upper() in ('FRAUD', 'DENIED', 'GUILTY', 'LOSS', 'SCAM') else GOLD, rot=-12, size=80)
    c.restore()

# ---------------- charts
def bar_chart(c, x0, y0, x1, y1, values, labels, u, colors=None, fmt=lambda v: f'${v:,.0f}', dark=True, title=None):
    """Bars grow in one after another. colors: list of GOLD / ORANGE (loss) / NAVY3. Axis + labels in white (dark bg) or navy."""
    tc = WHITE if dark else NAVY; n = len(values); vmax = max(values) or 1; bw = (x1 - x0) / n
    c.drawLine(x0, y1, x1, y1, ink(6, tc))
    if title: text(c, title.upper(), x0, y0 - 30, 50, tc, F_LABEL)
    for i, (v, lb) in enumerate(zip(values, labels)):
        g = ease_out(K(u, i * .12, .45)); h = (y1 - y0 - 70) * v / vmax * g; bx = x0 + i * bw + bw * .18; col = (colors or [GOLD] * n)[i]
        if h > 1: rect(c, bx, y1 - h, bx + bw * .64, y1, col, 5, r=6); c.drawRect(skia.Rect(bx + 10, y1 - h + 10, bx + 22, y1 - 10), fp(WHITE, 60))
        if g > .9: text(c, fmt(v), bx + bw * .32, y1 - h - 18, 40, col if col != NAVY3 else tc, F_LABEL, 'center')
        text(c, lb.upper(), bx + bw * .32, y1 + 48, 36, tc, F_LABEL2, 'center')

def line_chart(c, x0, y0, x1, y1, values, u, color=GOLD, dark=True, labels=None, area=True):
    """Line draws on left to right with a glowing dot at the head. Use ORANGE only for a falling (loss) line."""
    tc = WHITE if dark else NAVY; c.drawLine(x0, y1, x1, y1, ink(5, tc)); c.drawLine(x0, y1, x0, y0, ink(5, tc))
    lo, hi = min(values), max(values); rng = (hi - lo) or 1; n = len(values)
    pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - 30 - (y1 - y0 - 60) * (v - lo) / rng) for i, v in enumerate(values)]
    m = (n - 1) * min(max(u, 0), 1); k = int(m); fr = m - k; vis = pts[:k + 1] + ([(lerp(pts[k][0], pts[k + 1][0], fr), lerp(pts[k][1], pts[k + 1][1], fr))] if k + 1 < n else [])
    if len(vis) < 2: return
    p = skia.Path(); p.moveTo(*vis[0]); [p.lineTo(*q) for q in vis[1:]]
    if area:
        a = skia.Path(p); a.lineTo(vis[-1][0], y1); a.lineTo(vis[0][0], y1); a.close(); c.drawPath(a, fp(NAVY3 if dark else '#D6DEEC', 150))
    c.drawPath(p, ink(16, INK)); c.drawPath(p, ink(9, color)); hx_, hy_ = vis[-1]
    c.drawCircle(hx_, hy_, 26, fp(color, 70, blur=10)); circ(c, hx_, hy_, 11, color, 4)
    if labels:
        for i, lb in enumerate(labels):
            if lb: text(c, lb, pts[i][0], y1 + 44, 34, tc, F_LABEL2, 'center')

# ---------------- money props
def bill(c, x, y, rot=0, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(c, -80, -36, 80, 36, '#F4F1E8', 4); rect(c, -70, -27, 70, 27, None, 2.5, v=NAVY); circ(c, 0, 0, 20, GOLD, 2.5); text(c, '$', 0, 11, 30, NAVY, F_TITLE, 'center'); c.restore()
def coin(c, x, y, r=22): circ(c, x, y, r, GOLD, 3.5); circ(c, x, y, r * .7, None, 2, v='#B07A0A'); text(c, '$', x, y + r * .4, r * 1.05, '#9A6A08', F_TITLE, 'center')
def cash_stack(c, x, y, n=6, s=1.0):
    for i in range(n): bill(c, x + (i % 2) * 4, y - i * 10 * s, 0, s)
def gold_bar(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); poly(c, [(-90, 30), (90, 30), (64, -30), (-64, -30)], GOLD, 5); poly(c, [(-64, -30), (64, -30), (52, -44), (-52, -44)], '#FFD266', 4); c.restore()
def falling_money(c, t, seed=3, n=18, area=(0, 0, W, H)):
    r = random.Random(seed)
    for _ in range(n):
        x0, sp, ph, rot = r.uniform(area[0], area[2]), r.uniform(120, 260), r.uniform(0, 10), r.uniform(-40, 40)
        y = area[1] - 80 + ((t + ph) * sp) % (area[3] - area[1] + 160); x = x0 + math.sin((t + ph) * 2) * 40
        bill(c, x, y, rot + math.sin(t * 3 + ph) * 25, .8)

# ---------------- ending
def polaroid(c, frame, u, caption=None, ring=None):
    """Freeze-frame polaroid ending. frame = skia.Image of the last frame. ring = (x, y, r) in frame coords to circle in gold."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(NAVY)); k = ease_out(K(u, 0, .3)); s = lerp(1.0, .67, k); rot = lerp(0, -4, k)
    c.save(); c.translate(W / 2, H / 2 - 20 * k); c.rotate(rot); c.scale(s, s)
    rect(c, -W / 2 - 40, -H / 2 - 40, W / 2 + 40, H / 2 + 200, '#FBF8F0', 6 / s); c.drawImageRect(frame, skia.Rect(-W / 2, -H / 2, W / 2, H / 2), skia.SamplingOptions())
    if ring and u > .35:
        rx, ry, rr = ring; sw = 360 * ease_out(K(u, .35, .5)); p = skia.Path(); p.addArc(skia.Rect(rx - W / 2 - rr, ry - H / 2 - rr, rx - W / 2 + rr, ry - H / 2 + rr), -100, sw); c.drawPath(p, ink(16 / s, GOLD))
    if caption and u > .5: text(c, caption, 0, H / 2 + 130, 80, NAVY, F_TYPE, 'center')
    c.restore()
    if u < .12: c.drawRect(skia.Rect(0, 0, W, H), fp(WHITE, int(255 * (1 - u / .12))))
