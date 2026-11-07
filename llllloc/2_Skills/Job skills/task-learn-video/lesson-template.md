# LESSON card template

Strict: the headings, their order, and the step format of RECIPE. Free: the length of each part. Write it as `LESSON_<slug>.md` next to the batch (SKILL.md, WHERE IT GOES). A field with nothing in it says `none`, never disappears.

The four tags, one per step, after the frame:
- SEEN: read on the frame named in the step (the text reader found it, or a zoom crop shows it).
- HEARD: said in the transcript at that time.
- LINKED: taken from a file or page linked in the description (a workflow JSON, a LUT, a preset, a post).
- INFERRED: my reading of what happened. Not shown, not said. Never a number.

A value read by eye from a crop when the text reader missed it is written `~0.82` (a tilde in front), so `check` does not flag it and a reader knows it was not machine-read.

---

```markdown
# LESSON: <title of the video>

Source: <link> | <channel> | <upload date> | <length> | studied <YYYY-MM-DD>
Kind: <from kinds.md: software tutorial, workflow setup, breakdown, talk, review, process> | Program: <DaVinci Resolve 20.2 / ComfyUI / none>
Batch: <path of the batch folder>
Skipped: <sponsor 0:00 to 0:48, outro 15:40 to end> or none

## WHAT IT TEACHES
<Three lines at most. The claim of the video in plain words, and the one idea that makes it work.>

## RECIPE
<One numbered step per action, in the order of the video. Each step: what is done, where (the panel, the node, the field), the value, then its proof.>
1. <Action, panel, field = value.> t=m:ss frame=frames/f_HHMMSS.png SEEN
2. <...> t=m:ss frame=frames/f_HHMMSS.png HEARD
3. <...> t=m:ss frame=frames/f_HHMMSS.png LINKED (workflow.json, node 12)

## VALUES
| Setting | Value | Where | Proof |
|---|---|---|---|
| <Lift Y> | <-0.02> | <Node 02, Primaries> | SEEN f_000412 |

## WHY IT WORKS
<The reasons the speaker gives, and the ones the picture shows. One line each. A reason I added is marked INFERRED.>

## BEFORE AND AFTER
<What changed on screen between the first and the last frame of the recipe, in words a colorist, editor or builder would use. The measure to check an APPLY against: a scope reading, a render beside the reference, a file that opens.>

## WHAT TRANSFERS
<What works on any job, in one line each. Empty when the video is only about its own material. This part decides whether the lesson gets a line in From videos.md.>

## APPLY TO <project> (<certain | likely>)
<How this recipe lands on his material: which clips or files, which tool skill, the steps that change, the values to start from.>

## OPEN
<What the video did not show or say: a value typed too fast, a panel off screen, a step cut out. A question to ask before applying.>

## COMPARE (only in a many-video study)
<Where this video agrees or disagrees with the others studied in the same ask, and which recipe to try first.>

## APPLIED
<One line per apply: date, project, what changed. Empty at first.>

## FILES
transcript: <batch>/transcript.txt | index: <batch>/index.md | sheets: <batch>/sheets/ | frames: <batch>/frames/
```
