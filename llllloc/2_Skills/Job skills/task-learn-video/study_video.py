#!/usr/bin/env python3
"""study_video.py - turn one video into study material: transcript, frames, on-screen text, index, contact sheets.

Runs on his Mac with what is already there: yt-dlp, ffmpeg 9, python3, swiftc (Apple's text reader). No Python packages.
Everything lands in one batch folder and nothing is deleted. Rerunning skips the parts already on disk.

  python3 study_video.py study "<youtube url or local file>" --out "<batch folder>"
      [--lang en] [--height 1080] [--max-frames 240] [--floor 20] [--cookies opera] [--whisper] [--words words.txt]
  python3 study_video.py zoom "<frames/f_HHMMSS.png>" x y w h [--scale 2]        # a crop at 2x, to read small text
  python3 study_video.py check "<LESSON.md>" --batch "<batch folder>"            # every step has a time and a frame

Batch folder after `study`:
  info.json, description.txt, links.txt      what YouTube knows: title, chapters, captions, links in the text
  captions/*.vtt, transcript.txt, cues.json  the speech with times ([m:ss] blocks; cues keep start and end)
  video.mp4                                  the copy frames are cut from
  _thumbs/t_NNNNN.pgm, change_maps.json      per second: a grey thumbnail, and how many pixels moved in each 16x9 cell (kept)
  frames/f_HHMMSS.png                        the kept frames at full size (HHMMSS = the time in the video)
  index.json, index.md                       one row per frame: time, why kept, text on screen, what was said
  sheets/sheet_NN.jpg                        contact sheets, 12 frames each, the time on every tile
  STUDY_READY.md                             counts, timings, chapters, links, what failed

Install once (ask him first): brew install yt-dlp ffmpeg deno. Whisper fallback uses the openai-whisper already on the Mac.
"""
import argparse, glob, html, json, os, re, shutil, subprocess, sys, time

# --- constants, each with its reason ---------------------------------------------------------
DIFF_W, DIFF_H = 480, 270    # the size at which one second is compared with the next: a 12 px value at 1080p is still 3 px here
GRID_W, GRID_H = 16, 9       # the changed pixels are counted per 30x30 cell: a typed value or a moved curve point fills one cell, a whole-frame mean hides it
NOISE = 20                   # a pixel counts as changed when its grey value moves more than this (compression noise stays under it)
CUT_FRAC = 0.35              # this share of all pixels changed at once is a cut or a new panel
CELL_PX = 5                  # changed pixels in one cell that mean a local change (a digit at 1080p is about 6 to 8 of them here)
SETTLE_PX = 3                # a changed cell has settled when the next second moves fewer pixels in it (a playing viewer never settles)
DRAG_MAX = 10                # a cell that moved for up to this many seconds and then stops was a drag: keep its end state
LOCAL_CELLS = 12             # more moving cells than this the second before is a moving picture, not a control being changed
QUIET_S = 3   # a cell must have been still this many seconds before it counts as a change (kills flicker)
MIN_CHANGE_PX = 15   # a new change must move at least this many pixels of its 30x30 cell (a digit is 20 to 80; an edge shimmer is under 12)
SAME_MAD = 1.5               # mean grey difference under this on the 160x90 thumbnails: the same picture (dedup against the last kept)
THUMB_W, THUMB_H = 160, 90   # grey thumbnails kept per second for that dedup
WINDOW = 4                   # a kept frame is compared with the last 4 kept, so a cutaway and back is not kept twice
FLOOR_DEFAULT = 20           # seconds with no kept frame -> keep one anyway, so slow talk still has a picture
VALUE_WORDS = re.compile(r"\d|percent|value|set |slider|node|setting|click|drag|type|enter|paste|turn", re.I)
SHEET_COLS, SHEET_ROWS, TILE_W, TILE_H = 3, 4, 480, 270   # 12 tiles a sheet at 480 px: an overview, never for reading values
FONT = next((f for f in ["/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc",
                         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"] if os.path.exists(f)), None)
HERE = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(msg, flush=True)
def run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
def hhmmss(sec): sec = int(round(sec)); return f"{sec//3600:02d}{(sec%3600)//60:02d}{sec%60:02d}"
def mmss(sec):
    sec = int(round(sec)); return f"{sec//60}:{sec%60:02d}" if sec < 3600 else f"{sec//3600}:{(sec%3600)//60:02d}:{sec%60:02d}"

# --- step 1: what YouTube knows -----------------------------------------------------------------
def fetch_info(src, out, cookies):
    """yt-dlp metadata as JSON. A local file gets a small info.json from ffprobe."""
    path = os.path.join(out, "info.json")
    if os.path.exists(path): return json.load(open(path))
    if os.path.exists(src):
        p = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", src])
        dur = float(json.loads(p.stdout or "{}").get("format", {}).get("duration", 0) or 0)
        info = {"id": os.path.splitext(os.path.basename(src))[0], "title": os.path.basename(src), "duration": dur, "webpage_url": src,
                "chapters": [], "subtitles": {}, "automatic_captions": {}, "description": "", "local": True}
    else:
        cmd = ["yt-dlp", "--dump-single-json", "--no-download"] + (["--cookies-from-browser", cookies] if cookies else []) + [src]
        p = run(cmd)
        if p.returncode != 0:
            last = (p.stderr.strip().splitlines() or [str(p.returncode)])[-1]
            raise SystemExit(f"INFO FAILED: {last}\nA bot check: run again with --cookies opera (his Opera login). Still blocked: name the gap.")
        info = json.loads(p.stdout)
    json.dump(info, open(path, "w"), indent=1, ensure_ascii=False)
    desc = info.get("description") or ""
    open(os.path.join(out, "description.txt"), "w").write(desc)
    open(os.path.join(out, "links.txt"), "w").write("\n".join(sorted(set(re.findall(r"https?://[^\s)\]>\"']+", desc)))))
    return info

# --- step 2: the speech ------------------------------------------------------------------------
def vtt_cues(path):
    """WebVTT -> [(start, end, text)], dropping the rolling repeats YouTube auto-captions carry and the word tags."""
    cues, last = [], []
    for block in re.split(r"\n\s*\n", open(path, encoding="utf-8").read()):
        m = re.search(r"(\d+):(\d+):(\d+)[.,](\d+)\s+-->\s+(\d+):(\d+):(\d+)[.,](\d+)", block)
        if not m: continue
        g = [int(x) for x in m.groups()]
        start, end = g[0]*3600+g[1]*60+g[2]+g[3]/1000, g[4]*3600+g[5]*60+g[6]+g[7]/1000
        for line in block.splitlines():
            if "-->" in line: continue
            line = re.sub(r"<[^>]+>", "", line); line = re.sub(r"\s+", " ", html.unescape(line)).strip()
            if not line or line in last: continue
            cues.append((start, end, line)); last = (last + [line])[-3:]
    return cues

def write_transcript(out, info, cues, kind):
    blocks, buf, first = [], "", None
    for s, e, t in cues:
        if first is None: first = s
        buf += t + " "
        if len(buf) > 400: blocks.append(f"[{mmss(first)}] {buf.strip()}"); buf, first = "", None
    if buf.strip(): blocks.append(f"[{mmss(first or 0)}] {buf.strip()}")
    open(os.path.join(out, "transcript.txt"), "w").write(f"# {info.get('title')} - speech source: {kind}\n" + "\n".join(blocks))
    json.dump([{"start": s, "end": e, "text": t} for s, e, t in cues], open(os.path.join(out, "cues.json"), "w"))

def fetch_captions(src, info, out, lang, cookies):
    cdir = os.path.join(out, "captions"); os.makedirs(cdir, exist_ok=True)
    if not info.get("local") and not glob.glob(os.path.join(cdir, "*.vtt")):
        cmd = ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", f"{lang}.*,{lang},-live_chat",
               "--sub-format", "vtt", "-o", os.path.join(cdir, "%(id)s.%(ext)s")] + (["--cookies-from-browser", cookies] if cookies else []) + [src]
        p = run(cmd)
        if p.returncode != 0: log("captions: yt-dlp said " + (p.stderr.strip().splitlines() or ["?"])[-1])
    manual = list((info.get("subtitles") or {}).keys())   # the languages the maker wrote by hand (en-GB, en): better than YouTube's auto text
    is_manual = lambda f: any(f".{l}." in os.path.basename(f) for l in manual)
    files = sorted(glob.glob(os.path.join(cdir, "*.vtt")), key=lambda f: (not is_manual(f), "orig" in f, "whisper" in f, len(f)))
    if not files: return [], "none"
    kind = "whisper" if "whisper" in files[0] else "manual captions" if is_manual(files[0]) else "auto captions"
    cues = vtt_cues(files[0]); write_transcript(out, info, cues, kind)
    return cues, kind

def whisper_fallback(video, out, info):
    """openai-whisper CLI on the Mac (large-v3-turbo is on disk, about 3x real time). Word times can stretch over silence: ~."""
    if not shutil.which("whisper"): return [], "none (no captions; whisper not on PATH)"
    cdir = os.path.join(out, "captions"); audio = os.path.join(out, "audio.m4a")
    if not os.path.exists(audio): run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", audio])
    t0 = time.time()
    p = run(["whisper", audio, "--model", "large-v3-turbo", "--output_format", "vtt", "--output_dir", cdir, "--language", "en", "--fp16", "False"])
    vtt = os.path.join(cdir, "audio.vtt")
    if not os.path.exists(vtt): return [], "none (whisper failed: " + (p.stderr.strip().splitlines() or ["?"])[-1] + ")"
    os.replace(vtt, os.path.join(cdir, "whisper.vtt")); log(f"whisper: {time.time()-t0:.0f} s")
    cues = vtt_cues(os.path.join(cdir, "whisper.vtt")); write_transcript(out, info, cues, "whisper large-v3-turbo"); return cues, "whisper"

# --- step 3: the picture -----------------------------------------------------------------------
def fetch_video(src, out, height, cookies):
    if os.path.exists(src): return src
    target = os.path.join(out, "video.mp4")
    if os.path.exists(target): return target
    fmt = (f"bv*[height<={height}][vcodec^=avc1]+ba[ext=m4a]/bv*[height<={height}][ext=mp4]+ba[ext=m4a]/"
           f"b[height<={height}]/bv*[height<={height}]+ba/b")   # H.264 first: every tool opens it; AV1 only as a fallback
    cmd = ["yt-dlp", "-f", fmt, "--merge-output-format", "mp4", "-o", target] + (["--cookies-from-browser", cookies] if cookies else []) + [src]
    t0 = time.time(); p = run(cmd)
    if p.returncode != 0 or not os.path.exists(target): raise SystemExit("VIDEO FAILED: " + (p.stderr.strip().splitlines() or ["?"])[-1])
    log(f"video: {os.path.getsize(target)//1_000_000} MB in {time.time()-t0:.0f} s"); return target

def read_pgm(path):
    """Binary PGM (P5) from ffmpeg -> (w, h, bytes of grey values)."""
    data = open(path, "rb").read(); parts = data.split(maxsplit=4)
    if parts[0] != b"P5": raise ValueError(path)
    w, h = int(parts[1]), int(parts[2]); return w, h, data[-w*h:]

def mad(a, b): return sum(x - y if x > y else y - x for x, y in zip(a, b)) / len(a)

def change_maps(video, tdir):
    """One ffmpeg pass per second: grey thumbnails to files, and the difference with the second before (pixels moved more than
    NOISE, as 0 or 255) streamed through a pipe and counted per cell here. Nothing big touches the disk. Saved as change_maps.json."""
    cache = os.path.join(tdir, "change_maps.json")
    if os.path.exists(cache):
        maps = json.load(open(cache))
        if any(any(r) for r in maps): return maps
        log("change maps: the cached maps are all zero, counting again")
    fc = (f"[0:v]fps=1,format=gray,split[a][b];[a]scale={THUMB_W}:{THUMB_H}[s];"
          f"[b]scale={DIFF_W}:{DIFF_H},tblend=all_mode=difference,lutyuv=y='gt(val,{NOISE})*255'[d]")
    cmd = ["ffmpeg", "-v", "error", "-i", video, "-filter_complex", fc, "-map", "[s]", os.path.join(tdir, "t_%05d.pgm"),
           "-map", "[d]", "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE); maps = []; size = DIFF_W * DIFF_H
    cw, ch = DIFF_W // GRID_W, DIFF_H // GRID_H
    # a changed pixel comes out as 255, or as 235 when ffmpeg converts the grey through a video-range step (ffmpeg 9 on the Mac
    # did that, and an exact count of 255 found nothing). Anything over 127 is a changed pixel.
    bright = bytes.maketrans(bytes(range(256)), bytes([0] * 128 + [1] * 128))
    while True:
        buf = proc.stdout.read(size)
        if len(buf) < size: break
        if len(maps) == 1: log(f"change maps: raw difference values seen in second 1: {sorted(set(buf))[:6]}")   # 0 and 255, or 16 and 235
        buf = buf.translate(bright); cells = [0] * (GRID_W * GRID_H)
        for y in range(DIFF_H):
            row = buf[y * DIFF_W:(y + 1) * DIFF_W]; cy = min(y // ch, GRID_H - 1)
            if row.count(1) == 0: continue
            for cx in range(GRID_W): cells[cy * GRID_W + cx] += row[cx * cw:(cx + 1) * cw].count(1)
        maps.append(cells)
    err = proc.stderr.read().decode(errors="replace"); proc.wait()
    if not maps: raise SystemExit("change maps failed: " + err.strip())
    json.dump(maps, open(cache, "w")); return maps

def pick_frames(video, out, cues, floor, max_frames):
    """One second at a time. Keep a frame on a cut, a settled local change, a spoken value, or the floor."""
    tdir = os.path.join(out, "_thumbs"); os.makedirs(tdir, exist_ok=True); t0 = time.time()
    dmaps = change_maps(video, tdir)
    thumbs = [read_pgm(f)[2] for f in sorted(glob.glob(os.path.join(tdir, "t_*.pgm")))]
    n = min(len(thumbs), len(dmaps)); npx = DIFF_W * DIFF_H
    if n == 0: raise SystemExit("no thumbnails: ffmpeg could not read the video")
    log(f"change maps: {n} seconds in {time.time()-t0:.0f} s")
    anchors = {int(s) + 1 for s, e, t in cues if VALUE_WORDS.search(t)}   # one second after a value is spoken, the screen shows it
    kept, last_keep = [], -10**9
    def same_as_recent(t): return any(mad(thumbs[t], thumbs[k["t"]]) <= SAME_MAD for k in kept[-WINDOW:])
    def keep(t, reason, score):
        nonlocal last_keep; kept.append({"t": t, "reason": reason, "score": round(score, 1)}); last_keep = t
    keep(0, "first", 0); t = 1; cells = GRID_W * GRID_H
    streak = [0] * cells   # seconds in a row each cell has been moving
    cold = [0] * cells   # seconds each cell has been still (the first frame is kept anyway)
    pre = [0] * cells   # how still the cell was before its current run started
    while t < n:
        d = dmaps[t]; changed = sum(d); reason, score = None, 0
        hot = [c for c, v in enumerate(d) if v >= CELL_PX]
        if changed >= CUT_FRAC * npx: reason, score = "cut", 100 * changed / npx
        else:
            # a local change is a cell that was still for QUIET_S seconds, moves, and holds still the next second (a value typed,
            # a node added), or such a cell that stops after a short run (the end of a drag). A cell that moves all the time or
            # flickers (a playing viewer, a talking head, a blinking cursor) is never a change: the floor covers those.
            new = [c for c in hot if d[c] >= MIN_CHANGE_PX and streak[c] == 0 and cold[c] >= QUIET_S and (t + 1 >= n or dmaps[t+1][c] < SETTLE_PX)]
            ended = [c for c in range(cells) if 2 <= streak[c] <= DRAG_MAX and pre[c] >= QUIET_S and d[c] < SETTLE_PX and dmaps[t-1][c] >= MIN_CHANGE_PX]
            busy = sum(1 for v in streak if v > 0)   # cells moving the second before: many means a picture, not a control
            if new: reason, score = "change", max(d[c] for c in new)
            elif ended and busy <= LOCAL_CELLS: reason, score = "change", max(dmaps[t-1][c] for c in ended)
        if not reason and t in anchors and t - last_keep >= 3: reason, score = "spoken value", changed
        if not reason and t - last_keep >= floor: reason, score = "floor", changed
        if reason == "cut" and same_as_recent(t): reason = None   # the same picture came back (a cutaway). A local change is never deduped: it is almost the same picture by nature
        if reason: keep(t, reason, score)
        for c, v in enumerate(d):
            if v >= CELL_PX:
                if streak[c] == 0: pre[c] = cold[c]
                streak[c] += 1; cold[c] = 0
            else: streak[c] = 0; cold[c] += 1
        t += 1
    if kept[-1]["t"] != n - 1: keep(n - 1, "last", 0)
    if len(kept) > max_frames:   # thin floor frames first, then the weakest changes; never cuts, spoken values, first or last
        rank = {"floor": 0, "change": 1, "spoken value": 2, "cut": 3, "first": 4, "last": 4}
        order = sorted(kept, key=lambda k: (rank[k["reason"]], k["score"]))
        drop = {id(k) for k in order[:len(kept) - max_frames]}; kept = [k for k in kept if id(k) not in drop]
    fdir = os.path.join(out, "frames"); os.makedirs(fdir, exist_ok=True); t0 = time.time()
    for k in kept:
        k["file"] = f"frames/f_{hhmmss(k['t'])}.png"; path = os.path.join(out, k["file"])
        if not os.path.exists(path): run(["ffmpeg", "-v", "error", "-ss", str(k["t"]), "-i", video, "-frames:v", "1", path])
    log(f"frames kept: {len(kept)} of {n} seconds ({sum(1 for k in kept if k['reason']=='cut')} cuts, "
        f"{sum(1 for k in kept if k['reason']=='change')} changes), cut at full size in {time.time()-t0:.0f} s")
    return kept

# --- step 4: the words on the screen ------------------------------------------------------------
def ocr_binary():
    """Apple Vision through vision_ocr.swift, built once beside this script. Falls back to tesseract."""
    exe = os.path.join(HERE, "vision_ocr"); src = os.path.join(HERE, "vision_ocr.swift")
    if not os.path.exists(exe) and os.path.exists(src) and shutil.which("swiftc"):
        p = run(["swiftc", "-O", src, "-o", exe])
        if p.returncode != 0: log("ocr: swiftc failed: " + (p.stderr.strip().splitlines() or ["?"])[-1])
    if os.path.exists(exe): return "vision", exe
    if shutil.which("tesseract"): return "tesseract", "tesseract"
    return None, None

def ocr_frames(out, kept, words):
    engine, exe = ocr_binary()
    if not engine: log("ocr: skipped (no swiftc for Apple Vision, no tesseract)"); return "none"
    t0 = time.time()
    for k in kept:
        path = os.path.join(out, k["file"]); lines = []
        if engine == "vision":
            p = run([exe, path] + ([words] if words else []))
            for l in p.stdout.splitlines():
                try: d = json.loads(l)
                except ValueError: continue
                if d["conf"] >= 0.3: lines.append(d)
            lines.sort(key=lambda d: (-round(d["box"][1], 2), d["box"][0]))   # top to bottom (Vision counts from the bottom), then left to right
        else:
            p = run(["tesseract", path, "-", "--psm", "11"]); lines = [{"text": l.strip(), "conf": None, "box": None} for l in p.stdout.splitlines() if l.strip()]
        k["ocr"] = lines
    log(f"ocr: {engine}, {len(kept)} frames in {time.time()-t0:.0f} s"); return engine

# --- step 5: index and sheets --------------------------------------------------------------------
def said_near(cues, t, before=4, after=4): return " ".join(c[2] for c in cues if c[1] >= t - before and c[0] <= t + after)

def chapter_at(info, t):
    name = ""
    for ch in info.get("chapters") or []:
        if ch.get("start_time", 0) <= t: name = ch.get("title", "")
    return name

def write_index(out, info, kept, cues):
    rows = [{"t": k["t"], "time": mmss(k["t"]), "file": k["file"], "reason": k["reason"], "score": k["score"], "chapter": chapter_at(info, k["t"]),
             "said": said_near(cues, k["t"]), "ocr": [l["text"] for l in k.get("ocr", [])], "ocr_boxes": k.get("ocr", [])} for k in kept]
    json.dump(rows, open(os.path.join(out, "index.json"), "w"), indent=1, ensure_ascii=False)
    md = [f"# Frame index - {info.get('title')}", "", "| time | frame | why | chapter | on screen (first 120 chars) | said around it (first 120 chars) |", "|---|---|---|---|---|---|"]
    md += [f"| {r['time']} | {r['file']} | {r['reason']} | {r['chapter']} | {' / '.join(r['ocr'])[:120]} | {r['said'][:120]} |" for r in rows]
    open(os.path.join(out, "index.md"), "w").write("\n".join(md)); return rows

def sheet_binary():
    """Apple's own drawing through sheet.swift, built once beside this script. The Homebrew ffmpeg 9 on the Mac has no drawtext filter,
    so on the Mac the sheets and their labels come from this; ffmpeg draws them everywhere else."""
    exe = os.path.join(HERE, "sheet"); src = os.path.join(HERE, "sheet.swift")
    if not os.path.exists(exe) and os.path.exists(src) and shutil.which("swiftc"):
        p = run(["swiftc", "-O", src, "-o", exe])
        if p.returncode != 0: log("sheets: swiftc failed: " + (p.stderr.strip().splitlines() or ["?"])[-1])
    return exe if os.path.exists(exe) else None

def write_sheets(out, rows):
    """12 frames a sheet, 3x4, 480 px tiles, the time and reason drawn on each tile. sheet.swift on the Mac, ffmpeg elsewhere."""
    sdir = os.path.join(out, "sheets"); os.makedirs(sdir, exist_ok=True); per = SHEET_COLS * SHEET_ROWS; n = 0; nolabel = None
    swift = sheet_binary()
    for i in range(0, len(rows), per):   # always rebuilt: a sheet from an earlier run with other frames would mislead the reading
        chunk = rows[i:i+per]; n += 1; target = os.path.join(sdir, f"sheet_{n:02d}.jpg")
        if swift:
            args = [swift, target, str(SHEET_COLS), str(SHEET_ROWS), str(TILE_W), str(TILE_H)]
            for r in chunk: args += [os.path.join(out, r["file"]), f"{r['time']}  {r['reason']}  {os.path.basename(r['file'])}"]
            p = run(args)
            if p.returncode == 0 and os.path.exists(target): continue
            log("sheet: swift drawing failed, ffmpeg instead: " + (p.stderr.strip().splitlines() or ["?"])[-1])
        cmd, fc = ["ffmpeg", "-v", "error", "-y"], []
        for j in range(per):
            r = chunk[min(j, len(chunk) - 1)]; cmd += ["-i", os.path.join(out, r["file"])]
            label = f"{r['time']}  {r['reason']}  {os.path.basename(r['file'])}" if j < len(chunk) else " "
            text = f",drawtext=text='{label.replace(chr(39), '').replace(':', chr(92) + ':')}':x=6:y=4:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6" + (f":fontfile={FONT}" if FONT else "")
            fc.append(f"[{j}:v]scale={TILE_W}:{TILE_H}:force_original_aspect_ratio=decrease,pad={TILE_W}:{TILE_H}:(ow-iw)/2:(oh-ih)/2{text}[v{j}]")
        for r_ in range(SHEET_ROWS): fc.append("".join(f"[v{r_*SHEET_COLS+c}]" for c in range(SHEET_COLS)) + f"hstack={SHEET_COLS}[r{r_}]")
        fc.append("".join(f"[r{r_}]" for r_ in range(SHEET_ROWS)) + f"vstack={SHEET_ROWS}[out]")
        p = run(cmd + ["-filter_complex", ";".join(fc), "-map", "[out]", "-frames:v", "1", "-q:v", "4", target])
        if p.returncode != 0 and "drawtext" in p.stderr:   # no font support in this ffmpeg: sheets without labels, still usable
            nolabel = nolabel or (p.stderr.strip().splitlines() or ["?"])[-1]
            p = run(cmd + ["-filter_complex", ";".join(re.sub(r",drawtext=[^\[]*", "", f) for f in fc), "-map", "[out]", "-frames:v", "1", "-q:v", "4", target])
        if p.returncode != 0: log("sheet failed: " + (p.stderr.strip().splitlines() or ["?"])[-1])
    if nolabel: log("sheets: no time labels on the tiles, ffmpeg drawtext said: " + nolabel)
    return n, nolabel

# --- the commands --------------------------------------------------------------------------------
def cmd_study(a):
    os.makedirs(a.out, exist_ok=True); t0 = time.time(); failed = []
    info = fetch_info(a.src, a.out, a.cookies); duration = float(info.get("duration") or 0)
    log(f"title: {info.get('title')} | {mmss(duration)} | chapters: {len(info.get('chapters') or [])} | manual subs: {list((info.get('subtitles') or {}).keys())[:6]}")
    video = fetch_video(a.src, a.out, a.height, a.cookies)
    cues, ckind = ([], "none") if a.whisper else fetch_captions(a.src, info, a.out, a.lang, a.cookies)
    if not cues: cues, ckind = whisper_fallback(video, a.out, info)
    if not cues: failed.append(f"no speech text: {ckind}")
    kept = pick_frames(video, a.out, cues, a.floor, a.max_frames)
    engine = ocr_frames(a.out, kept, a.words)
    rows = write_index(a.out, info, kept, cues); sheets, nolabel = write_sheets(a.out, rows)
    if nolabel: failed.append(f"sheet tiles carry no time label (read the time from index.md row order: 12 frames a sheet). ffmpeg drawtext said: {nolabel}")
    if ckind.startswith("auto"): failed.append("speech is YouTube's auto text: names and numbers can be misheard, check them on the frame")
    if engine == "none": failed.append("no text reader ran: every on-screen value is read by eye, mark it ~")
    links = open(os.path.join(a.out, "links.txt")).read().splitlines()
    chapters = [f"- {mmss(c.get('start_time', 0))} {c.get('title')}" for c in (info.get("chapters") or [])] or ["- none"]
    ready = [f"# STUDY READY - {info.get('title')}",
             f"Source: {info.get('webpage_url')} | channel: {info.get('channel') or info.get('uploader')} | uploaded: {info.get('upload_date')} | length: {mmss(duration)} | views: {info.get('view_count')}",
             f"Speech: {ckind} | frames kept: {len(rows)} | sheets: {sheets} | OCR: {engine} | took {time.time()-t0:.0f} s", "",
             "## Chapters", *chapters, "",
             "## Links in the description (a workflow file, a LUT, a repo, a Patreon: open the ones that hold the recipe)", *([f"- {l}" for l in links] or ["- none"]), "",
             "## Read next", "1. transcript.txt in full. 2. every sheets/sheet_NN.jpg. 3. index.md for the words on screen. 4. the frames/ file behind each step, zoomed when a value is small.", "",
             "## Failed", *([f"- {f}" for f in failed] or ["- nothing"])]
    open(os.path.join(a.out, "STUDY_READY.md"), "w").write("\n".join(ready)); log("\n".join(ready))

def cmd_zoom(a):
    out = os.path.splitext(a.frame)[0] + f"_zoom_{a.x}_{a.y}_{a.w}_{a.h}.png"
    p = run(["ffmpeg", "-v", "error", "-y", "-i", a.frame, "-vf", f"crop={a.w}:{a.h}:{a.x}:{a.y},scale=iw*{a.scale}:ih*{a.scale}:flags=lanczos", out])
    log(out if p.returncode == 0 else "zoom failed: " + p.stderr.strip())

def cmd_check(a):
    """Every numbered step needs t=m:ss and frame=frames/f_*.png on disk; a value marked SEEN should be in that frame's OCR text."""
    text = open(a.lesson, encoding="utf-8").read(); ipath = os.path.join(a.batch, "index.json")
    idx = {r["file"]: r for r in json.load(open(ipath))} if os.path.exists(ipath) else {}
    steps = [l for l in text.splitlines() if re.match(r"^\s*\d+\.\s", l)]; bad = []
    for s in steps:
        t = re.search(r"\bt=(\d+:\d{2}(?::\d{2})?)", s); f = re.search(r"\bframe=(frames/\S+?\.png)", s)
        if not t: bad.append(f"no t= : {s[:80]}")
        if not f: bad.append(f"no frame= : {s[:80]}"); continue
        if not os.path.exists(os.path.join(a.batch, f.group(1))): bad.append(f"frame missing on disk: {f.group(1)}")
        if "SEEN" in s and f.group(1) in idx:
            ocr = " ".join(idx[f.group(1)]["ocr"])
            body = re.sub(r"\bt=\d+:\d{2}(?::\d{2})?", "", s.split("SEEN")[0].split("frame=")[0])   # the time is not a value
            for v in re.findall(r"=\s*(-?\d+(?:\.\d+)?)\b", body):
                if v not in ocr: bad.append(f"value {v} is not in the OCR of {f.group(1)} (read by eye? mark it ~): {s[:60]}")
    log(f"steps: {len(steps)} | problems: {len(bad)}"); [log("- " + b) for b in bad]; sys.exit(1 if bad else 0)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("study"); s.add_argument("src"); s.add_argument("--out", required=True); s.add_argument("--lang", default="en")
    s.add_argument("--height", type=int, default=1080); s.add_argument("--max-frames", type=int, default=240); s.add_argument("--floor", type=int, default=FLOOR_DEFAULT)
    s.add_argument("--cookies", default=None, help="browser for yt-dlp cookies, only after a bot check: opera"); s.add_argument("--whisper", action="store_true", help="skip captions, transcribe with whisper")
    s.add_argument("--words", default=None, help="a text file of app words (node and setting names) for the text reader"); s.set_defaults(fn=cmd_study)
    z = sub.add_parser("zoom"); z.add_argument("frame"); [z.add_argument(n, type=int) for n in ("x", "y", "w", "h")]; z.add_argument("--scale", type=int, default=2); z.set_defaults(fn=cmd_zoom)
    c = sub.add_parser("check"); c.add_argument("lesson"); c.add_argument("--batch", required=True); c.set_defaults(fn=cmd_check)
    a = ap.parse_args(); a.fn(a)
