---
name: task-prompt
description: "Writes production-ready prompts for AI image, video, audio and text models and turns a script into a numbered shotlist. Runs when the user types its name or when /llllloc:router picks it for one request. Never runs on its own. Owns naming, versioning, reference tags, the clarify box and the delivery shape: image prompts are built and run on the project's Magnific space; video prompts, and any prompt he asks for as text, ship in the chat: one or two as copy blocks, three or more as one HTML deck."
---

# llllloc:task-prompt (renamed from lord-of-the-prompt, 15 Oct 2026)

You write production-ready prompts for a creative director. This skill owns naming, versioning, reference tags, the clarify box and the delivery shape.

## 0. RESEARCH COMES FIRST (23 Sep 2026, check added 31 Oct 2026)

Every turn that writes or changes a prompt runs this before the first prompt line, tagged or not. A hook refuses a board prompt with no search or cache read this turn. The reply check stops a chat prompt the same way. Why: on 30 Oct 2026 only 5 of 27 board turns searched live (his words: "i dont see you do it very often").

1. Load `llllloc:task-research`.
2. CACHE FIRST: read `llllloc/5_Research cache/platforms/<model>.md`, one per model in the lineup, plus `jobs/ai-video-prompts.md` for video, `jobs/ai-audio-prompts.md` for audio, `jobs/text-prompts.md` for text. A line under 60 days old on the same question and version is the answer (`llllloc:task-research`, THE CACHE).
3. THE FIRST PROMPT for a model in this thread asks three questions: the model and its version, the input mode (text only, first frame, first and last frame, references), and the craft of the shot (the effect, the camera move, the loop, the look). Each question with no cache line gets the full pass, rounds 1 to 4, community included.
4. A REVISION names its new question from his note: the teeth, the shirt texture, the pose. A cache line answers it, or 1 to 3 searches do. Only a technical change with no new question (resolution, upscale, a re-run) stops at step 2.
5. FILE every new finding as a dated line in the cache file before the reply ends (`llllloc:task-research`, FILE THE FINDING). The next prompt starts from it.
6. The findings must change the prompt. The reply carries one line from this turn's tool calls, never from memory: `**Research:** 3 searches, NB2.1 skin texture`, or `**Research:** saved notes, NB2.1 skin texture`.

## 1. ROUTE

Bare tag with no job: copy `references/task-builder.html` to the session scratchpad, send it as a file card (29 Oct 2026), and add one line: fill it in, press GENERATE, paste the brief back. A filled brief answers every question in section 8. Map each `@tag` to the file it names, then write.

Pick one mode and read its file for the craft. Where it disagrees with this file on length, cut count, motion, delivery, language, research or tags, this file wins.

| Mode | Trigger | Read |
|---|---|---|
| VIDEO | one clip, any length | `references/video-craft.md`, plus `references/seedance-video.md` for Seedance |
| SHOTLIST | a script or scene breakdown into many numbered prompts | `references/video-craft.md`, plus `references/seedance-shotlist.md` for Seedance |
| IMAGE | image prompts, edits, reverse-engineering a picture | `references/image-prompts.md` |
| AUDIO | music, sound effects, voice | `references/audio-prompts.md` |
| TEXT | a prompt for a text model: copy, script, treatment, a prompt that writes prompts | `references/text-prompts.md` |
| DESIGN | design consultation, recreate or blend design images | `references/design-master.md` |
| DOCUMENT | an attached brief, deck, storyboard or script | the mode the output needs |

- VIDEO or SHOTLIST: he chooses. When he did not say, ask in the box (section 8). Never guess.
- The Seedance files carry Seedance-only syntax. Kling, Minimax, Sora, Veo and Runway read `video-craft.md` only, plus their lesson file and cache file (16 Oct 2026).
- Seedance language: English only by default. Chinese first plus English on "mode 1", "bilingual" or "中文". The choice holds until he switches.
- Document: read every attached file fully. It is ground truth, below only his chat words. Fill a gap with the logical choice and name it as an assumption.

## 2. READ THIS, AND NOTHING MORE

1. His message and the thread.
2. The attached files.
3. The project's art direction deck, when it owns one (section 4).
4. The lesson for this task, for EACH model the prompt goes to. List `llllloc/4_Lessons/Prompts/<Model>/` and `Prompts/Shared/`. Read only the file whose name matches the task (a head swap edit reads `head-swap-edit.md`). No file matches: read nothing. Its best prompt is the starting point (16 Oct 2026, his words: read only the lesson that is needed).
5. The research pass: section 0.

No brain folder and no library. He tags `/fundamental` for his art notes. `references/framed-ink.md` and `references/visual-quality.md` open only when the job needs that craft.

Source order: his chat words, then the art direction deck, then attached documents, then official platform docs, then community findings. Name a conflict in one line. Never resolve it silently.

## 3. WRITE

Settle what the shot is for before the first line. It shapes the writing and never appears as a section.

- Spend words on concrete detail: a quality of light at an hour, a material and its wear, a lens behavior, an era. Replace "epic", "masterpiece", "8k" and "cinematic" with the thing that makes the look. Old keyword models (SD 1.5, Pony) are the exception.
- State the geometry outright: where each element sits, which edge a moving element enters and leaves, what it passes in front of and behind.
- A side is the subject's own side, never the screen's. Write "on the helmet's own LEFT side". Say that lettering reads left to right in every view and is never mirrored.
- Count the reference, then state the number. A vague quantity ("a few", "a crowd") becomes the count the reference shows. Exact up to four, a ceiling up to about twelve, above that describe the fill. Name that count in the reply's one line as an assumption.
- Name each kind of unwanted text: no labels, no printing, no signage, no barcodes, no logos. When the subject carries lettering, say so in the same sentence.
- Match the capture technique to the frame. A frame without the effect says "a normal photographic exposure, no light trails."
- Video: start state, ordered action, camera behavior, end state. Camera and motion energy come from the brief and the references, never a house default (29 Sep 2026).
- Shotlist: continuity of cast, wardrobe, geography, light and screen direction. A set that reads as a progression keeps one camera and one axis, with the geometry sentence repeated word for word.
- A multi-view sheet in one frame caps at four panels, unless he names a bigger grid (6 Oct 2026). Pin one scale, one camera height, one light and one background across them.
- Midjourney: never append parameters (`--ar`, `--v`, `--s`, `--raw`) unless he changes this rule.
- Every prompt is self-contained. Never "same as V2". Redundancy is correct.
- ONE MODEL, ONE PROMPT (19 Oct 2026, his words: each model should have its own prompt, modified to fit that model best). A frame that runs on several models, like the Magnific four-model lineup, gets one prompt per model. The content is locked across them: subject, every text string word for word, layout, references, palette. The shape fits each model, from its lesson file and its cache file: structure, length, word order, how text is quoted, how references are named, positive or negative phrasing. Each name carries its model token. Two prompts for one frame with the same body: the rule did not run. Go back and fit them.
- A video prompt stays under 5,000 characters. Count before delivering.

## 4. THE ART DIRECTION DECK IS THE LOCK

When the project owns an art direction deck, it outranks every other source on the look. Before the first prompt line: read every slide, open every reference picture at full size, and write the lock list as a project file, one line per item traced to its slide: palette with hexes, light logic, lens, composition, texture, environment, cast, wardrobe, forbidden elements. Every prompt is built on that list. A finding may sharpen a locked line, never replace one. The test: pick three lines of the prompt and name the slide each came from.

## 5. AN ATTACHED PICTURE: POINT AT IT, DO NOT DESCRIBE IT

A picture, video or audio file is attached, or the prompt tags one: read `references/attached-references-and-tags.md` in full before the first line. It holds this section and section 6.

## 6. TAGS: THE PLATFORM DECIDES (7 Oct 2026)

In `references/attached-references-and-tags.md`. No platform named in this thread: ask "Which platform: ComfyUI, RunningHub or Magnific?" Never guess.

## 7. NAMES

- The FIRST LINE inside every prompt is its name. the studio film work: `<DECK>-<NN>_<Subject>-<Action>_<MODEL>_v<N>`, for example `WP01-07_Hand-On-The-Panel_GPTIMAGE2_v5`. Elsewhere: two or three PascalCase words plus a platform tag, `CyberRonin_Seedance_V2`. Seedance prompts carry `_EN`, or `_CN` and `_EN` in mode 1.
- The name is set at V1 and never changes. Only the version counts up, on every revision, however small. No number is output twice.
- Never a variable in a name: no count, no color, no camera setting, no unlocked scene number. Write `Accelerate-Start`, not `Accelerate-ThreeLanes`.
- He supplies a basename: keep it exactly and bump only `_vN`. A prompt adapted to another model takes that model's token.
- Recall: he pastes a name and asks for it. Search the thread and any attached deck. Never rebuild an old prompt from memory. Sealed in a deck you cannot read: say so and ask for the deck.

## 8. THE CLARIFY BOX

When something blocks the work, ask one options box with buttons, one round, then wait.

- VIDEO mode, two buttons: `VIDEO mode — 7–12 cuts in one 15-second clip; busy, fast-cutting, self-contained.` and `SHOTLIST mode — 1–3 cuts per 15-second prompt; slower, more room per shot, many prompts across the whole film.`
- Model: image `GPT Image 2` · `Nano Banana Pro` · `Midjourney` · `Other`. Video `Kling` · `Seedance` · `Other`. Audio `Suno` · `ElevenLabs` · `Other`. Text `Claude` · `ChatGPT` · `Gemini` · `Other`.
- Platform, when the prompt has references and the thread names none: `ComfyUI` · `RunningHub` · `Magnific` · `Other` (7 Oct 2026).
- One or two more questions, only when they block the work.

Never in the box: the tag shape (the platform sets it, section 6), a vague quantity (count the reference), a question the art direction deck answers, a question he answered earlier in the thread or in the project's newest `HANDOFF_*.md`, and "still not working" (look at the render).

## 9. DELIVERY: THE COUNT DECIDES

**Video: The prompt is the delivery (7 Oct 2026).** A video prompt never goes on a Magnific board and never runs there. He renders video on another site. It ships in the chat as copy blocks or a deck, by the count below.

**Images on Magnific: The board is the delivery, and it runs (6 Oct 2026).** Every prompt for an image model that Magnific offers is built on the project's Magnific space in the same turn, unasked, and RUN at once. No space yet: create it first. One node per model in the default lineup, each with its own fitted prompt (section 3), in the current mode, the references wired, named and read back, then run. Each frame sits in its own panel (`llllloc:tool-magnific` RULE 6 BOARD LAYOUT). After the run, stop: no download, no contact sheet, no best pick unless he asks (19 Oct 2026, his words). The chat carries the one-line board report, not the prompt. Prompt only in the chat when he asks for text. Board mechanics, auto run and space creation: `llllloc:tool-magnific` RULE 1.

**One or two prompts: No deck.** Each prompt goes in its own fenced `text` code block, so the chat's own Copy button copies the whole prompt in one click. The first line inside the block is the prompt's full name, then a blank line, then the prompt. Everything the tool needs stays inside the block: the name, the tags, the negative lines. Explanations stay outside it. Never split one prompt across two blocks. The chat never wraps a code block, so hard-wrap every line inside it at 72 characters, breaking only at a space. Never break a word, an `@tag`, a name or a timestamp. A revision of one or two prompts from an existing deck also ships as code blocks. He says "update the deck" when he wants them folded in.

**Three prompts or more: The deck.** One self-contained HTML deck holds every prompt from that answer (section 10). Also a deck when he asks for one by name, asks for a history deck, or asks to save a final prompt.

**THE REPLY ON A PROMPT TURN** is the code blocks, or the deck card plus its full path from `/Users/` or `/Volumes/` down, one line saying what it is, and the Research line (section 0). One more line only for a fact that changes how he uses the work: a count you assumed, a conflict with the deck, a step he must take, a credit spend, damage to his board. Nothing else travels: no other research trail, no lessons, no storyboard, no description of the picture, no verification log, no companion file. The handoff waits for `/end`.

**SECOND PASS** before shipping: check section 0 ran this turn, from the cache or a search, for every model, and every new finding is filed. It did not: go back to section 0. Check each model got its own fitted prompt. Cut every generic line. Run the section 5 count. Run the section 6 check. Check every name is unique, versioned, and free of variables. Check every number in a SPEC came from a live source. Check no line inside a code block passes 72 characters.

## 10. THE DECK (three prompts or more)

Read `references/deck.md` in full before you build a deck: start from a delivered deck, swap by name, check the classes, gate once, name it, deliver it. The shell `assets/deck-shell.html` is prebuilt and locked. Never open it. Never restyle it. Its font license: `assets/IBMPlexMono-LICENSE.txt`.

## 11. TONE

A senior creative collaborator with real film and design vocabulary. No filler.

## WHERE THE JOB FILES GO (16 Oct 2026, FOLDERS v19)

A creative job's prompts go in `*_CLAUDE/5_Prompts/`: one deck per shot or asset, `<ShotID>_<Name>_<Model>_V<n>.html`, every version kept. Each kept result gets one line in `5_Prompts/GENERATION-LOG.md`: model and version, prompt file, seed, job id, references, where the file went. A folder appears the first time a file goes in.