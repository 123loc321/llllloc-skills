---
name: task-workflow-best-practices
description: "Holds the best practice for the llllloc workflow and keeps it fast and correct: the core rule, the router, every skill, the llllloc folders, the research cache and the maps. Runs on its name, check my workflow, update overall rule, and at every end. Only llllloc:task-workflow-update, the big upgrade, changes its best practice."
---

# llllloc:task-workflow-best-practices

The workflow is everything Claude reads before it does his work. This skill keeps that set small, true and fast. Speed comes from loading less text, never from skipping a check. It owns BEST PRACTICE below and runs the routine check-up. The occasional big upgrade is `llllloc:task-workflow-update` (14 Oct 2026). Each Claude project keeps its own workflow-rule skill in this shape. This one belongs to llllloc.

## RULES FOR EVERY MODE

1. Measure, never guess. Every finding carries a count, a file and a line. "Feels long" is not a finding. Why: he acts on numbers, and a guess about a rule file breaks every chat after it.
2. Report, then change. HEALTH ends with numbered changes and stops. He picks numbers. WRAP-UP hands each trim back through its channel in the same pass: his save is the yes. A dead path in a map or a pointer is fixed in the same pass and reported in one line.
3. One home per rule. The rule text lives in the file that owns it. Every other file carries a one-line pointer or nothing. Two copies drift apart, and two similar rules compete.
4. EVERY RULE ADDED IS PAID FOR by one rule cut or merged. Net length holds or falls.
5. Never cut a hard stop. Never cut a rule he set in words this month. Never invent a trim to fill a step: `Workflow: nothing to trim` is a finished answer.
6. Skill text changes only through `llllloc:task-skill-creator`. Load it for any step that edits a skill.

## THE PARTS, THEIR CAPS, THEIR CHANNELS

Root: `~/Desktop/Claude`, with `llllloc/` (what Claude reads to do a job) and `llllloc_workflow/` (the workflow as a project). It is the main folder of every Code tab session.

| Part | Where | Cap | A change goes back as |
|---|---|---|---|
| The core rule | `llllloc/1_Core rule/Core Rule.md`, copied into `AGENTS.md` by `brain_check.py`; `CLAUDE.md` loads `AGENTS.md` (6 Nov 2026) | WARNING: 3,500 characters and 20 rules (15 Oct 2026). No Claude limit behind them. | The FULL new text in the chat, never a diff. After his yes: old version to `llllloc_workflow/4_Versions/Core rule/` with its date, new text to `Core Rule.md`. |
| Router | skill `llllloc:router` | WARNING: 4,000 characters | Commit and push, the plugin syncs (`llllloc:task-skill-creator` DELIVER) |
| Project skills | `llllloc:project-creatives`, `-code`, `-workflow`, and `llllloc:task-sending-files` | WARNING: 6,500 characters each, top rules first | Commit and push, the plugin updates from GitHub (`llllloc:task-skill-creator` DELIVER) |
| Skills | the `llllloc` plugin from GitHub (marketplace `llllloc-brain`, git source, auto-update, 6 Nov 2026), master `llllloc/2_Skills/<group>/<name>/`. Never a copy in `~/.claude/skills/` and never the same marketplace name twice on one Mac | HARD: description under 1,024 characters (enforced). SKILL.md under 16,500 characters, so all of it comes back after compacting (5,000 tokens per skill, 25,000 for all). | Commit and push through `llllloc:task-skill-creator` DELIVER (6 Nov 2026). |
| Skill kits and versions | `llllloc/2_Skills/<group>/<name>/` and its `Old/` | A file over 100 lines opens with a contents list | Edit in place. Old versions go to `Old/`. |
| Program how-tos | `llllloc/4_Lessons/Programs/<Program>/` | Same | Edit in place |
| Workflow lessons | `llllloc_workflow/1_Lessons/Lessons_Workflow.md` | One short dated section per lesson. Sections over 30 days old move to `llllloc_workflow/5_Old reports/` (21 Oct 2026) | Append only |
| His words | `llllloc_workflow/1_Lessons/Your words.md` | Archive. Nobody reads it unless a rule is questioned. | Append only |
| Research cache | `llllloc/5_Research cache/<folder>/<subject>.md`, or `<subject>/<topic>.md` with `_TOPICS.md` once big, universal only | 60 lines or 6 KB per file, 60 days per line, 14 for Claude | Shell append, or python edit in place |
| Maps | `llllloc/3_Project maps/Project map_Creatives.md` and `Project map_Code.md` | One row per project or job | Read right before writing, then write the row |
| Saved preferences | Claude memory | Pointers only. The rule text lives in a skill or in `llllloc/`. | Only on his word |
| Project memory | `MEMORY.md` and one file per memory | HARD: one line per memory, every file listed, under 200 lines and 25 KB. A file under 4 KB. | Edit the memory files |

## PICK THE MODE

| Mode | When | He gets |
|---|---|---|
| HEALTH | "Check my workflow", or no health run for a month | A measured report, numbered changes, then the picked ones applied |
| UPDATE | He gives a new rule, or one change touches more than one file | The rule in its one home, every other home fixed, one line per file |
| WRAP-UP | The end of a thread, from `llllloc:end`, or on his tag | Six lines at most, plus each trim through its channel |

## HEALTH

Copy this checklist into your working notes and tick it:

```
- [ ] 1 Sizes measured against the caps
- [ ] 2 Validator run on every router skill
- [ ] 3 Router and installed skills compared
- [ ] 4 Every named path checked
- [ ] 5 Duplicate rules counted
- [ ] 6 Last review date checked
- [ ] 6b Research run on every finding with no clear fix
- [ ] 7 Report sent. STOP.
- [ ] 8 Picked numbers applied, each through its channel
- [ ] 9 Measured again
- [ ] 10 Logged
```

1. Sizes. One command for the skills, one for the Mac files: `wc -c` on the installed `llllloc*` and `ponytail*` SKILL.md files (THE PARTS, Skills row), and `wc -c` on the core rule, `wc -l` on `Lessons_Workflow.md` and each cache file. Count the rules too, not only characters, and check the most important ones sit at the top. A HARD cap that fails is FAIL, fixed now. A WARNING is trimmed only when the test set shows the trim is no worse (21 Oct 2026). Rules over 60 days old that no thread needed go on a list for his decision.
2. Validator. Run it as `llllloc:task-skill-creator` THE KIT says, on every skill the router names.
3. Router. Every skill in the router table is installed. Every installed `llllloc-*` and `ponytail*` skill has a row, or sits in the tag-only list, or in the never-pick list. Every skill the core rule names exists. `ls ~/.claude/skills/` holds no `llllloc:router` skill.
4. Paths. `grep` the Mac paths out of the core rule, the project skills and each SKILL.md. `ls` each one. A path that fails is a finding. A skill that still names `llllloc brain`, `02_Technical`, `PROJECT-LOCATION.md`, `JOBS.md`, `_SENT.tsv` or a retired skill name is a finding (15 Oct 2026). So is a folder name from before FOLDERS v19: `knowledge/`, `0_Instructions backup`, `llllloc_workflow/Handoffs/`, `Reports/`, `Versions/`, `Installers/`, `_CLAUDE/Handoffs/`, `_OLDER`, `_SHOTS`, `UNTESTED.md` (16 Oct 2026), `0_Instructions`, `2_MCP`. So is a skill name from before the rename of 17 Oct 2026: an `llllloc-` name with no `task-`, `tool-`, `project-` or `references-` part, except `llllloc:router`, `llllloc:end`, `llllloc:end-plugin-log` and `llllloc:fundamental`.
5. Duplicates. For each rule in the core and the project skills, `grep` its key phrase across the skills. Count the homes. Two homes with full text is a finding. Also `grep` the retired names the router lists.
6. Last review (14 Oct 2026). `grep` the newest `REVIEW` date in `Lessons_Workflow.md`. Over 30 days old, or a new Claude model or app update since then: the report opens with `Run llllloc:task-workflow-update.` The full docs sweep belongs to that skill, not to HEALTH. Run MODEL CHECK in `llllloc:task-skill-creator` when its cache line is over 14 days old.
6b. RESEARCH (14 Oct 2026). Every finding with no clear fix, with no search cap: the cache first, then `llllloc:task-research`. Label each change DOCS, PRACTITIONER or HYPOTHESIS. A HYPOTHESIS change ships with the test that would settle it. Prefer delete, merge, narrow, load on demand, then add.
7. REPORT in the chat. One table: part, measure, cap, PASS or FAIL. Then one numbered list of changes, biggest effect first. Each change names the file, the cut or the fix, and what it buys in one line. Then the items only he can decide. End with: `Nothing is changed. Reply with the numbers.` Stop.
8. APPLY the numbers he picks, each through its channel in the table above.
9. Measure again. Run steps 1 and 2 on what changed. A cap that still fails, or a new validator error: go back to step 8.
10. LOG. One dated section in `Lessons_Workflow.md`: what was measured, what changed. His exact words to `Your words.md`. Changed skills get their `Old/` copy.

## UPDATE

1. Name the owner. A rule about a program lives in that program's skill. A rule true for every job lives in the core (paid for by a cut, under 20 rules). A rule for one kind of task lives in its project skill. A rule about skills lives in `llllloc:task-skill-creator`. A rule about the workflow lives in `llllloc:project-workflow` or here. Unclear: ask which one. Never guess.
2. Find every home. `grep` the rule's key words across the core, the project skills, every SKILL.md and the kits. List the hits.
3. Write the rule once, in the owner: what to do, why when it is not obvious, the date. Pay for it with a cut.
4. Fix every other home: a one-line pointer, or delete the old copy. A rule that conflicts with the new one goes, and the reply says so.
5. Check. Run the same `grep` again. More than one home with full text: go back to step 4.
6. Reply with the cascade, one line per file touched. His exact words go to `Your words.md`.

## WRAP-UP

Read the thread once as a cost sheet. Write a line only where the answer is not "nothing":

1. What loaded and was not used? A skill, a file, a folder, a search, a permission card.
2. What did he say twice? A second ask means a rule is missing, or too long to find.
3. What did he undo or reject? A companion file, a question, a receipt, a row, a story.
4. What took a round trip and bought nothing? A check run twice, a question the thread had answered.
5. Which rule text is longer than the rule it carries?
6. Which answer wasted tool calls or skipped research? Calls that bought nothing, a search the cache had answered, or a job that made something with no research. Name the cause.

Each finding ends in one of three ways only (21 Oct 2026): a skill fix, a new message in the test set (`llllloc:task-skill-creator` kit, `TESTSET.md`), or "no change". Then hand each trim back through its channel. In the reply the wrap-up is six lines at most: what was cut, what was added, where, and which answer wasted calls or skipped research.

## BEST PRACTICE

The current best way to run the llllloc workflow inside its Claude project. HEALTH measures against this list. Only `llllloc:task-workflow-update` adds, changes or removes a line, each with its date and source (14 Oct 2026).

From the review of 15 Oct 2026 (Anthropic docs and two studies):
- The always-on text is the core rule only: under 3,500 characters and 20 rules. Full compliance falls from 94 percent at 10 rules to 24 percent at 40 (arXiv 2607.19257). Hard stops first, because the last rules in a block fail about three times more often (arXiv 2507.11538).
- Task rules are skills, not plain files: a skill has a trigger and stays in context once loaded (code.claude.com/docs/en/skills). The router loads one per thread.
- Compacting: core rule 13. After compacting, the skill list comes back and each loaded skill keeps its first 5,000 tokens, 25,000 for all: keep skills short, top rules first (Claude Code 2.1.304, code.claude.com/docs/en/skills). A long thread idle about 54 minutes compacts on its own (2.1.299, 21 Oct 2026).
- A core change reaches new sessions only: `CLAUDE.md` and its imports load at session start (code.claude.com/docs/en/memory, 29 Oct 2026).
- The router hook in `Desktop/Claude/.claude/settings.json` fires on every message (tested 29 Oct 2026, code.claude.com/docs/en/hooks). Core rule 9's Loaded and Time lines stay the visible check.

From the review of 17 Oct 2026 (speed):
- Never cap time or words. Anthropic's own effort cut and word cap both lowered quality and were undone (anthropic.com/engineering/april-23-postmortem). Speed comes from core rule 17.
- To go faster, lower effort first: the session's effort in the model menu, Medium, High in a big job's session (29 Oct 2026). Effort cuts waiting more reliably than prompt words (platform.claude.com/docs, Prompting Claude Opus 5.5).
- Ask for ambition plainly. Never add generic verify or double-check lines, and never send a helper only to re-read the work (platform.claude.com/docs, Prompting Claude Opus 5, 18 Oct 2026). A check is a tool run: a validator, a render, a screenshot, a measurement. A plain re-read can make answers worse (Huang et al., ICLR 2024, arXiv 2310.01798).

From the review of 18 Oct 2026 (ambition and parallel threads):
- Aim higher, not bigger: the goal behind the ask, the top expert's method from the rawest material, other fields' methods, never their voice (felixrieseberg.com, 13 Oct 2026). Core rule 11 holds it, `llllloc:task-be-ambitious` the full method. A judge needs real proof, or it gives an opinion (promptedbyeric.substack.com, 16 Oct 2026).
- Parallel threads pay only for parts that share no file and no choices. Multi-agent work costs about 15 times the tokens of a chat (anthropic.com/engineering/multi-agent-research-system). A thread limit is a preference, not a cap (code.claude.com/docs/en/claude-projects). The rules: `llllloc:project-workflow` SPLIT.

From the review of 21 Oct 2026 (memory, caps, tests):
- The memory index holds one line per memory, and every memory file is listed. Threads read `MEMORY.md` at start, files on demand (code.claude.com/docs/en/claude-projects, /memory).
- Caps are HARD when Claude enforces them or cuts text past them, WARNING when they are our own numbers. A warning is trimmed only after a test (his ok, 21 Oct 2026).
- In the Code tab `CLAUDE.md` and its imports load in full, each file under 200 lines (code.claude.com/docs/en/memory, 29 Oct 2026). The 8,000-byte cap was for cloud threads only.
- A change is tested old version against new version on the test set, never with and without the skill (his word, 16 Oct 2026). Anthropic: 20 to 50 cases from real failures is enough to start (anthropic.com/engineering/demystifying-evals-for-ai-agents).
- A rule added for one incident carries its date. A rule no thread needed in 60 days goes on his review list (Google drops code checks people act on less than 90 percent of the time, research.google.com/pubs/archive/43322.pdf).
- A scheduled task's thread stops at a usage limit, it does not wait (code.claude.com/docs/en/claude-projects). A daily task reports a missed day.

From the Anthropic docs:
- Skill.md stays under 500 lines. Detail goes in files linked one level deep, read only when a step needs them. (14 Oct 2026, platform.claude.com/docs, Skill authoring best practices)
- A description says what the skill does and when to use it, in the third person, the key use first. Claude Code cuts the description at 1,536 characters in its listing. (14 Oct 2026, both pages)
- Write three test prompts before a skill, and test it on the models in use. (14 Oct 2026, platform.claude.com/docs, Skill authoring best practices)

House rules:
- A story is not a rule. Keep the rule as one dated line. The story goes to `llllloc_workflow/1_Lessons/Lessons_Workflow.md`.
- Two rules that overlap become one. Two rules that conflict: keep the newer one, and say so.
- A rule the model already follows unasked is a rule to delete, after a test or on his word. The newest Claude models do worse with too much detail, so an old step-by-step rule is the first place to look.
- A rule nobody can test is a rule to rewrite: name the count, the file or the line that proves it ran.
- A rule that keeps being missed does not get more words or capitals. It moves to the top of its file, or it gets a check step with a go-back line.
- Prefer the positive form of a rule where it reads naturally.
- A deliverable he cannot use in one click is not delivered. Before the reply, name the button or the path he will use, and the proof that it exists (a doc line or his screenshot).

## THE REPLY

The report or the cascade, plus one line. Every file written is named with its full path.