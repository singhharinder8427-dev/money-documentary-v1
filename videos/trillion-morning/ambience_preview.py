"""Owner preview (24 Nov 2026): living backgrounds on two existing sets. Run from this folder:
   python ambience_preview.py   ->  out/ambience_preview.mp4  (silent, ~14 s)"""
import sys, pathlib
SKILL = pathlib.Path(__file__).resolve().parents[2] / '.claude' / 'skills' / 'documentary-animator'; sys.path.insert(0, str(SKILL))
from engine import shots, render, ambience
from engine.actor import Actor
ambience.enable()
OUT = pathlib.Path(__file__).parent / 'out'; OUT.mkdir(exist_ok=True)

OFFICE = [   # night/nvidia_office: glass meeting room right, city window left, wall screen centre, 4 desk monitors, mugs
    ('silhouettes', dict(y=560, x0=1400, x1=1862, n=3, s=1.75, speed=48, clip=(1404, 112, 1858, 558), glass=.45)),
    ('birds', dict(y=200, n=4, period=9, s=.7, within=(60, 110, 520, 560))),
    ('plane', dict(y=150, period=14, s=.8, within=(60, 110, 520, 560))),
    ('screen', dict(rect=(668, 140, 1252, 490), kind='chart', bg='#14213D')),
    ('screen', dict(rect=(288, 620, 412, 700), kind='chart', v='#FFFFFF', bg='#5B8FD8')),
    ('screen', dict(rect=(182, 722, 338, 830), kind='code', bg='#5B8FD8')),
    ('screen', dict(rect=(1448, 622, 1570, 700), kind='mail', bg='#5B8FD8')),
    ('screen', dict(rect=(1502, 724, 1658, 832), kind='chart', v='#FFFFFF', bg='#5B8FD8')),
    ('steam', dict(x=405, y=852, s=.8)), ('steam', dict(x=1724, y=852, s=.8)),
    ('dust', dict(rect=(560, 560, 1360, 900), n=18)),
]
STREET = [   # night/sg_street: pavement y~790, road 800-1080, lamps at x 330 / 1610
    ('stars', dict(region=(0, 0, 1920, 220), n=30)),
    ('clouds', dict(y=70, n=3, speed=12, a=120, s=.8)),
    ('birds', dict(y=150, n=6, period=10, s=.9)),
    ('window_lights', dict(rects=[(162, 302, 240, 418), (1272, 302, 1350, 418), (1662, 302, 1740, 418), (702, 452, 780, 568), (1662, 452, 1740, 568)], period=5)),
    ('moths', dict(x=330, y=330)), ('moths', dict(x=1610, y=330)),
    ('silhouettes', dict(y=792, n=7, s=.8, speed=60)),
    ('cars', dict(y=905, n=2, period=6, d=1, s=.8)), ('cars', dict(y=1030, n=2, period=7, d=-1, s=1.0)),
]
an = Actor('analyst', 960, 1010, 1.0, face=.35, rim='#9FB8F0').pose(.2, ('down', 'point'))
office = shots.wide('night/nvidia_office', [an], amb=OFFICE, t0=0.0)
street = shots.wide('night/sg_street', amb=STREET, t0=7.0)
files = [render.render_shot(str(OUT / 'amb_office.mp4'), 7.0, office, zoom=(1.0, 1.06), focus=((900, 560), (1060, 560))),
         render.render_shot(str(OUT / 'amb_street.mp4'), 7.0, street, zoom=(1.0, 1.05), focus=((900, 600), (1020, 600)))]
print(render.join(files, str(OUT / 'ambience_preview.mp4')))
