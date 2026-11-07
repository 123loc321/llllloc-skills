# The method

The craft behind the steps. From the 10 Oct 2026 research pass (film, trailer, music video and brand film sound designers, Premiere mixers; ~40 sources, report in `llllloc/5_Research cache/jobs/sound.md` line 2026-10-10 and `reports/Sound design for brand films.md`).

## Contents
- The rule above the others
- Spotting
- The palette
- Layering
- Levels
- Ducking
- Delivery
- The amateur tells

## The rule above the others

Decide what the listener hears at each second, then remove or duck everything that competes with it. Walter Murch: an audience follows two and a half elements at once. Randy Thom: if everything is loud, nothing is loud. The ad designer's line: silence is half the job. A 60 s film needs one real drop toward near-silence before its biggest moment, so the moment reads as loud.

## Spotting

One list, every event with a time, the VO word it lands on, and the intent. Categories: UI (a card, a stat, a phone, a button), AIR (a riser into a reveal, a whoosh out of one, a texture bed under a hero shot), LOW (a sub land on a logo, a product, a big number), SIL (a planned near-silence). A cut gets a designed sound only when:
1. something visibly moves, lands or appears,
2. the cut changes place, time or chapter,
3. it is a hero moment: logo, product, title, stat, call to action.
A montage cut to music gets at most one accent every other cut, and the music carries it. Trailer shape for the end: riser, then strip everything except one hit transient and a low-end drop, hold the music down, let the tail ring.

## The palette

Five families cover a brand film: close material contact (click, cap, glass, paper), air and breath (whoosh, riser, swish), one mono sub for lands only, tonal elements in the music's key (chime, ping, shimmer), and a bed so a drop never reads as dead air. Luxury beauty words: whisper, muted click, chime, crisp, precise. Rejected: friction, hiss, rubbing, braam, anything "indefinite". Search Soundly by the material, never by "whoosh".

## Layering

A hit is two or three layers with their peaks on the same frame: transient (4 to 12 kHz), body (80 to 500 Hz), sub (20 to 80 Hz, mono, high-passed off every other layer). A whoosh starts 10 to 20 ms before the move, peaks at the fastest moment, stays under 0.5 s for a fast move, 1 to 3 s for a sweep. Never the same file twice unmodified: another take, a pitch shift, or 2 dB less.

## Levels

The VO is the anchor. Everything else is measured against it, from measured numbers (premiere-mechanics.md MEASURE), never by ear through a script.
- Music under speech: 12 to 18 dB below the VO (broadcast 8 to 16, phone-first about 20). Swell 6 to 10 dB in a real gap of 1 s or more. Phone speakers forgive nothing: lean to 15.
- UI sounds: peaks 12 to 18 dB under the VO peak.
- Lands and risers: peaks 14 to 18 dB under the VO peak, the biggest one (logo) 12.
- Texture beds: 20 dB or more under the VO.
- Hits never stack with a music swell: the logo gets one chime and one sub, not three.

## Ducking

His music curve is a Volume > Level keyframe list. Read it first. Add windows to it with `add_audio_keyframes`, or reproduce his end swell inside a `setup_ducking` call, because that tool replaces the whole curve. Windows: speech spans from the transcript, fades 0.3 to 0.8 s, dip starting before the first word. Duck against the voice only, never against SFX, or every hit pumps the music. Premiere's Essential Sound ducking is his tool, not Claude's: scripting cannot tag clips.

## Delivery

Web and social: -14 LUFS integrated, -1 dBTP (VO-led corporate: -16). EBU R128: -23 LUFS, -1 dBTP. ATSC A/85 (US TV ads): -24 LKFS, -2 dBTP. Platforms only turn loud files down. A hard limiter sits on the master for the mix export only. Stems (VO, MUSIC, SFX) go out unlimited, 48 kHz 24-bit WAV, all starting at zero, so they sum to the mix. Check on a phone and in mono. Measure the exported file again (`analyze_loudness`).

## The amateur tells

One library whoosh on every cut. The same hit reused. A sound on every movement. Music at one level under the VO. No high-pass, so the low end piles up. Untrimmed tops and tails. Reverb on everything. A braam under a beauty logo. No bed, no silence. Each one has its fix above.
