# Checkpoint - 22 Nov 2026 (read this right after START_HERE.md)

## 1. Where we are
- **"The Nvidia Files - Part 1"** ("How Nvidia's CEO Ended Up at Dinner With a Suspected Spy", ~10 min, cloud render,
  no end screen, "subscribe for Part 2" card) - **the owner declared Part 1 done (22 Nov 2026).**
  - Script: `videos/nvidia-files-part1/script.json` (copy in `videos/nvidia-files-part1-draft/`). Shots: `videos/nvidia-files-part1/shots.py` (~173).
  - The last preview render (v2) was made BEFORE the final fixes (quieter sounds, "United States", the new real-colour sets). If the
    owner wants a final file with everything: ask first (cloud or PC), then delete `videos/nvidia-files-part1-draft/voices/` and
    `out/shot_*.mp4`, and run `make_video.py voices -> qa (QA_CHECKLIST.md) -> render -> audio -> final`.
  - ElevenLabs narration (if the owner sends it): `videos/nvidia-files-part1-draft/narration.mp3`, narrator only - character
    dialogue stays Kokoro. The text he records from: `videos/nvidia-files-part1/narrator_clean.txt`.
  - Still open for Part 1: thumbnails (ask for reference thumbnails -> 3 prompts with the `thumbnail-prompt` skill); check the
    unconfirmed facts in `videos/nvidia-files-part1/sources.md`.
- **Next video:** Part 2 (or a new story) - start with CLAUDE.md step 2 (script / length / PC-or-cloud questions).

## 2. The NEW LOOK for every new asset (locked 22 Nov 2026) - CLAUDE.md 3d
1. Draw the real place / office / street / company building / prop scene in **flat 2D with its REAL colours**, matching the real
   one (reference photos give layout + colours; draw fresh in code, never paste or trace a photo). Code goes in
   `engine/sets_src/real_places.py` as `draw_<name>(c)` + `<name>_night()` (light pools, lamp glows, logo colours to keep, which
   colours are light sources).
2. `looks.real_night` puts our brand on it: navy night sky with dots + stars, unlit parts on our 4 navies with a hint of real
   colour, light only from real sources, halftone dots in shadows, gold lamp heads, exact logo colours, **dark-navy dotted
   vignette from the BOTTOM edge only**, paper grain.
3. Register in `engine/sets.py` with `real=` + `night=` (+ `real_fg=` for tables in front of actors), preview with a character
   in front, owner approves, add to `ASSET_LIBRARY.md`, ask "save now or later?".
- Sets already in this look: `night/nvidia_hq`, `night/sg_street`, `night/megaspeed`, `night/diner93`, `night/restaurant`,
  `night/datacenter`, `night/nvidia_office`, `night/newsroom`, `night/desk_clean`. The old navy versions (`ng_scenes.py`) were deleted.
- The Ponzi-era night-print sets (`night/office`, `night/street`...) still work and stay LOCKED.
- Reference stills: `branding/real_night_look_step1_flat.png` (step 1) and `branding/real_night_look_nvidia_hq.png` (step 2,
  made with the earlier round vignette - the locked vignette is bottom-only).

## 3. Everything learned in this project (also FIXES.md 27-38, QA_CHECKLIST.md, CLAUDE.md)
- **QA every time** with `make_video.py qa` + `QA_CHECKLIST.md`, before a render and on the finished video. The owner checks every
  small detail: picture matches the line, props held / grounded, faces match the emotion, every movement has a sound, stamps gold,
  no text overflow, no repeated backdrops, the camera never crops a graphic, speech-to-text on every voice clip.
- **Sound levels:** ring, pops, chapter boom and card typing all stay soft under the voice.
- **Voices:** write "United States", not "U.S."; delete `voices/` after any script change; espeak-ng must be installed (Kokoro
  drops words without it).
- **Props** are built in `engine/props.py` and listed in the library; never drawn ad hoc inside a shot.
- **Real companies:** brand colours + a rough 2D logo drawn fresh (Nvidia green eye `#76B900`).
- **Synopsis hook** before chapter 1 (like Ponzi) builds suspense - keep doing it.
- **Use library modules** (maps, flags, calendars...) where the story fits, never many at once.
- **Owner workflow:** collect the full feedback list before changing anything; PowerShell commands one per block; never save or
  render without the owner's OK.

## 3b. Research to apply to the NEXT video (23 Nov 2026)
Read `research/APPLY_NEXT_VIDEO.md` (owner's competitor-style research, files in `research/competitor-style/`). Not applied to Nvidia Files Part 2. Nothing built, nothing rendered.

## 4. On the owner's PC
```
cd D:\money-documentary-v1
git pull
claude
```
First message to Claude Code: "Read CHECKPOINT.md and continue."
