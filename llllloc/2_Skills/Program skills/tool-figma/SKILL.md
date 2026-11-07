---
name: tool-figma
description: "How Figma behaves when Claude drives it through the plugin API, Slides and Design files. Runs when the user types its name or when /llllloc:router picks it for one request. Never on its own. Owns duplicate-first editing, section state colors, the Figma link file, the account check, parking a slide, the font wall, style binding, finding nodes by structure, the grid and rows, the row-by-VO board layout for video projects, node placement, one element one layer, auto layout, text measurement, picture justification, the JPG export he calls with `export`, a video frame sent to his Premiere timeline, the cutout export of a frame with a video placeholder, and saving a reusable item to his shared library. Craft lives in llllloc:task-design."
---

# llllloc:tool-figma — the mechanics

Everything that bites when driving a Figma Slides or Design file through the plugin API. Craft lives in `llllloc:task-design`. A job's look lives in that project's `*_CLAUDE/3_Art Direction/ART-DIRECTION.md` (the lock) and `*_CLAUDE/3_Art Direction/DESIGN-SYSTEM.md`. Runs only when he types its name or `/llllloc:router` picks it. Before any `use_figma` call, load `figma-use`, plus `figma-use-slides` for a Slides file.

## READ ONE FILE FOR THE JOB

The sections in this file (0b, 1, 1b, 11) apply on every Figma turn. Every other section lives in one file. Read the file in full before the first write. Why: a file opened only in part hides the rule that bites.

| The job | Read |
|---|---|
| Any build or edit that writes nodes or text | `references/build-mechanics.md` (sections 2, 3, 4, 6, 6b, 6c, 7, 8, 10) |
| A video project page: rows by VO line, VO headers, under and motion lines, archive | `references/video-board-layout.md` (section 1c) |
| A Slides file: park a slide, the grid, rows, picture rows | `references/slides-file.md` (Slides park, sections 5, 9) |
| A file refuses access, or the first job on a Figma file (the link file) | `references/access-and-link-file.md` (sections 0, 12) |
| He types `export`, or a frame goes to his Premiere timeline | `references/export-and-premiere.md` (sections 13, 15, 15b) |
| "Save it to the library" | `references/shared-library.md` (section 14) |

Lessons: list `llllloc/4_Lessons/Programs/Figma/` and read only the file whose name matches the job. No match: read nothing (16 Oct 2026, his words: read only the lesson that is needed).

## 0b. THE FAST PATH ON AN EDIT TURN

A Figma edit ships in one to two minutes (29 Sep 2026). It takes about 8 to 10 tool calls. Past 15, stop and find the waste.

1. The start stays. Run `llllloc:project-creatives` section 1 in full, the handoff read included (29 Sep 2026).
2. One read. A single read-only script dumps every target frame in full before any write: the tree to the text layers, fonts and their styles, auto-layout settings, leader paths, and which font styles load. Never a second read to fill a gap. Read again only after a failed write.
3. Build, then look. Build from the read, take the screenshot, fix what it shows. Do not work out every coordinate before the first build.
3b. Check the parts before the picture (30 Sep 2026). A screenshot at full frame width hides a 5 px fault, and the page overlap check sees only sections. In the same script as the build, print three lists, each must be empty: (1) children of one head row whose vertical centers differ by more than 1 px, (2) sibling buttons in one row with different widths or heights, (3) two parts inside one panel whose boxes cross. He caught all three by eye on MOTION v3 to v6: an icon over the ball lane, the timeline controls 5 px low, two strip buttons at two widths.
4. A failed call: read only the nodes that call touched, then retry once. A union with more than 100 children takes no `appendChild` (it times out): make a new union beside it and copy its fills, strokes, stroke weight and effects.
5. KEPT, on his word (29 Sep 2026): fixes that make the design right though he did not name them, the section color step (1b), the link file check (12), full-size screenshots, and the full reply with its self-review.

## 1. DUPLICATE FIRST, EDIT THE COPY. NEVER EDIT IN PLACE (23 Sep 2026).

Every update starts with a duplicate: a rebuild, a recolor, a text edit, a nudge. This includes a version Claude built earlier in the same chat. The original stays untouched and visible.

Design file:

```js
const dup = original.clone();
figma.currentPage.appendChild(dup);
dup.y = original.y;                             // same row
dup.x = rightEdgeOfRow(original) + 200;          // right of the newest item in its row (1c)
dup.name = original.name.replace(/_v(\d+)[A-Z]?/, (m, n) => '_v' + (+n + 1));
```

- Rows, in every Figma file, video or not (30 Oct 2026). One row per piece. A new version or update goes 200 px right of the newest item in its row, top-aligned with the row: oldest left, newest right. Two options on one round become `_v2A` and `_v2B`, side by side. A board paired with one version (its mockup, export or test) goes 200 px under that version, same x. Only a new piece with no row yet starts a row, 700 px under the lowest row, at x 0. Never stack a version under the last one. A video project adds the VO headers and lines of 1c.
- No overlap (29 Sep 2026). Before placing a new section, frame or clone, read the box of every top-level node on the page, parallel chats' work included. The new box plus 200 px on every side crosses none of them. Something in the way: go further right in the same row. Never move someone else's section to make room.
- Check the place (30 Oct 2026). Read the page again. The new top equals its row's top (a paired board: its version's bottom plus 200), nothing in its row sits right of it, nothing overlaps. A fail: move it, check again. Report it in one line.
- The name carries the version and the change: `MAP_Dark_7-Countries_v3A_Halftone-In-Countries`.
- Section names are short (7 Oct 2026). A section (board) name is `<SCENE> <KIND> v<n>`, plus ` - ` and two to four words only when two sections in a row need telling apart. 45 characters at most. Example: `SCENE-2B STORYBOARD v3`, not `SCENE-2B STORYBOARD v3 - first 4 cards born in the middle one by one, then...`. The detail goes in the reply and the handoff, never the name. Frame names keep their own rule above.
- A layer retired during a build gets `visible = false` and a name ending `-retired`.
- Retired layers in a new version may be deleted (27 Sep 2026). In the newest version, delete every hidden `-retired` layer inside its frames: the earlier version still holds them. Filter the list first, then remove: skip a layer inside an INSTANCE (the plugin cannot remove it) and a layer whose parent is already on the list. Never delete a layer from an older version, and never delete a visible layer. Report the count.
- The archive moves only on his word, both ways (27 Sep 2026). A superseded version stays on its working page. Never move a version, a component or a section INTO an Archive page, and never move one OUT of it, unless his message says to. To build on an archived version, clone it and place the clone on the working page. The original stays in the archive. Name what you moved in the reply.
- "ARCHIVE" means every previous version (27 Sep 2026, changed 7 Oct 2026). When he says "archive" with no target, move every version older than the newest one in each row to the Archive page, into its row there (1c step 8). The `LAYOUT OPTIONS` sections, the assets and his reference frames stay on the working page, in the under line of their row (1c). `_SYSTEM` and the component sections stay in the top row. A Figma call keeps the page it last switched to: switch back to the working page before you read or place anything there.
- LINE UP ON ARCHIVE (30 Oct 2026). After the moves, tidy the working page: every row starts on one shared left line (the row start, x 0), rows stack top to bottom 700 px apart, and the boards left in each row close up to 200 px gaps, the paired boards under their versions. Nothing sits left of the line or floats between rows. Check: read the page, every row's first left edge equals the line and every gap is 200 or 700. A fail: move it, check again. Report what moved in one line.
- ARCHIVE AFTER HE PICKS ONE OPTION, "KEEP THE OTHER OPTIONS HERE" (6 Oct 2026, changed 7 Oct 2026). The picked frame moves out of the `LAYOUT OPTIONS` section into its own new top-level section, named with the next version, green at 44 %, placed at x 0 in its row (1c). The old version section turns red and moves to the Archive page, into its row there. The `LAYOUT OPTIONS` section stays in the under line of the row. Shrink it back to the height its frames need. Report each move and each color in the reply, one line each.
- "UPDATE" means read his Figma comments first (27 Sep 2026). He may type only "update". On "update" with no other instruction, scan the newest version before building, then follow every note found: (1) comment boxes (`Comments` instances) at section level and inside frames, (2) red-stroke vectors he drew inside frames, (3) any card, chip or icon lying outside its frame at section level, (4) his own edits on a frame since the last version, which are the spec for the next version. No notes found: say so in one line and ask what to update.
- His comment boxes stay on the version he marked (27 Sep 2026). When he leaves notes on a version (yellow boxes or any comment layer), make every change on the new copy, then remove those comment layers from the new copy only. The version he marked keeps them as the record of what he asked for.
- His own edit is the spec (6 Oct 2026). A layer he hid or a text he moved on a frame stays as he left it in every copy. Never turn a hidden layer back on.

### 1b. THE SECTION COLOR IS THE STATE (28 Sep 2026)

Every section on a working page carries one fill that says its state. Read the fill off the node before you set one.

| State | Fill | When |
|---|---|---|
| JUST UPDATED | yellow `#FEF660` at 44 % | Every section Claude builds or updates. It stays yellow until he says it is good, or says archive. |
| FINAL | green `#85FE60` at 44 % | On "good" or "archive", the yellow section turns green. Only one green section per part. |
| PAST | red `#F84F4F` at 44 % | The section a new version was cloned from in full, and every older version. |
| LAYOUT OPTIONS | dark grey `#444444` | Every `LAYOUT OPTIONS` section. Never recolor it. |
| COMPONENTS | white, as it is in the file | `_SYSTEM` and component sections. Never recolor it. |
| MOTION FINAL | violet `#A78BFA` at 44 % | A MOTION (animation) section follows every rule in this table and in 1b, the same as a design section. Only its FINAL color differs: violet where a design section is green (8 Oct 2026). Yellow, red, the 33 % dim and the archive swap all apply. |
| VO HEADER | black `#000000` | The VO line on the left of each row (1c). |

- 44 % fill opacity (28 Sep 2026). Set it on the paint, not on the section: `{type:'SOLID', color, opacity:0.44}`. The section's own opacity stays 100 %.
- Every update is a new section (28 Sep 2026, changed 8 Oct 2026). Any update, on a section of any color, builds a NEW yellow section, 200 px right of the newest item in its row (1c). Never build inside the old section, and never put a yellow board inside a green section: he could not read it as an update (8 Oct 2026).
  - A note on a yellow section: clone the whole section, every screen, even when only some changed. The old yellow section turns red.
  - A note on some screens of a green section (8 Oct 2026): put only the updated screens in the new section. The green section stays green, and each replaced screen in it goes to 33 % opacity. Why: green holds the approved film, and the dimmed screens show which screens the new section replaces. Every later update on that yellow section clones the whole yellow section (rule above). ON "ARCHIVE" (8 Oct 2026): move the newest screens into the green section, each into the place of the screen it replaces, with its VO words under it. Move the replaced screens, back at 100 % opacity, into the emptied section. Rename that section `<name> v<old> - replaced screens`, turn it red, and move it to the Archive page, into its row there. Rename the green section to the newest version. Why: one green section holds the whole current film, in film order.
  - A NOTE ON THE WHOLE DESIGN, any color: clone the whole section. The old section turns red.
- After "archive", the section left on the working page is green (violet for MOTION).
- A version he has not judged is never green or violet.
- No stale yellow (7 Oct 2026). Yellow means waiting for his word, never a resting state. Every Figma reply that leaves a yellow section ends with one line: the yellow sections by name, and "Good? Say archive and I turn them green and archive the past versions." At the start of any later Figma turn on that file, if a yellow section from an earlier turn is still there, remind him in one line before the work.
- Report every color change in the reply, one line.

Slides file: park a slide, never hide it. `slide.visible = false` takes a slide out of the grid. Read `references/slides-file.md` before any change to a Slides file.

Video project board layout (1c): read `references/video-board-layout.md` before you place, duplicate or archive a section in a video project.

## 11. THE BUILD ORDER

1. Read the project's newest `DesignSystem_<Name>_V<N>.md` first (older project: `ART-DIRECTION.md`), then `DESIGN-SYSTEM.md`. Its `## Master and parts` names the master version: copy parts from it, never from an archived version. No design system yet: `llllloc:task-design-system` runs first (17 Oct 2026). If he pointed at a slide he edited, that slide is the spec: copy its real numbers and fills.
2. Confirm the styles exist. Create only what is missing, with flat names.
3. Duplicate every frame or slide you will change (section 1). On a Design file with part sections, build the next version as a new yellow section first, to the right in its row (sections 1b, 1c). Edit only the copy. The original stays visible.
4. Build. On a rebuild, move and restyle the nodes already there.
5. Wrap every element in one layer (section 6b). Set z-order last by re-appending the wrappers bottom to top.
6. Sweeps: measure on every body, word fit, text under block, nothing crosses a rule, safe area, ink overlap, `visible !== true`.
7. Screenshot the worst case of each archetype and look: brightest plate, longest body.
8. Set the section colors (section 1b), each fill at 44 %. Yellow on the new section. Red on the section it came from, except when it was green and only some screens changed (1b): it stays green, and the replaced screens go to 33 %.
9. Return node ids from every script.
10. Check the Figma link file is in the project folder (section 12).

A build ends without an export. The JPG export runs only on his `export` (section 13). The video export runs only when he asks for the video or says to put the frame on his timeline (section 15).

A layout direction ships as OPTIONS: two or three named options per archetype, each on a duplicate, all in one `LAYOUT OPTIONS` row, each tagged. He picks before anything rolls out. Work he cannot see is work that did not happen: every park step, and every archive move he asked for, ends in something visible, and the reply says where to look.

