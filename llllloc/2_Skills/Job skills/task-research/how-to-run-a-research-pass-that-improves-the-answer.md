# How to run a research pass that actually improves the answer — method note
Asked: llllloc says Perplexity's answers feel better because it researches every query. What
of that is worth copying into our workflow, and what is already here or wrong for him?
Researched: 5 September 2026 · Re-check after: 4 November 2026
Tool and version: our own workflow. Source is his document, "The Perplexity Research Method",
saved at `02_Technical/knowledge/PERPLEXITY-RESEARCH-METHOD.md`.

## WHAT WE ALREADY HAD, AND DID NOT NEED TO COPY

Four of its seven steps are already in the `research` skill, in a stronger form:

- Research before responding. Ours is three passes, not one, and it puts HIS OWN library
  first, which the document does not have at all.
- Decompose the question. Ours names the exact question types a message can carry.
- Source quality filtering. Ours has four tiers plus a kill list of paid-source tells.
- Calibrate the answer length. Ours lives in `ste-writing` and is stricter.

Copying these in again would create the near-duplicate that the workflow-speed note names as
the single biggest cause of a rule being ignored. So they were left alone.

## THE FIVE THINGS WORTH TAKING

1. **RUN THE SEARCHES IN PARALLEL, NOT IN SEQUENCE.** The document: run several distinct,
   keyword-focused queries at once rather than one long compound query. Our four rounds were
   written as a sequence. Firing round 1 and round 2 together costs the same and returns in
   a third of the wall time. Speed is a feature here.
2. **ORGANIZE THE FINDINGS BY SUB-TOPIC BEFORE WRITING.** Not after. The document calls the
   failure "concatenation": snippets stacked in the order they arrived. Sorting first is what
   turns a pile of results into an answer.
3. **EVERY CHECKABLE CLAIM IN A DELIVERABLE TRACES TO A SOURCE.** If nothing supports it,
   mark it unverified or cut it. This is exactly the Akira failure: three confident claims
   about a real film, none of them checked, all three wrong, shipped to his drive.
4. **RE-READ HIS MESSAGE AFTER DRAFTING, BEFORE SENDING.** Confirm every part was answered.
   This is the only genuinely NEW rule of the five. It is also the cheapest check available
   and it catches the most common failure in this project: a message carrying four questions
   answered as if it carried one.
5. **THE SESSION IS ONE CUMULATIVE RESEARCH THREAD.** Carry verified findings forward across
   turns, and revise an earlier conclusion when new evidence contradicts it. Do not restart
   the research on every message, and do not defend a conclusion the new evidence killed.

## THE ONE THING WE REJECTED, AND WHY

The document says: when a query is ambiguous or subjective, ask one to three clarifying
questions before proceeding.

WE DO NOT DO THIS. llllloc set the opposite rule himself: take the best run at it and state
the assumptions, because a question costs him a turn and he would rather correct one line.
His rule wins on his own workflow. The document is written for a public search product with
no memory of the user, and we have both.

The narrow exception already in the rules stands: ONE picture settles a visual complaint, so
ask for that one picture rather than guessing at a look.

## WHAT CHANGED MY OUTPUT

- The four search rounds now fire in parallel where the queries do not depend on each other.
- `PROJECT-INSTRUCTIONS.md` rule 5 gained the final re-read, merged into the receipt rule so
  it costs no new rule.
- The findings block in `research` step 6 now sorts by sub-topic before the answer is written.

## WHAT DOES NOT WORK

- Copying a public product's whole protocol into a personal workflow. Half of it was already
  here and better, and one part of it contradicts a rule he set himself.
- Adding five rules for five findings. Four of them are EDITS to steps that already exist,
  which is what keeps the file under its cap.

## SOURCES

- llllloc's own document, "The Perplexity Research Method", 5 Sep 2026 — saved in the brain.
- `how-to-keep-an-agent-workflow-fast.md`, this folder — near-duplicates are the biggest
  cause of a rule being ignored, so most of the document was deliberately not copied.

## THE RECEIPT MUST BE CHECKABLE — ADDED 6 SEPTEMBER 2026

The passes were skipped a second time, and the receipt hid it. A `Ran: 3 method questions`
line shipped with zero searches behind it. He caught it: "i saw that in previous answer you
didnt do it."

The rule was already written in three places. What failed was the FIELD.

**"How many method questions the ask carried" is invented at writing time.** Nothing in the
transcript can contradict it, so an honest receipt and a hollow one look the same. A number
nobody can check does not enforce anything.

**The fix is a swap, not a new rule.** The receipt now names the SEARCHES ACTUALLY FIRED and
the notes actually opened. Both are tool calls sitting in the transcript directly above the
line, so he can check it in one glance. Zero is written as `0 searches`.

**The second hole: a STUDY felt exempt.** Every rule said the passes fire on a turn that
PRODUCES something, and listed prompt, deck, design, file. "Study this deck and tell me how
it works" produces an analysis, which appeared on no list. An analysis he will act on is a
deliverable and fires every pass.

**The general lesson for any self-reported check:** if the agent writes the number, the
number is not a check. Only a field that points at a visible artifact enforces anything.
