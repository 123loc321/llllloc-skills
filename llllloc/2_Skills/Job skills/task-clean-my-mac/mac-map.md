# His Mac: where the fat lives (measured 5 Nov 2026)

## Contents
- SAFE: rebuilds itself or is a checked duplicate
- HIS CALL: ask first
- KEEP: never offer
- ADOBE: old versions
- MAXON: old Cinema 4D
- GOOGLE DRIVE
- TRAPS on his Mac

Sizes are from 5 Nov 2026. Measure again every run.

## SAFE (rebuilds itself or is a checked duplicate)
| What | Path | Size seen | How |
|---|---|---|---|
| After Effects debug capture | `~/Library/Preferences/Adobe/After Effects/<ver>/logs/DirectOutFastDraftCapture.ae3d` | 11.4 GB (25.4), 1.4 GB (24.3) | Trash the file. AE quit. |
| AE settings of versions not installed | `~/Library/Preferences/Adobe/After Effects/<ver>` | 0.4 GB | Trash the folder if no AE of that year is in `/Applications` |
| After Effects disk cache (his custom place) | `~/Desktop/Cache/Adobe/After Effects`, `~/Desktop/Cache/Media Cache Files`, `~/Desktop/Cache/Peak Files` | 9 GB | AE closed: trash the folders, `mkdir -p` them again. Or AE > Settings > Media & Disk Cache > Empty |
| Adobe media cache | `~/Library/Application Support/Adobe/Common/Media Cache Files`, `Media Cache`, `Peak Files` | 2.6 GB | Never the whole `Common` folder: it holds LUTs and MOGRTs |
| Media Encoder audio previews | `~/Documents/Adobe/Adobe Media Encoder/Adobe Adobe Media Encoder Audio Previews` | 11 GB | Media Encoder closed |
| Premiere cache | `~/Library/Caches/com.adobe.PremierePro.<ver>` | 1 GB | Premiere closed |
| Premiere, Animate user folders of versions not installed | `~/Documents/Adobe/Premiere Pro/<ver>`, `~/Library/Application Support/Adobe/Animate <year>` | 1.7 GB | Check `/Applications` first |
| Blender settings of old versions | `~/Library/Application Support/Blender/<ver>` | 5.7 GB | Keep the installed version's folder (`defaults read /Applications/Blender.app/Contents/Info.plist CFBundleShortVersionString`) |
| Electron app caches | `Cache`, `Code Cache`, `GPUCache` inside Notion, Figma (`DesktopProfile/v<newest>`), Zalo, Slack | 3 GB | App quit. Never `Cookies`, `Local Storage`, `IndexedDB` |
| Old Figma profiles | `~/Library/Application Support/Figma/DesktopProfile/v<older>` | 0.3 GB | Keep the newest `v` |
| Capture One cache | `~/Library/Caches/com.captureone.captureone16` | 0.9 GB | Capture One quit |
| Opera data | `~/Library/Application Support/com.operasoftware.Opera` | 9 GB | Opera is unused (Ego Lite is his browser, core rule 12) |
| Installers of installed apps | `~/Downloads/*.dmg`, `*.zip`, BorisFX, Capture One | 8 GB | Check the app is in `/Applications`. Downloads only, never a job folder |
| `_DELETE` folders outside client jobs | `CODE/**/_DELETE`, `~/Desktop/Claude/**/_DELETE`, `~/Downloads/_DELETE`, `~/Desktop/Scheduled tasks_*/*/_DELETE`, `~/Movies/MOTION/_DELETE` | 13 GB | Contents only. Never a client job's `_DELETE` |
| Code build output | `CODE/Apps/*/source/build`, `src-tauri/target`, `.build` | 7 GB | Rebuilt by the next build |
| Old installers of his apps | `CODE/Apps/MOTION App/_CLAUDE/4_Builds/Old/MOTION-V0.<old>-INSTALLER*` | 4 GB | Keep the newest two. Never Phosphene, SuperIsland, Rclone UI or COTABBY restore points |
| Old Claude temp | `/private/tmp/claude-<uid>/<project>/<session>` | 18 GB | Only folders with nothing changed in 1 day. Never this session's |
| Apps not installed any more | `~/Library/Application Support/<App>` (Spotify, dolphin_anty) | 1.2 GB | `ls /Applications` and `list_apps` first |
| Fonts (Removed), `.thumbnails` | `~/Library/Fonts (Removed)`, `~/.thumbnails` | 1 GB | |

## HIS CALL (ask first)
| What | Path | Size | Who uses it |
|---|---|---|---|
| Finished jobs on the Desktop | `~/Desktop/PERSONAL PROJECT/*/*` | 355 GB | A MOVE to an archive drive, never a delete: `llllloc:task-files-organize`, on his word. He skipped it on 5 Nov 2026 |
| Unreal Engine | `/Users/Shared/Epic Games/UE_<ver>` | 43 GB | Unreal connector. Removed 5 Nov 2026 |
| SELECTS previews | `~/Library/Application Support/SELECTS/Previews` | 28 GB | SELECTS rebuilds them slowly. Removed 5 Nov 2026 |
| Krotos library | `/Library/Application Support/Krotos/Krotos Studio/Factory Assets`, `/Applications/Krotos` | 24 GB | Krotos Studio plugin. Removed 5 Nov 2026 |
| Ollama models | `~/.ollama/models` (`ollama list`) | 22 GB | KEEP `qwen3.6`: Cotabby Rewrite. Remove only with `ollama rm` |
| ComfyUI models | `~/ComfyUI-Shared/models` | 19 GB | His ComfyUI jobs |
| Claude Cowork VM | `~/Library/Application Support/Claude/vm_bundles/claudevm.bundle` | 15 GB | Comes back as a 10 GB download. Only with no VM process running |
| Docker | `/Applications/Docker.app`, `~/Library/Containers/com.docker.docker` | 8 GB | macOS blocks the Containers folder: he drags it |
| Filestage downloads | `~/Library/Application Support/filestagemedia/*.mp4` | 6 GB | Client videos of an app no longer installed |
| MacWhisper history | `~/Library/Application Support/MacWhisper/Database` | 3.5 GB | His transcripts |
| Plugin data | Aniom, MisterHorse, Blace Plugins, BorisFX, Red Giant | 30 GB | Only if the plugin is gone |

## KEEP (never offer)
- Everything inside a client project folder (TOP RULE 3): `OLD VERSIONS` renders, job media, final renders, a job's `_DELETE` folders (his edit may still use them, he empties them himself), unpacked zips. Report their sizes as info only.
- `~/.cache/whisper` (subtitle pipeline), Cotabby `LlamaRuntime` models, Comet (the comet-bridge connector uses it), Xcode (his app builds), Ego Lite data.
- `4_Builds/Old` of Phosphene, SuperIsland, Rclone UI, COTABBY: restore points.
- Cookies, Keychains, Mail, Messages, `~/Library/Containers` of apps in use, anything under `/System` or `/private/var/db`.
- `~/.claude` (Claude Code cleans it by `cleanupPeriodDays`), the brain folder.

## ADOBE: old versions
1. Every installed version has a record: `ls "/Library/Application Support/Adobe/Uninstall/"` (`AEFT_25_6_6_32.app`, `AME_24_...`, `AUDT_...`, `KBRG_...`, `AMEBETA_...`).
2. Start one at a time: `open -n "/Library/Application Support/Adobe/Uninstall/<record>.app"`. A plain `open` while another one runs does nothing.
3. The question shows in the Creative Cloud app. Grant it with `request_access` on bundle id `com.adobe.acc.AdobeCreativeCloud` (the name "Creative Cloud" fails; find ids with `list_apps`). A first record may show its own "Adobe Installer" window (`com.adobe.HDInstall`).
4. Pick **Remove** for the old version's preferences. The 2026 apps keep theirs.
5. Wait until the row says Waiting or Uninstalling, then start the next. Media Encoder 2024 asked for his Mac password once.
6. A version with no record (Photoshop 2024 and 2025, Premiere 2024, After Effects Beta on 5 Nov 2026) is an empty shell or leftover `Plug-ins`: trash the folder with `scripts/trash.sh` (Finder asks his password once for root-owned folders).
7. In the Creative Cloud side list, a hover does not show the three dots while keyboard focus sits on another row. Use Shift + Tab to move focus, then the arrow keys and Return in the menu. DockDoor Pro covers the lower menu items: use keys.

## MAXON: old Cinema 4D
The Maxon App 2025.4.2 should offer Products > three dots > Uninstall. With no licence it shows only "Discover More". Then use Maxon's manual route: trash `/Applications/Maxon Cinema 4D <old>` (Finder asks his password) and the matching `~/Library/Preferences/Maxon/Maxon Cinema 4D <old>_<id>` folders. Quit the Maxon App first. Keep the newest version.

## GOOGLE DRIVE
- A folder in `~/Library/CloudStorage` whose name ends with a date, like `GoogleDrive-<mail> (25-10-26 01:03)`, is a copy left after Drive disconnected. `fileproviderctl evaluate <path>` answers "No item". It cannot be made online only.
- Before trashing it, prove each file exists elsewhere with the same size (`find <job folder> -name <name> -size <bytes>c`). On 5 Nov 2026 all 40 a client clips were on the CREATIVE drive.
- A live Drive folder: tell him to right-click > Remove Download in Finder. Never clear the DriveFS cache by hand: unsent uploads are lost.

## TRAPS on his Mac
- Finder `delete (POSIX file p as alias)` follows a symlink and trashes the TARGET (5 Nov 2026: `~/.agents/skills/agent-reach`). trash.sh moves links itself.
- A file in a `_DELETE` folder can still be linked in a Premiere edit (5 Nov 2026: 14 the studio Showreel clips went offline).
- `ls ~/.Trash` is refused (privacy), but direct paths `~/.Trash/<name>` work: put_back.sh uses them.
- Finder's "every item of trash whose name is" takes about a minute per item on a full Trash.
- A scan line that greps a whole After Effects Prefs file prints 1 MB of text. scan.sh skips it.
- His screen has three monitors and the Dock is hidden. Computer use prefers full-screen control. Release it before he types a password.
