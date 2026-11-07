# Tests — llllloc:task-learn (22 Oct 2026)

### End of a job thread
Prompt: `learn`
Should trigger: yes, after the router
First thing Claude should do: run thread_scan.py and read_thread in one tool block
Done looks like: a study file, numbered lines in the chat, "Nothing is changed", no file changed

### The RB06 case
Prompt: `ok let's end here, deep study this thread, and suggest me what to add to the overall workflow`
Should trigger: yes
Done looks like: the two wrong skill rules (Plasticity "hide the old group", Magnific "GPT only") found as WRONG RULE with file and line

### Apply his answers
Prompt: a reply `ok` to line 2 and `skip` to line 5
Should trigger: stays in the skill
Done looks like: line 2 applied through its channel, line 5 untouched, both rows in Learn log.tsv

### Should not trigger
Prompt: `I want to learn Blender shortcuts`
Should trigger: no
