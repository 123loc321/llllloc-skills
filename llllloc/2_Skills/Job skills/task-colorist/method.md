# The method, step by step

## Contents
1. Pipeline
2. Balance
3. Contrast
4. Skin
5. Saturation and hue
6. Look, print, texture
7. Shot match
8. The LUT
9. Targets and the check
10. What the best do, long form

## 1. Pipeline
Read the file: `ffprobe` for range, matrix, transfer, primaries, bit depth. Decide the working space: camera log when every shot is one camera (LogC3 preferred), DaVinci Wide Gamut Intermediate when cameras are mixed, ACES only for a VFX pipeline. Display: Rec.709 gamma 2.4 for his deliveries, P3 2.6 for cinema. Write the mid grey of the working space: Linear 0.180, LogC3 0.391, LogC4 0.278, DWG Intermediate 0.336, ACEScct 0.414, S-Log3 0.411, Log3G10 0.333, BMD Film Gen5 0.384, V-Log 0.423, Rec.709 gamma 2.4 0.489 (mononodes Middle Gray table). Rec.709 footage (his usual ProRes 4444 from Premiere) is graded as display-referred Rec.709 with the LUT doing a log-like pivot inside: say so.

## 2. Balance
Offset (printer lights) only: exposure and white balance in one move. Offset in log behaves like camera exposure within two stops (Volpatto). Never Lift for balance: it tints the blacks. Balance on a known neutral of the subject (shirt, paper, concrete, a grey card), never on the whole frame. Under coloured light, balance what should be neutral and let the light stay coloured. Never change the DP's temperature and tint in the RAW settings (Volpatto). Then exposure: the lead's skin into its luma band (section 4). A global hue rotate of one to three degrees puts skin back on its line after a printer light move (mononodes Auto Hue Rotate).

## 3. Contrast
One structural decision per piece, pivoted at the working space's mid grey: black point, midtone slope, highlight compression (mononodes). Make it on the look node, not per shot. Kelly: exposure first, then contrast and pivot, then balance on the skin axis and the green-magenta axis. Test alternatives side by side (plus or minus 0.1 and 0.2 contrast, plus or minus half a stop) before choosing. The eye is more sensitive to contrast than to colour (Kelly): a note "more colour" is often "more contrast".

## 4. Skin
Measure the lead's skin on the hero shot: luma band (Rec.709 about 590 to 720 in 10-bit for light skin, lower for darker skin), vectorscope angle against 123 degrees, Lab L and chroma. Then hold it: every later move is checked against these numbers. Skin is steered through the Red and Yellow vectors and the global hue, never through a skin qualifier (mononodes: the slice is too narrow and goes patchy). A secondary on skin is a beauty fix (blemish, a red ear), applied last. Darker skin reads toward yellow-green on the false colour, lighter toward yellow and pink: these are placements, not targets. There is no wrong skin tone, only skin in or out of harmony with the intent (Kelly).

## 5. Saturation and hue
Saturation is subtractive and comes with density: lower the luminance of a hue while raising its saturation, so reds go deep instead of garish (Yedlin's two kinds of saturation, mononodes). Additive saturation turned down goes grey. Keep density in the mids and shadows, desaturate the highlights the way film does. Order inside the look: density → saturation → hue shift. Hue shift moves a hue toward its neighbour (blue toward cyan), and can be luminance dependent (bright toward one neighbour, dark toward the other). A split tone is two per-channel curves crossing at mid grey with soft knees and protected white and black: name the shadow hue and the highlight hue in degrees. Nakamura: desaturate everything except two or three key colours to make them pop. Bogdanowicz: darken the unimportant, lighten the important, tame a bright lamp that pulls the eye.

## 6. Look, print, texture
The look is one node tree, identical on every shot, decided before the shots are touched. Variations between scenes are temperature, colour separation and saturation, with skin held (mononodes). The print stage once, at the tail: Kodak 2383 (Resolve's free LUT, Cineon Film Log in) for warm skin and blues toward cyan, Fuji 3513 for pink skin and cooler greens. Split the print into its colour and its tone so each can be dialed (Kelly: steal what is good, leave the rest). Fix the print's lifted tinted blacks with black level and R/G/B shadow offsets. Texture only after colour and only when the piece asks: grain about 35 percent and halation about 50 percent as Kelly's starting values, physical order MTF → chromatic aberration → distortion → vignette → grain → halation → dirt → flicker (0.005 to 0.010) → gate weave. Halation = threshold the highlights, blur red more than green, orange tint, add in linear. Grain the delivery compression will kill is not added (Volpatto). Film prints peak about 48 nits: a print look is dense, not bright.

## 7. Shot match
Under the look, one hero per scene (the widest frame). Match in this order: black level first (a jumping black is what viewers feel), then contrast around the pivot, then density of the mids, then saturation, then hue of the key colours (skin, sky, greens, oranges). Do not match content: a red sauce stays red (Van Hurkman). Strong colour areas fool the eye, so balance on the subject. With a fixed node order, a match is three trims on the balance node: exposure, tint, saturation (mononodes MONO Match). The V3 engine of the client match thread does this by numbers: log space, Offset balance on the subject, skin hue locked within 3 degrees, chroma matched per tone band in Oklab and pulled halfway, tone curve limited to slopes 0.5 to 2. Its targets are the check (section 9). Then the flip test at playback speed: the cut must feel continuous. Lucas: "Perfect continuity is what makes a good colourist."

## 8. The LUT
A grade ships as a 3D .cube, LUT_3D_SIZE 33 (65 when a hue shift is steep), red fastest, DOMAIN 0 to 1, tetrahedral. One file per shot for a match (`MATCH_Snn_to_<hero>.cube`), one file for the look. Version every file, never overwrite. Proof: apply the same .cube with `ffmpeg -vf lut3d=file=<x>.cube:interp=tetrahedral` to the source frame and compare with the preview, max error under 1 code value in 10-bit. Check for banding on a grey ramp and a Granger rainbow (mononodes Test Charts): a LUT that bands is not shipped. In Premiere a .cube goes in as a Lumetri Look (his hand, until the COLOR LUT slot effect ships). In Resolve: a LUT node after the balance, tetrahedral in the project settings.

## 9. Targets and the check
Per shot, after the grade, in the plan's CHECK table (10-bit codes unless HDR):
- Blacks within 1 code of the hero across the scene. Grey balance within 1 code (parade bottoms and mids aligned).
- Skin hue within 3 degrees of the hero. Skin luma within 10 codes.
- Mid density within 0.03 Oklab L of the hero.
- Chroma per band (shadows, mids, highlights) within 25 percent of the hero.
- No new clipping: pixels at 940 or above no more than the source. No pixels under 64 on a tv-range delivery.
- Vectorscope inside the 75 percent targets for broadcast, under 100 percent always.
- The flip test passed by eye at playback speed, full screen.
A missed target is written with its number, never rounded into a pass.

## 10. What the best do, long form
- Tom Poole (Company 3): watch the piece alone two or three times, make notes, set a couple of shots per scene as a colour bible, review as a sizzle reel, then big blocks to detail. A LUT for every show. The image should look like it could be printed on photographic paper, with texture in the highlights and the blacks. A good grade complements the narrative and the viewer is not conscious of it.
- Greg Fisher (Company 3 London, FilmLight award for Poor Things): the overall look first, then a look per scene, then shots, then detail. Start where the exposure and colour naturally sit. Carry the dailies LUT to the final.
- Yvan Lucas (Company 3): LUT first, then printer lights and density under it, keys and windows at the end. Custom stock LUTs (Kodak 5219 as processed at FotoKem, ENR, 3-strip). "There are many ways a LUT can break."
- Walter Volpatto: skin of the lead first, then everything else. Offset in log, no secondaries on skin, no change to the DP's temperature and tint. Profiled negative and print for Dunkirk and applied that to every digital source. Refused to re-saturate The Last Jedi. No grain unless present or asked.
- Stephen Nakamura (Company 3): the dailies set contrast, temperature and saturation, the grade refines. Desaturate all but a few key colours. A little shadow darkening changes a shot. Unpolished films have mismatched shots.
- Jill Bogdanowicz (Company 3, HPA award for Joker): one show LUT per film that holds back saturation. Dodge and burn to steer the eye. Desaturated skin disconnects the audience, so it is a tool. Grain kept off warm skin. Done when the filmmakers feel it is their movie.
- Mitch Paulson: it is all about the eye. Test LUTs with the DP before the shoot. Protect skin with a keyer while pulling backgrounds. Good exposure first, files can only be pushed so far before noise.
- Cullen Kelly: exposure, then contrast with pivot, then balance on two axes. The 10-minute grade: a global curve, a fast exposure pass, then the priority shots. Print emulation once at the tail, grain 35 percent, halation 50 percent. Do not take the bait on a literal client note.
- Dan Moran (Mixing Light): normalise the colour space, balance contrast, wipe to neutralise colour, judge on the cut.
- Dado Valentic: colour-manage every shot from the first take, the look built on pre-production tests; "bring the soul back to digital imagery".
- Juan Melara: Kodak 2393 with a D55 white point on Alexa LogC for warmth and flattering skin; free 2383, 2393, 3510, 3513 print LUTs.
- mononodes (Stefan Ringelschwandtner): fixed 6-node tree around Kodak 2383; balance with Offset, pivot at middle grey, contrast as a structural decision, subtractive saturation with density, skin steered by the red and yellow vectors, vectorscope read for relationships not single colours, texture in physical order, order of operations is the method, accept imperfect matches.
- What separates the best (FilmLight and HPA jurors, Perry, Hobson): invisibility, continuity, restraint ("the best colour is not necessarily the most colour"), serving the story and the DP's vision, texture not video-flat, emotion over realism, and "the pocket every image wants to lie in".
Sources: COLOR/_CLAUDE/2_Research/COLORISTS-RESEARCH_2026-10-21.md and MONONODES-RESEARCH_2026-10-21.md, each line with its link.
