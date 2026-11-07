#!/usr/bin/env python3
"""SORT CHECK for a FilmCraft project: build his shared bin tree, file every loose item, archive versions.

Usage:
  fc_sort.py sort    [--bridge 127.0.0.1:9876 | --project p.fcproj]            build bins, file loose items, list the top
  fc_sort.py archive <sequence name> [--bridge ... | --project ...]          copy the sequence he saw to OLD VERSIONS/<Vn>/, bump the working name
--project saves back to the file. --bridge edits the open app and never saves.
"""
import json, os, re, subprocess, sys

CLI = os.path.expanduser("~/.local/bin/filmcraft-cli")
TREE = {
    "**_EXPORT": [],
    "0_SEQUENCE": ["LINKED", "NESTED", "*Sequence_Unsure"],
    "1_VISUAL ASSET": ["**_Ref", "*Video_Unsure", "*Image_Unsure"],
    "2_GRAPHIC ASSET": ["*Graphic_Unsure"],
    "3_SOUND ASSET": ["MUSIC", "SFX", "VO", "*Sound_Unsure"],
    "4_RENDERS": [],
    "5_OTHER": ["Solid", "*Other_Unsure"],
}
VIDEO_EXT = {".mov", ".mp4", ".mxf", ".m4v", ".avi", ".mkv", ".webm"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".exr", ".dpx", ".webp", ".bmp", ".gif", ".psd"}
GRAPHIC_EXT = {".svg", ".ai", ".eps", ".pdf"}
SOUND_EXT = {".wav", ".aif", ".aiff", ".mp3", ".m4a", ".aac", ".flac"}


class Fc:
    def __init__(self, args):
        self.args = args
        self.p = subprocess.Popen([CLI, *args, "mcp"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        self.n = 0
        self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "sort", "version": "1"}})
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"); self.p.stdin.flush()

    def rpc(self, method, params):
        self.n += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params}) + "\n"); self.p.stdin.flush()
        while True:
            m = json.loads(self.p.stdout.readline())
            if m.get("id") == self.n:
                if "error" in m:
                    raise RuntimeError(f"{method}: {m['error']}")
                return m["result"]

    def cmd(self, id, **params):
        r = self.rpc("tools/call", {"name": "command_run", "arguments": {"id": id, "params": params}})
        txt = "".join(c.get("text", "") for c in r.get("content", []))
        if r.get("isError"):
            raise RuntimeError(f"{id} {params}: {txt}")
        try:
            return json.loads(txt)
        except ValueError:
            return txt

    def tree(self):
        return self.cmd("project.inspect")["root"]


def kids(node):
    return node.get("children", [])


def is_bin(c):
    return "children" in c and "item" not in c  # bins carry children and id; items carry item and type


def find_bin(node, name):
    return next((c for c in kids(node) if is_bin(c) and c["name"] == name), None)


def ensure(fc, parent, name):
    b = find_bin(parent, name)
    if b:
        return b["id"]
    r = fc.cmd("file.newBin", name=name, **({"parent": parent["id"]} if parent.get("id") else {}))
    return r["bin"]


def home(item):
    """Family bin for a loose root item, from its type and file extension."""
    t, name = item.get("type"), item["name"]
    ext = os.path.splitext(name)[1].lower()
    if t == "Sequence":
        return None  # deliverables are filed by video name
    if ext in SOUND_EXT or t == "Audio":
        return ("3_SOUND ASSET", "*Sound_Unsure")
    if ext in GRAPHIC_EXT:
        return ("2_GRAPHIC ASSET", None)
    if ext in VIDEO_EXT or ext in IMAGE_EXT or t in ("Movie", "Still"):
        return ("1_VISUAL ASSET", None)
    if t in ("ColorMatte", "BlackVideo", "TransparentVideo", "AdjustmentLayer", "BarsAndTone"):
        return ("5_OTHER", "Solid")
    return ("5_OTHER", "*Other_Unsure")


def video_of(seq_name):
    m = re.match(r"^(.+?)_FC_V[\d.]+$", seq_name)
    return m.group(1) if m else None


def build(fc):
    for top, subs in TREE.items():
        root = fc.tree()
        bid = ensure(fc, root, top)
        node = find_bin(fc.tree(), top)
        for s in subs:
            ensure(fc, node, s)
            node = find_bin(fc.tree(), top)
    return fc.tree()


def sort(fc):
    root = build(fc)
    bins = {c["name"]: c for c in kids(root) if is_bin(c)}
    for it in [c for c in kids(root) if not is_bin(c)]:
        if it.get("type") == "Sequence":
            video = video_of(it["name"]) or "*Sequence_Unsure"
            if video == "*Sequence_Unsure":
                dest = find_bin(bins["0_SEQUENCE"], video)["id"]
            else:
                exp = find_bin(fc.tree(), "**_EXPORT")
                vb = ensure(fc, exp, video)
                ensure(fc, find_bin(find_bin(fc.tree(), "**_EXPORT"), video), "OLD VERSIONS")
                dest = vb
        else:
            top, sub = home(it)
            node = find_bin(fc.tree(), top)
            dest = ensure(fc, node, sub) if sub else node["id"]
        fc.cmd("project.moveToBin", items=[it["item"]], bin=dest)
    return check(fc)


def check(fc):
    root = fc.tree()
    top = [c["name"] for c in kids(root)]
    loose = [n for n in top if n not in TREE]
    exp = find_bin(root, "**_EXPORT")
    loose_exp = [c["name"] for c in kids(exp) if not is_bin(c)] if exp else []
    ok = not loose and not loose_exp and all(n in top for n in TREE)
    return {"ok": ok, "top": top, "loose_top": loose, "loose_in_export": loose_exp}


def archive(fc, seq_name):
    root = fc.tree()
    def walk(n):
        for c in kids(n):
            if c.get("type") == "Sequence" and c["name"] == seq_name:
                return c
            r = walk(c) if is_bin(c) else None
            if r:
                return r
    seq = walk(root)
    if not seq:
        raise SystemExit(f"no sequence named {seq_name}")
    video = video_of(seq_name)
    ver = re.search(r"_FC_(V[\d.]+)$", seq_name).group(1)
    sort(fc)
    vbin = find_bin(find_bin(fc.tree(), "**_EXPORT"), video)
    old = find_bin(vbin, "OLD VERSIONS")
    dest = ensure(fc, old, ver)
    def items(n):
        for c in kids(n):
            yield from (items(c) if is_bin(c) else [c])
    before = {c["item"] for c in items(fc.tree())}
    fc.cmd("project.select", items=[seq["item"]])
    fc.cmd("edit.duplicate")
    copy = next(c for c in items(fc.tree()) if c.get("type") == "Sequence" and c["item"] not in before)
    fc.cmd("clip.rename", item=copy["item"], name=seq_name)
    fc.cmd("project.moveToBin", items=[copy["item"]], bin=dest)
    a, *b = ver[1:].split(".")
    nxt = f"V{a}.{int(b[0]) + 1}" if b else f"V{a}.1"
    fc.cmd("clip.rename", item=seq["item"], name=f"{video}_FC_{nxt}")
    return {"archived": f"OLD VERSIONS/{ver}/{seq_name}", "working": f"{video}_FC_{nxt}", **check(fc)}


if __name__ == "__main__":
    a = sys.argv[1:]
    mode = a.pop(0)
    target = []
    if "--bridge" in a:
        i = a.index("--bridge"); target = ["--bridge", a[i + 1]]; del a[i:i + 2]
    if "--project" in a:
        i = a.index("--project"); target = ["--project", a[i + 1]]; del a[i:i + 2]
    fc = Fc(target)
    out = sort(fc) if mode == "sort" else archive(fc, a[0])
    if "--project" in target:
        fc.cmd("file.save")
    print(json.dumps(out, ensure_ascii=False))
