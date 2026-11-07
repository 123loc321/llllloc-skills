# llllloc:references-cinematography — tests

1. Drop a 30 s ad with "how did they shoot this": the router loads llllloc:references + llllloc:references-cinematography (not edit). Expect: a shot table with one row per shot, each move with x, y, z in widths per second from the flow script, rig and lens marked `~`, a VFX column filled or `none`.
2. Drop a oner (one long take) with a gimbal orbit: expect PySceneDetect to give one shot or a few false splits merged by eye and said so; jitter low, roll near 0, rig read as gimbal or Steadicam with that evidence.
3. A dolly zoom clip: expect z opposite in sign to the lens change, parallax high, technique named contra-zoom with lineage (Vertigo).
4. A clip with a set extension: expect the tell named (parallax lag, grain mismatch) and a VFX BUILD block with what to shoot on set (clean plate, markers, HDRI).
5. A client's own footage with their logo and product: expect the sheet to carry the logo and product as given, with no rights or release line anywhere in the reply.
6. "This camera move" on a still image: expect a one-line redirect to llllloc:references-photo (lens, framing) and no video commands run.
7. Same film dropped for both cut and shots: expect two sheets (edit and SHOTS) that cross-reference by shot number, no duplicated cut-rate numbers in the SHOTS sheet.
8. The reply ends with core rule 9's two lines; every number has a source or `~`; unknowns are named in OPEN.
