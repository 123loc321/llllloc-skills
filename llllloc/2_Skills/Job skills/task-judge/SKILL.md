---
name: task-judge
description: "Judges ONE finished deliverable blind and returns BLOCK or APPROVE with a 1-to-5 score per line. It never makes or fixes work. Use when he types or names llllloc:task-judge, never otherwise, in a Code tab session in his brain folder (Desktop/Claude). No skill and no router row calls it on its own."
---

# llllloc:task-judge (renamed from llllloc-review, 15 Oct 2026)

It does one thing: judge the finished work he points it at. It does not make the work (that is the maker skill) and it does not fix it (the maker fixes, then this skill checks again).

Why it exists: the maker always believes in its own work. A judge who never saw the build finds what the maker cannot.

## WHEN IT RUNS

Only in a Code tab session in his brain folder, `~/Desktop/Claude` (29 Oct 2026), and only on his word: he types `llllloc:task-judge`, or he names it in a message ("run llllloc:task-judge on this deck"). Nothing else starts it, a client delivery included (18 Oct 2026, his words: "let's just judge when i say so").

## THE TASK TABLE

Read `references/critic-brief.md` first, every time. Then read one rubric. Read the file before you judge. Nothing in this body is enough to judge with.

| The work | Read |
|---|---|
| A prompt or a prompt deck | `references/rubric-prompt.md` |
| An art direction deck, slides, a layout, a key visual, UI | `references/rubric-design.md` |
| A motion film or a part | `references/rubric-motion.md` |
| Generated images or clips (takes) | `references/rubric-render.md` |
| Concept territories, a treatment | `references/rubric-concept.md` |

## THE LOOP

1. Fill the critic brief. Start a FRESH agent with the Agent tool and send it the brief. Never judge in the maker's own context. The judge runs a real check with its tools: it opens the render at full size, puts frames beside the Figma frames, runs the validator, measures, opens the source the work claims to follow. A helper that only re-reads the work is not a judge: Anthropic's Opus 5 guide says not to use helpers to double-check your own work. No real check is possible: say so to him in one line before starting the helper (Oct 2026, re-check at the next workflow update).
2. A line under 4 goes back to the maker with its fix.
3. After the fix, a NEW fresh agent checks again. It marks each old item FIXED, PARTLY or STILL PRESENT, and looks for new damage.
4. Stop at APPROVE, or after three rounds. After three rounds he gets the work with the open items listed.

## THE REPLY

He gets the work, then one line: `REVIEW: APPROVE · lowest 4/5 (<line>) · <n> rounds`. A BLOCK after three rounds adds one line per open item. The full report stays in the workspace. It goes to disk only on his word.
