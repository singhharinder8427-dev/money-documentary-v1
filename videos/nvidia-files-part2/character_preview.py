"""Preview of Part 2 characters. Run ONLY after the owner OKs a preview render.
   cd .claude/skills/documentary-animator && python3 ../../../videos/nvidia-files-part2/character_preview.py"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / '.claude' / 'skills' / 'documentary-animator'))
import skia
from engine.actor import Actor
from engine.core import W, H, F_TITLE, F_LABEL, NAVY, GOLD, WHITE
from engine.kit import label, rect, text_w
OUT = HERE / 'previews'; OUT.mkdir(exist_ok=True)
surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.Color(246, 239, 226))
ROW = [('intel', 'THE OFFICER', 'intel office (generic)', dict(face=.3, mouth='flat')),
       ('reporter2', 'THE REPORTER', 'no bun (generic)', dict(face=-.3, mouth='o')),
       ('lawyer', 'THE LAWYER', 'existing, locked (reused)', dict(face=.3, mouth='flat')),
       ('analyst', 'THE ANALYST', 'locked, for scale', dict(face=-.3, mouth='smile'))]
for i, (w, nm, sub, kw) in enumerate(ROW):
    x = 260 + i * 470; sc = 1.0
    Actor(w, x, 760 if i < 2 else 760, sc, light=1, rim='#FFE3A6', **kw).draw(c, 1.0)
    rect(c, x - 200, 862, x + 200, 982, NAVY, 5, r=10)
    label(c, nm, x, 912, 36 * min(1, 360 / text_w(nm, 36, F_TITLE)), GOLD, font=F_TITLE, align='center', skew=0)
    label(c, sub, x, 960, 24, WHITE, font=F_LABEL, align='center', skew=0)
surf.makeImageSnapshot().save(str(OUT / 'generic_preview.png'), skia.kPNG); print('wrote generic_preview.png')
