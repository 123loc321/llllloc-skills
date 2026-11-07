---
name: project-workflow
description: "The task rules for a workflow ask in llllloc: a rule, a skill, the setup, this project. Where the workflow lives, how a rule changes, which skill does what, and SPLIT: when and how one big job runs as parallel side sessions. Loaded by /llllloc:router once per thread on a workflow ask, and by any session before it splits a job."
---

# llllloc:project-workflow (15 Oct 2026; folders FOLDERS v19, 16 Oct 2026)

The workflow is a project of its own: `~/Desktop/Claude/llllloc_workflow/`. What Claude reads to do a job lives beside it in `llllloc/`.

## 1. THE START OF A WORKFLOW ASK
1. Read the newest `HANDOFF_*.md` in `llllloc_workflow/0_Handoffs/`. Then only what the ask needs.
2. Load the skill that owns the ask: a check-up or a rule across files is `llllloc:task-workflow-best-practices`, the big upgrade is `llllloc:task-workflow-update`, a skill is `llllloc:task-skill-creator`. `llllloc:task-research` always comes along: a fact about Claude is looked up, never remembered. Its cache is `llllloc_workflow/2_Research cache/`.

## 2. WHERE THINGS LIVE
| What | Where |
|---|---|
| GitHub, skills only (6 Nov 2026, his words) | repo `123loc321/llllloc`, branch `main`, holds only the plugin: `llllloc/2_Skills/`, `llllloc/1_Core rule/`, `.claude-plugin/`, `.agents/`, `AGENTS.md`, `CLAUDE.md`, `README.md` (`.gitignore` lists them). A session pulls at start (hook). A skill change pushes the moment it is written (`llllloc:task-skill-creator` DELIVER). Everything else stays on the Mac |
| The core rule | `llllloc/1_Core rule/Core Rule.md`, copied into `AGENTS.md` by `brain_check.py`; `CLAUDE.md` loads `AGENTS.md` every session |
| Every skill | the `llllloc` plugin, synced by claude.ai from GitHub as `llllloc:<name>`. Master in `llllloc/2_Skills/<group>/<skill>/` with its `Old/` versions, listed in `.claude-plugin/marketplace.json` |
| Memory | `llllloc/9_Memory/` (`autoMemoryDirectory` in the brain's `.claude/settings.local.json`, written per Mac by `setup_mac.py`), `MEMORY.md` is the index |
| Hooks (6 Nov 2026) | inside the `llllloc` plugin entry in `.claude-plugin/marketplace.json`, scripts in `llllloc/1_Core rule/hooks/`. Never also in a settings file, or they fire twice |
| Books, videos, frames, installers, Old versions | the Mac folder only, backed up by the Drive copy. The media repo `123loc321/llllloc-media` is no longer used (6 Nov 2026) |
| Backup, new Mac, rebuild (6 Nov 2026) | Google Drive `*llllloc_System_Full backup` (map row "Brain Drive backups"), one-way copy by `llllloc/8_Scheduled tasks/Drive backup/drive_backup.sh`, once a week by the scheduled task `llllloc-weekly-drive-backup` (Mondays about 12:20), never at `end` (6 Nov 2026, his words). Each backup writes `BACKUP-STAMP.json` first (`brain_stamp.py`: which copy is newer, never overwrite a newer Mac copy). New Mac or account (7 Nov 2026): AGENTS.md "First session" runs `SETUP.md`; a pasted Drive link runs that folder's `START HERE.md`. The shareable copy `*llllloc_System_Template` (no memory, maps, client names, accounts, books or videos; skills load from the folder): `template_build.py` beside the backup script, first run `--dry-run` |
| The brain check | `llllloc/1_Core rule/brain_check.py`, run at every `end` |
| The maps | `llllloc/3_Project maps/` |
| Connector installers, newest only | `llllloc/2_MCP/<Program>/`, older in `Old/` |
| Templates | `llllloc/7_Templates/`: PROJECT-TEMPLATE, PROJECT-TEMPLATE_CODE, client-storyboard-deck, deck-shell.md |
| Timed tasks | `llllloc/8_Scheduled tasks/Outside updates/` |
| Dated copies of the core rule | `llllloc/0_Instructions/` |
| Lessons about models and programs | `llllloc/4_Lessons/Prompts/`, `llllloc/4_Lessons/Programs/` |
| Lessons about the workflow | `llllloc_workflow/1_Lessons/Lessons_Workflow.md` |
| Universal research | `llllloc/5_Research cache/` |
| Research about Claude itself | `llllloc_workflow/2_Research cache/` |
| Handoffs, plans, versions, old reports, backups, trash | `llllloc_workflow/0_Handoffs/` (newest 3, older in `Old/`), `3_Plans/`, `4_Versions/`, `5_Old reports/`, `6_Backups/`, `_DELETE/` |
| His exact words | `llllloc_workflow/1_Lessons/Your words.md` |

## 3. UPDATING A RULE
- A rule lives in one file, the one that owns its subject. Every other file points to it. A rule about a program lives in that program's skill, prompts in `llllloc:task-prompt`, design in `llllloc:task-design`, motion in `llllloc:task-motion`, skills in `llllloc:task-skill-creator`, the task rules in the project skills, the always-on rules in the core.
- Name the target, show the new text, wait for his yes, then change it. EXCEPTION: `update overall rule` IS the yes. Target unclear: ask which. Never guess.
- A new core rule is paid for by a cut. The core stays under 3,500 characters and 20 rules. Everything else goes into a project skill.
- A core change ships through its channel in `llllloc:task-workflow-best-practices` THE PARTS, and reaches new sessions only. After it, start a new session.
- A plan is only a plan until he says `go`. Nothing on the Mac or in a skill changes before that word.
- Every skill change goes through `llllloc:task-skill-creator` DELIVER: Mac master and `Old/` written, then committed and pushed, so the `llllloc` plugin syncs it to every account (6 Nov 2026).
- An outside skill, a skill built from one, an MCP or a tool joins the workflow: the same turn, without asking, it gets its row in `Outside sources.md` and its line in `check_outside_updates.py` (`llllloc/8_Scheduled tasks/Outside updates/`), so the daily outside check watches it (18 Oct 2026, his words). An app he runs as his own build of GitHub code goes on the weekly app check instead: `llllloc:project-code` section 8 (26 Oct 2026).

## 4. SPLIT: SIDE SESSIONS (18 Oct 2026, Code tab 29 Oct 2026)
Each side session is a full session with its own memory of the chat, and it uses his plan limit like one. Split only when the parts truly run alone.
Suggest it first (1 Nov 2026, his words: "please be smart and suggest me to divide the task into multiple nested sessions like this, if i say yes then do it"). A huge job, like seven videos of one film, gets a one-line suggestion before work starts: how many sessions, and what each owns. Start them only on his yes.
1. Split only parts that share no file and do not wait on each other's choices. Example: the open, frame 2 and end videos of one film. Keep in one session: one design under feedback, one render chain, work on the same file.
2. Lock the shared choices first, in one file: the `DesignSystem_<Name>_V<N>.md`, the job's STATE, the spec. Then split.
3. Start with 2 or 3 side sessions. More only after the first ones came back right.
4. One owner per file. On his Mac, one `.aep`, `.prproj` or Figma page has one owner at a time. The others work in their own copy, comp or section. The lead merges. File rules per job: `llllloc:project-creatives` section 4, `llllloc:project-code` rule 5.
5. Each brief holds the goal, the locked choices, the files it owns, the test for done, and where the result goes. History does not carry over.
6. A correction he gives one session goes the same turn to project memory and to every sibling session (`mcp__ccd_session_mgmt__send_message`, untested, Mac test list). Why: in a client two lanes got the same correction (Lessons, 28 Sep 2026).
7. The last step: the lead checks the merged result with a tool (a render, a validator, a measurement). The judge skill `llllloc:task-judge` runs only on his word (18 Oct 2026).
8. The session that holds the job starts the side sessions with `mcp__ccd_session__start_session` (tested 29 Oct 2026) and stays the lead. A side session never starts its own: it sends the lead the plan (parts, owners, briefs).
9. Inside one session, read-only research, a crew of fields and a judge are helpers (the Agent tool), not side sessions. A side session is for a part he will look at and talk about.
10. A method every part shares: one session builds it, he approves it at real speed, then the lead sends it to the others. Spreading numbers he had not seen cost two extra rounds (1 Nov 2026).
11. A session's idea that breaks a locked rule stays in that session until he decides.
12. Before sending work that needs an app, the lead checks the app answers. One closed app or popup stops every session.
