---
name: tool-motion-app
description: How Claude drives his own MOTION app (Mac motion-graphics app, MOTION connector) - boards and their state colors, reusable master cards, media paths, building films as files, checking and rendering ProRes for Premiere. Use when he asks to build, edit, duplicate, render or reuse anything in MOTION or the motion app. Runs when /llllloc:router picks it.
---

# llllloc:tool-motion-app

The mechanics of his MOTION app. Motion craft (look, timing, sync, the bar) lives in `llllloc:task-motion`. This skill says how the app behaves and how to work in it. Every rule here was learned on a real job (9 Oct 2026, a client Scene 2 country cards).

## TOP RULES

1. Film and board on every call (MOTION V0.21, 9 Oct 2026). Pass `film` (the .motion full path) and `board` (artboard id or name) on every MOTION tool call except `motion_status`. The work then runs in a hidden worker for that film: his screen never switches, other chats work on other films at the same time, and two chats can share one film on two artboards. Why: on 9 Oct 2026 a second chat switched the app's film three times mid-build. A call without `film` works on his screen: never send one unless he asks to see it there. One artboard per chat: two chats on one artboard, the last save wins.
2. Check the version. `motion_status` must say `parallel: true` (V0.21 or newer). No `parallel`: the old app is installed, so stop and ask him to install `MOTION-V0.21-INSTALLER`. "#" paths (CREATIVE #1) load pictures from V0.21. Older app: media goes to `~/Movies/MOTION/media/<FILM-NAME>/`.
3. BOARDS CARRY THE STATE COLOR, like Figma sections (`llllloc:tool-figma` 1b). Every board sits in a group, and the group color is its state:
   - Yellow: just built or updated, waiting for his word.
   - Green: final, after he says good or archive. One green group per piece.
   - RED: a past version.
   An update is a new board (`motion_board duplicate`), placed right of the newest board in its row, in a new yellow group. Never edit a green board in place. The board it came from turns red. Every reply that leaves a yellow group names it and ends: "Good? Say archive and I turn them green and the past versions red."
4. Reuse before build. He wants every element built once, then reused fast. Before a new card, title or text box, read the MASTERS list in the project's `**_MOTION/_STATE/MOTION-STATE.md`. A close master exists: duplicate its board and change only the Content slots. None exists: build it as a master (MASTER RULES below) and add it to the list.

## MASTER RULES

A master is one element any later job can reuse in a minute.
- One code layer holds the element. Every word, font, color and size he may change is a Content slot (`slots` on the layer). Every move is measured from the words, so new text keeps the animation.
- A picture that changes per variant (a country map, a logo) is its own image layer, named `<WHAT> (swap picture in Content)`, above the card. Its size and place come from the same numbers as the card.
- One board per variant, named `<SCENE>-<NN>_<SUBJECT>_<KIND>_V<N>`, for example `SCENE-2-01_EGYPT_CARD_V1`.
- Transparent board (`bg ""`) when it goes over footage in Premiere.
- Add the master to MASTERS in `MOTION-STATE.md`: film path, board, what the slots change.

## BUILD A FILM AS A FILE

A code layer is often 8,000 characters or more. Do not paste it into `motion_scene_set` or `motion_layer_set`: it costs the minute and breaks easily.
1. Write the JS into the job folder on the Mac and check it parses (`node -e "new Function(src+';return draw')"`).
2. Build the film JSON with a script: `{v:1, name, w, h, fps, dur, bg, fxShared:[], rev:1, audio, layers:[...]}`. Each layer has `id, name, type, in, out, hidden, locked, fx, keys, props`, and a code layer has `slots`. `layers[0]` is the TOP layer.
3. Write it straight into the job folder (a rewrite overwrites it), then `motion_project open` that path.
4. Every later call carries `film` and `board` (TOP RULE 1).
5. After any later code edit: rewrite the file, open again. Small value changes go through `motion_content_set` or `motion_layer_set`.

## THE CODE LAYER

- `draw(g, t, p, PIXI, ctx)`. `g` is emptied every frame. `t` is the layer's own time. Wrap every filter in `ctx.temp(...)`.
- Errors show in `motion_snapshot` and `motion_scene_get` as `Errors: {layerId: message}`. An error stops the draw at that line, so everything after it is missing. Read the error before you tune a look.
- PIXI v8 traps found: `TextStyle.toFontString` does not exist. For a letter's top use `PIXI.CanvasTextMetrics.measureText(ch, style).fontProperties.ascent` minus the cap height from a canvas `measureText('H').actualBoundingBoxAscent`.
- A gradient fill or stroke: draw strips or short segments colored by position. It is safe in every PIXI build.
- `motion_scene_get` returns 60,000 characters or more on a film with code layers. Read the saved result with a script, never in full.

## KEYS FROM FIGMA

- MOTION easing sits on the key it LEAVES: `e` shapes the run into the NEXT key. Figma easing sits on the key it ARRIVES at. When you port a Figma track, move each easing one key back.
- Easing names: `smooth`, `out`, `in`, `inout`, `flat`, `snap`, `linear`, `hold`, or `[x1, y1, x2, y2]`.
- Figma pictures with real alpha (maps, icons with glow): the white and black two-pass export in `llllloc/4_Lessons/Programs/Figma/how-to-export-a-transparent-overlay-from-figma.md`. A plain Figma PNG export comes out opaque.

## CHECK

1. `motion_sheet` at 9 to 12 times across the board, and `motion_snapshot` at the moment he should see first.
2. A transparent board can show an old frame behind it in a sheet. Check with `bg "#000000"`, then set `bg ""` again before the render. Note it in the reply.
3. Side by side with the Figma frame (`llllloc:task-motion` R35): glow, stroke and color within 15 levels.
4. Save (`motion_project save`). Then `motion_project open` with `show: true`, and seek to the first moment he should see (`motion_seek`). Why: he cannot see a film opened out of sight (9 Oct 2026). Check: `motion_status` names the film as the open project.

## RENDER FOR PREMIERE

Only on his word, or when the job is a file for his edit (`llllloc:task-motion` R32).
- `motion_render kind prores` gives ProRes 4444 with alpha. Premiere opens it with no extra steps. `layers true` gives one transparent file per layer.
- One file per board: `motion_render` with that `board`.
- Path: the job's `1_VISUAL ASSET/*From Claude/<SCENE>/`, named `Claude_<project>_<BOARD-NAME>.mov`. Never `4_RENDERS/`.
- After the render: `ffprobe` the file for size, frame rate, length and `yuva444p` (alpha). It reaches him as a file card plus its full path (29 Oct 2026, his ok).

## THE REPLY

What changed, the film path, the board to look at, the yellow groups, the least-sure choice. No video in the chat.
