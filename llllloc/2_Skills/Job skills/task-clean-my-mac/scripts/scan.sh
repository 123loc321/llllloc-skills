#!/bin/bash
# Read-only scan of where the space went. Prints sizes only. Moves and deletes nothing.
# Usage: bash scan.sh [drive path]   (default: /Volumes/CREATIVE #1)
# Takes 5 to 10 minutes on a full 2 TB Mac: run it in the background.
H="$HOME"; D="${1:-/Volumes/CREATIVE #1}"
s(){ for p in "$@"; do [ -e "$p" ] && du -sh "$p" 2>/dev/null; done; }
hdr(){ echo; echo "=== $1"; }
top(){ du -sh "$@" 2>/dev/null | sort -rh | head -"${N:-15}"; }
big(){ awk '{printf "%.1fG %s\n", $5/1073741824, substr($0, index($0,$9))}'; }

hdr "DISK"; df -h /System/Volumes/Data "$D" 2>/dev/null | tail -n +2
hdr "RUNNING APPS (their caches stay)"; ps -axo comm | grep -oE "/Applications/[^/]+\.app|/Applications/[^/]+/[^/]+\.app" | sed 's#.*/##' | sort -u | tr '\n' ',' ; echo
pgrep -fl ollama | head -2; command -v ollama >/dev/null && ollama list 2>/dev/null
hdr "SNAPSHOTS, SWAP"; tmutil listlocalsnapshots / 2>/dev/null; sysctl vm.swapusage; ls -l /private/var/vm 2>/dev/null | tail -n +2
hdr "HOME TOP"; top "$H"/* "$H"/.[!.]*
hdr "LIBRARY TOP"; top "$H/Library"/*
hdr "APPLICATION SUPPORT TOP"; N=25 top "$H/Library/Application Support"/*
hdr "SYSTEM LIBRARY, USERS SHARED"; top "/Library/Application Support"/* /Users/Shared/*
hdr "CACHES"; top "$H/Library/Caches"/* "$H/.cache"/*
hdr "TEMP"; s /private/var/folders "$TMPDIR" /private/tmp; N=8 top /private/tmp/claude-*/*
hdr "ADOBE"; s "$H/Desktop/Cache"/* "$H/Library/Application Support/Adobe/Common/Media Cache Files" "$H/Library/Application Support/Adobe/Common/Peak Files" "$H/Documents/Adobe"/*/*Previews
N=20 top "$H/Library/Preferences/Adobe"/*/*
find "$H/Library/Preferences/Adobe" -name "DirectOutFastDraftCapture.ae3d" -exec ls -l {} \; 2>/dev/null | big
ls /Applications | grep -E "^Adobe |^Maxon " ; ls "/Library/Application Support/Adobe/Uninstall/" 2>/dev/null | grep "\.app$" | tr '\n' ' '; echo
hdr "OTHER CREATIVE APPS"; s "$H/Movies/CacheClip" "$H/Library/Application Support/Blackmagic Design" "$H/Movies/CapCut" "$H/Library/Caches/com.captureone.captureone16"; N=10 top "$H/Library/Application Support/Blender"/* "$H/Library/Preferences/Maxon"/*
hdr "BROWSERS AND ELECTRON CACHES"; find "$H/Library/Application Support" -maxdepth 5 -type d \( -name "Cache" -o -name "Code Cache" -o -name "GPUCache" -o -name "Service Worker" \) -prune -exec du -sh {} + 2>/dev/null | sort -rh | head -20
hdr "CLOUD FOLDERS (a name ending in a date is a disconnected copy)"; s "$H/Library/CloudStorage"/*
hdr "DEV AND AI"; s "$H/.ollama/models" "$H/ComfyUI-Shared/models" "$H/Library/Containers/com.docker.docker" "$H/Library/Application Support/Claude/vm_bundles" "$H/Library/Developer/CoreSimulator" "$H/.npm" "$H/.cargo" "$H/.rustup" "$H/.claude"
find "$H/Desktop" "$H/Documents" -maxdepth 7 -type d \( -name node_modules -o -name .venv -o -name target -o -name .build -o -name build \) -prune 2>/dev/null | while read -r d; do du -sh "$d"; done | sort -rh | head -15
hdr "_DELETE FOLDERS"; { find "$H" -xdev -type d -iname "_DELETE*" -prune -not -path "*/Library/*" -not -path "*/.Trash/*" 2>/dev/null; find "$D" -type d -iname "_DELETE*" -prune -not -path "*/.Trashes/*" 2>/dev/null; } | while read -r d; do du -sh "$d"; done | sort -rh | head -40
hdr "OLD FOLDERS (OLD VERSIONS renders are KEEP)"; find "$H/Desktop" "$H/Documents" "$H/Movies" -type d \( -iname "OLD VERSION*" -o -iname "_Old*" -o -iname "Old" -o -iname "_OLDER" \) -prune 2>/dev/null | while read -r d; do du -sh "$d"; done | sort -rh | head -25
hdr "INSTALLERS AND ZIPS OVER 100 MB"; find "$H" -xdev -type f \( -iname "*.dmg" -o -iname "*.pkg" -o -iname "*.zip" -o -iname "*.tar.gz" \) -size +100M -not -path "*/Library/*" -not -path "*/.Trash/*" 2>/dev/null -exec ls -l {} \; | big | sort -rh | head -25
hdr "BIG FILES OVER 3 GB (outside Library)"; find "$H" -xdev -type f -size +3G -not -path "*/Library/*" -not -path "*/.Trash/*" 2>/dev/null -exec ls -l {} \; | big | sort -rh | head -25
hdr "DESKTOP JOBS"; N=20 top "$H/Desktop/PERSONAL PROJECT"/*/*
hdr "DOWNLOADS"; N=20 top "$H/Downloads"/*
hdr "APP DATA OF APPS NOT INSTALLED (check each by hand)"
ls /Applications "$H/Applications" 2>/dev/null | sed 's/\.app$//' | tr 'A-Z' 'a-z' > "${TMPDIR:-/tmp}/apps_installed.txt"
du -sm "$H/Library/Application Support"/* 2>/dev/null | awk '$1>200' | sort -rn | while read -r sz p; do k=$(basename "$p" | tr 'A-Z' 'a-z' | sed 's/^com\.[a-z]*\.//; s/ .*//'); grep -qi "$k" "${TMPDIR:-/tmp}/apps_installed.txt" || echo "${sz}M | $(basename "$p")"; done
echo; echo "SCAN DONE"
