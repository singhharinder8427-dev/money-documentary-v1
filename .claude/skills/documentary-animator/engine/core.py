"""Shared settings for the documentary animator: frame size, locked palette, locked fonts.
Fonts come from <repo>/fonts (run fetch_fonts.sh in the repo root) or $DOCANIM_FONTS."""
import os, pathlib, skia

W, H, FPS = 1920, 1080, 30
VIDEO_BITRATE = '24M'                       # locked: 1920x1080, 30 fps, 24 Mbps
REPO = pathlib.Path(__file__).resolve().parents[4]
FONT_DIR = os.environ.get('DOCANIM_FONTS', str(REPO / 'fonts')) + '/'

# ---- locked palette (BRAND.md). Gold = money/brand, orange = losses only (with a minus or down arrow), no green.
NAVY, NAVY2, NAVY3 = '#14213D', '#1E3157', '#2B4A7A'
BLACK, WHITE, GREY = '#000000', '#FFFFFF', '#E5E5E5'
GOLD, GOLD_D = '#FCA311', '#D68408'
ORANGE = '#F35B04'
PAPER = '#F6EFE2'
INK = (24, 22, 27)

def _tf(name):
    t = skia.Typeface.MakeFromFile(FONT_DIR + name)
    if t is None: raise FileNotFoundError(f'font {name} missing in {FONT_DIR} - run fetch_fonts.sh in the repo root')
    return t
# ---- locked fonts
F_COUNTER = _tf('DSEG7Classic-Bold.ttf')        # number counters (digits and . only)
F_TITLE = _tf('AlfaSlabOne-Regular.ttf')        # titles, chapter names, stamps
F_TYPE = _tf('SpecialElite-Regular.ttf')        # text cards, documents, quotes (typed word by word)
F_LABEL = _tf('BarlowCondensed-Bold.ttf')       # labels, name tags, sticky notes, place tags
F_LABEL2 = _tf('BarlowCondensed-SemiBold.ttf')
