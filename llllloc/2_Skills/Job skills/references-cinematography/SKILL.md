---
name: references-cinematography
description: 'Reads a video reference for how each SHOT is made, the way a director of photography, a camera operator and a VFX supervisor would: the camera move per shot with its rig, speed and motivation (pan, dolly, crane, handheld, gimbal, drone, motion control), lens and focal length, framing, shutter and motion blur, speed ramps, light changing inside the shot, in-camera tricks, and the VFX by type (comp, roto, set extension, CG, sim) with how each was likely built. Measures with TransNetV2, PySceneDetect, optical flow, ffmpeg and GeoCalib. Writes a shot sheet a video prompt, a shoot plan or an After Effects build can be made from. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when /llllloc:router picks it for a dropped video with how did they shoot this, this camera move, this VFX, this technique, or a video reference for a new film. The cut is llllloc:references-edit; one frame''s light and colour is llllloc:references-photo.'
---

# llllloc:references-cinematography (17 Oct 2026, his words: "reference for VFX, camera movement, cinematic techniques ... of a video")

A video reference is read shot by shot as a camera on a rig, through a lens, at a shutter, with what was added after. The output is a shot sheet: a new film can be shot, prompted or built the same way. The cut (shot lengths, rhythm, structure): `llllloc:references-edit`. One frame's light, colour and grade: `llllloc:references-photo`. Designed motion graphics: `llllloc:references-motion`. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. A move is a vector, not a feeling. "Dynamic" is not a finding; "push-in at about 0.4 frame widths per second over 3.2 s, parallax on the foreground, so a dolly not a zoom" is. Every move carries its direction, speed, duration and what motivates it (a look, a line, a reveal).
2. Measure, then look. Shot list, flow, freeze and signal stats come from the commands below; rig, lens and VFX method are read by eye from that evidence and marked `~`. Observed, inferred and unknown stay in separate sentences.
3. VFX is named by how it was built, with the tell that gives it away. "Looks CG" is nothing; "set extension above the second floor: the parallax on the upper windows lags the real wall by about one pixel per frame, and the grain is cleaner there" is a finding.
4. Mechanism transfers, material by ownership. The move, the rig logic, the lens choice, the shutter, the VFX method all transfer to a new subject. His own and a client's footage, logo, product and faces go into the work as given; an outside reference's subject comes in when he says so. No legal rule caps a job (his words, 17 Oct 2026).

## MEASURE (run first, raw output to `_batches/`)

```
brew install ffmpeg; pip install scenedetect opencv-python-headless numpy; uv tool install transnetv2-pytorch   # once (ask first, core rule 1)
ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height,r_frame_rate,avg_frame_rate,codec_name,pix_fmt,color_primaries,color_transfer -of default=nw=1 <file>
scenedetect -i <file> detect-adaptive list-scenes -s                                         # shot list with timecodes -> <file>-Scenes.csv
transnetv2_pytorch <file> --device cpu --output transnet_shots.csv --no-progress-bar    # finds dissolves; merge as llllloc:references-edit MERGE
ffmpeg -i <file> -vf cropdetect=limit=24:round=2:reset=0 -f null - 2>&1 | grep -o 'crop=[0-9:]*' | sort | uniq -c | sort -rn | head -3   # letterbox, aspect
ffmpeg -i <file> -vf freezedetect=n=0.001:d=0.1 -f null - 2>&1 | grep freeze_             # freeze frames
ffprobe -f lavfi "movie=<file>,signalstats" -show_entries frame=pkt_pts_time:frame_tags=lavfi.signalstats.YAVG,lavfi.signalstats.YDIF,lavfi.signalstats.UAVG,lavfi.signalstats.VAVG,lavfi.signalstats.SATAVG -of csv=p=0 > signal.csv   # light and change per frame
ffmpeg -i <file> -vf vidstabdetect=shakiness=5:accuracy=9:result=transforms.trf -f null -   # per-frame x, y, rotation of the camera shake
python3 - <<'EOF'   # per-shot camera move from optical flow (Farneback), one line per shot
import cv2, numpy as np, csv
cap = cv2.VideoCapture("<file>"); fps = cap.get(cv2.CAP_PROP_FPS)
shots = [(float(r["Start Time (seconds)"]), float(r["End Time (seconds)"])) for r in csv.DictReader(open("<file>-Scenes.csv")) if "Start Time (seconds)" in r]
def frame_at(t): cap.set(cv2.CAP_PROP_POS_MSEC, t*1000); ok, f = cap.read(); return cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (320, 180)) if ok else None
for i, (s, e) in enumerate(shots, 1):
    ts = np.arange(s, e - 1/fps, 1/fps)[:: max(1, int(fps/6))]; vec = []
    for t in ts[:-1]:
        a, b = frame_at(t), frame_at(t + 1/fps)
        if a is None or b is None: continue
        fl = cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        h, w = a.shape; ys, xs = np.mgrid[0:h, 0:w]; dx, dy = fl[..., 0], fl[..., 1]
        cx, cy = xs - w/2, ys - h/2; rad = (dx*cx + dy*cy) / (np.hypot(cx, cy) + 1e-6)
        vec.append((dx.mean()/w*fps, dy.mean()/h*fps, rad.mean()/w*fps, np.hypot(dx, dy).std()/w))
    if not vec: continue
    v = np.array(vec); mx, my, mz, par = v.mean(0); jitter = v[:, :2].std(0).mean()
    kind = "static" if abs(mx) < .02 and abs(my) < .02 and abs(mz) < .01 else ("push/pull" if abs(mz) > max(abs(mx), abs(my)) else "pan/truck" if abs(mx) > abs(my) else "tilt/pedestal")
    print(f"shot {i} {s:.2f}-{e:.2f}s {kind} x={mx:+.3f} y={my:+.3f} z={mz:+.3f} widths/s parallax~{par:.3f} jitter={jitter:.3f}")
EOF
```

- Units: x, y and z are frame widths (heights) per second. z positive is a push-in or zoom-in. Parallax high with z: a dolly (near things move more); parallax near zero with z: a zoom (flow is radial and even). Jitter above about 0.02 is handheld; a smooth low-frequency drift with roll near 0 is a gimbal or Steadicam; a near-linear x is a slider or dolly.
- Shutter angle by eye: in a pan, the blur streak against the per-frame displacement from the flow. A streak about half the displacement is 180°; much shorter is a tight shutter (staccato); longer is a wide shutter or added motion blur.
- Speed ramps and slow motion: YDIF that drops to zero every n-th frame is frame duplication; a rising or falling YDIF envelope inside one shot is a ramp; true high frame rate shows no duplicates and clean blur.
- Light inside a shot: a step in YAVG is a practical switched or a flash; a slow ramp is a dimmer or the sun; VAVG up with UAVG down is a warmer drift.
- Lens on one frame: GeoCalib (`pip install -e "git+https://github.com/cvg/GeoCalib#egg=geocalib"`, CPU) gives focal length, roll and pitch; the gravity tilt confirms a low or high camera. A full camera path needs a GPU model (ViPE, MegaSaM, MonST3R) or COLMAP on a static scene; say so and mark `unknown` without one.
- Shot detection on fast camera motion: a cut only PySceneDetect found (a move, a light streak, a person passing the lens) is often false; check its frame pair. A long move split: merge by eye, say so.

## THE PRO READ

| Field | What to write |
|---|---|
| SPEC | Size, aspect from cropdetect, frame rate, codec, SDR or HDR (`color_transfer` smpte2084 or arib-std-b67 is HDR), shot count. |
| MOVE | Per shot: type (static, pan, tilt, roll, dolly in/out, truck, pedestal, arc, crane up/down, tracking lead/tail/side, orbit, aerial, dolly zoom), speed and duration from the flow, the beat it starts and ends on, what motivates it. |
| RIG | The rig the move needs (tripod, slider, dolly, crane or jib, Steadicam, gimbal, handheld, car mount, cable cam, drone or FPV, probe or snorkel lens, motion control such as a Bolt for a repeatable high-speed pass), with the tell: jitter signature, roll, path shape, impossible-for-a-human speed or height. |
| LENS | Focal class per key shot (ultra wide, wide, normal, long) from perspective and compression, depth of field and the focus pulls with their timing, anamorphic tells (oval bokeh, horizontal flares, squeeze), distortion, GeoCalib numbers when run. |
| FRAME | Size and angle per shot, camera height, headroom, where the subject sits, how blocking moves the subject through the frame, the eye path. |
| SHUTTER AND TIME | Shutter angle by eye, frame rate feel (24 filmic, 30 and 60 video), slow motion and its method, speed ramps with their seconds, freeze frames, reverse, stop motion, long exposure. |
| LIGHT IN TIME | Changes inside a shot from signal stats: practical switches, flashes, flicker, sun through a window, moving sources, light motivated by the move. |
| IN-CAMERA | Tricks made on set: mirrors, reflections, forced perspective, practical smoke, prisms and filters, double exposure, whip transitions, match-on-action hidden cuts, rear or LED wall projection (soft parallax, no key edge). |
| VFX | Per shot that has it: type (comp, key, roto, clean plate, set extension, CG element, sim or FX, DMP, 2.5D, screen replacement, matchmove, wire or rig removal, beauty, crowd tiling, morph, clone), the tell (edge, grain mismatch, parallax lag, light direction mismatch, repeating texture, too-clean motion blur), and the likely build order. |
| TECHNIQUE NAME | What a DP or VFX supervisor calls the device (oner, invisible stitch, speed ramp into match cut, contra-zoom, snorricam, bullet time, hidden wipe, day-for-night, poor man's process) and its lineage. |
| WHAT MAKES IT LAND | The three to five choices with their numbers. Also what reads generic: a drone pull-out for scale, a gimbal orbit with no motivation, slow motion on everything, a dolly zoom for drama. |

## THE SHOT SHEET

The dossier (`llllloc:references`) carries what recurs across his references. The sheet is the usable part, written to the job's `*_CLAUDE/2_References/SHOTS_<name>.md` (or beside the dossier when no job is named):

```markdown
# SHOTS <name>                <date> · built by llllloc:references-cinematography
## SPEC          size, aspect, fps, SDR/HDR, shot count
## SHOT TABLE    one row per shot: n | in-out s | size/angle | move + speed | rig ~ | lens ~ | shutter ~ | VFX | motivation
## LIGHT IN TIME the changes inside shots, with seconds
## IN-CAMERA     the tricks and how to repeat them
## VFX BUILD     per VFX shot: type, tell, likely build order, what to shoot on set to make it easy (clean plate, tracking markers, HDRI)
## PROMPT LINES  per shot for llllloc:task-prompt VIDEO: camera move in plain geometry with speed and duration, lens class, shutter feel, the one thing that changes in the frame; which reference gives which attribute
## SHOOT LINES   per shot for llllloc:task-art-direction: rig, lens, frame rate, what the operator does on which beat
## OPEN          moves not resolved, VFX not sure, lens with no evidence
```

## RESEARCH (with `llllloc:task-research`)

The DP, director, camera operator, VFX house and supervisor from the credits (Shots, LBB, IMDb, the production company's case study); the technique by its trade name; the DP's or supervisor's own breakdown (fxguide, befores & afters, Art of VFX, ASC articles, a BTS cut); the rig and lens when published (ASC Manual, lens tests); whether it is a durable craft or a trend of the year; what breaks when copied (a move with no motivation reads as a demo reel, a comp with mismatched grain, a ramp with no sound hit). Cache: `llllloc/5_Research cache/jobs/reference-analysis.md`.

## WHAT TRANSFERS, WHAT DOES NOT

Transfers: the move with its speed and motivation, the rig logic, the lens class, the shutter and frame rate feel, the ramp timing, the in-camera trick, the VFX method and its build order, the on-set prep that makes the VFX work. Does not, from an outside reference: its subject, its location, its product, unless he asks for it. From his own or a client's footage: everything.

## HAND-OFF

`llllloc:task-prompt` VIDEO uses PROMPT LINES as intent: one move per shot in geometry, lens class, shutter feel, one change in the frame. `llllloc:task-art-direction` uses SHOOT LINES for the shoot plan and the shot list. `llllloc:tool-after-effects` and `llllloc:tool-premiere-pro` use VFX BUILD and the ramp timings. A sheet and a cut read of the same film: this skill owns the shot, `llllloc:references-edit` owns the cut, and the two sheets cross-reference by shot number.
