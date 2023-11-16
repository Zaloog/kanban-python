from datetime import datetime
from pathlib import Path
from random import choice

from rich.console import Console

from .config import get_list_of_visible_columns, read_config

console = Console()


def get_motivational_quote():
    return choice(QUOTES)


def current_time_to_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_db_exists() -> bool:
    return Path("pykanban.json").exists()


def create_task_strings_for_rows(data):
    ready, doing, done = "", "", ""

    for id, task in data.items():
        task_id = f"[[cyan]{id}[/]]" if int(id) > 9 else f"[[cyan]0{id}[/]]"
        task_tag = f'([orange3]{task.get("Tag")}[/])'
        task_title = f' [white]{task["Title"]}[/]\n'
        task_total_str = task_id + task_tag + task_title
        if task["Status"] == "Ready":
            ready += task_total_str
        if task["Status"] == "Doing":
            doing += task_total_str
        if task["Status"] == "Done":
            done += task_total_str

    return ready, doing, done


def check_if_there_are_visible_tasks_in_board(data):
    visible_columns = get_list_of_visible_columns()
    for task in data.values():
        if task["Status"] in visible_columns:
            return True
    return False


def delete_json_file(boardname):
    config = read_config()
    path = Path(config["kanban_boards"][boardname] + "/pykanban.json")
    try:
        path.unlink()
    except FileExistsError:
        console.print("File already deleted")


QUOTES = ["\n:wave:Stay Hard:wave:", "\n:wave:See you later:wave:"]
CAPTION_STRING = "Tasks have the following Structure:\
     [[cyan]ID[/]] ([orange3]TAG[/]) [white]Task Title[/]"

COLUMN_COLOR_DICT = {
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
