---
name: task-files-organize
description: "Starts and feeds llllloc's project folders on his CREATIVE drive in his house structure, sorts downloads into asset folders and renames them. Runs on its name or when /llllloc:router picks it. Never deletes."
---

# llllloc:task-files-organize

Three jobs: start a project folder, add Claude's folder to one that exists, feed a project with downloaded files. Every job ends with a `Filed:` line listing every full path from `/Volumes/` or `/Users/` down. Runs only when he types its name or `/llllloc:router` picks it.

The template: `llllloc/7_Templates/PROJECT-TEMPLATE/`. The house structure is explained in `llllloc/4_Lessons/Programs/Premiere Pro/project-folder-and-sort.md`.

Projects live at the root of `/Volumes/CREATIVE #1`, one folder each, named `YYMMDD_Client Name_Project Name`. Spaces are fine.

## THE HOUSE FOLDERS

| Folder | What goes in it |
|---|---|
| `*_PROJECT FILES/*_CLAUDE/` | everything Claude makes EXCEPT presentations, exported assets and animation work. Every file sits in a folder (see THE CLAUDE FOLDER) |
| `*_PROJECT FILES/<APP>/` | every app project file: `*_PR`, `**_AE`, `***_DAVINCI`, `***_CAVARLY`, `***_FILMCRAFT`, a new app `***_<APP>`. Never in `*_CLAUDE` (26 Oct 2026, his words) |
| `*_PROJECT FILES/**_MOTION/` | EVERY animation file: MOTION films, code builds, frames, mattes, stills, a film's VO, test scripts and the state files, one folder per film or part (see THE MOTION RULE) |
| `0_DOCUMENTS & LUTS/` | a brief, a PDF, a guideline, a LUT |
| `0_DOCUMENTS & LUTS/Presentations/` | EVERY presentation: a client deck, a .pptx, a PDF export of a deck, a Google Slides export. Claude-made ones too |
| `1_VISUAL ASSET/` | a generated still or clip he downloaded. Every Magnific download in `From Magnific/ROUND <nn>/` (THE MAGNIFIC RULE). References in `**_Ref/`. Claude's exports in `*From Claude/`, films too. Every ComfyUI output in `From Comfy UI/<Job>/<Model>/` (llllloc:tool-comfyui, 27 Oct 2026) |
| `2_GRAPHIC ASSET/` | a logo, an alpha PNG, a vector, a font. Claude's exports in `*From Claude/`. Figma frame JPGs, on his `export`, in `*From Figma/` |
| `3_SOUND ASSET/MUSIC/`, `SFX/`, `VO/` | music, a sound effect, a voice track. Claude's exports in `*From Claude/` |
| `4_RENDERS/` | FINAL videos only: the export of the last app in the chain (THE RENDER RULE) |

Every file in a folder (28 Sep 2026). Never leave a loose file anywhere Claude writes: the `*_CLAUDE` root, any folder inside it, `**_MOTION/`, `*From Claude/`, `*From Figma/`. Every file sits in a folder named for its group, whatever its type, even when it is the only file of its kind.
- Before a write: pick the folder from the table below. No folder fits: make a new one, in UPPERCASE, named for the group (`STILLS/`, `SCRIPT/`).
- After a write: list the folder you wrote to. A loose file is a fail: group it before the reply.
- A turn that finds loose files from an earlier turn groups them in the same turn and says so in one line.
- No exception. A state file sits in a `_STATE/` folder.
- Inside a film folder, group by kind: `build/` (code, zips, scripts), `media/` (what the film reads), `VO/`, `REF/`, `frames_V<n>/`, `_STATE/`, `_DELETE/`.

The Claude folder (FOLDERS v15, 16 Oct 2026). Only notes live in `*_CLAUDE/`. Media stays outside: plates in `1_VISUAL ASSET`, renders in `4_RENDERS`, animation files in `**_MOTION/`. A folder appears the first time a file goes in: a poster job never makes `7_Motion/` or `8_3D/`.

| Place | What goes in it |
|---|---|
| on top | `STATE.md` (read first, rewritten each end, under 150 lines), `PROJECT.md` (the stable card), `DECISIONS.md` (one line per decision), `FEEDBACK-LOG.md` (his and the client's exact words, the one home), `WRAP-UP.md` (once, at delivery) |
| `0_Handoffs/` | every `HANDOFF_*.md`. The newest 3 stay; older ones go to `0_Handoffs/Old/` |
| `1_Brief/` | `BRIEF.md`, `DELIVERABLES.md`, `CHANGES.md`, `RIGHTS.md`, `INGEST-LOG.md`, `DELIVERY-LOG.md` |
| `2_Research/` | `RESEARCH.md`, `REFERENCES.md`, `References/`, `Ref study/` (frames and contact sheets) |
| `3_Art Direction/` | `DesignSystem_<Name>_V<n>.md` (every version kept; older jobs: `ART-DIRECTION.md`), `DESIGN-SYSTEM.md`, `VISUAL-PREFERENCES.md`, `Directions/`, reference stills Claude made |
| `4_Story/` | `SCRIPT-LATEST.md` (THE SCRIPT RULE), `SCRIPT_V<n>.md`, `SHOT-LIST.md`, `STORYBOARD_V<n>.md`, brief, territories, treatment |
| `5_Prompts/` | prompt decks `<ShotID>_<Name>_<Model>_V<n>.html`, `GENERATION-LOG.md` |
| `6_Design/` | `<Piece>_BUILD.md`, `PREFLIGHT.md`, `Brand/` |
| `7_Motion/` | `<Program>-BUILD.md` (AE-BUILD, CAVALRY-BUILD), `RENDER.md`, `Scripts/` |
| `8_3D/` | `SCENE-BUILD.md`, `LOOKDEV.md`, `RENDER-PASSES.md` |
| `9_Post/` | `EDIT.md`, `SOUND.md`, `COLOR.md`, `Subtitles/`, `QC.md` |
| `_DELETE/` | files to remove. He empties it himself |


A skill that names a `*_CLAUDE` file with no folder means this layout. An older project keeps files at the root: look there when the folder is missing, and group them on that turn.

The script rule (7 Oct 2026). A video project keeps one live script doc: `*_CLAUDE/4_Story/SCRIPT-LATEST.md`.
- Make it the first turn a video project has none, from the newest script file in `0_DOCUMENTS & LUTS/Script/` (newest by date in its name or by file date).
- Contents: the source files with their dates, one table row per VO line (Figma row, time, text on screen, VO word for word with footage notes cut), the client's open notes, the recorded VO read when one exists, and a change log.
- When feedback changes the script (a client comment, a screenshot of one, a new script file): edit this doc first, add a change-log line (date, source, old words, new words), then update the Figma VO header of that row the same turn (`llllloc:tool-figma` 1c step 9).
- His and the client's words stay word for word. Never a second script doc.

The presentation rule (27 Sep 2026). Every presentation goes in `<project>/0_DOCUMENTS & LUTS/Presentations/`. Make the subfolder if it is missing. Never save a presentation in `*_CLAUDE/`.

The from Claude rule (28 and 29 Sep 2026).
- Every asset Claude exports, from any skill or job, goes in the folder `*From Claude` inside its type folder: `1_VISUAL ASSET/*From Claude/`, `2_GRAPHIC ASSET/*From Claude/`, `3_SOUND ASSET/*From Claude/`. Make it the first time a file needs it.
- Inside it, one subfolder per group, named for what it holds, in UPPERCASE: `PART-1/` for every Part 1 version, `PART-2/` and on, `DEMO/`, `ORB/` for one asset family, `FULL_V1/` or `FINAL_V1/` for the stems of one film version. Every file sits in a group subfolder.
- Every film Claude renders is a visual asset: `1_VISUAL ASSET/*From Claude/PART-<n>/`, `FULL/`, `SOUND-REVIEW/`, `FINAL_V<n>/`, `FINAL_V<n>_SECTIONS/`.

The Magnific rule (19 Oct 2026, his words). Every file downloaded from Magnific, in any job, by Claude or by him, goes in `1_VISUAL ASSET/From Magnific/ROUND <nn>/`. One folder per round: all the renders of one run, `ROUND 01` first, the next free number for the next run. The round's contact sheet sits in the same folder. Never in `**_Ref/`, `*From Claude/` or `*_CLAUDE/`.

The render rule (18 Oct 2026, his words), the same in After Effects, Cavalry and Premiere.
- `4_RENDERS/`: only the final video, from the LAST app in the chain. Name `YYMMDD_<Client>_<Project>_<Video>_V<n>.<ext>` (his house name, `V<n>` from its sequence). An older final goes to `4_RENDERS/OLD VERSIONS/` first.
- A render to import into another app: `1_VISUAL ASSET/Transfer render/From AE/` (`From Cavalry/`, `From PR/`), named `<Project>_<comp or sequence>.<ext>`, older ones in its `OLD VERSIONS/`.
- Never delete, trash or move out an `OLD VERSIONS/` render, in any cleanup, even one he approved in general (5 Nov 2026).
- Comps, sequences and timelines: `<Video>_<APP>_V<n>` (`Act 1_AE_V1.4`, `Act 1_CAV_V3`, `Act 1_PR_V2`, `Act 1_DVR_V1`), one count per app, `_V<n>` last because SORT learns that shape.

The bin tree (25 Oct 2026, his words). AE, Premiere, Cavalry, DaVinci and FilmCraft keep the same bin tree and file items the same way: `**_EXPORT/<Video>/` with its `OLD VERSIONS/<version>/`, then `0_SEQUENCE` to `5_OTHER`. Read `references/bin-tree.md` before any turn that adds, moves or versions an item in an app's bin panel.
- Name: `Claude_<Client>_<Project>_<KIND>_V<n>.<ext>`. `<Client>_<Project>` is the project folder name without its `YYMMDD_` date. No date or time. `<KIND>` says what it is: `PART-2`, `FULL`, `SOUND-REVIEW`, `FINAL`, `SEC-01`, `FINAL_V1_VO`, `FINAL_V1_BG` (the film with no text), `FINAL_V1_TEXT` (the text only, a transparent `.mov`, `llllloc:task-motion` FINAL DELIVERY). A new export takes the next version number, never an old name.
- Never a loose folder at the project root.

The MOTION rule (2 Oct 2026, widened 7 Oct 2026).
- Every animation file lives in `<project>/*_PROJECT FILES/**_MOTION/`, in the right project, never in `*_CLAUDE/`: every `.motion` version, code builds and render scripts (`build/`), frames, mattes, stills, its VO and word times (`VO/`), the Figma and AE test files, and `media/` with every clip and picture the film reads. One folder per film or part: `**_MOTION/<FILM>/` or `**_MOTION/P<n>/`. Make `**_MOTION/` the first time a film needs it.
- State files: the lead's `MOTION-STATE.md` and `SECTIONS.md` in `**_MOTION/_STATE/` (an older `LOOK-LOCK.md` there counts until the DesignSystem file replaces it, 17 Oct 2026). A part or scene: `**_MOTION/<FILM>/_STATE/` (a lane: `**_MOTION/P<n>/_STATE/STATE-P<n>.md`).
- `<FILM>` is the scene or piece in UPPERCASE: `SCENE-2B_SEVEN-WORLDS/`, `TITLE-SLAM/`.
- The `#` link that MOTION needs on `CREATIVE #1`, and how to move an old film: read `references/motion-link.md`.
- A loose test film with no project (`Untitled.motion`) stays in `~/Movies/MOTION/`.

The from Figma rule (29 Sep 2026): only when he types `export`, the newest Figma version goes out as JPG to `2_GRAPHIC ASSET/*From Figma/`. Folders, names and steps: read `references/figma-export.md`.

Moving any file (7 Oct 2026). A file can be read by path from somewhere else. Before a move, find every reader: `*_PR/*.prproj` (gunzip, then read `ActualMediaFilePath`), `**_AE/*.aep` (`strings`), every `.motion` film (its `src` paths), every build script (relative paths such as `here.parent + "/..."`), and the state docs. Fix each path the same turn, or leave the file where it is read. A moved file that Premiere uses goes offline: name each one in the reply, with the folder to relink it from.

When the drive does not list, a shell move is refused, or an older project has an `ANIMATION/` folder in `*_CLAUDE/`: read `references/legacy-and-drive.md`.

SORT, his Premiere panel, mirrors folders 1 to 4 into Premiere bins on the next sync. It never mirrors `*_PROJECT FILES`, which is why Claude's folder lives there. Folders an app makes for itself (`Adobe Premiere Pro Auto-Save`) are not part of the template. Never create them.

Final check (7 Oct 2026). Every filing mistake he corrected is a line here. Run it before any reply that wrote, moved or made a file, on every folder touched (`ls -R`). One fail: fix it before the reply. Add a line each time he corrects a new one.
1. No loose file outside a group folder (a `.motion` film in its film folder is fine).
2. No animation file or app project file in `*_CLAUDE/`.
3. The `*_CLAUDE/` root holds only the files on top and the folders in THE CLAUDE FOLDER table. No empty folder.
4. Every `HANDOFF_*.md` sits in `0_Handoffs/`, the newest 3 on top, older in `Old/`.
5. No duplicate left after a move: the source is gone or in `_DELETE/`.
6. Every path that reads a moved file still finds it (MOVING ANY FILE).
7. `4_RENDERS/` holds only final videos (THE RENDER RULE). A render made for another app sits in `1_VISUAL ASSET/Transfer render/From <App>/`.
8. A video project has `4_Story/SCRIPT-LATEST.md` (THE SCRIPT RULE).

## MODE 1 — NEW: start a project folder

1. Run `date`. The folder name takes today's date as `YYMMDD`.
2. Build `YYMMDD_Client Name_Project Name`, English, ASCII, in his words. Show it in one line before you make it.
3. `ls "/Volumes/CREATIVE #1"`, or the path he gave. Nothing lists: the drive is not plugged in. Stop and tell him to plug it in (29 Oct 2026).
4. Copy the template tree to the root under the new name: the house folders, and in `*_CLAUDE/` only the files on top. A numbered folder is copied from the template the first time a file goes in. Never invent a different layout. Move `_TEMPLATE-RULES.md` to `_DELETE/`.
5. Fill `*_CLAUDE/PROJECT.md`: client, kind, kinds of job, start date, status ACTIVE, the full path. The brief from what he said goes in `1_Brief/BRIEF.md`. Leave DECISIONS and STATE as templates. Do not invent a brief.
6. Add a PATHS row for the project to the map `llllloc/3_Project maps/Project map_Creatives.md` the same turn, and say so in one line.
7. Documents he attached go in `0_DOCUMENTS & LUTS/`, presentations in `0_DOCUMENTS & LUTS/Presentations/`, references in `1_VISUAL ASSET/**_Ref/`. Keep their names.
8. Reply with the tree and a `Filed:` line.

## MODE 2 — ADD: the project exists, Claude's folder does not

1. `ls` the project folder, full path from its map row.
2. Copy the template's `*_PROJECT FILES/*_CLAUDE/` files on top into the project's `*_PROJECT FILES/*_CLAUDE/`. Touch nothing else.
3. Fill `PROJECT.md` and add the map row, as in NEW steps 5 and 6.
4. Reply with a `Filed:` line.

## MODE 3 — INGEST: sort downloaded files into the project

1. `ls` `~/Downloads` and the project folder.
2. Take the files he named. If he named none, take the files newer than the last line in `*_CLAUDE/1_Brief/INGEST-LOG.md`, or newer than the project start when the log is empty. Never touch any other file in Downloads.
3. Route each file by the table above. When the type is not clear, ask once, as a two-button choice. Never drop a file you cannot place.
4. Match each generated image or clip to its prompt by the prompt words in the file name, against the decks in `*_CLAUDE/5_Prompts/`. A Midjourney file is `<username>_<prompt words>_<job id>.png`. No match: keep it and mark it UNMATCHED.
5. New name for a matched file: `<DECK>-<NN>_<Subject>-<Action>_<MODEL>_v<N>_t<TT>.<ext>`, where `<TT>` is the take number from the log, starting at 01. An UNMATCHED file keeps its name with `YYMMDD_UNMATCHED_` in front. Other files keep their names.
6. Show the move map before you copy: one line per file, old name, new name, destination. Wait only when a match or a destination is a guess.
7. COPY each file, then read the copy back. A size that differs means the copy failed: say so and stop.
8. Append one line per file to `*_CLAUDE/1_Brief/INGEST-LOG.md`: `| date | new name | original name | went to | prompt or note |`. The original name carries the generator's job id, which recovers the seed and the exact prompt later.
9. Move the originals into `~/Downloads/_DELETE/`. Make it if needed. He empties `_DELETE` folders himself.
10. Add one line to `STATE.md`. Reply with the count per folder, the UNMATCHED files, and a `Filed:` line.

## RULES FOR EVERY MODE

- Never delete a file, anywhere. A file to remove goes into a `_DELETE` folder beside it.
- Never edit or move anything outside `*_CLAUDE/`, `**_MOTION/`, the house folders above, `0_DOCUMENTS & LUTS/Presentations/`, and the named Downloads files.
- Never rename a file inside `*_CLAUDE/5_Prompts/`. The deck name is the prompt's name.
- Never overwrite a file that exists. A second copy of the same take gets the next take number.
- Never a loose file (EVERY FILE IN A FOLDER). Check: FINAL CHECK passes on every folder touched this turn.
- A presentation, from any skill or job, is saved in `<project>/0_DOCUMENTS & LUTS/Presentations/`. Resolve the path with `ls -d "<full path>"/0_DOCUMENTS*` first (the map row's path, 29 Oct 2026). Empty listing: stop and ask.
- A Claude export is saved in `*From Claude/<GROUP>/`. Resolve the type folder with `ls -d "<full path>"/1_*` (or `2_*`, `3_*`) first. Empty listing: stop and ask.
- A Figma frame JPG is saved in `2_GRAPHIC ASSET/*From Figma/<GROUP>/`. Resolve it with `ls -d "<full path>"/2_*` first. Empty listing: stop and ask.
- Every file you create, a shell-written one too, is written in its final Mac folder, then sent as a file card plus its full Mac path: `llllloc:task-sending-files` (10 Oct 2026). Check: one card per file made this turn.