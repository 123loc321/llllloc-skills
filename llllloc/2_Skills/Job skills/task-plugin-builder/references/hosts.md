# HOSTS — which plugin system each software uses

## Contents
- Adobe apps — CEP (the well-trodden path)
- OBS Studio — Lua / Python scripts, or C plugins
- DaVinci Resolve — Lua / Python (DaVinciResolveScript) or Fusion plugins
- Figma — plugin (HTML UI + sandbox JS)
- VS Code — extension (webview UI + extension host JS)
- Blender — Python add-on
- When the target isn't a normal file-copy install


Map the user's target software to the right plugin system before writing any code. If the
user hasn't named the software, ask once — it determines the architecture, the language, and
the install path.

---

## Adobe apps — CEP (the well-trodden path)

**Premiere Pro, After Effects, Photoshop, Illustrator, InDesign, Audition, Animate.**
CEP (Common Extensibility Platform) runs an HTML/JS panel with an ExtendScript backend. This
is the most reliable Adobe option and what the bundled `assets/cep-template/` provides.

```
PLUGIN/
  CSXS/manifest.xml     registers the panel; set <Host Name="…"> per app + version range
  .debug                DevTools debug port
  index.html            the UI (llloc-UI by default)
  js/CSInterface.js     Adobe's bridge library
  jsx/hostscript.jsx    ExtendScript backend that calls the app's API
```

- **Host codes** for the manifest `<Host Name="…">`: Premiere `PPRO`, After Effects `AEFT`,
  Photoshop `PHXS`, Illustrator `ILST`, InDesign `IDSN`, Audition `AUDT`, Animate `FLPR`.
- **Backend is ExtendScript = ES3.** No `const`/`let`/arrow/template-literals/`forEach`/
  `map`/destructuring/default-params/spread. Use `var`, classic `for`, `function`, string
  concat. Syntax-check: `.jsx` → copy to `.js` → `node --check`.
- **Panel JS runs in Chromium** — modern JS is fine, but honour the llloc-UI platform rules in `panel-ui/references/platform-notes.md`
  (mouse events not pointer events; `transform:scale()` not `zoom`).
- **`localStorage` persists** — use it for presets/settings so reinstalls don't wipe them.
- **File dialogs:** `window.cep.fs.showOpenDialogEx/showSaveDialogEx/readFile/writeFile` in
  CEP; hidden `<input type=file>` + Blob download as a browser fallback.
- **Install:** enable unsigned panels (CSXS 9–12) then copy to the extensions folder — see
  `installers.md`.

### Adobe UXP (newer; Photoshop + InDesign, growing)
UXP is Adobe's newer system (React-like UI, JS backend, a `.ccx`/UXP plugin package). Prefer
CEP unless the user specifically needs UXP or targets a Photoshop version where CEP is
deprecated. UXP UI uses its own component set — llloc-UI tokens can be approximated with UXP
styling, but confirm with the user before committing. UXP plugins can install via the
Creative Cloud Desktop app or UPIA; the one-double-click story is weaker, so set expectations.

### Common Adobe API limits (be honest)
- **Premiere:** can read/write keyframe values, times, interpolation; read the playhead;
  listen for selection changes. **Cannot** read which keyframes are highlighted in Effect
  Controls, bend keyframe bezier handles (After Effects only), read the audio waveform, or
  read the Program Monitor image.
- **After Effects:** far richer keyframe/expression access than Premiere.
- **Photoshop:** strong document/layer/action access via ExtendScript or UXP.

---

## OBS Studio — Lua / Python scripts, or C plugins

- **Scripts** (Lua or Python) are the one-double-click-friendly path: a single script file
  dropped into OBS's scripts folder, loaded via Tools → Scripts. UI is OBS's own properties
  API (not HTML) — llloc-UI doesn't apply; use OBS property widgets.
- **Native C plugins** are heavier (compiled per platform) — only if the user needs
  performance or sources/filters that scripting can't reach.
- Install path (scripts): copy the `.lua`/`.py` into the user's OBS scripts folder; the
  installer can do this, though the user still adds it via Tools → Scripts once.

## DaVinci Resolve — Lua / Python (DaVinciResolveScript) or Fusion plugins

- Scripting via the Resolve scripting API (Lua/Python) for automation; Fusion has its own
  fuses/macros. UI options are limited; llloc-UI generally doesn't apply.

## Figma — plugin (HTML UI + sandbox JS)

- HTML/JS UI in an iframe + a sandboxed `code.js` that calls the Figma plugin API. **This is
  a great llloc-UI fit** — the UI is a normal webview. Packaged via a `manifest.json`;
  distribution is through the Figma Community or a private link, not a file installer, so the
  "one-double-click" rule becomes "one-click install from Community."

## VS Code — extension (webview UI + extension host JS)

- Webview panels are HTML/JS (**llloc-UI fits**); the extension host is Node. Packaged as a
  `.vsix` (one-click install in VS Code) — the double-click installer becomes "install this
  .vsix."

## Blender — Python add-on

- A `.py` (or zipped package) using `bpy`; UI is Blender's own panel API, not HTML, so
  llloc-UI doesn't apply. Install: Blender → Preferences → Add-ons → Install, or drop into
  the addons folder (the installer can place the file).

---

## When the target isn't a normal file-copy install

Some hosts (Figma, VS Code, UXP, Blender) have their own install mechanism where a raw file
copy isn't the norm. In those cases:
- Still produce the **package the host expects** (`.vsix`, Figma manifest folder, UXP
  package, Blender add-on zip).
- Provide the closest one-click experience that host allows, and say plainly in the README
  how the user installs it. Don't fake a double-click installer that the host would reject.

For everything that IS a file-copy install (all CEP apps, OBS scripts, Blender add-on files),
use the one-double-click installer in `installers.md`.
