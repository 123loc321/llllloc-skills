#!/bin/bash
# The gate on a handoff. Use: bash "_System file/_TEMPLATE/check-state.sh" "<path to STATE.md>"
# Exit 0: the eight headings in order, under 60 lines, under the char cap, written today. Exit 1 names what is wrong.
F="$1"; bad=0
H=("## NEWEST BUILD" "## THE ONE TEST" "## NOW" "## DONE THIS ROUND" "## DO NOT" "## UNTESTED ON HIS MAC" "## HIS LAST WORDS" "## WHERE TO LOOK")
[ -f "$F" ] || { echo "x no file: $F"; exit 1; }
last=0
for h in "${H[@]}"; do n=$(grep -n -m1 "^$h" "$F" | cut -d: -f1); if [ -z "$n" ]; then echo "x missing: $h"; bad=1; elif [ "$n" -le "$last" ]; then echo "x out of order: $h"; bad=1; else last=$n; fi; done
L=$(wc -l < "$F" | tr -d ' '); [ "$L" -le 60 ] || { echo "x $L lines, cap 60"; bad=1; }
# Hook output over 10,000 chars arrives cut. The hook prints the named panel first and the suite STATE only when room is left, so every STATE gets 9,000.
CAP=9000
C=$(wc -c < "$F" | tr -d ' '); [ "$C" -le $CAP ] || { echo "x $C chars, cap $CAP: move detail to LOG.md, a rule to .claude/rules/"; bad=1; }
TODAY=$(TZ=Asia/Ho_Chi_Minh date "+%-d %B %Y"); head -4 "$F" | grep -q "$TODAY" || { echo "x not written today ($TODAY) in the first 4 lines"; bad=1; }
[ $bad -eq 0 ] && echo "ok  $L lines, $C chars, eight headings, written $TODAY: $F"; exit $bad
