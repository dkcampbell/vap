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
    global bfile
    bfile = os.path.expanduser(vim.eval('g:auto_cmake_builds_config'))

    # Create configuration file if it doesn't already exits
    if not os.path.exists(bfile):
        db_file = open(bfile, 'w')
        template = {}
        template['source_location'] = {
            'debug': {
                'dir_name'   : 'folder-name',
                'type'       : 'DEBUG',
                'cc'         : 'clang',
                'cxx'        : 'clang++',
                'toolchain'  : '',
                'extra_args' : [],
                'run'        : '',
                'debug_run'  : '',
                'generator'  : 'Unix Makefiles',
                'default'    : True
            },
            'release': {
                'dir_name'   : 'folder-name',
                'type'       : 'RELEASE',
                'cc'         : 'clang',
                'cxx'        : 'clang++',
                'toolchain'  : '',
                'extra_args' : [],
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

def get_vim_cwd():
    return vim.eval('getcwd()')

def get_current_build():
    cwd = get_vim_cwd()
    if cwd in database.builds:
        # TODO: support multiple builds
        return database.builds[cwd]['debug']
    else:
        return None

# TODO: Make this more robust
def set_make_prg(build):
    if 'generator' in build:
        if build['generator'] == 'Unix Makefiles':
            vim.command('set makeprg=make\ -C\ ' + build['dir_name'])
        elif build['generator'] == 'Ninja':
            vim.command('set makeprg=ninja\ -C\ ' + build['dir_name'])

    # Assume the default is makefiles
    else:
        vim.command('set makeprg=make\ -C\ ' + build['dir_name'])



# Function auto loaded when a cmake build is found
def cmake_auto():
    '''
    Fucction to be automatically callled when a CMake directory is found.
    '''
    build = get_current_build()

    if build is not None:
        set_make_prg(build)


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

    if build is None:
        print('Could not find project')
        return

    # Check to see if the build directory already exist, if not create it
    if not os.path.exists(build['dir_name']):
        os.mkdir(build['dir_name'])

    command = [
        'cmake',
        '-B' + build['dir_name'],
        '-H' + get_vim_cwd()
    ]

    # Check if option is a non-empty string
    if 'cc' in build and build['cc']:
        os.environ['CC'] = build['cc']

    if 'cxx' in build and build['cxx']:
        os.environ['CXX'] = build['cxx']

    if 'type' in build and build['type']:
        command.append('-DCMAKE_BUILD_TYPE=' + build['type'])

    if 'toolchain' in build and build['toolchain']:
        command.append('-DCMAKE_TOOLCHAIN_FILE=' + build['toolchain'])

    if 'extra_args' in build:
        for arg in build['extra_args']:
            command.append(arg)

    if 'generator' in build and build['generator']:
        command.append('-G')
        command.append(build['generator'])

    # Generate build files
    output = subprocess.check_output(command)
    # Pipe output to vim
    print(output)

def debug():
    print(get_vim_cwd())
