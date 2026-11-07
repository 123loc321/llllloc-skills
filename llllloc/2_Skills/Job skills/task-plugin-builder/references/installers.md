# INSTALLERS — the one-double-click auto-installer

## Contents
- Bundle shape
- Target paths per host
- Adobe CEP — Mac installer (`INSTALL-MAC.command`)
- Adobe CEP — Windows installer (`INSTALL-WINDOWS.bat`)
- Adapting to other file-copy hosts
- README (always include, as the fallback)


The deliverable is always a folder the user double-clicks to install, on any Mac or PC, for
any username. This file has the tested scripts and the target paths per host. Copy them,
swap `PLUGIN-NAME` and the target path, and ship.

**Golden rules**
- Use path **variables** (`$HOME`, `%APPDATA%`) — never hardcode a username or computer name.
- **Replace on exist:** delete any old copy before copying the new one, so it doubles as an
  updater.
- **No admin/sudo** — target user-writable paths.
- Print a clear success message telling the user to restart the host and where to find the
  plugin.
- Keep **user data out of the plugin folder** (host storage / localStorage) so reinstalling
  never wipes presets.

---

## Bundle shape

```
PLUGIN-NAME-INSTALLER/
  INSTALL-MAC.command
  INSTALL-WINDOWS.bat
  PLUGIN-NAME/            ← the plugin, copied into place
    README.md            ← usage + manual-install fallback
```

Zip the **INSTALLER** folder, named `PLUGIN-NAME-V<version>-INSTALLER`, so the zip and
the folder inside it carry the same name and the same version. On Mac, `.command` files are double-click-runnable; if
Gatekeeper blocks the first run, the user right-clicks → Open once (note this in the README).

---

## Target paths per host

| Host | Mac | Windows |
|---|---|---|
| Adobe CEP (all apps) | `$HOME/Library/Application Support/Adobe/CEP/extensions/PLUGIN` | `%APPDATA%\Adobe\CEP\extensions\PLUGIN` |
| OBS scripts | `$HOME/Library/Application Support/obs-studio/basic/scripts/` | `%APPDATA%\obs-studio\basic\scripts\` |
| Blender add-ons (version X.Y) | `$HOME/Library/Application Support/Blender/X.Y/scripts/addons/` | `%APPDATA%\Blender Foundation\Blender\<X.Y>\scripts\addons\` |

For hosts with their own installer (Figma, VS Code `.vsix`, UXP), don't use a file-copy
installer — ship the host's package and document its one-click install (see hosts.md).

---

## Adobe CEP — Mac installer (`INSTALL-MAC.command`)

Enables unsigned panels, then copies the plugin. Swap `EASEUP` for the plugin name.

```bash
#!/bin/bash
clear
echo ""
echo "  ==== PLUGIN-NAME — INSTALLER ===="
echo ""
DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$DIR/PLUGIN-NAME"
if [ ! -d "$SRC/CSXS" ]; then
  echo "  x  Can't find the PLUGIN-NAME folder next to this installer."
  read -p "  Press Enter to close." d; exit 1
fi
echo "  [1/3]  Enabling unsigned panels..."
for v in 9 10 11 12; do defaults write com.adobe.CSXS.$v PlayerDebugMode 1 2>/dev/null; done
echo "         Done."
DEST="$HOME/Library/Application Support/Adobe/CEP/extensions"
mkdir -p "$DEST"
if [ -d "$DEST/PLUGIN-NAME" ]; then echo "  [2/3]  Replacing existing install..."; rm -rf "$DEST/PLUGIN-NAME";
else echo "  [2/3]  Installing..."; fi
cp -R "$SRC" "$DEST/PLUGIN-NAME"
if [ ! -d "$DEST/PLUGIN-NAME/CSXS" ]; then
  echo "  x  Copy failed. Try: sudo bash \"$0\""; read -p "  Press Enter to close." d; exit 1
fi
echo "  [3/3]  All set."
echo ""
echo "  Restart the Adobe app, then: Window > Extensions > PLUGIN-NAME"
echo ""
read -p "  Press Enter to close." d
```

Make it executable in the build: `chmod +x INSTALL-MAC.command`.

## Adobe CEP — Windows installer (`INSTALL-WINDOWS.bat`)

```bat
@echo off
cls
echo.
echo   ==== PLUGIN-NAME - INSTALLER ====
echo.
set "SRC=%~dp0PLUGIN-NAME"
if not exist "%SRC%\CSXS" (
  echo   X  Can't find the PLUGIN-NAME folder next to this installer.
  pause & exit /b 1
)
echo   [1/3]  Enabling unsigned panels...
for %%v in (9 10 11 12) do reg add "HKCU\Software\Adobe\CSXS.%%v" /v PlayerDebugMode /t REG_SZ /d 1 /f >nul 2>&1
echo          Done.
set "DEST=%APPDATA%\Adobe\CEP\extensions"
if not exist "%DEST%" mkdir "%DEST%"
if exist "%DEST%\PLUGIN-NAME" ( echo   [2/3]  Replacing existing install... & rmdir /s /q "%DEST%\PLUGIN-NAME" ) else ( echo   [2/3]  Installing... )
xcopy "%SRC%" "%DEST%\PLUGIN-NAME\" /e /i /q /y >nul
if not exist "%DEST%\PLUGIN-NAME\CSXS" ( echo   X  Copy failed. Try running as Administrator. & pause & exit /b 1 )
echo   [3/3]  All set.
echo.
echo   Restart the Adobe app, then: Window - Extensions - PLUGIN-NAME
echo.
pause
```

---

## Adapting to other file-copy hosts

Same two scripts, two changes:
1. Swap the `DEST` path (see the table above).
2. Drop the "enable unsigned panels" step if the host doesn't need it (only CEP does).

For OBS scripts and Blender add-ons the file lands in the right folder, but the user still
enables it once inside the app (Tools → Scripts / Preferences → Add-ons) — say so in the
README, and keep the installer as the file-placement step.

---

## README (always include, as the fallback)

Every plugin folder ships a `README.md` with: what it does, the one-double-click install
steps, the Gatekeeper right-click note for Mac, a **manual-install fallback** (the target
path + "copy the folder here, restart the app"), and a short troubleshooting list (panel not
appearing → re-run installer + restart; wrong nesting; minimum app version).
