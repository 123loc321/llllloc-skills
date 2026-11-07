# llloc-UI — the house editorial-monospace design system

One fixed system for every interface that lives inside a host app or a browser window: Adobe panels, web tools, dashboards, forms, calculators, prototypes. Technical, editorial, Swiss. Near-black monospace type, one vermilion accent used sparingly, no decorative chrome, no strokes. A new project is the same shell, tokens, theme, scaler, tooltip engine and hardening modules, with only the working content swapped. Part of `llllloc:task-plugin-builder` since 30 Sep 2026 (it was the `llloc-ui` skill). `llllloc:task-plugin-builder` reads it before any panel UI. Every path below is relative to this `panel-ui/` folder.

## RULE ZERO

Open `assets/reference-panel.html` (FIND V1.20) BEFORE the first line of CSS, and end the reply with a `Cloned:` line naming what you copied out of it: `Cloned: FIND's .lmenu -> the preset picker`, or `Cloned: nothing — this build changed no UI`. A missing line means the rule was skipped.

A new row, a new dialog, a new menu, a new control is a NEW LOOK. The test is "is there any element here that this panel does not already have?" When a panel and FIND disagree, FIND is right.

## RULE ZERO-B — WHAT THIS SYSTEM GOVERNS

FIND is a PANEL. A standalone desktop app that sits beside the host is not in this system: it wears the platform's own clothes (system font, controls, window chrome, spacing) and keeps only the vermilion. When he names a real product for the look, by a link or a screenshot, that product is the lock and this system steps aside. Never blend the two. Say it on the `Cloned:` line: `Cloned: Atlas — the grey sidebar and the justified grid. Not FIND: this is an app, not a panel.` A panel and its companion app share the accent and nothing else.

## DOCUMENTING A PANEL

Any guide, deck or README about a panel carries a picture of that panel, captured from the shipped build, before the first paragraph about it. Never a mockup. Boot the panel headless against a stub host, park the mouse on one control at a time, and let the panel open its own tooltip, so every word in the picture ships. `_GUIDE/capture.js` in his PR Plugin folder is the harness. A button list under a picture is deleted: the picture carries it.

## READ-FIRST MAP

| When | Open |
|---|---|
| Before anything, every time | `references/LOCKED-RULES.md`: the 21-point gate, the reload glyph, the pixel-kind trap, the specificity trap |
| Before the first line of CSS, every time | `assets/reference-panel.html`, FIND V1.20. Search it for the element you are about to build |
| Before writing any code | `references/design-system.md`: tokens, the size ladder, every component with its numbers |
| A content-heavy build: canvas editor, preset library, folds | `assets/reference-extended.html`, EASEUP |
| Many sibling items, one on screen: a prompt, a shot, a preset per view | `assets/tab-strip.html`: the engine, the overflow fade, the three traps |
| Any Adobe CEP panel, Electron or webview | `references/platform-notes.md`: the blank-panel fix, fonts, storage, packaging gates |

Drop-in files that travel with every build: `assets/llloc-revive.js`, `assets/llloc-prefs.js`, `assets/fonts/` (six woff2 plus the license).

## WHAT HE SET, IN HIS OWN WORDS

- Flat. White page, pale grey blocks, one vermilion block, lots of air. An editorial dashboard, not a control surface.
- "no box in the design system should have stroke" (15 Aug 2026). Separation comes from tone. A stroke survives in three places only, because FIND keeps it there: the rule above the bottom bar, a text field, and a control switched ON.
- Small corners, 1.5px. One right edge: toolbars, blocks and the rule above the bar end at the same x.
- Air around anything you press: about 8px before the end of a row highlight, about 6px before a scroll bar.
- Weight 400 to 500, wide letter-spacing, small type. He has asked for smaller twice, never bigger.
- One word, not a sentence: `SEARCH`. No standing instructional text ("remove all these texts"). What a key does lives in its hover tip.
- No message announcing success. The panel speaks only when something fails.
- The bottom bar sits on the panel floor at every size. A list scrolls inside its own box. The page never scrolls.
- The palette is five colors, from his ARRIVAL FLEET sheet (29 Aug 2026): CANVAS `#FFFFFF`, SURFACE `#F2F2F2`, INK `#171717`, LIVE `#F44E16`, TERTIARY `#909090`, held as primitive tokens with semantic roles. Two of the five cannot carry small text and have a measured text step each (`design-system.md`).
- Full dark mode with the same accent. Contrast is measured in BOTH themes. Light failed on seven elements once.
- Many sibling items go in a tab strip, one on screen, each tab collapsible (29 Aug 2026). His 28 Aug rule against packing a deliverable with folds is about hiding every FIELD, not about navigation.
- No native browser widgets showing through: build menus from panel elements, turn off the number spinner. Nothing in the chrome exceeds 11px. Nothing ragged, nothing flush against a scroll bar, no big radius.

## WHAT IS FIXED (clone from FIND, never redesign)

- Tokens: near-black ink, one vermilion accent `#F0481E`, IBM Plex Mono, 1.5px radius. Never a second accent. The dark ramp is byte-identical in every panel.
- Bottom bar, no header: `.hd{display:none}`. `NAME.` wordmark (700, 8.5px), version, `made by llllllloc`, then size / tips / theme pushed right, bare.
- Flat card: `.card` transparent, borderless, `flex:1`. Icon toolbar: `.tbar` of 24x24 `.tb` buttons with `.tbd` dividers.
- Complete dark mode, persisted, filled sun/moon toggle. Every button sets an explicit `color`. Theme differences ride in `--edge` / `--edge-2` tokens, never in `html.dark .thing` rules.
- Styled hover tooltips, every control carries `data-tip`. Never native `title`.
- Narrow-dock rail at `max-width:200px`. The two hardening modules, loaded first.

## THE SCALER — CSS zoom

```css
html,body{height:100%}
#zoomRoot{display:flex;flex-direction:column;zoom:var(--uis,1);height:100%}
```

`applySize` does only `document.documentElement.style.setProperty("--uis", String(s))`, at 1.16 / 0.98 / 0.83 for L / M / S. `transform: scale()` scales the paint, not the layout, and left every panel scrolling 155px at S. The check at each size: `document.documentElement.scrollHeight - window.innerHeight` must be 0. Under zoom, `getComputedStyle` reports layout pixels and `getBoundingClientRect()` reports visual pixels. Never compare one to the other or assert a computed pixel against a literal. `check-build.js` still warns on zoom. That warning is stale.

## THE SIZE LADDER

Control heights: 24px toolbar button, 19px chip, 15px toggle, 14px tiny button, 12px badge, 10px spinner arrow. Type: 11px pill, 10.5px field input, 9.5px value or status, 9px label, 8.5px bar and tooltip, 7 to 8px micro-caption. Never override a shared component's size in a local rule.

## BUILD RECIPE

1. Open `assets/reference-panel.html` and read `references/design-system.md`.
2. Start from that file. Keep the tokens, `#zoomRoot`, the flat card, the toolbar, theme, scaler, tooltip engine, bottom bar and rail as they are.
3. Copy in `assets/fonts/`, `llloc-revive.js`, `llloc-prefs.js`. Load order: panel name, revive, prefs, CSInterface, panel.
4. Rename the wordmark and the storage prefix.
5. Replace the card body with the controls the job needs. Every control gets a `data-tip`. Anything secondary goes into `.ovl`.
6. No permanent hint text. No success message.
7. Non-browser target: read `references/platform-notes.md` and honor every rule.
8. Verify: no scroll at L, M or S. The gates in platform notes. Check the built archive, not the working folder.

## HARD DON'TS

No accent under small text and no small text in the accent (use `--accent-txt`). No `--ink-soft` on a control's own label. No hit box under 24px at S. No block of text past 80 characters. No tab strip without an ALL tab, a print rule and a search across tabs. No second accent. No strokes on boxes or buttons. No script or serif logo. No gradients, shadows or heavy borders. No fully round corners. No third-party UI kits. No top header. No boxes around the bottom-bar controls. No permanent status or hint text. Never native `title`. Never `transform: scale()`. Never a remote webfont link. One look, one family.

The reference builds, both modules and the fonts travel with every copy of this skill.