# llllloc:references-color-grading — notes

- 2026-10-17 08:05 UTC: built on his pick "Option A, one skill: llllloc:references-color-grading". Reads the grade as a curve plus a colour system; the planned llllloc-task-color-grading job skill will do the grading itself.
- Tools verified 17 Oct 2026: ffmpeg waveform, vectorscope, histogram filter options (run locally on ffmpeg 6.1), signalstats keys (YMIN, YLOW, YAVG, YHIGH, YMAX, SATAVG, HUEAVG, UAVG, VAVG, BRNG), ffprobe colour fields and HDR side data (mastering display, MaxCLL, Dolby Vision record), scikit-image rgb2lab and rgb2ycbcr, colour-science 0.4.7 (Oklab), lut-estimator 0.1.2 (fits a .cube from a before and after), OpenColorIO ociobakelut, Adobe Cube LUT spec 1.0.
- Reading facts: S-Log3 grey at about 41 percent, LogC4 grey at about 28 percent, DaVinci Intermediate grey 0.336; print emulation tells from the SMPTE article (Cullen Kelly); Kodak 2383 "rich blacks, neutral highlights"; bleach bypass from Kodak; CineStill 800T halation; skin on the I line at about 123 degrees (not verified, common practice).
- No legal rule: his own and a client's footage is graded as given; an outside reference gives its system.
- Sheet: job `*_CLAUDE/2_Research/GRADE_<name>.md`.
- 2026-10-21: HAND-OFF names llllloc:task-colorist as the grading skill (was the planned llllloc-task-color-grading). 13,164 to 13,138 characters.
