# llllloc:task-motion — REFERENCE

The how-to detail behind the rules in `llllloc:task-motion` SKILL.md. Read the section a job needs, not the whole file.
## Contents
A output and encode · B sync · C fields, edges, banding · D living gradients · E cards, chips, button · F easing · G sound · H Figma export walls · I delivery on the Mac · J stitch · K tool choice and revision map · L final delivery files · M sections · N MOTION app methods · O Figma Motion methods

Moved out of the SKILL.md on 28 Sep 2026 (`/llllloc-log` trim: the skill was 29,400 characters, the cap is 16,500).
29 Sep 2026: L, M and the dated lines in E, I, J and K moved out of the SKILL.md. His words live in `00_My Claude Instruction/HIS-WORDS.md`, never here.

## A. OUTPUT AND ENCODE
- Every delivery, final included: 1920 x 1080, 30 fps, H.264 High, 4:2:0, progressive, MP4 with faststart, AAC 48 kHz [R3].
- 4K only when he asks for it on one job. Then time 3 hard frames first: 4K costs 1.5 to 2 times a 1080p frame for skia layers, 4 times for a per-pixel math field (a client, 2 CPUs).
- YouTube asks 8 Mbps for 1080p SDR at 30 fps (YouTube Help, 28 Sep 2026). Our CRF 14 master with grain runs 40 to 45 Mbps, far above it.
- Encode: `-c:v libx264 -profile:v high -pix_fmt yuv420p -crf 14 -preset slow -x264-params aq-mode=3:aq-strength=0.8:psy-rd=1.0,0:deblock=-1,-1 -g 60 -c:a aac -b:a 320k -ar 48000 -movflags +faststart`. AQ mode 3 gives more bits to dark areas (Advanced Encoding Guide). With grain a 1080p review runs about 45 Mbps.
- Section keyframes: encode the master with `-force_key_frames` at the first frame of every section in `SECTIONS.md`. Split with `-f segment` and `-c copy`: frame-exact, no quality loss. A fixed section, encoded with the same settings, goes back in with the concat demuxer and `-c copy` in seconds (FFmpeg Formats Documentation, 28 Sep 2026). This swap is a file copy, so it runs in Bash on his drive.
- MEZZ for stitching: chain mode, CRF 12 (about 335 MB for 30 s). CRF 8 with grain is 520 MB.
- Run renders and encodes in the background with `nohup`, poll with `sleep`. Never `pkill -f` a pattern that matches your own command: write `pkill -f "render.py frame[s]"`.

## B. SYNC MECHANICS
- Onset: RMS in 10 ms windows. A whisper start that sits in silence moves forward to the first window above -40 dBFS. A start inside sound stays.
- Window: readable (50% opacity) 3 frames before to 1 frame after the onset. ITU-R BT.1359: sound ahead of picture is noticed at 45 ms, sound behind at 125 ms.
- `sync.py`: `EVENTS = [(event, word, occurrence, readable_time)]`. It rebuilds the paced VO from `pace.py` and prints `event | word | whisper | onset | readable | offset`. Exit 1 on any FAIL.
- A morph with fade-through is readable at u = 0.55 of its window. Put the window start 0.55 x length before the readable time.

## C. FIELDS, EDGES, BANDING
- Half-float canvas: `skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_F16_ColorType, skia.kPremul_AlphaType))`. Snapshot with `toarray(colorType=skia.kRGBA_F16_ColorType)`.
- Field images: float RGB, premultiplied, `np.float16`, `skia.Image.fromarray(rgba, colorType=skia.kRGBA_F16_ColorType, alphaType=skia.kPremul_AlphaType)` (`fields.to_image`).
- Finish (`post_np`): vignette multiply, grain `N(0,1) * 0.010 * (0.35 + 2.6 * clip(lum*(1-lum), 0, 0.25))`, triangular dither `rand - rand`, floor to 8 bits.
- Plate fit (`orbmath.py`): edge per angle = largest brightness drop between 0.95 and 1.07 R, smoothed to 3 Fourier terms. Resample so the edge sits at 1. Fit Fourier K=4 per radius separately inside (0 to 0.996) and outside (1.004 to 1.45), savgol window 21, cubic spline, 8192-step table. Join with `clip(r_px - R + 0.5, 0, 1)`. Rim gain band `exp(-((1-r)/0.014)^2)` inside only. Soft shoulder `0.8 + 0.2 * tanh((x-0.8)/0.2)` above 0.8.
- Evaluate each side only where it shows (`inside = r_px < R+1`, `outside = r_px > R-1`). Cache one orb image per frame key `(frame, cx, cy, R, rot, full, form, spark)`.
- Banding QC: stretch dark crops 5 to 7 times and look for steps, in the source PNG and in a frame decoded from the MP4.

## D. LIVING GRADIENTS
- `fields.mesh(t, w, h, colors, speed, seed, res)`: 3 to 5 color sources on orbits `(0.5 + 0.42 cos a, 0.5 + 0.38 sin 1.3a)`, coordinates warped by `0.18 sin(y*3.1 + t*0.9) + 0.08 sin(y*7.3 - t*1.3)` (and the same for y), weights `exp(-2.2 * d^2)`. Computed at 1/4 size, upscaled bicubic in float.
- `fields.horizon(t)`: plate color curve (`HLUT`) along an effective height `y + (118 + 22 sin 0.55t) u^2 + ripples`, magenta and blue lobes running along the horizon, drifting sky light.
- Rim comet: ONE path segment from `PathMeasure.getSegment` with a linear gradient tail to head. A wrap past the path start is two separate paths (skia-python drops the first piece when both go into one path). Card loop 3.4 s, chip 2.6 s, tail 15 to 25%.
- Sweep rim: `GradientShader.MakeSweep` with a rotation matrix, 38 deg per second, stroke 1.4 px, 60%.
- Orb swirl: drift per wave k = 1..4 of 18 / 38 / 50 / 55 deg, speeds 0.70 / 0.55 / 0.80 / 0.50.

## E. CARDS, CHIPS, BUTTON (a client values)
- `glass_card`: under-glow (offset 18 px blur 34 `#7B4DFF` 30%, offset 26 px blur 70 `#4F2BD0` 22%), body stops `#0B0616` 0, `#0E0721` 0.50, `#3B2394` 0.76, `#9C7CF2` 0.92, `#D9C2FF` 1.0 (floor breathes 3%), mesh in screen blend 26%, `inner_flow`, sweep rim.
- `spring(u)`: `1 - exp(-zeta w u)(cos(wd u) + zeta w / wd sin(wd u))`, zeta 0.68, w 10 (about 5% overshoot).
- Morph: container rect springs. Old content out u 0 to 0.35 (blur to 6 px, scale to 0.97). New content in u 0.35 to 0.75 (rises 14 px, blur clears). Content at native size, clipped 2.5 px inside the rim.
- Entry: card slides 300 px, scale 0.94 to 1, over 0.6 s. Chip drops 36 px, scale 0.9 to 1.
- Button: press to 0.94 over 2 frames. Release `1 - exp(-5u)(0.06 cos 12u - 0.14 sin 12u)` (peak about 1.08). Flood circle from the click point over 0.42 s with a white ring, magenta and violet glow bloom, mesh fill `#6A3CF0 #C04CFF #FF6FD8 #4F6BFF`. Sound: tick + thump 62 Hz + shimmer.
- Research values (28 Sep 2026): press 0.97, hover 1.04, stiffness 400, damping 15 (Framer Motion practice). Material container transform: fade modes IN, OUT, CROSS, THROUGH.
- Glass cards are code, from the design's own recipe (blur sigma = Figma radius / 2). A past rebuild got a card's color wrong (28 Sep 2026), so one card is checked against the design render first. Method: `02_Technical/Program Instruction/Figma/how-to-rebuild-a-figma-frame-in-code.md`.

## F. EASING ROLES
reveal-primary, reveal-secondary, travel-heavy, travel-light, settle, exit-decisive, camera-glide, impact-accent, ambient. Describe the velocity in words first (start, peak, braking, landing), then pick the math: power, expo, cubic Bézier, spring, piecewise, hold, linear. Hero moves: 3 to 6 truly different candidates on the real element, picked by eye. Position leads scale. Blur clears on landing. Shadow and glow lag the body.

## G. SOUND
- Layers per hit: sub + body + transient. Hits on a VO word stay sub-heavy. Big hits in VO gaps. Whooshes start before the cut. Risers stop dead on the cut. Silence before the biggest reveal.
- Music 12 to 15 dB under the VO, ducked 7 dB more while the VO speaks. SFX ducked too, 10 dB under the VO above 300 Hz. Master -14 LUFS, -1 dBTP, soft-knee limiter.
- Synth kit (`audio_template.py`): whoosh (STFT band sweep), sub boom, hit, tick, glass ping, sonar, riser, reverse swell, shimmer, thump, pad (detuned saws, low-passed), pluck, stereo reverb send.
- Chain mode for stitching: env `OFFSET` (part start in the film), `TOTAL` (film length), `STEMS_OUT` (folder). Writes pre-master `vo`, `sfx`, `music` stems on the whole-film timeline.

## H. FIGMA EXPORT WALLS (tested 27 Sep 2026)
- `download_assets` PNGs are opaque. Two-pass matte: clone into a temporary off-canvas frame, black fill, export, white fill, export, delete. alpha = 1 - (white - black), color = black / alpha.
- `use_figma` output truncates at 20 KB. Return node IDs and bounds only. Fetch files by `download_assets` URL and `curl`.
- Text: temporary text nodes in one temporary frame, export the frame as SVG once, delete it. Nodes outside the frame bounds export as null.
- Exports of a layer inside a frame are clipped by it. Clone the layer out when its glow must be whole.
- Temporary nodes are named `_TMP_EXPORT_CLAUDE ... (temporary, delete)`, sit far off-canvas, and are deleted in the same step.
- skia-python has no SVG path parser: use `svgelements`. MaskFilter blur follows the canvas scale.

## I. DELIVERY ON THE MAC (29 Oct 2026)
- A render is written straight into its job folder and reaches him as a file card plus its full path (his ok). The card's Show in Finder button opens the folder. The file stays on disk, at any size: no pieces, no copy, no preview encode.

## J. STITCH
`stitch.py stitch.json` with `{"fps":30,"out":"FILM.mp4","crf":14,"parts":[{"name":"P1","dir":"P1","mezz":"P1/..._MEZZ_v6.mp4","audio":"audio2.py","frames":897}, ...]}`. It checks frame counts, runs each part's audio in chain mode on one timeline, masters once, concatenates the MEZZ files and encodes once. Tested: P1 + P1 = 1794 frames, -14.0 LUFS, about 5 min for 60 s.
- Each join is composited on its own part's edge frames (`STITCH/tr.py`). The film encodes once, with section keyframes (A). Moved 29 Sep 2026.

## K. TOOL CHOICE AND REVISION MAP
- Default: Python + skia-python + numpy. Remotion or HTML + GSAP with frame capture for text-heavy UI jobs with local fonts. Seedance or other video models only on his ask (paid: ask first).
- "It lags": an easing curve. "Make it pop": more contrast on the hero, in the piece's own look. "The logo looks glitchy": an interpolated snap. "Text is off": SYNC. "Low res" or "smoke": FIELDS or ASSETS. "Not animated": the drift is too small to see.
- "Hard edge in the gradient" (a client v6, 28 Sep 2026): a field went above 1.0. Skia clamps it where anything is drawn over it with Plus (a hard box the size of the blur bounds), and a clip after the vignette draws a hard curve. Keep every field under 1 with a soft shoulder, never hard-clip in post.
- "The glow is cut off": a Lighten blend hides the glow on a bright ground. Draw light with Screen. A forming ring needs circular angle distance at its seam.
- "Ghost copies" on fast objects: raise the shutter samples for that shot (8 to 12), not the whole film.
- NOTE MECHANICS (moved 29 Sep 2026). Encode the new frames with the master settings (A). With section keyframes: swap the section into the master (concat demuxer `-c copy`, in Bash on his drive). Without them: re-join the MEZZ files with the stitch (about 10 min, no render) and add the keyframes. The master takes the next version number. The old one stays where it is, never in `4_RENDERS/`. Same frame count: the stems stay. A new length: the sound is rebuilt on the whole timeline.
- TIME ESTIMATE (old 2 CPU cloud box, 28 Sep 2026): 1.4 to 2.9 s a frame at 1080p, 3.4 s with heavy blur, plus the join. The Mac has 16 cores: time 3 frames there first.
- Stop a render by PID (`$!`), never `pkill -f`.

## L. FINAL DELIVERY FILES (moved from the SKILL.md, 29 Sep 2026)
- VIDEO BG (no text): 1920 x 1080, 30 fps, H.264 High, no audio, section keyframes. To `1_VISUAL ASSET/*From Claude/FINAL_V<n>/Claude_<Client>_<Project>_FINAL_V<n>_BG.mp4`.
- VIDEO TEXT (big text only, with its glow and shadow): ProRes 4444 `.mov` with a transparent background (ffmpeg `prores_ks`, `yuva444p10le`), same frames and keyframes. `..._FINAL_V<n>_TEXT.mov`. He puts it on the track above BG. A black-background MP4 for a blend mode only on his ask: then say that Screen drops the dark shadow under the labels.
- VO, SFX, MUSIC: WAV, 48 kHz, 24-bit, as in the approved mix (levels, ducking baked in). To `3_SOUND ASSET/*From Claude/FINAL_V<n>/Claude_<Client>_<Project>_FINAL_V<n>_VO.wav`, `_SFX.wav`, `_MUSIC.wav`. A VO taken from his MP4 [R24] is decoded to this WAV as it is.
- Checks: TEXT over BG matches the approved picture (a composite test on 5 frames per section). The TEXT file opens with transparency. The stems add up to the approved mix. Every file md5-checked on the drive.

## M. SECTIONS (moved from the SKILL.md, 29 Sep 2026)
- The next full encode builds the section keyframes (A). Each cut is frame-exact, no fade.
- Map `**_MOTION/_STATE/SECTIONS.md`: one row per section, with frames, timecode, shots, the part build and its frames.
- Section files, on his ask: stream copies in `FINAL_V<n>_SECTIONS/` beside the master, `..._SEC-01_V1.mp4`. Video only, stems stay whole. The BG and TEXT layers split at the same frames.

## N. MOTION APP METHODS (a client Scene 2B, tested 2 Oct 2026)
- PATHS: MOTION cannot read a media path with `#` (it builds a file:// address with encodeURI, which leaves `#` as is). The media lives in `<project>/*_PROJECT FILES/**_MOTION/<FILM>/media/`. MOTION reads it through a link with no `#`: `ln -s "<that media path>" ~/Movies/MOTION/media/<FILM>`, and every `src` points at the link. Tested 2 Oct 2026 on SCENE-2B V4: clips and map load. The fix in the app: encode `#` and `?` in that address, then drop the links.
- GLOW WITH NO CUT (R35): a card glow is a nine-slice of a canvas `shadowBlur` gaussian (inner box 360 px). A dot glow is a radial-gradient sprite that fades to zero. Never a PIXI BlurFilter: its filter box cuts the glow. Never stacked strokes. A MeshRope halo folds into wedges at a sharp turn, and its square end cuts hard where two ropes meet at a dot. A thin map line takes no halo (the storyboard has none).
- THE QC CROP (R35): snapshot the frame, then crop each card corner, each line join and each line end at 400% (PIL, Lanczos). Look for a hard edge, a wedge, a step or a box. Then the same crop of the Figma frame beside it.
- SHADERS: `vTextureCoord` is not 0..1 over the layer, so no geometry in a shader. Use a shader for ambient light only. Shader blend `screen` fails: output premultiplied `vec4(col, 0.0)` for added light.
- ADD BLEND: an image on `add` needs a black ground. A Figma export with a navy ground: subtract that color in the PNG first, or it shows as a box.
- BORDERS: one FillGradient stroke, aligned inside. Round caps on each segment make a dotted line.
- CLIPS IN SMALL CARDS: a 1080p CRF 12 proxy (ping-pong where it must loop), mipmaps on (MOTION V0.16). Live playback is native from V0.16.
- MAP CAMERA: screen = Z x map + (BX, BY). Every map layer is keyed from the same three numbers, so the map moves as one picture. Code layers take CamZoom, CamX, CamY.
- TEXT: animated rich text does not wrap. A two-line name is a second text layer that takes over.
- STORYBOARD GEOMETRY (R34): `get_metadata` on the storyboard section gives each line, dot and tile in pixels (`leader_<C> (line + dot)`, `thread`). Copy those numbers. Then check each dot against the map pixels: it must sit inside its country.

## O. FIGMA MOTION METHODS (a client Scene 2B v1 to v3, tested 2 Oct 2026)
- BUILD ON A COPY: clone the storyboard end frame into a new section, below the lowest node on the page. Key every element against its resting place in that frame.
- CARDS: key WIDTH, HEIGHT and TRANSLATION on the card frame. Children follow by constraints: scrim STRETCH plus SCALE, shade STRETCH, name MIN, coordinates MIN plus MAX, corner marks on their own corner.
- SCALE GOES ABOUT THE CENTER: SCALE_XY grows a node from its center. To keep a top-left anchor, add (s - 1) x w / 2 to TRANSLATION_X and (s - 1) x h / 2 to TRANSLATION_Y.
- LINE DRAW (PATH_TRIM): it runs only on an open path. A closed outline needs `setVectorNetworkAsync` with a 0.6 px gap and CENTER stroke. A light that runs around the border keys PATH_TRIM_START behind PATH_TRIM_END.
- GLOW: a second DROP_SHADOW on the card, keyed by `effects` index 1 (RADIUS and COLOR, alpha included). Turn the card's `clipsContent` off so the glow spills outside. A ring's stroke grows with its scale, so key STROKE_WEIGHT down as it grows.
- CAMERA: move every scene layer into one `CAMERA` frame. Its tracks survive the move. Key damped TRANSLATION_XY hits about 34 ms apart, ROTATION under 0.4 degrees on the big beat, and a steady 1.015 scale so no edge shows. The HUD stays outside the camera.
- STEPS: a PATH_TRIM progress line needs keys that only climb. Overlapping steps make it jump back.
- TEXT: the plugin sees only fonts on Figma's servers (DM Mono worked). Brand fonts can be cloned and moved, not typed.
- CLIPS AND AUDIO: the connector places pictures only. He drops each clip on the card's fill. The VO goes in as an MP4 (navy picture, AAC sound) dropped on a bottom rectangle. Whether its sound plays on the Figma timeline is unverified.
- CHECK: `export_video` at low quality, 1280 wide, 10 fps, then ffmpeg stills. The file stays on Figma's server for one hour, never on his disk or in the chat.
