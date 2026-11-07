---
name: tool-premiere-pro
description: "How Claude works on his Adobe Premiere Pro edits through the Premiere MCP: find a clip's source, place graphics, copy new footage into 1_VISUAL ASSET first, put footage under a design's cutout, time cuts to the VO, leave yellow note boxes for what it cannot do, log MCP failures. Runs when the user types its name or when /llllloc:router picks it for any job in his Premiere Pro edit. Never on its own."
---

# llllloc:tool-premiere-pro

The mechanics of driving his Premiere Pro edit through the `MCP_for_Adobe_Premiere_Pro` tools. Craft lives in `llllloc:task-motion` and `llllloc:task-design`. Subtitles and sound design are always done in Premiere (18 Oct 2026): the rules live in `llllloc:task-vo-to-srt-subtitle` ALWAYS IN PREMIERE and `llllloc:task-sound-design` ALWAYS IN PREMIERE. How the MCP behaves (frame-snapped marks, scale values, audio routing, false "no placement" errors): `llllloc/4_Lessons/Programs/Premiere Pro/README.md`, plus only the one other file in that folder that matches the job (16 Oct 2026, his words: read only the lesson that is needed). What the MCP fails at: `llllloc/2_MCP/Premiere Pro/Notes/MCP-FAILURES-LOG.md`. Read both before any placement.

## MUST HOLD ON EVERY PLACEMENT (9 Oct 2026)

Tick each box before the first `overwrite_clip` (missed on 9 Oct):

```
- [ ] Item and its bin labeled pink: `set_color_label` 11, before placing. A placed clip cannot be labeled.
- [ ] An animation file = its slot + 2 s handle (`llllloc:task-motion` R40). Item in/out = 0 to the slot.
- [ ] Scale and Position read from the clip it replaces, and copied.
- [ ] Blend mode by `set_effect_property` (11 Lighten, 18 Normal). Never `set_blend_mode`: it writes a wrong value.
- [ ] Version archived into `**_EXPORT/<Video>/OLD VERSIONS/<version>/` (section 4b), then `set_active_sequence` by id before each write.
- [ ] No `save_project`.
- [ ] No nested clip. Every layer sits on the main timeline. Nest only a moment he names (30 Oct 2026, his words: "i dont like nested clip"). Why: he edits each clip himself.
```
CHECK after placing: `get_color_label` is 11 on every new item, each clip's out minus in is its slot, and one `export_frame` looks right. A file with no handle: stop and rebuild it. Any other miss: go back to that box.

## TASKS

| Task | Section |
|---|---|
| Any Premiere turn | 0. START |
| "Find the working file of this frame" | 1. FIND A SOURCE |
| Put graphics, PNGs or renders on the timeline | 2. PLACE ON THE TIMELINE |
| New footage from outside the project | 2b. CUT FOOTAGE, step 1 |
| Cut footage under a part | 2b. CUT FOOTAGE |
| "Put the video into the placeholders" of a design frame, a cutout over footage | 2c. VIDEO IN A DESIGN'S PLACEHOLDERS |
| Time a card or a cut to the voice | 3. TIME TO THE VO |
| Any change to the timeline | 4. SAFETY |
| Anything Claude cannot do, or he must check | 5. NOTE BOXES |
| Any MCP call that fails or is missing | 6. MCP FAILURE LOG |

## 0. START

JOB: know which edit is open before anything else.
Steps:
1. `get_active_sequence`. Note the sequence name, frame size, every track and every clip with its start and end.
2. Times are in seconds. His sequences run at 25 fps, so a frame is 0.04 s. Snap every time to a whole frame.
3. He may edit the same timeline while Claude works. Read the track again right before each write.
4. A feedback round: client times belong to the version they reviewed. Map each time to the working sequence before any edit. Compare the two sequences clip by clip: a pause added in between moves every later time (7 Oct 2026).
Check: the sequence name in the reply matches the one he sees.

## 1. FIND A SOURCE

JOB: from a frame he shows, name the file that made it.
Steps:
1. Convert his timecode to seconds.
2. `get_clip_at_position` on every video track at that time. The top track with a clip wins.
3. `get_full_clip_info` on that clip: the media path.
4. A render name points to its build: `a client-TITLE-SLAM_MAIN_<date>.mp4` is a MOTION render of `a client-TITLE-SLAM_MAIN.motion`. Find the `.motion`, `.aep` or Figma frame in the project folder and read what it holds now.
Output: the working file's full path from `/Volumes/` or `/Users/`, the clip's track and time, and what to change in it to get that frame back.
Rule: a working file may hold different words now than the render. Say so when it does.

## 2. PLACE ON THE TIMELINE

JOB: put new graphics on his timeline without moving anything he cut.
Steps:
1. Archive the version first (section 4b).
2. Pick a video track that is EMPTY for the whole range. Overlay text goes on the track above the picture, so he can drop footage under it.
3. Import into a new bin named `<PART>_From Figma` (or `_From MOTION`). Files come from the project's `2_GRAPHIC ASSET/*From Figma/<GROUP>/` or `MOTION to PR/`.
3b. Pink label: Must hold. Why: he sees what Claude added. Note boxes stay Yellow (section 5).
4. Place with `overwrite_clip`, by the node id from `find_items_by_media_path` (his SORT panel imports a second copy with the same name, and a name then fails, 8 Oct 2026). Never `add_to_timeline`: it is an insert edit and pushes every later clip down.
5. A still lands 0.6 s long. Set each end with `set_clip_duration`. A video: set the item in/out first.
6. A replacement goes directly above the old clip (8 Oct 2026). Put it on the track directly above the old clip, same start and end. Clips on that track or higher inside the slot: lift only those up one track each, top clip first, onto tracks empty for the slot. Place the replacement in the freed spot, then DISABLE the old clip. Never delete it. List each lifted and each disabled clip in the reply. Why: his track layout stays, and the overlays stay on top. Check: the track count is the same as before, and every overlay in the slot is still above the replacement.
7. Read the track back with `get_active_sequence`.
Output: a list of each item with its track, start and end.
Check: the clip count on every other track is the same as before.
Rules:
- Motion > Position is stored as 0-1 of the frame. Never use `set_clip_position`: it writes pixels and throws the clip off screen. Use `set_effect_property` Motion Position `[x/1920, y/1080]` (7 Oct 2026).
- `overwrite_clip` places the whole source. A long clip covers every clip after it on that track. Set the in-point AND the out-point first, or place it on a track empty to the clip's full length (7 Oct 2026). Check: the clip count after the slot is the same as before.
- Never add a VIDEO track to his sequence. It adds at the BOTTOM and renumbers every track (7 and 8 Oct 2026). No empty track above the slot: add a yellow note box (section 5) and ask. Audio tracks for SFX are allowed: `llllloc:task-sound-design` ALWAYS IN PREMIERE (18 Oct 2026).

## 2b. CUT FOOTAGE

JOB: full-screen shots under a part, 2 or 3 per beat, from his `1_VISUAL ASSET` folder.
Steps:
1. New footage first (7 Oct 2026). Footage from outside the project (Downloads, a drive, a link) is copied into the matching `1_VISUAL ASSET/` folder first, by country, city or subject. Then import it from there. Never import from the outside path. Reason: the project must hold its own copy of every file. A file Claude cannot copy (the drive does not mount): he drags it in. The reply names each file and its folder. Check: every new clip's media path starts with the project's `1_VISUAL ASSET/`.
2. Find shots: `generate_media_contact_sheet` 8 x 8 per long film, `detect_source_scene_changes` for its cuts, ffmpeg in place for exact frames. Never use a shot with burned-in text across the picture.
3. Per shot: `set_item_in_out` on the project item, then `overwrite_clip` on the picture track, in order, each range a little long so the next shot trims it. Target a muted or new audio track for source sound.
4. A 29.97 fps source, or a source 1 or 2 frames long: the frame-time and `roll_edit` rules in the README.
5. Set Scale so the shot fills the frame (values in the README). Burned-in subtitles or titles: scale and move until they leave the frame. Check the LAST frame too: titles slide in late.
6. `export_frame` the first and last frame per shot, read them in place, look. Fix every wrong shot before the reply. The export folder must exist.
7. `clear_item_in_out` on every item touched.
Output: a table of beat, shots and sources, plus the least-sure shot.

## 2c. VIDEO IN A DESIGN'S PLACEHOLDERS (7 Oct 2026)

JOB: a Figma frame with footage placeholders plays real video in his edit, exactly inside each hole.
Input: the frame's newest version, its panel names, and the handoff that names each still's source file and time.
Steps: `llllloc/4_Lessons/Programs/Premiere Pro/how-to-put-video-in-design-placeholders.md`. In short:
1. Match each Figma still to its source frame: the source file, the time, the crop offset.
2. Figma, on a copy (one-screen yellow board on a green section): export the frame with transparent holes (white and black passes, rebuild alpha).
3. Rectangle holes with straight gaps: place each clip live under the overlay (Scale and Position from the FILL math).
4. Slanted holes: keep one big hole live. Bake every other hole into one H.264 plate with `tools/video_holes_plate.py`, plus a black stencil PNG open only on the live hole.
5. Stack, bottom to top, on tracks empty for the slot: live clip, stencil, plate (Opacity > Blend Mode 11 = Lighten), overlay, note box. Disable the old opaque graphic.
6. `export_frame` mid-slot and look before the reply.
Output: the stack with track, start and end per layer, the file paths, and which panel is live.
Rules:
- The cutout way (7 Oct 2026). The overlay is the Figma frame exported with each placeholder cut out (`llllloc:tool-figma` 15b). It sits on the track directly above its footage, same start and end. The footage keeps Crop 0 and stays free to move. Reason: he repositions the video under the cutout himself. Check: no footage clip under a cutout has a crop value.
- The MCP cannot add any effect: no Crop, no mask, no Track Matte. Never plan on one. Check: no `crop_clip` or `apply_effect` call in the job.
- Blend mode: Must hold. Check: the exported frame shows the live clip through the stencil.
- A VFR source refuses in/out marks: bake it.
- Read the slot again before every write. He edits the same timeline. Check: every layer ends on the overlay's end.
Check: one exported frame matches the Figma frame panel by panel, with no clip in the wrong hole.

## 3. TIME TO THE VO

JOB: make each card or cut land on its word.
Steps:
1. `get_full_clip_info` on the VO clip: its media path, `inPointSeconds` and `startSeconds`.
2. Cut the used range of the VO file in place with ffmpeg to 16 kHz mono WAV.
3. Word times: the Mac's `whisper` with `--model large-v3-turbo --word_timestamps True --output_format json` (on disk, 29 Oct 2026).
4. Sequence time = word time in the cut + the clip's `startSeconds`.
5. A card starts 2 to 3 frames before its first word. It ends where the next card starts. The last card ends with the VO clip.
Rule: caption tracks cannot be read through the MCP. Never treat an empty caption read as "no captions".

## 4. SAFETY

- A version archive before every timeline change (MUST HOLD, section 4b), named in the reply. Check: `get_sequence_settings` names his working sequence.
- Never delete a clip, a track, a bin or a sequence. To take a clip out, disable it.
- A nest he did not ask for: copy its layers to the main timeline (README, 30 Oct 2026). `unnest_sequence` drops keyframes and effects, so never use it.
- Never insert or ripple unless he asks for it in words. A client pause or cut that needs a ripple becomes a note box (section 5).
- Never move or trim a clip he did not name or a client note did not name.
- Never type into the Premiere window with computer control. Keys land on the timeline as shortcuts. The Search panel is not usable from Claude yet.
- Never save, export or render the sequence unless he says so. Premiere's auto-save stays his.
- A video never comes to the chat. A render stays on disk and reaches him as a file card plus its path (29 Oct 2026, his ok).

## 4b. BINS AND VERSIONS (25 Oct 2026, his words: adapt the AE `**_EXPORT` rule to Premiere)
Premiere, AE, Cavalry and DaVinci keep one bin tree: `llllloc:task-files-organize` `references/bin-tree.md`. Read it before a turn that adds, moves or versions an item. Premiere only:
1. Each deliverable has its bin `**_EXPORT/<Video>/` (`create_bin` with `parent_bin_id`), with `OLD VERSIONS` inside it. The working sequence `<Video>_PR_V<n>` sits there alone. A new sequence goes there the turn it is made, never at the root.
2. The first write of a change round archives what he saw: `create_sequence_checkpoint` (or `duplicate_sequence`), name the copy `<Video>_PR_V<n>`, move it to `OLD VERSIONS/V<n>/` with `move_item_to_bin` (`item_id` = its project node id from `list_project_items`, `target_bin` = the bin id; the sequence id fails). The working sequence takes the next number (`V1` to `V1.1`) with `rename_project_item`.
3. Older projects keep their `**_EXPORT/Checkpoint/` bins. Leave them.
4. Check: `list_project_items` on `**_EXPORT/<Video>` shows one sequence plus `OLD VERSIONS`, and the root shows only the seven bins. A miss: move it, then list again. The reply says `Bins sorted`.

## 5. NOTE BOXES (7 Oct 2026)

JOB: everything Claude cannot do, or he must check, sits on the timeline as a yellow note box at the time it belongs. Every project.
Input: the feedback list, mapped to the working sequence (section 0 step 4).
Steps:
1. One note per item, one or two short STE sentences: the client time in brackets first (`[v11 1:28]`), then what to do, then why Claude did not (needs a ripple, a VO re-record, footage, animation, client data).
2. Build each note as a 1920 x 1080 transparent PNG: a yellow box `#F9E442`, black monospace text 30 px, padding 28 x 16, square corners, centered, 60 px from the top. Wrap at 52 characters. Premiere text clips cannot be made or edited through the MCP (failure log), so the note is a PNG in his look.
3. Save to `2_GRAPHIC ASSET/*From Claude/PR-NOTES/Claude_<Client>_<Project>_PR-NOTE-<NN>_V<n>.png`. Write each PNG straight into that folder on the Mac. Up to 3 notes: one file card each. More: one card for the first note plus the folder path (`llllloc:task-sending-files`, 29 Oct 2026, his ok).
4. Import into a bin `<SEQUENCE>_Claude notes`. Set each item's label to Yellow (`set_color_label` 15) before placing, never pink (8 Oct 2026).
5. Place every note on the TOP video track, named `CLAUDE NOTES`, so no opaque graphic hides it. Span the shot or the VO line it belongs to. Notes never overlap on the track.
6. Work Claude DID that he must judge (a footage swap with burned-in text, a guessed country) also gets a box.
Output: the note count, the track, and one line per note in the reply.
Rules:
- He hides the `CLAUDE NOTES` track before an export. Say so in the reply.
- His own note clips stay where he put them. Never move or edit them.
Check: `export_frame` on one note over the busiest picture. The box reads and nothing hides it.

## 6. MCP FAILURE LOG (7 Oct 2026)

JOB: every Premiere MCP call that fails, lies, or is missing is written down, so he can fix the MCP later.
Steps:
1. During the job, keep a list: tool, what failed, what Claude saw, the workaround, the fix to try.
2. At the end of the job, add one dated block, newest on top, with the project and the sequence, to `~/Desktop/Claude/llllloc/2_MCP/Premiere Pro/Notes/MCP-FAILURES-LOG.md` (moved 16 Oct 2026). Request that folder once if it is not connected.
3. Read the log before a Premiere job. A listed failure is never retried blind: use its workaround.
Output: one line in the reply: the count of new failures and the log path.
Check: every error and every "unavailable" tool of the job has a row.

## REPLY

Done, then what to look at: the sequence, the track, the time range. One line each for the archived version, the disabled clips, the note count, the failure log, and any copy or timing choice he should check.

## WHERE THE JOB FILES GO (16 Oct 2026, FOLDERS v19)

A creative job's edit notes go in `*_CLAUDE/9_Post/EDIT.md`: cut versions, timeline names, locked or not, EDL or XML. A folder appears the first time a file goes in.
