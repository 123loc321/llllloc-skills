# FINAL DELIVERY, SECTIONS, PARTS, THE HANDLE, FILES ON DISK

Part of `llllloc:task-motion`.

## FINAL DELIVERY [R20] [R3] [R25] [R26]
Five files on every film, same length to the frame, all from 00:00:00:00: VIDEO BG (no text), VIDEO TEXT (the big text with its glow and shadow, a transparent `.mov`), VO, SFX and MUSIC (WAV, as in the approved mix). The text layer lets him change client text without a re-render [R25] [R26]. More layers only when he names them for one job. Specs, names, folders and checks: REFERENCE L. Review versions stay in the MOTION app [R32]. A mixed MP4 only on his ask.

## SECTIONS [R6] [R21]
ONE master with a keyframe at every section start, so a client note re-renders one section, plus the map `**_MOTION/_STATE/SECTIONS.md`. His count is a target ("15 to 20"). Cut on a hard cut or inside a still hold, never inside a move, a morph, a part join or a word. Section files only on his ask. Detail: REFERENCE M.

## RENDER TO PROJECT [R39] (6 Oct 2026)
He names a render and asks for its project. Find the `.motion` file with the same name and version in the job's `**_MOTION/` folder. Open it in MOTION at once, without asking (`motion_project open`). First check the film that is open now (`motion_status`). If it has unsaved changes, stop and ask him. Here this check replaces the save step in START OF EVERY MOTION TURN. The reply gives the full path. It also says when someone saved the `.motion` file after the render, because the file can then differ from the render.

## SESSIONS, PARTS, STITCH [R8]
- One film = parts, each in `**_MOTION/P<n>/` with its own clock, the VO split at a word gap. Parts share grade, grain, key, tempo and the brief.
- Review happens in MOTION [R32]. At FINAL DELIVERY each part renders a MEZZ (`CHAIN=1`, no end fade).
- STITCH (lead session, on the Mac): the MEZZ files join and encode once, with section keyframes. No part renders again. REFERENCE J.

## TWO SECONDS OF HANDLE [R40] (7 Oct 2026)
Every animation he will cut into an edit is built 2 s longer than the length it needs, so he can retime it later without a new render.
- The 2 s go at the END. The motion keeps going through them: no freeze, no fade out, no end hold.
- The first frame stays the first frame of the shot. The needed length starts at 00:00.
- On his timeline, place only the needed length (source in/out). The 2 s stay in the file as a handle.
- Name the length in the reply: "7.68 s = 5.68 s slot + 2 s handle".
CHECK: file duration = slot length + 2 s, and the last 2 s still move.

## DELIVERY [R22]
- Names and folders: `llllloc:task-files-organize`, THE FROM CLAUDE RULE. A rendered film goes to `1_VISUAL ASSET/*From Claude/<GROUP>/`, never `4_RENDERS/`.
- EVERY animation file, never in `*_CLAUDE/` (7 Oct 2026): MOTION films, build code, frames, mattes, stills, VO, test scripts and every asset they use sit in `*_PROJECT FILES/**_MOTION/<FILM>/`, grouped in `build/`, `media/`, `VO/`, `REF/`, `frames_V<n>/`. State files: `**_MOTION/_STATE/` (lane: `**_MOTION/P<n>/_STATE/`). Owner: `llllloc:task-files-organize`, THE MOTION RULE and FINAL CHECK, run before the reply.
- A video never comes to the chat as an upload [R32]: it stays on disk and reaches him as a file card plus its full path (29 Oct 2026, his ok).
- Reply: done, the film with its full path, the flags, the least-sure choice, the next step.

