---
name: references-people
description: 'Reads a people reference (a pose, a body, a face or expression, a haircut, makeup, an outfit, wardrobe, styling) the way a movement director, a casting director, a hair and makeup artist and a fashion stylist would: what the picture is OF: joint angles and weight share from pose landmarks, head turn and gaze, face shape by its measures, expression as FACS action units, hair by type, length landmark, cut, part, finish and colour technique, makeup by finish and placement, each garment with silhouette, fit, fabric, construction and the proportion split. Writes a subject sheet a prompt, a casting brief, a shoot plan or a wardrobe plan can be built from. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when /llllloc:router picks it for a dropped picture of a person, pose, hair, makeup or outfit to analyze, learn from or use in new work. How the picture was lit and shot is llllloc:references-photo.'
---

# llllloc:references-people (17 Oct 2026, his words: "references pictures for human, pose, hair ... and outfit, wardrobe")

A person in a reference is read as what is there: the geometry of the pose, the measures of the face, the system of the hair, the build of the clothes. The output is a subject sheet: a new model, a new shoot or a new prompt can be directed from it. Light, lens and grade of the picture itself: `llllloc:references-photo`. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. Geometry, not mood. A pose is joint angles, a weight share, a head turn and a gaze target. "Confident" and "sultry" are not findings; "weight 70 percent on the left hip, shoulders tilted 6° against the hips, chin down, eyes to lens" is.
2. Measure first, then one neutral word. Shoulder to hip ratio and face measures from landmarks, then a plain descriptor (slim, athletic, broad, soft, hourglass). Loaded words give caricature in a prompt.
3. Hair and clothes by their trade names. Hair type 1A to 4C, length by the body landmark it reaches, cut, part, finish, colour technique. Garments by silhouette, fit, fabric, construction and closure. A guessed brand or a vague "nice dress" sends the next skill nowhere.
4. One attribute per source. When several references come in, the sheet says which gives the pose, which the hair, which the wardrobe. Mixing them in one prompt blends them.

## MEASURE (run first, raw output to `_batches/`)

```
pip install mediapipe rtmlib py-feat transformers torch pillow opencv-python-headless     # once (ask first, core rule 1); py-feat needs Python 3.11+
python3 - <<'EOF'   # pose: joint angles, tilts, weight share (MediaPipe, 33 landmarks; model file pose_landmarker_heavy.task)
import math, mediapipe as mp
from mediapipe.tasks import python; from mediapipe.tasks.python import vision
opts = vision.PoseLandmarkerOptions(base_options=python.BaseOptions(model_asset_path="pose_landmarker_heavy.task"))
res = vision.PoseLandmarker.create_from_options(opts).detect(mp.Image.create_from_file("<file>"))
P, W = res.pose_landmarks[0], res.pose_world_landmarks[0]
def ang(a,b,c):
    A,B,C = W[a],W[b],W[c]; v1=(A.x-B.x,A.y-B.y,A.z-B.z); v2=(C.x-B.x,C.y-B.y,C.z-B.z)
    return round(math.degrees(math.acos(max(-1,min(1,sum(i*j for i,j in zip(v1,v2))/(math.hypot(*v1)*math.hypot(*v2)+1e-9))))),1)
def tilt(l,r): return round(math.degrees(math.atan2(P[r].y-P[l].y, P[r].x-P[l].x)),1)
print("elbow L/R", ang(11,13,15), ang(12,14,16), "knee L/R", ang(23,25,27), ang(24,26,28), "hip L/R", ang(11,23,25), ang(12,24,26))
print("shoulder tilt", tilt(11,12), "hip tilt", tilt(23,24), "contrapposto", tilt(11,12)*tilt(23,24) < 0)
m=(P[23].x+P[24].x)/2; dL,dR=abs(P[27].x-m),abs(P[28].x-m); print("weight L share ~", round(dR/(dL+dR+1e-9),2))
print("shoulder:hip width", round(abs(W[11].x-W[12].x)/(abs(W[23].x-W[24].x)+1e-9),2), "min visibility", round(min(l.visibility for l in P),2))
EOF
python3 -c "from feat import Detectorv2; f=Detectorv2(device='cpu').detect('<file>', data_type='image'); print(f.aus.round(2)); print(f.poses); print(f[['valence','arousal']])"   # expression as action units, head pose
python3 - <<'EOF'   # garments: masks per garment, then zero-shot labels per crop
from transformers import pipeline; pipe = pipeline("zero-shot-image-classification", model="patrickjohncyh/fashion-clip")
print(pipe("<crop>", candidate_labels=["slip dress","A-line midi skirt","oversized blazer","tailored blazer","wide-leg trousers","straight jeans","trench coat","bomber jacket","knit polo"])[:3])
print(pipe("<crop>", candidate_labels=["satin","crepe","denim","tweed","leather","jersey","poplin","linen","sequin","lace"])[:3])
EOF
```

- Whole body with hands and face: `rtmlib` `Wholebody(mode='balanced', backend='onnxruntime', device='cpu')` gives 133 points, and its DWPose skeleton is the same control image ControlNet `dw_openpose_full` takes, so a measured pose can drive a new image.
- Garment masks: `mattmdjaga/segformer_b2_clothes` (18 labels: upper clothes, skirt, pants, dress, belt, shoes, bag, scarf, hair, hat). Crop each mask for Fashion-CLIP, read the hem against the knee and ankle landmarks, and quantize each mask for the garment's hex and share.
- Proportion split: shoulder to hem of the top over shoulder to floor, from the landmarks. Thirds (1:2 or 2:1) read as styled; halves read flat.
- A joint with visibility under 0.5 is not reported. Weight share from one still is `~` and says so.

## THE PRO READ

| Field | What to write |
|---|---|
| POSE | Stance (standing, seated, floor, walking freeze), weight share, contrapposto with both tilts, each joint angle, torso twist against the camera, line of action (S, C, straight), open or closed, negative space, foreshortening. |
| HEAD AND GAZE | Turn (square, three-quarter 30 to 45°, profile, back three-quarter), tilt, chin forward and down or lifted, eyes to lens, away, over the shoulder. Camera height and angle. |
| HANDS | Placement by name (pocket, hip, collarbone, waist, crossed, hair), fingers soft or fist, which side shows. |
| BODY | Shoulder to hip ratio, leg share of height, then one neutral descriptor. Height class when a scale object is there. |
| FACE | Shape by the four measures (forehead, cheekbone, jaw width, length): oval, round, square, oblong, heart, diamond. Feature words: brow, eye set and lid, nose bridge, lip, cheekbone, jaw, chin, skin tone. |
| EXPRESSION | The action units and their intensity (6+12 Duchenne smile, 12 alone social smile, 1+2+5+26 surprise, 25 lips parted), valence and arousal, one micro-gesture. Editorial faces are mostly low intensity: say so. |
| HAIR | Type 1A to 4C, length by landmark (chin, shoulder, collarbone, mid-back), cut (bob, lob, shag, wolf, mullet, taper, fade, undercut, crop), part, texture as styled (sleek, tousled, piecey, braided, locs), volume (root lift, flat, crown), finish (wet, glossy, satin, matte), colour as base level 1 to 10, tone, technique (balayage, babylights, foils, ombre, money piece, root smudge, gloss), condition. |
| MAKEUP | Skin finish (matte, satin, dewy, glowy, glass) and coverage; brow shape and finish; eye (liner shape, shadow placement, lash); cheek product and placement; lip colour, finish and line; the intent (soft glam, no-makeup, graphic, colour story). |
| WARDROBE | Each garment: type, silhouette (A-line, column, oversized, boxy, tailored, bias, cocoon), fit and rise, length against a landmark, fabric with confidence (crepe, satin, poplin, twill, jersey, tweed, boucle, velvet), construction seen (darts, pleats, yoke, lapel type, topstitch, closure, hardware), colour hex and share, print placement. |
| STYLING | Layering order, proportion split, tucks and cuffs, belt position, monochrome or accent, shoe to trouser line, accessories, the era or subculture cue with its garment proof (70s flare, 90s slip, Y2K low rise, quiet luxury tailoring). |
| WHAT MAKES IT LAND | The three to five choices with their numbers. Also what reads generic: symmetrical Superman stance, hands buried, lifted chin, both pieces loose, hem at the widest point. |

## THE SUBJECT SHEET

The dossier (`llllloc:references`) carries what recurs across his references. The sheet is the usable part, written to the job's `*_CLAUDE/2_References/PEOPLE_<name>.md` (or beside the dossier when no job is named):

```markdown
# PEOPLE <name>                <date> · built by llllloc:references-people
## POSE          stance, weight, tilts, angles, head, gaze, hands, line of action, camera
## BODY          ratios, one descriptor
## FACE          shape, features, action units
## HAIR          type, length landmark, cut, part, finish, colour technique
## MAKEUP        finish, coverage, eye, cheek, lip, intent
## WARDROBE      one row per garment: type | silhouette | fit | length | fabric | construction | hex share
## STYLING       layering, split, devices, era cue
## PROMPT LINES  shot and camera height, body position, weight, hands, head and gaze in degrees, one micro-gesture; each garment's construction; "preserve silhouette, length, colour, seams"; which reference gives which attribute
## OPEN          joints not visible, fabric not sure
```

## RESEARCH (with `llllloc:task-research`)

The photographer, stylist, hair and makeup artist, casting director and movement director from the credits (ELLE Vietnam: Nhiếp ảnh, Stylist, Trang điểm & Làm tóc, Người mẫu từ Agency; ELLE Man mixes Photography, Styling, Làm tóc, Trang điểm; models.com indexes L'Officiel and Harper's Bazaar Vietnam editorials; Instagram captions carry the same labels with handles); the technique by name (cut, colour, makeup, styling device); the garment's designer and season when a runway look; whether it is durable or a trend; what breaks when copied (a garment described only in words comes back different, prints and fine stripes drift most, "dynamic" framing hides closures, several references in one prompt blend). Cache: `llllloc/5_Research cache/jobs/reference-analysis.md`.

## WHAT TRANSFERS, WHAT DOES NOT

Transfers: the pose geometry and the skeleton as a control image, the body ratios, the face shape class and the action units, the hair system, the makeup placements, the garment construction and silhouette, the proportion split, the styling devices. Does not: the model, the exact garments.

## HAND-OFF

`llllloc:task-prompt` IMAGE and VIDEO use PROMPT LINES as intent: geometry first, one micro-gesture, garments by construction, one attribute per reference. `llllloc:task-art-direction` uses the sheet for a casting brief, a shoot plan or a wardrobe plan. The light and lens of the picture itself is `llllloc:references-photo`; a person in a room also loads `llllloc:references-space`.
