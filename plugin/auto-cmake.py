import json
import os
import subprocess
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

def get_current_build():
    return database.builds['/home/dan/tmp/blob-detect']['debug']


# Function auto loaded when a cmake build is found
def cmake_auto():
    '''
    Fucction to be automatically callled when a CMake directory is found.
    '''
    bname = get_current_build()['dir_name']
    vim.command('set makeprg=make\ -C\ ' + bname)


# Public facing functions from the vim plugin
def cmake_edit():
    '''
    Load the build database into vim for editing
    '''
    vim.command('edit ' + bfile)

def cmake_reload():
    '''
    Reload the database (after editing)
    '''
    loadDb()

def cmake_run():
    subprocess.call(get_current_build()['run'], '')

def cmake_debug():
    subprocess.call(get_current_build()['debug'], '')

def cmake_generate():
    '''
    Generate a new cmake build
    '''
    build = get_current_build()

    # Check to see if the build directory already exist, if not create it
    if not os.path.exists(build['dir_name']):
        os.mkdir(build['dir_name'])

    # Generate build files
    output = subprocess.check_output(['cmake', '-B' + build['dir_name'], '-H/home/dan/tmp/blob-detect'])
    # Pipe output to vim
    print(output)

def debug():
    print(subprocess.check_output(['ls', '-al']))
    #cmake_auto()
