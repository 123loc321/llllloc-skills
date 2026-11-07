---
name: references
description: "The shared rules for every dropped reference in llllloc: how a reference is sorted, measured, researched, judged and written into the craft dossiers. Always loads together with one medium skill, which holds the professional read and the tools: llllloc:references-photo, -design, -edit, -motion, -sound, -code, -people, -space, -cinematography, -color-grading or -art. Runs when the user types its name or when /llllloc:router picks it for a dropped reference to analyze or break down, learn from these, add to my references, is this good, does this feel like me, or a prompt or design that needs his style or follows references he just dropped. Never the only skill on a reference job: a reference with no clear medium is sorted first, then the medium skill loads."
---

# llllloc:references (split 17 Oct 2026, his words: "we will split the reference skill"; rebuilt 16 Oct 2026: "analyze reference like a true professional")

He drops references. Each one is read the way the professional who made it would. This skill holds what every medium shares. The read itself, the fields and the tools live in one medium skill:

| He drops | Medium skill | The result feeds |
|---|---|---|
| A photo, render, key visual, one film frame | `llllloc:references-photo` | `llllloc:task-prompt` IMAGE, `llllloc:tool-magnific`, `llllloc:task-art-direction` |
| A poster, deck page, layout, UI screenshot, Figma file, PDF | `llllloc:references-design` | `llllloc:task-design`, `llllloc:tool-figma`, `llllloc:task-app-builder` |
| A cut film, ad, music video, any edited video file or link | `llllloc:references-edit` | `llllloc:tool-premiere-pro`, `llllloc:task-art-direction`, `llllloc:task-prompt` VIDEO |
| An animation, motion graphics, title, web or app animation | `llllloc:references-motion` | `llllloc:task-motion`, its program skill, `llllloc:task-prompt` VIDEO |
| A track, mix, sound design, VO, SFX | `llllloc:references-sound` | `llllloc:task-sound-design`, `llllloc:tool-premiere-pro`, `llllloc:task-prompt` AUDIO |
| A website or app link, or its code, to learn from or rebuild | `llllloc:references-code` | `llllloc:task-app-builder`, `llllloc:task-plugin-builder`, the Code job (`llllloc:project-code`) |
| A person: pose, body, face, hair, makeup, outfit, wardrobe, styling | `llllloc:references-people` | `llllloc:task-prompt` IMAGE and VIDEO, `llllloc:task-art-direction` (casting, shoot, wardrobe) |
| A place: architecture, interior, room, set, props, landscape | `llllloc:references-space` | `llllloc:task-prompt`, `llllloc:task-art-direction` (set, location), `llllloc:task-design` |
| A video for its shots: camera move, rig, lens, VFX, cinematic technique | `llllloc:references-cinematography` | `llllloc:task-prompt` VIDEO, `llllloc:task-art-direction` (shoot plan), `llllloc:tool-after-effects` |
| A look for its colour: a grade on a still or a film, a LUT, a film stock feel | `llllloc:references-color-grading` | `llllloc:tool-premiere-pro` (Lumetri), `llllloc:task-prompt`, `llllloc:tool-magnific` |
| An illustration, drawing, painting, concept art, character design, animation frame, comic | `llllloc:references-art` | `llllloc:task-prompt` IMAGE, `llllloc:task-design`, `llllloc:task-art-direction` |

The first six read how a reference is MADE. People and space (17 Oct 2026) read what a picture is OF; the same picture's light and lens still go to photo. Cinematography reads the shot, color-grading reads the grade, edit reads the cut; a film often loads two of them. Art (17 Oct 2026) reads a drawn or painted picture; a photographed one is photo. A film with sound loads edit and sound. A site with motion loads code and motion. The router picks; a medium skill he names always loads.

## TOP RULES

1. Describe how it is MADE, never only what it is OF. Every finding names a measurable property: not "blue" but "cool cyan shadows near #1E4D5C at about 15 percent saturation against warm highlights".
2. Measure before you judge. A number from a tool beats a number by eye. Every number carries its source: the tool and its output, `~` for by eye, `unknown` when nothing could read it. Observations, inferences and unknowns stay in separate sentences (borrowed from REA, 17 Oct 2026). A field with no evidence is `unknown`, never a guess.
3. Every batch gets research on the TECHNIQUE and the MAKER, never on the subject or the client.
4. Anti-homage: a recipe line that only works on the original subject is a copy, not knowledge. Every line must transfer. Whose material it is decides what goes in: his own files and a client's files (logo, face, product, footage, code, copy) go straight into the work as given. An outside reference gives its mechanism; its own content comes in when he says so. No legal rule caps a job (his words, 17 Oct 2026).
5. Honesty over flattery, his own work included. Never ask him to describe his style; read it off the work.

## WHERE EVERYTHING LIVES

llllloc holds only what is universal: the dossiers and the index. A job holds everything about its own references (his rule, 17 Oct 2026: "each reference analyze belongs to a job ... llllloc only holds universal stuff").

```
<job>/_CLAUDE/2_References/                       the job's reference work, written first (his words, 17 Oct 2026: references and research are two folders)
  <KIND>_<name>.md                           the sheet or spec: SHOTS_, GRADE_, ART_, PEOPLE_, SPACE_, REFERENCE_<site>
  _batches/<source>.md                       the raw reads, measurements and tool output, rarely re-read
  _batches/<source>/Claude screenshots/      every frame and scope picture grabbed, kept for good (rule below)
  _batches/frame_index/                      sampled frames and features of the job's footage, kept for good (rule below)
<job>/_CLAUDE/2_Research/                         the job's facts (RESEARCH.md), never a reference note
llllloc/2_Skills/Job skills/references/   the universal part, written second
  INDEX.md                                   read FIRST, every session: medium to dossier map, tag vocabulary
  <MEDIUM>.md                                one dossier per medium: what recurs across jobs, never a job's raw notes
  _batches/                                  only for a reference with no job (his taste library, "add to my references")
llllloc/6_Fundamental knowledge/visual-library/MASTER-STYLE-PROFILE.md   the aggregate across every medium
```

`<source>` is the reference's name as he gave it, with no date in front (his words, 17 Oct 2026). The dropped file itself (picture, clip, sound) stays with the project's assets, `1_VISUAL ASSET/**_Ref/` or `3_SOUND ASSET/`, never in `*_CLAUDE/`, which holds notes only. A Code job has no asset folders, so its dropped files go to `_CLAUDE/2_References/Files/` (his words, 17 Oct 2026: a code job gets a reference folder too). Every medium skill's "raw output to `_batches/`" means the job's `2_References/_batches/` when the reference serves a job, and llllloc's only when it serves none. A creative job's folder is `*_CLAUDE/`, a Code job's is `_CLAUDE/`.

## THE MODES

Every mode starts with the medium skill loaded and named on the Loaded line. Not loaded: load it before the first read (his words, 19 Oct 2026: "When i drop references like this, you suppose to load the correct reference skill").

| Mode | Trigger | Does |
|---|---|---|
| ANALYZE | a dropped reference with "analyze", "break this down", "learn from these", "add to my references", or no instruction | the six passes below |
| CRITIQUE | "is this good", "does this feel like me", "rate this" | two tracks, CRAFT and TASTE |
| CONSULT | a prompt, design, edit, motion, mix or build is being made in his style, or from references he just dropped | the treatment from the dossier. Fresh drops: run ANALYZE on them first, then build from that sheet, never from a glance |

## ANALYZE, the six passes

1. **Sort.** A compact table: item, medium, confidence, one-line reason. What he drops is work he admires, TIER 2. Ask only whether any item is HIS OWN work (TIER 1). Load the medium skill for each medium present, if the router did not.
2. **Measure.** Run the medium skill's MEASURE block on the file first. Check `which` for each tool. Missing: install only on his yes (core rule 1), Python with `uv run --with <package>` (29 Oct 2026). No yes: say which, read by eye, mark every number `~`.
3. **Read like the pro.** Fill every field of the medium skill's table, or write `unknown` and why.
4. **Research, mandatory.** 3 to 6 searches with `llllloc:task-research`, starting with the medium skill's RESEARCH list: the maker and the team, what practitioners call this technique, the tools and process, interviews or breakdowns by the makers, whether it is a durable technique or a dated trend, what goes wrong when people copy it. Cache first: `llllloc/5_Research cache/jobs/reference-analysis.md`. Skip only when the batch repeats a medium already researched, and say so. A maker's video, a Reddit thread or a page a plain fetch cannot open goes through REACH in `llllloc:task-research`.
5. **Interpret, then judge.** For each key choice, say whether it is reproductional (just records), pictorial (decorative) or representational (carries the story's meaning), and what it makes the viewer feel. Then judge it as craft: what is strong, what is weak.
6. **Write.** Append to the medium's dossier (format below), add the raw reads, numbers and tool output to the job's `_batches/` (llllloc's only with no job), update `INDEX.md` (one line per medium) and `MASTER-STYLE-PROFILE.md` (only what recurs ACROSS mediums: three items is a signature, two a lean, one a note). Deliver every written file with `llllloc:task-sending-files`.

Check before the reply: every number has a source, every field is filled or `unknown`, every recipe line transfers to a new subject. One fails: go back to that pass.

## THE DOSSIER

```markdown
# <MEDIUM> — craft dossier
Updated: <date> · Batches: <n> · Items: <n>
## THE RECIPE            the reproducible build, in order. Every line names a mechanism.
## WHAT MAKES IT LAND    three to five choices: the choice, why it works, what breaks without it
## MEASURED FACTS        numbers only, each with its tool or `~`
## WHAT THE RESEARCH FOUND   makers, technique names, tools, shelf life, links
## DO NOT COPY           what is signature to that maker, what is a dated trend, what this reference cannot do
## OPEN                  what the batch does not answer yet, the unknowns by name
```

## CRITIQUE

Two tracks, always named. CRAFT: is it well made, style-neutral, tested with the medium skill's read and `llllloc:task-prompt/references/visual-quality.md` for images. TASTE: does it match his dossier for that medium. When they disagree, say so; that is the most useful output. Lead with the verdict, name what is weak in craft terms, then give directions with trade-offs. "Looks great" is worthless to a creative director.

## CONSULT

Load that medium's dossier and supply the TREATMENT only: light logic, material, palette, framing, timing, sound, structure, anti-patterns, as integrated intent, not a bag of tags. The job skill owns the output: `llllloc:task-prompt` the prompt, `llllloc:task-design` the layout, `llllloc:task-motion` the motion, `llllloc:tool-premiere-pro` the cut, `llllloc:task-sound-design` the mix, the Code job the build. Name the dossier lines you used. If the brief fights the dossier, say so and propose a way through.

## GLOBAL RULES

- Read `INDEX.md` first, every session. Never start a dossier that exists.
- Treatment from an outside reference, content from him and the client. A client's logo, face or object is content to use, not a reference to translate.
- Never write into `llllloc/6_Fundamental knowledge/` unless he says so in that message. `MASTER-STYLE-PROFILE.md` is the one exception. His own art notes open only through `llllloc:fundamental`, on his tag.
- Ask in one options box or not at all.
- Claude screenshots and frame indexes (his words, 25 Oct 2026): every frame grabbed from a video, every scope picture and every frame index (sampled frames, their features, the script that made them) is saved in the job's `2_References/_batches/`: frames in `_batches/<source>/Claude screenshots/`, indexes in `_batches/frame_index/`. Never in a temporary work area (the Mac work area's disk is small: it filled and stopped, 25 Oct 2026), and never deleted, because a later turn may need them. File names carry the shot number and time (`shot_07_12.40s.png`). A reference with no job uses llllloc's `_batches/`.

## THE REPLY AFTER AN ANALYSIS

One line on what came in and how it sorted. The single strongest finding, with its number and its source. What the research added, with links. What the batch still lacks, as named unknowns. The files carry the rest.