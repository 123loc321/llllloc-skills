---
name: task-web-publish
description: "His standard way to put a website, web game or app online, or update one: Cloudflare Pages drag and drop on the free plan. Claude prepares and tests the folder, he uploads."
---

# llllloc:task-web-publish (20 Oct 2026)

His words, 20 Oct 2026: "please remember this website publishing method, we will always use this in the future". The method is Cloudflare Pages, Direct Upload (drag and drop), on the free plan. Claude prepares and tests. He uploads, because it needs his Cloudflare login.

## TOP RULES
1. He uploads, Claude never does. Why: core hard stop 1 (never publish) and his account login. His ask to publish is the go for preparing the folder, not for touching his account.
2. Client work is locked. Why: a pages.dev link is public, and client names and data leak with it. The folder gets the noindex line, and the reply gives the Access lock steps (STEP 4). He can say "public" to skip the lock.
3. The project name never holds the client's name. Why: the name becomes the web address (`<name>.pages.dev`). Suggest a neutral name, like `beauty-tech-level-up`.
4. Not live until he sends the link. "Ready to upload" is the finished answer before that (core hard stop 4).
5. Never Cloudflare Drop (cloudflare.com/drop) for a site he keeps. Why: an unclaimed Drop site is deleted after 60 minutes.

## STEPS
```
- [ ] 1 Upload folder built in the job folder
- [ ] 2 Tested over a local web server
- [ ] 3 Folder on his Mac, path in the reply
- [ ] 4 Steps sent: upload, update, lock
- [ ] 5 Live link saved (after he sends it)
```

1. **Build the folder.** `WEB_Cloudflare/` beside the build in the job's own code folder (never in llllloc). Two sites in one code folder: one folder each, `WEB_Cloudflare_<Site>/` (23 Oct 2026). The start page is named `index.html`. Every file the page needs sits inside, linked by relative paths. Outside libraries from cdn.jsdelivr.net or cdnjs work as they are. For client work add `<meta name="robots" content="noindex, nofollow">` after the viewport line. Limits for drag and drop: 1,000 files, 25 MB per file. Over a limit: shrink or split the file, then check again. A Godot web game ships as a small `index.html` plus the wasm and pck pre-gzipped as `.gz.bin` files (`pack_cloudflare.py` in `G1 Jump-Run Godot/`), never as one big page: a 23 MB one-file page gave HTTP 500 on Cloudflare (24 Oct 2026).
2. **Test it.** Serve the folder with `python3 -m http.server` and open it in headless Chromium (Playwright). Pass: no page error, the start screen shows, its main button works with a real click. A fail: fix the build, go back to step 1. Say "not tested" if this step did not run. A Godot or other WebGL game (23 Oct 2026, proved on Beauty Isle V4): launch with `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`, viewport 640x360, wait 60 s before the first screenshot, screenshot timeout 120 s. 1280x720 times out in software GL.
3. **Deliver** with `llllloc:task-sending-files`: the folder on his Mac, the copyable Mac path first in the reply.
4. **Send the steps**, numbered, in his words:
   - Upload: dash.cloudflare.com, log in or make a free account. **Workers & Pages**, **Create application**, **Get started**, **Drag and drop your files**. Type the project name, drag in the whole `WEB_Cloudflare` folder, **Deploy site**. The link is `https://<name>.pages.dev`.
   - Update later: open the project, **Create a new deployment**, drag the folder in again. The link stays the same.
   - Lock (client work): **Zero Trust**, **Access**, **Applications**, **Add an application**, **Self-hosted**. Domain `<name>.pages.dev`, subdomain `*`. Policy **Allow**, **Emails ending in** `@<your-domain>` plus the client's domain. Visitors get a one-time code by email. Free up to 50 people.
   A button name he reports as different: search the Cloudflare docs, fix the step here (skill-creator REFINE), then answer.
5. **Save the link.** When he sends it: the job's map row (core rule 16) and the job's STATE file, with the date.

## FACTS (checked 20 Oct 2026)
- Free plan: unlimited visits and data for static files, 20,000 files per site. Sources: developers.cloudflare.com/pages/get-started/direct-upload/ and flaviocopes.com/hosting-free-tiers.md (Sept 2026).
- Pages is still fully supported in 2026. Workers static assets suit sites with server code, which these jobs do not have.
- A Godot web export with threads off (GODOT_THREADS_ENABLED false) needs no COOP/COEP headers or `_headers` file (23 Oct 2026).
- A fact over 60 days old, or a page that looks different from these steps: search again first (core rule 10).