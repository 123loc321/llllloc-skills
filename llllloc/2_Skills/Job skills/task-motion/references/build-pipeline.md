# Build pipeline, sync, pacing, cards, craft defaults

Moved from SKILL.md on 14 Oct 2026, unchanged. Read in full before the first build of a film and before any retime.

## PIPELINE (starting shape)
1. VO CLOCK: faster-whisper `small.en` with word times into `words.json`, then measure onsets from the audio (SYNC). Put the VO on the MOTION timeline (`motion_film_set { audio }`).
   - VO SOURCE [R24]: his WAV when he gives one. Otherwise take the audio track of his rough-cut MP4 and go on. Never stop to ask for the WAV.
   - THE VOICE SETS THE PACE [R23]: his rough cut is a reference for content and order only. Its cut points never set the timing. Every cut and beat lands on the VO.
2. PACING and BEAT SHEET: one beat per phrase, a named transition per cut, the word each text event lands on.
3. ASSET PLAN: rebuild in code or export, element by element (ASSETS). Every big text sits on its own TEXT layer or slot from V1 [R25], so the split at delivery is a render switch, not a rebuild.
4. MOTION GRAMMAR: the brief's language as easing roles. THE SIGNATURE tried in 3 to 6 candidates (REFERENCE F).
5. STILLS FIRST: `motion_sheet` of 9 to 15 frames per section against the design. Fix, then hand it to him in the app.
6. QC in the app. Encode and deliver only at FINAL DELIVERY or on his ask [R32].

## SYNC. TEXT LANDS ON THE VOICE [R2]. A GATE.
- Measure each word onset from the VO. Never trust a whisper start that sits in silence.
- Every text event (word, chip, card, counter, label, reveal) is bound to one word. Readable (50%) from 3 frames before to 1 frame after the onset. Motion starts 4 to 8 frames earlier.
- `sync.py` checks every event. A FAIL blocks the hand-off. After any pacing change, measure again.
- A word swap is a slot or a fade-through. Never two words on top of each other. Detail: REFERENCE B.

## PACING. FRAMES BREATHE [R15]
Default holds: a new card, frame or hero state 1.2 s after it lands. A text line 0.4 s + 0.05 s per character. A number counts 0.6 s or more, then holds 0.8 s. Short of that: add silence in the VO gap (0.15 to 0.9 s) with `pace.py`. Never stretch or speed the voice. Busy lists get the most silence. A shorter hold is fine when the shot reads faster: name it.

## CARDS, CHIPS, BUTTONS
- Rebuild each one in code from the design's own values, never a past film's. Crop one beside the design render: within 15 levels. Method: REFERENCE E.
- Morph: the container changes size, the content fades through at its own size. Screen swap: the old screen stays opaque under the new one.
- Button click [R12], a special moment in every piece: it scales and bounces a little, glows up, and a gradient fills in. How it glows and fills is new for each piece, never a copy of a client. The cursor tip never covers the label.

## CRAFT DEFAULTS
- Cut on the word.
- Easing: `eio` moves, `eout` arrivals, `ein` short exits. Exits faster than entries.
- Motion blur: 4 samples, half a frame, more on fast moves.

## REFERENCE BUILD
A code model, never a look: a client CORE Part 1 v7, `film2.py` in `/Volumes/CREATIVE #1/260921_a client India_a client CORE/*_PROJECT FILES/*_CLAUDE/ANIMATION/P1/`. a client's look and its rule [R13] live in its own `LOOK-LOCK.md`. An adaptable MOTION title: `a client-TITLE-SLAM_MAIN.motion` (code layer with Content slots, every move measured from the words), in `/Volumes/CREATIVE #1/260921_a client a client_Introduction to Grwoth/*_PROJECT FILES/**_MOTION/TITLE-SLAM/`.

## THE KIT
Code on his drive (`kit/README.md`): render engine, living gradients, sync check, pause tool, sound synth, stitcher. Run it in place or copy it to the job folder. Change any tool. NOT LIMITED BY THE APP [R36] [R41] (8 Oct 2026): MOTION is his preview and swap desk, never the limit. Build each element with what works best (kit render, shaders, After Effects, Cavalry, Figma), then bring it in as layers: plates, PNG or ProRes sequences, code. Text, clips and pictures stay swappable layers. Never cut a shot to fit the app. What he must always be able to edit: the text, the animation (timing, distance, speed) and the easing. A change that helps every film goes back to the kit, lead chat only.
