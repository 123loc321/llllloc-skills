---
name: task-plugin-builder
description: "Builds installable plugins, panels and add-ons for desktop creative software (Adobe CEP/UXP, OBS, Resolve, Figma, VS Code, Blender), always packaged as a one-double-click installer folder."
---

# llllloc:task-plugin-builder — cross-software plugin & extension builder (renamed from plugin-builder, 15 Oct 2026)

Builds installable plugins for desktop software and packages them so **the final output is
always a folder the user double-clicks to auto-install** — on any Mac or PC, for any
username, no manual path editing. That makes every plugin sellable as a product: the buyer
unzips, double-clicks the installer, restarts the host app, done.

Three rules govern every build:

1. **The deliverable is a one-double-click installer folder.** Never hand back loose files
   with "copy this to that folder" instructions as the primary path. Always produce the
   installer bundle (see "Delivery format"). Manual steps only ever appear as a fallback in
   the README.
2. **A PANEL's UI uses the llloc-UI design system by default.** Read `panel-ui/PANEL-UI.md` and
   build the panel from its reference deck, unless the user explicitly asks for a different
   look (host-native styling, a client's brand, etc.).
   **A standalone companion app is not a panel — 17 September 2026.** KEEP shipped a Mac app
   beside its Premiere panel, and the app was built in the house panel style. the studio had to
   send a screenshot and say *"the Ui should be more like the app atlas here"*. An app that
   sits beside the host wears the platform's own clothes — system font, system controls,
   system window chrome — and keeps only the accent. **And when the user names a real
   product for the look, in words or with a link or a screenshot, that product is the lock.**
   Name it on the `Cloned:` line, with what you did not use and why.
3. **Never overwrite the user's own file. Rename it aside and leave it there.** See the
   next section. This one cost a 38.7 MB Premiere project on 30 August 2026.

---

## NEVER OVERWRITE THE USER'S FILE — 30 August 2026

**A plugin that rewrites a document the user made can destroy a day of their work in one
click. SPLIT did. Read this before writing any code that saves over an existing file.**

**What happened.** SPLIT rebuilds a Premiere project file to do its job. It asked Premiere
to open the new file, then told Premiere to save that project over the user's real one.
`app.openDocument()` returns as soon as the host ACCEPTS the request — **it is not a
promise that the file opened**, and Adobe documents no completion signal. The open failed,
the save went ahead anyway, and a 38.7 MB project became unopenable.

**The four rules, in order. Every one of them is a step the old code skipped:**

1. **Write the new file somewhere else first**, beside the original, never over it.
2. **Read it back and prove it.** Compare the CONTENT to what you built, **and the BYTE
   COUNT on disk to the byte count you wrote.** Both, because either alone lets a bad file
   through — a gzip that stops short still decodes to the right text if your reader does
   not verify the checksum.
3. **Confirm the host really opened it by asking the HOST, not the command.** Poll
   `app.project.path` (or the host's equivalent) until it is the new file, with a bound and
   a timeout. **Never let the thing being commanded report its own success.**
4. **Move the original aside with a RENAME, then save under its name.** A rename is
   instant, cannot half-succeed, and if any later step fails the user's file is still on
   disk under the new name. **A COPY IS NOT A BACKUP** — a 38 MB copy through the host file
   API can fail silently, and SPLIT ignored its return value for months.

**Then delete only files you made yourself. The renamed original is the user's to delete.**

**Before the rename, every failure exit must say so in those words** — *"your project was
not changed"* — because it is true, and because a user who has just seen a plugin touch
their work needs to know which side of that line they are on.

**Test it by recording what was touched.** A test that drives the real finishing code
against a fake host, records every file operation, and asserts the ORDER — write, verify,
open, confirm, rename, save — catches this. `SPLIT/tests/test-safety.js` is the worked
example: 25 checks, and the one that matters proves that when the rename fails, **nothing
is saved over the user's filename.**

---

## Read-first map

| When | Read / open |
|---|---|
| Before building the panel UI | **`panel-ui/PANEL-UI.md`**, then `panel-ui/assets/reference-panel.html` + `panel-ui/references/design-system.md` — the llloc-UI default look for a PANEL |
| Before building a standalone companion app's UI | the product the user named. Not `llloc-UI`, and not FIND |
| To pick the right architecture for the host | `references/hosts.md` — which plugin system each app uses (CEP, UXP, Lua, extension APIs) |
| Before theming any panel control | `panel-ui/references/LOCKED-RULES.md` — the 21-point gate, read every time |
| Before packaging any version | `references/build-checklist.md` — the checks every build passes |
| Where a panel UI runs, and what Adobe CEP does not forgive | `panel-ui/references/platform-notes.md` |
| To write the installer | `references/installers.md` — the one-double-click Mac + Windows pattern, per host |
| Starting an Adobe CEP plugin | `assets/cep-template/` — a minimal working CEP panel (manifest, .debug, CSInterface.js, host bridge) to build on |

---

## The shape of a plugin (any host)

Every plugin has three parts. The names differ per host but the roles are constant:

1. **UI panel** — what the user sees. Built with llloc-UI by default. HTML/JS for CEP,
   UXP, OBS docks, VS Code webviews; host-native for others.
2. **Backend / API bridge** — the code that talks to the host app's own API to actually do
   the work (read the timeline, transform a layer, filter a video, etc.). ExtendScript for
   CEP, UXP JS for UXP, Lua for OBS/Resolve, the host's extension API elsewhere.
3. **Installer** — the one-double-click folder that puts everything in the right place on
   any machine.

Read `references/hosts.md` to map the user's target software to the right system before
writing code.

**A fourth part, when the job needs it: a companion desktop app.** A host app gives an
outside program no door of its own, so the app reaches the HOST through the panel. Make the
app the SERVER and the panel the CLIENT, on `127.0.0.1`, with a token the app writes to a
file the panel reads. The panel then needs only the browser calls it already has, and no
extra manifest permission. Say in the README that the panel must stay open, because it is
the only door.

---

## Build recipe

1. **Identify the host and its plugin system** (`references/hosts.md`). If the user hasn't
   said which software, ask once — it determines everything.
2. **Build the UI panel with llloc-UI** (unless told otherwise): clone the reference deck's
   shell, theme, size scaler, and tooltip engine; design only the content cards for this
   plugin's job. Give every control a `data-tip`.
3. **Write the backend bridge** in the host's language, honouring its constraints (e.g.
   ExtendScript is ES3 — see hosts.md and the CEP template).
4. **Write the one-double-click installer** for Mac and Windows (`references/installers.md`).
   It must work for any username on any machine (use `$HOME` / `%APPDATA%`-style variables,
   never hardcode a user or computer name), replace any existing install, and print a
   "restart the app → find it here" message.
5. **Run the build checklist** (below), then **package the installer folder as a zip** and
   present it. Name it `PLUGIN-NAME-V<version>-INSTALLER.zip`, with a root folder of the
   same name inside.

---

## Delivery format (ALWAYS this shape)

```
PLUGIN-NAME-V<version>-INSTALLER/     ← top folder carries the version
  INSTALL-MAC.command          ← double-click to install on Mac
  INSTALL-WINDOWS.bat          ← double-click to install on Windows
  NOTES-FOR-NEXT-SESSION.md    ← what changed, what's untested, what not to redo
  PLUGIN-NAME/                 ← the plugin itself (copied into place by the installer)
    …host-specific files…
    README.md                  ← usage + a manual-install fallback
```

- Zip **the installer bundle**, not the bare plugin folder.
- **The zip's single root folder must be named exactly like the zip.**
  `LINK-V1.7-INSTALLER.zip` unzips to `LINK-V1.7-INSTALLER/` — never a generic
  `LINK-INSTALLER/`, and never the name of your working directory. Two versions
  unzipped side by side must not collide or silently overwrite each other. Check it
  before shipping: `unzip -l the.zip | head -4`.
- The installers do all the work: enable whatever the host needs (e.g. unsigned panels for
  CEP), create the target folder, remove any old copy, copy the plugin in, confirm success.
- **No admin/sudo** required — target user-writable paths.
- **User data** (presets, settings) must live in the host's persistent storage
  (localStorage for webview panels), not in the plugin folder, so reinstalling/updating
  never wipes it.
- **A file is not delivered until the user has a file card for it — 17 September 2026.**
  KEEP V0.1 was built, gated and announced, and the studio had to ask where the installer was.
  Write the file straight into his own folder, send that Mac file as a file card
  (`SendUserFile`), then name the full path in the reply (29 Oct 2026). A build that reached
  only a working directory did not ship.
- **A file written by a tool can arrive without its executable bit.** After writing any
  `.command` or `.sh` next to an installer, read the mode back and `chmod +x`. The bit
  inside the zip can be correct while the loose copy beside it is not, and the loose copy
  is the one he double-clicks first.

See `references/installers.md` for the exact, tested Mac + Windows scripts and the target
paths per host.

---

## Build checklist (before packaging any version)

Read `references/build-checklist.md` in full and run every point before packaging any version. A point that fails: fix it, then run the checklist again from the top.

---

## Updating an existing plugin

0. **Ship one change at a time when something is already broken.** A build carrying two
   changes cannot tell you which one broke it. On 30 August 2026 one build moved a working
   file AND rewrote a loop; the rewrite was reverted on a clean correlation and **it was
   innocent** — a day went on the wrong change. **Revert one, test, then the other.** And
   **a revert is a hypothesis, not a fix**: say which it is, and do not write the cause into
   a build note until the revert is confirmed.
1. Read the current files before editing — don't work from memory.
2. Targeted `str_replace` for small changes; full rewrite for large ones.
3. Bump the version chip in the header — every version-bearing place agrees (UI chip,
   backend constant, manifest, and any in-app version gate).
4. Re-run the full build checklist.
5. Re-package the installer zip under the new version number, and **keep the old zip**.
   Versions are cheap; a bad build that overwrote the last good one is not. Tell the user: "unzip, double-click the installer, restart
   the app." User data survives because it lives in the host's storage, not the folder.

---

## Honesty about host APIs

Be straight about what each host's API can and can't do — don't promise impossible features.
`references/hosts.md` lists the common limits per host (e.g. Premiere can't read which
keyframes are highlighted or bend keyframe handles; that's After Effects only). When a
feature isn't possible, say why and offer the closest alternative.

**A capability is a claim, and it needs the same evidence a limit does — 30 August 2026.**
A sentence that says the host CAN do something is written just as flatly as one that says
it cannot, and it is checked far less often. Three SPLIT builds rested on *"a CEP panel
carries Node"*. **Adobe's own cookbook says the opposite** — Node is off unless the
manifest asks — and one page held that answer plus a second fault behind it.

Words to watch in your own writing, on both sides:

| claiming a limit | claiming a capability |
|---|---|
| no API · cannot · not possible · there is no way · nothing reports | carries · supports · has · is available · is built in · ships with · can |

**Search the host's own documentation for the call before you build on it. If no search
ran, write the claim as ASSUMED, in that word.** A wrong limit gets built around. A wrong
capability gets built ON, which is worse.

**When a panel is accused of breaking another app, read the host's own logs — 17 September
2026.** Adobe writes one log per host at `~/Library/Logs/CSXS/CEP12-<HOST>.log`, and it
names every manifest it read, kept or dropped: a panel whose `<Host>` list excludes that
app is logged as `ExtensionManifest is not valid for this host` and never loads. A macOS
crash report at `~/Library/Logs/DiagnosticReports/*.ips` is one JSON header line plus a
JSON body — `usedImages` names every loaded binary and the frames of the faulting thread
name the guilty one. Answer with those two files. Never with a theory, and never by
changing the accused plugin first.

---

## Delivering an edited skill

After editing this skill, ship it by `llllloc:task-skill-creator` rule 2 (29 Oct 2026). The `.skill` carries
the whole folder, the CEP template and the references too. Keep the SKILL.md description dense but
under the character cap.

## WHERE THE JOB FILES GO (16 Oct 2026, FOLDERS v19)

In the job's `_CLAUDE/`: every build in `4_Builds/` (`CHANGELOG.md` newest first, `RELEASE-CHECKLIST.md`), older builds in `4_Builds/Old/`, never in `_DELETE` (the last good build is the way back). Tests in `5_Tests/` (`SMOKE-TEST.md`, `BUGS.md`, test scripts). Pictures in `6_Shots/` (`<NAME>-V<n>_<screen>_before-after.png`, `Golden/` changed only on his word). Feature status in `1_Spec/FEATURES.json`. The full tree: `llllloc:project-code`.
