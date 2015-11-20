import json
import os
import vim

class CMakeDatabase(object):
    def __init__(self, builds):
        self.builds = builds

    def dump():
        for build in builds:
            json.dump(build.dump)

class CMakeBuild(object):
    pass

def auto_cmake_init():
    global bdir
    bdir = os.path.expanduser(vim.eval('g:auto_cmake_build_dir'))
    if not os.path.isdir(bdir):
        os.mkdir(bdir)

def hello_vim():
    print(bdir)
