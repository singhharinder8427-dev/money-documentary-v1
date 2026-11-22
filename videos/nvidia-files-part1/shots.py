"""Shot list - The Nvidia Files, Part 1 (full video: hook, title, CH1-CH5, twist, ending, subscribe-for-Part-2 card).
Night print. Follows shot_plan_ch1.md. Only LOCKED assets (ASSET_LIBRARY.md). Applies FIXES.md: start close, vary angles,
new picture every 2-3 s, a visual beat every 20-30 s, name + role lower-thirds (standing rule), moving camera.
QA: make_video.py qa (3 frames per shot, real camera) before every render (CLAUDE.md 4b)."""
import math, skia
from engine import shots, widgets as Wd, anim as A, kit, props
from engine.actor import Actor
from engine.cast import person
from engine.core import W, H, GOLD, ORANGE, WHITE, NAVY, NAVY2, PAPER, F_LABEL, F_TYPE, F_TITLE
from engine.kit import rect, label, fp, ease, ease_out, K
from engine.sets import get_set

NG = '#76B900'                                                    # Nvidia brand green (CLAUDE.md rule 3b)
import json as _json, pathlib as _pl
_SCRIPT = _json.load(open(_pl.Path(__file__).resolve().parent / 'script.json'))
SHOT_BREAKS = tuple(l['id'] for l in _SCRIPT['lines'])          # every line starts its own picture
NR = '#9FB8F0'

def build(tl):
    S = []; at = tl.at; mouths = tl.mouths()
    order = [l['id'] for l in tl.lines]
    def nxt(lid):
        i = order.index(lid); cands = [e for e in tl.events if e['t0'] > tl.start(lid) + .01]
        nl = order[i + 1] if i + 1 < len(order) else None
        ev = min(cands, key=lambda e: e['t0']) if cands else None
        if ev and (nl is None or ev['t0'] < at(nl)): return f"chapter:{ev['n']}" if ev['kind'] == 'chapter' else ev['kind']
        return nl
    def add(lid, draw, **kw): S.append(dict(name=lid, dur=tl.dur(lid, nxt(lid)), draw=draw, **kw))
    def multi(lid, parts):
        """One line, several pictures: parts = [(fraction, mk), ...]; mk(t0) -> dict(draw=..., **shot kwargs)."""
        d = tl.dur(lid, nxt(lid)); t = at(lid); tot = sum(f for f, _ in parts)
        for i, (f, mk) in enumerate(parts):
            dd = d * f / tot; S.append(dict(name=lid if i == 0 else f'{lid}_{i + 1}', dur=dd, **mk(t))); t += dd
    def chapter(n, title): card_shot(f'chapter:{n}', shots.card('chapter', 2.2, n=n, title=title))
    def two(lid, f, mk_a, mk_b, **kw):
        """One line, TWO pictures: the first f of the line, then the rest. mk_x(t0) -> dict(draw=..., **shot kwargs)."""
        d = tl.dur(lid, nxt(lid)); t0 = at(lid)
        a = mk_a(t0); b = mk_b(t0 + d * f)
        S.append(dict(name=lid, dur=d * f, **a)); S.append(dict(name=lid + '_2', dur=d * (1 - f), **b))
    def card_shot(marker, draw, **kw): S.append(dict(name=marker.replace(':', ''), dur=tl.dur(marker, nxt_ev(marker)), draw=draw, **kw))
    def nxt_ev(marker):
        t0 = at(marker); later = [l for l in order if at(l) > t0 + .01]; ev = [e for e in tl.events if e['t0'] > t0 + .01]
        c1 = at(later[0]) if later else 1e9; c2 = min((e['t0'] for e in ev), default=1e9)
        if c2 < c1: return f"chapter:{min(ev, key=lambda e: e['t0'])['n']}" if min(ev, key=lambda e: e['t0'])['kind'] == 'chapter' else min(ev, key=lambda e: e['t0'])['kind']
        return later[0] if later else 'end'
    def say(a, lid): return a.say(tl, lid, mouths)
    D = lambda lid: tl.dur(lid, nxt(lid))
    shake = lambda hit: A.stamp_shake(hit)

    _stage_cache = {}
    def _stage_img(kind):
        if kind not in _stage_cache:
            if kind == 'desk':   # drawn directly (the set pipeline's night print turned the wood into grey blobs)
                import random as _r
                surf = skia.Surface(W, H); cv = surf.getCanvas(); rnd = _r.Random(7); cv.drawRect(skia.Rect(0, 0, W, H), fp('#4A3424'))
                for i in range(0, H, 12):
                    y = i + rnd.uniform(-2, 2); cv.drawLine(0, y, W, y + rnd.uniform(-5, 5), kit.ink(rnd.choice((2, 3)), rnd.choice(('#3C2A1D', '#57402C', '#45311F')), 170))
                p = skia.Paint(); p.setShader(skia.GradientShader.MakeRadial((900, 460), 1000, [skia.Color(255, 205, 140, 60), skia.Color(0, 0, 0, 0)])); cv.drawRect(skia.Rect(0, 0, W, H), p)
                v = skia.Paint(); v.setShader(skia.GradientShader.MakeRadial((960, 540), 1150, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(8, 12, 28, 220)], [0, .5, 1])); cv.drawRect(skia.Rect(0, 0, W, H), v)
                cv.drawCircle(170, 930, 64, kit.ink(9, '#2A1B12', 150)); rect(cv, 1500, 860, 1740, 882, GOLD, 4, r=10)
                _stage_cache[kind] = surf.makeImageSnapshot()
            else:
                base = get_set(kind).base; surf = skia.Surface(W, H); cv = surf.getCanvas(); p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(14, 14))
                cv.save(); cv.translate(960, 540); cv.scale(1.25, 1.25); cv.translate(-960, -540); cv.drawImage(base, 0, 0, skia.SamplingOptions(), p); cv.restore()
                cv.drawRect(skia.Rect(0, 0, W, H), fp('#0A1226', 120)); _stage_cache[kind] = surf.makeImageSnapshot()
        return _stage_cache[kind]
    def plain(overlay, framed=True):
        """shots.plain, but the backdrop can be swapped per shot after build (STAGES below): a clean desk for documents,
        a blurred real room for charts / counters / newspapers."""
        base = shots.plain(overlay, framed=framed)
        def draw(c, t):
            st = getattr(draw, 'stage', None)
            if st: c.drawImage(_stage_img(st), 0, 0); overlay(c, t)
            else: base(c, t)
        return draw
    # ---- year-flip calendar (custom: the engine calendar counts days, we need years) ----
    def year_cal(c, x, y, t, y0, y1, dur, s=1.5, label_txt='YEAR'):
        k = K(t, 0, dur); yr = int(round(y0 + (y1 - y0) * ease(k)))
        c.save(); c.translate(x, y); c.scale(s, s)
        rect(c, -180, -200, 180, 220, PAPER, 6, r=10); rect(c, -180, -200, 180, -110, NAVY, 6, r=10)
        Wd.text(c, label_txt, 0, -140, 42, WHITE, F_LABEL, 'center'); Wd.text(c, str(yr), 0, 120 if yr < 100 else 100, 150 if yr < 100 else 96, NAVY, F_TITLE, 'center')
        for i in range(2): kit.circ(c, -90 + i * 180, -200, 14, '#8C93A6', 4)
        ph = (t * 7) % 1.0
        if 0 < k < 1 and ph > .08: c.save(); c.translate(120 + ph * 160, -40 - ph * 120); c.rotate(ph * 40); c.scale(.55 * (1 - ph * .6), .55 * (1 - ph * .6)); rect(c, -150, -120, 150, 150, PAPER, 4); c.restore()
        c.restore()

    HUDPOP = lambda txt, x, y, t0, col=GOLD, size=110, rot=-4: (lambda c, t: Wd.pop_label(c, txt, x, y, (t - t0) / .4, col, size, rot=rot))   # screen-space pop label (never cropped by the camera)
    def both(*fs): return lambda c, t: [f(c, t) for f in fs]

    # ---- shared little drawings for the hook and later chapters ----
    _cache = {}
    def silhouette(who, x, y, sc, key):
        """A character as a soft dark shape behind frosted glass (cached)."""
        if key not in _cache:
            surf = skia.Surface(W, H); cv = surf.getCanvas(); Actor(who, x, y, sc, rim=NR).draw(cv, 1.0); img = surf.makeImageSnapshot()
            s2 = skia.Surface(W, H); c2 = s2.getCanvas(); p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(22, 22))
            p.setColorFilter(skia.ColorFilters.Blend(skia.Color(10, 16, 36), skia.BlendMode.kSrcIn)); c2.drawImage(img, 0, 0, skia.SamplingOptions(), p)
            _cache[key] = s2.makeImageSnapshot()
        return _cache[key]
    def smartphone(c, x, y, t, caller='BLOOMBERG', s=1.0, ring=True, icon='B'):
        """Modern phone, incoming call screen (navy/gold), buzzing while it rings."""
        bz = math.sin(t * 70) * 5 * (ring and int(t * 2.2) % 2 == 0)
        c.save(); c.translate(x + bz, y); c.scale(s, s); c.rotate(-4)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-210, -400, 230, 420), 50, 50), fp((0, 0, 0), 100, blur=24))
        rect(c, -220, -410, 220, 410, '#1B1D26', 8, r=48); rect(c, -196, -370, 196, 370, NAVY, 3, r=22)
        c.drawCircle(0, -120, 120 + 30 * ((t * 1.4) % 1), fp(GOLD, int(80 * (1 - (t * 1.4) % 1)), blur=10))
        kit.circ(c, 0, -120, 90, '#24365E', 5); Wd.text(c, icon, 0, -88, 96, GOLD, F_TITLE, 'center')
        Wd.text(c, 'INCOMING CALL', 0, 40, 34, '#9DB0DA', F_LABEL, 'center'); Wd.text(c, caller, 0, 110, 66, WHITE, F_LABEL, 'center')
        kit.circ(c, -100, 270, 48, ORANGE, 5); kit.circ(c, 100, 270, 48, GOLD, 5)
        c.restore()
    def big_door(c, t, close_at=.5, plate='CEO'):
        """Tall boardroom door that swings shut (perspective squeeze), brass plate, light spill disappearing."""
        k = ease(K(t, 0, close_at)); rect(c, 560, 90, 1360, 1080, '#0F1A38', 8)                       # door frame / dark room
        c.drawRect(skia.Rect(600, 120, 1320, 1080), fp('#FFD27A', int(150 * (1 - k)), blur=30))       # warm light inside
        w = 720 * (.18 + .82 * k); x0 = 600
        p = skia.Path(); p.moveTo(x0, 120); p.lineTo(x0 + w, 120 + 40 * (1 - k)); p.lineTo(x0 + w, 1080 - 40 * (1 - k)); p.lineTo(x0, 1080); p.close()
        c.drawPath(p, fp('#5A3B24')); c.drawPath(p, kit.ink(7))
        if k > .6:
            for yy in (220, 620): rect(c, x0 + 60, yy, x0 + w - 60, yy + 320, None, 5, v='#3E2816')
            pw = max(110, len(plate) * 13 + 30); rect(c, x0 + w / 2 - pw, 160, x0 + w / 2 + pw, 210, GOLD, 4, r=6); Wd.text(c, plate, x0 + w / 2, 200, 36, NAVY, F_LABEL, 'center')
        kit.circ(c, x0 + w - 50, 640, 18, GOLD, 4)

    # ================= HOOK =================
    # 1-2  n001  a phone buzzing in the dark office (Bloomberg calling) -> Jensen picks up behind his desk
    def n001a(t0): return dict(draw=shots.wide('night/office', [], overlay=lambda c, t: smartphone(c, 960, 560, t, s=.92)), zoom=(1.12, 1.02), focus=((960, 560), (960, 540)),
                               hud=lambda c, t: Wd.place_tag(c, 'Oct 29, 2026', (t - .3) / .4, 'a call with Bloomberg'), sfx=[(0, 'ring', 4.0)])
    jh = Actor('jensen', 930, 950, 1.08, face=-.2, rim=NR).pose(.15, ('phone', 'down')).expression(0, mouth='smile', eyes='dot')
    def n001b(t0): return dict(draw=shots.wide('night/office', [jh], t0=t0), zoom=(1.15, 1.35), focus=((900, 640), (930, 560)),
                               hud=lambda c, t: Wd.lower_third(c, 'Jensen Huang', 'Nvidia CEO', (t - .2) / .5), sfx=[(.15, 'pickup')])
    multi('n001', [(.45, n001a), (.55, n001b)])

    # 3-4  n002  the newspaper spins in (headline hidden), then a push onto the blurred headline
    def paper(c, t, push=False):
        A.newspaper(c, 960, 540, t if not push else 9, 'The New York Times', ' ', None)
        for i, w_ in enumerate((900, 760, 840)):                                              # headline kept blurred (not shown)
            c.drawRoundRect(skia.Rect(960 - w_ / 2, 400 + i * 100, 960 + w_ / 2, 470 + i * 100), 12, 12, fp(NAVY, 200 if t > .7 or push else 0, blur=10))
    def n002a(t0): return dict(draw=plain(lambda c, t: paper(c, t)), zoom=(1.0, 1.08), sfx=[(.05, 'whoosh'), (.7, 'stamp')], shake=shake(.7))
    def n002b(t0): return dict(draw=plain(lambda c, t: paper(c, t, True)), zoom=(1.5, 1.7), focus=((960, 480), (960, 440)), hud=HUDPOP('a woman close to him', 960, 960, .4, GOLD, 90, -2))
    multi('n002', [(.45, n002a), (.55, n002b)])

    # 5  n003  HUANG (real on-record quote, Bloomberg Oct 29): close-up, calm smile, phone at the ear
    jq = say(Actor('jensen', 960, 1390, 2.15, face=-.3, rim=NR).pose(0, ('phone', 'down')).expression(0, mouth='smirk', eyes='half'), 'n003')
    add('n003', shots.closeup('night/office', jq, focus=(1250, 560), t0=at('n003')), zoom=(1.0, 1.06),
        hud=lambda c, t: Wd.text(c, 'ON THE RECORD - BLOOMBERG, OCT 29', 1880, 70, 34, '#9DB0DA', F_LABEL, 'right'))

    # 6-7  n004  ten days later: tear-off calendar, then the note to employees slides out of an envelope
    def n004a(t0): return dict(draw=plain(lambda c, t: year_cal(c, 960, 520, t, 0, 10, 1.2, s=1.5, label_txt='DAYS LATER')), zoom=(1.0, 1.1), sfx=[(0, 'flips', 1.2)])
    def n004b(t0): return dict(draw=plain(lambda c, t: A.envelope(c, 960, 700, t, 'To: all employees', ['Nov 8, 2026', 'From: Jensen'])), zoom=(1.05, 1.2), focus=((960, 600), (960, 460)), sfx=[(.4, 'paper')])
    multi('n004', [(.45, n004a), (.55, n004b)])

    # 8  n005  card (real quote from his Nov 8 note)
    add('n005', shots.card('text', D('n005'), text=tl.by_id['n005']['text'], gold_words=['unfaithful']), zoom=(1.0, 1.03))

    # 9-10  n006  the boardroom door slams shut; the $4 trillion counter
    def n006a(t0): return dict(draw=plain(lambda c, t: big_door(c, t, .7)), zoom=(1.2, 1.05), focus=(960, 560), sfx=[(.7, 'stamp')], shake=shake(.7),
                               hud=HUDPOP('he is out', 1500, 300, .8, WHITE, 100, -4))
    staff = [Actor('analyst', 400, 1010, 1.0, face=.5, rim=NR).expression(0, eyes='wide', mouth='o', brow=.5).pose(.6, ('cheer', 'down')),
             Actor('worker', 1550, 1010, 1.0, face=-.5, rim=NR).expression(0, eyes='wide', mouth='open').pose(.9, ('down', 'cheer')),
             Actor('jensen', 960, 1040, 1.05, face=0, rim=NR).expression(0, mouth='smile', eyes='dot').pose(.4, ('hip', 'down'))]
    def screen_chart(c, t):
        props.nvidia_logo(c, 760, 175, .45)
        e = K(t, .1, 1.6); pts = [(700 + i * 53, 470 - (i / 10) ** 1.7 * 280) for i in range(11)]; n = max(2, int(2 + 9 * ease(e)))
        p = skia.Path(); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:n]]; c.drawPath(p, kit.ink(9, NG))
        Wd.counter(c, 900, 285, 0, 4_000_000_000_000, (t - .1) / 1.6, label='', size=34, panel=True)
    def n006b(t0): return dict(draw=shots.wide('night/nvidia_office', [], staff, overlay=screen_chart, t0=t0), zoom=(1.0, 1.12), focus=((960, 560), (960, 420)), sfx=[(.2, 'tick'), (1.8, 'ding')],
                               hud=lambda c, t: (Wd.pop_label(c, 'first company ever worth $4 trillion', 960, 120, (t - 1.2) / .4, GOLD, 70, rot=-2), Wd.lower_third(c, 'Jensen Huang', 'Nvidia co-founder', (t - 1.8) / .5)))
    multi('n006', [(.42, n006a), (.58, n006b)])

    # 11-12  n007  a woman's silhouette behind frosted glass; closer, her name withheld
    def frosted(c, t, close=False):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#5A72A8'))
        [c.drawImage(silhouette('alice', 960, 1080, 1.4, 'alice_sil'), 20 * math.sin(t * .8), 0) for _ in range(3)]
        rect(c, 300, 40, 1620, 1040, None, 10, v='#2E4A7E'); c.drawRect(skia.Rect(300, 40, 1620, 1040), fp('#C9D3EA', 18))
        for i in range(14): c.drawLine(300, 80 + i * 70, 1620, 80 + i * 70, kit.ink(2, '#C9D3EA', 30))
        c.drawRect(skia.Rect(300, 40, 1620, 1040), fp('#FFFFFF', int(20 + 10 * math.sin(t * 3))))
    def n007a(t0): return dict(draw=plain(lambda c, t: frosted(c, t), framed=False), zoom=(1.0, 1.12), focus=(960, 560), hud=HUDPOP('reportedly', 1500, 260, .6, GOLD, 90, -4))
    def n007b(t0): return dict(draw=plain(lambda c, t: frosted(c, t), framed=False), hud=lambda c, t: Wd.stamp(c, 'Name withheld', 960, 800, t - .5, GOLD, rot=-6, size=80),
                               zoom=(1.35, 1.55), focus=(960, 520), sfx=[(.5, 'stamp')], shake=shake(.5))
    multi('n007', [(.5, n007a), (.5, n007b)])

    # 13  n008  card + UNPROVEN stamp (pale navy-white, not orange)
    def n008(c, t):
        Wd.text_card(c, tl.by_id['n008']['text'], max(t - .3, 0), ['charged.', 'groundless.'], dur=D('n008'))
        Wd.stamp(c, 'Unproven', 1480, 860, t - D('n008') * .7, GOLD, rot=-8, size=90)
    add('n008', n008, zoom=(1.0, 1.03), sfx=[(D('n008') * .7, 'stamp')], shake=shake(D('n008') * .7))

    # 14-15  n009  a 401(k) statement slides in; a gold coin flips onto it
    def stmt(c, t):
        Wd.document(c, 960, 560, '401(k) statement', ['Retirement account', 'Index fund ....... 72%', 'Bond fund ........ 28%'], t, w=900, h=620, rot=-2)
    def coin_flip(c, t):
        stmt(c, 9); k = ease_out(K(t, .1, .6)); sq = abs(math.cos(t * 9)) if t < .7 else 1
        c.save(); c.translate(1400, 420 - (1 - k) * 600); c.scale(3.0 * max(sq, .08), 3.0); Wd.coin(c, 0, 0, 40); c.restore()
    def n009a(t0): return dict(draw=plain(stmt), zoom=(1.0, 1.1), sfx=[(.1, 'paper')])
    def n009b(t0): return dict(draw=plain(coin_flip), zoom=(1.1, 1.3), focus=((1000, 540), (1200, 480)), sfx=[(.7, 'coin')], hud=HUDPOP('your retirement', 760, 960, .5, GOLD, 90, -2))
    multi('n009', [(.45, n009a), (.55, n009b)])

    # 16  n010  card, then the title card
    add('n010', shots.card('text', D('n010'), text=tl.by_id['n010']['text'], gold_words=['she?', 'AI?']), zoom=(1.0, 1.03))
    card_shot('title', shots.card('title', 2.5, title='Who is Alice Huang?', gold_word='Huang', sub='The Nvidia Files - Part 1'))

    chapter(1, 'Out of Nowhere')
    # ================= CH1 "Out of Nowhere" =================
    def crowd(c, t, press, n=9):
        """Dark silhouette crowd at the bottom of the frame that presses in towards the centre (press 0..1)."""
        for i in range(n):
            side = -1 if i % 2 else 1; k = (i // 2) / max(n // 2, 1)
            x = 960 + side * (780 - 300 * press * (1 - .3 * k) - k * 260); y = 1090 - 20 * math.sin(t * 3 + i) ** 2
            sc = 1.0 + .08 * k
            c.drawOval(skia.Rect(x - 70 * sc, y - 250 * sc, x + 70 * sc, y + 60 * sc), fp('#0A1126'))
            c.drawCircle(x, y - 290 * sc, 60 * sc, fp('#0A1126')); c.drawCircle(x, y - 290 * sc, 60 * sc, kit.ink(4, '#1E2B52'))

    # 1  n011  Rewind to 2023, Singapore: whip-pan in, low push, year calendar flips back (big, centre-right, fully on screen)
    add('n011', shots.wide('night/sg_street', [], overlay=lambda c, t: (year_cal(c, 1350, 700, t, 2026, 2023, D('n011') * .8, s=1.05),)),
        zoom=(1.0, 1.12), focus=((760, 640), (1000, 620)), whip_in=True, sfx=[(.05, 'whoosh'), (0, 'flips', D('n011') * .8)],
        hud=lambda c, t: Wd.place_tag(c, 'Singapore', (t - .3) / .4, '2023'))

    # 2-3  n012  Megaspeed reborn: sign drops slowly into the blank frame with a bounce + flash, then lights up; close flicker
    def sign_drop(c, t):
        k = K(t, .15, 1.0); e = ease_out(k); bounce = (math.exp(-(t - 1.15) * 7) * math.sin((t - 1.15) * 24) * 14) if t > 1.15 else 0
        y = 380 - (1 - e) * 560 + bounce; glow = K(t, 1.2, .5) * (.75 + .25 * math.sin(t * 14))
        props.sign_megaspeed(c, 960, y, .88, glow=glow)
        if 1.15 < t < 1.6: c.drawCircle(960, 380, 120 + 700 * (t - 1.15), fp(GOLD, int(70 * (1 - (t - 1.15) / .45)), blur=30))     # landing flash
    def n012a(t0): return dict(draw=shots.wide('night/sg_street', [], overlay=sign_drop), zoom=(1.0, 1.25), focus=((960, 480), (960, 440)), sfx=[(.2, 'whoosh'), (1.15, 'stamp')], shake=shake(1.15))
    def n012b(t0): return dict(draw=shots.wide('night/sg_street', [], overlay=lambda c, t: props.sign_megaspeed(c, 960, 380, .88, glow=.8 + .2 * math.sin(t * 16))),
                               zoom=(1.9, 1.7), focus=((960, 420), (960, 360)), hud=HUDPOP('reborn', 1450, 860, .3, GOLD, 130))
    two('n012', .5, n012a, n012b)

    # 4-5  n013  Before: the old game-company sign hangs, shudders, unscrews and falls; then a worker walks through the new office
    def old_sign(c, t):
        sway = math.sin(t * 9) * 3 * (1 - K(t, .3, .6)); k = K(t, .75, .8)
        props.sign_old_arcade(c, 960 - 40 * k, 380 + 640 * k ** 2, .88, hanging=-3 + sway - 55 * k)
        if k > 0 and k < .55: [c.drawCircle(960 + 90 * math.cos(i), 400 + 40 * i + 30 * k, 6 + 3 * i, fp('#B9BFCF', 160)) for i in range(5)]
    def n013a(t0): return dict(draw=shots.wide('night/sg_street', [], overlay=old_sign), zoom=(1.7, 1.45), focus=(960, 420), sfx=[(.3, 'paper'), (1.2, 'stamp')], shake=shake(1.5),
                               hud=HUDPOP('a game company', 960, 190, .1, WHITE, 74, -2))
    w2 = Actor('worker', 1500, 1000, 1.0, face=-.6, rim=NR).pose(0, ('hold', 'hold')).walk_to(0, D('n013') * .5, 600)
    def n013b_(t0): return dict(draw=shots.wide('night/megaspeed', [], [w2], overlay=lambda c, t: props.sign_megaspeed(c, 960, 240, .85, glow=.9), t0=t0),
                                zoom=(1.0, 1.15), focus=((1300, 600), (700, 600)), sfx=[(0, 'steps', D('n013') * .45)])
    two('n013', .55, n013a, n013b_)

    # 6-7  n013b  certificate spins onto a clean stage (NOT the old Ponzi desk), REPORTED stamp, then the green chip flies in
    def cert(c, t):
        k = K(t, .15, .7); e = ease_out(k); props.certificate(c, 960 + (1 - e) * 1100, 520 - (1 - e) * 80 + 8 * math.sin(t * 2.5), 1.9, rot=-6 + (1 - e) * 40)
    def cert2(c, t):
        k = K(t, .1, .6); e = ease_out(k); props.certificate(c, 760, 560, 1.7, rot=-5 + 1.5 * math.sin(t * 2))
        props.chip(c, 1500 + (1 - e) * 700, 430, 1.9, rot=12 - (1 - e) * 120, glow=.6 + .3 * math.sin(t * 6), accent=NG)
    two('n013b', .55, lambda t0: dict(draw=plain(cert), hud=lambda c, t: Wd.stamp(c, 'Reported', 1560, 900, t - 1.7, GOLD, rot=-8, size=84), zoom=(1.0, 1.1), rot=(2, -1), sfx=[(.25, 'paper'), (1.7, 'stamp')], shake=shake(1.7)),
        lambda t0: dict(draw=plain(cert2), zoom=(1.05, 1.25), focus=((900, 540), (1100, 500)), hud=HUDPOP('official partner?', 960, 190, .6, GOLD, 96, -2), sfx=[(.3, 'whoosh')]))

    # 8-9  n014  data-center aisle: dolly in with light pulses running down the aisle; then the glowing chip with orbiting chips
    def pulses(c, t):
        for i in range(6):
            z = (t * .55 + i / 6) % 1.0; y = 500 + 520 * z ** 2; r = 30 + 330 * z ** 2; a = int(120 * math.sin(z * math.pi))
            c.drawOval(skia.Rect(960 - r * 1.6, y - r * .25, 960 + r * 1.6, y + r * .25), fp(GOLD, a, blur=18, blend=skia.BlendMode.kPlus))
    def chipscene(c, t):
        for i in range(4):
            a = t * 1.3 + i * 1.57; props.chip(c, 960 + math.cos(a) * 560, 520 + math.sin(a) * 250, .85, rot=math.degrees(a), glow=.3, accent=NG)
        props.chip(c, 960, 520, 3.0 + .08 * math.sin(t * 5), glow=.6 + .4 * math.sin(t * 5), accent=NG)
        c.drawCircle(960, 520, 200 + 260 * ((t * .8) % 1), fp(NG, int(60 * (1 - (t * .8) % 1)), blur=20))
    two('n014', .55, lambda t0: dict(draw=shots.wide('night/datacenter', [], overlay=pulses), zoom=(1.0, 1.5), focus=(960, 540), sfx=[(.2, 'whoosh'), (0, 'amb:hum', None)], hud=HUDPOP('rent computing power', 960, 190, .9, WHITE, 70, 0)),
        lambda t0: dict(draw=plain(chipscene), zoom=(1.0, 1.12), hud=HUDPOP('AI chips', 960, 900, .2, WHITE, 96, 0)))

    # 10-11  n015  chip on velvet with a crowd pressing in; then the hand reaches and the red rope stops it
    def velvet(c, t, reach, press):
        props.velvet_display(c, 960, 950, 1.3, hand_k=reach, glow=1.0); crowd(c, t, press)
    def n015a(t0): return dict(draw=plain(lambda c, t: velvet(c, t, 0.0, K(t, 0, D('n015') * .45))), zoom=(1.0, 1.15), focus=(960, 560), sfx=[(0, 'amb:murmur', None)])
    def n015b_(t0): return dict(draw=plain(lambda c, t: velvet(c, t, .58 * ease(K(t, .2, .8)) - .12 * ease(K(t, 1.15, .4)) + .02 * math.sin(max(t - 1.15, 0) * 30) * math.exp(-max(t - 1.15, 0) * 5), 1.0)),
                                zoom=(1.0, 1.2), focus=((960, 560), (1100, 520)), sfx=[(1.1, 'stamp')], shake=shake(1.1), hud=HUDPOP('not everyone', 960, 190, .3, GOLD, 100, -3))
    two('n015', .45, n015a, n015b_)

    # 12-13  n015b  Jensen Huang, 1993 (grey hair) in the diner; the wall calendar flips to 2026 (camera keeps his head clear of it)
    j93 = say(Actor('jensen93', 800, 1010, 1.1, face=.3, rim=NR).pose(.3, ('chin', 'down')).expression(0, mouth='smile', eyes='dot'), 'n015b')
    def n015ba(t0): return dict(draw=shots.wide('night/diner93', [j93], t0=t0), zoom=(1.6, 1.25), focus=((820, 640), (900, 620)),
                                hud=lambda c, t: Wd.lower_third(c, 'Jensen Huang', 'Nvidia co-founder, 1993', (t - .3) / .5))
    def n015bb(t0): return dict(draw=shots.wide('night/diner93', [j93], overlay=lambda c, t: year_cal(c, 750, 235, t, 1993, 2026, D('n015b') * .35, s=.52, label_txt='YEAR'), t0=t0),
                                zoom=(1.0, 1.15), focus=(960, 540), sfx=[(0, 'flips', D('n015b') * .35)], hud=HUDPOP('33 years', 1450, 880, .4, GOLD, 120, -4))
    two('n015b', .5, n015ba, n015bb)

    # 14-15  n016  Alice first appears (alleged); two attributed cards slam in and keep drifting
    al = say(Actor('alice', 960, 1000, 1.0, face=.0, rim=NR).expression(0, mouth='flat', eyes='dot').pose(.3, ('down', 'hip')), 'n016')
    def n016a(t0): return dict(draw=shots.wide('night/megaspeed', [al], overlay=lambda c, t: props.sign_megaspeed(c, 960, 240, .85, glow=.9), t0=t0),
                               zoom=(1.5, 1.2), focus=((960, 600), (960, 500)), hud=lambda c, t: Wd.lower_third(c, 'Alice Huang (alleged)', 'then-CEO, Megaspeed', (t - .3) / .5))
    def n016b(t0): return dict(draw=plain(lambda c, t: (Wd.paper_card(c, 520, 560 + 8 * math.sin(t * 2), 'U.S. reports', ['Chinese national'], t, w=700, h=480, rot=-4 + math.sin(t * 1.5), slam=True),
                                                             Wd.paper_card(c, 1400, 560 + 8 * math.sin(t * 2 + 1), 'Singapore says', ['Hong Kong resident'], t - .8, w=700, h=480, rot=4 + math.sin(t * 1.7), slam=True),
                                                             Wd.stamp(c, 'Attributed', 960, 900, t - 1.8, GOLD, rot=-6, size=90))),
                               zoom=(1.0, 1.12), sfx=[(.2, 'stamp'), (1.0, 'stamp'), (1.9, 'stamp')], shake=shake(1.9))
    two('n016', .4, n016a, n016b)

    # 16  n017  two HUANG tags fly in from the sides, big on screen; the equals sign is crossed out with a hit
    def tags(c, t):
        d = D('n017'); k = ease_out(K(t, 0, .5)); c.save(); c.translate(0, 0)
        c.translate(960, 540); c.scale(1.35, 1.35); c.translate(-960, -540); props.tag_pair(c, 960, 540 + 6 * math.sin(t * 2.5), k, K(t, d * .45, .35)); c.restore()
    add('n017', plain(tags), zoom=(1.0, 1.1), focus=(960, 540), shake=shake(D('n017') * .55), sfx=[(.1, 'whoosh'), (D('n017') * .55, 'stamp')])

    # 17  n018  $33 million over the office, big and centred
    add('n018', shots.wide('night/megaspeed', [Actor('alice', 330, 1010, 1.0, face=.4, rim=NR).pose(.2, ('down', 'hip'))],
                           overlay=lambda c, t: (props.sign_megaspeed(c, 960, 240, .85, glow=.9), Wd.counter(c, 1050, 520, 0, 33000000, (t - .1) / 1.4, label='Megaspeed assets, 2023', size=130),), t0=at('n018')),
        zoom=(1.0, 1.15), focus=((900, 600), (1000, 560)), sfx=[(.2, 'tick')])

    # 18  n019  a year later: counter races to $3 billion with a shake; the year calendar flips (kept fully on screen)
    add('n019', shots.wide('night/megaspeed', [], overlay=lambda c, t: (props.sign_megaspeed(c, 960, 240, .85, glow=.9), Wd.counter(c, 960, 470, 33000000, 3000000000, (t - .1) / 1.6, label='a year later', size=112), year_cal(c, 960, 800, t, 2023, 2024, 1.0, s=.7)), t0=at('n019')),
        zoom=(1.0, 1.1), focus=(960, 540), shake=lambda t: (math.sin(t * 60) * 8 * K(t, .1, .1) * (1 - K(t, .8, 1.2)), math.cos(t * 53) * 6 * K(t, .1, .1) * (1 - K(t, .8, 1.2))),
        sfx=[(.2, 'tick'), (0, 'flips', 1.0), (1.7, 'ding')])

    # 18-20  n020 / n020b / n020c  dramatised dialogue: analyst, investor, analyst
    an = say(Actor('analyst', 960, 1390, 2.15, face=.4, rim=NR).expression(0, eyes='wide', mouth='o', brow=.6).pose(.2, ('down', 'chin')), 'n020')
    add('n020', shots.closeup('night/megaspeed', an, focus=(700, 560), t0=at('n020')), zoom=(1.0, 1.06), hud=lambda c, t: Wd.lower_third(c, 'The Analyst', 'Dramatised', (t - .3) / .5))
    inv = say(Actor('investor', 960, 1390, 2.15, face=-.4, rim=NR, spec=person('investor', suit='#7A1E2A', suit_d='#5E1620', outfit='open')).expression(0, eyes='half', mouth='smile').pose(.2, ('hold', 'shrug')), 'n020b')
    add('n020b', shots.closeup('night/megaspeed', inv, focus=(1250, 560), t0=at('n020b')), zoom=(1.0, 1.05), hud=lambda c, t: Wd.lower_third(c, 'The Investor', 'Dramatised', (t - .3) / .5))
    an2 = say(Actor('analyst', 960, 1390, 2.15, face=-.5, rim=NR).expression(0, eyes='half', mouth='flat', brow=.5, brow_tilt=.4), 'n020c')
    add('n020c', shots.closeup('night/megaspeed', an2, focus=(1250, 520), t0=at('n020c'), zoom=1.8), zoom=(1.12, 1.0), sfx=[(D('n020c') * .6, 'pop')])

    # 21  n021  Tufts professor: big close-up, the sticky note slaps on beside him (screen-sized, marked as his OPINION)
    pr = say(Actor('professor', 700, 1390, 2.15, face=.5, rim=NR).pose(.3, ('present', 'hip')).expression(0, mouth='flat'), 'n021')
    add('n021', shots.closeup('night/office', pr, focus=(700, 560), overlay=lambda c, t: Wd.sticky(c, 'Appeared out of nowhere (his opinion)', 1450 + 6 * math.sin(t * 2), 470, (t - 1.0) / .4, rot=-5, w=480), t0=at('n021')),
        zoom=(1.0, 1.08), hud=lambda c, t: Wd.lower_third(c, 'The Professor', 'Tufts University', (t - .3) / .5), sfx=[(1.0, 'pop')])

    # 22-23  n022  Dec 7, 2023: restaurant candle close, then a flash and a polaroid labelled REPORTED
    jn = Actor('jensen', 760, 1060, 1.18, face=.3, rim=NR).expression(0, mouth='smile', eyes='dot')
    ai = Actor('alice', 1160, 1060, 1.18, face=-.3, rim=NR).expression(0, mouth='smile', eyes='dot')
    def n022a(t0): return dict(draw=shots.wide('night/restaurant', [jn, ai], t0=t0), zoom=(1.55, 1.25), focus=((960, 640), (960, 600)), sfx=[(0, 'amb:murmur', None)],
                               hud=lambda c, t: Wd.place_tag(c, 'Singapore', (t - .2) / .4, 'Dec 7, 2023'))
    def photo(c, t):
        st = get_set('night/restaurant'); s = skia.Surface(W, H); cv = s.getCanvas()
        st.draw(cv, [lambda c_, a=a: a.draw(c_, 1.0) for a in (jn, ai)]); img = s.makeImageSnapshot()
        Wd.polaroid(c, img, K(t, .05, 1.2), caption='REPORTED')
    def n022b(t0): return dict(draw=plain(photo, framed=False), zoom=(1.0, 1.04), sfx=[(.05, 'shutter')],
                               hud=lambda c, t: (Wd.lower_third(c, 'Jensen Huang', 'Nvidia CEO', (t - 1.0) / .5, y=150, x=60), Wd.lower_third(c, 'Alice Huang (alleged)', 'then-CEO, Megaspeed', (t - 1.3) / .5, y=150, x=1040)))
    two('n022', .45, n022a, n022b)

    # 24-25  n023  Malaysia, Sept 2024: the inspector walks the long aisle, then crates appear
    ins = Actor('inspector', 960, 700, .5, face=.0, rim=NR).pose(0, ('hold', 'down')).walk_to(0, D('n023') * .55, 960, 1010)
    ins.s = .5
    def n023a(t0): return dict(draw=shots.wide('night/datacenter', [ins], overlay=lambda c, t: props.flashlight(c, 960, 640 + 300 * K(t, 0, D('n023') * .55 / 1), 90 + 14 * math.sin(t * 2), 520, 200, .7), t0=t0),
                               zoom=(1.0, 1.35), focus=(960, 620), sfx=[(0, 'steps', D('n023') * .5), (0, 'amb:hum', None)], hud=lambda c, t: (Wd.place_tag(c, 'Malaysia', (t - .2) / .4, 'Sept 2024'), Wd.lower_third(c, 'The Inspector', 'U.S. official, dramatised', (t - .6) / .5)))
    def n023b(t0): return dict(draw=shots.wide('night/datacenter', [Actor('inspector', 620, 1010, .95, face=.4, rim=NR).pose(0, ('hold', 'down')), Actor('inspector2', 1280, 1010, .95, face=-.4, rim=NR)],
                                                overlay=lambda c, t: props.crate(c, 960, 840, 1.1, glow=K(t, .3, 1.0)), t0=t0), zoom=(1.0, 1.2), focus=((600, 640), (1200, 640)), sfx=[(0, 'amb:hum', None)])
    def n023m(t0): return dict(draw=lambda c, t: A.map_route(c, t, 1.4, (560, 520), (1360, 470), 'SINGAPORE', 'MALAYSIA', icon='OFFICIAL', flag_a='singapore', flag_b='malaysia'), zoom=(1.0, 1.08), sfx=[(.2, 'whoosh'), (1.3, 'pop')])
    multi('n023', [(.3, n023m), (.4, n023a), (.3, n023b)])

    # 26  n024  inspector asks about the boxes: close-up, then the flashlight lands on the crates
    qi = say(Actor('inspector', 960, 1390, 2.15, face=.4, rim=NR).expression(0, eyes='wide', mouth='o', brow=.4).pose(.2, ('hold', 'point')), 'n024')
    add('n024', shots.closeup('night/datacenter', qi, focus=(1300, 700), overlay=lambda c, t: None if t < .5 else props.flashlight(c, 1515, 708, -10 + 30 * ease(K(t, 0, D('n024'))), 640, 240, .9), t0=at('n024')),
        zoom=(1.0, 1.1), sfx=[(.1, 'whoosh')])
    # 27  n024b  colleague with clipboard: should I take photos?
    cl = say(Actor('inspector2', 960, 1390, 2.15, face=-.4, rim=NR).expression(0, eyes='dot', mouth='smile').pose(.2, ('hold', 'hip')), 'n024b')
    add('n024b', shots.closeup('night/datacenter', cl, focus=(700, 700), t0=at('n024b')), zoom=(1.0, 1.05), hud=lambda c, t: Wd.lower_third(c, 'The Colleague', 'Dramatised', (t - .3) / .5))
    # 28  n024c  "Of every box." flashlight sweeps the crates
    ic = say(Actor('inspector', 760, 1010, .95, face=.5, rim=NR).expression(0, eyes='half', mouth='flat').pose(.2, ('hold', 'point')), 'n024c')
    def sweep(c, t):
        for i, x in enumerate((1000, 1250, 1500)): props.crate(c, x, 900 + (i % 2) * 40, 1.0, glow=.3)
        props.flashlight(c, 900, 760, -20 + 25 * ease(K(t, 0, D('n024c'))), 800, 260, 1.0)
    add('n024c', shots.wide('night/datacenter', [ic], overlay=sweep, t0=at('n024c')), zoom=(1.2, 1.0), focus=((1000, 700), (1250, 700)), sfx=[(.2, 'whoosh')])

    # 29-30  n025  the crate stencil glows gold under the flashlight, then a hard cut to the typed card
    def stencil(c, t):
        props.crate(c, 960, 900, 2.6, glow=min(1, .2 + K(t, .2, .8))); props.flashlight(c, 260, 260, 32, 900, 380, .9)
        c.drawRect(skia.Rect(0, 0, W, H), fp(GOLD, int(40 * K(t, .5, .6) * (1 + math.sin(t * 8)) / 2), blur=0, blend=skia.BlendMode.kPlus))
    d25 = D('n025'); f25 = min(.35, 1.4 / max(d25, .1))
    S.append(dict(name='n025', dur=d25 * f25, draw=shots.wide('night/datacenter', [], overlay=stencil), zoom=(1.3, 1.6), focus=(960, 620), sfx=[(.2, 'whoosh')]))
    S.append(dict(name='n025_2', dur=d25 * (1 - f25), draw=shots.card('text', d25 * (1 - f25), text=tl.by_id['n025']['text'], gold_words=['boxes.'], lead=0.0), zoom=(1.0, 1.02), sfx=[(0, 'stamp')]))

    # ---- helpers for the later chapters ----
    def doc(c, x, y, title, lines, u, hl=None, w=900, h=640, rot=-2, hl_t=.9, label_txt=None):
        """Document that slides in, lines typed, line index `hl` highlighted gold (marker sweep), optional small label."""
        k = kit.back(min(max(u / .35, 0), 1)); c.save(); c.translate(x, y + (1 - k) * 500); c.rotate(rot)
        c.drawRect(skia.Rect(-w / 2 + 14, -h / 2 + 18, w / 2 + 14, h / 2 + 18), fp((0, 0, 0), 80, blur=12)); rect(c, -w / 2, -h / 2, w / 2, h / 2, PAPER, 5)
        Wd.text(c, title.upper(), -w / 2 + 40, -h / 2 + 76, 50, NAVY, F_LABEL); c.drawRect(skia.Rect(-w / 2 + 40, -h / 2 + 98, w / 2 - 40, -h / 2 + 104), fp(NAVY))
        for i, ln in enumerate(lines):
            yy = -h / 2 + 170 + i * 64
            if hl is not None and i == hl and u > hl_t:
                ww = (w - 80) * ease_out(K(u, hl_t, .5)); c.drawRect(skia.Rect(-w / 2 + 32, yy - 40, -w / 2 + 32 + ww, yy + 14), fp(GOLD, 150))
            Wd.text(c, ln[:max(0, int((u - .2) / .6 * 60))] if u < .8 else ln, -w / 2 + 40, yy, 38, NAVY, F_TYPE)
        if label_txt: Wd.text(c, label_txt, w / 2 - 40, h / 2 - 36, 30, '#6B7390', F_LABEL, 'right')
        c.restore()
    def date_cal(c, x, y, t, month, d0, d1, dur, s=1.3, circle_at=None):
        """Tear-off date calendar: month header, day counts d0 -> d1 with pages flying, optional gold circle when it lands."""
        year_cal(c, x, y, t, d0, d1, dur, s=s, label_txt=month)
        if circle_at is not None and t > circle_at:
            e = ease_out(K(t, circle_at, .5)); p = skia.Path(); p.addArc(skia.Rect(x - 150 * s, y - 40 * s, x + 150 * s, y + 210 * s), -90, 360 * e)
            c.drawPath(p, kit.ink(14 * s, GOLD))
    def passport(c, x, y, s=1.0, rot=0.0):
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
        c.drawRect(skia.Rect(-150, -200, 166, 216), fp((0, 0, 0), 90, blur=14)); rect(c, -160, -210, 160, 210, '#1E2A50', 7, r=14)
        kit.circ(c, 0, -30, 70, None, 6, v=GOLD); kit.circ(c, 0, -30, 40, None, 4, v=GOLD); Wd.text(c, 'PASSPORT', 0, 130, 48, GOLD, F_LABEL, 'center')
        c.restore()
    def talk(lid, who, set_name, focus, face, tag=None, role=None, expr=None, pose=('down', 'down'), zoom=(1.0, 1.06), overlay=None, extra_hud=None, sfx=None, spec=None, rim=NR, light=-1):
        """Dialogue close-up with the name + role lower-third (standing rule)."""
        a = say(Actor(who, 960, 1390, 2.15, face=face, rim=rim, light=light, spec=spec).pose(.2, pose).expression(0, **(expr or {})), lid)
        def hud(c, t):
            if tag: Wd.lower_third(c, tag, role, (t - .3) / .5)
            if extra_hud: extra_hud(c, t)
        add(lid, shots.closeup(set_name, a, focus=focus, overlay=overlay, t0=at(lid)), zoom=zoom, hud=hud, **({'sfx': sfx} if sfx else {}))

    # ================= CH2 "Still in the Boxes" =================
    chapter(2, 'Still in the Boxes')
    # n030  US -> China route draws; then the chip
    def n030a(t0): return dict(draw=lambda c, t: A.map_route(c, t, 1.6, (470, 470), (1450, 520), 'UNITED STATES', 'CHINA', icon='CHIPS', flag_a='usa', flag_b='china'), zoom=(1.0, 1.06), sfx=[(.2, 'whoosh')])
    def n030b(t0): return dict(draw=plain(lambda c, t: props.chip(c, 960, 500, 2.6 + .1 * math.sin(t * 4), rot=8 * math.sin(t * 1.5), glow=.8, accent=NG)), zoom=(1.2, 1.0),
                               hud=HUDPOP('chips', 960, 900, .15, GOLD, 140, -3), sfx=[(.15, 'pop')])
    multi('n030', [(.65, n030a), (.35, n030b)])
    # n031  the route stops at the border; BANNED; since Oct 2022
    def banned_map(c, t, d):
        A.map_route(c, min(t, .55 * 1.6), 1.6, (470, 470), (1450, 520), 'UNITED STATES', 'CHINA', icon='CHIPS', flag_a='usa', flag_b='china')
        bk = ease_out(K(t, .9, .3)); c.drawRect(skia.Rect(1130, 300 - 300 * (1 - bk), 1150, 740), fp('#C9D3EA')); c.drawRect(skia.Rect(1130, 300 - 300 * (1 - bk), 1150, 740), kit.ink(4))
    def n031a(t0): return dict(draw=lambda c, t: banned_map(c, t, D('n031')), zoom=(1.0, 1.06), focus=((960, 540), (1000, 530)), sfx=[(.9, 'stamp')], shake=shake(.9),
                               hud=lambda c, t: Wd.stamp(c, 'Banned', 1500, 250, t - 1.2, GOLD, rot=-8, size=100))
    def n031b(t0): return dict(draw=plain(lambda c, t: (date_cal(c, 960, 500, t, 'OCT 2022', 2026, 2022, .8, s=1.2), Wd.pop_label(c, 'most advanced chips', 960, 900, (t - .6) / .4, GOLD, 80, rot=-2))), zoom=(1.0, 1.08), sfx=[(0, 'flips', .8)])
    multi('n031', [(.55, n031a), (.45, n031b)])
    # n032  smugglers keep trying (per DOJ): crates slipping across a dotted border, money rain; handcuffs snap
    def sneak(c, t):
        c.drawLine(960, 120, 960, 980, kit.ink(10, '#9DB0DA')); [c.drawLine(960, y, 960, y + 30, kit.ink(14, '#14213D')) for y in range(120, 980, 60)]
        for i in range(3): props.crate(c, 300 + ((t * 260 + i * 330) % 1400), 820 - i * 170, .7 + i * .08)
        Wd.falling_money(c, t, n=12, area=(200, 0, 1720, 700))
    def n032a(t0): return dict(draw=plain(sneak), zoom=(1.0, 1.08), hud=lambda c, t: (Wd.pop_label(c, "hundreds of millions of dollars' worth", 960, 180, (t - .4) / .4, GOLD, 70, rot=-2),
                                                                                         Wd.text(c, 'PER THE JUSTICE DEPARTMENT', 1880, 1000, 32, '#9DB0DA', F_LABEL, 'right')))
    def n032b(t0): return dict(draw=plain(lambda c, t: props.handcuffs(c, 960, 600, 1.6, close_k=ease_out(K(t, .3, .25)), rot=-6)), zoom=(1.3, 1.1), sfx=[(.5, 'stamp')], shake=shake(.5), hud=HUDPOP('over several years', 960, 900, .7, WHITE, 80, 0))
    multi('n032', [(.6, n032a), (.4, n032b)])
    # n033  Singapore: an officer outside the Megaspeed door; the case file slams down
    off_w = Actor('officer', 400, 905, .6, face=.5, rim=NR, hat=True).walk_to(0, 1.6, 820).pose(1.6, ('hold', 'down'))
    def n033a(t0): return dict(draw=shots.wide('night/sg_street', [off_w], overlay=lambda c, t: props.sign_megaspeed(c, 960, 380, .88, glow=.7), t0=t0), zoom=(1.2, 1.4), focus=((700, 640), (900, 600)), sfx=[(0, 'steps', 1.6)],
                               hud=lambda c, t: Wd.place_tag(c, 'Singapore', (t - .2) / .4, 'Feb 2025'))
    def n033b(t0): return dict(draw=plain(lambda c, t: A.hand_slam(c, 960, 540, t, 'paper', 'Case file', ['Subject: Megaspeed', 'Police + customs', 'Opened Feb 2025'], hit=.3)),
                               zoom=(1.0, 1.06), shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t, hit=.3), sfx=[(.3, 'stamp')], hud=HUDPOP('investigation', 960, 950, .6, GOLD, 80, -2))
    multi('n033', [(.5, n033a), (.5, n033b)])
    # n034  the suspicion (highlighted), then OFFICIAL FINDING + acted on its own
    def n034a(t0): return dict(draw=plain(lambda c, t: doc(c, 960, 540, 'Singapore authorities', ['Suspected offence:', 'False declarations about', 'server purchases', 'No foreign request'], t / 1.6, hl=1, label_txt='OFFICIAL STATEMENT')),
                               zoom=(1.0, 1.12), focus=((960, 540), (900, 480)), sfx=[(.1, 'paper')])
    def n034b(t0): return dict(draw=plain(lambda c, t: doc(c, 960, 540, 'Singapore authorities', ['Suspected offence:', 'False declarations about', 'server purchases', 'No foreign request'], 3, hl=3, hl_t=0)),
                               zoom=(1.25, 1.35), focus=(960, 600), hud=lambda c, t: Wd.stamp(c, 'Official finding', 1450, 860, t - .3, GOLD, rot=-8, size=76), sfx=[(.3, 'stamp')], shake=shake(.3))
    multi('n034', [(.55, n034a), (.45, n034b)])
    # n035  June 24, 2025
    add('n035', plain(lambda c, t: date_cal(c, 960, 520, t, 'JUNE 2025', 1, 24, D('n035') * .7, s=1.5, circle_at=D('n035') * .72)), zoom=(1.0, 1.12), sfx=[(0, 'flips', D('n035') * .7), (D('n035') * .72, 'pop')])
    # n036  inspectors walk into the Megaspeed office; Alice is there (tag again after a gap)
    i1 = Actor('inspector', 1700, 1000, 1.0, face=-.6, rim=NR).walk_to(0, 1.4, 1350).pose(1.4, ('hold', 'down'))
    i2 = Actor('inspector2', 1900, 1000, 1.0, face=-.6, rim=NR).walk_to(.2, 1.6, 1600).pose(1.6, ('hold', 'hold'))
    al36 = Actor('alice', 560, 1000, 1.0, face=.5, rim=NR).expression(0, mouth='flat', eyes='wide')
    def n036a(t0): return dict(draw=shots.wide('night/megaspeed', [al36], [i1, i2], overlay=lambda c, t: props.sign_megaspeed(c, 960, 240, .85, glow=.9), t0=t0), zoom=(1.0, 1.1), focus=((1100, 600), (1000, 580)), sfx=[(0, 'steps', 1.6)],
                               hud=lambda c, t: Wd.place_tag(c, 'Megaspeed site', (t - .2) / .4, 'U.S. export officials'))
    def n036b(t0): return dict(draw=shots.wide('night/megaspeed', [al36], [i1, i2], overlay=lambda c, t: props.sign_megaspeed(c, 960, 240, .85, glow=.9), t0=t0), zoom=(1.5, 1.9), focus=((700, 620), (600, 560)),
                               hud=lambda c, t: Wd.lower_third(c, 'Alice Huang (alleged)', 'then-CEO, Megaspeed', (t - .2) / .5))
    multi('n036', [(.5, n036a), (.5, n036b)])
    # n037  police interview (investigation room); the passport slides across the desk and a hand slams on it
    of37 = Actor('officer', 930, 950, 1.08, face=-.3, rim=NR, hat=True).pose(.2, ('push', 'down')).expression(0, mouth='flat', brow=-.3)
    al37 = Actor('alice', 420, 1080, 1.1, face=.6, rim=NR).expression(0, mouth='flat', eyes='half')
    def n037a(t0): return dict(draw=shots.wide('night/investigation_room', [of37], [al37], t0=t0), zoom=(1.1, 1.3), focus=((930, 620), (930, 560)), hud=lambda c, t: Wd.place_tag(c, 'Singapore police', (t - .2) / .4, 'June 24, 2025'))
    def pp(c, t):
        k = ease_out(K(t, .1, .6)); passport(c, 960 + (1 - k) * -700, 560, 1.4, rot=-8 + (1 - k) * 30)
        A.hand_slam(c, 1060, 600, t - .9, 'sticky', 'Impounded', hit=.25, rot=6)
    def n037b(t0): return dict(draw=plain(pp), zoom=(1.0, 1.1), sfx=[(.1, 'paper'), (1.15, 'stamp')], shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t - .9, hit=.25))
    multi('n037', [(.45, n037a), (.55, n037b)])
    # n038  OFFICER (dramatised)
    talk('n038', 'officer', 'night/investigation_room', (700, 560), .4, 'The Officer', 'Singapore police, dramatised', dict(mouth='flat', brow=-.4), ('push', 'down'))
    # n039  Nvidia cuts Megaspeed off: green chip behind a door that slams, gold padlock
    def cutoff(c, t):
        props.chip(c, 960, 560, 2.2, glow=.6, accent=NG); big_door(c, t, .7, plate='MEGASPEED ORDERS')
        if t > .8:
            e = kit.back(K(t, .8, .35)); c.save(); c.translate(1230, 640 - (1 - e) * 200); kit.rect(c, -60, -10, 60, 100, GOLD, 6, r=12)
            p = skia.Path(); p.addArc(skia.Rect(-42, -80, 42, 20), 180, 180); c.drawPath(p, kit.ink(14)); c.drawPath(p, kit.ink(8, '#C9CFDB')); kit.circ(c, 0, 45, 12, NAVY, 4); c.restore()
    add('n039', plain(cutoff, framed=False), zoom=(1.15, 1.0), focus=(1000, 560), sfx=[(.7, 'stamp'), (1.0, 'pop')], shake=shake(.7),
        hud=lambda c, t: (Wd.pop_label(c, 'no new orders', 1560, 300, (t - 1.2) / .4, GOLD, 80, rot=-4), Wd.pop_label(c, 'no shipments', 1560, 440, (t - 1.8) / .4, WHITE, 80, rot=3),
                          Wd.text(c, "NVIDIA'S ACCOUNT", 80, 1000, 34, '#9DB0DA', F_LABEL)))
    # n039b / n039c  clerk and manager (dramatised)
    talk('n039b', 'clerk', 'night/office', (1300, 560), -.4, 'The Clerk', 'Dramatised', dict(mouth='smile'), ('phone', 'down'))
    talk('n039c', 'manager', 'night/office', (650, 560), .4, 'The Manager', 'Dramatised', dict(mouth='flat', eyes='half', brow=-.3), ('down', 'push'),
         extra_hud=lambda c, t: Wd.stamp(c, 'Cancelled', 1520, 230, t - .5, GOLD, rot=-10, size=96), sfx=[(.5, 'stamp')])
    S[-1]['shake'] = shake(.5)
    # n040  card
    add('n040', shots.card('text', D('n040'), text=tl.by_id['n040']['text'], gold_words=['why.']), zoom=(1.0, 1.03))
    # n041  Aug 30 circled; Alice walks out of the office
    def n041a(t0): return dict(draw=plain(lambda c, t: date_cal(c, 960, 520, t, 'AUGUST 2025', 1, 30, 1.0, s=1.5, circle_at=1.1)), zoom=(1.0, 1.1), sfx=[(0, 'flips', 1.0), (1.1, 'pop')])
    alw = Actor('alice', 900, 1000, 1.0, face=-.6, rim=NR).walk_to(.2, 2.6, 200)
    def n041b(t0): return dict(draw=shots.wide('night/megaspeed', [], [alw], overlay=lambda c, t: props.sign_megaspeed(c, 960, 240, .85, glow=.9), t0=t0), zoom=(1.1, 1.2), focus=((900, 600), (600, 600)), sfx=[(.2, 'steps', 2.4)],
                               hud=lambda c, t: Wd.text(c, "THE COMPANY'S ACCOUNT", 1880, 1000, 34, '#9DB0DA', F_LABEL, 'right'))
    multi('n041', [(.45, n041a), (.55, n041b)])
    # n042  hold that date: the circled 30 stays, music drops, slow push
    add('n042', plain(lambda c, t: date_cal(c, 960, 520, 9, 'AUGUST 2025', 1, 30, 1.0, s=1.5, circle_at=0) or c.drawCircle(960, 600, 300 + 30 * math.sin(t * 3), fp(GOLD, 30, blur=40))), zoom=(1.2, 1.6), focus=(960, 560))
    # n043  short seller report (CLAIM, NOT PROVEN)
    def n043a(t0): return dict(draw=plain(lambda c, t: doc(c, 960, 540, 'Culper Research (short seller)', ['Report on Megaspeed', 'An employee quoted:', '"she is still the boss"'], t / 1.4, hl=2, label_txt='SHORT-SELLER REPORT')),
                               zoom=(1.0, 1.12), sfx=[(.1, 'paper')])
    def n043b(t0): return dict(draw=plain(lambda c, t: doc(c, 960, 540, 'Culper Research (short seller)', ['Report on Megaspeed', 'An employee quoted:', '"she is still the boss"'], 3, hl=2, hl_t=0)),
                               zoom=(1.3, 1.45), focus=(960, 620), hud=lambda c, t: Wd.stamp(c, 'Claim, not proven', 1400, 880, t - .3, GOLD, rot=-7, size=70), sfx=[(.3, 'stamp')], shake=shake(.3))
    multi('n043', [(.55, n043a), (.45, n043b)])
    # n044  card with two arrows splitting
    def n044(c, t):
        Wd.text_card(c, tl.by_id['n044']['text'], max(t - .3, 0), ['records', 'claims'], dur=D('n044'))
    add('n044', n044, zoom=(1.0, 1.03))
    # n044b  NYT, Oct 2025: newspaper, the question, the $2 billion counter
    def nyt(c, t):
        A.newspaper(c, 960, 520, t, 'The New York Times', ' ', None); Wd.text(c, 'OCTOBER 2025', 960, 900, 40, '#9DB0DA', F_LABEL, 'center') if t > .7 else None
        for i, w_ in enumerate((900, 760)): c.drawRoundRect(skia.Rect(960 - w_ / 2, 380 + i * 100, 960 + w_ / 2, 450 + i * 100), 12, 12, fp(NAVY, 200 if t > .7 else 0, blur=10))
    multi('n044b', [(.3, lambda t0: dict(draw=plain(nyt), zoom=(1.0, 1.08), sfx=[(.05, 'whoosh'), (.7, 'stamp')], shake=shake(.7))),
                    (.3, lambda t0: dict(draw=plain(lambda c, t: nyt(c, 9)), zoom=(1.4, 1.5), focus=(960, 450), hud=HUDPOP('Is China buying banned Nvidia chips?', 960, 800, .2, GOLD, 76, -2))),
                    (.4, lambda t0: dict(draw=plain(lambda c, t: ([props.chip(c, 380 + i * 290, 880 - 30 * (i % 2), .8, glow=.3 * K(t, .3 + i * .15, .3), accent=NG) for i in range(5)],
                                                                         Wd.counter(c, 960, 420, 0, 2_000_000_000, (t - .1) / 1.6, label='poised to buy within a year (reported)', size=120))),
                                         zoom=(1.0, 1.1), sfx=[(.2, 'tick'), (1.8, 'ding')]))])
    # n045  a phone lights up in the dark: who was she talking to?
    def n045a(t0): return dict(draw=shots.wide('night/restaurant', [], overlay=lambda c, t: props.phone_flat(c, 960, 860, 1.3, lit=1.0 if int(t * 2.2) % 2 == 0 else .3, t=t)), zoom=(1.3, 1.6), focus=(960, 760), sfx=[(0, 'ring', 4.0), (0, 'amb:murmur', None)])
    def n045b(t0): return dict(draw=plain(lambda c, t: smartphone(c, 960, 560, t, caller='UNKNOWN', s=1.0, icon='?')), zoom=(1.0, 1.15), sfx=[(0, 'ring', 4.0)], hud=HUDPOP('who was she talking to?', 960, 960, .4, GOLD, 80, -2))
    multi('n045', [(.45, n045a), (.55, n045b)])

    # ================= CH3 "How the Door Opens" =================
    chapter(3, 'How the Door Opens')
    DR = '#FFE3A6'
    def doors3(c, t, lit=None):
        for i in range(3):
            x = 480 + i * 480; k = kit.back(K(t, .2 + i * .35, .35)); 
            if k <= 0: continue
            c.save(); c.translate(x, 600); c.scale(k, k)
            rect(c, -140, -300, 140, 300, '#0F1A38', 7); rect(c, -122, -284, 122, 300, '#5A3B24' if lit != i else '#7A5236', 6)
            if lit == i: c.drawRect(skia.Rect(-122, -284, 122, 300), fp(GOLD, 60, blur=20))
            kit.circ(c, 90, 30, 14, GOLD, 4); kit.circ(c, 0, -170, 62, GOLD, 6); Wd.text(c, str(i + 1), 0, -146, 80, NAVY, F_TITLE, 'center')
            Wd.text(c, ('SMUGGLING', 'MIDDLEMEN', 'RENTING')[i], 0, -330, 50, GOLD if lit == i else WHITE, F_LABEL, 'center') if lit is not None else None
            c.restore()
    # n050  three numbered doors pop in
    add('n050', plain(lambda c, t: doors3(c, t)), zoom=(1.0, 1.08), sfx=[(.2, 'pop'), (.55, 'pop'), (.9, 'pop')], hud=HUDPOP('three ways', 960, 170, 1.2, GOLD, 90, -3))
    # n051  door 1 opens; a hair dryer peels a label off a server box (alleged, separate case)
    def dryer(c, x, y, ang, t):
        c.save(); c.translate(x, y); c.rotate(ang)
        rect(c, -40, -10, 40, 170, '#2E2E38', 6, r=16); rect(c, -150, -60, 60, 60, '#3A3F4F', 7, r=50); kit.circ(c, -150, 0, 56, '#2E2E38', 6)
        for i in range(4): c.drawLine(-210, -30 + i * 20, -330 - 20 * math.sin(t * 20 + i), -40 + i * 26, kit.ink(6, GOLD, 160))
        c.restore()
    def peel(c, t):
        props.crate(c, 760, 900, 2.4, label_text='SERVERS')
        k = ease(K(t, .6, 1.6)); c.save(); c.translate(560, 560)
        rect(c, 0, 0, 380 - 0 * k, 150, '#F4EFE2', 5, r=6); Wd.text(c, 'OTHER BRAND', 190, 92, 46, NAVY, F_LABEL, 'center')
        if k > 0:
            p = skia.Path(); p.moveTo(380 - 200 * k, 0); p.lineTo(380, 0); p.lineTo(380, 150 * k); p.close(); c.drawPath(p, fp('#D8D2C4')); c.drawPath(p, kit.ink(4))
        c.restore(); props.hair_dryer(c, 1350, 560, 1.0, -10 + 4 * math.sin(t * 3), t)
    multi('n051', [(.35, lambda t0: dict(draw=plain(lambda c, t: doors3(c, 9, lit=0)), zoom=(1.0, 1.15), focus=((960, 560), (700, 480)), sfx=[(.1, 'whoosh')])),
                   (.65, lambda t0: dict(draw=plain(peel), zoom=(1.0, 1.15), focus=((900, 640), (800, 600)),
                                         hud=lambda c, t: (Wd.text(c, 'ALLEGED - A SEPARATE CASE, PER PROSECUTORS', 80, 90, 36, '#9DB0DA', F_LABEL), HUDPOP('swapped labels', 1500, 300, .9, GOLD, 80, -4)(c, t))))])
    # n051b / n051c  worker + colleague (dramatised, separate case)
    talk('n051b', 'worker', 'night/datacenter', (700, 700), .4, 'The Worker', 'Dramatised, separate case', dict(mouth='flat', brow=.5, brow_tilt=-.4), ('push', 'push'))
    talk('n051c', 'grad', 'night/datacenter', (1250, 700), -.4, 'The Colleague', 'Dramatised, separate case', dict(mouth='smile', eyes='half'), ('point', 'down'),
         overlay=lambda c, t: props.hair_dryer(c, 1480, 820, 1.0, -30, t, sleeve='#3A3F4F', skin='#8A5A3C'))
    # n052  middlemen: boxes slide along a conveyor; a map pin hops
    def conveyor(c, t):
        rect(c, -20, 760, W + 20, 840, '#2E2E38', 6); [kit.circ(c, x + (t * 120) % 120, 800, 26, '#5A6076', 4) for x in range(0, W, 120)]
        for i in range(5): props.crate(c, ((t * 240 + i * 420) % 2300) - 200, 760, .9)
        for i, lbl in enumerate(('BUYER', 'MIDDLEMAN', '?')):
            x = 380 + i * 580; rect(c, x - 140, 200, x + 140, 300, NAVY, 5, r=12); Wd.text(c, lbl, x, 268, 54, GOLD if i == 1 else WHITE, F_LABEL, 'center')
    def hop(c, t):
        Wd.framed_bg(c); pts = [(420, 560), (960, 520), (1500, 560)]
        for i, (x, y) in enumerate(pts):
            if i < 2:
                rect(c, x - 110, y - 160, x + 110, y + 90, '#2B3F70', 6); [rect(c, x - 80 + (j % 4) * 44, y - 130 + (j // 4) * 52, x - 52 + (j % 4) * 44, y - 98 + (j // 4) * 52, '#FFE2A0' if (j + i) % 3 else '#1B2A52', 3) for j in range(16)]
            else: A.flag(c, 'china', x, y - 30, 300, 200, t)
            Wd.text(c, ('SOUTHEAST ASIA', 'ANOTHER COMPANY', 'CHINA')[i], x, y + 180, 48, GOLD if i == 2 else WHITE, F_LABEL, 'center')
        ph = min(t / 1.0, 1.999); i = int(ph); u = ph - i; (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        x = x0 + (x1 - x0) * u; y = y0 + (y1 - y0) * u - math.sin(u * math.pi) * 220
        kit.circ(c, x, y - 90, 40, GOLD, 6); kit.poly(c, [(x - 30, y - 70), (x + 30, y - 70), (x, y)], GOLD, 5); kit.circ(c, x, y - 90, 14, NAVY, 0)
    multi('n052', [(.5, lambda t0: dict(draw=plain(conveyor), zoom=(1.0, 1.08), sfx=[(0, 'amb:rumble', None)], hud=HUDPOP('quietly passed on', 960, 980 - 60, .6, GOLD, 80, -2))),
                   (.5, lambda t0: dict(draw=hop, zoom=(1.0, 1.06), sfx=[(.5, 'pop'), (1.5, 'pop')]))])
    # n053  renting: a laptop in Beijing, a dotted line to a server room in Asia, ding
    def laptop(c, x, y, s, t, screen='LOG IN'):
        c.save(); c.translate(x, y); c.scale(s, s)
        rect(c, -200, -260, 200, 0, '#2E2E38', 6, r=12); rect(c, -180, -240, 180, -20, NAVY, 3, r=6); Wd.text(c, screen, 0, -110, 50, GOLD, F_LABEL, 'center')
        kit.poly(c, [(-240, 0), (240, 0), (270, 40), (-270, 40)], '#3A3F4F', 6); c.restore()
    def rent(c, t):
        laptop(c, 420, 640, 1.0, t, 'LOG IN' if t < 1.4 else 'CONNECTED'); Wd.text(c, 'BEIJING (USER)', 420, 760, 46, WHITE, F_LABEL, 'center'); A.flag(c, 'china', 420, 260, 220, 146, t)
        for i in range(3): props.server_rack(c, 1400 + i * 170, 760, .8, phase=t + i)
        Wd.text(c, 'DATA CENTER, ELSEWHERE IN ASIA', 1570, 840, 40, WHITE, F_LABEL, 'center')
        e = ease(K(t, .3, 1.0)); n = 30
        for i in range(int(n * e)):
            if i % 2 == 0: c.drawLine(640 + 18 * i * 1.0, 480 - math.sin(i / n * math.pi) * 160, 640 + 18 * (i + 1), 480 - math.sin((i + 1) / n * math.pi) * 160, kit.ink(10, GOLD))
    multi('n053', [(.6, lambda t0: dict(draw=plain(rent), zoom=(1.0, 1.08), sfx=[(1.4, 'ding')], hud=HUDPOP('the chips never leave', 1300, 220, 1.6, GOLD, 72, -2))),
                   (.4, lambda t0: dict(draw=plain(lambda c, t: laptop(c, 960, 760, 2.2, t, 'CONNECTED')), zoom=(1.0, 1.1), focus=(960, 500)))])
    # n053b  Commerce Department warning, May 2025
    CD = ['May 2025', 'To U.S. companies:', 'Watch for partners offering', 'cloud access to China']
    multi('n053b', [(.5, lambda t0: dict(draw=plain(lambda c, t: doc(c, 960, 560, 'Commerce Department guidance', CD, t / 1.6, hl=3, hl_t=1.0, label_txt='OFFICIAL WARNING')), zoom=(1.0, 1.1), sfx=[(.1, 'paper')])),
                    (.5, lambda t0: dict(draw=plain(lambda c, t: doc(c, 960, 560, 'Commerce Department guidance', CD, 3, hl=3, hl_t=0, label_txt='OFFICIAL WARNING')), zoom=(1.3, 1.45), focus=((900, 600), (1000, 620)),
                                         hud=HUDPOP('a warning to U.S. firms', 760, 920, .3, GOLD, 80, -2), sfx=[(.3, 'pop')]))])
    # n054  analogy: an oven banned in town, a scooter delivers pizza anyway
    def oven(c, t, banned_t=.6):
        rect(c, 560, 380, 1100, 860, '#3A3F4F', 8, r=20); rect(c, 620, 470, 1040, 760, '#14141A', 6, r=12)
        c.drawRect(skia.Rect(640, 650, 1020, 740), fp(GOLD, int(120 + 60 * math.sin(t * 6)), blur=20))
        for i in range(3): kit.circ(c, 680 + i * 150, 420, 18, GOLD, 4)
        Wd.stamp(c, 'Banned in town', 830, 620, t - banned_t, GOLD, rot=-10, size=80)
    def scooter(c, t):
        x = -300 + 1650 * ease_out(K(t, .1, 1.4)); c.save(); c.translate(x, 840 + 4 * math.sin(t * 25))
        kit.circ(c, -110, 60, 50, '#2E2E38', 6); kit.circ(c, 110, 60, 50, '#2E2E38', 6); rect(c, -150, -20, 150, 40, '#2B4A7A', 6, r=20)
        rect(c, -150, -140, -30, -20, '#C9A26A', 5, r=4); Wd.text(c, 'PIZZA', -90, -70, 30, NAVY, F_LABEL, 'center'); c.drawLine(120, -20, 160, -120, kit.ink(10)); c.restore()
    multi('n054', [(.5, lambda t0: dict(draw=plain(oven), zoom=(1.0, 1.12), focus=(830, 600), sfx=[(.6, 'stamp')], shake=shake(.6), hud=HUDPOP('think of a pizza oven', 1450, 250, .1, GOLD, 70, -3))),
                   (.5, lambda t0: dict(draw=plain(lambda c, t: (oven(c, 9), props.scooter_rider(c, -300 + 1650 * ease_out(K(t, .1, 1.4)), 830, .9, t))), zoom=(1.05, 1.0), sfx=[(.1, 'whoosh')], hud=HUDPOP('pizza: fine', 1450, 250, .8, GOLD, 90, -3)))])
    # n054b-e  the analogy as a shop-counter scene (dramatised)
    def banned_sign(c, t): rect(c, 1350, 180, 1820, 330, '#F4EFE2', 6, r=10); Wd.text(c, 'NO OVENS SOLD', 1585, 278, 54, NAVY, F_LABEL, 'center')
    talk('n054b', 'customer', 'day/shop_counter', (700, 600), .4, 'The Customer', 'Dramatised analogy', dict(mouth='smile'), ('present', 'down'), rim=DR, light=1)
    talk('n054c', 'seller', 'day/shop_counter', (1250, 600), -.4, 'The Seller', 'Dramatised analogy', dict(mouth='flat', brow=-.3), ('point', 'down'), rim=DR, light=1, extra_hud=banned_sign)
    talk('n054d', 'customer', 'day/shop_counter', (700, 600), .5, None, None, dict(mouth='open', eyes='wide', brow=.5), ('cheer', 'down'), rim=DR, light=1, zoom=(1.08, 1.0))
    def pizza_box(c, t):
        x = 1750 - 400 * ease_out(K(t, .2, .6)); rect(c, x - 200, 820, x + 200, 900, '#C9A26A', 6, r=6); Wd.text(c, 'PIZZA', x, 878, 44, NAVY, F_LABEL, 'center')
    talk('n054e', 'seller', 'day/shop_counter', (1250, 600), -.4, None, None, dict(mouth='smile', eyes='half'), ('push', 'down'), rim=DR, light=1, overlay=pizza_box, sfx=[(.6, 'pop')])
    # n055  card
    add('n055', shots.card('text', D('n055'), text=tl.by_id['n055']['text'], gold_words=['proven', 'denies']), zoom=(1.0, 1.03))
    # n056  company statement, DENIED stamp (navy, on the paper)
    add('n056', plain(lambda c, t: doc(c, 960, 540, 'Megaspeed statement', ['December 2025', '"No evidence of illicit', 'chip transfers"'], t / 1.4, hl=1, hl_t=.9, label_txt="THE COMPANY'S WORDS")),
        hud=lambda c, t: Wd.stamp(c, 'Denied', 1120, 680, t - D('n056') * .6, GOLD, rot=-10, size=100), zoom=(1.0, 1.12), sfx=[(.1, 'paper'), (D('n056') * .6, 'stamp')], shake=shake(D('n056') * .6))
    # n057  headphones and a live waveform: intelligence was listening
    def listen(c, t):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#0B1226'))
        for i in range(60):
            x = 300 + i * 22; hgt = 30 + 180 * abs(math.sin(i * .7 + t * 6) * math.sin(i * .23 + t * 2.3)); c.drawRoundRect(skia.Rect(x, 820 - hgt / 2, x + 12, 820 + hgt / 2), 6, 6, fp(GOLD, 220))
        p = skia.Path(); p.addArc(skia.Rect(660, 140, 1260, 740), 180, 180); c.drawPath(p, kit.ink(46)); c.drawPath(p, kit.ink(30, '#3A3F4F'))
        for x in (660, 1260): rect(c, x - 70, 380, x + 70, 620, '#2E2E38', 7, r=40)
    add('n057', plain(listen, framed=False), zoom=(1.0, 1.12), focus=(960, 520), sfx=[(0, 'amb:static', None)], hud=HUDPOP('it was listening', 960, 110, D('n057') * .5, GOLD, 90, -2))

    # ================= TWIST =================
    def gold_line(c, t):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#05070D')); e = ease_out(K(t, .2, 1.4)); c.drawRect(skia.Rect(960 - 700 * e, 538, 960 + 700 * e, 544), fp(GOLD))
        c.drawRect(skia.Rect(960 - 700 * e, 520, 960 + 700 * e, 560), fp(GOLD, 40, blur=16))
        if t > 1.2: Wd.text(c, 'WASHINGTON', 960, 640, 54, '#9DB0DA', F_LABEL, 'center', alpha=int(255 * K(t, 1.2, .5)))
    add('n060', plain(gold_line, framed=False), zoom=(1.0, 1.06), sfx=[(.2, 'whoosh')])
    def monitors(c, t, focus_i=None):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#0B1226'))
        for i in range(6):
            x0, y0 = 160 + (i % 3) * 560, 140 + (i // 3) * 420; rect(c, x0, y0, x0 + 500, y0 + 340, '#1B1D26', 7, r=12); rect(c, x0 + 20, y0 + 20, x0 + 480, y0 + 300, '#0F1A38', 3, r=6)
            for j in range(34):
                hh = 8 + 90 * abs(math.sin(j * .6 + t * (4 + i) + i) * math.sin(j * .21 + t * 1.7 + i)); xx = x0 + 40 + j * 13
                c.drawRect(skia.Rect(xx, y0 + 160 - hh / 2, xx + 7, y0 + 160 + hh / 2), fp(GOLD, 200))
            Wd.text(c, ('LINE 1', 'LINE 2', 'SUBJECT: A. HUANG', 'LINE 4', 'LINE 5', 'LINE 6')[i], x0 + 40, y0 + 278, 30, GOLD if i == 2 else '#9DB0DA', F_LABEL)
        c.drawRect(skia.Rect(0, 900, W, H), fp('#141A2E')); c.drawLine(0, 900, W, 900, kit.ink(6))
    multi('n061', [(.5, lambda t0: dict(draw=plain(monitors, framed=False), zoom=(1.0, 1.1), sfx=[(0, 'amb:static', None)], hud=lambda c, t: Wd.text(c, 'ACCORDING TO THE NEW YORK TIMES', 80, 1010, 34, '#9DB0DA', F_LABEL))),
                   (.5, lambda t0: dict(draw=plain(monitors, framed=False), zoom=(2.3, 2.6), focus=(1260, 300), hud=HUDPOP('watched (reported)', 960, 980 - 40, .3, GOLD, 80, -2)))])
    add('n062', shots.card('text', D('n062'), text=tl.by_id['n062']['text'], gold_words=['CEO', 'Nvidia.']), zoom=(1.0, 1.03), sfx=[(D('n062') * .8, 'boom')])
    def redacted(c, t, reveal=0.0, name='JENSEN HUANG'):
        k = kit.back(min(max(t / .35, 0), 1)); c.save(); c.translate(960, 560 + (1 - k) * 400); c.rotate(-2)
        rect(c, -460, -360, 460, 360, PAPER, 6); Wd.text(c, 'INTELLIGENCE REPORT', -410, -270, 50, NAVY, F_LABEL); c.drawRect(skia.Rect(-410, -246, 410, -240), fp(NAVY))
        Wd.text(c, 'U.S. PERSON (NAME MASKED):', -410, -150, 38, NAVY, F_TYPE)
        if reveal > 0: Wd.text(c, name, -410, -60, 70, NAVY, F_TITLE)
        c.drawRect(skia.Rect(-410 + 830 * reveal, -120, 420, -30), fp('#14141A'))
        for i, w_ in enumerate((700, 560, 760, 480)): c.drawRect(skia.Rect(-410, 40 + i * 70, -410 + w_, 80 + i * 70), fp('#14141A'))
        c.restore()
    add('n063', plain(lambda c, t: redacted(c, t, 0.0)), zoom=(1.0, 1.15), focus=((960, 560), (900, 480)), sfx=[(.1, 'paper')], hud=HUDPOP('name masked', 1500, 200, .8, GOLD, 80, -4))
    talk('n063b', 'analyst', 'night/investigation_room', (700, 560), .4, 'The Analyst', 'Dramatised', dict(mouth='flat', brow=.3), ('down', 'point'))
    talk('n063c', 'supervisor', 'night/investigation_room', (1250, 560), -.4, 'The Supervisor', 'Dramatised', dict(mouth='flat', eyes='half', brow=-.3), ('push', 'down'))
    d64 = D('n064'); f64 = .6
    S.append(dict(name='n064', dur=d64 * f64, draw=plain(lambda c, t: redacted(c, 9, ease(K(t, .2, .8)))), zoom=(1.3, 1.5), focus=(860, 480), sfx=[(.3, 'whoosh'), (1.1, 'stamp')],
                  shake=shake(1.1), hud=lambda c, t: Wd.stamp(c, 'Revealed', 1400, 760, t - 1.1, GOLD, rot=-8, size=110)))
    S.append(dict(name='n064_2', dur=d64 * (1 - f64), draw=shots.card('text', d64 * (1 - f64), text='Jensen Huang.', gold_words=['Jensen', 'Huang.'], lead=0.0), zoom=(1.0, 1.03)))

    # ================= CH4 "Completely Normal" =================
    chapter(4, 'Completely Normal')
    def nyt2(c, t, sub='OCTOBER 29, 2026'):
        A.newspaper(c, 960, 520, t, 'The New York Times', ' ', None)
        for i, w_ in enumerate((900, 760, 820)): c.drawRoundRect(skia.Rect(960 - w_ / 2, 400 + i * 100, 960 + w_ / 2, 470 + i * 100), 12, 12, fp(NAVY, 200 if t > .7 else 0, blur=10))
        if t > .7: Wd.text(c, sub, 960, 940, 44, '#9DB0DA', F_LABEL, 'center')
    add('n070', plain(nyt2), zoom=(1.0, 1.15), sfx=[(.05, 'whoosh'), (.7, 'stamp')], shake=shake(.7), hud=HUDPOP('goes public', 1700, 700, 1.0, GOLD, 90, -6))
    R71 = ['People briefed on the surveillance:', 'officials had concluded she was', 'a Chinese intelligence asset']
    multi('n071', [(.5, lambda t0: dict(draw=plain(lambda c, t: doc(c, 960, 540, 'The New York Times reports', R71, t / 1.4, hl=2, label_txt='REPORTED, NOT PROVEN')), zoom=(1.0, 1.1), sfx=[(.1, 'paper')])),
                   (.5, lambda t0: dict(draw=plain(lambda c, t: doc(c, 960, 540, 'The New York Times reports', R71, 3, hl=2, hl_t=0, label_txt='REPORTED, NOT PROVEN')), zoom=(1.45, 1.55), focus=((900, 600), (1000, 580)),
                                        hud=lambda c, t: Wd.stamp(c, 'Reported', 1250, 720, t - .3, GOLD, rot=-8, size=90), sfx=[(.3, 'stamp')], shake=shake(.3)))])
    def warn_env(c, t):
        c.save(); c.translate(960, 600 + 6 * math.sin(t * 1.5)); c.rotate(-3)
        c.drawRect(skia.Rect(-400, -230, 420, 250), fp((0, 0, 0), 90, blur=16)); rect(c, -420, -250, 420, 250, '#E9DFC8', 6)
        kit.poly(c, [(-420, -250), (420, -250), (0, 40)], '#DDD1B6', 6); kit.circ(c, 0, 40, 46, GOLD, 5)
        Wd.text(c, 'WARNING', 0, 180, 70, NAVY, F_TITLE, 'center'); Wd.text(c, 'DEFENSIVE BRIEFING', 0, -150, 40, NAVY, F_LABEL, 'center'); c.restore()
        c.drawRect(skia.Rect(0, 0, W, H), fp('#000000', int(40 + 30 * math.sin(t))))
    add('n072', plain(warn_env), zoom=(1.0, 1.15), hud=lambda c, t: (Wd.pop_label(c, 'never given (reported)', 960, 950, (t - .8) / .4, GOLD, 80, rot=-2),
                                                                         Wd.text(c, 'A WARNING AGENCIES SOMETIMES GIVE', 80, 90, 36, '#9DB0DA', F_LABEL)))
    def mics(c, t):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#0A1226', 120)); props.nvidia_logo(c, 905, 660, .55, word=False)
        for i, x in enumerate((900, 1020)):
            c.drawLine(x, 620, x + (i - .5) * 40, 520, kit.ink(10, '#2E2E38')); kit.oval(c, x + (i - .5) * 40 - 26, 470, x + (i - .5) * 40 + 26, 540, '#3A3F4F', 5)
        if t > .4: c.drawRect(skia.Rect(0, 0, W, H), fp(WHITE, int(90 * max(0, 1 - (t - .4) * 6) + 60 * max(0, 1 - abs(t - 1.6) * 6))))
    add('n073', shots.wide('day/press_conference', [], overlay=mics), zoom=(1.0, 1.15), focus=(960, 560), sfx=[(.4, 'pop'), (1.6, 'pop')],
        hud=lambda c, t: (Wd.place_tag(c, "Nvidia's answer", (t - .2) / .4, 'statement'), Wd.pop_label(c, 'one of many regional customers', 960, 880, (t - 1.0) / .4, GOLD, 72, rot=-2)))
    talk('n074', 'jensen', 'night/office', (1250, 560), -.3, 'Jensen Huang', 'Nvidia CEO', dict(mouth='flat', brow=.5, brow_tilt=-.3, sweat=0), ('shrug', 'shrug'),
         extra_hud=lambda c, t: Wd.pop_label(c, 'never told', 1450, 300, (t - .9) / .4, WHITE, 90, rot=-4))
    def lectern_cn(c, t):
        rect(c, 760, 560, 1160, 1000, '#8A1C1C', 7, r=10); rect(c, 720, 520, 1200, 580, '#6E1414', 6, r=8)
        for i, (sx, sy, r_) in enumerate(((880, 680, 34), (950, 640, 12), (975, 670, 12), (975, 705, 12), (950, 735, 12))):
            pts = [(sx + r_ * math.cos(math.pi / 2 + k * 2 * math.pi / 5 * 2 - math.pi), sy + r_ * math.sin(math.pi / 2 + k * 2 * math.pi / 5 * 2 - math.pi)) for k in range(5)]
            c.drawPath(skia.Path.Polygon([skia.Point(*p) for p in pts], True), fp('#FFDE00'))
        Wd.stamp(c, 'Groundless', 1430, 380, t - 1.0, GOLD, rot=-8, size=90)
    add('n075', plain(lectern_cn), zoom=(1.0, 1.12), focus=(960, 620), sfx=[(1.0, 'stamp')], shake=shake(1.0),
        hud=lambda c, t: (Wd.place_tag(c, "China's foreign ministry", (t - .2) / .4, 'their words'),))
    def verdict(c, t):
        rect(c, 760, 600, 1160, 1000, '#3A2A1E', 7, r=10); kit.circ(c, 960, 760, 60, GOLD, 6); Wd.text(c, 'DOJ', 960, 778, 44, NAVY, F_LABEL, 'center')
        k = kit.back(K(t, .5, .4)); c.save(); c.translate(1420, 420); c.scale(k, k); c.rotate(4)
        rect(c, -260, -160, 260, 160, PAPER, 6); Wd.text(c, 'IS SHE A SPY?', 0, -70, 50, NAVY, F_LABEL, 'center'); Wd.text(c, 'NO CONCLUSION', 0, 60, 44, NAVY, F_TITLE, 'center'); c.restore()
    multi('n076', [(.5, lambda t0: dict(draw=plain(verdict), zoom=(1.0, 1.08), sfx=[(.5, 'pop')], hud=lambda c, t: Wd.place_tag(c, 'Justice Department', (t - .3) / .4, 'Attorney General Todd Blanche'))),
                   (.5, lambda t0: dict(draw=plain(lambda c, t: verdict(c, 9)), zoom=(1.4, 1.55), focus=(1350, 480), hud=HUDPOP('whether she was a spy', 960, 900, .3, GOLD, 80, -2)))])
    add('n077', plain(lambda c, t: doc(c, 960, 540, 'Singapore Ministry of Home Affairs', ['Statement:', 'She was never investigated', 'for espionage'], t / 1.4, hl=1, label_txt='OFFICIAL STATEMENT')),
        zoom=(1.0, 1.14), focus=((960, 540), (900, 520)), sfx=[(.1, 'paper')], hud=HUDPOP('a twist', 1500, 200, .2, GOLD, 90, -4))
    W78 = ['Too little evidence to charge', 'Warned', 'Banned from returning:', 'inaccurate information about her role']
    multi('n078', [(.5, lambda t0: dict(draw=plain(lambda c, t: doc(c, 960, 540, 'Singapore: outcome', W78, t / 1.6, hl=0, label_txt='OFFICIAL STATEMENT', w=1000)), zoom=(1.0, 1.1), sfx=[(.1, 'paper')])),
                   (.5, lambda t0: dict(draw=plain(lambda c, t: doc(c, 960, 540, 'Singapore: outcome', W78, 3, hl=3, hl_t=0, label_txt='OFFICIAL STATEMENT', w=1000)), zoom=(1.15, 1.3), focus=(960, 600),
                                        hud=lambda c, t: Wd.stamp(c, 'Entry banned', 1080, 700, t - .3, GOLD, rot=-8, size=90), sfx=[(.3, 'stamp')], shake=shake(.3)))])
    add('n079', lambda c, t: (Wd.text_card(c, tl.by_id['n079']['text'], max(t - .3, 0), ['Reported.', 'proven.'], dur=D('n079')), Wd.stamp(c, 'Unproven', 1480, 860, t - D('n079') * .75, GOLD, rot=-8, size=90)),
        zoom=(1.0, 1.03), sfx=[(D('n079') * .75, 'stamp')], shake=shake(D('n079') * .75))
    lw80 = Actor('lawyer', 1500, 1000, 1.0, face=-.6, rim=NR).walk_to(0, 1.4, 1100).pose(1.4, ('hold', 'down'))
    def briefcase(c, t):
        x = 1500 - 400 * ease(K(t, 0, 1.4)); rect(c, x + 40, 820, x + 140, 900, '#5A3B24', 5, r=8); c.drawLine(x + 70, 820, x + 110, 820, kit.ink(10))
    def knock(c, t):
        big_door(c, 9, .1, plate='HOME'); hit = [(.4, 0), (.75, 1), (1.1, 2)]
        pull = sum(math.exp(-max(t - h, 0) * 10) * (t > h) for h, _ in hit)
        A.sleeve(c, W + 80, 900, 1180 - 40 * min(pull, 1), 640, col='#22283A', cuff=WHITE, skin='#EFCFB2')
    multi('n080', [(.55, lambda t0: dict(draw=shots.wide('night/apartment_hallway', [], [lw80], overlay=briefcase, t0=t0), zoom=(1.0, 1.15), focus=((1300, 600), (1100, 580)), sfx=[(0, 'steps', 1.4)],
                                         hud=lambda c, t: (Wd.place_tag(c, 'Nov 5, 2026', (t - .2) / .4, "Huang's home, reportedly"), Wd.lower_third(c, "Nvidia's top lawyer", 'As reported', (t - 1.0) / .5)))),
                   (.45, lambda t0: dict(draw=plain(knock, framed=False), zoom=(1.1, 1.2), focus=(1000, 600), sfx=[(.4, 'stamp'), (.75, 'stamp'), (1.1, 'stamp')],
                                         hud=HUDPOP('are the reports true?', 600, 260, 1.4, GOLD, 72, -3)))])
    add('n081', plain(lambda c, t: big_door(c, 9, .1, plate='HOME'), framed=False), zoom=(1.0, 1.12), focus=(960, 560), hud=HUDPOP('reportedly', 1500, 300, .5, GOLD, 90, -4))
    talk('n081a', 'lawyer', 'night/apartment_hallway', (1250, 600), -.4, None, None, dict(mouth='flat', brow=.4), ('hold', 'down'),
         extra_hud=lambda c, t: Wd.text(c, 'PARAPHRASE OF A REPORTED EXCHANGE - DRAMATISED', 1880, 70, 32, '#9DB0DA', F_LABEL, 'right'))
    talk('n081c', 'jensen', 'night/apartment_hallway', (700, 600), .3, None, None, dict(mouth='flat', eyes='half', brow=-.2), ('down', 'down'), zoom=(1.0, 1.1),
         extra_hud=lambda c, t: Wd.text(c, 'PARAPHRASE OF A REPORTED REPLY - DRAMATISED', 1880, 70, 32, '#9DB0DA', F_LABEL, 'right'))
    def chairs(c, t):
        rect(c, 200, 700, 1720, 780, '#5A3B24', 7, r=10)
        for i, x in enumerate((420, 760, 1160, 1500)):
            empty = i == 2; k = kit.back(K(t, .2 + i * .25, .35))
            if k <= 0: continue
            c.save(); c.translate(x, 700); c.scale(k, k)
            rect(c, -90, -280, 90, 0, '#2B4A7A' if not empty else '#3A3F4F', 6, r=18)
            if empty: c.drawRect(skia.Rect(-110, -300, 110, 20), fp(GOLD, int(60 + 40 * math.sin(t * 5)), blur=20))
            rect(c, -100, 20, 100, 70, PAPER, 4, r=4); Wd.text(c, 'HUANG?' if empty else 'CHAIR', 0, 58, 32, NAVY, F_LABEL, 'center'); c.restore()
    add('n081b', plain(chairs), zoom=(1.0, 1.1), sfx=[(.2, 'pop'), (.45, 'pop'), (.7, 'pop')], hud=HUDPOP('closed-door briefing', 960, 170, 1.0, GOLD, 80, -2))
    W82 = ['November 8, 2026', '"I was unfaithful to my wife."', 'Her name: __________']
    add('n082', plain(lambda c, t: doc(c, 960, 540, 'Note to colleagues', W82, t / 1.6, hl=2, hl_t=1.2, label_txt='REAL NOTE, QUOTED')), zoom=(1.0, 1.15), focus=((960, 540), (900, 620)), sfx=[(.1, 'paper')],
        hud=HUDPOP('no name', 1500, 860, D('n082') * .6, GOLD, 90, -4))
    dirs = [Actor('director', 520, 1060, 1.05, face=.4, rim='#FFE3A6', light=1), Actor('director2', 1320, 1000, 1.0, face=-.4, rim='#FFE3A6', light=1)]
    def folder(c, t):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#0A1226', 110))
        x = 1800 - 840 * ease_out(K(t, .3, .8)); rect(c, x - 160, 860, x + 160, 960, '#C9A26A', 6, r=6); Wd.text(c, 'INDEPENDENT INVESTIGATION', x, 922, 24, NAVY, F_LABEL, 'center')
    multi('n083', [(.5, lambda t0: dict(draw=shots.wide('day/boardroom', [], dirs, overlay=folder, t0=t0), zoom=(1.0, 1.12), focus=(960, 600), sfx=[(.4, 'paper')],
                                        hud=lambda c, t: Wd.place_tag(c, "Nvidia's board", (t - .2) / .4, 'Nov 2026'))),
                   (.5, lambda t0: dict(draw=plain(lambda c, t: doc(c, 960, 540, "The board's statement", ['No reason to believe national', 'security or Nvidia secrets', 'were compromised'], t / 1.4, hl=0, label_txt="THE BOARD'S WORDS")),
                                        zoom=(1.0, 1.12), sfx=[(.1, 'paper')]))])
    talk('n083b', 'director', 'day/boardroom', (700, 600), .4, 'The Director', 'Dramatised', dict(mouth='flat', brow=.3), ('push', 'down'), rim='#FFE3A6', light=1)
    def phone_slide(c, t):
        props.phone_flat(c, 1800 - 500 * ease_out(K(t, .2, .5)), 960, 1.2, lit=1.0, t=0)
    talk('n083c', 'director2', 'day/boardroom', (1250, 600), -.4, 'The Second Director', 'Dramatised', dict(mouth='flat', eyes='half'), ('push', 'down'), rim='#FFE3A6', light=1, overlay=phone_slide, sfx=[(.3, 'paper')])
    def drop(c, t, d):
        Wd.line_chart(c, 300, 260, 1620, 820, [100, 101, 99, 100, 98, 94.5], K(t, .1, 1.2), ORANGE, labels=['', '', '', '', '', 'NEXT DAY'])
        Wd.counter(c, 1400, 200, 0, 5.0, (t - .3) / 1.4, unit='', loss=True, size=110, suffix='%', label='NVIDIA SHARES, NEXT DAY', decimals=1)
    add('n084', plain(lambda c, t: drop(c, t, D('n084'))), zoom=(1.0, 1.08), sfx=[(1.3, 'falling')])
    talk('n084b', 'trader', 'night/trading', (700, 600), .4, 'The Trader', 'Dramatised', dict(mouth='o', eyes='wide', brow=.6), ('phone', 'down'))
    def coffee(c, t):
        k = K(t, .5, .5); x, y = 1185 + 195 * k, 920 + 200 * k ** 2; c.save(); c.translate(x, y); c.rotate(70 * k)
        rect(c, -50, -70, 50, 70, WHITE, 6, r=10); c.drawRect(skia.Rect(-44, -64, 44, -40), fp('#5A3B24')); c.restore()
        if t > 1.0: [c.drawCircle(1380 + 40 * math.cos(i), 1060 + 10 * math.sin(i * 2), 16, fp('#5A3B24')) for i in range(6)]
    talk('n084c', 'trader', 'night/trading', (1250, 600), -.4, 'The Second Trader', 'Dramatised', dict(mouth='o', eyes='wide', brow=.6), ('hold', 'down'),
         spec=person('trader', hair='curly', hair_col='#1A1414', skin='#8A5A3C', skin_d='#6E4428'), overlay=coffee, sfx=[(.9, 'pop')])
    add('n085', plain(lambda c, t: (Wd.line_chart(c, 300, 260, 1620, 820, [100, 94.5, 92, 90.5, 89], K(t, .1, 1.4), ORANGE, labels=['NOV 6', '', '', '', 'NOV 11']),
                                          Wd.pop_label(c, 'about -11% in five days', 1300, 200, (t - 1.2) / .4, ORANGE, 80, rot=-3))), zoom=(1.0, 1.1), sfx=[(1.2, 'falling')])
    multi('n086', [(.35, lambda t0: dict(draw=plain(lambda c, t: date_cal(c, 960, 520, 9, 'AUGUST 2025', 1, 30, 1.0, s=1.5, circle_at=0)), zoom=(1.3, 1.05), sfx=[(.1, 'pop')],
                                         hud=HUDPOP('remember?', 1500, 260, .2, GOLD, 90, -4))),
                   (.65, lambda t0: dict(draw=plain(lambda c, t: doc(c, 960, 540, 'Megaspeed statement, Nov 15', ['She left more than a year ago', 'We are investigating ourselves'], t / 1.6, hl=0, label_txt="THE COMPANY'S WORDS")),
                                         zoom=(1.0, 1.12), sfx=[(.1, 'paper')]))])
    add('n087', plain(lambda c, t: A.hand_slam(c, 960, 540, t, 'paper', 'Form 8-K: Nvidia', ['Nov 12, 2026', 'CEO resigned', 'Effective immediately'], hit=.3, rot=-4)),
        zoom=(1.0, 1.12), sfx=[(.3, 'stamp'), (D('n087') * .65, 'stamp')], shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t, hit=.3) if t < 1 else shake(D('n087') * .65)(t),
        hud=lambda c, t: (Wd.stamp(c, 'Resigned', 1250, 800, t - D('n087') * .65, GOLD, rot=-8, size=100), Wd.text(c, 'SEC FILING', 1880, 1000, 34, '#9DB0DA', F_LABEL, 'right')))
    add('n088', shots.card('text', D('n088'), text=tl.by_id['n088']['text'], gold_words=['warned?']), zoom=(1.0, 1.03))

    # ================= CH5 "Look Inside the Box" (day print, lesson) =================
    chapter(5, 'Look Inside the Box')
    def board_bg(c): rect(c, 600, 110, 1500, 640, '#F8FAFD', 8, r=10)
    def teacher(pose=('down', 'point'), **e): return Actor('analyst', 470, 1000, 1.1, face=.35, light=1, rim=DR).pose(.2, pose).expression(0, **e)
    def your_money(c, t):
        board_bg(c); Wd.text(c, 'YOUR MONEY', 1050, 300, 90, NAVY, F_TITLE, 'center')
        Wd.arrow(c, 1050, 380, 1050, 560, (t - .6) / .5, GOLD, 50); [Wd.coin(c, 900 + i * 150, 590, 34) for i in range(3) if t > 1.0 + i * .2]
    add('n090', shots.wide('day/lesson', [], [teacher()], overlay=your_money, t0=at('n090')), zoom=(1.0, 1.08), focus=(1000, 520), whip_in=True, sfx=[(0, 'whoosh'), (1.0, 'coin')])
    def laptop_day(c, x, y, s, t, lines=('401(k)', 'Index fund')):
        c.save(); c.translate(x, y); c.scale(s, s)
        rect(c, -200, -260, 200, 0, '#2E2E38', 6, r=12); rect(c, -180, -240, 180, -20, '#F8FAFD', 3, r=6)
        for i, ln in enumerate(lines): Wd.text(c, ln, -150, -170 + i * 70, 44, NAVY, F_LABEL)
        kit.poly(c, [(-240, 0), (240, 0), (270, 40), (-270, 40)], '#3A3F4F', 6); c.restore()
    sv91 = Actor('saver', 760, 985, .98, face=.3, light=1, rim=DR).pose(.3, ('down', 'chin')).expression(0, mouth='flat')
    add('n091', shots.wide('day/living', [], [sv91], overlay=lambda c, t: laptop_day(c, 1250, 900, .9, t), t0=at('n091')), zoom=(1.1, 1.25), focus=((900, 620), (1050, 600)),
        hud=HUDPOP('you probably own Nvidia', 1350, 220, .8, GOLD, 80, -3))
    talk('n091b', 'saver', 'day/living', (700, 560), .4, 'The Saver', 'Dramatised', dict(mouth='flat', brow=.5, brow_tilt=-.4), ('shrug', 'shrug'), rim=DR, light=1)
    def vcall(c, t): rect(c, 40, 40, W - 40, H - 40, None, 14, v='#2E2E38'); kit.circ(c, 110, 110, 16, GOLD, 0); Wd.text(c, 'VIDEO CALL', 140, 124, 40, NAVY, F_LABEL)
    talk('n091c', 'analyst', 'day/lesson', (1250, 560), -.4, 'The Analyst', 'Dramatised', dict(mouth='smile'), ('point', 'down'), rim=DR, light=1, extra_hud=vcall)
    def stmt_hold(c, t): hx_, hy_ = kit.hand_pos(960, 1390, 2.15, ('hold', 'chin'), -1); props.paper_in_hand(c, hx_, hy_, .9)
    talk('n091d', 'saver', 'day/living', (700, 560), .4, None, None, dict(mouth='flat', eyes='half', brow=-.4), ('hold', 'chin'), rim=DR, light=1, overlay=stmt_hold, zoom=(1.08, 1.0))
    talk('n091e', 'analyst', 'day/lesson', (1250, 560), -.4, None, None, dict(mouth='smirk', eyes='half'), ('present', 'down'), rim=DR, light=1, extra_hud=vcall, sfx=[(D('n091e') * .7, 'pop')])
    def pie(c, t, share=6.0, label='NVIDIA'):
        e = ease_out(K(t, .1, 1.0)); cx, cy, r = 760, 560, 330
        c.drawCircle(cx + 10, cy + 14, r, fp((0, 0, 0), 60, blur=14)); c.drawCircle(cx, cy, r, fp('#2B4A7A')); c.drawCircle(cx, cy, r, kit.ink(7))
        for i in range(10): a = math.radians(-90 + i * 36); c.drawLine(cx, cy, cx + r * math.cos(a), cy + r * math.sin(a), kit.ink(3, '#9DB0DA', 120))
        sweep = 360 * share / 100 * e; p = skia.Path(); p.moveTo(cx, cy); p.arcTo(skia.Rect(cx - r - 20, cy - r - 20, cx + r + 20, cy + r + 20), -90, sweep, False); p.close()
        c.drawPath(p, fp(NG)); c.drawPath(p, kit.ink(6))
        Wd.text(c, 'S&P 500 INDEX FUND', 1400, 360, 54, WHITE, F_LABEL, 'center')
        Wd.counter(c, 1400, 560, 0, share, (t - .2) / 1.0, unit='', suffix='%', label=label + ' (ABOUT)', decimals=0, size=120)
    add('n092', plain(pie), zoom=(1.0, 1.08), sfx=[(.2, 'tick'), (1.2, 'ding')])
    add('n092b', plain(lambda c, t: (Wd.line_chart(c, 300, 260, 1620, 820, [1, 2, 3.5, 5, 7, 8.5, 6], K(t, .1, 1.6), GOLD, labels=['2022', '', '', '', '', 'SPRING', 'NOW']),
                                           Wd.pop_label(c, '~8.5%', 1340, 300, (t - 1.3) / .4, GOLD, 80, rot=-3), Wd.pop_label(c, '~1%', 330, 760, (t - .3) / .4, WHITE, 70, rot=-3),
                                           Wd.text(c, "NVIDIA'S SHARE OF THE S&P 500 (APPROX.)", 960, 950, 36, '#9DB0DA', F_LABEL, 'center'))), zoom=(1.0, 1.1), sfx=[(1.3, 'pop')])
    def bundles(c, t):
        for i in range(10):
            x = 420 + (i % 5) * 270; y = 520 + (i // 5) * 260; out = i == 4
            dy = -180 * ease_out(K(t, 1.4, .5)) if out else 0
            if out and t > 1.4: c.drawRect(skia.Rect(x - 120, y + dy - 90, x + 120, y + dy + 70), fp(GOLD, 70, blur=18))
            Wd.cash_stack(c, x, y + dy, n=6, s=1.4); Wd.text(c, '$1,000', x, y + dy + 100, 36, WHITE, F_LABEL, 'center')
        Wd.counter(c, 960, 160, 0, 600, (t - .2) / 1.2, label='of every $10,000', size=100)
    add('n093', plain(bundles), zoom=(1.0, 1.06), sfx=[(.2, 'tick'), (1.4, 'cash')])
    def cushion(c, t):
        base = 640; e = ease_out(K(t, .2, .8))
        rect(c, 560, base, 860, base + 240 * e, ORANGE, 6); Wd.text(c, 'NVIDIA', 710, base - 30, 54, WHITE, F_LABEL, 'center'); Wd.text(c, '-11%', 710, base + 150 * e, 60, WHITE, F_LABEL, 'center') if e > .5 else None
        rect(c, 1060, base - 90 * e, 1360, base, '#9DB0DA', 6); Wd.text(c, 'THE REST OF THE INDEX', 1210, base - 90 * e - 30, 44, WHITE, F_LABEL, 'center')
        c.drawLine(400, base, 1520, base, kit.ink(5, WHITE)); Wd.pop_label(c, 'this time', 1450, 260, (t - D('n094') * .7) / .4, GOLD, 90, rot=-4)
    add('n094', plain(cushion), zoom=(1.0, 1.08), focus=(960, 600))
    def conc(c, t):
        base = 900
        for i, (lbl, v, col) in enumerate((('A DECADE AGO: TOP 10', 19, '#9DB0DA'), ('TODAY: TOP 7', 33, GOLD))):
            x = 640 + i * 640; hgt = 600 * v / 33 * ease_out(K(t, .2 + i * 1.0, .8)); rect(c, x - 160, base - hgt, x + 160, base, col, 6)
            Wd.text(c, lbl, x, base + 70, 46, WHITE, F_LABEL, 'center')
            if hgt > 10: Wd.text(c, ('under 1/5', 'about 1/3')[i], x, base - hgt - 30, 60, col, F_LABEL, 'center')
        c.drawLine(300, base, 1620, base, kit.ink(5, WHITE))
    multi('n095', [(.55, lambda t0: dict(draw=plain(conc), zoom=(1.0, 1.06), sfx=[(.2, 'pop'), (1.2, 'pop')], hud=lambda c, t: Wd.text(c, 'SHARE OF THE S&P 500 (APPROX.)', 960, 120, 40, '#9DB0DA', F_LABEL, 'center'))),
                   (.45, lambda t0: dict(draw=plain(lambda c, t: conc(c, 9)), zoom=(1.1, 1.2), focus=((1050, 640), (1150, 640)), hud=HUDPOP('seven companies', 600, 300, .3, GOLD, 90, -3)))])
    def seesaw(c, t):
        Wd.text_card(c, tl.by_id['n096']['text'], max(t - .3, 0), ['concentration', 'one'], dur=D('n096'))
        ang = -12 * ease(K(t, 1.2, .8)) + 2 * math.sin(t * 2); c.save(); c.translate(960, 900); c.rotate(ang)
        rect(c, -420, -12, 420, 12, GOLD, 4, r=6); c.drawCircle(-360, -50, 36, fp('#9DB0DA')); c.drawCircle(-290, -50, 36, fp('#9DB0DA')); c.drawCircle(360, -60, 46, fp(WHITE)); c.restore()
        kit.poly(c, [(960, 912), (920, 990), (1000, 990)], '#9DB0DA', 4)
    add('n096', seesaw, zoom=(1.0, 1.03))
    FLAGS = ['A few companies, most of your fund', 'One founder holds it together', 'One customer drives the growth', "Big customers you can't check", 'Rules move after the headlines']
    def flags_board(c, t, n_show, new_t=0.3):
        board_bg(c); Wd.text(c, 'RED FLAGS', 1050, 190, 72, NAVY, F_TITLE, 'center')
        for i in range(5):
            y = 270 + i * 76; kit.rect(c, 650, y - 32, 1460, y + 20, None, 2, v='#C9D3EA', r=6)
            if i < n_show:
                u = 1 if i < n_show - 1 else K(t, new_t, .35)
                if u > 0:
                    kit.poly(c, [(660, y - 30), (660, y + 6), (694, y - 12)], ORANGE, 4); c.drawLine(660, y - 30, 660, y + 24, kit.ink(6))
                    Wd.pop_label(c, f'{i + 1}. ' + FLAGS[i], 1070, y, u, NAVY, 48, rot=0, stroke=0)
    add('n097', shots.wide('day/lesson', [], [teacher(('down', 'present'))], overlay=lambda c, t: flags_board(c, t, 0), t0=at('n097')), zoom=(1.0, 1.05), focus=(1000, 500))
    for k, lid in enumerate(('n098', 'n099', 'n100', 'n101', 'n102')):
        fy = 270 + k * 76
        if k in (1, 3):   # close-up of the teacher with the new flag on a card beside him (owner: no 6 identical board shots)
            def flag_card(c, t, k=k):
                u = K(t, .3, .35)
                if u > 0:
                    c.save(); c.translate(1470, 800); c.scale(kit.back(u) * .78, kit.back(u) * .78); c.rotate(-3); rect(c, -380, -110, 380, 110, '#F8FAFD', 6, r=10)
                    kit.poly(c, [(-350, -60), (-350, -10), (-306, -35)], ORANGE, 4); Wd.text(c, f'{k + 1}. ' + FLAGS[k], -290, -18, 40, NAVY, F_LABEL); c.restore()
            talk(lid, 'analyst', 'day/lesson', (700, 560), .4, None, None, dict(mouth='flat', brow=.3), ('down', 'count'), rim=DR, light=1, extra_hud=flag_card, sfx=[(.3, 'pop')])
        else:
            tch = teacher(('down', 'point'), mouth='flat')
            add(lid, shots.wide('day/lesson', [], [tch], overlay=lambda c, t, k=k: flags_board(c, t, k + 1), t0=at(lid)), zoom=((1.05, 1.3), (1.25, 1.05), (1.0, 1.15))[k // 2],
                focus=((1000, 500), (1060, min(fy + 40, 470))) if k != 2 else ((1060, 420), (900, 520)), rot=(0, 0) if k != 4 else (-1.5, 1.5), sfx=[(.3, 'pop')])
    def look_inside(c, t):
        board_bg(c); Wd.text(c, 'EDUCATION, NOT FINANCIAL ADVICE', 1050, 210, 44, NAVY, F_LABEL, 'center')
        A.hand_slam(c, 1050, 430, t - D('n103') * .55, 'sticky', 'Look inside the box', hit=.25, rot=-4, sleeve_col='#E5E5E5')
    add('n103', shots.wide('day/lesson', [], [teacher(('down', 'present'), mouth='smile')], overlay=look_inside, t0=at('n103')), zoom=(1.0, 1.06), focus=(1000, 480),
        shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t - D('n103') * .55, hit=.25), sfx=[(D('n103') * .55 + .25, 'stamp')])

    # ================= ENDING (night) =================
    def n110(c, t): smartphone(c, 960, 560, t, s=.92, ring=False)
    add('n110', shots.wide('night/office', [], overlay=n110), zoom=(1.1, 1.0), focus=(960, 540), whip_in=True, sfx=[(0, 'whoosh'), (D('n110') * .6, 'pop')],
        hud=HUDPOP('"normal"', 1450, 300, D('n110') * .6, GOLD, 130, -5))
    PROPS5 = ['A company', 'A woman', 'A CEO', 'A letter', 'A resignation']
    def five(c, t):
        d = D('n111'); start = .1
        for i in range(5):
            k = kit.back(K(t, start + i * (d * .6 / 5), .3))
            if k <= 0: continue
            x = 260 + i * 350; c.save(); c.translate(x, 560 + 6 * math.sin(t * 2 + i)); c.scale(k, k)
            if i == 0: props.sign_megaspeed(c, 0, 0, .5, glow=.6)
            elif i == 1: kit.rect(c, -110, -150, 110, 150, '#2B3F70', 6, r=10); Wd.text(c, '?', 0, 40, 140, GOLD, F_TITLE, 'center')
            elif i == 2: kit.rect(c, -140, -60, 140, 60, '#F4EFE2', 6, r=10); Wd.text(c, 'CEO', 0, 22, 60, NAVY, F_TITLE, 'center')
            elif i == 3: kit.rect(c, -130, -90, 130, 90, '#E9DFC8', 6); kit.poly(c, [(-130, -90), (130, -90), (0, 10)], '#DDD1B6', 5)
            else: kit.rect(c, -100, -140, 100, 140, PAPER, 6); Wd.text(c, '8-K', 0, -60, 50, NAVY, F_TITLE, 'center')
            Wd.text(c, PROPS5[i].upper(), 0, 230, 40, WHITE, F_LABEL, 'center'); c.restore()
    add('n111', plain(five), zoom=(1.0, 1.06), sfx=[(.1 + i * D('n111') * .12, 'pop') for i in range(5)], hud=HUDPOP('what we can prove', 960, 170, .3, GOLD, 80, -2))
    def q_card(c, t):
        Wd.text_card(c, tl.by_id['n112']['text'], max(t - .3, 0), ['question.'], dur=D('n112'))
        c.save(); c.translate(960, 860); c.rotate(-3 + math.sin(t) * 1.5); kit.rect(c, -150, -90, 150, 90, '#E9DFC8', 5); kit.poly(c, [(-150, -90), (150, -90), (0, 10)], '#DDD1B6', 4); c.restore()
    add('n112', q_card, zoom=(1.0, 1.03))
    add('n113', shots.card('text', D('n113'), text=tl.by_id['n113']['text'], gold_words=['knew', 'when?']), zoom=(1.0, 1.03))
    def teaser(c, t):
        k = kit.back(K(t, .1, .4)); c.save(); c.translate(960, 420); c.scale(k, k)
        Wd.text(c, 'THE NVIDIA FILES', 0, -60, 56, '#9DB0DA', F_LABEL, 'center'); Wd.text(c, 'PART 2', 0, 70, 140, GOLD, F_TITLE, 'center', stroke=14); c.restore()
        if t > .7: Wd.text(c, 'THE BRIEFINGS', 960, 680, 80, WHITE, F_TITLE, 'center', alpha=int(255 * K(t, .7, .4)))
        for i in range(4):
            x = 560 + i * 270; k2 = K(t, 1.0 + i * .15, .3)
            if k2 > 0: c.save(); c.translate(x, 880); kit.rect(c, -90, -60, 90, 60, PAPER, 5, r=6); c.drawRect(skia.Rect(-70, -30, 50, -16), fp('#14141A')); c.drawRect(skia.Rect(-70, 0, 70, 14), fp('#14141A')); c.restore()
    add('n114', plain(teaser), zoom=(1.0, 1.08), sfx=[(.1, 'boom')])
    S.append(dict(name='outro', dur=tl.dur('outro', 'endscreen'), draw=lambda c, t: A.outro(c, t), zoom=(1, 1.02)))
    S.append(dict(name='subscribe', dur=tl.dur('endscreen', 'end'), draw=lambda c, t: A.subscribe_next(c, t, 'Part 2: The Briefings', series='The Nvidia Files'), zoom=(1, 1.02), sfx=[(1.8, 'pop'), (2.1, 'ding')]))
    STAGES = {'desk': 'n053_2 n004_2 n009 n009_2 n013b n013b_2 n016_2 n017 n033_2 n034 n034_2 n037_2 n043 n043_2 n053b n053b_2 n056 n063 n064 n071 n071_2 n072 n077 n078 n078_2 n082 n083_2 n086_2 n087',
              'night/newsroom': 'n002 n002_2 n044b n044b_2 n070',
              'night/nvidia_office': 'n084 n085 n092 n092b n093 n094 n095 n095_2',
              'night/megaspeed': 'n035 n041 n042 n044b_3 n086',
              'night/office': 'n004 n031_2 n075 n076 n076_2 n081b n050 n051',
              'night/datacenter': 'n014_2 n030_2 n015 n015_2',
              'night/investigation_room': 'n032_2',
              'night/restaurant': 'n045_2',
              'day/shop_counter': 'n054 n054_2'}
    where = {n: k for k, v in STAGES.items() for n in v.split()}
    for x in S:
        if x['name'] in where and hasattr(x['draw'], '__code__'): x['draw'].stage = where[x['name']]
    return S
