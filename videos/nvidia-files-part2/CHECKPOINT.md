# CHECKPOINT: The Nvidia Files Part 2, 24 Nov 2026 (read this first, then CLAUDE.md)

Owner: Mukesh Kumar Jha (Dirty Dollar). Strict compliance: follow every instruction and standing rule, no extras.

## State
- Code is at commit tagged `checkpoint-nvidia-p2-ch5-charts`. Script: 91 shots, 61 voiced lines. Narrator is a Kokoro placeholder.
- A full cloud render of the PREVIOUS version exists (6:10, 1080p, transcript match 0.931). Chapter 5 has since been redone and NOT rendered or seen yet.
- Chapter 5 "Why It's a Big Deal for Your 401(k)" changes (this checkpoint):
  1. Legs fix: study set front desk removed; credenza is background; full body always visible.
  2. Music: BEAT_MOOD CH5 = 'suspense' (same bed as ch1-4, no break).
  3. Full-screen explainer charts, no character: n053 (H200 25% cut bar + NOT CONNECTED folders), n054 ($10,000 grid, 6 squares Nvidia = $600, then example dip), n055 (layers: products / customers / government rules). n052 analyst + wall-mounted screen. n056 cards, n057 saver closeup unchanged.
  4. The n054 "EXAMPLE: IF NVIDIA FELL 20%" ($10,000 -> $9,880) is Claude's own illustration, flagged to the owner, not yet confirmed.

## Update 24 Nov 2026 (later)
- Chapter 5 QA fixes (25% CUT label, n054 text overlap, n055 gold box overflow, n052 serious face). n054 20% example: owner said KEEP.
- Full video rendered on the owner's PC (6:10, 1080p30): `out/final.mp4`, `out/captions.srt`. **Owner approved the video.**
  `check` not run on the PC: Parakeet model missing from D:\models (cloud check of the previous version: 0.931).
- All Part 1 + Part 2 PENDING assets LOCKED in ASSET_LIBRARY.md (office workstation marked REMOVED: ng_scenes.py was deleted).
- Next: youtube.md disclaimer question, then thumbnails (ask for reference thumbnails -> 3 prompts).

## Standing rules (do not break)
- Never render (video, stills, contact sheets) without the owner's explicit OK. Ask first.
- After any change ask "save now or later?".
- QA stills are the standing workflow before a full render.
- Audio level is perfect, only measure it. No end screen. Generated assets stay PENDING until the owner approves.
- Reported stamps removed; stamps are gold; Nvidia green (#76B900) for company elements only.
- Script change means regenerate voices.

## Next steps (run in videos/nvidia-files-part2: `python3 ../../.claude/skills/documentary-animator/make_video.py <cmd>`)
1. `git pull`, then `voices` (if voices/ missing), then `qa`. Review chapter 5 stills (n052-n057): legs visible, charts readable, nothing under captions (keep y < 960).
2. Fix what the owner flags, then `render`, `audio` (check music is continuous through ch5), `final`, `check` (aim > 0.9).
3. Deliver to owner. Then: approve PENDING assets (hand_mic, passport, night/study, fund_screen, chip_box, question_card), update ASSET_LIBRARY.
4. Open questions: remove "Not financial advice. Educational..." wording in youtube.md? Thumbnails (ask for reference thumbnails; 3 prompts via thumbnail-prompt skill). Part 1 thumbnail CTR 0.7%.

## Prompt to start Claude Code on the PC
"Read CLAUDE.md and videos/nvidia-files-part2/CHECKPOINT.md. Continue from that checkpoint. Do not render anything until I say OK."
