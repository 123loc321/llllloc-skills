# TESTSET — old against new (21 Oct 2026)

Twenty messages from real misses in `Lessons_Workflow.md` and project memory. Used by `testing.md`, "Old against new on TESTSET.md". Each run reads the skills Claude loads with the Skill tool before its first other tool call. A script grades it: every MUST skill loaded, no NEVER skill loaded.

Format: `id | message | MUST load | NEVER load | source of the miss`

```
T01 | make 4 Magnific renders of the client mascot in world 2 | llllloc:project-creatives, llllloc:task-prompt, llllloc:tool-magnific | - | Lessons 2026-10-19, tool skill won over prompt skill
T02 | build a small web app to customize the mascot colors | llllloc:project-code, ponytail, using-agent-skills | - | Lessons 2026-10-19, code job skipped ponytail
T03 | here is a screenshot of a website I like, make our home screen feel like this | llllloc:references, llllloc:references-design, llllloc:task-design | - | Lessons 2026-10-19, medium skill never loaded
T04 | here is a still from a film, match its color for the end video | llllloc:references, llllloc:references-color-grading | - | change 4, 21 Oct 2026
T05 | here is a clip, I love the camera moves, use them for the open | llllloc:references, llllloc:references-cinematography, llllloc:task-motion | - | change 4, 21 Oct 2026
T06 | check my workflow | llllloc:project-workflow, llllloc:task-workflow-best-practices | llllloc:task-workflow-update | router STEP 2
T07 | update my workflow, Claude has a new model | llllloc:project-workflow, llllloc:task-workflow-update, llllloc:task-research | - | router STEP 2
T08 | end | llllloc:end | - | core rule 15
T09 | thanks, that works | - | any skill | must not trigger
T10 | add subtitles from this VO script to the Premiere timeline | llllloc:task-vo-to-srt-subtitle, llllloc:tool-premiere-pro | - | memory premiere-sound-subs-rule
T11 | add whoosh and click sounds to the client open in Premiere | llllloc:task-sound-design, llllloc:tool-soundly, llllloc:tool-premiere-pro | - | memory premiere-sound-subs-rule
T12 | new job for Honda: start the look for the XL250R film | llllloc:project-creatives, llllloc:task-design-system | - | router STEP 2 design-system row
T13 | put the racing game online | llllloc:task-web-publish | - | memory web-publish-cloudflare
T14 | export the Figma frames of the deck to the job folder | llllloc:tool-figma, llllloc:task-files-organize | - | router STEP 2 Figma export
T15 | be ambitious: the client deck for the client pitch | llllloc:task-be-ambitious, llllloc:task-design, impeccable | - | memory ambition-and-split
T16 | animate the logo in After Effects with a soft bounce | llllloc:tool-after-effects, llllloc:task-motion | - | router STEP 2 program row
T17 | rename all renders in 4_RENDERS to the Video_APP_Vn names | llllloc:task-files-organize | llllloc:task-design | memory render-naming-rule
T18 | the subtitle skill forgot the two-line rule again, fix it | llllloc:task-skill-creator | - | testing.md prompts
T19 | write the brief and three territories for the Honda film | llllloc:task-art-direction | - | router STEP 2
T20 | what time is it in Paris | - | llllloc:project-creatives, llllloc:project-code | chat row, no job
T21 | look at my current opening pr project, goal is to color match each clip | llllloc:project-creatives, llllloc:task-colorist, llllloc:tool-premiere-pro | llllloc:project-code | router STEP 2 grade row (21 Oct 2026: whole-frame number match was rejected)
T22 | (mid-thread, after Magnific renders) no i mean design the card template in figma | llllloc, llllloc:tool-figma, llllloc:task-design, impeccable | - | router STEP 3.3 new route (22 Oct 2026: figma-generate-design loaded alone)
T23 | (thread with no Mac folder tools) update the design skill so exploring needs no design system | llllloc, llllloc:project-workflow, llllloc:task-skill-creator; .skill in a new Desktop round folder | - | skill-creator rule 2 (22 Oct 2026: .skill left in cloud To Mac/)
T24 | learn | llllloc:task-learn | llllloc:end | new command, 22 Oct 2026
T25 | ok let's end here, deep study this thread, and suggest me what to add to the overall workflow | llllloc:task-learn, llllloc:project-workflow | - | RB06 thread, 22 Oct 2026
T26 | I want to learn Blender shortcuts | - | llllloc:task-learn | must not trigger, 22 Oct 2026
T27 | ok end | llllloc:end | llllloc:task-learn | his words 22 Oct 2026, end inside a short message
T28 | (code job) screenshot of his own app's UI bug with "fix this" | llllloc:project-code, ponytail, using-agent-skills | llllloc:references, llllloc:references-design | COTABBY thread, 25 Oct 2026: a bug screenshot is not a dropped reference
T29 | stricter prompt for the shirt texture on this sheet | llllloc:project-creatives, llllloc:task-prompt, llllloc:task-research, llllloc:tool-magnific | - | Lessons 2026-10-31, a revision skipped research
```

Add a line when a lesson shows a new miss (`llllloc:end` STEP 3). Never edit an old line to make a run pass.

- 2026-10-22 | Mac Remote Control thread, he attaches 2 images and says "find back the design of this map" | PASS = Claude reads the images from ~/.claude/uploads/<session>/ in its first calls, without asking the coordinator
- 2026-10-23 | Mac Remote Control code thread on a Godot game, Claude needs test screenshots | PASS = every test render runs hidden (open -g -j, window off screen), his front app stays in front, no Godot window on his screen; FAIL = a Godot window opens on his screen (his words: "dont open the godot up,it disturb me") | Beauty Isle Godot thread
- 2026-10-23 | he asks to match style frames in colour and light in a game | PASS = the look is judged on 6 or more screenshots per scene in contact sheets before the reply; FAIL = 1 or 2 shots (his words: "take more screenshots to judge better") | Beauty Isle Godot thread
- 2026-10-26 | coordinator asks a thread to edit his videos in DaVinci Resolve | PASS = the router loads llllloc:tool-davinci-resolve from a table row; FAIL = no router row names Resolve (or Filmcraft), so the thread picks skills by its own judgment | a client edit in DaVinci Resolve thread
- 2026-10-27 | he asks to grade his footage to match reference photos in DaVinci | PASS = before showing any grade, the studio paper or a white garment is measured on the real Resolve output and reads neutral (Oklab a, b within 3 x1000 of the camera image), and the look carries no colour tint; FAIL = a warm or magenta cast ships (his words: "the white balance is super off and bad") | a client grade thread
- 2026-10-28 | he types "end" | PASS = the reply's Workflow line is a real wrap-up (findings or "nothing to trim"); FAIL = "Workflow review: not run" (his word: "why") | a client Seedance stills-style thread
- 2026-10-28 | he says "for this one let's test with just 480 first" after a paid workflow was shown | PASS = rebuild at 480p, show the new price, wait for "go"; FAIL = the paid run starts | a client Seedance stills-style thread
- 2026-10-30 | Claude builds a ComfyUI workflow for him to review | PASS = the UI file is in his Comfy Cloud panel AND in his local Comfy Desktop folder (~/ComfyUI-Installs/loc/ComfyUI/user/default/workflows/<Client>/<Job>/<Model>/), inputs copied to ~/ComfyUI-Shared/input/; FAIL = cloud panel only (his words: "i dont see it") | a client GTS loop thread
- 2026-10-31 | an rclone call needs --drive-root-folder-id from a zsh variable | PASS = written as "--drive-root-folder-id=$ID", runs first try; FAIL = "unknown flag" (hit twice)
- 2026-10-31 | he asks for Enter to send in a text box | PASS = Enter is tested with focus in the box, on a list item and on the empty page before "done"; FAIL = tested in the box only, he reports it again ("press enter should trigger this button") | Review Studio thread
- 2026-10-31 | one more marked note arrives in a code thread that already loaded its skills | PASS = the router runs and the Loaded line is honest with no reload of unchanged skills; FAIL = 8 skills reloaded on every small note, the router says project skills load once per thread but STEP 4 copies Skill calls for this ask | Review Studio thread
- 2026-11-01 | he asks for new frames on a new deck slide next to an old one | PASS = the slide copies the grid and sizes of the neighbour slide, no name labels; FAIL = a new grid with labels (he asked to re-layout)
- 2026-11-02 | a Magnific run ends and the reply names credits | PASS = the number comes from account_balance read this turn; FAIL = worked out by hand (780 said, 390 real)
- 2026-11-02 | he calls a metaphor frame "slop, not nice idea" | PASS = new ideas from the client's own objects and the subject's world (task-design RULE 0 point 2); FAIL = another render of the same symbol
- 2026-11-04 | he says a prompt formula that worked should be used for all future videos | PASS = it is saved as a lesson file in 4_Lessons/Prompts/<Model>/ only, no skill edit, because the formula may change; FAIL = the prompt and tool skills got a hard rule and a round folder (reverted, round 103)
- 2026-11-05 | he says Ctrl + Z or Cmd + Z does not work in one Premiere sequence | PASS = Window > History is read before any answer, and llllloc:task-research loads; FAIL = the answer is only the shortcut key (he had to ask again)
- 2026-11-05 | a code job zips a new panel build | PASS = the zip has no ._ files and the gate runs on the zip before delivery; FAIL = ditto packs ._ twins and the gate fails it
- 2026-11-06 | a code job changes a Godot game and needs screenshots (G1 look pass) | PASS = llllloc/4_Lessons/Programs/Godot/ is read before the first run, every check runs headless, and all shots of a check come from ONE hidden launch (open -g -j -n, --position 9000,9000); FAIL = a visible Godot window per shot (he asked "why godot keep opning and then close again?")
- 2026-11-06 | he says a game looks "too ugly", "low contrast" or "too ai" (Sky Climb, 3 rounds) | PASS = before the change, every zone is measured (signalstats luma range and saturation) against the style frames, backdrops are drawn in the engine (no painted AI plates), and the before/after numbers ship with the sheet; FAIL = a look pass judged by eye only, or painted AI plates as the fix
