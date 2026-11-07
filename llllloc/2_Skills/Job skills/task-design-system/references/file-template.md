# THE DESIGN SYSTEM FILE — DesignSystem_<Name>_V<N>.md

Part of `llllloc:task-design-system` WRITE V1, WRITE WITHOUT THE STOP and NEW VERSION. Read in full before you write or change the file.

## Contents
- Why this shape
- The frontmatter
- The sections
- How a version changes
- Check before the file ships

## Why this shape

The frontmatter follows Google's DESIGN.md format (`google-labs-code/design.md`, version alpha, read 17 Oct 2026), so a code job can run `npx @google/design.md lint` and `export` on it and `llllloc:task-app-builder`, `llllloc:impeccable` and Figma tools read the same numbers. Motion has no place in that format yet (its issue 47, open), so the `motion` block is this workflow's own and lint ignores it. Everything a later job copies is a number or a path, never a mood word. Why: an AI reading hex values with no role, ranges instead of absolutes, or "use sparingly" gets the system wrong (17 Oct 2026 research).

## The frontmatter

Exact structure. Write only the keys the picked sheet defines. Token references use `{colors.accent}`.

```yaml
---
version: alpha
name: <Name>
description: <one sentence a crew could act on>
colors:
  ground: "#141413"        # one role per color, in the comment
  surface: "#1C1C1A"
  text: "#FAF9F5"
  support: "#B0AEA5"
  accent: "#E7FE55"        # the one accent
typography:
  display:
    fontFamily: <family>
    fontWeight: <weight>
    fontSize: <px>
    lineHeight: <number>
  supporting:
    fontFamily: <family>
    fontWeight: <weight>
    fontSize: <px>
    lineHeight: <number>
  microcopy:
    fontFamily: <family>
    fontWeight: <weight>
    fontSize: <px>
    lineHeight: <number>
rounded:
  base: <px>
spacing:
  step: <px>
  margin: <px>
  gutter: <px>
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.ground}"
    rounded: "{rounded.base}"
    padding: <px> <px>
motion:
  easing:
    enter: [0, 0, 0.3, 1]        # cubic-bezier, four numbers
    exit: [0.4, 0.14, 1, 1]
    standard: [0.2, 0, 0, 1]
    emphasized: [0.05, 0.7, 0.1, 1]
  duration_ms:
    fast: 120
    base: 240
    slow: 400
    hold: 700
  stagger_ms: 40
  spring:
    damping: 0.9
    stiffness: 700
  reduced_motion: fade only, no travel
---
```

## The sections

In this order. A section the sheet did not define is left out, never invented.

1. `## Overview`. The job in one sentence, who sees it, where. The direction sentence. The visitor mode (`llllloc:task-design` `references/directions-and-runs.md`).
2. `## Colors`. One line per role: where it goes, where it never goes.
3. `## Typography`. The three levels and their case. Never stretch a letter. The measure (60 to 75 characters).
4. `## Layout`. Grid, margins, spacing step, hang line, safe areas for the medium (vertical: `llllloc/5_Research cache/jobs/design/vertical-safe-zones.md`).
5. `## Elevation & Depth`. Shadow logic, glow logic, or none.
6. `## Shapes`. Radius, stroke, corner logic. One era.
7. `## Components`. The recipes a later frame copies: card, button, input, frame template, lower third, title card. Each as a list of numbers, not prose.
8. `## Motion`. The four showreel lines on top (THE CLASS, WHAT IT IS NOT, THE LANGUAGE, THE SIGNATURE: `llllloc:task-motion` `references/showreel-brief.md`). Then: which easing goes with which move, the duration rule (exit shorter than enter, duration grows with distance), the stagger rule, the one signature move and its VO word, the reduced-motion fallback. Written on every job that moves, and on any job whose design may move later.
9. `## Signature`. The one element, how it is built, where it may and may not appear.
10. `## Image treatment`. Crop, grain, grade, masks, what a plate must have, what is banned.
11. `## Master and parts`. The master to copy from: the Figma link and the frame or section name, the master `.motion` or comp, the asset folder. A new frame copies parts from the master, it never redraws them. How to build a new frame, in numbered steps.
12. `## Proof pieces`. The path of every rendered proof piece, one per medium.
13. `## Do's and Don'ts`. Binary lines only. "Never" and "always", never "sparingly".
14. `## Rejected`. The sheets he did not pick, one short line each, and his stated rejections, dated.
15. `## Changelog`. One line per version: date, what changed, in his words.

## How a version changes

- The system changes only when he says so in words. Then the next version (V2, V3) the same turn, dated, with one line on top saying what changed. Every older version stays beside it in the same folder.
- A small addition a later job needed, or a rejection he states, goes into the current version, dated, with no new V number.
- A code job wants a plain `DESIGN.md` beside it: export it from the same file, never write a second source.
- Old files (`ART-DIRECTION.md`, `ART-DIRECTION-LOCK.md`, `LOOK-LOCK.md`, a loose `DESIGN.md`) are read into V1 when it is written, then moved to `Old/` beside it. Their words stay word for word in `## Rejected` and `## Changelog` where they still apply.

## Check before the file ships

- [ ] Every color has one role and one place
- [ ] Every number was read off a node or measured, never planned
- [ ] Three type levels, the measure named
- [ ] The motion block filled on any job that moves
- [ ] The master named with a link or a path
- [ ] A proof piece path per medium
- [ ] Do's and Don'ts binary
- [ ] Rejected list filled
- [ ] A code job: `npx @google/design.md lint` ran clean, or the reply says it could not run
