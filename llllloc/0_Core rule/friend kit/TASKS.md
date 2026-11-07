# Scheduled tasks for a friend's copy (7 Nov 2026)

`SETUP.md` step 6 creates these three with the scheduled-tasks tool (`create_scheduled_task`). Before each call, fill in:
`{BRAIN}` = the full path of this brain folder, `{P}` = the prefix in MINE.json (llllloc when the copy was not renamed),
`{KIT}` = `{BRAIN}/{P}/0_Core rule/friend kit`, `{BACKUP}` = the backup folder picked in step 5 (skip task 1 when none).
Each block below is the whole prompt. The tasks run while the Claude app is open. A missed run starts at the next launch.

## 1. Weekly backup
taskId `{P}-weekly-backup`, cron `17 12 * * 1` (Mondays 12:17), description "Weekly one-way copy of the {P} brain folder to the backup folder, then a check."

```
Weekly backup of the {P} brain folder. Work in {BRAIN}. Do not load the router or any job skill. Do not change, move or delete any file in the brain folder.
1. Run in Bash: python3 -I "{KIT}/backup_folder.py" "{BACKUP}"
   It copies the brain one way into {BACKUP}/Claude. A replaced or removed file moves into {BACKUP}/_DELETE/<date>, never lost. The last line names the differences left: 0 is a pass.
2. "STOP: ... is not on this Mac": Google Drive for desktop is closed or signed out. Say so in one line. Never sign in for the owner.
3. Reply in simple English, short sentences: "Backup done: <files> files, <n> differences" or "Backup FAILED: <one-line reason>".
```

## 2. Daily outside check
taskId `{P}-daily-outside-check`, cron `13 9 * * *` (every day 9:13), description "Daily: refreshes the outside skills from their repos and lists newer connector versions."

```
Daily check of the skills and connectors the owner did not write. Work in {BRAIN}. Load the router as usual ({P}:router, then {P}:project-workflow, {P}:task-skill-creator, {P}:task-research).
Everything a run delivers goes into ~/Desktop/Scheduled tasks_Daily outside check/<YYYY-MM-DD>/ and nowhere else. Never delete: leftovers go to a _DELETE folder.
1. Run: python3 -I "{BRAIN}/{P}/8_Scheduled tasks/Outside updates/check_outside_updates.py" "~/Desktop/Scheduled tasks_Daily outside check/<YYYY-MM-DD>/" (write the real date and the full Desktop path).
   It copies every outside skill 1 to 1 from its repo into {P}/2_Skills/Outside skills/<name>/, moves the old copy to Outside skills/_DELETE/, rebuilds the plugin list and writes REPORT.md.
2. For each UPDATED or NEW outside skill, read its changelog or commits and write one plain line on what changed. A change that would break a rule of this system (an interview before work, a skill that turns itself on in every session) gets a WARNING line.
3. Run python3 -I "{BRAIN}/{P}/0_Core rule/brain_check.py". Fix any FAIL, then run it again.
4. When the brain folder has a .git: git add -A, commit "Daily outside check <date>", git push origin main (refused: git pull --rebase origin main, then push, never --force).
5. Connectors: list each newer version from REPORT.md with its release page link. Never download or install anything.
6. Reply in simple English: what updated, one line each, or "Nothing new today."
```

## 3. Weekly check of Loc's updates
taskId `{P}-weekly-loc-updates`, cron `23 10 * * 2` (Tuesdays 10:23, the day after Loc's Monday refresh), description "Weekly: lists what is new in Loc's shared llllloc, so the owner picks what to take."

```
Weekly check of what Loc changed in his shared llllloc (the public GitHub repo 123loc321/llllloc-skills and his Drive shared copy). This system started as a copy of it. NEVER CHANGE THE SYSTEM IN THIS RUN: only report. Work in {BRAIN}. Load the router as usual ({P}:router, {P}:project-workflow, {P}:task-skill-creator).
Everything goes into ~/Desktop/Scheduled tasks_Loc updates/<YYYY-MM-DD>/ and nowhere else.
1. Run: python3 -I "{KIT}/check_upstream.py" "<that folder, full path>"
   It writes REPORT.md (Loc's commits, every changed file in Loc's names and in yours, and whether you changed your own copy) and upstream.patch (every change, already in your names). "No new commits" and no Drive changes: reply "No new updates from Loc this week." and stop.
2. Read upstream.patch. For each changed skill or file, write at the top of REPORT.md one plain line: what Loc changed and what it would change for the owner. Group them: Worth taking, Maybe, Probably not (Loc-only: his clients, his apps, his accounts). Mark every row "untouched: safe to take" or "you changed it: merge by hand" as REPORT.md says.
3. Reply in simple English with the grouped list, numbered. End with: "Reply with the numbers you want. Nothing is changed until you say so."
Later, when the owner answers with numbers (in a normal session, not this task): for an "untouched" file run python3 -I "{KIT}/check_upstream.py" --take "<Loc's path>" (the old copy goes to Old/). For "you changed it", merge by hand with {P}:task-skill-creator REFINE. Then deliver as that skill says (commit and push when the folder has a .git).
```
