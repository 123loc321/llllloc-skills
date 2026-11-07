---
name: references-code
description: 'Reverse engineers a website or app reference the way a senior front-end engineer would: stack, rendering, design tokens, layout, animation libraries with their durations and easings, interactions, assets and performance, every claim with its evidence, then writes a rebuild spec that can be built from scratch and legally for another client. Loads with llllloc:references (shared rules, dossier) and borrows its evidence method from REA (github.com/morluto/rea). Running REA on an app is llllloc:task-rea. Runs when the user types its name or when /llllloc:router picks it for a dropped website or app link, a bundle, a repo or an Electron app with ''learn from this'', ''how did they do this'', ''rebuild this'', ''make something like this'', or a reference inside a Code job. Builds fresh from what it learns, uses a client''s own code and assets as given, and never hammers a server.'
---

# llllloc:references-code (17 Oct 2026, his words: "for code, it will be somewhat of reference + reverse engineering too, that's what I want when I put a web or app reference in here")

The method is REA's (Reverse Engineer Anything, MIT; running REA itself is `llllloc:task-rea`, 24 Oct 2026): route the target by its kind, read passively first, return findings WITH their evidence and their unknowns, summary first and drill second, then build a new version from what was learned. Shared rules, modes and the dossier: `llllloc:references`.

## TOP RULES

1. Evidence or unknown. Every claim is one of three: OBSERVED (a tool output, a selector, a URL, a timestamp), INFERRED (say from what) or UNKNOWN. Why: a rebuild on a guessed easing or a guessed font is wrong on the first frame. A field with no evidence says `unknown`.
2. Passive first, polite always. Open the page as a visitor, read, measure, one visit per breakpoint, no crawling, no load on their server. A sign-in, a wall or a client's private site: with the access he gives. An app on his Mac is read when he asks.
3. Learn the mechanism, build fresh. Record tokens, timings, easings, breakpoints, layout patterns, library names and versions, then build from scratch, because pasted code from another stack breaks and teaches nothing. A client's own site, code, images, fonts and copy are the material of the job and go in as given. An outside site's assets or code come in when he says so. No legal rule caps a job (his words, 17 Oct 2026).
4. Summary first, drill second. One overview of the whole page, then only the section, component or interaction he asked about. Repeat nothing: a second question reads the saved capture.
5. The output is a REBUILD SPEC, not a report. Every line tells the builder what to make, with its number and its source. A line that only works with the reference's own content is a copy, not a spec.

## ROUTE THE TARGET

| He drops | Read it with | Hand part of it to |
|---|---|---|
| A live website link | MEASURE A to H below, Playwright in the cloud (Chromium is installed) | motion → `llllloc:references-motion` with the frames, look → `llllloc:references-design` |
| A screen recording or video of a site or app | no code to read: `llllloc:references-motion` and `-design` own it; this skill adds only the STACK guess from visible chrome | |
| A bundle, a repo, a zip of source | static read: MEASURE G, folder tree, package.json, no execution | |
| An Electron or desktop app on his Mac | static read with REA, after his "run REA" | `llllloc:task-rea` |
| A Figma file | `llllloc:references-design` owns it; this skill reads only the dev-mode tokens | |

## MEASURE

Run `which node npx python3` first. Each step prints what it found; the raw output goes to `_batches/`. Default tool first, escape hatch second, never a menu.

**A. Stack and rendering.** Globals exist only after the page runs, so detect in a browser, never with curl. One Playwright script: load the page, wait for network idle, then collect `Object.keys(window)` filtered on `React|__NEXT_DATA__|__NUXT__|__sveltekit|astro|gsap|ScrollTrigger|lottie|__THREE__|Lenis|Webflow|Framer|motion`, `<meta name="generator">`, `<html>` attributes (`data-wf-site` is Webflow, `data-framer-hydrate-v2` is Framer), every script URL, the `x-powered-by` and `server` headers, and the `.riv`, `.json`, `.glb`, `.woff2` requests. Fingerprint file for the long tail: enthec/webappanalyzer (the open Wappalyzer data). Escape hatch: `whatweb -a 3 <url>` when installed.

**B. Design tokens.** Default: `npx -y dembrandt <url> --dtcg --save-output` (Playwright rendered; colors, type, spacing, borders, logos, each with a confidence). Escape hatch when it fails: a CDP `DOMSnapshot.captureSnapshot` with `computedStyles` for font-family, font-size, line-height, color, background-color, margin, padding, gap, border-radius, then a histogram of each value to read the type scale, the spacing scale and the color shares. Fonts: `[...document.fonts].map(f => [f.family, f.weight, f.style, f.status])`. Breakpoints: every `@media` width in the collected CSS. Keep the output in DTCG `tokens.json` shape.

**C. Layout.** Full-page screenshots at 390, 768, 1280 and 1920 px wide, plus the bounding box of each top-level section (`getBoundingClientRect`). Read container width, column count, gutter, section rhythm, sticky and pinned elements.

**D. Motion.** In the page: `document.getAnimations().map(a => [a.effect.target, a.effect.getTiming(), a.effect.getKeyframes()])` for CSS and Web Animations; `gsap.globalTimeline.getChildren(true, true, false)` and `ScrollTrigger.getAll().map(t => [t.trigger, t.start, t.end])` when GSAP is present; `gsap.globalTimeline.timeScale(0.25)` to watch slowly. Finished transitions: `getComputedStyle(el).transitionDuration` and `transitionTimingFunction`. Animations driven by requestAnimationFrame, springs and Lottie do not show there: record them with Playwright `page.screencast()` (1.59 or newer) or `recordVideo`, and hand the frames to `llllloc:references-motion`.

**E. Interactions.** Hover, focus, scroll and click states captured as screenshots and computed styles before and after. Listener sources with CDP `DOMDebugger.getEventListeners` on the element he asked about. Routing: client side or full page, and what the URL does.

**F. Assets and performance.** `page.on('response')`: list every image, font, video and model with type, size and lazy-loading; download into the job when he asks. `npx -y lighthouse <url> --output=json --only-categories=performance,accessibility` for LCP, CLS, font display and non-composited animations.

**G. Bundles and source.** Look for `//# sourceMappingURL=` or `<bundle>.map`; with a map, `npx -y source-map-explorer bundle.js bundle.js.map --json` shows the real module tree. Without one: `npx -y webcrack bundle.js -o out/` then `npx -y wakaru out/*.js --unpack -o modules/`. Read for structure, library versions and the mechanism of one effect. Paste from it when he asks; otherwise rebuild.

**H. The one effect he asked about.** Isolate it: the element, its classes and styles, the script that moves it, its timing numbers, what triggers it, what it depends on. This is the paragraph the rebuild needs most.

## THE PRO READ

| Field | What to write, with its evidence |
|---|---|
| STACK | Framework, meta framework, hosting hints, CMS or builder, versions where a bundle names them. |
| RENDERING | Server rendered, static, client app; hydration; what loads first; route style. |
| TOKENS | Palette with shares and roles, type families with weights and the size scale, spacing scale, radii, shadows, breakpoints. DTCG shape. |
| LAYOUT | Container width, grid, gutters, section order and rhythm, sticky and pinned parts, how the hero is built. |
| MOTION | Library and version, each key move: trigger, property, duration, easing, delay, stagger, scroll binding. Frames per second observed. |
| INTERACTIONS | States, feedback, cursor, page transitions, forms, what the URL does. |
| ASSETS | Formats, sizes, lazy loading, video codecs and loops, 3D or Lottie or Rive files. |
| PERFORMANCE | LCP, CLS, font loading strategy, what is composited. |
| ACCESSIBILITY | Landmarks, focus order, contrast on the main text, reduced-motion handling. |
| WHAT MAKES IT PREMIUM | The three to five mechanisms, named, each with the number that proves it. |

## THE REBUILD SPEC

Written to the job that will use it: a Code job's `_CLAUDE/2_References/REFERENCE_<site>.md` (tokens also to `3_Design/`), or a creative job's `*_CLAUDE/2_References/`. The craft lines that transfer across jobs go to the `CODE.md` dossier in the `llllloc:references` data home.

```markdown
# REFERENCE <site> — rebuild spec        <date> · built by llllloc:references-code
## EVIDENCE LEDGER     | claim | O / I / U | source (tool, selector, URL, timestamp) |
## STACK               what they run, what we will run instead and why
## TOKENS              the DTCG block, renamed for the new client's brand
## LAYOUT              per breakpoint: container, grid, sections, sticky
## MOTION SPEC         per element: trigger, property, from, to, duration, easing, delay, stagger
## INTERACTIONS        state by state
## BUILD PLAN          what gets built from scratch, which libraries, what changes for this client
## DO NOT COPY         what is signature to them and would read as their site, anything that failed in use; empty when he wants a close rebuild
## UNKNOWNS            what no tool could read, and what would read it
```

Check before delivery: every ledger row has a source or says U, the motion spec has a number in every cell or `unknown`, the build plan names what differs for the new client. One fails: go back to that MEASURE step.

## RESEARCH (with `llllloc:task-research`, 3 to 6 searches)

The studio or agency behind the site (site credits, Awwwards, Godly, Siteinspire write-ups), the libraries' current versions and docs, what practitioners call the pattern (for example "scroll pinned storytelling", "view transitions", "magnetic cursor"), the maker's own breakdown or talk, and what breaks when people copy it (performance, accessibility, reduced motion).

## REA

Running REA (commands, his "run REA", Ghidra and Java, where it runs) moved to `llllloc:task-rea` on 24 Oct 2026. Keep REA's rules even without REA: observations, inferences and unknowns in separate sentences; never claim a runtime observation from a static read; preserve limitations.
