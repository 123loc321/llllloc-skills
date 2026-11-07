---
name: task-clean-my-mac
description: "Deep cleans his Mac and the CREATIVE drive: measures where the space went, lists what can go with sizes and risk, then moves only the picks he approves to the Trash with Finder, uninstalls old Adobe and Maxon versions with their own uninstallers, and checks the space freed. Use when he types its name, or when /llllloc:router picks it for a full disk, storage cleanup, free up space, old versions, caches, temp files, _DELETE folders or leftover apps. Never empties the Trash, never deletes for good, and never touches OLD VERSIONS renders or project files."
---

# llllloc:task-clean-my-mac (5 Nov 2026)

Built from the 5 Nov 2026 cleanup: 387 GB free at the start, about 700 GB once he emptied the Trash. Paths, sizes and traps of his Mac: [mac-map.md](mac-map.md). Why each item is safe or not, with sources: [research.md](research.md).

## TOP RULES
1. **Move to the Trash, never delete.** Core rules 1 and 2. Every removal is a Finder move to the Trash (`scripts/trash.sh`), so it can be put back. Emptying the Trash is his step, always. A plain `rm`, `uv cache clean`, `docker system prune` or an app's "delete all" button is a permanent delete: never run one.
2. **His yes per round.** The scan and the list need no yes. Moving anything needs his yes on that list. "Delete them", "remove all", "ok" on a line are the yes for those lines only (5 Nov 2026).
3. **Nothing inside a client project folder, ever** (5 Nov 2026, his words: "nothing from client project folder, but for the code folder and or from claude folder you can delete", and "dont delete old render versions"). A client project folder is every job in `~/Desktop/PERSONAL PROJECT/` except `CODE/`, and every job on `/Volumes/CREATIVE #1/`. That includes `OLD VERSIONS` renders, unpacked zips and the job's own `_DELETE` folders: an edit can still use a file in `_DELETE`. Why: 14 the studio Showreel clips in `_DELETE` folders went offline in his Premiere edit, and round 1's job items were emptied for good. List their sizes as info only. `scripts/trash.sh` refuses these paths. `CODE/` and the brain folder `~/Desktop/Claude` may be cleaned: `_DELETE` contents, build output, old installers. Keep `4_Builds/Old` restore points and the newest two installers.
4. **Check who uses it before you list it as safe.** A model, cache or app another tool needs stays: run `scripts/scan.sh`, then read the KEEP list in mac-map.md. On 5 Nov 2026 he asked to remove Ollama, but Cotabby's Rewrite runs on it (`ollama list`, `ps`).
5. **An open app keeps its cache.** Check `ps` first. After Effects, Premiere, Media Encoder, SELECTS or Claude open: skip their caches, or ask him to quit the app.
6. **Prove every claim.** Sizes come from `du` and `df` this turn. "Safe" comes from a check: the zip's files exist unzipped, the copy exists on the drive with the same size, the app is not installed. No check: the line goes to HIS CALL.

## STEPS

```
- [ ] 1 Scan (read only)
- [ ] 2 Research what is new
- [ ] 3 Report: SAFE, HIS CALL, KEEP
- [ ] 4 His picks
- [ ] 5 Move to Trash, check nothing is left
- [ ] 6 Uninstall old app versions
- [ ] 7 He empties the Trash, then measure
```

1. **Scan.** Run `bash ${CLAUDE_SKILL_DIR}/scripts/scan.sh > <scratch>/scan.txt` in the background (about 4 minutes on his 2 TB Mac, tested 5 Nov 2026), then read it by section (`grep -n "^==="`). It prints free space, running apps, Library and drive tops, `_DELETE` and old folders, caches, models, leftovers of uninstalled apps and big files.
2. **Research.** `llllloc:task-research` loads with this skill. Check research.md first. A new tool, app or folder not in it gets a search before it is called safe. Add what you learn to research.md.
3. **Report** in the chat, biggest first, three groups:
   - **SAFE**: rebuilds itself or is a checked duplicate. Path, size, how it is removed.
   - **HIS CALL**: he may still use it. Say who uses it and what is lost.
   - **KEEP**: say why in one line.
   Cookies are under 4 MB in total, and deleting them signs him out everywhere. Never offer them. Offer to open the folders in Finder (`open`, `open -R` for one file).
4. **Wait** for his picks.
5. **Move.** Write the picked paths to a list file, then `bash ${CLAUDE_SKILL_DIR}/scripts/trash.sh <list>`. It refuses project paths, moves a symlink itself (Finder would trash its target), moves the rest in batches of 40, and prints what is still in place. A cache folder with thousands of files: move the folder, then `mkdir -p` it again. Root-owned folders open a Mac password box: tell him to type it. macOS refuses `~/Library/Containers/...` and `Group Containers`: give him the Finder steps (Cmd + Shift + G, paste the path, drag to Trash). Something still in place: fix the path or give him the Finder steps, then return to step 5. Never skip it quietly.
6. **Uninstall old app versions** with the maker's route, never by dragging the app: Adobe and Maxon steps in mac-map.md, ADOBE and MAXON.
7. **Measure.** Tell him: open the Trash, look once, Empty. Then `df -h` before and after, in GB.

**Put back** a wrong move with `bash ${CLAUDE_SKILL_DIR}/scripts/put_back.sh <list>`, the same day, before he empties the Trash. It moves each item from `~/.Trash/<name>` to its old folder. Two items with one name: the first trashed keeps the name, later ones get ` HH.MM.SS` added, in list order (`osascript -e 'tell application "Finder" to get name of every item of trash'` lists them in a second). Finder "whose name" restore takes a minute per item: never use it.

## OUTPUT
The reply opens with GB freed and GB waiting in the Trash. Then a table per round: what, size, where. Then what is left for him (password box, a protected folder, emptying the Trash). His English is his second language: short sentences, numbered steps for every click. Sources as links. Then the Loaded and Time lines.

## DO NOT
- Never empty the Trash, run a permanent delete, or clear cookies or passwords.
- Never install a cleaner (Mole, OnyX, Pearcleaner, DaisyDisk) without his yes: core rule 1. pearcleaner.com is a fake site that installs malware. The real Pearcleaner is on GitHub (alienator88).
- Never trash a running session's Claude temp folder, or `vm_bundles` while a Cowork VM runs.
- Never move job folders to another drive in this skill. That is `llllloc:task-files-organize`, and only on his word.
