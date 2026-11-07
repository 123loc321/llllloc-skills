---
name: task-learn-video
description: Learns from videos. One or many YouTube links or video files are studied frame by frame plus the transcript, and what is useful is written as a LESSON card (the recipe with a time and a frame per step, the values, what transfers, how to apply it to a named project). Later applies a card to his work on his word. Any kind of video for any project or task (a tutorial, a workflow setup, a breakdown, a talk, a review, a vlog). Use when he types its name, or when /llllloc:router picks it for a dropped link or video with the words learn, study, lesson, teach me, how they did it, or apply what you learned. Never for a dropped reference to match or copy (llllloc:references), the word learn alone (llllloc:task-learn), or subtitles (llllloc:task-vo-to-srt-subtitle).
---

# llllloc:task-learn-video (26 Oct 2026)

A video becomes a LESSON card: what it teaches, the recipe step by step with the time and the frame that proves each step, the values, what transfers to other work, and how to apply it to his project. The card is the thing he keeps. The raw material (transcript, frames, on-screen text, contact sheets) stays beside it so a later thread can check a step without watching the video again.

## TOP RULES

1. **The study runs on his Mac, in this session** (29 Oct 2026). The Mac opens YouTube and has yt-dlp, ffmpeg 9, python3 and Apple's text reader, and the script `study_video.py` uses only those. Nothing is installed and nothing paid (core rule 1).
2. **Every step carries its proof.** A numbered recipe step ends with `t=m:ss frame=frames/f_HHMMSS.png` and one tag: SEEN (read on the frame), HEARD (said in the transcript), LINKED (in a file from the description), INFERRED (my reading, not shown or said). A value that was neither seen nor heard is INFERRED, never stated as a fact. Why: the card gets applied to client work later, and a wrong number there costs a day. `study_video.py check` fails the card when a step has no time, no frame, or a SEEN value the text reader did not find.
3. **Job material in the job, universal in llllloc** (his words, 17 Oct 2026). A study for a named project goes in that project's `*_CLAUDE/2_References/`. A study with no project, or a lesson that works on any job, goes under `llllloc/4_Lessons/`. Paths: WHERE IT GOES.
4. **A video is studied once.** APPLY and ASK read the card and the index. They never download or cut frames again. A second study of the same link reuses the batch (the script skips what is on disk).
5. **Nothing is deleted.** Batches, frames and thumbnails are kept forever, like every reference batch (25 Oct 2026). A wrong card gets a new version beside it.
6. **Promo, sponsor and intro segments are marked in the card and never learned from.** The tell: a product name with a discount code, "this video is sponsored", a channel plug.
7. **The transcript is read in full, the frames through the sheets first.** Reading only the first minutes, or only the frames the index flagged, is the one mistake that makes a card wrong. The reading order is in HOW TO READ.

## THE MODES

| He says | Mode | He gets |
|---|---|---|
| A link or a video file, with or without a project name | STUDY | One LESSON card per video, its batch, and one line in the program's `From videos.md` |
| Many links at once | STUDY each, then COMPARE | The cards, plus a COMPARE block: where the videos agree, disagree, and which recipe to try first |
| "apply what you learned from X to Y", "use the Qazi recipe on the client clips" | APPLY | The recipe done in his tool on his material, with every deviation named |
| A question about a studied video | ASK | The answer with `t=` and the frame, from the card and the index |

## WHERE IT GOES

| Study for | Batch (raw material) | Card | Index line |
|---|---|---|---|
| A named project | `<job>/*_PROJECT FILES/*_CLAUDE/2_References/_batches/<videoid>_<slug>/` | `<job>/*_PROJECT FILES/*_CLAUDE/2_References/LESSON_<slug>.md` | `llllloc/4_Lessons/Programs/<Program>/From videos.md`, only when WHAT TRANSFERS is not empty |
| No project, a program is taught (DaVinci Resolve, ComfyUI, Premiere Pro, After Effects, Blender...) | `llllloc/4_Lessons/Programs/<Program>/Videos/<videoid>_<slug>/` | `llllloc/4_Lessons/Programs/<Program>/LESSON_<slug>.md` | the same `From videos.md` |
| No project, no program (a talk, a craft lesson, a breakdown) | `llllloc/4_Lessons/Craft/<Topic>/Videos/<videoid>_<slug>/` | `llllloc/4_Lessons/Craft/<Topic>/LESSON_<slug>.md` | `llllloc/4_Lessons/Craft/<Topic>/From videos.md` |

The job path comes from the project map (`llllloc/3_Project maps/`), never guessed (core rule 3). `<slug>` is the channel and the subject in a few words, like `cullen-kelly_look-development`. `From videos.md` holds one line per video: date, title, link, card path, the lesson in one line. It is how APPLY finds a card from another job.

## STUDY

Copy this checklist into the status checklist and tick it:

```
- [ ] 1 The ask read: links, project, what he wants to learn it for
- [ ] 2 The batch folder and the card path chosen (WHERE IT GOES)
- [ ] 3 Script run on the Mac (mac-brief.md), STUDY_READY.md read, failures named
- [ ] 4 Material read in the order of HOW TO READ, transcript in full
- [ ] 5 Card written from lesson-template.md, every step with t= frame= and a tag
- [ ] 6 study_video.py check passed. Fail: back to 5
- [ ] 7 Card, index line and batch on the Mac, the card sent as a file card with its path
```

1. **Read the ask.** The links, a local file, the project if named, and what he wants it for ("for the client grade", "to set up background replacing"). No project named: the card still ends with APPLY TO for the project the video most likely serves, labeled "likely", and the study goes to the universal path. Done when the links, the project and the purpose are written in the checklist.
2. **Choose the paths** from WHERE IT GOES. Done when both paths exist or are about to be created by the script.
3. **Run the study on the Mac.** This session runs the script in Bash, with the steps in `mac-brief.md`. The script writes the batch and ends with `STUDY_READY.md`, read in place. A bot check from YouTube: run again with `--cookies opera`, and say so in the reply. No captions: the script runs whisper on its own. Done when STUDY_READY.md is read and its Failed list is empty or named in the checklist.
4. **Read the material** in the order of HOW TO READ. Done when every chapter of the video has at least one note, and every value the card will carry has a frame.
5. **Write the card** from `lesson-template.md`. The kind of video decides which fields matter: `kinds.md`. Done when the card has WHAT IT TEACHES, RECIPE, VALUES, WHAT TRANSFERS, APPLY TO and OPEN filled, and every recipe step carries `t=`, `frame=` and a tag.
6. **Check it.** Run `python3 -I study_video.py check "<card>" --batch "<batch>"` on the batch path. A problem: return to step 5, fix the step or change its tag, then check again. Done when the check prints `problems: 0`.
7. **Deliver.** The card and the index line are written straight to their Mac folders. The card reaches him as a file card plus its full Mac path (`llllloc:task-sending-files`). Done when both files are on disk and the reply is sent.

Many links: steps 1 to 6 per video, one batch each, then the COMPARE block in the reply and at the end of each card. Three or more long videos: say how long the Mac will take before starting (about 1 minute per 10 minutes of video on his M3 Max, whisper adds 3 minutes per 10 minutes).

## HOW TO READ

Claude reads pictures, not video, so the study is a reading job with these rules. Why they exist: the baseline run on a 17-minute grading video (26 Oct 2026) got the panel names right, missed the node labels, and invented one value that was never shown.

1. `STUDY_READY.md` first: length, chapters, what failed, the links in the description. A link to a workflow file, a LUT, a preset, a repo or a Patreon post is opened: it often holds the whole recipe in one file (LINKED beats SEEN).
2. `transcript.txt` in full, start to end. Note every sentence with a number, a setting, a "why", a warning, a "most people get this wrong". The speaker says the reason, the screen shows the value.
3. Every `sheets/sheet_NN.jpg`, in order. A sheet is 12 frames with the time on each tile: enough to see the shape of the video, which panel is open, when the picture changed. Never read a value from a tile.
4. `index.md`: one row per frame with the text the Apple text reader found and what was said around it. The words on screen are the evidence for SEEN. A value in the transcript that is not in any row: find its frame on the sheets and open it.
5. The frame behind every step: `frames/f_HHMMSS.png` at full size. A value still small: `python3 -I study_video.py zoom <frame> x y w h` cuts a 2x crop. Open the crop, not a guess. A node tree or a curve: the crop of that panel.
6. Between two kept frames the screen did not change in a way the detector saw. A value typed and overwritten inside one second can hide there: when the transcript says a number the frames do not show, say so in OPEN.
7. A sponsor, intro or outro segment is skipped after one line notes its time range.

Twenty pictures per reply is the limit in this app, and a full 1080p frame costs about 1,600 tokens: read sheets for the overview, frames for the values, crops for the small ones, and nothing twice.

## APPLY

1. Find the card: the project's `2_References/`, then every `From videos.md` under `llllloc/4_Lessons/`. No card: say so and offer STUDY, never start a study on an apply ask.
2. Read the card in full, and the frame behind any step whose value matters for this material.
3. Load the tool skill of his program (`llllloc:tool-davinci-resolve`, `llllloc:tool-premiere-pro`, `llllloc:task-colorist`, the ComfyUI route...) and do the recipe on his material, in the order of the card. A step that does not fit his material is changed, and the change is written as a deviation, with the reason.
4. The check is the card's BEFORE AND AFTER line: the same measure on his result (a scope reading, a render beside the reference, a file that opens). No measure possible: "no outside check" in the reply.
5. The reply: the result, the deviations, the check. The card gets a line under APPLIED: date, project, what changed.

## THE REPLY

The card as a file card plus its Mac path, then five lines at most: what the video teaches in one line, the one step that matters most, what transfers, what is open, where the files are. Many videos: the COMPARE block after the lines. Then the closing lines of core rule 9 (Loaded, Time). No transcript, no frame list in the reply.

## FILES

| File | What it is | When |
|---|---|---|
| `study_video.py` | The script: metadata, captions or whisper, download, frames on change, text on screen, index, sheets, zoom, check. Run it, do not read it. | STUDY steps 3 and 6, HOW TO READ 5 |
| `vision_ocr.swift`, `sheet.swift` | Apple's text reader and Apple's drawing (the contact sheets with their labels) as commands. The script builds both on first run. | never read |
| `mac-brief.md` | The steps this session follows to run the study in Bash | STUDY step 3 |
| `lesson-template.md` | The LESSON card, strict in its headings and the step format, free in its length | STUDY step 5, APPLY 1 |
| `kinds.md` | What to capture for each kind of video, and what the program-specific recipe needs (a grade, a ComfyUI workflow, an edit, a 3D build, a talk) | STUDY steps 4 and 5 |
| `words_davinci_resolve.txt`, `words_comfyui.txt`, `words_premiere_pro.txt` | The program's own words for the text reader (`--words`). A new program gets its own list, one word per line. | STUDY step 3 |
