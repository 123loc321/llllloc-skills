# Why each item is safe, with sources (checked 5 Nov 2026)

Full report: `llllloc/5_Research cache/deep research/reports/Mac deep clean for video editors.md`. Re-check a line older than 60 days, or a new macOS, Adobe or Maxon version, before you rely on it.

## Contents
- Findings
- Keep-clean settings to offer
- Tools
- Sources

## Findings
- **macOS itself is small on his Mac.** No local snapshots, swap 5 GB, logs 3.6 GB. System Data is a category, not a folder. The real fat is his own files and app data. Apple Intelligence on macOS 27 takes 14 to 30 GB and cannot be removed. CONFIRMED (Apple, Eclectic Light, his scan).
- **Local Time Machine snapshots** are the biggest surprise for most users (588 GB in one r/mac thread). Thin them in Disk Utility, keep the newest. `deletelocalsnapshots` on all of them broke one user's backups. Check with `tmutil listlocalsnapshots /` every run.
- **A huge Spotlight index** (174 GB in one thread) is fixed by a rebuild in System Settings > Spotlight. Its size needs admin rights to read: ask him if System Data is huge.
- **Adobe caches rebuild themselves.** After Effects disk cache, media cache, peak files, Media Encoder previews. Clear with the apps quit. Never empty `~/Library/Application Support/Adobe/Common` whole: it holds LUTs, MOGRTs and export presets. CONFIRMED (helpx.adobe.com).
- **AE "Clean Database & Cache" with media drives offline** treats offline footage as missing and drops its cache. Plug drives in first.
- **DirectOutFastDraftCapture.ae3d** is a draft capture file in AE's `logs`. Called "just a cache" by a senior forum member, not Adobe staff. LIKELY. It came back in 23.6 and 24.3, not in 26.x.
- **Old Creative Cloud versions** go through Creative Cloud only. Never drag to the Trash. "Remove older versions" does not remove versions already kept (open bug). CONFIRMED.
- **Maxon** says: uninstall in the Maxon App, or move the install folder to the Trash on macOS. Preferences stay per version. CONFIRMED (support.maxon.net).
- **DaVinci Resolve**: Playback > Delete Render Cache, or Preferences > User > Cache Management by age. Deleting CacheClip by hand shows Media Offline until the cache is cleared in the app. Keep `.gallery`, the audio folder and the Disk Database.
- **Electron apps** (Slack, Notion, Figma, Zalo, Opera, Comet): `Cache`, `Code Cache`, `GPUCache` rebuild. `Service Worker` is medium risk. Logins live in `Cookies`, `Local Storage`, `IndexedDB`: keep. Community-tools source only. LIKELY.
- **Developer caches** have their own commands: `brew cleanup`, `uv cache prune`, `npm cache verify`, `ollama rm`, `hf cache rm`. These delete for good: offer them to him to run, or move the folder to the Trash instead.
- **Claude**: `~/.claude` cleans itself after `cleanupPeriodDays` (30 by default). `vm_bundles` is the Cowork VM, safe to remove with no VM running, comes back as a 10 GB download.
- **Google Drive** clears its own cache. Hand clearing loses files not yet uploaded. Use Remove Download in Finder.
- **Docker.raw** shows a huge size but uses less on disk. Removing it broke one user's tool: only when Docker is unused.

## Keep-clean settings to offer
1. After Effects: Settings > Media & Disk Cache. Set a size limit.
2. Premiere: Settings > Media Cache > turn on automatic deletion (older than 90 days).
3. Resolve: Preferences > User > Cache Management, delete cache older than a set number of days.
4. Creative Cloud: Preferences > Apps > Remove previous versions after update.
5. A monthly run of this skill.

## Tools
- Built in first: Finder Calculate all sizes, System Settings > General > Storage, `du`, `df`.
- GrandPerspective, OmniDiskSweeper: free, read only. DaisyDisk: paid.
- Mole (tw93/mole): the 2026 community pick, but its clean step now empties the Trash by itself. Preview mode only.
- OnyX only from titanium-software.fr (fake support pages exist).
- Pearcleaner only from GitHub alienator88. pearcleaner.com is a fake that installs a password stealer. It once moved a Mail folder out of Application Support.
- Every tool needs his yes before install (core rule 1).

## Sources
- Adobe, memory and storage in After Effects: https://helpx.adobe.com/after-effects/desktop/memory-storage-performance/memory-and-storage/memory-storage1.html
- Adobe, clear media cache: https://helpx.adobe.com/premiere/desktop/troubleshooting/media-issues/clear-media-cache-using-preferences.html
- Adobe, automatic media cache: https://helpx.adobe.com/lv/premiere/desktop/troubleshooting/media-issues/automatically-manage-your-media-cache-files.html
- Adobe, uninstall Creative Cloud apps: https://helpx.adobe.com/download-install/apps/manage-installed-apps/uninstall-creative-cloud-apps.html
- Adobe community, remove older versions bug: https://community.adobe.com/t5/creative-cloud-desktop-bugs/remove-older-versions-doesnt-work/idi-p/15574425
- Adobe community, DirectOutFastDraftCapture.ae3d: https://community.adobe.com/questions-529/directoutfastdraftcapture-ae3d-file-size-is-too-large-43264
- Maxon, uninstall Cinema 4D on macOS: https://support.maxon.net/hc/en-us/articles/5551135016348-How-to-uninstall-Cinema-4D-on-macOS
- Maxon, uninstall products: https://support.maxon.net/hc/en-us/articles/212508807-How-do-I-uninstall-my-products
- Resolve 21 manual, render cache: https://www.imaster.org/docs/davinci-resolve-21-manual/part-2-setup-and-workflows/ch.-8-improving-performance,-proxies,-and-the-render-cache
- Apple, free up storage: https://support.apple.com/en-us/102624
- Eclectic Light, snapshots: https://eclecticlight.co/2026/09/09/take-control-of-snapshots/
- MacRumors, Apple Intelligence size on macOS 27: https://macrumors.com/2026/09/23/apple-intelligence-30gb-some-macs-macos-27
- Google, Drive for desktop cache: https://support.google.com/a/answer/7644837
- Ollama FAQ: https://docs.ollama.com/faq
- uv cache: https://docs.astral.sh/uv/concepts/cache/
- Docker Desktop Mac FAQ: https://docs.docker.com/desktop/troubleshoot-and-support/faqs/macfaqs/
- Claude Code, the .claude directory: https://code.claude.com/docs/en/claude-directory.md
- Mole V1.45.0: https://github.com/tw93/Mole/releases/tag/V1.45.0
- r/macapps, fake pearcleaner.com: https://www.reddit.com/r/macapps/comments/1ucstzy/psa_pearcleanercom_is_a_fake_site_pushing_macos/
- r/MacOS, rebuild Spotlight index: https://www.reddit.com/r/MacOS/comments/1vkyi1o/how_i_freed_180gb_on_macos_rebuild_spotlight_index/
- r/davinciresolve, clean your cache: https://www.reddit.com/r/davinciresolve/comments/1sxncre/psa_to_clean_out_your_cache/
- r/AfterEffects, project broke after a move: https://www.reddit.com/r/AfterEffects/comments/1o72u44/help_my_after_effects_project_disappeared_after/
