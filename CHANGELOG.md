# Changelog

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
