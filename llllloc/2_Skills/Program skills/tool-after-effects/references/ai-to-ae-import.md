# Import Illustrator layers into After Effects

Learned on a client (1 Nov 2026): 77 boards built by 7 sessions on one project. Read before the first import of a job. A job's look and colour table stay in the job's `AE-BUILD.md`.

## How he does it by hand
He pushes each artboard with Overlord. Vectors arrive as shape layers, text as live text, heavy art as a 2x PNG at about 50%. He then names each part, removes extras, and adds `TEX ▸`, `RIG ▸`, `CAM` and `VOX_JITTER`. Overlord lost the halftone dots, his native .ai import kept them. Claude cannot press the Overlord button, so Claude uses a route below.

## Pick a route
| Route | When | How |
|---|---|---|
| A, split and import | Most boards, one session at a time | Split the .ai per artboard, one layer per moving part. Import the .ai as a comp. Run Create Shapes from Vector Layer on each layer |
| B, read paths and build | Art far past the frame, or many sessions at once | A script reads the paths from Illustrator and builds shape layers. No crop, true colours, any object split |

Create Shapes takes over the viewer: `app.findMenuCommandId`, one layer selected, its comp open. That is unsafe while other sessions drive After Effects. Scripts that worked: `*_CLAUDE/7_Motion/Lanes/` in `261031_a client_a client` (Act 1 `ai_dump.jsx`, `board_lib.jsx`).

## Steps
1. Split. One `_split.ai` per artboard. One layer per object that moves on its own. A row of repeated items gets one layer each, so each can enter alone.
2. Art past the frame. Import crops at the artboard. Grow the working artboard (600 to 1400 pt per side), import, set the comp to 1920 x 1080, then move every layer back by the growth. A board too close to the canvas edge fails: move the art first.
3. Colours. The .ai may carry a monitor profile, and After Effects takes raw numbers, so blue and red go dull. Create Shapes numbers can differ from the .ai too. Measure a table against the design render, and map every fill.
4. Heavy art goes to PNG at 2x, at 50% in the comp: stickers, maps, torn paper, colour emoji. Illustrator PNG numbers are raw, so run `sips -e doc.icc`, then `sips -m sRGB`.
5. Text. Rebuild it live at a rough spot, export a frame, measure the offset against the design, and move it. Rotation is the .ai matrix, atan(B/A), negated. Set `autoLeading = false`. Use the exact font name. `HiraKakuStdN-W8` falls back silently, `HiraKakuStd-W8` works.
6. Name each part, then add the rig the job's `AE-BUILD.md` asks for.
7. Check with jitter off: the board against the design render by pixel diff, under about 2.6% off, text within 1 px. `saveFrameToPng` writes 16-bit, so divide by 257 in a compare.

## Traps
- Create Shapes leaves Position separated: set `dimensionsSeparated = false` before `setValue`.
- Create Shapes drops text inside groups, and turns some clip groups into a grey frame. Find a path over 3000 px wide and remove it, or export that part as PNG.
- Compound paths can lose holes: set Fill Rule to even-odd. A country map went to PNG.
- Illustrator walks over 10,000 paths too slowly for one call, and many edits on a board with texture dots held it 13 minutes. Both block the bridge for every session. Export by item.
- `open_project` fails on a path with `*`: use `app.open(new File(path))`.
- `copyToComp` may not land on layer 1: find the copy by name. It refuses a parented layer inside an undo group.
