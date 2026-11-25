"""Shot list - "The $1.7 Trillion Morning That Left OpenAI Behind" (~4.5 min, NO end screen, NO wallet chapter).
Follows shot_plan.md (69 pictures). Only LOCKED assets (ASSET_LIBRARY.md): cast dario / daniela / altman / trader2 + roles,
sets night/nasdaq_tower / nasdaq_studio / openai_hq + library sets, props_ipo, logos, ambience, widgets.chapter_fade.
Owner rules for this video: one continuous film - chapter changes are widgets.chapter_fade OVER the moving first scene of the
chapter (never a black card); the title fades in over the moving Nasdaq tower; every set runs its living background;
subscribe ending (n055) runs to the last frame. Real people (Dario, Daniela, Altman) never speak: mouths flat.
No REPORTED stamps (owner 24 Nov); "reportedly" lives in the narration + a small attribution label.
QA: make_video.py qa (3 frames per shot) before any render (CLAUDE.md 4b). Sounds are added after the owner approves the shots."""
import math, random, skia, json as _json, pathlib as _pl
from engine import shots, widgets as Wd, anim as A, kit, props, props_dc as PD, props_ipo as P, logos, ambience
from engine.actor import Actor
from engine.core import W, H, GOLD, ORANGE, WHITE, NAVY, NAVY2, PAPER, F_LABEL, F_TYPE, F_TITLE
from engine.kit import rect, fp, ease, ease_out, K, lerp, circ, poly

_SCRIPT = _json.load(open(_pl.Path(__file__).resolve().parent / 'script.json'))
SHOT_BREAKS = tuple(l['id'] for l in _SCRIPT['lines'])          # every line starts its own picture
NR = '#9FB8F0'                                                  # night rim light
INKN = ambience.NIGHT_INK
AN_DK, AN_IV = logos.BRAND['anthropic'][:2]                      # Anthropic dark / ivory (rule 3b)
SOFT = '#9DB0DA'

# ---------- living backgrounds, placed once per set (ambience_preview.py / assets_preview.py) ----------
ambience.enable()
ambience.AMBIENCE.update({
    'night/nasdaq_tower': [('birds', dict(y=60, n=5, period=8)), ('flashes', dict(region=(0, 700, 1920, 880), rate=2)),
                           ('silhouettes', dict(y=880, n=8, s=.62, speed=60)), ('cars', dict(y=1010, n=2, period=6, s=.9))],
    'night/nasdaq_studio': [('ticker', dict(rect=(60, 562, 1860, 628), items=(('NVDA', '+0.8%'), ('MSFT', '+0.3%'), ('S&P 500', '+0.2%')))),
                            ('flashes', dict(region=(200, 650, 1720, 760)))],
    'night/openai_hq': [('clouds', dict(y=60, n=3, speed=10, a=110)), ('birds', dict(y=90, n=4, period=9)),
                        ('window_lights', dict(rects=[(387, 282, 487, 370), (1560, 506, 1660, 594), (1450, 618, 1550, 706)], period=6)),
                        ('silhouettes', dict(y=880, n=4, s=.6, speed=50)), ('cars', dict(y=1010, n=2, period=7, d=-1, s=.9))],
    'night/trading': [('ticker', dict(rect=(40, 196, 1880, 258), items=(('NVDA', '+0.8%'), ('MSFT', '+0.3%'), ('AAPL', '+0.5%'), ('S&P 500', '+0.2%')))),
                      ('papers', dict(n=5))],
    'night/megaspeed': [('birds', dict(y=260, n=4, period=9, s=.7, within=(90, 120, 620, 530))), ('plane', dict(y=200, period=14, s=.8, within=(90, 120, 620, 530))),
                        ('screen', dict(rect=(700, 150, 1220, 325), kind='chart', bg='#14213D'))],
    'night/private_banker': [('clock', dict(x=759, y=213, r=58))],
    'night/newsroom': [('screen', dict(rect=(160, 110, 414, 272), kind='chart', v=WHITE)), ('screen', dict(rect=(760, 310, 1016, 476), kind='chart', v=WHITE))],
    'night/desk_clean': [('dust', dict(rect=(1000, 480, 1900, 1060), n=18))],
    'night/office': [('dust', dict(rect=(1000, 560, 1500, 900), n=14))],
    'night/bank_vault': [('dust', dict(rect=(1100, 560, 1600, 1000), n=14))],
    'night/datacenter': [('dust', dict(rect=(700, 240, 1220, 800), n=20))],
})

def build(tl):
    S = []; at = tl.at; mouths = tl.mouths()
    order = [l['id'] for l in tl.lines]
    def mk(ev): return f"chapter:{ev['n']}" if ev['kind'] == 'chapter' else ev['kind']
    def nxt(lid):
        i = order.index(lid); cands = [e for e in tl.events if e['t0'] > tl.start(lid) + .01]
        nl = order[i + 1] if i + 1 < len(order) else None
        ev = min(cands, key=lambda e: e['t0']) if cands else None
        if ev and (nl is None or ev['t0'] < at(nl)): return mk(ev)
        return nl
    def add(lid, draw, **kw): S.append(dict(name=lid, dur=tl.dur(lid, nxt(lid)), draw=draw, **kw))
    def multi(lid, parts):
        """One line, several pictures: parts = [(fraction, mk), ...]; mk(t0) -> dict(draw=..., **shot kwargs)."""
        d = tl.dur(lid, nxt(lid)); t = at(lid); tot = sum(f for f, _ in parts)
        for i, (f, m) in enumerate(parts):
            dd = d * f / tot; S.append(dict(name=lid if i == 0 else f'{lid}_{i + 1}', dur=dd, **m(t))); t += dd
    def nxt_ev(marker):
        t0 = at(marker); later = [l for l in order if at(l) > t0 + .01]; ev = [e for e in tl.events if e['t0'] > t0 + .01]
        c1 = at(later[0]) if later else 1e9; c2 = min((e['t0'] for e in ev), default=1e9)
        if c2 < c1: return mk(min(ev, key=lambda e: e['t0']))
        return later[0] if later else 'end'
    def fade_in(n, title, draw, **kw):
        """Chapter change (owner 24 Nov): the chapter's first scene is already moving, the chapter_fade card dims over it."""
        m = f'chapter:{n}'; d = tl.dur(m, nxt_ev(m)); hud0 = kw.pop('hud', None)
        def hud(c, t):
            if hud0: hud0(c, t)
            Wd.chapter_fade(c, n, title, t / d)
        S.append(dict(name=f'chapter{n}', dur=d, draw=draw, hud=hud, **kw))
    def say(a, lid): return a.say(tl, lid, mouths)
    D = lambda lid: tl.dur(lid, nxt(lid))
    shake = lambda hit: A.stamp_shake(hit)
    plain = shots.plain
    HUDPOP = lambda txt, x, y, t0, col=GOLD, size=96, rot=-4: (lambda c, t: Wd.pop_label(c, txt, x, y, (t - t0) / .4, col, size, rot=rot))
    LT = lambda name, role, t0=.3, **kw: (lambda c, t: Wd.lower_third(c, name, role, (t - t0) / .5, **kw))
    PT = lambda place, sub=None, t0=.2: (lambda c, t: Wd.place_tag(c, place, (t - t0) / .4, sub))
    def both(*fs): return lambda c, t: [f(c, t) for f in fs if f]
    def desk(overlay): return shots.desk(overlay, 'night/desk_clean')
    def wide(set_name, back=(), front=(), overlay=None, t0=0.0, amb=()): return shots.wide(set_name, back, front, overlay=overlay, t0=t0, amb=amb)
    class _Nobody:                                                    # a blurred room with no one in it (screens / props in close)
        def draw(self, c, t, abs_t=None): pass
    def blurred(set_name, focus, overlay=None, t0=0.0, zoom=1.5): return shots.closeup(set_name, _Nobody(), focus=focus, overlay=overlay, t0=t0, zoom=zoom)
    def talk(lid, who, set_name, focus, face, tag=None, role=None, expr=None, pose=('down', 'down'), zoom=(1.0, 1.06), overlay=None, extra_hud=None, real=False):
        """Dialogue / close-up with the name + role lower-third (standing rule). real=True: real person, mouth stays flat."""
        a = Actor(who, 960, 1390, 2.15, face=face, rim=NR).pose(.2, pose).expression(0, **(expr or {}))
        if not real: say(a, lid)
        def hud(c, t):
            if tag: Wd.lower_third(c, tag, role, (t - .3) / .5)
            if extra_hud: extra_hud(c, t)
        add(lid, shots.closeup(set_name, a, focus=focus, overlay=overlay, t0=at(lid)), zoom=zoom, hud=hud)
        return a
    def hand(a_x, a_y, s, arms, side=-1): return kit.hand_pos(a_x, a_y, s, arms, side)

    # ---------- small shared drawings ----------
    def pinned(c, x, y, s, rot):
        """Gold pin at the top of a price tag's string, so the tag hangs from something."""
        a_ = math.radians(rot); px, py = -300 * s, -120 * s
        circ(c, x + px * math.cos(a_) - py * math.sin(a_), y + px * math.sin(a_) + py * math.cos(a_), 14, GOLD, 4)
    def cal_page(c, x, y, t, top, big, s=1.4, ring_at=None, sub=None):
        """Calendar page; a gold ring draws round the date when ring_at is set (seconds)."""
        k = kit.back(K(t, 0, .35)); c.save(); c.translate(x, y); c.scale(s * k, s * k)
        rect(c, -180, -200, 180, 220, PAPER, 6, r=10); rect(c, -180, -200, 180, -110, NAVY, 6, r=10)
        Wd.text(c, top, 0, -140, 46, WHITE, F_LABEL, 'center'); Wd.text(c, big, 0, 120, 190 if len(big) < 3 else 110, NAVY, F_TITLE, 'center')
        for i in range(2): kit.circ(c, -90 + i * 180, -200, 14, '#8C93A6', 4)
        if ring_at is not None and t > ring_at:
            p = skia.Path(); p.addArc(skia.Rect(-135, -30, 135, 210), -90, 360 * ease(K(t, ring_at, .5))); c.drawPath(p, kit.ink(16, GOLD))
        if sub: Wd.text(c, sub, 0, 205, 30, '#6B7390', F_LABEL, 'center')
        c.restore()
    def year_flip(c, x, y, t, y0, y1, dur, s=1.6):
        """Tear-off year calendar: pages fly away while the year runs from y0 to y1."""
        k = K(t, .15, dur); yr = int(round(lerp(y0, y1, ease(k))))
        c.save(); c.translate(x, y); c.scale(s, s)
        rect(c, -180, -200, 180, 220, PAPER, 6, r=10); rect(c, -180, -200, 180, -110, NAVY, 6, r=10)
        Wd.text(c, 'YEAR', 0, -140, 42, WHITE, F_LABEL, 'center'); Wd.text(c, str(yr), 0, 100, 112, NAVY, F_TITLE, 'center')
        for i in range(2): kit.circ(c, -90 + i * 180, -200, 14, '#8C93A6', 4)
        ph = (t * 5) % 1.0
        if 0 < k < 1 and ph > .08:
            c.save(); c.translate(ph * 520, -60 - ph * 380); c.rotate(ph * 60); rect(c, -150, -120, 150, 150, PAPER, 4); c.restore()
        c.restore()
    def flashes(times, big=1.0):
        def f(c, t):
            for tt in times:
                d = t - tt
                if 0 <= d < .18: c.drawRect(skia.Rect(0, 0, W, H), fp('#FFFFFF', int(130 * big * (1 - d / .18))))
        return f
    def figure(c, x, y, s=1.0, a=235, v=INKN):
        """A plain night silhouette (head + shoulders + body), feet at (x, y)."""
        c.save(); c.translate(x, y); c.scale(s, s)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-34, -150, 34, -10), 26, 26), fp(v, a)); c.drawCircle(0, -176, 26, fp(v, a))
        c.drawRect(skia.Rect(-22, -20, -6, 0), fp(v, a)); c.drawRect(skia.Rect(6, -20, 22, 0), fp(v, a)); c.restore()
    def certs(c, t, t_in=0.0, signed=None, glow=0.0):
        """The seven co-founder share certificates fanned on the desk; slide in one by one from t_in."""
        for i in range(7):
            k = ease_out(K(t, t_in + i * .14, .4)); x = 960 + (i - 3) * 236; y = 470 + abs(i - 3) * 34
            if k <= 0: continue
            sg = 1.0 if signed is None else K(t, signed + i * .32, .3)
            c.save(); c.translate(0, -(1 - k) * 700)
            if glow > 0: c.drawCircle(x, y, 170, fp(GOLD, int(70 * glow), blur=30))
            P.share_certificate(c, x, y, .52, rot=(i - 3) * 4, signed=sg); c.restore()
    def anthropic_wall(c, t, a=1.0):
        """The studio video wall switched to Anthropic (dark + ivory, the rough mark)."""
        rect(c, 120, 80, 1800, 540, AN_DK, 0, r=24); logos.anthropic(c, 400, 310, 120)
        Wd.text(c, 'ANTHROPIC', 1060, 350, 150, AN_IV, F_TITLE, 'center')
        Wd.text(c, 'NOW TRADING ON NASDAQ', 1060, 440, 46, SOFT, F_LABEL, 'center')
    def phone(c, x, y, s, screen_fn, t):
        """A phone held in a hand from the bottom of a top-down desk shot."""
        A.sleeve(c, x + 380 * s, y + 760 * s, x + 120 * s, y + 330 * s, w=150 * s)
        c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-4)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-232, -432, 248, 448), 54, 54), fp((0, 0, 0), 90, blur=14))
        rect(c, -240, -440, 240, 440, '#1B1D26', 8, r=54); rect(c, -212, -400, 212, 400, '#14213D', 3, r=30)
        screen_fn(c, t); c.restore()
        A.sleeve(c, x + 420 * s, y + 820 * s, x + 200 * s, y + 380 * s, w=150 * s)

    # ===================================== HOOK =====================================
    # 1-2  n001: the Nasdaq tower close on the LED screen pulling back (Times Square) -> whip to the trading floor
    def n001a(t0): return dict(draw=wide('night/nasdaq_tower', t0=t0), zoom=(1.9, 1.0), focus=((965, 420), (960, 540)),
                               hud=PT('Nasdaq, Times Square', 'Nov 19, 2026', t0=tl.dur('n001', nxt('n001')) * .55 * .7), sfx=[(0, 'amb:murmur', None)])
    def n001b(t0): return dict(draw=wide('night/trading', t0=t0), zoom=(1.0, 1.12), focus=((960, 560), (960, 500)), whip_in=True, sfx=[(0, 'whoosh'), (0, 'amb:murmur', None)])
    multi('n001', [(.55, n001a), (.45, n001b)])

    # 3  n002 the ticker board, a new row ANT --- blinking gold
    def slot(c, t):
        rect(c, 640, 60, 1280, 300, '#0D1630', 6, r=12); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(652, 72, 1268, 288), 8, 8), kit.ink(3, GOLD))
        Wd.text(c, 'NEW LISTING', 960, 120, 40, SOFT, F_LABEL, 'center'); Wd.text(c, 'ANT', 830, 240, 120, WHITE, F_TITLE, 'center')
        if int(t * 3) % 2 == 0: Wd.text(c, '- - -', 1110, 236, 110, GOLD, F_TITLE, 'center')
    add('n002', wide('night/trading', overlay=slot, t0=at('n002')), zoom=(1.45, 1.7), focus=((960, 300), (960, 260)), sfx=[(.2, 'tick'), (.9, 'tick'), (1.6, 'tick')])

    # 4  n003 THE TRADER, phone to the ear, brows up
    talk('n003', 'trader', 'night/trading', (700, 520), .4, 'The Trader', 'Dramatised', dict(mouth='flat', brow=.5), ('phone', 'down'), zoom=(1.0, 1.06))
    # 5  n004 THE SECOND TRADER, the screen behind him flips to $111.50
    def price_screen(c, t):
        rect(c, 1330, 110, 1830, 400, '#1E2026', 6, r=14); rect(c, 1348, 128, 1812, 382, '#0D1630', 3, r=8)
        Wd.text(c, 'ANT', 1400, 190, 50, SOFT, F_LABEL)
        if t < .7: Wd.text(c, '- - -', 1580, 320, 110, '#52618A', F_TITLE, 'center')
        else:
            k = kit.back(K(t, .7, .3)); c.save(); c.translate(1580, 290); c.scale(1, k); Wd.text(c, '$111.50', 0, 40, 110, GOLD, F_TITLE, 'center'); c.restore()
    talk('n004', 'trader2', 'night/trading', (1250, 520), -.4, 'The Second Trader', 'Dramatised', dict(mouth='smile', brow=.2), ('present', 'down'), zoom=(1.0, 1.25), overlay=price_screen)

    # 6-7  n005 (a) the studio wall switches to Anthropic; (b) 2021: people leave an office behind the glass
    def n005a(t0): return dict(draw=wide('night/nasdaq_studio', overlay=anthropic_wall, t0=t0), zoom=(1.0, 1.1), focus=((960, 420), (960, 400)),
                               sfx=[(0, 'amb:murmur', None)])
    walkers = [Actor(w, x, 1010, .8, face=.5, rim=NR).expression(0, mouth='flat', eyes='dot').pose(0, ('hold', 'hold')).walk_to(.1, 2.4, x + 1500) for w, x in (('analyst', -200), ('grad', -520), ('worker', -840))]
    def boxes(acts, t0=.1, t1=2.4):
        def f(c, t):
            for a in acts:
                k = min(max((t - t0) / (t1 - t0), 0), 1) if a.walk else 1; x = a.walk[2] + (a.walk[4] - a.walk[2]) * k
                hx, hy = kit.hand_pos(x, a.y, a.s, ('hold', 'hold'), -1); rect(c, hx - 30, hy - 120 * a.s, hx + 150 * a.s, hy + 10, '#C9A96A', 5, r=4)
        return f
    def n005b(t0): return dict(draw=wide('night/megaspeed', front=walkers, overlay=boxes(walkers), t0=t0), zoom=(1.0, 1.12), focus=((800, 600), (1100, 600)), whip_in=True,
                               hud=PT('San Francisco', '2021'), sfx=[(0, 'whoosh'), (.2, 'steps', 2.2)])
    multi('n005', [(.4, n005a), (.6, n005b)])

    # 8-9  n006 seven share certificates fan out on the desk -> the $280,000,000 counter over them
    def n006a(t0): return dict(draw=desk(lambda c, t: certs(c, t, .1)), zoom=(1.0, 1.08), rot=(-3, 0), sfx=[(.1 + i * .14, 'paper') for i in range(7)])
    def n006b(t0): return dict(draw=desk(lambda c, t: (certs(c, 9), Wd.counter(c, 960, 760, 0, 280_000_000, (t - .1) / 1.2, label='about, each'))), zoom=(1.08, 1.18))
    multi('n006', [(.5, n006a), (.5, n006b)])
    # 10  n007 typed card
    add('n007', shots.card('text', D('n007'), text=tl.by_id['n007']['text'], gold_words=['single']), zoom=(1.0, 1.02))

    # 11-12  n008 (a) OpenAI HQ at night, push to the door; (b) close on the lit door, one silhouette waiting
    def n008a(t0): return dict(draw=wide('night/openai_hq', t0=t0), zoom=(1.0, 1.3), focus=((960, 560), (960, 300)), whip_in=True,
                               hud=PT('OpenAI HQ', 'San Francisco'), sfx=[(0, 'whoosh'), (0, 'amb:murmur', None)])
    def n008b(t0): return dict(draw=wide('night/openai_hq', overlay=lambda c, t: figure(c, 1400, 884, .85), t0=t0), zoom=(2.0, 2.3), focus=((1000, 760), (1060, 780)))
    multi('n008', [(.55, n008a), (.45, n008b)])
    # 13  n009 typed card
    add('n009', shots.card('text', D('n009'), text=tl.by_id['n009']['text'], gold_words=['rich', 'paid']), zoom=(1.0, 1.02))

    # ===================================== TITLE (over the moving tower) =====================================
    def title_over(c, t):
        d = tl.dur('title', nxt_ev('title')); u = t / d; a = ease(K(u, .05, .3)) * (1 - ease(K(u, .88, .12)))
        c.drawRect(skia.Rect(0, 0, W, H), fp(NAVY, int(150 * a)))
        k = .9 + .1 * kit.pop(K(u, .05, .3)); c.save(); c.translate(W / 2, H / 2 + 20); c.scale(k, k)
        f = skia.Font(F_TITLE, 96); parts = [('THE ', WHITE), ('$1.7 TRILLION', GOLD), (' MORNING', WHITE)]
        tw = sum(f.measureText(s_) for s_, _ in parts); x = -tw / 2
        for s_, col in parts:
            Wd.text(c, s_, x, 0, 96, col, F_TITLE, stroke=12, alpha=int(255 * a)); x += f.measureText(s_)
        c.restore()
        Wd.text(c, 'THE DAY ANTHROPIC WENT PUBLIC', W / 2, H / 2 + 120, 46, SOFT, F_LABEL, 'center', stroke=8, alpha=int(255 * a * ease(K(u, .25, .25))))
    S.append(dict(name='title', dur=tl.dur('title', nxt_ev('title')), draw=wide('night/nasdaq_tower', t0=at('title')), hud=title_over, zoom=(1.18, 1.0), focus=((960, 460), (960, 540)),
                  sfx=[(0, 'amb:murmur', None)]))

    # ===================================== CH1 "The Walkout" =====================================
    rewind = lambda c, t: year_flip(c, 960, 520, t, 2026, 2021, 1.3)
    fade_in(1, 'The Walkout', desk(lambda c, t: year_flip(c, 960, 520, 0, 2026, 2026, 1)), zoom=(1.0, 1.0))
    add('n010', desk(rewind), zoom=(1.0, 1.08), rot=(0, -2), sfx=[(.15, 'flips', 1.3)])
    # 16-17  n011 (a) OpenAI glowing, 2021; (b) its people walk out with boxes
    def n011a(t0): return dict(draw=wide('night/openai_hq', t0=t0), zoom=(1.05, 1.15), focus=((960, 500), (960, 440)), hud=PT('OpenAI', '2021'))
    walk2 = [Actor(w, x, 1010, .82, face=.5, rim=NR).expression(0, mouth='flat', eyes='dot').pose(0, ('hold', 'hold')).walk_to(0, 3.0, x + 1700) for w, x in (('investor', -160), ('analyst', -480), ('grad', -800), ('worker', -1120))]
    def n011b(t0): return dict(draw=wide('night/megaspeed', front=walk2, overlay=boxes(walk2, 0, 3.0), t0=t0), zoom=(1.1, 1.1), focus=((700, 600), (1250, 600)), sfx=[(0, 'steps', 3.0)])
    multi('n011', [(.45, n011a), (.55, n011b)])
    # 18-19  n012 (a) Dario + Daniela walk out together, tagged; (b) close on Dario, the Anthropic badge catches the light
    dar = Actor('dario', 260, 1010, 1.0, face=.5, rim=NR).expression(0, mouth='flat', eyes='dot').walk_to(.1, 2.6, 980)
    dan = Actor('daniela', 20, 1010, 1.0, face=.5, rim=NR).expression(0, mouth='flat', eyes='dot').walk_to(.1, 2.6, 700)
    def n012a(t0): return dict(draw=wide('night/megaspeed', front=[dan, dar], t0=t0), zoom=(1.05, 1.15), focus=((600, 640), (900, 640)), sfx=[(.1, 'steps', 2.5)],
                               hud=both(LT('Dario Amodei', 'Co-founder', .3, x=80, y=600), LT('Daniela Amodei', 'Co-founder', .9)))
    def glint(c, t):
        g = K(t, .5, .25) * (1 - K(t, .9, .4)); bx, by = 960 + 44 * 2.15 * .9, 1390 - 275 * 2.15
        if g > 0:
            c.drawCircle(bx, by, 60, fp(GOLD, int(120 * g), blur=16))
            for a_ in (0, 90): c.save(); c.translate(bx, by); c.rotate(a_ + 45 * g); c.drawRect(skia.Rect(-70 * g, -4, 70 * g, 4), fp('#FFF4D6', int(230 * g))); c.restore()
        if t > .8:
            k = kit.back(K(t, .8, .35)); c.save(); c.translate(1440, 300); c.scale(k, k); logos.anthropic(c, -300, -22, 46)
            Wd.text(c, 'ANTHROPIC', 40, 10, 72, WHITE, F_TITLE, 'center', stroke=12); c.restore()
    def n012b(t0): return dict(draw=shots.closeup('night/megaspeed', Actor('dario', 960, 1390, 2.15, face=.3, rim=NR).expression(0, mouth='smile', eyes='dot'), focus=(900, 560), overlay=glint, t0=t0),
                               zoom=(1.0, 1.2), sfx=[(.5, 'ding'), (.8, 'pop')])
    multi('n012', [(.55, n012a), (.45, n012b)])
    # 20-22  n013-n015 analyst / investor / analyst
    talk('n013', 'analyst', 'night/office', (1300, 520), -.4, 'The Analyst', 'Dramatised', dict(mouth='flat', brow=.55), ('present', 'down'))
    def mug(a_pose):
        def f(c, t):
            hx, hy = kit.hand_pos(960, 1390, 2.15, a_pose, -1); rect(c, hx - 40, hy - 120, hx + 50, hy + 10, PAPER, 6, r=10)
            ambience.steam(c, t, hx + 5, hy - 130, 1.6)
        return f
    talk('n014', 'investor', 'night/office', (600, 520), .4, 'The Investor', 'Dramatised', dict(mouth='smirk', eyes='half', brow=.2), ('hold', 'down'), overlay=mug(('hold', 'down')))
    talk('n015', 'analyst', 'night/office', (1300, 520), -.4, None, None, dict(mouth='flat', eyes='half', brow=-.3), ('down', 'down'), zoom=(1.0, 1.2))
    # 23-24  n016 (a) Times Square pavement, everyone's phone lights up one by one; (b) the user counter
    def led_2022(c, year=True):
        cyl = skia.RRect.MakeRectXY(skia.Rect(668, 158, 1262, 636), 296, 66); c.drawRRect(cyl, fp('#1A2366'))
        if year: Wd.text(c, '2022', 965, 520, 150, '#3D7BFF', F_LABEL, 'center')
    def phones_on(c, t, n=9, year=True):
        led_2022(c, year)
        for i in range(n):
            x = 140 + i * 205; k = K(t, .2 + i * .18, .25)
            figure(c, x, 890, .9); c.drawCircle(x + 26, 760, 50 * k + 1, fp('#FFE2A0', int(110 * k), blur=18)); rect(c, x + 14, 744, x + 40, 782, '#FFE2A0' if k > .5 else '#24365E', 3, r=4)
    def n016a(t0): return dict(draw=wide('night/nasdaq_tower', overlay=phones_on, t0=t0), zoom=(1.35, 1.5), focus=((900, 760), (1000, 760)),
                               hud=PT('ChatGPT launches', 'Nov 30, 2022'), sfx=[(.2 + i * .18, 'pop') for i in range(9)])
    def n016b(t0): return dict(draw=wide('night/nasdaq_tower', overlay=lambda c, t: (phones_on(c, 9, year=False), Wd.counter(c, 960, 380, 0, 100_000_000, (t - .1) / 1.2, unit='', label='people using it within 2 months (estimate)')), t0=t0),
                               zoom=(1.3, 1.0), focus=((960, 700), (960, 540)), sfx=[(.1, 'tick'), (1.4, 'ding')])
    multi('n016', [(.5, n016a), (.5, n016b)])
    # 25-26  n017 business contracts slide across the desk, the Anthropic one gets signed; n018 a gold coin drops on it
    def contract(c, x, y, rot, title, signed=0.0, mark=False, s=1.0):
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
        c.drawRect(skia.Rect(-226, -296, 246, 316), fp((0, 0, 0), 70, blur=12)); rect(c, -240, -310, 240, 310, PAPER, 5, r=4)
        if mark: logos.anthropic(c, -170, -240, 34)
        Wd.text(c, title, 30 if mark else 0, -228, 40, NAVY, F_LABEL, 'center'); c.drawRect(skia.Rect(-200, -200, 200, -194), fp(NAVY))
        for i in range(6): c.drawRect(skia.Rect(-200, -150 + i * 46, 200 - (i % 3) * 60, -136 + i * 46), fp('#B8B0A0'))
        Wd.text(c, 'ENTERPRISE CUSTOMER', -200, 180, 28, '#6B7390', F_LABEL)
        c.drawLine(-200, 250, 120, 250, kit.ink(3, NAVY))
        if signed > 0:
            p = skia.Path(); n_ = int(30 * min(signed, 1))
            for k_ in range(n_ + 1): xx = -190 + k_ * 9; yy = 236 + math.sin(k_ * .9) * 14; p.moveTo(xx, yy) if k_ == 0 else p.lineTo(xx, yy)
            c.drawPath(p, kit.ink(5, NAVY))
        c.restore()
    def contracts(c, t, sign_t=1.2, pen=True):
        for i, (x0, x1, rot, ttl) in enumerate(((-400, 520, -8, 'SERVICE AGREEMENT'), (2300, 1420, 7, 'SERVICE AGREEMENT'))):
            k = ease_out(K(t, .1 + i * .3, .5)); contract(c, lerp(x0, x1, k), 560, rot, ttl, signed=1, s=.9)
        k = ease_out(K(t, .6, .5)); contract(c, 960, lerp(1500, 560, k), -2, 'ANTHROPIC AI', signed=K(t, sign_t, .8), mark=True)
        if pen and t > sign_t - .3:
            px = -190 + 270 * min(K(t, sign_t, .8), 1) + 960; A.sleeve(c, px + 520, 1180, px + 60, 760)
            c.save(); c.translate(px, 790); c.rotate(-30); rect(c, -12, -170, 12, 0, GOLD, 4, r=6); poly(c, [(-12, 0), (12, 0), (0, 26)], '#2E2E38', 3); c.restore()
    add('n017', desk(contracts), zoom=(1.0, 1.1), sfx=[(.1, 'paper'), (.4, 'paper'), (.6, 'paper'), (1.2, 'paper')])
    def coin_drop(c, t):
        contracts(c, 9, 0, pen=False)
        k = K(t, .3, .45); y = lerp(-120, 560, ease(k) if k < 1 else 1); bounce = math.sin(K(t, .75, .35) * math.pi) * 40 * (1 - K(t, .75, .35))
        c.drawCircle(960, 600, 110 * k, fp((0, 0, 0), int(60 * k), blur=14)); Wd.coin(c, 960, y - bounce, 90)
        g = K(t, .9, .2) * (1 - K(t, 1.2, .4))
        if g > 0:
            for a_ in (0, 90): c.save(); c.translate(1010, 510); c.rotate(a_ + 45); c.drawRect(skia.Rect(-80 * g, -5, 80 * g, 5), fp('#FFF4D6', int(240 * g))); c.restore()
    add('n018', desk(coin_drop), zoom=(1.05, 1.3), focus=((960, 560), (960, 560)), sfx=[(.75, 'coin'), (.9, 'ding')])

    # ===================================== CH2 "The Swap" =====================================
    def sora_screen(grey_at=None, stamp_at=None):
        def f(c, t):
            Wd.text(c, '9:41', -150, -340, 34, WHITE, F_LABEL, 'center')
            g = 0 if grey_at is None else K(t, grey_at, .6)
            for i, (xx, yy) in enumerate(((-110, -150), (110, -150), (-110, 100), (110, 100))):
                if i == 0: P.app_icon(c, xx, yy, .9, grey=g, name='SORA')
                else: rect(c, xx - 80, yy - 80, xx + 80, yy + 80, ('#2B4A7A', '#3A63A0', '#24365E')[i - 1], 5, r=30)
        return f
    def n019a_draw(c, t): phone(c, 960, 520, .95, sora_screen(), t)
    fade_in(2, 'The Swap', desk(n019a_draw), zoom=(1.0, 1.0))
    def n019a(t0): return dict(draw=desk(n019a_draw), zoom=(1.0, 1.15), focus=((960, 540), (860, 420)), hud=PT('OpenAI shuts down Sora', 'March 2026'))
    def n019b_draw(c, t):
        phone(c, 960, 520, .95, sora_screen(grey_at=.2), t); PD.prop_stamp(c, 'Shut down', 900, 420, t - .8, rot=-8, size=110)
    def n019b(t0): return dict(draw=desk(n019b_draw), zoom=(1.15, 1.3), focus=((860, 420), (880, 420)), shake=shake(.8), sfx=[(.8, 'stamp')], hud=HUDPOP('6 months after launch', 960, 960, .3, WHITE, 70, -2))
    multi('n019', [(.5, n019a), (.5, n019b)])
    # 29  n020 the DISNEY DEAL folder snaps shut, the deal counter in orange
    def deal(c, t):
        PD.memo_folder(c, 960, 470, 1.35, rot=-4, open_k=1 - ease_out(K(t, .3, .4)), label_text='DISNEY DEAL')
        if t > .7: Wd.counter(c, 960, 770, 0, 1_000_000_000, (t - .7) / 1.2, loss=True, label='the deal: gone', size=90)
    add('n020', desk(deal), zoom=(1.0, 1.12), shake=shake(.7), sfx=[(.7, 'paper'), (.8, 'low_tone')], hud=lambda c, t: Wd.text(c, 'PER REPORTS: NO MONEY CHANGED HANDS', 1880, 70, 34, SOFT, F_LABEL, 'right', stroke=6))
    # 30-31  n021 THE CLERK with the phone; n022 THE MANAGER, hand over the face
    talk('n021', 'clerk', 'night/office', (1300, 520), -.4, 'The Clerk', 'Dramatised', dict(mouth='flat', brow=.4), ('phone', 'down'))
    talk('n022', 'manager', 'night/office', (600, 520), .4, 'The Manager', 'Dramatised', dict(mouth='flat', eyes='closed', brow=.3), ('facepalm', 'down'), zoom=(1.0, 1.2))
    # 32-35  n023 (a) the newsroom, push to the TV wall; (b) bar chart, Anthropic rises; n024 (a) OpenAI bar; (b) newspaper "a first"
    def bars(c, t, both_=False, t2=0.0):
        Wd.text(c, 'REVENUE, SECOND QUARTER 2026', 960, 170, 54, WHITE, F_TITLE, 'center')
        base = 820; x0s = (560, 1160); hmax = 400   # clear of the raised captions
        for i, (val, nm, fill, line_c, mark) in enumerate(((11.6, 'ANTHROPIC', AN_IV, AN_DK, logos.anthropic), (6.7, 'OPENAI', '#000000', WHITE, logos.openai))):
            if i == 1 and not both_: continue
            g = ease_out(K(t, .3 if i == 0 else t2, 1.0)) if (i == 0 and not both_) or i == 1 else 1.0
            h = hmax * val / 11.6 * g; x = x0s[i]
            if h > 2: rect(c, x, base - h, x + 220, base, fill, 6, r=8, v=line_c if i == 1 else '#14213D')
            mark(c, x + 110, base - h - 70, 46)
            Wd.text(c, nm, x + 110, base + 60, 46, WHITE, F_LABEL, 'center')
            if g > .95: Wd.text(c, f'${val} BILLION', x + 110, base - h - 140, 52, GOLD, F_TITLE, 'center', stroke=8)
        c.drawLine(480, base, 1460, base, kit.ink(6, WHITE))
        if both_ and t > t2 + 1.1:
            Wd.pop_label(c, 'counted differently', 1270, 330, (t - t2 - 1.1) / .4, SOFT, 50, rot=-3, stroke=8)
        Wd.text(c, 'WALL STREET JOURNAL, Q2 2026', 1860, 1010 - 0, 28, SOFT, F_LABEL, 'right')
    def tv_bars(c, t):
        rect(c, 156, 105, 1020, 480, '#0D1630', 0, r=6)
        c.save(); c.translate(156, 105); c.scale(864 / 1920, 375 / 1080); bars(c, t + .3); c.restore()
    def n023a(t0): return dict(draw=wide('night/newsroom', overlay=tv_bars, t0=t0), zoom=(1.0, 1.9), focus=((960, 540), (588, 292)), whip_in=True, sfx=[(0, 'whoosh'), (0, 'amb:murmur', None)])
    def n023b(t0): return dict(draw=plain(lambda c, t: bars(c, t)), zoom=(1.0, 1.06), sfx=[(.3, 'whoosh'), (1.3, 'ding')])
    multi('n023', [(.4, n023a), (.6, n023b)])
    def n024a(t0): return dict(draw=plain(lambda c, t: bars(c, t, True, .1)), zoom=(1.06, 1.1), sfx=[(.1, 'whoosh'), (1.1, 'tick')])
    def paper_in(c, t):
        A.newspaper(c, 960, 600, t - .1, 'Business News', 'Anthropic passes OpenAI: a first', 'Q2 2026 revenue, as reported', dur=.7)
    def n024b(t0): return dict(draw=wide('night/newsroom', overlay=lambda c, t: (c.drawRect(skia.Rect(0, 0, W, H), fp(NAVY, int(120 * K(t, 0, .3)))), paper_in(c, t)), t0=t0), zoom=(1.0, 1.08), sfx=[(.1, 'whoosh'), (.8, 'paper')])
    multi('n024', [(.55, n024a), (.45, n024b)])
    # 36  n025 typed card
    add('n025', shots.card('text', D('n025'), text=tl.by_id['n025']['text'], gold_words=['passed']), zoom=(1.0, 1.02))
    # 37  n026 (a) Altman under the OpenAI sign, flashes; (b) close, his September statement as a label (narrated, he does not speak)
    alt = Actor('altman', 1470, 905, .62, face=0, rim=NR).expression(0, mouth='flat', eyes='dot').pose(.2, ('down', 'down'))
    def n026a(t0): return dict(draw=wide('night/openai_hq', front=[alt], overlay=flashes([.3, .8, 1.4]), t0=t0), zoom=(1.06, 1.12), focus=((1100, 430), (1160, 420)),   # raised OpenAI sign in frame, under the place tag
                               hud=both(LT('Sam Altman', 'CEO, OpenAI', .3), PT('San Francisco', 'September 2026')), sfx=[(.3, 'shutter'), (.8, 'shutter'), (1.4, 'shutter')])
    def n026b_hud(c, t):
        Wd.pop_label(c, 'OpenAI IPO: not in 2026', 1340, 300, (t - .3) / .4, GOLD, 80, rot=-3, stroke=12)
        Wd.text(c, 'WHAT HE SAID, SEPT 2026', 1340, 380, 34, SOFT, F_LABEL, 'center', stroke=6, alpha=int(255 * K(t, .6, .3)))
    def n026b(t0): return dict(draw=shots.closeup('night/openai_hq', Actor('altman', 760, 1390, 2.15, face=.3, rim=NR).expression(0, mouth='flat', eyes='dot').pose(.2, ('down', 'down')), focus=(960, 640), t0=t0),
                               zoom=(1.0, 1.08), hud=n026b_hud, sfx=[(.3, 'pop')])
    multi('n026', [(.5, n026a), (.5, n026b)])
    # 38  n027 the calendar tears to NOVEMBER, gold ring on 19
    def nov(c, t):
        if t < .6: year_flip(c, 960, 540, t, 9, 11, .5, s=1.7)
        else: cal_page(c, 960, 540, t - .6, 'NOVEMBER 2026', '19', s=1.7, ring_at=.4)
    add('n027', desk(nov), zoom=(1.0, 1.15), shake=shake(1.0), sfx=[(0, 'flips', .6), (1.0, 'stamp')])

    # ===================================== CH3 "Who Gets Paid First" =====================================
    STEPS = (('BANKS', 'set the price'), ('BIG INVESTORS', 'buy first'), ('FOUNDERS', 'sell some'), ('THE PUBLIC', 'last'))
    def icon(c, i, x, y, s):
        c.save(); c.translate(x, y); c.scale(s, s)
        if i == 0:   # bank: pediment + columns
            poly(c, [(-90, -40), (90, -40), (0, -100)], GOLD, 5); [rect(c, -76 + k * 44, -36, -56 + k * 44, 50, PAPER, 4) for k in range(4)]; rect(c, -96, 50, 96, 70, GOLD, 5)
        elif i == 1:  # briefcase
            rect(c, -90, -50, 90, 70, '#7A5A3C', 5, r=10); rect(c, -36, -80, 36, -50, None, 5, r=8); rect(c, -90, -4, 90, 6, GOLD, 0)
        elif i == 2:  # certificate
            rect(c, -90, -64, 90, 64, PAPER, 5, r=6); circ(c, 54, 34, 18, GOLD, 3); [c.drawRect(skia.Rect(-66, -36 + k * 22, 30, -28 + k * 22), fp('#B8B0A0')) for k in range(3)]
        else:        # a small person
            figure(c, 0, 76, .62, 255, '#9DB0DA')
        c.restore()
    def lineup(c, t, upto=4):
        Wd.text(c, 'AN IPO MORNING, IN ORDER', 960, 190, 62, WHITE, F_TITLE, 'center')
        for i, (nm, sub) in enumerate(STEPS[:upto]):
            k = kit.pop(K(t, .3 + i * .5, .4)); x = 300 + i * 440; s = .78 if i == 3 else 1.0
            if k <= 0: continue
            c.save(); c.translate(x, 560); c.scale(k, k); c.translate(-x, -560)
            rect(c, x - 170, 380, x + 170, 760, NAVY if i < 3 else '#1A2747', 6, r=18); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 160, 390, x + 160, 750), 12, 12), kit.ink(3, GOLD if i < 3 else '#52618A'))
            Wd.text(c, str(i + 1), x - 130, 450, 48, GOLD, F_TITLE, 'center'); icon(c, i, x, 540, s)
            Wd.text(c, nm, x, 680, 48 if i < 3 else 40, WHITE, F_LABEL, 'center'); Wd.text(c, sub, x, 730, 32, SOFT, F_LABEL, 'center')
            c.restore()
            if i < 3 and K(t, .55 + i * .5, .3) > 0: Wd.arrow(c, x + 180, 570, x + 255, 570, K(t, .55 + i * .5, .3), GOLD, 26)
    fade_in(3, 'Who Gets Paid First', plain(lambda c, t: Wd.text(c, 'AN IPO MORNING, IN ORDER', 960, 190, 62, WHITE, F_TITLE, 'center')), zoom=(1.0, 1.0))
    add('n028', plain(lineup), zoom=(1.0, 1.04), sfx=[(.3 + i * .5, 'pop') for i in range(4)])
    # 40-41  n029 (a) THE BANKER in the private banker's office; (b) the price tag $70-78 -> $83
    bk = Actor('banker', 1500, 1040, 1.0, face=-.4, rim=NR).expression(0, mouth='flat', eyes='half').pose(.2, ('down', 'hip'))
    def n029a(t0): return dict(draw=wide('night/private_banker', front=[bk], t0=t0), zoom=(1.0, 1.15), focus=((1100, 620), (1300, 620)), hud=LT('The Banker', 'Dramatised', .3), sfx=[(0, 'amb:murmur', None)])
    def n029b(t0): return dict(draw=blurred('night/private_banker', (960, 700), overlay=lambda c, t: (P.price_tag(c, 960, 520, 1.6, rot=-6 + 3 * math.sin(t * 2), price='$83', old='$70-78', u=K(t, .5, .5)), pinned(c, 960, 520, 1.6, -6 + 3 * math.sin(t * 2)),
                                                                                           Wd.text(c, 'WEDNESDAY NIGHT', 960, 900, 48, GOLD, F_LABEL, 'center', stroke=8)), t0=t0),
                               zoom=(1.0, 1.1), sfx=[(.2, 'paper'), (.5, 'tick'), (.9, 'ding')], hud=HUDPOP('above the range', 1450, 260, .9, WHITE, 64, -3))
    multi('n029', [(.45, n029a), (.55, n029b)])
    # 42  n030 the allocation list unrolls on the desk
    def unroll(c, t):
        P.investor_list(c, 960, 540, 1.5, open_k=ease_out(K(t, .2, .9)), rows=9)
        for i in range(3):
            k = ease_out(K(t, 1.2 + i * .3, .4)); x = lerp(1700, 1250, k); y = 300 + i * 160
            if k > 0: rect(c, x - 80, y - 46, x + 80, y + 46, PAPER, 4, r=6); Wd.text(c, 'SHARES', x, y + 14, 36, NAVY, F_LABEL, 'center')
    add('n030', desk(unroll), zoom=(1.0, 1.08), rot=(2, 0), sfx=[(.2, 'paper'), (1.2, 'paper'), (1.5, 'paper'), (1.8, 'paper')])
    # 43-45  n031 THE SAVER, hopeful; n032 THE BANKER over his glasses; n033 the list rolls shut in front of her
    talk('n031', 'saver', 'night/private_banker', (500, 700), .4, 'The Saver', 'Dramatised', dict(mouth='smile', brow=.4), ('present', 'down'))
    talk('n032', 'banker', 'night/private_banker', (1300, 600), -.4, None, None, dict(mouth='flat', eyes='half', brow=-.4), ('down', 'hip'), zoom=(1.0, 1.2))
    talk('n033', 'saver', 'night/private_banker', (500, 700), .4, None, None, dict(mouth='o', eyes='wide', brow=.6), ('present', 'down'), zoom=(1.1, 1.25),
         overlay=lambda c, t: P.investor_list(c, *hand(960, 1390, 2.15, ('present', 'down'), -1), 1.15, open_k=1 - ease_out(K(t, .3, .5))))   # held in her hand, not floating
    # 46-47  n034 (a) share stacks fill the vault, $81 billion; (b) gold RECORD stamp on the vault door
    def stacks(c, t, ctr=True):
        for i in range(9):
            col, row = i % 3, i // 3; x = 860 + col * 220 + row * 60; base = 1000 - row * 20; k = ease_out(K(t, .1 + i * .12, .35))
            for j in range(int(7 * k)): rect(c, x - 90, base - j * 26 - 26, x + 90, base - j * 26, PAPER if j % 2 else '#F0E6CC', 3, r=3)
            if k > .9: rect(c, x - 90, base - 7 * 26 - 8, x + 90, base - 7 * 26, GOLD, 3, r=2)
        if ctr: Wd.counter(c, 960, 160, 0, 81_000_000_000, (t - .1) / 1.4, label='more than, for 980 million shares', size=86)
    def n034a(t0): return dict(draw=wide('night/bank_vault', overlay=stacks, t0=t0), zoom=(1.0, 1.1), focus=((1000, 600), (1050, 620)), sfx=[(.1 + i * .12, 'paper') for i in range(9)])
    def n034b(t0): return dict(draw=wide('night/bank_vault', overlay=lambda c, t: (stacks(c, 9, False), Wd.stamp(c, 'Record', 585, 500, t - .4, GOLD, rot=-10, size=120)), t0=t0), zoom=(1.3, 1.5), focus=((700, 520), (600, 500)),
                               shake=shake(.4), sfx=[(.4, 'stamp')], hud=HUDPOP('biggest IPO on record', 1300, 950, .7, WHITE, 66, -2))
    multi('n034', [(.55, n034a), (.45, n034b)])
    # 48  n035 the seven certificates again; signatures write themselves one by one
    add('n035', desk(lambda c, t: certs(c, t, 0, signed=.3)), zoom=(1.08, 1.0), rot=(0, 3), sfx=[(.3 + i * .32, 'paper') for i in range(7)],
        hud=HUDPOP('just over 3 million shares each', 960, 900, 2.0, WHITE, 64, -2))
    # 49-50  n036 THE BANKER stamps; n037 THE CLERK stacks the signed pages
    talk('n036', 'banker', 'night/private_banker', (1100, 640), -.3, None, None, dict(mouth='smirk', eyes='half'), ('push', 'down'), zoom=(1.0, 1.08),
         overlay=lambda c, t: Wd.stamp(c, 'Signed', 1420, 560, t - .4, GOLD, rot=-8, size=100))
    def pages(c, t):
        hx, hy = kit.hand_pos(960, 1390, 2.15, ('hold', 'hold'), -1)
        for j in range(7): rect(c, hx - 60 + j * 3, hy - 200 - j * 12, hx + 260 + j * 3, hy + 20 - j * 12, PAPER, 4, r=3)
        g = K(t, .5, .2) * (1 - K(t, .8, .4))
        if g > 0: c.drawCircle(hx + 200, hy - 270, 70, fp(GOLD, int(130 * g), blur=18))
    talk('n037', 'clerk', 'night/private_banker', (1450, 640), -.4, 'The Clerk', 'Dramatised', dict(mouth='smile', eyes='half'), ('hold', 'hold'), overlay=pages)
    # 51  n038 the studio before the bell: empty podium, the wall clock at 9:29, the bell silent
    def preclock(c, t):
        rect(c, 120, 80, 1800, 540, '#0B2A3A', 0, r=24); circ(c, 960, 300, 170, PAPER, 8)
        for k_ in range(12): a_ = math.radians(k_ * 30); c.drawLine(960 + 140 * math.cos(a_), 300 + 140 * math.sin(a_), 960 + 155 * math.cos(a_), 300 + 155 * math.sin(a_), kit.ink(6, NAVY))
        for ang, ln, w_ in ((29 * 6 + t * 1.2, 130, 10), (9 * 30 + 29 * .5, 85, 14)):
            a_ = math.radians(ang - 90); c.drawLine(960, 300, 960 + ln * math.cos(a_), 300 + ln * math.sin(a_), kit.ink(w_, NAVY))
        a_ = math.radians(t * 36 - 90); c.drawLine(960, 300, 960 + 140 * math.cos(a_), 300 + 140 * math.sin(a_), kit.ink(4, ORANGE)); circ(c, 960, 300, 12, GOLD, 3)
        Wd.text(c, '9:29 AM', 1380, 330, 80, WHITE, F_TITLE, 'center'); Wd.text(c, 'MARKET OPENS 9:30', 540, 330, 46, SOFT, F_LABEL, 'center')
    add('n038', wide('night/nasdaq_studio', overlay=preclock, t0=at('n038')), zoom=(1.0, 1.12), focus=((960, 520), (960, 420)), sfx=[(0, 'tick'), (1, 'tick'), (2, 'tick'), (3, 'tick')],
        hud=HUDPOP('nearly $2 billion - before the bell', 960, 800, 1.2, GOLD, 72, -2))

    # ===================================== TWIST =====================================
    add('n039', wide('night/nasdaq_studio', overlay=lambda c, t: (rect(c, 120, 80, 1800, 540, '#0B2A3A', 0, r=24), P.bell(c, 960, 320, 1.7, t=t, ring=K(t, .2, .1))), t0=at('n039'),
                     amb=[('gold_dust', dict(n=50, region=(0, 0, 1920, 760)))]),
        zoom=(1.0, 1.25), focus=((960, 480), (960, 380)), sfx=[(.2, 'ding_carriage'), (.25, 'boom')])
    def two_tags(c, t):
        P.price_tag(c, 560, 520, 1.25, rot=-6, price='$83', u=K(t, .1, .4)); pinned(c, 560, 520, 1.25, -6); Wd.text(c, 'WHAT ANTHROPIC SOLD AT', 560, 300, 40, SOFT, F_LABEL, 'center')
        P.price_tag(c, 1380, 520, 1.25, rot=5, price=' ', u=1); pinned(c, 1380, 520, 1.25, 5); c.save(); c.translate(1380, 520); c.rotate(5); kit.label(c, '$111.50', 38 * 1.25, 34 + (1 - ease_out(K(t, .9, .4))) * 60, 84, NAVY, font=F_TITLE, align='center', skew=0, alpha=min(1, K(t, .9, .4) * 2)); c.restore(); Wd.text(c, 'WHERE IT OPENED', 1380, 300, 40, SOFT, F_LABEL, 'center')
        g = K(t, 1.6, .5)
        if g > 0:
            c.drawRoundRect(skia.Rect(820, 440, 1100, 600), 30, 30, fp(GOLD, int(90 * g * (.8 + .2 * math.sin(t * 6))), blur=24))
            Wd.pop_label(c, '+$28.50', 960, 560, (t - 1.6) / .4, GOLD, 90, rot=-3, stroke=12)
    add('n040', plain(two_tags), zoom=(1.0, 1.08), sfx=[(.1, 'paper'), (.9, 'paper'), (1.6, 'ding')])
    add('n041', shots.card('text', D('n041'), text=tl.by_id['n041']['text'], gold_words=['jump', 'eighty-three']), zoom=(1.0, 1.02))
    def list_glow(c, t):
        c.drawCircle(960, 440, 400, fp(GOLD, int(70 + 30 * math.sin(t * 4)), blur=60)); P.investor_list(c, 960, 440, 1.2, open_k=1)
        Wd.counter(c, 960, 800, 0, 14_000_000_000, (t - .2) / 1.4, label='more, by the closing bell (our estimate)', size=78)
    add('n042', blurred('night/private_banker', (960, 760), overlay=list_glow, t0=at('n042')), zoom=(1.0, 1.1), sfx=[(.2, 'tick'), (1.6, 'ding')])

    # ===================================== CH4 "The Morning After" =====================================
    DOWN = [('ticker', dict(rect=(40, 196, 1880, 258), items=(('ANT', '-9%'), ('NVDA', '+0.4%'), ('ANT', '-9%'), ('S&P 500', '-0.1%')), down=('ANT',)))]
    fade_in(4, 'The Morning After', wide('night/trading', t0=at('chapter:4'), amb=DOWN), zoom=(1.0, 1.0), focus=(960, 540))
    def fall(c, t): Wd.counter(c, 960, 740, 0, 9, (t - .2) / 1.2, unit='', suffix='%', loss=True, label='to about $85', size=100)
    add('n043', wide('night/trading', overlay=fall, t0=at('n043'), amb=DOWN), zoom=(1.0, 1.12), focus=((960, 500), (960, 460)), hud=PT('Wall Street', 'Nov 20, 2026'), sfx=[(.2, 'tick'), (1.6, 'low_tone')])
    def slice_(c, t):
        Wd.text(c, 'BOUGHT AT THE OPEN: $111.50', 960, 190, 56, WHITE, F_TITLE, 'center')
        cx, cy, r = 960, 560, 260; k = ease_out(K(t, .6, .6)); c.drawCircle(cx + 16, cy + 20, r, fp((0, 0, 0), 70, blur=16))
        p = skia.Path(); p.moveTo(cx, cy); p.arcTo(skia.Rect(cx - r, cy - r, cx + r, cy + r), -90 + 86, 274, False); p.close(); c.drawPath(p, fp(GOLD)); c.drawPath(p, kit.ink(7))
        Wd.text(c, '$85', cx - 60, cy + 100, 110, '#3A2A00', F_TITLE, 'center')
        c.save(); c.translate(160 * k, 90 * k); c.rotate(14 * k)
        q = skia.Path(); q.moveTo(cx, cy); q.arcTo(skia.Rect(cx - r, cy - r, cx + r, cy + r), -90, 86, False); q.close(); c.drawPath(q, fp(ORANGE)); c.drawPath(q, kit.ink(7)); c.restore()
        if t > 1.2: Wd.pop_label(c, '- almost a quarter', 1500, 860, (t - 1.2) / .4, ORANGE, 66, rot=-3, stroke=10)
    add('n044', plain(slice_), zoom=(1.0, 1.06), sfx=[(.6, 'whoosh'), (1.0, 'low_tone')])
    talk('n045', 'trader', 'night/trading', (700, 520), .4, 'The Trader', 'Dramatised', dict(mouth='flat', eyes='half', brow=.5, sweat=0), ('chin', 'down'), zoom=(1.0, 1.08))
    t2 = say(Actor('trader2', 1500, 1150, 1.25, face=-.4, rim=NR).expression(0, mouth='flat', eyes='half', brow=.4).pose(.2, ('facepalm', 'down')), 'n046')
    add('n046', wide('night/trading', front=[t2], t0=at('n046'), amb=DOWN + [('loss_flicker', dict(a=30))]), zoom=(1.6, 1.4), focus=((520, 420), (1350, 640)),
        hud=LT('The Second Trader', 'Dramatised', .6), sfx=[(D('n046') * .8, 'low_tone')])
    # 60-62  n047 index-fund boxes on a conveyor in the data center; n048 (a) arms grab ANT shares; (b) $8 of every $10,000
    def belt(c, t, grab_t=None):
        P.conveyor(c, t, 900, 0, 1920, speed=80)
        for i in range(4):
            x = ((i * 520 + t * 80) % 2280) - 180; g = 0 if grab_t is None else K(t, grab_t + i * .4, .4)
            P.fund_box(c, x, 790, .9, grab=g)
    def n047(t0): return dict(draw=wide('night/datacenter', overlay=lambda c, t: belt(c, t), t0=t0), zoom=(1.0, 1.15), focus=((960, 640), (960, 700)), sfx=[(0, 'amb:hum', None), (0, 'amb:rumble', None)])
    add('n047', **n047(at('n047')))
    def n048a(t0): return dict(draw=wide('night/datacenter', overlay=lambda c, t: belt(c, t + D('n047'), grab_t=D('n047') + .1), t0=t0), zoom=(1.15, 1.25), focus=((900, 700), (1000, 700)),
                               sfx=[(.1, 'stamp'), (.5, 'stamp'), (.9, 'stamp')])
    def eight(c, t):
        rect(c, 300, 120, 1620, 960, '#1E2026', 6, r=18); rect(c, 322, 142, 1598, 938, '#0F1A38', 3, r=8)
        Wd.text(c, 'A TOTAL STOCK MARKET FUND: EVERY $10,000', 960, 210, 46, WHITE, F_TITLE, 'center')
        z = ease(K(t, 1.0, .9)); gx, gy, cell = 420, 270, 62
        if z < 1:
            a = int(255 * (1 - z))
            for i in range(100):
                col_, row = i % 10, i // 10; c.drawRect(skia.Rect(gx + col_ * cell, gy + row * cell, gx + col_ * cell + 52, gy + row * cell + 52), fp('#2B4A7A' if i else GOLD, a))
            Wd.text(c, 'each square = $100', 1300, 700, 40, SOFT, F_LABEL, 'center', alpha=a)
        if z > 0:
            a = int(255 * z); s_ = 31
            Wd.text(c, 'zoom: the first $100', 1300, 700, 40, SOFT, F_LABEL, 'center', alpha=a)
            for i in range(100):
                col_, row = i % 10, i // 10; lit = i < 8 and t > 1.9
                c.drawRect(skia.Rect(gx + col_ * cell, gy + row * cell, gx + col_ * cell + 52, gy + row * cell + 52), fp(GOLD if lit else '#2B4A7A', a))
        Wd.counter(c, 1340, 420, 0, 8, (t - 1.9) / .9, label='in Anthropic (Morningstar estimate)', size=110, panel=False)
    def n048b(t0): return dict(draw=blurred('night/datacenter', (960, 600), overlay=eight, t0=t0), zoom=(1.0, 1.06), sfx=[(1.0, 'whoosh'), (1.9, 'tick'), (2.8, 'ding')])
    multi('n048', [(.45, n048a), (.55, n048b)])
    add('n049', shots.card('text', D('n049'), text=tl.by_id['n049']['text'], gold_words=['S&P', 'year', 'profits.']), zoom=(1.0, 1.02))
    # 64  n050 OpenAI HQ, a sealed CONFIDENTIAL envelope, then 2027 (no REPORTED stamp - owner 24 Nov)
    def sealed(c, t):
        k = ease_out(K(t, .1, .5)); c.save(); c.translate(760, 520 + (1 - k) * 700); c.rotate(-5)
        c.drawRect(skia.Rect(-300, -186, 330, 214), fp((0, 0, 0), 90, blur=14)); rect(c, -320, -200, 320, 200, '#E9DFC8', 6)
        poly(c, [(-320, -200), (320, -200), (0, 40)], '#DDD1B6', 6); circ(c, 0, 40, 46, GOLD, 5); Wd.text(c, 'CONFIDENTIAL FILING', 0, 160, 46, NAVY, F_LABEL, 'center'); c.restore()
        if t > 1.2: cal_page(c, 1420, 520, t - 1.2, 'AIMING FOR', '2027', s=1.15)
    add('n050', wide('night/openai_hq', overlay=lambda c, t: (c.drawRect(skia.Rect(0, 0, W, H), fp(NAVY, int(110 * K(t, 0, .3)))), sealed(c, t)), t0=at('n050')),
        zoom=(1.0, 1.1), sfx=[(.1, 'whoosh'), (.6, 'paper'), (1.2, 'page')], hud=lambda c, t: Wd.text(c, 'REPORTED: FILED IN SECRET, JUNE 2026', 1880, 70, 34, SOFT, F_LABEL, 'right', stroke=6))

    # ===================================== ENDING =====================================
    def price_band(c, t):
        rect(c, 662, 762, 1268, 858, '#0B0D12', 0); Wd.text(c, 'ANT', 760, 836, 70, WHITE, F_LABEL, 'center'); Wd.text(c, '$111.50', 1080, 840, 82, GOLD, F_TITLE, 'center')
    add('n051', wide('night/nasdaq_tower', overlay=price_band, t0=at('n051')), zoom=(1.9, 1.05), focus=((965, 600), (960, 540)), sfx=[(0, 'amb:murmur', None)])
    def seven_walk(c, t):
        for i in range(7):
            x = lerp(300 - i * 120, 2300 - i * 120, ease(K(t, 0, D('n052') * 1.1))); figure(c, x, 892, .9 + .03 * (i % 2), 245)
    add('n052', wide('night/nasdaq_tower', overlay=seven_walk, t0=at('n052')), zoom=(1.3, 1.3), focus=((700, 760), (1200, 760)), sfx=[(0, 'steps', D('n052'))],
        hud=HUDPOP('7 people - nearly $2 billion', 960, 700, .8, GOLD, 74, -2))
    def door_light(c, t):
        figure(c, 1400, 884, .85); g = K(t, 1.0, .3)
        if g > 0: c.drawRect(skia.Rect(1270, 812, 1400, 876), fp('#FFE2A0', int(200 * g))); c.drawCircle(1335, 844, 120, fp('#FFE2A0', int(60 * g), blur=30))
    add('n053', wide('night/openai_hq', overlay=door_light, t0=at('n053')), zoom=(1.35, 2.1), focus=((960, 420), (1040, 780)), sfx=[(1.0, 'pickup')])   # starts on the sign, tilts down to the door
    add('n054', shots.card('text', D('n054'), text=tl.by_id['n054']['text'], gold_words=['first']), zoom=(1.0, 1.02))
    dend = tl.dur('n055', 'end')
    def sub(c, t):
        P.subscribe_button(c, 960, 800, 1.25, u=K(t, .5, .5), click=K(t, dend - 3.0, 1.0))
    S.append(dict(name='n055', dur=dend, draw=wide('night/nasdaq_tower', t0=at('n055'), amb=[('gold_dust', dict(n=40, region=(0, 0, 1920, 760)))]), hud=sub, zoom=(1.0, 1.12), focus=((960, 540), (960, 480)),
                  sfx=[(dend - 2.5, 'pickup'), (dend - 2.4, 'ding')]))
    return S
