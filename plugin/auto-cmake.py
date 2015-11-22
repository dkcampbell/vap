import json
import os
import vim

class CMakeDatabase(object):
    def __init__(self, builds=None):
        if builds is not None:
            self.builds = builds
        else:
            self.builds = {}

    def __str__(self):
        return json.dumps(self.builds, sort_keys=True, indent=4,
                separators=(',', ': '))

def auto_cmake_init():
    # Create build directory if it doesn't already exist
    global bdir
    global bfile
    bdir = os.path.expanduser(vim.eval('g:auto_cmake_build_dir'))
    if not os.path.isdir(bdir):
        os.mkdir(bdir)
    bfile = bdir + '/builds.json'
    # Create configuration file if it doesn't already exits
    if not os.path.exists(bfile):
        db_file = open(bfile, 'w')
        template = {}
        template['source_location'] = {
            'debug': {
                'dir_name'   : 'folder-name',
                'type'       : 'Debug',
                'cc'         : 'clang',
                'cxx'        : 'clang++',
                'toolchain'  : '',
                'extra_args' : '',
                'run'        : '',
                'debug_run'  : '',
                'generator'  : 'Unix Makefiles',
                'default'    : True
            },
            'release': {
                'dir_name'   : 'folder-name',
                'type'       : 'Release',
                'cc'         : 'clang',
                'cxx'        : 'clang++',
                'toolchain'  : '',
                'extra_args' : '',
                'run'        : '',
                'debug_run'  : '',
                'generator'  : 'Unix Makefiles',
                'default'    : False
            }
        }
        db = CMakeDatabase(template)
        db_file.write(str(db))
        db_file.close()
        loadDb()
    else:
        loadDb()

def loadDb():
    global database
    db_file = open(bfile)
    database = CMakeDatabase(json.loads(db_file.read()))
    db_file.close()

def cmake_edit():
    vim.command('edit ' + bfile)

def cmake_reload():
    loadDb()

def cmake_generate():
    cwd = vim.command('pwd')
    if cwd in database.builds:
        if not os.path.exists(cwd):
            os.mkdir(cwd)

def cmake_auto():
    '''
    Fucction to be automatically callled when a CMake directory is found.
    '''
    bname = database.builds['/home/dan/tmp/blob-detect']['name']
    vim.command('set makeprg=make\ -C\ ' + bname)

def debug():
    cmake_auto()
