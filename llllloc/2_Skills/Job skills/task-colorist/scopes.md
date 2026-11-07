# Reading the scopes at OmniScope level

## Contents
- The scale
- Waveform
- RGB parade
- Vectorscope
- Sat/Lum
- Histogram
- CIE plot
- False colour, skin and neutral overlays
- HDR
- The reading in order

Every value is R'G'B' 0 to 1 full range, as Lumetri and the COLOR app see it. 10-bit code = 64 + 876 x value. IRE = (code - 64) / 876 x 100. Legal video range 64 to 940 (16 to 235 in 8-bit). A number in a plan is a 10-bit code or a percent, never "dark" or "a bit hot".

## The scale
Pick one scale per job and keep it: 10-bit codes for a grade (Resolve default), percent or IRE when he talks to a DP, nits only on HDR. Say the scale in the plan's first line.

## Waveform (luma, RGB overlay, YRGB)
x is the picture column, y is the level. Luma Y' = 0.2126 R + 0.7152 G + 0.0722 B (Rec.709), 0.2627/0.6780/0.0593 for Rec.2020.
- Clip: a flat line pressed on the ceiling. Irreversible after the clipping node. Fix exposure before that node.
- Black: the bottom of the trace. Crushed = a flat line on 64. Lifted = a floor well above 64 with nothing under it. Dune sat its blacks near 128 (10 IRE) on purpose, and the eye drifted them to 20 to 25 IRE in a day: the scope caught it (Haine).
- Rec.709 skin: about 60 to 75 IRE (590 to 720), darker skin lower; 85 IRE is hot.
- An exterior does not need to hit 100. Log footage sits as a narrow mid band and is not "wrong".
- Read the shadows at 1 to 2 percent sensitivity, highlights at 10 percent (Jordan).

## RGB parade
Three waveforms side by side. Neutral grey = the three traces aligned top to bottom.
- Read the bottom, the middle and the top as three separate questions. A highlight-only mismatch needs a different fix from a shadow mismatch.
- Equal shift of all three = exposure. Unequal = balance.
- Never force the parade to match under coloured light. Balance what should be neutral (a white shirt, concrete, paper), not the whole frame.
- A cast in the shadows can be one channel clipping at the bottom.

## Vectorscope
Angle = hue, radius = saturation, centre = neutral. Cb to the right, Cr up. Targets at 75 percent: R 102.9 degrees, Mg 49.7, B 354.8, Cy 282.9, G 229.7, Yl 174.8 (Rec.709). 100 percent is the same angles at 4/3 the radius.
- Neutrals collapse to a dot at the centre. A dot off centre = a global cast; read its direction.
- The skin line at 123 degrees is the NTSC I axis, a guide and not a law (Van Hurkman). Skin falls on it or a few degrees clockwise, in a band of about plus or minus 10 to 20. Measured skin averages 122.5 degrees in ICtCp and 136 in BT.2020 Y'CbCr (Dolby, second hand). Never force a face onto the line: lighting and makeup move it. Toward red with more saturation reads blotchy, toward yellow with less reads sickly.
- Split Low/Mid/High (three small scopes): a split tone shows as the Low cluster and the High cluster on opposite sides. Read where the shadows and the highlights sit, in degrees.
- Inside the 75 percent targets for broadcast, 100 percent is the hard limit. In HDR the trace rarely passes 75 percent.
- 2x zoom to read a cast of one or two percent.

## Sat/Lum
x is luma, y is chroma length. Greys lie on the floor, pure primaries at the top.
- A bulge top right = saturated highlights, they read burned. Pull chroma from the highlights.
- A bulge top left = chroma in the blacks, noise or a tinted crush. Pull chroma from the shadows.
- A healthy graded image clusters mid luma, low to mid chroma, with one hue allowed to stay strong.

## Histogram (RGB, luma)
x is the level, y is the count, log scale to see the tails.
- A pile at the right edge = clipping. Left-heavy with an empty top = underexposed.
- RGB mode shows single-channel clipping that the luma histogram hides.
- The waveform says where, the histogram says how much.

## CIE plot (1931 xy, 1976 u'v')
Every pixel as a dot on the horseshoe, luminance dropped. Triangles: Rec.709, P3, Rec.2020. White points D65 (0.3127, 0.3290), DCI (0.314, 0.351).
- Outside the display triangle = will clip or be mapped. Inside is not proof of a good gamut (no volume shown).
- Neutrals on the Planckian locus = a natural light source. Off it toward green or magenta = a tint to fix.
- u'v' for comparing coverage, xy for matching a spec.

## False colour, skin and neutral overlays
- False colour bands (Rec.709 luma, 10-bit): under 100 purple, to 180 blue, to 410 cyan, 410 to 560 green = grey and skin mids, 560 to 680 pink = light skin, to 780 yellow, to 880 orange, above 880 red = near clip. A camera log preset moves the grey band: Alexa 35 grey sits at 28 percent LogC4, S-Log3 at 41 percent. Never read log with a Rec.709 preset.
- Skin indicator: pixels in the skin hue window marked yellow when on the line, green when too green, magenta when too magenta (OmniScope Skintone, mononodes Balance).
- Neutral overlay: pixels within 5 percent of R = G = B marked, by shadows, mids and highs. A marked region that leans a hue is the cast, and tells which tone band to fix.

## HDR
PQ: 100 nits = code 509, 203 nits (reference white) = 573, 1000 nits = 723, 4000 = 855. Bulk of a PQ image 0 to 200 nits, diffuse white about 203, only speculars above. HDR10 limits MaxCLL 1000 and MaxFALL 400; keep 10 percent headroom. One outlier pixel inflates MaxCLL. HLG: 75 percent signal = 203 nits, 18 percent grey at 38 percent.

## The reading in order
1. Pipeline: range, matrix, log or graded, HDR or SDR (ffprobe).
2. Black level (waveform floor, parade bottoms aligned or not).
3. White level and clip (waveform ceiling, histogram right edge, RGB histogram per channel).
4. Cast (parade bands, vectorscope centre dot, neutral overlay).
5. Skin (vectorscope angle against 123, luma band on the waveform, false colour band).
6. Saturation by zone (Sat/Lum bulges, vectorscope radius against the 75 percent targets).
7. Gamut (CIE against the display triangle).
8. Across shots: the same six numbers per shot in a table. One shot more than about 1.5 MAD from its scene's median is the match issue, named by number.
