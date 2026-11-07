# PIPELINE — from an audio file to a Whisper JSON on his Mac

Part of `llllloc:task-vo-to-srt-subtitle`. Read before Mode 1. Rebuilt on 8 Oct 2026 from SKILL.md. Lines marked NOT VERIFIED were not checked on his Mac.

JOB: he gets one command to paste, and a JSON with a start and an end for every word comes back.

INPUT: the file name and folder, read off his screenshot.

STEPS
1. Give the Mode 1 command from SKILL.md with the file name, the language and this film's names filled in.
2. The JSON lands beside the audio, same name, `.json` on the end. He says done. Claude reads it from disk (29 Oct 2026).
3. Check the JSON before Mode 2: it must hold a `words` list inside each segment. No `words`: the run had no `--word_timestamps True`. Say so and give the command again.

SETUP, only when the command fails or the Mac is new
- `whisper: command not found`: ask first, then put `uv run --with openai-whisper` before the command (29 Oct 2026).
- `ffmpeg` missing: `brew install ffmpeg`
- First run of a model downloads it once. `large-v3` is about 3 GB.
- A video file works as it is. Whisper reads the audio track through ffmpeg.

MACWHISPER (he said on 30 Aug 2026 that he moves to it)
- Its export must carry word-level timings. A segment-only export (`"timestamp": "00:04-00:07"`) cannot be cut. SKILL.md, NO WORD TIMINGS.
- The menu path for a word-level export in MacWhisper: NOT VERIFIED. Look it up before telling him where to click.

RULES
- `--word_timestamps True` is never left out. Reason: without it the job starts again.
- `large-v3` for a client film. `turbo` only for a rough pass. Reason: `turbo` loses rare words, and the rare words are the brand names.
- A Whisper word can stretch over a silence (the model does this, it is not a bug in one tool). A caption that seems to start early in a pause is this fault. Flag it. Never move the time by hand.
- Never promise how long the run takes.

CHECK: the JSON opens, and `segments[0].words[0]` has `word`, `start` and `end`.
