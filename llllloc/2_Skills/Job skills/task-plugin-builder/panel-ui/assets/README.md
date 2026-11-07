# assets

| File | What it is |
|---|---|
| `reference-panel.html` | **SORT V8.0** — the reference build. The source of truth for every shared token, the bottom bar, the icon toolbar and the four global systems. Clone this. |
| `reference-extended.html` | **EASEUP V10.8** — the content-heavy variant: canvas editor, preset library, collapsible sections. Same tokens, more furniture. |
| `llloc-revive.js` | Blank-panel recovery + boot journal. Loads first, owns the flyout menu. Copy into `js/` unchanged. |
| `llloc-prefs.js` | Mirrors localStorage to a real file so settings survive a restart. Loads second. Copy into `js/` unchanged. |
| `fonts/` | Space Mono, six subsets (400/700 × latin / latin-ext / vietnamese). Copy into `fonts/`. Never link a remote font. |

Both reference files are complete, working panels — open them in a browser to see the system
live. They include their own panel logic; keep the shell, replace the content.

Load order in the built panel, before anything else:

```html
<script>window.LLLOC_PANEL = "YOURPANEL";</script>
<script src="js/llloc-revive.js"></script>
<script src="js/llloc-prefs.js"></script>
<script src="js/CSInterface.js"></script>
```
