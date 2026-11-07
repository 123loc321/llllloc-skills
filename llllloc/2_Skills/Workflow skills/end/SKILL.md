---
name: end
description: "Closes a Code tab session in his brain folder in 7 steps. Runs only when he types llllloc:end or sends only the word end. Rewrites STATE.md, writes the ten-part handoff, files the lesson, tends the research cache, runs the workflow WRAP-UP, delivers the handoff as a file card, saves and pushes the brain to GitHub, then titles the session with its Logged line and marks it done."
---

# /end — STATE, the handoff, the cache, the wrap-up, the Logged line (7 steps, 16 Oct 2026, FOLDERS v19, Mac first 29 Oct 2026)

Runs only when he types `/end`, sends a message that is only the word `end` (2 Oct 2026), or the lead session passes his `end` (NESTED SESSIONS), at the end of a thread. Never on its own. Never mid-thread. `end` inside a longer sentence is not the trigger.

## HARD STOPS

- Never delete a file on the Mac. Move it into a `_DELETE` folder beside it. The one exception is CLEAR ARCHIVE (core rule 2).
- Never write STATE, a handoff, a lesson, a cache line or a trim for work that did not happen.
- Never guess a path. Check that it exists before you follow it.
- Never run on your own.

## SPEED (17 Oct 2026)

Core rule 17: once STEP 1 has the folder, send the STEP 2 writes, STEP 3 and STEP 4 in one tool block, then STEP 5. One Bash call holds `date` and every `ls` of a step. Never one call per file.

## NESTED SESSIONS (1 Nov 2026, tested on 7 sessions, his words: "can you send my "end" command to each of them?")

A thread that started nested sessions ends them first, and itself last. Check with `mcp__ccd_session_mgmt__list_sessions` `{"linked": true}`.

1. Only on his word. Send one child `end` with `SendMessage`, quote his words, and wait for its report. Then the next child. Never two at once: a child's end once wrote over the parent's DECISIONS and FEEDBACK-LOG.
2. The message tells each child: write only your lane state file and your own handoff, put lines for STATE, DECISIONS and FEEDBACK-LOG in part 11 of the handoff, and do not save the project.
3. A child that gets this message skips the shared files in STEP 2 and adds that part 11. It still titles itself and marks itself done.
4. The lead last. It saves the project once, reads every child's part 11, merges those lines in its own STEP 2, moves the older handoffs to `Old/`, and is the only one that pushes to GitHub (STEP 6).

## STEP 1 — FIND THE FOLDER

1. Read the map: a creative job `llllloc/3_Project maps/Project map_Creatives.md`, a code job `Project map_Code.md` beside it, a workflow job needs no map.
2. Match the active project to a row. Take the full path from that row.
3. A drive under `/Volumes/` gets an `ls` first. Not mounted: tell him and use the pending row below.
4. Resolve the Claude subfolder. Never type it: a creative job `ls -d "<full path from the row>"/*/*_CLAUDE`, a code job `ls -d "$HOME/Desktop/PERSONAL PROJECT/CODE/<Kind>/<Job>/_CLAUDE"`. An empty listing means stop and ask him where to write.

A thread with no project row does not stop. Pick the row that fits and say which one you used:

| The thread was about | Write the handoff to |
|---|---|
| His workflow, his skills, or the llllloc folders | `llllloc_workflow/0_Handoffs/` |
| A job with no folder yet | `llllloc_workflow/0_Handoffs/_To projects/` |
| A project whose drive did not mount | `llllloc_workflow/0_Handoffs/_To projects/` |

A handoff in the pending folder carries one line at the top naming the folder it moves to when the drive is back.

## STEP 2 — STATE, THEN THE TEN-PART HANDOFF

1. Rewrite `STATE.md` on top of `*_CLAUDE` in place, never added to, under 150 lines. Top line: last updated, date, time, thread. A creative job: Now, Deliverables (ID, version, status, path), Locked, Open questions, Next task. A code job: Newest build, The one test to ask him for, Open (bugs and untested features by number), Do not, Next task. No STATE.md yet: start one from `llllloc/7_Templates/PROJECT-TEMPLATE/` (creative) or `PROJECT-TEMPLATE_CODE/` (code). A workflow thread has no STATE.
2. Add every decision of this thread to `DECISIONS.md`, one line: `D<n> · date · decision · why · what was turned down · status`, numbered after the last line. Read the file first and never edit an old line (31 Oct 2026). The same for the file in point 3.
3. His exact words: a creative job to `FEEDBACK-LOG.md`, one block per round. A code job to `HIS-WORDS.md`, plus `4_Builds/CHANGELOG.md` (the build) and `1_Spec/FEATURES.json` (only the status of a feature: untested, passed; "confirmed live" only on his words).
4. Name the handoff `HANDOFF_<ProjectName>_<YYYY-MM-DD_HHmm>.md`. Run `date` first. The clock is Asia/Ho_Chi_Minh. It goes in `0_Handoffs/`. The newest 3 stay there; move older ones to `0_Handoffs/Old/` with `mv -n`.
5. Write all ten parts, in this order. Skip none. A part with nothing in it says "Nothing this thread".

```
# HANDOFF — <Project> — <date> <time>
Session: <$CLAUDE_CODE_SESSION_ID> · Kinds of job: <list> · Skills loaded: <list>
(code job: Build before: <V> · Build after: <V>)

1. Goal of the thread: done, partly done or not done
2. Files made or changed: full path and version
3. Checked or only believed: what was proved, and how (screenshot, render, measurement). Code: tests run, gate passed or failed
4. Decisions taken, with their DECISIONS numbers
5. Tried and failed, and why
6. His words this thread (also copied to FEEDBACK-LOG or HIS-WORDS)
7. Technical state: app, project file, comp, settings, every number
8. Open questions for him
9. Next step: one task, first action, files to open
10. Copied into STATE and DECISIONS (code: STATE, CHANGELOG, FEATURES): yes or no
```

Do not simplify. Keep every file name, every number, every prompt word, every tool name, every setting, every rejected direction. A handoff that reads well but lost the numbers is a failed handoff.

## STEP 3 — FILE THE LESSON, WHEN THERE IS ONE

The folder name is the index. Pick the folder by what the lesson is about. Check that the path exists before you write to it.

| The lesson is about | Write it to |
|---|---|
| A MODEL: GPT, Seedream, Kling, Midjourney, Nano Banana, Seedance, Minimax, Recraft | `llllloc/4_Lessons/Prompts/<Model>/<task>.md` |
| A KIND of work, not tied to one model | `llllloc/4_Lessons/Prompts/Shared/<task>.md` |
| A PROGRAM: Magnific, Figma, Premiere Pro, After Effects, Cavalry, Illustrator, Soundly | `llllloc/4_Lessons/Programs/<Program>/` |
| HOW A SESSION RUNS: a rule, a habit, a skill, a cascade | `llllloc_workflow/1_Lessons/Lessons_Workflow.md` |
| A CODE JOB: the rule a mistake bought | the job's `_CLAUDE/7_Lessons/LESSONS.md`, one line |

A prompt lesson goes in one file per kind of task, named in plain words: `head-swap-edit.md`, `product-visual.md` (16 Oct 2026, his words). List the folder and add to the file that matches. No file matches: start one with three sections, `## Best prompt so far`, `## Worked`, `## Failed`. Add one line under Worked or Failed:

`2026-09-23 | what was tried | what happened | the rule it buys`

A prompt that beat the best one replaces it under Best prompt so far. The old one moves under Worked.

`Lessons_Workflow.md` is the exception to the one line. Append a short dated section: what happened, and the rule it bought. Never rewrite what is already there. When the thread taught nothing, write nothing. A workflow lesson ends in one of three ways only (21 Oct 2026): the rule goes into the skill that owns it, a new message goes into the test set (`llllloc:task-skill-creator` kit, `TESTSET.md`), or "no change". A lesson whose fix is a skill line gets that line in the same pass.

A lesson is what HIS render or HIS session taught. What a search found is not a lesson. It goes to the cache, STEP 4.

Say the file you wrote, in the reply, with its full path.

## STEP 4 — TEND THE CACHE

The cache is `llllloc/5_Research cache/` for universal findings (`INDEX.md` names the folders), `llllloc_workflow/2_Research cache/` for facts about Claude itself, and the project's own `*_CLAUDE/2_Research/RESEARCH.md` for findings about one project or client (16 Oct 2026). Open only the files this thread read or wrote:

1. Every finding this thread's searches produced sits in its subject file. Append the missing ones (`>>`).
2. Drop every line older than 60 days, and every line about a version this thread found replaced.
3. Merge two lines that answer one question. Keep the newer date.
4. A file over 60 lines or 6 KB: turn the subject into a folder of topic files, each listed in its `_TOPICS.md` (16 Oct 2026, his words: a task never loads a file it does not need). A new finding goes in the topic file that matches. No match: a new topic file and one `_TOPICS.md` line.
5. A line about one client or project that landed in `5_Research cache`: move it to that project's `*_CLAUDE/2_Research/RESEARCH.md`.

Edit in place with a short python read-modify-write in Bash, never by retyping a file. Nothing to change: write nothing, say `Cache: unchanged`. Otherwise say `Cache: +n, -m`.

## STEP 5 — WRAP-UP: REVIEW THE WORKFLOW

Load `llllloc:task-workflow-best-practices` and run its WRAP-UP mode on this thread. That skill owns the six questions, the trim rules, the caps and the channel for each change (8 Oct 2026). Note what loaded but was not used. Install every trim in the same pass: the skill's Mac master (`llllloc:task-skill-creator` rule 2, it goes up in STEP 6), the core rule file, the workflow section. Never leave a review item as a note only. Nothing to trim: write `Workflow: nothing to trim` and move on. When `learn` ran in this thread, this step and the workflow lesson of STEP 3 are done: write `Workflow: see learn` and move on (22 Oct 2026).

In the reply, the review is six lines at most: what was cut, what was added, where, and which answer wasted tool calls or skipped research.

## STEP 6 — DELIVER THE HANDOFF, THEN SAVE TO GITHUB (6 Nov 2026, his words: GitHub is the master)

1. The handoff is already on the Mac (STEP 2). Send it as a file card with `SendUserFile`, plus its full Mac path (`llllloc:task-sending-files`).
2. Run the brain check: `python3 -I "$HOME/Desktop/Claude/llllloc/1_Core rule/brain_check.py"`. A FAIL line: fix it, then run it again.
3. In the brain folder: `git add -A`, commit `End: <Project>, <what this thread did>`, `git push origin main`. A refused push: `git pull --rebase origin main`, then push again. Never `--force`.
3b. GitHub holds only the plugin, so `git add -A` sends skill files only (`.gitignore`). The Drive backup is weekly, by its own scheduled task, never here (6 Nov 2026, his words).
4. Check: `git status -sb` shows `main...origin/main` with nothing ahead. The reply says `GitHub: pushed <short hash>`, or why not. Skills reach every account when the `llllloc` plugin syncs.

## STEP 7 — THE LOGGED LINE, THEN TITLE AND MARK DONE (28 Oct 2026, his words)

The LAST line of the reply, nothing after it: `Logged_<Project>_<what this thread did>`, matched to the real work, like `Logged_Honda XL250R_character prompt`. Same turn, Claude: `mcp__ccd_session_mgmt__set_session_title` to that line, then `mcp__ccd_sidebar__mark_completed` (both tested 29 Oct 2026). Several sessions of one job: each gets its own line, title and mark (NESTED SESSIONS).

## RESTART MESSAGE (core rule 13)

On his yes to a new thread, write the message he pastes there: the goal, what failed, the next try and the file paths.

## CLEAR ARCHIVE (core rule 15, 18 Oct 2026)

`clear archive` deletes, without asking, the archive of the job in this thread: every `_DELETE`, `OLD VERSIONS`, `Old` or archive folder, on disk and inside his apps (After Effects, Premiere Pro, Figma and others). The reply lists what went and the space freed.