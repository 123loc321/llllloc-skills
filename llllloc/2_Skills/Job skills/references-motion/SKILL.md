---
name: references-motion
description: 'Reads a motion reference (animation, motion graphics, title design, UI motion, a web or app animation, a Lottie or Rive file, a screen recording) the way a senior motion designer would: timing in frames, spacing and easing as measured curves, staggers in milliseconds, holds, overshoot, hierarchy, transitions and the system of rules that repeats, measured from frames or from the file before judged. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when /llllloc:router picks it for a dropped animation to analyze or learn from, a timing or easing to follow in motion work, or ''is this good'' on an animation. A live-action cut is llllloc:references-edit; a live site''s animation code is read by llllloc:references-code, which hands the frames here.'
---

# llllloc:references-motion (split from llllloc:references, 17 Oct 2026)

Motion is read as timing (how many frames a move takes) and spacing (how the distance between frames changes). The output is a motion spec a program skill can key: per element, trigger, property, duration, easing, delay, stagger. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. Timing in frames and milliseconds, easing as a curve, never "snappy" or "smooth". A move is `18 frames at 24 fps, 750 ms, ease out, overshoot 4 percent, settles in 6 frames`.
2. Easing is measured, not named by feel. Track the element, normalize position and time to 0 to 1, fit a cubic bezier, and compare with the named curves. A guessed ease is wrong on frame one.
3. Hold frames and staggers are findings. A dead hold of 12 frames after a hit, a 60 ms stagger across cards: these are the system.
4. The rules of movement transfer from any reference. A client's assets, characters, logo and illustration are the material of the job and go in as given; an outside reference's assets come in when he says so.

## MEASURE (run first, raw output to `_batches/`)

- **A video file:** `ffprobe` for fps and frame count (see `llllloc:references-edit`), then every frame of the move: `ffmpeg -ss <start> -to <end> -i <file> -vsync 0 frames/f_%04d.png`. Holds: `ffmpeg -i <file> -vf "freezedetect=n=0.003:d=0.2" -f null -` and `mpdecimate` drop counts (a drop is a repeated frame). Motion blur per frame: Laplacian variance against the shot's still frames.
- **The curve:** track the element across the frames (`cv2.TrackerCSRT_create()` or `cv2.calcOpticalFlowPyrLK`), normalize, then `scipy.optimize.curve_fit` to a cubic bezier with x1, x2 in 0 to 1. Overshoot above 1.0 is a back or spring ease. Compare: ease-out 0,0,0.58,1; ease-in-out 0.42,0,0.58,1; easeInOutCubic 0.65,0,0.35,1; easeOutBack 0.34,1.56,0.64,1; Material standard 0.2,0,0,1 and emphasized decelerate 0.05,0.7,0.1,1. `pip install opencv-python-headless scipy` (ask first, core rule 1).
- **Stagger:** the ms gap between the first-motion frame of each element. Norms: 30 to 80 ms per item on a 300 ms base; over 150 ms reads sluggish.
- **A Lottie JSON:** read it directly: `fr` fps, `ip` and `op` in and out frames, each keyframe `t` (frame), `s` and `e` values, handles `o` and `i` with x and y in 0 to 1, `h: 1` a hold. `cubic-bezier(o.x, o.y, i.x, i.y)` is the bodymovin convention.
- **A Rive file:** binary, no reader here. Render or screen-record it and read the frames.
- **After Effects keys:** influence to bezier, x1 = 1 minus influence/100, x2 = influence/100 (inferred, mark it).
- **A website or app animation:** `llllloc:references-code` reads `document.getAnimations()`, GSAP timelines and CSS transitions for the exact numbers and records the rest with Playwright screencast; this skill reads those frames the same way as a video.
- **A screen recording from his Mac:** frame rate is the recorder's, not the app's. Say so.

## THE PRO READ

| Field | What to write |
|---|---|
| SPEC | fps, length, size, the number of distinct moves. |
| TIMING | Frames and ms per key move: anticipation, action, settle, hold. Norms for UI: short 50 to 200 ms, medium 250 to 400, long 450 to 600 (Material 3). |
| SPACING | Even, ease out (tight then wide), ease in (wide then tight), both; the fitted curve and the closest named one; overshoot and settle in frames; spring stiffness and damping when it is a spring. |
| STAGGER | Offset per item in ms, the order (reading order, radial, random), the base duration. |
| HIERARCHY | What moves first, what holds, what leads the eye, what never moves. |
| TRANSITIONS | How one scene becomes the next: cut, wipe, morph, match, field swap, shared element, container transform. Duration and ease of each. |
| SYSTEM | The rules that repeat: grid, shapes, type behavior (letters as objects or as a block), color swaps, loop logic, what is on ones and what on twos, smears and sparks. |
| PHYSICS | Squash and stretch, follow through, secondary motion, blur by shutter or by effect. |
| WHAT MAKES IT LAND | The three to five choices, each with its number. |

## THE MOTION SPEC

The dossier carries the recipe. The spec a program skill keys goes to the job's `*_CLAUDE/3_Design/MOTION-SPEC_<name>.md`: one row per element, `trigger | property | from | to | duration | easing | delay | stagger | hold`.

## RESEARCH (with `llllloc:task-research`)

The studio, animator or motion designer and their stated process; the tool (After Effects, Cavalry, Rive, Lottie, GSAP, Figma motion); the device name (field swap, smear, shared axis, container transform, kinetic type); whether it is durable or a trend; what breaks when copied (bounce on everything, staggers over 150 ms, motion with no holds). Cache: `llllloc/5_Research cache/jobs/motion/_TOPICS.md`, then the one topic file.

## HAND-OFF

`llllloc:task-motion` owns the motion rules of the house and takes the spec. The program skill keys it: `llllloc:tool-after-effects`, `llllloc:tool-cavalry`, `llllloc:tool-motion-app`. `llllloc:task-prompt` VIDEO uses TIMING and HIERARCHY for an AI video shot. A critique of motion runs CRAFT with this read and TASTE with the MOTION dossier.
