#!/usr/bin/env python3
"""check_upstream.py: what is new in Loc's shared llllloc since last week (7 Nov 2026). Changes nothing in the system.

Loc's words (7 Nov 2026): "my friends might want it too ... they can still check to see my lastest workflow updates,
and choose for themselves whether to adapt the new updates to their own workflow or not."

  python3 -I check_upstream.py <report folder>        weekly: REPORT.md + upstream.patch (in your own names)
  python3 -I check_upstream.py <report folder> --baseline    first time: remember where Loc is today
  python3 -I check_upstream.py --take <upstream path>  take one file as Loc has it now (your old copy goes to Old/)

Two places are checked:
1. GitHub 123loc321/llllloc-skills (skills, core rule, hooks): every commit, every changed file, and whether you
   changed your own copy of that file (then merge by hand) or not (then --take is safe).
2. The Drive folder *llllloc_System_Template, when Google Drive for desktop shows it on this Mac (MINE.json
   "drive_template"): new, changed and removed files outside the plugin, by size and date.
"""
import datetime, json, os, shutil, subprocess, sys

KIT = os.path.dirname(os.path.abspath(__file__))
BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(KIT)))
sys.path.insert(0, KIT)
from make_it_mine import mapper  # noqa: E402

MINE = json.load(open(os.path.join(KIT, "MINE.json"))) if os.path.isfile(os.path.join(KIT, "MINE.json")) else {}
PREFIX = MINE.get("prefix", "llllloc")
URL = MINE.get("upstream", "https://github.com/123loc321/llllloc-skills.git")
HOME_DIR = os.path.expanduser(f"~/Library/Application Support/{PREFIX}/upstream")
CLONE, STATE = os.path.join(HOME_DIR, "repo"), os.path.join(HOME_DIR, "state.json")
swap = mapper(PREFIX, MINE.get("github_user", "")) if MINE else (lambda t: t)
PLUGIN_PARTS = ("llllloc/2_Skills/", "llllloc/0_Core rule/", ".claude-plugin/", "AGENTS.md", "CLAUDE.md", "README.md")


def git(*a, check=True):
    r = subprocess.run(["git", "-C", CLONE, *a], capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"STOP: git {a[0]} failed: {(r.stderr or r.stdout).strip()[:300]}")
    return r.stdout


def fetch():
    if not os.path.isdir(os.path.join(CLONE, ".git")):
        os.makedirs(HOME_DIR, exist_ok=True)
        r = subprocess.run(["git", "clone", "-q", URL, CLONE], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"STOP: cannot reach {URL}: {r.stderr.strip()[:200]}")
    git("fetch", "-q", "origin", "main")
    return git("rev-parse", "origin/main").strip()


def show(sha, path):
    r = subprocess.run(["git", "-C", CLONE, "show", f"{sha}:{path}"], capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def local(path):
    return os.path.join(BRAIN, swap(path))


def drive_manifest():
    root = MINE.get("drive_template", "")
    root = os.path.join(os.path.expanduser(root), "Claude") if root else ""
    if not root or not os.path.isdir(root):
        return None
    out = {}
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in {"_DELETE", ".git"}]
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), root)
            if not rel.startswith(PLUGIN_PARTS) and f != ".DS_Store":
                st = os.stat(os.path.join(dp, f))
                out[rel] = [st.st_size, int(st.st_mtime)]
    return out


def take(path):
    head = json.load(open(STATE))["commit"]
    text = show(head, path)
    if text is None:
        sys.exit(f"STOP: {path} is not in Loc's repo at {head[:7]}.")
    dst = local(path)
    had = os.path.exists(dst)
    if had:
        old =os.path.join(os.path.dirname(dst), "Old", f"{datetime.date.today():%y%m%d}_before_upstream")
        os.makedirs(old, exist_ok=True)
        shutil.copy2(dst, os.path.join(old, os.path.basename(dst)))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w", encoding="utf-8").write(swap(text))
    print(f"took {path} from Loc ({head[:7]}) -> {os.path.relpath(dst, BRAIN)}" + (", your old copy is in Old/" if had else ""))


def main():
    if "--take" in sys.argv:
        return take(sys.argv[sys.argv.index("--take") + 1])
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    head = fetch()
    man = drive_manifest()
    state = json.load(open(STATE)) if os.path.isfile(STATE) else None
    if "--baseline" in sys.argv or not state:
        json.dump({"commit": head, "drive": man, "date": datetime.date.today().isoformat()}, open(STATE, "w"))
        print(f"baseline set: Loc's repo at {head[:7]}" + (f", Drive copy {len(man)} files" if man is not None else ", Drive copy not on this Mac"))
        return
    lines = [f"# Loc's updates, {datetime.date.today():%d %b %Y}", "",
             f"Checked: GitHub {URL} from {state['commit'][:7]} to {head[:7]}" + (f", and the Drive copy" if man is not None else ""), ""]
    if head == state["commit"]:
        lines += ["## GitHub", "No new commits.", ""]
    else:
        lines += ["## GitHub commits", "```", git("log", "--date=short", "--format=%h %ad %s", f"{state['commit']}..{head}").strip(), "```", "",
                  "## Changed files", "| What | Loc's file | Your file | Your copy |", "|---|---|---|---|"]
        for row in git("diff", "--name-status", f"{state['commit']}..{head}").splitlines():
            parts = row.split("\t")
            st, was, path = parts[0], parts[1], parts[-1]  # a move (R) has the old path first
            mine = local(path) if os.path.exists(local(path)) else local(was)
            old = show(state["commit"], was)
            if path == "README.md":
                yours = "the repo's front page, not part of your system: skip"
            elif not os.path.exists(mine):
                yours = "not in your copy"
            elif old is not None and swap(old) == open(mine, encoding="utf-8", errors="replace").read():
                yours = "untouched: safe to --take"
            else:
                yours = "you changed it: merge by hand"
            what = {"A": "new", "M": "changed", "D": "removed by Loc"}.get(st[0], f"moved by Loc from `{was}`" + (", and changed" if st != "R100" else ""))
            lines.append(f"| {what} | `{path}` | `{os.path.relpath(mine, BRAIN)}` | {yours} |")
        patch = swap(git("diff", f"{state['commit']}..{head}"))
        open(os.path.join(out, "upstream.patch"), "w", encoding="utf-8").write(patch)
        lines += ["", "Every change in your own names: `upstream.patch` beside this file.", ""]
    if man is not None and state.get("drive") is not None:
        was = state["drive"]
        new = sorted(set(man) - set(was))
        gone = sorted(set(was) - set(man))
        moved = sorted(k for k in set(man) & set(was) if man[k] != was[k])
        lines += ["## Drive copy (outside the skills)", f"New: {len(new)}, changed: {len(moved)}, removed: {len(gone)}", ""]
        lines += [f"- new: `{k}`" for k in new[:60]] + [f"- changed: `{k}`" for k in moved[:60]] + [f"- removed by Loc: `{k}`" for k in gone[:60]]
    open(os.path.join(out, "REPORT.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump({"commit": head, "drive": man if man is not None else state.get("drive"), "date": datetime.date.today().isoformat()}, open(STATE, "w"))
    print(f"report: {os.path.join(out, 'REPORT.md')}")


if __name__ == "__main__":
    main()
