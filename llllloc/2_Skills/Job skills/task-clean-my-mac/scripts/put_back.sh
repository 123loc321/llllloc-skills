#!/bin/bash
# Puts items back from the Mac Trash to the folder they came from.
# Usage: bash put_back.sh <list file of the ORIGINAL full paths>
# Reads ~/.Trash/<name> directly: listing ~/.Trash is refused, direct paths work.
# Items from an external drive sit in that drive's .Trashes/<uid>/ instead.
L="$1"
[ -f "$L" ] || { echo "List file not found: $L"; exit 1; }
ok=0; miss=0
while IFS= read -r p; do
  [ -z "$p" ] && continue
  [ -e "$p" ] && continue
  n=$(basename "$p"); d=$(dirname "$p")
  case "$p" in
    /Volumes/*) v=$(echo "$p" | cut -d/ -f1-3); t="$v/.Trashes/$(id -u)/$n" ;;
    *) t="$HOME/.Trash/$n" ;;
  esac
  if [ -e "$t" ] && mkdir -p "$d" && mv -n "$t" "$d/"; then ok=$((ok+1)); else miss=$((miss+1)); echo "NOT FOUND IN TRASH: $n"; fi
done < "$L"
echo "put back: $ok, not found: $miss"
