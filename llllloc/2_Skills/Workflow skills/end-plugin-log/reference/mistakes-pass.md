# The mistakes pass

## Contents
- What counts
- What NOT to turn it into
- The entry shape
- Where the rule really belongs — and you must GO AND PUT IT THERE
- THE HARDEST CASE: A RULE THAT WAS ALREADY WRITTEN DOWN
- Running the pass
- If the session made no mistakes

The part of the run that stops the same mistake being made twice.

Everything else in `PLUGIN-LOG.md` records what the PLUGINS do. This records what
**Claude** did wrong while building them, why, and the rule it bought. It goes in
**section 15 · MISTAKES AND THE RULES THEY BOUGHT**.

It exists because the expensive mistakes in this project have not been Premiere's
fault. They have been the same handful of working habits, repeating: shipping a
symptom fix, trusting a check nobody verified, writing a guess down as a fact.
Section 7 stops the platform being re-investigated. This stops the process being
re-learned.

---

## What counts

A mistake worth recording is one where **the work had to be redone, or the studio had to
correct something that should not have needed correcting.** Not every bug — a bug
found by a test and fixed before shipping is the system working.

Record it when:

- the studio pushed back on something shipped ("this is too confusing", "do not hide the
  mask layer", "it doesn't work")
- something shipped broken and had to be rebuilt the same day
- a fix addressed the symptom and the real cause turned up later
- a check or gate passed something that was actually broken
- a note or the log itself said something that turned out to be untrue
- the same wall was hit twice and the third attempt was still a guess
- **a rule already written down was broken anyway** — that is the most valuable entry
  in the section, because it proves the rule needs a command behind it, not a paragraph

**Include this run's own mistakes.** The pass covers the whole session, and the log
update is part of the session. The timestamp entry in section 15 exists because the
rule against future-dating the stamp was sitting in this very skill, unread, twice.

Do **not** record: the studio changing his mind, a new feature request, a genuine
platform limit (that is section 7), or a bug caught by testing before it shipped.

## What NOT to turn it into

- **Not an apology.** No "sorry", no self-criticism. It is an engineering record.
- **Not a diary.** Six lines per entry. If it needs more, the detail belongs in the
  panel's own section 3 entry and this one links to it in words.
- **Not a list of everything that went wrong.** Merge entries that share a cause —
  three symptoms of one habit is ONE rule, not three.
- **Never delete an entry** because it feels old. Like section 7, this is
  append-mostly. Superseded rules get corrected in place with a note, not removed.

## The entry shape

```
### The mistake, in one line

**Happened:** what shipped or was said, and how it surfaced.
**Real cause:** the habit underneath, not the typo on top.
**The rule now:** an instruction a future session can actually follow.
**Would have caught it:** the check, question or test that was missing.
```

The rule line is the whole point. "Be more careful" is not a rule. "Anything
generated or spliced gets parsed before it is zipped" is.

## Where the rule really belongs — and you must GO AND PUT IT THERE

A rule is only worth writing if it lands somewhere it will be *obeyed*. **Writing it
here is not putting it there.** Step 3c of the skill is the step that does it, and it
is not optional. Ask, in this order:

1. **Can it become a gate check?** Then say so and put it in section 9 as well.
   `_CLAUDE/Shared/check-build.js` is the only rule that enforces itself. **Never edit that
   file without the studio's OK** — it is the shared gate for every panel.
2. **Can it become a visible output in the reply?** A `Searched:` line, a `Cloned:`
   line, a version chip. This is the second-strongest home and it is the right one
   for a habit no gate can see. Put it at the top of the code rules (`llllloc:project-code`)
   AND in the skill that owns the work.
3. **Does it belong to one kind of work?** Then it belongs in that skill — `llllloc:task-plugin-builder`
   (panel look in `panel-ui/`), `ste-writing`, this one — at the TOP, where it is read. Edit a
   copy and ship it by `llllloc:task-skill-creator` rule 2 (commit and push, the plugin syncs).
4. **Is it a platform fact?** Section 7, not here.
5. **Is it a code rule?** Section 8, with a one-line pointer here.
6. **Otherwise it lives here**, and here alone. This is the weakest home. Say so.

An entry whose rule is already enforced by a gate should say which check, so the
next session knows it is covered and does not re-litigate it.

## THE HARDEST CASE: A RULE THAT WAS ALREADY WRITTEN DOWN

**This is the most common shape in section 15, and it has its own answer.**

On 17 August 2026 the design-system rule was written in THREE places — the project
instructions, the `llloc-ui` skill, and gate item 16 of `LOCKED-RULES.md` — and it was
broken four times in one session anyway.

**Do not write it a fourth time.** A rule that was read and skipped does not need
better wording. It needs one of two things:

- **To move** to where it is actually read. The top of a checklist, not the ninth
  section of a file.
- **To gain an output** whose absence is visible. That is what the `Searched:` line is
  for, and what the `Cloned:` line was added for on 17 August.

The rule for this case: *"the fix for a skipped rule is not a louder rule."* Follow it here.

## Running the pass

1. Re-read the session from the top. Look for the moments the studio corrected something,
   and the moments a version number went up twice in one hour for the same feature.
2. For each, find the habit underneath. Two entries with the same habit are one entry.
3. Check the rule against sections 7, 8 and 9 — it may already exist, in which case
   the entry is a note that it was broken anyway, and why that was possible.
4. Write it. Newest first.
5. If a rule can be mechanised, say so in the handback and ask the studio before touching
   `check-build.js`.

## If the session made no mistakes

Say so and write nothing. An empty pass is a real outcome. Manufacturing a mistake
to look thorough is its own kind of dishonesty, and it dilutes the section for
everyone who reads it later.
