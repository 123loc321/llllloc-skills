# RUBRIC: RENDER

JOB: judge a batch of generated images or clips, take by take, so he only looks at the ones worth his time.

INPUT: the takes (paths or Magnific creation links), the prompt each one came from, the lock list.

STEPS
1. Make one contact sheet of all takes, numbered.
2. Open each take at full size. For a clip, look at the start, the middle and the end frame.
3. Give each take PASS or FAIL against the lines below. One sentence of reason per take.
4. Rank the passes, best first.

OUTPUT: a table: take, PASS or FAIL, the failed line, the reason. Then the ranked passes.

RULES
- R1. Reject and re-prompt, never patch a weak take. Why: a fix on a bad base costs more than a new run. Check: does every FAIL name the prompt change that would fix it?
- R2. Judge at full size. Why: hands, joins and text break only at full size. Check: was each take opened full size?

CHECK: every take has a verdict and a reason.

| # | Line | FAIL when |
|---|---|---|
| R1 | Identity | The face, product or logo differs from its reference. |
| R2 | The lock | A locked color, outfit, material or lens is wrong. |
| R3 | Anatomy and geometry | Extra fingers, melted joins, bent straight lines, floating parts. |
| R4 | Text | Any letter on screen is wrong or invented. |
| R5 | Model drift | The model added its own taste: cleaner, darker, more symmetric, more "corporate" than asked. |
| R6 | The job | The take does not do the job its shot was written for. |
