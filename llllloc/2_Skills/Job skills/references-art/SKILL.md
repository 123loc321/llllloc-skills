---
name: references-art
description: 'Reads an art reference (illustration, drawing, painting, concept art, character design, an animation frame, a comic or manga page, a book page, an ArtStation piece) the way a senior illustrator and an animation art director would: shape language and silhouette, line weight and lost and found edges, value grouping as a notan, palette and gamut mask, edge softness, rendering technique and medium, stylization level, proportion in heads, appeal, composition, and the printed or studio devices (halftone, line boil, twos). Measures line, values, palette and medium with OpenCV and CLIP. Writes an art sheet an image prompt, a character brief or a style frame can be built from. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when the router picks it for a dropped drawn or painted picture with analyze, this style, draw like this, or an art reference for a new image. A photographed still is llllloc:references-photo; a layout is llllloc:references-design.'
---

# llllloc:references-art (17 Oct 2026, his words: "reference for illustration, drawing, painting art as well: art station, disney, spiderman")

A drawn or painted picture is read as decisions: what shapes were chosen, how the line behaves, how the values are grouped, which colours were allowed in, how much the real was pushed. The output is an art sheet: a new piece can be drawn, prompted or art-directed the same way. A photographed still (light, lens, grade): `llllloc:references-photo`. A grade as a system: `llllloc:references-color-grading`. A moving animation's timing: `llllloc:references-motion`. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. Name the device, not the studio. "Pixar style" and "Disney look" are not findings; "six heads tall, round shape family, cel shade with one soft terminator, saturated local colour under one warm key" is. A studio name in a prompt collapses to a generic blend; the devices transfer.
2. Measure what can be measured, then read the rest by eye and mark it `~`. Line width, value shares, palette, hue spread, edge ratio and the medium score come from the commands below. Appeal, intent and lineage are read by eye.
3. Values before colour. The notan (two values) and the three to five value groups decide whether a piece reads; the palette sits on top. A piece that fails in two values is not saved by its colours.
4. Mechanism transfers, material by ownership. Shape family, line rules, value grouping, gamut, rendering and proportion all transfer to a new subject. His own and a client's characters, art, logos and books go into the work as given; an outside artist's subject and characters come in when he says so. No legal rule caps a job (his words, 17 Oct 2026).

## MEASURE (run first, raw output to `_batches/`)

```
pip install opencv-python-headless numpy scikit-image scikit-learn open_clip_torch torch pillow     # once (ask first, core rule 1)
python3 - <<'EOF'   # values, palette, gamut, edges, line width, halftone, one picture
import cv2, numpy as np
from skimage.morphology import skeletonize
from sklearn.cluster import KMeans
im = cv2.imread("<file>"); lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB); L = lab[..., 0].astype(float)
for k in (2, 3, 5):
    km = KMeans(k, n_init=4, random_state=0).fit(L.reshape(-1, 1)); c = sorted(zip(km.cluster_centers_.ravel(), np.bincount(km.labels_) / km.labels_.size))
    print(f"{k} values:", " | ".join(f"L{int(v*100/255)} {s*100:.0f}%" for v, s in c))
px = im.reshape(-1, 3)[::20]; km = KMeans(6, n_init=4, random_state=0).fit(px); shares = np.bincount(km.labels_) / km.labels_.size
print("palette:", " ".join(f"#{int(r):02X}{int(g):02X}{int(b):02X} {s*100:.0f}%" for (b, g, r), s in sorted(zip(km.cluster_centers_, shares), key=lambda t: -t[1])))
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); h = hsv[..., 0][hsv[..., 1] > 40].astype(float) * 2
if h.size: ang = np.deg2rad(h); r = np.hypot(np.sin(ang).mean(), np.cos(ang).mean()); print(f"gamut: mean hue {np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean()))%360:.0f}°, spread {(1-r)*100:.0f}% (0 tight mask, 100 full wheel), sat mean {hsv[...,1].mean()/2.55:.0f}%")
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); t = 64; v = [cv2.Laplacian(g[y:y+t, x:x+t], cv2.CV_64F).var() for y in range(0, g.shape[0]-t, t) for x in range(0, g.shape[1]-t, t)]
print(f"edges: hard tiles {np.mean(np.array(v) > 100)*100:.0f}% (Laplacian var > 100), soft {np.mean(np.array(v) < 20)*100:.0f}%")
bw = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8); sk = skeletonize(bw > 0); dt = cv2.distanceTransform(bw, cv2.DIST_L2, 5)
w = 2 * dt[sk]; print(f"line: ink {bw.mean()/2.55:.0f}% of picture, width median {np.median(w):.1f}px, p10 {np.percentile(w,10):.1f}, p90 {np.percentile(w,90):.1f} (taper = p90/p10)") if w.size else print("line: none found")
F = np.abs(np.fft.fftshift(np.fft.fft2(g.astype(float) - g.mean()))); cy, cx = np.array(F.shape)//2; F[cy-8:cy+8, cx-8:cx+8] = 0; py, px_ = np.unravel_index(F.argmax(), F.shape)
print(f"halftone/screen: peak at {np.hypot(py-cy, px_-cx):.0f} cycles, angle {np.rad2deg(np.arctan2(py-cy, px_-cx)):.0f}°, strength {F.max()/F.mean():.0f}x (above ~40x is a real screen)")
EOF
python3 - <<'EOF'   # medium and stylization by zero-shot CLIP
import open_clip, torch; from PIL import Image
m, _, pre = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k"); tok = open_clip.get_tokenizer("ViT-B-32")
def score(labels):
    with torch.no_grad():
        p = (100 * m.encode_image(pre(Image.open("<file>")).unsqueeze(0)) @ m.encode_text(tok([f"a {l}" for l in labels])).T).softmax(-1)[0]
    return sorted(zip(labels, p.tolist()), key=lambda t: -t[1])[:3]
print(score(["photograph","3D render","digital painting","oil painting","watercolor painting","gouache painting","ink drawing","pencil sketch","cel shaded illustration","flat vector illustration","comic book page","manga page","children's book illustration","pixel art"]))
print(score(["photorealistic image","semi-realistic illustration","stylized illustration","cartoon","abstract art"]))
EOF
```

- Line extraction on a painted piece with no ink: skip the line block and say so. For manga or anime line work, `Anime2Sketch` or `MangaLineExtraction_PyTorch` give a cleaner line layer before measuring width.
- Proportion: count heads by eye from chin to crown against the full figure (realistic 7.5 to 8, standard cartoon about 6, cartoony 3, chibi 2 to 3). MediaPipe Pose fails on stylized figures; do not report its numbers there.
- The CLIP score is a hint with its percentage, never a verdict; the medium is confirmed by eye (brush edge, paper grain, vector cleanness).

## THE PRO READ

| Field | What to write |
|---|---|
| SHAPE | The shape family per element (round safe, square stable, triangle danger), the silhouette test (does it read as a black shape), shape contrast between characters, the line of action, asymmetry. |
| LINE | Present or lineless; width median and taper from the measure; weight hierarchy (outer contour heavier, inner lines lighter); lost and found edges, where they are lost and why; line colour (black, darker local, coloured); hand feel (boil, wobble, pressure) or clean vector. |
| VALUE | The notan and the three to five groups with their shares; where the darkest dark meets the lightest light (the focal point); lights grouped with lights; how the shadow shape is designed, not copied. |
| COLOUR | Palette hexes with shares; the gamut mask (hue spread and centre), local colour versus global light, saturation by value zone, the one accent and its share, the colour script role of the piece when it is a frame. |
| EDGES | Hard to soft ratio from the measure, where the hard edges sit (focal area), soft on the silhouette or in depth. |
| RENDER | Technique (cel with n steps, painterly, lineless, flat, gradient mapped, impasto, dry brush, wash), medium real or imitated (poster colour, gouache, watercolour, oil, ink, pencil, digital), texture and paper, the brush economy (one stroke per form or blended). |
| STYLIZATION | Level from realistic to graphic in one line with its proof (proportion, simplification of hands and faces, outline). Proportion in heads. Where the real is pushed and where it is kept. |
| APPEAL | What makes the character or scene likeable or sharp: clear read, contrast of shapes, expression economy, pose thrust, one clear idea. |
| COMPOSITION | Focal point and eye path, framing device, the push and pull of the frame, where the piece breathes. |
| PRINTED AND STUDIO DEVICES | Halftone (frequency, angle), misregistered colour offset, hatching in shadows, motion lines and smears, animation on twos, painted textures over CG, 2D FX at 12 fps over 24 fps characters, lines drawn as geometry. Named by device, with its tell. |
| WHAT MAKES IT LAND | The three to five choices with their numbers. Also what reads generic: a studio name as the only style, symmetrical pose, every edge hard, full-wheel palette, seven values with no grouping. |

## THE ART SHEET

The dossier (`llllloc:references`) carries what recurs across his references. The sheet is the usable part, written to the job's `*_CLAUDE/2_References/ART_<name>.md` (or beside the dossier when no job is named):

```markdown
# ART <name>                <date> · built by llllloc:references-art
## SHAPE AND LINE   family, silhouette, line width and taper, edge rule
## VALUE            notan, groups with shares, focal contrast
## COLOUR           palette hexes with shares, gamut mask, local vs global, accent
## RENDER           technique, medium, texture, brush economy, stylization level, heads tall
## DEVICES          printed and studio devices with their numbers
## PROMPT LINES     for llllloc:task-prompt IMAGE: medium and rendering words, line rule, value rule, palette hexes, lighting, stylization level, proportion; no studio or artist name unless he asks; halftone and offset as a post step
## BRIEF LINES      for llllloc:task-art-direction or llllloc:task-design: the shape rules and value rules a new piece must keep
## OPEN             medium not sure, lines not measured, artist not found
```

## RESEARCH (with `llllloc:task-research`)

Find the piece and the artist first: Google Lens or TinEye on the file, then the ArtStation page (software used, tags, process posts) or the studio's "The Art of" book and talks (Cartoon Brew, fxguide, befores & afters, SIGGRAPH talks for a studio look); the technique by name (gamut masking, notan, lost and found edges, cel, poster colour); the artist's own process video or breakdown; whether it is a durable craft or a trend of the year; what breaks when copied (a studio name gives a blend, line weight words barely work in a prompt, halftone needs a post process, a palette without value grouping reads muddy). Cache: `llllloc/5_Research cache/jobs/reference-analysis.md`.

## WHAT TRANSFERS, WHAT DOES NOT

Transfers: the shape family, the line rules, the value grouping, the gamut mask, the edge rule, the rendering technique, the stylization level and proportion, the composition device, the printed devices as a post step. Does not, from an outside reference: the character, the subject, the artist's signature motifs, unless he asks for them. From his own or a client's art: everything, the characters included.

## HAND-OFF

`llllloc:task-prompt` IMAGE uses PROMPT LINES as intent: medium and rendering words first, line and value rules, palette hexes, stylization level, proportion, and a style reference image when the model takes one (Midjourney `--sref`, Nano Banana or Flux with the picture attached). `llllloc:task-design` and `llllloc:task-art-direction` use BRIEF LINES for a style frame, a character brief or a book look. A piece that is also a photo-like render loads `llllloc:references-photo` for its light; a frame from a film also loads `llllloc:references-motion` for its timing.
