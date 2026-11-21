# Part 1 - Chapter 1 "Out of Nowhere" - SHOT PLAN (n011-n025)  [PROPOSAL, no code written, no render]

Only LOCKED assets are used (see ASSET_LIBRARY.md). Night print throughout. Chapter card "Out of Nowhere" comes first (existing chapter-card widget).
Rhythm: new picture every 2-3 s, a visual beat every 20-30 s, no repeated wide, camera always moving (zoom/pan).
Tags = lower_third(name, role) in each shot's `hud`. Total chapter about 60-70 s.

| # | Line | Picture (set / characters / props) | Camera | Animation + beat | Tag / hud |
|---|------|-----------------------------------|--------|------------------|-----------|
| 1 | n011 "Rewind to 2023, in Singapore." | night/sg_street, empty | whip-pan in from skyline, settles low-angle | calendar page flips back to 2023 (anim.calendar) | place tag: Singapore, 2023 |
| 2 | n012 "...Megaspeed has just been reborn." (a) | sg_street, blank sign frame above a door | push-in on the frame | sign_megaspeed drops in with glow (new name lights up) | - |
| 3 | n012 (b) | close-up of the door + sign, glow flicker | slow tilt up | "REBORN" pop label | - |
| 4 | n013 "Before that, the Singapore arm of a Chinese video game company." | same street, sign_old_arcade (GAME PALACE, invented) hanging | pull-back from close | old sign unscrews, swings down, falls out of frame | pop label "formerly a game company" |
| 5 | n013 (b) | Megaspeed office, wide | slow pan right | new sign goes up, old one carried off by `worker` | - |
| 6 | n013b "...official Nvidia cloud partner." | megaspeed_office desk, close, 2 hands | top-down push | certificate slides onto desk (props.certificate), stamp "REPORTED" | chip uses Nvidia green #76B900 (rule 3b); owner OK needed to change the old "no green" hint |
| 7 | n014 "...rent out computing power." (a) | night/datacenter, one-point aisle | dolly forward down the aisle | server racks light up row by row | - |
| 8 | n014 (b) | close-up chip glowing gold on a rack | rack-focus punch-in | chip pulses | - |
| 9 | n015 "Everyone wants those chips." | velvet_display, chip on velvet | slow orbit/zoom | crowd silhouettes press in (queue widget, worried=False) | - |
| 10 | n015 "Not everyone is allowed." | same, tighter | snap zoom | red rope drops, hand_k reaching hand stops at rope | pop label "ALLOWED?" |
| 11 | n015b "Jensen Huang co-founded Nvidia in 1993." | night/diner93, `jensen93` in booth, grey hair | start close on face, pull back | calendar on wall, 1993 | **Jensen Huang / Nvidia co-founder, 1993** |
| 12 | n015b "...only CEO for 33 years." | diner93 wide, napkin sketch on table | pan to calendar | calendar flips 1993 -> 2026 fast (anim.calendar days) | counter-style "33 YEARS" gold |
| 13 | n016 "Its boss was Alice Huang..." | megaspeed office, `alice` at desk, lanyard | slow push to face | first appearance, expression neutral | **Alice Huang (alleged) / then-CEO, Megaspeed** |
| 14 | n016 "A Chinese national, per U.S. reports. A Hong Kong resident, per Singapore." | split card over office: two paper cards, "U.S. REPORTS" vs "SINGAPORE SAYS" | cards slide in left/right | cards slam with stamp "ATTRIBUTED" | - |
| 15 | n017 "No relation. Same last name." | blank navy plate, props.tag_pair HUANG / HUANG | static punch-in | equals sign draws, crosses out (cross_k 0 -> 1), small shake | - |
| 16 | n018 "2023 assets about $33 million." | megaspeed_office, alice small at desk | wide, slow drift | widgets.counter 0 -> $33,000,000, gold | - |
| 17 | n019 "A year later, almost three billion." | same set | camera shake + push on the counter | counter races to $3,000,000,000, calendar page +1 year | - |
| 18 | n020 ANALYST "$33M to $3B? In one year?" (dramatised) | night office/desk, `analyst` close-up, wide eyes | close-up, slight dutch | takes glasses off, jaw drop; counter ghosted behind | **THE ANALYST / dramatised** |
| 19 | n021 "A Tufts professor said it appeared out of nowhere." | `professor` at lectern/bookshelf (office set) | slow push | sticky note with his opinion (widgets.sticky), shown as OPINION | **THE PROFESSOR / Tufts University** |
| 20 | n022 "Dec 7, 2023, a photo..." (a) | night/restaurant, candle table, `jensen` + `alice` in front, backs/profile | close on candle then pull back | candlelight flicker | place tag: Singapore, Dec 7 2023 |
| 21 | n022 (b) | restaurant wide, camera flash | snap | polaroid slides in, labelled REPORTED (widgets.polaroid) | **Jensen Huang / CEO, Nvidia**, **Alice Huang (alleged)** |
| 22 | n023 "Sept 2024, U.S. official in a Malaysia data center." (a) | night/datacenter, long aisle, `inspector` (hi-vis, lanyard) small at far end | low tracking shot following him | inspector walks toward camera, flashlight beam sweeps | place tag: Malaysia, Sept 2024; **THE INSPECTOR / U.S. official (dramatised)** |
| 23 | n023 (b) | aisle side view, inspector + `inspector2` | pan along racks | sealed crates come into view at the end of the aisle | - |
| 24 | n024 INSPECTOR "Why are these Nvidia servers still sitting in their boxes?" | close-up, inspector face + flashlight on sealed crates | push-in, then whip-pan to crates | flashlight lands on crate stencil; echo hum SFX | - |
| 25 | n025 "Remember those boxes..." CARD | crate stencil glows gold, hard cut to black, text card | locked zoom 1.0 -> 1.02 | gold glow, hard cut | - |

Notes
- Dialogue moments in this chapter: n020 and n024 (script already has 29 dialogue lines in total).
- Not yet built (shot-level animation only, no new assets): sign swap, certificate slide, reaching hand, flashlight sweep, inspector walk, whip-pan.
- Real people (Jensen, Alice, professor) never get invented quotes; the professor's note is paraphrase of reported opinion.
- Megaspeed's real brand colours are NOT verified, so the sign stays in our palette until verified.
- Imported codex assets: none needed for Chapter 1.
