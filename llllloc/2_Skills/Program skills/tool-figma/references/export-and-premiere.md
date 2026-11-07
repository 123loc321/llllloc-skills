# EXPORT, AND A FRAME TO PREMIERE

Part of `llllloc:tool-figma`. The section numbers are the ones every rule in the skill uses, so "section 13, 15 or 15b" in any rule points here.

## 13. EXPORT ONLY WHEN HE TYPES `export` (29 Sep 2026)

- Never export on your own. Only his word `export` starts it.
- Export ONLY the newest version: on each part, the newest section on the working page. Never an older version, a red section, a `LAYOUT OPTIONS` section or the Archive page. When he names a part or a frame, export only that.
- Folder and name rules: `llllloc:task-files-organize`, THE FROM FIGMA RULE.
- A VIDEO export is a different job: section 15.

1. Resolve the folder: `ls -d "<full path from the map row>"/2_*`. A `/Volumes/` drive not mounted, or an empty listing: stop and tell him. Make `*From Figma/<GROUP>/` when it is missing.
2. Call `download_assets` on each frame node with `defaultFormat: "jpg"` and `defaultScale: 2`. It returns a temporary URL for the export. Download it at once with `curl` in Bash, into that folder under the step 3 name.
3. Name it `Figma_<Client>_<Project>_<FRAME>_V<n>.jpg`. Never overwrite a file that exists.
4. Deliver it by `llllloc:task-sending-files`: a file card plus the full Mac path (29 Oct 2026).
5. Open one JPG and check it against the Figma screenshot. A blank or cropped JPG is a fail: say so.
6. Reply with the count and the full folder path.

The 2x scale is Claude's default for a sharp file. He can name another scale.

## 15. A VIDEO FRAME TO PREMIERE (6 Oct 2026)

JOB: a frame whose fills are videos becomes one MP4 on his Premiere timeline, with no step left for him.

ONLY when he asks for the frame as a video. A frame with a video placeholder that goes to Premiere is a CUTOUT by default: section 15b.

INPUT: he put the clips into the frame (section 10) and says "export it as a video and put it on my timeline", or asks for the video. That sentence is the word to export. No more asking.

STEPS:

1. THE FRAME must sit directly on a page or in a section, never inside another frame. Load `figma-use-motion` with `figma-use`. Motion off for him: the call throws `is not a supported API`. Say so and stop.
2. SET THE LENGTH FIRST. The default is 2 s, and a 2 s file on an 11 s slot is a miss. Length = the slot (the clip it replaces, else the VO line) + 2 s handle that keeps moving (`llllloc:task-motion` R40). Read it with `f.timelines[0].duration`. Set it with `f.setTimelineDuration(f.timelines[0].id, <seconds>)`. Never shorten a timeline. Return the node id.
3. EXPORT: `export_video` with the frame id, `quality: "high"`, `fps: 25` (his sequences run at 25 fps), no `constraint`. A `jobId` comes back. Wait 12 s with `sleep 12`, then call again with the same `fileKey` and `jobId`. The link lives about one hour.
4. DOWNLOAD with `curl` in Bash to this session's scratchpad. Check with `ffprobe`: 1920 x 1080, 25 fps, length within 0.04 s of slot + 2 s, no audio stream. Pull four frames across the length with `ffmpeg` and compare them. The video areas must change. If they do not, the clips are not playing: say so, do not place the file.
5. NAME `Figma_<Client>_<Project>_<FRAME>-Video_V<n>.mp4`. Never overwrite a file that exists. Folder: `2_GRAPHIC ASSET/*From Figma/<GROUP>/`.
6. PUT IT ON HIS DISK (29 Oct 2026): `ls` the step 5 folder (drive not mounted: stop and tell him), copy the file in, then deliver it by `llllloc:task-sending-files`.
7. PLACE IT in Premiere with `llllloc:tool-premiere-pro` sections 0, 2 and 4: `get_active_sequence`, `create_sequence_checkpoint`, a bin `<PART>_From Figma`, `import_media`, then `overwrite_clip` on a video track that is empty for the whole range, at the old graphic's start time. A file with no audio stream needs no audio track. Never leave the default audio track: pass nothing and confirm the file has no audio first. Item in/out = 0 to the slot, and every box in `llllloc:tool-premiere-pro` MUST HOLD. Read the track back.
8. THE OLD GRAPHIC: `llllloc:tool-premiere-pro` section 2 step 6 (place above it, disable it, never delete it).
9. REPLY: track, start, end, checkpoint name, file path. One line each.

RULES:

- A video comes to the chat only as the one card step 6 needs. Never play it, never preview it there.
- The export is not a paid generation, so it needs no asking.
- A second export after a length fix saves as the next V number. The first file stays on disk.

CHECK: ffprobe length equals the slot + 2 s, four frames differ, `get_clip_at_position` returns the new clip with the exact start and end.

## 15b. A VIDEO PLACEHOLDER FRAME TO PREMIERE: THE CUTOUT (7 Oct 2026)

JOB: a frame with a video placeholder goes to Premiere as a PNG with the placeholder cut out. The footage plays under it, and he moves the video himself.

INPUT: he asks to put the frame, or its footage, on his timeline. That request is the word to export (section 13).

STEPS:

1. On a copy (section 1), find every placeholder: the panel, image or shape where the footage shows. Hide its fill on the copy, so only the background shows through it.
2. Export the frame twice at 1920 x 1080: once on white, once on black. Use a temporary sheet, then remove it.
3. Rebuild the alpha: `alpha = 1 - mean(white - black) / 255`, color = black / alpha. The placeholder becomes fully transparent. Every scrim, gradient and shadow on top of it stays, half transparent.
4. NAME `Figma_<Client>_<Project>_<FRAME>_CUTOUT_V<n>.png`. Folder: `2_GRAPHIC ASSET/*From Figma/<GROUP>/`. Write it there directly.
5. PLACE it with `llllloc:tool-premiere-pro` section 2c: the cutout on the track above its footage, same start and end.

RULES:

- Never bake the footage into the PNG. Never crop the footage to fit the hole. Reason: he repositions the video under the cutout himself. Check: the PNG is transparent in the hole, and every footage clip under it has Crop 0.
- The old opaque frame stays on the timeline, disabled.

CHECK: open the PNG on a checker background. The hole is clear, and the design around it is solid.