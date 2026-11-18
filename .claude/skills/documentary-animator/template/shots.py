"""Per-video shot list (copy into videos/<slug>/shots.py and write one entry per sentence).
build(tl) returns a list of shots, in order. Each shot:
  dur      seconds (use the timeline: tl.end(last_line) - tl.start(first_line) + gaps)
  draw     a function from engine.shots (wide / closeup / card / desk / plain) - or your own draw(c, t)
  zoom     (start, end) push-in, default (1.0, 1.07); focus (x, y); rot (deg start, end) for desk shots
  whip_in / whip_out  transitions; shake = function(t) -> (dx, dy) (e.g. from a stamp)
  sfx      [(t_in_shot, name)], names from engine.audio.SFX: stamp, coin, cash, pop, paper, whoosh, falling, shutter, ding, low_tone
Night sets for the story parts, day sets for the lesson part (Ch5). Always the locked cast / fonts / colours."""
from engine import shots, widgets as Wd
from engine.actor import Actor
from engine.core import GOLD, ORANGE

SHOT_BREAKS = ('n003',)                 # line ids that start a new shot (timeline adds a 0.3 s lead before them)
# Shot boundaries are markers: a line id, 'title', 'chapter:N', 'end'. Use tl.dur(this_marker, next_marker) so the
# shots tile the whole timeline exactly. The first shot starts at 0 (use the first line id with tl.at -> fine).

def build(tl):
    S = []
    def d(a, b): return tl.dur(a, b) + (tl.at(a) if not S else 0.0)   # first shot also covers the 0.3 s lead-in
    # hook: start in the middle of the action - CEO behind the desk, a counter climbing
    ceo = Actor('ceo', 930, 950, 1.08, face=-.2).pose(.6, ('present', 'hip')).expression(1.2, mouth='smirk', eyes='half')
    S.append(dict(dur=d('n001', 'n003'), draw=shots.wide('night/office', [ceo], overlay=lambda c, t: Wd.counter(c, 960, 190, 0, 4800000000, t / 1.6, label='missing'), t0=tl.start('n001')),
                  zoom=(1.0, 1.08), focus=(930, 560), sfx=[(.2, 'whoosh')]))
    # text card line (script line marked "card": true)
    S.append(dict(dur=d('n003', 'title'), draw=shots.card('text', tl.cues['n003'][1], text=tl.by_id['n003']['text'], gold_words=['did.']), zoom=(1, 1)))
    # title card (sound logo plays automatically)
    S.append(dict(dur=d('title', 'end'), draw=shots.card('title', 2.5, title='The $4.8 Billion Lie', gold_word='$4.8', sub='a true money story'), zoom=(1, 1.03)))
    return S
