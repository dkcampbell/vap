import vim

def hello_vim():
    build_directory = vim.eval('g:auto_cmake_build_dir')
    print(build_directory)
