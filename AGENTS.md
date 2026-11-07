# llllloc brain: start here

This folder holds the rules, skills, maps and notes of **llllloc**, a video, motion and design studio run by Loc. Any AI app (Claude, ChatGPT, Codex, Cursor, Copilot, Gemini, DeepSeek) reads this file first.

**Where things live (6 Nov 2026, his words: "skill on github, the rest in my mac, then google drive as 2nd backup").** The Mac folder `~/Desktop/Claude` is the main place and holds everything. The GitHub repo `123loc321/llllloc`, branch `main`, holds only the llllloc plugin: `llllloc/2_Skills/`, `llllloc/1_Core rule/` (core rule and hooks), `.claude-plugin/`, `.agents/` and this file. A session pulls them when it starts, a skill change is pushed at once. The Google Drive folder `*llllloc_System_Full backup` holds a one-way copy of the whole folder (`llllloc/8_Scheduled tasks/Drive backup/drive_backup.sh`). A cloud session sees only the skills, never memory or maps, and never pushes straight to `main`: it proposes a branch or a pull request. Friends get a cleaned copy of the plugin from the PUBLIC repo `123loc321/llllloc-skills` (marketplace `llllloc-skills`), refreshed every Monday by `llllloc/8_Scheduled tasks/Drive backup/shared_repo_push.py` (7 Nov 2026). Never add that marketplace on his own Macs: every skill would show twice. A friend makes the copy their own with `SETUP.md` PART B (their name in place of llllloc, their own GitHub, Drive backup, weekly tasks), then sees Loc's changes each Tuesday and picks what to take (`llllloc/1_Core rule/friend kit/`).

## First session on a new Mac or account (7 Nov 2026)
His words: "when i switch to another claude account i can just pick the claude folder on my desktop and you will auto understand what to do". A first session shows one of two signs: your skill list has no `llllloc:router`, or the session start printed "this Mac is not set up for this brain folder yet". Then, before the job: say so in one line, follow `SETUP.md` in this folder, then do the job. He pasted a Google Drive link instead: read `START HERE.md` at the top of that Drive folder and follow it. It never overwrites a newer Mac copy.

## Read in this order
1. The core rule below. It wins over everything else. Its master file is `llllloc/1_Core rule/Core Rule.md`.
2. The router: `llllloc:router` in Claude, or the file `llllloc/2_Skills/Workflow skills/router/SKILL.md`. It says which skill a task needs.
3. The skill the router names, then only the files that skill points to.
4. `llllloc/3_Project maps/`: where every project, folder and app lives on the Mac.
5. Memory: `llllloc/9_Memory/MEMORY.md`, the index of what Claude has learned about him and his work.

## Skills
- In Claude every skill is `llllloc:<name>`, from the `llllloc` plugin that claude.ai syncs from this repo (`.claude-plugin/marketplace.json`). The master of each skill is `llllloc/2_Skills/<group>/<name>/SKILL.md`. Change a skill by editing that file, then commit and push.
- Never write a skill into `~/.claude/skills/` and never upload a `.skill` by hand: the same skill would show twice.

## If you are not Claude (Codex, Gemini, Cursor, Copilot, DeepSeek in another app)
- You have no Skill tool. Open the router file named above and read it as your checklist. A skill named `llllloc:<name>` is the folder `.agents/skills/<name>/`: read its `SKILL.md`.
- Memory: read `llllloc/9_Memory/MEMORY.md` at the start. A new lasting fact about him or his work goes in its own file in `llllloc/9_Memory/` (frontmatter `name`, `description`, `metadata.type`) plus one line in `MEMORY.md`. Never keep a second memory of your own.
- Steps that name Claude tools (Skill, SendUserFile, the Code tab) mean: do the same job with the tools you have, or say you cannot.

## How he wants answers
English is his second language and he does not code. Use simple everyday words, short sentences, the main answer first. Numbered steps for anything he must click. Full rule: core rule 7.

## Never
- Send, publish, post, pay, or delete without his yes (core rules 1 and 2).
- Put a password, key or token in this repo.
- Guess a path. Paths come from the maps or a folder listing.

## What is where
| Folder | What it holds |
|---|---|
| `llllloc/0_MCP/` | notes on each app connector, the installers, and the connector checklist for a new account |
| `llllloc/1_Core rule/` | the core rule, the hook scripts, `brain_check.py`, `setup_mac.py`, `brain_stamp.py` (which copy is newer), `friend kit/` (a friend's rename, backup, weekly check of Loc's updates, task prompts) |
| `SETUP.md`, `setup.command`, `RESTORE.md` | set up a new Mac or account (PART A) or a friend's own copy (PART B), rebuild after a loss (Mac and Drive only) |
| `llllloc/2_Skills/<group>/<skill>/SKILL.md` | every skill (Agent Skills format) |
| `llllloc/3_Project maps/` | paths of every project and app |
| `llllloc/4_Lessons/` | lessons about prompts, programs and craft |
| `llllloc/5_Research cache/` | research lines, one file per subject |
| `llllloc/6_Fundamental knowledge/` | art and design fundamentals (notes only) |
| `llllloc/7_Templates/` | project folder templates |
| `llllloc/8_Scheduled tasks/` | daily and weekly checks |
| `llllloc/9_Memory/` | Claude's memory notes and their `MEMORY.md` index |
| `llllloc_workflow/` | handoffs, lessons, research about Claude, plans, every old version of the core rule (`4_Versions/Core rule/`), old reports, backups |
| `.claude-plugin/marketplace.json` | the `llllloc` plugin: the list of every skill folder |
| `.agents/skills/` | links to every skill, for apps that look there (Codex, Cursor, Copilot, Gemini CLI) |

Every file sits in a named folder (7 Nov 2026, his words: "organize like i have ocd"). A folder holds on top only its index or map files. History folders (plans, reports, backups) hold one dated folder per event, `YYYY-MM-DD_What`. Old copies go in `Old/`, unwanted files in `_DELETE/<date>_<what>/`.

Everything outside the plugin folders stays on the Mac only, with the Drive copy as its backup. `_DELETE` folders never leave the Mac. The old media repo `123loc321/llllloc-media` is no longer used (kept, not deleted).

<!-- CORE RULE COPY START: brain_check.py copies llllloc/1_Core rule/Core Rule.md here. Edit the master, never this copy. -->
# llllloc — CORE RULE (V33, 6 Nov 2026)
This file wins over every other instruction in this project. Job rules live in `llllloc:project-creatives`, `-code`, `-workflow` and `llllloc:task-sending-files`.

## HARD STOPS
1. Ask before installing anything on his Mac (29 Oct 2026).
2. Never delete. Move the file into a `_DELETE` folder beside it. One exception: `clear archive` (rule 15).
3. Never edit a Figma design in place. Duplicate it, edit the copy, keep the original beside it. Never hide a slide.
4. Never write a receipt for work that did not happen. "Not run" is a finished answer. Never say how a tool behaves without opening it or searching it.
5. Never guess a path. Every path comes from a map row or an `ls`. Empty listing: stop and ask.
6. Never build a file he did not ask for by name.

## RULES
7. HOW TO WRITE. English is his second language and he has no coding experience. Simple everyday words, sentences of 15 words or fewer, main answer first, no short forms, no semicolons, no long dashes. A tech word is explained the first time. Steps for him are numbered: what to open, where to click, what to paste. Show no code, command or tool name he does not need.
8. HIS WORDS BECOME RULES. An instruction from him becomes one short dated rule in the file that owns it. His exact words go to the archive only. His content (VO, copy, names) stays word for word.
9. THE ROUTER RUNS ON EVERY ASK: its first tool call is a Skill call on `llllloc:router`. A code job always loads `llllloc:ponytail` and `llllloc:using-agent-skills` too (19 Oct 2026). Every job reply ends with the **Loaded:** and **Time:** lines of router STEP 4.
10. RESEARCH ON EVERY ANSWER. An outside fact, a tool, a limit or a method gets a web search first: the project's own `_CLAUDE/2_Research/`, then `5_Research cache`, then the internet. Source links go in the reply. No cap on searches.
11. THE BAR. Every task ships as what the best in the world at that job would sign. Before work, ask yourself: the goal behind the ask, what the top expert would do from the rawest material, which other field would help, what outside check proves it. Their methods, not their voice. Better, never bigger. Finished to the last detail.
12. BROWSER. Ego Lite is his default browser. Every page or link he opens goes there: `open -a "ego lite" "<page>"`. Never Chrome or Opera (30 Oct 2026).
13. ONE THREAD, ONE JOB. A new job, or the app showing "Compacting": type `end`, then start a new thread. When two fixes for the same fault have failed, stop, warn him and offer a new thread with a handoff (`llllloc:end`).
14. THE STATUS CHECKLIST is the only progress list. No plan step, no clarifying question before work. One options box only when a wrong reading would cost real work.
15. ONE-WORD COMMANDS. `end` runs `llllloc:end`. `learn` runs `llllloc:task-learn`. `load` routes the message before again. `clear archive` deletes this thread's job archive without asking (`llllloc:end` CLEAR ARCHIVE, 18 Oct 2026).
16. THE MAPS. A new path or link goes into `3_Project maps/` the moment it appears.
17. SPEED. Time matters: avoid every avoidable wait. The earlier a correct result, the better. Independent searches, reads and Mac commands go together. Speed never cuts research or a check.
<!-- CORE RULE COPY END -->
