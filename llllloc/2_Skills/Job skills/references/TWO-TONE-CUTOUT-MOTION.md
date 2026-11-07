# TWO-TONE CUTOUT MOTION — craft dossier
Updated: 10 Oct 2026 · Batches: 1 · Items: 1 (Coca-Cola "Alexa, I See Coke", cinema spot, 31 s, 1920 x 1080, 23.976 fps, 743 frames). Tier 2 assumed (work he admires).

## THE RECIPE
Flat vector cutout animation in three flat tones. Every line below is a mechanism that transfers to a new subject.

1. CANVAS. One flat field color fills the frame at all times (red 57% of all pixels, black 17%, white 17%, nothing else above 1%). No gradient, no vignette, no texture, no glow. Depth comes from overlap and scale only.
2. THREE INKS, THREE JOBS. The field is one color. Silhouettes are the darkest ink. The third ink is a highlight that touches only the hero object (the bottle's shine, the blade's edge, the eye of a face). The highlight never appears on a background element. This is what makes the hero read in a split second.
3. INVERT TO CUT. A scene change is a field swap, not a dissolve. Two devices, used in turn: (a) the TYPE SCATTER: the letters of the old line fly apart on their own paths, the field color swaps under them, the new line assembles from the scatter (about 1.0 s, ten frames of chaos between two readable states); (b) the SILHOUETTE WIPE: the hero's own outline, scaled 8 to 10 times, slides across the frame and its inside becomes the next scene's field (bottle at 2.1 s, 9.5 s, 21.9 s, 26.7 s). Nothing fades. Opacity is never used.
4. ONE HERO, ONE SCALE PER SHOT. Each shot plants the hero at one size and leaves the camera still. The drama is a scale jump between shots: bottle tiny beside a dinosaur's foot, then bottle filling the frame beside a swordsman, then bottle as a skyscraper. The eye re-reads the same shape as a new thing.
5. TIMING MIX. Cut-outs move on ones for action (48 single-frame holds, 10 double, 3 triple between 1 and 21 s: 73% of frame pairs change) and sit dead still on holds of 11 to 13 frames (about half a second) at the end of each gag. A smear is one frame (the sword's arc, the thrown cap): the shape stretched along the path, with 3 to 6 white sparks that live two frames.
6. PHYSICAL ACTING ON A GRAPHIC BODY. Anticipation before every hit: the swordsman winds back 7 frames, strikes in 2, the cap flies 12. The dinosaur leans in for 4 frames, roars for 6, then holds. The body is a flat silhouette, the timing is hand-animated character timing.
7. GRAPHIC STAND-INS FOR EFFECTS. No particle systems. A splash is five white commas. Speed is three thin white lines. A web is six straight white strokes from one point. Each effect is a drawn shape and it reads at 240 px wide.
8. TYPE AS A CHARACTER. Heavy rounded grotesk (Coca-Cola's TCCC Unity family), 3 to 4 words, left-aligned block, 1/5 of frame height. Letters animate as individual objects (rotation plus travel, each on its own curve), never as a text animator preset.
9. ENDING. Field to black, the scattered type line reassembles as the tagline, then a 3 s logo card on red. Nothing moves on the logo card.

## WHAT MAKES IT LAND
- The field is never empty but never busy. Why: a flat field makes a black silhouette read in 2 frames, so cuts can be fast and still read. What breaks without it: a gradient or texture softens the silhouette edge and every cut needs an extra 6 frames.
- Highlights only on the hero. Why: the third ink is a pointer, the eye goes where the white is. What breaks: white on a background building makes the frame flat.
- Field swap instead of fade. Why: the picture is always 100% opaque, so the eye never sees two scenes at once and the cut lands like a drum hit. What breaks: a dissolve between two three-tone frames makes muddy fourth colors.
- Scale jump between shots. Why: it turns one asset into comedy and awe for free. What breaks: if the hero is the same size in two consecutive shots the cut feels like nothing happened.
- Dead holds after action. Why: the half-second freeze lets the gag land and makes the next cut hit harder. What breaks: continuous motion with no holds reads as a screensaver.

## MEASURED FACTS
- Palette: field red #f80808 (57.5%), black #080808 (16.9%), white #f8f8f8 (16.5%). Two reds in one frame never happen.
- Frame: 1920 x 1080, 23.976 fps, 31.0 s, 743 frames, 1.03 Mbit/s H.264.
- Cuts (scene change over 0.15): 2.13, 3.09 to 3.29 (type scatter, 5 frames), 9.55, 11.47, 12.22 to 12.60 (type scatter), 18.44, 21.90, 26.65, 29.57 s. Nine cuts, mean shot 3.4 s, shortest hard shot 1.9 s.
- Motion: 27% of frame pairs are still. Holds: 48 of 1 frame, 10 of 2, 3 of 3, four long holds of 11 to 13 frames.
- Type block: 3 lines, cap height about 1/9 of frame height, left margin 1/40 of width.
- Highlight share per hero: bottle shine is one tall white shape about 1/6 of the bottle width, plus a thin white rim on the cap.

## WHAT THE RESEARCH FOUND
- The spot is "I See Coke", Coca-Cola, 2023, launched in Saudi Arabia with Alexa's Khaleeji Arabic launch. Agencies: VMLY&R Commerce and VML MENA (VML New York and VML Dubai on the D&AD entry). The idea: spot a Coke bottle placed in famous movie and TV scenes, say "Alexa, I see Coke", get a scene-specific line and a discount code. The illustrations were animated by Believe Digital, an animation studio in Chile. No director or illustrator is named. Style described as "Coke's iconicity with its colours and minimalistic approach". Sources: [LBB Online](https://lbbonline.com/news/how-ai-voice-campaign-alexa-i-see-coke-came-to-the-movies), [D&AD archive](https://www.dandad.org/work/d-ad-awards-archive/i-see-coke), [WPP case study](https://www.wpp.com/en/case-studies/vml-commerce-the-coca-cola-companys-i-see-coke), [VML](https://www.vml.com/work/i-see-coke).
- The lineage is Saul Bass: flat cut-paper silhouettes, one field color, type that moves as objects (Anatomy of a Murder, Vertigo). Durable, not a trend: it has been copied for 65 years and still reads as premium when the drawing is good. Tutorials exist for the look in After Effects. Sources: [Tuts+ Saul Bass title in AE](https://photography.tutsplus.com/tutorials/how-to-create-a-saul-bass-style-title-animation-in-after-effects--cms-109184), [Art of the Title](https://artofthetitle.com/title/around-the-world-in-eighty-days), [Design Your Way](https://www.designyourway.net/blog/saul-bass/).
- Smear frames: one frame, used only on fast exaggerated moves (strike, throw, fall), never in isolation, combined with anticipation and a hold; build in 2D by stretching or multiplying the drawing along the path. Mixing ones and twos per element is a known device (Spider-Verse). Sources: [GarageFarm on smear frames](https://garagefarm.net/blog/smear-frames-enhancing-motion-in-animation), [Creative COW, animating on 2s](https://creativecow.net/forums/thread/animating-on-2s/), [Motion Design School, CC Smear](https://motiondesign.school/cc-smear-effect/).
- Halftone and grain searches returned stock listings only. No technique source found this batch. OPEN.

## DO NOT COPY
- The bottle-as-wipe is this spot's signature, built on the most recognised silhouette in advertising. Use the device (hero outline as a wipe), never the bottle.
- Movie parodies (dinosaur, samurai, Kong, Spider-Man) are the campaign's content. They do not transfer.
- The red field is Coca-Cola's. On a non-Coke job the field color is the brand's.
- What this reference cannot do: narration-led storytelling. It has no VO and no on-screen explanation. It is a gag reel of three-second shots. A 3 to 4 minute narrated episode needs holds, text that stays readable, and camera moves this spot never uses.

## OPEN
- The halftone texture on the client designs: how to keep a dot screen still under a moving silhouette (screen fixed to camera, or to object?). Not answered by this batch.
- No frame-by-frame source of the type scatter: the letter paths look hand-keyed, 10 letters, each a different arc.
- No numbers found for the ideal hold length after a gag beyond this spot's own 11 to 13 frames.
