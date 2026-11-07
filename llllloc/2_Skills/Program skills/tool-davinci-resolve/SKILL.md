---
name: tool-davinci-resolve
description: How Claude works in his DaVinci Resolve Studio projects through the davinci-resolve MCP (samuelgursky) - media pool bins in his shared bin tree, timelines named Video_DVR_Vn with archived versions, safe tools only, no save, render or delete without his word. Use when a job touches DaVinci Resolve or Resolve (bins, media pool, timelines, a grade in Resolve). Runs when /llllloc:router picks it, or on its name.
---

# llllloc:tool-davinci-resolve (25 Oct 2026)

The mechanics of his DaVinci Resolve Studio projects through the `davinci-resolve` MCP. Grading craft lives in `llllloc:task-colorist`. Edit craft lives in `llllloc:task-motion` and `llllloc:references-edit`. Premiere stays his main edit app: Resolve is for grading and for tests he names.

## MUST HOLD ON EVERY WRITE

```
- [ ] The project and timeline read first (START), named in the reply.
- [ ] The version he saw is archived before the first change (VERSIONS).
- [ ] Only safe_* , *_checked or dry_run actions where the tool offers them.
- [ ] No delete_timelines, delete_folders, delete_track or ripple delete_clips. To take a clip out, disable it.
- [ ] No project save, render or export unless he says so in words.
```
Why: the tool marks those deletes DESTRUCTIVE or CATASTROPHIC, and a project change alters his work for every later session. A miss: stop, undo with his word, and say what happened.

## TASKS

| Task | Section |
|---|---|
| Any Resolve turn | START |
| Make, file or move a bin, clip or timeline | BINS |
| Change a timeline he has seen | VERSIONS |
| Copy a grade, set node values, take stills, render | GRADE TREE |
| The MCP is down, slow or fails | SETUP AND FAILURES |

## START

1. `project_manager` `get_current`, then `timeline` `get_current`. One read of the whole state: `project_manager` `snapshot` with only the sections needed (it walks every clip).
2. Calls can take 20 s or more (25 Oct 2026, `folder` `get_subfolders` took 20 s). Send reads in parallel. Never retry a slow call before it answers.
3. He may work in the same project. Read again right before each write.
4. Frames: the `timeline` tool counts record frames unless an action says SOURCE. A SOURCE frame is in the media's own rate. Read `source_fps`, never assume it.

## BINS

His bin tree is the same in AE, Premiere, Cavalry and Resolve: `llllloc:task-files-organize` `references/bin-tree.md`. Read it before this section. In Resolve the tree sits under `Master`.
1. Build missing bins with `media_pool` `add_subfolder` (`name`, `parent_path` like `Master/**_EXPORT`). Read with `folder` `get_subfolders` (`path`).
2. Timelines: `<Video>_DVR_V<n>` in `Master/**_EXPORT/<Video>/`, with `OLD VERSIONS` inside it. A new timeline goes there the turn it is made.
3. Compound and Fusion clips: `Master/0_SEQUENCE/NESTED`. Footage, graphics, sound: their family bin by type, mirroring the disk folders `1_` to `3_`. Generators and mattes: `5_OTHER/Solid`.
4. Import only from the project's own asset folders (`llllloc:tool-premiere-pro` 2b step 1: outside files are copied into `1_VISUAL ASSET` first). Prefer `safe_import_media` over `import_media`.
5. The MCP makes its own `Archive` bin when a destructive action auto-archives a timeline. Leave it at the root.
6. SORT CHECK before the reply: `folder` `get_subfolders` on `Master`. Only the seven bins plus `Archive`, and no timeline loose in `**_EXPORT`. A miss: move it, then read again. The reply says `Bins sorted`.

## VERSIONS

1. The first write of a change round archives the timeline he saw: duplicate it, name the copy `<Video>_DVR_V<n>`, move it to `**_EXPORT/<Video>/OLD VERSIONS/V<n>/`. The working timeline takes the next number (`V1` to `V1.1`) with `timeline` `set_name`.
2. Read the tool's action list for the duplicate and move actions before the first use. Write their exact names into this skill's NOTES when found.
3. Several destructive calls in one round: wrap them in `timeline_versioning` `begin_run` and `end_run`, so the MCP keeps one archive, not one per call. `rollback` restores an archived version.
4. Check: `timeline` `list` shows one working timeline per `<Video>`, and every older one in its `OLD VERSIONS`. If the check fails, return to step 1.

## GRADE TREE

The tree itself and the grade steps: `llllloc:task-colorist` `davinci-tree.md`. What the script can and cannot do (21.1.1, 27 Oct 2026):
1. No script adds, deletes, moves or renames a node, and none sets a CST. He builds the tree on one shot. Send him the clicks. Read it back: `GetNodeGraph()` `GetNumNodes`, `GetNodeLabel`.
2. Copy: `TimelineItem.CopyGrades([items])` from his shot. It works across timelines (targets from `GetTimelineByIndex`). It copies his shot's values too: put back every shot's own values right after. `ApplyGradeFromDRX` returned None on every route: do not use it.
3. Groups: `project.AddColorGroup`, `item.AssignToColorGroup`. Group pre and post graphs take `SetLUT` only.
4. Values: `item.SetCDL({"NodeIndex": "n", ...})`, n counts clip nodes from 1. `SetLUT(n, "MCP/<name>.cube")` after `project.RefreshLUTList()`: a new LUT can fail the first call, so read back with `GetLUT`. LUTs go to `/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/MCP/`, copies to the project's `0_DOCUMENTS & LUTS/`.
5. Stills: `SetCurrentTimecode` then `project.ExportCurrentFrameAsStill(path.tif)`, 16-bit TIFF, the full output with groups. At most 3 timelines per call (60 s limit). `GrabStill` from a script leaves Resolve blocked: never.
6. Every UI call returns None (page, timeline, playhead): a window is open in Resolve. Ask him to close it (Project Settings counts), then go on.
7. Render, on his word only: one job per timeline, `SetCurrentRenderFormatAndCodec("mp4","H264")`, `SetRenderSettings` (TargetDir, CustomName `<Project>_<Video>_DVR_V<n>`, 1920x2560 or the timeline size, no audio unless asked), `AddRenderJob`, `StartRendering`. Sharpening off unless he asks: check the Fusion sharpen tool is pass-through on every shot first. Check: ffprobe frame count equals the timeline.

## SETUP AND FAILURES

- Install facts, the two install faults and their fixes: `llllloc/2_MCP/DaVinci Resolve/NOTES_davinci-resolve-mcp_4.15.3_2026-10-25.md`. In short: Resolve Studio 21.1.1 with External scripting = Local, server 4.15.3 in `~/Library/Application Support/davinci-resolve-mcp`, config key `davinci-resolve`. Run any setup with Claude quit (Cmd+Q), or Claude writes its old config back.
- The MCP down: ask him to open Resolve and check Preferences, System, General, External scripting using = Local. Then `npx davinci-resolve-mcp@4.15.3 setup` only on his yes.
- Every call that fails, lies or is missing goes in one dated block, newest on top, in `llllloc/2_MCP/DaVinci Resolve/Notes/MCP-FAILURES-LOG.md` (make it the first time): tool, what failed, what Claude saw, the workaround, the fix to try. Read it before a Resolve job. A listed failure is never retried blind.

## REPLY

Done, then what to look at: the project, the timeline, the bin. One line each for the archived version, the disabled clips and the failure log count.
