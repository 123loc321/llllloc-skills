---
name: references-space
description: 'Reads a space reference (architecture, a facade, an interior, a room, a shop, a set, props, a landscape, a location) the way an architect, an interior designer and a production designer would: what the picture is OF: camera height and lens from the geometry, scale from a door or a chair, massing, rhythm, materials with finish and age, zones, the light plan with sources and Kelvin, the palette with roles, hero props and dressing, style tells, sun and time of day. Writes a subject sheet a prompt, a set build, a location brief or an interior plan can be built from. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when /llllloc:router picks it for a dropped picture of a building, room, set or place to analyze, learn from or use as a space in new work. How the picture was lit and shot is llllloc:references-photo.'
---

# llllloc:references-space (17 Oct 2026, his words: "architecture, interior design as well")

A space is read as what it IS: how big, how built, what it is made of, how it is lit, how it is dressed, where the camera stood. The output is a subject sheet: a new room, set or building can be described, prompted or built from it. Light, lens and grade of the picture itself: `llllloc:references-photo`. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. Scale before style. Find the horizon and one known height (a door, 2.0 to 2.1 m) first. Camera height, ceiling height and room depth follow. A room described without scale cannot be rebuilt or prompted.
2. Materials with finish and age, never "concrete". Board-formed or polished, new or weathered, honed or glossy. The finish is what reads premium or cheap.
3. Light as a plan, not a mood. Count the sources, name the kind (ambient, task, accent, practical, daylight), the direction and the Kelvin. "Warm and cozy" is not a finding.
4. Name the mechanism, not the landmark. A famous building or architect in a prompt pulls the model to that signature and gives a generic copy. The sheet writes massing, rhythm, material, light and camera instead.

## MEASURE (run first, raw output to `_batches/`)

```
pip install lu-vp-detect opencv-python-headless transformers torch pillow astral        # once (ask first, core rule 1)
python3 - <<'EOF'   # vanishing points, horizon, tilt
import cv2; from lu_vp_detect import VPDetection
img = cv2.imread("<file>"); h, w = img.shape[:2]
vpd = VPDetection(length_thresh=60, focal_length=max(h, w)); vpd.find_vps(img)
print("size", w, h); print("vps 2D", vpd.vps_2D.round(0).tolist()); vpd.create_debug_VP_image(save_image="vp_debug.png")
EOF
python3 - <<'EOF'   # relative depth bands
from transformers import pipeline; from PIL import Image; import numpy as np
d = np.asarray(pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")(Image.open("<file>"))["depth"])
print("near, mid, far share", [round(float((d > t).mean()), 2) for t in (170, 85, 0)])
EOF
```

- **Horizon and camera height:** the line through the two horizontal vanishing points. Horizon at door handles means camera about 1.0 m, at heads about 1.6 m. A vertical vanishing point inside or near the frame means a tilted camera (converging verticals).
- **Scale (Criminisi):** pick one vertical of known height standing on the floor (interior door 2.0 to 2.1 m, dining chair seat 0.45 m, worktop 0.9 m, light switch 1.2 m, art centre 1.45 to 1.5 m). Camera height = known height × (base to horizon) ÷ (base to top), measured along that vertical in pixels. Every other height follows by the same ratio. Mark each as `~` with the reference used.
- **Lens and tilt from the picture:** GeoCalib (`pip install -e "git+https://github.com/cvg/GeoCalib#egg=geocalib"`, ask first, core rule 1. `GeoCalib().calibrate(image)` returns camera and gravity) or PerspectiveFields (roll, pitch, vertical field of view). Without them: the lens is `~` from the converging lines and the field of view.
- **Palette with share:** the photo skill's quantize line, read as room roles (dominant, secondary, accent).
- **Sun:** for an exterior with a known place and time, `astral` gives azimuth, elevation and golden hour (sun from 4° below to 6° above the horizon). Shadow length = height ÷ tan(elevation).
- **A 360 pano:** HorizonNet reads the full room layout (corners as JSON); a normal photo cannot, so use the vanishing points and depth bands instead.

## THE PRO READ

| Field | What to write |
|---|---|
| KIND | Exterior, interior, set, landscape, street. Building type and use. Period and place when readable. |
| CAMERA | Height in m, lens in mm equivalent, tilt, horizon position, where it stood in the room. The numbers a prompt or a scout needs. |
| SCALE | Ceiling or storey height, room or facade width and depth, the reference used. Door 2.0 to 2.1 m, ceiling 2.44 old, 2.74 new, 3.0 to 3.7 period. |
| MASSING AND PLAN | Bar, tower, podium, L, U, stacked, carved; courtyard, atrium, enfilade, spine, pilotis; for an interior, the zones (sit, dine, work, sleep) and the circulation. |
| RHYTHM | Bays, columns, mullions, window to wall ratio, what repeats (A-B-A-B) and what breaks it. Reveal depth. |
| MATERIALS | Each surface with finish and age: board-formed concrete, terrazzo, rammed earth, corten, charred timber, lime render, brick bond and mortar, tadelakt, breeze block. Count the wood tones and the metals. |
| LIGHT PLAN | Daylight direction and hardness; each source by kind and Kelvin (living 2700 to 3000 K, office 3500 to 4000 K); practicals; where shadows fall. Premium rooms use many low sources, not one ceiling grid. |
| PALETTE | Measured shares as 60/30/10 roles, with finish (matte, honed, polished, brushed). |
| LAYERS | Envelope, large furniture, textiles and rugs, lighting, art and objects, plants. What each layer adds. |
| FOCAL AND SIGHTLINES | What the eye hits first; which walls can be shot; the approach view, framed view, terminated vista. |
| HERO AND DRESSING | For a set: 3 to 5 hero objects, then dressing by zone, age per surface (new, used, worn, derelict), the colour script in one line. |
| STYLE TELLS | Brutalist, Bauhaus, mid-century, tropical modern, Indochine, tube house, Japandi, wabi-sabi, quiet luxury, industrial: the tells that prove it, never the name alone. |
| PROPORTION CHECKS | Rug under the front legs, 30 to 45 cm floor border; art centre 1.45 to 1.5 m, 15 to 25 cm above the sofa; coffee table 2/3 of the sofa. Misses are findings. |
| WHAT READS PREMIUM | The three to five choices with their numbers. Also what reads generic: builder-grade fixtures, undersized rug, matching sets, mixed floors, unlined curtains, flat palette. |

## THE SUBJECT SHEET

The dossier (`llllloc:references`) carries what recurs across his references. The sheet is the usable part, written to the job's `*_CLAUDE/2_References/SPACE_<name>.md` (or beside the dossier when no job is named):

```markdown
# SPACE <name>                 <date> · built by llllloc:references-space
## CAMERA        height, lens, tilt, horizon, position
## SCALE         dimensions with the reference used
## BUILD         massing, plan, rhythm, materials with finish and age
## LIGHT PLAN    sources by kind, direction, Kelvin, time of day, sun
## PALETTE       60/30/10 roles with finish
## DRESSING      layers, focal point, hero objects, age
## STYLE TELLS   what proves it
## PROMPT LINES  subject, materials, context, light, camera: one lens, camera height in words
## OPEN          what no tool could read
```

## RESEARCH (with `llllloc:task-research`)

The architect, interior designer, production designer or studio and their stated process (ArchDaily, Dezeen, Architectural Digest, the studio's own site, film art department interviews); the style name and its period; the material by name and supplier; what practitioners call the device (borrowed landscape, colour drenching, wild wall, light well); whether it is durable or a trend; what breaks when copied (structural nonsense, wrong scale, one ceiling grid). Cache: `llllloc/5_Research cache/jobs/reference-analysis.md`.

## WHAT TRANSFERS, WHAT DOES NOT

Transfers: the scale, the camera, the massing logic, the rhythm, the material and finish list, the light plan, the palette roles, the layering, the dressing logic. Does not: the landmark itself, a signature facade one to one, the exact objects.

## HAND-OFF

`llllloc:task-prompt` IMAGE and VIDEO use PROMPT LINES as intent (subject, materials, context, light, camera; one lens per image; camera height in words). `llllloc:task-art-direction` uses the sheet for a treatment, a set brief or a location brief. `llllloc:task-design` takes the palette and material list for a board. A photo of a person in the space also loads `llllloc:references-people`; the light and lens of the picture itself is `llllloc:references-photo`.
