"""brain_check.py: proves the llllloc brain is whole (6 Nov 2026). Runs at every `end` (llllloc:end STEP 6).

  python3 -I "<brain folder>/llllloc/0_Core rule/brain_check.py"

Prints PASS, WARN, FAIL or FIXED lines. Exit code 1 when any FAIL is left.
The one thing it fixes by itself: the core rule copy inside AGENTS.md.
"""
import json, os, re, subprocess, sys

BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # any Mac, any user name
SKILLS = os.path.join(BRAIN, "llllloc/2_Skills")
MEMORY = os.path.join(BRAIN, "llllloc/9_Memory")
SKIP = {"Old", "_DELETE", "OLD VERSIONS", "Old versions", "node_modules", ".git", "worktrees"}
fails = 0


def say(kind, msg):
    global fails
    fails += kind == "FAIL"
    print(f"{kind:5} {msg}")


def git(*a):
    return subprocess.run(["git", "-C", BRAIN, *a], capture_output=True, text=True).stdout.strip()


# 1. Skills: folder name = frontmatter name = plugin line = .agents link.
folders = {}
for g in sorted(os.listdir(SKILLS)):
    gd = os.path.join(SKILLS, g)
    if not os.path.isdir(gd) or g in SKIP:
        continue
    for n in sorted(os.listdir(gd)):
        if os.path.isfile(os.path.join(gd, n, "SKILL.md")):
            folders[n] = g
bad = []
for n, g in folders.items():
    head = open(os.path.join(SKILLS, g, n, "SKILL.md"), encoding="utf-8").read(3000)
    m = re.search(r"(?m)^name:\s*\"?([^\"\n]+?)\"?\s*$", head)
    if not m or m.group(1) != n:
        bad.append(f"{n} (name: {m.group(1) if m else 'missing'})")
    if n.startswith("llllloc-") or n == "llllloc":
        bad.append(f"{n} (old name)")
say("FAIL" if bad else "PASS", f"{len(folders)} skills, folder and name match" + (": " + ", ".join(bad) if bad else ""))

mp = json.load(open(os.path.join(BRAIN, ".claude-plugin/marketplace.json")))
listed = {os.path.basename(p.rstrip("/")) for p in mp["plugins"][0].get("skills", [])}
missing, extra = sorted(set(folders) - listed), sorted(listed - set(folders))
say("FAIL" if missing or extra else "PASS", f"plugin lists {len(listed)} skills"
    + (f", missing {missing}" if missing else "") + (f", no folder for {extra}" if extra else ""))

ag = os.path.join(BRAIN, ".agents/skills")
links = set(os.listdir(ag)) if os.path.isdir(ag) else set()  # a copy from Drive has no links until setup_mac.py runs
broken = sorted(l for l in links if not os.path.isfile(os.path.join(ag, l, "SKILL.md")))
nolink = sorted(set(folders) - links)
say("FAIL" if broken or nolink else "PASS", f".agents/skills has {len(links)} links"
    + (f", broken {broken}" if broken else "") + (f", missing {len(nolink)}: run setup_mac.py" if nolink else ""))

dead = []
for g in {g for g in folders.values()}:
    for n in [n for n, gg in folders.items() if gg == g]:
        for dp, dn, fn in os.walk(os.path.join(SKILLS, g, n)):
            dn[:] = [d for d in dn if d not in SKIP]
            for f in fn:
                if f.endswith(".md"):
                    text = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
                    for rel in set(re.findall(r"(?<![\w.])((?:\.\./)+[\w./-]+\.\w+)", text)):
                        if not os.path.exists(os.path.normpath(os.path.join(dp, rel))):
                            dead.append(f"{n}/{os.path.relpath(os.path.join(dp, f), os.path.join(SKILLS, g, n))}: {rel}")
say("WARN" if dead else "PASS", f"links that leave a skill folder: {len(dead)} dead" + "".join(f"\n      {x}" for x in dead[:8]))

# 2. AGENTS.md carries the core rule word for word (other AIs never follow @ imports).
core = open(os.path.join(BRAIN, "llllloc/0_Core rule/Core Rule.md"), encoding="utf-8").read().strip()
ap = os.path.join(BRAIN, "AGENTS.md")
agents = open(ap, encoding="utf-8").read()
m = re.search(r"(<!-- CORE RULE COPY START[^\n]*-->\n)(.*?)(\n<!-- CORE RULE COPY END -->)", agents, re.S)
if not m:
    say("FAIL", "AGENTS.md has no core rule copy markers")
elif m.group(2).strip() == core:
    say("PASS", "AGENTS.md core rule copy matches Core Rule.md")
else:
    open(ap, "w", encoding="utf-8").write(agents[:m.start(2)] + core + agents[m.end(2):])
    say("FIXED", "AGENTS.md core rule copy updated from Core Rule.md")
size = len(open(ap, "rb").read()) + len(open(os.path.join(BRAIN, "CLAUDE.md"), "rb").read())
say("WARN" if size > 28000 else "PASS", f"AGENTS.md + CLAUDE.md = {size:,} bytes (Codex reads 32 KiB)")
if open(os.path.join(BRAIN, "CLAUDE.md")).read().strip() != "@AGENTS.md":
    say("WARN", "CLAUDE.md should hold only @AGENTS.md, or Claude reads the core rule twice")

# 3. Memory: inside the brain, under the load limit, every index link real, no keys.
idx = os.path.join(MEMORY, "MEMORY.md")
if not os.path.isfile(idx):
    say("FAIL", "llllloc/9_Memory/MEMORY.md is missing")
else:
    raw = open(idx, "rb").read()
    lines, kb = raw.count(b"\n") + 1, len(raw)
    kind = "FAIL" if lines > 200 or kb > 25000 else "WARN" if lines > 180 or kb > 22500 else "PASS"
    say(kind, f"MEMORY.md {lines} lines, {kb:,} bytes (Claude loads 200 lines or 25,000 bytes)"
        + (": trim it with consolidate-memory" if kind != "PASS" else ""))
    dead = [l for l in re.findall(r"\]\(([^)#]+\.md)\)", raw.decode("utf-8", "ignore"))
            if not os.path.isfile(os.path.join(MEMORY, l))]
    say("WARN" if dead else "PASS", f"MEMORY.md links: {len(dead)} dead" + (f" {dead[:5]}" if dead else ""))
    key = re.compile(r"(sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AIza[0-9A-Za-z_-]{35}|xox[bp]-[0-9A-Za-z-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY)")
    hits = []
    for dp, dn, fn in os.walk(MEMORY):
        for f in fn:
            if f.endswith(".md") and key.search(open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()):
                hits.append(f)
    say("FAIL" if hits else "PASS", "memory holds no key or token" + (f": {hits}" if hits else ""))

# 4. Settings and hooks: memory folder; the hooks ride in the plugin entry, never also in a settings file (6 Nov 2026).
s = {}
for sp in (".claude/settings.json", ".claude/settings.local.json"):  # local wins; setup_mac.py writes it per Mac
    if os.path.isfile(os.path.join(BRAIN, sp)):
        s.update(json.load(open(os.path.join(BRAIN, sp))))
amd = os.path.expanduser(s.get("autoMemoryDirectory", ""))
say("PASS" if os.path.realpath(amd) == os.path.realpath(MEMORY) else "FAIL", f"autoMemoryDirectory = {s.get('autoMemoryDirectory')}"
    + ("" if os.path.realpath(amd) == os.path.realpath(MEMORY) else ": run setup_mac.py"))
hooks = json.dumps(mp["plugins"][0].get("hooks", {}))
for word, what in [("llllloc:router", "router hook names llllloc:router"), ("git-pull", "session start pulls from GitHub"),
                   ("core-rule", "session start prints the core rule outside the brain"), ("delete-guard", "delete guard"),
                   ("research-guard", "research guard"), ("stop-check", "stop check"), ("impeccable_hook", "impeccable hook")]:
    say("PASS" if word in hooks else "FAIL", f"plugin hook: {what}")
twice = []
for sp in [os.path.join(BRAIN, ".claude/settings.json"), os.path.join(BRAIN, ".claude/settings.local.json"),
           os.path.expanduser("~/.claude/settings.json")]:
    if os.path.isfile(sp) and re.search(r"llllloc_hooks\.py|impeccable_hook\.py|llllloc:router", json.dumps(json.load(open(sp)).get("hooks", {}))):
        twice.append(sp)
say("FAIL" if twice else "PASS", "no llllloc hook also in a settings file" + (f" (fires twice): {twice}" if twice else ""))

# 5. Old names left in live rule files (history files are skipped).
old = re.compile(r"anthropic-skills:llllloc|(?<![\w/.-])llllloc-(?:task|tool|project|references)-[a-z-]+")
found = []
for root in ["llllloc/0_Core rule", "llllloc/2_Skills", "llllloc/3_Project maps", "llllloc/7_Templates"]:  # memory notes keep their history
    for dp, dn, fn in os.walk(os.path.join(BRAIN, root)):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if f.endswith((".md", ".py")) and f not in ("NOTES.md", "brain_check.py"):
                text = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
                for mm in old.finditer(text):
                    line = text[text.rfind("\n", 0, mm.start()) + 1:text.find("\n", mm.end())]
                    if mm.group(0) != "llllloc-tool-rea" and "Never pick" not in line:  # history and the router's own ban
                        found.append(f"{os.path.relpath(os.path.join(dp, f), BRAIN)}: {mm.group(0)}")
say("WARN" if found else "PASS", f"old skill names left: {len(found)}" + ("".join(f"\n      {x}" for x in found[:8])))

# 5b. Fixed Mac paths: rules and scripts write ~/ or find the brain from their own file, so any Mac works (6 Nov 2026).
fixed = re.compile(r"/Users/(?!Shared/|you/|guest/)[A-Za-z0-9._-]+/")
hits = []
for root in ["AGENTS.md", "README.md", "SETUP.md", "RESTORE.md", ".claude-plugin", "llllloc"]:
    top = os.path.join(BRAIN, root)
    walk = [(os.path.dirname(top), [], [os.path.basename(top)])] if os.path.isfile(top) else os.walk(top)
    for dp, dn, fn in walk:
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if f.endswith((".md", ".py", ".json", ".sh", ".command", ".txt", ".js")) and f != "brain_check.py":
                p = os.path.join(dp, f)
                if os.path.isdir(os.path.join(BRAIN, ".git")) and subprocess.run(["git", "-C", BRAIN, "check-ignore", "-q", p]).returncode == 0:
                    continue
                if fixed.search(open(p, encoding="utf-8", errors="ignore").read()):
                    hits.append(os.path.relpath(p, BRAIN))
say("FAIL" if hits else "PASS", f"files with a fixed /Users/<name>/ path: {len(hits)}" + "".join(f"\n      {x}" for x in hits[:8]))

# 6. Git: the files that must travel are not ignored, and GitHub is in step.
if not os.path.isdir(os.path.join(BRAIN, ".git")):  # a copy from the Drive template (7 Nov 2026)
    say("PASS", "local copy with no GitHub link: git checks skipped")
    print(f"\n{'ALL GOOD' if not fails else f'{fails} FAIL'}")
    sys.exit(1 if fails else 0)
skipped = [l for l in git("ls-files", "--others", "--ignored", "--exclude-standard", "--", "llllloc/2_Skills").splitlines()
           if not re.search(r"/(Old|_DELETE|OLD VERSIONS|__pycache__|node_modules)/|\.skill$|\.zip$|\.DS_Store$", l)]
say("FAIL" if skipped else "PASS", f"skill files git skips: {len(skipped)}" + ("".join(f"\n      {x}" for x in skipped[:8])))
# A git mv into a _DELETE folder keeps the file tracked (7 Nov 2026): _DELETE never leaves the Mac.
leaked = [l for l in git("ls-files").splitlines() if "/_DELETE/" in "/" + l]
say("FAIL" if leaked else "PASS", f"_DELETE files on GitHub: {len(leaked)}" + ("".join(f"\n      {x}" for x in leaked[:8]))
    + (": git rm --cached is blocked, use git update-index --force-remove" if leaked else ""))
# GitHub holds only the plugin (6 Nov 2026, his words): these must go online...
for p in [".claude-plugin/marketplace.json", "AGENTS.md", "llllloc/0_Core rule/Core Rule.md", "llllloc/0_Core rule/hooks/llllloc_hooks.py"]:
    ignored = subprocess.run(["git", "-C", BRAIN, "check-ignore", "-q", p]).returncode == 0
    say("FAIL" if ignored else "PASS", f"git keeps {p}" if not ignored else f".gitignore hides {p}")
# ...and these must stay on the Mac.
for p in ["llllloc/9_Memory/MEMORY.md", "llllloc/3_Project maps/Project map_Code.md", "llllloc_workflow/1_Lessons/Your words.md", ".claude/settings.json"]:
    ignored = subprocess.run(["git", "-C", BRAIN, "check-ignore", "-q", p]).returncode == 0
    say("PASS" if ignored else "FAIL", f"stays on the Mac: {p}" if ignored else f"would go to GitHub: {p}")
git("fetch", "-q", "origin")
ahead_behind = git("rev-list", "--left-right", "--count", "HEAD...origin/main").split()
dirty = len([l for l in git("status", "--porcelain").splitlines() if l and not l.endswith(".obsidian/")])
if len(ahead_behind) == 2:
    a, b = ahead_behind
    say("PASS" if a == b == "0" and not dirty else "WARN",
        f"GitHub: {a} commits to push, {b} to pull, {dirty} unsaved files" + ("" if a == b == "0" and not dirty else ": `end` saves and pushes"))

print(f"\n{'ALL GOOD' if not fails else f'{fails} FAIL'}")
sys.exit(1 if fails else 0)
