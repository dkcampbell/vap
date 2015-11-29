"auto-projects.vim A personalized projects management plugin
"Maintainer:   Dan Campbell <http://compiledworks.com>
"Version:      0.0

"if exists('g:loaded_auto_projects') || &cp
"    finish
"else
"    let g:loaded_auto_projects = 1
"endif

if !has('python')
    finish
endif

if !exists('g:auto_projects_config')
    let g:auto_projects_config = '~/builds.json'
endif

let s:cwd = escape(expand('<sfile>:p:h'), '\')
exe 'pyfile ' . s:cwd . '/auto-projects.py'

"Initialize the build directory if this is the first time auto-cmake is used.
python auto_cmake_init()
"If in a cmake project diretory load the appropriate settings
python cmake_auto()

command! CMake         : python debug()
command! CMakeEdit     : python cmake_edit()
command! CMakeGenerate : python cmake_generate()
command! CMakeReload   : python cmake_reload()
command! CMakeRun      : python cmake_run()
command! CMakeDebug    : python cmake_debug()
