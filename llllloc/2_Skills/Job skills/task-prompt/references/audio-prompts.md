# Audio prompts

## Contents
1. Settle before writing
2. Music
3. Sound effects
4. Voice
5. Audio inside video models
6. Model table
7. Failures and fixes
8. Templates
9. Sources

## 1. Settle before writing
- Use: spot music, VO bed, logo sting, UI sound, dialogue, ambience.
- Length: write the exact seconds. Cut length beats "short".
- Loop: say if it must loop. Then ask for a loop and give bars, BPM and key.
- Sync points: list hits in seconds (logo at 0:12). Expect to edit to picture.
- Loudness: take the target from the delivery spec. Normalize in the edit. Models ignore LUFS.
- Names and lyrics: a client's own track, artist, lyrics or voice goes in as given. ElevenLabs Music rejects an artist name in a prompt (its bad_prompt error), so describe the sound there; other models take the name. No legal rule caps a job (his words, 17 Oct 2026).
- Make 3+ takes. One take tells you nothing.

## 2. Music
Prompt order: subgenre, mood, instruments, BPM, key, vocals or instrumental, era/production, arrangement over time, exclusions.
- Name subgenre and era ("80s gated reverb"). Vague prompts give average music.
- Use exact moods ("euphoric"), not "happy".
- Give BPM and key. ElevenLabs holds them. Stable Audio treats BPM as a guide. Lyria 3 has no numeric BPM or key control. Use words there.
- Narrate the arrangement in order: "start with just piano, then bring in drums at 0:15".
- Say where silence goes. Models fill empty space.
- Exclude with "just" and "no melody". In Suno use the Exclude field.
- Never name artists. ElevenLabs returns `bad_prompt` with a suggested rewrite. Describe the sound instead.
- Long prompts are not better by default.

**Structure tags (lyrics box)**
- Use square brackets: [Intro] [Verse] [Pre-Chorus] [Chorus] [Bridge] [Outro] [End].
- Add a cue inside the tag: `[Chorus: fuller drums, wider harmony]`. Suno v6 reads delivery written there.
- Put instrument cues on their own line: `[Cello Solo]`.
- Keep one or two cues per section. Stacked or clashing cues get ignored.
- Lyria 3 Pro: use timestamps `[00:00] ... [00:15] ...` and write `Lyrics:` before sung lines.
- ElevenLabs: use a composition plan for exact section timing.

**Instrumental vs lyrics**
- Suno: turn on the Instrumental toggle. Writing "instrumental" in Style is not enough.
- ElevenLabs: write "instrumental only". Time vocals: "lyrics begin at 15 seconds".
- Lyria: write "Instrumental" in the prompt.
- Write your own lyrics for ads. Keep lines short.
- Full songs from video models (Seedance) are not reliable.

**What each model ignores or misreads**
- Suno v6: negatives in the Style box read as inclusions. Style Influence at 50% dilutes a detailed prompt. Raise it. Set Variety to 0 when testing tags.
- ElevenLabs Music: no stated prompt limit. Fills silence unless told.
- Stable Audio 2.5: no negative prompt. Describe what you want.
- Udio: no downloads on any plan (Sep 2026). Not for delivery.

## 3. Sound effects
- One sound per prompt. Split unrelated sounds into separate generations.
- Write: source + material + action + space + perspective + duration.
  Example: "heavy oak door, slow creak then latch click, small stone room, close mic, dry, 3 s".
- Use terms: impact, whoosh, riser, braam, drone, one-shot, loop.
- Multi-part sound: describe events in order.
- Set duration. Short hits work best at 1 to 10 s. Ambience can run to the cap.
- Prompt influence (ElevenLabs): high = literal, low = varied.
- Loops: turn on Loop (ElevenLabs). Use it for rain, hum, room tone. MP3 only for loops; WAV 48 kHz only for non-loops.
- Layering: make each layer alone (transient, body, tail). Mix in the edit. Do not ask for a full mix in one prompt.
- Stable Audio 2.5: describe change over time ("grows into"). Raise guidance for literal results.

## 4. Voice
**Script**
- Write as spoken. Spell out numbers and units.
- Give the model context. Very short lines come out unstable. ElevenLabs suggests 250+ characters for v3.
- Split long scripts at paragraph breaks.
- Write in the target language. Do not ask the model to translate.

**Emotion and audio tags**
- ElevenLabs v4 / v4 Turbo / v3: square brackets, before the words: `[whispers]`, `[excited]`, `[sighs]`, `[laughs]`, `[rushed]`, `[British accent]`.
- A tag carries through the line. Add a new tag only when delivery changes.
- One tag per clause. Combine in one bracket: `[whispering, playful]`.
- Free-text tags work: `[like a tired night-shift nurse]`.
- Match tags to the voice. A shouting voice will not whisper well.
- MiniMax Speech 2.8: round brackets: `(laughs)`, `(sighs)`, `(breath)`, `(clear-throat)`. Only 2.8 models. Emotion is a parameter, not a tag.
- OpenAI gpt-4o-mini-tts: put direction in the `instructions` field (tone, accent, pace, whisper). Keep the script clean.

**Pauses**
- ElevenLabs v4/v3: `[pause]`, `[long pause]`, ellipses, dashes. No SSML break tags.
- ElevenLabs older models (Multilingual v2, Flash): `<break time="1.5s" />`, max 3 s.
- MiniMax: `<#0.6#>` between words. Range 0.01 to 99.99 s. Never two in a row.

**Pronunciation**
- ElevenLabs v4: IPA between slashes. Phoneme tags only on Flash v2 / Turbo v2 (English).
- MiniMax: `pronunciation_dict` -> `"tone": ["API/A P I", "lead/(liːd)"]`. Keep the left side narrow.
- Others: respell the word ("Nye-key").

**Voice choice**
- The voice matters more than the tags. Pick it first.
- Use library or neutral voices for finals. Pro voice clones are not tuned for v3.
- ElevenLabs stability: lower = expressive, higher = consistent.
- OpenAI: use `marin` or `cedar` for best quality. English-optimized.

## 5. Audio inside video models
- Veo 3.1: quote speech: `He says, "We open at nine."` Use `SFX:` and `Ambient noise:` labels. Clips are 4, 6 or 8 s.
- Kling 3.0: chain clauses with semicolons; speaker, delivery, then quoted line. Keep each line next to its speaker. 3 to 15 s. Languages: Chinese, English, Japanese, Korean, Spanish.
- Seedance 2.0: quote lines, 5 to 10 words each. Name sounds. Write "no music" if you mean it. Call for room tone or silence. 4 to 15 s.
- All: keep the speaking face in frame. Treat this audio as scratch. Replace music and key SFX in post.

## 6. Model table
| Model | Version (Oct 2026) | Limits | Syntax |
|---|---|---|---|
| Suno | v6, v6-wild, v6-mini (9 Sep 2026) | Style 1,000 chars; lyrics 5,000 | [Section: cue], Exclude field, sliders |
| ElevenLabs Music | music_v2_5 (11 Sep 2026) | 3 s to 5 min; ref ~30 s | composition plan; no artist names |
| Lyria 3 / 3 Pro | Google (Apr 2026) | 30 s / 3 min | [mm:ss] timestamps, `Lyrics:` |
| Stable Audio 2.5 | 2.5 | up to 190 s (API) | plain text; guidance 1 to 25 |
| Udio | v4 (Jul 2026) | no downloads | [Section] tags |
| ElevenLabs SFX | eleven_text_to_sound_v2 | 0.1 to 30 s | loop, prompt influence |
| ElevenLabs TTS | eleven_v4, v4_turbo; v3 previous | v4 10,000 chars; v3 5,000 | [tags], IPA, no SSML |
| MiniMax Speech | speech-2.8-hd / turbo | <10,000 chars | (tags), <#x#>, pronunciation_dict |
| OpenAI TTS | gpt-4o-mini-tts-2025-12-15 | not stated | `instructions` field |
| Veo | 3.1 / Fast / Lite | 4, 6, 8 s | quotes, SFX:, Ambient noise: |
| Kling | VIDEO 3.0 / 3.0 Omni | 3 to 15 s | semicolon clauses, quotes |
| Seedance | 2.0 | 4 to 15 s | quotes, "no music" |

## 7. Failures and fixes
- Generic track -> add subgenre, era, BPM, key, two named instruments.
- Unwanted vocals -> Suno Instrumental toggle; ElevenLabs "instrumental only".
- Excluded thing appears -> move it to the Exclude field. Do not write "no X" in Suno Style.
- Tags ignored -> cut to one cue per section. Fix the section's job, not the tag.
- Artist name error -> describe the sound; use the suggested rewrite.
- SFX mush -> split into one sound per prompt and layer in the edit.
- Tag spoken aloud -> move it next to its words or reword it as plain direction.
- Flat read -> change the voice first, then stability.
- Wrong pronunciation -> IPA or respelling; MiniMax dictionary.
- Video adds music -> "no music" plus room tone.
- Lip sync drift -> shorter lines, cut on each speaker, face in frame.

## 8. Templates
```text
MUSIC (Style / prompt)
[subgenre], [era] production, [mood 1], [mood 2], [BPM] BPM, [key],
lead [instrument], supporting [instrument], [vocals: type | instrumental only],
start with [element], bring in [element] at [time], [hit/drop] at [time],
end on [clean ending / ring-out] at [time]. Just [what stays]; no [what goes].

LYRICS BOX (Suno)
[Intro: solo piano, sparse]
[Verse 1: low, close vocal]
line / line
[Chorus: full drums, wide harmony]
line / line
[Outro: strip back]
[End]
```
```text
SFX
[source], [material], [action/sequence], [space], [perspective: close/distant],
[dry/reverb], [one-shot | seamless loop], [duration] s
```
```text
VOICE (ElevenLabs v4)
[warm, confident] Some days you just need... [pause] a little more light.
[softly] Brightline. [slowly] Made for mornings.

VOICE (MiniMax 2.8)
Some days you need more light.<#0.5#>(breath) Brightline.
```
```text
VIDEO WITH SOUND (Veo / Kling / Seedance)
[shot]. [character] says in a [tone] voice, "[5-10 words]."
SFX: [one named sound tied to action]. Ambient noise: [room tone]. No music.
```

## Sources (checked 2026-10-16)
- https://suno.com/blog/introducing-v6 - Suno v6 variants, 9 Sep 2026, plain-language edits.
- https://hookgenius.app/learn/suno-v6-guide/ - v6 style 1,000 / lyrics 5,000 chars, Exclude field, Style Influence, Variety.
- https://jackrighteous.com/blogs/guides-using-suno-ai-music-creation/why-your-suno-v6-meta-tags-arent-working - why v6 tags fail.
- https://alexanderweichart.de/2_Areas/Music/Suno-Instructions - brackets, Instrumental toggle.
- https://elevenlabs.io/docs/overview/capabilities/music/best-practices - Eleven Music prompting rules.
- https://elevenlabs.io/docs/overview/capabilities/music - 3 s to 5 min, music_v2_5, audio reference.
- https://elevenlabs.io/docs/eleven-api/guides/cookbooks/music - composition plans, bad_prompt on artist names.
- https://musicbusinessworldwide.com/elevenlabs-launched-music-v2-5-shortly-after-announcing-its-umg-licensing-deal - v2.5 date.
- https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-lyria-3-pro - Lyria 3 lengths, timestamps, Lyrics:.
- https://kb.stability.ai/knowledge-base/stable-audio-2.5-prompt-guide - Stable Audio prompt order, BPM ranges.
- https://fal.ai/models/fal-ai/stable-audio-25/text-to-audio/llms.txt - 190 s cap, guidance range.
- https://www.orcarouter.ai/blog/suno-v6-vs-udio - Udio v4, downloads off (Sep 2026).
- https://elevenlabs.io/docs/overview/capabilities/sound-effects - SFX 0.1-30 s, loop, prompt influence, terms.
- https://help.scenario.com/articles/3629745009-elevenlabs-sound-effects-sfx-the-essentials - SFX structure and failures.
- https://elevenlabs.io/docs/overview/models - eleven_v4, v3 previous gen, char limits, SFX model id.
- https://elevenlabs.io/blog/elevenlabs-audio-tags-list - v4 tag rules, pauses, 10,000 chars.
- https://elevenlabs.io/docs/best-practices/prompting - v3 tags, stability, 250+ chars, PVC caveat.
- https://elevenlabs.io/docs/help-center/technical/do-pauses-and-ssml-phoneme-tags-work-with-the-api - no break tags on v3/v4, 3 s max.
- https://morphic.com/resources/how-to/eleven-v4-guide - v4 no SSML, IPA, failures.
- https://platform.minimax.io/docs/api-reference/speech-t2a-http - Speech 2.8 tags, <#x#>, emotions, dictionary.
- https://minimax-ai.chat/docs/minimax-tts-pronunciation-subtitles/ - dictionary examples, pause rules.
- https://developers.openai.com/api/docs/guides/text-to-speech - instructions field, voices, marin/cedar.
- https://developers.openai.com/blog/updates-audio-models - gpt-4o-mini-tts-2025-12-15.
- https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1 - quotes, SFX:, Ambient noise:.
- https://ai.google.dev/gemini-api/docs/veo - Veo 3.1 variants, 4/6/8 s, audio always on.
- https://kling.ai/blog/kling-video-3-omni-native-lip-sync-audio-guide - Kling 3.0 dialogue syntax, languages.
- https://fal.ai/learn/tools/seedance-2-0-prompting-guide - Seedance 2.0 quotes, "no music".
- https://www.cutout.pro/learn/blog-seedance-2-0-audio-guide/ - Seedance line length, layer limits.
