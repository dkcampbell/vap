VAP
===

VAP is a project configuration plugin for Vim. Useful for people who work with
several CMake based projects. A JSON configuration file is used to change the
behavior of Vim depending on the project you're currently working on.

Here's a few features of VAP:

* Automatically set the `makeprg` variable to use the Makefile located in the project's out-of-source build.
* Configure YouCompleteMe to use a CMake generated code completion database.
* Easily support multiple build targets with CMake.
* Simplifies use of non-default compilers
* Convenience commands for running and debugging executables
* Integration with vim-dispatch plugin for performing asynchronous task


VAP is suitable for daily use. There will be no effort to make VAP backwards
compatible until a stable version 1.0 is released.


VAP version: 0.5

Code name: "Good enough"

## Installation ##
If you use [Vundle](https://github.com/gmarik/vundle), add the following line
to your '~/.vimrc':
```vim
Plugin 'dkcampbell/vap'
```

## Tutorial ##
The first time Vim is run after VAP is installed a `builds.json` file will be
created in `$HOME/builds.json`. Here is a quick glance at the default
`builds.json` file:

```json
{
    "source_dir": {
        "debug": {
            "build_dir": "folder-name",
            "cc": "clang",
            "cxx": "clang++",
            "debug_run": [],
            "default": true,
            "extra_args": [],
            "generator": "Unix Makefiles",
            "run": [],
            "toolchain": "",
            "type": "DEBUG",
            "ycm": false
        },
        "release": {
            "build_dir": "folder-name",
            "cc": "clang",
            "cxx": "clang++",
            "debug_run": [],
            "default": false,
            "extra_args": [],
            "generator": "Unix Makefiles",
            "run": [],
            "toolchain": "",
            "type": "RELEASE",
            "ycm": false
        }
    }
}
```

The configuration above is an example of a single project with two build
targets. The source_dir is the location of the project. If Vim is started in
this directory VAP will configure the various project settings you have
specified for the current build target. The particular target chosen by VAP
is whichever has "default" set to true.

You can use the `:Edit` command to load `builds.json` file into a buffer for
easy editing. Here is a modified example used for an actual project I'm
working on:

```json
{
    "/home/dan/git/immovable-objects": {
        "debug": {
            "cc": "clang",
            "cxx": "clang++",
            "debug_run": [
                "/home/dan/builds/imo-debug-clang/blob"
            ],
            "default": true,
            "build_dir": "/home/dan/builds/imo-debug-clang/",
            "extra_args": [
                "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"
            ],
            "generator": "Unix Makefiles",
            "run": [
                "/home/dan/builds/imo-debug-clang/blob"
            ],
            "toolchain": "",
            "type": "DEBUG",
            "ycm": true
        },
        "release": {
            "cc": "clang",
            "cxx": "clang++",
            "debug_run": [
                "/home/dan/builds/imo-release-clang/blob"
            ],
            "default": false,
            "build_dir": "/home/dan/builds/imo-release-clang/",
            "extra_args": [],
            "generator": "Unix Makefiles",
            "run": [
                "/home/dan/builds/imo-release-clang/blob"
            ],
            "toolchain": "",
            "type": "RELEASE",
            "ycm": true
        }
    }
}
```

This will automatically load the debug target for the immovable-objects
project when Vim is started in the `/home/dan/git/immovable-objects`
directory.  Among the things it does is set various CMake configuration
tweaks. For example, when `:CMakeGenerate` is executed it will place the build
files in the `build_dir` folder. The `extra_args` will be passed to CMake just
as you would pass them on the command line. VAP will also properly setup the
`:make` command to work for this project. I can also launch the executable using
the `:Run` command, which will execute what is configured in the target for the
`run` property. For more information what the available options do see the
documentation with `:help VAP`.
