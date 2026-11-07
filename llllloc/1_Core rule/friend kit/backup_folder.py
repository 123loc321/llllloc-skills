#!/usr/bin/env python3
"""backup_folder.py: one-way weekly copy of this whole brain folder into a backup folder (7 Nov 2026).

  python3 -I backup_folder.py "<backup folder>"     e.g. ~/Library/CloudStorage/GoogleDrive-<you>/My Drive/<prefix>_System_Full backup

Made for Google Drive for desktop (the Drive folder shows on the Mac), works for any folder. The brain goes into
<backup folder>/Claude. A file that changed or was removed here: its old backup copy moves to
<backup folder>/_DELETE/<date>/, never lost. Left out: _DELETE folders, .claude/worktrees, node_modules, key files.
"""
import datetime, os, shutil, sys

BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SKIP_DIRS = {"_DELETE", "node_modules", "__pycache__"}
SKIP_ENDS = (".env", ".mcp-token", ".pem", ".key", ".p12", ".DS_Store")


def files(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        rel_dp = os.path.relpath(dp, root)
        dn[:] = [d for d in dn if d not in SKIP_DIRS and os.path.join(rel_dp, d) != os.path.join(".claude", "worktrees")]
        for f in fn:
            p = os.path.join(dp, f)
            if not f.endswith(SKIP_ENDS) and not os.path.islink(p):
                st = os.stat(p)
                out[os.path.normpath(os.path.join(rel_dp, f))] = (st.st_size, int(st.st_mtime))
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit("STOP: give the backup folder.")
    top = os.path.expanduser(sys.argv[1])
    if not os.path.isdir(os.path.dirname(top.rstrip("/"))):
        sys.exit(f"STOP: {os.path.dirname(top)} is not on this Mac. Is Google Drive for desktop running and signed in?")
    dst = os.path.join(top, "Claude")
    aside = os.path.join(top, "_DELETE", datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
    os.makedirs(dst, exist_ok=True)
    src, old = files(BRAIN), files(dst)
    copied = moved = 0
    for rel, sig in src.items():
        if old.get(rel) == sig:
            continue
        d = os.path.join(dst, rel)
        if rel in old:  # keep the replaced version
            os.makedirs(os.path.dirname(os.path.join(aside, rel)), exist_ok=True)
            shutil.move(d, os.path.join(aside, rel))
            moved += 1
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(BRAIN, rel), d)
        copied += 1
    for rel in set(old) - set(src):  # gone from the brain: its backup copy moves aside
        os.makedirs(os.path.dirname(os.path.join(aside, rel)), exist_ok=True)
        shutil.move(os.path.join(dst, rel), os.path.join(aside, rel))
        moved += 1
    left = sum(1 for rel, sig in files(dst).items() if src.get(rel) != sig) + len(set(src) - set(files(dst)))
    print(f"backup: {len(src)} files in {dst}, {copied} copied, {moved} old copies moved to _DELETE, {left} differences")
    sys.exit(1 if left else 0)


if __name__ == "__main__":
    main()
