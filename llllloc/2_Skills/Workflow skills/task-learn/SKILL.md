---
name: task-learn
description: "Deep-studies one finished llllloc thread and turns what went wrong, and what worked, into numbered changes to the workflow he can accept line by line. Measures the thread from its own transcript, finds the root cause of each correction (often a wrong rule inside a skill), names the one file that owns each fix, then applies only the lines he answers ok. Use when he sends only the word learn, types llllloc:task-learn, or asks to deep study a thread and suggest what to add to the workflow. Never runs on its own, never on a sentence that only contains the word learn, and never changes a file before his ok."
---

# llllloc:task-learn (22 Oct 2026)

A thread that taught something pays for itself only when the lesson reaches the file that owns it. This skill finds those lessons, proves each with numbers from the thread, and hands them to him as short lines he answers with `ok`, `skip` or his own words.

## TOP RULES

1. Nothing changes before his answer. The study ends with `Nothing is changed. Reply to each line: ok, skip, or your words.` Why: a rule change alters every later thread, and that call is his.
2. Root cause before fix. Every finding names WHY it happened and quotes the line that caused it. Why: in the RB06 thread two of his corrections came from a wrong rule inside a skill. A new rule on top would have fought the wrong one.
3. Evidence is a tool result. A count, a time, a quote of his words, a file and line. "Felt slow" is not a finding. Never write a finding for something that did not happen.
4. Fix the old line before adding a new one. A rule that existed and was missed gets a check step with a go-back line, never more words (house rule). A wrong rule gets rewritten. Only a gap gets a new line, paid for by a cut.
5. Better, never bigger. At most 9 suggestions. The ones that do not make the cut go to the study file under "Also seen".

## STEPS

Copy this checklist into your notes and tick it:

```
- [ ] 1 Evidence gathered in one tool block
- [ ] 2 Moments listed: corrections, repeats, undos, waste, skips, wins
- [ ] 3 Root cause and owner file for each
- [ ] 4 Each fix checked against the files and the learn log
- [ ] 5 Study file written, reply sent. STOP.
- [ ] 6 His ok lines applied, each through its channel
- [ ] 7 Logged
```

### 1. Gather the evidence (one tool block, core rule 17)

- Run `python3 -I thread_scan.py` in this skill's Base directory. It reads this session's transcript, `~/.claude/projects/<folder key>/$CLAUDE_CODE_SESSION_ID.jsonl` (29 Oct 2026), which keeps every turn, also the ones a compacted chat forgot. It prints his messages with correction marks, every Skill call, the rule 9 and Loaded line checks, tool cost, errors, results over 20,000 characters, repeated calls and compactions.
- His exact words: a message the scan cut at 300 characters is read in full in the transcript.
- The learn log `llllloc_workflow/1_Lessons/Learn log.tsv`.
- Another session named: pass its id to the scan (find it with `mcp__ccd_session_mgmt__list_sessions`, untested, Mac test list).

No transcript: work from this session's context and say so in the study.

### 2. List the moments

Read the thread as a cost sheet. One line per moment, with its time:

| Kind | The sign |
|---|---|
| CORRECTION | He said no, wrong, again, I said, you skipped |
| REPEAT | He asked for the same thing twice |
| UNDO | He rejected or reverted something made |
| WASTE | A result over 20,000 characters, a call made twice, a compaction, a round trip that bought nothing |
| SKIP | A rule 9 or Loaded line failure from the scan, research or a check that did not run |
| WIN | A method that worked first time, a measured result he approved |

Wins count. A method that worked is worth keeping as much as a mistake is worth fixing.

### 3. Root cause and owner

For each moment ask why, up to three times, until the answer is a file, a missing file, or a program fact. Then put it in one class:

| Class | Meaning | The fix goes |
|---|---|---|
| WRONG RULE | A skill or file told Claude the wrong thing | Rewrite that line. Quote file and line (`grep -n`) |
| MISSED RULE | The rule exists and was skipped | A check step with a go-back line, or a TESTSET line |
| MISSING RULE | No file covers it | One dated line in the owner, paid for by a cut |
| TOOL TRAP | A program behaves in a way Claude did not know | The tool skill TRAPS list, or `4_Lessons/Programs/<Program>/` |
| METHOD | A craft method that worked better | The job's method file, or the task skill that owns the craft |
| COST | Time or tokens spent for nothing | The step or tool skill that caused it |

The owner file comes from `llllloc:task-workflow-best-practices` UPDATE step 1: one home per rule. Every finding ends in one of three ways: a file fix, a TESTSET line (`llllloc:task-skill-creator` kit), or no change.

### 4. Check each fix before it is shown

1. `grep` the key words across the skills (`llllloc/2_Skills/`, the master of the plugin), the core rule and the method files. Found: it is a MISSED or WRONG rule, not a missing one.
2. Read the learn log. A fix applied before whose fault came back means the fix did not work: propose a check step or a test, never the same words again. A line he skipped before is not offered again unless the fault grew.
3. A fix with no clear answer gets research (`llllloc:task-research`) and a label: DOCS, PRACTITIONER or HYPOTHESIS. A HYPOTHESIS names the test that settles it.
4. Rank by effect: times it happened, multiplied by what it cost him (a round of his notes beats a wasted call).

### 5. Write the study, reply, stop

The study file is `LEARN_<thread title>_<YYMMDD>.md`, written straight to `llllloc_workflow/5_Old reports/` and sent with `llllloc:task-sending-files`. It holds, in this order:

1. What went wrong, and why: one table, moment, times, class, root cause.
2. Suggestions, biggest effect first. Each: the change in one line, the owner file, the new text drafted in full, what it buys with a number, its label.
3. What worked and why: the wins worth keeping.
4. Also seen: findings that did not make the top 9.
5. Only he can decide: choices that change his goal.
6. `Nothing is changed. Reply to each line: ok, skip, or your words.`

The chat reply: the main finding in two sentences, then the top suggestions as numbered lines of 15 words or fewer, each line able to stand alone, so he can reply to each one. Then the rule 1 closing line. Stop and wait.

### 6. Apply what he answers

- `ok` or his words: apply through the channel `llllloc:task-workflow-best-practices` names for that part. A skill change goes through `llllloc:task-skill-creator` DELIVER. A method file is edited in place, its old copy in `Old/`. A core rule change: the full draft in the chat, then that skill's core rule row on his yes.
- `skip`: change nothing.
- Every answered line, ok or skip, gets one row in the learn log.
- Check: count the ok lines against the changes made. One is missing: go back to step 6.

### 7. Log

1. Append to `llllloc_workflow/1_Lessons/Learn log.tsv`, one row per suggestion: `date | thread | finding | class | owner file | ok or skip`. No file yet: start it with that header.
2. Append one dated section to `Lessons_Workflow.md`: what the study found, what changed.
3. His exact words go to `Your words.md`.

## WITH END

`learn` comes before `end`. When `end` runs after `learn`, its WRAP-UP and workflow lesson are already done: `llllloc:end` writes `Workflow: see learn` and moves on.

## THE REPLY

The two-sentence finding, the numbered lines, the closing line, then the router STEP 4 Loaded and Time lines.
