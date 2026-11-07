---
name: task-sending-files
description: "The rules for sending a file to him in llllloc: the file straight to its Mac folder, the file card with its Mac path, export names. Loaded by /llllloc:router the moment any job ships a file to his Mac. Not for a reply with no file."
---

# llllloc:task-sending-files (15 Oct 2026, Mac first 29 Oct 2026, scheduled tasks 18 Oct 2026)

The Mac file is the only copy. It is written straight to its final folder (29 Oct 2026). Drafts and backups stay in Claude's own scratch space.

## FILE CARD AND MAC PATH (29 Oct 2026, his words)
Every file or item he gets reaches him as a file card in the chat (`SendUserFile`), plus its full Mac path in the reply. Why: a click on the card opens the right panel, which has a Show in Finder button. Content that shows in the chat itself, a short text or an inline picture, may go straight in the chat. A `.skill` also goes into the Desktop round folder for upload: its card has no Save button (tested 29 Oct 2026).

## THE THREE STEPS, EVERY FILE
1. Write the file straight into the right numbered folder on the Mac, full path from `/Users/` or `/Volumes/` down, from the map row or an `ls`. A drive under `/Volumes/` gets an `ls` first: not mounted, stop and tell him. File names have no dashes except in a date: `Project map_Code.md`, `Research_Rules in instructions_2026-10-15.md`. A `.command` gets `chmod +x`, mode read back.
2. Send that Mac file as a file card with `SendUserFile`. A shell-written file too. A file he cannot open in one click is not delivered.
3. Reply: open with the Mac folder path in a code block, ready to copy (16 Oct 2026). The card's Show in Finder button replaces the old three Finder steps (29 Oct 2026, his ok). Then the work plus one line, then the closing lines of core rule 9. One more line only for a fact that changes how he uses the work.

## SCHEDULED TASKS: ONE DESKTOP FOLDER (18 Oct 2026, his words)
Everything a scheduled task delivers goes into one Desktop folder: `~/Desktop/Scheduled tasks_<task name>/<YYYY-MM-DD>/`, one date folder per run. Reports, installers and any other file he asked for all go there and nowhere else. A skill change is never a file: it is committed and pushed (`llllloc:task-skill-creator` rule 2). A new tool or MCP version always ships its installer in the same date folder, never only an offer. The only file a run may also touch outside it is a library copy in `llllloc/2_Skills/` (Old/ backup first). Every new scheduled task's prompt carries this rule.

## WHAT COUNTS AS A FILE
A handoff, a report, a prompt file, a deck, a map, a rule file, a render path, a zip. A skill ships through rule 2 of `llllloc:task-skill-creator`: commit and push, the `llllloc` plugin syncs it (6 Nov 2026). No file card for a skill. The core rule ships as its file card. `CLAUDE.md` loads the Mac file in every session, so the change is live at once.

## NAMES AND PLACES
- Export names and folders: `llllloc:task-files-organize`. Never `4_RENDERS/`, except an After Effects render.
- A render stays on disk and reaches him as a file card plus its path (29 Oct 2026, his ok).
- A sheet of two or more images (a compare, a contact sheet, a before and after) shows each image's name above it: the node, file or version name. Why: he cannot tell the pictures apart without it (27 Oct 2026, his words: label the name in each image, always).
- Deliver the number of prompts he asked for. Offer extras in one line. Editing his files needs no asking.

## WRITING TO DISK IS GATED
Write to a rule file, a log or a handoff only when his message says to. `end` is the only trigger for a handoff. What changed mid-thread lives in the reply only. Three exceptions, each reported in one line: a map row (same turn), a research cache line (shell append), a film state file the turn a render ships.
