"""Shot list - 50% in 45 Days (Ponzi test). One picture per sentence. Night print for the story, day print for the lesson."""
import math, skia
from engine import shots, widgets as Wd, kit
from engine.actor import Actor
from engine.core import W, H, GOLD, ORANGE, WHITE, NAVY, NAVY3, PAPER, F_LABEL, F_TYPE, F_TITLE
from engine.sets import get_set

SHOT_BREAKS = ('n001', 'n003', 'n004', 'n005', 'n006', 'n007', 'n008', 'n009', 'n010', 'n011', 'n013', 'n014', 'n015', 'n017', 'n018', 'n019', 'n020')
NIGHT_RIM, DAY_RIM = '#9FB8F0', '#FFE3A6'
QUEUE = ['worker', 'saver', 'retiree', 'grad', 'reporter', 'agent', 'banker', 'analyst']

def coupon(c, x, y, rot=0, s=1.0, a=255):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    kit.rect(c, -110, -70, 110, 70, PAPER, 4); kit.rect(c, -98, -58, 98, 58, None, 2.5, v=NAVY)
    Wd.text(c, 'REPLY COUPON', 0, -22, 26, NAVY, F_LABEL, 'center'); Wd.text(c, 'POSTAGE', 0, 14, 22, NAVY, F_TYPE, 'center')
    kit.circ(c, 0, 40, 10, GOLD, 2); c.restore()

def queue(t, phones=False, n=8):
    """A line of people along the night street, shuffling slightly (s 0.52, feet y 880)."""
    acts = []
    for i in range(n):
        a = Actor(QUEUE[i % len(QUEUE)], 160 + i * 105, 880 + (i % 2) * 6, .5, face=.6, light=-1, rim=NIGHT_RIM, hat=(QUEUE[i % len(QUEUE)] == 'worker'))
        a.pose(0, ('down', 'hold') if phones else (('pocket', 'down') if i % 3 else ('down', 'chin')))
        acts.append(a)
    return acts

def phone_glow(c, acts, t):
    for a in acts:
        hx, hy = kit.hand_pos(a.x, a.y, a.s, ('down', 'hold'), 1)
        c.drawCircle(hx, hy - 8, 26, kit.fp(GOLD, 60, blur=10)); kit.rect(c, hx - 9, hy - 22, hx + 9, hy + 6, '#1B2A52', 2.5, r=3); c.drawRect(skia.Rect(hx - 6, hy - 19, hx + 6, hy + 2), kit.fp('#FFE2A0'))

def build(tl):
    S = []; at = tl.at
    def add(a, b, draw, **kw): S.append(dict(dur=tl.dur(a, b), draw=draw, **kw))
    def rel(lid, a): return tl.start(lid) - at(a)
    mouths = tl.mouths()

    # ---------------- HOOK
    q = queue(0)
    add('n001', 'n003', shots.wide('night/street1920', q, overlay=lambda c, t: Wd.place_tag(c, 'Boston', t / .4, '1920'), t0=at('n001')),
        zoom=(1.0, 1.1), focus=(700, 640), sfx=[(.1, 'whoosh')])
    add('n003', 'n004', shots.card('text', tl.cues['n003'][1], text=tl.by_id['n003']['text'], gold_words=['fifty', 'percent']), zoom=(1, 1.02))
    ponzi = Actor('ponzi', 930, 950, 1.08, face=-.15, rim=NIGHT_RIM, hat=True).pose(.3, ('present', 'hip')).expression(.2, mouth='smirk', eyes='half', sparkle=0)
    add('n004', 'title', shots.wide('night/office', [ponzi], overlay=lambda c, t: Wd.lower_third(c, 'Charles Ponzi', 'Boston, 1920', (t - .4) / .5), t0=at('n004')),
        zoom=(1.0, 1.08), focus=(930, 560))
    add('title', 'chapter:1', shots.card('title', 2.5, title='50% in 45 Days', gold_word='50%'), zoom=(1, 1.03))
    add('chapter:1', 'n005', shots.card('chapter', 2.2, n=1, title='The Loophole'), zoom=(1, 1.02))

    # ---------------- CH1
    p2 = Actor('ponzi', 930, 950, 1.08, face=0, rim=NIGHT_RIM, hat=True).pose(.2, ('down', 'gesture')).expression(0, mouth='smile')
    add('n005', 'n006', shots.wide('night/office', [p2], t0=at('n005')), zoom=(1.04, 1.1), focus=(930, 600))
    def coupons(c, t):
        Wd.text(c, 'EUROPE', 420, 200, 64, WHITE, F_TITLE, 'center'); Wd.text(c, 'AMERICA', 1500, 200, 64, GOLD, F_TITLE, 'center')
        for i in range(3): coupon(c, 420 + (i - 1) * 40, 520 + i * 18, -6 + i * 4, 1.2)
        k = kit.ease(kit.K(t, 1.2, 1.4)); [coupon(c, kit.lerp(420, 1500, k) + (i - 1) * 40, 520 + i * 18, 6 - i * 4, 1.2) for i in range(3) if k > 0]
        kit.poly(c, [(860, 500), (1060, 500), (1060, 470), (1120, 530), (1060, 590), (1060, 560), (860, 560)], GOLD, 5)
        Wd.pop_label(c, 'cheap', 420, 760, (t - .5) / .4, WHITE, 60); Wd.pop_label(c, 'worth more?', 1500, 760, (t - 2.6) / .4, GOLD, 60)
    add('n006', 'n007', shots.plain(coupons), zoom=(1.0, 1.05), sfx=[(.3, 'paper'), (1.3, 'whoosh')])
    inv = Actor('worker', 960, 1390, 2.15, face=.6, light=-1, rim=NIGHT_RIM, hat=True).expression(0, eyes='wide', brow=.7, brow_tilt=-.5, mouth='flat').say(tl, 'n007', mouths)
    add('n007', 'n008', shots.closeup('night/office', inv, focus=(1300, 600), t0=at('n007')), zoom=(1.0, 1.04), focus=(960, 560))
    p3 = Actor('ponzi', 960, 1390, 2.15, face=-.6, light=-1, rim=NIGHT_RIM, hat=True).expression(0, eyes='half', mouth='smirk').pose(.2, ('down', 'count')).say(tl, 'n008', mouths)
    add('n008', 'n009', shots.closeup('night/office', p3, focus=(800, 560), t0=at('n008')), zoom=(1.0, 1.04), focus=(960, 560))
    p4 = Actor('ponzi', 930, 950, 1.08, face=-.1, rim=NIGHT_RIM, hat=True).pose(.1, ('cheer', 'hip')).expression(0, mouth='open', eyes='closed')
    add('n009', 'n010', shots.wide('night/office', [p4], overlay=lambda c, t: (Wd.falling_money(c, t, n=14, area=(300, 0, 1600, 900)), Wd.counter(c, 960, 190, 0, 15000000, (t - .2) / 1.5, label='poured in')), t0=at('n009')),
        zoom=(1.0, 1.06), focus=(930, 540))
    p5 = Actor('ponzi', 930, 950, 1.08, face=.3, rim=NIGHT_RIM, hat=True).pose(.6, ('shrug', 'shrug')).expression(.6, mouth='grit', eyes='wide', sweat=0)
    add('n010', 'n011', shots.wide('night/office', [p5], overlay=lambda c, t: (coupon(c, 1180, 600 + 300 * kit.ease_out(kit.K(t, 1.6, .6)), 20 * kit.K(t, 1.6, .6), .7) if t < 2.4 else None, Wd.pop_label(c, 'almost no coupons', 960, 220, (t - 1.8) / .4, WHITE, 70)), t0=at('n010')),
        zoom=(1.0, 1.1), focus=(930, 520))

    # ---------------- TWIST
    add('n011', 'n013', shots.card('text', tl.cues['n011'][1], text=tl.by_id['n011']['text'], gold_words=['27,000']), zoom=(1, 1.03))

    # ---------------- THE FALL (paper on navy)
    def paper(c, t):
        Wd.document(c, 960, 560, 'The Boston Post', ['Questions about', "Mr. Ponzi's coupons", '', 'Investigation', 'continues...'], t / 2.0, w=700, h=760, rot=-2)
    add('n013', 'n014', shots.plain(paper), zoom=(1.0, 1.06), rot=(0, 1.5), sfx=[(.1, 'paper')])
    hit = rel('n014', 'n014') + 0.5
    def fall(c, t):
        Wd.document(c, 960, 560, 'The Boston Post', ['Questions about', "Mr. Ponzi's coupons", '', 'Investigation', 'continues...'], 1.0, w=700, h=760, rot=-2)
        Wd.stamp(c, 'FRAUD', 1000, 520, t - hit, ORANGE, rot=-10, size=120)
        Wd.pop_label(c, 'pleaded guilty - mail fraud', 960, 960, (t - hit - .5) / .4, WHITE, 56)
        Wd.stamp(c, 'Pulitzer prize', 1450, 260, t - hit - 1.8, GOLD, rot=8, size=60)
    add('n014', 'chapter:5', shots.plain(fall), zoom=(1.0, 1.05), shake=lambda t: Wd.stamp(skia.Surface(4, 4).getCanvas(), 'x', 0, 0, t - hit),
        sfx=[(hit, 'stamp'), (hit + 1.8, 'stamp')])

    # ---------------- CH5 YOUR WALLET (day)
    add('chapter:5', 'n015', shots.card('chapter', 2.2, n=5, title='Your Wallet'), zoom=(1, 1.02))
    sv = Actor('saver', 760, 985, .98, face=.3, light=1, rim=DAY_RIM).pose(.3, ('phone', 'down')).expression(0, eyes='wide', mouth='o', brow=.5)
    add('n015', 'n017', shots.wide('day/living', [], [sv], t0=at('n015')), zoom=(1.0, 1.08), focus=(800, 600), whip_in=True)
    an = Actor('analyst', 420, 990, 1.0, face=.3, light=1, rim=DAY_RIM).pose(.2, ('down', 'point'))
    flags = ['Guaranteed high returns', 'Returns that never dip', 'Seller not registered']
    def board(c, t):
        kit.rect(c, 600, 110, 1500, 640, '#F8FAFD', 8, r=10); Wd.text(c, 'RED FLAGS', 1050, 200, 72, NAVY, F_TITLE, 'center')
        starts = [rel('n017', 'n017') + x for x in (1.0, 2.9, 4.6)]
        for i, (f, s0) in enumerate(zip(flags, starts)):
            u = kit.K(t, s0, .35)
            if u > 0:
                y = 300 + i * 105; kit.poly(c, [(660, y - 40), (660, y + 10), (700, y - 15)], ORANGE, 4); c.drawLine(660, y - 40, 660, y + 30, kit.ink(6))
                Wd.pop_label(c, f, 1080, y, u, NAVY, 60, rot=0, stroke=0)
    add('n017', 'n018', shots.wide('day/lesson', [], [an], overlay=board, t0=at('n017')), zoom=(1.0, 1.05), focus=(960, 520), sfx=[(1.0, 'pop'), (2.9, 'pop'), (4.6, 'pop')])
    an2 = Actor('analyst', 420, 990, 1.0, face=.3, light=1, rim=DAY_RIM).pose(.1, ('down', 'present')).expression(0, mouth='smile')
    def board2(c, t):
        kit.rect(c, 600, 110, 1500, 640, '#F8FAFD', 8, r=10); Wd.text(c, 'BEFORE YOU INVEST', 1050, 220, 64, NAVY, F_TITLE, 'center')
        Wd.sticky(c, 'Check them at investor.gov', 1050, 420, t / .4, rot=-4, w=380)
    add('n018', 'n019', shots.wide('day/lesson', [], [an2], overlay=board2, t0=at('n018')), zoom=(1.0, 1.06), focus=(1000, 480), sfx=[(.1, 'pop')])

    # ---------------- ENDING (callback: the same line, now on phones)
    q2 = queue(0, phones=True)
    add('n019', 'n020', shots.wide('night/street', q2, overlay=lambda c, t: phone_glow(c, q2, t), t0=at('n019')), zoom=(1.1, 1.0), focus=(700, 640), whip_in=True)
    add('n020', 'end', shots.card('text', tl.cues['n020'][1], text=tl.by_id['n020']['text'], gold_words=['line?']), zoom=(1, 1.02))
    return S
