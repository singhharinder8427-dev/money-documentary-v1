"""Preview stills for the Part 1 chapter-1 assets (characters, sets, props). Run ONLY after the owner OKs a preview render.
   cd .claude/skills/documentary-animator && python3 ../../../videos/nvidia-files-part1/assets_preview.py
Writes PNGs to videos/nvidia-files-part1/previews/ (one per new set with actors, one character line-up, one prop sheet)."""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / '.claude' / 'skills' / 'documentary-animator'))
import skia
from engine import sets, props
from engine.actor import Actor
from engine.core import W, H
OUT = HERE / 'previews'; OUT.mkdir(exist_ok=True)

def save(surf, name): surf.makeImageSnapshot().save(str(OUT / name), skia.kPNG); print('wrote', name)

def shot(setname, cast, name, extra=None):
    st = sets.get_set(setname); surf = skia.Surface(W, H); c = surf.getCanvas()
    actors = [Actor(who, *st.spots[spot], rim=st.rim, light=st.light, **kw) for (who, spot, kw) in cast]
    st.draw(c, back=[lambda cv, a=a: a.draw(cv, 1.0) for a in actors])
    if extra: extra(c)
    save(surf, name)

shot('night/sg_street', [('jensen', 'right', dict(face=-.3, mouth='smile')), ('alice', 'left', dict(face=.3, mouth='flat'))], 'set_sg_street.png',
     lambda c: props.sign_megaspeed(c, 960, 380, 1.0))
shot('night/megaspeed', [('alice', 'center', dict(face=0, mouth='flat'))], 'set_megaspeed_office.png',
     lambda c: props.sign_megaspeed(c, 960, 240, 1.0, glow=.6))
shot('night/diner93', [('jensen93', 'left', dict(face=.3)), ('analyst', 'right', dict(face=-.3))], 'set_diner93.png')
shot('night/restaurant', [('jensen', 'left', dict(face=.3, mouth='smile')), ('alice', 'right', dict(face=-.3, mouth='smile'))], 'set_restaurant.png')
shot('night/datacenter', [('inspector', 'near_left', dict(face=.3, eyes='wide')), ('inspector2', 'near_right', dict(face=-.3))], 'set_datacenter.png',
     lambda c: (props.flashlight(c, 760, 760, -20, 700, 300), props.crate(c, 1500, 980, 1.2, glow=1.0)))

# character line-up (one row, wide shot scale)
surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.Color(246, 239, 226))
who = ['jensen', 'jensen93', 'alice', 'inspector', 'inspector2', 'professor']
for i, w in enumerate(who): Actor(w, 170 + i * 315, 900, .72, light=1, rim='#FFE3A6').draw(c, 1.0)
save(surf, 'characters_ch1.png')

# prop sheet
surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.Color(246, 239, 226))
props.sign_megaspeed(c, 520, 150, .9); props.sign_old_arcade(c, 1400, 150, .9, hanging=-4)
props.chip(c, 220, 480, 1.1, glow=.4); props.certificate(c, 700, 520, .8, rot=-4); props.velvet_display(c, 1280, 700, .8, hand_k=.6)
props.server_rack(c, 1700, 760, 1.0); props.crate(c, 330, 950, 1.0, glow=1.0); props.tag_pair(c, 980, 930, 1.0, cross_k=1.0)
save(surf, 'props_ch1.png')
