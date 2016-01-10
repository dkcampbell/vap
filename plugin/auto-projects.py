import json
import os
import subprocess
import vim

AP_TARGET  = None
BUILD_FILE = None
DATABASE   = None

class ProjectDatabase(object):
    def __init__(self, builds=None):
        if builds is not None:
            self.builds = builds
        else:
            self.builds = {}

    def __str__(self):
        return json.dumps(self.builds, sort_keys=True, indent=4,
                separators=(',', ': '))

def loadDb():
    global DATABASE
    db_file = open(BUILD_FILE)
    DATABASE = ProjectDatabase(json.loads(db_file.read()))
    db_file.close()

def auto_projects_init():
    # Create build directory if it doesn't already exist
    global BUILD_FILE
    BUILD_FILE = os.path.expanduser(vim.eval('g:auto_projects_config'))

    # Create configuration file if it doesn't already exits
    if not os.path.exists(BUILD_FILE):
        db_file = open(BUILD_FILE, 'w')
        template = {}
        template['source_location'] = {
            'debug': {
                'cc'         : 'clang',
                'cxx'        : 'clang++',
                'debug_run'  : '',
                'default'    : True,
                'dir_name'   : 'folder-name',
                'extra_args' : [],
                'generator'  : 'Unix Makefiles',
                'run'        : '',
                'toolchain'  : '',
                'type'       : 'DEBUG',
                'ycm'        : False
            },
            'release': {
                'cc'         : 'clang',
                'cxx'        : 'clang++',
                'debug_run'  : '',
                'default'    : False,
                'dir_name'   : 'folder-name',
                'extra_args' : [],
                'generator'  : 'Unix Makefiles',
                'run'        : '',
                'toolchain'  : '',
                'type'       : 'RELEASE',
                'ycm'        : False
            }
        }
        db = ProjectDatabase(template)
        db_file.write(str(db))
        db_file.close()
        loadDb()
    else:
        loadDb()

def get_vim_cwd():
    return vim.eval('getcwd()')

def get_current_build():
    cwd = get_vim_cwd()
    if cwd in DATABASE.builds:
        # If a target is manually set automatically return it
        if AP_TARGET is not None:
            return DATABASE.builds[cwd][AP_TARGET]
        # If target isn't manually selected search for the default
        for build in DATABASE.builds[cwd]:
                if DATABASE.builds[cwd][build]['default']:
                    return DATABASE.builds[cwd][build]
    else:
        return None

def set_make_prg(build):
    if 'generator' in build:
        if build['generator'] == 'Unix Makefiles':
            vim.command('set makeprg=make\ -C\ ' + build['dir_name'])
        elif build['generator'] == 'Ninja':
            vim.command('set makeprg=ninja\ -C\ ' + build['dir_name'])

    # Assume the default is makefiles
    else:
        vim.command('set makeprg=make\ -C\ ' + build['dir_name'])

def set_ycm_conf(build):
    if 'ycm' in build:
        if build['ycm']:
            vim.command('let g:ycm_global_ycm_extra_conf=\'' + build['dir_name'] + '/.ycm_extra_conf.py\'')

def dispatch_run(cmd):
    try:
        print('Dispatch ' + ' '.join(cmd))
        vim.command('Dispatch ' + ' '.join(cmd))
    except:
        output = subprocess.check_output(cmd)
        print(output)

# Function auto loaded when a projects directory is found
def projects_auto():
    '''
    Function to be automatically callled when a project directory is found.
    '''
    build = get_current_build()

    if build is not None:
        set_make_prg(build)
        set_ycm_conf(build)

# Public facing functions from the vim plugin
def ap_edit():
    '''
    Load the build database into vim for editing
    '''
    vim.command('edit ' + BUILD_FILE)

def ap_reload():
    '''
    Reload the projects database stored in memory.
    '''
    loadDb()
    # Auto load updated settings
    projects_auto()

def ap_run():
    subprocess.call(get_current_build()['run'], '')

def ap_debug():
    subprocess.call(get_current_build()['debug'], '')

def ap_set_target(target):
    '''
    Each project supports multiple builds. This function is used if you want
    to select a build thats not the default.
    '''
    global AP_TARGET
    AP_TARGET = target
    # Reload settings with the new target assigned
    projects_auto()

def ap_cmake_generate():
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
        command.append("'" + build['generator'] + "'")

    dispatch_run(command)

