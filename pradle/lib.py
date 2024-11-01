from json import load
from os import makedirs, listdir
from os.path import isdir, join
from shutil import rmtree, copytree, copy2

properties = {}

with open("properties.json") as f:
    properties = load(f)
    f.close()

def clear_cache():
    CACHE_PATH = properties["path"]["cache"]
    rmtree(CACHE_PATH)
    makedirs(CACHE_PATH)

def copy_content(src, dst):
    for item in listdir(src):
        s = join(src, item)
        d = join(dst, item)
        if isdir(s):
            copytree(s, d)
        else:
            copy2(s, d)