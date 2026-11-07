# Premiere mechanics

Facts tested on his Mac, 10 Oct 2026, Premiere 25.x, premiere-pro-mcp 1.18.6. General Premiere behavior: `llllloc/4_Lessons/Programs/Premiere Pro/README.md`.

## Contents
- Measure
- Place
- Level
- Keyframes and his music
- Tools that do not exist

The Soundly connector: `llllloc:tool-soundly` (split out 17 Oct 2026).

## Measure

On his Mac, one shell call, every source:
```
ffmpeg -i "<file>" -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input Integrated|Input True Peak"
```
Effective loudness of a clip = file LUFS + clip Volume dB. `get_clip_volume` reads a clip's dB. Premiere stores Volume > Level as a number: dB = 20 x log10(value / 0.1778). So 0.1778 is 0 dB, 0.2884 is +4.2 dB, 0.0262 is -16.6 dB.
`analyze_loudness(media_path, target_lufs, max_true_peak_dbfs)` measures a rendered file (EBU R128). Use it on the last render to know where his mix stands, and on the export after.
The timeline mix cannot be measured without a render. Track faders and the master are invisible to the MCP: a render that reads -13.4 LUFS from sources that sum lower means a fader is up. Keep every change relative.

## Place

1. `create_sequence_checkpoint` with a label.
2. `create_bin "<SEQUENCE>_From Soundly"` under `03_SOUND`. `set_color_label` 11 on the bin and on every imported item, before placing (a placed clip cannot be labeled).
3. `add_tracks audio_tracks=N` adds at the bottom and shifts nothing (video tracks and indexes unchanged, verified). `rename_track audio <index> "SFX UI"`. Three tracks: `SFX UI`, `SFX AIR`, `SFX LOW`.
4. `set_item_in_out(item, 0, <length>, media_type=2)` on any file longer than its slot. Then `overwrite_clip(item_id, start_seconds, track_index=<any empty video track>, audio_track_index=<SFX track>)`. An audio-only item lands on the audio track only. Snap starts to 0.04 s.
5. `set_active_sequence` by id before each batch of writes: he switches tabs.
6. `clear_item_in_out` on every trimmed item at the end.
7. Read the audio tracks back with `get_active_sequence(track_type="audio")`.

## Level

`set_clip_volume(node_id, volume_db)` on a clip with no keyframes. It reports back `volumeDb` and `clamped`. A clip with a speed change reports its keyframes with `time: null`: read `mediaSeconds` against the clip's in and out points instead.

## Keyframes and his music

`get_keyframes(node_id, "Volume", "Level")` lists his curve (time from clip start, value). Convert with the formula above. Before the first keyframe the clip holds the first keyframe's value. `setup_ducking` writes a whole new curve: reproduce his existing windows inside it or use `add_audio_keyframes` for one window at a time. Never leave his logo swell out.

## Tools that do not exist

No audio effect can be added or tagged through the MCP: no EQ, compressor, limiter, Essential Sound tag, auto-duck, crossfade. Those are his hands, and the reply says what to add (a limiter on the master before export). `apply_audio_effect` and `setup_ducking` run on the unsupported QE path: test on a checkpoint copy first.
