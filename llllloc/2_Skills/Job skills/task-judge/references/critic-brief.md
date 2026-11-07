# CRITIC BRIEF

JOB: give the fresh critic agent everything it needs to judge, and nothing that defends the work.

INPUT
- The work itself: the file path, the Figma frame link, the render path, or the prompt text. Never a screenshot the maker chose.
- The brief, and his own words on this job (from `FEEDBACK-LOG.md` and the thread).
- The lock: the lock list, `DesignSystem_<Name>_V<n>.md`, `BRAND-<Client>.md`, whichever exist.
- The rubric file for this kind of work. Paste it whole.
- Round 2 and later: the previous critic's report.

STEPS
1. Fill the template below. Every slot gets a real value or the word NONE.
2. Leave out the maker's reasons, its list of what it fixed, and its own opinion of the work.
3. Send it to a new general-purpose agent. One agent per round. Never reuse one.

OUTPUT: the critic's report, in the shape the template asks for.

RULES
- R1. Never pass the maker's reasoning. Why: a critic who reads the excuse accepts it. Check: does the brief hold any sentence that starts with "I", "we" or "because"?
- R2. The critic looks at the real thing. Why: a chosen screenshot hides the weak frame. Check: does every work slot point at the full file?
- R3. His words go in word for word. Why: they are the bar the client will apply. Check: are his notes quoted, not summed up?

CHECK: the template is filled, no slot is empty, no maker reasoning is inside.

## THE TEMPLATE

```
You are an independent, strict critic. You did NOT make this work. Judge only what you can see, hear or measure, never what the maker meant.

WORK: <path, link or text>. <Kind of work, size, length, format.>
BRIEF: <the brief in 3 to 6 lines>
HIS WORDS ON THIS JOB: <verbatim notes, or NONE>
THE LOCK: <lock list / design system / brand file, pasted or linked, or NONE>
PREVIOUS REPORT: <pasted, or NONE>

RUBRIC:
<paste the rubric file>

METHOD: Open the work at full size. For a film, pull frames with ffmpeg (a contact sheet every 0.25 s, plus every frame around each cut) and look at them. For a deck or design, look at every frame at full size and once at phone size.

REPORT, under 500 words:
1. If a previous report exists: each old item as FIXED, PARTLY or STILL PRESENT.
2. A score from 1 to 5 for every rubric line, with one sentence of evidence (a slide number, a timestamp, a quote).
3. THE DEFAULT TEST: name the generic version any agency would make first. Say if this work is that version.
4. Every line under 4: the exact fix, one sentence each, biggest first.
5. Last line: APPROVE (no line under 4) or BLOCK.
Be blunt. No praise. No padding.
```
