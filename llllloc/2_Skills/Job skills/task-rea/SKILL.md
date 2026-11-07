---
name: task-rea
description: "Runs REA (Reverse Engineer Anything, github.com/morluto/rea, the rea-agents CLI) to read how a shipped app works without its source: a Mac app, an Electron or JavaScript app, a native binary, a .NET assembly, an APK or a packaged file. Returns findings with evidence, kept apart as observed, inferred and unknown, so a Code job can build its own version. Runs when the user types its name or says REA, or when /llllloc:router picks it for \"look inside this app\", \"how does this app do it\", \"reverse engineer\" or \"decompile\" on an installed or downloaded app. A website or web app to rebuild belongs to llllloc:references-code, which calls this skill only for an app bundle. Never runs REA before his own words \"run REA\" (the Mac's safety check blocks it), never installs Ghidra, Java, Hopper or the REA MCP without his yes, and never launches or changes the app it reads."
---

# llllloc:task-rea (24 Oct 2026, renamed from llllloc-tool-rea the same day, his words "call it llllloc task REA instead"; first words: "make this a new skill ... I want it to be a separate skill, and also add it to the schedule update list")

REA reads an app without its source code and returns what it found with the evidence and the limits. This skill says how REA runs in this project. REA's own skill (`.agents/skills/reverse-engineer-anything` in the repo, 33 KB) is never installed: it assumes the MCP server, which is not set up here. Its rules are folded in below.

## TOP RULES

1. His words before the first run. REA downloads code with `npx` and runs it. The safety check on his Mac blocks that (Typer thread, 24 Oct 2026). Ask him to type `run REA` in the chat. Then he approves the command prompt in this chat (29 Oct 2026). One "run REA" covers every REA command of that ask.
2. Read only. Never launch the target, never change its files, never send it anywhere. A file REA must cut (a universal binary) is copied into the job first. Runtime capture (it runs the app) only on his word, named in the ask.
3. Evidence or unknown. Every claim is OBSERVED (REA evidence ID or command output), INFERRED (say from what) or UNKNOWN. A static read never claims what the app does at run time. Keep REA's limitations in the notes. Why: a rebuild on a guessed number is wrong from the start.
4. Nothing installed without his yes: `rea setup` (it rewrites his agent settings), the REA MCP, Ghidra, Java, Hopper, JADX, a global `npm install`. Show `setup --dry-run --json` before any setup. Name the size and the folder before any install.
5. Everything lands in the job. The npm cache, the raw evidence and the notes stay in the job's `_CLAUDE/2_References/` folder, never in `llllloc/` (H10). The craft lines that serve every job go to the `CODE.md` dossier of `llllloc:references`.

## WHERE IT RUNS

On his Mac, in Bash, in the job folder under `~/Desktop/PERSONAL PROJECT/CODE` (29 Oct 2026). Node 24.22.1 there meets REA's floor (`^22.23.4`, `^24.22.1` or `>=26.12.1` since 6.8.0. Node 23 and 25 refused). A bundle, ASAR or binary he sends or that is public is copied or downloaded into the job's references folder first, then read with the same commands.

Command shape on the Mac, run from the job's references folder:

```
cd "<job>/_CLAUDE/2_References" && npm_config_cache="$PWD/.npm-cache" npx -y rea-agents@latest <command> <absolute target path> --detail summary --evidence_output "$PWD/_batches/<target>.evidence.json" --json
```

Big apps make huge evidence (a 14 MB `app.asar` gave 253 MB of JSON in a practitioner test). Always ask for `--detail summary` with `--evidence_output`, then read only the parts the question needs with `rea inspect-evidence-bundle` or `inspect-analysis-view`. An existing output file is never overwritten, so each run gets a new name. Since 6.8.0 the same summary-then-page way works for call graphs, load images and browser scenarios: `--detail summary`, then `inspect-analysis-view` on the returned parent evidence ID, one page at a time. Ask for `--format json`, never `jsonl`, when the whole report is needed. A batch decompile and a feature trace page the same way (views `batch-decompile` and `feature-trace`). Big pseudocode too: decompile with `--detail summary`, then `inspect-analysis-view` with view kind `native`, facet `pseudocode`, offset 0, limit 20000, and follow `coverage.next_offset`. Offsets count UTF-16 code units, not lines. Pages reuse the one decompile, never a rerun (REA skill tree dc9854f). A later command that needs an earlier result gets `--evidence-bundle <absolute path of that evidence.json>`, never a rerun of the first read (REA skill v60). Run `npx` from the job folder, never from inside the target, with absolute target paths.

## ROUTE THE TARGET

| He gives | First command | Needs |
|---|---|---|
| A Mac `.app`, runtime unknown | `inspect-desktop-application <app>` | nothing more |
| An Electron app or `app.asar`, a JavaScript folder | `analyze-javascript-application <asar or folder>` | nothing more |
| A native binary: the exact logic inside a function | `analyze`, `search`, `decompile`, `xrefs` with `--provider ghidra` | Ghidra 12.1.x and a full JDK 21 (not installed, about 1 GB, rule 4). Universal Mac binary refused: `lipo -thin arm64` a copy into the job, then read the copy. A big binary that times out on Ghidra start (330 s): run it once more with `REA_GHIDRA_STARTUP_TIMEOUT_MS=1800000` in front of the command, never repeat the same cold import unchanged. |
| A .NET `.dll` or `.exe` | `inspect-managed-artifact`, `inspect-managed-members` | nothing more |
| An Android APK | `inspect-android-package`, `inspect-android-class`. A release build with its `mapping.txt`: pass that file's absolute path as the mapping path. Native (JNI) code: `inspect-android-jni-bindings`. | JADX and a full JDK (rule 4) |
| A packed or firmware file: a Bun `--compile` app, an ESP32 image, Intel HEX, S-record, UF2, DfuSe, U-Boot uImage, a classic NES `.nes`, a Unity AssetBundle, a WeChat `.wxapkg` | `inspect-artifact <file>`, then `extract-artifact` into a new folder in the job. A Bun app: read its extracted JavaScript with `analyze-javascript-application`. | nothing more. REA never decrypts: an encrypted package stays unknown. |
| A Go or Rust binary, a `.gguf` or `.safetensors` model, a Godot `.pck`, a SQLite file | `inspect-go-binary`, `inspect-rust-binary`, `inspect-model-artifact`, `inspect-artifact`, `inspect-sqlite-database` | nothing more |
| A Windows `.exe` or `.dll`: TLS callbacks, security flags | `inspect-pe-load-config <file>` | nothing more |
| An ELF, PE or Mach-O binary: is it hardened (PIE, NX, RELRO, stack protector, FORTIFY, stripped) | `inspect-binary-hardening <file>` | nothing more, the file is not run. One answer per Mach-O slice. A missing import is UNKNOWN, not proof the protection is off. A code signature row means present, not valid. Hardened runtime stays unknown: REA's signature reader (`inspect_signature` in its skill, CLI name from `--help`) reads it. |
| A Linux kernel module `.ko` | `inspect-kernel-module <file>`. A `.ko.xz` or `.ko.zst`: unpack a copy into the job first. | nothing more |
| A stand-in copy of a web app that agents can test against (AgentEnv bundle) | `capture-browser-scenario` once, then `environment-export`. From a HAR he has: `environment-build <capture.har> <dir>`. | Chrome (rule 4). Record only on a throwaway copy he names, because each write step changes real data. Write steps go through the app's own forms and buttons, so each request carries what the app really sends; a create keeps the new object's ID with `save_response`, and IDs are never guessed (REA skill v50). Passwords only from environment variables he names, never typed in chat. |
| A test task for a desktop app's stand-in copy (from a `capture-desktop-application` folder) | `describe-desktop-application-task <capture> --format json`, then write the task JSON (`name`, `prompt`, `checks`), then `export-desktop-application <capture> <dir> --task <task.json>` | CLI only. Capture runs the app: his word first (rule 2). The prompt says what the user wants in the app's words, never paths, file formats or the checks. Checks hold only what the user changed: never what the app stamps (times, IDs, window sizes), never a whole file. A few strong checks: whole lines, rows by real columns, `at_least` when more may come. REA keeps the task only when every check fails on the seed and passes on the end state. An app no apt repository installs: ask him for its `.deb`, never fetch a vendor download page. Never run agents unless he asks. The seed is his real data: it stays on his Mac. |
| A website | `llllloc:references-code`. REA's browser tools need Chrome with remote debugging, an install step (rule 4). | When it captures a site's traffic: find the API origins in the loaded scripts first, pass the page origin plus them in `allowed_origins`, and read `completeness.excluded` before saying an API is absent. |
| His own source code | normal code tools. REA is for shipped apps only. | |

Unsure of a command or flag: `npx -y rea-agents@latest --help`, or the repo `docs/cli.md`. Never guess a flag. The additions from REA skill v53 to v60 and tree dc9854f (mapping file, JNI, the packed and firmware readers, `--evidence-bundle`, binary hardening, pseudocode pages, desktop app tasks) may need a rea-agents newer than 6.8.0: check `--help` first. Missing there: say it is not in the current REA yet.

## STEPS

```
- [ ] 1 Target named, its path read with ls (never guessed)
- [ ] 2 His "run REA" in the thread
- [ ] 3 Questions written: what must REA answer, and what evidence would answer it
- [ ] 4 Smallest overview first (summary), then only the feature asked about
- [ ] 5 Every finding marked O / I / U with its evidence ID or command
- [ ] 6 Notes written to the job's _batches/<target>.md
- [ ] 7 Each question marked answered, partly answered or open
```

1. "My app" with no name: ask which app. Never pick one for him.
2. Plan the questions before the commands. Example: "how does TypeSeer hide weak suggestions" needs the model call, its settings and the filter code.
3. Run the route command. A missing engine (Ghidra, JADX) stops only the part that needs it: finish the static part, then ask once for the install, with its size and folder.
4. A blocked or failed command: read the error, fix the cause once. The same error twice: stop and tell him what blocks it. Never repeat an unchanged command.
5. Check: every line in the notes has its evidence or says unknown. One has neither: go back to step 4 for it, or mark it unknown.
6. Reply in plain words: what the app does, how sure, what is still unknown and what would read it.

## AFTER THE READ

A Code job builds its own version from the findings, never from pasted decompiled code: `llllloc:project-code`. A web or app reference gets its rebuild spec from `llllloc:references-code`.

## UPDATES

The daily outside check watches REA two ways: the `rea-agents` tags (the CLI, run fresh with `@latest`) and REA's skill folder as a base of this skill. Every change to that base is folded in here with `llllloc:task-skill-creator` REFINE and shipped, with no judging of fit (5 Nov 2026, his words: "whatever REA does, it's ok"). Only the hard stops and the top rules above still win. REA's MCP server and client plugin are not used here, so their setup and repair steps stay out. Folded in: skill version 60, tree dc9854f, rea-agents 6.8.0 (6 Nov 2026: binary hardening, big pseudocode in pages, test tasks for desktop app copies. 5 Nov 2026, tree cb2cb7d: v53 to v60, mapping file and JNI for APKs, packed and firmware readers, evidence reuse, batch and trace views, SPA traffic origins. Before: v50, tree 20e4e29 on 27 Oct).