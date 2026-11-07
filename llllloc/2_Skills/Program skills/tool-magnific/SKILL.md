---
name: tool-magnific
description: "How Magnific is driven on every job: a space, board, node, reference plate, style frame or generation. Runs when the user types its name or when /llllloc:router picks it for one request. Never on its own. Owns board rules, the default render (the 2-node lineup: GPT 2.5 Sunburst Low 1K, Nano Banana 2.1 1K), plate uploading and naming, the @file name tag, reference wiring, the fresh-prompt version rule, the download command (Mac plus Figma), the new-prompt-new-node rule, space creation, the image auto-run rule and the no-video rule."
---

# llllloc:tool-magnific

This skill owns the BOARD. `llllloc:task-prompt` owns the prompt text, the naming and the deck. Write the prompt there. Place it here. Runs only when he types its name or `/llllloc:router` picks it. When a Magnific tool is about to be called and this skill has not loaded, say so in one line and let him tag it.

## RULE 1 — EVERY IMAGE GENERATION LIVES ON A SPACE AND RUNS AT ONCE (6 Oct 2026). VIDEO NEVER RUNS HERE (7 Oct 2026)

- Video: never build a video node and never run a video on Magnific. He renders video on another site. The video prompt ships in the chat as a copy block (`llllloc:task-prompt` section 9).
- Every image generation is a node on the project's Magnific space, run on the board. Never generate with `images_generate` and bring the result back (19 Oct 2026, his words: make everything inside this space only).
- No space yet: create one with `spaces_create`, named after the project folder. Add its row to `llllloc/3_Project maps/Project map_Creatives.md` on the Mac the same turn (bare address) and say `Added: <project> SPACE link.`
- Build the nodes, then RUN every one at once, unasked, with the rule 4 settings. He never has to say run.
- Before the run: `account_balance`. The report line carries the settings and the cost.
- A board node that fails: fix its settings and run it on the board once more. Only a node that fails twice runs through `images_generate` (rule 6), its result back beside it as `<node name> RESULT`, and the reply names each node that did.
- After the run: STOP. The board is the delivery (19 Oct 2026, his words: skip downloading, checking every frame, the contact sheet and the best pick). No download, no contact sheet, no model ranking, until he says `download`. The reply is the one-line board report.
- `DOWNLOAD` MEANS MAC PLUS FIGMA (20 Oct 2026, his words: whenever I say download, do this, but do not download the already downloaded assets). The frames are the ones he names, else every node marked Approved.
  1. Skip what is already on his Mac: list every `1_VISUAL ASSET/From Magnific/ROUND <nn>/` of the job and drop each frame whose file name is already there. Nothing new: say so in one line and stop.
  2. Save the rest in the next free `ROUND <nn>/` (owner `llllloc:task-files-organize` THE MAGNIFIC RULE), named after the node. Download on the Mac with `curl` in Bash, which uses his Mac's own network (29 Oct 2026).
  3. Place them in Figma: a new section beside the last style-frame section, one frame per picture (`llllloc:tool-figma` 1b and 1c for colour and place). Upload from his Mac with `curl` to the Figma upload link.
  4. Never wait for his OK on this upload (20 Oct 2026, his words: for this do not wait for my ok): it is his standing OK for his own downloads into his own Figma file. Quote it in the chat before the `curl`. The Mac's safety check can still block it: then ask him once for `upload to Figma` and upload on his line.
  5. Check the Figma frames are filled. Report the frames as file cards plus the Mac folder path (`llllloc:task-sending-files`), and the Figma link.
- Never delete a node. Never rebuild his columns. Never re-run a node holding a result he has not rejected.
- "Usage limit for this tool" or "not enough credits": stop all runs. Do not retry. Say it in one line. The nodes stay built.

## RULE 2 — EVERY ATTACHED IMAGE IS TAGGED `@file name`, ALWAYS, UNASKED (12 Sep 2026)

Every image on a node is named in the prompt by its exact file name with the extension dropped. Never "reference image 1", never "the second picture". The tag is written when the prompt is written, in `llllloc:task-prompt`, so the deck and the node carry the same names. Outside Magnific, the platform's tag shape replaces it (`llllloc:task-prompt` section 6). A plate named by a hash or `image.png` gets a short name you invent (rule 3 shape), and you say so in one line.

The check: read the finished prompt and count the positional words. One present means the rule did not run.

## REFERENCES ARE WIRES PLUS MENTIONS (20 Oct 2026)

A plate reaches a generator only through a connection. Magnific's own guide (`guides_get('spaces')`, read 20 Oct 2026): a mention needs its connection, and a connection that feeds the prompt needs its mention.

1. Create the generator with a short seed prompt. Its id comes back.
2. `spaces_add_connection`: each plate's `output` into the generator's `reference` port. All connections in one call.
3. `spaces_patch_node` the full prompt into `patch.data.prompt`. Each plate is named as `@[<plate node id>:<plate name>:output]`. The plate name is the rule 2 tag.
4. Read the node with `spaces_get_nodes`: mentions in the prompt equal connections into the node. A mention without a connection, or a connection without a mention: fix it, read again.

## RULE 3 — PLATE NAMES ARE THE ADDRESS

`creations_finalize_upload` drops the file name. Every plate lands called "Creation", so the rename pass is not optional.

1. Pick the plates by eye (rule 5).
2. Convert to JPEG, longest edge about 2000 px.
3. `creations_request_upload`, PUT the bytes with curl, `creations_finalize_upload`. A failed PUT is never retried on the same URL. Request a fresh one. Finalize only after the PUT returns 200, never in the same tool block. The PUT runs with `curl` in Bash on the Mac (29 Oct 2026).
4. Put them on the board as named nodes in one `spaces_create_node` call: `nodeType: creation`, `name` in the shape below, `data.creationIdentifier`. A node is named when it is created, never later.
5. A plate already on the board with a bad name: `spaces_patch_node` with `name`, up to 20 per call.

Name shape: `CODE-CAT-NN_Word`, ASCII, 22 characters or fewer. `CODE` is the project code. `CAT` is the moodboard category: LT light, CG grade, CO costume, CA cast, EN environment, EL element or product, CM camera, TX texture. Example: `HXL-LT-06_Lighting`. Past 22 characters the name truncates inside the mention. Use the same name the plate carries in his moodboard folder.

## RULE 4 — THE 2-NODE LINEUP (31 Oct 2026, replaces the 4-model draft lineup)

Every image frame runs on these two nodes, unasked (31 Oct 2026, his words: "replace the old gpt with gpt sunbrust please remember it next time"). No plain GPT, no Seedream, no Nano Banana Pro. One panel per frame, two nodes in it, left to right in this order:

| Model | Slug | Settings |
|---|---|---|
| GPT 2.5 Sunburst | `gpt-2-mini` | Variant sunburst, Quality Low, 1K. Never High or Max quality. |
| Nano Banana 2.1 | `imagen-nano-banana-2-1` | 1K |

- Another model, size or quality only when he names it, and only for that job. "GPT only" or "chat gpt low 2k" from him means one GPT node, Low, 2K, for that job.
- Each node gets its OWN prompt, written for that model in `llllloc:task-prompt` (19 Oct 2026, his words: each model should have its own prompt). Content locked across the nodes, shape fitted to each.
- Naming trap: `imagen-nano-banana-2` is Nano Banana PRO, out of the lineup. Nano Banana 2.1 is `imagen-nano-banana-2-1`. The old Nano Banana 2 (`imagen-nano-banana-2-flash`) is out too.
- The model goes in `data.mode` as its slug, never `auto`. Four Nano Banana slugs look alike (`-2`, `-2-1`, `-2-flash`, `-2-lite`), so read the model back on the node.
- Variants (Sunburst, Flare) exist only on GPT 2.5. GPT 2 (`gpt-2`) has no variants. "GPT" or "chat gpt" with no number means GPT 2.5.
- QUALITY AND VARIANT ARE SET AT CREATE TIME (20 Oct 2026, variant 31 Oct 2026). A GPT node made without a quality runs at Medium (G1 Run GPT v2, he caught it). Every `spaces_create_node` call for a GPT node carries `data: {mode: "gpt-2-mini", variant: "sunburst", quality: "low", resolution: "1k"}`. The read-back shows neither quality nor variant, so a missing one there proves nothing. The check is the create call itself: no `quality: "low"` or `variant: "sunburst"` in it, build the node again. After the run, read the variant on the render with `creations_get` (`metadata.variant`). A duplicated node inherits its source's settings, so check every copy too.
- Aspect ratio: whatever HE set on his own node. Never change it. If the deck wants another shape, say so in one line. He crops in post.
- The cost line: `GPT Sunburst Low 1K + NB2.1 1K, <n> frames, <n> nodes, <n> credits`.

## RULE 5 — PICK THE PLATES BY EYE, NEVER BY FILE NAME

His moodboard folders hold up to twenty plates each. Build a contact sheet per folder on the Mac with the `sheet` tool of `llllloc:task-learn-video` (a name on each tile), write it into the project folder, and look. ImageMagick `montage` fails here ("bad CPU type", 29 Oct 2026). Then name the plate you picked and the one property you picked it for.

- Claude can see a render: `curl` the signed URL from `creations_get` or `creations_wait`. Look before asking him to describe it.
- Three to five plates per node: one grade, one light, one wardrobe or cast, plus the product. More than five averages into mud.
- The product plate rides on every node, so the product stays true in every frame.
- Every plate gets an instruction in the REFERENCES line, ending with a line like "Take color, light and texture from these only, never their subject or framing."
- A render he praises for one property (texture, light, grade) becomes a plate: save it to `3_Art Direction/plates/` and name it in the rule 3 shape with the matching CAT (TX, LT or CG). A model copies a property from its own past render better than from words.

## RULE 6 — THE BOARD IS WRITTEN WITH THE spaces_* TOOLS (20 Oct 2026)

The old board agent `spaces_edit` is gone (deprecated by Magnific, checked 20 Oct 2026). The board is written with `spaces_create_node`, `spaces_patch_node`, `spaces_add_connection` and `spaces_delete_connection`. Read Magnific's guide `guides_get('spaces')` once per thread before the first write.

- Nodes before connections. Create every node first, then add every connection, then patch the prompts.
- Every field goes in `data`: `patches: [{ nodeId, patch: { data: { prompt: '...' } } }]`. Never a JSON string.
- Read each result. `ok: true` means that step is done; never repeat it. An error names what to fix: fix it and try once more. Still failing: say it is not done.
- Ids from an earlier turn can be stale, because he edits the board. "Node not found" means a stale id: read the board again.
- Verify with `spaces_get_nodes`: name, model, size, connections. The read-back never shows quality or variant (rule 4).
- A big `spaces_state` result is saved to a file: read it with a short script (node names, ids, positions), never by eye.
- BOARD LAYOUT (19 Oct 2026, his words and screenshot: always organize them like this). One panel per frame, named after the frame (`G1 Jump-Run`, `KR03 Rare-Drop`). Inside it, the lineup nodes in one row, left to right in the RULE 4 order (or the models he named, in his order). Rows stack top to bottom in frame order, 160 apart. Build it with `spaces_create_node`: first the panel (`nodeType: panel`), then each generator with `layout.groupId` set to that panel and `relativeToNodeId` the node before it, `direction: right`. PLATES AND GENERATORS ALIGN (31 Oct 2026, his marked screenshot: always): plates panels sit left of their row, every RIGHT edge on one vertical line. Generator panels: every row's first panel has its LEFT edge on a second line, 200 right of the first. All plates panels are purple (`#2B192D`), generator panels `#16222F`. Other hex shows blue. No nested panels. Old versions move out of the panel, renamed `OLD ...`.
- EVERY BATCH IS ITS OWN GROUP (31 Oct 2026, his words: each batch in a different group node so i can review better). A new batch of prompts for a frame or person never joins an old panel. It gets a new panel in the same row, right of the row's last panel, named `<row name> Batch <n>`, same colour. Create it with `layout.relativeToNodeId` on that last panel, `direction: right`, `alignment: start`, its nodes with `layout.groupId` in the same call, chained `right`. Unchained, 5 or more nodes wrap to 2 lines.
- The board runner can fail instantly: `spaces_run` returns `completed_with_errors` after a second or two. GPT nodes fail most. A second failure is the only case for the API (rule 1): the same prompt through `images_generate` with the rule 4 settings, the results added back and renamed `<node name> RESULT`. The API takes references by position, so the prompt's `@names` become `@img1`, `@img2` in plate order.
- More than about seven `images_generate` calls in one block can fail with "Not enough credits" while the balance is full. Send a big batch in groups of six or fewer.

## RULE 7 — A NEW PROMPT ALWAYS GETS A NEW NODE (9 Sep 2026)

A node is a version. Overwriting one leaves the old picture under a prompt that never made it. New frame or new version: create a fresh node with the rule 4 settings, then wire and prompt it (REFERENCES). His template nodes stay untouched. The node name carries the version when there is more than one: `FR 03 GPT v2`. An old version is renamed `OLD ...` and moved aside, never deleted. A node he duplicated by hand copies the prompt text and settings, not the connections: wire it again before it runs.

## RULE 8 — A NEW VERSION IS A FRESH PROMPT, NEVER A PAST RENDER (20 Oct 2026)

Each edit saves the picture again, so grain and blur pile up (20 Oct 2026, his words: the texture got worse after each edit). And he wants each version made new (20 Oct 2026, his words: create the pic again by fresh prompt, not by attaching past generated pic). Every new version is a fresh, full prompt that folds in all his notes so far. Only the source plates are wired: the character sheet, the world or product plate, his own references. Never a past render of the same frame. An edit of a past render runs only when he asks for an edit by name; then it wires the clean master, never an edit of an edit, and ends with texture lines: a fresh, clean first-pass render matching the master's surfaces, with no added noise, grain, blur, smudging, compression marks, over-sharpening or extra contrast. First used on LBT-OPEN_Amber-Cabinet_GPT_v3 and v4.

## RULE 9 — RELIGHT AND GRADE: NB2.1 PLUS A PROMPT (7 Nov 2026, his words: use this method as the main one)

New light or the brief's grade: one fresh NB2.1 node per frame that edits the finished frame, the client's photo of that scene wired for light only. Never the Relight node: it redraws the scene (4 of 4 broke). Prompt shape and checks: `llllloc/4_Lessons/Programs/Magnific/relight-nb21-prompt.md`.

## THE ORDER THAT WORKS

1. Prompts first, in `llllloc:task-prompt` (load it if it is not loaded): one fitted prompt per model per frame, two per frame for the lineup.
2. Read the board. Find his own generator node per model. That is the pattern.
3. Pick the plates by eye off contact sheets.
4. Upload, then put the plates on the board as named creation nodes (rule 3).
5. Per frame: a NEW panel for this batch, never an old one (RULE 6 EVERY BATCH), then the fresh lineup nodes inside it with the rule 4 settings and seed prompts. Never reuse a node that ran. A new version is a fresh prompt with source plates only (rule 8).
6. Wire the plates, then patch the full prompt with its mentions (REFERENCES).
7. A model he named for this job, outside the lineup: repeat in full for it (rule 4).
8. Read every node back: mentions equal connections, no `<p>` in the text, the right slug and size, and every GPT create call carried the rule 4 settings. One missing: go back to step 5 for that node.
9. RUN every node on the board (rule 1). A node that fails twice is the only one that runs through `images_generate`.
10. Report in one line: what is on the board, the settings, what it cost. Then stop (RULE 1).

Deeper cases live in `llllloc/4_Lessons/Programs/Magnific/`. List it and read only the file that matches the job (16 Oct 2026, his words: read only the lesson that is needed).