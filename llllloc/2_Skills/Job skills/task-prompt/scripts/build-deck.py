#!/usr/bin/env python3
"""Build a Lord Of The Prompt deck.

You write ONLY the deck body: masthead, SPEC block, prompt cards. This script
wraps it in the locked llloc-UI shell (fonts, CSS, theme, scaler, tooltips,
copy logic) and writes the finished single-file HTML.

Never open assets/deck-shell.html. It carries about 120 KB of embedded font
data. Reading it wastes the whole point of this script.

    python3 scripts/build-deck.py --body body.html --out MyDeck.html

Options:
    --body   the deck body fragment you wrote          (required)
    --out    where to write the finished deck          (required)
    --shell  path to the shell (default: ../assets/deck-shell.html)
    --title  browser tab title (default: read from the body's <h1>)

Exit code 0 on success. Any problem prints one line to stderr and exits 1.
"""
import argparse, html, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
MARKER = "<!--DECK-->"
PROMPT_RE = re.compile(r'(<pre class="prompt-text">)(.*?)(</pre>)', re.S)


def normalize(text):
    """Strip the markup indentation out of a prompt block.

    A <pre> keeps every space you type. The name line sits hard against the
    opening tag so it has no indent, while every line after it inherits the
    indentation of the surrounding markup. On screen that shows as a gap before
    the first word - the studio reported it on 29 August 2026 - but the real damage is
    invisible: those spaces go onto the clipboard and into the model.

    So: drop blank lines top and bottom, then take the indentation off. If the
    first line is flush and the rest share an indent, that indent is markup and
    it goes. Anything indented DEEPER than that keeps the difference, so a
    prompt that really uses structure survives.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return ""

    def ind(line):
        return len(line) - len(line.lstrip(" \t"))

    body = [ind(l) for l in lines[1:] if l.strip()]
    if ind(lines[0]) == 0 and body and min(body) > 0:
        pad = min(body)
        out = [lines[0]] + [l[pad:] if ind(l) >= pad else l.lstrip(" \t") for l in lines[1:]]
    else:
        pad = min(ind(l) for l in lines if l.strip())
        out = [l[pad:] if l.strip() else "" for l in lines] if pad else lines
    return "\n".join(out)


def fail(msg):
    print("build-deck: " + msg, file=sys.stderr)
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--starter", metavar="PATH", default=None,
                    help="write the deck-body starter to PATH and stop. "
                         "Every deck begins as a copy of it - never from scratch.")
    ap.add_argument("--body", required=False)
    ap.add_argument("--out", required=False)
    ap.add_argument("--shell", default=str(HERE.parent / "assets" / "deck-shell.html"))
    ap.add_argument("--title", default=None)
    a = ap.parse_args()

    if a.starter:
        src = HERE.parent / "references" / "deck-body-starter.html"
        if not src.is_file():
            sys.exit("no starter at %s" % src)
        dst = pathlib.Path(a.starter)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print("%s  <- deck body starter. Edit it, then build with --body/--out." % dst)
        return
    if not a.body or not a.out:
        sys.exit("--body and --out are required (or use --starter PATH)")

    shell_p, body_p = pathlib.Path(a.shell), pathlib.Path(a.body)
    if not shell_p.is_file():
        fail(f"no shell at {shell_p}")
    if not body_p.is_file():
        fail(f"no body at {body_p}")

    shell = shell_p.read_text(encoding="utf-8")
    body = body_p.read_text(encoding="utf-8").strip()
    if MARKER not in shell:
        fail(f"the shell has no {MARKER} marker")
    if not body:
        fail("the body file is empty")

    # the prompt blocks are cleaned BEFORE they are spliced, so the file on
    # disk is right and nothing depends on JavaScript to make it right.
    fixed = [0]

    def clean(m):
        before, inner = m.group(2), normalize(m.group(2))
        if inner != before:
            fixed[0] += 1
        return m.group(1) + inner + m.group(3)

    body = PROMPT_RE.sub(clean, body)

    title = a.title
    if not title:
        m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        # the <h1> already carries entities (&#8212;). Decode once, re-encode once,
        # or the tab reads "Night Market &#8212; Seedance Prompts".
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else "Prompt Deck"

    out = shell.replace(MARKER, body).replace("{{DECK_TITLE}}", html.escape(title, quote=False))

    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if left:
        fail("unfilled placeholders left in the body: " + ", ".join(sorted(set(left))))

    out_p = pathlib.Path(a.out)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(out, encoding="utf-8")

    cards = out.count('class="card')
    note = f"  {fixed[0]} prompt(s) de-indented" if fixed[0] else ""
    print(f"{out_p}  {out_p.stat().st_size/1024:.0f} KB  {cards} cards{note}")


if __name__ == "__main__":
    main()
