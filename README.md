<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/kanban-python.svg?branch=main)](https://cirrus-ci.com/github/<USER>/kanban-python)
[![ReadTheDocs](https://readthedocs.org/projects/kanban-python/badge/?version=latest)](https://kanban-python.readthedocs.io/en/stable/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/kanban-python.svg)](https://anaconda.org/conda-forge/kanban-python)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/kanban-python)
-->

[![Coveralls](https://img.shields.io/coveralls/github/Zaloog/kanban-python/main.svg)](https://coveralls.io/r/Zaloog/kanban-python)
[![PyPI-Server](https://img.shields.io/pypi/v/kanban-python.svg)](https://pypi.org/project/kanban-python/)
[![Monthly Downloads](https://pepy.tech/badge/kanban-python/month)](https://pepy.tech/project/kanban-python)
[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
# kanban-python

> A Terminal Kanban Application written in Python to boost your productivity :rocket:

## Introduction
Welcome to **kanban-python**, your Terminal Kanban Board Manager.

The [clikan] Kanban App inspired me to write
my own Terminal Kanban Application, since I preferred a more simple and guided workflow.

**kanban-python** also comes with more features and customization options.
This package was developed with [pyscaffold], which provides nice project templates
and takes over much of the boilerplate for python packaging.
Which was a great help for developing my first package.

## Features
- *colorful and interactive*: kanban-python uses [rich] under the hood to process user input
and display nice looking tables to the terminal.

- *configfile*: A `pykanban.ini` file gets created on first initialization in your `Home`-Directory.
This can be edited manually or within the kanban-python application. It tracks the location for all your created boards
![configfile](https://github.com/Zaloog/kanban-python/blob/main/images/image_config.PNG)

- *storage-file for each board*: Each created board comes with its own name and `pykanban.json` file,
which stores all tasks for that board.

- *column customization*: kanban-python comes with 5 pre-defined colored columns: [Ready, Doing, Done, Archived, Deleted]
More column can be added in the `pykanban.ini`, also the visibility can be configured.

- *time-tracking*: for each task it is tracked, how long it was in the
 <span style="color:green">Doing</span> column.


## Installation
You can install kanban-python with:
```bash
python -m pip install kanban-python
```

## Usage
There are 3 commands available after installation of kanban-python:

### Create new Boards
  ```bash
  kanban init
  ```
Is used to create a new kanban board i.e. it asks for a name and then creates a `pykanban.json` file with a Welcome Task.
On first use, it will also create the `pykanban.ini` configfile automatically.
![init_file](https://github.com/Zaloog/kanban-python/blob/main/images/image_kanban_init.PNG)

### Interact with Tasks/Boards
  ```bash
  kanban
  ```
This is your main command to interact with your boards and tasks. It also gives the option to show the current settings and adjust them.
Adjusting the settings can also be done directly by using the 3rd command which is:
![kanban](https://github.com/Zaloog/kanban-python/blob/main/images/image_kanban.PNG)

### Change Settings
  ```bash
  kanban configure
  ```
![settings](https://github.com/Zaloog/kanban-python/blob/main/images/image_kanban_configure.PNG)

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.

[clikan]: https://github.com/kitplummer/clikan
[pyscaffold]: https://pyscaffold.org/
[rich]: https://github.com/Textualize/rich
