# Owner feedback from the first test render (Ponzi test, "50% in 45 Days")

The owner watched the test (`videos/ponzi-test/`, rendered on their PC) and called it "a banger - with a few tweaks
it hits mind-blowing". These are the owner's instructions. **Apply all of them in the engine / shot rules before the
next render** (the full-length Ponzi video). Do not re-render the test video.

## Sound (rules from now on)
1. **Music level is perfect** - keep the current music gain and ducking exactly as they are.
2. **Sound effects are too loud** - lower all SFX (stamp, cash, coin, whoosh, pop, paper, ticks, ding / low tone).
3. **Typed text = a real typewriter sound, by default, in every video.** The current synthetic click does not fit.
   Use a believable typewriter (key strike + typebar clack, slight variation per key, a carriage "ding"/return at the
   end of a card), quieter than now, timed to each word as it appears.

## Picture
4. **Opening shot looks like a long shot.** Too wide: people and buildings look tiny and far. Start closer (medium shot
   on the line) and travel along the line to the building. Check every shot for the same problem: prefer medium and
   close shots; use full-width wides only as short establishing beats.
5. **Say where the line is going.** In the opening, highlight the building the people are queuing for (Ponzi's
   Securities Exchange Co.): big readable sign, lit doorway, the line ending at that door.
6. **Buildings and road too small next to the characters.** Fix the scale of the street sets (taller buildings, wider
   road) or the characters, so people and places feel real together.
7. **Tables / objects not visible in the dark navy (night print) shots.** In several shots the desk and things are not
   clear. Known cause found during review: in `engine/sets.py` the light map's ambient value is computed wrongly
   (`skia.Color4f(kit.hx(amb))` gives ~0), so the whole room counts as half-lit and the dotted lit/dark dither covers
   everything. Also in `engine/looks.py` very dark navy fills are mistaken for ink lines (detect ink by low saturation,
   not darkness), and lit areas carry too many dots. Fix so rooms are properly dark, lamp/window areas clean and
   readable, desks and props clearly visible. Show the owner before/after before changing the locked look.
8. **Diagram / "plain navy" shots get a frame** - like the owner's reference for the coupon scene: navy background
   with a soft dotted vignette, a double rounded light-navy border around the whole frame, big Alfa Slab labels
   ("EUROPE" -> "UNITED STATES"), a big gold arrow, and a large paper card ("POSTAL REPLY" heading + rule +
   "INTERNATIONAL POSTAGE COUPON" in Special Elite). Use this framed style for all diagram, document and newspaper
   shots.
9. **Don't repeat the same wide shot.** The office wide was used 4 times in a row - vary angles: medium shot,
   close-up, desk close-up, push-in on the face.
10. **No empty first frames.** Text cards started black with only the cursor, the title card started tiny, chapter
    cards started blank - the first frame of every shot must already show something.
11. **Documents / newspapers bigger and readable** (fill the frame, framed style from 8).
12. **Ending street:** closer framing; phones big and glowing so "it moved online" reads instantly.
13. **Small text too small** (name tag, labels like "pleaded guilty - mail fraud", place tag): make them bigger for
    phone screens.
14. **Lesson board:** the presenter stood far left and small - put them closer to the board and bigger.

## Keep / add (owner's notes after watching)
15. **Keep the red-flags board - the owner loved it.** Make it a standard segment of the lesson part (Ch5) in every
    video: a whiteboard (or the framed style) where the warning signs / takeaways **pop in one by one, timed to the
    narrator**, each with a soft pop (quiet). Reuse as "Red flags", "How to spot it", "What to do", etc.
16. **Make the ending obvious.** The test ended so suddenly the owner couldn't tell it was over. The music resolves on a
    clear final note (no fade to nothing), the final question card holds longer with a soft sting, then a short outro
    card in the channel look, then an end-screen section (~15-20 s) laid out for YouTube's "next video" + "subscribe"
    elements, quiet music under it.
17. **More relevant animation - it will make our videos stand out.** Add to the toolkit and use them often:
    - Hands + desk (top-down): a hand **slams a stack of cash / notes / a document on the table** (thud, papers bounce,
      small camera shake, dust puffs); a hand stamps a document; hands slide papers, count bills, tap a key line;
      coins dropped that bounce and spin.
    - Charts + numbers: line charts that draw on / crash (orange arrow for losses), bar charts that grow, pie charts,
      money stacks growing / shrinking, a **pyramid diagram** (new money at the bottom paying the top - ideal for
      Ponzi), scales tipping.
    - Story props: tear-off calendar countdown ("45 DAYS"), receipts unrolling, ledger pages flipping, envelopes
      opening, newspapers spinning in, phone ringing with ring lines, handcuffs closing, map with a dotted route
      (e.g. Europe -> United States).
    - Always in the locked style (navy, gold = money, orange = losses only, the framed look from item 8), quiet SFX.

## Next
- Make the **full-length Ponzi video** (full Template A script, ~10 min) with the `documentary-script` skill, then
  animate it with all fixes above applied. Ask the owner PC or cloud before rendering.
