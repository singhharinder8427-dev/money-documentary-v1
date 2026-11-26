# Checkpoint - Trillion Morning HINDI (26 Nov 2026, evening IST)

Video 1 for the owner's Hindi channel = Hindi version of `videos/trillion-morning`. Nothing rendered yet.

## Done
- `script.json`: `"lang": "hi"`, `"max_pause": 0.3`; every line has `say` (Devanagari) + `text` (Hinglish captions, Rs amounts
  as ₹ with English digits). Narrator lines = the owner's RE-RECORDED script (rupees, rewritten wording), transcribed from
  `narration.mp3` (ElevenLabs Viraj, 5:49). `voice_script.md` = narration as recorded. `text_en` keeps the English line.
- `shots.py`: Hinglish chapter pages (Bagaawat / Palti Baazi / Pehle Paisa Kisko? / Agli Subah), title "₹158 LAKH CRORE WALI
  SUBAH" / "JIS DIN ANTHROPIC PUBLIC HUI", every $ amount -> ₹ (rate ~93, as the owner used): counters in ₹ CRORE / LAKH CRORE,
  price tags ₹7,700 (range ₹6,500-7,250), ₹10,400, +₹2,700, ₹7,900, fund grid per ₹1 lakh -> ₹80. Card gold words updated.
- Engine: `kit.mw/ds` draw the ₹ sign with a system font (Barlow / Special Elite have no ₹) - used by widgets.text, text_card,
  counter, captions, kit.label. `voices.tighten` + `max_pause` shorten pauses inside narration lines. Splitter matches
  letter-by-letter (digits vs spelled numbers no longer shift the cuts). Hindi Whisper: VAD, model loaded once, gap re-transcribe
  (Whisper skipped 5:27-5:36). HINDI_VOICES: two traders get different voices.
- Dialogue (Kokoro Hindi) checked; English words written in Latin for the voice (OpenAI, open, list); n036 "Saat signature."

## Next (in this order)
1. voices.py `words_with_times` (Hindi): cap each word's end at the next word's start (a 9 s "ल" word at 5:27 can push the
   n053/n054 cut). Then `rm -rf voices` + `make_video.py voices`; check n054 is ~4 s and n055 ~13 s, speech-check every clip.
2. Long cards: n041 (24 words) and n049 (~40 words) are too long for a typed card - give them a short card text; n049 is a
   14 s line, add a second picture.
3. `make_video.py qa` + QA_CHECKLIST (every caption's pacing, typewriter sound = typing, ₹ labels fit their boxes/tags).
4. Ask the owner before rendering (PC). Then the Hinglish youtube.md.
- Temp files in this folder (words.json, silences.json, out_transcript.txt) are not saved.
