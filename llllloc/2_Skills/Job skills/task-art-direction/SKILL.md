---
name: task-art-direction
description: "Does the thinking before any picture: reads a client brief, writes three concept territories, writes a director treatment, keeps one brand file per client. Runs on its name or when /llllloc:router picks it."
---

# llllloc:task-art-direction

It does one thing: turn a client ask into a clear idea before any deck, prompt or motion work starts. It does not build the slides (`llllloc:task-design`), write prompts (`llllloc:task-prompt`) or judge the work (`llllloc:task-judge`, on his word only).

Why it exists: when work starts at the picture, the idea is whatever comes first, and the first idea is the generic one. This step puts his choice at the start, before credits are spent.

## THE TASK TABLE

Pick one row. Read its file before you write. Nothing in this body is enough to do the task.

| He gives or asks | Task | Read |
|---|---|---|
| A brief: a PDF, an email, notes, a call transcript. "Read this brief." | BRIEF | `references/brief.md` |
| "Concepts", "directions", "ideas", "territories" for a job | TERRITORIES | `references/territories.md` |
| "Treatment", "director's note", "write it up for the client", after he picked a territory | TREATMENT | `references/treatment.md` |
| Brand guidelines, past approved work, "the client's rules", a new client | BRAND | `references/brand.md` |

## ORDER IN A JOB

BRIEF, then TERRITORIES, then he picks, then TREATMENT. BRAND is written once per client and read by every task after it. No BRIEF file yet when he asks for territories: run BRIEF first in the same turn, then TERRITORIES.

## WHERE FILES GO

- `*_CLAUDE/4_Story/BRIEF.md`, `*_CLAUDE/4_Story/TERRITORIES_V<n>.md`, `*_CLAUDE/4_Story/TREATMENT_V<n>.md`.
- `llllloc/5_Research cache/_Move to projects/clients/BRAND-<Client>.md`, one per client. Never put one client's rules in another client's file.

Resolve every path with `ls -d "<full path from the map row>"/*/*_CLAUDE` (29 Oct 2026). Deliver each file as a file card plus its full Mac path (`llllloc:task-sending-files`).