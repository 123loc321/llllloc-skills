---
name: task-design
description: "Design craft and visual judgment on any design task in any program: a deck, slide, layout, poster, key visual, brand system, chart, UI, website, or any judgment about how something looks. Runs when the user types its name or when /llllloc:router picks it for one request. Never on its own. Universal craft only: reads the job's DesignSystem_Name_V1 file first (llllloc:task-design-system writes it once a direction is picked; exploring runs without it), runs the research pass with llllloc:task-research, runs the twelve-point creative direction review, builds the whole job on the system, audits an existing interface, then a self-review, a fat-trim pass and a deslop pass. Never writes the design system itself. The brief, concepts and treatment before any picture belong to llllloc:task-art-direction."
---

# llllloc:task-design (renamed from lord-of-design, 15 Oct 2026)

Craft that holds on every project in every program. A job's numbers live in its project folder. A program's mechanics live in its own skill or lessons folder (RULE 6). Runs only when he types its name or `/llllloc:router` picks it. His art notes open only through `/fundamental`. One exception: `llllloc/6_Fundamental knowledge/visual-library/MASTER-STYLE-PROFILE.md` may be read on any design job.

THE SPINE OF A DESIGN JOB, in order: RULE 6 read, RULE 13 research, RULE 0 direct, RULE 4 three or four rendered directions of the piece and he picks. EXPLORING NEEDS NO DESIGN SYSTEM (22 Oct 2026, his words: it can be skipped while we still explore the direction). Once he picks a direction and before it rolls out, no `DesignSystem_<Name>_V<N>.md` means `llllloc:task-design-system` writes it, then build the whole job on the system, RULE 1 self-review, RULE 12 fat trim, RULE 11 deslop. `llllloc:impeccable` rides along on every step (RULE 14). Rolling a direction out with no design system is the failure this file prevents (30 Sep 2026). Reviewing or improving an existing interface without changing its identity runs `references/design-audit.md` instead of the spine.

## READ ONE FILE PER STEP

| Step | Read |
|---|---|
| A picked direction with no design system yet, a new version of one, or a system rebuilt from a live product | Load `llllloc:task-design-system`. It owns the sheets, the pick and the file (17 Oct 2026) |
| Before any build | `references/craft-library.md` (RULE 7), then impeccable `reference/craft-floor.md` (RULE 14) |
| Before handoff | `references/deslop-and-trim.md` (RULE 11, RULE 12) |
| Review or improve an existing interface | `references/design-audit.md` |

## RULE 0 — THE CREATIVE DIRECTION REVIEW. Before one element moves.

Twelve answers, written down, each checkable against the result.

1. The job. What is it for, in one sentence? Who sees it, where, for how long?
2. The direction. One sentence a crew could act on, anchored to real reference pictures, a named style from RULE 7, or his own work. Never an adjective. "Modern", "clean", "premium" and "bold" are the absence of a direction. Take it from the subject's world: its industry, materials and vernacular. A toy for girls aged 8 to 11 and a dashboard for analysts share nothing.
3. The hierarchy. Primary, secondary, supporting. What the eye hits first, and whether that is correct.
4. The layout system. Grid, margins, spacing rhythm, alignment, one measure every element obeys, the hang line.
5. The type contrast. Three levels named: display, supporting, microcopy. Each with family, weight, size and case. Never stretch a letter.
6. The color roles. Every color gets one role: dominant, support, accent, neutral. One accent per view. A color with no role is cut.
7. The signature. The one element you would recognize out of context. No signature means a template. Spend the boldness there and keep everything around it quiet. On a web page, open with the most typical thing in the subject's world.
8. What it is not. Name the nearest cliché for this category and refuse it before drawing (RULE 11).
9. One era, one voice. Never mix type eras, icon styles, corner radii, shadow logics or illustration styles in one piece.
10. Use what the file already has. Read its styles, variables, components and presets first. A hardcoded value is a bug.
11. The sequence. More than one page means design the run (RULE 3).
12. The budget. What gets cut to pay for what gets added.

A text edit, a recolor or a nudge runs points 1, 3 and 10 only. So does a RECREATION of his own mockup: copy his numbers, skip RULE 4 and RULE 13, and say so in the reply (28 Sep 2026). Anything structural runs all twelve.

Visitor mode (PERSUADE and EXPERIENCE, or OPERATE and READ) decides how far to push. Read it in `references/directions-and-runs.md` before RULE 0 point 2.

## RULE 1 — THE SELF-REVIEW SHIPS WITH THE WORK

Look at the picture. Mark each finding CRITICAL, MODERATE or MINOR.

| Check | The question | The tell that it failed |
|---|---|---|
| HIERARCHY | Does the eye land where 0.3 decided? | It lands on the picture and stays |
| WHITESPACE | Carved, or left over? | A hole with nothing on the other side |
| MEASURE | Every text box inside 60 to 75 characters? | You never counted |
| CONTRAST | Can the smallest text be read at final size? | You had to zoom in |
| CROP | Does the crop keep why the plate was chosen? | A face cut at the chin |
| ALIGNMENT | Does every element sit on the measure? | One element 4px off |
| REPETITION | Has this arrangement appeared already? | Three in a row, a fourth coming |
| DISTINCTIVENESS | Ours with the logo removed? | Could be any brand |
| VO ORDER | Super in VO word order? He reads what he hears. Numbers may shorten (8 Oct 2026) | VO "sales in Asia", super "ASIA SALES" |

THE SQUINT TEST first: at 25 percent, with the words unreadable, can you still name the primary, the secondary and the groups in order? If not, the hierarchy is type size alone.

Contrast has numbers: body text 4.5:1, large text (24px and up) 3:1, a rule, icon or bar 3:1. Check in greyscale. Functional text has an 11px floor. Color alone never carries a level.

Name two specific positives before the fault list. Then output, every time:

```
WHAT I CHANGED: <the substantive moves>
WHAT REMAINS WEAK: <the honest one>
BEST NEXT REVISION: <one specific move>
```

"Nothing remains weak" means you did not look.

## RULE 2 — LOOK AT THE PICTURE, NOT AT THE NUMBERS

Every build ends with a screenshot, a render or an export at final size. Open a reference plate full size before describing it. Position display type by its ink, not its box. Proof the WORST case: the brightest plate, the longest body, the widest ratio, the most items.

## RULE 3 — DESIGN THE RUN, NOT THE PAGE. RULE 4 — THREE OR FOUR DIRECTIONS, RENDERED, THEN HE PICKS

Never accept the first arrangement. Render three or four directions, he picks. Read `references/directions-and-runs.md` in full before any option set and before any run of more than three pages.

## RULE 5 — HOW A TOOL BEHAVES IS A FACT, NOT A GUESS

A picker, a panel, a menu, a setting, an API: open it and look, or read the vendor docs plus one practitioner thread, then write the answer into the program folder (RULE 9). A typographic constant is also a fact: measure it with a hidden probe node. Never repair a guess with another guess. When he says the fix did not work, the cause was wrong. `llllloc:task-research` owns the procedure.

## RULE 6 — WHERE THE KNOWLEDGE LIVES. Read before you build.

This skill holds universal craft only (10 Sep 2026). Project facts live in the project folder on his disk. Program rules live in `llllloc/4_Lessons/Programs/`.

1. THE PROJECT FOLDER, `<project>/*_PROJECT FILES/*_CLAUDE/3_Art Direction/`: the newest `DesignSystem_<Name>_V<N>.md` first (the job's design system, written by `llllloc:task-design-system`; older jobs hold `ART-DIRECTION.md` or `LOOK-LOCK.md` instead until a V1 replaces them), then `DESIGN-SYSTEM.md` (working notes: this job's grid, tokens, archetypes, locked recipes, mistakes), `VISUAL-PREFERENCES.md` (his instructions for this job, one short dated rule each), the newest `HANDOFF_*.md`. Resolve the path: `ls -d "<full path from the map row>"/*/*_CLAUDE`. A job with no folder is normal: say so in one line and work from the message.
2. THE PROGRAM FOLDER, `llllloc/4_Lessons/Programs/<Program>/`: how the software behaves. A program with its own skill keeps its rules there, and the skill wins: `llllloc:tool-figma`, `llllloc:tool-magnific`, `llllloc:task-plugin-builder` (panel look in its `panel-ui/`). A model's behavior lives in `llllloc/4_Lessons/Prompts/<Model>/PROMPT-EXPERIENCE.md`.

Check that a path exists before you follow it. Say plainly when one is gone.

Design system before the roll-out (27 Sep 2026, its own skill 17 Oct 2026, exploring exempt 22 Oct 2026). Every design job gets its design system before the whole thing is built, any medium, any program. Exploring options may run before it. The file, the sheets, the stop for his pick and how a version changes live in `llllloc:task-design-system`. A picked direction with no `DesignSystem_<Name>_V<N>.md`: load it and roll nothing out until V1 exists. A new frame copies parts from the master named in that file. A value the file lacks is added there first, then used.

The order of authority: what he says in this message, then `VISUAL-PREFERENCES.md`, then the newest `DesignSystem_<Name>_V<N>.md`, then `DESIGN-SYSTEM.md`, then the program folder, then this skill. A craft rule here never overrides a number he locked on a job. When they disagree, follow the job and say which rule you set aside.

## RULE 7 — THE CRAFT LIBRARY

Read `references/craft-library.md` in full before any build. It holds the style vocabulary, his case system, and the numbers for spacing, type, color, surface, motion and microcopy.

## RULE 8 — WORKING WITH `llllloc:task-prompt`

When a design needs an AI-generated element, the direction is decided here first. This skill writes the ART DIRECTION LOCK (subject, framing, light, color roles, texture, what is banned) and hands it to `llllloc:task-prompt`. Never the reverse. When the project owns an art direction deck, that deck is the lock.

## RULE 9 — THE FOLDERS LEARN. THIS FILE DOES NOT.

After every request, without asking, write what was learned to the folder that owns it: this job's numbers, recipes and mistakes to its `DESIGN-SYSTEM.md`, his instruction as one short dated rule to its `VISUAL-PREFERENCES.md` and his exact words to its `FEEDBACK-LOG.md`, a program's behavior to `llllloc/4_Lessons/Programs/<Program>/`, a model's behavior to `llllloc/4_Lessons/Prompts/<Model>/PROMPT-EXPERIENCE.md`. One line in the reply. The handoff is `/end`'s job.

This skill changes only when he says so in words, never on its own after a task (10 Sep 2026): "update the skill", "this holds everywhere". Then project RULE 7. Only universal craft belongs here. A lesson that names a file id, a hex, a coordinate or one program's API goes to a folder. A folder fact that is wrong is fixed in place, both dates kept, the old value said out loud.

## RULE 10 — ROUTING

Any other job (`dataviz` for a chart, `llllloc:task-plugin-builder` for a panel, `llllloc:references` for dropped references) loads on his tag or through `/llllloc:router`, never from here. `llllloc:task-research` is the one exception: it runs with this skill on every design turn (RULE 13).

## RULE 11 — THE DESLOP PASS. Runs last, on everything.

Read `references/deslop-and-trim.md` in full before handoff. Ask of each tell found: was this DECIDED or DEFAULT? Report each tell found, decided or default, and what replaced it. A tell that stays after the fix: go back and run the pass again.

## RULE 12 — TRIM THE FAT. Less, but better.

Same file. On every design, only what matters goes on screen (27 Sep 2026). Remove each element in your head: the meaning stays the same, it goes. List what was cut, one line each, so he can ask for any piece back.

## RULE 13 — THE RESEARCH PASS. Every design turn, first or revision.

`llllloc:task-research` runs with this skill on every design turn, after RULE 6 and before RULE 0. It skips only on a recreation, a text edit, a recolor or a nudge with no new reference, look or tool. Read `references/research-pass.md` for the three questions, the cache, the findings block and the filing.

## RULE 14 — IMPECCABLE COMES ALONG (16 Oct 2026)

The router loads `llllloc:impeccable` (Paul Bakaus, Apache 2.0) with this skill on every design job. It is a second pair of eyes, not a second boss.

1. Before any build, read its `reference/craft-floor.md`: the quality floor and the bans. Its anti-patterns join the RULE 11 pass. Missing (`ls <impeccable folder>/reference/craft-floor.md` fails): say "impeccable files missing" in the reply, never go on in silence (24 Oct 2026, only SKILL.md had reached the threads).
2. A named fix reads one command file of its `reference/`: critique, polish, typeset, layout, colorize, bolder, quieter, distill, clarify or animate. Only the one the job needs.
3. Any HTML, CSS or app code, a print poster in HTML too: run `sh <impeccable folder>/scripts/impeccable context --target <file>` once, and `sh <impeccable folder>/scripts/impeccable detect --json <file>` once on the finished pages. Always start it with `sh`: an uploaded skill loses the run permission, so a direct call fails with "Permission denied" (chain test, 16 Oct 2026). Its PRODUCT.md and DESIGN.md come from the brief and the DesignSystem file, never from an interview before work (core rule 14).
4. Anything with no code (Figma, a deck, a poster in a design app, a key visual, a board): its principles and reference files only. Skip its engine, `init`, `live` and `generate`.
5. When it disagrees, his words and locked numbers win, then this skill, then impeccable. Say which rule you set aside.
6. Before handoff, always: `detect` came back clean (point 3, code only) and `references/deslop-and-trim.md` was read and applied (RULE 11, RULE 12). A job without both is not finished (chain test, 16 Oct 2026: one run skipped the deslop pass).

## DELIVERY

A design version is parked visibly, never hidden, and the reply says where to look. Files and sending: `llllloc:task-sending-files` and the core hard stops.

A client storyboard deck (the whole film as slides for him to present) follows `llllloc/7_Templates/client-storyboard-deck/how-to-build-a-client-storyboard-deck.md`, every project. His rule, 27 Sep 2026: the frame's VO words sit centered over the picture, and no frame number or timing tag goes on the slide.

SOURCES and licenses: `references/sources.md`.

## WHERE THE JOB FILES GO (16 Oct 2026, FOLDERS v19)

A creative job's design notes go in `*_CLAUDE/`: the look in `3_Art Direction/` (DesignSystem, DESIGN-SYSTEM.md, VISUAL-PREFERENCES.md), each piece in `6_Design/`: `<Piece>_BUILD.md` (Figma link, frames, grid, versions, what is locked), `PREFLIGHT.md` (the check before export), `Brand/` for identity jobs. A code job: `_CLAUDE/3_Design/`. A folder appears the first time a file goes in.
