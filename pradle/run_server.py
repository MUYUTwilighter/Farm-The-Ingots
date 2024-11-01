from subprocess import run
from os import getcwd
from os.path import join
from shutil import move

src_path = join(getcwd(), "./server")
dst_path = join(getcwd(), "./run")

move(src_path, dst_path)

bat_path = join(getcwd(), "./server/start.bat")
work_path = join(getcwd(), "./run")

run(bat_path, cwd=work_path, shell=True)