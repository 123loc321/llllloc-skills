---
name: tool-rclone
description: "How Claude moves files between Google Drive and his Mac with rclone and the Rclone UI app, for llllloc and the studio jobs. Never deletes, never mirrors without a dry run and his go."
---

# llllloc:tool-rclone (V2, 28 Oct 2026)

## TOP RULES
1. NEVER DELETE. Downloads use `copy`, never `sync`: sync deletes on the side it writes to. A mirror up to Drive moves every removed or replaced Drive file into `_DELETE/<date>` inside that Drive folder (`--backup-dir`). Never `rclone dedupe`, `delete`, `purge` or `cleanup`, above all on a client's Drive.
2. HE WATCHES BIG JOBS (his words, 28 Oct 2026: "but you didn't use the rclone ui?"). Start every job over a few GB through Rclone UI's engine (RC in DOWNLOAD), so it shows in Transfers. The maker's Rclone UI 3.7.5 hides a job until its first file finishes, and its Quit warning misses it, so quitting kills the job with no warning (28 Oct 2026). His build from `his-changes` (RCLONE-UI-LOC installer in `CODE/Apps/Rclone UI/`) fixes both. On the maker's build: tell him the job shows after its first file, and never ask him to quit or restart the app during a job. Terminal (`-P`) only when Rclone UI is closed, in a window he can see.
3. MIRROR = DRY RUN FIRST. Run `drive-mirror.sh ... --dry-run`, show what would upload and what would move to `_DELETE`, wait for his "go". A mirror runs only with a write remote, never from an unplugged drive or an empty folder (the script stops with "Nothing done").
4. HIS YES for: a Google sign-in (passwords are always his), ticking a Google policy or terms box, pressing Allow on a NEW permission (write access is bigger than read). His "do this for me" on 28 Oct 2026 covered those two logins only.
5. MEASURE BEFORE BLAMING. Slow job: `networkQuality -s` first. On 28 Oct 2026 the line fell from 160 Mbps (15:20) to 27 Mbps (18:10). No tool beats the line.
6. THE KEY NEVER LEAVES THE MAC. Client ID and secret live in `~/.config/rclone/llllloc-client.txt` (mode 600). Never in a note, a chat, a skill or the repo. Never print it.

## SETUP (28 Oct 2026)
| Thing | Where |
|---|---|
| rclone 1.75.2, official arm64 binary (Homebrew failed: portable Ruby could not reach GitHub) | `~/.local/bin/rclone`, checksum checked against `downloads.rclone.org/v<ver>/SHA256SUMS` |
| Accounts | `~/.config/rclone/rclone.conf`. `gd-studio` = <e-mail>, scope `drive.readonly` (all downloads). `gd-studio-write` = same account, scope `drive` (uploads, mirror) |
| Own Google key | Google Cloud project `llllloc-rclone` (org <your-domain>, work account). Auth Platform: External, In production, Drive API on, branding links <your-domain> and /privacy-policy, authorized domain <your-domain>. Desktop client `rclone mac` |
| Rclone UI 3.7.5 (signed, from github.com/rclone/rclone-ui releases) | `/Applications/Rclone UI.app`, uses the system rclone. Engine: `rcd --rc-no-auth` on `localhost:5572`. Settings: `~/Library/Application Support/com.rclone.ui/store.json`. On the weekly app check: `CODE/Apps/Rclone UI/source`, branch `his-changes`. His fixed build (Transfers fix, commit 233cb53, signed Apple Development, needs Rust in `~/.cargo`): `CODE/Apps/Rclone UI/RCLONE-UI-LOC-V1-INSTALLER/` |
| His scripts | `CODE/Scripts/Drive Download/` (map row in Project map_Code). `Drive Download.command` (also on his Desktop), `drive-download.sh`, `drive-mirror.sh`, `Add Google account.command`, `drive-id.zsh` |
| Logs | `~/Library/Logs/Drive Download/` |

Why our own key: rclone's shared key "will stop working during 2026" (rclone.org/drive). In Testing mode a sign-in expires after 7 days, so the app stays In production.

## TASKS
| He wants | Do |
|---|---|
| Download a Drive link | DOWNLOAD |
| Finish a slow Cyberduck download | Ask him to press Stop on the Cyberduck row. Then DOWNLOAD into the SAME folder: finished files are skipped, a half file is downloaded again whole |
| Watch or check a job | POST `localhost:5572/core/stats` (bytes, speed, transferring) and `job/status` |
| Upload or mirror a Mac folder | MIRROR |
| Another Google account | He double-clicks `Add Google account.command` (read-only `gd-<name>`), or Claude runs `rclone config create gd-<name> drive client_id=... client_secret=... scope=drive.readonly` from the key file and opens the printed `127.0.0.1:53682/auth` link in an Ego Lite Space where that account is signed in |
| Cyberduck instead | Its Transfers toolbar, Connections (hidden behind `»` in a narrow window): 10. Pref `queue.connections.limit`. 1 meant 0.85 MB/s |

## DOWNLOAD
1. Destination from the project map row and an `ls`. Never guessed (core rule 5).
2. Check the account sees it: `rclone size gd-studio: --drive-root-folder-id <ID> --json`. A Shared with me folder may be shared to another of his accounts and still open by ID.
3. Start it. RC (Rclone UI open, big job): POST `localhost:5572/sync/copy` with `{"srcFs":"gd-studio,root_folder_id=<ID>:","dstFs":"<dest folder>","_async":true,"_config":{"Transfers":8,"Checkers":16,"MultiThreadStreams":4,"UseListR":true,"Retries":5,"LowLevelRetries":20}}`, then `caffeinate -i -w <rcd pid> &`. Otherwise `drive-download.sh <link> gd-studio <parent folder>`.
4. CHECK after 20 s: `core/stats` shows speed and transfers. Zero: read `job/status` error and the log, fix, go back to step 3.
5. Reply: size, files, speed, where to watch. At the end `rclone check` one way: `0 differences`, or name each file.

`drive-download.sh` names the new folder from the top level of Shared with me or My Drive. A deeper folder gets its ID as the name, so give such a job its full destination path in step 3.

## MIRROR
1. Mac folder (`ls` it) and Drive folder link from him.
2. `drive-mirror.sh "<mac folder>" gd-studio-write "<drive link>" --dry-run`. Show the would-upload and would-move lists.
3. His go, then the same line without `--dry-run`. Hourly runs only on his word, as a launchd job that calls the same script.
4. CHECK: `rclone check "<mac folder>" gd-studio-write: --drive-root-folder-id <ID> --one-way --exclude "/_DELETE/**"`. Differences: go back to step 3.

## TRAPS
- Rclone UI never updates itself. Settings, General, "Tap to update" installs the maker's build over his fixed one: never tap it, never ask him to (28 Oct 2026).
- `rclone copy` keeps an unfinished file as `.partial` and renames it when complete. A restart downloads that file again from zero.
- Google Docs come down as Office files. `--drive-skip-gdocs` leaves them out.
- A Google Doc, Sheet or Slides shortcut (`.gdoc`, `.gslides`, 171 bytes) holds only a doc ID. `rclone backend copyid` and the Drive connector both give 404 or "not found" when the file is not shared to his account: no tool gets it, the owner must share it (7 Nov 2026). A folder opened by ID shows no name: read it with the Drive connector `get_file_metadata`.
- "Download quota exceeded" (403) locks one popular shared file for about 24 h. No tool gets past it: wait, or "Make a copy" in Drive. Uploads stop at about 750 GB a day per account.
- An Ego Lite Space ended with `task.finish` cannot be reused: open a new one. His logins carry over.
- A run can print `Promise { <pending> }` and still have worked: read the page or the result, never retry blind.
- One Drive file (7 Nov 2026): `copyto "gd-studio,root_folder_id=<ID>:<path>/<file>.png" <dest>.png` started copying the whole folder (1.1 GB) into a folder named like the png. Cause not found. First `rclone lsf` that exact path, then copy with `--max-transfer` just above the file size, and `ls` the result.
- Research: `llllloc/5_Research cache/deep research/reports/Google Drive multi account downloads.md`, lines in `llllloc/5_Research cache/platforms/cyberduck.md`.