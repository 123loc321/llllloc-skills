---
name: tool-blender
description: "How Claude drives Blender 5.2 on his Mac through the official Blender Lab MCP connector (blender) for llllloc and the studio. Runs when the user types its name, or when /llllloc:router picks it for one request: any job that reads, builds, edits, lights, animates, checks or renders a scene in Blender. Holds universal rules only: the bridge check, setup facts, read tools before code, the modeling method (route, size table, parts, blockout, number checks), material rules, image-to-3D cleanup, the version rule (save a numbered copy, never overwrite what he has seen), the code safety rule, render rules and his own rules. Sits beside llllloc:task-motion: llllloc:task-motion owns the craft, this skill owns how Blender and the connector behave. Never renders, saves over his file, or retries a dead bridge on its own."
---

# llllloc:tool-blender

Claude drives his live Blender through the official Blender Lab MCP (connector `blender`, 26 tools). He reviews in the Blender viewport. No render unless he asks.

This skill holds universal Blender knowledge only (19 Oct 2026). A job's look lives in its `*_CLAUDE/3_Art Direction/DesignSystem_<Name>_V<N>.md`. Its scene build lives in `*_CLAUDE/7_Motion/BLENDER-BUILD.md`. His exact words go to `*_CLAUDE/FEEDBACK-LOG.md`. A job note goes to those files, never into this skill. A rule changes only when he says so in words.

## TOP RULES
1. Check the bridge first. Every tool talks to the add-on inside Blender on localhost port 9876. Blender closed or the add-on off: every call fails with "Cannot connect to Blender".
2. Read before you write. Use the read tools (`get_objects_summary`, `get_object_detail_summary`, `get_blendfile_summary_*`, screenshots) before any change. `execute_blender_code` is the last resort, when no other tool does the job.
3. Code runs with no guard. Blender's own warning: the server runs Python Claude writes inside Blender, with no safety net. Never write, move or delete a file outside the job folder from code. Never delete objects or data without his yes (core HARD STOP 2).
4. Never overwrite a scene he has seen. Save a numbered copy first (VERSIONS).
5. No render and no save over his file unless he says so.
6. One dead call, one stop. A failed connection means stop and send BRIDGE DOWN. Never retry in a burst.
7. Every model follows MAKING A MODEL: route first, sizes before geometry, numbers after every step. Why: Claude judges size and proportion badly by eye. In the 6 Nov 2026 bake-off the method gave 0% proportion error, the one-prompt way 10.9% and a bottle 20 times too big.

## HIS RULES
His own rules for Blender go here, one dated line each, in his words made short (core rule 8).
- 6 Nov 2026: the modeling method below is his rule ("Yes, update skill", after the perfume bottle bake-off).

## MAKING A MODEL: ROUTE, SIZE, CHECK (6 Nov 2026)
Proof and scores: `/Volumes/CREATIVE #1/261106_llllloc_Blender Bake-off/*_PROJECT FILES/*_CLAUDE/8_3D/BAKEOFF-RESULTS.md`. Research: `llllloc/5_Research cache/deep research/reports/Claude Blender modeling quality.md`.
```
- [ ] 1 Route named
- [ ] 2 Size table written (metres, 3 to 6 ratios)
- [ ] 3 Parts list
- [ ] 4 Box blockout, numbers checked
- [ ] 5 Clay views shown, shape approved
- [ ] 6 Detail, then materials, then light
- [ ] 7 Numbers and views checked again
```
1. ROUTE, before any geometry. Products and hard objects with a known size (bottle, device, box, furniture): Claude builds them in code. Anything transparent (glass, liquid) always stays in code: image-to-3D paints glass opaque (Tripo P2 and Hunyuan 3.1 both did). Organic things (character, animal, food, plant, cloth): image-to-3D on Magnific, then Claude cleans. Common real objects: an asset library first. Scenes: a kit of parts first, then one room at a time.
2. SIZE TABLE. Real size in metres plus 3 to 6 key ratios, written in the job's `BLENDER-BUILD.md`. He gave no size: pick a real-world default, say so in the reply.
3. PARTS LIST. Name every part. Each part is its own object, named `<Version>_<Part>_<Material>`. Glass and liquid are separate objects with a small gap.
4. BLOCKOUT. One box or cylinder per part at its exact size, scale 1, base on the floor (z = 0). Build exact geometry with bmesh, never by scaling a default cube.
5. NUMBER CHECK, after every step: each part's dimensions against the table, the ratios, gaps between parts that should touch (0), nothing floating, scale 1, 1, 1. Show it as a short table. A miss: fix it, check again.
6. CLAY GATE. Flat front and side views (orthographic camera) beside the reference, plus one three-quarter view. He approves the shape before materials. A bake-off or a test he asked to run end to end: go on, and show the views in the reply.
7. STAGES. Shape, then materials, then light. A later stage never edits an earlier one. Detail with modifiers (Bevel on every hard edge, Boolean for hollows, Mirror), never by moving single points.
8. ROUND CAP. At most 5 fix rounds per stage. Then keep the best and report what is left.
9. DOCS FIRST. Search the bundled 5.2 docs (`search_api_docs`) before a command not used before. Blender 5.2 changed some geometry-nodes code.
10. ONE CONNECTOR. Only the official Blender MCP. The community mcp-for-blender uses the same port 9876 and the same name: never add it without his yes.

## MATERIALS (6 Nov 2026)
1. Real surfaces (wood, metal, fabric, stone): scanned CC0 maps from Poly Haven or ambientCG. A download needs his yes. Clean plastic, glass, metal: Principled values from physicallybased.info. Never invented noise on a hero object. Logos: his artwork only.
2. Wiring: the colour map is sRGB. Roughness, metal, normal and height maps are Non-Color. A normal map goes through a Normal Map node (Blender is OpenGL style). Metal is 0 or 1. Texture scale matches the real size.
3. Tested values: glass Transmission 1, Roughness 0, IOR 1.5. Liquid colour comes from a Volume Absorption node, not the surface colour (surface colour came out pink): density about 70 for 5 cm of amber. Gold Metallic 1, linear base (1.0, 0.71, 0.29), Roughness 0.15. Matte black base 0.015, Roughness 0.4.
4. Judge materials under two lights with AgX. Three area lights alone blow out a three-quarter view: use a studio HDRI (Poly Haven, his yes).
5. Render and compare with the reference after each change. Cycles glass at 48 samples, 700 px takes about 1 minute. Queue renders with `bpy.app.timers` so the tool call does not time out.

## IMAGE-TO-3D CLEANUP (6 Nov 2026)
1. Input: one clean front view on plain grey, side views from Magnific `change-camera-angle`. Hunyuan 3.1 still built the bottle 28% too slim, matching the side view: measure every result.
2. Every engine result arrives at the wrong size and turned sideways: rotate, scale to the size table, centre, set on the floor.
3. A GLB holds triangles only, so Tripo P2's quads are lost. The mesh is one piece: split by part before any material fix. Retopology: `llllloc/4_Lessons/Programs/Blender/retopology.md`.
4. Measure it like a code model: width profile per height slice, ratios, face count, which maps came with it (Tripo P2: colour only. Hunyuan 3.1 Pro with PBR: colour, metal, roughness, normal at 4K).

## START OF EVERY BLENDER TURN
```
- [ ] 1 blender tools loaded in one ToolSearch
- [ ] 2 Bridge answered
- [ ] 3 Scene probed, target named
- [ ] 4 Job files read
```
1. Load every `mcp__blender__` tool the job needs in one ToolSearch call (`select:` with a comma list). List `llllloc/4_Lessons/Programs/Blender/` if it exists and read only the file that matches the job.
2. Probe with `get_objects_summary`. A status `ok` means go. "Cannot connect": stop, send BRIDGE DOWN. Go back to step 2 only after he says it runs.
3. Probe the file: `get_blendfile_summary_path_info` for the file path and its saved state, then `get_object_detail_summary` on the object you will touch. Never assume the scene state. Address objects by name.
4. First Blender turn of a job: read the newest DesignSystem file and `BLENDER-BUILD.md`. No `BLENDER-BUILD.md` yet: create it when the first build decision lands.

## BRIDGE DOWN: WHAT TO SEND HIM
1. Open Blender, if it is closed.
2. Edit > Preferences > Add-ons, search MCP, tick it. Open its arrow and click Start if it shows.
3. Tell me when it runs.

## SETUP FACTS (19 Oct 2026)
- Blender 5.2.2 LTS at `/Applications/Blender.app`. The add-on needs Blender 5.1 or newer.
- Add-on `mcp` 1.0.3 in `~/Library/Application Support/Blender/5.2/extensions/user_default/mcp`. Auto Start is on by default.
- Server `~/.blender-mcp/venv/bin/blender-mcp`, entry `blender` in the Claude app config. A config change needs a Claude app restart.
- Installers, notes and the update steps: `llllloc/2_MCP/Blender/README.md`.
- Trap: installing the add-on from the command line while Blender is open does not stick. Blender writes its old settings back on quit. Turn it on in Preferences instead.
- The `_for_cli` tools open a .blend in a background Blender. They need no bridge and never touch his open scene. Use them to read a file he has not opened.

## VERSIONS: A NUMBERED COPY, NEVER OVERWRITE (19 Oct 2026)
Why: he compares and rolls back a whole version (same rule as `llllloc:tool-after-effects` VERSIONS).
1. The first call of every change round saves a copy of the file he has seen: `bpy.ops.wm.save_as_mainfile(filepath=<OLD VERSIONS path>, copy=True)`. The open file stays the same.
2. The copy goes to `OLD VERSIONS/` beside the .blend, named `<name>_V<N>.blend`. Take the path from the file path probe, never a guess.
3. An unsaved file has nothing to copy: ask where to save it first.
4. Check: list the folder, the copy is there. A miss: go back to step 1.

## SAVING
- Claude does not save over his open file (default, 19 Oct 2026). After a checked change round, tell him to press Cmd + S. He can change this in HIS RULES.

## CHECKING THE PICTURE
- Numbers decide, the picture is the second check: a picture judge agreed with people only 66% of the time (BlenderGym). Read size, location and colour values from `get_object_detail_summary` or a read-only code call. Then look with `get_screenshot_of_area_as_image` (the 3D viewport) or a render.
- After a change, update the dependency graph before reading computed values (world matrix, modifier results).

## RENDER
Only on his word. `render_thumbnail_to_path` and `render_viewport_to_path` are quick checks and may run for a look. A full render goes to disk only, and the reply gives its path. Output folder: `llllloc:task-files-organize` THE RENDER RULE.

## REPLY
Lead with done or not done. Name the object or file to look at. State every default you picked that he did not give. Flag what was not checked. Say whether the file is saved.
