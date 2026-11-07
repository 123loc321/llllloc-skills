---
name: tool-filmcraft
description: How Claude drives FilmCraft (the open-source Rust video editor by ArtCraft) on his Mac through filmcraft-cli - headless or bridged to the open app - with project bins in his shared bin tree, sequences named Video_FC_Vn with archived versions, the media it cannot read, motion and speed units, and export. Use when a job builds, edits, sorts, checks or renders anything in FilmCraft. Runs when /llllloc:router picks it, or on its name.
---

# llllloc:tool-filmcraft (26 Oct 2026)

The mechanics of FilmCraft 0.13.0 (alpha) on his Mac. Edit craft lives in `llllloc:task-motion` and `llllloc:references-edit`. Premiere stays his main edit app: FilmCraft is for tests and jobs he names.

## MUST HOLD ON EVERY WRITE

```
- [ ] The project and sequence read first (START), named in the reply.
- [ ] The sequence he saw is archived before the first change (VERSIONS).
- [ ] Bins sorted before the reply (BINS, SORT CHECK).
- [ ] No project.delete (Clear) on any item or bin. To take a clip out, disable it (clip.enable).
- [ ] A project he made is never saved over without his word. A project Claude built is saved as a new file in `*_PROJECT FILES/***_FILMCRAFT/`, never in `*_CLAUDE` (`llllloc:task-files-organize`).
```
Why: Clear removes media and sequences for good, and a save changes his work for every later session. A miss: stop, `edit.undo`, and say what happened.

## TASKS

| Task | Section |
|---|---|
| Any FilmCraft turn | START |
| Make, file or move a bin, clip or sequence | BINS |
| Change a sequence he has seen | VERSIONS |
| Place clips, speed, zoom, position, colour, export | COMMANDS |
| A file shows MEDIA UNREADABLE | MEDIA |

## START

1. Two ways in. Headless: `~/.local/bin/filmcraft-cli --project <p.fcproj> run <script.jsonl>` or `... mcp` (no window, `--save` writes back). Live app: start it with a control port, then add `--bridge 127.0.0.1:9876` to every call:
   `FILMCRAFT_CONTROL_TOKEN=<new hex> /Applications/FilmCraft.app/Contents/MacOS/FilmCraft --control 9876`. The CLI needs the same token in its environment. The app already open without a port: ask him to quit it first. Never kill it.
2. Read before writing: `inspect project`, then `inspect sequence`. Ids change per session. Read them again after he touches the app.
3. `run` cannot pass an id from one line to the next. A job that needs new ids drives `filmcraft-cli mcp` from a script (`command_run`, `project_inspect`).
4. Exact params: `filmcraft-cli describe <id>`. Never guess a param name: an unknown one is an error, and a wrong time key is silently ignored (`file.exportFrame` takes `time` in ticks, not `seconds`).

## BINS

His bin tree is the same in AE, Premiere, Cavalry, DaVinci and FilmCraft: `llllloc:task-files-organize` `references/bin-tree.md`. Read it before this section.
1. Run `scripts/fc_sort.py sort --project <p.fcproj>` (or `--bridge 127.0.0.1:9876`). It builds the seven bins and their sub-bins, files each sequence `<Video>_FC_V<n>` into `**_EXPORT/<Video>/` with `OLD VERSIONS`, files footage, graphics and sound by family, and prints the SORT CHECK.
2. By hand: `file.newBin` (`name`, `parent`), `project.moveToBin` (`items`, `bin`), `project.renameBin`. In `project.inspect` a bin has `id` and `children`, an item has `item` and `type`.
3. Nested sequences go to `0_SEQUENCE/NESTED`. Imported Premiere or Resolve timelines go to `0_SEQUENCE/LINKED`. A name with no `_FC_V<n>` goes to `0_SEQUENCE/*Sequence_Unsure`.
4. SORT CHECK before the reply: `ok` true, the top holds only the seven bins, nothing loose in `**_EXPORT`. A miss: file it, run the check again. The reply says `Bins sorted`.

## VERSIONS

1. The first write of a change round: `scripts/fc_sort.py archive <Video>_FC_V<n>`. It copies the sequence (`project.select`, `edit.duplicate`), names the copy `<Video>_FC_V<n>`, moves it to `**_EXPORT/<Video>/OLD VERSIONS/V<n>/`, and renames the working one to the next number (`V1` to `V1.1`).
2. Edit only the working one. Check: each `<Video>` bin holds one working sequence. If the check fails, return to step 1.

## COMMANDS (tested 26 Oct 2026)

- Time: 254,016,000,000 ticks per second. `timeline.place` takes `frame` for the record start, `sourceIn` and `duration` in ticks of SOURCE time. Set `audio:false` for picture only.
- Speed: `clip.speedDuration` (`clips`, `speed` percent, `reverse` true, `ripple` false). Place the source length first: the speed change makes the timeline length.
- Motion is Premiere's: scale 100 = one source pixel per sequence pixel, `anchor` = the source centre, `position` = where the anchor sits, in sequence pixels. To centre source point (cx, cy) at scale s: position = (W/2 + (srcW/2 - cx)·s/100, H/2 + (srcH/2 - cy)·s/100).
- Keyframes: `effects.setParam` (`clip`, `effect` "motion", `param` "scale" or "position", `value`, `keyframe` true, `time` in sequence ticks).
- Colour: `clip.interpretFootage` (`items`, `colorSpace`). Canon Log 3: `clog3-cinemagamut`. Canon Log 2: `clog2-cinemagamut`.
- Export: `file.exportMedia` (`path`, `format` "h264", `crf`, `audio`, `wait` true). One frame: `file.exportFrame` (`path`, `time`).
- Open a project in the app: `file.open` (`path`), then `sequence.open` (`item`) per sequence, `window.workspace.editing`.

## MEDIA

1. FilmCraft's H.264 decoder reads 8-bit 4:2:0 only. Canon C50 XF-AVC MXF (4:2:2 10-bit) shows MEDIA UNREADABLE, in the app too (26 Oct 2026). The fix for an offline edit: his Premiere proxies (`<camera folder>/Proxies/<clip>_Proxy.mov`), never a full-res transcode unless he asks (his words, 26 Oct 2026).
2. Proxies are smaller: multiply every scale by full width / proxy width (960 wide proxy of 4K: x4). Positions stay the same. Check the proxy width with `filmcraft-cli probe`, never assume it.
3. Check a build: `file.exportFrame` at a shot's middle frame, laid beside the same frame of the reference.

## SETUP AND FAILURES

- Installed 26 Oct 2026 on his yes: `/Applications/FilmCraft.app` (signed and notarized, Learning Machines LLC) and `~/.local/bin/filmcraft-cli`, from github.com/storytold/filmcraft releases. An update only on his word.
- Every call that fails, lies or is missing goes in one dated block, newest on top, in `llllloc/1_Connectors/1_Apps/FilmCraft/Notes/FAILURES-LOG.md` (make it the first time): command, what failed, what Claude saw, the workaround. Read it before a FilmCraft job. A listed failure is never retried blind.

## REPLY

Done, then what to look at: the project file, the sequence, the bin. One line each for the archived version and `Bins sorted`.
