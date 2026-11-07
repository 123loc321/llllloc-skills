# Scripting traps

Moved from SKILL.md on 14 Oct 2026, unchanged. Read in full before the first script or tool call that changes the project in a chat.

## SCRIPTING TRAPS
- Reach for a named tool first. `run_jsx_json` for a read or a one-off that no tool covers. `run_jsx` returns no data.
- ExtendScript is ES3: no `let`, `const`, arrow functions, template strings or trailing commas.
- Wrap every change in `app.beginUndoGroup` and `app.endUndoGroup`, so he undoes it in one step.
- Never call anything that opens a modal dialog (alert, confirm, save prompt). Nobody can answer it through the bridge, and After Effects stops taking scripts.
- Adding an effect makes every older effect object on that layer invalid. After each `addProperty` on the Effect Parade, fetch older effects again by name.
- Font by name: `app.fonts.getFontsByFamilyNameAndStyleName(family, style)[0].postScriptName`, set inside `try`.
- Trim paths: `addProperty("ADBE Vector Filter - Trim")`, end is `"ADBE Vector Trim End"`. Name the trim, and expressions read `content("<name>").end`.
- A Gradient Ramp on a shape layer takes raw comp coordinates, never `fromComp()` (tested on pixels, 9 Oct 2026).
- Making a precomp wider by script re-centers that layer's anchor in the parent comp. Set the anchor back right after.
- Many items: use the `batch_*` tools. One call per item is slow and floods the bridge.
- A failed call: read `error` and `line`, then `get_recent_errors`. A call that timed out may still finish in After Effects: list the layers before you repeat it.
