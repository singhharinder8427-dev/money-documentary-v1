"""Shot list - The Nvidia Files, Part 2: "Who Warned Trump About Nvidia's CEO?" (~6 min, no end screen).
Follows shot_plan.md. Only LOCKED assets + new props_dc.hand_mic / passport (PENDING). Night print; Ch5 = day lesson room.
Legal rules in the picture: briefing claims are attributed in the narration; DISPUTED stamp only where sources conflict (no REPORTED stamps, owner 24 Nov); Trump / Rubio / Lutnick mouths stay flat;
the only words ever shown in a real person's name are documented ones (Trump "I haven't heard that", Nov 16). Alice never speaks.
QA: make_video.py qa (3 frames per shot) before any render (CLAUDE.md 4b)."""
import math, skia, json as _json, pathlib as _pl
from engine import shots, widgets as Wd, anim as A, kit, props, props_dc as PD
from engine.actor import Actor
from engine.cast import person
from engine.core import W, H, GOLD, ORANGE, WHITE, NAVY, NAVY2, PAPER, F_LABEL, F_TYPE, F_TITLE
from engine.kit import rect, label, fp, ease, ease_out, K
from engine.sets import get_set

NG = '#76B900'                                                    # Nvidia brand green (rule 3b)
_SCRIPT = _json.load(open(_pl.Path(__file__).resolve().parent / 'script.json'))
SHOT_BREAKS = tuple(l['id'] for l in _SCRIPT['lines'])          # every line starts its own picture
NR, DR = '#9FB8F0', '#FFE3A6'

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
    def card_shot(marker, draw, **kw): S.append(dict(name=marker.replace(':', ''), dur=tl.dur(marker, nxt_ev(marker)), draw=draw, **kw))
    def chapter(n, title): card_shot(f'chapter:{n}', shots.card('chapter', 2.2, n=n, title=title))
    def say(a, lid): return a.say(tl, lid, mouths)
    D = lambda lid: tl.dur(lid, nxt(lid))
    shake = lambda hit: A.stamp_shake(hit)
    plain = shots.plain
    HUDPOP = lambda txt, x, y, t0, col=GOLD, size=110, rot=-4: (lambda c, t: Wd.pop_label(c, txt, x, y, (t - t0) / .4, col, size, rot=rot))
    LT = lambda name, role, t0=.3: (lambda c, t: Wd.lower_third(c, name, role, (t - t0) / .5))
    def both(*fs): return lambda c, t: [f(c, t) for f in fs]
    def desk(overlay): return shots.desk(overlay, 'night/desk_clean')
    def pshake(hit): return lambda t: A.stamp_shake(hit)(t)

    # ---------- shared little drawings ----------
    def year_cal(c, x, y, t, y0, y1, dur, s=1.5, label_txt='YEAR'):
        k = K(t, 0, dur); yr = int(round(y0 + (y1 - y0) * ease(k)))
        c.save(); c.translate(x, y); c.scale(s, s)
        rect(c, -180, -200, 180, 220, PAPER, 6, r=10); rect(c, -180, -200, 180, -110, NAVY, 6, r=10)
        Wd.text(c, label_txt, 0, -140, 42, WHITE, F_LABEL, 'center'); Wd.text(c, str(yr), 0, 100, 96, NAVY, F_TITLE, 'center')
        for i in range(2): kit.circ(c, -90 + i * 180, -200, 14, '#8C93A6', 4)
        c.restore()
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
    def doc(c, x, y, title, lines, u, hl=None, w=900, h=640, rot=-2, hl_t=.9, label_txt=None):
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
    def flashes(times, big=1.0):
        def f(c, t):
            for tt in times:
                d = t - tt
                if 0 <= d < .18: c.drawRect(skia.Rect(0, 0, W, H), fp('#FFFFFF', int(150 * big * (1 - d / .18))))
        return f
    def stars(c, t, n=70):
        import random as _r; r = _r.Random(11)
        for i in range(n): c.drawCircle(r.uniform(0, W), r.uniform(0, 640), r.uniform(1.5, 3.6), fp('#FFFFFF', int(150 + 90 * math.sin(t * 2 + i))))
    def stamp_on(txt, x, y, t0, rot=-8, size=100, s=1.0):
        return lambda c, t: PD.prop_stamp(c, s, x, y, t - t0, rot=rot, size=size)
    def talk(lid, who, set_name, focus, face, tag=None, role=None, expr=None, pose=('down', 'down'), zoom=(1.0, 1.06), overlay=None, extra_hud=None, sfx=None, rim=NR, light=-1):
        """Dialogue / close-up with the name + role lower-third (standing rule)."""
        a = say(Actor(who, 960, 1390, 2.15, face=face, rim=rim, light=light).pose(.2, pose).expression(0, **(expr or {})), lid)
        def hud(c, t):
            if tag: Wd.lower_third(c, tag, role, (t - .3) / .5)
            if extra_hud: extra_hud(c, t)
        add(lid, shots.closeup(set_name, a, focus=focus, overlay=overlay, t0=at(lid)), zoom=zoom, hud=hud, **({'sfx': sfx} if sfx else {}))

    # ---- actors reused in several shots (real people: mouths flat on every line, see Risks for QA) ----
    def trump(x=960, y=900, s=.98, face=-.3, **e): return Actor('trump', x, y, s, face=face, rim=NR).expression(0, mouth='flat', eyes='dot', **e)
    def rubio(x, y, s=1.05, face=.3, **e): return Actor('rubio', x, y, s, face=face, rim=NR).expression(0, mouth='flat', eyes='dot', **e)

    # ================= HOOK =================
    # 1  n001 (a) lit portico, flashes, close on the reporter; (b) push to Trump at the podium, mic enters
    rep_a = Actor('reporter2', 620, 960, .8, face=.3, rim=NR).expression(0, mouth='mid', eyes='dot').pose(.3, ('hold', 'down'))
    cam = [Actor('reporter', 1300, 960, .8, face=-.4, rim=NR), Actor('worker', 1500, 970, .75, face=-.5, rim=NR)]
    tr1 = trump(960, 980, .95, -.35).pose(.3, ('down', 'down'))
    rep_b = Actor('reporter2', 560, 960, .9, face=.35, rim=NR).expression(0, mouth='mid', eyes='dot').pose(.3, ('hold', 'down'))
    def held_mic(c, hp, s, rot):
        r_ = math.radians(rot); PD.hand_mic(c, hp[0] + 50 * s * math.sin(r_), hp[1] - 50 * s * math.cos(r_), s, rot=rot, arm=False)
    def mic_b(c, t):
        k = ease_out(K(t, .2, .7)); hp = kit.hand_pos(560, 960, .9, ('hold', 'down'), -1); held_mic(c, (hp[0] - (1 - k) * 140, hp[1] + (1 - k) * 60), .8, 35)
    def n001a(t0): return dict(draw=shots.wide('night/white_house', [rep_a] + cam, overlay=flashes([.2, .55, .9, 1.3]), t0=t0), zoom=(1.9, 1.15), focus=((640, 700), (960, 640)),
                               hud=lambda c, t: Wd.place_tag(c, 'Washington', (t - .2) / .4, 'Nov 16'), sfx=[(.2, 'shutter'), (.55, 'shutter'), (.9, 'shutter')])
    def n001b(t0): return dict(draw=shots.wide('night/white_house', [rep_b, tr1], overlay=lambda c, t: (mic_b(c, t), flashes([.6, 1.4], .7)(c, t)), t0=t0), zoom=(1.1, 1.55), focus=((900, 700), (960, 640)),
                               hud=LT('Donald Trump', 'President', .5), sfx=[(.2, 'whoosh'), (.6, 'shutter')])
    multi('n001', [(.4, n001a), (.6, n001b)])

    # 3-4  n002 newspaper spins in (headline hidden) + REPORTED; the classified folder lands + TOP SECRET
    def paper(c, t):
        A.newspaper(c, 960, 540, t, 'The Washington Post', ' ', None)
        for i, w_ in enumerate((900, 760, 840)): c.drawRoundRect(skia.Rect(960 - w_ / 2, 400 + i * 100, 960 + w_ / 2, 470 + i * 100), 12, 12, fp(NAVY, 200 if t > .7 else 0, blur=10))
    def n002a(t0): return dict(draw=desk(lambda c, t: paper(c, t)), zoom=(1.0, 1.1), sfx=[(.05, 'whoosh')],
                               hud=lambda c, t: Wd.text(c, 'THE WASHINGTON POST', 1880, 70, 34, '#9DB0DA', F_LABEL, 'right'))
    def folder_in(c, t):
        k = ease_out(K(t, .1, .55)); PD.memo_folder(c, 760 + (1 - k) * 900, 560 + 6 * math.sin(t * 2), 1.5, rot=-8 + (1 - k) * 20, label_text='MEMO')
        PD.prop_stamp(c, 'Top secret', 900, 420, t - .9, rot=-8, size=100)
    def n002b(t0): return dict(draw=desk(folder_in), zoom=(1.05, 1.2), focus=((960, 540), (860, 520)), sfx=[(.1, 'paper'), (.9, 'stamp')], shake=shake(.9), hud=HUDPOP('a warning about Nvidia\'s CEO', 960, 940, .5, WHITE, 70, -2))
    multi('n002', [(.5, n002a), (.5, n002b)])

    # 5  n003 the one documented quote, typed card, held beat of silence
    def n003(c, t):
        Wd.text_card(c, tl.by_id['n003']['text'], max(t - .3, 0), ['heard'], dur=D('n003'))
        Wd.text(c, 'PRESIDENT TRUMP, NOV 16', 960, 1010, 34, '#9DB0DA', F_LABEL, 'center')
    add('n003', n003, zoom=(1.0, 1.03), sfx=[(.3, 'type_key')])

    # 6-7  n004 the oval office, calendar FALL 2025; then Air Force One, calendar MAY 2026, two gold REPORTED stamps
    def n004a(t0): return dict(draw=shots.wide('night/oval_office', [trump(960, 900, .98, 0)], overlay=lambda c, t: cal_page(c, 1470, 560, t, 'LAST FALL', '2025', s=.8), t0=t0), zoom=(1.3, 1.1), focus=((960, 800), (1100, 700)), sfx=[(.2, 'page')])
    def n004b(t0): return dict(draw=shots.wide('night/af1_cabin', [rubio(700, 1010, 1.05, .35), trump(1220, 1010, 1.05, -.3)], overlay=lambda c, t: (cal_page(c, 1600, 330, t, 'MAY', '2026', s=.6),), t0=t0), zoom=(1.0, 1.2), focus=((700, 700), (1200, 700)), sfx=[(.2, 'page')])
    multi('n004', [(.45, n004a), (.55, n004b)])

    # 8  n005 sealed crates (Part 1 callback), counter to $4.8 billion, flashlight cone
    def crates(c, t):
        for i, (x, y, s_) in enumerate(((640, 840, 1.1), (900, 880, 1.2), (1200, 850, 1.1), (1480, 880, 1.0))): props.crate(c, x, y, s_, 'SERVERS', glow=.25)
        props.flashlight(c, 1500, 220, 200, length=900, spread=300)
        Wd.counter(c, 960, 330, 0, 4_800_000_000, (t - .2) / 1.8, label='of Nvidia chips bought', size=118)
    add('n005', shots.wide('night/datacenter', [], overlay=crates), zoom=(1.0, 1.5), focus=(960, 560), sfx=[(0, 'amb:hum', None), (.2, 'tick'), (2.0, 'ding')])

    # 9  n006 a phone with the fund pie, one slice glows Nvidia green
    def phone_pie(c, t):
        c.save(); c.translate(960, 560); c.rotate(-3); rect(c, -250, -430, 250, 430, '#1B1D26', 8, r=50); rect(c, -222, -392, 222, 392, NAVY, 3, r=26)
        Wd.text(c, 'MY S&P 500 FUND', 0, -300, 40, WHITE, F_LABEL, 'center'); kit.circ(c, 0, -60, 150, '#2B4A7A', 6)
        p = skia.Path(); p.moveTo(0, -60); p.arcTo(skia.Rect(-150, -210, 150, 90), -90, 36 * ease_out(K(t, .1, .8)), False); p.close(); c.drawPath(p, fp(NG)); c.drawPath(p, kit.ink(5))
        c.drawCircle(60, -190, 40 + 12 * math.sin(t * 6), fp(NG, 60, blur=14)); Wd.text(c, 'NVIDIA', 0, 240, 56, NG, F_LABEL, 'center'); Wd.text(c, 'inside your fund', 0, 310, 34, '#9DB0DA', F_LABEL, 'center'); c.restore()
    add('n006', desk(phone_pie), zoom=(1.0, 1.25), focus=((960, 560), (960, 500)), sfx=[(.2, 'pop')])

    # 10  n007 black card, typed
    add('n007', shots.card('text', D('n007'), text=tl.by_id['n007']['text'], gold_words=['knew?']), zoom=(1.0, 1.03), sfx=[(.3, 'type_key')])

    # ================= TITLE =================
    card_shot('title', shots.card('title', 2.5, title='Who Warned Trump?', gold_word='Warned', sub='The Nvidia Files - Part 2'))

    # ================= CH1 "The Memo" =================
    chapter(1, 'The Memo')
    add('n009', desk(lambda c, t: cal_page(c, 960, 540, t, 'SPRING', '2026', s=1.7)), zoom=(1.0, 1.1), sfx=[(0, 'flips', 1.0)])
    # n010 (a) a courier walks up to the lit portico with a folder; (b) the folder slides across a desk, TOP SECRET
    cou = Actor('worker', 300, 960, .7, face=.5, rim=NR).pose(0, ('hold', 'down')).walk_to(0, 2.6, 900)
    def cour_f(c, t): 
        x = 300 + 600 * min(t / 2.6, 1); PD.memo_folder(c, x + 40, 800, .38, rot=-8)
    def n010a(t0): return dict(draw=shots.wide('night/white_house', [cou], overlay=cour_f, t0=t0), zoom=(1.2, 1.35), focus=((520, 780), (900, 760)), sfx=[(0, 'steps', 2.4)],
                               hud=lambda c, t: Wd.place_tag(c, 'Washington', (t - .2) / .4, 'Spring 2026'))
    def slide(c, t):
        k = ease_out(K(t, .1, .7)); PD.memo_folder(c, 300 + k * 700, 560, 1.5, rot=-6, label_text='MEMO'); PD.prop_stamp(c, 'Top secret', 1000, 420, t - 1.0, rot=-8, size=100)
    def n010b(t0): return dict(draw=desk(slide), zoom=(1.0, 1.15), focus=((960, 540), (1000, 520)), sfx=[(.1, 'paper'), (1.0, 'stamp')], shake=shake(1.0))
    multi('n010', [(.5, n010a), (.5, n010b)])
    # n011 (a) Alice at her desk, silent, alleged; (b) two portrait cards joined by a dotted line, REPORTED
    al = Actor('alice', 960, 1000, 1.0, face=0, rim=NR).expression(0, mouth='flat', eyes='dot').pose(.3, ('down', 'hip'))
    def n011a(t0): return dict(draw=shots.wide('night/megaspeed', [al], overlay=lambda c, t: props.sign_megaspeed(c, 960, 240, .85, glow=.9), t0=t0), zoom=(1.5, 1.2), focus=((960, 600), (960, 520)),
                               hud=LT('Alice Huang (alleged)', 'ex-CEO, Megaspeed'))
    jp, ap_ = Actor('jensen', 560, 1000, 1.05, face=.2, rim=NR), Actor('alice', 1360, 1000, 1.05, face=-.2, rim=NR)
    def portraits(c, t):
        for x, nm, act in ((560, 'JENSEN HUANG', jp), (1360, 'ALICE HUANG (ALLEGED)', ap_)):
            c.save(); c.translate(x, 620); rect(c, -250, -340, 250, 340, '#2B4A7A', 6, r=14); c.save(); c.clipRect(skia.Rect(-244, -334, 244, 334)); c.translate(-x, -620 - 150); act.draw(c, 1.0); c.restore()
            rect(c, -250, 250, 250, 340, NAVY, 6, r=10); Wd.text(c, nm, 0, 312, 34, GOLD, F_LABEL, 'center'); c.restore()
        e = K(t, .4, 1.0)
        for i in range(int(26 * e)): c.drawCircle(830 + i * 10.5, 620, 6, fp(GOLD))
    def n011b(t0): return dict(draw=plain(portraits), zoom=(1.0, 1.08), hud=lambda c, t: Wd.lower_third(c, 'Jensen Huang', 'CEO, Nvidia', (t - .2) / .5, y=80, x=60))
    multi('n011', [(.55, n011a), (.45, n011b)])
    # n012 (a) Singapore shophouse street, (b) passport slam + IMPOUNDED, (c) SINGAPORE SAYS sticky
    def n012a(t0): return dict(draw=shots.wide('night/sg_street', [], overlay=lambda c, t: None), zoom=(1.0, 1.25), focus=((700, 640), (1000, 620)), whip_in=True, sfx=[(.05, 'whoosh')],
                               hud=lambda c, t: Wd.place_tag(c, 'Singapore', (t - .3) / .4, 'June 2025'))
    def pass_slam(c, t):
        k = ease_out(K(t, .1, .4)); PD.passport(c, 960, 520 - (1 - k) * 600, 1.4, rot=-8)
        PD.prop_stamp(c, 'Impounded', 960, 740, t - .8, rot=-8, size=100)
    def n012b(t0): return dict(draw=shots.wide('night/sg_street', [], overlay=pass_slam), zoom=(1.35, 1.2), focus=(960, 620), sfx=[(.4, 'stamp'), (.8, 'stamp')], shake=shake(.8))
    def n012c(t0): return dict(draw=plain(lambda c, t: Wd.sticky(c, 'Singapore says: false declarations, not espionage', 960, 500, (t - .1) / .4, rot=-3, w=620)), zoom=(1.0, 1.08), sfx=[(.15, 'pop')])
    multi('n012', [(.3, n012a), (.35, n012b), (.35, n012c)])
    # n013 recap card + stamp
    def n013(c, t):
        Wd.text_card(c, tl.by_id['n013']['text'], max(t - .3, 0), ['charged.', 'groundless.', 'conclusion.'], dur=D('n013'))
        Wd.stamp(c, 'Alleged - not proven', 1250, 880, t - D('n013') * .75, GOLD, rot=-8, size=66)
    add('n013', n013, zoom=(1.0, 1.03), sfx=[(.3, 'type_key'), (D('n013') * .75, 'stamp')], shake=shake(D('n013') * .75))
    # n014 (a) memo copies fan out to numbered desks, (b) a hand places a copy, REPORTED
    def fan(c, t):
        for i in range(5):
            k = ease_out(K(t, .15 + i * .25, .5)); x = 960 + (i - 2) * 330 * k; y = 560 + (1 - k) * -200 + (i % 2) * 40
            rect(c, x - 110, y - 150, x + 110, y + 150, PAPER, 5, r=4); Wd.text(c, str(i + 1), x, y + 40, 110, NAVY, F_TITLE, 'center'); Wd.text(c, 'COPY', x, y - 90, 34, '#6B7390', F_LABEL, 'center')
    def n014a(t0): return dict(draw=desk(fan), zoom=(1.2, 1.0), focus=(960, 540), sfx=[(.2, 'paper'), (.45, 'paper'), (.7, 'paper'), (.95, 'paper')])
    def n014b(t0): return dict(draw=desk(lambda c, t: (A.hand_slam(c, 960, 540, t, 'paper', 'Memo', ['Copy 3 of 12'], hit=.4))), zoom=(1.1, 1.25), focus=((960, 540), (900, 540)), sfx=[(.4, 'paper')])
    multi('n014', [(.5, n014a), (.5, n014b)])
    # n015-n018 dramatised exchange: officer / analyst / officer / analyst
    talk('n015', 'intel', 'night/office', (500, 520), .4, 'The Officer', 'Dramatised', dict(mouth='flat', eyes='half', brow=.3), ('down', 'chin'), zoom=(1.0, 1.06))
    talk('n016', 'analyst', 'night/office', (1300, 520), -.4, 'The Analyst', 'Dramatised', dict(mouth='flat', brow=.2), ('present', 'down'), zoom=(1.05, 1.0))
    talk('n017', 'intel', 'night/office', (500, 520), .5, None, None, dict(mouth='flat', eyes='half', brow=-.4), ('down', 'chin'), zoom=(1.0, 1.08))
    talk('n018', 'analyst', 'night/office', (1300, 520), -.5, None, None, dict(mouth='flat', eyes='half', brow=.3), ('shrug', 'shrug'), zoom=(1.0, 1.1), sfx=[(D('n018') * .8, 'low_tone')])
    # n019 two stacked memos; the top lifts to show the 2025 date
    def stack(c, t):
        k = ease(K(t, .8, .7)); rect(c, 560, 380, 1360, 860, '#EDE6D2', 5, r=4); Wd.text(c, 'MEMO - 2025', 960, 520, 80, NAVY, F_TITLE, 'center'); Wd.text(c, 'BRIEFING', 960, 620, 54, '#6B7390', F_LABEL, 'center')
        c.save(); c.translate(60 * k, -250 * k); c.rotate(-5 * k); rect(c, 560, 420, 1360, 900, PAPER, 5, r=4); Wd.text(c, 'MEMO - 2026', 960, 560, 80, NAVY, F_TITLE, 'center'); c.restore()
    add('n019', desk(stack), zoom=(1.0, 1.1), sfx=[(.8, 'paper')])

    # ================= CH2 "Air Force One" =================
    chapter(2, 'Air Force One')
    # n020 (a) the oval office: a folder is placed on the desk, REPORTED; (b) memo page, both names circled in gold
    def folder_desk(c, t):
        k = ease_out(K(t, .2, .5)); PD.memo_folder(c, 960, 940 - (1 - k) * 300, .6, rot=-4)
    def n020a(t0): return dict(draw=shots.wide('night/oval_office', [trump(960, 900, .98, 0)], overlay=folder_desk, t0=t0), zoom=(1.1, 1.4), focus=((960, 780), (960, 700)),
                               hud=LT('Donald Trump', 'President', .4), sfx=[(.25, 'paper'), (1.0, 'stamp')], shake=shake(1.0))
    def circled(c, t):
        rect(c, 560, 220, 1360, 860, PAPER, 5, r=4); Wd.text(c, 'ASSESSMENT', 960, 300, 56, NAVY, F_LABEL, 'center')
        for i, (nm, x, y) in enumerate((('Jensen Huang', 780, 480), ('Alice Huang', 1140, 640))):
            Wd.text(c, nm, x, y, 64, NAVY, F_TYPE, 'center'); e = ease(K(t, .5 + i * .6, .5))
            p = skia.Path(); p.addOval(skia.Rect(x - 250, y - 70, x + 250, y + 30)); m = skia.PathMeasure(p, False); dst = skia.Path(); m.getSegment(0, m.getLength() * e, dst, True); c.drawPath(dst, kit.ink(10, GOLD))
        for i in range(3): c.drawLine(640, 380 + i * 34 + (160 if i else 0), 1280, 380 + i * 34 + (160 if i else 0), kit.ink(3, '#B8B0A0'))
    def n020b(t0): return dict(draw=desk(circled), zoom=(1.0, 1.15), focus=((960, 540), (960, 520)), sfx=[(.5, 'pop'), (1.1, 'pop')])
    multi('n020', [(.5, n020a), (.5, n020b)])
    # n021 newspaper line highlighted: took no action
    add('n021', desk(lambda c, t: doc(c, 960, 540, 'The New York Times', ['Reported: briefed on intelligence', 'about Huang\'s closeness.', 'He took no action.'], t / 1.6, hl=2, hl_t=.9, w=980, h=600, label_txt='ATTRIBUTED: NYT')),
        zoom=(1.0, 1.35), focus=((960, 540), (900, 640)), sfx=[(.1, 'paper'), (1.0, 'pop')])
    # n022 (a) a polaroid: the two Huangs (REPORTED), Taipei Jun 7 2024; (b) calendar flips two years
    j_, a_ = Actor('jensen', 760, 1060, 1.18, face=.3, rim=NR).expression(0, mouth='smile', eyes='dot'), Actor('alice', 1160, 1060, 1.18, face=-.3, rim=NR).expression(0, mouth='smile', eyes='dot')
    def photo(c, t):
        st = get_set('night/nvidia_office'); s = skia.Surface(W, H); cv = s.getCanvas(); st.draw(cv, [lambda c_, a=a: a.draw(c_, 1.0) for a in (j_, a_)]); img = s.makeImageSnapshot()
        Wd.polaroid(c, img, K(t, .05, 1.2))
    def n022a(t0): return dict(draw=desk(photo), zoom=(1.0, 1.05), sfx=[(.05, 'shutter')], hud=lambda c, t: (Wd.place_tag(c, 'Taipei', (t - .3) / .4, 'Jun 7, 2024'), Wd.lower_third(c, 'Alice Huang (alleged)', 'with Jensen Huang', (t - 1.2) / .5, y=150, x=1040)))
    def n022b(t0): return dict(draw=plain(lambda c, t: year_cal(c, 960, 520, t, 2024, 2026, D('n022') * .4, s=1.6)), zoom=(1.0, 1.1), sfx=[(0, 'flips', 1.0)], hud=HUDPOP('almost 2 years', 960, 960, .8, GOLD, 100, -3))
    multi('n022', [(.55, n022a), (.45, n022b)])
    # n023 (a) May 12 ringed in gold, (b) Air Force One crosses a starry night
    def n023a(t0): return dict(draw=desk(lambda c, t: cal_page(c, 960, 540, t, 'MAY', '12', s=1.9, ring_at=.5)), zoom=(1.0, 1.08), sfx=[(.5, 'stamp')], shake=shake(.5))
    def sky(c, t):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#0E1830')); stars(c, t); PD.af1_plane(c, -400 + 2700 * ease(K(t, 0, D('n023') * .5)), 540 - 20 * math.sin(t), 1.3, rot=-2, lights=.5 + .5 * math.sin(t * 8))
    def n023b(t0): return dict(draw=shots.plain(sky, framed=False), zoom=(1.0, 1.1), sfx=[(0, 'amb:hum', None)], hud=lambda c, t: Wd.place_tag(c, 'Air Force One', (t - .2) / .4, 'May 12, 2026'))
    multi('n023', [(.4, n023a), (.6, n023b)])
    # n024 (a) the Secretary of State hands the folder across the table; (b) it lands, REPORTED
    rb = rubio(700, 1010, 1.05, .35).pose(.3, ('present', 'down')); tp = trump(1220, 1010, 1.05, -.3)
    def hand_over(c, t):
        k = ease(K(t, .4, .9)); PD.memo_folder(c, 780 + 280 * k, 800, .5, rot=-6)
    def n024a(t0): return dict(draw=shots.wide('night/af1_cabin', [rb, tp], overlay=hand_over, t0=t0), zoom=(1.5, 1.2), focus=((760, 760), (960, 760)), hud=LT('Marco Rubio', 'Secretary of State'), sfx=[(.4, 'paper')])
    def land(c, t):
        PD.memo_folder(c, 960, 800, .6, rot=-4)
    def n024b(t0): return dict(draw=shots.wide('night/af1_cabin', [rb, tp], overlay=land, t0=t0), zoom=(1.2, 1.6), focus=((960, 760), (960, 780)), sfx=[(.7, 'stamp')], shake=shake(.7))
    multi('n024', [(.5, n024a), (.5, n024b)])
    # n025 the delegation boards at the stairs, Jensen in his leather jacket
    jb = Actor('jensen', 300, 940, .55, face=.4, rim=NR).pose(0, ('down', 'down')).walk_to(.3, 2.2, 1130)
    sb = [Actor('banker', 160, 945, .5, face=.4, rim=NR).walk_to(0, 1.6, 980), Actor('worker', 40, 950, .5, face=.4, rim=NR).walk_to(0, 1.9, 1060)]
    def stairs(c, t):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#0E1830')); stars(c, t, 40); c.drawRect(skia.Rect(0, 960, W, H), fp('#1B2540'))
        PD.af1_plane(c, 1060, 640, 2.0, rot=0, lights=.6)
        poly = kit.poly; poly(c, [(1150, 960), (1420, 700), (1470, 700), (1470, 960)], '#8C93A6', 5)
        for a in sb + [jb]: a.draw(c, t, t)
    def n025(t0): return dict(draw=plain(stairs, framed=False), zoom=(1.0, 1.25), focus=((700, 800), (1150, 760)), sfx=[(0, 'steps', 2.0)], hud=LT('Jensen Huang', 'CEO, Nvidia', .6))
    add('n025', n025(0)['draw'], **{k: v for k, v in n025(0).items() if k != 'draw'})
    talk('n026', 'worker', 'night/af1_cabin', (500, 640), .4, 'The Staffer', 'Dramatised', dict(mouth='flat', eyes='half'), ('hold', 'chin'), zoom=(1.0, 1.06),
         overlay=lambda c, t: props.paper_in_hand(c, *kit.hand_pos(960, 1390, 2.15, ('hold', 'chin'), -1), .9, title='DELEGATION', lines=('List: FINAL',)))
    talk('n027', 'banker', 'night/af1_cabin', (1250, 640), -.4, 'The Official', 'Dramatised', dict(mouth='o', eyes='wide', brow=.5), ('down', 'chin'), zoom=(1.0, 1.08))
    talk('n028', 'worker', 'night/af1_cabin', (500, 640), .4, None, None, dict(mouth='flat', eyes='half'), ('hold', 'chin'), zoom=(1.0, 1.0), sfx=[(0, 'amb:hum', None)])
    add('n029', shots.card('text', D('n029'), text=tl.by_id['n029']['text'], gold_words=['twelfth.']), zoom=(1.0, 1.03), sfx=[(.3, 'type_key'), (D('n029') * .7, 'low_tone')])

    # ================= CH3 "The Stall" =================
    chapter(3, 'The Stall')
    add('n030', shots.wide('night/commerce_hq', [], overlay=None), zoom=(1.0, 1.25), focus=((960, 300), (960, 640)), whip_in=True, sfx=[(.05, 'whoosh')], hud=lambda c, t: Wd.place_tag(c, 'Commerce Dept', (t - .3) / .4, 'Washington'))
    # n031 (a) four at the table, one empty chair, REPORTED; (b) three plates slide on: Treasury, Intelligence, Pentagon
    seat = [Actor('analyst', 560, 1010, 1.0, face=.4, rim=NR), Actor('intel', 860, 1010, 1.0, face=.2, rim=NR), Actor('banker', 1380, 1010, 1.0, face=-.4, rim=NR)]
    for s_ in seat: s_.expression(0, mouth='flat', eyes='dot')
    def n031a(t0): return dict(draw=shots.wide('night/commerce_room', seat, t0=t0), zoom=(1.0, 1.2), focus=((560, 700), (1300, 700)))
    def plates(c, t):
        for i, nm in enumerate(('TREASURY', 'INTELLIGENCE', 'PENTAGON')):
            k = ease_out(K(t, .2 + i * .6, .45)); x = 960 + (i - 1) * 520 + (1 - k) * 700
            rect(c, x - 230, 440, x + 230, 600, NAVY, 6, r=10); rect(c, x - 230, 440, x + 230, 456, GOLD, 0, r=6); Wd.text(c, nm, x, 560, 58, WHITE, F_LABEL, 'center')
    def n031b(t0): return dict(draw=desk(plates), zoom=(1.0, 1.1), sfx=[(.2, 'paper'), (.8, 'paper'), (1.4, 'paper')], hud=lambda c, t: Wd.text(c, 'PER AXIOS', 1880, 70, 34, '#9DB0DA', F_LABEL, 'right'))
    multi('n031', [(.5, n031a), (.5, n031b)])
    # n032 (a) Lutnick; (b) AXIOS REPORTS vs COMMERCE DENIES + DISPUTED; (c) Bessent / Trump comments on record
    lu = say(Actor('lutnick', 960, 1390, 2.15, face=.2, rim=NR).pose(.2, ('down', 'down')).expression(0, mouth='flat', eyes='half', brow=-.4), 'n032')
    def n032a(t0): return dict(draw=shots.closeup('night/commerce_room', lu, focus=(960, 560), t0=t0), zoom=(1.0, 1.08), hud=LT('Howard Lutnick', 'Commerce Secretary'))
    def versus(c, t):
        Wd.text(c, 'AXIOS REPORTS', 520, 400, 58, WHITE, F_TITLE, 'center'); Wd.text(c, 'COMMERCE DENIES', 1400, 400, 58, GOLD, F_TITLE, 'center')
        c.drawLine(960, 260, 960, 560, kit.ink(8, '#9DB0DA')); Wd.text(c, 'Lutnick\'s department resisted', 520, 500, 40, '#9DB0DA', F_LABEL, 'center'); Wd.text(c, '"This is false"', 1400, 500, 40, '#9DB0DA', F_LABEL, 'center')
        Wd.stamp(c, 'Disputed', 960, 820, t - 1.0, GOLD, rot=-6, size=130)
    def n032b(t0): return dict(draw=plain(versus), zoom=(1.0, 1.05), sfx=[(1.0, 'stamp')], shake=shake(1.0))
    def quotes(c, t):
        Wd.paper_card(c, 480, 560 + 8 * math.sin(t * 2), 'Sec. Bessent', ['Frustrated by Commerce', 'delay (AP, Nov 13)'], t, w=700, h=480, rot=-4, slam=True)
        Wd.paper_card(c, 1440, 560 + 8 * math.sin(t * 2 + 1), 'President Trump', ['Lutnick "might have', 'delayed it" (Nov 16)'], t - .8, w=700, h=480, rot=4, slam=True)
    def n032c(t0): return dict(draw=plain(quotes), zoom=(1.0, 1.1), sfx=[(.2, 'stamp'), (1.0, 'stamp')], shake=shake(1.0))
    multi('n032', [(.3, n032a), (.3, n032b), (.4, n032c)])
    # n033 (a) the head lawyer, phone ringing, REPORTED; (b) split: lawyer on the phone | Commerce window
    lw = Actor('lawyer', 930, 950, 1.08, face=-.2, rim=NR).pose(.2, ('phone', 'down')).expression(0, mouth='flat', eyes='half')
    def n033a(t0): return dict(draw=shots.wide('night/office', [lw], overlay=lambda c, t: A.phone_ring(c, 1350, 820, t, .9), t0=t0), zoom=(1.2, 1.45), focus=((930, 640), (1000, 640)),
                               hud=LT('Nvidia head lawyer', 'per Bloomberg'), sfx=[(0, 'ring', 2.0), (1.2, 'stamp')], shake=shake(1.2))
    def split(c, t):
        c.save(); c.clipRect(skia.Rect(0, 0, 960, H)); c.drawImage(get_set('night/office').base, 0, 0); lw.draw(c, t, t); c.restore()
        c.save(); c.clipRect(skia.Rect(960, 0, W, H)); c.drawImage(get_set('night/commerce_hq').base, 0, 0); c.restore(); c.drawLine(960, 0, 960, H, kit.ink(10, GOLD))
    def n033b(t0): return dict(draw=shots.wide('night/office', [], overlay=lambda c, t: split(c, t)), zoom=(1.0, 1.1), sfx=[(.1, 'pickup')], hud=HUDPOP('then called Commerce', 960, 860, .3, WHITE, 70, -2))
    multi('n033', [(.5, n033a), (.5, n033b)])
    # n034 Megaspeed's statement pinned in an empty office
    add('n034', shots.wide('night/megaspeed', [], overlay=lambda c, t: (props.sign_megaspeed(c, 960, 240, .85, glow=.9), doc(c, 960, 640, 'Megaspeed statement', ['Complied with U.S. law.', 'Alice Huang left Aug 2025.'], t / 1.6, hl=1, hl_t=1.0, w=760, h=380, label_txt='ITS STATEMENT')), t0=at('n034')),
        zoom=(1.0, 1.15), focus=((900, 600), (960, 560)), sfx=[(.1, 'paper')])
    talk('n035', 'analyst', 'night/office', (700, 520), .4, 'The Analyst', 'Dramatised', dict(mouth='flat', brow=.2), ('present', 'down'), zoom=(1.0, 1.06))
    talk('n036', 'intel', 'night/office', (1300, 520), -.4, 'The Officer', 'Dramatised', dict(mouth='flat', eyes='half', brow=-.4), ('down', 'chin'), zoom=(1.05, 1.0))
    def beam(c, t):
        for i, (x, y, s_) in enumerate(((640, 860, 1.1), (900, 890, 1.2), (1220, 860, 1.1), (1500, 890, 1.0))): props.crate(c, x, y, s_, 'SERVERS', glow=.2 + .5 * K(t, .8, .4) * (i == 1))
        props.flashlight(c, 300 + 600 * ease(K(t, .2, .8)), 200, 200 - 20 * ease(K(t, .2, .8)), length=900, spread=280)
    add('n037', shots.wide('night/datacenter', [], overlay=beam), zoom=(1.0, 1.4), focus=((700, 600), (960, 700)), whip_in=True, sfx=[(.05, 'whoosh'), (0, 'amb:hum', None), (1.0, 'low_tone')])

    # ================= TWIST =================
    def n038(c, t): Wd.text_card(c, tl.by_id['n038']['text'], max(t - .3, 0), ['October.'], dur=D('n038'))
    add('n038', n038, zoom=(1.0, 1.04), sfx=[(.1, 'boom')])
    jc = Actor('jensen', 960, 1390, 2.15, face=-.2, rim=NR).pose(.2, ('down', 'down')).expression(0, mouth='flat', eyes='half', brow=.2)
    add('n039', shots.closeup('night/office', jc, focus=(1000, 540), t0=at('n039')), zoom=(1.0, 1.1), hud=LT('Jensen Huang', 'Nvidia CEO, to Bloomberg'), sfx=[(0, 'amb:hum', None)])
    def objs(c, t):
        for i, fn in enumerate((lambda: PD.memo_folder(c, 380, 560, 1.4, rot=-6), lambda: PD.af1_plane(c, 960, 560, .85), lambda: PD.memo_folder(c, 1540, 560, 1.4, rot=5, label_text='BRIEFING'))):
            k = ease_out(K(t, .15 + i * .7, .35))
            if k > 0: c.save(); c.translate(0, -(1 - k) * 500); fn(); c.restore()
    def empty(c, t):
        c.drawRect(skia.Rect(0, 0, W, H), fp('#0E1830')); r_ = 700 - 380 * ease(K(t, .2, 1.6)); p = skia.Paint(); p.setShader(skia.GradientShader.MakeRadial((960, 600), r_, [skia.Color(255, 226, 160, 120), skia.Color(0, 0, 0, 0)])); c.drawRect(skia.Rect(0, 0, W, H), p)
        rect(c, 880, 620, 1040, 700, '#3A3F4F', 6, r=10); rect(c, 900, 520, 1020, 640, '#5A3B24', 6, r=10); rect(c, 900, 700, 920, 820, '#2E2E38', 4); rect(c, 1000, 700, 1020, 820, '#2E2E38', 4)
        rect(c, 860, 840, 1060, 900, NAVY, 5, r=6); Wd.text(c, 'HUANG', 960, 884, 40, GOLD, F_LABEL, 'center')
    def n040a(t0): return dict(draw=desk(objs), zoom=(1.0, 1.08), sfx=[(.2, 'stamp'), (.9, 'stamp'), (1.6, 'stamp')], shake=shake(.2))
    def n040b(t0): return dict(draw=plain(empty, framed=False), zoom=(1.0, 1.0), hud=HUDPOP('everyone, reportedly, but him', 960, 220, .6, WHITE, 70, -2))
    multi('n040', [(.55, n040a), (.45, n040b)])

    # ================= CH4 "I Haven't Heard That" =================
    chapter(4, "I Haven't Heard That")
    def stack3(c, t):
        for i, (x, y, r_) in enumerate(((440, 600, -6), (960, 520, 3), (1480, 620, 8))):
            k = ease_out(K(t, .1 + i * .35, .6)); c.save(); c.translate(x, y); c.scale(.5, .5); c.translate(-x, -y); A.newspaper(c, x, y, t - .1 - i * .35, ['The New York Times', 'The Washington Post', 'Reuters'][i], ['HUANG RESIGNS', 'WHO KNEW?', 'SEC PROBE'][i], None, dur=.6); c.restore()
    add('n041', plain(stack3), zoom=(1.0, 1.08), sfx=[(.1, 'whoosh'), (.45, 'whoosh'), (.8, 'whoosh')])
    # n042 (a) Nov 8 calendar page; (b) the board statement, highlighted line
    def n042a(t0): return dict(draw=desk(lambda c, t: cal_page(c, 960, 540, t, 'NOVEMBER', '8', s=1.8)), zoom=(1.0, 1.1), sfx=[(.1, 'page')], hud=lambda c, t: Wd.place_tag(c, 'Nvidia', (t - .3) / .4, 'Nov 8'))
    def n042b(t0): return dict(draw=desk(lambda c, t: doc(c, 960, 540, 'Board statement', ['Independent investigation opened.', 'No reason to believe national', 'security was compromised.'], t / 1.8, hl=1, hl_t=1.1, w=980, h=600, label_txt='NVIDIA BOARD')),
                               zoom=(1.0, 1.3), focus=((960, 540), (900, 620)), sfx=[(.1, 'paper'), (1.1, 'pop')])
    multi('n042', [(.4, n042a), (.6, n042b)])
    # n043 (a) Nov 9 split: phone | Foreign Ministry plate; (b) the President by phone
    def split9(c, t):
        Wd.framed_bg(c); k = ease_out(K(t, .2, .4)); c.save(); c.translate(-(1 - k) * 700, 0)
        rect(c, 330, 260, 590, 780, '#1B1D26', 8, r=40); rect(c, 350, 300, 570, 740, NAVY, 3, r=20); Wd.text(c, 'CALL', 460, 560, 56, GOLD, F_LABEL, 'center'); c.restore()
        c.save(); c.translate((1 - k) * 700, 0); rect(c, 820, 360, 1620, 600, NAVY, 7, r=14); Wd.text(c, 'FOREIGN MINISTRY', 1220, 470, 62, WHITE, F_LABEL, 'center'); Wd.text(c, '"groundless"', 1220, 560, 50, GOLD, F_LABEL, 'center'); c.restore()
    def n043a(t0): return dict(draw=plain(split9), zoom=(1.0, 1.08), sfx=[(.2, 'whoosh'), (.6, 'stamp')], shake=shake(.6), hud=lambda c, t: Wd.place_tag(c, 'Beijing', (t - .3) / .4, 'Nov 9'))
    def n043b(t0): return dict(draw=shots.wide('night/oval_office', [trump(960, 900, .98, -.1)], overlay=lambda c, t: A.phone_ring(c, 1300, 800, t, .9), t0=t0), zoom=(1.3, 1.15), focus=((960, 760), (1100, 760)),
                               hud=both(LT('Donald Trump', 'President', .4), HUDPOP('the President says', 1500, 300, .5, GOLD, 72, -3)), sfx=[(0, 'ring', 1.6)])
    multi('n043', [(.5, n043a), (.5, n043b)])
    # n044 (a) Nov 12: Jensen walks out of the Nvidia lobby; (b) the letter lands, RECEIVED
    jw = Actor('jensen', 640, 700, .55, face=.3, rim=NR).pose(0, ('down', 'down')).walk_to(.2, 2.4, 1050, 900)
    def n044a(t0): return dict(draw=shots.wide('night/nvidia_hq', [jw], t0=t0), zoom=(1.0, 1.25), focus=((700, 700), (1000, 760)), sfx=[(0, 'steps', 2.0)],
                               hud=lambda c, t: (Wd.place_tag(c, 'Nvidia HQ', (t - .3) / .4, 'Nov 12'), cal_page(c, 1700, 330, t, 'NOV', '12', s=.5)))
    def letter(c, t):
        k = ease_out(K(t, .1, .6)); c.save(); c.translate(960, 540 - (1 - k) * 700); c.rotate(-3)
        rect(c, -420, -300, 420, 300, PAPER, 5, r=4); Wd.text(c, 'TO: SEC. LUTNICK', -380, -220, 44, NAVY, F_LABEL); Wd.text(c, 'FROM: SENS. NEAL & WYDEN', -380, -150, 40, NAVY, F_TYPE)
        for i in range(4): c.drawLine(-380, -70 + i * 50, 380, -70 + i * 50, kit.ink(3, '#B8B0A0'))
        c.restore(); PD.prop_stamp(c, 'Received', 960, 760, t - 1.0, size=100)
    def n044b(t0): return dict(draw=desk(letter), zoom=(1.0, 1.15), focus=((960, 540), (960, 520)), sfx=[(.15, 'paper'), (1.0, 'stamp')], shake=shake(1.0))
    multi('n044', [(.5, n044a), (.5, n044b)])
    # n045 (a) the empty witness chair with a HUANG nameplate; (b) 1 December, ringed in gold
    def n045a(t0): return dict(draw=plain(lambda c, t: empty(c, t)), zoom=(1.0, 1.12), focus=((960, 700), (960, 640)), sfx=[(.4, 'low_tone')], hud=HUDPOP('Congress wants answers', 960, 220, .3, WHITE, 70, -2))
    def n045b(t0): return dict(draw=desk(lambda c, t: cal_page(c, 960, 560, t, 'DECEMBER', '1', s=1.6, ring_at=.5)), zoom=(1.0, 1.08), sfx=[(.5, 'stamp')], shake=shake(.5), hud=lambda c, t: Wd.text(c, 'CLOSED-DOOR INTERVIEW', 960, 120, 62, GOLD, F_LABEL, 'center', stroke=10))
    multi('n045', [(.45, n045a), (.55, n045b)])
    # n046 the same podium as the hook, lit differently, push in on the President
    tr46 = trump(960, 980, .95, -.35).pose(.3, ('down', 'down')); rp46 = Actor('reporter2', 560, 960, .9, face=.35, rim=NR).expression(0, mouth='mid', eyes='dot').pose(.3, ('hold', 'down'))
    add('n046', shots.wide('night/white_house', [rp46, tr46], overlay=flashes([.4, .9, 1.6, 2.2, 3.0]), t0=at('n046')), zoom=(1.0, 1.6), focus=((960, 640), (960, 620)), sfx=[(.4, 'shutter'), (.9, 'shutter'), (1.6, 'shutter'), (2.2, 'shutter')],
        hud=lambda c, t: Wd.place_tag(c, 'Washington', (t - .2) / .4, 'Monday, Nov 16'))
    mic = lambda c, t: held_mic(c, kit.hand_pos(960, 1390, 2.15, ('hold', 'down'), -1), 1.3, 35)
    talk('n047', 'reporter2', 'night/white_house', (960, 640), .3, 'The Reporter', 'Dramatised', dict(mouth='mid', eyes='wide', brow=.5), ('hold', 'down'), overlay=mic, zoom=(1.0, 1.06))
    talk('n048', 'banker', 'night/white_house', (1100, 640), -.4, 'The Official', 'Dramatised', dict(mouth='flat', eyes='half'), ('down', 'chin'), zoom=(1.0, 1.06))
    talk('n049', 'reporter2', 'night/white_house', (960, 640), .3, None, None, dict(mouth='flat', eyes='half', brow=-.4), ('hold', 'down'), overlay=mic, zoom=(1.05, 1.0))
    talk('n050', 'banker', 'night/white_house', (1100, 640), -.5, None, None, dict(mouth='flat', eyes='half'), ('down', 'chin'), zoom=(1.0, 1.1), sfx=[(D('n050') * .6, 'low_tone')])
    # n051 (a) SEC probe, reported; (b) "honored to return"
    def n051a(t0): return dict(draw=desk(lambda c, t: (doc(c, 960, 540, 'Wall Street Journal', ['Reported: the SEC opened a probe', 'into Nvidia. Scope unclear.'], t / 1.4, hl=0, hl_t=.8, w=980, h=500, label_txt='ATTRIBUTED: WSJ'), PD.prop_stamp(c, 'Reported', 1360, 300, t - 1.3, size=84))),
                               zoom=(1.0, 1.1), sfx=[(.1, 'paper'), (1.3, 'stamp')], shake=shake(1.3), hud=lambda c, t: Wd.place_tag(c, 'Nov 17', (t - .3) / .4))
    def n051b(t0): return dict(draw=plain(lambda c, t: Wd.text(c, 'HUANG: "WOULD BE HONORED" TO RETURN', 960, 560, 70, WHITE, F_TITLE, 'center', stroke=10)), zoom=(1.0, 1.06), hud=HUDPOP('his words, Nov 17', 960, 860, .4, GOLD, 70, -2), sfx=[(.2, 'pop')])
    multi('n051', [(.55, n051a), (.45, n051b)])

    # ================= CH5 "Why It's a Big Deal for Your 401(k)" (night study, analyst; no board) =================
    chapter(5, "Why It's a Big Deal for Your 401(k)")
    def an_(x=700, face=.35, pose=('down', 'point'), **e): return Actor('analyst', x, 1010, 1.0, face=face, rim=NR).pose(.2, pose).expression(0, **e)
    # n052 "This is how it affects you."  analyst + the 401(k) screen, coins drop in
    def n052o(c, t):
        PD.fund_screen(c, 1330, 565, 1.0, t - .5, title='YOUR 401(k)', share=6.0)
    add('n052', shots.wide('night/study', [an_()], overlay=n052o, t0=at('n052')), zoom=(1.0, 1.12), focus=((1000, 560), (1150, 560)), whip_in=True, sfx=[(0, 'whoosh'), (1.0, 'tick')])
    # n053 (a) the H200 rule + chip, 25% cut counter; (b) briefings folder and rule folder, NOT CONNECTED
    def rule_chip(c, t):
        k = ease_out(K(t, .1, .5)); PD.memo_folder(c, 1000, 770 - (1 - k) * 300, .75, rot=-5, label_text='H200 RULE'); PD.chip_box(c, 1450, 716, 1.0, rot=3)
        Wd.counter(c, 1450, 400, 0, 25, (t - .8) / 1.0, unit='', suffix='%', label='cut announced, Dec 2025', size=90, panel=True)
    def not_conn(c, t):
        PD.memo_folder(c, 900, 770, .75, rot=-4, label_text='BRIEFINGS'); PD.memo_folder(c, 1500, 770, .75, rot=4, label_text='H200 RULE')
        for i in range(int(12 * K(t, .2, .8))): c.drawCircle(1040 + i * 30, 700, 6, fp('#C9B995'))
        Wd.stamp(c, 'Not connected', 1300, 500, t - 1.2, GOLD, rot=-6, size=64)
    def n053a(t0): return dict(draw=shots.wide('night/study', [an_(face=.35)], overlay=rule_chip, t0=t0), zoom=(1.0, 1.15), focus=((1000, 560), (1250, 560)), sfx=[(.1, 'paper'), (1.0, 'tick')])
    def n053b(t0): return dict(draw=shots.wide('night/study', [an_(pose=('down', 'present'))], overlay=not_conn, t0=t0), zoom=(1.1, 1.0), focus=(1150, 600), sfx=[(1.2, 'stamp')], shake=shake(1.2))
    multi('n053', [(.55, n053a), (.45, n053b)])
    # n054 "more than six hundred dollars of every ten thousand"  big screen, ten stacks of cash, six percent glows
    def waffle(c, t):
        PD.fund_screen(c, 1230, 610, 1.2, t, title='YOUR 401(k)', share=6.0); Wd.cash_stack(c, 560, 836, 10, 1.0)
        Wd.counter(c, 1230, 175, 0, 6.0, (t - .2) / 1.0, unit='', suffix='%', label='NVIDIA', size=80, panel=False)
    add('n054', shots.wide('night/study', [an_(x=420, face=.4)], overlay=waffle, t0=at('n054')), zoom=(1.0, 1.1), focus=((900, 600), (1200, 560)), sfx=[(.2, 'tick'), (1.2, 'ding')],
        hud=lambda c, t: Wd.text(c, 'ABOUT $600 OF EVERY $10,000', 960, 925, 40, '#9DB0DA', F_LABEL, 'center', alpha=int(255 * K(t, 1.0, .4))))
    # n055 the habit  a rule folder slides over the screen, typed line on top
    def rule_on_screen(c, t):
        PD.fund_screen(c, 1330, 565, 1.0, 9, title='YOUR 401(k)', share=6.0); k = ease_out(K(t, .3, .6))
        PD.memo_folder(c, 760 + k * 520, 800 - k * 180, .7, rot=-6 + 6 * k, label_text='THE RULE')
    add('n055', shots.wide('night/study', [an_(x=560, pose=('down', 'present'))], overlay=rule_on_screen, t0=at('n055')), zoom=(1.0, 1.12), focus=((1000, 560), (1150, 560)), sfx=[(.3, 'paper'), (.9, 'tick')],
        hud=lambda c, t: Wd.text(c, ('THE RULE IS PART OF WHAT YOU OWN')[:max(0, int((t - .4) / 2.4 * 40))], 960, 150, 52, WHITE, F_TYPE, 'center', stroke=10))
    # n056 three questions: three index cards pop onto the desk one by one
    CARDS = [('What can switch its', 'market on or off?'), ('Who checks its', 'biggest customers?'), ('Who gets warned,', 'and when?')]
    def three_cards(c, t):
        for i, (l1, l2) in enumerate(CARDS): PD.question_card(c, 760 + i * 410, 640, .78, rot=(-3, 2, -2)[i], n=i + 1, line1=l1, line2=l2, u=K(t, .6 + i * 1.7, .45))
    add('n056', shots.wide('night/study', [an_(x=300, face=.45, pose=('down', 'count'), mouth='flat')], overlay=three_cards, t0=at('n056')), zoom=(1.0, 1.08), focus=((1000, 600), (1100, 600)), sfx=[(.6, 'pop'), (2.3, 'pop'), (4.0, 'pop')])
    # n057 you at home with your fund statement
    sv = Actor('saver', 960, 1390, 2.15, face=.4, rim=NR).pose(.2, ('hold', 'chin')).expression(0, mouth='flat', eyes='half')
    add('n057', shots.closeup('night/study', sv, focus=(700, 560), overlay=lambda c, t: props.paper_in_hand(c, *kit.hand_pos(960, 1390, 2.15, ('hold', 'chin'), -1), .9, title='FUND STATEMENT', lines=('S&P 500 index fund',)), t0=at('n057')), zoom=(1.0, 1.08))

    # ================= END =================
    tr59 = trump(960, 980, .95, -.35).pose(.3, ('down', 'down')); rp59 = Actor('reporter2', 560, 960, .9, face=.35, rim=NR).expression(0, mouth='mid', eyes='dot').pose(.3, ('hold', 'down'))
    def n059(c, t): pass
    add('n059', shots.wide('night/white_house', [rp59, tr59], overlay=flashes([.3, .8]), t0=at('n059')),
        zoom=(1.7, 1.0), focus=((960, 640), (960, 540)), sfx=[(.3, 'shutter'), (.8, 'shutter'), (1.4, 'pop')],
        hud=lambda c, t: (Wd.pop_label(c, '"I haven\'t heard that."', 960, 150, (t - 1.4) / .5, WHITE, 80, rot=-2), Wd.text(c, 'PRESIDENT TRUMP, NOV 16', 960, 230, 30, '#9DB0DA', F_LABEL, 'center', alpha=int(255 * K(t, 1.6, .4)))))
    def end3(c, t):
        for i, fn in enumerate((lambda: PD.memo_folder(c, 480, 560, 1.4, rot=-6), lambda: empty_chair(c), lambda: (rect(c, 1280, 400, 1600, 720, PAPER, 5, r=4), Wd.text(c, 'SEC', 1440, 600, 90, NAVY, F_TITLE, 'center'), Wd.text(c, 'PROBE', 1440, 670, 40, '#6B7390', F_LABEL, 'center')))):
            k = ease_out(K(t, .15 + i * .8, .3))
            if k > 0: c.save(); c.translate(0, -(1 - k) * 500); fn(); c.restore()
    def empty_chair(c):
        rect(c, 880, 560, 1040, 640, '#3A3F4F', 6, r=10); rect(c, 900, 460, 1020, 580, '#5A3B24', 6, r=10); rect(c, 900, 640, 920, 760, '#2E2E38', 4); rect(c, 1000, 640, 1020, 760, '#2E2E38', 4)
    add('n060', desk(end3), zoom=(1.0, 1.08), sfx=[(.2, 'stamp'), (1.0, 'stamp'), (1.8, 'stamp')])
    add('n061', desk(lambda c, t: cal_page(c, 960, 540, t, 'MAY', '12', s=1.9, ring_at=.6)), zoom=(1.0, 1.08), sfx=[(.6, 'stamp')], shake=shake(.6))
    def n062(c, t): Wd.text_card(c, tl.by_id['n062']['text'], max(t - .3, 0), ['four'], dur=D('n062'))
    add('n062', n062, zoom=(1.0, 1.03), sfx=[(.3, 'type_key'), (D('n062') * .85, 'low_tone')])
    def teaser(c, t):
        k = kit.back(K(t, .1, .4)); c.save(); c.translate(960, 420); c.scale(k, k)
        Wd.text(c, 'THE NVIDIA FILES', 0, -60, 56, '#9DB0DA', F_LABEL, 'center'); Wd.text(c, 'PART 3', 0, 70, 140, GOLD, F_TITLE, 'center', stroke=14); c.restore()
        if t > .7: Wd.text(c, 'THE FOUR DAYS', 960, 680, 80, WHITE, F_TITLE, 'center', alpha=int(255 * K(t, .7, .4)))
    add('n063', plain(teaser), zoom=(1.0, 1.08), sfx=[(.1, 'boom')])
    S.append(dict(name='outro', dur=tl.dur('outro', 'endscreen'), draw=lambda c, t: A.outro(c, t), zoom=(1, 1.02)))
    return S
