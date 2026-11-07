---
name: tool-capture-one
description: "How Claude drives Capture One on his Mac through the c1 plugin (kiri11/c1cmd) for llllloc and the studio: the document check, the Catalog backup, the scratch test for a new build or a new action, final exports, and the traps found on his Mac. Sits beside the plugin skill c1:edit: c1:edit owns the editing craft, this skill owns how Capture One and c1 behave here. Runs when the user types its name, or when /llllloc:router picks it for one request: any job that reads, edits, grades, crops, rates or exports photos in a Capture One Catalog or Session. Never writes to a document he did not name, never deletes, never updates Capture One or c1, and never runs a final export without his word."
---

# llllloc:tool-capture-one

Claude reads and edits his open Capture One document with the `c1` program. He reviews in the Capture One window. `c1:edit` holds the editing loop, so load it for every edit. This skill holds universal facts only. A job's look and notes live in its `*_CLAUDE` folder.

## TOP RULES
1. Name the target before any write. Run `c1 doctor` and read `document.name` and `document.kind`. It is not the document he named: stop. Why: c1 writes to the current document, and two can be open.
2. Back up a Catalog first. `doctor` warns: he clicks File, then Backup Catalog. Wait for his word. Why: `revert` cannot restore mask pixels or a luma range. A Session has no backup step.
3. Originals and variants stay. Never delete a variant, a layer he made, or a file (core rule 2).
4. `revert` is the undo. `action variant.reset` is not an undo, so never use it to go back.
5. New build or new action: scratch test first (SCRATCH TEST below). Why: c1 is tested on 16.8.5.30, and this Mac runs a newer build.
6. Take turns. Say when Claude starts and when it hands back. He leaves those photos alone between the two.
7. Never update Capture One or c1 without his yes (core rule 1). Never quit Capture One, and never close a document he opened.
8. A preview is not a delivery. A final export runs only on his word (FINAL EXPORT below).

## START OF EVERY CAPTURE ONE TURN
```
- [ ] 1 c1 found
- [ ] 2 doctor read, every warning told to him in one line
- [ ] 3 Target document named
- [ ] 4 Catalog backup done, or a Session
- [ ] 5 Photos found by id
```
1. Run `c1 --version`. Command not found: use `~/.claude/plugins/cache/c1/c1/<version>/bin/c1`. Take `<version>` from an `ls` of `~/.claude/plugins/cache/c1/c1/`. Still missing: load `c1:setup`.
2. Run `c1 doctor '{}'`. No `document` in the result: see TRAPS, then go back to step 2.
3. Compare `document.name` with the document he named. Different: ask him to bring the right one forward. Go back to step 2.
4. Top rule 2.
5. Use `c1 selection '{}'`, `c1 list`, or `c1 contact_sheet`. Ids belong to one document, so read them again after a switch.

## COMMAND SHAPES (tested 3 Nov 2026)
`c1 <command> --help` is the contract. Arguments are one JSON object in single quotes.
- Edit: `c1 set '{"ids":["2"],"adjustments":{"exposure":0.8,"curves":{"luma":[[0,0],[25,15],[100,100]]},"colorEditor":{"basic":[{"name":"red","saturation change":20}]}},"variant":{"rating":4}}'`
- `colorEditor.basic` is a list, one item per colour with its name. An object is refused.
- Preview: `c1 preview '{"id":"2","size":800,"timeout":20}'`. The result gives the JPEG path. Read that image before saying how it looks.
- Undo: `c1 revert '{"ids":["2"],"scope":"all"}'`, then `c1 get` to prove it.
- After every write, prove it from `after` in the result or from `c1 get`. A `warnings` item with `sent` and `stored` means Capture One kept another value.

## SCRATCH TEST
Runs before a new build or a new action touches a real document.
```
- [ ] 1 Copy one test image to a folder in the scratchpad
- [ ] 2 Make the session
- [ ] 3 Bring in the image
- [ ] 4 doctor names the scratch session
- [ ] 5 set, get, preview, revert, get
- [ ] 6 Close the scratch session and return to his document
```
1. Copy a picture. Never move it.
2. `osascript -e 'tell application "Capture One" to make new document with properties {name:"c1 scratch test", path:"<folder>", kind:session}'`
3. Copy the picture into `<folder>/c1 scratch test/Capture/`. Then run `import d source {"<that file>"}` with `d` as the new document. Make the collection "All Images" current.
4. `doctor` must name the scratch session. It names his document: stop and go back to step 2.
5. Set a value, read it, preview it, revert it, read it again. Any value wrong: stop and tell him.
6. `osascript -e 'tell application "Capture One" to close document "c1 scratch test.cosessiondb"'`. Then `tell application "Capture One" to activate`. `doctor` must name his document again.

## CATALOG AND ALBUMS BY SCRIPT (tested 3 Nov 2026)
- New catalog: `make new document with properties {name:"<name>", path:"<job>/*_PROJECT FILES/****_CAPTURE 1", kind:catalog}`.
- Link files in place: set each option as `set destination type of import settings of d to current location`. Holding `import settings` in a variable fails with "Invalid key form".
- Import a list of paths: pass them as `osascript` arguments, never typed into the script. Wait until `c1 collections` shows the full count.
- Tree: `make new collection` with `kind:group`, `project` or `album`, then `add inside <album> variants {v}`. Find `v` by name in "All Images".
- Names cannot be changed by script (-10006). Pick them before you make them.
- One `add inside` in 85 failed with no error. Read every album back and compare names before the reply.
- Remove a style: `c1 action variant.reset` refuses a layer c1 did not make. First run a no-change `c1 set` (rating it already has), so `revert` has a snapshot. Then `reset adjustments v` in AppleScript, which also clears every layer.

## FINAL EXPORT
c1 has no final export (2.0.48). On his word, use Capture One's own output:
1. Read the recipes first: `tell current document to get name of every recipe`. Use the one he names.
2. Check the recipe never overwrites. Check the output folder is the job's delivery folder.
3. Run the `process` command on the picked variants. Not yet tested on his Mac: run it on the scratch session first.
4. `ls` the output folder and open one file. The file name and size prove it, not the command.

## ASSISTED REVIEW (Capture One 16.9)
Scripts can flag closed eyes, out of focus and bad exposure. The commands are `review variants` and `reset assisted review`. c1 does not use them yet. Results sit on the variant as read-only `assisted review` properties. Not yet tested: run the scratch test first.

## TRAPS (his Mac, 3 Nov 2026)
- `doctor` has no document after a close: Capture One has no current document, though the window is open. Run `tell application "Capture One" to activate`, then `doctor`.
- The first preview in a new document can time out at 120 s. The JPEG lands in that document's Output folder. Run it again with `"timeout":20`. It then lands in c1's cache.
- A catalog with no output folder: `preview` sets it to c1's preview folder and warns. Tell him.
- `preview` adds a `c1-preview` recipe to the document. It is not a job recipe, so never export with it.
- New session: `list` is empty until "All Images" is the current collection.
- A session can show a variant named "EmptyName". Skip it.
- Never pipe a long `c1` chain in one foreground call. A stuck preview holds the whole queue. Pass `timeout`.
- `doctor` lists 15 script differences on 16.9. It prints 10, all new terms. No effect seen in the scratch test.
- Keywords cannot be created by script (reported on 16.8.5). He adds them by hand.
- Skin Tone in the Color Editor cannot be set alone. Whole Color Editor settings can only be copied (Capture One docs).
- Hand-drawn masks stay his. `c1:edit` says how to ask for one.
- 3 Nov 2026: the Silver+ style with a layer "Fuji Fortia SP 50 1" appeared on 24 pictures of a new catalog. No script applied it. The last one was the picture selected in Capture One. Cause unknown: check `styles` in `c1 get` after an import.

## SETUP FACTS (3 Nov 2026)
- Capture One 16.9.0.10 at `/Applications/Capture One.app`, bundle `com.captureone.captureone16`, macOS 27.0.1. Mac only: scripts do not run on Windows.
- Script list: `/Applications/Capture One.app/Contents/Resources/CaptureOne.sdef`.
- c1 2.0.48, Claude Code plugin `c1@c1`, user scope, from `github.com/kiri11/c1cmd`. MIT licence. An unsigned download from one maker.
- Snapshots and the write log: `~/.c1/documents/<document uuid>/`.
- Styles and crop policy: `~/.c1/styles/`, `~/.c1/crop-policy.md`.
- Previews: `~/Library/Caches/c1/previews/<document uuid>/`.
- The daily outside check watches c1 for new versions.

## HIS RULES
His own rules for Capture One go here, one dated line each (core rule 8). None yet.

## REPLY
Say which document, which photos, what changed, and how it was proved. End with how to undo it.
