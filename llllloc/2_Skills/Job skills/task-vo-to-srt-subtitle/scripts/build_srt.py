#!/usr/bin/env python3
"""Build a broadcast-ready SRT from a Whisper JSON with word timings.

Usage:
  python3 build_srt.py INPUT.json --out-dir DIR --name NAME [--extend]
      [--fixes fixes.json] [--split 0.0,4.74] [--compare OTHER.json]
      [--segments] [--terms terms.md]

Writes NAME_final.srt and NAME_breakdown.md, and prints a fault report.
With --segments (a source with no word timings) the SRT is named
NAME_draft-EST.srt, because most of its times are calculated.

The script never creates a time when word timings exist. A caption starts at
its first word's start and ends at its last word's end. With --extend, a
caption that reads too fast may end at the NEXT caption's real start.

Rebuilt on 8 Oct 2026 from the rules in SKILL.md and references/caption-rules.md.
Standard library only. Python 3.8 or newer. Run it, there is no need to read it.
"""
import argparse
import difflib
import json
import os
import re
import sys
import unicodedata

# ---- Limits. Source: Netflix Timed Text Style Guide (English), as quoted in SKILL.md.
MAX_LINE = 42          # characters per line
MAX_LINES = 2          # lines per caption
MIN_DUR = 0.833        # seconds a caption stays up, at least (20 frames at 24 fps)
MAX_DUR = 7.0          # seconds a caption stays up, at most
MAX_CPS = 20.0         # characters per second, at most
GAP_BREAK = 1.0        # a silence longer than this starts a new caption
DUP_MAX_DUR = 0.2      # a repeated sentence shorter than this is a likely Whisper duplicate
SAME_TIME_RUN = 3      # this many words on one start time is a fault worth a flag
FIX_AT_WINDOW = 1.0    # a fix with "at" matches a word that starts within this many seconds

SENT_END = re.compile(r"[.?!][\"')\]]*$")
ABBREV = {"mr.", "mrs.", "ms.", "dr.", "st.", "vs.", "e.g.", "i.e.", "no.", "inc.", "ltd.", "co."}
# Never cut AFTER one of these. A cut BEFORE a conjunction, article or preposition is a good cut.
CUT_BEFORE = {
    "and", "but", "or", "nor", "so", "yet", "because", "although", "while", "if", "when", "that",
    "which", "who", "as", "than", "a", "an", "the", "of", "in", "on", "at", "to", "from", "by",
    "with", "about", "into", "over", "after", "before", "under", "between", "through", "during",
    "without", "within", "across", "for",
}
FUNCTION = CUT_BEFORE | {
    "is", "are", "was", "were", "be", "been", "has", "have", "had", "will", "would", "can", "could",
    "should", "my", "your", "our", "their", "his", "her", "its", "this", "these", "those", "not",
    "we", "i", "you", "they", "he", "she", "it",
}
UNITS = {"%", "percent", "million", "billion", "thousand", "k", "x", "points", "bps"}


def die(msg):
    print("ERROR: " + msg)
    sys.exit(2)


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def bare(s):
    return s.strip(".,;:!?\"'()[]").lower()


def parse_clock(s):
    parts = [float(p) for p in s.strip().split(":")]
    sec = 0.0
    for p in parts:
        sec = sec * 60 + p
    return sec


def seg_times(seg):
    if "start" in seg and "end" in seg:
        return float(seg["start"]), float(seg["end"])
    ts = seg.get("timestamp")
    if isinstance(ts, (list, tuple)) and len(ts) == 2 and ts[0] is not None and ts[1] is not None:
        return float(ts[0]), float(ts[1])
    if isinstance(ts, str) and "-" in ts:
        a, b = ts.split("-", 1)
        return parse_clock(a), parse_clock(b)
    return None


def load_raw(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        die("file not found: %s" % path)
    except json.JSONDecodeError as e:
        die("%s is not valid JSON (%s). Export the JSON again." % (path, e))
    if isinstance(data, list):
        return {"segments": data}
    return data


def word_items(data):
    """Return raw word dicts [{'raw','start','end'}] or [] when the file has none."""
    out = []

    def take(w):
        txt = w.get("word", w.get("text", ""))
        st, en = w.get("start"), w.get("end")
        if st is None or en is None:
            ts = w.get("timestamp")
            if isinstance(ts, (list, tuple)) and len(ts) == 2:
                st, en = ts
        if txt and st is not None and en is not None:
            out.append({"raw": txt, "start": float(st), "end": float(en)})

    for seg in data.get("segments", []) or []:
        for w in seg.get("words", []) or []:
            take(w)
    if not out:
        for w in data.get("words", []) or []:
            take(w)
    return out


def glue(raw):
    """Join the pieces Whisper splits (numbers, punctuation). Returns words and the glue count."""
    if not raw:
        return [], 0
    spaced = sum(1 for w in raw if w["raw"].startswith(" "))
    by_space = spaced >= 0.6 * len(raw)
    words, glued = [], 0
    for w in raw:
        txt = w["raw"].strip()
        if not txt:
            continue
        join = False
        if words:
            prev = words[-1]["text"]
            if by_space and not w["raw"].startswith(" "):
                join = True
            elif re.match(r"^[.,]\d", txt) and prev[-1:].isdigit():
                join = True
            elif txt in {"%", ".", ",", "?", "!", ":", ";"}:
                join = True
            elif prev.endswith(("$", "€", "£")):
                join = True
        if join:
            words[-1]["text"] += txt
            words[-1]["end"] = max(words[-1]["end"], w["end"])
            if re.search(r"\d", txt):
                glued += 1
        else:
            words.append({"text": txt, "start": w["start"], "end": w["end"], "est": False})
    return words, glued


def words_from_segments(data):
    """--segments: no word timings. Spread each segment's words by character count. Marked EST."""
    words = []
    for seg in data.get("segments", data.get("chunks", [])) or []:
        t = seg_times(seg)
        toks = (seg.get("text") or "").split()
        if not t or not toks:
            continue
        st, en = t
        total = sum(len(x) for x in toks) or 1
        pos = st
        for i, tok in enumerate(toks):
            nxt = en if i == len(toks) - 1 else pos + (en - st) * len(tok) / total
            words.append({"text": tok, "start": pos, "end": nxt, "est": True,
                          "real_start": i == 0, "real_end": i == len(toks) - 1})
            pos = nxt
    return words


def load_terms(path):
    terms = []
    if path and os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if line.startswith("- "):
                term = line[2:].split("|")[0].strip().strip("`")
                if " " in term:
                    terms.append([bare(x) for x in term.split()])
    return terms


def apply_fixes(words, path):
    try:
        fx = json.load(open(path, encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        die("cannot read the fixes file %s (%s). Shape: references/caption-rules.md, FIXES FILE." % (path, e))
    report = []
    for d in fx.get("drop", []):
        before = len(words)
        words = [w for w in words if not (d["start"] <= w["start"] < d["end"])]
        report.append("drop %.2f-%.2f: %d words removed" % (d["start"], d["end"], before - len(words)))
    for r in fx.get("replace", []):
        src = r["from"].split()
        dst = r["to"].split()
        n, i, hits = len(src), 0, 0
        while i <= len(words) - n:
            span = words[i:i + n]
            ok = all(bare(span[k]["text"]) == bare(src[k]) for k in range(n))
            if ok and "at" in r and abs(span[0]["start"] - float(r["at"])) > FIX_AT_WINDOW:
                ok = False
            if ok:
                lead = re.match(r"^[\"'(\[]*", span[0]["text"]).group(0)
                tail = re.search(r"[.,;:!?\"')\]]*$", span[-1]["text"]).group(0)
                new = []
                for k, tok in enumerate(dst):
                    new.append({"text": tok, "start": span[0]["start"], "end": span[-1]["end"],
                                "est": span[0].get("est", False)})
                # keep real times: the first new word starts where the span started, the last ends where it ended
                if len(new) > 1:
                    cut = span[0]["end"] if n > 1 else span[0]["start"]
                    for k in range(1, len(new)):
                        new[k]["start"] = cut
                    for k in range(0, len(new) - 1):
                        new[k]["end"] = cut
                new[0]["text"] = lead + new[0]["text"]
                new[-1]["text"] = new[-1]["text"] + tail
                words[i:i + n] = new
                hits += 1
                i += len(new)
            else:
                i += 1
        report.append("replace '%s' -> '%s': %d" % (r["from"], r["to"], hits))
    return words, report


# ---------------------------------------------------------------- cutting

def is_sentence_end(w):
    t = w["text"]
    if t.lower() in ABBREV:
        return False
    return bool(SENT_END.search(t))


def text_of(ws):
    return " ".join(w["text"] for w in ws)


def protected(ws, i, terms):
    """True when a cut between ws[i] and ws[i+1] would break a name, a number or a brand term."""
    a, b = ws[i]["text"], ws[i + 1]["text"]
    if re.search(r"\d", a) and (re.match(r"^[\d.,]+%?$", b) or bare(b) in UNITS):
        return True
    if a[:1].isupper() and b[:1].isupper() and not is_sentence_end(ws[i]) and not a.endswith(","):
        if i > 0 or len(a) > 1:
            return True
    for term in terms:
        n = len(term)
        for s in range(max(0, i - n + 2), i + 1):
            if s + n <= len(ws) and s <= i < s + n - 1:
                if [bare(w["text"]) for w in ws[s:s + n]] == term:
                    return True
    return False


def cut_rank(ws, i, terms):
    """1 = after a comma, 2 = before a conjunction, article or preposition, 3 = other, 9 = forced."""
    a, b = ws[i]["text"], ws[i + 1]["text"]
    if protected(ws, i, terms):
        return 9
    if bare(a) in FUNCTION and not a.endswith((",", ";", ":")):
        return 9
    if a.endswith((",", ";", ":")) or is_sentence_end(ws[i]):
        return 1
    if bare(b) in CUT_BEFORE:
        return 2
    return 3


def best_cut(ws, terms, fit=None):
    """Pick the cut: lowest rank first, then the most balanced. Returns (index, rank)."""
    best = None
    for i in range(len(ws) - 1):
        left, right = text_of(ws[:i + 1]), text_of(ws[i + 1:])
        if fit and (len(left) > fit or len(right) > fit):
            continue
        key = (cut_rank(ws, i, terms), abs(len(left) - len(right)))
        if best is None or key < best[0]:
            best = (key, i)
    if best is None:
        return None, None
    return best[1], best[0][0]


def layout(ws, terms):
    """Return (lines, forced) for one caption, or None when it cannot fit two lines."""
    txt = text_of(ws)
    if len(txt) <= MAX_LINE:
        return [txt], False
    i, rank = best_cut(ws, terms, fit=MAX_LINE)
    if i is None:
        return None
    return [text_of(ws[:i + 1]), text_of(ws[i + 1:])], rank == 9


def split_to_fit(ws, terms, forced):
    if layout(ws, terms) is not None or len(ws) == 1:
        return [ws]
    i, rank = best_cut(ws, terms)
    if rank == 9:
        forced.append(text_of(ws)[:60])
    return split_to_fit(ws[:i + 1], terms, forced) + split_to_fit(ws[i + 1:], terms, forced)


def hard_chunks(words):
    chunks, cur = [], []
    for k, w in enumerate(words):
        if cur and w["start"] - cur[-1]["end"] > GAP_BREAK:
            chunks.append(cur)
            cur = []
        cur.append(w)
        if is_sentence_end(w):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def stamp(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def main():
    ap = argparse.ArgumentParser(description="Build an SRT from a Whisper JSON with word timings.")
    ap.add_argument("input")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--name")
    ap.add_argument("--extend", action="store_true", help="hold a too-fast caption until the next caption's start")
    ap.add_argument("--fixes", help="JSON file of approved word corrections")
    ap.add_argument("--split", default="", help="caption start times to cut in two, comma separated")
    ap.add_argument("--compare", help="a second Whisper JSON of the same audio")
    ap.add_argument("--segments", action="store_true", help="source has no word timings: calculate them (EST)")
    ap.add_argument("--terms", help="glossary file, lines of '- TERM | ...'")
    a = ap.parse_args()

    name = a.name or os.path.splitext(os.path.basename(a.input))[0]
    data = load_raw(a.input)
    raw = word_items(data)
    est_mode = False
    glued = 0
    if raw:
        words, glued = glue(raw)
    elif a.segments:
        words = words_from_segments(data)
        est_mode = True
        if not words:
            die("no segments with a time found in %s." % a.input)
    else:
        die("%s has no word timings. Export it again with word timestamps "
            "(whisper --word_timestamps True). For a draft now, add --segments: "
            "the times are then calculated and marked EST." % a.input)

    terms_path = a.terms or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "glossary.md")
    terms = load_terms(terms_path)

    fix_report = []
    if a.fixes:
        words, fix_report = apply_fixes(words, a.fixes)

    # faults that live in the words
    same_time, run = [], [words[0]] if words else []
    for w in words[1:]:
        if abs(w["start"] - run[-1]["start"]) < 1e-6:
            run.append(w)
        else:
            if len(run) >= SAME_TIME_RUN:
                same_time.append((run[0]["start"], text_of(run)))
            run = [w]
    if len(run) >= SAME_TIME_RUN:
        same_time.append((run[0]["start"], text_of(run)))

    forced, caps, dups = [], [], []
    prev_norm = None
    for chunk in hard_chunks(words):
        n = norm(text_of(chunk))
        if n and n == prev_norm and chunk[-1]["end"] - chunk[0]["start"] < DUP_MAX_DUR:
            dups.append((chunk[0]["start"], chunk[-1]["end"], text_of(chunk)))
        prev_norm = n
        for part in split_to_fit(chunk, terms, forced):
            caps.append(part)

    split_at = [float(x) for x in a.split.split(",") if x.strip()]
    for t in split_at:
        for k, c in enumerate(caps):
            if abs(c[0]["start"] - t) < 0.01 and len(c) > 1:
                i, _ = best_cut(c, terms)
                caps[k:k + 1] = [c[:i + 1], c[i + 1:]]
                break
        else:
            print("NOTE: --split %.2f matched no caption start." % t)

    rows, extended, est_bounds = [], 0, 0
    for k, c in enumerate(caps):
        lay = layout(c, terms)
        lines = lay[0] if lay else [text_of(c)]
        start, end = c[0]["start"], c[-1]["end"]
        chars = len(text_of(c))
        if a.extend and k + 1 < len(caps):
            nxt = caps[k + 1][0]["start"]
            dur = end - start
            too_fast = dur <= 0 or chars / max(dur, 1e-6) > MAX_CPS or dur < MIN_DUR
            if too_fast and nxt > end and nxt - start <= MAX_DUR:
                end = nxt
                extended += 1
        dur = end - start
        flags = []
        if dur < MIN_DUR:
            flags.append("SHORT")
        if dur > MAX_DUR:
            flags.append("LONG")
        if dur > 0 and chars / dur > MAX_CPS:
            flags.append("FAST")
        if est_mode:
            est_bounds += (0 if c[0].get("real_start") else 1) + (0 if c[-1].get("real_end") else 1)
        rows.append({"n": k + 1, "start": start, "end": end, "dur": dur, "lines": lines, "flags": flags})

    os.makedirs(a.out_dir, exist_ok=True)
    srt_path = os.path.join(a.out_dir, name + ("_draft-EST.srt" if est_mode else "_final.srt"))
    with open(srt_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write("%d\n%s --> %s\n%s\n\n" % (r["n"], stamp(r["start"]), stamp(r["end"]), "\n".join(r["lines"])))
    md_path = os.path.join(a.out_dir, name + "_breakdown.md")
    total = rows[-1]["end"] if rows else 0.0
    one_line = sum(1 for r in rows if len(r["lines"]) == 1)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# %s — caption breakdown\n\n" % name)
        f.write("%d captions. Running time %s. %d on one line.\n" % (len(rows), stamp(total), one_line))
        if est_mode:
            f.write("\nTIMING IS CALCULATED (EST): the source has no word timings. %d of %d caption "
                    "boundaries are estimates. This is a draft, not a final.\n" % (est_bounds, 2 * len(rows)))
        f.write("\n| # | In | Out | Sec | Text | Flag |\n|---|---|---|---|---|---|\n")
        for r in rows:
            txt = "<code>" + "<br>".join(x.replace("|", "\\|") for x in r["lines"]) + "</code>"
            f.write("| %d | %s | %s | %.2f | %s | %s |\n" % (
                r["n"], stamp(r["start"]), stamp(r["end"]), r["dur"], txt, " ".join(r["flags"])))

    # ---- the fault report drives the reply
    print("FILES: %s | %s" % (srt_path, md_path))
    print("CAPTIONS: %d | RUNNING TIME: %s | ONE LINE: %d of %d" % (len(rows), stamp(total), one_line, len(rows)))
    for flag in ("SHORT", "LONG", "FAST"):
        hit = [str(r["n"]) for r in rows if flag in r["flags"]]
        print("%s: %s" % (flag, ", ".join(hit) if hit else "none"))
    print("EXTENDED INTO SILENCE: %d" % extended)
    print("FORCED CUTS (no clean place to cut): %d" % len(forced))
    for x in forced:
        print("  - %s..." % x)
    print("NUMBER PIECES GLUED: %d" % glued)
    print("WORDS SHARING ONE TIME: %d run(s)" % len(same_time))
    for t, x in same_time:
        print("  - at %s: %s" % (stamp(t), x[:80]))
    print("LIKELY DUPLICATE: %d" % len(dups))
    for s, e, x in dups:
        print("  - %.2f-%.2f: %s  (ask him before a drop rule)" % (s, e, x[:80]))
    forms = {}
    for w in words:
        t = w["text"].strip(".,;:!?\"'()[]")
        if t[:1].isupper() and len(t) > 2:
            forms.setdefault(norm(t), set()).add(t)
    multi = {k: v for k, v in forms.items() if len(v) > 1}
    print("ONE WORD, SEVERAL SPELLINGS: %d" % len(multi))
    for v in multi.values():
        print("  - " + " / ".join(sorted(v)))
    if est_mode:
        print("EST BOUNDARIES: %d of %d. This file is a draft, never a final." % (est_bounds, 2 * len(rows)))
    for line in fix_report:
        print("FIX " + line)

    if a.compare:
        other_raw = word_items(load_raw(a.compare))
        if not other_raw:
            print("COMPARE: %s has no word timings, so it cannot be compared." % a.compare)
        else:
            other, _ = glue(other_raw)
            x = [bare(w["text"]) for w in words]
            y = [bare(w["text"]) for w in other]
            sm = difflib.SequenceMatcher(a=x, b=y, autojunk=False)
            print("COMPARE: words the two runs disagree on")
            print("| Time | This run | Other run |")
            print("|---|---|---|")
            n = 0
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "equal":
                    continue
                t = words[min(i1, len(words) - 1)]["start"] if words else 0
                print("| %s | %s | %s |" % (stamp(t), text_of(words[i1:i2]) or "(nothing)",
                                            text_of(other[j1:j2]) or "(nothing)"))
                n += 1
            print("COMPARE: %d disagreement(s)" % n)


if __name__ == "__main__":
    main()
