"""REAL PLACES for "The $1.7 Trillion Morning" (24 Nov 2026). Same method as real_places.py (CLAUDE.md 3d): the real place
drawn flat in REAL colours from memory of public photos (fresh shapes, never traced), then looks.real_night brands it.
Sets: nasdaq_tower (Nasdaq MarketSite, Times Square, night), nasdaq_studio (MarketSite studio + opening-bell podium),
openai_hq (OpenAI headquarters, 1515 Third Street, Mission Bay, San Francisco, night).
References: Wikimedia Commons photos (kept outside the repo in D:\\money-documentary-refs\\trillion-morning).
Status: LOCKED by the owner 24 Nov 2026. Company marks from engine/logos.py (rough 2D, real colours)."""
import skia
from engine.core import W, H, F_TITLE, F_LABEL
from engine.sets_src.night_scenes import rect, line, poly, circ, fp, ink, txt
from engine.sets_src.real_places import _night, _pl, LIT, LAMP
from engine import logos

NQ = logos.BRAND['nasdaq'][0]
SKY = ('#2A2F5A', '#363C6E', '#454B80')
BILL = ('#E2574C', '#F2C14E', '#4FA3E0', '#B45FD0', '#F4EFE2')          # Times Square billboards (real, saturated: light sources)

def _sky(c, horizon):
    for k, (y0, y1) in enumerate(((0, horizon * .45), (horizon * .45, horizon * .75), (horizon * .75, horizon))):
        c.drawRect(skia.Rect(0, y0, W, y1 + 1), fp(SKY[k]))

# ---------- 1. Nasdaq MarketSite, Times Square (night): the curved screen tower, billboards, street, crosswalk
def draw_nasdaq_tower(c):
    _sky(c, 760)
    for i, (x0, x1, top) in enumerate(((-20, 330, 120), (330, 600, 260), (1330, 1600, 200), (1600, 1940, 90))):   # side buildings
        rect(c, x0, top, x1, 860, ('#5A5F78', '#4C5068')[i % 2], 5)
        for k in range(3):                                                                                       # stacked billboards
            by = top + 60 + k * 190; rect(c, x0 + 24, by, x1 - 24, by + 150, BILL[(i + k) % len(BILL)], 5, r=6)
            for j in range(3): rect(c, x0 + 50, by + 34 + j * 34, x0 + 50 + (x1 - x0 - 100) * (.4 + .2 * j), by + 50 + j * 34, '#FFFFFF', 0)
    # ref photo (Commons, Nasdaq Tower May 2026): tall blue-glass tower above, a curved dark-navy LED cylinder with big blue
    # text, a black band with the teal 'N' + white 'Nasdaq' wordmark, glass storefront at street level
    rect(c, 560, -10, 1370, 860, '#5E7CA8', 5)                                                                    # glass skyscraper
    for k in range(1, 9): line(c, 560 + k * 90, -10, 560 + k * 90, 860, 2, (40, 60, 95), 170)
    for k in range(1, 14): line(c, 560, k * 64, 1370, k * 64, 2, (40, 60, 95), 120)
    cyl = skia.RRect.MakeRectXY(skia.Rect(660, 150, 1270, 740), 300, 70)
    c.drawRRect(cyl, fp('#1A2366')); c.drawRRect(cyl, ink(6))                                                     # curved LED screen
    for k, (s_, cl) in enumerate((('ANTHROPIC', '#FFFFFF'), ('IS NOW', '#3D7BFF'), ('PUBLIC.', '#3D7BFF'))):
        txt(c, s_, 965, 300 + k * 110, 104, cl, font=F_LABEL, align='center', skew=0)
    rect(c, 660, 640, 1270, 760, '#0B0D12', 5)                                                                    # black band + Nasdaq mark
    logos.nasdaq_n(c, 790, 700, 70); txt(c, 'Nasdaq', 1010, 728, 84, '#FFFFFF', font=F_LABEL, align='center', skew=0)
    rect(c, 660, 760, 1270, 860, '#2A3142', 5)                                                                    # glass storefront
    for k in range(6): rect(c, 680 + k * 98, 776, 760 + k * 98, 852, LIT if k % 2 == 0 else '#4E6A86', 3)
    rect(c, -10, 860, W + 10, 900, '#8A8C98', 4)                                                                  # pavement
    rect(c, -10, 900, W + 10, H + 10, '#3A3D4A', 0)                                                               # street
    for x in range(560, 1380, 90): rect(c, x, 930, x + 54, 1070, '#E8E6DE', 0)                                    # crosswalk
    for lx in (470, 1460): line(c, lx, 640, lx, 868, 8); poly(c, [(lx - 26, 640), (lx + 26, 640), (lx + 16, 616), (lx - 16, 616)], LAMP, 5)
def nasdaq_tower_night():
    return _night([_pl(965, 450, 620, 1.0), _pl(165, 450, 360, .8), _pl(1765, 420, 360, .8), _pl(965, 960, 620, .6), _pl(470, 640, 220, .7), _pl(1460, 640, 220, .7)],
                  glows=[(470, 616, 60), (1460, 616, 60), (965, 330, 260)], sky=SKY, keep=(NQ,) + BILL, src=(LIT, LAMP, NQ) + BILL)

# ---------- 2. Nasdaq MarketSite studio: curved video wall, opening-bell podium (in FRONT of actors), glossy floor
def draw_nasdaq_studio(c):
    c.drawRect(skia.Rect(0, 0, W, H), fp('#1C2236'))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(60, 60, 1860, 640), 60, 60), fp(NQ)); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(60, 60, 1860, 640), 60, 60), ink(6))
    for k in range(1, 9): line(c, 60 + k * 200, 64, 60 + k * 200, 636, 2, (0, 90, 120), 140)
    logos.nasdaq_n(c, 760, 330, 190, '#FFFFFF'); txt(c, 'Nasdaq', 1060, 400, 150, '#FFFFFF', font=F_LABEL, align='center', skew=0)
    rect(c, 60, 560, 1860, 630, '#0B2A3A', 0)                                                                     # ticker band (ambience scrolls on it)
    rect(c, -10, 640, W + 10, 760, '#2C3348', 4); rect(c, -10, 760, W + 10, H + 10, '#6E7690', 0)                  # balcony rail + floor
    for x in range(0, W, 240): line(c, x, 760, x - 160, H, 2, (90, 98, 120), 160)
_PODIUM = (560, 820, 1360, 1080)
def _podium(c):
    l, t, r, b = _PODIUM; rect(c, l, t, r, b, '#2B3145', 6, r=10); rect(c, l, t, r, t + 26, '#C9CEDA', 5); logos.nasdaq(c, 960, 930, 60)
def draw_nasdaq_studio_full(c): draw_nasdaq_studio(c); _podium(c)
def nasdaq_studio_night():
    return _night([_pl(960, 350, 900, 1.0), _pl(960, 880, 700, .7)], glows=[(960, 260, 300)], keep=(NQ,), src=(LIT, LAMP, NQ))

# ---------- 3. OpenAI headquarters, 1515 Third Street, Mission Bay, San Francisco (night)
# ref photo (Commons, '1515 Third Street'): 6-storey glass box in a thin bronze frame, dense bronze/wood vertical fins over
# the glass, glass ground floor, palm trees along the pavement, street-light poles
BRONZE, FIN, GLASS = '#8C6A4E', '#A57B52', '#6C8FB6'
def _palm(c, x, base, h):
    line(c, x, base, x + 10, base - h, 9, (110, 90, 60))
    for a in range(-150, 31, 30):
        import math; r = math.radians(a); ex, ey = x + 10 + math.cos(r) * 110, base - h + math.sin(r) * 60 + 30
        c.drawLine(x + 10, base - h, ex, ey, ink(16, '#3E7A3E')); c.drawLine(x + 10, base - h, ex, ey, ink(3, (30, 60, 30)))
def draw_openai_hq(c):
    _sky(c, 720)
    rect(c, 200, 120, 1720, 800, GLASS, 0)                                                                         # glass box
    for fl in range(6):                                                                                            # floors: some lit inside (night)
        y0 = 130 + fl * 112
        if fl in (1, 3): rect(c, 220, y0 + 8, 1700, y0 + 100, LIT if fl == 3 else '#FFE2A0', 0)
        line(c, 200, y0 + 108, 1720, y0 + 108, 6, (115, 88, 62))
    for x in range(214, 1712, 22): c.drawLine(x, 124, x, 796, ink(7, FIN))                                         # vertical fins
    rect(c, 200, 120, 1720, 800, None, 12, v=BRONZE)                                                               # bronze frame
    rect(c, 200, 800, 1720, 880, '#2A2E36', 5)                                                                     # glass ground floor
    for k in range(10): rect(c, 220 + k * 150, 812, 350 + k * 150, 876, LIT if k in (4, 5) else '#4E6A86', 3)
    rect(c, 600, 742, 1320, 846, '#000000', 5, r=6)                                                                # big entrance sign (owner, 24 Nov)
    logos.openai(c, 690, 794, 40)
    # shortcut: OpenAI's wordmark is a plain sans; Arial (Windows) is the closest font we have, Barlow is the fallback - add a free geometric sans to fonts/ for cloud renders
    sans = skia.Typeface.MakeFromName('Arial', skia.FontStyle.Normal()) or F_LABEL
    c.drawString('OpenAI', 760, 824, skia.Font(sans, 84), fp('#FFFFFF'))
    rect(c, -10, 880, W + 10, 910, '#9A9890', 4); rect(c, -10, 910, W + 10, H + 10, '#3A3D4A', 0)                  # pavement + street
    for x in range(40, W, 260): rect(c, x, 995, x + 120, 1003, '#D8D6CC', 0)
    for px, ph in ((120, 420), (430, 380), (1460, 400), (1640, 450), (1800, 430)): _palm(c, px, 888, ph)
    for lx in (600, 1300): line(c, lx, 600, lx, 888, 7); line(c, lx, 600, lx + 70, 590, 6); poly(c, [(lx + 50, 586), (lx + 96, 586), (lx + 88, 600), (lx + 58, 600)], LAMP, 4)
def openai_hq_night():
    return _night([_pl(960, 540, 700, .8), _pl(960, 840, 500, .9), _pl(680, 600, 200, .7), _pl(1380, 600, 200, .7)],
                  glows=[(673, 600, 50), (1373, 600, 50)], sky=SKY, keep=('#000000', '#FFFFFF'), src=(LIT, '#FFE2A0', LAMP))
