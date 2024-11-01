import zipfile
from os import walk
from os.path import join, relpath

from lib import properties, clear_cache, copy_content

clear_cache()

CLIENT_PATH = properties["path"]["client"]
COMMON_PATH = properties["path"]["common"]
CACHE_PATH = properties["path"]["cache"]
BUILD_PATH = properties["path"]["build"]

copy_content(COMMON_PATH, CACHE_PATH)
copy_content(CLIENT_PATH, CACHE_PATH)

manifest = ""
with open(join(CACHE_PATH, "manifest.json"), "r") as f:
    manifest = f.read()
manifest = manifest.replace("${version}", properties["version"])
with open(join(CACHE_PATH, "manifest.json"), "w") as f:
    f.write(manifest)

archive_name = properties["archive_base_name"] + '-client-' + properties["version"]
with zipfile.ZipFile(join(BUILD_PATH, archive_name + ".zip"), 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in walk(CACHE_PATH):
        for file in files:
            zipf.write(join(root, file), join(relpath(root, CACHE_PATH), file))
    zipf.close()

print(f"Successfully built archive {archive_name}")
clear_cache()