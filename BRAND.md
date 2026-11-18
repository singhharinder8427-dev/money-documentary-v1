# Money Documentary v1: locked brand decisions

Owner-approved, 18 Nov 2026. Change only with the owner's say-so.

## Channel
- Long-form 16:9 money videos for a **US audience**: money lessons + real money stories. Max **10 minutes**.
- Delivery: **1920x1080, 30 fps, 24 Mbps**, rendered on the owner's PC.

## Colours (locked)
| Colour | Hex | Job |
|---|---|---|
| Navy | `#14213D` | Main background, ink for text on paper |
| Black | `#000000` | Data walls, dark story scenes |
| White | `#FFFFFF` | Paper |
| Light grey | `#E5E5E5` | Cards, desks |
| **Gold** | `#FCA311` | **Brand**: key words, chapter stamps, dollar amounts, highlights |
| **Orange** | `#F35B04` | **Losses and alerts only** |

Rules: gold = money / brand, orange = danger / loss, never swapped; they never touch; orange always with a minus sign
or down arrow; gains in navy ink with an up arrow (no green); small handwriting on white paper is navy, not gold.

## Characters (locked) - `characters/`
- **Head:** slightly rectangular, soft top corners, a well-curved rounded chin. **Short neck.**
- **Body:** rectangle with small rounded corners: jacket, lapels, shirt V, tie or bow tie, pocket square.
- **Legs:** trouser legs in the outfit colour + dark rounded shoes. **Arms:** thin ink-line arms, **round ball hands** (no paper hands).
- **Eyes:** white with a dark pupil + highlight (also half-lidded, closed, wide).
- One thick near-black ink outline. **Crisp, bright, glossy** (jacket + head sheen, blue rim light). **No grain on characters.**
- Outfits in navy / gold / grey / brown / black. Cast so far: CEO (fair skin, side-parted silver hair, white outlined
  moustache, glasses, navy suit, gold tie), Analyst, Worker, Banker, Investor.
- Built on the drawing kit of the "Claude 2D Animation Long Form" skill **made by aivxer** (keep this credit), modified.

## Night scenes (locked: "night print") - `environments/`
- Used for the **story / drama parts**; the night twin of the daytime print look, so the whole channel shares one style.
- **Dark areas:** navy paper in 4 shades by each object's brightness (`#0D1630` `#1B2A52` `#2B3F70` `#3E5689`),
  so floors, desks and walls stay separate, with light-navy ink outlines `#9FB3DE`.
- **Lamp / window light:** reveals the day print (cream `#F8EDD3`, warm grey, small soft navy dots), with only outlines
  in dark navy; the light fades out through a **dotted halftone edge**. Gold `#FCA311` stays the spot colour; orange
  only for losses. No smooth glow, no bloom (that is the reference channel's signature).
- **Paper grain on the background only**; locked cast drawn crisp on top with correct occlusion (desks/tables in front
  still hide them). Locked fonts (Alfa Slab / Barlow / Special Elite).
- Sample sets: CEO office, trading floor, desk top-down, street (bank / cash advance / pawn / mortgages), kitchen.

## Daytime scenes (locked: style A "printed illustration") - `daytime/`
- Used for **lessons / "your money" parts**; night scenes stay for the story and drama parts.
- The world is a **2-colour print**: navy ink outlines on cream paper `#F6EFE2`, light navy tint `#D6DEEC` under
  shade, **small soft navy halftone dots** `#465C8C` for shading (lightened on the owner's request), solid mid-navy
  for navy objects, **gold `#FCA311` as the only spot colour**. No smooth gradients, no bloom, no green.
- Sunlight = clean cream areas cutting through the dotted shade.
- **Characters stay full-colour and glossy** on top (drawn after the print pass), with a soft contact shadow.
- Our own details instead of the reference channel's: no checkerboard floors (bank = cream marble + gold medallion),
  autumn-gold trees and dried pampas grass instead of green plants.
- Sample sets: living room, kitchen (morning), bank lobby, Main Street, lesson room (whiteboard + counter).
- Animation tip: render each shot's background once as a still, animate characters/props over it.

## Fonts (locked) - `type/`
| Use | Font |
|---|---|
| Number counters | **DSEG7 Classic** (digital); gold for money, orange for losses |
| Titles + chapter names | **Alfa Slab One** |
| Text cards, documents, quotes | **Special Elite** (typewriter, typed word by word, gold cursor) |
| Labels, name tags, sticky notes, place tags | **Barlow Condensed** |

## Script structure (locked) - `.claude/skills/documentary-script/`
- **Template A** for every documentary (money stories, corruption, scams, rackets, fraud): hook (<= 45 s, title at
  ~0:45) -> Ch 1 origin -> Ch 2 the opening -> Ch 3 the plan -> midpoint twist -> Ch 4 the fallout -> Ch 5 your
  wallet -> callback ending. 10 min default, ~1,500 words at 155 wpm.

## Thumbnails (locked) - `.claude/skills/thumbnail-prompt/`
- Made by the owner in an AI image tool from **detailed prompts written at the end of every video** (after render),
  2-3 options per video.
- Every prompt names the locked palette (hex + jobs, no green) and describes **our character style**; real people
  drawn in our style with their signature traits.
- Formula: top text band (white + one gold/orange word), one big expressive face, one glowing story object,
  dark blurred story background, dramatic rim light.

## Not decided yet
- voices + lip-sync, music/sound mood, final channel name, rendering pipeline.
