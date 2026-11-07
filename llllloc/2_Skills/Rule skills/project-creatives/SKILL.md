---
name: project-creatives
description: "The task rules for every creative job in llllloc: how a project opens, the project folder shape, lanes, how each task runs. Loaded by /llllloc:router once per thread when a message names a project, a client, a film, a design, a prompt or slides."
---

# llllloc:project-creatives (15 Oct 2026; project folder FOLDERS v15, 16 Oct 2026)

Loads once per thread. Compacting: core rule 13.

## 1. THE START OF A JOB
1. Read only the project's row in `llllloc/3_Project maps/Project map_Creatives.md`. Take the folder path and every link from that row. Never build a Figma or Magnific URL from an ID.
2. Find the Claude folder with `ls -d "<full path from the row>"/*/*_CLAUDE`. No access step: the session runs on his Mac (29 Oct 2026). A `/Volumes/` path that does not list: the drive is not plugged in. Stop and tell him to plug it in. Never ask him to attach a folder.
3. Read `*_CLAUDE/STATE.md` first, then the newest `HANDOFF_*.md` in `*_CLAUDE/0_Handoffs/`. No STATE yet: read `*_CLAUDE/PROJECT.md`. Then only the numbered folder the job needs.
4. A place word (the deck, the Figma file, the board, the space) takes its link from the map row.
5. Before a "waits for" item is carried on, check the newest source: the deck, the board, the feedback (31 Oct 2026).

## 2. THE PROJECT FOLDER
`*_CLAUDE/` holds STATE.md, PROJECT.md, DECISIONS.md, FEEDBACK-LOG.md (his and the client's exact words, one home) and WRAP-UP.md (at delivery) on top, then `0_Handoffs/` (newest 3, older in `Old/`), `1_Brief/`, `2_Research/` (facts, RESEARCH.md), `2_References/` (Claude's reference notes: the sheets, `_batches/`, Claude screenshots, frame indexes, all kept for good: `llllloc:references` GLOBAL RULES; two folders, his words, 17 Oct 2026), `3_Art Direction/`, `4_Story/`, `5_Prompts/` (decks and GENERATION-LOG.md), `6_Design/`, `7_Motion/`, `8_3D/`, `9_Post/`, `_DELETE/`. A folder appears the first time a file goes in. Only notes live in `*_CLAUDE`. Template: `llllloc/7_Templates/PROJECT-TEMPLATE/`. Animation files live in `*_PROJECT FILES/**_MOTION/<FILM>/`, state files in `**_MOTION/_STATE/`. Every other filing rule, and the FINAL CHECK after a reply that wrote, moved or made a file: `llllloc:task-files-organize`.

Research for THIS project is filed in `*_CLAUDE/2_Research/RESEARCH.md`, one dated line per finding. Universal findings go to `llllloc/5_Research cache/`. Read the project folder first, then the cache, then search.

## 3. HOW EACH TASK RUNS (one-minute rule removed 16 Oct 2026)
- A prompt, a design, a motion job: the research pass first, every time, never skipped, cache first. A revision searches only its new question.
- A job inside a program (Premiere, Figma, MOTION, Cavalry, Magnific, After Effects, Illustrator): list `llllloc/4_Lessons/Programs/<Program>/` first and read the matching how-to. It holds what the tool does on his Mac.
- A file job: the calls that touch the file, plus the delivery calls (`llllloc:task-sending-files`). Nothing else.
- No check-back agent, except `llllloc:task-judge` when he types or names it.
- Any job that makes something gets the time and research it needs. Speed never cuts quality.

## 4. PARALLEL CHATS ON ONE PROJECT (28 Sep 2026)
- A message that names a project and a part ("continue a client, render part 2") makes this chat that part's LANE. Say it in one line: `Lane P2 of <project>.` Then run section 1 and read `**_MOTION/P<n>/_STATE/STATE-P<n>.md`. No stub there: create it from the P1 lane's shape.
- Part 1, or no part named, makes this chat the LEAD. Only the lead writes shared files: `MOTION-STATE.md`, the `DesignSystem_<Name>_V<N>.md` (older project: `LOOK-LOCK.md`), the kit, skills, the core rule.
- A lane writes only in `**_MOTION/P<n>/` and its own renders. Wanted shared changes go to PROPOSALS in its `STATE-P<n>.md`. The lead merges them.
- Figma: a lane edits only its own part's section, on duplicates.

## 5. WRITES THAT NEED NO ASKING
The map in `llllloc/3_Project maps/` gets a new path or link row the moment one appears (core rule 16). The film's state file is updated the turn a render ships. A research line is appended by shell (`>>`) the turn a search ran. Everything else on disk waits for his word or for `end`.

## 6. PAID AND PROGRAM RULES
Image prompts run at once on the project's Magnific space, a video prompt ships in the chat: `llllloc:tool-magnific` RULE 1. A video renders only on his word, to disk, never to the chat: `llllloc:task-motion`. Export names and folders: `llllloc:task-files-organize`, never `4_RENDERS/` except an After Effects render. The Figma link file and JPGs only on his `export`: `llllloc:tool-figma`.