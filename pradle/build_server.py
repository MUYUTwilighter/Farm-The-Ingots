from os.path import join

from lib import clear_cache, properties, copy_content2cache, fhandle_placeholders, archive_cache

print("Building server")
clear_cache()

SERVER_PATH = properties["path"]["server"]
COMMON_PATH = properties["path"]["common"]
CACHE_PATH = properties["path"]["cache"]

copy_content2cache(COMMON_PATH)
copy_content2cache(SERVER_PATH)

fhandle_placeholders(join(CACHE_PATH, "start.bat"))

archive_name = properties["archive_base_name"] + '-server-' + properties["version"]
archive_cache(archive_name)

clear_cache()
print(f"Successfully built server archive {archive_name}\n")