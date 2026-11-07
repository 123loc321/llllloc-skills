#!/usr/bin/env python3
"""setup_mac.py: writes the Mac settings the llllloc plugin cannot carry (6 Nov 2026, local copies 7 Nov 2026). Safe to run again.

  python3 -I setup_mac.py                      this brain folder, and this Mac's user settings
  python3 -I setup_mac.py --brain-only         only the brain folder's own settings (used by the setup test)
  python3 -I setup_mac.py --local              load the skills from this folder even when GitHub answers

1. <brain>/.claude/settings.local.json: autoMemoryDirectory = this brain's llllloc/9_Memory.
   A local file, so each Mac points at its own copy, wherever it lives.
2. <brain>/.agents/skills: one link per skill folder, for Codex, Gemini, Cursor and Copilot.
   Google Drive cannot store links, so a copy from Drive needs them made again.
3. ~/.claude/settings.json (a dated backup first): the llllloc-brain marketplace, the llllloc plugin turned on,
   the skill list room at 3%. Every other line stays as it was. The marketplace source is
   - his git copy (a .git folder): his private GitHub 123loc321/llllloc (marketplace llllloc-brain, auto-update on)
     when it answers, else this folder. Never the shared repo: the same plugin twice shows every skill twice.
   - a copy with no .git (the Drive template, a friend's Mac): the public shared repo 123loc321/llllloc-skills
     (marketplace llllloc-skills, auto-update on, refreshed weekly) when it answers (7 Nov 2026), else this folder
     ("directory" source, edits here load at the next session). --local always picks this folder.
   The marketplace not picked is turned off, so a Mac never loads the plugin twice.
   Docs: code.claude.com/docs/en/plugins/marketplace-reference, code.claude.com/docs/en/plugins/host-marketplace
"""
import datetime, json, os, shutil, subprocess, sys

BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOME = os.path.expanduser("~")
GIT = {"source": {"source": "git", "url": "https://github.com/123loc321/llllloc.git"}, "autoUpdate": True}
SHARED_URL = "https://github.com/123loc321/llllloc-skills.git"  # public, no account needed (his pick, 7 Nov 2026)
SHARED = {"source": {"source": "git", "url": SHARED_URL}, "autoUpdate": True}


def tilde(p):
    return "~" + p[len(HOME):] if p.startswith(HOME + "/") else p


def load(p):
    try:
        return json.load(open(p))
    except (OSError, ValueError):
        return {}


def save(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def answers(*cmd):
    try:  # no prompt: a missing sign-in fails fast instead of waiting
        env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
        return subprocess.run(["git", *cmd], capture_output=True, timeout=20, env=env).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def pick_source():
    """(marketplace name, source entry, words for the report)."""
    if "--local" not in sys.argv:
        if os.path.isdir(os.path.join(BRAIN, ".git")):
            if answers("-C", BRAIN, "ls-remote", "-q", "origin", "HEAD"):
                return "llllloc-brain", GIT, "GitHub 123loc321/llllloc (auto-update on)"
        elif answers("ls-remote", "-q", SHARED_URL, "HEAD"):
            return "llllloc-skills", SHARED, "the shared GitHub repo 123loc321/llllloc-skills (auto-update on)"
    name = json.load(open(os.path.join(BRAIN, ".claude-plugin", "marketplace.json"))).get("name", "llllloc-brain")
    return name, {"source": {"source": "directory", "path": BRAIN}}, f"this folder ({tilde(BRAIN)})"


# 1. Memory folder of this brain.
local = os.path.join(BRAIN, ".claude", "settings.local.json")
d = load(local)
d["autoMemoryDirectory"] = tilde(os.path.join(BRAIN, "llllloc", "9_Memory"))
save(local, d)
idx = os.path.join(BRAIN, "llllloc", "9_Memory", "MEMORY.md")
if not os.path.isfile(idx):
    os.makedirs(os.path.dirname(idx), exist_ok=True)
    open(idx, "w").write("Index of memory files. One line per memory: a link to its note file and a short hook.\n")
print(f"settings: {tilde(local)} -> memory {d['autoMemoryDirectory']}")

# 2. Skill links for other AI apps.
mp = json.load(open(os.path.join(BRAIN, ".claude-plugin", "marketplace.json")))
ag = os.path.join(BRAIN, ".agents", "skills")
os.makedirs(ag, exist_ok=True)
made = 0
for rel in mp["plugins"][0].get("skills", []):
    name = os.path.basename(rel.rstrip("/"))
    link = os.path.join(ag, name)
    if not os.path.lexists(link) and os.path.isfile(os.path.join(BRAIN, rel, "SKILL.md")):
        os.symlink(os.path.join("..", "..", os.path.normpath(rel)), link)
        made += 1
print(f"links: .agents/skills -> {made} made, {len(os.listdir(ag))} in all")

# 3. Mac user settings.
if "--brain-only" not in sys.argv:
    user = os.path.join(HOME, ".claude", "settings.json")
    if os.path.isfile(user):
        shutil.copy2(user, f"{user}.before-llllloc-setup-{datetime.date.today().isoformat()}")
    u = load(user)
    name, market, where = pick_source()
    known, enabled = u.setdefault("extraKnownMarketplaces", {}), u.setdefault("enabledPlugins", {})
    for other in ("llllloc-brain", "llllloc-skills"):
        if other != name and f"llllloc@{other}" in enabled:
            enabled[f"llllloc@{other}"] = False  # one plugin copy only
            known.pop(other, None)
    known[name] = market
    enabled[f"llllloc@{name}"] = True
    u["skillListingBudgetFraction"] = 0.03
    if os.path.realpath(BRAIN) not in {os.path.realpath(os.path.expanduser(p)) for p in ("~/llllloc", "~/Desktop/Claude")}:
        u.setdefault("env", {})["LLLLLOC_BRAIN"] = BRAIN  # the hooks look in those two places, else here
    save(user, u)
    print(f"settings: ~/.claude/settings.json -> llllloc plugin from {where}, skill list room 3%")
