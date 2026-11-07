---
name: task-skill-creator
description: "Audits, creates and updates the skills of the llllloc workflow against Anthropic's current skill-writing rules and the llllloc house rules. Every skill change ships by commit and push to GitHub, and the llllloc plugin syncs it to every account."
---

# llllloc:task-skill-creator

Keeps every skill in the best shape for the Claude model he runs today. A skill is a contents page, not a manual: the description gets it picked, SKILL.md says what to do, and detail waits in a file until a step needs it.

## RULES FOR EVERY MODE

1. Report before you change. In AUDIT, change nothing until he picks fixes by number. Why: a skill change alters every future chat, and that call is his. A direct order to fix one named problem is already the yes.
2. One delivery path: GitHub (6 Nov 2026, his words: skills come from git, no doubles). Every skill lives in `llllloc/2_Skills/<group>/<name>/` and ships as the `llllloc` plugin from the private repo `123loc321/llllloc`. Delivery is: write the Mac master, then commit and push to `main`. Every Mac loads it from GitHub through the Claude Code marketplace `llllloc-brain` (git source, auto-update on; Customize > Plugins > Update now for at once), and a new session loads it as `llllloc:<name>`. One Mac never registers the same marketplace name twice (a local folder route and the GitHub route clash, tested 6 Nov 2026). A new skill also gets its path in `.claude-plugin/marketplace.json`, or it never loads. Never write into `~/.claude/skills/` and never upload a `.skill` by hand: either makes the same skill show twice. Say a change is pushed, never that it is live, until a new session shows it. Steps: DELIVER below.
3. Absorb, do not layer. Fold new guidance into the rule it refines. Delete what it replaces. The file holds its length or gets shorter.
4. Test before you delete. A line that looks useless can hold one edge case. Cut a rule for being "too detailed for the new model" only after the test in `testing.md`, or on his word.
5. A fact about Claude is looked up. Read `llllloc_workflow/2_Research cache/skill-authoring/_TOPICS.md` first, then only the topic files the change needs. A line older than 14 days, or a new Claude model, means MODEL CHECK below runs before any rule is quoted.
6. Never cut a hard stop. Never cut a rule he set in words this month. Never write a receipt for a check that did not run.

## THE KIT

The kit is `llllloc/2_Skills/Workflow skills/task-skill-creator/`. The brain folder is the main folder of the session. Read one file per task, in full.

| Task | Read |
|---|---|
| Mark rules in an audit, or check a finished skill | `audit-checklist.md` (every rule with its ID, reason and source, the house rules H1 to H9, what differs in the Claude app, the report format) |
| Write or rewrite a skill | `authoring-guide.md` |
| Write tests, cut rules as too detailed, or run the old-against-new test on `TESTSET.md` | `testing.md` |
| The mechanical check | Run `validate_skill.py`. Do not read it. |

Run the validator on the Mac, on the Mac master `llllloc/2_Skills/<group>/<skill-name>/` (the plugin is synced from it):

```
python3 -I "$HOME/Desktop/Claude/llllloc/2_Skills/Workflow skills/task-skill-creator/validate_skill.py" "<skill folder>"
```

A draft is checked the same way: write it to `<scratch>/<skill-name>/SKILL.md` and point the validator at that folder. Python 3.8 or newer. Nothing to install.

## PICK THE MODE

| Mode | When | He gets |
|---|---|---|
| AUDIT | Check one skill, some skills, or all of them | A report. Then only the fixes he picks. |
| NEW | No skill covers the job | The skill, its router row and its marketplace line in one pushed commit, four test prompts |
| REFINE | A skill missed, or he corrected it | The same skill rewritten around the reason. Not longer. |
| MODEL CHECK | A new Claude model or app update, or the cache line is over 14 days old | The changed rules, then AUDIT against them |

"Improve this skill" and "update all my skills" mean AUDIT, then REFINE with the fixes he picks.

## AUDIT

Copy this checklist into your working notes and tick it:

```
- [ ] 1 Validator run on every skill in scope
- [ ] 2 Each skill in scope read in full
- [ ] 3 Every rule marked PASS, FAIL or N/A with file and line
- [ ] 3b Every path the skill writes to listed: job or universal (H10)
- [ ] 4 Report sent. STOP.
- [ ] 5 He picked numbers
- [ ] 6 Picked fixes applied and delivered (DELIVER)
- [ ] 7 Every changed skill is in the pushed commit
```

1. Scope. One named skill: that skill. "All": every skill the router names. Run the validator on each.
2. Read in full only the skills that will get a report row with a fail. For a library, read in full the five with the most findings, and mark the others from the validator, `wc -c` and `grep`.
3. Mark every rule in `audit-checklist.md`. A script rule takes the validator result. A read rule needs a file and a line. "Looks fine" is not evidence. HK1 applies: hooks work in the Code tab (THE CODE TAB below).
   H10 is always read, never skipped: list every path the skill writes to and mark each one job or universal. A job's output (sheets, raw reads, batches, Claude screenshots, specs) under `llllloc/` is a fail, because llllloc holds only what is universal (his words, 17 Oct 2026).
4. Report in the chat. One table: skill, number of fails, worst problem. Then every fix in one numbered list, biggest effect first. Each fix names the skill, the rule ID and the change in one line. Then the items only he can decide. End with: `Nothing is changed. Reply with the numbers.`
5. Stop. Wait for the numbers.
6. Apply with REFINE, then DELIVER. Any number of skills in one turn.
7. Count the skills in the pushed commit against the list of changed skills. One is missing: go back to step 6.

## NEW

```
- [ ] 1 The job done once with no skill. Gaps written down.
- [ ] 2 Three test prompts and one that must not trigger
- [ ] 3 Shape chosen: one file, or a body plus task files
- [ ] 4 Description, then body
- [ ] 5 Validator clean on the draft
- [ ] 6 Audit checklist passed, house rules too
- [ ] 7 Delivered: the skill and the router, one `.skill` each
```

1. Evidence first. Read how the job went in this chat or in a handoff. List only what Claude got wrong or had to be told. That list is the skill. Why: a skill that restates what Claude already does is paid for on every turn and buys nothing.
2. Write the tests before the skill, in `llllloc/2_Skills/<group>/<skill-name>/TESTS.md`.
3. Shape: `authoring-guide.md`, "In the llllloc workflow". A task that costs money, sends, publishes or moves files gets exact steps and a check. A creative task gets a goal and room.
4. Write the description first. Then the body: top rules, task table, steps with a go-back line, output.
5. Validate. An error: go back to step 4.
6. Mark the checklist. A fail: go back to step 4.
7. DELIVER the skill, the router with its new row and the marketplace line, in one commit.

## REFINE

1. Name the evidence in one line: what happened, what he said.
2. Find the reason behind it. If you cannot name the reason, you are not ready to edit.
3. Rewrite every line the reason touches. Delete what the rewrite makes redundant. Move a rule that was missed toward the top. A rule that was missed twice does not get more words: it gets a check step with a go-back line.
4. Count it with `wc -c`. Longer than before: find what the new rule replaced, and go back to step 3.
5. DELIVER. His exact words go to `llllloc_workflow/1_Lessons/Your words.md`.

## DELIVER

Every mode ends here. Exact steps, because a skill that is not pushed never reaches his other accounts.

```
- [ ] 1 Work copy built from the Mac master
- [ ] 2 No line lost
- [ ] 3 Validator clean
- [ ] 4 Description counted, under 1,024
- [ ] 5 Backed up in the version folder, new files written
- [ ] 6 Committed and pushed
- [ ] 7 marketplace.json lists every skill folder
```

1. Work copy. Copy the Mac master `llllloc/2_Skills/<group>/<skill-name>/` to `<scratch>/<skill-name>`. A new skill: make the folder. Edit the copy with the Edit tool or a script. Never retype a file from memory or from tool output.
2. No line lost. Compare with a script: every line of the old SKILL.md is in the new folder, or on the list of lines you meant to change. A lost line: put it back, then check again.
3. VALIDATE the folder (THE KIT). A new error or warning: fix it, then validate again.
4. COUNT the description out of the new file. Over 1,024 characters: cut, then count again.
5. Back up (H8): the old Mac copy goes to `llllloc/2_Skills/<group>/<skill-name>/Old/<YYMMDD>_before_<change>/`, then the new files and a one-line-per-change `NOTES.md` replace it, written straight to the Mac. A new skill: add `./llllloc/2_Skills/<group>/<skill-name>` to `.claude-plugin/marketplace.json`.
6. Push the moment the skill is written, the same turn, no asking, never left for `end` (6 Nov 2026, his words): in the brain folder, `git add` the skill folder (and `marketplace.json`), commit `Skill <name>: <change>`, push to `origin main`. A push refused: `git pull --rebase`, then push again.
7. Check: `git status -sb` shows `main...origin/main` with nothing ahead, and every skill folder has its line in `marketplace.json`. One is missing: go back to step 5. The reply names the commit and says the change reaches a new session after the plugin syncs.

## MODEL CHECK

1. Fetch the four sources at the end of `audit-checklist.md`, plus the prompting guide of the model he runs now. Use one tool block.
2. Compare with the kit. List only what changed: a limit, a field, a new behavior, a rule that is gone.
3. Update the kit file that owns each changed rule, in place. Replace the matching line in its topic file under `llllloc_workflow/2_Research cache/skill-authoring/`.
4. Report the changes in five lines or fewer, then run AUDIT against the new rules.

## THE RULES ON ONE SCREEN

Enough for a small fix. The kit holds the reasons and the checks.

1. Skill.md under 500 lines and under 16,500 characters (HARD: all of it comes back after compacting). Description under 1,024 (HARD, enforced). Other size numbers are warnings (21 Oct 2026). Every other file is linked straight from SKILL.md, one level deep. Claude may read only the first 100 lines of a file it reached through another file.
2. A file over 100 lines opens with a contents list.
3. Detail matches risk. Exact steps where a mistake costs money, a client or a file. A plain goal where many ways work.
4. Skills written for older models are often too detailed for Fable 5 and the 5.5 models, and can make the work worse. Test with the detail removed.
5. Keep only what Claude cannot work out alone: his prices, names, paths, taste, decisions. Description in the third person: what it does and when it runs.
6. A job with many steps gets numbered steps, a checklist to tick, and a go-back line after each check.
7. Quality work runs check, fix, repeat until it passes. The check can be a list to compare against.
8. A template says how strict it is. Style is shown with input and output pairs. A job that branches names the fork first.
9. Name every tool or package the skill needs, with its install line. Forward slashes in paths.
10. A rule that must hold every time needs more than capitals: a hook (THE CODE TAB below).
11. Three test prompts before the skill is written. No with-and-without-skill test (his word, 16 Oct 2026). A change is tested old version against new on `TESTSET.md`, as `testing.md` says (21 Oct 2026).
12. The most important rules sit at the top. After a compacted chat only about the first 5,000 tokens of a skill stay.
13. Never ask Claude to write out its reasoning in the reply. The newest models can decline the whole request. A short explanation of the answer is fine.

## THE CODE TAB (29 Oct 2026)

- Skill delivery: rule 2 and DELIVER.
- Skill names: every llllloc skill loads as `llllloc:<name>` from the plugin (6 Nov 2026). Write that full name in skills.
- Write two frontmatter fields: `name` and `description`.
- Hooks work here: a hook in `Desktop/Claude/.claude/settings.json` fires in every session of the brain folder (the router hook, tested 29 Oct 2026). A must-hold rule can get a hook, with his yes. It also goes in the first lines of SKILL.md with its reason and a check step with a go-back line.
- Tested on his Mac 29 Oct 2026: a file card opens a side panel with Show in Finder, and a `.skill` card has no save button. Rename and mark done work at `end`. `request_access` shows its Allow card in the same chat. A dropped document is read where it lives. A dropped picture sits in a temporary session folder: copy it into the job folder. The core rule survives compacting. A side session starts and answers.
- No skill fires by its description. A new skill needs its router row, or it never loads.
- How this app behaves is a fact with a date on it. Before you tell him a button, a card or a setting exists, find it in a doc or in his own screenshot. "The tool said shown" is not proof that he saw it.

## THE REPLY

The report or the pushed commit, plus one line. A skill change is listed one line per skill: name, what changed, characters before and after.