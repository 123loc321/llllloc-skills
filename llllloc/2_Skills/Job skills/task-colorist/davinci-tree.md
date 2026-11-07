# The house grade in DaVinci Resolve (27 Oct 2026, his words: "in future color grading jobs in resolve, always use this node setup and color grading workflow")

Built on the client AI Video Batch (V3.0), after Danny Gan's commercial shot-matching setup. Every Resolve grade uses it. Driving Resolve by script: `llllloc:tool-davinci-resolve` GRADE TREE.

Contents: 1 Settings · 2 The tree · 3 The run · 4 Checks · 5 What failed

## 1 Project settings (File > Project Settings > Color Management, his set on a client, read back 27 Oct 2026)
| Setting | Value |
|---|---|
| Color science | DaVinci YRGB (not Color Managed, Automatic color management off) |
| Use separate color space and gamma | on |
| Timeline color space | DaVinci WG / DaVinci Intermediate |
| Output color space | Rec.709 / Rec.709-A |
| Input DRT, Output DRT | None (the CST nodes do the tone mapping) |
| Output gamut mapping | None |
| Timeline size and frame rate | the delivery spec of the job (a client: 1920x2560, 25 fps) |
- Set them on the project for a new grading project. A project that holds older graded versions: set the same values per timeline (Timeline Settings, Use custom settings) so the older versions keep their look.
- Read back after setting: `GetSetting` colorScienceMode davinciYRGB, colorSpaceTimeline DaVinci WG, colorSpaceTimelineGamma DaVinci Intermediate, colorSpaceOutput Rec.709, colorSpaceOutputGamma Rec.709-A.
- With custom timeline settings, the Project Settings page shows "Any modification done here will not impact the currently loaded timeline": normal.
- A clip from an unknown camera: read its colour space and gamma from the media before the IDT.

## 2 The tree. One colour group for all shots of a look that are the same (one camera, one light)
| Where | Node (his names) | What it does | Who sets it |
|---|---|---|---|
| Group Pre-Clip | 01 IDT | Color Space Transform: camera gamut / log (for example Canon Cinema Gamut / Canon Log 2) to DaVinci Wide Gamut / DaVinci Intermediate. Tone Mapping DaVinci, Adaptation 9.00, Gamut Mapping None, White Point Adaptation on | his hands, once |
| Clip 1 | 02 NULL | empty, a spare spot for a one-shot fix | - |
| Clip 2 | 03 EX | exposure: Offset equal on R G B, per shot | Claude, measured |
| Clip 3 | 04 WB | white balance: Offset R and B, G fixed, per shot | Claude, measured |
| Clip 4 | 5 HSV SAT | node colour space HSV, channels 1 and 3 off, Gain (slope) channel 2 = saturation. a client: 1.40 | Claude, one value per look |
| Clip 5 | 06 SKIN BRIGHTNESS | a skin-only LUT that lifts skin in linear light, or empty | Claude, only on his ask |
| Group Post-Clip | 07 LOOK, then his creative nodes (a client: lab DCTL MONO-LAB-v1.0, print), then 08 ODT | ODT = CST DaVinci WG / Intermediate to Rec.709 / Gamma 2.4, Tone Mapping DaVinci, Adaptation 9.00, Forward OOTF on, White Point Adaptation on | his hands |

Why groups: the IDT, the look and the ODT are the same on every shot. Change them once, all shots follow. Clip nodes hold only what differs per shot.

## 3 The run (copy into the status checklist)
```
- [ ] 1 Project settings of section 1 set and read back; timelines duplicated as the next version, grades cleared
- [ ] 2 He builds the tree once on one shot (Claude sends the steps: section 2). Claude reads it back: node count and labels
- [ ] 3 Colour group made, every shot assigned; tree copied to every shot (CopyGrades), node count read back on every shot
- [ ] 4 Stills of every shot (3 frames each), the paper and the person measured
- [ ] 5 04 WB per shot: the studio paper R = G = B. 03 EX per shot: the reference brightness (below). Closed loop on new stills until it holds
- [ ] 6 5 HSV SAT against the style target (garment colour first; skin follows)
- [ ] 7 Check (section 4). A miss: back to 5
- [ ] 8 Contact sheet before and after sent; render only on his word, sharpening off unless he asks
```
- Log offsets: one stop = 0.0733 in DaVinci Intermediate. A white balance gain g on a channel = 0.0733 x log2(g).
- Reference brightness: he names a hero shot ("follow this shot"). Match the white studio paper (bright, outside the person, the 20 percent least coloured pixels, picked on the camera image) to the hero's paper. A close-up with no paper in frame takes the mean exposure change of the paper shots of its video, never a paper read on fabric. Clamp one round's change to 0.06 (about 0.8 stop) and say which shots stopped at it.
- No hero named yet: match each shot's person to the last approved version, and ask which shot is the hero.

## 4 Checks, every round
- Paper neutral: Oklab a and b x1000 within 3 on every shot (a client V3.0: worst 2.6).
- Paper brightness within 0.01 Oklab L of the hero on paper shots.
- Skin: brightness near the style target, and fine noise on skin vs no lift between x0.9 and x1.1. Above: the key edges are too steep.
- A colour change of the tree (move to groups, rename) is proved with stills: mean change under 1 code (10-bit).
- Flip the contact sheet by eye before the reply (TOP RULE 7).

## 5 What failed on a client (do not repeat)
- A skin key with steep hue and chroma edges made blotchy, grainy skin (noise x3.4): his note "super noisy and grainy". Keep the skin weight flat inside skin, the ramps wide (hue 50 plus or minus 30 full, gone at 90).
- A full skin lift to the photo target flattened skin against the white background: his note "50% ... too strong ... super low contrast to the white background". Lift skin half way at most (a client: L01 +0.45 stop, L02 +0.3).
- Looks fitted to sunlit style photos added colour casts (V1.6 to V1.9). Balance stays neutral; the look carries no tint.
