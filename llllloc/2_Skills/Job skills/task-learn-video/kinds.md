# Kinds of video, and what to capture

Pick the kind in STUDY step 1 and write it in the card header. The kind says where the lesson hides: in the screen, in the speech, or in a linked file. A video can be two kinds (a breakdown that ends in a tutorial): capture both.

| Kind | The lesson is in | Capture | What goes wrong |
|---|---|---|---|
| Software tutorial (a grade, an edit, a comp, a 3D build, an app feature) | the screen | every panel and field touched, in order, with its value; the node tree or layer stack as a list; the before and after | the speaker says a reason while the screen shows the value, and a reader keeps only one |
| Workflow setup (ComfyUI, a pipeline, an automation, a script) | a linked file | the file from the description (workflow JSON, repo, Patreon post) first; then the node list, the models and custom nodes to install, the inputs and outputs, the run order | the JSON is in the PNG or behind a membership, and the frames are the only copy: then list every node name from the frames |
| Breakdown, case study, making-of | the speech | the decisions and their reasons, the references named, the order of work, the numbers (lens, frame rate, budget, days) | mistaking the result for the method: a breakdown shows what, rarely how |
| Talk, lecture, essay | the speech | the claims, the principles, the examples that carry them, the sources named | copying slides as the lesson: the slide is the claim, the talk is the argument |
| Review, comparison | the speech and the test frames | the criteria, the verdict per item, the numbers, the test setup, the deal breakers | the sponsor shaping the verdict: mark the segment, weigh the verdict |
| Process, vlog, day-in-the-life | the speech | the steps and their timing, the tools, the checks the person does, what they redo | nothing to apply: then the card is short, WHAT TRANSFERS says why |
| A finished film, ad or piece (he asks to learn the craft, not to match it) | the screen | the shot list by time (cut points from `llllloc:references-edit` MEASURE and MERGE: TransNetV2 plus PySceneDetect), the technique per shot, the cut points, the sound against the picture | matching it: that is `llllloc:references` with its medium skills, not this skill |

## What a program's recipe needs

A recipe that cannot be rebuilt from the card is not a recipe. For these programs the card lists:

- **A grade (DaVinci Resolve, Premiere Pro, his COLOR app):** the color management (input and output color space, the transform nodes, the timeline space), the node tree in order with each node's purpose, every value per node (lift, gamma, gain, offset, saturation, curves points, qualifier ranges, LUT names), the scopes shown and their readings, the still exported. A `.drx`, `.dpx`, LUT or PowerGrade link counts as LINKED.
- **A ComfyUI workflow:** the workflow file (JSON, or the PNG that carries it), every node by name with its key values, the models and files by exact name and where they load from, the custom node packs to install, the inputs (image, mask, prompt) and where the output goes, the run time and VRAM said.
- **An edit (Premiere Pro, DaVinci Resolve, FilmCraft):** the sequence settings, the cut points with their reason, the transitions and their lengths, the speed changes, the sound steps, the export settings.
- **Motion and compositing (After Effects, Cavalry, MOTION app, Fusion):** the layer or node stack, the keyframe times and values, the easing, the expressions as written, the effects and their values, the comp settings.
- **3D (Blender, Plasticity):** the modifier or operation order, the values, the material setup, the render settings, the reference images used.
- **Code and automation:** the repo or gist linked, the commands run, the files changed, the versions named, what broke and how it was fixed.
- **AI image and video models (Magnific, a prompt tutorial):** the model and its version, the prompt as written, every setting, the seed when shown, the inputs, the one change that fixed the result.

## Words for the text reader

The script accepts `--words words.txt`, one word per line, and the Apple text reader then prefers those spellings. Give it the program's node, panel and setting names before the run: it turns `Ga1n` into `Gain` and keeps `DaVinci Wide Gamut` in one piece. A short list of the program's own words beats a long one.
