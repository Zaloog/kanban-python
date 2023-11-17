from datetime import datetime
from pathlib import Path
from random import choice

from rich.console import Console

from kanban_python import __version__

from .config import cfg

console = Console()


def get_motivational_quote() -> str:
    return choice(QUOTES)


def current_time_to_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_db_exists() -> bool:
    return Path("pykanban.json").exists()


def create_status_dict_for_rows(data: dict, vis_cols: list) -> dict:
    status_dict = {col: [] for col in vis_cols}

    for id, task in data.items():
        if not task["Status"] in vis_cols:
            continue
        task_id = f"[[cyan]{id}[/]]" if int(id) > 9 else f"[[cyan]0{id}[/]]"
        task_tag = f'([orange3]{task.get("Tag")}[/])'
        task_title = f' [white]{task["Title"]}[/]'
        task_total_str = task_id + task_tag + task_title
        status_dict[task["Status"]].append(task_total_str)

    return status_dict


def check_if_there_are_visible_tasks_in_board(data: dict) -> bool:
    for task in data.values():
        if task["Status"] in cfg.vis_cols:
            return True
    return False


def delete_json_file(boardname: str) -> None:
    path = Path(cfg.config["kanban_boards"][boardname] + "/pykanban.json")
    try:
        path.unlink()
    except FileNotFoundError:
        console.print("File already deleted")


QUOTES = ["\n:wave:Stay Hard:wave:", "\n:wave:See you later:wave:"]
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
    "Tag": "Hi",
    "Status": "Ready",
    "Creation_Date": current_time_to_str(),
}
DUMMY_DB = {1: DUMMY_TASK}

FOOTER_FIRST = "kanban-python [grey35](by Zaloog)[/]"
FOOTER_LAST = f"version {__version__}"
FOOTER = [FOOTER_FIRST, FOOTER_LAST]
