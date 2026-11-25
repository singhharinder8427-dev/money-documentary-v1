# CHECKPOINT: "The $1.7 Trillion Morning That Left OpenAI Behind" - 24 Nov 2026 (read after CLAUDE.md)

## State
- Topic from search demand (TLDR Business video, YouTube autocomplete "is openai in trouble"). Option B (follow the money of the
  Anthropic IPO morning). Owner choices: ~4-5 min, render on the owner's PC, title above, NO wallet chapter, one continuous film,
  fade chapter cards, subscribe ending line (n055), NO end screen.
- Script: script.json n001-n055 (owner: "great script"). Sources + "not checked" list in sources.md. Written by Claude (made by
  Anthropic): conflict of interest flagged; only sourced facts.
- Assets LOCKED 24 Nov (ASSET_LIBRARY.md): living backgrounds (engine/ambience.py, opt-in), company marks (engine/logos.py) +
  chest badges (kit spec `chest=`), cast dario / daniela / altman / trader2, sets night/nasdaq_tower, night/nasdaq_studio,
  night/openai_hq (engine/sets_src/real_places_ipo.py), props (engine/props_ipo.py), widgets.chapter_fade.
- Reference photos (Wikimedia Commons) are kept OUTSIDE the repo: D:\money-documentary-refs\trillion-morning.
- Shot plan: shot_plan.md (69 pictures) - written, waiting for the owner's OK to code shots.py. Nothing rendered except previews.

## Next (25 Nov 2026)
- DONE: shots.py coded + QA'd; voices for all 55 lines (narrator = Kokoro placeholder); contact-sheet fixes (OpenAI sign on top
  of the building, captions above framed-card borders, list held, etc.); living-background sounds (ambience.sound_events,
  synced to the pictures) + belt rumble / subscribe pop; test mix out/mix.wav (254 s).
- PC setup: use `py -3.12` (packages installed there).
1. Narrator = Kokoro (owner, 25 Nov), +2 dB in this video only (script.json "narrator_gain": 1.26). No ElevenLabs file needed.
2. DONE 25 Nov: full qa + fixes, rendered on the PC -> out/final.mp4 (4:14, 1080p30). Speech check NOT run: the PC has no ASR model (D:modelssherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8). Next: owner watches -> youtube.md -> thumbnails.
3. Open: Daniela Amodei reference photo; OpenAI wordmark font for cloud renders; re-check the CNBC "filed in June" report.
