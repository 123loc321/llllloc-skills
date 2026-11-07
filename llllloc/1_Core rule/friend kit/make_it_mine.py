#!/usr/bin/env python3
"""make_it_mine.py: turns a shared copy of llllloc into the friend's OWN system (7 Nov 2026).

Loc's words (7 Nov 2026): "i want to skill start with their own name: not llllloc, because this workflow system
when sharing with my friend, i want them to be able to customize things based own their own workflow."

  python3 -I make_it_mine.py --name "Mira Tran" --prefix mira [--github-user mira-t] [--dry-run]

Every "llllloc" in every text file and every file or folder name becomes the prefix: skills load as
"<prefix>:<skill>", the folders become <prefix>/ and <prefix>_workflow/, the marketplace <prefix>-brain.
Kept as they are, so the weekly upstream check still finds Loc's updates: the public repo 123loc321/llllloc-skills
and the Drive folder *llllloc_System_Template. Loc's private repo 123loc321/llllloc becomes <github-user>/<prefix>.
Writes MINE.json beside this script. Runs once, only on a copy with no .git (never on Loc's own brain).
"""
import argparse, datetime, json, os, re, sys

KIT = os.path.dirname(os.path.abspath(__file__))
BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(KIT)))
FROM = "llllloc"
UPSTREAM = "https://github.com/123loc321/llllloc-skills.git"
KEEP = ("123loc321/llllloc-skills", "llllloc-skills", "llllloc_System_Template", "Loc's shared llllloc", "Loc's llllloc")  # Loc's places, never renamed
RESERVED = {"claude", "anthropic", "claude-code", "official", "plugins", "skills", "agents", "mcp"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}


def mapper(prefix, github_user=""):
    """Returns map(text) -> text with Loc's names swapped for the friend's. Also used by check_upstream.py."""
    gh = github_user or "<your-github-user>"
    env = re.sub(r"[^A-Z0-9]", "_", prefix.upper())
    pairs = [("123loc321/llllloc", f"{gh}/{prefix}"), ("123loc321", gh), (FROM, prefix),
             (FROM.upper(), env), (FROM.capitalize(), prefix.capitalize())]

    def run(text):
        for i, k in enumerate(KEEP):
            text = text.replace(k, f"\0KEEP{i}\0")
        for a, b in pairs:
            text = text.replace(a, b)
        for i, k in enumerate(KEEP):
            text = text.replace(f"\0KEEP{i}\0", k)
        return text
    return run


def read_text(path):
    try:
        if os.path.getsize(path) > 5_000_000:
            return None
        b = open(path, "rb").read()
        return None if b"\x00" in b else b.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def check_prefix(p):
    if not re.fullmatch(r"[a-z][a-z0-9-]{1,29}", p) or p.endswith("-"):
        return "use 2 to 30 small letters, numbers or -, starting with a letter (example: mira or mira-studio)"
    if FROM in p or p in RESERVED:
        return f"'{p}' is taken, pick another"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--github-user", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if err := check_prefix(a.prefix):
        sys.exit(f"STOP: {err}")
    if os.path.isdir(os.path.join(BRAIN, ".git")):
        sys.exit("STOP: this folder has a .git, so it is Loc's own brain or already set up. Nothing changed.")
    mp = json.load(open(os.path.join(BRAIN, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
    if mp["plugins"][0]["name"] != FROM:
        sys.exit(f"STOP: this copy is already renamed to '{mp['plugins'][0]['name']}'. Nothing changed.")
    swap = mapper(a.prefix, a.github_user)

    texts = renames = links = 0
    for dp, dn, fn in os.walk(BRAIN):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            p = os.path.join(dp, f)
            if os.path.islink(p):
                t = os.readlink(p)
                if FROM in t:
                    links += 1
                    if not a.dry_run:
                        os.unlink(p)  # a link, not data: remade at once with the new target
                        os.symlink(swap(t), p)
                continue
            if dp == KIT and f.endswith(".py"):  # the kit's own code keeps Loc's names: it maps them
                continue
            text = read_text(p)
            if text is not None and swap(text) != text:
                texts += 1
                if not a.dry_run:
                    st = os.stat(p)
                    open(p, "w", encoding="utf-8").write(swap(text))
                    os.utime(p, (st.st_atime, st.st_mtime))
    for dp, dn, fn in os.walk(BRAIN, topdown=False):  # deepest first, so parent folders rename last
        if any(s in dp.split(os.sep) for s in SKIP_DIRS):
            continue
        for n in dn + fn:
            if FROM in n:
                renames += 1
                if not a.dry_run:
                    os.rename(os.path.join(dp, n), os.path.join(dp, swap(n)))

    if not a.dry_run:
        mpp = os.path.join(BRAIN, ".claude-plugin", "marketplace.json")
        mp = json.load(open(mpp, encoding="utf-8"))
        mp["owner"] = {"name": a.name}
        mp["description"] = f"{a.name}'s {a.prefix} workflow skills, built from Loc's llllloc"
        mp["plugins"][0]["description"] = f"{a.name}'s {a.prefix} workflow skills"
        open(mpp, "w", encoding="utf-8").write(json.dumps(mp, indent=2, ensure_ascii=False) + "\n")
        ag = os.path.join(BRAIN, "AGENTS.md")
        s = open(ag, encoding="utf-8").read()
        note = (f"\n**Owner: {a.name}** (set {datetime.date.today():%d %b %Y}). This system started as a copy of Loc's llllloc. "
                f"In these files \"he\", \"his\" and \"Loc\" mean the owner of this folder, {a.name}, until you rewrite them. "
                f"Loc's newest updates are checked weekly (`{a.prefix}/1_Core rule/friend kit/check_upstream.py`): you pick what to take.\n")
        s = s.replace("\n", "\n" + note, 1) if "**Owner:" not in s else s
        open(ag, "w", encoding="utf-8").write(s)
        kit = os.path.join(BRAIN, a.prefix, "1_Core rule", "friend kit")
        json.dump({"name": a.name, "prefix": a.prefix, "github_user": a.github_user, "from": FROM, "upstream": UPSTREAM,
                   "date": datetime.date.today().isoformat()}, open(os.path.join(kit, "MINE.json"), "w"), indent=2)
    print(f"{'trial: ' if a.dry_run else ''}{texts} files rewritten, {renames} files and folders renamed, {links} links remade. "
          f"Skills now load as {a.prefix}:<skill>.")


if __name__ == "__main__":
    main()
