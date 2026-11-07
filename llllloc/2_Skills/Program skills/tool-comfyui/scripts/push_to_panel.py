"""Put a UI-format ComfyUI workflow into his Comfy Cloud Workflows panel, in its job folder.

Usage: python3 -I push_to_panel.py <workflow_comfy-ui.json> <Client>/<Job>/<Model> [panel name]
Example: python3 -I push_to_panel.py a client_BG-Swap_SD25_L01top_S01_V2_comfy-ui.json "a client/bg swap test/Seedance"

Panel layout: workflows/<Client>/<Job>/<Model>/ holds the latest version of each workflow,
workflows/<Client>/<Job>/<Model>/_Old versions/ the older ones, workflows/_DELETE/ the strays.
After the push, older versions of the same workflow move to _Old versions. Nothing is deleted.
"""
import json, os, re, sys, urllib.parse, urllib.request

SECRETS = os.path.expanduser("~/Library/Application Support/comfy-cli/secrets.json")
OLD = "_Old versions"

session = json.load(open(SECRETS))["cloud_session"]
BASE = session["base_url"].rstrip("/")
AUTH = {"Authorization": f"Bearer {session['tokens']['access_token']}"}
q = lambda p: urllib.parse.quote(p, safe="")


def call(path, method="GET", data=None):
    headers = dict(AUTH, **({"Content-Type": "application/json"} if data else {}))
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req) as r:
        return r.read().decode()


def listing():
    return [e["path"] if isinstance(e, dict) else e
            for e in json.loads(call("/api/userdata?dir=workflows&recurse=true"))]


def move(src, dst):
    call(f"/api/userdata/{q('workflows/' + src)}/move/{q('workflows/' + dst)}?overwrite=false", "POST")


def stem_version(name):
    m = re.match(r"(.+)_V(\d+)([a-z]?)$", name)
    return (m.group(1), (int(m.group(2)), m.group(3))) if m else (name, (0, ""))


if __name__ == "__main__":
    src, folder = sys.argv[1], sys.argv[2].strip("/")
    name = sys.argv[3] if len(sys.argv) > 3 else os.path.splitext(os.path.basename(src))[0].removesuffix("_comfy-ui")
    wf = json.load(open(src))
    if "nodes" not in wf:
        sys.exit("Not a UI-format workflow (no 'nodes'). The panel cannot open an API-format file.")

    target = f"{folder}/{name}.json"
    print(call(f"/api/userdata/{q('workflows/' + target)}?overwrite=true&full_info=true", "POST",
               json.dumps(wf).encode())[:200])

    stem, ver = stem_version(name)
    for path in listing():
        d, f = os.path.split(path)
        s, v = stem_version(os.path.splitext(f)[0])
        if d == folder and s == stem and v < ver:
            move(path, f"{folder}/{OLD}/{f}")
            print("moved to _Old versions:", f)

    print("IN PANEL" if target in listing() else "NOT LISTED", target)
