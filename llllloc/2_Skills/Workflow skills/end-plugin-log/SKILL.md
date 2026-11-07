---
name: end-plugin-log
description: "End-of-day maintenance for the studio's apps and plugins log: the core PLUGIN-LOG.md, its part files and STATE.md. Reads the LOG-UPDATED stamp and folds the session's new versions, bug root causes, CEP findings and the studio corrections into the part that holds each section. A MISTAKES PASS records every wrong turn, and step 3c carries each rule into the instrument that enforces it: a gate check, a visible output, a skill, a test, or the code rules. A LEAN PASS holds every file under its cap, and a count-in/count-out check proves nothing was lost. Snapshots what it replaces, writes disk, rewrites STATE.md, tidies zips into 4_Builds/Old. ALWAYS use when the user types /end-plugin-log, when llllloc:end runs on a Premiere suite job (CODE/PR Plugin/), or when the user says \"update the plugin log\", \"log today's work\", \"end of day update\", \"keep it lean\". NOT for building plugins - that's llllloc:task-plugin-builder."
---

# llllloc:end-plugin-log

Keeps the plugin log, the source of truth for the Premiere suite, current AND short.

Four jobs: **record what the plugins do**, **record what went wrong** (3b), **carry each rule into the instrument that enforces it** (3c), **keep every file under its cap** (6).

**TRIGGER:** `/end-plugin-log`, or `end` on a Premiere suite job: it runs with `llllloc:end` (renamed from plugin-log-update, 17 Oct 2026).

This file holds rules only. The stories and his exact words behind them live in `CODE/PR Plugin/_CLAUDE/PLUGIN LOG/` and `MISTAKES.md` (16 Oct 2026, FOLDERS v19; the old `_WORKFLOW/RULES-WITH-REASONS.md` was retired on 14 Oct 2026). The scripts and tables for steps 6 and 8: `CODE/PR Plugin/_CLAUDE/PLUGIN LOG/PLUGIN-LOG-UPDATE-METHOD.md` (moved 17 Oct 2026).

## THE FOLDER

```
CODE/PR Plugin/                      (16 Oct 2026, FOLDERS v19)
├── <PANEL>/_CLAUDE/                 <- one per plugin: STATE, 0_Handoffs, 1_Spec/FEATURES.json, 4_Builds (+Old), 6_Shots
└── _CLAUDE/                         <- the suite
    ├── PROJECT.md · README.md
    ├── MISTAKES.md · LIMITS.md · OPEN-QUESTIONS.md   <- parts 15, 7, 11, on top
    ├── PLUGIN LOG/
    │   ├── STATE.md                 <- ONE SCREEN, read first (start it when missing)
    │   ├── PLUGIN-LOG.md            <- THE CORE AND THE MAP
    │   ├── 06-*, 09-*, 12-*.md      <- the parts left here
    │   ├── PLUGIN-LOG-UPDATE-METHOD.md  <- the scripts for steps 6 and 8
    │   └── _previous/PLUGIN-LOG-<date-time>/ <- the 3 newest snapshots
    ├── Shared/ (check-build.js) · Share packs/ · Guides/ · Tools/
    ├── 0_Handoffs/ · 2_Research/ · 6_Shots/
    └── _DELETE/
```

**Disk is the only copy** (29 Oct 2026). the studio never downloads or re-uploads anything.

**THE RESEARCH CACHE IS NOT THIS SKILL'S JOB (2 Oct 2026).** `llllloc:task-research` writes it. `PLUGIN LOG/RESEARCH-CACHE.md` and the old project doc are retired: never read or write them.

| File | Holds | Cap |
|---|---|---|
| `STATE.md` | newest versions, open work, each file's size | 60 lines |
| `PLUGIN-LOG.md`, the core | sections 0 to 5, 8, 10, 13. Section 0 is the map | 330 lines |
| `06-DESIGN-SYSTEM.md` | section 6 | 110 lines |
| `../LIMITS.md` (on top of `_CLAUDE`) | section 7 | 350 lines |
| `09-GATES-AND-SHARED-MODULES.md` | sections 9 and 14 | 170 lines |
| `../OPEN-QUESTIONS.md` (on top) | section 11 | 220 lines |
| `12-UPDATE-HISTORY.md` | section 12 | 40 lines |
| `../MISTAKES.md` (on top) | section 15. Every session reads it whole | 220 lines |
| `README.md` | the folder map | 80 lines |
| `llllloc:project-code` (the code rules) | how to work. Count with Python `len(text.split())` | 3,000 words |
| `_previous/` | the snapshots | 3 |

`reference/file-structure.md` is older than the split, except its 6f cascade section. Where it differs, this file wins.

## WHERE THIS RUNS

The Code tab session that did the build (5 Aug 2026, 29 Oct 2026). No session can read a finished session, and the failure is SILENT. The source is this session's own context. If the build happened somewhere else, say so. Never produce a thin update from the folder alone.

## THE TIMESTAMP IS THE BOUNDARY

Line 1 of the core is `<!-- LOG-UPDATED: 2026-08-05T02:05+07:00 -->`. Everything after it is unlogged. Read it first, write a new one last. Always ICT, `+07:00`.

- **GENERATE THE STAMP, NEVER TYPE IT.** Run `date` in the script that writes the file, and let that script write both the stamp and the human line. A stamp ahead of the real moment empties the next run's window, silently.
- **A SESSION CAN OUTLIVE THE DAY.** Read the clock at the moment each dated file is written. A shipped file's date that differs from today is a long session, never a discrepancy. Never raise it, never re-date a shipped file, never ask which clock is right. The part 12 row names the days the work ran. `check-build.js` RULE F enforces this.

## PROCEDURE

### 1 · Read the current log

Read `STATE.md`, the core and `_CLAUDE/MISTAKES.md` from disk, whole. Parse the stamp. Section 0 names the part that holds each section. Then read only what the session touched:

- **Part 11:** THE WHOLE SUITE block, plus the block of every panel touched.
- **Part 07:** its contents table, then grep for every host call, panel and feature touched. Read every entry the grep finds.
- **Part 12:** the newest row.
- **Parts 06 and 09:** only when the session changed the look, a gate or `_CLAUDE/Shared`.
- **A whole part** when the session changed many of its entries.

Never read a `PLUGIN-LOG-FULL-*` archive whole. Find one entry with `grep -n '^## '` and read that entry whole.

`PLUGIN LOG/` sits in the suite `_CLAUDE/`, beside the panel folders: `~/Desktop/PERSONAL PROJECT/CODE/PR Plugin/_CLAUDE/` (the map row). `ls` it first. Missing: say the log and `_CLAUDE/Shared` are out of reach. Never report "nothing new".

Never regenerate a file. Edit with a script on his Mac: one anchored substitution per change, each anchor found EXACTLY ONCE, stop if not. The step 8 snapshot is the undo.

Stamp missing or malformed: use the newest part 12 row as the cutoff, say so, and restore the stamp in step 7. Ask the studio only when part 12 has no usable row. No log at all: build one from the folder map and `reference/file-structure.md`.

### 2 · Gather the window

1. **This session** is the primary source: everything built, tested, fixed or rejected. Read it properly, never from impression.
2. **The plugin folders.** `<PANEL>/_CLAUDE/4_Builds/` holds the newest zip and its unpacked folder, older ones in `4_Builds/Old/`, pictures in `6_Shots/`. **The folder is evidence. The log is a claim.** Say where they disagree. `NOTES-FOR-NEXT-SESSION.md` inside a zip is the only thing that crosses a session boundary.
3. **Project memory** only tells you that something happened, never what. It is lossy.

Work done elsewhere: say so, name the panel, ask for the zip. Never fill the gap from memory.

### 3 · What to extract, in priority order

1. **New version numbers shipped.** Check every panel in the window. This is the most common drift.
2. **Panels missing from section 2** of the core.
3. **CEP findings** to part 07, in the group that fits. **ONE ENTRY PER CALL.** An entry carries facts about its titled call only. A fact about another call gets its own entry, plus a pointer.
4. **Bug root causes:** the symptom AND the cause.
5. **the studio corrections and rejected directions.** "Do not do X again" is the most valuable line in the log.
6. **Part 11:** delete answered questions, add new ones to the panel's block.
7. **Ports and extension IDs** confirmed, to section 5 of the core.

### 3b · The mistakes pass

Read `reference/mistakes-pass.md` first. Its "section 15" means `_CLAUDE/MISTAKES.md`.

Find the wrong turns: the studio's corrections, a version bumped twice in one hour for one feature, a check that passed something broken. Write the habit underneath, not the typo, as ONE LINE in part 15, in the group that fits.

- What counts, the merge by cause and the entry shape: `reference/mistakes-pass.md`. A rule broken again gets its date added, not a twin.
- **A rule a file can prove belongs in a gate.** Add it to part 09 as a candidate. **Never edit `_CLAUDE/Shared/check-build.js` without the studio's OK.** Ask in the hand back.
- No mistakes: write nothing.

### 3c · Carry every rule into the instrument that enforces it

**Never skip this step.** Part 15 is a record, and a record does not fire. For each mistakes-pass entry, find where the rule must live to be obeyed, in this order, and change that file:

| # | Home | When | Do |
|---|---|---|---|
| 1 | **A gate check** (`check-build.js`, `check-pack.js`) | a file can prove the rule | Propose it in the hand back, name the check, prove it both ways. Never edit without his OK |
| 2 | **A visible output:** exit code, file card, picture, test count. Never a line in the reply | a habit a gate cannot see | Put it where he looks: the code rules (`llllloc:project-code`) AND the skill that owns the work |
| 3 | **A skill** (`llllloc:task-plugin-builder`, its `panel-ui/`, this one) | one kind of work | Rule at the TOP of the skill, changed as "Where a skill change goes" below says, print the description count |
| 4 | **A test** in the panel's `tests/` | code behavior | Write it, name its case number |
| 5 | **The code rules** (`llllloc:project-code`) | how the whole project runs | A skill change, as below. The rule is one or two lines, paid for by one cut or merge, the story to `RULES-WITH-REASONS.md`. The rule and its payment land in ONE script that counts words and refuses to save over 3,000 |
| 6 | **Part 15 alone** | none above can hold it | Say so plainly. This should be rare |

- **A rule that existed and was broken gets an instrument, never more words.**
- **Where a skill change goes (29 Oct 2026, replaces the 13 Oct rule).** A skill change goes the way `llllloc:task-skill-creator` delivers it: the Mac master in `llllloc/2_Skills/` is changed, committed and pushed, and the `llllloc` plugin syncs it (its rule 2, 6 Nov 2026). Never write into `~/.claude/skills/`.
- **THE `description` CAPS AT 1024 CHARACTERS.** Count it back out of the saved file and print the count beside the `.skill` path:

  ```
  awk '/^description:/{s=1} s{print} /"$/{if(s&&NR>2)exit}' SKILL.md | wc -c
  ```

  Trim by dropping a clause, to under 1000. Keep the triggers and the NOT-for line.

### 4 · Provenance

Record as fact only what the studio confirmed by testing.

| What happened | Record it as |
|---|---|
| the studio tested live and confirmed | Plain fact |
| Claude proposed, the studio did not respond | Nothing, or untested |
| Discussed as a maybe | Part 11, or nothing |
| Claude shipped, the studio has not tested | The version, marked `⚠️ untested` |

Never promote a suggestion into a decision, even when he reacted well.

### 4b · Count the pipes in every table you touched

A stray `|` in a cell silently truncates the row. In every file touched: `awk '/^\|/{n=gsub(/\|/,"|"); print NR": "n" pipes"}' <file>`. Every row of one table has one count.

### 5 · Edit, do not rewrite

Keep each file's headings and group order. Keep every settled fact unless superseded, then correct it and say so. **Never renumber a section or move one to another file without the studio's word.** Other files point at the numbers. A moved section keeps its `## N · TITLE` heading in its part and a one-line pointer in the core. A new part or section needs his word.

### 6 · THE LEAN PASS — EVERY RUN

A file nobody opens holds nothing.

#### 6a to 6d · Measure, shape, count, distill

**Read `CODE/PR Plugin/_CLAUDE/PLUGIN LOG/PLUGIN-LOG-UPDATE-METHOD.md` whole before this step.** It holds the measuring script (6a), the shape table (6b), the count proof (6c) and the distill steps (6d). The rules that bind every run:

- Print the 6a numbers. A number over its cap is the work of this step.
- **THE RULE STAYS IN ITS PART. THE STORY GOES TO THE ARCHIVE.**
- The part 07, part 15 and part 11 counts only go UP or hold, unless the studio said so, a part 11 item was answered, or a 6d merge has a map. Part 07 counts headings plus bullets. A drop for any other reason is a failed run: restore from `_previous/`.
- Distill only the file that broke its cap. Archive it whole first with `cp -n`.

#### 6e · Trim the folders

- `_previous/` keeps the 3 newest snapshots by the date in the name. Move the rest to `_to_delete/PLUGIN-LOG-previous-<today>/` with `mv -n`.
- **Park, never delete.** A workflow doc whose facts all live somewhere better goes to an `Old/` folder beside it, renamed with its date. Name the three places its facts went. A fact that lives only there means it stays. Everything else goes to `_DELETE/`. Name the folder in plain words and say only the studio empties it.

#### 6f · Cascade, in the same run

A changed shape, size or name makes six pointers wrong. Fix all six now, never next time. The list: `reference/file-structure.md`, section "6f cascade".

Find them with the 6f grep in the METHOD file, never from memory. Read every hit. Leave `Old/` and `_DELETE/` alone.

A changed `llllloc:project-code` ships whole, as a skill change (step 3c). Never a diff.

### 7 · Close the loop

1. Run `date`, ICT `+07:00`.
2. The script writes the new stamp on core line 1 and the **Last updated** line from that reading.
3. One short row in part 12, newest first.
4. **THE SAME SCRIPT ASSERTS WHAT IT WROTE**, and stops before saving unless every check in `reference/file-structure.md` section "7 asserts" holds. Then it reads each file back and compares.

### 8 · Write it to disk

In this order, so a half-finished run still leaves the newest copy on disk:

1. **Snapshot:** `_previous/PLUGIN-LOG-YYYY-MM-DD-HHMM/`, stamped when made, holding the outgoing copy of EVERY file this run changes. Never skip it. It is the only undo.
2. **Write each changed file** to disk.
3. **Rewrite `STATE.md`.** One screen: each panel's newest version READ OFF THE ZIPS, the newest pack, part 11's open work with the top item first, and the where-to-look table with each file's lines and cap, generated by the script. Remove settled lines. Check the versions with the step 8 command in the METHOD file. Every version in STATE.md matches the zips, or the file is wrong.
4. **Tidy.** In each panel's `_CLAUDE/4_Builds/` touched and in `_CLAUDE/Share packs/`, only the newest zip and its unpacked folder stay at the top. The rest go to `4_Builds/Old/` (packs: `Share packs/Old/`) with `mv -n`, pictures to `_CLAUDE/6_Shots/`.
5. **Run `node "_CLAUDE/Shared/check-build.js" --all` and say the exit code.** Exit 0 ships.

No download, no re-upload, no manual step.

### 9 · Hand back

Briefly, in this order:

1. **What changed:** versions first, then the parts.
2. **What the mistakes pass found**, one line each.
3. **WHERE EACH RULE NOW LIVES**, one line each. Each skill changed, with its description count and its `.skill` path. Gate checks waiting for his OK. **A rule with no instrument is named as such.**
4. **THE LEAN NUMBERS:** the 6a output and the 6c before and after. A missing count means the lean pass did not run.
5. **What needs his judgement.**
6. **Every file written or parked**, folder and file name in plain words.
7. **Any gap:** panels touched outside this session.

## GUARDRAILS

The ones a run breaks most:

- Never invent a version number. Untouched panel: leave it. Unclear: mark it and ask.
- Never drop a part 07 limit, a part 15 rule or an unanswered part 11 item, in the lean pass included. The 6c counts are the proof.
- Never overwrite a log file without its snapshot, or an archive at all (`mv -n`, `cp -n`).
- Never report "nothing new" without saying where you looked. Nothing to record: update the stamp only, and the lean pass still runs.