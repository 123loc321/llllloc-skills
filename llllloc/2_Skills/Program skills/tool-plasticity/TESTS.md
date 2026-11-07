# llllloc:tool-plasticity — tests (22 Oct 2026)

1. "what is in my Plasticity file" -> loads the skill, loads the plasticity tools in one ToolSearch, list windows, connect, status, answers with bodies and sizes in mm, changes nothing.
2. "make a 20 mm cylinder next to the cube" -> reads status for the revision, saves a copy first if the file is saved, calls plasticity_call with plasticity_create_cylinder, reads back the bounds, says the file is not saved.
3. Plasticity opened from the Dock, "take a screenshot" -> list windows fails with "fetch failed", the reply is the BRIDGE DOWN steps, Plasticity is not closed by Claude.
4. Must NOT trigger: "model a chair in Blender" (llllloc:tool-blender, no Plasticity).
