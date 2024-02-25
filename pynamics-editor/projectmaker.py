import os
import shutil
import compileall
import presets

__lib__ = os.path.dirname(os.path.abspath(__file__))

def make_directory(dir:str):
    os.mkdir(dir)
    shutil.copytree(__lib__ + "/lib-1.0.0", dir + "/pynamics_1_0_0")
    compileall.compile_dir(dir + "/pynamics_1_0_0")

def make_basicfile(dir: str):
    f = open(dir + "/main.py", "w")
    f.write(presets.MAIN)
    f.close()