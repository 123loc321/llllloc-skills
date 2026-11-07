---
name: project-code
description: "The task rules for every code job in llllloc: plugins, panels, apps, extensions, websites and scripts in his CODE folder. How a job opens, the job folder shape, proof, building, delivery and end. Loaded by /llllloc:router once per thread when a message names a code product or code Claude writes."
---

# llllloc:project-code (15 Oct 2026; job folder FOLDERS v16, 16 Oct 2026)

Every code job lives under `~/Desktop/PERSONAL PROJECT/CODE/`. He is a visual artist, not an engineer. He installs and tests every build. This skill loads once per thread and stays. The detail files sit beside it on the Mac in `llllloc/2_Skills/Rule skills/project-code/`: `building.md` (any code), `panels.md` (Premiere and After Effects panels), `apps.md` (apps). Read the one the job touches, when the first line of code is near.

## HARD STOPS
- Every code job loads `llllloc:ponytail` and `llllloc:using-agent-skills` with this skill, before the first tool call of the work, whatever skill the job adds (his words, 19 Oct 2026). Why: the mascot app thread loaded only this skill and app-builder. Check before each reply: the Loaded line names both. One is missing: load it, check the work against it, fix, then reply.
- Never delete anything: move it into the job's `_CLAUDE/_DELETE/`. A stray folder nobody made on purpose: `diff -rq` it, then park it under a name that says what it was.
- Ask first before you: install anything outside the CODE folder, touch another job's folder, make any change that needs his password, or change a gate (`check-build.js`, `check-pack.js`).
- Never ship a mechanism you cannot test. Nothing acts unasked. A delete button arms on the first click and acts on the second.
- A rule that gets skipped never gets louder: give it a gate, a test or an output he can see, then words.

## 1. THE START OF A JOB
1. Read only the job's row in `llllloc/3_Project maps/Project map_Code.md`. Match his words against the HE SAYS column. Two rows match: name them and ask. No row and a code request: NEW JOB, section 7.
2. Say `Job: <name>.` Load the row's skills. The CODE folder needs no access step: use full paths (29 Oct 2026).
3. Read the job's `_CLAUDE/STATE.md`, pick ONE unfinished feature in `1_Spec/FEATURES.json`, then read the newest `HANDOFF_*.md` in `0_Handoffs/`, then only what they name. One feature per thread. It is done only after its test passes; "confirmed live" only on his words. A build behaves wrongly: ask for its report now, before anything is installed. An install wipes it.
4. Something needed is missing (a file, an app, a connector): say exactly what, and stop. Never guess or substitute.
5. Two threads on one job: the first is the LEAD and writes the shared files. The second writes only its own part and lists the shared changes it wants in its reply.

## 2. THE JOB FOLDER
```
CODE/<Kind>/<Job>/
  <NAME>-V<n>-INSTALLER/  the newest build only: install file, WHAT'S NEW, INSTALL guide
  _CLAUDE/                everything Claude needs and he never opens
    STATE.md  PROJECT.md  DECISIONS.md  HIS-WORDS.md  (CLAUDE.md only when Claude Code works on his Mac)
    0_Handoffs/   HANDOFF_<NAME>_<date_time>.md, ten parts; newest 3, older in Old/
    1_Spec/       SPEC.md, FEATURES.json (untested, passed, confirmed live), ROADMAP.md, COMPATIBILITY.md
    2_Research/   RESEARCH.md (one dated line per fact), LIMITS.md (TESTED or ASSUMED)
    2_References/ Claude's reference notes: REFERENCE_<site>.md, _batches/<source>.md, Claude screenshots; the dropped files in Files/ (his words, 17 Oct 2026)
    3_Design/     DesignSystem_<NAME>_V<n>.md, DESIGN.md, Figma links; older in Old/
    4_Builds/     CHANGELOG.md, RELEASE-CHECKLIST.md, SIGNING.md, Old/ = every older build
    5_Tests/      SMOKE-TEST.md, BUGS.md, test scripts
    6_Shots/      <NAME>-V<n>_<screen>_before-after.png, Golden/
    7_Lessons/    LESSONS.md, the rule each mistake bought
    8_Samples/    Test Project/, Sample files/
    _DELETE/      trash. Never deleted. Old builds never go here.
```
A folder appears the first time a file goes in: a script job never makes 3_Design or 6_Shots. Templates: `llllloc/7_Templates/PROJECT-TEMPLATE_CODE/`. Kinds: `PR Plugin/` (one folder per panel), `AE Plugin/`, `Apps/`, `Plugins/`, `Scripts/`, `Websites/`. A job that fits no kind starts a new kind folder named in plain words.
The Premiere suite `PR Plugin/_CLAUDE/`: STATE.md, MISTAKES.md, LIMITS.md, OPEN-QUESTIONS.md, PROJECT.md on top; `0_Handoffs/`, `2_Research/`, `PLUGIN LOG/` (PLUGIN-LOG.md and its parts), `Shared/` (shared code and the gate), `Guides/`, `Share packs/`, `Tools/`, `_DELETE/`.
One home for each fact: STATE.md (newest build, the one test, open work, do not), PROJECT.md (what it does, its look, choices expensive to undo), DECISIONS.md (one line per tech choice), CHANGELOG.md (what shipped), FEATURES.json (each feature and its status), HIS-WORDS.md (his exact words). No password or key is ever written in these notes. The build on disk beats the log.

## 3. A TURN IS FAST AND CHEAP
- Finish fast with zero faults. Speed never cuts a test. Size the proof to the risk: a text edit gets one read-back, a code change its own tests and the picture if it looks different, shared code or an installer full proof.
- Fewer, bigger steps. Batch reads, edits and checks into one script. After each edit run the one test that covers it. The full suite and the gate once, at the end.
- Long output never enters the chat raw: `tail`, `grep` or a summary line.
- No spec for a fix that changes one behavior. `llllloc:using-agent-skills` may list assumptions, ask, and write a spec for a bigger one. Its tests take the time they need.

## 4. SILENCE MEANS IT WORKED
A build on his disk is a build he installed. Never ask if he installed it. Ask once, plainly: one test, one screen, one expected result. Three states in the log: CONFIRMED LIVE (his yes in words or his picture, dated), PASSED, NO PROBLEM REPORTED (asked, stayed quiet), untested. A choice resting on an untested limit is a bug. Status lives in `1_Spec/FEATURES.json`.

## 5. A FACT FROM OUTSIDE NEEDS A SEARCH
A claim of a LIMIT, or that something WORKS on his Mac, needs two searches: the mechanism tried and the outcome he asked for. Otherwise write ASSUMED. Findings go to the job's `_CLAUDE/2_Research/RESEARCH.md`, one dated line each, source link inline.

## 6. DELIVERY AND END
- A new build is a NEW `<NAME>-V<n+1>-INSTALLER/`. The build it replaces moves into `_CLAUDE/4_Builds/Old/` the same turn, never `_DELETE`: the last good build is the way back. Tick `4_Builds/RELEASE-CHECKLIST.md`. Every version is kept. Never overwrite a zip. Zip a folder from OUTSIDE it. `install.command`: `chmod 755` before any zip, then read the mode back.
- A file is delivered when he can find it: folder and file name in plain words, revealed with `open -R`. Never propose a step that needs the terminal or hand-editing a file: put it behind a button, or do it yourself.
- If it will look different, show the picture: before and after at his width, saved to `_CLAUDE/6_Shots/`, opened with `open`.
- `end` runs `llllloc:end` like every other job: STATE.md rewritten, the handoff in `_CLAUDE/0_Handoffs/`, the build in CHANGELOG.md, feature status in FEATURES.json, his words in HIS-WORDS.md. Premiere suite jobs also run `llllloc:end-plugin-log` for the suite top files and the PLUGIN LOG parts.

## 7. A NEW JOB
1. Ask what he calls it. An unsaid name is a placeholder.
2. He double-clicks `New job.command` (in this skill's folder on the Mac) and types the kind and the name. It makes `<Kind>/<NAME>/_CLAUDE/` with STATE, PROJECT, DECISIONS, HIS-WORDS, `0_Handoffs/`, `1_Spec/FEATURES.json`, `4_Builds/CHANGELOG.md` and `_DELETE/`, and prints what it made. Other folders appear when a file needs them. Claude may run it with `bash` instead.
3. Add the row to `llllloc/3_Project maps/Project map_Code.md`, with the words he used.
4. Say it in one line: `Added job: <name>, in <Kind>/.`

## 8. AN APP BUILT FROM SOMEONE ELSE'S GITHUB CODE (26 Oct 2026, his words)
"Update the overall workflow so that any future app updates are automatically added to this schedule."
1. His changes live on his own branch, never on the maker's branch. Note the maker commit his build sits on.
2. The same turn the app is set up, without asking: its line in `APPS` of `check_app_updates.py` and its row in `Apps watched.md`, both in `llllloc/8_Scheduled tasks/App updates/` (Mac only, 29 Oct 2026). Row: maker repo and branch, his folder and branch, base commit, maker pull requests he took, where its settings live.
3. The scheduled task "Weekly app updates" (Mondays) then lists the maker's changes for him. Nothing is applied without his yes. After an approved update is installed, move the base in both files.