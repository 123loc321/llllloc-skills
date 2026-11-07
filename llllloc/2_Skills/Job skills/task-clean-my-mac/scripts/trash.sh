#!/bin/bash
# Moves every path in a list file to the Trash, so each can be put back.
# Usage: bash trash.sh <list file, one full path per line>
# Never deletes for good. Root-owned items open a Mac password box: he types it.
# Refuses client project folders, renders and restore points. CODE and the brain folder are allowed (his words 5 Nov 2026).
L="$1"
[ -f "$L" ] || { echo "List file not found: $L"; exit 1; }
H="$HOME"
GO="$(mktemp -t trashgo)"; : > "$GO"; refused=0; links=0
while IFS= read -r p; do
  [ -z "$p" ] && continue
  case "$p" in
    *"/OLD VERSIONS"*|*"/4_RENDERS/"*|*"/Phosphene/_CLAUDE/4_Builds/Old"*|*"/SuperIsland/_CLAUDE/4_Builds/Old"*|*"/Rclone UI/_CLAUDE/4_Builds/Old"*|*"/COTABBY/_CLAUDE/4_Builds/Old"*)
      refused=$((refused+1)); echo "REFUSED (render or restore point): $p"; continue ;;
    "$H/Desktop/PERSONAL PROJECT/CODE/"*|"$H/Desktop/Claude/"*) ;;
    "$H/Desktop/PERSONAL PROJECT/"*|/Volumes/*)
      refused=$((refused+1)); echo "REFUSED (client project folder): $p"; continue ;;
  esac
  if [ -L "$p" ]; then
    # Finder would follow the link and trash its target: move the link itself
    t="$H/.Trash/$(basename "$p") link $(date +%H.%M.%S)"
    mv -n "$p" "$t" && links=$((links+1))
    continue
  fi
  printf '%s\n' "$p" >> "$GO"
done < "$L"
AS="$(mktemp -t trash).applescript"
cat > "$AS" <<'EOF'
on run argv
  set ok to 0
  repeat with p in argv
    try
      with timeout of 600 seconds
        tell application "Finder" to delete (POSIX file (p as text) as alias)
      end timeout
      set ok to ok + 1
    end try
  end repeat
  return ok
end run
EOF
# 40 paths per Finder call: fast, and one bad path loses one batch at most
tr '\n' '\0' < "$GO" | xargs -0 -n 40 osascript "$AS" 2>/dev/null | awk '{s+=$1} END{print "moved to Trash:", s+0}'
echo "links moved: $links, refused: $refused"
left=0
while IFS= read -r p; do [ -n "$p" ] && [ -e "$p" ] && { left=$((left+1)); echo "STILL IN PLACE: $p"; }; done < "$GO"
echo "still in place: $left"
rm -f "$AS" "$GO"
