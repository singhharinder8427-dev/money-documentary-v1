"""HINDI TEST (26 Nov 2026): the Ponzi hook (n001-n006 + title) from videos/ponzi-full, in Hindi. Same pictures and SFX.
Night print for the story, day print for the lesson (Ch5). Applies FIXES.md: start close, vary angles, framed stage,
documents fill the frame, story animations every 20-30 s, red-flags board, big phones at the end, outro + end screen."""
import math, skia
from engine import shots, widgets as Wd, anim as A, kit
from engine.actor import Actor
from engine.cast import person
from engine.core import W, H, GOLD, ORANGE, WHITE, NAVY, NAVY3, PAPER, F_LABEL, F_TYPE, F_TITLE
from engine.sets import get_set

SHOT_BREAKS = tuple(f'n{i:03d}' for i in range(1, 7))
NR, DR = '#9FB8F0', '#FFE3A6'                                   # night rim, day rim
MCMASTERS = person('analyst', suit='#2E2E38', suit_d='#1E1E26', tie='#14213D', hair='slick', hair_col='#3A2A20', glasses=False, skin='#F0CDA4', skin_d='#D2AC80')
EDITOR = person('banker', bowtie=False, tie='#14213D', suit='#3A3F4A', suit_d='#2A2E36', hanky=None, glasses=True)
GUARD = person('agent', suit='#2B3A55', suit_d='#1E2A40', hat_col='#1E2A40', hat_band='#0E1424')

queue, held, stamp_shake = A.queue, A.held, A.stamp_shake        # now in the shared library (engine/anim.py)

def build(tl):
    S = []; at = tl.at; mouths = tl.mouths()
    order = [l['id'] for l in tl.lines]
    def mk(ev): return f"chapter:{ev['n']}" if ev['kind'] == 'chapter' else ev['kind']
    def nxt(lid):
        """Next shot boundary after a line: next line, or an inserted card / outro."""
        i = order.index(lid); cands = [e for e in tl.events if e['t0'] > tl.start(lid) + .01]
        nl = order[i + 1] if i + 1 < len(order) else None
        ev = min(cands, key=lambda e: e['t0']) if cands else None
        if ev and (nl is None or ev['t0'] < at(nl)): return mk(ev)
        return nl
    def add(lid, draw, **kw): S.append(dict(name=lid, dur=tl.dur(lid, nxt(lid)), draw=draw, **kw))
    def card_shot(marker, draw, **kw): S.append(dict(name=marker.replace(':', ''), dur=tl.dur(marker, nxt_ev(marker)), draw=draw, zoom=kw.pop('zoom', (1, 1.02)), **kw))
    def nxt_ev(marker):
        t0 = at(marker); later = [l for l in order if at(l) > t0 + .01]; ev = [e for e in tl.events if e['t0'] > t0 + .01]
        c1 = at(later[0]) if later else 1e9; c2 = min((e['t0'] for e in ev), default=1e9)
        if c2 < c1: return mk(min(ev, key=lambda e: e['t0']))
        return later[0] if later else 'end'
    def say(a, lid): return a.say(tl, lid, mouths)
    T = lambda lid: tl.cues[lid][1]

    # ================= HOOK =================
    q = queue()
    add('n001', shots.wide('night/street1920', q, t0=at('n001')), hud=lambda c, t: Wd.place_tag(c, 'Boston', t / .4, 'July 1920'),
        zoom=(1.7, 1.55), focus=((380, 700), (930, 640)), sfx=[(.1, 'whoosh')])                     # start close, travel to his door
    q2 = queue()
    add('n002', shots.wide('night/street1920', q2, overlay=lambda c, t: held(c, q2, 'cash', t), t0=at('n002')), zoom=(2.3, 2.4), focus=((560, 720), (720, 720)))
    add('n003', shots.card('text', T('n003'), text=tl.by_id['n003']['text'], gold_words=['50%', 'munafa.']), zoom=(1, 1.02))
    p4 = Actor('ponzi', 930, 950, 1.08, face=-.2, rim=NR, hat=True).pose(.2, ('pocket', 'hip')).expression(0, mouth='smirk', eyes='half')
    add('n004', shots.wide('night/office', [p4], t0=at('n004')), hud=lambda c, t: Wd.lower_third(c, 'Charles Ponzi', 'Boston, 1920', (t - .3) / .5),
        zoom=(1.15, 1.3), focus=(930, 600))
    p5 = Actor('ponzi', 960, 1390, 2.15, face=-.3, rim=NR, hat=True).expression(0, mouth='smile', eyes='dot').expression(1.2, mouth='smirk', eyes='half')
    add('n005', shots.closeup('night/office', p5, focus=(930, 520), overlay=lambda c, t: Wd.pop_label(c, 'the Ponzi scheme', 960, 190, (t - 1.4) / .4, GOLD, 96, rot=-3), t0=at('n005')),
        zoom=(1.0, 1.05), sfx=[(1.4, 'pop')])
    p6 = Actor('ponzi', 960, 1390, 2.15, face=.2, rim=NR, hat=True).pose(.3, ('down', 'hat')).expression(.3, mouth='smirk', eyes='closed', sparkle=1.0)
    add('n006', shots.closeup('night/office', p6, focus=(1100, 520), t0=at('n006')), zoom=(1.0, 1.06))
    card_shot('title', shots.card('title', 2.5, title='50% in 45 Days', gold_word='50%'))
    return S
