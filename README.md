# [Monkey-Shovel][]

Reusable [Shovel][] tasks for projects based on [Monkey][].

## Installation

1. Switch to the directory of your project

        cd $YOUR_PROJECT

1. Create the shovel task directory

        [ ! -d shovel ] && mkdir shovel

1. Add this repository as submodule

        git submodule add git@github.com:michaelcontento/monkey-shovel.git shovel/meta

1. Make it loadable for shovel

        touch shovel/meta.py

    **TODO:** This should be fixed! I have no clue why this is important but
    this file, in combination with `meta/__init__.py`, was the only way to get
    it running.

1. Install all required dependencies

        pip install -r shovel/meta/requirements.txt --use-mirrors

## Tasks

### meta.commandr.build

All tasks are responsible for a single and small job and this is the point where
all tasks in the `meta.commandr` namespace are different. They are "the glue
to build something bigger". And `meta.commandr.build` is capable of
building your project from zero to hero with a single click :)

#### Workflow

1. Read all config files
1. Replace all template files
1. Execute all core commands
1. Execute all app commands
1. Done

#### Config files

Config files are stored as [YAML][] files and loaded from two locations:

1. The global one: `$HOME/.commandr.yml`
1. App local at: `meta/commandr.yml`

Both files are merged together (local overwrites global) and the final result
is used in all further steps.

An example configuration file can be found at [data/example-commandr.yml][].
If you update some paths (like `apps[monkey]` and `apps[wizard]`) this file
should successfully build monkey projects.

#### Template files

All files with the `.tpl` extension are processed and saved under the same name
just without the `.tpl` extension.

This mechanism is very useful to inject configuration values into [Monkey][]. A
small example of this can be found at [data/example-commandr.monkey.tpl].

#### Executed commands

Just define whatever command you want and they get executed in the following
order:

1. `commands['core']['all']`
1. `commands['core'][vendor]` *Example:* `commands['core']['ios']`
1. `commands['app']['all']`
1. `commands['app'][vendor]` *Exmaple:* `commands['app']['ios']`

### meta.icon.resize

Converts the _"mast icon file"_ `meta/icon.png` into all required sizes with and
without rounded borders. It also depends on `meta.pxm.export` so you don't have
to export `.PXM` files manually.

Before:

    meta
    └── icon.png

After:

    meta
    ├── generated
    │   ├── icon-36x36.png
    │   ├── icon-48x48.png
    │   ├── icon-57x57.png
    │   ├── icon-72x72.png
    │   ├── icon-96x96.png
    │   ├── icon-114x114.png
    │   ├── icon-144x144.png
    │   ├── icon-512x512.png
    │   ├── icon-1024x1024.png
    │   ├── icon-rounded-36x36.png
    │   ├── icon-rounded-48x48.png
    │   ├── icon-rounded-57x57.png
    │   ├── icon-rounded-72x72.png
    │   ├── icon-rounded-96x96.png
    │   ├── icon-rounded-114x114.png
    │   ├── icon-rounded-144x144.png
    │   ├── icon-rounded-512x512.png
    │   └── icon-rounded-1024x1024.png
    └── icon.png

### meta.loading.resize

Same as `meta.icon.resize` but just for the _"master loading image"_
`meta/loading.png`.

Before:

    meta
    └── loading.png

After:

    meta
    ├── generated
    │   ├── loading-320x480.png
    │   ├── loading-640x1136.png
    │   ├── loading-640x960.png
    │   ├── loading-768x1024.png
    │   ├── loading-1024x768.png
    │   ├── loading-1536x2048.png
    │   └── loading-2048x1536.png
    └── loading.png

### meta.pxm.export

This task simply looks for all [Pixelmator][] `.PXM` files inside the `meta/`
directory and exports them as `.PNG` file with the same name.

Before:

    meta
    ├── even-in-subdirs
    │   └── some-other-file.pxm
    └── some-file.pxm

After:

    meta
    ├── even-in-subdirs
    │   ├── some-other-file.png
    │   └── some-other-file.pxm
    ├── some-file.png
    └── some-file.pxm

### meta.screenshots.export

Converts all _"mast screenshots"_ `meta/screen-*.png` into all required sizes
and, optionally, merges some overlay images. It also depends on `meta.pxm.export`
so you don't have to export `.PXM` files manually.

What are "overlay images"? Simple transparent `.PNG` files that contain some
buttons, effects or just some text. They are placed over the raw screenshot
to generate the final result (which is saved and scaled to all required sizes).

All files `meta/screen-*.png` and `overlay-*.png` are expected to be in
1024x768. In fact -- that's not quite true for the raw screenshots. They can
also be higher and are trimmed down to 768. This is very nice because it allows
one to simply use OSX screenshots (`alt+shift+4 + space + mouse click`) from the
`GLFW` target (the nasty window border at the top will be removed).

Before:

    meta
    ├── overlay-1.pxm
    ├── overlay-2.pxm
    ├── overlay-3.pxm
    ├── overlay-4.pxm
    ├── screen-1.png
    ├── screen-2.png
    ├── screen-3.png
    └── screen-4.png

After:

    meta
    ├── generated
    │   ├── screen-1-960x640.jpg
    │   ├── screen-1-1024x768.jpg
    │   ├── screen-1-1136x640.jpg
    │   ├── screen-1-1280x720.jpg
    │   ├── screen-2-960x640.jpg
    │   ├── screen-2-1024x768.jpg
    │   ├── screen-2-1136x640.jpg
    │   └── screen-2-1280x720.jpg
    ├── overlay-1.png
    ├── overlay-1.pxm
    ├── overlay-2.png
    ├── overlay-2.pxm
    ├── screen-1.png
    └── screen-2.png

## Development

The [Monkey-Shovel][] source code is hosted on [GitHub][]. It's clean, modular,
and easy to understand, even if you're not a shell hacker.

Please feel free to submit pull requests and file bugs on the [issue tracker][].

## License

    Copyright 2013 Michael Contento <michaelcontento@gmail.com>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

  [GitHub]: https://github.com
  [Monkey-Shovel]: https://github.com/michaelcontento/monkey-shovel
  [issue tracker]: https://github.com/michaelcontento/monkey-shovel/issues
  [Pixelmator]: www.pixelmator.com
  [Monkey]: http://monkeycoder.co.nz/
  [YAML]: http://en.wikipedia.org/wiki/YAML
  [Shovel]: https://github.com/seomoz/shovel
  [data/example-commandr.yml]: http://github.com/michaelcontento/monkey-shovel/tree/master/data/example-commandr.yml
  [data/example-commandr.monkey.tpl]: http://github.com/michaelcontento/monkey-shovel/tree/master/data/example-commandr.monkey.tpl
