from datetime import datetime
from pathlib import Path
from random import choice

from rich.console import Console

from kanban_python import __version__

console = Console()


def get_motivational_quote() -> str:
    return choice(QUOTES)


def current_time_to_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_time_delta_str(start_time_str: str, end_time_str: str) -> float:
    date_format = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.strptime(start_time_str, date_format)
    end_time = datetime.strptime(end_time_str, date_format)

    delta = end_time - start_time
    delta_minutes = delta.total_seconds() / 60

    return round(delta_minutes, 2)


def check_db_exists() -> bool:
    return Path("pykanban.json").exists()


def create_status_dict_for_rows(data: dict, vis_cols: list) -> dict:
    status_dict = {col: [] for col in vis_cols}

    for id, task in data.items():
        if not task["Status"] in vis_cols:
            continue
        task_str = f"[[cyan]{id}[/]]" if int(id) > 9 else f"[[cyan]0{id}[/]]"
        task_str += f'([orange3]{task.get("Tag")}[/])'
        task_str += f' [white]{task["Title"]}[/]'
        status_dict[task["Status"]].append(task_str)

    return status_dict


def check_if_there_are_visible_tasks_in_board(data: dict, vis_cols: list) -> bool:
    for task in data.values():
        if task["Status"] in vis_cols:
            return True
    return False


def delete_json_file(board_dict, boardname: str) -> None:
    path = Path(board_dict[boardname] + "/pykanban.json")
    try:
        path.unlink()
    except FileNotFoundError:
        console.print("File already deleted")


def calculate_duration(start, end):
    return end - start


QUOTES = [
    "\n:wave:Stay Hard:wave:",
    "\n:wave:See you later:wave:",
    "\n:wave:Lets get started:wave:",
    "\n:wave:Lets work on those tasks:wave:",
]

CAPTION_STRING = "Tasks have the following Structure:\
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
    "Description": "Welcome to kanban-python, I hope this helps you being productive",
    "Tag": "HI",
    "Status": "Ready",
    "Begin_Time": "",
    "Complete_Time": "",
    "Duration": "0",
    "Creation_Date": current_time_to_str(),
}
DUMMY_DB = {i: DUMMY_TASK for i in range(1, 200)}

FOOTER_FIRST = "kanban-python [grey35](by Zaloog)[/]"
FOOTER_LAST = f"version {__version__}"
FOOTER = [FOOTER_FIRST, FOOTER_LAST]
