# RUBRIC: MOTION

JOB: score a motion film or one part before it is handed over.

INPUT: the render path, the VO script, the look lock, his notes.

STEPS
1. Pull frames with ffmpeg: a contact sheet every 0.25 s, plus every frame from 0.2 s before to 0.2 s after each cut.
2. Find frozen stretches: `ffmpeg -i <file> -vf freezedetect=n=-60dB:d=0.5 -map 0:v -f null -`
3. Measure sound: `ffmpeg -i <file> -af ebur128 -f null -` (read the integrated loudness and the loudness range).
4. Score every line 1 to 5 with a timestamp as evidence.

OUTPUT: the scored table, the measured numbers, the default test, the fixes.

RULES
- R1. Measure what can be measured. Why: "it feels slow" starts an argument, "4.1 s frozen in 30 s" does not. Check: are frozen time and loudness given as numbers?
- R2. Pacing errs slow. Why: client notes on films ask to slow down or hold far more often than to speed up. Check: does the logo hold at least 1 s, and does the first cut have room to read?

CHECK: every line has a score and a timestamp. M1 and M7 have numbers.

| # | Line | 5 means |
|---|---|---|
| M1 | No dead time | Frozen time under 1 s per 30 s. No single hold over 0.6 s except the end card. |
| M2 | Frame 0 is finished | The first frame is a complete composition, not a half-entered word. |
| M3 | Holds long enough | Every line of text stays on screen long enough to read twice. Logo hold at least 1 s. |
| M4 | Clean transitions | No text crosses text. No title split by a wipe. One object or direction carries across each cut. |
| M5 | Readable text | Body text at least 32 px tall at 1080p, key words at least 56 px, measured on the frame. |
| M6 | On the VO | Each beat lands on its VO word. Nothing important happens during silence by accident. |
| M7 | Sound | Integrated loudness near -14 LUFS (punchy) or -16 LUFS (calm). Range at least 3 LU on energetic music. Music does not die before the logo. |
| M8 | Obeys the look lock | Colors, type, materials and camera match `LOOK-LOCK.md` and the brand file. |
| M9 | Not the default | The default test passes: this is not "image, then video, then text" stock motion. |
