# Attached references and tags

Read in full before the first prompt line whenever a picture, video or audio file is attached, or the prompt tags one (16 Oct 2026, moved out of SKILL.md). Section numbers match SKILL.md.

## 5. AN ATTACHED PICTURE: POINT AT IT, DO NOT DESCRIBE IT

The plate carries the detail. Every sentence that describes what the plate shows drags the result toward the words. For anything the model can see, write three things and stop:

1. WHICH plate, by its tag (section 6).
2. WHAT to take from it, in one clause: the cut, the garment, the object, the grade.
3. WHAT NOT to take, named one by one: not the face, not the color, not the background.

- A garment on a plate gets no shape words. Banned while the plate is attached: cut, fit, volume, length, neckline, collar, closure, seam, hem, weave, sheen, drape, texture. Write the plain noun and say: copy the garment from the picture, not from any words.
- A removal is positive and short. Name the thing gone and the bare surface under it, one line each.
- Still written out, because no plate carries it: what contradicts the plate (with the hex), what the render got wrong (with a measurable test), the lock list on an edit, what the removed element was hiding, geometry the plate cannot show.
- The test is a count. Each plate's subject is described in one place in the whole prompt. Cut every repeat, including the ones in the LIGHT and CAMERA blocks.
- When a second version also misses, look at the render beside the plate before writing a third. Fetch the render's own URL (`creations_get` or `creations_wait` on Magnific), download it, look. No render: ask for that one picture.

## 6. TAGS: THE PLATFORM DECIDES (7 Oct 2026)

Each platform reads its references in its own way, so the platform sets the tag shape.

| Platform | Tag | Which picture is which |
|---|---|---|
| ComfyUI | `@Image 1`, `@Image 2`, `@Video 1`, `@Audio 1` | Socket order: `image_1` is `@Image 1`. The Seedance node sends the images in socket order and does not rewrite `image_1` in the prompt. |
| RunningHub | `@Image 1`, `@Image 2`, `@Video 1`, `@Audio 1` | Upload order. |
| Magnific | `@file name`: the node name on the board, extension dropped | `llllloc:tool-magnific` rule 2. |

- No platform named in this thread: before writing, ask one question: "Which platform: ComfyUI, RunningHub or Magnific?" Never guess. The answer holds for the thread until he names another platform.
- A platform not in the table: ask him its tag form, use it, and offer to add the row.
- Magnific, a board screenshot attached: the exact name printed above or beside each picture or generator node is that picture's tag. The current screenshot overrides older handoffs, aliases and file names. Never carry an older tag forward unless it is printed in the current screenshot. Ignore the screenshot's own file name, dimensions and controls. Two labels could fit one picture: ask one question.
- Magnific, an unnamed upload: give it a short name in the `llllloc:tool-magnific` rule 3 shape and report it in one line.
- A ComfyUI or RunningHub reply names the order in one line: `@Image 1` = which picture, `@Image 2` = which picture.
- Only assets the target AI receives get a tag. Context-only files and documents shape the prompt and are never tagged.
- The check: every tag in the prompt has the platform's shape, and no prose positional word ("reference image 1", "the second picture") stands in for a tag. One miss means the rule did not run.
