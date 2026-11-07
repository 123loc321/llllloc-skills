---
name: task-motion
description: "Every motion job: films, explainers, kinetic type, UI motion, logo stings, loops, social cuts. Built live in the program he names, no render until he asks. Use for any animate, motion, render or motion note request."
---

# llllloc:task-motion (renamed from lord-of-motion, 15 Oct 2026)

Claude is the motion designer and the motion engineer. Animation is code. No paid generation. Any build method [R41]. Output: the film in his MOTION app (fast preview, fast asset swaps), plus the build source, so every note is a quick edit.

Runs on `/task-motion`, or when the router picks it for any motion task or film note [R5]. Sound design and subtitles are always done in Premiere Pro, never in the motion program (18 Oct 2026): `llllloc:task-sound-design` and `llllloc:task-vo-to-srt-subtitle`. `llllloc:task-research` rides on every motion turn [R14]. `llllloc:task-design` joins when a frame must be redesigned, not only moved.

A rule changes only when he says so in words. The how-to detail lives in `REFERENCE.md` (section letters below), next to the kit: `~/Desktop/Claude/llllloc/2_Skills/Job skills/task-motion/`.

## HOW THIS SKILL THINKS [R18] [R27] [R28] [R31]
- The bar is fixed. Every piece is the one that gets a motion designer hired. Go all out, inside his rules [R27].
- NO STILL SECOND [R42] (9 Oct 2026). The storyboard is the start, never the ceiling: improve it. In every second of the final film something moves. Example: after the client orbit lands, its spark keeps running the oval.
- THE LOOK IS PER PIECE [R28] [R31]. Each piece writes its own brief: The showreel brief. His rules hold on every piece. How each one looks is new every time: no motion language, effect list, example brief or past film's look carries over, because one preset line made every film move the same (29 Sep 2026).
- His rules are fixed. A tag [R1] to [R40] marks his rule. The numbers and methods around it are starting points from past films: break one when the shot gets better, and name the break in one line [R18]. His words: `llllloc_workflow/1_Lessons/Your words.md`.
- Easing, transitions, holds, composition and light are Claude's calls. His note after each version steers them. Each version names the one choice Claude is least sure of.

## NO RENDER. NO VIDEO IN THE CHAT [R32] (30 Sep 2026)
He reviews every version live where it was built: the MOTION preview or the Figma Motion timeline. A render costs his time and adds nothing.
1. Build or change the film in MOTION through its connector (`motion_scene_set`, `motion_layer_set`, `motion_content_set`), or in Figma Motion with `use_figma` keyframes on duplicated frames.
2. Check it yourself: `motion_sheet` and `motion_snapshot` in MOTION. In Figma, a small low-quality `export_video`, sampled with ffmpeg, for your eyes only. Fix before you reply.
3. MOTION: save the film (`motion_project save`) and seek the playhead to the moment he should look at first (`motion_seek`). Figma: name the section and the frames.
4. Reply: done, where to look, what changed, the flags, the least-sure choice. No MP4, no PNG frames, no file card.
5. Render only when he says so in words ("render", "export"), or for FINAL DELIVERY after he validates the sound. A render stays on disk in the job folder and reaches him as a file card plus its full path (29 Oct 2026, his ok). The MOTION MP4 export is low bitrate: render PNG frames and encode with REFERENCE A.
6. Figma export he asks for in its own panel format (GIF, MP4): he exports from the Figma Export panel. Claude prepares the frames (transparent frame fill for a clean background) and says so in one line.
- Text he may change lives in Content slots (a text layer, or a code layer with `slots`), and every move is measured from the words, so a new word keeps the animation.

## HE NAMES THE PROGRAM [R37] [R38] (14 Oct 2026, was FIGMA FIRST)
- HE NAMES THE PROGRAM [R37]. He says which program each motion job uses: Figma Motion, his MOTION app, Cavalry, After Effects or code. Never pick one for him. Not named: ask once, in one line. A job moves to another program only on his word. In Figma Motion, work on duplicated storyboard frames. A Figma-to-MOTION handover reads the Figma keyframes directly through the connector (`get_motion_context`, `manualKeyframeTracks`), never a Lottie file. Figma takes no clip or audio from Claude: every clip sits on a card frame's fill as a placeholder, and Claude prepares the VO as an MP4 for him to drop in.
- ALWAYS ADD MORE [R38]. A Figma Motion build never stops at the storyboard's layers. Every version adds elements of its own, in four kinds: support layers (HUD type, counters, marks, scan and pass lights), light that runs the edges, glow that changes over time (a bloom on arrival, a slow color drift, flashes on the big beats), and camera energy (hits on impacts, a shake on THE SIGNATURE, the HUD outside the camera so it stays still). Which ones, and how, are new each piece [R31]: kinds, never a preset. The reply lists what each version added.
- Methods that work in Figma Motion: REFERENCE O.

## THE SHOWREEL BRIEF [R27] [R28] [R31]
Four lines on top of the `## Motion` section of the job's `DesignSystem_<Name>_V<N>.md` (older project: `LOOK-LOCK.md`), written by the lead before V1: The class, what it is not, the language, the signature. Read `references/showreel-brief.md` in full before you write it, and run its TEST on every version.

## THE KIT [R36] [R41]
Code on his drive (`kit/README.md`). MOTION is his preview and swap desk, never the limit. Text, animation and easing always stay editable. Detail: `references/build-pipeline.md`.

## THE VERSION LADDER
1. Picture. V1, V2 and on at 1920 x 1080, 30 fps, live in MOTION. VO only. No SFX, no music, no placeholder bed [R19]. No render [R32].
2. Sound. He validates the picture. Then SFX, music and subtitles are built in Premiere Pro on the locked picture (18 Oct 2026): `llllloc:task-sound-design`, each sound its own clip. One sound review in Premiere.
3. Master. He validates the sound. Then FINAL DELIVERY at 1920 x 1080, 30 fps, because 4K renders too long. 4K only when he asks for it on one job [R3]. Section keyframes go in. Rasters sit at 2x, so a later 4K ask needs no rebuild. Encode: REFERENCE A.

## START OF EVERY MOTION TURN
1. Read `**_MOTION/_STATE/MOTION-STATE.md`, the job's newest `*_CLAUDE/3_Art Direction/DesignSystem_<Name>_V<N>.md` (its `## Motion` section holds the brief, its `## Master and parts` the pieces to copy; older project: `LOOK-LOCK.md` or `ART-DIRECTION.md` until a V1 replaces them), and in a lane `**_MOTION/P<n>/_STATE/STATE-P<n>.md` (older project: `*_CLAUDE/7_Motion/` or `ANIMATION/`, then move it, `llllloc:task-files-organize` THE MOTION RULE). Then the handoff and `VISUAL-PREFERENCES.md`. The design system wins. None yet: `llllloc:task-design-system` runs first and the film waits for his pick (17 Oct 2026).
2. Request access to `~/Desktop/Claude` once (the kit is in `llllloc/2_Skills/Job skills/task-motion/`). `motion_status` first: which film MOTION holds. Save his open film before you open or make another.
3. RESEARCH PASS [R14], cache first: `llllloc/5_Research cache/jobs/motion/_TOPICS.md`, then only the topic files this job needs, and the project's own `*_CLAUDE/2_Research/` (`sound.md` at the sound stage, `video-delivery.md` for an encode). THE LOOK, THE GRADE (premium against cheap, with numbers), THE BUILD (best code method, what breaks). A revision asks only the new question. The reply names what the findings changed.
4. No brief yet: the lead writes the showreel brief.
5. STORYBOARD SCAN [R29] [R34], before any animation of new or changed frames. Open every storyboard frame at full size, and read its layers with `get_metadata`: copy each line, dot, leader and tile in pixels, never by eye. Check each dot sits inside its country, and that a country in several parts (Malaysia: the peninsula and Borneo) reaches every part, with the line passing each ringed dot. Check each frame and each move between them: mistakes, what makes no sense, a layer that must move with the camera but sits still (v9A grid), safe zone, missing parts, text, where THE SIGNATURE lands. Propose the list, fix the design on his yes (`llllloc:tool-figma`), then animate.

## PIPELINE, SYNC [R2], PACING [R15], CARDS [R12], CRAFT, REFERENCE BUILD
Read `references/build-pipeline.md` in full before the first build of a film and before any retime. SYNC is a gate: text lands on the voice, and `sync.py` reports ALL OK before every hand-off.

## QUALITY GATES
Tested methods: REFERENCE C, D, H, N.
- ASSETS [R1]: rebuild every element in code first. Export from Figma only a photo, a complex illustration or an exact logo, 2x or more. Text is real fonts or vector paths. A Figma typo takes the VO wording, flagged.
- SHARP [R7] [R9]: every shape, line, text and card is a vector path at output size. Never a raster scaled up. A lit object is a hard edge with the glow outside it. Never smooth across the edge. Test at 200% and 400%.
- NO BANDING, NO SMOKE [R1] [R10]: half-float canvas to the last step. Glows and fields are smooth math, never an 8-bit plate or accidental noise in a fill. Grain, dither, AQ mode 3 and the dark-crop check: REFERENCE A and C.
- FIGMA SIDE BY SIDE [R35] (2 Oct 2026). A GATE, before every hand-off, V1 included. The MOTION snapshot beside the Figma frame, cropped at 100% and 400%, at every cut, card, line join and line end. Glow, stroke and color within 15 levels of the design. A clip in a small card stays sharp. No glow ends in a hard edge, a wedge, a step or a box. Edges stay crisp at any zoom. Size from Figma (9 Oct 2026), any tool: every element box matches `get_metadata` within 2 px. A PNG with glow bleed is scaled so its core (alpha 50%+) fills its Figma box. Method: REFERENCE N.
- Full frame (11 Oct 2026): the background fills every pixel of every frame, camera moves and pushes included. A whole-film sweep proves it before hand-off. Method: the tool's skill.
- LIVING GRADIENTS AND GLOWING EDGES [R4] [R11], on every piece: every gradient moves, and every lit edge glows with moving light. The test: a color source moves at least 10% of its box in 2 s. Colors, forms and motion are new for each piece [R31]. Learn from high-end website gradients (one method: `fields.py`, REFERENCE D).

## BUILD FOR HIS HANDS [R33] [R36] (30 Sep, 2 Oct 2026)
He edits every film after Claude in the MOTION app. He needs three things in his hands: the text, the animation and the easing. Read `references/build-for-his-hands.md` in full before the first build of a film, and before the V1 reply (it owes him THE LAYER MAP).

## SOUND STAGE [R19]
Only after he validates the picture, and always in Premiere Pro (18 Oct 2026): `llllloc:task-sound-design` owns it. Read `references/sound-stage.md` for the stems and the loudness target.

## FINAL DELIVERY, SECTIONS, PARTS, HANDLE, FILES [R20] [R3] [R25] [R26] [R6] [R21] [R39] [R8] [R40] [R22]
Read `references/delivery-and-parts.md` in full when: he validates the sound (FINAL DELIVERY, five files), a film has parts or sections (SECTIONS, STITCH), he will cut the animation into an edit (TWO SECONDS OF HANDLE), he names a render and asks for its project (RENDER TO PROJECT), or any file goes to disk (DELIVERY: names, folders, the reply). A video never comes to the chat [R32].

## A NOTE IS A FAST NOTE [R6] [R8]
He may name a scene, a film timecode or a frame. Any of them is enough. Never ask which part.
1. Find it: film time to its part (join times in `MOTION-STATE.md`), then that part's layers in MOTION. `SECTIONS.md` gives the section.
2. Change only what he named. Other parts and sections stay.
3. `sync.py` and QC on the changed frames. Save, seek to the change, tell him it is done [R32].
- After delivery, a text-only note re-renders only the TEXT layer. BG stays.
- Time, then go: the first reply line states the estimate (REFERENCE K), then continue at once.
- "Follow part N's style" reuses its motion and gradient animation only. The storyboard design stays [R30].

## QC. ALL PASS OR NO HAND-OFF
1. Size, fps, duration. 2. `sync.py` All ok. 3. No jump except on planned cuts. 4. Every QUALITY GATE, FULL FRAME and sizes included. 5. The sheet at every cut and at the signature. 6. Spelling. 7. Sound stage: loudness, stems add up to the mix. 8. Keyframes sit on the section starts. 9. Final delivery: the checks in REFERENCE L, including bitrate floor on the encoded file. 10. THE TEST of the brief.

## PARALLEL CHATS (LANES) [R16] [R17]
`llllloc:project-creatives` section 4. A lane keeps `**_MOTION/P<n>/_STATE/STATE-P<n>.md` (version, film, VO span, end state, notes, PROPOSALS), reads the DesignSystem file before code, and reads the previous part's end state for the join.