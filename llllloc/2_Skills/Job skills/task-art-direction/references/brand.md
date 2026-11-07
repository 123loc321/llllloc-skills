# TASK: BRAND

JOB: keep one file per client that every prompt, design and review checks against, so the client's rules are never guessed.

INPUT: brand guidelines (PDF, deck, site), past approved work, his notes and client feedback on past jobs, `llllloc/5_Research cache/_Move to projects/clients/<client>.md` if it exists.

STEPS
1. Open `llllloc/5_Research cache/_Move to projects/clients/BRAND-<Client>.md`. None: create it from the shape below.
2. Fill each section only from a source. Write the source after each line (the guideline page, the job, his note with its date).
3. A section with no source stays empty with the word UNKNOWN. Never fill it from general knowledge of the brand.
4. A new note on an existing file: add the line, keep the old one, mark the old one REPLACED with the date.

OUTPUT: `llllloc/5_Research cache/_Move to projects/clients/BRAND-<Client>.md` with these sections:
- COLORS: hex and the ROLE of each (background, accent, never-text).
- TYPE: fonts, weights, what each is used for.
- PICTURE: lens habits, light, skin and hair rules, casting rules, product angles.
- MOTION: pace, transitions, logo animation rules.
- WORDS: approved names and spellings, words to never use.
- NEVER: forbidden motifs, colors, claims, music styles.
- APPROVED BEFORE: past work the client signed off, with a path or link.
- REJECTED BEFORE: past work the client turned down, with their words.
The chat gets the file card plus one line: how many sections are UNKNOWN.

RULES
- R1. One file per client, and no client's material in another's file. Why: client work is confidential (the studio rule). Check: does the file name match every source in it?
- R2. Every line has a source. Why: an unsourced rule is a guess that looks like a fact. Check: does every filled line end with a source?
- R3. Unsure of a brand rule: ask for the guidelines, never guess (the studio rule). Why: a wrong brand detail is the fastest way to lose a client's trust. Check: is every gap marked UNKNOWN?

CHECK: eight sections, every line sourced, gaps marked UNKNOWN.
