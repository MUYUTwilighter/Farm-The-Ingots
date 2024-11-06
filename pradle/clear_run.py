from lib import properties
from os import exists, makedirs
from shutil import rmtree

RUN_PATH = properties["path"]["run"]

if exists(RUN_PATH):
    rmtree(RUN_PATH)
makedirs(RUN_PATH)

print("Cleared run directory")