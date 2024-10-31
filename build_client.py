from shutil import make_archive
from json import load
import zipfile;
from os import listdir, walk
from os.path import isdir, join, exists, relpath, dirname, exists

properties = {}
with open("properties.json") as f:
    properties = load(f)

archive_name = properties["archive_base_name"] + '-client-' + properties["version"]

files_to_zip = [
    "overrides",
    "cover.png",
    "LICENSE",
    "logo.png",
    "manifest.json",
    "modlist.html",
    "README.md"
]

with zipfile.ZipFile("build/" + archive_name + ".zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in files_to_zip:
        if isdir(file):
            for root, dirs, files in walk(file):
                for filename in files:
                    file_path = join(root, filename)
                    zipf.write(file_path, relpath(file_path, dirname(file)))
        else:
            if exists(file):
                zipf.write(file)

print(f"Successfully built archive {archive_name}")