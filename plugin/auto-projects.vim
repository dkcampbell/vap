"auto-projects.vim A personalized projects management plugin
"Maintainer:   Dan Campbell <http://compiledworks.com>
"Version:      0.0

if exists('g:loaded_auto_projects') || &cp
    finish
else
    let g:loaded_auto_projects = 1
endif

if !has('python')
    finish
endif

if !exists('g:auto_projects_config')
    let g:auto_projects_config = '~/builds.json'
endif

let s:cwd = escape(expand('<sfile>:p:h'), '\')
exe 'pyfile ' . s:cwd . '/auto-projects.py'

"Initialize the builds.json file if this is the first time auto-projects is used.
python auto_projects_init()
"If in a projects diretory load the appropriate settings
python projects_auto()

command! PDebug          : python debug()
command! CMakeGenerate   : python ap_cmake_generate()
command! Edit            : python ap_edit()
command! Reload          : python ap_reload()
command! Run             : python ap_run()
command! -nargs=1 Target : python ap_set_target(<f-args>)
command! Debug           : python ap_debug()
