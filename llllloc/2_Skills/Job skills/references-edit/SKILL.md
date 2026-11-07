---
name: references-edit
description: 'Reads a cut reference (a film, ad, music video, trailer, social cut, any edited video file or link) the way a senior editor would: the cut list, average and median shot length, cutting rate over time, cut types (hard, match, J and L cuts, smash), speed ramps and holds, story structure as time ranges with shot counts, grade and camera per shot, measured with ffmpeg, TransNetV2 and PySceneDetect before judged. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when /llllloc:router picks it for a dropped video to analyze, break down or learn from, a pace or structure to follow in an edit, or ''is this good'' on a cut. Pure animation or motion graphics with no live cut is llllloc:references-motion; the sound of the film is llllloc:references-sound.'
---

# llllloc:references-edit (split from llllloc:references, 17 Oct 2026)

An edit is read as rhythm and structure: how long shots hold, where the pace rises and falls, how one shot becomes the next, and what the structure does to the viewer at each second. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. Never say "fast paced". Say ASL, median shot length and the cutting rate per 10 seconds, from the cut list. Report ASL and median together: two cuts can share a median and differ a lot in ASL (Salt, Cinemetrics).
2. Never state the frame rate from memory. Read `r_frame_rate` (nominal) and `avg_frame_rate` (phone captures can be variable).
3. A dissolve or a fade is not a cut. Two shot finders run together (MERGE): TransNetV2 finds the dissolves and fades, PySceneDetect the hard cuts in fast photo montages. Mark gradual transitions as their own type. Counting a fade as three cuts ruins the ASL.
4. The structure is written as time ranges with shot counts, not as adjectives: 0 to 3 s hook (2 shots), 3 to 14 s build (9 shots), 14 to 22 s turn (3 shots), 22 to 30 s payoff and logo (2 shots).
5. What transfers from an outside reference is the rhythm, the cut logic and the structure. The client's own footage, music and brand are the material of the job and go in as given; an outside reference's footage comes in when he says so.

## MEASURE (run first, raw output to `_batches/`)

```
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=r_frame_rate,avg_frame_rate,nb_read_frames,duration,width,height -of default=noprint_wrappers=1 <file>
uv tool install transnetv2-pytorch; uv tool install "scenedetect[opencv]"      # once; TransNetV2 1.0.5 (weights inside), PySceneDetect 0.7.2
transnetv2_pytorch <file> --device cpu --output transnet_shots.csv --no-progress-bar     # always cpu: on the Apple GPU (mps) the cut count changes
scenedetect -q -i <file> -o out detect-adaptive list-scenes -s -f pyscene.csv save-images -o out -n 1     # adaptive only: detect-threshold adds false cuts
ffmpeg -i <file> -vf "freezedetect=n=0.003:d=0.5" -f null - 2>&1 | grep freeze                            # holds and freeze frames
ffmpeg -i <file> -vf mpdecimate -loglevel debug -f null - 2>&1 | grep -c "drop pts"                       # duplicated frames: periodic drops mean slow motion by duplication
ffmpeg -i <file> -vf "fps=1,scale=160:-1,drawtext=text='%{pts\:hms}':fontsize=14:x=4:y=4:fontcolor=white:box=1:boxcolor=black@0.5,tile=6x5:padding=2:margin=2" -frames:v 1 -update 1 sheet.png
ffmpeg -ss <seconds> -i <file> -frames:v 1 -update 1 frame.png                                            # one exact frame, -ss before -i
```

MERGE (28 Oct 2026 test, our 87 s WESTPOINT film: 29 cuts shared to the frame; TransNetV2 alone lost 3 of 33 hard cuts, PySceneDetect alone lost 8 of 8 dissolves and added 7 false cuts). Keep every cut either list has. Match by seconds within 2 frames, never by frame number: PySceneDetect counts frames from 1, TransNetV2 from 0. Every cut only one tool found gets a frame pair (1 frame before and after, 5 before and after) and a look: TRUE, DISSOLVE or FALSE. Drop the FALSE ones and say how many.

From the merged list: ASL = mean of Length (seconds), MSL = median, cuts = shots minus 1, cutting rate = shots per 10 s bin, shortest and longest shot. J and L cuts: the signed offset in ms between each picture cut and the nearest audio onset (`librosa.onset.onset_detect` on the extracted audio); over two frames is a split edit. Match cuts: last frame of one shot against first of the next (HSV histogram similarity above 0.8 is a candidate, then confirm by eye). A link rather than a file: ask for the file, or for his yes to fetch it; never download from a site that forbids it.

## THE PRO READ

| Field | What to write |
|---|---|
| SPEC | Length, frame rate, size, aspect, shot count. |
| EDIT | ASL, MSL, their ratio, cutting rate per 10 s as a short series, shortest and longest shot. Where the pace speeds up and slows, in seconds. |
| CUT TYPES | Hard, match, J cut, L cut, smash, jump, dissolve, fade, wipe, whip, the count of each and where. |
| STRUCTURE | The beats as time ranges with shot counts: hook, build, turn, payoff, logo. What each beat does to the viewer. For a 30, where the gag or reveal lands (10 to 13 s is the ad norm). |
| SHOTS | Size and angle per key shot, how coverage is built, the insert logic. |
| CAMERA | Movement per shot (static, push, track, handheld, crane), speed, motivation. |
| TIME | Speed ramps, slow motion and its method (duplicated frames or true high frame rate), freeze frames, with their seconds. |
| GRADE | Contrast curve, black level, skin tone treatment, the look in one line, from the key frames (the STILL read of `llllloc:references-photo` on one frame per beat when the look matters). |
| SOUND SYNC | Which cuts land on which hits, in seconds; the rest is `llllloc:references-sound`. |
| WHAT MAKES IT LAND | The three to five editing choices, each with its number (Murch: emotion first, then story, then rhythm). |

## RESEARCH (with `llllloc:task-research`)

The editor, director and production company (credits, Shots, LBB, the agency's case study), what editors call the device (invisible cut, hidden split, hard world cut), the editor's own breakdown or interview, whether the pace is a durable craft or a dated trend, what breaks when people copy it (a fast cut with no holds reads as noise). Cache: `llllloc/5_Research cache/jobs/reference-analysis.md` and `jobs/video-delivery.md`.

## WHAT TRANSFERS, WHAT DOES NOT

Transfers: the rhythm numbers, the beat structure, the cut logic, where the holds sit, the sync rule. Does not: the footage, the music, the performances, the brand, the gag itself.

## HAND-OFF

`llllloc:tool-premiere-pro` builds the cut from the structure table and the ASL target. `llllloc:task-art-direction` uses the structure for a treatment or a storyboard. `llllloc:task-prompt` VIDEO uses the shot table for AI video shots. A film with a mix also loads `llllloc:references-sound`; a film with graphics also loads `llllloc:references-motion`.
