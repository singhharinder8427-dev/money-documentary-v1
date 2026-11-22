# Checkpoint - 22 Nov 2026 (read this after START_HERE.md)

## Where we are: "The Nvidia Files - Part 1"
Title: "How Nvidia's CEO Ended Up at Dinner With a Suspected Spy". About 10 min, cloud render, no end screen,
a "subscribe for Part 2" card instead.

- Script is locked: `videos/nvidia-files-part1/script.json` (copied into `videos/nvidia-files-part1-draft/`).
  "U.S." is now "United States" everywhere.
- Shots are fully coded: `videos/nvidia-files-part1/shots.py` (~173 shots: hook, CH1-CH5, twist, ending, subscribe card).
- The draft runner is `videos/nvidia-files-part1-draft/` (its `shots.py` wraps the main one; voices/ and out/ are not in git).
- The v2 preview was rendered (10:02, transcript match 0.929). The owner's notes on it are ALL fixed in code:
  the phone in Jensen's hand, calendar page flips, ring sound, the $4T chart in the Nvidia office, the Nvidia logo,
  the Megaspeed desks, gold stamps, the United States pronunciation, the 29 QA items, and props built properly.
- Last fix (not yet rendered): the ring, pop, chapter-card boom and card typing sounds are quieter.

## Next steps
1. **Full re-render, owner's OK needed (cloud or PC, ask again).** The voices changed, so do all of it:
   delete `videos/nvidia-files-part1-draft/voices/` and `out/shot_*.mp4`, then
   `make_video.py voices -> qa (follow QA_CHECKLIST.md) -> render -> audio -> final`.
2. **ElevenLabs narration:** when the owner sends it, put it at `videos/nvidia-files-part1-draft/narration.mp3`
   (narrator only; the character dialogue clips stay Kokoro), delete `voices/`, rerun voices, then a full render, audio and final.
   The text he records from is `videos/nvidia-files-part1/narrator_clean.txt`.
3. **PENDING assets** waiting for approval cards (see `ASSET_LIBRARY.md`): nvidia_logo, phone_flat, hair_dryer,
   handcuffs, scooter_rider, paper_in_hand, phone_in_hand, the nvidia_office / newsroom / desk_clean sets, and the new sounds.
4. Open idea, not confirmed: make the Nvidia logo on the $4T screen bigger.
5. Later: Part 1 thumbnails (ask for reference thumbnails, then 3 prompts), and check the unconfirmed facts in `sources.md`.

## NEW LOCKED LOOK for new assets (22 Nov 2026, later the same day)
- Every new place / office / street / company / prop scene: flat 2D in real colours, then `looks.real_night`
  (CLAUDE.md 3d, BRAND.md). First asset: `night/nvidia_hq` (Nvidia HQ Endeavor entrance). Reference stills in `branding/`.
- Next idea: use `night/nvidia_hq` in Part 1 where the story is at Nvidia, and remake upcoming new places this way.

## Rules learned this session (also written into CLAUDE.md / QA_CHECKLIST.md)
- QA follows `QA_CHECKLIST.md` every time, before and after a render.
- After ANY script text change, delete `voices/` first, because the voices step reuses old clips.
- Every real company gets a rough 2D logo drawn in code, in its brand colours.
