# BUILD CHECKLIST — before packaging any version

Part of `llllloc:task-plugin-builder`.

## Build checklist (before packaging any version)

1. **Backend syntax** — copy the backend to a checkable file and lint it (for ExtendScript:
   `.jsx` → `.js` → `node --check`; grep for ES6 leaks `=>` `const ` `let ` `forEach`
   backticks).
2. **Panel JS syntax** — extract the `<script>` block, `node --check`.
3. **Element IDs** — every `$("id")` in JS has a matching `id="…"` in the HTML.
4. **UI compliance** — every interactive element has a `data-tip`; no native `title`
   tooltips; scaling uses `transform: scale()` not `zoom`; drag uses mouse events not
   pointer events (see `panel-ui/references/platform-notes.md`).
5. **Manifest / config** — parse any XML/JSON manifest with a real parser.
6. **INVISIBLE BYTES — run a byte census over every source file you wrote, and refuse to
   package on a hit.** Look for a control byte (under 32, tab and newline and carriage
   return excepted) and for an invisible character (NBSP, zero-width space, word joiner,
   BOM, line and paragraph separators). **A backslash-u escape typed into a file through a
   tool arrives on disk as the REAL byte, not as the characters you typed.** On 17 September
   2026 that put a NUL inside a regex in one source file, a NUL in a build note, and
   invisible characters in a build script. Build the character with `String.fromCharCode`
   instead — and build the census's own list of forbidden characters from numbers, for the
   same reason. `KEEP/tests/build-app.mjs` is the worked example: it censuses, parses every
   `.js`, and exits 1 rather than package.
7. **Installer** — `chmod +x` the `.command`; sanity-check both scripts use path variables,
   replace-on-exist, and print the success message.
8. **Zip name = root folder name** — `unzip -l` the finished archive and confirm its
   single root folder is `PLUGIN-NAME-V<version>-INSTALLER/`, matching the filename.
   Easy to get wrong by zipping your working directory; it means two versions unzipped
   side by side collide.
9. **A test for a change to a function CALLS THAT FUNCTION.** Never re-implement the code
   inside the test and compare your two copies — that is not a test, it is the same
   understanding written twice. On 30 August 2026 a test did exactly that, reported the
   output IDENTICAL and 3.8x faster, and stayed green for three builds while the code it
   stood for produced a project Premiere refused. **If the real function cannot be reached
   from a test, that is the finding — say so.** Delete a test that proves nothing; a green
   test that proves nothing is worse than no test.
10. **Scratch never lands in the user's plugin folder.** Working zips, probes and staging
   copies go in a scratch folder, not beside their installers. If one lands there, name it
   in the handback and ask before removing it. **Probe a folder for write access with
   `test -w`, never by creating a file** — on a mounted folder a delete can need the user's
   own permission, and the probe file is then permanent litter.
11. **Package** the installer folder as a zip and present it.

Run the checklist against the **built archive**, not the working folder — that is the
thing the user actually receives. **A gate cannot see inside a zip nested in your package**
(an app bundle, a second archive), so whatever builds that inner zip runs its own checks.

