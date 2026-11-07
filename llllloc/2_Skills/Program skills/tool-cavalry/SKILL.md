---
name: tool-cavalry
description: "How Claude drives Cavalry (Canva's motion app) through the Cavalry MCP connector for llllloc and the studio. Runs when the user types its name or when /llllloc:router picks it for one request: any job that builds, edits, animates or checks a scene in Cavalry. Holds universal rules only: the version rule (duplicate, never overwrite), the crash budget and save points, render and fps methods, and the API traps found in real jobs. A job's look and rig live in its *_CLAUDE files. Sits beside llllloc:task-motion: llllloc:task-motion owns the craft, this skill owns how Cavalry behaves."
---

# llllloc:tool-cavalry

Claude drives Cavalry live through the Cavalry MCP connector. He reviews in the Cavalry viewport. No render unless he asks.

This skill holds universal Cavalry knowledge and key working rules only (3 Oct 2026). A job's look lives in its `*_CLAUDE/3_Art Direction/DesignSystem_<Name>_V<N>.md` (approved, and rejected in its `## Rejected`; older job: `ART-DIRECTION.md`), written by `llllloc:task-design-system` (17 Oct 2026). Its scene build and rig live in `*_CLAUDE/7_Motion/CAVALRY-BUILD.md`. His exact words live in `*_CLAUDE/FEEDBACK-LOG.md`. A job note goes to those files, never into this skill. A rule changes only when he says so in words.

## EASING: BEZIER WITH HANDLES, NEVER MAGIC EASING (2 Nov 2026, his words)
"dont use Magic Easing, please always use Bezier with handle in easing so i can control manually". Why: Magic Easing shows no handles in the Graph Editor, so he cannot shape the curve.
1. Never set a Magic Easing name. A script keyframe takes `api.modifyKeyframeTangent(id,{attr:{frame,outHandle:true,inHandle:false,type:2,xValue,yValue}})` on its out handle, and the same with `inHandle:true,outHandle:false` on the next key. `xValue` and `yValue` are the absolute frame and value of the handle tip.
2. Handle tips as a share of the move: slow out 1/3, 2/3 and 2/3, 1. Slow in 1/3, 0 and 2/3, 1/3. Slow in and out 0.45, 0 and 0.55, 1. Very slow out 0.22, 1 and 0.36, 1. Constant 1/3, 1/3 and 2/3, 2/3.
3. A key that already has Magic Easing: `api.magicEasing(id,attr,frame,"None")` first, or the handles are ignored.
4. A spring or overshoot: extra Bezier keys, not a Magic Easing name.
CHECK: `api.getMagicEasing` is "None" on every key of the comp, and a mid-move value differs from linear. Fail: go back to step 3.

## START OF EVERY CAVALRY TURN
1. Call `read_preamble` once per chat, and again after every Cavalry restart. Load every Cavalry tool in one search pass.
2. First Cavalry turn of a job: read the newest `DesignSystem_<Name>_V<N>.md` (its `## Motion` and `## Master and parts` sections first) and `CAVALRY-BUILD.md`. No design system yet: `llllloc:task-design-system` runs first. No `CAVALRY-BUILD.md` yet: create it when the first rig decision lands. Then list `llllloc/4_Lessons/Programs/Cavalry/` and read only the file that matches the job (16 Oct 2026, his words: read only the lesson that is needed).
3. Probe first: list the comps, the active comp and the layer count of the comp you will touch. Never assume the scene state. After a crash, Cavalry may reopen an older save.
4. Name the comp you will change. Start every script with `api.setActiveComp(<id>)`. A script that skips this writes into whatever comp is open.
5. Each feedback round: his exact words to `FEEDBACK-LOG.md`, a changed look to the current DesignSystem version, dated (`llllloc:task-design-system` NEW VERSION), a changed rig to `CAVALRY-BUILD.md`.
6. VO in every comp (9 Oct 2026). A comp that plays under a voice holds its VO as a sound layer named `VO (review only) - <first words>`, at the same offset as in his edit, so he reviews the pacing in Cavalry. `api.loadAsset` the file, `api.addAssetToComp`, file the asset in `3_SOUND ASSET/VO`. Render with `generator.exportAudio` false: the VO already sits in Premiere.
7. Last step of every turn: the SORT CHECK in assets panel. It was skipped on 9 Oct and he had to ask.

## VERSIONS: DUPLICATE, NEVER OVERWRITE (3 Oct 2026)
- The first call of every change round duplicates the comps he has seen (`api.duplicate(compId,false)`, 450 layers copy fine). Then edit the copies. He caught one round built on a version he had seen.
- Name: `<Video>_CAV_V<n>` (his naming rule, 18 Oct 2026, `llllloc:task-files-organize` THE RENDER RULE). The copy takes the next number. The comps he saw keep their names and move to `**_EXPORT/<Video>/OLD VERSIONS/<version>/`.
- A new look on the same 3D build: a new final comp that references the same 3D comp. A change to the 3D build: duplicate the 3D comp too. A duplicated final comp still points at the old 3D comp: `api.createCompReference(newComp)`, move it to the back, delete the copied reference.
- Removing layers inside a version is fine only when he asks for that change.

## ASSETS PANEL: THE SHARED BIN TREE (9 Oct 2026, shared 25 Oct 2026)
Every Cavalry scene uses the bin tree that AE, Premiere and DaVinci use too: `llllloc:task-files-organize` `references/bin-tree.md` (tree, where each item goes, versions, SORT CHECK). Read it before a turn that adds or moves an asset. Cavalry only:
- SORT CHECK, every Cavalry turn, before the reply, in any scene, new or old, with `api.getAssetWindowLayers(true)` as the listing. The reply says `Assets sorted`.
- The API sets no label: ask him for red current comps and green folders.
- Method: `api.createAssetGroup`, `api.parent`, `api.reorder` (layer, the one it goes under). A new group lands on top, so set the order last. `api.unParent` does not reorder.

## CRASH BUDGET AND SAVE POINTS (3 Oct 2026)
Cavalry crashed 6 times in one job. The pattern:
- One `execute_script` call that creates more than about 150 layers can drop the connection.
- A 2.5D comp past about 400 layers, plus filters on a precomp of it, crashes on snapshots.
- A ProRes render of a 459-layer 3D comp crashed. PNG chunks of 300 frames rendered fine (render item `frameRangeMode` 2, `generator` `renderPNG`, `alpha` on). Join them with ffmpeg on his machine.
Rules:
1. Build in steps of 60 to 80 new layers per call. One part, one call.
2. After every build step, ask him to press Cmd + S before the next one. Say it in one line. Unsaved work was lost twice.
3. Snapshots: `maxSize` 420 or less. One snapshot per check, not a burst.
4. On a lost connection: stop, tell him plainly, list what was done, ask him to reopen and save. Then probe before any rebuild.
5. `api.render` blocks: past 60 s the call times out but the render finishes. Check the files on disk. `api.backgroundRender` wrote nothing.

## FIGMA LOOK TO CAVALRY: EFFECT BY EFFECT (9 Oct 2026)
A look that only resembles Figma fails. On 9 Oct a `glowFilter` stood in for Figma's two text shadows, and he saw at once that the glow on the big number was wrong. Rebuild each Figma effect with its own Cavalry twin:
1. Read the node's `effects`, `fills`, `strokes` and `strokeAlign` with `use_figma`: colors, alpha, radius, offset, gradient transform. Never read them off a screenshot.
2. Map one to one. Colors as 8-digit hex, which is ARGB: `#AARRGGBB`.
   - DROP_SHADOW: `dropShadowFilter`, `offset` 0 unless Figma has one, `shadowColor` with the Figma alpha. Never `glowFilter`.
   - INNER_SHADOW: `innerShadowFilter` on the shape. Figma y runs down: Figma offset y -30 is Cavalry `offset.y` +30.
   - Linear fill, transform identity: `gradientShader` `generator.rotation` 0, left to right. Not 90.
   - Gradient stroke: `stroke.colorMode` 0, white `stroke.strokeColor`, a `gradientShader` connected into `stroke.colorShaders`. `colorMode` 1 runs the colors along the path, not across the box.
   - `strokeAlign` INSIDE: `stroke.align` 1 (0 centre, 2 outer).
3. Filters in one `filters` list chain: the second shadow also shadows the first. Measured once (text 138 px): Figma radius 32.8 at 85 % became `amount` 18 at 65 %, radius 9.4 became `amount` 5. A start point, not a law.
4. CHECK BY NUMBERS before any render he sees. Render one frame (`renderPNG`, `frameRangeMode` 2, `frameRange` x = y) into a connected folder, pull the Figma frame with `get_screenshot` at 1920, and compare pixels at the glow edge, the glass center and the border. Over 15 levels off: fix, render, compare again. A snapshot by eye is not the check.

## RENDER AND FPS METHODS
- Render folder: `1_VISUAL ASSET/Transfer render/From Cavalry/`, or `4_RENDERS/` only when Cavalry is the last app. Owner `llllloc:task-files-organize` THE RENDER RULE (18 Oct 2026). Element sizes come from Figma `get_metadata` (owner `llllloc:task-motion` R35, SIZE FROM FIGMA).
- Render item: `api.addRenderQueueItem(comp)`, `api.setGenerator(item,"generator","renderQuicktime"|"renderPNG")`, then `filePath`, `fileName`, `frameRangeMode` 0 (comp start/end; 1 playback range, 2 custom `frameRange`, 3 current frame). `filePath` is a path on his Mac. ProRes 4444: `generator.codec` 2, `generator.proResCodec` 4. MP4: `generator.mp4Quality` 4 (Custom) and `generator.mp4Bitrate` in Mbps.
- Before a render that replaces a file, move the old file into an `OLD VERSIONS` or `_DELETE` folder. Check the result with ffprobe (frames, fps, size) and one frame grab.
- New fps: set comp `fps`, `endFrame`, `playbackEnd`, and set each FRAME behaviour `value` to old/new fps so frame math stays. Then `api.setOutFrame(layer, end)` on every layer, all depths: out-frames stay at the old end and the picture goes black.
- ProRes 4444 does not write the comp background color into alpha: a background-only comp renders transparent. Use a solid shape for a background.
- Split layers for an edit: one comp per layer (background, subject with alpha, graphic with alpha), each a duplicate with the other layers hidden.

## API TRAPS FOUND IN REAL JOBS
- `scale` is double2. `api.set(id,{scale:[1,1,1]})` sets scale to 0. Use `"scale.x"` and `"scale.y"`.
- `blurFilter` `amount` is double2: set `amount.x` and `amount.y`, a plain number does nothing.
- `api.parent` keeps the world transform: under an animated null it bakes a hidden counter-scale or rotation (9 Oct: plates at 0.98, an edge gap he caught). Set position, rotation and scale again after every parent call. CHECK: every full-frame layer's `getBoundingBox` is ±960 x ±540 at frame 0. Off: fix, check again.
- A null that rejects a connection on `position` or `rotation.*`: put a new null above it and drive that one.
- `api.get` on a JS-driven attribute returns a stale value. Check the picture with `snapshot_layer`.
- `snapshot_layer` shows a blank frame past frame 299 in a 90 fps comp. Check late frames by numbers or an ffmpeg frame grab.
- `api.getBoundingBox` on a duplicator ignores per-copy shape transforms. Check copies by snapshot.
- A JavaScript utility can return a 3D value as `[x, y, z]`. It drives a camera `position` in one node.
- Duplicator copies have no z depth. Per-copy 3D needs separate layers.
- A linear `gradientShader` is measured from the layer's own position point, not from its outline (9 Oct 2026). A path drawn far from its position gets one end color only. Center each shape's points on its position first. Rotation 90 plus `reverse` true runs top to bottom. Linear `generator.scale` 1 = 100 %, radial `generator.scale` 100 = 100 %. A shared shader on many small 3D shapes also shows diagonal bands: one shader per large shape.
- Children of a shape with `masks` do not render (9 Oct 2026). Keep them as siblings and connect the parent's `position.y` and `opacity` into them. `api.getInConnection` returns `<id>.id`: strip `.id` before using it as a layer id.
- A layer used as a track matte or a clipping mask (`masks`) is hidden by Cavalry (mask: 9 Oct 2026). To show it AND use it, give the matte or mask its own hidden copy.
- One matte per 3D object per comp. Every layer that uses a 3D precomp as its matte makes Cavalry draw the whole 3D comp again. 16 mattes crashed it. Build a texture in its own flat comp, then put one reference of it on the object with one matte.
- Filter mattes (blur, glow): connect a shape into the filter's `mattes` list, then `mattes.<i>.mode` 3 (Alpha Inverted) to filter only inside it, `mattes.<i>.feather` 100 for a soft edge. Hidden shapes still work as mattes.
- Footage: a rectangle plus `imageShader` (`image` from `api.loadAsset`). Set the rectangle `material.materialColor` alpha 0, or white shows through transparent pixels. An ffmpeg-made ProRes 4444 did not display: load the PNG sequence (`api.loadAsset(firstFrame, true)`, shader `useFootageFps` off, `fps` set).
- Time remap: one `value` CTRL in source frames, one JS (`n0/sourceFps*compFps`) into each linked shader's `time`. `getInConnectedAttributes` does not list `time`: check with `getInConnection`.
- Never `api.set` an attribute he keyframed: it writes a key at the playhead. Check `api.getKeyframeTimes` first.
- Keyframes default to linear. Rotation keyframes 0 to 360 over the loop length loop clean.

## 2.5D METHODS
- Camera: one `planarCamera`, type Look At, `lookAt` on the subject. Orbit with one JS node fed by the FRAME behaviour. Controls are `value` layers named `CTRL <what> (<unit>)`.
- Seamless loop: every JS term runs whole cycles over the loop length, and the loop ends in the state it starts.
- No Cavalry tool bends one flat shape in 3D (checked in the docs, 3 Oct 2026). Curve a flat part by cutting it into slices, each a child null rotated by a CTRL value.
- Many small 3D squares: One editable shape per color whose path holds many square contours, not one layer per square.
- Grain: `sceneGroup::grainFilter`, monochrome, size about 0.7. Large sizes read as blotches.

## REPLY
Lead with done or not done. Name the comp to open and the frame to look at. List the controls he will use. Flag what was not checked. Name the least-sure choice. Remind him to save.