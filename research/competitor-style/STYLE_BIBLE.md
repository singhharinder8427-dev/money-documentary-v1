# Style bible for original money documentaries

## The visual approach

Open with one impossible-to-miss picture of the story's main pressure. Make the audience understand the situation from silhouette, scale and color before the explanation arrives. The spy opener pairs the green-lit object with an amber dinner at 00:00, then makes the same green the point of interest on a global map at 00:02–00:04. The Jensen opener makes growth a stack against a skyline at 00:04–00:06.6. The AI story returns from a tight character crop to a balloon wide at 00:03.4–00:05.0. The crash story puts a falling-market number next to a giant chip at 00:02.8–00:04.0. Evidence for each: hook_survey_001–002 in its video folder.

Build each section in a cycle: an establishing view locates the scene, a closer shot directs attention, a prop insert makes the claim concrete, and a black phrase card creates a pause at a change of idea. Vary the format when the viewer's question changes. An overhead document handles evidence, a diagram handles relationships, and a character reaction handles stakes. Give one detail motion priority while the rest of the frame continues quietly. Return to a recognizable motif near the end and change its state. See the [comparison](CROSS_VIDEO_COMPARISON.md) for source references for these patterns.

## Numbers for a first Remotion pass

| Parameter | Observed reference | Suggested starting point |
|---|---|---|
| Frame rate | All four sources are 30 fps. See meta.json. | 1920×1080 at 30 fps |
| Editorial cadence | Mean intervals between >0.25 candidates are 3.06–3.67 s. These are detector intervals. The verified Jensen hook includes 1.43 s, 2.63 s, 2.60 s and 2.40 s shots. | Plan 60–120 frame shots, with shorter evidence inserts and longer explanatory holds |
| Handwritten narrative cards | 48 sampled frames from partial to complete in spy hook 00:04.2–00:05.8, 60 in Jensen 00:01.6–00:03.6, 66 in AI 00:01.0–00:03.2 | Start at 112–128 CSS px in Caveat or Kalam and size to about 95–100 px of visible glyph height at 1080p. Use near-white #FAF9F5, at least 8% horizontal safe area, and vertical center. Reveal within a fixed text block over 40–65 frames, then hold 8–16 frames. Glyph height evidence: Jensen frame 8818, AI frame 19447, Crash frame 16548 |
| Lower thirds | Spy portrait labels build in around 00:06.6–00:07.0 and 00:09.2–00:09.6 | 32–40 px Barlow Condensed or Archivo Narrow, neutral text and a small lime rule. Slide 12 px and fade in over 10–12 frames |
| Camera | Crash crop grows head approximately 1.3× between 00:05.8 and 00:06.0. Exact transform uncertain. | Slow push 1.05→1.12 over 75 frames with cubic ease-in-out. For information emphasis, use a hard cut from 1.00 to 1.25 or a 6-frame punch |
| Parallax | Distinct depth groups are visible in Jensen 00:00–00:01.4 and spy 00:00–00:01.8. Source layer speeds uncertain. | Over 75 frames move rear 12 px, subject 26 px, near prop 42 px. That is 4.8, 10.4, 16.8 px/s respectively. Enable edge overscan |
| Shake | Independent shake amplitude and frequency remain uncertain | Optional punctuation on a physical impact, 6 px peak at 8 Hz decaying to zero in 10 frames. Keep captions outside the shake parent |
| Transitions | Spy whip is blurred at 00:02.0 and resolved by 00:02.4. AI whip is smeared at 00:08.6–00:08.8 and resolved by 00:09.0 | Hard cut uses 0 overlap frames. Start whips at 12 frames, with 20–24 px horizontal smear at midpoint |
| Counters | Crash counter settles by 00:04.0 after the first readable number at 00:02.8, approximately 36 frames | Ramp over 36 frames with out-cubic easing. Hold the target for at least 20 frames |
| Full mix | −14.3 to −14.6 LUFS integrated, 2.2–2.4 LU range, −3.0 to −1.8 dBTP across four files. See loudness.txt | Start near −14.5 LUFS integrated and a −2 dBTP ceiling. For your own stems, start the bed 14–18 dB below the voice in active narration, with a 4–6 dB duck over 4 frames and release over 12 frames. Check by ear and meter. Reference stem levels are uncertain |

## Color families for original sets

| Scene role | Design swatches | Visual evidence |
|---|---|---|
| Intimate suspense | #171320, #7B182B, #FFD791 | Warm face, wine-red seat and black edges in spy 00:00 |
| Night technical | #0B1830, #192846, #8CF53B | Spy map 00:03.6 and crash chip 00:02.8 |
| Public optimism | #251841, #C55A83, #F5A767 | Jensen skyline 00:04.2–00:06.6 |
| Speculation and scale | #0B1830, #32DBEE, #F0D696 | AI hook 00:04.2 and AI ballroom around 19:30 |
| Loss signal | #27131D, #80242F, #E14B57 | Crash counter 00:04.0 and crash exchange around 10:40 |

Keep the strongest hue local to its source and the strongest edge contrast near the fact being explained. These swatches approximate observed color relationships for new scenes.

## Code

[The effects catalog](EFFECTS_CATALOG.md) contains copyable Remotion building blocks for layered drift, practical light, whip, text reveal, chart stagger, facial beats, counters, and shake.

## Scene-building checklist

- Choose a clear subject and a narrative job for the shot.
- Give the frame a rear set, subject plate, and a foreground element where it supports scale.
- Place a motivated light and check that the title, prop, or face remains the highest-priority read.
- Animate one primary action, one secondary cue and a restrained background accent. Time them at different frames.
- Key the cut or visual payoff to a marker in the original script.
- Check visibility at 25% size. Verify flat and animated states are equally legible.
- Give the voice room and audition any music or accent against the finished edit.

## Ten changes from a flat framed backdrop

1. Stage objects in front of the subject to establish occlusion.
2. Give each distance plane a deliberate movement speed.
3. Use pools of light to direct attention to the active object.
4. Anchor scale with recognizable small things beside the centerpiece.
5. Switch shot size when the emotional question changes.
6. Put evidence on objects characters can hold or manipulate.
7. Reveal one figure at a time and preserve the comparison baseline.
8. Give a held character a small, timed expression change.
9. Insert a clean black card at a meaningful narrative turn.
10. Reintroduce older settings and props in a visibly changed state.

## Five quick wins

1. Add a local amber light and a cool rear layer to one existing set.
2. Put one foreground object on a separate plate and give it a slightly faster drift.
3. Replace one exposition hold with a 1–2 second evidence insert.
4. Introduce one number with a short settling animation and a readable hold.
5. Start and end a section with the same original motif in two different states.

