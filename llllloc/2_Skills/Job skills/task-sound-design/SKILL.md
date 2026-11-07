---
name: task-sound-design
description: "Sound design for his films, always in Premiere Pro, never in After Effects, Cavalry, MOTION or Figma: spot the hero moments, pull real sounds from his library with llllloc:tool-soundly, place each sound as its own clip on SFX tracks named by family, never one mixed stem, and balance VO, music and SFX to a web or broadcast loudness target. Runs when the user types its name, or when /llllloc:router picks it for sound design, SFX, a sound pass or a VO and music mix on a Premiere edit. It never picks music, never records or rewrites VO, never renders, and never saves his project."
---

# llllloc:task-sound-design

Claude is the sound designer and the mixer for a picture-locked edit. The job has two halves: the SFX pass (what sounds, where, how loud) and the mix (VO, music and SFX against each other, to a loudness target). The craft comes from `method.md`. The Premiere mechanics come from `premiere-mechanics.md`. `llllloc:tool-soundly` finds and copies the sounds. `llllloc:tool-premiere-pro` loads with this skill for everything else on his timeline (checkpoint, labels, note boxes, the failure log).

Lessons: list `llllloc/4_Lessons/Programs/Premiere Pro/`, and read only the file that matches the job (16 Oct 2026, his words: read only the lesson that is needed).

## ALWAYS IN PREMIERE, ONE CLIP PER SOUND (18 Oct 2026)

- Sound design is always done in Premiere Pro, on the edit's own timeline. Never in After Effects, Cavalry, MOTION or Figma. Why: he mixes and delivers from Premiere, and a sound baked into a motion render cannot be moved or levelled.
- Every sound is its own clip on the timeline, with its own level. Never bounce or mix several sounds into one WAV or one stem. Why: he trims, moves and levels each sound himself (a client, 18 Oct 2026: a mixed stem had to be redone as 113 clips).
- One SFX track per family, named `SFX <FAMILY>` (examples: `SFX UI`, `SFX AIR`, `SFX LOW`, `SFX TYPING`). Adding audio tracks for SFX is allowed by default: `add_tracks` puts them at the bottom and moves no other track (premiere-mechanics.md, PLACE).

## MUST HOLD (10 Oct 2026)

Tick before the first write:

```
- [ ] Checkpoint made, named in the reply. Why: no scripted undo exists.
- [ ] The VO is the anchor. Measured, never assumed: every VO source, the music and each SFX file with ffmpeg loudnorm on his Mac (premiere-mechanics.md, MEASURE). Two VO sources can sit 6 dB apart (LUXE, 10 Oct 2026).
- [ ] His music keyframes read with get_keyframes before any music change. His curve is his mix. Add to it, never replace it.
- [ ] One sound per hero moment. A cut with no visible move gets nothing. Why: a sound on every cut is the cheap-corporate tell.
- [ ] SFX files copied into the project (copy_to_project), bin and items pink before placing.
- [ ] Each sound is its own clip on an `SFX <FAMILY>` track. No mixed WAV, no stem.
- [ ] No render, no save_project, no video to the chat. He listens in Premiere.
```

CHECK after the pass: the video track clip counts are unchanged, the SFX clip count equals the spotting list, every SFX clip's level reads back (get_clip_volume), and the loudest moment (logo, final hit) adds no more than two SFX peaks on top of a music swell. If the check fails, return to the box it names, then to step 6.

## SCOPE

In: SFX from his library, ambience and texture beds, risers and lands, UI sounds, VO level balance, music ducking and swells, SFX levels, the loudness check, stems advice. A revision ("the logo hit is too loud") is a full request on that moment only.
Out: music choice or edit, VO recording or cutting, the picture. Say so in one line and stop.

## STEPS

1. Read the film. `get_active_sequence` (both track types). Find the newest render in `RENDERS/`: contact sheet (`fps=2, tile 8x12`) and a 16 kHz mono WAV with ffmpeg on his Mac, stage both, read the sheet, transcribe with faster-whisper `small` word times. Now every cut, card and word has a time. No render: `export_frame` at each cut instead.
2. Measure. premiere-mechanics.md MEASURE. Write down: VO effective loudness per source (file LUFS + clip dB), music effective loudness under VO, the gap. Target gap 12 to 18 dB during speech. Fix a VO source that sits off the others by clip volume, not by touching music.
3. Spot. method.md SPOTTING. A list of 10 to 20 events for a 60 s film, each with time, the VO word, the visible move, the family (UI, AIR, LOW) and the file. Write it in the reply as the table. The list IS the design: an ordinary list of whooshes is the default, name it and beat it (RULE 9).
4. Pull. `llllloc:tool-soundly` STEPS: one search per family from the spotting list, by the real material, copied into the project's SFX folder. Never the same file twice unmodified.
5. Place. premiere-mechanics.md PLACE. Bin `<SEQUENCE>_From Soundly` under `03_SOUND`, pink. One clip per sound, on new tracks `SFX <FAMILY>` under his music (ALWAYS IN PREMIERE). A riser ends on the cut. A whoosh starts 1 frame before the move. A land sits on the cut frame. A texture bed runs the hero shot and stops with it.
6. Level. method.md LEVELS. Set every SFX clip by its measured peak: UI peaks 12 to 18 dB under the VO peak, lands 14 to 18 under, textures 20 or more under. Read each back.
7. MIX. VO sources matched. Music gap checked. The last 3 s (logo) checked for stacking. Delivery target named in the reply: web -14 LUFS and -1 dBTP, ebu -23, atsc -24.
8. CHECK and REPLY. The CHECK above. Reply: tracks and counts, the spotting table, what the mix changed and why, the checkpoint name, the one choice he should listen to first, and the delivery note (limiter on the master before export, stems unlimited).

## REPLY

Done, then where to listen first (sequence, two time ranges). The spotting table. One line each: checkpoint, VO change, music change, the least-sure sound, the export note. The closing lines of core rule 9.

## WHERE THE JOB FILES GO (16 Oct 2026, FOLDERS v19)

A creative job's cue sheet goes in `*_CLAUDE/9_Post/SOUND.md`: VO, music and SFX with source, licence and timecode. A folder appears the first time a file goes in.