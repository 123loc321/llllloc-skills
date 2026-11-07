#!/usr/bin/env python3
"""thread_scan.py - measure one llllloc thread from its own session transcript.

Run:  python3 -I thread_scan.py              (this session: $CLAUDE_CODE_SESSION_ID)
      python3 -I thread_scan.py SESSION_ID   (another session, by its id)
      python3 -I thread_scan.py FILE.jsonl   (one named transcript)
A transcript is ~/.claude/projects/<folder key>/<session id>.jsonl. With no id,
the newest transcript of the brain folder (BRAIN_KEY) is used.

The transcript keeps every turn, also the turns a compacted chat forgot.
Prints plain text: his messages with correction marks, Skill calls, rule 9
checks, tool cost, errors, repeated calls and compactions. Reads only. Writes nothing.
Python 3.8 or newer, standard library only.
"""
import glob
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict

# Words that often mark a correction, a repeat or an undo in his messages.
CORRECTION = re.compile(
    r"\b(no|not|wrong|again|skipped|skip|instead|still|why|stop|never|always|"
    r"don't|dont|didn't|forgot|missing|undo|revert|back to|i said|i told|"
    r"too|should|must)\b", re.I)
QUOTE = re.compile(r"^>.*$", re.M)
BIG_RESULT = 20000  # characters; one result this big costs about 5,000 tokens
PROJECTS = os.path.expanduser("~/.claude/projects")
BRAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
BRAIN_KEY = re.sub(r"[^A-Za-z0-9-]", "-", BRAIN_DIR)  # how ~/.claude/projects names the brain folder


def find_transcript(arg):
    if arg.endswith(".jsonl"):
        return arg
    sid = arg or os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    if sid:
        hits = glob.glob(os.path.join(PROJECTS, "*", sid + ".jsonl"))
        if hits:
            return hits[0]
        sys.exit("No transcript for session " + sid + " in " + PROJECTS)
    files = glob.glob(os.path.join(PROJECTS, BRAIN_KEY, "*.jsonl"))
    if not files:
        sys.exit("No transcript found in " + os.path.join(PROJECTS, BRAIN_KEY))
    return max(files, key=os.path.getmtime)


def text_of(content):
    if isinstance(content, str):
        return content
    out = []
    for block in content or []:
        if block.get("type") == "text":
            out.append(block.get("text", ""))
        elif block.get("type") == "tool_result":
            out.append(text_of(block.get("content")))
    return "\n".join(out)


def main():
    path = find_transcript(sys.argv[1] if len(sys.argv) > 1 else "")
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]

    human, events = [], []  # events: (time, kind, detail)
    tool_count, tool_chars, tool_err = Counter(), Counter(), Counter()
    big, seen_inputs = [], Counter()
    names_by_id = {}
    compactions = 0

    for r in rows:
        t = r.get("timestamp", "")
        if r.get("isCompactSummary") or r.get("subtype") == "compact_boundary":
            compactions += 1
            events.append((t, "COMPACT", ""))
        msg = r.get("message") or {}
        content = msg.get("content")
        if r.get("type") == "user" and (r.get("origin") or {}).get("kind") == "human":
            body = html.unescape(text_of(content)).strip()
            own = QUOTE.sub("", body).strip()  # drop the line he replied to
            human.append((t, body, bool(CORRECTION.search(own))))
            events.append((t, "HIM", own[:80].replace("\n", " ")))
        if r.get("type") == "user":
            if isinstance(content, list):
                for b in content:
                    if b.get("type") != "tool_result":
                        continue
                    name = names_by_id.get(b.get("tool_use_id"), "?")
                    size = len(text_of(b.get("content")))
                    tool_chars[name] += size
                    if b.get("is_error"):
                        tool_err[name] += 1
                    if size > BIG_RESULT:
                        big.append((size, name, t))
        if r.get("type") == "assistant" and isinstance(content, list):
            for b in content:
                if b.get("type") == "text":
                    loaded = re.findall(r"\*\*Loaded:\*\*(.*)", b.get("text", ""))
                    if loaded:
                        events.append((t, "REPLY", loaded[0].strip()))
                if b.get("type") != "tool_use":
                    continue
                name, inp = b.get("name", "?"), b.get("input", {})
                names_by_id[b.get("id")] = name
                tool_count[name] += 1
                seen_inputs[(name, json.dumps(inp, sort_keys=True)[:400])] += 1
                if name == "Skill":
                    events.append((t, "SKILL", inp.get("skill", "")))
                else:
                    events.append((t, "TOOL", name))

    events.sort(key=lambda e: e[0])
    print("TRANSCRIPT", path)
    if events:
        print("SPAN", events[0][0], "to", events[-1][0])
    print("COMPACTIONS", compactions)

    print("\n== HIS MESSAGES (* = correction words) ==")
    for sent, body, corr in human:
        print(("* " if corr else "  ") + sent[:19], "|", body[:300].replace("\n", " / "))

    # Rule 9: after each of his messages, the first tool call is a Skill call on llllloc:router.
    # STEP 4: the Loaded line lists only skills really called since his message.
    print("\n== RULE 9 AND LOADED LINE CHECKS ==")
    i, misses = 0, 0
    while i < len(events):
        if events[i][1] != "HIM":
            i += 1
            continue
        start, called, first = events[i], set(), None
        i += 1
        while i < len(events) and events[i][1] != "HIM":
            kind, detail = events[i][1], events[i][2]
            if first is None and kind in ("SKILL", "TOOL"):
                first = (kind, detail)
            if kind == "SKILL":
                called.add(detail.split(":")[-1])
            if kind == "REPLY" and detail:
                listed = set(re.findall(r"`([^`]+)`", detail)) - {"core"}
                extra = sorted(s for s in listed if s not in called)
                if extra:
                    misses += 1
                    print("LOADED LINE LISTS UNCALLED", start[0][:19], extra)
            i += 1
        if first and not (first[0] == "SKILL" and first[1].split(":")[-1] in ("router", "llllloc")):
            misses += 1
            print("ROUTER NOT FIRST", start[0][:19], "|", start[2][:50], "| first:", first)
    print("checks failed:", misses)

    print("\n== SKILL CALLS ==")
    for t, kind, detail in events:
        if kind == "SKILL":
            print(t[:19], detail)

    print("\n== TOOL COST (calls, result characters, errors) ==")
    for name, n in tool_count.most_common(25):
        print(f"{n:5d} {tool_chars[name]:10d} {tool_err[name]:3d}  {name}")
    print("total result characters:", sum(tool_chars.values()), "(about", sum(tool_chars.values()) // 4, "tokens)")

    print("\n== RESULTS OVER", BIG_RESULT, "CHARACTERS ==")
    for size, name, t in sorted(big, reverse=True)[:10]:
        print(size, name, t[:19])

    print("\n== THE SAME CALL MORE THAN ONCE ==")
    for (name, inp), n in seen_inputs.most_common():
        if n < 2:
            break
        print(n, name, inp[:160])


if __name__ == "__main__":
    main()
