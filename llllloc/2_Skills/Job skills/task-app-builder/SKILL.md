---
name: task-app-builder
description: "Builds websites and apps in code so they run smooth, fast and at award level: landing pages, campaign microsites, portfolios, brand sites, app screens, dashboards, tools. Also fixes the code of an existing site or app. Runs when the user types its name or when /llllloc:router picks it for one request. Never on its own. Design is not decided here: llllloc:task-design-system writes the DesignSystem_Name_V1 file and llllloc:task-design sets the direction and the visitor mode first, and this skill builds on them. Holds the build rules for SHOWPIECE and PRODUCT pages, accessibility, motion performance, page speed and metadata, then passes the 100-point APP GATE at 88 or more."
license: "Merged work. Sources: MIT (awwwards-ui-skill, ui-skills), Apache 2.0 (frontend-design, now in llllloc:task-design). See licenses/."
---

# llllloc:task-app-builder

Turns a design system into a website or app that runs smooth and fast, and fixes the code of existing ones. Runs only when the user types its name or `/llllloc:router` picks it. Every design choice lives in `llllloc:task-design`. This skill never picks a color, a font or a layout.

## STEP 0 — THE DESIGN SYSTEM COMES FIRST

Read the newest `DesignSystem_<Name>_V<N>.md` in the job's `_CLAUDE/3_Design/` (a creative job: `*_CLAUDE/3_Art Direction/`) (older jobs: `ART-DIRECTION.md`, `ART-DIRECTION-LOCK.md` or `ANIMATION/LOOK-LOCK.md`). None: stop, and run `llllloc:task-design-system` before any code (17 Oct 2026). Every value in the build comes from that file. A value it lacks goes into the file first. A plugin panel for a desktop app is out of scope: `llllloc:task-plugin-builder` builds it with its own `panel-ui/` system.

## STEP 1 — PICK THE JOB

| The ask | Job | Read |
|---|---|---|
| Build a new page, site, app screen or component | BUILD | STEP 2 to STEP 5 |
| Check a file for accessibility, janky motion or metadata | FIX | `accessibility.md`, `motion-performance.md` or `metadata.md` |

FIX output, per problem: quote the exact line, say why it matters in one sentence, give a concrete fix. Keep fixes small. Never refactor unrelated code. A design audit, or a design system rebuilt from an existing product, belongs to `llllloc:task-design` (its `references/`).

## STEP 2 — PICK THE BUILD FROM THE VISITOR MODE

`llllloc:task-design` RULE 0 sets the visitor mode. This skill follows it.

| Visitor mode | Build | Read |
|---|---|---|
| PERSUADE or EXPERIENCE | SHOWPIECE: smooth scroll, depth, springs, optional cursor and WebGL | `references/showpiece.md` |
| OPERATE or READ | PRODUCT: no decorative motion, feedback 200ms or less, accessible primitives | `references/product.md` |

A site with marketing pages and an app uses both, page by page. Unsure: build the calmer one and say so.

## STEP 3 — BUILD RULES FOR BOTH

- Stack: follow the project's stack. A new standalone page is one HTML file with its CSS and JS inside. Load libraries only from the hosts the delivery allows.
- Semantics: `<button>` for actions, `<a>` for navigation. A name on every control. Decorative layers `aria-hidden="true"`. Full floor: `references/accessibility.md`.
- States: every interactive item has hover, `:focus-visible`, active and disabled. Every data view has loading (a skeleton shaped like the content), empty and error.
- Layout safety: `100dvh`, never `100vh` (it follows the real visible screen on phones). Fixed items respect `env(safe-area-inset-*)`. Wide content scrolls inside its own box. No text overflows a button or card.
- Type in code: headings `text-wrap: balance`, body `text-wrap: pretty`, data `font-variant-numeric: tabular-nums`.
- CSS: one `z-index` scale. Watch selector specificity: a type selector and a class selector must not cancel each other's spacing.
- MOTION: animate only `transform` and `opacity`. Respect `prefers-reduced-motion`. Pause loops off screen. Scroll and pointer handlers only write values that one `requestAnimationFrame` loop reads. Full rules: `references/motion-performance.md`.
- Speed: targets are the Core Web Vitals "good" marks, Google's page-speed scores. LCP (main content shows) 2.5s or less. INP (reaction to a tap) 200ms or less. CLS (layout jump) 0.1 or less.
  - Images: modern formats (AVIF or WebP), `width` and `height` set so nothing jumps, `srcset` for screen sizes, `loading="lazy"` below the first screen.
  - Fonts: few files, `font-display: swap`, preload the display face.
  - Heavy code (WebGL, GSAP, video) loads after the first screen shows.
- Public page: run `references/metadata.md` before it ships.
- Look at it: if a browser or screenshot tool exists, render at 375, 768 and 1440 wide. Test with keyboard only. Test with reduced motion on.

## STEP 4 — THE APP GATE

Score out of 100. Ship at 88 or more. Below 88: fix, then score again. If 88 is not honestly possible, name the shortfall. The design itself is checked by `llllloc:task-design` RULE 1 and RULE 11, not here.

| ID | Points | Pass evidence |
|---|---:|---|
| SYSTEM-01 | 12 | Every color, size, space and radius comes from the DesignSystem file. No stray hardcoded value. |
| MOTION-01 | 12 | Matches the mode. SHOWPIECE: the signature moment eased and staggered, two depth techniques, no layout shift. PRODUCT: no decorative motion, feedback 200ms or less. |
| PERF-01 | 16 | Speed targets met or measured. Compositor-only animation, one frame loop, heavy code deferred, WebGL disposed. |
| A11Y-01 | 16 | Semantic HTML, names, keyboard reach, visible focus, AA contrast, `aria-hidden` decoration, reduced-motion fallback. |
| RESP-01 | 12 | Holds at 375, 768 and 1440. `dvh` and safe areas used. No overflow. |
| STATE-01 | 12 | Hover, focus, active, disabled, loading, empty and error all exist. |
| CODE-01 | 10 | No console errors, no dead handlers, no specificity clashes, no sideways page scroll. |
| SHIP-01 | 10 | Title, description, social card, favicon. Metadata rules pass. |

## STEP 5 — REPORT

Short, in the user's language. Lead with the result.

```
BUILD: SHOWPIECE | PRODUCT
DESIGN SYSTEM: <file name read>
APP GATE: NN/100
<one line of evidence per gate row>
TRADE-OFFS: <any deliberate cut, for example no WebGL on a corporate page>
```

Show a draft before anything is published or sent. Never publish, send or delete without asking.

Sources and licenses: `licenses/CREDITS.md`. Read it only when he asks where a rule came from.

## WHERE THE JOB FILES GO (16 Oct 2026, FOLDERS v19)

In the job's `_CLAUDE/`: every build in `4_Builds/` (`CHANGELOG.md` newest first, `RELEASE-CHECKLIST.md`, `SIGNING.md` names only), older builds in `4_Builds/Old/`, never in `_DELETE`. Tests in `5_Tests/` (`SMOKE-TEST.md`, `BUGS.md`, test scripts). Pictures in `6_Shots/` (before and after, `Golden/` changed only on his word). Feature status in `1_Spec/FEATURES.json`. The full tree: `llllloc:project-code`.
