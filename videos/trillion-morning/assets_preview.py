"""Owner preview of the PENDING assets for "The $1.7 Trillion Morning" (24 Nov 2026). Run from this folder:
   python assets_preview.py  ->  out/assets_characters.jpg, out/assets_places_props.jpg"""
import sys, pathlib
SKILL = pathlib.Path(__file__).resolve().parents[2] / '.claude' / 'skills' / 'documentary-animator'; sys.path.insert(0, str(SKILL))
from engine import shots, render, ambience, widgets as Wd, props_ipo as P
from engine.actor import Actor
ambience.enable(); OUT = pathlib.Path(__file__).parent / 'out'; OUT.mkdir(exist_ok=True); RIM = '#9FB8F0'

AMB = {
 'night/nasdaq_tower': [('birds', dict(y=60, n=5, period=8)), ('flashes', dict(region=(0, 700, 1920, 880), rate=2)),
                        ('silhouettes', dict(y=880, n=8, s=.62, speed=60)), ('cars', dict(y=1010, n=2, period=6, s=.9))],
 'night/nasdaq_studio': [('ticker', dict(rect=(60, 562, 1860, 628), items=(('ANT', '+17%'), ('NVDA', '+0.8%'), ('MSFT', '+0.3%'), ('S&P 500', '+0.2%')))),
                         ('gold_dust', dict(n=50, region=(0, 0, 1920, 760))), ('flashes', dict(region=(200, 650, 1720, 760)))],
 'night/openai_hq': [('clouds', dict(y=60, n=3, speed=10, a=110)), ('birds', dict(y=90, n=4, period=9)),
                     ('window_lights', dict(rects=[(387, 282, 487, 370), (1206, 506, 1306, 594), (621, 618, 721, 706)], period=6)),
                     ('silhouettes', dict(y=880, n=4, s=.6, speed=50)), ('cars', dict(y=1010, n=2, period=7, d=-1, s=.9))],
}
for k, v in AMB.items(): ambience.AMBIENCE[k] = v

def act(who, x, y=1010, s=1.0, **e): return Actor(who, x, y, s, face=.3, rim=RIM).pose(.2, ('down', 'down')).expression(0, **e)
stills = []
# 1. characters: full body on the studio + one close-up each for the faces and chest logos
cast_wide = shots.wide('night/nasdaq_studio', [act('dario', 420), act('daniela', 760), act('altman', 1160), act('trader2', 1500)])
stills.append(render.still(cast_wide, 2.0, str(OUT / 'pv_cast_wide.png')))
for who in ('dario', 'daniela', 'altman'):
    stills.append(render.still(shots.closeup('night/openai_hq' if who == 'altman' else 'night/nasdaq_studio', Actor(who, 960, 1390, 2.15, face=.3, rim=RIM).expression(0, mouth='flat'), focus=(960, 560)),
                               1.0, str(OUT / f'pv_{who}.png')))
render.contact_sheet(stills, str(OUT / 'assets_characters.jpg'), cols=2)

# 2. places (with living backgrounds + a character) and props
stills = [render.still(shots.wide('night/nasdaq_tower', [act('trader', 760, 880, .55)]), 3.1, str(OUT / 'pv_tower.png')),
          render.still(shots.wide('night/nasdaq_studio', [act('trader2', 960, 1010)]), 2.4, str(OUT / 'pv_studio.png')),
          render.still(shots.wide('night/openai_hq', [act('altman', 1300, 900, .6)]), 4.2, str(OUT / 'pv_openai.png'))]
def props(c, t):
    Wd.framed_bg(c)
    P.price_tag(c, 330, 300, .8, old='$70-78', u=1); P.investor_list(c, 820, 330, .55); P.share_certificate(c, 1360, 270, .75, signed=1)
    P.app_icon(c, 1740, 260, .8, grey=.5); P.bell(c, 330, 760, .9, t=1.1); P.conveyor(c, t, 900, 560, 1300)
    for i, x in enumerate((680, 930, 1180)): P.fund_box(c, x, 790, .55, grab=(.2, .7, 1)[i])
    P.subscribe_button(c, 1640, 760, .7, click=.45)
stills.append(render.still(props, 1.0, str(OUT / 'pv_props.png')))
tower = shots.wide('night/nasdaq_tower'); stills.append(render.still(tower, 1.5, str(OUT / 'pv_fade.png'), hud=lambda c, t: Wd.chapter_fade(c, 1, 'The Walkout', .45)))
render.contact_sheet(stills, str(OUT / 'assets_places_props.jpg'), cols=2)
print(OUT / 'assets_characters.jpg', OUT / 'assets_places_props.jpg')
