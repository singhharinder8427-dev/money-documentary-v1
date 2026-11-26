# Dirty Dollar - standing instructions (owner's locked workflow, set 21 Nov 2026)

These rules apply to EVERY new video and every time this repo or one of its skills is called. The owner should never
have to repeat them. Details of the look live in `BRAND.md`; the handover is `START_HERE.md`.

## 0. Repo isolation (hard rule)
- The ONLY repository to read-write, commit or push is **`singhharinder8427-dev/money-documentary-v1`** (branch `main`).
- Never touch any other repo (`-google`, `-codex`, `harry-shorts`, `claude-cartoon-engine`, ...), even if attached.
  Exception (owner, 22 Nov 2026): when the owner asks, Claude may READ from `singhharinder8427-dev/money-documentary-v1-codex`
  (read-only clone) to import graphics/code into `money-documentary-v1`. Never write, commit or push to the codex repo.
- Still never save / commit / push without the owner's OK: after every change ask **"save now or later?"**

## 1. FIRST STEP, every time the repo or a skill is called: read everything
Before answering anything, read the whole repo so no context has to be repeated. Read, in this order:
1. `START_HERE.md`, `BRAND.md`, `README.md`, this file.
2. Every `.claude/skills/*/SKILL.md` and `documentary-animator/FIXES.md` (owner feedback history 1-38).
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
4. **Language:** "Should the audio be in Hindi or English?" (ask EVERY new project, at topic selection). English = the existing
   pipeline (US audience, this channel). Hindi = the Hindi pipeline, for the owner's separate Hindi-only channel (rule below).

**Hindi videos (standing rule, owner-set 26 Nov 2026):**
- `script.json` gets `"lang": "hi"`. Every line has `say` (the spoken words in Devanagari, natural spoken Hindi, English
  loanwords as people really say them) and `text` (the same line in **Hinglish, Roman script**). `text` drives the captions.
- **All numbers on screen are in English digits and English format** ($1.7 trillion, 24 Nov, 45%) - in captions, cards,
  counters, charts and tags. Never Devanagari digits. Cards, counters, chart labels and name tags stay in English.
- **Captions are Hinglish** (Hindi words in Roman letters mixed with English, e.g. "Ek hi subah mein $1.7 trillion"),
  never Devanagari script.
- **Chapter pages and title cards are Hinglish too** (owner, 26 Nov 2026), not English. Numbers stay English digits.
- Voices: narrator = the owner's ElevenLabs Hindi file (Kokoro `hm_omega` is only the placeholder); dialogue = Kokoro's
  Hindi voices (`voices.py HINDI_VOICES`); pronunciations come from espeak-ng `hi`. Speech check = Whisper
  (`D:\models\faster-whisper-large-v3-turbo`), because Parakeet is English only.
- The search-demand rule applies to Hindi too: check what Indian viewers search (Hindi / Hinglish search terms) and write
  the title, description and thumbnail text in Hinglish.
**Search-demand topics (standing rule, owner-set 24 Nov 2026):** from now on every video is about what people are actively
searching for. When finding or checking an idea, show the owner the search evidence first (Google Trends, YouTube search
suggestions, recent news volume, competitor videos' views) and pick the topic and title wording people actually type.
If the owner has a script: fact-check/adapt it into Template A (`documentary-script` skill). If not: research + write it
with the `documentary-script` skill (3 outlines -> full script -> sources). Wait for the owner to lock the script.

**No wallet chapter - one continuous video (standing rule, owner-set 24 Nov 2026):** NEVER add a separate "your wallet" /
lesson chapter (Template A Ch5, day-print lesson sets, red-flags board). Every video is one continuous story from the first
frame to the last, motion never stops, the viewer never looks away; any money point is woven into the story itself.
This overrides Template A, BRAND.md and the skills wherever they mention Ch5 / the lesson part.

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
  office...), in the real-colour night look (rule 3d). Show the current set library so reuse vs new is the owner's choice.
- **Props** the story needs (documents, evidence, signs, vehicles).
The library keeps growing; never reuse the same office/street for every story.

## 3b. Company brand colours (standing rule, owner-set 21 Nov 2026)
Wherever a real company appears (signs, chips, certificates, cards, screens, thumbnails), use that company's **original
logo / brand colours** (e.g. Nvidia green `#76B900`), not our navy/gold swap. This is a second owner-approved exception to the
"no green" rule, next to national flags (see `BRAND.md`). It applies to company-specific elements only; characters, places
and everything else stay in the locked palette. Logos (owner, 22 Nov 2026): for EVERY real company draw a simple, rough 2D version of its logo in our flat style
(e.g. Nvidia = a green eye-like swirl mark + the name), so the company is recognisable at a glance. Draw it fresh in code -
simplified shapes only, never a traced or pixel copy of the real artwork. Check each company's real colours from its official brand page before using them, and list them in
`videos/<name>/sources.md`.

## 3c. Asset library (standing rule, owner-set 22 Nov 2026)
Every approved character, place (office, street, room...), prop, animation or widget is saved in `ASSET_LIBRARY.md` under ONE
clear name with its code key, source video and status, so later videos can reuse it by name. When the owner approves an asset:
lock it in code (`cast.py` / `sets.py` / `props.py` ...) AND add or update its row in `ASSET_LIBRARY.md` in the same step,
then ask "save now or later?". Assets not yet approved are listed as PENDING. At step 3 of every new video, show the library
first so the owner can choose reuse vs new. Never rename or change a LOCKED asset without asking.
Imported codex assets (see the bottom of `ASSET_LIBRARY.md`) are used ONLY when the story needs them, never many at once, and each is
restyled to our print look (with a preview for the owner) the first time it is used.

## 3d. NEW ASSETS: real-colour night look (hard rule, owner-locked 22 Nov 2026)
From now on EVERY new place, office, street, company building, room and prop scene is made in this exact way
(reference still: `branding/real_night_look_nvidia_hq.png`, code: `engine/looks.py real_night` + `engine/sets_src/real_places.py`):
1. **Draw the real place in flat 2D with its REAL colours** - same building / layout / mood as the real one (use reference
   photos for layout and colours): green grass stays green, glass, concrete, wood and the company's own colours stay as they
   are. Simple flat shapes, thin dark outlines, no gradients, no photo textures. Drawn fresh in code - never a traced or
   pasted photo. Company logos as the rough 2D version from rule 3b.
2. **Put our brand on it with `looks.real_night`**: dark navy night sky with halftone dots + a few stars; everything unlit
   goes onto our 4 night navies with only a hint of its real colour; only real light sources (lamps, lobby, windows, a
   sign uplight) keep full colour and spill light; halftone dots in the shadows; lamp heads in brand gold; logo colours
   kept exact; a dark-navy dotted vignette rising from the BOTTOM edge only (`REAL_VIGNETTE = 'bottom'`, owner-locked
   22 Nov 2026 - no round vignette); paper grain.
3. Register it as a set with `real=` + `night=` in `engine/sets.py` (see `night/nvidia_hq`), show the owner a preview with
   a character in front, then add it to `ASSET_LIBRARY.md` (rule 3c).
The Ponzi-era night-print sets stay LOCKED and reusable; every set made for The Nvidia Files was redrawn in this look and the old
navy versions deleted. New assets ONLY use this look. Do not go back to monochrome line-art
recreations for new places.

## 4. Shot plan (the "Ponzi standard")
Plan the shot list like `videos/ponzi-full`: a hook that starts mid-action, a new picture every 2-3 s, a visual beat
(card / counter / stamp / chart / dialogue / place jump) every 20-30 s, moving camera, varied angles (no repeated wides),
story-specific animation (`anim`: hand slams, stamps, newspapers, calendars, police car + spotlight), the red-flags
board in the lesson part, the creative quality check (3 frames per shot, "would adding something make it more
engaging?"). Match the *rhythm and engagement techniques*, not the Ponzi timing or content.
Then ask: **"Do you want the end screen at the end of this video, or skip it?"** (ask EVERY project).
**Name + role tag (standing rule, owner-set 22 Nov 2026):** every time an important character appears (first appearance, and
again when they return after a long gap), show their name and role in a lower-third tag, exactly like the Ponzi video
(`widgets.lower_third(c, name, role, u)`, e.g. `'Charles Ponzi', 'Boston, 1920'`). Real people get their real name and role;
Alice Huang is always tagged "alleged"; generic dramatised roles get "THE <ROLE>". Put the tag in each shot's `hud` and
record it in the shot hint. Never skip it and never wait for the owner to ask.

("Shorts" in the owner's point 3 means SHOTS - the shot plan - not YouTube Shorts.)

## 4b. Quality check BEFORE any render (hard rule, owner-set 22 Nov 2026)
After the shots are coded and before asking to render: run `make_video.py qa` (3 frames per shot, real camera), review every sheet against SKILL.md step 5, fix, re-check changed shots, and tell the owner what was found.
**How:** follow `QA_CHECKLIST.md` EVERY time (owner's standard, 22 Nov 2026): picture matches the line, props held / grounded, faces match
the emotion, every movement has a sound, stamps gold, no overflow, no repeated backdrops, new props built properly, speech-to-text on
every clip. Log findings as a numbered list, fix all, re-check. After a render, repeat it on frames from the finished video. The QA stills are part of the owner's standing workflow; the video render still needs consent.

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
