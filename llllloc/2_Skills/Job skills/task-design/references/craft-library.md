# THE CRAFT LIBRARY

Part of `llllloc:task-design`. "RULE 7" in any rule points here.

## RULE 7 — THE CRAFT LIBRARY

- PHILOSOPHY BEFORE PIXELS. Write the direction in four to six sentences, then express it through form, space, color and composition. About 90 percent visual, 10 percent essential text.
- A THEME IS THREE THINGS: a palette with hexes, a type pairing for display and body, one named identity. Build all three.
- THE STYLE VOCABULARY, name one, never describe: brutalism, neobrutalism, editorial, swiss, riso, dithered, halftone, glassmorphism, neumorphism, claymorphism, skeuomorphic, flat, geometric, bento, terracotta, vintage, retro-arcade, neon, matrix, cosmic, paper, sketch, doodle, fantasy, dramatic, immersive, minimal, mono, spacious, premium, corporate. "Modern" is not a style.
- HIS WORDS AND VALUES SURVIVE THE DESIGN. Never rewrite his sentences to fit a layout. Copy his colors off the node, never from a screenshot. When he says "follow this one", his edit is the spec: read its real numbers into `DESIGN-SYSTEM.md`.
- HIS CASE SYSTEM: UPPERCASE for labels, tags, states and buttons. Sentence case for values, notes and prompt text. The web default (sentence case everywhere) applies only on a real product UI.

THE CRAFT DETAILS, any medium:

- Spacing on one 4 or 8 base (4, 8, 12, 16, 24, 32, 48, 64, 96, 128). No value off the scale. About 12px between neighboring bordered controls. A full-width button stays inside the page margins.
- Optical beats geometric. Nudge an icon until it LOOKS centered. Concentric radius: nested radius equals parent radius minus padding.
- Space before rules. Tight inside a group, generous between groups. More space above a heading than below it. A sideways list shows 16 to 32px of the next item. A scroll area fades its edge where more content waits.
- Line length 60 to 75 characters: `characters = boxWidth / (perChar * fontSize)`. Inter at -4% tracking is 0.431. Probe other faces. Re-run after every resize. A long label in a tight space fades out at its end or clamps to set lines, never a hard cut mid-word.
- Heading leading near 1.1. Body looser, and looser as the measure widens. Display tracking about -0.04em at most.
- The title says the idea, not the section. No lonely words. One alignment inside a column.
- Light type on a dark ground: more leading, more tracking, one step more weight.
- White type over a picture needs a scrim, always: a vertical gradient from about 70 percent black to zero over about 240px. A shadow on the letters is the amateur version.
- Tabular figures in any column of numbers. Icon stroke matches the text beside it, about 2px against semibold, 1.5px against regular. Outline icons, filled for the active one.
- Shadow means elevation and carries an offset and a soft blur. A border means structure. A picture gets a thin neutral outline, never a tinted ring. A modal backdrop is a solid scrim, never a full-screen blur.
- Never grey text on a colored ground: use a darker shade of the hue. The brand color goes to links and actions. Headings stay neutral. Muted text still passes RULE 1 contrast.
- THE SURFACES NOBODY DRAWS on any HTML page: selection color, caret, scrollbar, focus ring, underline offset, numerals in a data column. Theming them is the cheapest signal a page was built.
- QUIET IS HARDER THAN LOUD, in order: saturation to 70 to 85 percent, tinted greys, weights one step down, wider white space, thinner rules, animation travel 10 to 20px. Some anchor must survive.
- MOTION: 100 to 150ms feedback, 150 to 300ms a state change, 300 to 500ms a view transition, 500 to 800ms for ONE authored entrance. Ease out on the way in, `cubic-bezier(0.16, 1, 0.3, 1)`. Enter from about 95 percent, never from zero. Pair every fade with movement (translate, scale or mask). Related items never arrive together: stagger 40 to 80ms in a UI, 80 to 140ms in a hero. Keep shape continuity between states: a thumbnail grows into the hero, a pill opens into a panel. One signature moment per page, never a fade-up on every section or a lift on every card. Exits short, transitions interruptible, an ease-out on toggles and toasts (a spring wobbles). Press feedback: scale near 0.96. A popover or menu grows from the control that opened it and closes with a short fade. Enter and exit match. Only first loads animate: a repeated action such as a tab switch is instant. A changing icon cross-fades with opacity, scale and a little blur. A changing label gets a short blur. A tooltip next to an open one shows faster.
- GENERATIVE WORK: seed everything. Parameters are properties of the system, never presets. Mix a regular force with an irregular one.
- MICROCOPY: a button starts with a verb and names the outcome, `Download the deck`, never `Submit`. An error says what happened, why, and how to fix it, and never apologizes. Name things by what the user understands (`Notifications`, not `Webhook config`). An action keeps its word through the flow: `Publish` gives `Published`. An empty screen offers one next action. Anything that deletes or cannot be undone asks first and names what will be lost.
- THE SYSTEM AUDIT on any file past about thirty elements: count styles, hardcoded values, near-duplicate names and unstyled elements. Bind, merge under the older name, park the rest. Report the four numbers before and after.

