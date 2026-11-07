# THE DECK — three prompts or more

Part of `llllloc:task-prompt`. "Section 10" in any rule points here.

## 10. THE DECK

The shell `assets/deck-shell.html` is prebuilt and locked. Never open it. Never restyle it.

PATHS (29 Oct 2026). Scratch body (`$SCRATCH`): the session scratchpad. Deck (`$PROMPTS`): the job's `*_CLAUDE/5_Prompts/`, from `ls -d "<map row path>"/*/*_CLAUDE`. Drive not mounted or empty: stop and tell him. No job: `~/Desktop/Prompt decks/` (29 Oct 2026, his ok).

1. START FROM A DELIVERED DECK. `cp` the newest deck in the project's `5_Prompts/` folder, or the newest one in this thread, to the new name. Change three things only: the `<h1>`, the SPEC values, and the prompt text inside each `<pre>`. No deck yet: `python3 "$SKILL_DIR/scripts/build-deck.py" --starter <body.html>` writes the card patterns to copy from, then `python3 "$SKILL_DIR/scripts/build-deck.py" --body <body.html> --out <deck path>` builds it.
2. SWAP BY NAME. The string `<pre class="prompt-text">` also sits inside the shell's CSS. Anchor every match on the prompt name, assert one match, and print the first line of each block you captured.
3. CHECK THE CLASSES. One line of python: every `class="..."` in the body appears in the shell's CSS. An unknown class is invented markup and a dead COPY button.
4. GATE ONCE. `python3 "$SKILL_DIR/scripts/test-deck.py" <file> > /tmp/gate.txt 2>&1 || true`. Read FAIL and PASS there. One run. Needs playwright: ask first, then `uv run --with playwright`.
5. LOOK. Screenshot the top 1000 px in Chromium with playwright and read the PNG. Then send the file. The scratch body stays.

Body rules:

- Card patterns come from the starter: (A) a simple card, (B) a version group with `<details class="archive">` history, (C) just updated this turn, (D) a shotlist card with a `.ck` checkbox. A card is `<details class="card">` with `<summary class="card-head">`, never a `<div>`. COPY is `<button class="copy-btn" onclick="copyOne(this,event)">`.
- A card is a head row plus one `<pre class="prompt-text">`. No fact rail, no notes, no file chip. Base prompt and negative prompt sit together in that one block.
- One tab per top-level unit: `data-tab` (a short label) and `data-tname` (under 16 characters, unique). Never on a card inside a history box.
- A badge only on this turn's changes: `<span class="badge-new"><span class="bdot"></span>JUST UPDATED</span>`, or the same span with NEW, plus `data-new="1"` on the unit. Clear last turn's badges.
- SPEC: THREE rows at most, each value under about 60 characters. Row 1 is MODEL. Rows 2 and 3 only when they earn the space (`VO 07`, `FRAMES`, `REFS`, `CHANGE`). No RESEARCH row and no fourth row, ever. A live number (a VO, a scene, a line) enters the SPEC only after reading the project's current list. Not in that list: `FR 01`, `FR 02`, and the SPEC says the line has no number yet.
- Prompt text flush at column 0, HTML-escaped. Leave `<span class="chars"></span>` empty.
- History stays in the deck. Each lineage is its own `.group`: the current card on top, older versions below in their own archive, each with COPY. On an update, re-emit the WHOLE deck, every prompt, same order. Never remove a prompt unless he says so.
- Never set a color, a width, a border, a transition or a handler in a body. Something the shell lacks: say so in one line.
- An the studio film deck is named after its VO line verbatim, `_V<N>.html`. A colon becomes a semicolon.
- Style frames from a script: the lock list first, one deck per script sentence, 3 to 4 frames in the cut, 4 to 8 in the deck, marked.

