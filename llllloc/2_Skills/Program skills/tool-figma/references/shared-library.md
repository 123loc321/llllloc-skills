# THE SHARED LIBRARY

Part of `llllloc:tool-figma`. The section numbers are the ones every rule in the skill uses, so "section 14" in any rule points here.

## 14. THE SHARED LIBRARY (29 Sep 2026)

Everything he wants to reuse across projects lives in three library files in his `Library` team folder. Take every link from `llllloc/3_Project maps/Project map_Creatives.md`. Never build a Figma URL from an ID.

| File | Holds | Pages |
|---|---|---|
| `llllloc_LIBRARY` | Review tools: the Comment box, status tags, version labels | `Review Tools` |
| `llllloc_LIBRARY_UI` | The design system: colors, type, spacing, effects, buttons, panels, icons | `Foundations`, `Buttons`, `Inputs`, `Panels`, `Icons` |
| `llllloc_LIBRARY_VISUAL` | Backgrounds, textures, glows, shading, graphic elements | `Backgrounds`, `Textures`, `Glows and Shading`, `Elements` |

"SAVE IT TO THE LIBRARY" RUNS THESE STEPS:

1. Pick the file and the page from the table. A new kind of item gets a new page in the file that fits. Never a fourth file unless he says so.
2. Read the source node in full in ONE read (0b): tree, fills, strokes, effects, blend modes, masks (`isMask`), `relativeTransform` of each part, full `vectorPaths`, fonts. Screenshot the source.
3. REBUILD IT. The plugin cannot copy a node from one file to another. Rebuild it part by part as a COMPONENT from the real numbers. Set each part's `relativeTransform`, minus the source group's offset. A flipped or rotated part keeps its matrix. A mask group: build the parts, `figma.group([...])` with the mask shape first, then `mask.isMask = true`.
4. Every word he will change becomes a TEXT component property (`Label`, `Note`). A label centered in the source stays centered: a fixed-width text box the width of the component, `textAlignHorizontal = 'CENTER'`.
5. Name it `<Kind>_<Name>` (`Button_Glow-Blue`, `Comment`). No `/` in the name. Put one line in `description`: what it is and where it came from.
6. Screenshot the component beside the source screenshot. Same look, or fix it before the reply.
7. Add a LINKS row for the source file he pasted (section on adding a link in `llllloc/3_Project maps/Project map_Creatives.md`).
8. The reply says the file, the page, the component name and the property to edit.

WHAT ONLY HE CAN DO. The plugin cannot publish a library, cannot move a file between folders and cannot switch a library on in another file. The reply ends with his one step: open the file, Assets, the book icon, Publish. Figma will not publish a file that holds no component or style.

A NEW LIBRARY FILE goes straight into the `Library` folder: `create_new_file` with that folder's `projectId` (in its LINKS row). A file made without it lands in Drafts, and moving it is his job.

KEEP THE BASE IN ONE PLACE. Colors, type styles and effect styles live in `llllloc_LIBRARY_UI` `Foundations`. The other two files use them from there. The same color in two libraries drifts.

Deeper cases live in `llllloc/4_Lessons/Programs/Figma/`.

