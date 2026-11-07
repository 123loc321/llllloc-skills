---
name: tool-figjam
description: "His rules for FigJam boards (figma.com/board links), such as the llllloc workflow board. Use when /llllloc:router picks it for any read, build or update on a FigJam board. Holds the section state colors (yellow, red, green), the archive rule, versioning and the panel layout rules. Figma Design and Slides files belong to llllloc:tool-figma."
---

# llllloc:tool-figjam

How Claude works on his FigJam boards. Before the first `use_figma` write, load `figma-use` and `figma-use-figjam`: they hold the plugin mechanics. This file holds his rules. Figma Design and Slides files follow `llllloc:tool-figma`.

A board is a design job (16 Oct 2026, his words: "for these kind of task they are design task as well"). Every build or change on a board loads `llllloc:task-design` and `llllloc:task-research` with this skill, also inside a workflow thread. Why: Claude skipped the design rules on a board built in a workflow thread. His style choice wins: he likes a node map (shapes joined by arrows) for any flow, with text readable at panel size (node text 34 px or more).

Lessons: read `llllloc/4_Lessons/Programs/Figma/figjam-board-lessons.md` before the first write, and nothing else in that folder (16 Oct 2026, his words: read only the lesson that is needed).

## TOP RULES (16 Oct 2026)

1. Add, never delete. Never delete, hide or rewrite a section he made, or move it to another page without his word. Moving a section up to close a gap is allowed (LAYOUT). Why: the board is his record of every decision.
2. Every update is a new version. Clone the top-level section, edit only the clone, and name it `<NAME> v<n>` (the first update of an unnumbered section is `v2`). The old version stays where it is.
3. The color is the state. Every top-level section Claude builds or updates carries one state:

| State | Color at 44 % | When |
|---|---|---|
| JUST UPDATED | yellow `#FEF660` | Every section Claude builds or updates. It stays yellow until he says "good" or "archive". |
| FINAL | green `#85FE60` | On "good" or "archive" the yellow section turns green. One green version per subject. |
| PAST | red `#F84F4F` | The version a new one was cloned from, and every older version. |
| ARCHIVE | grey, as it is | The ARCHIVE section on the Archive page. Never recolor it. |

   - The colors look exactly as in his Figma files (his words, 16 Oct 2026): one paint on the section, `{type:'SOLID', color:<state>, opacity:0.44}`. Light text (white or grey) that sits straight on the section turns charcoal `#1E1E1E`, so it reads on the pale color.
   - Only top-level sections carry a state. Panels and rows inside keep their own fills.
   - A version he has not judged is never green.
4. Archive only on his word. "good": the yellow sections turn green. "archive": the yellow sections turn green, and every red version moves to the board's Archive page (his words, 16 Oct 2026), below the lowest item there, its layout kept. A board with no Archive page: ask him to add one (the plugin cannot make a FigJam page). Never move a section into or out of the archive without his word. To build on an archived section, clone it out. The original stays in the archive.
5. No stale yellow. A reply that leaves a yellow section ends with one line: the yellow sections by name, then "Good? Say archive and I turn them green and move the red versions to the archive." At the start of a later board turn, a yellow section from an earlier turn gets a one-line reminder before the work.
6. Report every color change and every move in the reply, one line each.

## LAYOUT

- A flow is one big map (16 Oct 2026, his words: "put everything in 1 map so i can see the big picture and no need to force each board to fit my 16 by 9 screen, I can scroll"). One connected node map, sized to its content, never split into 16:9 panels. Other boards: a panel may be 16:9, 3840 by 2160.
- No text overlaps. After every build, check each pair of text boxes in one section, and each text box against its section edge with 20 px to spare. A hit: fix it, then check again.
- Working sections line up on one left edge, x 0, top to bottom (16 Oct 2026). A new version goes 200 px right of the newest version in its row. Read every top-level box first. The new box plus 200 px on every side crosses none of them. No room in the row: 200 px below the lowest node.
- No gaps (16 Oct 2026, his words: "never leave a gap like this, always move things up so they fit nicely"). Rows sit exactly 200 px apart. After any archive, split, move or shrink, move every row below the hole up, in order, until each gap is 200 px.
- Match the board's style. Read the fonts, sizes and fills of one existing panel before building. The llllloc workflow board today: outer section `#161616`, panel `#1E1E1E`, row `#2C2C2C`, title Inter Semi Bold 88 white, subtitle Inter Regular 36 grey, row label 56, body 32 at 150 %.
- Section names are short, with no dashes. Use `·` to join parts.

## AN UPDATE, STEP BY STEP

```
- [ ] 0 llllloc:task-design and llllloc:task-research loaded
- [ ] 1 Board read with get_figjam (save the dump, read only the sections needed)
- [ ] 2 Each section to change cloned, placed, renamed v<n>
- [ ] 3 Only the clones edited
- [ ] 4 Overlap check empty, no gap over 200 px between rows
- [ ] 5 Colors set: clones yellow, their sources red
- [ ] 6 Screenshot looked at
- [ ] 7 Reply with the color lines and the yellow line
```

Step 4 finds a hit: fix, then run step 4 again. Step 6 shows a fault: fix, then go back to step 4.
