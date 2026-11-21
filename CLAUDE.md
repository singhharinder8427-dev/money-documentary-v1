# Dirty Dollar - standing instructions (owner's locked workflow, set 21 Nov 2026)

These rules apply to EVERY new video and every time this repo or one of its skills is called. The owner should never
have to repeat them. Details of the look live in `BRAND.md`; the handover is `START_HERE.md`.

## 0. Repo isolation (hard rule)
- The ONLY repository to read-write, commit or push is **`singhharinder8427-dev/money-documentary-v1`** (branch `main`).
- Never touch any other repo (`-google`, `-codex`, `harry-shorts`, `claude-cartoon-engine`, ...), even if attached.
- Still never save / commit / push without the owner's OK: after every change ask **"save now or later?"**

## 1. FIRST STEP, every time the repo or a skill is called: read everything
Before answering anything, read the whole repo so no context has to be repeated. Read, in this order:
1. `START_HERE.md`, `BRAND.md`, `README.md`, this file.
2. Every `.claude/skills/*/SKILL.md` and `documentary-animator/FIXES.md` (owner feedback history 1-26).
3. The engine: `.claude/skills/documentary-animator/make_video.py`, all `engine/*.py` (`core kit cast actor sets looks
   widgets anim shots timeline render audio voices captions`), `engine/sets_src/*.py`, `template/`.
4. Past videos, especially `videos/ponzi-full/` (`script.md`, `script.json`, `shots.py`, `voice_script.md`,
   `sources.md`, `youtube.md`, `thumbnails/make_thumb.py`) and `videos/ponzi-test/`: how the script is written, how
   shots are planned and how clips are handled.
5. The look-development folders (`characters/`, `environments/`, `daytime/`, `branding/`, `type/`) - code and docs only.
Skip binaries (images, fonts, audio, video). Then continue; do not summarise all of it back to the owner.

## 2. New project - start by asking (use the question tool, one message)
1. **Script:** "Do you already have a script, should I research and write one, or do you want me to find the idea first?"
2. **Length:** "How long should this video be?" (ask EVERY video; never assume 10 min).
3. **Render:** "Render on your Windows PC or in the cloud?" (ask EVERY new project; asking is not consent to render, see 5).
If the owner has a script: fact-check/adapt it into Template A (`documentary-script` skill). If not: research + write it
with the `documentary-script` skill (3 outlines -> full script -> sources). Wait for the owner to lock the script.

**Dialogue moments (standing rule, every script):** like the Ponzi video, about a quarter of the lines are short
dialogue moments (each <= 10 s, 2-4 lines, two speakers, usually ending on a sting or a joke) that turn a fact into a
scene. Use generic roles (analyst, inspector, clerk, trader, director, saver...) marked `"dramatised": true`. Real people
only speak short real quotes or paraphrases of documented exchanges; never invent claims in their mouths. Never skip
this and never wait for the owner to ask.

## 3. When the script is final: re-read the engine, then plan the assets BEFORE any shot is coded
Re-read `engine/` + `videos/ponzi-full/shots.py` + `FIXES.md` against this script, then tell the owner exactly which new
assets are needed to make the video engaging, and build them first (references -> design in our style -> owner
approves -> lock into the library):
- **Characters.** A documentary about a real person needs that person as a 2D character in our brand kit, built from their
  real traits (face cut, hair, facial hair, glasses, build, signature outfit/props), locked in `REAL` in `engine/cast.py`
  and used as the main character in the video AND the thumbnail. Also every role character with their
  trademark attire/props: e.g. a judge in robes with a gavel and court bench, police officer in uniform, teller, reporter.
- **Places.** Every story-specific location the script needs (cafe, shop, airport, police station, bus stand, courtroom,
  office...), in the locked night/day print look. Show the current set library so reuse vs new is the owner's choice.
- **Props** the story needs (documents, evidence, signs, vehicles).
The library keeps growing; never reuse the same office/street for every story.

## 4. Shot plan (the "Ponzi standard")
Plan the shot list like `videos/ponzi-full`: a hook that starts mid-action, a new picture every 2-3 s, a visual beat
(card / counter / stamp / chart / dialogue / place jump) every 20-30 s, moving camera, varied angles (no repeated wides),
story-specific animation (`anim`: hand slams, stamps, newspapers, calendars, police car + spotlight), the red-flags
board in the lesson part, the creative quality check (3 frames per shot, "would adding something make it more
engaging?"). Match the *rhythm and engagement techniques*, not the Ponzi timing or content.
Then ask: **"Do you want the end screen at the end of this video, or skip it?"** (ask EVERY project).
("Shorts" in the owner's point 3 means SHOTS - the shot plan - not YouTube Shorts.)

## 5. Never render without consent
- Never start ANY render (video, YouTube Shorts, stills, contact sheets, test frames) without the owner's explicit OK
  for that render. Build assets and shot code first, then ask.
- The PC/cloud answer from step 2 decides where; confirm it again at the moment of asking to render.

## 6. Thumbnails (final stage)
When the video is finished, ask the owner for **reference thumbnails**, then deliver **3 different variations** as
thorough, ready-to-use prompts (the `thumbnail-prompt` skill): brand kit applied (palette, character style, Alfa Slab
headline), the real characters/props/places of THIS video, composition engineered for click-through. Claude knows the
whole script and shot plan, so each prompt is specific and truthful. Say which to test first and why.

## 7. Working style
- Owner is not a developer: PowerShell commands one per code block, step by step. Owner is in India (IST).
- Listen first when feedback comes; collect the full list before changing anything. Keep usage low.
