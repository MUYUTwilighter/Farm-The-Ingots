from lib import validate_path, properties, merge_nested_dicts
from os import makedirs
from os.path import exists, join
from sys import argv
from json import dump

kwargs={}
for arg in argv[1:]:
    if arg.startswith("-"):
        arg = arg[1:]
        arg = arg.split("=")
        kwargs[arg[0]] = arg[1]
merge_nested_dicts(properties, kwargs)

if not exists("properties.json"):
    with open("properties.json", "w") as f:
        dump(properties, f, indent=4)
        f.close()

validate_path(properties["path"]["cache"])
validate_path(properties["path"]["build"])
validate_path(properties["path"]["run"])

# INIT CLIENT
validate_path(properties["path"]["client"])
# init manifest
manifest_path = join(properties["path"]["client"], "manifest.json")
if not exists(manifest_path):
    with open(manifest_path, "w") as f:
        f.write('''{
  "type": "minecraftModpack",
  "manifestType": "minecraftModpack",
  "manifestVersion": 1,
  "name": "${pack_name}",
  "version": "${version}",
  "author": "MUYU_Twilighter",
  "overrides": ".",
  "minecraft": {
    "version": "${minecraft_version}",
    "modLoaders": [
      {
        "id": "fabric-${loader_version}",
        "primary": true
      }
    ]
  },
  "files": []
}''')
        f.close()
# init client mods dir
client_mods_path = join(properties["path"]["client"], "mods")
if not exists(client_mods_path):
    makedirs(client_mods_path)

# INIT SERVER
validate_path(properties["path"]["server"])
# init start.bat
start_path = join(properties["path"]["server"], "start.bat")
if not exists(start_path):
    with open(start_path, "w") as f:
        f.write("""@echo off

set installer="fabric-server-mc.${minecraft_version}-loader.${loader_version}-launcher.${launcher_version}.jar"
set java_path=java

:: if not exist, download fabric installer

if not exist %installer% (
    curl -o %installer% "https://meta.fabricmc.net/v2/versions/loader/${minecraft_version}/${loader_version}/${launcher_version}/server/jar"
)

:: run fabric installer

%java_path% -jar %installer% -nogui""")
        f.close()
# init server mods dir
server_mods_path = join(properties["path"]["server"], "mods")
if not exists(server_mods_path):
    makedirs(server_mods_path)

# INIT COMMON
validate_path(properties["path"]["common"])
# init common mods dir
common_mods_path = join(properties["path"]["common"], "mods")
if not exists(common_mods_path):
    makedirs(common_mods_path)