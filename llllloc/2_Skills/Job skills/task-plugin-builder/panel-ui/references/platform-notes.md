# PLATFORM NOTES — where the UI runs

## Contents
- Universal (applies even in a plain browser)
- The blank-panel problem (CEP) — read this before shipping any panel
- Settings that survive a restart (CEP)
- ExtendScript (the .jsx backend) — strict ES3
- Electron / standalone webview
- Packaging gates — run these before shipping


A browser tab forgives a lot. Adobe CEP does not. Everything here was learned by shipping
a broken build first — treat it as settled, not as suggestions.

---

## Universal (applies even in a plain browser)

- **Never CSS `zoom`.** Use `transform: scale()` on `#zoomRoot`. `zoom` breaks hit-testing:
  clicks land in the wrong place.
- **`getBoundingClientRect()` for all canvas hit-testing.** Anything based on `offsetX`,
  `clientX` minus a hardcoded offset, or element position breaks the moment the UI is scaled.
- **Mouse events, not pointer events, for drag handles.** Pointer events lose capture in
  embedded webviews mid-drag.
- **Fixed-position elements live outside the scaled root.** A `transform` creates a
  containing block, so a `position:fixed` child positions against the scaled box, not the
  viewport. The tooltip is outside `#zoomRoot` and is sized by hand in `applySize()`.
- **Call `syncZoomHeight()` after any DOM change that alters height.**
- **Every button sets an explicit `color`.** Inherited colour goes black-on-black in dark mode.

---

## The blank-panel problem (CEP) — read this before shipping any panel

When Premiere restarts it restores docked panels, and they can come back **completely
blank**. Closing the panel and reopening it from Window → Extensions fixes it. Three
distinct causes were found; a shipped panel defends against all three.

### 1. A remote webfont blocks the first paint
A `<link rel="stylesheet">` to Google Fonts is render-blocking. When Premiere restarts with
the network asleep the request **hangs** rather than failing fast, and the panel paints
nothing until it times out. It is timing-dependent, so it only bites on some restarts.

**Fix — bundle the font.** Copy `assets/fonts/` into the panel and declare six `@font-face`
subsets (400/700 × latin / latin-ext / vietnamese) with `font-display:swap`. No network at
boot, and the panel works offline — which a sold plugin has to. **Never link a remote font.**

### 2. The browser surface stops compositing
The page loads and lays out correctly — scripts run, elements measure fine — but CEP's
surface never paints. A reload does **not** help: it reuses the same dead surface. Only a
genuinely new surface fixes it, which is why reopening works.

**Detector:** `requestAnimationFrame` only fires while the compositor runs. Visible page +
no frame = dead surface. No pixel reading needed.

**Fix — `assets/llloc-revive.js`**, loaded before everything else. It escalates, cheapest
first, re-testing after each step: repaint kick (reflow + layer change) → `resizeContent()`
→ **`requestOpenExtension()` on itself** (the programmatic Window → Extensions, and the one
step known to work) → reload, last and only once. Since v3, reopen and reload are **gated
to the first 15 seconds after load** or a manual *Fix blank panel* — past that, a panel
that is not painting is treated as off-screen, not dead, so an occluded panel can never
resurrect itself on refocus. It also owns the panel's flyout menu, so
**Reload panel / Fix blank panel / Startup report** exist even when the panel script never
ran — which doubles as the fastest diagnostic you have.

### 3. Startup contention
Several panels restoring at once, each binding a debug port and spawning a CEF process.

**Fixes, in the manifest:**
- `<StartOn><Event>com.adobe.csxs.events.ApplicationActivate</Event></StartOn>` — **for
  panels that live docked only.** It loads the panel once Premiere is up rather than during
  the startup crush, and on a docked panel that is pure protection. On a panel the user
  opens ad hoc and **closes when done, it is a resurrection spell**: close the panel, click
  back into Premiere, and the activation event loads it straight back — and even where the
  host loads it headless, `llloc-revive` is inside its 15-second boot window, where
  reopening is deliberately allowed, so the panel pops open anyway. Measured on GRID,
  4 Aug 2026: closed GRID reopened on every app switch until this line was removed; the
  docked panels never showed it because they are never closed. **Decide per panel:** docked
  resident → keep StartOn. Close-when-done → ship without it.
- `--disable-application-cache` so a stale empty page cannot be restored.
- **Drop `--enable-nodejs` unless the panel truly needs it.** Node injection is a known
  blank-panel cause and pure startup weight otherwise. `window.cep.fs` (open/save dialogs,
  read/write file) works **without** Node — only real filesystem work needs it.
- **A unique `Port` in every `.debug` file.** Two panels sharing 8092 shipped once.

### Manifest edits are invisible until the CSXS cache is cleared
Premiere does not read `manifest.xml` at launch — it launches every extension from a cached
manifest copy in `~/Library/Caches/CSXS/cep_cache` (Windows:
`%LOCALAPPDATA%\Temp\cep_cache`). Any manifest change — StartOn, Size, CEF flags,
anything — **does not exist** until that folder is deleted **with Premiere closed** and
Premiere relaunched. This silently nullified at least one manifest fix during the DOCK/GRID
sessions and muddied a whole investigation: the file was right, the cache still said
otherwise. Pair every manifest edit with the cache clear, and put both in any repair script
that touches a manifest.

### Diagnosing it in the field
The journal in `llloc-revive.js` writes timestamped marks (`script`, `dom`, `load`, `frame`)
to storage each session. After a blank restart the user reopens the panel by hand and picks
**Startup report** from the ☰ menu. Two possible verdicts, pointing opposite ways:
- *ran but never painted a frame* → surface problem, the escalation applies.
- *no session on record* → the page never executed; **no in-page fix can ever work**. Look
  at the CEP cache, extension registration and how many panels are installed.

Fastest zero-install check: on a blank panel open ☰. If the llloc items are there, the page
ran. If only Premiere's defaults are there, it did not.

---

## Settings that survive a restart (CEP)

`localStorage` in CEP lives inside the CEF cache, and Premiere may clear it between
sessions — a user who picks small + light finds themselves back on large + dark.

**Fix — `assets/llloc-prefs.js`**, loaded before any panel code reads its settings. It
mirrors `localStorage` to a real file:

```
macOS    ~/Library/Application Support/CSXS/llllllloc/<panel>.json
Windows  %APPDATA%\CSXS\llllllloc\<panel>.json
```

On load it restores anything the cache lost; then a 1s poll, plus blur / hidden /
beforeunload, keeps the file in step. **No call sites change** — every existing
`localStorage` call gets persistence for free, so presets, libraries and calibration maps
are covered too, and settings survive a reinstall.

**Load order is not optional:** panel name → `llloc-revive.js` → `llloc-prefs.js` →
`CSInterface.js` → panel script. Panels read their settings while parsing, so the restore
has to have already happened.

---

## ExtendScript (the .jsx backend) — strict ES3

No `const`, `let`, arrow functions, template literals, `forEach`, `map`, `indexOf` on
arrays, or `JSON`. Build JSON strings by hand. Namespace the whole backend
(`var PANEL = (function(){ ... })()`) — panels share one script engine and will collide.

**Selection:** use `app.project.activeSequence.getSelection()` **only**. An `isSelected()`
scan across tracks over-reports on some builds and will read and write clips the user never
selected. Do not "use whichever returns more" for reads.

**Premiere blend modes are numbered ALPHABETICALLY** internally (0 = Color … 19 = Normal …
26 = Vivid Light), not in dropdown order. Effect Controls also does not reliably repaint
when a script changes a value, so a "read the name back" calibration cannot work on modern
builds.

---

## Electron / standalone webview

Same scaling and hit-testing rules. Storage is usually reliable, but `llloc-prefs.js` costs
nothing and makes settings portable. Bundle the font regardless.

---

## Packaging gates — run these before shipping

Check the **built archive**, not the working folder. A version-bump line once truncated
every manifest to zero bytes and the check passed because it read the source tree.

1. Manifest exists, is **> 800 bytes**, parses as XML, and contains `ExtensionBundleId`,
   `ExtensionBundleVersion`, `MainPath`, `Host Name="PPRO"`,
   `--disable-application-cache`, `Type>Panel` — and `StartOn` **present on
   docked-resident panels, absent on close-when-done panels** (see §3; wrong either way is
   a shipped bug).
2. Every `$("id")` / `getElementById("id")` in the panel script resolves to real markup.
3. Script load order correct; the two modules byte-identical to the copies in `panel-ui/assets/`.
4. Six `.woff2` files present, each starting with the `wOF2` magic bytes.
5. No `fonts.googleapis` / `fonts.gstatic` anywhere.
6. `#tip{position:fixed` present exactly once at top level.
7. No native `title=`, no CSS `zoom`.
8. Backend `.jsx` free of ES6 (`=>`, `const`, `let`, backticks, `forEach`).
9. Both installers present; `.debug` port unique across the suite.
10. Shared tokens byte-identical to `assets/reference-panel.html`.

**When editing existing files, always read fully, then write.**
`open(p,'w').write(open(p).read()...)` truncates the file before the read runs.
