#!/usr/bin/env python3
"""impeccable hook for llllloc on his Mac (24 Oct 2026, Mac version 29 Oct 2026).

PostToolUse. Web file saved: run the impeccable detector on it.
Figma or app render/export: add a review reminder (no code to scan there).
Prints hookSpecificOutput.additionalContext, or nothing when there is nothing to say.
"""
import glob, json, os, re, subprocess, sys, time

WEB = (".html", ".htm", ".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".vue", ".svelte", ".astro")
# Each family: tool name pattern, then the reminder (29 Oct 2026, his words: video apps only for the graphic
# design elements inside the working file, not the footage or the grade).
CHECK = "Before the next step, look at it (a screenshot, snapshot or frame) and check it against the bans in {floor} (glow, gradient text, weak contrast, generic AI look). Note the findings in the reply."
FAMILIES = [
    ("figma", re.compile(r"^mcp__(?!ccd_).+__(use_figma|send_code_to_figma|create_new_file)$"),
     "impeccable check due for this Figma edit. Before handoff: get_design_context on the changed frame, save its code to a scratch .tsx file "
     "(saving it triggers the detector), fix what it finds, then compare get_screenshot against {floor}."),
    ("illustrator", re.compile(r"^mcp__Design_Bridge_by_IE3__(create_\w+|modify_object|apply_\w+|place_\w+|replace_color|convert_to_outlines"
                               r"|import_svg_as_editable|align_objects|manage_swatches|resize_for_variation|export\w*)$"),
     "impeccable check due for this Illustrator edit. " + CHECK),
    ("cavalry", re.compile(r"^mcp__Cavalry_by_Canva__execute_script$"),
     "impeccable check due for this Cavalry scene. Snapshot the changed layers. " + CHECK),
    ("video_graphics", re.compile(
        r"^mcp__(ae-mcp__(add_(text|typewriter|timer|word_highlight|captions|lower_third|shape|layer_style|animated_chart|progress_bar"
        r"|callout|ticker|count_up|extruded_text|animated_gradient|repeater)\w*|set_(text|shape|gradient|layer_style)\w*|create_kinetic_text)"
        r"|MCP_for_Adobe_Premiere_Pro__(add_text_overlay|add_title|import_mogrt\w*|apply_mogrt\w*|create_mogrt\w*|create_caption_track)"
        r"|davinci-resolve__(fusion_comp|timeline_item_fusion|fuse_plugin)"
        r"|MOTION__(motion_layer_add|motion_layer_set|motion_content_set))$"),
     "impeccable check due for the graphic design elements in this video file: text, titles, lower thirds, captions, shapes, logos, "
     "layout and safe margins. Not the footage or the grade. Grab one frame where they show. " + CHECK),
    ("visual", re.compile(r"^mcp__(?!ccd_).+__(images_(generate|variations|restyle|relight|reimagine|expand|upscale|retouch|change_camera)"
                          r"|video_(generate|modify|relight))$"),
     "impeccable review due: {tool} produced a visual. " + CHECK),
]
REMIND_EVERY = 600  # shortcut: one reminder per tool family per 10 min, so a 20-call Figma build is not flooded
STATE = "/tmp/impeccable_hook_state.json"


def say(text):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": text}}))


def skill_dir():
    # 6 Nov 2026: impeccable is copied daily from pbakaus/impeccable into the brain (Outside skills).
    # Found from this file, so it works in the plugin cache and on any Mac: .../llllloc/1_Core rule/hooks/impeccable/
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "2_Skills", "Outside skills", "impeccable")
    if os.path.isfile(os.path.join(here, "scripts", "impeccable")):
        return here
    found = glob.glob(os.path.expanduser("~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills/impeccable/scripts/impeccable"))
    found.sort(key=os.path.getmtime, reverse=True)
    return os.path.dirname(os.path.dirname(found[0])) if found else None


def due(family):
    try:
        state = json.load(open(STATE))
    except (OSError, ValueError):
        state = {}
    if time.time() - state.get(family, 0) < REMIND_EVERY:
        return False
    state[family] = time.time()
    json.dump(state, open(STATE, "w"))
    return True


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    skill = skill_dir()
    if not skill:
        if due("missing"):
            say("impeccable files missing: the impeccable hook found no installed impeccable skill. Design rule 14 says to report this in the reply.")
        return
    floor = f"{skill}/reference/craft-floor.md"

    if tool in ("Write", "Edit", "MultiEdit"):
        path = (data.get("tool_input") or {}).get("file_path", "")
        if not path.lower().endswith(WEB) or not os.path.isfile(path):
            return
        try:
            out = subprocess.run(["sh", f"{skill}/scripts/impeccable", "detect", "--json", path],
                                 capture_output=True, text=True, timeout=60, cwd=data.get("cwd") or None)
        except subprocess.TimeoutExpired:
            say(f"impeccable detector timed out on {path}. Run it once by hand before handoff.")
            return
        try:
            findings = json.loads(out.stdout or "[]")
        except ValueError:
            say(f"impeccable detector output was not readable for {path}: {(out.stderr or out.stdout)[:300]}")
            return
        if not findings:
            return
        lines = [f"- [{f.get('antipattern') or f.get('id') or f.get('rule')}] {f.get('snippet') or f.get('description') or ''}"[:220]
                 for f in findings[:15]]
        say(f"impeccable detector: {len(findings)} finding(s) in {path}. Each needs a fix, or a stated reason when the brief or the DesignSystem file wins (design rule 14.5):\n"
            + "\n".join(lines))
    else:
        for family, pattern, text in FAMILIES:
            if pattern.match(tool):
                if due(family):
                    say(text.format(floor=floor, tool=tool))
                return

if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # a broken hook must never block his work
        print(f"impeccable hook error: {e}", file=sys.stderr)
