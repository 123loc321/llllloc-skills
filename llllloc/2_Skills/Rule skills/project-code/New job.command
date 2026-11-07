#!/bin/bash
# New job.command: makes a new code job folder in the llllloc shape (FOLDERS v16, 16 Oct 2026).
# Double-click it, then type the kind (Plugins, Apps, Scripts, Websites, or a new kind) and the job name.
# Or: bash "New job.command" "<Kind>" "<JOB NAME>"
set -euo pipefail
CODE="$HOME/Desktop/PERSONAL PROJECT/CODE"
KIND="${1:-}"; JOB="${2:-}"
[ -z "$KIND" ] && read -r -p "Kind (Plugins, Apps, Scripts, Websites, or a new kind): " KIND
[ -z "$JOB" ] && read -r -p "Job name, as you call it: " JOB
J="$CODE/$KIND/$JOB"
if [ -e "$J" ]; then echo "Already exists: $J"; exit 1; fi
mkdir -p "$J/_CLAUDE/0_Handoffs" "$J/_CLAUDE/1_Spec" "$J/_CLAUDE/4_Builds" "$J/_CLAUDE/_DELETE"
D="$(TZ=Asia/Ho_Chi_Minh date +%Y-%m-%d_%H%M)"
cat > "$J/_CLAUDE/0_Handoffs/HANDOFF_${JOB}_${D}.md" <<EOT
# HANDOFF — $JOB — $D
Thread: none · Job: $JOB · Build before: none · Build after: none

1. Goal of the thread: new job, made $D. Nothing built yet.
2. Files changed: the _CLAUDE folder.
3. Tests run: none.
4. Checked or only believed: nothing this thread.
5. Decisions taken: nothing this thread.
6. Tried and failed: nothing this thread.
7. His words this thread: nothing this thread.
8. Open questions for him: nothing this thread.
9. Next step: add the job's row to Project map_Code.md, write 1_Spec/SPEC.md, then the first build ($JOB-V1-INSTALLER/ beside _CLAUDE/).
10. Copied into STATE, CHANGELOG and FEATURES: yes.
EOT
printf '# STATE — %s\nLast updated: %s\n\n## 1. Newest build and where it is\nNone yet.\n## 2. The one test to ask him for\nNone yet.\n## 3. Open: bugs and untested features\nNone yet.\n## 4. Do not\n## 5. Next task\nWrite 1_Spec/SPEC.md, then the first build.\n' "$JOB" "$D" > "$J/_CLAUDE/STATE.md"
printf '# PROJECT — %s\n\nWhat it does, in one line · who uses it · kind · host apps and versions · how he installs it · look · choices costly to undo.\n' "$JOB" > "$J/_CLAUDE/PROJECT.md"
printf '# DECISIONS — %s\n\nOne line per tech choice: D01 · date · decision · why · what was turned down · status.\n' "$JOB" > "$J/_CLAUDE/DECISIONS.md"
printf '# HIS-WORDS — %s\n\nHis exact words, dated. One home.\n' "$JOB" > "$J/_CLAUDE/HIS-WORDS.md"
printf '{\n  "job": "%s",\n  "status_values": ["untested", "passed", "confirmed live"],\n  "features": []\n}\n' "$JOB" > "$J/_CLAUDE/1_Spec/FEATURES.json"
printf '# CHANGELOG — %s\n\nNewest build first: version, date, Added, Changed, Fixed, status.\n' "$JOB" > "$J/_CLAUDE/4_Builds/CHANGELOG.md"
echo "Made: $J"
find "$J" | sed "s|$CODE/||"
echo "Next: add the row to llllloc/3_Project maps/Project map_Code.md"
