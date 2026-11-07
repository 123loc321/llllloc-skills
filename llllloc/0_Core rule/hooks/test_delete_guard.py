import json, os, subprocess, sys

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llllloc_hooks.py")
CASES = [
    ("rm a job file", 'rm "/Volumes/CREATIVE #1/x/a.mp4"', "deny"),
    ("rm inside _DELETE", 'rm -rf "/Volumes/CREATIVE #1/x/_DELETE/old"', "ask"),
    ("rm temp", "rm -f /tmp/gate.txt", None),
    ("rm variable", 'rm -rf "$W"', "deny"),
    ("cd then rm", "cd /x && rm a.txt", "deny"),
    ("xargs rm", "ls | xargs rm a", "deny"),
    ("git rm", "git rm old.md", "deny"),
    ("find -delete", 'find . -name "*.tmp" -delete', "deny"),
    ("git clean", "git clean -fd", "deny"),
    ("echo text mentioning rm", "echo 'use rm to delete' > note.txt", None),
    ("commit message with words", 'git commit -m "blocks find -delete and git clean, rm too"', None),
    ("heredoc with words and apostrophe", "cat > a.md <<'EOF'\nHe said: don't rm it, find -delete and git clean are blocked\nEOF\necho done", None),
    ("two heredocs like the save step", "M=x; cat > \"$M/a.md\" <<'EOF'\n- blocks rm, rmdir, find -delete, git clean outside _DELETE\nEOF\n"
     "echo \"- line\" >> \"$M/MEMORY.md\"; cd \"/b\" && git add -A && git commit -q -F - <<'EOF'\nllllloc hooks: delete guard\n\nCo-Authored-By: x\nEOF\ngit log -1", None),
    ("ls", "ls -la ~/Desktop", None),
]
bad = 0
for name, cmd, want in CASES:
    r = subprocess.run([sys.executable, "-I", "-B", HOOK, "delete-guard"],
                       input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}), capture_output=True, text=True)
    got = json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] if r.stdout.strip() else None
    bad += got != want
    print(("ok " if got == want else "BAD"), f"{name:36} -> {got}")
print("failures:", bad)
