# CAPTION RULES — the three laws in full

Part of `llllloc:task-vo-to-srt-subtitle`. Read before Mode 2. Rebuilt on 8 Oct 2026 from SKILL.md. `scripts/build_srt.py` applies these rules. Never apply them by hand.

## Contents
- LAW 1: TIMING
- LAW 2: SHAPE
- LAW 3: WORD
- THE FLAGS
- THE FIXES FILE
- THE OPTIONS
- WHAT THE REPORT MEANS

## LAW 1: TIMING

- A caption starts at its first word's `start` and ends at its last word's `end`. Both values come from the `words` array.
- Never estimate, average, round, stretch or invent a time.
- One exception, with `--extend`: a caption that reads too fast may end at the NEXT caption's start. That value is also real. It is used only when the caption then stays up 7 seconds or less.
- A source with no word timings has no real time inside a segment. `--segments` calculates them, marks the file EST and names it `NAME_draft-EST.srt`. It is never handed over as final.

## LAW 2: SHAPE

Source: Netflix Timed Text Style Guide, English.

- Two lines at most. 42 characters per line at most. One line is better.
- A caption stays up 0.833 to 7 seconds.
- 20 characters per second at most.
- A new caption at every sentence end, and at every silence over one second.
- Where to cut, in this order: after a comma, then before a conjunction, an article or a preposition.
- Never cut after a function word (the, of, and, is, our ...).
- Never cut inside a name, a number or a brand term. "La Roche-Posay", "36.5%" and "TikTok Shop" stay whole. The script protects two capitalized words in a row, a number with its unit, and every term of two or more words in `glossary.md`.
- A cut with no clean place is a FORCED CUT. The report counts it and shows the text. Say each one in the chat.

## LAW 3: WORD

- Change no word he has not approved.
- Deliver what Whisper wrote. List what looks wrong in the flag table: `| Block | Whisper wrote | Probably |`.
- He marks the table. Then write the fixes file and rebuild.

## THE FLAGS

| Flag | Means |
|---|---|
| SHORT | The caption stays up less than 0.833 seconds |
| LONG | More than 7 seconds |
| FAST | More than 20 characters per second |

The Flag column carries these three only.

## THE FIXES FILE

`--fixes NAME_fixes.json`. Keep it beside the SRT. It is reusable on a new export of the same film.

```json
{
  "replace": [
    {"from": "Sapmina", "to": "a client"},
    {"from": "Marquette", "to": "market", "at": 132.4}
  ],
  "drop": [
    {"start": 212.10, "end": 213.40}
  ]
}
```

- `replace`: every match of `from` becomes `to`. Capitals and punctuation around the word are ignored for the match. The punctuation stays. `at` (seconds) limits the fix to the word that starts within one second of that time.
- `drop`: removes every word that starts inside the range. Use it for a clause Whisper doubled. Only after he says yes.
- The times stay real: a replaced word keeps the start and the end of the word it replaces.
- A fixes file made before 8 Oct 2026 used the first script's shape, which is lost. Rewrite it in this shape.

## THE OPTIONS

| Option | Does |
|---|---|
| `--extend` | Law 1 exception. Use by default. |
| `--fixes FILE` | Applies the approved corrections |
| `--split 0.0,4.74` | Cuts in two the captions that start at these times (seconds) |
| `--compare OTHER.json` | Lists every word two runs of the same audio disagree on |
| `--segments` | Draft from a source with no word timings. Marked EST. |
| `--terms FILE` | Another glossary. Default: `references/glossary.md` |

## WHAT THE REPORT MEANS

| Line | Do |
|---|---|
| SHORT, LONG, FAST | Give the block numbers in the chat |
| EXTENDED INTO SILENCE | Nothing. It is the count of Law 1 exceptions. |
| FORCED CUTS | Say each one |
| NUMBER PIECES GLUED | Nothing. "36" + ".5" + "%" became "36.5%". |
| WORDS SHARING ONE TIME | Whisper lost the timing there. Flag it, offer a merge or a second run. |
| LIKELY DUPLICATE | A sentence repeated with no duration. Ask him before a `drop`. |
| ONE WORD, SEVERAL SPELLINGS | Count them in the flag table. He picks one. |
