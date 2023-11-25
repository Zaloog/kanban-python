<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/kanban-python.svg?branch=main)](https://cirrus-ci.com/github/<USER>/kanban-python)
[![ReadTheDocs](https://readthedocs.org/projects/kanban-python/badge/?version=latest)](https://kanban-python.readthedocs.io/en/stable/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/kanban-python.svg)](https://anaconda.org/conda-forge/kanban-python)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/kanban-python)
[![Monthly Downloads](https://pepy.tech/badge/kanban-python/month)](https://pepy.tech/project/kanban-python)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![PyPI-Server](https://img.shields.io/pypi/v/kanban-python.svg)](https://pypi.org/project/kanban-python/)
[![Downloads](https://static.pepy.tech/badge/kanban-python)](https://pepy.tech/project/kanban-python)
[![Coveralls](https://img.shields.io/coveralls/github/Zaloog/kanban-python/main.svg)](https://coveralls.io/r/Zaloog/kanban-python)

# kanban-python

> A Terminal Kanban Application written in Python to boost your productivity :rocket:

## Introduction
Welcome to **kanban-python**, your Terminal Kanban-Board Manager.

![header](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_header.PNG)
The [clikan] Kanban App inspired me to write
my own Terminal Kanban Application, since I preferred a more simple and guided workflow.

**kanban-python** also comes with more features and customization options.
This package was developed with [pyscaffold], which provides nice project templates
and takes over much of the boilerplate for python packaging.
It was a great help for developing my first package.

## Features
- *colorful and interactive*: kanban-python uses [rich] under the hood to process user input
and display nice looking tables to the terminal.

- *configfile*: A `pykanban.ini` file gets created on first initialization in a `.kanban-python` folder in your `Home`-Directory.
This can be edited manually or within the kanban-python application. It tracks the location for all your created boards. \
![configfile](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_config.PNG)
   * `Active_Board`: current board that is shown when using `kanban`-command
   * `Done_Limit`: If the amount of tasks exceed this number in the  <span style="color:green">Done</span> column,
   the first task of that column gets its status updated to <span style="color:gold">Archived</span> and is moved into that column. (default: 10)
   * `Column_Min_Width`: Sets the minimum width of columns. (default: 40)
   * `Show_Footer`: Shows the table footer with package name and version. (default: True)

   <br />

- *storage-file for each board*: Each created board comes with its own name and `pykanban.json` file,
which stores all tasks for that board. The files are stored in board specific folders under `.kanban-python/kanban_boards/<BOARDNAME>`

- *column customization*: kanban-python comes with 5 pre-defined colored columns: [Ready, Doing, Done, Archived, Deleted]
More column can be added manually in the `pykanban.ini`, also the visibility can be configured.

- *time-tracking*: for each task it is tracked, how long it was in the
 <span style="color:yellow">Doing</span> column, based on the moments when you update the task status.
 The initial Task structure on creation looks as follows:
![task](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_task_example.PNG)


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
On first use of any command, the `pykanban.ini` configfile and the `.kanban-python` folder will be created automatically.
![init_file](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_kanban_init.PNG)

### Interact with Tasks/Boards
  ```bash
  kanban
  ```
This is your main command to interact with your boards and tasks. It also gives the option to show the current settings and adjust them.
Adjusting the settings can also be done directly by using the third command `kanban configure`:
![kanban](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_kanban.PNG)

Use `Ctrl-C` to exit the application at any time. :warning: If you exit in the middle of creating/updating a task,
or changing settings, your progress wont be saved.

### Change Settings
  ```bash
  kanban configure
  ```
![settings](https://raw.githubusercontent.com/Zaloog/kanban-python/main/images/image_kanban_configure.PNG)

To create a new custom Columns, you have to edit the `pykanban.ini` manually and add a new columnname + visibility status
under the `settings.columns.visible` section.


## Feedback and Issues
Feel free to reach out and share your feedback, or open an Issue, if something doesnt work as expected.
Also check the [Changelog](https://raw.githubusercontent.com/Zaloog/kanban-python/main/CHANGELOG.md) for new updates.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.

[clikan]: https://github.com/kitplummer/clikan
[pyscaffold]: https://pyscaffold.org/
[rich]: https://github.com/Textualize/rich
