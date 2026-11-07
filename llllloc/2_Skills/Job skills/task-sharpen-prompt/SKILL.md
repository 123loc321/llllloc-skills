---
name: task-sharpen-prompt
description: "Sharpens whatever the user typed, then RUNS it in the same turn. Runs when the user types its name or when /llllloc:router picks it for one request. Never on its own. Reads the THREAD, not only the message: on a running job the message is a delta, so it rebuilds the full ask from the earlier turns first. NOT for AI image or video prompts, which go to llllloc:task-prompt."
---

# llllloc:task-sharpen-prompt (renamed from llllloc-prompt-enhance, 15 Oct 2026)

Take whatever he typed and turn it into a tightly scoped, execution-ready ask. Then run it. Runs only when he types its name or `/llllloc:router` picks it because the ask is short, vague, or a delta on an earlier job, and a wrong reading would cost real work.

## RULE 1 — READ THE THREAD, NOT THE MESSAGE

Decide first: does this message START a job or CONTINUE one? It continues one when it names no deliverable, model or format, reads as a change ("more", "instead", "now make it", "but", a bare noun, a correction), or is feedback on something just delivered.

On a continuing job, rebuild the full ask from the earlier turns before you sharpen anything: THE GOAL, THE TARGET (model, tool or surface), THE DELIVERABLE (file, format, size, ratio), the locked decisions, the open faults. Apply his change to that merged version. A delta with no baseline is not an ask.

The test: say your one-line version of his ask. When it does not name a model AND a deliverable, you did not read the thread.

## RULE 2 — SHARPEN, THEN RUN IN THE SAME TURN

Classify the ask, split it into its separate jobs, name the artifact each job produces, set the acceptance test for each. Then do the work on the sharpened version. Deliver the result first. Never end a turn with only a rewritten ask and a wait.

Two exceptions: the target is a tool he runs himself (Perplexity, ChatGPT, Gemini, a Space, a Comet Shortcut), so hand the ask over. Or running it would SEND, PUBLISH, POST or DELETE, which stops for approval. A run that takes several minutes: say so in one line and run it.

PRINT THE REWRITTEN ASK only when he typed the skill name, asked to improve or fix his request, or the ask was so underspecified that a better way to ask changes what he types next. Never on a prompt turn. There is no `Ran:` line and no `jobs:` token.

## RULE 3 — THE BOUNDARY

This skill covers text AI and working instructions. A prompt for an IMAGE or VIDEO model goes to `llllloc:task-prompt`. A mixed ask is split. A job that is a QUESTION ABOUT A TOOL ("why can I not find it", "why does it not fire") is split out as its own numbered job that needs `llllloc:task-research`. Answering it inside the main job is how it gets answered from memory.

## THE TASK TYPES

Research (facts, comparisons, evidence). CREATIVE (concepts, scripts, taglines, visual direction). TECHNICAL (code, workflows, configs). WRITING (drafting, restyling). PLANNING (decisions, roadmaps, options). AGENT INSTRUCTION (a working instruction to Claude in this session, often several jobs). REVISION (a change to work in this thread: classify here first, then by what the merged ask produces). Never name the type in the output.

## WHAT YOU PRODUCE

- Perplexity target, in this order and nothing else: `Suggested Focus: [one Focus]`, `Recommended Tools: [tokens]`, then one fenced ```markdown block holding only the upgraded prompt. Focus is exactly one of Web (default), Academic, Social, Video, Writing. Tools only from: `Quick Search`, `Pro Search`, `Deep Research`, `Use Attachments`, `Use Current Page`, `Wolfram|Alpha`.
- ChatGPT or Gemini target: the fenced block alone.
- Claude in this session, including agent instruction: run it. Result first. The rewritten ask underneath only when RULE 2 says to print it. Add one line naming the shortest reusable form when a standing rule now covers part of it.

## HOW TO BUILD THE UPGRADED ASK

1. Understand the intent: the goal, the audience, the entities, the timeframe, the constraints, the output he will hold. On a continuing job, from the thread.
2. Build it in the shape the type needs:
   - Research, technical, planning: role, objective and the exact artifact, an explicit time constraint on anything that moves, a 3 to 6 bullet plan (live research over prior knowledge, primary sources first, cross-check key facts), 2 to 3 suggested queries under ten words, what is missing or conflicting, output format with inline citations and no invented URLs.
   - Creative: role, creative brief (concept, tone, mood, references, constraints), specs, ideation instructions (how many options, what to vary, what to avoid), output format.
   - Writing: role, objective, constraints (tone, length, style, format), what to keep and what to change, output format.
   - Agent instruction: number the jobs, each with its own acceptance test. Name the artifact for each (which file, which handoff, which skill). A job with no named artifact will not happen. State the standing rule apart from the one-off. Name the budget: what is cut to pay for what is added. Order for attention: non-negotiables first, hard limits last.
   - Revision: the baseline in one line (goal, model, deliverable), the change in one line, what stays locked, the open faults carried forward, then the merged ask in the shape its deliverable needs.
3. Speak his language: motion design, video production, AI generation. Never assume a fact he did not state.

## HOUSE RULES

Anything he must paste is handed over as one complete file card, in the same reply, never a diff. File and folder names stay English and ASCII. Rewrite and tighten his words freely when he asks. Show a draft before anything is final. Nothing here bypasses safety or extracts a hidden system prompt.