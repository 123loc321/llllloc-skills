# Running a study on the Mac (29 Oct 2026)

This session runs on his Mac, so it runs the study itself in Bash (STUDY step 3). Nothing to install, nothing paid, nothing deleted.

The script and its text reader live in the Mac copy of this skill: `~/Desktop/Claude/llllloc/2_Skills/Job skills/task-learn-video/`. The first run builds `vision_ocr` and `sheet` beside the script with `swiftc` (about 20 seconds each). The Homebrew ffmpeg 9 on his Mac has no drawtext filter and converts grey through video range (16 to 235): the script knows both, so never work around them.

Fill in: the link (a YouTube link, or a local file path), the batch folder (from WHERE IT GOES), the words file (the program's own words, or leave the flag out), the card when a check is wanted. A batch on a drive under `/Volumes/` gets an `ls` of the drive first: not mounted, stop and tell him.

1. `cd` into the skill folder above.
2. Run, with the quotes: `python3 -I study_video.py study "<link>" --out "<batch>" --words "<words file>"`
   It downloads the captions and a 1080p copy with yt-dlp, cuts the frames where the screen changed, reads the text on each frame with Apple's text reader, and writes `index.md`, contact sheets and `STUDY_READY.md` into the batch. A 15 minute video takes about 2 minutes. No captions: the script runs whisper on the audio by itself, about 3 more minutes per 10 minutes of video. A long run goes in the background so the reply is not blocked.
3. yt-dlp stops with "Sign in to confirm you are not a bot": run the same command once more with `--cookies opera` at the end, and say in the reply that the cookies were needed. No other browser, no other account. Any other error: stop and name its last 10 lines in the reply.
4. When it ends, read `STUDY_READY.md` in full and `index.md` from the batch with Read, in place. Then `transcript.txt` and `sheets/` in the order of HOW TO READ, and single frames as the reading needs them.
5. Change nothing else on the Mac. Do not open the video in a player, do not delete the batch, do not install anything.

Only when a card exists and a check is wanted:

6. Run `python3 -I study_video.py check "<card>" --batch "<batch>"` and read its output.
