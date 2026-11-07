---
name: tool-soundly
description: "How Claude drives his Soundly sound library through the soundly connector: search his local libraries, read a sound, and copy picked sounds into a job's SFX folder. Runs when the user types its name, or when /llllloc:router picks it for a Soundly search or an SFX pull, always beside llllloc:task-sound-design. Holds the connector rules only. What sounds to use, where and how loud belongs to llllloc:task-sound-design."
---

# llllloc:tool-soundly (split from llllloc-sound-design, 17 Oct 2026)

His words, 17 Oct 2026: the Soundly connector is its own tool skill, like the other llllloc-tool skills. `llllloc:task-sound-design` decides which sounds a film needs. This skill finds them and copies them in.

Lessons: read `llllloc/4_Lessons/Programs/Soundly/README.md` once per job (install and indexing notes).

## WHAT THE CONNECTOR IS (tested 10 Oct 2026, soundly-mcp by 1800doublegee)

- It reads Soundly's local index. It searches only the libraries he added, not the Soundly cloud. A new pack appears only after Soundly has indexed it: he opens the Soundly app once.
- Its tools: `search_sounds`, `get_sound`, `list_libraries`, `library_status`, `list_categories`, `copy_to_project`.
- `search_sounds` takes `query`, `limit`, `max_length`, `fmt`. Each result carries the file path.
- `copy_to_project(ids, dest)` copies the files and renames them by their description.

## STEPS

1. A search finds nothing he expects: run `library_status` and `list_libraries` first. A library on an unmounted drive returns nothing. Say which drive is missing in one line.
2. Search. 8 to 10 `search_sounds` calls in one block, one sound family each, named by the real material (pop, click, glass, air, riser, sub, chime, ping, shimmer). The family list comes from `llllloc:task-sound-design`.
3. Pick by path. Prefer `~/Desktop/MY STUFF/SFX/`. A path on `/Volumes/HCMC #26` is an old job's drive: use it only when nothing local fits.
4. Never the same file twice unmodified. A second use gets another take, or sits 2 dB lower.
5. Copy. `copy_to_project` into `<project>/PROJECT/PR/3_SOUND ASSET/SFX_From Soundly/`. An older project: `2_SOUND ASSET/2.2_SFX/`. The path comes from the project map or an `ls`, never a guess.
6. Hand back to `llllloc:task-sound-design` with the copied paths. It imports them into Premiere through `llllloc:tool-premiere-pro`.

## CHECK

`ls` the SFX folder after the copy. Every picked sound is there once. A missing file: copy it again, then check again.
