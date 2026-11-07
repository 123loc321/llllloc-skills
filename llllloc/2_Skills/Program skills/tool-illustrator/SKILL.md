---
name: tool-illustrator
description: "How Claude drives Adobe Illustrator on his Mac through the Synthetic Illustrator MCP connector. Runs on its name, or when /llllloc:router picks it for any Illustrator job."
---

# llllloc:tool-illustrator

Claude drives his live Illustrator through the Synthetic Illustrator MCP connector. Tools are named `mcp__illustrator__<tool>` (31 Oct 2026). He reviews in Illustrator. This skill holds universal Illustrator knowledge only (10 Oct 2026). A job's look lives in its `*_CLAUDE/3_Art Direction/` files. A rule changes only when he says so in words.

## TOP RULES
1. Never edit his file in place. Work in a new document (`create_document`), or duplicate the artboard and edit the copy, with the original kept beside it. Why: the connector changes his open file live, and his unsaved edits sit in the same file.
2. No save unless he says so. `save_document` only on his word, with a path built from the project folder listing. Never save over a file he has not named.
3. Every shape gets an explicit fill and stroke. `set_stroke_color` with no color removes the outline. Why: a new shape takes the default outline.
4. Look before you reply. `export_png`, then open the file with Read. An "ok" proves nothing: Illustrator silently ignores an unknown live effect.
5. One failed call, one stop. Tell him what to click (CONNECTOR DOWN). Never fire a burst of retries. One exception: "License server unreachable" gets one retry, because IPv6 drops on his network (31 Oct 2026).

## START OF EVERY ILLUSTRATOR TURN
```
- [ ] 1 Connector tools loaded in one ToolSearch
- [ ] 2 Connector answered, document named
- [ ] 3 Target artboard or new document chosen
- [ ] 4 Notes and job files read
```
1. Load every tool the job needs in one ToolSearch call (`select:` with a comma list).
2. Probe with `il_healthcheck`, then `get_document_info`. It returns the open file's name, path, artboards, color space and ruler units. `connected: false` or an error: stop and send connector down. Go back to step 2 only after he says it runs.
3. Name the file and artboard you will touch in the reply. His file: duplicate first (TOP RULE 1).
4. Read `llllloc/4_Lessons/Programs/Illustrator/ILLUSTRATOR-MCP-NOTES.md`. It holds every dated lesson. First Illustrator turn of a job: read the job's art direction files.

## CONNECTOR DOWN: WHAT TO SEND HIM
Three lines, no more:
- Illustrator is open with a document.
- Window > Extensions > Synthetic Illustrator MCP is open and says "Bridge active". The menu is grey: quit Illustrator and open it again (31 Oct 2026).
- Restart the Claude app. Tell me when it runs.
## SETUP FACTS (31 Oct 2026, checked live)
- Connector: Synthetic Illustrator MCP, server 0.5.1, panel 0.5.0, 138 tools, account <e-mail>, from $15 a month. It replaced Design Bridge by IE3, his words: "not so good". Server name `illustrator` in `claude_desktop_config.json`.
- The server updates itself through its launcher. The panel talks to it on port 41220.
- Synthetic Setup.app crashes on macOS 27 (bundled Node). To install or repair, run `node runner.mjs` from the app's `Contents/Resources/engine` folder with `NODE_USE_SYSTEM_CA=1`, then open the printed `SYNTHETIC_URL` in Ego Lite. He types the email code himself.
- The licence key never goes in this repo, a file he did not ask for, or a chat reply.
- Guides for Claude: `il_help` with a topic (documents, items, paths, color, text, effects, symbols-masks, export, scripting, recovery). Read only the one the job needs.
## DRAWING
- Coordinates: points from the top-left of the ACTIVE artboard, X right, Y down, in every document. Ruler units never change this.
- Point text: `y` is the BASELINE of the first line (seen in the 31 Oct 2026 test).
- `font` in `set_text_style` is the PostScript name, such as `Helvetica-Bold`. `list_fonts` shows only the first 200.
- RGB colors are 0 to 255.
- Name every object you create (`name`). Items are found by name, so keep names unique.
- Many objects of one kind: build one, then `duplicate_item` and edit the copy.
- Nothing removes a live effect. Keep an untouched copy with `duplicate_item` first.
## EXPORT
- The output folder must exist first. Create it with `mkdir -p`. `ls` a `/Volumes/` drive first. Not mounted: stop and tell him.
- Folder and file names come from `llllloc:task-files-organize`. Never `4_RENDERS/`.
- `export_png` and `export_jpg` cover the artboard: `scale` is a percent, `artboardIndex` picks one and makes it active. Art outside the artboard is cut. `transparent: false` for an opaque PNG.
- `export_svg` has no options. `export_pdf` uses default PDF options. After it, `get_document_info` shows the name the document now has.
- Delivery (29 Oct 2026): export straight into the job folder, then `llllloc:task-sending-files` (a file card plus the Mac path).
## KNOWN LIMITS (from `il_help`, 31 Oct 2026)
- Live effects: shadow, feather, round corners, offset path and the `apply_named_effect` list only. No blur, noise, grain, Warp or 3D. Say so and offer the closest look.
- `apply_live_effect_raw` only with exact values from him.
- The drop shadow is always black. Effects are tested by the maker on simple shapes only.
- Effects on groups, text and placed images are unverified. Export and look.
## REPLY
Lead with done or not done. Name the document and artboard to open. State every default you picked that he did not give (size, color mode, font). Flag what was not checked. Remind him what is unsaved.