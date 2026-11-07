# llllloc:task-motion KIT

The reusable engine for every motion job. Built on a client CORE Part 1 (27–28 Sep 2026).
The skill `llllloc:task-motion` holds the rules. This folder holds the code.

## HOW A SESSION STARTS
1. Copy this `kit/` folder into the new job folder on the Mac. The Mac's python3 has none of the kit's packages (29 Oct 2026). Ask first (core rule 1), then `uv run --with skia-python --with numpy --with svgelements --with opencv-python --with pillow --with scipy --with soundfile --with pyloudnorm python3 <script>`.
2. Motion job on an existing film: also read `<project>/*_PROJECT FILES/**_MOTION/_STATE/MOTION-STATE.md` first (older project: `*_CLAUDE/7_Motion/`).
   It names the parts, their versions, the build zips, the MEZZ files and the open notes.
3. Unzip the newest build zip of the part you touch over the kit copy.

## FILES
| File | Generic or per film | What it does |
|---|---|---|
| `lib.py` | generic | easing (eio, eout, ein, eback, smooth, pulse), color, svg path to skia, glyph groups, sprites, radial, ring, dot, line |
| `fields.py` | generic | living gradients as float math: `mesh` (Stripe-style flowing fill), `horizon`, `charcoal`, `to_image` (float to half-float skia image) |
| `fx.py` | generic | living light: `inner_flow` (light inside a card), `rim_comet` (light running along a stroke), `living_background` |
| `render.py` | generic | half-float canvas, stills, resumable frames, workers, motion blur averaged in float, then the film's `post_np` (vignette, grain, dither to 8 bits). `FILM=<module>` picks the film file. `FRAMES_DIR` picks the frame folder. |
| `sync.py` | table per film | text-to-voice check. Edit `EVENTS`. A FAIL blocks the encode. |
| `pace.py` | numbers per film | adds silence into VO gaps. Edit `GAPS`, `VO_END_OLD`, `DUR`. |
| `audio_template.py` | top generic, cues per film | synth kit on top (whoosh, sub, hit, tick, glass, sonar, riser, swell, shimmer, thump, pad, pluck, reverb), cue sheet in the middle, VO + ducking + master at the end. Chain mode: env `OFFSET`, `TOTAL`, `STEMS_OUT`. |
| `stitch.py` | generic | joins parts without rendering any part again. See STITCH. |
| `orbmath.py` | method generic, data per film | a glowing sphere as pure math, fitted once from a plate (`orb_polar.npy`). Hard 1-pixel edge, body field inside, glow field outside. |
| `sheet.py` | generic | contact sheet of stills |
| `pieces.py` | old | for the old cloud device link, not used on the Mac |

## CARDS, BUTTONS, POST (copy from the reference `film2.py`)
`spring`, `seq_state`, `glass_card`, `draw_content` (container transform, fade through), `draw_button` (press, pop, gradient flood, glow), `post_np`, the orb cache. See `LOOK-LOCK.md` in the client build for the numbers.

## A FILM FILE
One module (for example `film.py`) with: `W, H, FPS, DUR`, a `SHOTS` list `(start, end, name)`, one function per
shot, `shot_of(t)`, `draw_scene(c, t)`, `post(c, t)` (vignette + moving grain), and `CHAIN = os.environ.get('CHAIN') == '1'`.
Reference: `film2.py` inside `CER-P1_animation-build_v6.zip`.

## PARALLEL CHATS
One chat per part (lane). Lanes read `LOOK-LOCK.md`, write only in `**_MOTION/P<n>/`. The lead chat writes shared files and stitches.

## PARTS AND STITCH
- One film = parts. Each part is its own build folder with its own clock (0 = its first frame).
- The VO is split at word gaps. Every part shares the music key and tempo (a client: D minor pads, 120 bpm plucks).
- The transition INTO a part lives in the first second of that part. The part before it ends clean.
- Each part ships three things: the review MP4 (standalone: fade in and out), the MEZZ MP4 (chain mode: no end fade,
  CRF 12: with film grain, CRF 8 is 520 MB for 30 s), and its build zip.
- `stitch.py stitch.json` decodes the MEZZ files in order and encodes once (minutes, no render). Sound is rebuilt:
  each part's audio script runs in chain mode on one long timeline, so reverb tails and music ring across the joins,
  then one master pass (-14 LUFS, -1 dBTP).
- A join that needs a change: render only that part's first second again, then stitch.

## OUTPUT SIZE
Every delivery, final included, is 1920 x 1080, 30 fps (his rule, 28 Sep 2026). 4K only when he asks on one job:
canvas scale 2, rasters at 2x or more, time 3 hard frames first (REFERENCE A).

## SPEED NOTES (old 2 CPU cloud box: time 3 frames on the Mac first)
- 1080p frame with 4 blur samples: 2 to 3 s per worker. 30 s part: about 20 to 25 min.
- The orb costs most. `film2.orb()` caches one orb per frame, so blur samples of a still orb reuse it.
- Run long jobs in the background with `nohup`, poll with `sleep`. Never `pkill -f` a pattern that matches your own
  command line: write it as `pkill -f "render.py frame[s]"`.
