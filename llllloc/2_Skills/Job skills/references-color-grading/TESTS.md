# llllloc:references-color-grading — tests

1. Drop a graded ad with "this grade": expect per-shot YLOW, YHIGH, SATAVG, UAVG, VAVG averaged between cuts, a curve read (toe, shoulder) with numbers, a split tone in degrees, skin angle against the skin line, and a node order for Lumetri and DaVinci.
2. Drop a log clip: expect it called log with the tells (histogram bunched, YMIN far above 16, low SATAVG) and the likely camera log named with `~`.
3. Drop an HDR file: expect PQ or HLG from color_transfer, MaxCLL when present, and no SDR numbers claimed as nits.
4. Drop a before and after pair: expect a .cube written with lut-estimator or the numpy fit, applied back with ffmpeg lut3d for a check.
5. One graded still alone with "give me the LUT": expect "system only" in the LUT field and the sheet carrying the curve and split instead, said plainly.
6. A film with a warm scene and a cold scene: expect ACROSS SHOTS to name both looks as time ranges, and any single mismatched shot by number.
7. A client's own footage: graded as given, no rights line anywhere.
8. Reply ends with core rule 9's two lines; every number has a source or `~`.
