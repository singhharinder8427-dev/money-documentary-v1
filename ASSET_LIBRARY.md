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
| Jensen Huang | `jensen` | black leather jacket (shiny lapels), dark rectangular glasses, thick swept GREY hair, lighter grey temples (REAL) | Nvidia Files | LOCKED (22 Nov) |
| Jensen Huang, 1993 | `jensen93` | same jacket + glasses, same grey hair (REAL) | Nvidia Files | LOCKED (22 Nov) |
| Alice Huang (alleged) | `alice` | dark bob, charcoal blazer, white shirt, gold ID lanyard, silent (REAL, always tagged "alleged") | Nvidia Files | LOCKED |
| The Inspector | `inspector` | gold hi-vis vest, lanyard, buzz cut | Nvidia Files | LOCKED |
| The Colleague | `inspector2` | gold hi-vis vest, lanyard, glasses, long brown hair | Nvidia Files | LOCKED (22 Nov) |
| The Professor | `professor` | tweed suit, bow-tie look, grey slicked hair, glasses, moustache | Nvidia Files | LOCKED (22 Nov) |

## Sets / places  (`engine/sets.py`, key = `get_set(name)`)
NEW places from 22 Nov 2026 are made in the real-colour night look (CLAUDE.md 3d): flat 2D real colours -> `looks.real_night`.
| Name | Key | What it is | From video | Status |
|---|---|---|---|---|
| CEO Office (night) | `night/office` | corner office, skyline window | Ponzi | LOCKED |
| Trading Floor (night) | `night/trading` | busy trading floor | Ponzi | LOCKED |
| Desk top-down (night) | `night/desk` | hands + documents on a desk | Ponzi | LOCKED |
| Modern Street (night) | `night/street` | bank + pawn shop street | Ponzi | LOCKED |
| 1920 Street (night) | `night/street1920` | queue-at-the-door street | Ponzi | LOCKED |
| Kitchen (night) | `night/kitchen` | kitchen table, bills | Ponzi | LOCKED |
| Living Room / Kitchen / Bank / Street / Lesson (day) | `day/living` `day/kitchen` `day/bank` `day/street` `day/lesson` | lesson-part sets, day print | Ponzi | LOCKED |
| Singapore Shophouse Street (night) | `night/sg_street` | shophouse row, bay towers, blank sign frame | Nvidia Files | LOCKED (real-colour night look, 22 Nov) |
| Megaspeed Office (night) | `night/megaspeed` | open office, glass server room, blank wall panel | Nvidia Files | LOCKED (real-colour night look, 22 Nov) |
| 1993 Roadside Diner (night) | `night/diner93` | booth, counter, neon DINER, calendar frame | Nvidia Files | LOCKED (real-colour night look, 22 Nov) |
| Singapore Italian Restaurant (night) | `night/restaurant` | candle table, arched windows, wine shelf | Nvidia Files | LOCKED (real-colour night look, 22 Nov) |
| Data-Center Aisle (night) | `night/datacenter` | one-point-perspective racks + sealed crates | Nvidia Files | LOCKED (real-colour night look, 22 Nov) |
| Nvidia HQ - Endeavor entrance (real-colour night) | `night/nvidia_hq` | glass HQ, lit lobby, lamps, stairs, sign wall with rough eye logo; spots walkway/stairs/sign. FIRST asset in the new real-colour night look (CLAUDE.md 3d) | Nvidia Files | LOCKED |

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


---
# IMPORTED from the codex repo (22 Nov 2026) - USE ONLY WHEN THE STORY NEEDS THEM
Owner rule: these are in the library so they can be reused by name, but a video uses ONLY the ones its story needs, never
many at once. They arrive in the codex look (dark screen frames, `illustrative` labels); each one is RESTYLED to our print look
the first time a video uses it (preview shown to the owner first). Real documents carry their real source line, not "fictional sample".
Code: `engine/story_assets/*`, `engine/explainers.py`, `engine/paper_trail.py`, `engine/sets_src/{boardroom,courtroom,documentary_locations,sales_floor}.py`.
Reference notes: `graphics/codex-library/*.md`. Status for all rows: **IMPORTED** (not yet restyled / not yet used).

## Sets (key = `get_set(name)`)
| Name | Key | Good for |
|---|---|---|
| TV Interview Studio (night) | `night/tv_interview_studio` | interviews (e.g. Jensen's "completely normal" clip) |
| Press Conference Stage (day) | `day/press_conference` | statements, announcements |
| Boardroom (day) | `day/boardroom` | board meetings, directors |
| Charity Gala / Luxury Apartment / Mansion Exterior | `night/charity_gala` `night/luxury_apartment` `day/mansion_exterior` | wealth and public image |
| Private Banker's Office / Bank Vault | `night/private_banker` `night/bank_vault` | private banking, vaults |
| Ordinary Office Floor / Startup Workspace / Stock Exchange Exterior / Warehouse | `day/ordinary_office` `day/startup_workspace` `day/stock_exchange` `day/warehouse` | business scenes |
| Courtroom / Courthouse Exterior / Deposition Room / Regulator Hearing Room | `day/courtroom` `day/courthouse_exterior` `day/deposition_room` `day/regulator_hearing_room` | legal and regulator scenes |
| Jail Visiting Room (+call version) / Jail Intake Desk / Cell Corridor | `day/visiting_room` `day/visiting_room_call` `day/jail_intake_desk` `night/cell_corridor` | consequences |
| Investigation Room (night) | `night/investigation_room` | investigators, evidence wall |
| Sales Floor (night) | `night/sales_floor` | call-centre / sales scenes |
| Suburban Home / Hotel Ballroom (seminar) | `day/suburban_home` `day/hotel_ballroom` | victims at home, seminars |
| Public Park / Cafe Booth / Apartment Hallway / Shop Counter / Train Station | `day/public_park` `day/cafe_booth` `night/apartment_hallway` `day/shop_counter` `day/train_station` | everyday life |

## Props and graphics (draw functions on a 960x540 design canvas)
| Name | Code | Good for |
|---|---|---|
| Audit Memo, Corporate Filing, Signed Contract, Prospectus, Pitch Deck | `story_assets.paper_trail_props` | company records, filings (e.g. Megaspeed filings) |
| Court Exhibit Sticker, Evidence Bag, Archive Box | `story_assets.paper_trail_props` | investigations |
| General Ledger, Transfer Record, Vendor Invoice, Case Folder | `engine.paper_trail` | money trail |
| Email Window, Message Thread, Call Log | `story_assets.digital` | briefings, messages |
| Investment Dashboard, Transaction History, Fake Profit Screen, Withdrawal Error | `story_assets.digital` | scam-style screens |
| Check, Wire Receipt, Deposit Slip, Credit Card, Payment Terminal, Bank Statement, Cash Drawer | `story_assets.money` | money movement |
| Desk, Cubicle Walls, Conference Chair, Filing Cabinet, Podium, Queue Posts, Street Sign, Park Bench, Period Phone, Period Lamp | `story_assets.furniture` | set dressing |
| Document Callout, Evidence Inset, Border Highlight, Masked Place Label | `engine.explainers` | highlight a line in a real document or a place on a map |
| Route Map, Port Pulses, Goods-to-Routes (hub with routes) | `engine.explainers` | chip routes Singapore/Malaysia (Part 4), zoom-in locator maps |
| Portrait Reveal / Emphasis Portrait Card | `engine.explainers` | introducing a person on screen |

## Supporting characters (`story_assets.people.draw_person(canvas, slug, x, y, scale)`)
| Name | Slug | Good for |
|---|---|---|
| The Attorney | `attorney` | e.g. Nvidia's lawyer (Part 3/4) |
| The Compliance Officer | `compliance-officer` | export-control and compliance scenes |
| The Auditor | `auditor` | financial review |
| The Judge / The Court Clerk | `judge` `court-clerk` | court scenes |
| The Call-Center Operator | `call-center-operator` | scam-call scenes |
| The Small-Business Owner | `small-business-owner` | shop scenes |

## Nvidia Files Part 1, chapters 2-5 (owner approved 22 Nov 2026)
| Name | Code key | Notes | Status |
|---|---|---|---|
| The Officer | cast `officer` | police uniform, peaked cap (new kit hat_style 'peaked'), badge | LOCKED |
| The Clerk | cast `clerk` | | LOCKED |
| The Manager | cast `manager` | | LOCKED |
| The Lawyer | cast `lawyer` | | LOCKED |
| The Director / The Second Director | cast `director`, `director2` | | LOCKED |
| The Trader | cast `trader` | blue trading jacket + lanyard | LOCKED |
| The Supervisor | cast `supervisor` | | LOCKED |
| The Customer / The Seller | cast `customer`, `seller` | seller wears an apron (new kit spec 'apron') | LOCKED |
| Subscribe-for-next-part card | anim `subscribe_next` | replaces the end screen when the owner skips it | LOCKED |
| Reaching hand (sleeve + fingers) | props `velvet_display(hand_k)` | redrawn from the stick arm | LOCKED |
| Codex sets, first use | `night/investigation_room`, `day/shop_counter`, `day/press_conference`, `night/apartment_hallway`, `day/boardroom` | approved as they are (no restyle) for this video | LOCKED |
| Kit add-ons | kit `hat_style='peaked'`, `badge`, `apron` | usable on any character | LOCKED |

## PENDING - Nvidia Files Part 1 QA fixes (22 Nov 2026, owner to approve)
| Name | Code key | Notes | Status |
|---|---|---|---|
| Nvidia logo (rough 2D) | props `nvidia_logo` | green square + white eye swirl + NVIDIA name, drawn fresh (rule 3b) | PENDING |
| Phone lying flat | props `phone_flat` | on tables, lights up / buzzes | PENDING |
| Hair dryer in hand | props `hair_dryer` | with sleeve + hand, hot-air lines | PENDING |
| Handcuffs | props `handcuffs` | two cuffs + 3-link chain, snap shut | PENDING |
| Delivery scooter with rider | props `scooter_rider` | helmet, jacket, pizza box | PENDING |
| Paper / phone held in hand | props `paper_in_hand`, `phone_in_hand` | placed at kit.hand_pos | PENDING |
| Phone pose always holds a phone | kit `_draw_arm` | engine-wide fix | PENDING |
| Emotion-matched talking mouth | actor `draw` | wide grin only on happy lines | PENDING |
| Office workstation | ng_scenes `workstation` | desk on legs, drawer, monitor on stand, chair, keyboard, mug | PENDING |
| Megaspeed office (repaired desks) | set `night/megaspeed` | LOCKED set changed at owner's request (desks were on the floor) | LOCKED (real-colour night look, 22 Nov) |
| Nvidia office | set `night/nvidia_office` | wall screen, glass meeting room, plants, workstations | LOCKED (real-colour night look, 22 Nov) |
| Newsroom | set `night/newsroom` | TV wall, world clocks, desks | LOCKED (real-colour night look, 22 Nov) |
| Clean top-down desk | set `night/desk_clean` | dark wood, mug ring, pen, laptop corner, empty centre for documents | LOCKED (real-colour night look, 22 Nov) |
| Sounds | audio `page_flips`, `phone_ring`, `pickup`, `footsteps`, `room_tone` | flips, buzz+ring, pickup, steps, hum/murmur/rumble/static | PENDING |
| Flags | anim `flag` china / singapore / malaysia | simplified national flags | PENDING |
