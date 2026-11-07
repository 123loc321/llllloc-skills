# THE DESIGN SYSTEM — locked, editorial-monospace, compact

## Contents
- Tokens (copy verbatim, both themes)
- The palette — five primitives, and two steps they do not contain
- Lowering a box without lowering what is in it
- Hover: which species, and how to tell
- A state mark is an outline, and a label is not a fact-repeater
- One orange on screen
- Two token tiers, and a one-way reference
- Contrast — WCAG 2 is the gate, APCA is the truth in dark mode
- Deleting a container orphans its descendants
- Speed — measure before you optimise
- Motion — reduce what travels, keep what fades
- Dividing a list — the rule belongs to the row above it
- Hover — marks, not a block, and never the structure
- Never leave a gap — the column fills, the TYPE holds the measure
- Target size — the hit box, not the picture
- The size ladder — obey it
- Layout
- Bottom bar (there is no header)
- The four global systems (clone verbatim)
- Component library
- Narrow dock rail
- Copy voice
- UI motion
- Hard don'ts


Every value here is lifted from `assets/reference-panel.html` (SORT). That file is the
source of truth: if this document and SORT ever disagree, **SORT is right**.

The look: near-black monospace on a light page (or light on near-black in dark mode), thin
hairlines, one vermilion accent, near-square corners, no shadows, no gradients, no
decorative chrome. Technical, editorial, Swiss.

---

## Tokens (copy verbatim, both themes)

```css
:root{
  --paper:#FFFFFF; --card:#F1F0ED; --ink:#161513; --ink-soft:#8B8A85; --line:#E5E4E0;
  --field:#FFFFFF; --btn:#ECEBE8; --btn-line:#D9D8D4;
  --accent:#F0481E; --accent-dk:#D33E16;
  --radius:1.5px; --radius-sm:1.5px;   /* 15 Aug 2026 - the studio halved these twice */
  --font-mono:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
html.dark{
  --paper:#171613; --card:#201F1B; --ink:#EDEBE4; --ink-soft:#8F8E86; --line:#33322D;
  --field:#191814; --btn:#2B2A25; --btn-line:#3C3B35; --accent:#F0481E; --accent-dk:#F5602F;
}
```

Text selection is accent-tinted, dark needs the stronger tint:

```css
::selection{background:rgba(240,72,30,.26);color:var(--ink)}
html.dark ::selection{background:rgba(240,72,30,.42);color:var(--ink)}
```

**Never add a second accent.** Vermilion marks the primary action, the armed state, and
hover on the bar controls. Nothing else.

### Edge tokens — how the theme travels

Light hides every edge, dark puts it back. Carry that in TOKENS, never in
`html.dark .thing` rules:

```css
:root     { --edge:transparent; --edge-2:transparent }
html.dark { --edge:var(--line);  --edge-2:var(--btn-line) }
.card     { border:1px solid var(--edge) }     /* card, panel, block */
.tb,.fld  { border:1px solid var(--edge-2) }   /* controls */
```

**A `html.dark .thing` rule outranks a state rule like `.thing.on` and silently
beats it in dark mode, while light mode looks perfect.** This shipped live in
three states of one panel. Read the SPECIFICITY TRAP section in
`LOCKED-RULES.md` before you theme any control.

---

## The palette — five primitives, and two steps they do not contain

**the studio set the palette on 29 August 2026** from his ARRIVAL FLEET component sheet:

| Role | Value |
|---|---|
| CANVAS | `#FFFFFF` |
| SURFACE | `#F2F2F2` |
| INK | `#171717` |
| LIVE | `#F44E16` |
| TERTIARY | `#909090` |

**Two of the five cannot carry small text, and that is measured.**

| Pair | WCAG 2 | Needs |
|---|---|---|
| TERTIARY on CANVAS | 3.19:1 | 4.5 for text |
| TERTIARY on SURFACE | 2.85:1 | under even the 3:1 mark floor |
| LIVE on CANVAS | 3.53:1 | 4.5 for text (fine as a mark) |
| white on a LIVE fill | 3.53:1 | 4.5 for a badge label |

So the sheet gets **two extra steps of hues it already has** — not new colours, the legal
text weight of colours that are already there: `#6B6B6B` (5.33 / 4.76) and `#C93C0E`
(5.08 / 4.54, white on it 5.08).

**A five-colour sheet is complete for a DARK UI and two short for a light one.** In dark
the same five work unchanged by WCAG — a light value on a near-black page has room to
spare. See the APCA section below for why "unchanged by WCAG" was not the end of it.

---

## Lowering a box without lowering what is in it

**the studio, 29 August 2026:** lower the opacity of the box only — the text and the accent rule
keep theirs.

**Never reach for `opacity`.** It fades an element and everything inside it, so the prompt
text and the accent edge would go with the box. That is the opposite of the ask.

**Use a background with alpha.** It lowers only the paint it names:

```css
:root     { --surface-rest:rgba( 23, 23, 23,.035) }   /* INK at 3.5%     */
html.dark { --surface-rest:rgba(242,242,242,.045) }   /* SURFACE at 4.5% */
```

Measured: `#F7F7F7` over the light page, `#202020` over the dark one — about half the
weight of the full `--card` surface. Hover then steps it up to the full surface, so rest
and hover are two points on one scale instead of two unrelated decisions.

**A translucent fill breaks any checker that reads colours naively**, and it broke both of
mine. `rgba(23,23,23,.035)` read raw is *near-black*: the contrast probe called a legal pair
a failure, and APCA scored the prompt block at **Lc 0**. Both probes now walk up the tree,
blend each layer onto the one behind it, and stop at the first opaque one. **Composite
before you measure.**

---

## Hover: which species, and how to tell

**Both answers are correct, on different elements, and eBay's playbook is the test.**
An element **with a container** takes a state layer — a fill. An element with **no
container** takes an ink shift.

| Element | Container? | Hover answer |
|---|---|---|
| card head row | no — it is bare text on the page | the ID text darkens, the count comes to full ink |
| prompt block | yes — it is a painted surface | the fill steps one tone (`--surface-rest` → `--btn`) |

**An INVERT was built and rejected on 29 August 2026** — the block flipping to ink with
page-tone text. It reads as the block changing identity rather than waking up, and at 0s it
lands as a flash across the largest object on the page.

**Invert a small CONTROL, never a block of content.** FIND's `.tb:hover` inverts and it is
right there: a 24px button, gone before you finish reading it. The same move on a 700-line
prompt is a different event. Scale decides the treatment, not consistency.
| divider | it is structure, not an element you act on | nothing. Structure holds still |

**Measured:** the prompt block's step is a **3.1% overlay in light and 3.5% in dark** —
eBay's per-state increment is 4%, Material's hover layer is 8% with the note to keep it low
so it does not distract. On a block that large, anything more reads as a flash.

**And it earns its keep.** The prompt block is the click-to-copy target, so until it got
this the biggest button on the page was the only one with no hover state at all.

---

## A state mark is an outline, and a label is not a fact-repeater

**Two cuts on 29 August 2026, and they come from one idea.**

The `CURRENT` pill sat on a prompt that had its own version history directly beneath it.
the studio: *"no need for current box, remove."* **The pill was labelling a fact the layout
already stated.** If a reader can see the answer in the arrangement, a word for it is
noise. Look for these — they hide easily, because each one is individually defensible.

The `JUST UPDATED` badge then inherited the pill's TREATMENT rather than its own: an accent
**1px outline and a 5px dot, with the label in ink** — not a filled accent rectangle.

```css
.badge-new{background:none;border:1px solid var(--accent);color:var(--ink)}
.badge-new .bdot{width:5px;height:5px;border-radius:50%;background:var(--accent)}
```

**Why the outline wins in a long list.** A filled accent rectangle is the loudest object on
the page, and in a stack of ten rows it out-shouts the content it is annotating. As an
outline the accent still marks the row — a border and a dot are non-text, and 3.53:1 clears
the 3:1 they need — while the label reads in ink at 17.93:1. **Reserve the fill for a
control the reader acts on; a state gets an outline.**

**And every accent mark is round.** A 5px square carrying the 1.5px house radius reads as a
soft-cornered third shape nobody chose. At that size, commit: `border-radius: 50%`.

---

## One orange on screen

The accent has two values: the LIVE primitive, and a darker text step for the case where
the accent must carry small type. **The moment both appear on the same screen, the system
looks broken** — two vermilions a shade apart read as a mistake, not as a choice. the studio,
29 August 2026: *"this color is so weird."*

The badge was filling with the darker step while COPIED and the dots beside it used pure
LIVE. **The fix was not a new colour, it was a different pairing:** fill with LIVE and write
on it in INK, which measures 5.08:1 and clears 4.5. Dark mode had been doing that all along;
both themes match now.

**The rule.** Everything painted on screen at rest is the accent token itself. The darker
step is an escape hatch for accent-as-small-text, and the only thing that still uses it is
the empty-search message — which is text, on the page, and needs 4.5:1. **When the accent
has to be readable, invert the pairing before you reach for a second value.**

The gate walks every visible element and fails a build painting any accent that is not the
token.

---

## Two token tiers, and a one-way reference

**Primitives hold values. Semantics hold roles. A role never contains a hex.**

```css
:root{
  --c-canvas:#FFFFFF; --c-surface:#F2F2F2; --c-ink:#171717;   /* TIER 1 */
  --c-live:#F44E16;   --c-tertiary:#909090;
  --paper:var(--c-canvas); --card:var(--c-surface);           /* TIER 2 */
  --ink:var(--c-ink);      --accent:var(--c-live);
}
```

Three-tier systems add component tokens; most systems stop at two, and this one should.
The rule that matters is the **one-way reference**: a role points at a primitive, never at
a raw value and never sideways at another role. That is what turned "limit colour to this"
into a five-line edit instead of a search through eight hundred lines of CSS.

**A name that would become false when the value changes is the wrong name.** `--accent` is
a role and survives a rebrand; `--vermilion` would not. The same rule applies to TESTS: a
check that pinned the literal `rgb(240, 72, 30)` failed the moment the palette changed.
**Read the token, never the value.**

---

## Contrast — WCAG 2 is the gate, APCA is the truth in dark mode

The dark ramp was measured on 11 August and the light ramp on 29 August, both with the
WCAG 2 formula, and both passed. Then the APCA author's own note turned up:

> Once the brighter colour is darker than `#a0a0a0`, WCAG 2's prediction degrades until it
> stops being useful — and it **overstates** contrast when both colours are dark.

Our dark page is `#171717`. Every dark-mode number was inside that range. **Measured on
this file:**

| Pair | WCAG 2 | APCA |
|---|---|---|
| dark muted text `#909090` on `#171717` | 5.62:1 — a comfortable pass | **Lc 42** |
| light muted text `#6B6B6B` on `#FFFFFF` | 5.33:1 | Lc 77 |

APCA's floor for small text is **Lc 75**; Lc 45 is the decorative floor. So the dark
theme's labels were sitting just above *decorative* while WCAG called them fine. The fix
mirrors what light mode needed: TERTIARY stays the MARK colour and dark muted TEXT takes
its own step, `#CCCCCC`, which reaches Lc 75.

**How to work with both.** WCAG 2.2 is the standard and stays the pass/fail gate — it is
what anyone auditing this will use. APCA runs alongside as an **advisory number printed on
every build**, because it is the one that catches a dark theme going quietly muddy. Where
they disagree in dark mode, believe APCA and fix it.

**Two things APCA also makes plain, and neither is being fixed.** It weights font size and
weight, and this system's 8–9px labels are below the size any APCA table covers. That is
the house style and it is a deliberate trade. Know that it is a trade.

---

## Deleting a container orphans its descendants

**29 August 2026.** `.card-id` was removed from the head row. Its child rule was
`.card-id .dim { font: 500 8.5px … }`, a descendant selector, so it went with the parent —
and `.dim` was left in the markup with **no rule at all**, inheriting the 16px body size.
the studio: *"this word is so big."*

**Nothing caught it.** Contrast passed: the colour was inherited and legal. Layout passed:
nothing overflowed. The gate tested everything except the one thing that broke.

**Two rules come out of it.**

1. **When you delete a container, grep for its descendants.** A rule scoped to a parent dies
   silently with the parent, and the orphan still renders — just wrong.
2. **Check that nothing in a dense row inherits the body size.** That is now a gate: any
   element with text inside a head row that computes above 12px fails the build. It is the
   cheapest possible detector for a whole class of orphaned rule.

---

## Speed — measure before you optimise

**the studio, 29 August 2026: "prioritize speed over everything."** The obvious answer would have
been to start deleting work. Measured first, and the obvious answer was wrong.

| Interaction | Main-thread work |
|---|---|
| tab click | **1.24 ms** |
| keystroke in SEARCH | **0.08 ms** |
| collapse everything | **0.18 ms** |
| a scroll frame | **0.03 ms** |

RAIL's budget is 50ms of input work so the paint lands under 100ms. Every one of these was
already two orders of magnitude inside it. **The JavaScript was never slow.** What felt slow
were the two delays the file had ASKED FOR:

1. **A 130ms transition on forty elements.** Every hover and every state change took an
   eighth of a second to finish.
2. **A 120ms lock on the wheel.** A time lock makes the FIRST notch wait too, and the first
   notch is the one you care about.

**The fixes, and why each is safe.**

```css
:root{ --t:0s }        /* one token. Every transition in the file reads it. */
```

NN/g's warning that an animation can be "too fast" is about **motion** — a thing travelling,
which needs time to be followed. Nothing here travels; these are colour changes, and a
colour change at 0s reads as instant rather than jarring. One line softens it if that ever
changes.

**Throttle by DISTANCE, not by time.** A time lock delays the first event. An accumulator
does not: a mouse notch arrives as 100–120 units and fires immediately, while a trackpad's
stream of small deltas still costs one step per 50 units of travel. Reset the accumulator
after 250ms so two gestures never add up.

**Do not write to the DOM on an event that fires constantly.** The rail's fade recomputed
and rewrote `className` on every scroll event, dirtying style even when nothing changed, and
a `mask-image` repaint is not free. Compare first, write only on a real change.

**What the measuring bought, end to end:** DOM ready 136ms → **74ms**, first paint 188ms →
**100ms**, forty animating elements → **five**.

**Speed is now a gate, not a hope.** `test-deck.py` fails a build whose input work passes
50ms, or whose transitions do not all read the one token. A future change that quietly adds
a delay fails instead of shipping.

**What was NOT touched, and why.** Six embedded font faces, about 75KB decoded. Dropping the
latin-ext subsets would save 24KB, and would silently break the first accented character
anyone pastes into a prompt. 24KB against a wrong glyph is a bad trade.

---

## Motion — reduce what travels, keep what fades

The common implementation is wrong:

```css
@media (prefers-reduced-motion: reduce){ *{transition:none !important} }   /* WRONG */
```

The preference asks for less **motion**, not for a UI with no feedback. A colour fade does
not move anything and does not trigger a vestibular response. What has to go is anything
that **travels**: smooth scrolling, a strip sliding a tab into view, a panel flying in.

```css
@media (prefers-reduced-motion: reduce){
  html,body,#scroller,.trail{scroll-behavior:auto !important}
}
```

Keep the .13s hover fades. Cut the journeys.

---

## Dividing a list — the rule belongs to the row above it

**Three attempts on 29 August 2026. The first two were rejected by eye, and the sources
say why.**

1. A filled row head. Rejected in the hour: *"dont really like the box background here."*
2. A rule between rows, `border-top`, 20px above and 16px below. Rejected too: *"im still
   not very happy with the UI especially the divider part."*
3. A rule **under** each row, tight above and airy below. This one stayed.

**The second one floated, and that is measurable.** With 20px above and 16px below, the
rule sat almost centred between two rows, so it belonged to neither. Tufte's note on
tables gives the rule: a row has a line directly **below** it, and the distance to the next
line is larger than the distance to its own row. Proximity decides ownership.

```css
#scroller>.card,#scroller>.group{border-bottom:1px solid var(--line);padding:0 0 10px}
#scroller>.card                 {margin:0 0 18px}      /* more air below than above */
```

**10px above, 18px below. The gate checks that ratio**, because "it floats" is otherwise a
matter of opinion and this one had to be settled twice.

**A LIST and a TABLE are not the same case.** eBay's playbook says dividers separate
*groups*, not individual list items, and Material warns that heavy full-bleed dividers
become noise. Both are right about a list. the studio's reference layouts are **tables** — a game
inventory sheet, a product spec sheet — where the ladder of rules IS the structure and a
label at the far left has to be paired with a value at the far right. That is the one place
a rule per row earns its keep. The SPEC sheet is ruled per row and dropped its fill; the
prompt stack takes the same rhythm so the two read as one ladder.

**Keep the rule at 1px and at `--line`.** The data has to dominate the grid. A rule you
notice before you notice the content is doing the wrong job.

**Retire the machinery the old shape needed.** Marking the first VISIBLE row with a class
only existed because the rule was on TOP and `:first-child` cannot see through a filter.
With the rule underneath, every row carries its own and the last one closes the table.

---

## Hover — marks, not a block, and never the structure

**Rejected on 29 August 2026:** a `--btn` fill under the head on hover. *"The UI for that
part doest look sleek enough."*

**Why a fill was the wrong species, from the sources.** eBay splits the two cases: an
element WITH a container takes a state layer — a semi-transparent fill — while an element
with NO container takes an ink shift. The head row has no container. Material puts a hover
layer at 8% and says keep it low; ours measured about 7%, so the opacity was right and the
SHAPE was wrong. A hard-edged block appearing under bare text reads as a flash.

**The hover still has a job** — GitLab's own issue names it: on a wide row you cannot tell
which item the button on the far right belongs to. So make it precise, not absent:

```css
@media (hover:hover) and (pointer:fine){
  .card:hover>.card-head .tab   {background:var(--ink);color:var(--paper)}   /* FIND's own */
  .card:hover>.card-head .chars {color:var(--ink)}
}
```

**Hover must NOT touch the divider.** The first version darkened the rules above and below
the hovered row, and the whole ladder twitched as the pointer ran down the page — *"hovering
should not highlight the divider line."* **A divider is STRUCTURE, and structure holds
still.** Only the row's own contents answer a hover; the grid never moves.

**A divider between items is the FOURTH stroke this system allows.** The distinction is the
whole rule: a line BETWEEN siblings is a divider, a line AROUND one thing is a border.

**Scope any hover that could be read as a SELECTED state.** Touch never fires a "pointer
left" event, so on a tablet a tapped row or tab keeps its hover style and the UI looks
stuck. `@media (hover:hover) and (pointer:fine)` needs both halves — mobile browsers claim
`hover:hover` for long-press, so `pointer:fine` is what sorts them. A plain button's hover
can stay unscoped; a stuck button says nothing false, a stuck ROW does.

**A state inside an item must also be visible outside it.** A prompt changed this turn
wears a dot on its TAB. A mark you can only see after opening the thing is not a mark.

---

## Never leave a gap — the column fills, the TYPE holds the measure

**Two rounds, 29 August 2026.** First he circled dead space beside a text block:
*"never leave a gap like this, it must adapt to the width"*. The answer was one cap on
the column instead of two fighting caps. Then he circled the margins that cap left on a
wide panel: *"make it always adapt to panel width as well, but of course have some
margin"*.

**A fixed cap cannot do both jobs, and the scaler is why.** The scaler runs on CSS
`zoom`. At the S step every CSS pixel paints smaller, so a 600px column shrinks on screen
while the panel does not move. **The smaller the UI size, the more width the cap threw
away** — which is the opposite of what a size control should do.

**So the column fills, and the TYPE holds the 80-character limit.**

```css
.app{width:100%;max-width:1000px;margin:0 auto;padding:14px clamp(16px,4%,48px) 16px}
.cbody{container-type:inline-size}                      /* the block measures itself */
.prompt-text{font-size:clamp(11px,2.07cqw,20px)}        /* about 76 characters, always */
```

`1cqw` is one percent of the block's own width, so a wider panel gets bigger type on the
same number of characters. **The coefficient is measured, not guessed:** IBM Plex Mono
advances 0.637em for each character, so a line of 76 needs 48.4em and 100 / 48.4 = 2.07.

The floor of 11px keeps a narrow dock on the ladder. The ceiling of 20px and the 1000px
cap are the SAME constraint written twice — 76 characters at 20px is 993px — so past
that width the column centers and the leftover is a margin, not a gap.

**Verified, not assumed.** The gate reads the line length at 600, 780, 1000, 1400 and
1920px, at all three UI sizes: 15 measurements, none over 80. It also fails a column
that uses less than 80% of the panel.

**One consequence, and it is worth knowing.** The fluid rule cancels the zoom for that
block, so the L / M / S button no longer changes the prompt's size on screen — it still
scales all the chrome. Tie the coefficient to the size step if you want the button back.

---

## Target size — the hit box, not the picture

WCAG 2.2 SC 2.5.8 asks **24 x 24 CSS pixels**, and it counts the area you can
click, not the icon drawn inside it. The house ladder has 14px bar buttons and a
15px toggle. Both are legal, and both need the area added back:

```css
.hbtn{position:relative}
.hbtn::after{content:"";position:absolute;left:50%;top:50%;
             width:24px;height:24px;transform:translate(-50%,-50%)}
```

The mark stays 14px. Nothing moves on screen. The target becomes 24px.

**Measure at S, not at L.** The scaler runs on CSS `zoom`, so a target shrinks
with the UI. A control must clear 24px at the SMALLEST step. That is why the
tab is 30px: 30 x 0.83 = 24.9.

**And measure in one kind of pixel.** `getComputedStyle` gives LAYOUT pixels.
`getBoundingClientRect()` gives VISUAL pixels. Under zoom they are different
numbers. Divide the rect by the zoom before you compare it to anything.

---

## The size ladder — obey it

Harmony breaks through invented sizes, not wrong colours.

**Control heights** — 24px toolbar button · 19px chip / header button · 16px divider ·
15px toggle · 14px tiny button and bar control · 12px badge and bar icon · 10px spinner
arrow · 9px overlay dot · 3px progress track. **Chrome never exceeds 24px.**

**Type sizes** — 11px pill and overlay title · 10.5px field input · 9.5px value, status,
list text · 9px label, hint, field label · 8.5px bottom bar, tooltip, select · 8px meta ·
7px micro-caption. **Nothing exceeds 11px.**

Content targets clicked by eye (preset tiles, mode buttons) may break 24px — cap them near
30–32px and say why in a comment.

**AN ACCENT RULE ON THE LEFT MARKS THE CONTENT, NOT A STATE.** On 29 August 2026 the 2px
vermilion rule started life as the just-updated marker; the studio asked for it on every prompt
block the same evening. It is now the block's own edge — the thing you copy, marked — and
the update state moved to its badge and the dot on its tab. **A mark does one job.** When
a state mark goes universal, move the state onto a different mark rather than sharing one.

Watch the specificity: `html.dark .prompt-text{border:1px solid var(--edge)}` is a
shorthand and it silently overwrote the accent edge. Set the three other sides by name.

**ONE CONTROL HEIGHT PER ROW.** the studio, 29 August 2026: *"align the buttons sizes, make
other button same height with the copy button now"*. A chip at 19px beside a button at
26px reads as two systems in one row. Put the height in a token and let every control in
that row read it:

```css
:root{ --ctl-h:26px }
.tab, .now, .badge-new, .copy-btn { height:var(--ctl-h) }
```

The ladder still governs which heights EXIST. This governs which one a row picks. When a
row mixes two, the taller one wins, because the shorter one is the one that looks broken.

**The rule that matters most:** never restyle a shared component locally. One panel carried
`.dab .pill{padding:11px 14px;font-size:11.5px}` and silently grew out of the family.

---

## Layout

```css
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--paper);color:var(--ink);font-family:var(--font-mono);
          -webkit-font-smoothing:antialiased}
html,body{height:100%}
#zoomRoot{display:flex;flex-direction:column;zoom:var(--uis,1);height:100%}
.app{width:100%;max-width:none;margin:0;padding:16px 14px 20px;
     display:flex;flex-direction:column;flex:1}
.card{background:transparent;border:none;border-radius:0;overflow:visible;
      display:flex;flex-direction:column;flex:1}
.cbd{padding:0;display:flex;flex-direction:column;flex:1}
.grow{flex:1;min-height:0}          /* pushes the bottom bar down */
```

The card is **flat** — no fill, no border. A boxed container is allowed only for genuinely
separate collapsible sections (EASEUP), and the reason belongs in a comment.

**NO BOX INSIDE A BOX. One painted surface, and it is the content.** This rule was already
here on 29 August 2026 and the prompt deck broke it anyway: a white block inside a grey
block. the studio saw it in one look — *"I dont like how the prompt is boxed inside a prompt
card"*. Writing the rule a second time would change nothing, so it now has an instrument:
`llllloc:task-prompt/scripts/test-deck.py` walks every painted element and fails the build
when its nearest painted ancestor is also painted. Clone that check into any gate you write.

**When a fill stops earning its keep, remove it.** The card carried a fill so a reader could
tell one item from the next in a long stack. Adding the tab strip put one item on screen, so
the fill had no job left. A tone step is separation, and separation you do not need is
clutter.

---

## Bottom bar (there is no header)

`.hd{display:none}`. The bar carries everything:

```css
.foot{display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin-top:11px;padding:9px 0 0;
      border-top:1px solid var(--line);font:700 8.5px var(--font-mono);
      letter-spacing:.05em;color:var(--ink-soft)}
.foot .fbrand{font:700 8.5px/1 var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink)}
.foot .fbtns{margin-left:auto;display:flex;align-items:center;gap:11px}
/* bare in the bar - no boxes */
.foot .chip{border:none;background:none;padding:0;height:auto;color:var(--ink);
            font-size:8.5px;font-weight:700;letter-spacing:.05em;margin-left:-3px}
.foot .fby{margin-left:3px}
.foot .hbtn{width:14px;height:14px;min-width:0;padding:0;margin:0;border:none;background:none;
            color:var(--ink);line-height:1}
.foot .hbtn svg{width:12px;height:12px;display:block}
.foot #sizeBtn{font:700 11px/1 var(--font-mono);letter-spacing:0}
.foot .hbtn:hover{background:none;border-color:transparent;color:var(--accent)}
```

Markup order: wordmark `NAME.` · version chip · `made by llllllloc` · `.fbtns` (size, tips,
theme). `fitFooter()` sheds the wordmark, then the version, then the "made by" prefix as
the panel narrows — measuring **widths**, not element tops (a centred bar makes tops
useless).

---

## The four global systems (clone verbatim)

### 1 — Theme toggle
`html.dark` class + filled sun/moon SVGs, persisted under `<panel>.theme`. **Defaults to
dark.** Every button must set an explicit `color`, or it renders black-on-black.

### 2 — L / M / S size scaler
```js
var SIZES = [["L", 1.16], ["M", 0.98], ["S", 0.83]];
```
**CSS `zoom` on `#zoomRoot`, never `transform: scale()`.** `zoom` scales the LAYOUT, so
`height:100%` reaches the panel floor by itself and **the page can never scroll**.
`applySize()` sets ONE custom property and nothing else:

```js
document.documentElement.style.setProperty("--uis", String(s));
```

**Do not compute a layout height.** `transform: scale()` scales only the paint, so a panel
using it must lay out at `innerHeight / scale` and then correct the document height with a
margin. That correction was always a little short: measured on FIND V1.16 at 325x762 the
page could still scroll **155px at S**, with nothing down there. Scroll it and the toolbar
left the top of the panel while the bottom bar floated 172px above the floor. Every panel in
the suite had it. The check is one line:

```js
document.documentElement.scrollHeight - window.innerHeight   /* must be 0 at L, M and S */
```

**A trap that comes with `zoom`:** `getComputedStyle` and `clientWidth` report LAYOUT pixels
and `getBoundingClientRect()` reports VISUAL pixels, and under zoom those are different
numbers. A 1px rule reads back as 0.83px at S. **Never compare one to the other in a test,
and never assert a computed pixel number against a literal.**
result lands back on 100%. `syncZoomHeight()` gives the root a **definite** height derived
from `window.innerHeight / scale`, which is what lets the inner flex chain hand leftover
space to `.grow`. Guard it: below 80px of viewport, commit nothing and wait — a restoring
panel reports nonsense early. Re-measure on resize, on `document.fonts.ready`, and on a
staged retry ladder (60/250/600/900/1800/3000 ms).

### 3 — Hover tooltip engine
One delegated `mouseover` handler reading `data-tip`. The box is `position:fixed` and lives
**outside** `#zoomRoot`, so `applySize()` sizes it by hand (font 8.5×s, padding 6×s / 8×s,
max-width 210×s). Narrow dock pins it to `x=4`.

```css
#tip{position:fixed;z-index:99;max-width:210px;background:var(--ink);color:var(--paper);
     font:700 8.5px/1.55 var(--font-mono);letter-spacing:.06em;text-transform:uppercase;
     padding:6px 8px;border-radius:var(--radius-sm);pointer-events:none;display:none}
```

### 4 — Tips on / off
Speech-bubble button in the bar mutes every tooltip, persisted under `<panel>.tips`.

---

## Component library

### Icon toolbar — the house idiom
```css
.tbar{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.tb{width:24px;height:24px;padding:0;border:1px solid var(--btn-line);
    border-radius:var(--radius-sm);background:var(--btn);color:var(--ink);cursor:pointer;
    display:inline-flex;align-items:center;justify-content:center;transition:.13s;flex-shrink:0}
.tb:hover:not(:disabled){background:var(--ink);color:var(--paper);border-color:var(--ink)}
.tb.set{border-color:var(--accent);color:var(--accent)}   /* configured */
.tb.on{background:var(--accent);border-color:var(--accent);color:#fff}  /* armed */
.tb.acc{background:var(--accent);border-color:var(--accent);color:#fff} /* primary */
.tb:disabled{opacity:.35;cursor:default}
.tbd{width:1px;height:16px;background:var(--line);flex-shrink:0;margin:0 2px}
.tbw{position:relative;display:inline-flex}   /* wrapper for a badge */
.bdg{position:absolute;top:-4px;right:-4px;min-width:12px;height:12px;padding:0 2px;
     border-radius:6px;background:var(--accent);color:#fff;font:700 7px/12px var(--font-mono);
     text-align:center;display:none;pointer-events:none}
```
Icons are 12×12 SVG on `currentColor`, stroke-width 1.3–1.5. **Prefer a `.tb` over a small
text pill.** Group with `.tbd` dividers.

### Buttons
```css
.pill{display:block;width:100%;border:1px solid var(--btn-line);border-radius:var(--radius-sm);
      background:var(--btn);color:var(--ink);font:700 11px var(--font-mono);letter-spacing:.09em;
      text-transform:uppercase;padding:9px 12px;cursor:pointer;text-align:center;
      transition:background .15s,color .15s,border-color .15s}
.pill:hover:not(:disabled){background:var(--ink);color:var(--paper);border-color:var(--ink)}
.pill.acc{background:var(--accent);color:#fff;border-color:var(--accent)}
.pill.sm{padding:5px 10px;font-size:9.5px;width:auto;display:inline-block}
.pill:disabled{opacity:.4;cursor:default}
.dab{display:flex;flex-direction:column;gap:8px;margin-top:11px}   /* stack */
.xb{width:14px;height:14px;...}                                    /* tiny inline action */
```

### Field `.fld` — the workhorse input
```css
.frow{display:grid;grid-template-columns:1fr auto;gap:8px}
.fld{display:flex;align-items:center;gap:8px;border:1px solid var(--btn-line);
     border-radius:var(--radius-sm);background:var(--field);padding:5px 6px 5px 10px;
     cursor:text;min-width:0}
.fld:focus-within{border-color:var(--accent)}
.fld .fl{font:700 9px var(--font-mono);letter-spacing:.09em;text-transform:uppercase;
         color:var(--ink-soft);flex-shrink:0}
.fld input{flex:1;min-width:0;border:none;background:transparent;
           font:700 10.5px var(--font-mono);letter-spacing:.03em;color:var(--ink)}
```
Spinner arrows inside a field are **10px** tall. Two 13px arrows silently make the whole
field ~10px taller than SORT's — that is a real bug that shipped once.

### Tab strip — many items, one on screen

**`assets/tab-strip.html` is the working reference.** Open it, clone the marked
block, and never write a tab by hand — an engine builds them from `data-tab`
and `data-tname` on each panel.

Use it when a page holds MANY siblings of one kind and the reader works on one
at a time: one prompt, one shot, one preset. Not for steps in a sequence. Not
for a hierarchy. Under two items the engine hides itself.

```css
.tabs {display:flex;align-items:flex-end;gap:6px;border-bottom:1px solid var(--edge)}
.trail{flex:1 1 auto;min-width:0;display:flex;overflow-x:auto;
       scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.trail::-webkit-scrollbar{display:none}
.tbn  {height:30px;padding:0 11px;border:none;border-bottom:2px solid transparent;
       background:transparent;color:var(--ink)}
.tbn[aria-selected="true"]{background:var(--card);border-bottom-color:var(--accent)}
```

The rules, each one measured or cited:

1. **30px tall.** 30 x 0.83 = 24.9, so it still clears 24px at the S step.
2. **The unselected label is `--ink`.** It is a control. See the contrast
   section above.
2a. **An ID beside a control is TEXT, not a chip.** The row's identifier lost its fill and
   border on 29 August 2026 — *"remove the box, leave the text only; while hovering the text
   become darker."* One fewer painted surface per row, and it puts the hover answer back in
   line with the eBay rule: an element with no container takes an ink shift, not a fill.
3. **The selected tab wears FOUR marks** — a `--tab-on` fill, the label at FULL ink while
   unselected labels sit at `--ink-soft`, weight 700, and the accent underline. NN/g asks
   for at least two. **Dark needed four:** `--card` against the page measures 1.11:1, a
   whisper, and the studio read it exactly that way — *"the contrast of color in here is not
   enough"*. Navigation says where you are, so it gets its own token and a fill you can
   see: `#E2E2E2` light, `#3A3A3A` dark.
4. **The underline sits on the edge that touches the panel.** The eye joins the
   tab to its content.
5. **The rail scrolls. It never wraps.** A second row makes tabs jump and kills
   spatial memory (NN/g).
6. **A WHEEL OVER THE STRIP PANS IT.** Tried both ways in one evening, and panning won:

   ```js
   strip.addEventListener("wheel", function (e) {
     var d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
     if (!d) return;
     var before = rail.scrollLeft;
     rail.scrollLeft = before + d;                    // 1:1, painted this frame
     if (rail.scrollLeft !== before) e.preventDefault();   // only when it moved
   }, { passive: false });
   ```

   **SELECTING on a wheel cannot be smooth, by construction.** The smallest thing it can do
   is jump a whole item, so every notch is a discrete leap and the strip stutters — the studio:
   *"the scroll here is not so smooth, let just scroll to move the whole bar left and
   right."* Panning maps input to output one-to-one: move the wheel a little, the bar moves
   a little. It is also what the OS does for shift-wheel, so it needs no learning.

   **Never `scroll-behavior:smooth` on an input-driven scroll.** The animation lags behind
   the hand and the result feels heavier, not lighter. Map the delta and paint it this frame.

   **`preventDefault` only when it actually moved.** With every item already fitting there
   is nothing to pan, and swallowing the event there stops the page scrolling under the
   pointer. Put the listener on the STRIP, not the rail, so it works with the pointer over
   the pinned button.
7. **Hide the scrollbar, then put the signal back** — a mask fade at the end, appearing
   only on overflow. A hidden scrollbar with no fade hides the fact that tabs exist.
   **No arrow buttons.** They shipped first and came out the same day, once the wheel and
   the middle-drag were working: a button that repeats what the wheel already does is a
   button too many. The fade is the SIGNAL. The wheel is the CONTROL. Do not draw a
   control that only says what the signal already said.
7. **The strip sits OUTSIDE the scroll region.** Sticky inside it, the strip
   covers a card holding keyboard focus — the W3C's named failure F110.
8. **Arrow keys move and activate. Home is ALL. End is the last.** One roving
   `tabindex="0"`, the rest `-1`. One keydown listener, on the strip only —
   a second one on the rail runs the handler twice and jumps two tabs.

**A SEARCH STEERS THE STRIP.** A filter that narrows to one item must move the strip to
that item's tab, or the strip says ALL while one thing is on screen and the two disagree.
Several matches or none falls back to the ALL tab, which is also what lets a search reach
across hidden panels at all. Clearing the box returns to ALL.

**And the strip's own labels must be searchable.** A tab number and a tab name live on the
strip, not inside the panel, so `textContent` alone cannot find them — a search for the
name of a tab would return nothing. Put the label into the haystack:

```js
hay = (u.dataset.tab + " " + u.dataset.tname + " " + u.textContent).toLowerCase();
```

**Split deciding from drawing.** The first build had the draw function steering the strip,
which called the select function, which called the draw function. One function moves the
strip, one draws, and the caller does both in order.

**The three traps tabs carry. Answer all three or you have hidden the content.**

| Trap | Answer |
|---|---|
| Browser find cannot see a hidden panel | an **ALL** tab, and the page SEARCH jumps to ALL when a term is typed |
| Print drops a hidden panel | a print stylesheet that shows every panel and hides the strip |
| Readers never click a tab they did not notice | ALL is pinned left, outside the rail, so it never scrolls away |

### Other primitives
`.mini` select (8.5px, inline SVG chevron, re-coloured under `html.dark`) · `.tgl` 15px
toggle · `.lst` / `.rw` list rows (9px) · `.elab` 9px section label · `.hint` 9px ·
`.note` transient status (9.5px, `.show` / `.err` / `.okk`, never permanent) · `.prog`
3px progress track · `.ovl` / `.ovlc` / `.ovlh` overlay (392px max, 11px title, 9px dot).

---

## Narrow dock rail

```css
@media (max-width:200px){
  .app{width:64px;margin:0;padding:8px 0 12px;max-width:none}
  .tbar{flex-direction:column;align-items:center;gap:4px}
  .tbd{width:16px;height:1px;margin:2px 0}
  #tip{max-width:88px}
  #detail,#status{display:none!important}
  .foot{flex-direction:column;align-items:center;gap:4px;margin-top:6px;padding:6px 0 0;border-top:none}
  .foot .fbrand,.foot .fby,.foot .chip{display:none}
  .foot .fbtns{margin-left:0;flex-direction:column;gap:4px}
}
```
Docked thin, the panel becomes a vertical icon strip like Premiere's own toolbars. Keep the
narrow `#tip` override **inside** the media block — a stray copy at top level wipes the real
tooltip rule and ships unstyled tooltips.

---

## Copy voice

Uppercase mono for labels and buttons. Terse, factual, lowercase-free in chrome. Tooltips
say what the control does and what it affects, in one line, sentence case allowed. Status
lines describe what happened, not how the code feels. No exclamation marks, no emoji.

---

## UI motion

`transition:.13s` on buttons, `.15s` on pills, `.18s linear` on progress fills. Nothing
else animates. No entrance animation, no easing curves on layout.

---

## Hard don'ts

No second accent · no script or serif logo · no gradients, shadows or heavy borders · no
fully-round corners · no third-party UI kits · no top header · no boxes around the
bottom-bar controls · no permanent status text that shifts the layout · no local override
of a shared component's size · never native `title` · never `transform: scale()` for the scaler · never a remote
webfont link.
