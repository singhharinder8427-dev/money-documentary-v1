"""Preview stills for the Part 2 places + props. Run ONLY after the owner OKs a preview render.
   cd .claude/skills/documentary-animator && python3 ../../../videos/nvidia-files-part2/places_preview.py"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / '.claude' / 'skills' / 'documentary-animator'))
import skia
from engine import sets, props_dc, widgets
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
shot('night/white_house', [('trump', 'podium', dict(face=.2, mouth='flat'))], 'set_white_house.png')
shot('night/oval_office', [('trump', 'desk', dict(face=-.2, mouth='flat')), ('rubio', 'front_left', dict(face=.3, mouth='flat'))], 'set_oval_office.png')
shot('night/af1_cabin', [('rubio', 'left', dict(face=.3, mouth='flat')), ('trump', 'right', dict(face=-.3, mouth='flat'))], 'set_af1_cabin.png')
shot('night/commerce_hq', [('lutnick', 'steps', dict(face=0, mouth='smile'))], 'set_commerce_hq.png')
shot('night/commerce_room', [('lutnick', 'center', dict(face=0, mouth='flat')), ('intel', 'left', dict(face=.3, mouth='flat'))], 'set_commerce_room.png')
surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.Color(246, 239, 226))
props_dc.af1_plane(c, 560, 300, 1.2); props_dc.memo_folder(c, 1400, 330, 1.0, rot=-4)
props_dc.memo_folder(c, 480, 800, 1.0, rot=3, open_k=1.0)
try: props_dc.prop_stamp(c, 'TOP SECRET', 1400, 330, 1.0)
except Exception as e: print('stamp skipped:', e)
try: props_dc.prop_stamp(c, 'REPORTED', 1380, 800, 1.0, rot=-6, size=90)
except Exception as e: print('stamp2 skipped:', e)
save(surf, 'props_part2.png')
