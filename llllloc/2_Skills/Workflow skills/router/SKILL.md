---
name: router
description: "Skill router for llllloc. Use when any message arrives in the llllloc Project or in a Code tab session in his brain folder (Desktop/Claude), tagged /llllloc:router or not."
---

# llllloc:router

## STEP 1 — THE TASK KIND AND ITS PROJECT SKILL
A project skill loads once per thread. A second kind adds its own.

| The message | Kind | Project skill |
|---|---|---|
| Names a project, a client, a film, a design, a prompt, slides | Creative job | `llllloc:project-creatives` |
| Names a plugin, panel, app, extension, website, script, or code Claude writes | Code job | `llllloc:project-code` + `llllloc:ponytail` + `llllloc:using-agent-skills`, always (19 Oct 2026) |
| A rule, a skill, the setup, this project | Workflow ask | `llllloc:project-workflow` |
| Any kind, when a file ships to his Mac | Delivery | `llllloc:task-sending-files` |
| A question, a chat | Chat | none |

## STEP 2 — THE JOB SKILLS
| The request | Load |
|---|---|
| Art direction: brief, concepts, territories, treatment, brand | `llllloc:task-art-direction` |
| Image: a design system, or a design or motion job with a picked direction and none yet (exploring skips it, 22 Oct 2026) | `llllloc:task-design-system` first |
| Image: layout, slides, poster, key visual, board, UI | `llllloc:task-design` |
| Image: a prompt for any AI model, or an image render on Magnific | `llllloc:task-prompt` + `llllloc:task-research` |
| Video: motion, a film note, MOTION film sound | `llllloc:task-motion` |
| Video: Premiere Pro edit | `llllloc:tool-premiere-pro` |
| Video: DaVinci Resolve (media pool, timelines, a grade inside Resolve with `llllloc:task-colorist`) (25 Oct 2026) | `llllloc:tool-davinci-resolve` |
| Video: FilmCraft (project bins, sequences, an edit or render inside FilmCraft) (26 Oct 2026) | `llllloc:tool-filmcraft` |
| Video: grade, color correct, shot match, LUT, a look, his COLOR app (21 Oct 2026) | `llllloc:task-colorist` |
| Video: subtitles, SRT, transcripts | `llllloc:task-vo-to-srt-subtitle` |
| Video: a page or wall where many clips play at once (cut breakdown, contact sheet, ours vs client), opened in Ego Lite (26 Oct 2026) | `llllloc:task-render-preview` + `llllloc:impeccable` |
| Sound: sound design, SFX, VO, music mix | `llllloc:task-sound-design`, `llllloc:tool-soundly`, `llllloc:tool-premiere-pro` |
| Program: MOTION app, Cavalry, After Effects | its tool skill, `llllloc:task-motion` |
| Program: Illustrator, FigJam | its tool skill, `llllloc:task-design` |
| Program: Magnific (with `llllloc:task-prompt` + `llllloc:task-research`), Figma (`export` adds `llllloc:task-files-organize`, a design build adds `llllloc:task-design`) | its tool skill. Figma's own `figma-use` and `figma-generate-design` load with it, never instead (22 Oct 2026) |
| Program: Plasticity, 3D CAD modeling (22 Oct 2026) | `llllloc:tool-plasticity` |
| Program: Capture One: read, edit, grade, crop or rate photos in an open Catalog or Session (3 Nov 2026) | `llllloc:tool-capture-one`, `c1:edit`. First use or a c1 failure: `c1:setup`. On his ask: `c1:learn-style`, `c1:crop-policy` |
| Program: ComfyUI or Comfy Cloud: build, check, run or show a workflow, a partner node render (27 Oct 2026) | `llllloc:tool-comfyui`, plus `llllloc:task-prompt` + `llllloc:task-research` when it writes the prompt |
| Program: rclone or Rclone UI: download a Google Drive link, finish a slow Drive download, upload or mirror a folder to Drive, add a Google account (28 Oct 2026) | `llllloc:tool-rclone` |
| Any job: look inside an app with REA, reverse engineer, decompile (24 Oct 2026) | `llllloc:task-rea` |
| Any job: a dropped picture, clip, sound, link | `llllloc:references` + `llllloc:references-<medium>` for every medium it touches (21 Oct 2026): design (UI, layout), photo, motion, sound, art, cinematography (camera, light), color-grading, edit (cut, pacing), people, space (places, sets), code |
| Any job: learn from a video or a link (learn from, study, lesson, teach me, how they did it) or apply what was learned, for a project or not (26 Oct 2026) | `llllloc:task-learn-video`, plus the tool skill of his program on an apply |
| Deep research: a report across many sources, or "deep research" (22 Oct 2026) | `deep-research` + `llllloc:task-research` (its REACH through Ego Lite, COMMUNITY and one Perplexity Deep Research, 27 Oct 2026) |
| Any job: make, move, sort, rename files | `llllloc:task-files-organize` |
| Mac: full disk, clean up, free space, caches, old app versions, leftovers (5 Nov 2026) | `llllloc:task-clean-my-mac` + `llllloc:task-research` |
| A code product | the skills in its map row |
| Put a site, web game or app online, or update one online (Cloudflare, his method since 20 Oct 2026) | `llllloc:task-web-publish` |
| Audit, make, fix or update a skill | `llllloc:task-skill-creator` |
| "check my workflow", "update overall rule", a rule across files | `llllloc:task-workflow-best-practices` |
| "update/review/improve my workflow", a tip about Claude, a new model or app | `llllloc:task-workflow-update` |

A tool skill is `llllloc:tool-<program>`. A row that loads `llllloc:task-design` adds `llllloc:impeccable`. `llllloc:task-research` is never optional: core rule 10, every answer but small talk and his own files.

Add only when needed:
- `llllloc:ponytail-review` on a code review ask, `llllloc:ponytail-audit` for a whole app.
- `llllloc:task-sharpen-prompt`: a short, vague ask where a misreading costs real work.
- `llllloc:task-be-ambitious`: "be ambitious", "aim higher", or the start of a client job.

Tag only: `llllloc:end` (adds `llllloc:end-plugin-log` on a Premiere suite job), `llllloc:task-learn` (the word `learn` alone, or a deep study of a thread, 22 Oct 2026), `llllloc:fundamental`, `llllloc:task-judge`.

## NOT ON THE MAC (29 Oct 2026)
llllloc runs in the Code tab, in the brain folder `~/Desktop/Claude`. In claude.ai chat or on the phone there are no Mac files, apps, maps or core rule. There: say so in one line, keep the hard stops (never delete, never guess a path, core V31), and answer from the chat only. A job that needs the Mac waits for a Code tab session.

## STEP 3 — RULES OF SELECTION
1. The smallest set. Two is normal, four is a warning (project skills, research, impeccable, ponytail, using-agent-skills, reference pair do not count).
2. A word is not a trigger, except his commands and a dropped reference. A skill he names always loads. A skill not in this file never loads.
3. Route every message, mid-thread too. A new ask, a change of program (Magnific pictures to Figma layers), a correction, or the first message after compacting: the first tool call is the Skill tool on `llllloc:router` itself, then the picks it names, before any job call (22 Oct 2026, 3 skips in one thread). A plain "ok" or a pick keeps the route. A board in a workflow thread is a design job. Two jobs: load both, design first.
4. Unsure and it changes the answer (paid renders, which program): ask one question. Never load extra for doubt.
5. Every llllloc skill is `llllloc:<name>` from the plugin (6 Nov 2026). Never pick an old name still installed: `skill-creator`, any `llllloc-...` name, or any `anthropic-skills:llllloc...` copy.
6. A huge job with parts that can run apart, like many videos: suggest nested sessions in one line before work, how many and what each owns. On his yes, load `llllloc:project-workflow` and run SPLIT (1 Nov 2026, his words).

## STEP 4 — CHECK, THEN ANSWER
Every job reply ends with two lines, one empty line between them, never a code block (18 Oct 2026). **Loaded:** in bold, then each skill in its own inline code mark (`core` `<project skill>` `<skill>`). **Time:** in bold, then `<n> min <n> s` in one inline code mark: run `date` just before the reply, minus the arrival time the router hook prints ("His message arrived at ...", 29 Oct 2026). Never guess (17 Oct 2026). The Loaded line copies the Skill tool calls made for this ask, never memory (22 Oct 2026). Run STEP 2 on his message again and compare. A pick with no call (the hub alone too, `llllloc:impeccable`, the reference pair, `llllloc:task-research`, a code job without `llllloc:ponytail` or `llllloc:using-agent-skills`): load it, check the work against it, fix, then reply.