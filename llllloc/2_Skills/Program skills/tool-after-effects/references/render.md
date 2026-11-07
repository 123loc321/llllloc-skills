# Render: always this way

Moved from SKILL.md on 14 Oct 2026, unchanged. Read in full on his render word.

## RENDER: ALWAYS THIS WAY (12 Oct 2026, his word)
Only on his word. The After Effects render queue, never Media Encoder. Steps, with `run_jsx_json`:
1. Each main comp: turn off every rough-cut layer (`act<n>`, any client cut), set Full resolution, set the work area to the whole comp.
2. Save the project (SAVING).
3. One queue item per main comp: Render Settings `Best Settings`, time span the whole comp, output template `H.264 - Match Render Settings - 10 Mbps` (H.264 MP4, VBR 1 pass, 10 Mbps). Apply the template first, then set `om.file`.
4. File: `<project>/1_VISUAL ASSET/Transfer render/From AE/<project name without date>_<main comp>.mp4`, for example `a client_Act 1_AE_V1.4.mp4`. A file with that name exists: move it to `OLD VERSIONS/` in the same folder first. After Effects is the last app (no Premiere after it): `4_RENDERS/` with the house name instead (`llllloc:task-files-organize` THE RENDER RULE, 18 Oct 2026).
5. Template missing: a script cannot set the H.264 bitrate. By computer use, open an item's Output Module, Format Options, Target Bitrate 10, OK, then the output module menu, Make Template, under that exact name. Apply it to every item.
6. Save again, then start the render through the connector: `app.project.renderQueue.render()` in `run_jsx_json`, `timeoutMs` long enough for the queue (18 Oct 2026, his words: "never make this kind of mistake again"). Checked 18 Oct: an 18 s H.264 comp rendered in 10 s and the bridge stayed alive. Only if that call fails, say so and ask him to click Render. Never start a second renderer (`aerender`, Media Encoder) on the same queue or output path: on 18 Oct it broke the file. While it renders, After Effects is busy: say so with the time estimate.
7. When it ends: ffprobe each file (frames, fps, size, bitrate). No audio check after the render.
8. He reports bad audio: never render again. Old file to `OLD VERSIONS/` in its folder, then ffmpeg: `-c:v copy`, VO at the layer start (`adelay`), `pan=stereo|c0=c0|c1=c0`, AAC 192k, comp length. Reply with every full path.

## PATCH: A REVIEW ROUND (1 Nov 2026, his words: "just render the part i ask to correct, then patch that into the previous render seamlessly")
A full render of 7 videos took 40 minutes. A patch of 29 s took 2. Final delivery stays one full render, because a patch is one more encode.
1. Ranges. Read the changed key times from the session's report or the comp. Add 0.2 to 0.4 s each side. Use exact frames.
2. Queue one item per range: `Best Settings`, `timeSpanStart` = frame / 25, output template `Lossless`, into `From AE/Patches/<comp>_patch <n>.mov`. Save, then render as in step 6.
3. Wait for each file's frame count. `ffprobe` can print the count twice: take the first number.
4. Splice with ffmpeg, frame exact: `trim=start_frame:end_frame` on the old render, the patch through `scale=out_color_matrix=bt709:out_range=tv,format=yuv420p`, then `concat`. Encode `libx264 -crf 15 -colorspace bt709`, `-map 0:a -c:a copy`.
5. Name the result as the new version, for example `<project>_Act 1_AE_V1.2.mp4`. The old render stays.
6. Check: the first and last frame of each patch against the same frames of the old render (45 dB or more was clean), same frame count, same audio md5. A low seam: widen the range, go back to step 2.
