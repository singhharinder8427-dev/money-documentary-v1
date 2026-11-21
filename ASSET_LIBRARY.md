# Dirty Dollar - ASSET LIBRARY (named, reusable across videos)

Every approved character, set (office / street / room), prop, animation and widget lives here with ONE name, so any later
video can reuse it by name. Rule (CLAUDE.md 3c): when the owner approves an asset, lock it in code AND add/update its row
here in the same step, then ask "save now or later?". New videos start by showing this list (reuse vs new is the owner's choice).
Status: **LOCKED** = owner approved, never change without asking. **PENDING** = built, waiting for the owner's OK.
Code lives in `.claude/skills/documentary-animator/engine/` (`cast.py`, `sets.py`, `sets_src/`, `props.py`, `anim.py`, `widgets.py`).

## Characters  (`engine/cast.py`, key = what you pass to Actor / person)
| Name (on screen) | Key | Look (signature traits) | From video | Status |
|---|---|---|---|---|
| The CEO | `ceo` | navy suit, gold tie, silver hair, white moustache, glasses | Ponzi | LOCKED |
| The Analyst | `analyst` | grey suit, navy tie, slick black hair, glasses | Ponzi | LOCKED |
| The Worker | `worker` | brown suit, flat hat, slick brown hair | Ponzi | LOCKED |
| The Banker | `banker` | dark suit, gold bow tie, moustache, hanky | Ponzi | LOCKED |
| The Investor | `investor` | gold suit, navy tie, black bob | Ponzi | LOCKED |
| The Saver | `saver` | navy sweater, long brown hair | Ponzi | LOCKED |
| The Grad | `grad` | grey hoodie, curly black hair | Ponzi | LOCKED |
| The Scammer | `scammer` | black open jacket, slick hair, glasses | Ponzi | LOCKED |
| The Agent | `agent` | dark suit, buzz cut | Ponzi | LOCKED |
| The Reporter | `reporter` | grey jacket, glasses (has a bun - owner does not want buns; not used in new videos) | Ponzi | LOCKED |
| The Retiree | `retiree` | brown sweater, bald, glasses | Ponzi | LOCKED |
| Charles Ponzi | `ponzi` | straw boater, pencil moustache, wing collar, cane (REAL) | Ponzi | LOCKED |
| Jensen Huang | `jensen` | black leather jacket (shiny lapels), dark rectangular glasses, thick swept GREY hair, lighter grey temples (REAL) | Nvidia Files | PENDING (reworked 22 Nov) |
| Jensen Huang, 1993 | `jensen93` | same jacket + glasses, same grey hair (REAL) | Nvidia Files | PENDING |
| Alice Huang (alleged) | `alice` | dark bob, charcoal blazer, white shirt, gold ID lanyard, silent (REAL, always tagged "alleged") | Nvidia Files | LOCKED |
| The Inspector | `inspector` | gold hi-vis vest, lanyard, buzz cut | Nvidia Files | LOCKED |
| The Colleague | `inspector2` | gold hi-vis vest, lanyard, glasses, long brown hair | Nvidia Files | PENDING (hair changed) |
| The Professor | `professor` | tweed suit, bow-tie look, grey slicked hair, glasses, moustache | Nvidia Files | PENDING (hair changed) |

## Sets / places  (`engine/sets.py`, key = `get_set(name)`)
| Name | Key | What it is | From video | Status |
|---|---|---|---|---|
| CEO Office (night) | `night/office` | corner office, skyline window | Ponzi | LOCKED |
| Trading Floor (night) | `night/trading` | busy trading floor | Ponzi | LOCKED |
| Desk top-down (night) | `night/desk` | hands + documents on a desk | Ponzi | LOCKED |
| Modern Street (night) | `night/street` | bank + pawn shop street | Ponzi | LOCKED |
| 1920 Street (night) | `night/street1920` | queue-at-the-door street | Ponzi | LOCKED |
| Kitchen (night) | `night/kitchen` | kitchen table, bills | Ponzi | LOCKED |
| Living Room / Kitchen / Bank / Street / Lesson (day) | `day/living` `day/kitchen` `day/bank` `day/street` `day/lesson` | lesson-part sets, day print | Ponzi | LOCKED |
| Singapore Shophouse Street (night) | `night/sg_street` | shophouse row, bay towers, blank sign frame | Nvidia Files | LOCKED |
| Megaspeed Office (night) | `night/megaspeed` | open office, glass server room, blank wall panel | Nvidia Files | LOCKED |
| 1993 Roadside Diner (night) | `night/diner93` | booth, counter, neon DINER, calendar frame | Nvidia Files | LOCKED |
| Singapore Italian Restaurant (night) | `night/restaurant` | candle table, arched windows, wine shelf | Nvidia Files | LOCKED |
| Data-Center Aisle (night) | `night/datacenter` | one-point-perspective racks + sealed crates | Nvidia Files | LOCKED |

## Props  (`engine/props.py` = Nvidia Files; `engine/anim.py` + `engine/widgets.py` = earlier)
| Name | Function | Notes | From video | Status |
|---|---|---|---|---|
| Megaspeed Sign | `props.sign_megaspeed` | typographic wordmark + speed lines (real colours still to verify) | Nvidia Files | LOCKED |
| Old Arcade Sign ("GAME PALACE", invented) | `props.sign_old_arcade` | dull tilted sign | Nvidia Files | LOCKED |
| AI Chip | `props.chip` | navy package, `accent` colour (gold default, `BRAND['nvidia']` green) | Nvidia Files | LOCKED |
| Certificate | `props.certificate` | "NVIDIA CLOUD PARTNER", green chip mark | Nvidia Files | LOCKED |
| Server Rack | `props.server_rack` | blinking gold lights | Nvidia Files | LOCKED |
| Sealed Crate | `props.crate` | stenciled, tape cross, glow option | Nvidia Files | LOCKED |
| Velvet Chip Display | `props.velvet_display` | pedestal, gold rope, reaching hand | Nvidia Files | LOCKED |
| Flashlight Cone | `props.flashlight` | additive light cone | Nvidia Files | LOCKED |
| Name-Tag Pair | `props.tag_pair` | two HUANG tags, crossed-out equals | Nvidia Files | LOCKED |
| Hand Slam, Pyramid, Calendar, Flag, Map Route, Handcuffs, Newspaper, Phone Ring, Ledger, Envelope, Prison Bars, Police Car (+spotlight), Phone Screen, Coin Rain, Queue, Held item, End Screen, Outro | `anim.*` | story animations | Ponzi | LOCKED |
| Cards, counters, stamps, charts, sticky note, document, polaroid, lower third, place tag, money props | `widgets.*` | see `widgets.py` | Ponzi | LOCKED |

## Brand colours of real companies (CLAUDE.md 3b)
| Company | Colours | Verified from |
|---|---|---|
| Nvidia | green `#76B900`, dark grey `#1E1E1E`, white | Nvidia logo & brand usage page |
| Megaspeed | NOT YET VERIFIED | - |
