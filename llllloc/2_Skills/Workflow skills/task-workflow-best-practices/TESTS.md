# Tests — llllloc-workflow

### Health run
Prompt: `update overall workflow`
Should trigger: yes, together with llllloc:task-skill-creator
Done looks like: a table with a measure and a cap per part, numbered changes, nothing changed

### New rule cascade
Prompt: `new rule: every export gets the client name first. update the workflow`
Should trigger: yes
Done looks like: the rule in one owner file, one line per other file touched

### End of thread
Prompt: `end`
Should trigger: llllloc-log first, which runs REVIEW here once its trim card is saved
Done looks like: six lines at most, or `Workflow: nothing to trim`

### Should not trigger
Prompt: `what is my workflow for a Seedance prompt?`
Should trigger: no. It is a question.
