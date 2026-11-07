# llllloc:task-retopology tests (19 Oct 2026)
1. "this tripo model is too dense, can you clean it up" + a .glb -> loads the skill, runs retopo.py at 5k and 12k, sends the sheet and numbers.
2. "I need this AI character rigged for animation, retopo it first" -> 12k base, says hand loops or Quad Remesher are needed, does not run Quad Remesher.
3. "remesh this robot to low poly for a game" -> uses --crease 30, 5k target.
Must NOT trigger: "build a low-poly game level in Blender" (llllloc:tool-blender, no dense model to fix).
