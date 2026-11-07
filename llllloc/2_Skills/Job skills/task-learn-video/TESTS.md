# Tests — llllloc:task-learn-video (26 Oct 2026)

### A dropped link with a project
Prompt: `for the client project, learn from this: https://www.youtube.com/watch?v=...` (a DaVinci grading tutorial)
Should trigger: yes, after the router, with `llllloc:project-creatives` and `llllloc:task-research`
First thing Claude should do: read the client map row, then run `study_video.py` on the Mac through Remote Control (one brief, the whole pipeline)
Done looks like: `*_CLAUDE/2_References/LESSON_<video>.md` with a numbered recipe, every step with a time and a frame file, the raw batch in `_batches/<video>/`, one line in `llllloc/4_Lessons/Programs/DaVinci Resolve/From videos.md`, the files sent and attached

### Many links, no project
Prompt: `study these 3 comfyui videos, i want to learn how they replace the background` (three links)
Should trigger: yes
Done looks like: three LESSON cards under `llllloc/4_Lessons/Programs/ComfyUI/`, each with the workflow JSON link found in the description or marked "not shared", a COMPARE block that says what the three agree on and where they differ, no project folder touched

### Apply later
Prompt: `apply what you learned from the Qazi video to the client L01 clips`
Should trigger: yes, APPLY mode, with `llllloc:tool-davinci-resolve` and `llllloc:task-colorist`
First thing Claude should do: read the LESSON card, never re-study the video
Done looks like: the recipe mapped to his footage's pipeline, built with the tool skill, a before and after frame of his clip beside the tutorial's, the numbers compared, "not run" on any step with no tool

### Should not trigger
Prompt: `analyze this ad for its cut and pacing: https://www.youtube.com/watch?v=...`
Should trigger: no (that is `llllloc:references` + `llllloc:references-edit`: the video is the reference, not a lesson)

### Should not trigger
Prompt: `learn`
Should trigger: no (`llllloc:task-learn`, the thread study)
