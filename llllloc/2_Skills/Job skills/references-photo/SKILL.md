---
name: references-photo
description: 'Reads a still reference (photo, render, key visual, one film frame) the way a director of photography and a retoucher would: light, lens, color, composition, texture and world, measured with tools before judged by eye. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when /llllloc:router picks it for a dropped image to analyze or learn from, a look to follow in an image prompt or render, or ''is this good'' on a still. Never for a layout, poster, deck page or UI screenshot: that is llllloc:references-design. A drawn or painted picture is llllloc:references-art.'
---

# llllloc:references-photo (split from llllloc:references, 17 Oct 2026)

A still is read as light on a subject through a lens, recorded on a medium. A drawn or painted picture (illustration, concept art, animation frame) is `llllloc:references-art`; a grade as a system is `llllloc:references-color-grading`. The output is the mechanism, so a new subject can be lit, framed and graded the same way. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. Light first. Where the key is, how hard, how much fill, what the shadows agree on. A wrong light read makes every other field wrong, and the prompt or the shoot built on it fails.
2. Numbers from tools, direction from eyes. Hexes, shares, value split, sharpness, grain and EXIF come from the commands below. Light direction, ratio and lens are read by eye and marked `~` with the evidence that supports them.
3. The recipe names mechanisms, not "recreate this frame". A frame rebuilt one to one on a new subject is a copy, not a look. When he or the client wants the frame itself, say so in the sheet and do it.
4. The dossier names the technique and the lineage, not only an artist's name, because a name alone gives a generic copy and teaches nothing. A name he asks for stays in.

## MEASURE (run first, raw output to `_batches/`)

```
exiftool -j -n -FocalLength -FNumber -ISO -Model -LensModel -FocalLengthIn35mmFormat <file>      # camera facts when present
python3 - <<'EOF'   # palette with share, value split, sharpness, grain
from PIL import Image; import numpy as np
im = Image.open("<file>").convert("RGB"); w, h = im.size; print("size", w, h, "aspect", round(w/h, 3))
q = im.quantize(colors=6, method=Image.Quantize.MEDIANCUT); pal = q.getpalette()
for n, i in sorted(q.getcolors(), reverse=True): print("#%02x%02x%02x" % tuple(pal[i*3:i*3+3]), round(100*n/(w*h), 1), "%")
g = np.asarray(im.convert("L")); hist = np.bincount(g.ravel(), minlength=256)
print("shadows", round(100*hist[:64].sum()/g.size), "mids", round(100*hist[64:192].sum()/g.size), "highlights", round(100*hist[192:].sum()/g.size))
EOF
python3 -c "import cv2;g=cv2.imread('<file>',0);print('sharpness',round(cv2.Laplacian(g,cv2.CV_64F).var()))"
python3 -c "from skimage.restoration import estimate_sigma;from skimage.io import imread;print('noise sigma',round(float(estimate_sigma(imread('<file>'),channel_axis=-1,average_sigmas=True)),2))"
```

Install lines when missing: `pip install pillow opencv-python-headless scikit-image`, `brew install exiftool` on his Mac (ask first, core rule 1). No EXIF and the lens matters: GeoCalib (github.com/cvg/GeoCalib) estimates field of view and roll from one image; otherwise the lens is `~` with its evidence. A possible AI image: check Content Credentials (contentcredentials.org) and say what it showed.

## THE PRO READ

| Field | What to write |
|---|---|
| MEDIUM | Photograph, 3D render, oil, cel, ink, collage, AI image. Never "artwork". |
| SUBJECT | What is in the frame, five words. |
| COMPOSITION | Where the subject sits, what the eye hits first, second, third. Headroom, negative space, aspect ratio. |
| VALUE | The measured shadow, mid and highlight split. Focal contrast, or flat. |
| LIGHT | Key direction from the shadow side and the catchlight shape (the catchlight is the modifier). Hard or soft from the shadow edge: sharp is hard, a long gradient is soft. Key to fill ratio by eye: 2:1, 4:1, 8:1 (one, two, three stops). Non-black shadows mean fill. Fast falloff means a close source. Practicals. Whether all shadows agree. |
| COLOR | The temperature that runs the frame, where saturation sits, the measured hexes with shares. |
| LENS | Focal length with its evidence (perspective, compression, distortion, EXIF when present), depth of field, focus plane. |
| EDGE | Sharp where, soft where, the sharpness number. Uniform sharpness is a finding. |
| ATMOSPHERE | What each depth plane does: haze, smoke, falloff. |
| TEXTURE | Grain, halftone, brush, noise, clean. The noise number. Name the process. |
| REGISTER | How stylized, photoreal to graphic. |
| LORE | The world it implies: era, place, culture, what happened before this frame. The field a client buys. |

## RESEARCH (with `llllloc:task-research`)

The photographer, DP or studio and their stated method; the technique name (for example "Rembrandt key", "shoot-through diffusion", "mixed tungsten and daylight"); the camera, lens and film or render engine when the maker said; whether the look is a durable craft or a dated trend; what fails when people copy it (muddy shadows, flat fill, fake grain). Cache: `llllloc/5_Research cache/jobs/reference-analysis.md`.

## WHAT TRANSFERS, WHAT DOES NOT

Transfers: the light logic, the ratio, the lens behavior, the palette structure, the value split, the texture process, the framing rule. Does not, from an outside reference: the subject, the location, the model, a signature prop, unless he asks for it. From his or a client's picture: everything, the face and the product included.

## HAND-OFF

`llllloc:task-prompt` IMAGE builds the prompt from the dossier's light logic, material, palette and framing, as intent, not tags. `llllloc:tool-magnific` runs the renders. `llllloc:task-art-direction` uses LORE for a treatment. CRITIQUE of an image also loads `llllloc:task-prompt/references/visual-quality.md`.
