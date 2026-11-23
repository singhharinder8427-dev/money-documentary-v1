"""The channel's cast. The first five are LOCKED looks (BRAND.md). The rest are reusable archetypes in the same
style. Real people: copy an archetype and change only their signature traits (hair, colour, glasses, outfit),
and identify them with a name tag (lower third). Never a likeness of a photo."""
from engine.core import NAVY, GOLD, GREY, WHITE

LOCKED = {
 'ceo': dict(skin='#F8E2D2', skin_d='#E6C4AE', suit=NAVY, suit_d='#0C152B', shirt=WHITE, tie=GOLD, hair='silver', hair_col='#ECECF1',
             glasses=True, moustache=True, moustache_col='#FFFFFF', moustache_outline=True, moustache_dy=10),
 'analyst': dict(skin='#C8875A', skin_d='#A86C43', suit=GREY, suit_d='#BDBDBD', shirt=WHITE, tie=NAVY, hair='slick', hair_col='#1A1414', glasses=True),
 'worker': dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#6B4A2E', suit_d='#4F3520', shirt='#F4EFE2', tie='#2B4A7A', hair='slick', hair_col='#7A4A26',
                hat_col='#3A3F4A', hat_band=GOLD),   # wears the hat with hat=True
 'banker': dict(skin='#E2B48C', skin_d='#C49468', suit='#2E2E38', suit_d='#1E1E26', shirt=WHITE, tie=GOLD, bowtie=True, hair='slick', hair_col='#3A2A20',
                moustache=True, hanky=GOLD),
 'investor': dict(skin='#8D5A3B', skin_d='#6F4429', suit=GOLD, suit_d='#D88A06', shirt=WHITE, tie=NAVY, hair='bob', hair_col='#15110F'),
}
ARCHETYPES = {
 'saver': dict(skin='#E9B98F', skin_d='#CC9A6E', suit='#2B4A7A', suit_d='#1F3860', shirt='#F4EFE2', outfit='sweater', hair='long', hair_col='#4A2E1C'),
 'grad': dict(skin='#B97A50', skin_d='#9A6038', suit='#3A3F4A', suit_d='#2A2E36', shirt='#F4EFE2', outfit='hoodie', hair='curly', hair_col='#1A1414'),
 'scammer': dict(skin='#F2D3B5', skin_d='#D9B593', suit='#1E1E26', suit_d='#121218', shirt='#2E2E38', outfit='open', hair='slick', hair_col='#0E0E12', glasses=True),
 'agent': dict(skin='#7E4E32', skin_d='#633A22', suit='#24304A', suit_d='#18203A', shirt=WHITE, tie='#0E1424', hair='buzz', hair_col='#121212'),
 'reporter': dict(skin='#F5D9C4', skin_d='#DDBBA3', suit=GREY, suit_d='#BDBDBD', shirt=NAVY, outfit='open', hair='bun', hair_col='#8A5A2E', glasses=True),
 'retiree': dict(skin='#EFCFB2', skin_d='#D4AF8F', suit='#6B5A46', suit_d='#52432F', shirt='#F4EFE2', outfit='sweater', hair='bald', hair_col='#D9D9DE', glasses=True),
}
CAST = {**LOCKED, **ARCHETYPES}
# Real people (our style, signature traits only - always shown with a name tag)
REAL = {
 # Charles Ponzi (1882-1949), from period photos: short + dapper, slicked-back side-parted dark hair, thin trimmed
 # moustache, straw boater, light suit, pocket square, high starched collar, gold-handled cane (kit.cane), easy smile.
 'ponzi': dict(skin='#E6BC93', skin_d='#C99E76', suit='#E3DAC6', suit_d='#C7BCA3', shirt='#FFFFFF', tie='#2B2B36', hair='slick', hair_col='#15110F',
               hair_part=True, moustache=True, moustache_style='pencil', moustache_col='#15110F', wing_collar=True,
               hat_style='boater', hat_col='#E8C77A', hat_band='#14213D', hanky='#FFFFFF'),   # wear with hat=True; he was short: use ~0.9x scale
}
# LOCKED by the owner 22 Nov 2026: jensen, jensen93, alice, inspector, inspector2, professor (see ASSET_LIBRARY.md; do not change without asking)
# ---- The Nvidia Files (real people: signature traits only, never a photo likeness; always shown with a name tag)
REAL.update({
 # Jensen Huang: black leather jacket (his signature), swept salt-and-pepper hair, no glasses, warm round-ish face, easy smile.
 'jensen': dict(skin='#E9C7A5', skin_d='#CBA682', suit='#22222A', suit_d='#121218', lapel='#3E3E4C', shirt='#15151B', tie=None, outfit='jacket',
                hair='quiff', hair_col='#A5A5B2', hair_grey='#C9C9D3', glasses=True, glasses_style='rect', face_shape=(1.04, .98)),
 # 1993 version (company co-founder, 30): same jacket + glasses; hair grey like the current Jensen (owner, 22 Nov).
 'jensen93': dict(skin='#EBCBAA', skin_d='#CDAA86', suit='#22222A', suit_d='#121218', lapel='#3E3E4C', shirt='#15151B', tie=None, outfit='jacket',
                  hair='quiff', hair_col='#A5A5B2', hair_grey='#C9C9D3', glasses=True, glasses_style='rect', face_shape=(1.04, .98)),
 # Alice Huang (ALLEGED, per reports; never speaks): neutral professional look - dark bob, charcoal blazer, white shirt, ID lanyard.
 'alice': dict(skin='#F1D3B8', skin_d='#D8B496', suit='#3A3F4A', suit_d='#2A2E36', shirt='#FFFFFF', tie=None, outfit='open',
               hair='bob', hair_col='#15110F', lanyard=GOLD),
})
ARCHETYPES.update({
 'inspector': dict(skin='#B97A50', skin_d='#9A6038', suit='#4A5568', suit_d='#363F4F', shirt='#F4EFE2', tie=None, outfit='vest', hair='buzz', hair_col='#121212', lanyard=NAVY, hat_col='#E5E5E5', hat_band=GOLD),
 'inspector2': dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#4A5568', suit_d='#363F4F', shirt='#F4EFE2', tie=None, outfit='vest', hair='long', hair_col='#4A2E1C', glasses=True, lanyard=NAVY),
 'professor': dict(skin='#EFCFB2', skin_d='#D4AF8F', suit='#6B5A46', suit_d='#52432F', shirt='#F4EFE2', tie='#2B4A7A', hair='slick', hair_col='#B8B8C2', glasses=True, moustache=True, moustache_col='#B8B8C2'),
})
CAST.update(ARCHETYPES); CAST.update(REAL)
CAST.update(REAL)
NAMES = {'ceo': 'THE CEO', 'analyst': 'THE ANALYST', 'worker': 'THE WORKER', 'banker': 'THE BANKER', 'investor': 'THE INVESTOR',
         'saver': 'THE SAVER', 'grad': 'THE GRAD', 'scammer': 'THE SCAMMER', 'agent': 'THE AGENT', 'reporter': 'THE REPORTER', 'retiree': 'THE RETIREE', 'inspector': 'THE INSPECTOR', 'inspector2': 'THE COLLEAGUE', 'professor': 'THE PROFESSOR', 'jensen': 'JENSEN HUANG', 'jensen93': 'JENSEN HUANG, 1993', 'alice': 'ALICE HUANG (ALLEGED)', 'ponzi': 'CHARLES PONZI'}

def person(base, **changes):
    """New character from a cast entry: person('ceo', hair='slick', suit='#2E2E38', glasses=False)."""
    d = dict(CAST[base]); d.update(changes); return d

# LOCKED 22 Nov 2026 (owner approved): Nvidia Files Part 1, CH2-CH5 role characters (see ASSET_LIBRARY.md)
ARCHETYPES.update({
    'officer': dict(skin='#C98E62', skin_d='#A8714A', suit='#1E2A40', suit_d='#141D30', shirt='#9DB0DA', tie='#0E1424', hair='buzz', hair_col='#141414',
                    hat_style='peaked', hat_col='#1E2A40', hat_band='#0E1424', badge=True),
    'clerk': dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#3A3F4A', suit_d='#2A2E36', shirt='#F4EFE2', outfit='sweater', hair='long', hair_col='#2A1A12', glasses=True),
    'manager': dict(skin='#8A5A3C', skin_d='#6E4428', suit='#2E2E38', suit_d='#1E1E26', shirt=WHITE, tie=GOLD, hair='slick', hair_col='#121212'),
    'lawyer': dict(skin='#EFCFB2', skin_d='#D4AF8F', suit='#22283A', suit_d='#161B2A', shirt=WHITE, tie='#7A1E2A', hair='slick', hair_col='#8A8A94', glasses=True),
    'director': dict(skin='#E2B48C', skin_d='#C49468', suit='#3A3F4A', suit_d='#2A2E36', shirt=WHITE, tie=NAVY, hair='bald', hair_col='#D9D9DE'),
    'director2': dict(skin='#B97A50', skin_d='#9A6038', suit='#2B4A7A', suit_d='#1F3860', shirt=WHITE, tie=GOLD, outfit='open', hair='long', hair_col='#1A1414'),
    'trader': dict(skin='#F5D9C4', skin_d='#DDBBA3', suit='#3E6BB0', suit_d='#2E5590', shirt='#F4EFE2', tie=NAVY, outfit='open', hair='slick', hair_col='#C08A3A', lanyard=GOLD),
    'supervisor': dict(skin='#7E4E32', skin_d='#633A22', suit='#24304A', suit_d='#18203A', shirt=WHITE, tie='#0E1424', hair='slick', hair_col='#8A8A94', glasses=True),
    'customer': dict(skin='#E9B98F', skin_d='#CC9A6E', suit='#C0582A', suit_d='#9A4420', shirt='#F4EFE2', outfit='hoodie', hair='curly', hair_col='#3A2414'),
    'seller': dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#F4EFE2', suit_d='#D8D2C4', shirt=NAVY, outfit='sweater', apron='#9DB0DA', hair='buzz', hair_col='#5A3A22'),
})
CAST.update({k: ARCHETYPES[k] for k in ('officer', 'clerk', 'manager', 'lawyer', 'director', 'director2', 'trader', 'supervisor', 'customer', 'seller')})
NAMES.update({'officer': 'THE OFFICER', 'clerk': 'THE CLERK', 'manager': 'THE MANAGER', 'lawyer': 'THE LAWYER', 'director': 'THE DIRECTOR',
              'director2': 'THE SECOND DIRECTOR', 'trader': 'THE TRADER', 'supervisor': 'THE SUPERVISOR', 'customer': 'THE CUSTOMER', 'seller': 'THE SELLER'})

# ---- The Nvidia Files Part 2: 'trump' LOCKED by the owner 23 Nov 2026 (see ASSET_LIBRARY.md; do not change without asking). Real person, signature traits only, never a photo
# likeness; always shown with a name tag. Reference: official portrait sent by the owner (23 Nov).
REAL.update({
 # Donald Trump: thick light-blond hair swept up and over to the side, fair-warm skin, navy suit, white shirt, long blue patterned tie
 # (blue as in the reference - fits our navy palette), wide easy smile.
 'trump': dict(skin='#EBB48C', skin_d='#CE9468', suit=NAVY, suit_d='#0C152B', lapel='#22304F', shirt=WHITE, tie='#2B4A7A', hair='swoop',
               hair_col='#E2BE7E', hair_grey='#F0DCA8', face_shape=(1.12, 1.0), brow_col='#E6CB98', eye_h=.72, pin=True),
})
CAST['trump'] = REAL['trump']
NAMES['trump'] = 'DONALD TRUMP'

# Marco Rubio: 'rubio' LOCKED by the owner 23 Nov 2026 (see ASSET_LIBRARY.md; do not change without asking). Real person, signature traits only (never a photo likeness); always with a name tag.
# Reference: photo sent by the owner: short dark-brown hair combed to the side, high forehead, slimmer face, darker brows, calm serious look,
# navy suit, white shirt, red patterned tie.
REAL.update({
 'rubio': dict(skin='#E6B894', skin_d='#C99A74', suit='#1B2A4A', suit_d='#0F1A33', lapel='#2A3A5E', shirt=WHITE, tie='#9B2C3A', hair='slick',
               hair_col='#2E1D15', hair_part=True, face_shape=(.97, 1.05), brow_col='#3A2418', eye_h=.88),
})
CAST['rubio'] = REAL['rubio']
NAMES['rubio'] = 'MARCO RUBIO'

# Howard Lutnick: 'lutnick' LOCKED by the owner 23 Nov 2026 (see ASSET_LIBRARY.md; do not change without asking). Real person, signature traits only (never a photo likeness); always with a name tag.
# Reference: photo sent by the owner: bald on top with short grey hair at the sides, full trimmed grey-white beard, broad warm grin,
# wide ruddy face, dark suit, white shirt, navy patterned tie.
REAL.update({
 'lutnick': dict(skin='#E9AE8E', skin_d='#CC8E6E', suit='#1C2030', suit_d='#10131E', lapel='#2B3248', shirt=WHITE, tie='#444A86', hair='bald',
                 hair_col='#9C9CA6', beard=True, beard_col='#B9B9C0', moustache=True, moustache_col='#B9B9C0', moustache_outline=True, blush='#E58A82',
                 face_shape=(1.1, .98), brow_col='#9A9AA4', eye_h=.8),
})
CAST['lutnick'] = REAL['lutnick']
NAMES['lutnick'] = 'HOWARD LUTNICK'

# ---- The Nvidia Files Part 2 generic roles: 'intel', 'reporter2' LOCKED by the owner 23 Nov 2026 (do not change without asking) (see ASSET_LIBRARY.md)
ARCHETYPES.update({
    # intel / security officer for the Washington scenes: dark suit, white shirt, dark tie, gold-badge lanyard, short grey-flecked hair (NOT the hi-vis Inspector)
    'intel': dict(skin='#D9A27A', skin_d='#BC8760', suit='#2B3445', suit_d='#1B2230', shirt=WHITE, tie='#1B1B22', hair='slick', hair_col='#3A3A44',
                  lanyard=GOLD, glasses=False),
    # reporter, no bun (owner): short brown bob, glasses, soft blue jacket, press lanyard
    'reporter2': dict(skin='#F2D3B5', skin_d='#D9B593', suit='#5B6B82', suit_d='#44536A', shirt=WHITE, outfit='open', hair='bob', hair_col='#7A4A26',
                      glasses=True, lanyard=GOLD),
})
CAST.update({k: ARCHETYPES[k] for k in ('intel', 'reporter2')})
NAMES.update({'intel': 'THE OFFICER', 'reporter2': 'THE REPORTER'})
