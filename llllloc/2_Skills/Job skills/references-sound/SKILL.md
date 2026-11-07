---
name: references-sound
description: 'Reads a sound reference (a music track, a mix, sound design, VO, a film''s soundtrack, SFX) the way a senior sound designer and mix engineer would: layers, tempo and key, tonal balance, stereo width, dynamics and loudness, reverb, transients, sync points to picture, measured with ffmpeg, librosa, essentia and demucs before judged. Loads with llllloc:references, which holds the shared rules and the dossier. Runs when the user types its name or when /llllloc:router picks it for a dropped audio or a film with a mix to analyze or learn from, a sound or music feel to follow, or ''is this good'' on a mix. The picture cut of the same film is llllloc:references-edit.'
---

# llllloc:references-sound (split from llllloc:references, 17 Oct 2026)

Sound is read as layers in time: what plays, how loud, where in the stereo field, with what tone, and when it lands against the picture. The output is a palette and a spotting logic a mix can be built on. Shared rules, modes, the dossier and the reply: `llllloc:references`.

## TOP RULES

1. Loudness is measured, never felt. Integrated LUFS, loudness range and true peak from `ebur128` before any word about "punchy" or "quiet".
2. Tempo gets a cross check. Beat trackers return half or double tempo often: check the histogram and a hand count of 8 bars.
3. Layers are listed by hearing them apart. Separate the stems first (demucs), then list every element in order of level. "Music and some effects" is not a read.
4. A feel transfers: tempo, layer logic, tone, width, the hit anatomy. A client's track, VO and stems are the material of the job and go in as given. An outside track's melody or signature sound comes in when he says so; otherwise the prompt names the technique, because an artist's name alone gives a generic copy.

## MEASURE (run first, raw output to `_batches/`)

```
ffmpeg -i <file> -vn -ac 2 -ar 48000 ref.wav                                                   # the film's track as a wav
ffmpeg -nostats -i ref.wav -af ebur128=peak=true -f null - 2>&1 | tail -12                      # I (LUFS), LRA (LU), true peak (dBTP)
uv run --with demucs demucs -n htdemucs ref.wav       # separated/htdemucs/ref/{drums,bass,other,vocals}.wav (ask first, core rule 1)
python3 - <<'EOF'
import librosa, numpy as np
y, sr = librosa.load("ref.wav", sr=None, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr); print("tempo", float(np.atleast_1d(tempo)[0]), "beats", len(beats))
on = librosa.onset.onset_detect(y=y, sr=sr, units="time"); print("onsets per 10 s", np.histogram(on, bins=np.arange(0, len(y)/sr + 10, 10))[0].tolist())
print("centroid Hz", round(float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())), "rms dB", np.round(librosa.amplitude_to_db(librosa.feature.rms(y=y)[0]), 1)[::sr//512*5].tolist())
L, R = librosa.load("ref.wav", sr=None, mono=False)[0]; print("stereo correlation", round(float(np.corrcoef(L, R)[0, 1]), 2))
EOF
python3 -c "import essentia.standard as es;p=es.MusicExtractor()('ref.wav')[0];print(p['rhythm.bpm'],p['tonal.key_edma.key'],p['tonal.key_edma.scale'],p['rhythm.danceability'])"
```

Reverb tail on an isolated hit: `pyroomacoustics.experimental.rt60.measure_rt60(h, fs, decay_db=60)`. Stereo correlation: +1 mono, 0 wide, below 0 out of phase. Install lines: `pip install librosa essentia pyroomacoustics` (ask first, core rule 1). No `essentia` wheel: key and scale are `~` by ear, say so.

## THE PRO READ

| Field | What to write |
|---|---|
| SPEC | Length, sample rate, channels, format, the measured I, LRA and true peak. |
| LAYERS | Every element you can hear, from the stems, in order of level: VO, music parts, hero FX, textures, ambience, UI sounds. Which are hero moments, which routine. |
| TEMPO AND KEY | BPM with its cross check, time feel, key and scale, where the tempo or key changes. |
| TONE | Where the energy sits (lows, mids, highs, the centroid), what is cut to make room, how VO sits against music. |
| SPACE | Stereo placement and width (the correlation), reverb and depth, dry versus wet elements, how wide the hero is. |
| DYNAMICS | Loudness range, tension and release across sections, the onsets per 10 s series, side-chain or ducking, silence before a hit. |
| TRANSIENTS | Hits, risers, whooshes, ticks: their count, length, how they are built (layered sub, body, click, air), the tail length. |
| SYNC | Which sounds land on which cuts or moves, in seconds, and the offset (sound ahead or behind picture). |
| STRUCTURE | Sections as time ranges: intro, build, drop or reveal, outro, with what the music does to the picture. |
| WHAT MAKES IT LAND | The three to five choices, each with its number. |

## THE SPOTTING LOGIC

The dossier carries the recipe. A film reference also gets a spotting table in `_batches/`: `time | picture event | sound | kind (hero, routine, music in, music out, silence) | intent`. This is the shape `llllloc:task-sound-design` spots a new film with.

## RESEARCH (with `llllloc:task-research`)

The composer, sound designer, mix house or library and their stated process; the technique name (side-chain pump, riser into silence, granular texture, foley layering); the delivery target of the medium (web minus 14 LUFS minus 1 dBTP; EBU minus 23; ATSC minus 24; Netflix minus 27 dialog gated); whether it is durable or a trend; what breaks when copied (every cut gets a sound, risers bury VO). Cache: `llllloc/5_Research cache/jobs/sound.md` and `jobs/ai-audio-prompts.md`.

## WHAT TRANSFERS, WHAT DOES NOT

Transfers: the layer logic, the level ladder, the width plan, the spotting rule, the tempo feel, the tone balance, the hit anatomy. Does not: the track itself, its melody, its stems, its VO, a signature sound.

## HAND-OFF

`llllloc:task-sound-design` builds the palette and spots the film from the layer list and the spotting table; `llllloc:tool-premiere-pro` places it. `llllloc:task-prompt` AUDIO writes music or SFX prompts from TEMPO, TONE and STRUCTURE as intent, never as a track name. A film with a cut also loads `llllloc:references-edit`.
