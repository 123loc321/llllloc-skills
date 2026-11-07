#!/bin/bash
# Run this on the Mac where the After Effects connector already works.
# It copies the installed Synthetic AE MCP panel into this pack, in "panel".

cd "$(dirname "$0")" || exit 1
say_box() { osascript -e "display dialog \"$1\" buttons {\"OK\"} default button 1 with title \"Copy AE MCP panel\"" >/dev/null 2>&1; }
PACK="$(pwd)/AE-MCP 2nd Mac Pack"
[ -d "$PACK" ] || { say_box "Put this file next to the folder AE-MCP 2nd Mac Pack, then open it again."; exit 1; }

FOUND=""
for ROOT in "$HOME/Library/Application Support/Adobe/CEP/extensions" "/Library/Application Support/Adobe/CEP/extensions"; do
  [ -d "$ROOT" ] || continue
  for D in "$ROOT"/*/; do
    M="$D/CSXS/manifest.xml"
    [ -f "$M" ] || continue
    if grep -q 'Name="AEFT"' "$M" && grep -qi 'synthetic\|ae-mcp' "$M"; then
      FOUND="${D%/}"
      break 2
    fi
  done
done

if [ -z "$FOUND" ]; then
  say_box "Could not find the Synthetic AE MCP panel on this Mac. Send a screenshot of this window to Claude."
  ls -1 "$HOME/Library/Application Support/Adobe/CEP/extensions" "/Library/Application Support/Adobe/CEP/extensions" 2>/dev/null
  exit 1
fi

NAME="$(basename "$FOUND")"
rm -rf "$PACK/panel/$NAME"
mkdir -p "$PACK/panel"
cp -R "$FOUND" "$PACK/panel/" || { say_box "Copy failed. Send a screenshot of this window to Claude."; exit 1; }
VERSION="$(grep -o 'ExtensionBundleVersion="[^"]*"' "$FOUND/CSXS/manifest.xml" | head -n 1 | cut -d'"' -f2)"
echo "Copied: $FOUND"
echo "Version: $VERSION"
say_box "Done. The panel (version $VERSION) is now in the pack, in the folder named panel.\n\nNow send the folder AE-MCP 2nd Mac Pack to your coworker."
