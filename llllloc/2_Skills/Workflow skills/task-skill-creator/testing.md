# Testing skills

Adapted for the llllloc workflow from robonuggets/skill-creator-plus (MIT, see LICENSE).

Seeing a skill trigger proves Claude found it, not that it did the job. Test two things separately: does it fire on the prompts it should, and is the output right when it does.

## Contents
- In the llllloc workflow
- Old against new on TESTSET.md
- Build evaluations first
- Run a baseline in a fresh session
- Claude A writes, Claude B tests
- Watch how Claude navigates
- Test on the models you plan to use
- Test before you delete
- Verify with a fresh context
- Prompts for this skill

## In the llllloc workflow

- Tests for one skill live in `llllloc/2_Skills/<group>/<skill-name>/TESTS.md`, in the light format below. Tests for the whole workflow (router picks, rules) live in `TESTSET.md` beside this file.
- No with-and-without-skill test (his word, 16 Oct 2026). A change is tested old version against new version, below.
- He runs on the top model. Ask the Opus question: does the skill avoid over-explaining?
- A test costs his plan usage. Ask his yes before each run, with the number of runs (core rule 1).

## Old against new on TESTSET.md (21 Oct 2026)

Anthropic: start with 20 to 50 cases taken from real failures, grade them case by case, and compare versions on the same cases (anthropic.com/engineering/demystifying-evals-for-ai-agents). Status: WORKS (first run 21 Oct 2026: 20 cases, 1 run per arm, Opus 5.5, 11.28 dollars).

1. Two plugin folders in the scratchpad, both named `anthropic-skills` so the skill names match a real thread. Each holds `.claude-plugin/plugin.json` and every installed skill under `skills/` (the newest `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills/`). The Mac has no `claude` command line (29 Oct 2026): installing it needs his yes before a run. `A/` gets the old SKILL.md files from each `Old/<date>_before_<change>/`, `B/` the new Mac copies. Two core files: the old one from `llllloc_workflow/4_Versions/`, the new `Core Rule.md`.
2. Use `claude -p`, not `claude plugin eval`: its grader format is not documented and it adds a no-plugin arm. One run per case and arm, each in an empty folder with its own `CLAUDE_CONFIG_DIR`, so the synced skills of this thread stay out:
   `claude -p "<message>" --plugin-dir <A or B> --append-system-prompt-file <core> --model <his model> --max-turns 8 --max-budget-usd 1.5 --output-format stream-json --verbose --no-session-persistence`
3. Tools: give Claude its normal tools, not only `Skill` (his yes, 21 Oct 2026). With `--tools Skill` both versions passed 20 of 20, so the set could not tell them apart. With normal tools, one trial run loaded only the router on T04 and went straight to Bash: the real miss. Run in an empty folder so a tool call touches nothing.
4. Grade from the stream: the skills loaded with the Skill tool before the first other tool call. Pass = every MUST loaded and no NEVER loaded. T09 allows the router alone (core rule 9).
5. Before a run: one trial run to measure the cost, then his yes with the run count. A run costs about 0.27 to 0.50 dollars.
6. Compare case by case. B passes when no case drops and the changed case rises. Report: cases, runs, pass counts A and B, cost, and every case where the picks differ.
7. A run that fails to start is a finding about the recipe, not about the skill. Fix the recipe here, then run again on his yes.

## Build evaluations first

Write the tests before the skill, so the skill solves real gaps instead of imagined ones.

1. Run Claude on three or more real tasks with no skill. Note where it fails or needs context you keep repeating.
2. Turn each gap into a test prompt with the behaviour you expect.
3. Record how Claude does without the skill. That is the baseline.
4. Write the smallest skill that closes the gaps.
5. Re-run the tests, compare with the baseline, refine. If a test still fails, return to step 4.

A light format for each test, kept in the skill's repo or an `evals/` folder:

```text
### <short name>
Prompt: <exactly what a user would type>
Should trigger: yes
First file Claude should open: <file>
Done looks like: <one checkable line>
```

Add at least one prompt that should not trigger the skill, to catch a description that grabs too much.

Anthropic's page also shows a JSON shape (`skills`, `query`, `files`, `expected_behavior`) if you want machine-readable tests. There is no built-in runner for that format; Anthropic's skill-creator plugin uses its own `evals/evals.json`.

## Run a baseline in a fresh session

Run each prompt in a new session with the skill on, then again with it off, and compare. A fresh session matters because context left over from writing the skill hides gaps in what it says.

- **Personal or project skill in Claude Code:** turn it off for the second run with `"skillOverrides": { "<skill-name>": "off" }` in settings, or from the `/skills` menu.
- **Skill inside a plugin:** use `claude plugin eval`, which repeats each run with no plugin loaded.
- **To automate it:** Anthropic's skill-creator plugin (`/plugin install skill-creator@claude-plugins-official`) runs with-skill and without-skill passes, grades them and compares token cost and time.

## Claude A writes, Claude B tests

Work with one Claude (A) to write and refine the skill. Give it to a fresh Claude (B) with real tasks, not test scenarios. Watch B. Bring each miss back to A with the specifics: "B wrote the report but skipped the date filter, even though the skill mentions it. Is the rule buried?" Repeat until B handles new tasks without help.

## Watch how Claude navigates

While B works, note:

- **Unexpected order:** files read in an order you did not plan. The structure is less clear than you think.
- **Missed links:** an important file never opened. Make the pointer more explicit, or move the content into SKILL.md.
- **The same file every run:** that content probably belongs in SKILL.md.
- **A file never opened:** it is unneeded or badly signposted. Delete it or say when to read it.

## Test on the models you plan to use

A skill adds to a model, so results depend on the model. Ask one question per model:

- **Haiku:** does the skill give enough guidance?
- **Sonnet:** is it clear and efficient?
- **Opus:** does it avoid over-explaining?

Test prudently. Run the full sweep for skills you rely on heavily or that can cost money, delete data or publish. For the rest, test on the model you use most and widen only when something looks off. A full sweep of every skill on every model burns tokens for little gain.

## Test before you delete

Newer models often do better with fewer instructions, but a line that looks redundant may be holding up one edge case. Before cutting instructions for being too prescriptive:

1. List the candidate lines and why each might be dead weight.
2. Copy the skill, remove the candidates in the copy, and run the evaluations on both versions in fresh sessions, on the model the skill runs on.
3. Keep a removal only where the slim version does as well or better. Restore any line whose removal changed the result.
4. Note the evidence in the change list: which test, which model, what changed.

## Verify with a fresh context

When the skill's output matters, check it with a separate Claude that did not do the work, given the spec and the result. Fresh-context verifiers tend to catch more than self-review. Use the same idea inside long workflows: "after each stage, have a subagent check the output against the spec".

## Prompts for this skill

### Audit one skill
Prompt: `audit lord-of-motion`
Should trigger: yes
First file Claude should open: the validator output, then audit-checklist.md
Done looks like: one table, fails first, numbered fixes, no skill changed

### Audit the library
Prompt: `update overall workflow`
Should trigger: yes, together with llllloc-workflow
First file Claude should open: the validator table for every router skill
Done looks like: one row per skill, numbered fixes, biggest first, no skill changed

### New skill
Prompt: `make this a skill, I sort the footage like this on every job`
Should trigger: yes
First file Claude should open: testing.md, to write the tests first
Done looks like: a `.skill` card for the skill and one for the router, each with its button, and a TESTS.md with four prompts

### Refine after a miss
Prompt: `the subtitle skill forgot the two-line rule again, fix the skill`
Should trigger: yes
First file Claude should open: the whole current SKILL.md of that skill
Done looks like: the rule sits near the top with its reason, the file is no longer than before

### Should not trigger
Prompt: `write a prompt for a Seedance shot of a lotus`
Should trigger: no
