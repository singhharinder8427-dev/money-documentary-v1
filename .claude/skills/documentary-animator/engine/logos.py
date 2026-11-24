"""Rough 2D company marks in each company's real brand colours (CLAUDE.md 3b): simplified shapes drawn fresh in code,
never a traced copy. Used on signs, screens, props and as chest badges on characters (kit spec chest='<company>').
Colours checked 24 Nov 2026 (videos/trillion-morning/sources.md):
  Anthropic  #141413 dark, #FAF9F5 ivory, #D97757 orange (Anthropic brand-guidelines file)
  OpenAI     black / white only (openai.com/brand: no added colours on the Blossom)
  Nasdaq     #0092BC Nasdaq Blue (PMS 313 C, brand-guideline summary)"""
import math, skia
from engine.kit import fp, ink

BRAND = {'anthropic': ('#141413', '#FAF9F5', '#D97757'), 'openai': ('#000000', '#FFFFFF'), 'nasdaq': ('#0092BC', '#FFFFFF')}

def anthropic(c, x, y, r):
    """Dark roundel with a rough ivory 'A' + slash mark."""
    dk, iv, _ = BRAND['anthropic']; c.drawCircle(x, y, r, fp(dk)); w = r * .17; p = ink(w, iv)
    p.setStrokeCap(skia.Paint.kButt_Cap)
    c.drawLine(x - r * .55, y + r * .5, x - r * .12, y - r * .5, p); c.drawLine(x - r * .12, y - r * .5, x + r * .3, y + r * .5, p)
    c.drawLine(x + r * .2, y - r * .5, x + r * .62, y + r * .5, p)

def openai(c, x, y, r):
    """Black roundel with a rough white six-loop 'blossom' knot."""
    dk, wt = BRAND['openai']; c.drawCircle(x, y, r, fp(dk)); p = ink(r * .1, wt)
    for k in range(6):
        c.save(); c.translate(x, y); c.rotate(k * 60)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-r * .18, -r * .62, r * .18, r * .05), r * .18, r * .18), p); c.restore()

def nasdaq_n(c, x, y, h, col=None):
    """The rough Nasdaq 'N' mark (ref: MarketSite tower photo): two slanted parallelogram strokes in Nasdaq Blue, h = height."""
    bl = col or BRAND['nasdaq'][0]; w = h * .32
    for dx, a in ((-h * .3, 170), (h * .12, 255)):
        p = skia.Path(); p.moveTo(x + dx, y + h / 2); p.lineTo(x + dx + w, y + h / 2); p.lineTo(x + dx + w + h * .32, y - h / 2); p.lineTo(x + dx + h * .32, y - h / 2); p.close()
        c.drawPath(p, fp(bl, a))

def nasdaq(c, x, y, r):
    """Black roundel with the rough Nasdaq 'N' mark."""
    c.drawCircle(x, y, r, fp('#0B0D12')); nasdaq_n(c, x - r * .05, y, r * 1.1)

MARKS = {'anthropic': anthropic, 'openai': openai, 'nasdaq': nasdaq}

def badge(c, name, x, y, r=15):
    """Chest badge: the company mark with a thin white rim (reads on dark jackets)."""
    c.drawCircle(x, y, r + 2.5, fp('#F4EFE2')); MARKS[name](c, x, y, r)

if __name__ == '__main__':
    s = skia.Surface(200, 60); cv = s.getCanvas()
    for i, n in enumerate(MARKS): badge(cv, n, 30 + i * 70, 30, 22)
    assert s.makeImageSnapshot().toarray()[..., 3].sum() > 0; print('logos self-check ok:', ', '.join(MARKS))
