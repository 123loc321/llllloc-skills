# Text prompts

## Contents
1. Settle first
2. Anatomy of a strong prompt
3. Reasoning and effort controls
4. Copy: taglines, ad copy, captions
5. Scripts and VO
6. Reusable system prompts
7. Prompts that write image or video prompts
8. Per-model differences
9. Common failures and fixes
10. Templates
11. Sources

## 1. Settle first
- Target model. Name it. Rules differ (see section 8).
- The job. One deliverable per prompt: taglines, a 30 s VO, a treatment, a summary.
- The reader. Client, agency, crew, viewer, or another AI.
- Length. Give a number: words, seconds, lines, characters.
- Tone. Describe concrete choices, not labels. "Short sentences, no puns, dry" beats "fun".
- Language. Name the output language and market. For translation, name the locale (fr-FR, pt-BR).
- Done. Say what a good result looks like before you write.

## 2. Anatomy of a strong prompt
Write it like a brief to a smart freelancer with zero context.
1. Role and context. Who the model is, who the client is, why the work exists.
2. Task. One clear verb: "Write", "Rewrite", "Summarise". Not "Can you suggest".
3. Inputs. Wrap each input in its own XML tag: `<brief>`, `<script>`, `<brand_voice>`, `<references>`.
4. Constraints. Length, must-include, must-avoid, legal lines.
5. Output format. Say exactly what comes back: a numbered list, a table, plain prose, JSON.
6. Examples. 3 to 5, varied, in `<example>` tags. Say they show style, not content to copy.
7. Success criteria. How you will judge it.

Rules:
- Give the reason behind each rule. Models generalise from the why.
- Say what to do, not only what to avoid.
- Long material goes first. The question and key constraints go last.
- Use one structure style per prompt: XML tags or Markdown headings. Do not mix.
- Match prompt style to output style. A Markdown-heavy prompt gets Markdown back.
- State each instruction once. Repeats cause over-reaction.
- No ALL CAPS, no "CRITICAL", no "MUST". Calm wording works better on current models.
- Ground the model. "Use only the brief below. If a fact is missing, write [TBC]."

## 3. Reasoning and effort controls
- Claude (API): adaptive thinking only on new models. Control depth with `effort` (low, medium, high, xhigh). Fable 5.1 default advice: `high`; `medium`/`low` for routine copy.
- GPT-6 (API): `reasoning.effort` = low, medium (default on Sol), high, xhigh, max. Astra and Sol do not accept `none`.
- Gemini 4 Argon: `thinking_level` = low, medium (default), high. Remove temperature, top_p, top_k; they are ignored.
- Grok 4.7: `reasoning.effort` = low, medium, high, xhigh. Default high. Set it on every call.
- In chat apps, pick the "thinking" or "pro" mode for treatments and strategy. Use the fast mode for captions and variants.
- Do not ask the model to show or transcribe its reasoning. Claude Fable 5 may refuse that. Ask for a short rationale per option instead.
- Use high effort for treatments, briefs and meta-prompts. Use low effort for lists of variants.

## 4. Copy: taglines, ad copy, captions
- Paste 3 to 5 real samples of the brand voice in `<voice_samples>`. Say "match rhythm and word choice, do not reuse lines".
- Give a banned-word list in `<banned>`: "elevate, unlock, seamless, game-changer, journey, delve". Also ban em dashes if you hate them.
- Ask for a number: "Give 12 taglines, max 6 words each."
- Ask for spread: "4 literal, 4 emotional, 4 provocative."
- Ask for a one-line rationale under each option. Then pick and iterate on the best two.
- Give the hard limits: characters per caption, safe-title line length, platform (IG, TikTok, cinema end card).
- For translation, say "adapt, do not translate word for word. Keep the pun or replace it with a local one, and flag it."

## 5. Scripts and VO
- Pace: about 2.3 words per second for a normal read (about 140 wpm).
- Word budgets: 6 s ≈ 12 words. 15 s ≈ 35. 30 s ≈ 65 to 70. 60 s ≈ 130 to 140.
- Write 10% under budget. Leave room for pauses, music and the logo.
- Tell the model the duration and the word cap. Ask it to print the word count per line.
- Ask for a two-column script: TIME | VO / SUPER / PICTURE.
- Ask for read notes: pace, pause marks `(beat)`, emphasis in caps only inside the script.
- For TTS, say "this will be read by a text-to-speech engine, so spell out numbers and avoid symbols".

## 6. Reusable system prompts
For a Custom GPT, a Claude Project, or a Gemini Gem.
- Open with role and purpose in two lines.
- Add studio context: who you are, clients, house style, delivery formats.
- Add default output rules: language, length, format, banned words.
- Add a "when unsure" rule: ask one question, or proceed and list assumptions. Pick one.
- Add priority: "The user's message overrides these defaults."
- Keep it short. Old, long, prescriptive prompts degrade newer models. Prune every few months.
- Attach long brand docs as files. Do not paste them into the instructions.
- Test with 5 real jobs before you share it.

## 7. Prompts that make an LLM write image or video prompts
- Name the target generator and its version. Each one wants different syntax.
- Paste that generator's rules or a good prompt example into `<target_rules>`.
- Give the shot info: subject, action, camera, lens, light, palette, duration, aspect ratio.
- Ask for exactly one prompt per shot, inside a code block, with no commentary.
- Ask for the length the target likes: short tags, or one dense paragraph.
- For video, ask for one camera move and one action per shot.
- Ask for a negative-prompt line only if the target supports it.
- Say "Describe only what is visible. No brand names or real people unless I provide them."

## 8. Per-model differences
| Model | Latest version (Oct 2026) | Responds to | Quirks |
|---|---|---|---|
| Claude | Fable 5.1 / Mythos 5.1; Opus 5.5, Sonnet 5.5, Haiku 5.5 | XML tags, context and reasons, short steering lines, examples in tags | Thinking always on in Fable 5.1. No prefill on 4.6+. Opus 5 runs long: ask for brevity. Older prescriptive prompts can hurt quality. |
| ChatGPT / GPT | GPT-6 Astra (top), GPT-6.1 Sol, GPT-6 Luna | Clear constraints, success criteria, concrete style rules | Astra leans to lists, tables, heavy Markdown and stock phrases. Ask for prose. Asks more clarifying questions; say "proceed". |
| Gemini | Gemini 4 Argon (`gemini-4-argon`) | Direct, concise prompts; one consistent structure; question placed after the data | Concise by default: ask for detail. Drops early constraints in long prompts: put key constraints last. Follows personas very strictly. Sampling settings ignored. |
| Grok | Grok 4.7 (`grok-4.7`) | Task, constraints and output format stated directly; static content first | Default effort high, so it can be slow. If you set sampling, use temperature 0.7, top_p 0.95. |

## 9. Common failures and fixes
| Failure | Fix |
|---|---|
| Generic, "AI" copy | Add voice samples and a banned-word list. Ask for spread across angles. |
| Too long | Give a word or second count. Say "lead with the answer". |
| Too short or flat (Gemini, GPT-6) | Ask for the detail you need: "include rationale and one risk". |
| Bullet soup | Say "write in short paragraphs; lists only for parallel items". |
| Invents facts or claims | "Use only `<brief>`. Mark unknowns [TBC]." |
| Ignores a rule | Move it to the end. Give the reason. Remove repeats and caps. |
| Copies the example | Give 3+ varied examples. Say they show style only. |
| VO overruns | Give the word cap and ask for a word count per line. |
| Persona hijacks the task | Keep the role to one line. Put the task after it. |
| Keeps asking questions | "If something is unclear, assume, list assumptions, and proceed." |

## 10. Templates

Copy options
```text
You are a senior copywriter for <client>, a <what they do>.
The work is for <campaign>, seen by <audience> on <platform>.

<brief>
[paste brief]
</brief>

<voice_samples>
[3-5 real lines from the brand]
</voice_samples>

<banned>
elevate, unlock, seamless, game-changer, journey, delve
</banned>

Write 12 taglines, max 6 words each: 4 literal, 4 emotional, 4 bold.
Match the rhythm of the voice samples. Do not reuse their lines.
Under each, add one line on why it works.
Output a numbered list. No intro, no outro.
```

VO script
```text
Write a <30>-second VO script for <client> <film>.
Read pace is about 2.3 words per second, so stay under <62> words.

<brief>
[paste brief]
</brief>

<picture>
[shot list or board notes]
</picture>

Format as a table: TIME | VO | SUPER | PICTURE.
Mark pauses as (beat). Show the total word count at the end.
Give 2 versions: one calm, one punchy.
Use only facts from the brief. Mark gaps as [TBC].
```

Meta-prompt for image or video prompts
```text
You write prompts for <generator and version>.

<target_rules>
[paste the generator's prompting rules or 2 good example prompts]
</target_rules>

<shots>
[one line per shot: subject, action, camera, lens, light, palette, duration, ratio]
</shots>

For each shot, write one prompt that follows <target_rules>.
Describe only what is visible. One camera move and one action per shot.
Return each prompt in its own code block, labelled with the shot number.
No commentary.
```

## Sources (checked 2026-10-16)
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices : Claude rules (explicitness, reasons, XML, 3-5 examples, long docs first, format, adaptive thinking/effort, prefill removed, Fable 5.1 quirks, model list).
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5.md : Fable 5 effort levels, short steering, readability, no reasoning echo, prune old prompts, give the reason.
- https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md : GPT-6 Astra / 6.1 Sol / Luna, effort values, no `none` on Astra/Sol, Markdown and stock-phrase tendency, clarifying questions.
- https://developers.openai.com/api/docs/guides/gpt-5.6 : writing-style prompt (paragraphs, lists only for parallel items, plain language), GPT-5.6 verbosity and concise defaults.
- https://ai.google.dev/gemini-api/docs/prompting-strategies : Gemini direct prompts, one structure style, question at the end, concise default, personas, sampling deprecated on Gemini 4 (updated 2026-10-13).
- https://ai.google.dev/gemini-api/docs/generate-content/latest-model : Gemini 4 Argon id, thinking_level low/medium/high, sampling params ignored (updated 2026-10-14).
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide : Gemini constraints last, strict personas, over-applied negatives, grounding.
- https://docs.x.ai : Grok 4.7 is latest.
- https://docs.x.ai/developers/models/grok-4.7 : Grok 4.7 effort levels low-xhigh, default high, 500K context.
- https://docs.x.ai/developers/model-capabilities/text/best-practices : Grok state task/constraints/format, static content first, temperature 0.7 / top_p 0.95, set effort per call (updated 2026-10-12).
- https://aicatchup.com/practices/prompting-gpt-6 : practitioner tips for GPT-6 (style, set effort, define done), 2026-10-09.
- https://voicebros.com/en/blog/how-to-write-a-commercial-voice-over-script : VO pace 2.3 words/s, 35/70/140 words for 15/30/60 s, write 10% under (2026-07-01).
