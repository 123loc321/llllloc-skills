---
name: task-design-system
description: "Makes and keeps the one design system file of a job, DesignSystem_Name_V1 and its later versions, for any medium: UI, website, deck, poster, key visual, storyboard frames, film look, motion. Runs when the user types its name, or when /llllloc:router picks it for a design system ask or for any design or motion job whose direction is picked and that has no DesignSystem file yet. Shows three or four rendered system sheets, stops for his pick, then writes V1. Also rebuilds a system from a live product or site, and writes a new version when he changes the look in words. Never builds the job itself: llllloc:task-design, llllloc:task-motion and llllloc:task-app-builder build on the file this skill writes. Not for applying a system that already exists."
---

# llllloc:task-design-system (17 Oct 2026)

One job gets one design system, written down once, read by every skill after it. The file is `DesignSystem_<Name>_V<N>.md`. `<Name>` is the job or brand in ASCII with no spaces (`DesignSystem_HondaXL250R_V1.md`). The highest V number is the one in force. Never the word "lock" in a file name (his words, 17 Oct 2026).

## TOP RULES

1. THE FILE COMES BEFORE THE ROLL-OUT. No design, motion or app job rolls out before the file exists. Exploring directions runs first without it (22 Oct 2026, his words). Why: a direction rolled out with no system gives the generic default (30 Sep 2026).
2. THE STOP IS THE ONE QUESTION. He picks one rendered sheet. Nothing of the job is built before his pick. A rendered pick, never a text question. Only proceed when he has named a sheet or answered with criteria.
3. ONE FILE, EVERY MEDIUM. Motion, After Effects, Cavalry, Figma, decks, apps and prompts read the same file. Each sheet carries one proof piece per medium the job has. Why: a system with no real piece in it does not fit the work (Brad Frost; 17 Oct 2026 research).
4. A SYSTEM CHANGES ONLY ON HIS WORDS. Then a new version the same turn. Every older version stays beside it.
5. WHERE IT LIVES. A creative job: `*_CLAUDE/3_Art Direction/`. A code job: `_CLAUDE/3_Design/`. Older files count as the system until a V1 replaces them: `ART-DIRECTION.md`, `ART-DIRECTION-LOCK.md`, `LOOK-LOCK.md`, a loose `DESIGN.md`. A plugin panel skips this skill: `llllloc:task-plugin-builder/panel-ui/` is its system. A job with no folder is normal: deliver the file and say where it should live.

## THE TASK TABLE

Name the task first, then read its one file.

| The situation | Task | Read |
|---|---|---|
| No DesignSystem file, a new look to find | SHEETS | `references/system-sheets.md` |
| He picked a sheet, or gave criteria | WRITE V1 | `references/file-template.md` |
| An existing product, site or Figma file with no file yet | FROM PRODUCT | `references/design-system-from-product.md` |
| He changes the look in words, on a job with a file | NEW VERSION | `references/file-template.md`, section "How a version changes" |
| His own mockup, his brand guidelines, a text edit, a recolor, a nudge | WRITE WITHOUT THE STOP | `references/file-template.md` |

## THE STEPS

```
- [ ] 1 CHECK: newest DesignSystem_<Name>_V<N>.md found, or an older file named, or none
- [ ] 2 READ: ART-DIRECTION.md, VISUAL-PREFERENCES.md, DESIGN-SYSTEM.md, his message, the brief
- [ ] 3 RESEARCH: llllloc:task-research, the three design questions, cache first
- [ ] 4 SHEETS: three or four rendered, each with a proof piece per medium
- [ ] 5 STOP: he picked. Not yet: end the turn, build nothing
- [ ] 6 WRITE V1 the same turn as the pick
- [ ] 7 CHECK THE FILE: every color has a role, every number is read off a node, motion block filled, REJECTED list filled. A miss: back to 6
- [ ] 8 FILE: the path goes in the project map and in the job's STATE.md
```

1. CHECK. `ls` the folder. One exists: read it, say which file in one line, and stop here unless he asks for a change. Never guess a path (core rule 5).
2. READ the job's files in the order of authority: his message, `VISUAL-PREFERENCES.md`, the newest DesignSystem file, `DESIGN-SYSTEM.md`, then the brief. `llllloc:task-art-direction`'s brand file for a client with one.
3. RESEARCH runs on every sheet turn (`llllloc:task-research`): the reference look and what makes work read as it, what separates the premium grade from the cheap one, how the program builds it best. A revision asks only the new question.
4. SHEETS: `references/system-sheets.md`. The sheets differ in kind, never in shade. Each is rendered at final size and looked at before it ships (`llllloc:task-design` RULE 2).
5. STOP. The reply shows the sheets, one line of trade-off under each, numbered. It ends with the question. Nothing else in that reply.
6. WRITE V1 from the picked sheet: `references/file-template.md`. Real numbers read off the nodes, never the numbers you planned.
7. CHECK with the list in the template. Then one line in the reply: the file path and what the job builds on next.
8. FILE the path (core rule 16). The handoff is `llllloc:end`'s job.

## RULES

- SKIP THE STOP, still write the file (WRITE WITHOUT THE STOP): his numbers or his brand guidelines are the system. Say so in one line.
- The sheets are the RULE 4 directions of `llllloc:task-design`: that skill's craft rules, visitor mode and `references/craft-library.md` apply to every sheet. `llllloc:impeccable` comes along when the router loads it.
- The order of authority on any clash: what he says in this message, then `VISUAL-PREFERENCES.md`, then the newest DesignSystem file, then `DESIGN-SYSTEM.md`, then the program folder, then the craft skills. Say which rule you set aside.
- A value a later job needs and the file lacks: add it to the current version first, dated, then use it. No new V number for an addition.
- His exact words on the look go to the job's `FEEDBACK-LOG.md`. His instruction becomes one short dated rule in `VISUAL-PREFERENCES.md`.
- This skill changes only when he says so in words (`llllloc:task-skill-creator`). A job's fact never enters this file.

## THE REPLY

A SHEETS turn: the sheets, the trade-offs, the question. A WRITE turn: the path, the five numbers that define the system (ground, accent, display face, grid step, signature), what was rejected, one line on what builds next. Then core rule 9's two lines.
