# BUILD MECHANICS — fonts, styles, finding nodes, placing, layers, auto layout, text, plugin limits

Part of `llllloc:tool-figma`. The section numbers are the ones every rule in the skill uses, so "section 2, 3, 4, 6, 6b, 6c, 7, 8 or 10" in any rule points here.

## 2. THE FONT WALL

The plugin runs server-side and sees only fonts uploaded to Figma's servers. A font installed only on his Mac is invisible to it, and `loadFontAsync` fails.

- WORKS on an existing node: `x`, `y`, `fills`, `clone()`, `rescale(factor)`, `resize()`. `rescale` moves `x` and `y` too, so set the position after it.
- FAILS LOUDLY: `characters`, `insertCharacters`, `deleteCharacters`, `fontSize`, `textAutoResize`, `textAlignHorizontal`, `textAlignVertical`, `textCase`, `leadingTrim`.
- THE SILENT TRAP: `setTextStyleIdAsync` with an unloadable-font style applies, the node reports that font, and Figma draws a substitute at about half the correct width. Binding `fontSize` to a variable fails the same way. Never trust `fontSize` or `width` read back from such a node. A screenshot is the only check.
- To place a word the plugin cannot type: clone the nearest node in that face, rescale it, position it, and name the layer with the fix, e.g. `Number - change 02 to 03`.
- A FONT SWAP runs in his desktop app (24 Sep 2026): plugin clones the frames to a temporary page, full-screen computer use does Cmd+click one text, Edit > Select All With > Select All with Same Font, types the family in the font field. Background `app_click` cannot switch pages. Method: `llllloc/4_Lessons/Programs/Figma/how-to-swap-to-a-local-font-in-figma.md`.
- Display digits are not tabular. Hold ONE BOX WIDTH across a numbered series, not one font size. Align by `absoluteRenderBounds`.

## 3. STYLES

- Bind a fill to a paint style. `await node.setFillStyleIdAsync(id)` from `getLocalPaintStylesAsync()`. Same for text styles. A raw hex is a hundred edits later.
- Style names are flat. Never put a `/` in one: Figma reads the text before it as a folder, the picker searches the leaf only, and in Slides the folder does not surface.
- The picker lists THEME styles only. A style made by the plugin applies correctly and never joins a theme, so the picker cannot list it. No theme API is exposed. He manages styles in Design mode, Shift + D.
- Never truncate a style id. Ids are about 42 characters and end in a comma. A short id makes `getStyleByIdAsync` return null and `setTextStyleIdAsync` detach the style with no error.

## 4. FIND THINGS BY STRUCTURE, NEVER BY NAME

Slide names revert to numbers, a text layer's name follows its font size, and an instance he replaced is gone.

| Thing | Matcher |
|---|---|
| the plate | the RECTANGLE whose `fills[0].type === 'IMAGE'` |
| the title | the TEXT with the largest `fontSize` |
| a label | a 13pt TEXT, sorted by `y` |
| a body | the rest, sorted by `y` |
| a full-bleed slide | a RECTANGLE 1920 x 1080 with an IMAGE fill |
| an auto-layout slide | a FRAME named `CONTENT` with `layoutMode` set |

- Filter on `visible` too. A retired layer still answers a type query. Filter by `fontName.family`, `fontSize` AND `visible`, or a 13pt header label answers before the headline.
- A targeted edit must report a no-match. A loop that finds nothing still returns success. Count the hits and return the count.
- Edit from the file's state, not from your plan. Re-read the slide between passes.

## 6. PLACING NODES

- `appendChild` BEFORE `x`/`y`, every node, every level. A node parented after positioning lands 240px off. Fix the order, never add 240 back.
- Z-order is append order. On a rebuild, collect the finished stack bottom to top and `appendChild` each in order.
- A GROUP's children carry absolute coordinates. An INSTANCE's children are relative. Adding a group's offset to its child doubles the position.
- Read the band before you place anything in it. Before adding a rule, a label or a bar at a fixed y, list every node whose box crosses that band.
- An opaque box beats a z-fight. When a callout and a rule share a band, make the callout the last child of the slide.
- A cover may hold a picture parked off canvas on purpose. A safe-area sweep skips nodes outside the slide bounds and any word bled off the edge by design.

## 6b. ONE ELEMENT, ONE LAYER (27 Sep 2026)

Every element in a frame is ONE top-level layer, so he moves, hides or edits it with one click.

- An element is everything that moves together: a card with its glow plate, a button with its glow, its label and its quiet state, a connecting line with its two dots, a cursor with its click ring, an icon with its glass circle and its label.
- Build the wrapper first: `figma.createFrame()`, `fills = []`, `clipsContent = false`, sized to the element. Append it to the frame, then append the parts into it, bottom to top. The glow plate stays inside, behind the card.
- Name the wrapper by what it is: `card_A (plate + card)`, `approve_button (glow + label)`, `bridge_A (line + dots)`, `cursor + click_ring`.
- The background, the orb and the window stay one layer each, as before.
- Never leave loose parts at the top of a frame. A plate beside its card, a label beside its button: that is two layers where he wanted one.
- Z-order across elements stays a top-level decision: re-append the wrappers in order, bottom to top (section 6).
- THE TEST before handoff: list each frame's top-level children. Each one must be one whole element. Report the count per frame.

## 6c. CUTOUT FRAMES ARE TRANSPARENT, NEVER A KEY COLOR (8 Oct 2026)

When part of a frame is a cutout (a slash panel, a video hole, any area that a video or image fills later in the edit), leave that part empty. Set the frame fill to none and hide or remove any key-color layer. Never fill it with pink, magenta or any other key color. Why: he composites the frame over footage, and a key color reads as a mistake on the board.

- CHECK: no visible fill of `#FF00FF` (or any key color) in the frame or its children. A hit: clear it, then check again.

## 7. AUTO LAYOUT

`figma.createAutoLayout('VERTICAL', {name, itemSpacing})` gives a frame already hugging.

- `resize()` kills hugging. It switches that axis to FIXED. The instrument: a height equal to the dummy number you passed means it is not hugging. Set `primaryAxisSizingMode = 'AUTO'` as the LAST line of every build.
- Append to the auto-layout parent first, then set the sizing. `HUG` is valid only on the auto-layout frame or a TEXT child of one. `FILL` only on a non-absolute child of an auto-layout parent.
- `layoutSizingHorizontal` / `layoutSizingVertical` take `FIXED | HUG | FILL`. `primaryAxisSizingMode` / `counterAxisSizingMode` take `FIXED | AUTO`. Do not cross them.
- A wrapping TEXT needs `textAutoResize = 'HEIGHT'` and an explicit width.

## 8. TEXT MEASUREMENT

- Measure a typographic constant with a hidden probe TEXT in the real face, size and tracking: `width / characters.length`. Inter at -4% tracking is 0.431em per character, so `characters = boxWidth / (0.431 * fontSize)`. Other faces differ. Probe them.
- Place display type by its ink. `absoluteRenderBounds` is the ink, `absoluteBoundingBox` is the line box. Fit to a max width and a max height, never to a font size. To compare two faces, match ink height first.
- Cap every text box to its column. A cloned title keeps its old 1800px box even when the words are short.
- Never break a word. Probe the longest word at the target size, then `fontSize = floor(size * boxWidth / wordWidth)`.
- A predicted height is not a measured height. Build first, then read `frame.y + frame.height` against the bottom limit.
- `leadingTrim` is part of a spec. A 74pt heading reporting a height of 54 is CAP_HEIGHT trimmed. Copy it or the text sits low.
- A reference teaches layout, never type (9 Sep 2026). Take the grid, the numbering, the hierarchy, the accent and the white space. Keep his faces.

## 10. THE THINGS THAT ARE NOT REAL

- The big numbers on the grid thumbnails are Figma's own slide numbering, not layers. Before reporting a collision seen in a thumbnail, open the slide and read `visible` on the node you blame.
- `createPage()` throws in Slides. `get_metadata` does not work on Slides: validate with read-only `use_figma` scripts and `node.screenshot()`.
- A `PATTERN` fill cannot be set by the plugin: the type fails validation (23 Sep 2026). A texture (dots, halftone, grain) is a PNG through `upload_assets` onto a frame-size rectangle. Method: `llllloc/4_Lessons/Programs/Figma/how-to-build-a-glow-map-in-figma.md`.
- `vectorPaths` takes no arc command (`A`): the write fails, and everything the script made before it stays on the canvas half-built (30 Sep 2026). Draw a circle or an arc as cubic curves (`C`). Put a `vectorPaths` write in its own call, or early in the script, so a refusal leaves little behind, and on a refusal read the canvas before the retry.
- THE PLUGIN CANNOT ADD VIDEO (6 Oct 2026). `upload_assets` takes PNG, JPG, GIF, WebP and SVG only, and the Plugin API has no video import. He drops the clips into a frame himself (Fill, Video). Claude then reads and exports the frame (section 15).
- THE PLUGIN CANNOT CHANGE A VIDEO FILL (7 Oct 2026). Writing `fills` on a node that holds a VIDEO paint fails ("Setting VIDEO fills is not yet supported"). Reshaping such a node (new `vectorPaths` or size) stretches the video, because a CROP transform is relative to the box. Keep a video node's aspect, or ask him to set the fill to Fill in Figma.

