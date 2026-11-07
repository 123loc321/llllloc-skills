---
name: task-be-ambitious
description: "Raises one llllloc job to a more ambitious level with Felix Rieseberg's three types of ambition: Altitude (the goal behind the ask), Depth (the top expert's method from the rawest material, checked by an outside tool) and Range (other fields and their methods). Plans in the status checklist, then does the work. Use when /llllloc:router picks it: he says \"be ambitious\", \"aim higher\", \"go deeper\", \"what would a top expert do\", or a client job starts (Depth only). Not on a revision, a small fix or a chat. Core rule 11 holds the short form for every other turn."
---

# llllloc:task-be-ambitious (18 Oct 2026, update 18 Oct 2026)

Built from `github.com/robonuggets/be-ambitious` (MIT, RoboNuggets), from Felix Rieseberg's post "How to be more ambitious" (13 Oct 2026, felixrieseberg.com). Core rule 11 carries the short form. This skill is the full method.

## TOP RULES

1. **Better, not bigger.** Raise the goal, the standard or the points of view. Never the number of files, features or side jobs. A suggestion that makes the job larger without making it better is dropped.
2. **A bigger idea is offered, never built.** Altitude may say "a 3D walk-through would win this pitch, not slides". That is a new deliverable. Offer it in one line and build only on his yes (core rule 6). The same for anything that costs money, sends or deletes (core rules 1 and 2). Ambition raises the standard, not the permissions.
3. **Methods, not voice.** Bring in a field by doing what its experts do, with their tools. Writing in their style is role play: the text gets strange and the work stays the same.
4. **An outside check decides (Oct 2026, re-check at the next workflow update).** Never grade your own work, and never send a helper only to re-read it (Anthropic's Opus 5 guide). The check is a tool run: a frame beside the Figma frame, a render at full size, a validator, a measurement, the source the work claims to follow. No such check exists: write "no outside check" in the reply. The judge skill `llllloc:task-judge` runs only on his word (18 Oct 2026, his words).
5. **The hard target is reasonable.** Aim far past the safe number and keep going when it looks impossible. On a tool or model new to him or to you, the target is a learning one: learn X and prove it, not a number (Seijts and Latham 2001). Report honestly against the check: a missed hard target with real numbers is a good result. A faked one is not (core rule 4).
6. **Get the access, never fake it.** Name the data, folder, connector or tool the plan needs, and what is missing. Never invent a source or a result.

## PICK THE TYPES THAT FIT

The start of a client job (the first ask for a new deliverable) runs Depth only. Altitude and Range run when he says "be ambitious" or "aim higher", or on a pitch. Skip the types that do not fit, in one checklist line.

| Type | Fits when | Skip when |
|---|---|---|
| Altitude | The job serves an outcome: win the pitch, keep the plugin crash-free, make the client say yes | Pure creative work with no outcome beyond itself. Felix: altitude "works less well for creative endeavors" |
| Depth | The work should be done really well. Every client job | Throwaway work, a quick test |
| Range | The work must land with people, or the obvious field has run out of ideas | A narrow fix with one right answer |

## ALTITUDE: THE GOAL BEHIND THE ASK

Ask: what does he want to happen next? Write a ladder of three steps, each higher. A client deck: (1) the real story, (2) answers to the client's three meeting questions, (3) the finished result shown before it exists. Start on the highest step you can finish and check with the access you have. A step with no outside check is too high: go down one.

Durable work (a scheduled task, a check on every build) lives at the top step. Name the setup it needs.

## DEPTH: THE TOP EXPERT'S WAY

Answer Felix's four questions to yourself before the work:

1. What would a top professional in this field do here that he is not asking for?
2. What is the rawest material they would start from, instead of a summary? Then also read the best guidance on top of it, so nothing useful is skipped (a 16-run test found agents read only the raw source and missed the guidance). A source you cannot read in full is used through its summary, labeled as such, never skipped.
3. Which methods and tools would they use? Not a table in the chat: a database, a script, a render, a real reference.
4. What, other than you or him, would show the result is right? That is the check (rule 4).

Two more of Felix's Depth methods, when the job allows: question what you think you know against the raw material, and make something new that can be checked (a prediction, a test on material not yet seen).

Then set the hard target (rule 5). Research for these answers runs through `llllloc:task-research`.

## RANGE: OTHER FIELDS

1. **Nouns to verbs.** A trick from The Art of Innovation (Kelley and Littman). An opening title is not "a 10-second video". It is "make a festival crowd feel the place before the first word". The verbs show which fields can help.
2. **The crew.** Up to five fields that do those verbs best, two of them to find what is wrong. For each: the real job, its method or tool. Example: a cinematographer (lens choice), a sound designer, an editor, and as red team a festival programmer.
3. **Helpers for the crew.** Only when he said "be ambitious" or "aim higher", or on a pitch: give each field its own helper with the Agent tool, its method and its tools. A helper only reads and returns a short note (core rule 10). Helpers cost many tokens. A part he will look at and talk about is a thread, not a helper: `llllloc:project-workflow` SPLIT.

## OUTPUT

No plan block in the reply (core rule 14, 18 Oct 2026). The plan lives in the status checklist and in the work:

1. **Checklist first.** The goal behind the ask, the types used and skipped, the Depth answers in short, the hard target, the check. One line each.
2. **Then the work**, in the same turn.
3. **The reply** opens with the result, then the check and its numbers (or "no outside check"), then what is missing.
4. **Ask in one line** for rule 2 (a bigger idea, money, sending, deleting) or missing access. The asked work is still done first. Only the bigger idea waits for his yes.

When he asked only for a better prompt, the sharper ask goes in one copyable block and the turn stops there. A prompt for an image, video or audio model goes to `llllloc:task-prompt`.

## WHY IT WORKS

Specific hard goals beat "do your best" (Locke and Latham 2002), when there is honest feedback against a real check.