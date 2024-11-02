from os.path import join

from lib import properties, clear_cache, fhandle_placeholders, copy_content2cache, archive_cache

print("Building client")
clear_cache()

CLIENT_PATH = properties["path"]["client"]
COMMON_PATH = properties["path"]["common"]
CACHE_PATH = properties["path"]["cache"]

copy_content2cache(COMMON_PATH)
copy_content2cache(CLIENT_PATH)

fhandle_placeholders(join(CACHE_PATH, "manifest.json"))

archive_name = properties["archive_base_name"] + '-client-' + properties["version"]
archive_cache(archive_name)

clear_cache()
print(f"Successfully built client archive {archive_name}\n")