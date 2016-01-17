"VAP A plugin for project configuration
"Maintainer:   Dan Campbell <https://compiledworks.com>
"Version:      0.0

if exists('g:loaded_vap') || &cp
    finish
else
    let g:loaded_vap = 1
endif

if !has('python')
    finish
endif

if !exists('g:vap_config')
    let g:vap_config = '~/builds.json'
endif

let s:cwd = escape(expand('<sfile>:p:h'), '\')
exe 'pyfile ' . s:cwd . '/vap.py'

"Initialize the builds.json file if this is the first time auto-projects is used.
python vap_init()

"If in a projects diretory load the appropriate settings
python vap_auto()

command! CMakeGenerate   : python vap_cmake_generate()
command! Edit            : python vap_edit()
command! Reload          : python vap_reload()
command! Run             : python vap_run()
command! Debug           : python vap_debug()
command! -nargs=1 Target : python vap_set_target(<f-args>)
