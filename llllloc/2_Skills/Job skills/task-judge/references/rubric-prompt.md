# RUBRIC: PROMPT

JOB: score one prompt or one prompt deck before it costs credits.

INPUT: the prompt text or the deck file, the lock list, the attached reference names.

STEPS: score every line 1 to 5. Quote the words in the prompt that earn the score.

OUTPUT: the scored table, the default test, the fixes.

RULES
- R1. A failed generation costs credits and time. Why: the prompt is the cheapest place to catch a mistake. Check: is every line scored before he runs it?

CHECK: every line below has a score and a quote.

| # | Line | 5 means |
|---|---|---|
| P1 | Obeys the lock | Every locked item (face, outfit, palette, lens, product) is named and none is contradicted. |
| P2 | Every tag has a role | Each `@Filename` says what it defines and what NOT to take from it ("defines the jacket, ignore its background"). |
| P3 | Decisions, not adjectives | No bare "cinematic", "premium", "epic". Each one is replaced by a lens, a light, a material or a move. |
| P4 | Each shot has a job | Each shot changes emotion, moves the action or raises pressure. A pretty shot with no job scores 1. |
| P5 | Three physical details per shot | One pressure from the place (wind, rain, crowd), one small action, one repeated motif. |
| P6 | Fights the model's default | Says what the model does by default (perfect skin, centered face, empty background) and states the opposite twice. |
| P7 | Model syntax correct | Matches the one model file for this generator. Limits respected (length, reference count, duration). |
| P8 | Size | Under 5,000 characters, counted. Base and negative prompt in one copy block per shot. |
| P9 | Not the default idea | The default test passes: this is not the first image any agency would ask for. |
