
import json, os
DEFAULT_PATH = "spotmicroai.default.json"

def load_config(path=DEFAULT_PATH):
    with open(path) as f: return json.load(f)

def save_config(cfg, path=DEFAULT_PATH):
    tmp = path + ".tmp"
    with open(tmp, "w") as f: json.dump(cfg, f, indent=2)
    os.replace(tmp, path)
