# Ego Lite research scripts (tested 27 Oct 2026, ego lite 0.6.1.13, ego-browser guide v2.1.0)

Run on his Mac: `export PATH="$HOME/.local/bin:$PATH"`, then `ego-browser nodejs <<'EOF' ... EOF`. Each run is a new process: the Space and its page labels persist, variables do not. Resume a Space with `await taskSpace(<id>)`. Absolute paths only.

## Contents
1. Open a Space
2. Search YouTube, Reddit, X, Instagram
3. Read a whole Reddit post
4. A blocked page
5. Perplexity Deep Research
6. Close

## 1. Open a Space
```js
const task = await taskSpace("<question in a few words>"); console.log("space", task.spaceId);
const page = task.page("p1");
```

## 2. Search
```js
await page.goto("https://www.youtube.com/results?search_query=<words>"); await page.waitForTimeout(3000);
const yt = await page.evaluate(() => [...document.querySelectorAll("a#video-title")].slice(0,10).map(a=>({t:a.title, u:a.href})));
await page.goto("https://old.reddit.com/r/<sub>/search?q=<words>&restrict_sr=on&sort=top&t=year"); await page.waitForTimeout(3000);
const rd = await page.evaluate(() => [...document.querySelectorAll("a.search-title")].slice(0,10).map(a=>({t:a.innerText, u:a.href})));
await page.goto("https://x.com/search?q=<words>&f=top"); await page.waitForTimeout(5000);
const x = await page.evaluate(() => [...document.querySelectorAll('article [data-testid="tweetText"]')].slice(0,10).map(t=>t.innerText));
await page.goto("https://www.instagram.com/explore/tags/<tag>/"); await page.waitForTimeout(4000);
const ig = await page.evaluate(() => [...new Set([...document.querySelectorAll('a[href*="/p/"],a[href*="/reel/"]')].map(a=>a.href))].slice(0,12));
```
Reddit search as data, from a Reddit page: `await page.fetch("/r/<sub>/search.json?q=<words>&restrict_sr=1&sort=top&t=year&limit=10")`. A full link to another site fails on CORS.
YouTube words: `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs en --sub-format vtt -o "<scratch>/%(id)s.%(ext)s" "<link>"`. A frame: `page.evaluate(t => { const v=document.querySelector("video"); v.pause(); v.currentTime=t; }, <seconds>)`, wait 2 s, `page.screenshot({ path })`.

## 3. A whole Reddit post
From any reddit.com page: `const r = await page.fetch("<post link without the last slash>.json?limit=500")`, then `JSON.parse(r.body)`: `[0].data.children[0].data` is the post (`title`, `selftext`, `num_comments`), `[1].data.children` the comment tree (`data.body`, `data.replies`).

## 4. A blocked page
`await page.goto(url); await page.waitForTimeout(3000); const text = await page.evaluate(() => document.querySelector("main, article")?.innerText || document.body.innerText);`

## 5. Perplexity Deep Research
1. `goto("https://www.perplexity.ai/")`. 5 Nov 2026: "Add" and "Search" open no Deep Research menu any more. Click the box, type `/`: a list opens with the option "Deep Research" (Included in Pro). In the same run, read that option's box and `page.mouse.click(x, y)`: it has no ref, and `text=Deep Research` also matches old threads in the sidebar. Before sending, check the box shows the Deep Research chip. The 5 Nov run skipped that check and went out as a normal answer ("Finished 52s"). 6 Nov 2026: the "+" button ("Add files, plugins, and more") lists "Deep Research | Included in Pro", but a `.click()` from `evaluate` set nothing and the run again finished as a normal answer ("Finished 37s"). Use a real `page.mouse.click` on the option's box, then the chip check. A run that finishes under 2 minutes was not Deep Research: say so in the PERPLEXITY line.
2. Click the question box (a textfield, "Ask anything"), `page.keyboard.insertText("<question>")`, `page.keyboard.press("Enter")`, `page.waitForURL(/\/search\//)`. Print the URL: it resumes the run.
3. Wait in a later round: every 15 s read `document.querySelector("main").innerText.length`; done when it stops growing three times and no Stop button shows. About 7 min.
4. Open the report: the card "Deep research report". A normal click is blocked by a cover button: find the text node, `scrollIntoView`, read its box, `page.mouse.click(x, y)`.
   31 Oct 2026: a run can finish as a plain answer page with no card and no Download. Then save `main` text plus its links, and say so.
5. Snapshot, click the button "Download", then the menu item "Download as Markdown". Arm the wait first: `const dl = page.waitForEvent("download", { timeout: 30000 })`, click, `const d = await dl; await d.saveAs("<absolute path>.md")`. Also there: DOCX, PDF. No Download button (6 Nov 2026): the button "Session options" holds "Export as Markdown", same download wait. A wait loop with `ego-browser nodejs -e` lost its quotes and printed nothing: poll with the heredoc form.

## 6. Close
`await task.finish({ keep: [] })` once, last. A run that stopped on an error: resume the same Space, never open a new one.
