# VIDEO PROJECT BOARD LAYOUT

Part of `llllloc:tool-figma`. The section numbers are the ones every rule in the skill uses, so "section 1c" in any rule points here.

## 1c. VIDEO PROJECT BOARD LAYOUT (7 Oct 2026)

JOB: a video project's Figma page reads like the film, top to bottom, one row per VO line.
INPUT: the project's current script, VO column only: `*_CLAUDE/4_Story/SCRIPT-LATEST.md` (`llllloc:task-files-organize`, THE SCRIPT RULE).
STEPS:
1. TOP ROW: components, masters, design system, essential properties. Nothing else.
2. ONE ROW PER VO LINE, in film order, top to bottom. A section that holds two VO lines is split into one section per line: move the frames, never redraw them.
3. VO HEADER (his format, 7 Oct 2026): a BLACK section on the LEFT of each row, top-aligned with the row, its right edge 200 px left of the current section. The section name carries the scene: `VO SCENE 6-04 (6B)`. Inside, ONE white text: the VO line only, word for word (no scene name, no `VO:`, footage notes in brackets cut). a client Essentielle Bold 100, line height 118 %, left aligned. The text box is 1680 px wide and its height hugs the text, 60 px from the left and the top. The section is 1800 px wide and as tall as the text plus 120 px. A row with no VO says so in the same style.
3b. A PART OF THE VO ON ONE FRAME (7 Oct 2026): when a frame carries only part of the row's VO line, put that part UNDER the frame: the quoted VO words only, a client Essentielle Bold 30, black, centered on the frame, width hugs, 21 px under the frame's bottom edge. The section grows to hold it. Never above the frame, never with notes.
4. ONE ROW, UP TO THREE LINES (changed 7 Oct 2026). DESIGN LINE, left to right: the VO header, then the CURRENT section at x 0, then each newer revision to its right. Nothing else. UNDER LINE, 200 px under the tallest board of the design line, from x 0 to the right: his reference frames, the `LAYOUT OPTIONS` sections, the asset sections, his comment boxes. MOTION LINE: the animation (MOTION) boards, from x 0 to the right, 200 px under the under line, or 200 px under the design line when the row has no under line. Gap 200 px. 700 px from the bottom of a row to the next row.
4b. FRAMES IN AUTO LAYOUT, MAX 4 PER LINE (7 Oct 2026, changed 8 Oct 2026). A section's frames sit in ONE auto-layout frame, `FRAMES (auto layout, gap 100)`: horizontal, gap 100, wrap on at 4 frames per line, no fill, at 100, 100 in the section. Each frame and its VO part (3b) is one vertical auto-layout unit, gap 21, centered, no fill, named `<frame name> + VO`. Why: he moves a frame or duplicates one in between, and the rest follow (8 Oct 2026). The section hugs the auto-layout frame plus 100 px. His own line length on a frame row is the spec: keep it.
5. AN UPDATE duplicates the section to the right of the newest item in its row. Never below, never in a free spot elsewhere.
6. ON ARCHIVE: past versions move to the Archive page. The section's assets and every option developed for it stay on the working page, in the under line of its row. After a partial update on a green section, archive by swapping the screens (1b).
7. His comment boxes sit in the under line of the row they mark.
8. THE ARCHIVE PAGE USES THE SAME LAYOUT: one row per VO line, black VO header on the left, past versions left to right from oldest to newest from x 0, old options and assets in the under line, old MOTION boards in the motion line. A row for boards that mix several scenes sits under the masters row.
9. THE SCRIPT CHANGES (7 Oct 2026). Feedback may carry client comments as screenshots, and a comment may change the script. When it changes a VO line, update `Story/SCRIPT-LATEST.md` first, then the VO header text of that row on the working page, the same turn, in the step 3 format. A new VO line gets a new row in film order. A line the client cut keeps its row, and its header name ends ` CUT`. The designs do not change unless he asks. Report each changed row in one line: row, old words, new words.
OUTPUT: every node on the page sits in a row beside its black VO header, with no overlap.
RULES:
- Current at x 0 in every row, so the column reads down the film. Check: every current section has x = 0, every VO header ends at x -200.
- Never a node in a random spot. Check: every top-level node's top equals its row's VO header top, its row's under-line top, or its row's motion-line top.
- Motion never sits in the design line. Check: no section with ` MOTION ` in its name has the same top as its row's VO header.
- The Figma VO matches the script doc. Check: every VO header text equals the VO column of its row in `SCRIPT-LATEST.md`.
CHECK: run the overlap check on all top-level nodes. The list must be empty.

