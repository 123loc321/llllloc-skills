#!/usr/bin/env python3
"""Self-check for the research hooks. Runs the real hook script on made-up turns. Run: python3 -I -B test_research_check.py"""
import json, os, subprocess, sys, tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llllloc_hooks.py")
NODE = "mcp__e7915470-c988-4f55-9686-d2057987716a__spaces_patch_node"
PROMPT = {"patches": [{"patch": {"data": {"prompt": "FORMAT: vertical 9:16 photo, real family video still."}}}]}
HUMAN = {"type": "user", "origin": {"kind": "human"}, "message": {"content": "go"}}


def tool(name, **inp):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": inp}]}}


def text(t):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": t}]}}


def run(mode, lines, **payload):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl") as f:
        f.write("\n".join(json.dumps(x) for x in lines))
        f.flush()
        payload["transcript_path"] = f.name
        r = subprocess.run([sys.executable, "-I", "-B", HOOK, mode], input=json.dumps(payload), capture_output=True, text=True)
    assert not r.stderr, r.stderr
    return r.stdout


CACHE = tool("Read", file_path="/x/5_Research cache/platforms/nano-banana.md")
SEARCH = tool("WebSearch", query="Nano Banana shirt texture prompt")
FILED = tool("Bash", command='printf "line" >> "/x/5_Research cache/platforms/nano-banana.md"')
DONE = text("Board built.\n\n**Research:** saved notes, NB2.1 texture\n\n**Loaded:** `core`\n\n**Time:** `1 min 0 s`")

# research-guard
g = lambda *turn, inp=PROMPT, name=NODE: run("research-guard", [HUMAN, *turn], tool_name=name, tool_input=inp)
assert "deny" in g(), "a prompt with no research is refused"
assert g(CACHE) == "", "a cache read passes"
assert g(SEARCH) == "", "a search passes"
assert g(inp={"patches": [{"patch": {"layout": {"x": 1}}}]}) == "", "a layout patch passes"
assert "deny" in run("research-guard", [SEARCH, HUMAN], tool_name=NODE, tool_input=PROMPT), "last turn's search does not count"

# stop-check
s = lambda *turn: run("stop-check", [HUMAN, *turn])
assert s(text("Plain answer.")) == "", "no prompt, nothing to check"
assert "no search and no research cache read" in s(text("```text\nTB-SH_Baby-Sheet_NB21_v2\n\nprompt\n```\n\n**Research:** x"))
assert s(text("```text\nsome log output\n```")) == "", "a plain code block is no prompt"
assert "no **Research:** line" in s(CACHE, tool(NODE, **PROMPT), text("Built."))
assert "FILE THE FINDING" in s(SEARCH, tool(NODE, **PROMPT), DONE)
assert s(SEARCH, FILED, tool(NODE, **PROMPT), DONE) == "", "a clean search turn passes"
assert s(CACHE, tool(NODE, **PROMPT), DONE) == "", "a clean cache turn passes"
assert "section 0" in s(tool("Write", file_path="/job/5_Prompts/A_V1.html"), text("Deck."))
assert "Core rule 9" in s(tool("Skill", skill="llllloc"), text("No lines.")), "the Loaded check still works"
assert run("stop-check", [HUMAN, tool(NODE, **PROMPT)], stop_hook_active=True) == "", "blocks once only"
print("all research hook checks passed")
