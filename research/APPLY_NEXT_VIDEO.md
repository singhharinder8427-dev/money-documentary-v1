# Apply to the NEXT video (owner decision, 23 Nov 2026)

Source: owner's research on four similar channels (files in `research/competitor-style/`). Part 2 of The Nvidia Files stays as planned
(shot_plan.md unchanged). Start applying these when the next video starts. NOTHING here is built yet and nothing has been rendered.

Caveats: the research is from still frames + a cut detector, no transcript, no retention data; the ranking is the researcher's judgment.
It is a technique study. Do not copy another channel's compositions (one reference video covers the same Nvidia/Alice Huang story).
Keep our brand: gold accent (green only for real company colours), locked typewriter cards, big name tags, our audio levels (owner: music level perfect).

## A. Shot-plan rules (free, no engine work)
1. Thesis as a physical object: one dominant prop in the first 5 s, with a size contrast against a figure (e.g. giant memo folder).
2. Return the same motif at the end in a changed state (sealed -> open), never implying a verdict.
3. Hook: 4-5 distinct pictures in the first 10 s, each <= 2.5 s; the key card lands by about 6 s.
4. No gap longer than about 20 s without a cut or visual beat.
5. Keep cutting through the last 30 s (reference video speeds up there, ~2.5 s per cut); hold the final black card only the last 3-4 s.
6. Cut closer when the stakes turn personal (hard cut 1.0 -> 1.25 zoom, or a 6-frame punch).
7. Split about 8 long lines into two pictures (target average about 3.4 s per picture, reference 3.1-3.7 s).
8. Light the place the eye should read with a gold pool (existing `real_night` pools).
9. One measure at a time for numbers: counter ramps out-cubic over about 36 frames, final number held >= 20 frames.
10. Brief black phrase cards at turns of the story; evidence as held/desk objects; change shot size when the question changes.

## B. Small engine options (build as opt-in, default OFF so old videos render identically; preview before use)
1. Whip transition: about 10 frames at 30 fps, about 24 px horizontal smear at the midpoint, between place jumps.
2. Foreground drift: three planes (rear 12 px, subject 26 px, near prop 42 px over 75 frames), 12 px overscan; desk/table is the near plane.
3. Blink on punctuation + one-beat mouth change in held close-ups (check what `Actor` already does first).
4. Counter easing check in `widgets.counter` against A9.
Plan: build whip + drift for ONE chapter first, show the owner a preview, then decide on the rest.

## C. Audio: measure only
Reference mixes are -14.3 to -14.6 LUFS integrated, -3.0 to -1.8 dBTP. Measure our final mix against that and report; change nothing without asking.
