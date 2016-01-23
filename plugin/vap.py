#Copyright (c) 2015-2016, Dan Campbell <dan@compiledworks.com>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import json
import os
import shutil
import subprocess
import vim

VAP_TARGET  = None
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

def vap_init():
    # Create build directory if it doesn't already exist
    global BUILD_FILE
    BUILD_FILE = os.path.expanduser(vim.eval('g:vap_config'))

    # Create configuration file if it doesn't already exits
    if not os.path.exists(BUILD_FILE):
        db_file = open(BUILD_FILE, 'w')
        template = {}
        template['source_dir'] = {
            'debug': {
                'cc'         : 'clang',
                'cxx'        : 'clang++',
                'debug_run'  : [],
                'default'    : True,
                'build_dir'  : 'folder-name',
                'extra_args' : [],
                'generator'  : 'Unix Makefiles',
                'run'        : [],
                'toolchain'  : '',
                'type'       : 'DEBUG',
                'ycm'        : False
            },
            'release': {
                'cc'         : 'clang',
                'cxx'        : 'clang++',
                'debug_run'  : [],
                'default'    : False,
                'build_dir'   : 'folder-name',
                'extra_args' : [],
                'generator'  : 'Unix Makefiles',
                'run'        : [],
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

def get_script_directory():
    return vim.eval('s:cwd')

def get_current_build():
    cwd = os.getcwd()
    if cwd in DATABASE.builds:
        # If a target is manually set automatically return it
        if VAP_TARGET is not None:
            return DATABASE.builds[cwd][VAP_TARGET]
        # If target isn't manually selected search for the default
        for build in DATABASE.builds[cwd]:
                if DATABASE.builds[cwd][build]['default']:
                    return DATABASE.builds[cwd][build]
    else:
        return None

def set_make_prg(build):
    if 'generator' in build:
        if build['generator'] == 'Unix Makefiles':
            vim.command('set makeprg=make\ -C\ ' + build['build_dir'])
        elif build['generator'] == 'Ninja':
            vim.command('set makeprg=ninja\ -C\ ' + build['build_dir'])

    # Assume the default is makefiles
    else:
        vim.command('set makeprg=make\ -C\ ' + build['build_dir'])

def set_ycm_conf(build):
    if 'ycm' in build:
        if build['ycm']:
            vim.command('let g:ycm_global_ycm_extra_conf=\'' +
                        build['build_dir'] + '/.ycm_extra_conf.py\'')

def dispatch_run(cmd):
    if cmd is '':
        print('Command not configured')
        return

    try:
        print('Dispatch ' + ' '.join(cmd))
        vim.command('Dispatch ' + ' '.join(cmd))
    except:
        output = subprocess.check_output(cmd)
        print(output)

# Function auto loaded when a projects directory is found
def vap_auto():
    '''
    Function to be automatically callled when a project directory is found.
    '''
    build = get_current_build()

    if build is not None:
        set_make_prg(build)
        set_ycm_conf(build)

# Public facing functions from the vim plugin
def vap_edit():
    '''
    Load the build database into vim for editing
    '''
    vim.command('edit ' + BUILD_FILE)

def vap_reload():
    '''
    Reload the projects database stored in memory.
    '''
    loadDb()
    # Auto load updated settings
    vap_auto()

def vap_run():
    dispatch_run(get_current_build()['run'])

def vap_debug():
    dispatch_run(get_current_build()['debug_run'])

def vap_set_target(target):
    '''
    Each project supports multiple builds. This function is used if you want
    to select a build thats not the default.
    '''
    global VAP_TARGET
    VAP_TARGET = target
    # Reload settings with the new target assigned
    vap_auto()

def vap_cmake_generate():
    '''
    Generate a new cmake build
    '''
    build = get_current_build()

    if build is None:
        print('Could not find project')
        return

    # Check to see if the build directory already exist, if not create it
    if not os.path.exists(build['build_dir']):
        os.mkdir(build['build_dir'])

    command = [
        'cmake',
        '-B' + build['build_dir'],
        '-H' + os.getcwd()
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

    # Run CMake
    dispatch_run(command)

    # Copy the YCM file over if appropriate
    if 'ycm' in build and build['ycm']:
        srcFile = get_script_directory() + '/../ycm_extra_conf.py'
        dstFile = build['build_dir'] + '.ycm_extra_conf.py'
        shutil.copy2(srcFile, dstFile)

