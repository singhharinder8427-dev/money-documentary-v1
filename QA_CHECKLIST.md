# QA checklist - the owner's standard (set 22 Nov 2026, Nvidia Files Part 1)

This is HOW we do quality control on every video, every time, before the owner sees it. The owner watches frame by
frame and notices every small detail; Claude must catch those details first. "It renders" or "it is framed" is not QA.
Run it on the QA sheets (`make_video.py qa`, 3 frames per shot with the real camera) AND, after a render, on frames
pulled from the finished video, plus a speech-to-text pass over every voice clip. Log every finding in a numbered list,
fix them all, re-check the changed shots, then report.

## 1. Does the picture show what the line SAYS? (read every line next to its frame)
- Every object or action the line mentions is visible: "on the phone" -> a phone IN the hand; "boxes" -> boxes;
  "map / route / Malaysia" -> a real map, not empty ovals; a name tag -> that person is on screen.
- Every prop is HELD or RESTING on something: nothing floats (phones, hair dryers, papers, folders). Phones lie flat on
  tables. Furniture stands on the floor with legs: desks have tops, legs and height; monitors sit on stands on the desk.
- Vehicles have drivers; tools have hands; documents have a desk or a hand under them.

## 2. Does every face match the line's emotion?
- Talking mouths must follow the emotion: no grin on a threat, bad news, a question or a shock line.
  Angry / suspicious -> flat or frown + brows down; shocked -> o-mouth + wide eyes; worried -> flat + brows up.
- Characters who look alike in outfit must not be confused (e.g. an investor must not wear the inspector's hi-vis vest).

## 3. Does every movement have a sound?
- Calendar / page flips -> a page-flip sound per page. A ringing / vibrating phone -> buzz synced to each vibration +
  ringtone. Picking up a phone -> click. Walking -> footsteps. Doors -> slam / knock. Stamps -> thud. Counters -> ticks.
- Places have room sound: data center hum, restaurant / crowd murmur, conveyor rumble, surveillance static.
- List shots with no SFX at all and justify each (dialogue close-ups and cards are fine).

## 4. Brand and colour
- Every stamp is GOLD (never white / pale / navy). Orange only for losses / danger. No green except flags and real
  company brand colours (rule 3b). Real companies show a simple rough 2D logo in their colours (rule 3b).
- Night chapters stay night: a day-look set in the middle of a night chapter needs a reason.

## 5. Text, numbers and labels
- No text overflows its box (calendar years, mastheads, plates, stamps, tags) or the frame; nothing hides under the
  caption bar (bottom ~120 px) or at the frame edges after the camera zoom (check START and END frames).
- Labels read in the right order ("down more than 5%", not "-5.0% MORE THAN"). No duplicate labels in one shot.
- Typed cards finish typing by about half the line so the viewer can read them; the typing never trails the voice.

## 6. Repetition and immersion (the owner dislikes repeated backdrops)
- Count shots on the plain framed navy backdrop; keep it for typed quote cards and a few big beats only. Documents go
  on desks / in hands, counters and charts on screens in real rooms, newspapers on a newsroom desk.
- No more than 2 near-identical shots in a row (same board, same set, same angle). Vary angle or cut to a small scene.
- Use the map / explainer modules where the story moves between countries or companies (only where needed).

## 7. Props and assets
- Every new prop the story needs is BUILT as a proper prop in `engine/props.py` (not drawn ad hoc inside a shot),
  given one clear name, previewed to the owner, and listed in `ASSET_LIBRARY.md` (rule 3c).

## 8. Voice (speech-to-text on every clip; Claude cannot hear)
- Run Parakeet on every clip and diff with the script: flag mispronounced names, words that come out as a rude or wrong
  word ("hit" heard as something else), run-together phrases, and any skipped (OOV) words. Fix by rewording,
  MANUAL_LEX entries, or re-generating. Numbers / dates written as digits by the ASR are not errors.
- After ANY script text change, delete the `voices/` folder before `make_video.py voices`: it reuses clips already in
  clips.json, so changed lines would keep the OLD audio (this is how "U.S." survived into version 2).
- Sound levels: phone ring, pops, chapter boom and card typing stay soft under the voice (owner, 22 Nov).

## 9. Report format
Numbered list grouped by: faces/acting, props, graphics, repetition, sound, voice. Each item: what is wrong, which shots
(ids), the fix. Then fix everything in one pass and re-run QA on the changed shots before asking to render.
