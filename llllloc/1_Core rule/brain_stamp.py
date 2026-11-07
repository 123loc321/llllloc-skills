#!/usr/bin/env python3
"""brain_stamp.py: which copy of the brain is newer, the Mac folder or the Google Drive backup (7 Nov 2026).

  python3 -I brain_stamp.py write            write <brain>/BACKUP-STAMP.json (the weekly Drive backup runs this first)
  python3 -I brain_stamp.py show             print this folder's facts
  python3 -I brain_stamp.py compare <file>   compare a stamp from Drive with this folder, print MAC NEWER, DRIVE NEWER or SAME

Facts: when the stamp was made, on which Mac, the file count, a fingerprint of every path and size,
the newest file change, and the last git commit (its date comes from the commit, not from file times,
so it stays right after a download). Skips what the backup skips: _DELETE, .git, .git-media,
.claude/worktrees, node_modules, .DS_Store, keys, and the stamp itself.
His rule (6 Nov 2026): never overwrite a newer Mac copy. When the verdict is not clear, ask him.
"""
import datetime, hashlib, json, os, socket, subprocess, sys

BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STAMP = os.path.join(BRAIN, "BACKUP-STAMP.json")
SKIP_DIRS = {"_DELETE", ".git", ".git-media", "node_modules", "__pycache__"}
SKIP_ENDS = (".DS_Store", ".env", ".mcp-token", ".pem", ".key", "BACKUP-STAMP.json")


def iso(t):
    return datetime.datetime.fromtimestamp(t).astimezone().isoformat(timespec="seconds")


def facts():
    h, count, newest, newest_file = hashlib.sha256(), 0, 0.0, ""
    rows = []
    for dp, dn, fn in os.walk(BRAIN):
        rel_dp = os.path.relpath(dp, BRAIN)
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not (rel_dp == ".claude" and d == "worktrees")]
        for f in fn:
            p = os.path.join(dp, f)
            if f.endswith(SKIP_ENDS) or os.path.islink(p):
                continue
            st = os.stat(p)
            rel = os.path.relpath(p, BRAIN)
            rows.append(f"{rel}\t{st.st_size}")
            count += 1
            if st.st_mtime > newest:
                newest, newest_file = st.st_mtime, rel
    for r in sorted(rows):
        h.update(r.encode("utf-8", "surrogateescape") + b"\n")
    commit = {}
    if os.path.isdir(os.path.join(BRAIN, ".git")):
        out = subprocess.run(["git", "-C", BRAIN, "log", "-1", "--format=%h%x09%cI%x09%s"], capture_output=True, text=True).stdout.strip()
        if out:
            sha, date, subject = out.split("\t", 2)
            commit = {"sha": sha, "date": date, "subject": subject[:100]}
    try:
        mac = subprocess.run(["scutil", "--get", "ComputerName"], capture_output=True, text=True).stdout.strip()
    except OSError:
        mac = ""
    return {"made": iso(datetime.datetime.now().timestamp()), "mac": mac or socket.gethostname(), "files": count,
            "fingerprint": h.hexdigest()[:16], "newest_change": iso(newest), "newest_file": newest_file,
            "last_commit": commit}


def when(s):
    return datetime.datetime.fromisoformat(s) if s else None


def compare(drive):
    mac = facts()
    own = json.load(open(STAMP)) if os.path.isfile(STAMP) else {}
    print(f"Drive copy: stamp {drive.get('made')} from {drive.get('mac')}, {drive.get('files')} files, "
          f"last commit {drive.get('last_commit', {}).get('date', 'none')}")
    print(f"Mac copy:   {mac['files']} files, newest change {mac['newest_change']} ({mac['newest_file']}), "
          f"last commit {mac['last_commit'].get('date', 'none')}")
    if mac["fingerprint"] == drive.get("fingerprint"):
        print("SAME: every path and size match.")
        return
    if own.get("made") and own.get("made") == drive.get("made"):
        print("MAC NEWER: this Mac made that backup, and files changed here since. Keep the Mac copy.")
        return
    mc, dc = when(mac["last_commit"].get("date")), when(drive.get("last_commit", {}).get("date"))
    if mc and dc and mc != dc:
        print("MAC NEWER: its last commit is later. Keep the Mac copy." if mc > dc else
              "DRIVE NEWER: its last commit is later. Ask him before replacing the Mac copy.")
        return
    mn, dn = when(mac["newest_change"]), when(drive.get("newest_change"))
    if mn and dn:
        print("MAC NEWER (by file times): keep the Mac copy." if mn >= dn else
              "DRIVE NEWER (by file times): ask him before replacing the Mac copy.")
        print("File times can lie after a browser download. When in doubt, ask him.")
        return
    print("NOT CLEAR: ask him which copy to keep.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    if cmd == "write":
        f = facts()
        json.dump(f, open(STAMP, "w"), indent=2)
        print(f"stamp: {f['files']} files, newest change {f['newest_change']}, fingerprint {f['fingerprint']}")
    elif cmd == "compare" and len(sys.argv) > 2:
        compare(json.load(open(sys.argv[2])))
    else:
        print(json.dumps(facts(), indent=2))
