---
name: tool-comfyui
description: "How Claude drives ComfyUI for llllloc, on Comfy Cloud (his Pro account) and on his Mac through comfy-cli and the comfy-mcp connector. Runs when the user types its name, or when /llllloc:router picks it for one request: any job that builds, checks, runs or shows a ComfyUI workflow, a partner node (Seedance, Kling, MiniMax) or a Comfy Cloud render. Holds the panel rule (every running or latest workflow sits in his Workflows panel), the auto-run rule for paid renders, file names, setup facts and traps. The craft of the prompt lives in llllloc:task-prompt, the shot notes in the job folder."
---

# llllloc:tool-comfyui (V6, 4 Nov 2026)

## TOP RULES
1. THE PANEL RULE (his words, 27 Oct 2026). The workflow that is running now, or the latest one, always sits in his Comfy Cloud Workflows panel (left side bar, Workflows) so he can review it. Why: he checks the graph himself before and after a render. Do it the same turn the workflow is built, before the run. Steps: PANEL below.
2. OUTPUTS go to the project folder, tree like the panel (RENDERS below).
3. PAID RUN = AUTO RUN (his words, 4 Nov 2026: "always auto run without asking me again"). A partner node (validate says `spends_credits: true`) or a Comfy Cloud run spends his credit. Never ask: say the price in one line, run with `--allow-spend` the same turn, then log the cost (RENDERS step 6). If the Mac safety check blocks the run, tell him in one line what to type in that session. Free local runs need no asking.
4. NEVER DELETE. A stray panel entry moves to `workflows/_DELETE/` (MOVE below). An old version moves to `_Old versions`.
5. CHECK THE ACCOUNT before a cloud run: `comfy --where cloud --json cloud status` must show tier PRO. The browser may have signed in a Free account (402 error).
6. WIRE FIX CHECK before any local Comfy job (his words, 28 Oct 2026: "so this bug wont never happen again"). `ls ~/ComfyUI-Installs/*/ComfyUI/custom_nodes/llllloc_wirefix/js/wirefix.js` lists every install (loc, kling). One missing, or a new install: copy `llllloc_wirefix/` from the newest `CODE/Plugins/COMFY-WIRE-FIX/COMFY-WIRE-FIX-V<n>-INSTALLER/`, check again, then he reloads the window (Cmd + R). After a Comfy update: open `Wirefix_Test_SD20_V1` in loc. 4 image wires and 1 video wire on Seedance, or the add-on needs a fix (its CODE job).

## PANEL
Layout (his words, 27 Oct 2026: folders "like delete, job name, old version" so he can view better, plus one group folder per model family: MiniMax, Seedance). The job folder takes his name for it (a client BG swap: `bg swap test`):
```
workflows/
  _DELETE/                      strays, never deleted
  <Client>/<Job>/<Model>/               the latest version (e.g. a client/bg swap test/MiniMax/)
  <Client>/<Job>/<Model>/_Old versions/ every older version
```
1. Keep two files per version in the job folder: `<Name>_V<N>_comfy-ui.json` (UI format, has `nodes` and `links`, what the panel opens) and `<Name>_V<N>_api.json` (API format, what the run uses). Build the UI file from the template's UI JSON (`fetch_template`) or the last UI version, never by hand from the API file.
2. Validate both: `comfy --where cloud --json workflow validate --workflow <file>`. An error: fix it, validate again.
3. Push: `python3 -I scripts/push_to_panel.py <Name>_V<N>_comfy-ui.json <Client>/<Job>/<Model>`. The panel name drops `_comfy-ui`. Older versions of the same name move to `_Old versions` by themselves.
4. CHECK: the script prints `IN PANEL <Client>/<Job>/<Model>/<name>.json`. `NOT LISTED`: go back to step 3. Tell him the folder and name, and that the refresh arrow at the top of the Workflows panel shows it.
5. Another thread's workflow: push ITS latest UI file (newest modified time) into the right folder, read only. No UI file: build its UI file from that job's last UI version with the new settings, as a new file. Never edit the other thread's files.

`comfy workflow save --where cloud` writes a store the panel does not show. Use the script.

## MOVE (a stray entry, or a folder change)
`move(src, dst)` in the script: POST `<base>/api/userdata/<quoted workflows/src>/move/<quoted workflows/dst>`. Paths are relative to `workflows/`.

## SETUP FACTS
- comfy-cli 1.23.0 runs Comfy Cloud with `--where cloud`: upload, workflow validate, run, jobs wait, download. Sign-in is `comfy cloud login` (OAuth in the default browser). Token: `~/Library/Application Support/comfy-cli/secrets.json`.
- Cloud has no custom nodes. Partner nodes and native nodes only.
- Uploads come back as hashes (`<sha>.png`): note hash and real file name side by side.
- API format: autogrow inputs are 0-based for H3 (`ref_images.ref_image_0`), named for Seedance (`model.reference_images.image_1`). SaveVideo needs `format.codec`.
- Local ComfyUI: `~/ComfyUI-Installs/loc/ComfyUI`, start with the Desktop model paths yaml. How-tos and traps: `llllloc/4_Lessons/Programs/ComfyUI/comfyui-mcp.md`. Research lines: `llllloc/5_Research cache/platforms/comfyui.md`.
- Heavy video models (MiniMax H3) run on Comfy Cloud, not the Mac.

## SEEDANCE 2.5 (node ByteDance2ReferenceNodeV2)
- `task_type` edit keeps the source clip's length and aspect. Top size 1080p (short side 1080). No frame pinning: guides go in as reference images.
- In the prompt, tag by socket order: @Video 1, @Image 1, @Image 2.
- Wire bug (28 Oct 2026): the Comfy frontend drops this node's image_2+ wires when a workflow opens. Comfy Cloud runs no add-on: run from the API file, and tell him the panel lacks the image wires. Local: TOP RULE 6. Comfy Desktop opens its own saved draft (`Comfy.Workflow.Draft.v2`) when newer than the file, so a wire fix is tested on that draft, never only in a fresh browser tab. Node ids come back as text ("35").
- Stills that show a person: Seedance copies their poses and shots. Use one or two, or empty plates.
- Price at 1080p with a video in: about $0.01 per 1,000 pixel-frames, 4 s billed at least. A 3 s 3:4 clip costs about $2 to $3.

## RENDERS (his rule, 27 Oct 2026)
Every ComfyUI output goes straight to the job's project folder, never left in the app's own output folder (`~/ComfyUI-Shared/output/`).
1. Path: `<project>/1_VISUAL ASSET/From Comfy UI/<Job>/<Model>/`, the same tree as the panel under the client folder (a client: `From Comfy UI/bg swap test/MiniMax/`). Older versions and their compares go to `<Model>/_Old versions/`.
2. Cloud: `comfy --where cloud download <prompt_id> -o "<that path>"`, then rename the file to the job's export name (drop `_00001_`).
3. Local run: the same `-o` with `comfy download`, or move the file from `~/ComfyUI-Shared/output/` the same turn. A copy left there moves to its `_DELETE/`.
4. A new version lands: move the older output of the same model to `_Old versions/`.
5. CHECK: `ls` the model folder shows the new file. Missing: go back to step 2.
6. Write time, cost (balance before and after) and a read in the job's test notes. The map row holds the path.
