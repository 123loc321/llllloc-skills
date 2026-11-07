---
name: task-retopology
description: Turns a dense AI-generated 3D model (Tripo, Hunyuan, Magnific, Meshy, any picture-to-3D output, often 100k to 1M triangles) into a clean, light all-quad mesh with its texture baked back, using Instant Meshes in the cloud, then checks it by numbers and a contact sheet. Use when he asks to retopologize, remesh, clean up, lighten or "make quads" on a 3D model, or drops a .glb/.obj/.fbx and says it is too dense. Picks the route by use (still render, animation, game, print) and names the paid options (Quad Remesher, Magnific remesh) without running them. Never for building a scene or a model from scratch (llllloc:tool-blender), never for a 2D image.
---

# llllloc:task-retopology

Retopology means rebuilding a model's surface with fewer, cleaner faces. AI models come out as a fog of tiny triangles. That is fine to look at, but heavy, and impossible to rig, edit or texture by hand.

## TOP RULES (19 Oct 2026, tested on a 548k-triangle Tripo model)
1. Default route: Instant Meshes in the cloud with `scripts/retopo.py`. It gave 100% quads, 0 holes, 4 seconds per mesh, and kept the shape within 0.13% on average (1.2% worst spot). The texture bakes back onto the new mesh.
2. Never start with Blender's QuadriFlow on an AI model. Blender 5.2.2 refused that model 8 ways: raw, welded, decimated, and voxel-remeshed at 4 sizes. It only accepted the Instant Meshes result.
3. Decimate keeps the shape best but leaves triangles with seam scars. Use it only for a far background prop.
4. Paid tools run only on his yes: Quad Remesher (Exoside, best edge loops, $109.90 one-time Pro or $15.99 per 3 months, exoside.com/quadremesher/quadremesher-buy) and Magnific `models3d_remesh`.
5. The output goes to the job's folder, found by its map row or an `ls`. No folder found: stop and ask (core HARD STOP 5).

## PICK THE ROUTE
| His use | Target | Route |
|---|---|---|
| Still render, turntable, video close-up | 12k quads | Instant Meshes + bake |
| Video wide shot, real-time, web viewer | 5k quads | Instant Meshes + bake |
| Animation with a rig (face, elbows, knees bend) | 12k quads as a base | Instant Meshes, then hand fixes in Blender: loops around eyes, mouth and joints. Offer Quad Remesher if loops matter. |
| Hard-surface (robot, car, product) | 5k to 12k | Instant Meshes with `--crease 30` to keep sharp edges |
| 3D print | none | Keep the dense model. Retopology only loses detail. |

## STEPS
```
- [ ] 1 Model file in the cloud
- [ ] 2 Tools installed
- [ ] 3 Script run, report read
- [ ] 4 Sheet looked at
- [ ] 5 Files in the job folder
```
1. Get the file. An upload is already in the cloud. A file on his Mac: `device_stage_files`.
2. Install once per thread: `python3 -m pip install bpy pynanoinstantmeshes pillow numpy`. bpy is Blender 5.2 as a Python module, about 2 minutes. It brings `bmesh` and `mathutils` with it, so `pip install bmesh mathutils` is never needed.
3. Run: `python3 -I <skill folder>/scripts/retopo.py <model.glb> <out folder> --quads 5000 12000`. Add `--crease 30` for hard-surface. It writes one `<name>_IM<N>k.glb` per target (texture packed inside), `<name>_retopo_sheet.jpg` and `report.json`. About 40 seconds for two targets.
4. Check `report.json`: `quad_pct` 100, `open_edges` 0, `dist_max_pct` under 1.5. A fail: raise `--quads` and run again. Then look at the sheet yourself. Thin parts (fingers, antennas, eye bumps) melt at 5k. The baked texture often hides that. If it shows, go back to step 3 with a higher target.
5. Copy the GLBs and the sheet to the job folder, then reply with the Mac path. He opens them in Blender with File, Import, glTF. Claude imports them through `llllloc:tool-blender` only when he asks.

## LIMITS
- Edge flow follows the surface, not the anatomy. It is clean for rendering. A rig still needs loops placed by hand.
- Separate parts are joined into one mesh first. A model with no texture gets geometry only.
- Instant Meshes' own app (github.com/wjakob/instant-meshes) is a 2019 Intel-only build. On his Apple Silicon Mac it needs Rosetta, not tested. Its paint-the-flow brush is its one extra over the script.
- The same engine can run inside his Blender: `pynanoinstantmeshes` has a Mac arm64 build for Python 3.12 and newer. Not installed yet. Installing it is his call.

## REPLY
Lead with the result and the sheet. One line per file: faces, average and worst shape error. Say which route and target you picked and why. Flag what was not checked (rig test, his Blender).
