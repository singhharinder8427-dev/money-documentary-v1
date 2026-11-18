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

## Backgrounds (approved: "mesmerizing") - `environments/`
- Moody night scenes: navy darkness with light pools, lamp cones, glows, bloom, vignette.
- **Paper grain on the background only.**
- Note: the five sample images still show the earlier round-head characters; the final character style is in `characters/`.

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
- daytime scenes for lessons, voices + lip-sync, music/sound mood, final channel name, rendering pipeline.
