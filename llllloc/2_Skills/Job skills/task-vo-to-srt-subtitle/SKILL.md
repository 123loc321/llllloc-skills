---
name: task-vo-to-srt-subtitle
description: "the studio's subtitle pipeline. Turns a voice-over audio or video file into a clean, broadcast-ready SRT through Whisper. Runs when the user types its name or when /llllloc:router picks it for one request. Never on its own. Mode 1 reads a file name off a screenshot and hands back one ready-to-paste Terminal command. Mode 2 takes a Whisper JSON and delivers a review document plus the SRT. Subtitles always go on a Premiere Pro caption track, never into After Effects, Cavalry, MOTION or Figma. Never hand-writes caption grouping and never invents a timestamp."
---

# llllloc:task-vo-to-srt-subtitle

The pipeline, all on his Mac: audio file, then Whisper JSON, then SRT. Whisper writes a start and end time for every word. This skill never creates a time. It only chooses where to cut.

Read `references/pipeline.md` before Mode 1, `references/vocabulary.md` before Mode 1 on a branded film, `references/caption-rules.md` before Mode 2, and `references/glossary.md` on a client or a client film.

## ALWAYS IN PREMIERE (18 Oct 2026)

Subtitles are always done in Premiere Pro, as a caption track on the edit's own sequence (IMPORT INTO PREMIERE). Never as text layers in After Effects, Cavalry, MOTION or Figma, and never burned into a motion render. Why: captions change late, and a caption track is edited and exported from Premiere without a new render. A client sequence that already holds a caption track keeps it, with its style: copy their sequence, never rebuild their captions.

## MODE 1 — GIVE THE COMMAND

He shows where the file is, usually a Finder screenshot of Downloads.

1. Read the file name off the screen, extension included.
2. Read the folder off the Finder path bar. Usually `~/Downloads`.
3. Pick the language. English unless the file, the project or he says otherwise.
4. Give one command block, nothing to edit:

```bash
whisper "$HOME/Downloads/FILE_NAME.wav" \
  --model large-v3 \
  --language en \
  --task transcribe \
  --word_timestamps True \
  --initial_prompt "a client, a client, ONE a client, Vismay Sharma, Kérastase, Elseve, La Roche-Posay, CeraVe, 3CE, Dr. G, NEO, TikTok Shop. Divisions: CPD, LLD, LDB, PPD. Regions: GCC, ANZ, MENA, ASEAN." \
  --output_format json \
  --output_dir "$HOME/Downloads"
```

- `--word_timestamps True` is not optional. Without it Mode 2 cannot run and the job starts again.
- `large-v3` for a client film. `turbo` is two to five times faster and loses rare words, which are the brand names. Use it for a rough pass only.
- Change `--initial_prompt` to the names in THIS film, under 900 characters.

Then two lines: the JSON lands beside the audio, same name, `.json` on the end, and tell me when it is done. Claude reads it from disk (29 Oct 2026). Do not promise a time. Give the setup steps (`references/pipeline.md`) only when the command fails or the Mac is new.

## MODE 2 — BUILD THE SRT

Run the bundled script. Never group captions by hand.

```bash
python3 scripts/build_srt.py INPUT.json --out-dir "OUT_DIR" --name NAME --extend
```

It writes `NAME_final.srt` and `NAME_breakdown.md` and prints a fault report. Read the report. It drives the reply.

Options: `--extend` holds a caption that reads too fast into the silence after it, ending at the next caption's real start (use by default). `--fixes fixes.json` applies approved word corrections. `--split 0.0,4.74` cuts named captions in two. `--compare OTHER.json` lists every word two runs disagree on. `--segments` for a source with no words array.

The three laws, in full in `references/caption-rules.md`:

- Timing: only start and end values that exist in the `words` array. Never estimate, average, round, stretch or invent a time.
- Shape (Netflix Timed Text Style Guide, English): two lines max, 42 characters per line, one line is better. Each caption stays up 0.833 to 7 seconds, at most 20 characters per second. New caption at every sentence end and every silence over one second. Cut at a comma first, then before a conjunction, article or preposition. Never after a function word. Never inside a name, a number or a brand term.
- Word: change no word he has not approved. Deliver what Whisper wrote, list what looks wrong in a table, he marks it, you rebuild.

No word timings: a segment-only export (`"timestamp": "00:04-00:07"`) cannot be cut without a time inside it. Say so first. The right fix is a re-export with word timings. If he wants a file now, run `--segments`: every boundary except a segment's first start and last end is calculated, marked EST, counted in the report, and never handed over as final.

Two runs beat one guess: run the audio with `large-v3` and with `medium`, then `--compare`. Where they disagree, the audio is unclear and a human decides. That list is the flag table. Offer it on a film that matters.

WHAT WHISPER GETS WRONG, check every time: a sentence repeated with no duration (marked LIKELY DUPLICATE, ask before a `drop` rule), a run of real words sharing one time (flag it, offer merge or re-run), numbers in pieces (the script glues them), brand names ("Sapmina" for a client, see the glossary), one spelling in several forms (count them).

## DELIVERY — EVERY ANSWER

Two files, every time: `NAME_breakdown.md` for review and `NAME_final.srt` for Premiere. Both as file cards plus the Mac path (`llllloc:task-sending-files`).

The breakdown is ONE TABLE, one row per caption: `| # | In | Out | Sec | Text | Flag |`. The caption text stays in one column and wraps where the caption wraps, `<br>` inside `<code>`. Never a Line 1 / Line 2 pair. The Flag column carries SHORT, LONG or FAST only. Calculated timing is said once at the top, never per row.

The chat carries only: block count, running time, how many captions fit one line, any timing fault with its block number, the word flag table (`| Block | Whisper wrote | Probably |`), and the cuts you had to force. Never the whole caption list.

## IMPORT INTO PREMIERE

Not File > Import. Put the clip in a sequence, Window > Text > Captions, "Import captions from file", pick the SRT. Choose Source Timecode when the SRT came from that clip's own audio, Playhead position when it did not (park the playhead first). Premiere shows every SRT as 30 fps in the Project panel. Ignore it.

## WHERE THE JOB FILES GO (16 Oct 2026, FOLDERS v19)

A creative job's subtitle files go in `*_CLAUDE/9_Post/Subtitles/` (`OUT_DIR`, 29 Oct 2026). No job: the JSON's folder. A folder appears the first time a file goes in.