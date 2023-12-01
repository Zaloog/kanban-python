from pathlib import Path

from platformdirs import user_config_dir, user_data_dir

from kanban_python import __version__

# For Config Stuff
TASK_FILE_NAME = "pykanban.json"
CONFIG_FILE_NAME = "pykanban.ini"
KANBAN_BOARDS_FOLDER_NAME = "kanban_boards"

CONFIG_PATH = Path(
    user_config_dir(appname="kanban-python", appauthor=False, ensure_exists=True)
)
DATA_PATH = Path(
    user_data_dir(appname="kanban-python", appauthor=False, ensure_exists=True)
)
KANBAN_BOARDS_PATH = DATA_PATH / KANBAN_BOARDS_FOLDER_NAME
CONFIG_FILE_PATH = CONFIG_PATH / CONFIG_FILE_NAME


QUOTES = [
    "\n:wave:Stay Hard:wave:",
    "\n:wave:See you later:wave:",
    "\n:wave:Lets get started:wave:",
    "\n:wave:Lets work on those tasks:wave:",
]

BOARD_CAPTION_STRING = "Tasks have the following Structure:\
     [[cyan]ID[/]] ([orange3]TAG[/]) [white]Task Title[/]"

COLOR_DICT = {
    "Ready": "[red]Ready[/]",
    "Doing": "[yellow]Doing[/]",
    "Done": "[green]Done[/]",
    "Deleted": "[deep_pink4]Deleted[/]",
    "Archived": "[dark_goldenrod]Archived[/]",
}

DUMMY_TASK = {
    "Title": "Welcome Task",
    "Description": "Welcome to kanban-python, I hope this helps your productivity",
    "Tag": "HI",
    "Status": "Ready",
    "Begin_Time": "",
    "Complete_Time": "",
    "Duration": "0",
    "Creation_Date": "",
}
DUMMY_DB = {1: DUMMY_TASK}

FOOTER_LINK = "[link=https://github.com/Zaloog/kanban-python][blue]kanban-python[/]"
FOOTER_AUTHOR = "[/link][grey35] (by Zaloog)[/]"
FOOTER_FIRST = FOOTER_LINK + FOOTER_AUTHOR

FOOTER_LAST = f"version [blue]{__version__}[/]"
FOOTER = [FOOTER_FIRST, FOOTER_LAST]
