---
name: references-color-grading
description: 'Reads the colour grade of a still or a video the way a senior colourist would: the contrast curve with its toe and shoulder, black level and highlight roll-off, the split tone (shadow hue against highlight hue), saturation by luminance zone, skin placement on the vectorscope, the film stock or print family it sits in (print emulation, bleach bypass, teal and orange, halation), SDR or HDR, log or graded, and how the look holds or drifts across shots. Measures with ffmpeg scopes and signalstats, ffprobe colour fields and a Lab read in Python. Writes a grade sheet with a node order for DaVinci or Lumetri, a LUT when a before and after exist, and prompt lines. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when the router picks it for a dropped look with this grade, this colour, this film look, match this, LUT, or a colour reference for a film or image. One still''s light and lens are llllloc:references-photo; the cut is llllloc:references-edit.'
---

# llllloc:references-color-grading (17 Oct 2026, his words: "should i add one for colorgrading reference as well" then "Option A")

A grade is a curve and a colour system, applied to every shot. It is read as numbers on scopes first, then as the colourist's decisions: where the blacks sit, how the highlights roll off, which hues live in the toe and the shoulder, where the skin sits, what was taken out. The output is a grade sheet: a new film or image can be graded or prompted to the same system. A still's light, lens and composition: `llllloc:references-photo`. The shot's camera: `llllloc:references-cinematography`. The cut: `llllloc:references-edit`. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. Scopes before adjectives. "Moody" and "cinematic" are not findings; "blacks lifted to Y 28 of 255, highlights rolling off from the 90th percentile at 196 to a max of 221, shadows at hue 215° and highlights at 48°, a 167° split" is.
2. Read the curve as a shape: toe, midtone slope, shoulder, where it clips. Then the colour on top of it: the split tone, the saturation by zone, the cast. A look is the curve plus the split; the palette of the scene is the art direction, not the grade.
3. Skin is the anchor. Report where skin sits (luminance range and vectorscope angle against the skin line) before anything else, because every other choice is made around it.
4. Mechanism transfers, material by ownership. The curve, the split, the saturation map, the stock family, the grain and halation recipe all transfer to new footage. His own and a client's footage and stills are graded as given; an outside reference supplies its system, its images come in when he says so. No legal rule caps a job (his words, 17 Oct 2026).

## MEASURE (run first, raw output to `_batches/`)

```
brew install ffmpeg; pip install opencv-python-headless numpy scikit-image scikit-learn colour-science    # once (ask first, core rule 1)
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt,color_range,color_space,color_transfer,color_primaries,bits_per_raw_sample -of default=nw=1 <file>   # tv or pc range, bt709 or bt2020, smpte2084 (PQ) or arib-std-b67 (HLG) = HDR, 10-bit
ffprobe -v error -show_frames -read_intervals "%+#1" -select_streams v -show_entries frame=side_data_list -of json <file> | grep -i -A3 "mastering\|light level"   # HDR mastering and MaxCLL when present
ffprobe -f lavfi -i "movie=<file>,signalstats=stat=brng" -show_entries frame=pkt_pts_time:frame_tags=lavfi.signalstats.YMIN,lavfi.signalstats.YLOW,lavfi.signalstats.YAVG,lavfi.signalstats.YHIGH,lavfi.signalstats.YMAX,lavfi.signalstats.UAVG,lavfi.signalstats.VAVG,lavfi.signalstats.SATAVG,lavfi.signalstats.HUEAVG,lavfi.signalstats.BRNG -of csv=p=0 > signal.csv   # per frame, average per shot
ffmpeg -ss <t> -i <file> -frames:v 1 -vf "waveform=mode=column:intensity=0.1:graticule=green:flags=numbers:scale=ire" wf_<n>.png     # one per key shot
ffmpeg -ss <t> -i <file> -frames:v 1 -vf "vectorscope=mode=color3:graticule=color:flags=name+white:intensity=0.1" vs_<n>.png
ffmpeg -ss <t> -i <file> -frames:v 1 -vf "histogram=display_mode=parade:levels_mode=logarithmic" hist_<n>.png
python3 - <<'EOF'   # the grade as numbers, one frame or still (run on 3 to 10 frames per shot and average)
import cv2, numpy as np
from skimage.color import rgb2lab, rgb2ycbcr
from sklearn.cluster import KMeans
im = cv2.imread("<frame>"); rgb = cv2.cvtColor(cv2.resize(im, (480, int(im.shape[0]*480/im.shape[1]))), cv2.COLOR_BGR2RGB)/255.
lab = rgb2lab(rgb); L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]; C = np.hypot(a, b)
p1, p25, p50, p75, p99 = np.percentile(L, [1, 25, 50, 75, 99])
print(f"L: black p1 {p1:.1f}  mid p50 {p50:.1f}  white p99 {p99:.1f}  range {p99-p1:.1f}  mid slope {(p75-p25)/50:.2f}  (toe lifted if p1 > 6, shoulder soft if p99 < 92)")
def hue(mask): return (np.degrees(np.arctan2(b[mask].mean(), a[mask].mean())) % 360, C[mask].mean())
sh, hi = hue(L < np.percentile(L, 10)), hue(L > np.percentile(L, 90))
print(f"split tone: shadows hue {sh[0]:.0f}° C {sh[1]:.1f}  highlights hue {hi[0]:.0f}° C {hi[1]:.1f}  split {abs((hi[0]-sh[0]+180)%360-180):.0f}°  (teal/orange ~ shadows 200-260°, highlights 40-80°)")
print("chroma by zone:", " ".join(f"L{lo}-{hi_} {C[(L>=lo)&(L<hi_)].mean():.1f}" for lo, hi_ in ((0,25),(25,50),(50,75),(75,101))))
print(f"cast: mean a {a.mean():+.1f} (red+/green-)  mean b {b.mean():+.1f} (yellow+/blue-)")
ycc = rgb2ycbcr(rgb); skin = (L > 35) & (L < 75) & (a > 8) & (a < 30) & (b > 10) & (b < 40)
if skin.sum() > 200: print(f"skin: {skin.mean()*100:.0f}% of frame  L {L[skin].mean():.0f}  vectorscope angle {np.degrees(np.arctan2(ycc[...,2][skin].mean()-128, ycc[...,1][skin].mean()-128))%360:.0f}° (skin line ~123°)")
km = KMeans(6, n_init=4, random_state=0).fit(lab.reshape(-1, 3)[::10]); sh_ = np.bincount(km.labels_)/km.labels_.size
from skimage.color import lab2rgb; print("palette:", " ".join(f"#{''.join(f'{int(v*255):02X}' for v in np.clip(lab2rgb(c.reshape(1,1,3))[0,0],0,1))} {s*100:.0f}%" for c, s in sorted(zip(km.cluster_centers_, sh_), key=lambda t: t[0][0])))
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(float); print(f"grain: shadow noise {cv2.Laplacian(g, cv2.CV_64F)[g < 60].std():.1f}  highlight noise {cv2.Laplacian(g, cv2.CV_64F)[g > 180].std():.1f}")
EOF
```

- Per shot: average the signalstats keys between cut points (shot list from `llllloc:references-edit` or `scenedetect`). Plot YAVG, YLOW, YHIGH, SATAVG, UAVG, VAVG per shot. A step shared by every shot after a cut cluster is a scene-level look change; one shot more than about 1.5 MAD from its scene's median is a match issue, and say which.
- Readings: YMIN near 16 with YLOW close to it is crushed; YLOW well above 16 is lifted or milky. YMAX at 235 with YHIGH close to it is clipped; YMAX under 235 with a soft YHIGH is a roll-off. BRNG above 0 on a tv-range file is out of legal. UAVG above 128 leans blue, VAVG above 128 leans red or magenta.
- Log tell: histogram bunched in the middle, YMIN far above 16, YMAX far below 235, SATAVG very low, `color_transfer` unset or bt709. S-Log3 puts 18 percent grey near 41 percent; ARRI LogC4 near 28 percent. A graded Rec.709 file uses the 16 to 235 span with a visible toe and shoulder.
- Halation: a red or orange fringe only around clipped highlights (CineStill 800T, or a Resolve halation node); bloom is a neutral glow. Gate weave is a slow 1 to 3 px drift of the whole frame.
- A before and after of the same frame: `pip install lut-estimator` fits a 3D LUT and writes a `.cube`; or a 3x3 matrix plus per-channel curve in numpy, exported as `LUT_3D_SIZE 33` (red fastest). Apply with `ffmpeg -vf "lut3d=file=look.cube:interp=tetrahedral"`. From one graded image alone no tool recovers the LUT: the sheet carries the system instead, and says so.

## THE PRO READ

| Field | What to write |
|---|---|
| PIPELINE | SDR or HDR (PQ or HLG, MaxCLL when present), range, primaries, bit depth, log or graded, the likely camera log when the footage is flat. |
| CURVE | Black point, white point, midtone slope, toe shape (crushed, straight, lifted, milky), shoulder (hard clip, soft roll-off, where it starts), the contrast in one line, from L percentiles and YLOW, YHIGH. |
| SPLIT TONE | Shadow hue and chroma, highlight hue and chroma, the split in degrees, the midtone cast; named when it is a known pair (teal and orange, cyan shadows with warm highlights of a print emulation, cool and clean, warm and dense). |
| SATURATION | Chroma by luminance zone, the saturation curve shape (pulled in shadows, held in mids, pulled in highlights), the one hue allowed to stay strong, global saturation against the scene's palette. |
| SKIN | Luminance range, vectorscope angle against the skin line, consistency across faces, whether skin was isolated (secondary) from the look. |
| STOCK FAMILY | The family the look sits in with its tells: print emulation (dense blacks, neutral highlights, S curve with split in toe and shoulder, gamut compression), bleach bypass (high contrast, low saturation, dark shadows, grain), lifted film, digital clean, HDR bright. Name it as a family, never a certainty, with `~`. |
| TEXTURE | Grain amount and where it lives (shadow noise against highlight noise), grain size, halation, bloom, softening, gate weave, vignette. |
| ACROSS SHOTS | The scene-level looks as time ranges, how the system changes between scenes (warmer, denser, desaturated for the turn), the match issues by shot. |
| WHAT MAKES IT LAND | The three to five choices with their numbers (Cullen Kelly: a look is a curve, a split and a saturation map, held). Also what reads generic: one orange and teal on everything, a LUT on log with no balance first, lifted blacks with no reason, saturation pulled everywhere. |

## THE GRADE SHEET

The dossier (`llllloc:references`) carries what recurs across his references. The sheet is the usable part, written to the job's `*_CLAUDE/2_References/GRADE_<name>.md` (or beside the dossier when no job is named):

```markdown
# GRADE <name>                <date> · built by llllloc:references-color-grading
## PIPELINE      SDR/HDR, range, primaries, bit depth, log or graded
## CURVE         black, white, mid slope, toe, shoulder (numbers with source)
## COLOUR        split tone, cast, chroma by zone, skin placement, palette hexes
## FAMILY        stock or print family with its tells, marked ~
## TEXTURE       grain, halation, bloom, vignette
## ACROSS SHOTS  the looks by scene, the match issues
## NODE ORDER    for DaVinci: CST in (log to DaVinci Wide Gamut or ACEScct) > balance (offset) > primary contrast and saturation > secondary skin > look (curves, split tone) > print emulation > grain and halation > CST out. For Lumetri: Basic (white balance, tone, blacks and whites) > Curves (RGB, hue vs sat) > Color Wheels (shadow and highlight tint for the split) > HSL Secondary (skin) > Creative (Faded Film, Look LUT) > Vignette. Each step with its target number from above.
## LUT           the .cube when a before and after exist, else "system only"
## PROMPT LINES  for llllloc:task-prompt: the curve in words (dense blacks, soft highlights), the split in two hues, the saturation map, skin warm and held, the texture; no stock name unless he asks
## OPEN          frames not measured, family not sure, skin not found
```

## RESEARCH (with `llllloc:task-research`)

The colourist and the facility (credits, Shots, LBB, the DP's interview), the DP's intent (the camera, the lenses, the log), the look's trade name and lineage (print emulation and the stocks it imitates, bleach bypass, the CineStill halation, a known LUT family), the colourist's own breakdown or talk (Mixing Light, Lowepost, Cullen Kelly, the SMPTE print-stock article, a Resolve or Lumetri tutorial that rebuilds it), whether it is durable or a trend of the year, what breaks when copied (a LUT on unbalanced log, split tone with no skin secondary, grain added before the shoulder). Cache: `llllloc/5_Research cache/jobs/reference-analysis.md`.

## WHAT TRANSFERS, WHAT DOES NOT

Transfers: the curve shape, the black and white placement, the split tone, the saturation map, the skin placement, the stock family and its node order, the texture recipe, the way the look changes between scenes. Does not, from an outside reference: its footage, its palette as art direction (the colours of the set and costumes are a design choice, not the grade), unless he asks. From his own or a client's footage: everything.

## HAND-OFF

`llllloc:tool-premiere-pro` builds the NODE ORDER in Lumetri on his footage; a `.cube` goes in as a Look or an Input LUT. `llllloc:task-prompt` uses PROMPT LINES for an image or video prompt. `llllloc:tool-magnific` uses the curve and split for an upscale's colour. `llllloc:task-colorist` owns the grading itself (21 Oct 2026); this skill only reads. The same film often loads `llllloc:references-cinematography` (the shot) or `llllloc:references-edit` (the cut), and the sheets cross-reference by shot number.
