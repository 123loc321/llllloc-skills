# TESTS: llllloc:tool-filmcraft (26 Oct 2026)

Should load:
1. "open the client project in filmcraft and sort the bins like in premiere"
2. "rebuild the L01_top edit in FilmCraft from the plan and render it"
3. "make a V2 of the L02_bottom FilmCraft sequence with a slower shot 3"

Must not load:
4. "make a V2 of the L02_bottom Premiere sequence" (Premiere: llllloc:tool-premiere-pro)

Pass when: test 1 ends with `Bins sorted` and the check output ok; test 3 shows V1 in OLD VERSIONS/V1/ and the working sequence named V1.1.
