# TASK: BRIEF

JOB: read a client brief and write down the real ask, what is missing, and which parts are guesses.

INPUT: the brief in any form (PDF, email, notes, transcript). `BRAND-<Client>.md` if it exists. Past handoffs of this client, only if the brief points to earlier work.

STEPS
1. Read the whole brief. Mark every sentence that states a fact, a must or a must-not.
2. Write the real ask in one sentence: who must think, feel or do what, after seeing what.
3. Name the level of the idea: a whole campaign, one film, one key visual, one shot, or an edit of existing work. Why: a campaign idea for a single social post is waste, and a single shot for a campaign falls short.
4. List the deliverables: format, ratio, duration, count, deadline, where it plays.
5. List what is MISSING that changes the work (budget, deadline, VO, product shots, music rights, approval chain).
6. List what CONTRADICTS (two asks that cannot both be true).
7. Split everything into STATED (the client wrote it, quote the words) and ASSUMED (Claude filled it, say why). Never mix the two.
8. Write the DESIGN READ in one line: "Reading this as: a <kind of work> for <audience>, in a <feeling> language, leaning toward <a family of looks>."

OUTPUT: `*_CLAUDE/4_Story/BRIEF.md` with these headings, in order: THE ASK, LEVEL, DELIVERABLES, STATED, ASSUMED, MISSING, CONTRADICTS, DESIGN READ. The chat gets the file card plus one line: the ask and the number of ASSUMED items.

RULES
- R1. No questions before the file. Why: a guess he can see is faster to fix than a question he must answer (his rule, no clarifying questions). Check: does the reply contain zero questions?
- R2. STATED and ASSUMED stay apart. Why: the ASSUMED list is where he corrects the work. Check: does every STATED line quote the brief?
- R3. Never invent a client fact (a name, a number, a date, a claim). Why: a wrong fact in a pitch costs trust. Check: is every number and name in STATED traceable to the brief?

CHECK: all eight headings exist, every STATED line has a quote, the reply has no question.
