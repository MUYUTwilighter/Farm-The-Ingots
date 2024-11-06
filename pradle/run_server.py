from subprocess import run
from os.path import join

from lib import properties, copy_content2run, fhandle_placeholders

server_path = properties["path"]["server"]
common_path = properties["path"]["common"]
run_path = properties["path"]["run"]

print("Preparing working environment")
copy_content2run(common_path)
copy_content2run(server_path)

bat_path = join(run_path, "start.bat")
fhandle_placeholders(bat_path)

print("Running server")
run("start.bat", cwd=run_path, shell=True)