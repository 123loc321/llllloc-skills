---
name: task-colorist
description: "Grades footage the way an award-winning colorist does: pipeline first, balance with Offset in log, the lead's skin before blacks and whites, contrast at the mid grey pivot, one look for the whole piece, print emulation once at the tail, then shot match and texture. Reads every scope at Nobe OmniScope level (waveform, parade, vectorscope with targets and skin line, Sat/Lum, histogram, CIE, false color) and writes a grade plan with numbers, a .cube and a match report. Runs when he types its name, or when /llllloc:router picks it for a grade, color correct, shot match, LUT build, look, or any work in his COLOR app, Lumetri or DaVinci Resolve (always the house node tree). Never renders, saves his Premiere project or installs anything without his word. Reading a reference grade is llllloc:references-color-grading."
---

# llllloc:task-colorist (21 Oct 2026)

Grading is a fixed order of small global decisions, judged by eye and checked on scopes. The best grades are invisible, continuous across the cut, and built around the lead's skin. This skill does the grading. `llllloc:references-color-grading` reads a reference. `llllloc:tool-premiere-pro` touches his Premiere edit. The COLOR app (`CODE/PR Plugin/COLOR`) is his grading window: its scopes and LUT preview are the measuring tools here.

## TOP RULES

1. **Eye first, scopes to check.** The eye decides the look. Scopes catch what the eye drifts on: black level, a cast, a clip, a hue off the skin line (Haine: 80 to 95 percent eye, 5 to 10 percent scopes). Never stretch a shot to the rails because the waveform "should" touch 0 and 100 (davinciresolveclub). Why: an exterior at 85 can be right, and a chased scope is the mark of an amateur grade.
2. **Pipeline before colour.** Name the source (log or Rec.709, which log), the working space and the display before the first move. Grade in log, convert to display last (Volpatto, mononodes). Why: every number below depends on the space.
3. **Skin of the lead first, then everything else.** Volpatto: "There is no reason for me to make the white white, the black black, if the skin tone of the main character is not right." Never key or window skin as the first fix. Balance moves skin, the Red and Yellow vectors steer it. A secondary on skin only for a beauty fix.
4. **Fixed order on every shot.** Pipeline → balance (Offset or printer lights, never Lift) → contrast at the mid grey pivot → saturation (subtractive, with density) → hue shifts → look → print → texture. Same order on every shot of the piece. Why: order changes the result (mononodes), and a fixed order makes matching three sliders on one node.
5. **One look for the whole piece, built upfront.** A show LUT or look node sits on the timeline before any shot is touched (Poole, Lucas, Bogdanowicz). Shots are then balanced under it. Never a different creative LUT per shot.
6. **Restraint.** "The best colour is not necessarily the most colour." Add red before adding saturation (Kelly). Texture (grain, halation) only when the piece asks for it, and after colour.
7. **Done is judged on the cut, at playback speed, full screen.** Flip between shots. A match is a feeling of continuity, not aligned scopes (Moran). Then the numbers confirm.
8. **Nothing destructive without his word.** Never render, save his Premiere project, overwrite a LUT or install a tool. A new LUT is a new file with a version. Core rules 1, 2 and 6 hold.

## WHAT THE ASK IS

| He says | Job | Read |
|---|---|---|
| grade this, make it look like, give it a look, cinematic | LOOK: build one look for the piece | `method.md` sections 1 to 6 |
| match these shots, they jump, make them the same | MATCH: match every shot to the hero under the look | `method.md` section 7 |
| fix the colour, it looks off, too warm, the skin is wrong | BALANCE: correct one shot or all | `method.md` sections 2 to 4 |
| read the scopes, what do the scopes say, is this legal | READ: a scope reading with numbers | `scopes.md` |
| any grade in DaVinci Resolve | the house tree, then LOOK or MATCH inside it | `davinci-tree.md` |
| make a LUT, bake the LUT, export .cube | LUT: bake the current grade as a .cube and prove it | `method.md` section 8 |
| a reference look, "this grade", a dropped film | not this skill: `llllloc:references-color-grading` first, then LOOK | - |

Two jobs in one message: LOOK first, then MATCH. A short vague ask ("make it better") is BALANCE then LOOK, with the assumptions named in one line.

## THE RUN

Copy into the status checklist and tick:

```
- [ ] 1 Pipeline named: source space, working space, display, mid grey value (method.md section 1)
- [ ] 2 Hero shot picked per scene (the widest frame) and the lead's skin measured (L, vectorscope angle)
- [ ] 3 Scopes read before any move: black, white, cast, skin, clip (scopes.md). Numbers in the plan
- [ ] 4 The grade built in the fixed order of rule 4, one decision per step, numbers written down
- [ ] 5 Match: every shot against the hero, blacks first, then contrast, density, saturation, key hues
- [ ] 6 Check by eye: flip at playback speed, full screen. Fails: back to step 4 or 5
- [ ] 7 Check by tool: the scope numbers of every shot within the targets (method.md section 9). Fails: back to 5
- [ ] 8 LUT baked and proved against ffmpeg lut3d (method.md section 8), or "no LUT asked"
- [ ] 9 Grade plan written to the job's *_CLAUDE/2_Research/GRADE-PLAN_<name>.md
```

A step with no tool to run it (no footage on disk, no app open) is written as "not run", never ticked.

## TOOLS

- **The COLOR app** (`CODE/PR Plugin/COLOR/COLOR-V<n>-INSTALLER/OPEN COLOR.command`): the 13 shots or a session file, scopes at OmniScope level, LUT preview that is the baked LUT. Its self-test is `_CLAUDE/5_Tests/check.js`. A number read in the app is a number that ffmpeg confirms.
- **Measurement without the app**: the `ffmpeg`, `ffprobe` and Python lines in `llllloc:references-color-grading` MEASURE (signalstats per shot, Lab percentiles, split tone, skin angle).
- **Lumetri** (Premiere): Basic (white balance, tone), Curves, Color Wheels and Match, HSL Secondary (skin, beauty only), Creative (Look LUT). Lumetri cannot pivot contrast at mid grey or do subtractive saturation: say so and do that part in the LUT. Driving Premiere: `llllloc:tool-premiere-pro`.
- **DaVinci Resolve**: always the house tree and run in `davinci-tree.md` (27 Oct 2026, his words). project settings DaVinci YRGB, DaVinci WG / Intermediate, Rec.709-A out; IDT in the group pre-clip, EX, WB, HSV SAT per shot, LOOK and ODT in the group post-clip. Driving Resolve: `llllloc:tool-davinci-resolve`.
- **Match engine**: the V3 engine of the client match thread (log space, Offset balance on the subject, skin hue locked within 3 degrees, chroma per tone band in Oklab). Reuse it, never rebuild it.

## OUTPUT

The reply opens with what changed and what he should look at (one shot, one flip), then the numbers, then what is not done. Under fifteen lines, the rest in the plan file.

`GRADE-PLAN_<name>.md` (sensible default, adapt the sections to the job):

```markdown
# GRADE PLAN <name>            <date> · built by llllloc:task-colorist
## PIPELINE   source, working space, display, mid grey
## HERO       shot per scene, skin L and angle, why this shot
## READ       black, white, mid, cast, skin, clip per shot (table, 10-bit values)
## LOOK       the curve (black, white, pivot, contrast), the split, the saturation map, the hue shifts, the print, the texture, each with its number
## MATCH      per shot: exposure, tint, saturation trims; shots still off and why
## LUT        file, version, size, proof (max error vs ffmpeg lut3d)
## CHECK      flip test result, scope targets met or missed
## OPEN       not measured, not run, his decision
```

## WHAT THE BEST DO (short form, long form in method.md)

Poole watches the piece two or three times before a move. Fisher starts where exposure and colour naturally sit. Lucas sets the LUT first and grades underneath with printer lights, windows last. Volpatto balances the lead's skin first and never changes the DP's temperature or tint. Kelly: exposure, then contrast with pivot, then balance on two axes. Bogdanowicz: darken the unimportant, lighten the important. mononodes: middle grey is the anchor, contrast is structural, saturation is subtractive, skin is steered by red and yellow, order is the method. Nakamura: unpolished films have mismatched shots.

Test prompts: `TESTS.md`. Why each rule is here: `NOTES.md`.

## NEVER

A LUT before the balance. A skin qualifier as the first fix. Saturation pulled or pushed everywhere. Grain that the delivery compression kills. A number without a source or `~`. A receipt for a check that did not run.
