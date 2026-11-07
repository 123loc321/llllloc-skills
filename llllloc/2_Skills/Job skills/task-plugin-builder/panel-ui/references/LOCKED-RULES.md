# THE LOCKED RULES — FIND is the reference, and this is the checklist

## Contents
- RULE ZERO — OPEN FIND FIRST, AND SAY WHAT YOU CLONED
- THE GATE — run this before you show him anything
- A RANGE REPLACE SWALLOWS WHAT SITS BETWEEN THE ANCHORS
- A PATCH SCRIPT THAT WRITES AT THE END LOSES EVERYTHING
- THE PIXEL-KIND TRAP CAUGHT A THIRD TIME — now in a border width
- A SKIPPED SUBTREE RETURNS STALE STYLES — the checker's version of the pixel trap
- THE PIXEL-KIND TRAP SHIPPED — and it emptied the bottom bar
- THE LIGHT-MODE CONTRAST TRAP — measured 29 August 2026
- THE SPECIFICITY TRAP — the bug you cannot see in light mode
- THE FOUR THINGS THAT LOOK CHEAP, AND WHY
- THE HOUSE RELOAD GLYPH
- PIXEL KINDS — the trap that hides inside CSS zoom
- Pointer maths — prefer a delta over a position
- Testing a UI
- Layout watch-outs
- Adobe CEP, settled — do not re-investigate


**FIND V1.20 is the reference build. `assets/reference-panel.html` IS that file.**
When a panel and FIND disagree, **FIND is right**. Never design a panel's look.
Clone the shell and design only the working content.

**Read this page before the first line of CSS, every time.** Every rule below is a
correction the studio already made. Most of them he made twice.

---

## RULE ZERO — OPEN FIND FIRST, AND SAY WHAT YOU CLONED

**Added 17 August 2026, and it is first because it is the rule that gets skipped.**

SORT's RENDER SETTINGS window took **four rounds of the studio's marked-up screenshots**. Every
single correction was already solved in `assets/reference-panel.html`, and that file was
never opened:

| He wrote | FIND already had it |
|---|---|
| *"weird layout + stroke. Please clean up this"* | FIND V1.14 replaced its own native `<select>` for this exact reason, with the comment explaining why |
| *"improve the contrast so we can see the buttons"* | FIND V1.13 measured the identical **1.05:1** and moved its dialog to `--paper` |
| *"add same button to delete, rename preset, just like FIND"* | FIND's library bar — the `+`, the pen, the click-twice bin |
| *"resize the buttons so it line up with the big box evenly"* | one row height |

**Gate item 16 already said "no native widget shows through". It was broken anyway.** So
this is not a louder rule. It is an output.

### What counts as a NEW LOOK

The test is **not** "is this a new panel". It is:

> **Is there any element here that this panel does not already have?**

A new row, a new dialog, a new menu, a new kind of button, a new list — every one of them
counts. A new block inside an existing panel does not feel like designing a panel, and that
feeling is exactly how this rule gets skipped.

### The instrument — the `Cloned:` line

**Any reply that ships UI ends with a `Cloned:` line.** One line, naming what was copied
out of FIND and where it went:

```
Cloned: FIND's .lmenu dropdown -> SORT's preset picker; FIND's library bar -> SAVED SETUP.
```

If nothing was cloned, say that and say why:

```
Cloned: nothing — this build changed no UI.
Cloned: nothing — FIND has no equivalent of a curve editor. Built from the tokens.
```

**A missing `Cloned:` line means the rule was skipped, and the studio can see that for free.** It
is the same instrument as the `Searched:` line, for the same reason.

### The three searches, before the first line of CSS

1. **Does FIND already have this element?** Search `reference-panel.html` for the tag or the
   idea — `select`, `dialog`, `menu`, `rename`. FIND's own comments say why it does what it
   does.
2. **Has the studio already corrected this?** The list under "WHAT HE CORRECTS, OVER AND OVER" is
   every one of them.
3. **Which gate item covers it?** Run the gate below. If an item would fail, the answer is
   already written.

---

## THE GATE — run this before you show him anything

Every item is a yes or a no. A no is a build that is not finished.

| # | Check | Pass |
|---|---|---|
| 0 | **`assets/reference-panel.html` was opened, and the reply carries a `Cloned:` line** | see RULE ZERO above. Any new row, dialog, menu or control counts as a new look |
| 1 | No box carries a stroke in LIGHT mode | only four survive: the rule above the version bar, a text field, a control switched ON, and a divider BETWEEN items in a list. A line between siblings is not a line around a box |
| 2 | Dark mode puts those edges BACK | every stroke turned off in light has an `html.dark` rule |
| 3 | A field sits on `--card`, never on `--field` in light | `--field` is `#FFFFFF`, the same white as the page |
| 4 | Corners are 1.5px | `--radius` and `--radius-sm` both |
| 5 | Type runs 400 / 500 / 700 | 400 content, 500 chrome labels, 700 only pills, headers, footer. **Never 700 everywhere** |
| 6 | Tracking matches FIND | pill `.12em`, field label `.14em`, overlay label `.18em`, field text `.09em` |
| 7 | IBM Plex Mono, six woff2, bundled | never a remote link |
| 8 | The scaler is CSS `zoom` | never `transform: scale()` |
| 9 | The page cannot scroll | `scrollHeight - innerHeight` is **0** at L, M and S |
| 10 | One right edge | toolbar, content and the rule above the bar end at one x |
| 11 | Air around anything you press | ~8px button to end of its row highlight, ~6px list to scroll bar |
| 12 | One row height per row | `--row-h:34px`, and the text is centred in each box |
| 13 | No standing hint text | what a key does lives in its hover tip |
| 14 | The panel says nothing when a thing WORKS | `if (msg && !isErr) msg = "";` at the one choke point in `status()` |
| 15 | The scrollbar is FIND's | 9px, `--btn-line` thumb, 2px paper inset |
| 16 | No native widget shows through | no `<select>` popup, no number spinner |
| 17 | Icons are FIND's scale | 24px toolbar buttons, 15px marks, effective stroke 0.87–1.20px |
| 18 | Every interactive element has `data-tip` | never the native `title` |
| 19 | American spelling | color, organize, center |
| 20 | The theme travels in TOKENS, not in `html.dark .thing` rules | see the section below. A dark rule outranks a state rule and kills it |
| 21 | **Contrast is MEASURED, in both themes** | walk every text node, read its computed color against its nearest painted background. Small text 4.5:1, marks and borders 3:1. Never by eye |
| 21a | **In DARK, check APCA as well as WCAG 2** | once the brighter colour is under `#a0a0a0`, WCAG 2 overstates contrast. Measured here: dark muted text passed at 5.62:1 and scored Lc42, under the Lc75 floor for small text. WCAG stays the gate; APCA is the advisory that catches a muddy dark theme |
| 21b | **A role never contains a hex, and a test never pins one** | primitives hold values, semantics hold roles, one-way. A name that becomes false when the value changes is the wrong name — and a check that pinned `rgb(240, 72, 30)` failed on the first palette swap |
| 21c | **Reduced motion cuts what TRAVELS, not what fades** | `*{transition:none}` is the wrong reading. Kill smooth scrolling and fly-ins; keep the colour fades, which move nothing |
| 22 | **The accent carries no small text** | `#F0481E` is 3.72:1 on white, and white on it is the same 3.72:1. Fills and borders yes. Text no — use `--accent-txt` |
| 23 | **Text that is a CONTROL is `--ink`** | a tab label, a menu row, a button label. `--ink-soft` is for a static label next to a high-contrast value, and nothing else |
| 24 | **Every hit box clears 24 x 24, measured at S** | SC 2.5.8 counts the clickable area, not the icon. Grow a 14px mark with an `::after`. The scaler shrinks targets, so S is the size that must pass |
| 25h | **A `<pre>` is written flush at column 0** | it keeps every space in the markup. Indented content shows as a gap before the first word and rides invisibly onto the clipboard |
| 25e | **One control height per row** | a 19px chip beside a 26px button reads as two systems. Put the height in a token and let the row read it. The taller wins |
| 25f | **A list divides by a RULE BETWEEN items, plus hover** | the fourth legal stroke: a line BETWEEN siblings, never a line AROUND a box. A filled row head was tried on 29 Aug 2026 and rejected |
| 25o | **The rule sits UNDER its row, with more air below than above** | 10px above, 18px below. Centred between two rows it belongs to neither and floats — rejected twice before the ratio was fixed. Tufte: proximity decides ownership |
| 25p | **A rule per row is for a TABLE, not a list** | a table pairs a label at the far left with a value at the far right and the rule carries the eye across. A list of items is separated by whitespace. Getting this backwards is what "visual noise" means |
| 25ag | **Invert a small CONTROL, never a block of content** | FIND's 24px `.tb` inverts and it is right. The same move on a full prompt block reads as changing identity, not waking up. Built, tested, rejected 29 Aug 2026 |
| 25ae | **To lower a BOX, lower its background alpha — never `opacity`** | `opacity` fades the element and everything inside it. A background with alpha lowers only the paint it names |
| 25af | **Composite a translucent background before measuring it** | read raw, `rgba(23,23,23,.035)` is near-black. It made the contrast probe fail a legal pair and scored a block at APCA Lc0. Blend up the tree, stop at the first opaque layer |
| 25ad | **A test compares STATE, never a label** | two items may legitimately share a name, and a label comparison then reads a real move as no move. The starter deck proved it |
| 25k | **Hover answers with MARKS on a row that has no container** | a fill is a state layer and a state layer is for elements that already have a container (eBay). Invert the chip, lift the muted text, darken the rules — not a block that flashes |
| 25l | **Scope any hover that could read as SELECTED** | `@media (hover:hover) and (pointer:fine)`. Touch never fires "pointer left", so a tapped row or tab keeps its hover style and the UI looks stuck. Both halves are needed — mobile browsers claim hover:hover for long-press |
| 25m | **A signal is not a control** | the fade says the rail continues; the wheel moves it. An arrow button that only repeats the wheel is a button too many, and it came out the day it shipped |
| 25n | **A mark does one job** | the accent left rule marks a prompt block. It cannot also mark "just updated" — that moved to a badge and a tab dot. When a state mark goes universal, move the state, do not share the mark |
| 25i | **A wheel PANS a strip, it never selects** | selecting cannot be smooth: the smallest step is a whole item, so every notch is a leap. Map the delta 1:1, paint it this frame, and `preventDefault` only when the rail actually moved |
| 25z | **Never `scroll-behavior:smooth` on an input-driven scroll** | the animation lags behind the hand and reads as heavier, not lighter. Smooth is for a jump the user did not steer — an arrow button, a scrollIntoView |
| 25q | **A divider never responds to hover** | it is structure, and structure holds still. Darkening it made the whole ladder twitch as the pointer moved. Only the row's own contents answer |
| 25r | **Navigation state needs a fill you can see** | `--card` against the page is 1.11:1 in dark — a whisper. A selected tab gets its own token and four marks: fill, label colour, weight, underline |
| 25aa | **A state gets an OUTLINE, a control gets the FILL** | a filled accent rectangle is the loudest thing on the page and out-shouts the content it annotates. Border plus dot marks the row; the label reads in ink |
| 25ab | **Never label a fact the layout already states** | a `CURRENT` pill on the prompt directly above its own version history. Individually defensible, collectively noise |
| 25ac | **At 5px, commit to the shape** | the 1.5px house radius on a 5px square reads as a third shape. Marks are round: `border-radius:50%` |
| 25x | **One accent value on screen at rest** | two shades of the same accent read as a mistake. When the accent must be readable, INVERT the pairing (accent fill, ink text) before reaching for a darker step |
| 25y | **Deleting a container orphans its descendant rules** | `.parent .child` dies with `.parent` and the child still renders, at the inherited size. Grep for descendants before you delete, and gate that nothing in a dense row computes above 12px |
| 25t | **MEASURE before you optimise for speed** | the work here was 1.24ms; the lag was a 130ms transition and a 120ms lock this file asked for. Deleting work would have fixed nothing |
| 25u | **One speed token, and the gate enforces it** | every transition reads `--t`. Input work stays under RAIL's 50ms budget, and the gate fails a build that breaks either |
| 25v | **Throttle by DISTANCE, never by time** | a time lock delays the FIRST event, which is the one the user is waiting on. Accumulate the delta instead |
| 25w | **Never write the DOM on an event that fires constantly** | scroll and wheel handlers compare first and write only on a real change |
| 25s | **The content block is the click target too** | the biggest target on the page is the thing itself. Stand the handler down whenever a text selection is live, or highlighting a phrase overwrites the clipboard |
| 25j | **A filter that narrows to ONE moves the navigation to it** | otherwise the strip reads ALL while one item is on screen. Several or none goes back to ALL. And a label that lives on the strip, not in the panel, must be in the search haystack or it cannot be found |
| 25g | **A state inside an item is also visible outside it** | a prompt changed this turn wears a dot on its TAB. A mark you can only see after opening the thing is not a mark |
| 25b | **Nothing stops short of the column, and the column fills the panel** | a fixed cap wastes more width the SMALLER the UI size, because the scaler is CSS zoom. Let the column fill and hold the 80-character limit with fluid type (`cqw`), not with a cap |
| 25c | **One control for one state** | open-or-folded is ONE state, so it is ONE toggle, not two buttons. Armed means folded |
| 25d | **A number on screen is computed, never typed** | a character count, a total, a version — read it from the thing it describes. A typed number is a number that will be wrong later |
| 25a | **No filled box inside a filled box** | one painted surface, and it is the content. Written down since day one, broken by the prompt deck anyway. The instrument is the nested-box check in `llllloc:task-prompt/scripts/test-deck.py` |
| 25 | **A block of text stops at 80 characters** | WCAG 1.4.8. Cap the reading column in `ch`. A prompt running the full width of a 1040px deck was about 150 |

---

## A RANGE REPLACE SWALLOWS WHAT SITS BETWEEN THE ANCHORS

**29 August 2026, and this is the second shape of the same mistake in one session.** A doc
edit replaced everything between two headings — `find(A) .. find(B)` — to rewrite ONE
section. Two other sections lived between those anchors and were deleted with it. Nothing
failed: the deck's gate tests the BUILD, not the documentation, so it passed while two
pages of hard-won rules were gone.

**Never replace a range you have not printed.** Replace an exact block you can see, or
insert before a single anchor. And when a doc loses a section, no test will tell you —
count the headings before and after.

---

## A PATCH SCRIPT THAT WRITES AT THE END LOSES EVERYTHING

**29 August 2026, twice in one session.** A patch script applied four edits and wrote the
file at the end. The third edit missed its anchor, the script exited, and **the two
successful edits before it were thrown away** — silently, because the log had already
printed `ok` for both. The next screenshot showed a UI that was half old and half new and
made no sense.

**Write after every edit, not at the end.** One read, one replace, one write, per edit. It
costs nothing and it makes a missed anchor cost only that edit.

And read the log against the FILE, not against itself: `ok` in a script that later exits is
a lie.

---

## THE PIXEL-KIND TRAP CAUGHT A THIRD TIME — now in a border width

**29 August 2026.** A check read `borderLeftWidth` on a 2px rule and got **1.72414px**,
which is 2 ÷ 1.16, the L zoom step. The border was correct. The reading was not, and the
gate failed a build that was right.

Three separate times on this project now: the bottom bar that emptied itself, a
target-size check, and a border width. **Any number read back from the DOM inside
`#zoomRoot` is in the zoomed space.** Multiply by the zoom before comparing it to a CSS
pixel value — every time, without stopping to decide whether this one matters.

---

## A SKIPPED SUBTREE RETURNS STALE STYLES — the checker's version of the pixel trap

**Found 29 August 2026, while the gate was reporting a contrast failure that did not
exist.** A card below the fold sits in a `content-visibility:auto` subtree. The browser
does not restyle a subtree it is not rendering, so after a theme switch
`getComputedStyle` on that card still returned the OLD theme's grey. **The pixel it
paints is correct** — sampled it to be sure. Only the query was stale.

Two fixes did NOT clear it: an inline `content-visibility:visible`, and scrolling the
element into view. What works is measuring on a **fresh page load per theme** — no stale
subtree, no transition mid-flight, no hover state left over, and it is how the file is
actually opened.

**The rule: a checker must measure what is rendered.** `content-visibility`, `hidden`,
`display:none` and a collapsed `<details>` all give a query an answer that the screen does
not agree with. This is the same family as the pixel-kind trap below — a measurement that
looks authoritative and is not.

---

## THE PIXEL-KIND TRAP SHIPPED — and it emptied the bottom bar

**Found 29 August 2026, in code that had been running for weeks.** The deck's bottom bar
sheds parts as it narrows. Its test was:

```js
if (f.scrollWidth <= f.clientWidth + 1) break;      /* WRONG */
```

Under CSS `zoom` those two numbers round differently. The bar measured **5px too wide even
when it was completely empty**, so the condition could never be true, the loop ran to the
end, and it hid every part — the wordmark, the version, the credit. At every width. the studio
had to ask for the name back: *"bring back Lord of the prompt name + version name here"*.

**Two lessons, and the second is the bigger one.**

1. **A 1px tolerance is not a tolerance under zoom.** Use 6px, or measure something zoom
   does not round — whether the row WRAPPED, not whether it overflowed.
2. **Never let a shed order end with the identity.** A degrade path must name what it will
   never drop. This one dropped the product's own name first-class citizens last, which
   means it dropped them.

The trap was already written down in this file, in the section below. It shipped anyway.
That is the third time on this project a written rule failed without an instrument, so the
instrument is in the gate now: `test-deck.py` fails a deck whose bottom bar has lost its
name or its version.

---

## THE LIGHT-MODE CONTRAST TRAP — measured 29 August 2026

The dark ramp was measured on 11 August and widened, and the note that came
with it ends: *"Light mode is untouched."* It stayed untouched for eighteen
days and it was failing the whole time.

| Pair | Measured | Needs |
|---|---|---|
| `--ink-soft` `#8B8A85` on `--paper` | 3.46:1 | 4.5:1 |
| `--ink-soft` on `--card` | 3.03:1 | 4.5:1 |
| `--ink-soft` on `--btn` | 2.90:1 | 4.5:1 — under even the 3:1 non-text floor |
| white on an `--accent` fill | 3.72:1 | 4.5:1 |

Seven separate elements failed in the shipped prompt deck: the eyebrow, the
sub line, both `<summary>` labels, the spec key, the JUST UPDATED badge and the
bottom bar. **the studio reported it as "the UI is not that super clean, well
contrast".** He was right, and it was a number, not a taste.

**The fix, and it is two lines.** Light `--ink-soft` becomes `#6E6D68` — a value
FIND already uses. One token joins the set, `--accent-txt`, which is the same
vermilion one step down. Full numbers and the rule are in
`references/design-system.md`.

**The lesson for the gate: a ramp is not measured until BOTH themes are.**
Dark mode is the one that looks risky, so dark mode gets checked. The light
theme fails quietly, because grey on white still looks like design.

---

## THE SPECIFICITY TRAP — the bug you cannot see in light mode

**Found 17 August 2026, in the Lord Of The Prompt deck. It was live in three
states at once and only one of them was noticed.**

Count the specificity:

```
html.dark .copy-btn { background: var(--btn) }   /* 1 element + 2 classes */
.copy-btn.copied    { background: var(--accent) } /*             2 classes */
```

`html.dark .copy-btn` wins. So in DARK mode the dark rule beat every state the
control has. The button was clicked, the class went on, and nothing changed.

In that one panel it silently killed:

- the COPIED button, which stayed grey instead of going vermilion
- the JUST UPDATED card, which lost its accent border
- an armed toolbar button, which lost its accent ring

**Light mode looked perfect the whole time.** There is no `html.dark` rule in
light, so every state worked there. The build passed a visual check and shipped.

### The rule

**A theme difference on a component is a TOKEN, never a `html.dark .thing`
rule.** A token carries the theme without carrying specificity, so every state
rule still wins.

```css
:root      { --edge:transparent;   --edge-2:transparent;   --copy-bg:var(--btn-line) }
html.dark  { --edge:var(--line);   --edge-2:var(--btn-line); --copy-bg:var(--btn) }

.card     { border:1px solid var(--edge) }
.copy-btn { border:1px solid var(--edge-2); background:var(--copy-bg) }

.card.updated   { border-color:var(--accent) }   /* now wins in BOTH themes */
.copy-btn.copied{ background:var(--accent) }     /* now wins in BOTH themes */
```

`--edge` is the card / panel / block edge. `--edge-2` is the control edge. Light
sets both to `transparent`, which keeps the geometry and hides the stroke, and
dark puts the real color back. This is how rules 1 and 2 of the gate should be
built from now on.

### When a `html.dark` rule is still fine

Only when the property it sets has **no state rule anywhere** — a background on
a plain container, a re-colored inline SVG chevron. The moment a component grows
an `.on`, `.set`, `.acc`, `.updated`, `.copied` or `:focus` state, move that
property to a token.

### The check

For every `html.dark .x { p: … }` rule in the panel, search for `.x.` or `.x:`
setting the same property `p`. A hit is a live bug. Then arm each state in DARK
and read the computed value back — a state that looks armed in light proves
nothing about dark.

### One instance is live in FIND V1.20 itself

The scan finds three places in FIND where a dark rule sits over a state rule.
Two are guarded by an explicit `html.dark` copy of the state. **One is not:**

```css
html.dark .mini{border-color:var(--btn-line)}   /* line 297 */
.mini:focus{outline:none;border-color:var(--accent)}   /* line 299 - loses in dark */
```

A focused `.mini` select shows no accent border in dark mode. AWAITING the studio.
The one-line fix, when he approves it:

```css
html.dark .mini:focus{border-color:var(--accent)}
```

The token form is better and is what a new panel should use. FIND is left alone
until he says so, because eleven panels clone it.

---

## THE FOUR THINGS THAT LOOK CHEAP, AND WHY

These are the ones that made the studio say a panel "doesn't look as sleek as FIND".

1. **Bold everywhere.** FIND runs 400 / 500 / 700. A panel that runs 700 on every
   label reads heavy, not precise. This was the single biggest cause.
2. **No dark-mode rules.** If a panel has no `html.dark` component overrides, every
   border it declares is live in LIGHT mode, which is where the rule says there
   should be none. Light separates by tone. Dark puts the edges back.
3. **No shared row height.** Without `--row-h` every box in a row sizes itself from
   its own padding and they drift apart by two or three pixels each.
4. **Icons at the wrong scale.** An icon's weight on screen is
   `stroke-width x (render size / viewBox size)`. Two icons in one row can differ by
   36% and both look "fine" in the file.

---

## THE HOUSE RELOAD GLYPH

Use this exact glyph anywhere a panel reloads, rescans, refreshes or syncs. **Do not
redraw it.** the studio supplied the reference and one hand-drawn attempt already shipped
with the arrowheads sitting off the line.

```html
<svg width="12" height="12" viewBox="0 0 24 24">
  <polyline points="23 4 23 10 17 10" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="1 20 1 14 7 14" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

**Why it is drawn this way: the arc path ENDS on the arrowhead corner.** `L23 10` is
the same point as the corner in the first polyline. A head that is a separate shape
can drift, and it did.

An UNDO arrow is a different glyph. Do not swap it.

---

## PIXEL KINDS — the trap that hides inside CSS zoom

`clientWidth` is a **LAYOUT** pixel. `getBoundingClientRect()` is a **VISUAL** pixel.
Under CSS zoom they are different numbers.

- Keep any one calculation in ONE of the two spaces.
- **Never compare a `clientWidth` to a `getBoundingClientRect` value.**
- Never assert a computed pixel number against a literal in a test.

Mixing them made a test pass over a broken build, and it killed a drag.

## Pointer maths — prefer a delta over a position

A hit test that subtracts an origin from an event coordinate can be wrong in a host
whose browser handles zoom differently. Two rules that remove the whole class:

1. **Do not refuse an interaction on a distance threshold** when you can pick the
   nearest target instead. A threshold is a way to fail.
2. **Move by a DELTA, scaled by numbers from ONE rect read.** A ratio of two numbers
   from one measurement survives any coordinate convention.

## Testing a UI

- **PROVE EVERY NEW TEST FILE IN BOTH DIRECTIONS, WITH A COMMAND, NOT A PROMISE.**
  Added 18 August 2026, after four assertions shipped that passed on a broken
  build or failed on a correct one — one day after the rule to prove assertions
  both ways was written. **Every new test file takes the PREVIOUS build's folder
  as its first argument, runs the identical cases against it, and exits 1 if any
  guard case wrongly passes.** Name a guard case `C<n>`: it reproduces a reported
  fault and MUST fail on the build that had it. Name a property or a state sweep
  `D<n>` or `E<n>`: it may pass on both, and the runner must not demand
  otherwise. `SORT/tests/test-v941.js` is the reference implementation.
- **AFTER CHANGING A CLASS, WAIT THE TRANSITION OUT BEFORE READING A COMPUTED
  VALUE.** `.tb`, `.fc` and `.pill` all carry `transition:.13s`, so
  `getComputedStyle` in the same tick returns the value the transition is fading
  FROM. Measured: a chip armed with `.on` read back `rgb(58,57,52)` — `--btn` —
  while `--accent` was `#F0481E`. It failed a correct build twice. 260 ms clears
  the house 130 ms with room. Same family as the pixel-kinds trap: the test
  measured something the browser had not finished doing.

- **A synthetic `MouseEvent` skips hit testing.** A press that lands nowhere still
  "works". Drive a **real mouse** (Playwright `page.mouse`) or the test proves
  nothing about whether the click reaches the control.
- **Read the pixels, not the model.** For anything about drawing, scan the canvas.
  A test written from the same model as the code agrees with the code and both are
  wrong together.
- Ask of every green assertion: *what would still be true if this feature were
  broken?*

## Layout watch-outs

- A resize watcher only sees **resizes**. Collapsing a card or adding a list item
  changes the content, not the panel, so it never fires. Anything that opens,
  closes, adds or removes a block must call the re-layout itself.
- A `min-height` on a list stops it scrolling and makes the PAGE scroll instead.
  Give the card, the body and the list `min-height:0`.
- **A BOX THAT MAY SHRINK MUST ALSO CLIP.** `min-height:0` lets a BOX shrink and
  does nothing to the content inside it. Put a zero on a section whose children
  keep their own floors and the section shrinks while its rows paint straight out
  of it — the same overflow, moved one level down, now landing on a sibling
  instead of on the bar. Measured on SORT: `#wBody` squashed to 119 layout px
  around content that cannot go below 170. **Add `min-height:0` and an `overflow`
  together, or add neither.** Exactly ONE box in a panel clips, and everything
  inside it keeps its natural floor. That box is FIND's `.res`.
- **When a chain will not shrink, WALK IT FIRST.** Print `display`, `flex`,
  `min-height` and `overflow` for every link from the element to `<html>` before
  changing any of them. A partial fix looks exactly like no fix.
- A card with `flex:1` that has nothing to fill leaves an empty band. Give it
  `flex:0 0 auto` and let `.grow` take the slack.
- In CSS a `min-width` beats a `max-width`. Clear both when you clamp a box.

## Adobe CEP, settled — do not re-investigate

- **A panel extension cannot change its own size at run time in Premiere Pro.**
  Adobe's documentation says so. The manifest `<Size>` applies when a workspace
  first creates the panel. After that the workspace wins, and a panel that another
  extension opens is created fresh each time and takes the manifest size again.
- Adobe-CEP issue 48 records the manifest size being unreliable, still open.
