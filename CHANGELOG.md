# Changelog

## Version 0.3.9
- Add `from __future__ import annotations` to controls.py to not error on Union TypeHint if python version is <=3.9

## Version 0.3.8
- Add `Due_Date` to Task Structure
- App now asks for `Due_Date` on task creation and task update
- Show `days left` on board for task with `Due_Date`
- Show `days left` of most overdue or urgent task for each board when changing boards
- Add `freezegun` as test requirement

## Version 0.3.7
- Bug Fix, `Complete_Time`-Key was wrong in Task Creation, when task was created with `kanban scan`
- Add new function `kanban report` to show a github contribution like visual + creating a `.md` report
- The report is created in a `kanban_report` folder next to the `kanban_boards` folder
- Updated Readme/Docs accordingly

## Version 0.3.6
- Add an `Overview` of Task amounts when changing boards, to get an overview over all Boards
    - Behind the boardname you now have something like `Ready: 05 | Doing: 02 | Done: 10`
    - only tasks amount of columns set as visible are displayed

## Version 0.3.5
- Bug Fix: Datatype `Welcome Task` Duration: str -> int

## Version 0.3.4
- Bug fix: default separator for `settings.scanner` Pattern setting was space separated not comma separated
- Fix Image for kanban configure to show right Pattern

## Version 0.3.3
- Push lower bound Version of `platformdirs` dependency to be 3 or higher to include `ensure_exists` argument
in `user_data_dir` and `user_config_dir`.
- Update User Action Options with new option `Show Task Details`
- Change coloring and order of User Actions
- Added another Menu to configure settings when using `[6] Show Current Settings` or `kanban configure`
- Update DOCS/README and Images
- Bugfix for data type of min col width setter

## Version 0.3.2
- Add `^D` besides `^C` as option to close app (on windows pwsh its `^Z`).
- App closes now on `KeyboardInterrupt` and `EOFError`

## Version 0.3.1
- Bug fix: On first use the kanban_boards folder was not created. And therefore Board creation failed

## Version 0.3.0
- Move to XDG Path convention,
utilize `platformdirs` to write the config file to `user_config_dir` and the task files
to `user_data_dir`.
- added constants.py file for constants like the above mentioned Paths
- added more Tests
- added `platformdirs` <4 dependency
- Updated the docs

## Version 0.2.2
- BUGFIX settings.scanner keys not capitalized
- New Image for Readme

## Version 0.2.1
- New `kanban scan` option to scan for  `# TODO` entries or other patterns.
Check Docs for example and Usage.
- Bug Fix: Prevent ValueError, if active board is not in board_list (couldve happened
if active board was deleted.) Now gives you option to change to other board.
- Add config options for `kanban scan` functionality
- Updated Readme/Docs accordingly

## Version 0.2.0
- Moved the board specific `pykanban.json` files into a dedicated `kanban_boards` directory
in the `.kanban-python` directory under `<BOARDNAME>/pykanban.json`.
This allows centrally stored tasks and doesnt scatter multiple
`pykanban.json` files over your projects.
- Adjusted functions/tests accordingly to new structure
- limiting Namespace of new boardnames to alpha-numeric + `-_ ` due to folder creation
- added default option (active board selection) for board change
- updated docs/readme

## Version 0.1.2
- Instead of `pykanban.ini` configfile in Home Directory
Creates a `.kanban-python` Folder for the respective configfile
- Improved Dialog on first use when config is created
- Documentation update

## Version 0.1.1
- Documentation update

## Version 0.1.0
- published on PyPi
