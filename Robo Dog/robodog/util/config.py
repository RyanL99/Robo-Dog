
import json, os
DEFAULT="robodog.config.json"
def load(path=DEFAULT): 
    with open(path) as f: return json.load(f)
def save(cfg,path=DEFAULT):
    tmp=path+".tmp"
    with open(tmp,"w") as f: json.dump(cfg,f,indent=2)
    os.replace(tmp,path)
