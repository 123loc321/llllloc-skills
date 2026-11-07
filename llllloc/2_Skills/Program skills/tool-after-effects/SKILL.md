---
name: tool-after-effects
description: "How Claude drives Adobe After Effects 2026 on his Mac through the Synthetic ae-mcp connector (panel mode) for llllloc and the studio. Runs when the user types its name, or when /llllloc:router picks it for one request: any job that builds, edits, animates, checks or renders a comp in After Effects. Holds universal rules only: the bridge check, setup facts, the version rule (duplicate, never overwrite), the rig for his hands (one control layer per look, text boxes that resize, text on Essential Graphics), the project panel sort, scripting traps and render rules. Sits beside llllloc:task-motion: llllloc:task-motion owns the craft, this skill owns how After Effects and the connector behave. Never renders a video, saves as a new file, or retries a dead bridge on its own. Saves his open project itself (Cmd + S)."
---

# llllloc:tool-after-effects

Claude drives his live After Effects through the Synthetic ae-mcp connector, in panel mode. He reviews in the After Effects viewer. No render unless he asks.

This skill holds universal After Effects knowledge only (9 Oct 2026). A job's look lives in its `*_CLAUDE/3_Art Direction/DesignSystem_<Name>_V<N>.md` (older job: `ART-DIRECTION.md`), written by `llllloc:task-design-system` (17 Oct 2026). Its comp build lives in `*_CLAUDE/7_Motion/AE-BUILD.md`. His exact words go to `*_CLAUDE/FEEDBACK-LOG.md`. A job note goes to those files, never into this skill. A rule changes only when he says so in words.

## TOP RULES
1. Check the bridge first. Every tool goes through the panel inside After Effects. A stopped panel makes every call wait out its full timeout (9 Oct 2026: three calls hung 20 to 60 s each).
2. Never overwrite a comp he has seen. Archive the whole tree, then edit the working copy (VERSIONS).
3. No render and no save-as unless he says so. A render goes to disk only, and the reply gives its path (house RULE 5). Cmd + S on his open project is Claude's job (SAVING).
4. One dead call, one stop. A timeout means stop and tell him what to click. Never fire a burst of retries at a busy or stopped session.
5. Rig for his hands. Every build ships with its look settings on one control layer and its text in resizing boxes on Essential Graphics. A build without them is not finished.
6. No edge ever shows (11 Oct 2026, missed three times). Before every hand-off: FULL FRAME SWEEP in CHECKING THE PICTURE, a fail sends you back to the fix.
7. SORT CHECK IS THE LAST STEP OF EVERY TURN that touched the project (PROJECT PANEL). The project panel matches Cavalry and Premiere, folder for folder (10 Oct 2026).

## MAIN COMP AND SCENES (11 Oct 2026)
- Stack scenes in time order: the first scene at the bottom, each later scene above the one before, so the bars climb up and to the right. Why: an incoming scene must sit over the outgoing one for a transition.
- The VO layer is always locked, label 8 (white in his label set).
- The design's texture or halftone belongs to each object: one texture copy per object, parented to it and alpha-matted to it, so it moves with the object. Never one texture fixed over the whole comp.
- Script traps: `setTrackMatte` turns the matte layer's video off, so turn the object back on. A track matte that ends before its layer hides that layer: keep the matte as long as the layer.
- Audio is checked in After Effects (12 Oct 2026). Audio first put on a timeline: ffmpeg it to a 48 kHz WAV beside the source (`<name>_48k.wav`), import that, never an MP3 (MP3 VO rendered as noise). Check once: Convert Audio to Keyframes, 10 levels against the source. A miss: re-import. Before a render, every main-comp audio layer is a checked WAV.

## RIG FOR HIS HANDS (9 Oct 2026)
He tweaks a look in one place, and a client's new words never break a layout.
1. One control for a look. An effect setting that repeats across layers (Deep Glow 2, any glow, grain, texture, tint) is driven by one null `<LOOK>_CONTROL` in the main comp, one slider per setting. Its expressions name the main comp, so a new version re-points them (VERSIONS). A per-layer value becomes `value * <slider> / 100` (Radius %, Exposure %, Tint Strength %), so each layer keeps its own look. A shared value links straight (Threshold). Add `Mix %` on each effect's Effect Opacity (`ADBE Effect Mask Opacity`, inside the effect's last group). Every control layer is a guide layer (`layer.guideLayer = true`, so it shows the guide icon and never renders) with his pink label (`layer.label = 12`, checked on screen 9 Oct 2026. Label 10 is green).
2. Text boxes resize from the text. In a card, chip or box, the plate, stroke, divider and padding read the text's `sourceRectAtTime()` by expression, plus the Figma padding. Every move is measured from the words, so a longer word grows the box and keeps the animation.
3. Text on Essential Graphics. Every Source Text a client may change goes to the Essential Graphics of the comp that holds the text, under a plain name (HEADER, VALUE, LABEL): `addToMotionGraphicsTemplateAs(comp, name)`, the same as his drag into that panel. Text in a precomp then shows as Essential Properties on the precomp layer in the main comp. A script cannot add those Essential Properties to the main comp's own panel (`canAddToMotionGraphicsTemplate` is false). A counting number reads its target from the typed text, so the Source Text stays the field.
4. CHECK, then go back on a fail. Set one slider to 50 and read a linked value with `valueAtTime`. Type a long test string into one field, export a frame, see the box grow, restore the text.
- Deep Glow 2 shows "Unlicensed" on his Mac. That is normal. Never report it.

## START OF EVERY AFTER EFFECTS TURN
```
- [ ] 1 ae-mcp tools loaded in one ToolSearch
- [ ] 2 Bridge answered
- [ ] 3 Scene probed, target comp named
- [ ] 4 Job files read
```
1. Load every ae-mcp tool the job needs in one ToolSearch call (`select:` with a comma list). List `llllloc/4_Lessons/Programs/After Effects/` and read only the file that matches the job. No match: read nothing (16 Oct 2026, his words: read only the lesson that is needed).
2. Probe with `get_ae_version` and `timeoutMs` 20000. Not `panel_healthcheck` (it hung 60 s). `"ok": true` means go. A "Bridge timed out" result means the panel is stopped. Stop and send him BRIDGE DOWN below. Go back to step 2 only after he says it runs.
3. Probe the project: `project_info` or `list_comps`, then `list_layers` on the comp you will touch. Never assume the scene state. Comp indexes shift when he imports, so address comps and layers by name.
4. First After Effects turn of a job: read the newest `DesignSystem_<Name>_V<N>.md` (its `## Motion` and `## Master and parts` sections first) and `AE-BUILD.md`. No design system yet: `llllloc:task-design-system` runs first. No `AE-BUILD.md` yet: create it when the first build decision lands. Each feedback round: his words to `FEEDBACK-LOG.md`, a changed look to the current DesignSystem version, dated (`llllloc:task-design-system` NEW VERSION), a changed build to `AE-BUILD.md`.
5. A tool family used for the first time in a chat: read its built-in guide with `ae_help` and `topic` (`getting-started`, `layers-and-3d`, `keyframes-and-expressions`, `text`, `shapes-masks-mattes`, `effects-and-layer-styles`, `render-and-export`, `motion-tools`, `scripting-and-recovery`). The guide is free and current with the server version.

## BRIDGE DOWN: WHAT TO SEND HIM
Three lines, no more:
- In After Effects: Window > Extensions > Synthetic AE MCP, click Start bridge.
- Leave the Temp directory as it is. It resets to its default, and the connector follows it (1 Nov 2026). The status must read `Running`.
- Tell me when it runs.

## SETUP FACTS (9 Oct 2026)
Server, panel, license, bridge folder and permissions: read `references/setup-facts.md` when the bridge, the license or a script permission fails. Which app builds a job is his call per job. Never move a job between apps on your own.

## VERSIONS: THE WHOLE COMP TREE, NUMBERED (11 Oct 2026)
Why: he compares and rolls back a whole version, never loose boards. Applies in every motion app (Cavalry points here).
1. The first call of every change round archives the tree he has seen: duplicate the main comp and every precomp it holds.
2. The copies go to `**_EXPORT/<Scene>/OLD VERSIONS/<version>/`: `<Main>_<version>` (for example `Act 1_AE_V1`) and each precomp `<name>_<version>`. Point each archived main-comp layer at its archived precomp (`replaceSource`).
3. The working main comp gets the next number: `Act 1_AE_V1` becomes `Act 1_AE_V1.1`, then `V1.2`. The `_AE_` tag is his naming rule (18 Oct 2026, `llllloc:task-files-organize` THE RENDER RULE). Working precomps keep their plain names. Edit only the working tree.
4. Sliders live on `MOTION_CONTROL` in the working main comp (his choice, 12 Oct 2026). On every new version, re-point the working precomps' expressions to the new main-comp name. The archived precomps keep the old name, which is their archived main comp.
5. Check: `list_layers` on each archived main comp names only `_<version>` precomps, and the working main comp names none. A miss: go back to step 2.
- Build leftovers and partial backups go to `OLD VERSIONS/V0 (...)`. Never delete.
- Remove layers inside a version only on his word.

## PROJECT PANEL: THE SHARED BIN TREE (10 Oct 2026, shared 25 Oct 2026)
AE, Premiere, Cavalry and DaVinci keep one bin tree: `llllloc:task-files-organize` `references/bin-tree.md` (tree, where each item goes, versions, SORT CHECK). Read it before a turn that adds, renames or moves an item. AE only: `references/project-panel-sort.md`.
- Sort check: `create_folder` for any missing folder, `move_items_to_folder` for every loose item, then `list_project_items`. The reply says `Assets sorted`.

## SAVING
- Claude presses Cmd + S (12 Oct 2026, his word: full permission). Save his open project with `app.project.save()` in `run_jsx_json`, inside its own call, after the change round is checked and before any step that reads the file from disk (a render, `export_frame`). Why: asking him cost a round trip.
- Same file only. Never `save_project_as` or a new path unless he names one. An untitled project: ask where to save, then `save_project_as` with a path built from the project folder listing.
- A save the app blocks: say so in one line and ask him to press Cmd + S. Never retry it another way.

## SCRIPTING TRAPS
ExtendScript is ES3, every change sits in one undo group, and nothing may open a modal dialog. Read `references/scripting-traps.md` in full before the first script or tool call that changes the project in a chat.

## CHECKING THE PICTURE
- An unsaved project: `comp.saveFrameToPng(t, File)` in `run_jsx_json` writes a still into `Desktop/Claude/_DELETE/ae-check/`. Stage it to look. `export_frame` needs a saved `.aep`. The call returns at once: wait for the file count.
- Full frame sweep (11 Oct 2026, gate in `llllloc:task-motion`), before every hand-off. The main comp at `resolutionFactor` [2,2], a still every 4 frames, then full size every frame from 3 before to 19 after each cut. A fail: any edge or inner row or column with over 5% of pixels under alpha 250 (the grey comp background renders transparent). Two causes found: a 3D back plane sized for a still camera (scale it for (Zoom + z) / Zoom at its worst camera frame, plus 5%), and two scenes pushed edge to edge (the incoming one rides 6 px under the outgoing one by expression, clamped at its rest position). Third cause (AB14): a distortion effect (Wave Warp, displace, warp) on art that reaches the frame edge pulls in pixels from outside the layer. Set Pinning to All Edges, or give the art 10% overscan. Sweep each scene comp alone too: a main-comp safety solid hides a gap, and a gap over black reads alpha 255, so look at the edges of every distorted or moving full-frame layer.
- A Figma layer with background blur exports as an opaque PNG with the card behind it baked in. Rebuild it natively: the vector path from its SVG, its raw image fills from `download_assets`.
- Check a look against its source by numbers (position, size, color values from `get_transform`, `get_property_value`), not by eye alone.

## RENDER (12 Oct 2026, his word)
Only on his word. The After Effects render queue, never Media Encoder, H.264 10 Mbps into `1_VISUAL ASSET/Transfer render/From AE/` (into `4_RENDERS/` only when After Effects is the last app: `llllloc:task-files-organize` THE RENDER RULE). Read `references/render.md` in full before the first step. A review round renders only the corrected parts and patches them into the last render: PATCH in that file (1 Nov 2026).

## IMPORT FROM ILLUSTRATOR (1 Nov 2026)
Read `references/ai-to-ae-import.md` in full before the first import of a job: his hand route, the two Claude routes, colours, art past the frame, text and traps.

## REPLY
Lead with done or not done. Name the comp to open. State every default you picked that he did not give (length, fps, size). Flag what was not checked. Say that the project is saved.