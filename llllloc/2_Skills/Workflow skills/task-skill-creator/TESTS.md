# Tests — llllloc:task-skill-creator

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
