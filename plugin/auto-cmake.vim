"auto-cmake.vim A personalized cmake integration plugin
"Maintainer:   Dan Campbell <http://compiledworks.com>
"Version:      0.0

"if exists('g:loaded_auto_cmake') || &cp
"    finish
"else
"    let g:loaded_auto_cmake = 1
"endif

if !has('python')
    finish
endif

if !exists('g:auto_cmake_build_dir')
    let g:auto_cmake_build_dir = '~/builds'
endif

let s:cwd = escape(expand('<sfile>:p:h'), '\')
exe 'pyfile ' . s:cwd . '/auto-cmake.py'

"Initialize the build directory if this is the first time auto-cmake is used.
python auto_cmake_init()

command! CMake         : python debug()
command! CMakeEdit     : python cmake_edit()
command! CMakeGenerate : python cmake_generate()
command! CMakeReload   : python cmake_reload()
command! CMakeRun      : python cmake_run()
command! CMakeDebug    : python cmake_debug()
