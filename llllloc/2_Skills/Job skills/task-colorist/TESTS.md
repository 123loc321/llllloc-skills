# llllloc:task-colorist — tests

### Match
Prompt: "the 13 shots in MATCH COLOR still jump, match them"
Should trigger: yes
First file Claude should open: method.md (section 7)
Done looks like: a hero per scene named, blacks matched first, a CHECK table per shot in 10-bit codes against the section 9 targets, the flip test reported, LUTs versioned and proved against ffmpeg lut3d.

### Look
Prompt: "give the client film a warm filmic look, not too much"
Should trigger: yes
First file Claude should open: method.md (sections 1 to 6)
Done looks like: pipeline and mid grey named first, one look for the whole piece with the curve, split, saturation map and print written as numbers, skin of the lead measured and held, restraint stated in the plan.

### Read
Prompt: "what do the scopes say about shot 7"
Should trigger: yes
First file Claude should open: scopes.md
Done looks like: black, white, cast, skin angle, saturation by zone and gamut each as a number with the scale named, then the one fix in order.

### Must not trigger
Prompt: "this grade is beautiful, what film stock is it" with a dropped still
Should trigger: no (llllloc:references-color-grading reads a reference)
