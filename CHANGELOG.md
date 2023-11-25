# Changelog

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
