# VOCABULARY — the names Whisper must hear right

Part of `llllloc:task-vo-to-srt-subtitle`. Read before Mode 1 on a branded film. Rebuilt on 8 Oct 2026 from SKILL.md.

JOB: fill `--initial_prompt` so Whisper spells this film's names correctly the first time.

STEPS
1. Start from the names in THIS film: the speakers, the brands, the divisions, the regions, the product and program names. Take them from his brief, the script, the client transcript or the project handoff.
2. Add the terms from `glossary.md` that this film uses. Leave the others out.
3. Write them as one plain line: names separated by commas, then short groups ("Divisions: ...", "Regions: ...").
4. Count it. Under 900 characters.

THE BASE LINE for a client a client film (from SKILL.md):

```
a client, a client, ONE a client, Vismay Sharma, Kérastase, Elseve, La Roche-Posay, CeraVe, 3CE, Dr. G, NEO, TikTok Shop. Divisions: CPD, LLD, LDB, PPD. Regions: GCC, ANZ, MENA, ASEAN.
```

RULES
- Only names that are in the film. Reason: a name in the prompt that nobody says can appear in the transcript anyway.
- Spell each name the way the client spells it, accents included (a client, Kérastase, Lancôme).
- A name he has not confirmed is a guess. Ask for the script or the speaker list before a client film.
- One client's names never go into another client's prompt.

CHECK: every name in the prompt is in his material for this film, and the count is under 900.
