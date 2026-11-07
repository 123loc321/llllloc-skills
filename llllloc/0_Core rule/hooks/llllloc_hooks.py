#!/usr/bin/env python3
"""llllloc hooks (29 Oct 2026, his ok). One script, one mode per hook:

  delete-guard   PreToolUse   core rule 2: never delete. Blocks a delete outside a _DELETE folder,
                              asks inside one (clear archive) and before a cloud trash or purge.
  skills-guard   PreToolUse   never write a skill into ~/.claude/skills/ (it would show twice beside the llllloc plugin).
  git-pull       SessionStart  startup: pull GitHub main into the brain folder (GitHub is the master, 6 Nov 2026).
  core-rule      SessionStart  startup: print the core rule when the session folder is not the brain (a plugin
                              cannot carry CLAUDE.md, so job folders get the core rule this way, 6 Nov 2026).

Since 6 Nov 2026 these hooks ship inside the llllloc plugin (marketplace.json, entry hooks), so they run in
every folder on every Mac. A hook lives in the plugin or in a settings file, never both, or it fires twice.
  chmod-command  PostToolUse  a .command file Claude writes is made clickable (chmod +x).
  after-compact  SessionStart (compact) core rule 13 and the router, right after a session compacts.
  stop-check     Stop         a reply that loaded the router ends with the Loaded and Time lines (rule 9),
                              and a prompt turn shows its research, files new findings and has a Research line.
  research-guard PreToolUse   a prompt goes on a board only after a search or a research cache read this turn
                              (llllloc:task-prompt section 0, 31 Oct 2026, his ok).

Each mode reads the hook JSON on stdin. A broken hook must never block his work: errors exit 0.
"""
import json, os, re, shlex, stat, sys

HOME = os.path.expanduser("~")
TEMP_ROOTS = ("/tmp/", "/private/tmp/", "/private/var/folders/", "/var/folders/")
DELETE_WORDS = {"rm", "rmdir", "unlink", "srm", "trash"}
# claude.ai connectors (Drive, Gmail, Calendar, Magnific, Slack...) have id-like server names. Mac app tools
# (After Effects, Premiere, Illustrator...) are named servers: deleting a layer there is an edit, not a delete.
CLOUD_TRASH = re.compile(r"^mcp__[0-9a-f]{8}-[0-9a-f-]{27}__(trash_\w+|trash|delete_\w+|purge\w*|\w+_delete\w*|\w+_purge)$")
SKILLS_ROOT = os.path.join(HOME, ".claude", "skills")
COPY_WORDS = {"cp", "mv", "rsync", "ln", "ditto", "install"}
MAKE_WORDS = {"mkdir", "touch", "tee"}
PROMPT_TOOL = re.compile(r"__(spaces_create_node|spaces_patch_node|images_generate|video_generate|partner_generate)$")
PROMPT_FIELD = re.compile(r'"prompt":\s*"(?:[^"\\]|\\.){20}')  # layout-only patches carry no prompt text
PROMPT_BLOCK = re.compile(r"```text\n\S+_[vV]\d+")  # llllloc:task-prompt: a chat prompt's first line is its versioned name
WEB_TOOL = re.compile(r"WebSearch|WebFetch|web_search_exa|web_fetch_exa")
RESEARCH_FILES = ("5_Research cache", "2_Research")
# The brain working copy on this Mac: $LLLLLOC_BRAIN, else ~/llllloc (machine-owned copy, Phase 3),
# else ~/Desktop/Claude (the brain since 7 Nov 2026). Never a fixed user name (6 Nov 2026).
BRAIN_PLACES = ("~/llllloc", "~/Desktop/Claude")
CORE_RULE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Core Rule.md")


def brain_dir():
    places = [os.environ.get("LLLLLOC_BRAIN", "")] + [os.path.expanduser(p) for p in BRAIN_PLACES]
    for p in places:
        # a copy from the Drive template has no .git: the plugin list marks it as the brain (7 Nov 2026)
        if p and os.path.isfile(os.path.join(p, "AGENTS.md")) and os.path.isfile(os.path.join(p, ".claude-plugin", "marketplace.json")):
            return p
    return None


def out(obj):
    print(json.dumps(obj))


def pre(decision, reason):
    out({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision,
                                "permissionDecisionReason": reason}})


def strip_heredocs(command):
    """Drop heredoc bodies (file text, commit messages): words inside them are not commands."""
    return re.sub(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n.*?\n\s*\2\s*(?=\n|$)", " ", command, flags=re.S)


def segments(command):
    """The command split into simple commands, as word lists. Quoted text stays one word."""
    words = shlex.split(strip_heredocs(command), posix=True)
    segs, seg = [], []
    for w in words:
        if w in ("&&", "||", ";", "|"):
            segs.append(seg); seg = []
        else:
            seg.append(w)
    segs.append(seg)
    return [s for s in segs if s]


def delete_targets(command):
    """Paths after each delete word, or None when the command cannot be read safely."""
    try:
        segs = segments(command)
    except ValueError:
        return None
    targets = []
    for seg in segs:
        names = [os.path.basename(w) for w in seg]
        i = next((k for k, n in enumerate(names) if n in DELETE_WORDS and (k == 0 or names[k - 1] in ("sudo", "git", "command", "xargs"))), None)
        if i is not None:
            targets += [w for w in seg[i + 1:] if not w.startswith("-")]
    return targets


def finds_delete(command):
    try:
        segs = segments(command)
    except ValueError:
        return False
    for seg in segs:
        names = [os.path.basename(w) for w in seg]
        if names[0] == "find" and "-delete" in seg:
            return True
        if names[0] == "git" and len(seg) > 1 and seg[1] == "clean":
            return True
    return False


def is_temp(path):
    p = os.path.realpath(os.path.expanduser(path)) + "/"
    tmpdir = os.environ.get("TMPDIR", "")
    return p.startswith(TEMP_ROOTS) or (tmpdir and p.startswith(os.path.realpath(tmpdir) + "/"))


def delete_guard(data):
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    if tool == "Bash":
        command = inp.get("command", "")
        if finds_delete(command):
            return pre("deny", "Core rule 2: never delete. find -delete and git clean are blocked. Move the files into a _DELETE folder beside them.")
        targets = delete_targets(command)
        if targets == []:
            return
        if targets is None:
            return pre("deny", "Core rule 2: never delete. This delete could not be read safely. Move the files into a _DELETE folder beside them.")
        if any("$" in t or "*" in t or "`" in t for t in targets):
            return pre("deny", "Core rule 2: never delete. A delete with a variable or a wildcard is blocked: write the literal path, or move the files into a _DELETE folder.")
        if all(is_temp(t) for t in targets):
            return
        if all("/_DELETE" in os.path.expanduser(t) for t in targets):
            return pre("ask", "Core rule 2 exception: this deletes inside a _DELETE folder (clear archive). He confirms first.")
        return pre("deny", "Core rule 2: never delete. Move the file into a _DELETE folder beside it instead.")
    if CLOUD_TRASH.match(tool):
        return pre("ask", f"Core rule 2: {tool} trashes or deletes something online. He confirms first.")


def skills_guard(data):
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = os.path.realpath(os.path.expanduser(inp.get("file_path") or inp.get("notebook_path") or ""))
        if path.startswith(os.path.join(HOME, ".claude", "skills") + "/"):
            return pre("deny", "Never write a skill into ~/.claude/skills/: the same skill would show twice beside the llllloc plugin. Edit the master in llllloc/2_Skills, then commit and push (llllloc:task-skill-creator rule 2).")
    elif tool == "Bash":
        if any(in_skills(t) for t in write_targets(inp.get("command", ""))):
            return pre("deny", "Never write into ~/.claude/skills/: the same skill would show twice beside the llllloc plugin. Edit the master in llllloc/2_Skills, then commit and push (llllloc:task-skill-creator rule 2).")


def in_skills(path):
    p = os.path.realpath(os.path.expanduser(path.replace("$HOME", HOME)))
    return p == SKILLS_ROOT or p.startswith(SKILLS_ROOT + "/")


def write_targets(command):
    """Where a shell command writes: the destination of a copy or move, made folders and files, redirects."""
    try:
        words = shlex.split(command, posix=True)
    except ValueError:
        return [command]
    targets, seg = [], []
    for w in words + [";"]:
        if w in ("&&", "||", ";", "|"):
            args = [a for a in seg[1:] if not a.startswith("-")]
            name = os.path.basename(seg[0]) if seg else ""
            if name in COPY_WORDS and args:
                targets.append(args[-1])
            elif name in MAKE_WORDS:
                targets += args
            elif name == "unzip" and "-d" in seg:
                i = seg.index("-d")
                targets += seg[i + 1:i + 2]
            seg = []
        elif w in (">", ">>"):
            seg.append(w)
        else:
            if seg and seg[-1] in (">", ">>"):
                targets.append(w)
            seg.append(w)
    return targets


def chmod_command(data):
    path = (data.get("tool_input") or {}).get("file_path", "")
    if path.endswith(".command") and os.path.isfile(path):
        mode = os.stat(path).st_mode
        if not mode & stat.S_IXUSR:
            os.chmod(path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            out({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                        "additionalContext": f"{os.path.basename(path)} was made executable (chmod +x), so a double-click runs it."}})


def after_compact(data):
    print("This session was just compacted. Core rule 13: when the next message starts a new job, he is told to type end and start a new session. "
          "The next message routes through the llllloc router again before any job call (router STEP 3).")


def turn_entries(transcript):
    lines = []
    with open(transcript) as f:
        for line in f:
            try:
                lines.append(json.loads(line))
            except ValueError:
                pass
    start = 0
    for i, o in enumerate(lines):
        if o.get("type") == "user" and (o.get("origin") or {}).get("kind") == "human":
            start = i
    return lines[start:]


def assistant_blocks(entries):
    for o in entries:
        if o.get("type") == "assistant":
            yield from (b for b in (o.get("message") or {}).get("content") or [] if isinstance(b, dict))


def research_done(entries):
    """What this turn did: 'search' (web, Ego, a research helper), 'notes' (read the cache), 'filed' (appended to it)."""
    done = set()
    for b in assistant_blocks(entries):
        if b.get("type") != "tool_use":
            continue
        name, text = b.get("name", ""), json.dumps(b.get("input") or {})
        if WEB_TOOL.search(name) or (name == "Bash" and "ego-browser" in text) or (name == "Agent" and re.search("research", text, re.I)):
            done.add("search")
        if name in ("Read", "Grep", "Glob", "Bash") and any(f in text for f in RESEARCH_FILES):
            done.add("filed" if ">>" in text else "notes")
    return done


def is_prompt_tool(name, tool_input):
    return bool(PROMPT_TOOL.search(name) and PROMPT_FIELD.search(json.dumps(tool_input or {})))


def research_guard(data):
    if not is_prompt_tool(data.get("tool_name", ""), data.get("tool_input")):
        return
    path = data.get("transcript_path", "")
    if not path or not os.path.isfile(path) or research_done(turn_entries(path)) & {"search", "notes"}:
        return
    pre("deny", "llllloc:task-prompt section 0: no research this turn. Read the model's file in 5_Research cache/platforms, name the new question, "
                "search it when the cache has no line, file any new finding, then send this prompt again.")


def prompt_problems(entries, last_text):
    """Why a prompt turn cannot end yet. Empty when the turn made no prompt."""
    # shortcut: a prompt inside a subagent or a Comfy API file is not seen, a turn-level check would need the file's contents.
    made = False
    for b in assistant_blocks(entries):
        if b.get("type") == "text" and PROMPT_BLOCK.search(b.get("text", "")):
            made = True
        if b.get("type") == "tool_use":
            inp = b.get("input") or {}
            made = made or is_prompt_tool(b.get("name", ""), inp) or (b.get("name") == "Write" and "5_Prompts/" in inp.get("file_path", ""))
    if not made:
        return []
    done, problems = research_done(entries), []
    if not done & {"search", "notes"}:
        problems.append("llllloc:task-prompt section 0: this turn wrote a prompt with no search and no research cache read. Do the research now and fix the prompt if it changes it.")
    if "search" in done and "filed" not in done:
        problems.append("llllloc:task-research FILE THE FINDING: a search ran but no line went into the research cache. Append it now, unless the search changed nothing.")
    if "**Research:**" not in last_text:
        problems.append("llllloc:task-prompt section 0: the prompt reply has no **Research:** line. Add it from this turn's tool calls.")
    return problems


def stop_check(data):
    if data.get("stop_hook_active"):
        return
    path = data.get("transcript_path", "")
    if not path or not os.path.isfile(path):
        return
    entries = turn_entries(path)
    routed, last_text = False, ""
    for b in assistant_blocks(entries):
        if b.get("type") == "tool_use" and b.get("name") == "Skill" and "llllloc" in str((b.get("input") or {}).get("skill", "")):
            routed = True
        if b.get("type") == "text" and b.get("text", "").strip():
            last_text = b["text"]
    problems = prompt_problems(entries, last_text)
    if routed and last_text and not ("**Loaded:**" in last_text and "**Time:**" in last_text):
        problems.append("Core rule 9: this job reply loaded the llllloc router but does not end with the **Loaded:** and **Time:** lines of router STEP 4. Add them now.")
    if problems:
        out({"decision": "block", "reason": " ".join(problems)})


def git_pull(data):
    """SessionStart (startup): GitHub is the master (6 Nov 2026), so the brain folder takes the newest commits first."""
    import subprocess
    brain = brain_dir()
    if not brain:
        print("llllloc: no brain folder on this Mac yet. Put the Claude folder on the Desktop (download it from the Drive link), "
              "open that folder in the Code tab, and Claude sets it up from its SETUP.md.")
        return
    try:  # first session on a new Mac: the memory setting of this folder is missing (7 Nov 2026)
        amd = json.load(open(os.path.join(brain, ".claude", "settings.local.json"))).get("autoMemoryDirectory", "")
    except (OSError, ValueError):
        amd = ""
    if os.path.realpath(os.path.expanduser(amd)) != os.path.realpath(os.path.join(brain, "llllloc", "9_Memory")):
        print("llllloc: this Mac is not set up for this brain folder yet. Before the job, say so in one line and follow SETUP.md.")
    if not os.path.isdir(os.path.join(brain, ".git")):
        print("llllloc: local copy with no GitHub link, nothing to pull. The skills come from the llllloc plugin that "
              "SETUP.md turned on: the shared GitHub repo 123loc321/llllloc-skills (auto-update), or this folder.")
        return
    def git(*a):
        return subprocess.run(["git", "-C", brain, *a], capture_output=True, text=True, timeout=15)
    before = git("rev-parse", "HEAD").stdout.strip()
    r = git("pull", "--ff-only", "-q", "origin", "main")
    if r.returncode != 0:
        print("GitHub sync: the pull failed, so this session works from the Mac copy. Tell him in one line, and fix it at `end` "
              f"(llllloc:end pushes). Git said: {(r.stderr or r.stdout).strip()[:200]}")
        return
    after = git("rev-parse", "HEAD").stdout.strip()
    n = git("rev-list", "--count", f"{before}..{after}").stdout.strip() if before != after else "0"
    print(f"GitHub sync: the brain folder is up to date with GitHub ({n} new commits pulled).")


def core_rule(data):
    """SessionStart (startup): the brain folder loads the core rule through CLAUDE.md, every other folder gets it here."""
    brain = brain_dir()
    cwd = os.path.realpath(data.get("cwd") or os.getcwd())
    if brain and (cwd + "/").startswith(os.path.realpath(brain) + "/"):
        return
    with open(CORE_RULE, encoding="utf-8") as f:
        text = f.read()
    print("llllloc core rule (printed by the llllloc plugin, because this folder is not the brain folder):\n\n" + text[:9000])


MODES = {"delete-guard": delete_guard, "skills-guard": skills_guard, "chmod-command": chmod_command,
         "after-compact": after_compact, "stop-check": stop_check, "research-guard": research_guard,
         "git-pull": git_pull, "core-rule": core_rule}

if __name__ == "__main__":
    try:
        raw = sys.stdin.read()
        MODES[sys.argv[1]](json.loads(raw) if raw.strip() else {})
    except Exception as e:  # a broken hook must never block his work
        print(f"llllloc hook error: {e}", file=sys.stderr)
