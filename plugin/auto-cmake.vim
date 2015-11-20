" auto-cmake.vim A personalized cmake integration plugin
" Maintainer:   Dan Campbell <http://compiledworks.com>
" Version:      0.0

if exists('g:loaded_auto_cmake') || &compatible
    finish
else
    let g:loaded_auto_cmake = 1
endif

if !has('python')
    finish
endif

if !exists('g:auto_cmake_build_dir')
    let g:auto_cmake_build_dir = '~/builds'
endif

function! CMake()

endfunc
