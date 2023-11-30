import os
from datetime import datetime
from pathlib import Path
from random import choice

from rich.console import Console
from rich.progress import MofNCompleteColumn, Progress

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


def check_if_done_col_leq_X(cfg, data: dict) -> bool:
    done_col_idxs = [idx for idx, t in data.items() if t["Status"] == "Done"]
    return len(done_col_idxs) <= cfg.done_limit


def check_if_there_are_visible_tasks_in_board(data: dict, vis_cols: list) -> bool:
    for task in data.values():
        if task["Status"] in vis_cols:
            return True
    return False


def move_first_done_task_to_archive(data: dict):
    first_task_id = [idx for idx, t in data.items() if t["Status"] == "Done"][0]
    updated_task = data[first_task_id]
    updated_task["Status"] = "Archived"

    return first_task_id, updated_task


def delete_json_file(db_path: str) -> None:
    path = Path(db_path)
    try:
        path.unlink()
        path.parent.rmdir()
        console.print(f"File under {path.parent} was now removed")
    except FileNotFoundError:
        console.print("File already deleted")


def check_board_name_valid(boardname: str):
    checker = "".join(x for x in boardname if (x.isalnum() or x in "_- "))
    return True if (checker == boardname) else False


def scan_files(path=Path.cwd(), endings: list = [".py"]):
    def recursive_search(path, file_list: list, progress):
        for entry in os.scandir(path):
            try:
                if entry.is_dir(follow_symlinks=False) and not entry.name.startswith(
                    "."
                ):
                    recursive_search(
                        path=entry.path, file_list=file_list, progress=progress
                    )

                elif entry.is_file(follow_symlinks=False):
                    if any(entry.path.endswith(ending) for ending in endings):
                        file_list.append(entry.path)
                        prog.update(task_id=task, advance=1)
            except PermissionError:
                continue

    file_list = []
    with Progress(transient=True) as prog:
        task = prog.add_task("[blue]Collecting files...", total=None)
        recursive_search(path=path, file_list=file_list, progress=prog)

    return file_list


def scan_for_todos(file_paths: list, patterns: list = ["#TODO", "# TODO"]) -> list:
    todos = []
    with Progress(MofNCompleteColumn(), *Progress.get_default_columns()) as prog:
        task = prog.add_task("Files searched for TODOs...", total=len(file_paths))

        for file_path in file_paths:
            prog.update(task_id=task, advance=1)
            with open(file_path, "r") as file:
                try:
                    todos += [
                        (line.strip(), Path(file_path).relative_to(Path.cwd()))
                        for line in file.readlines()
                        if any(line.strip().startswith(pattern) for pattern in patterns)
                    ]
                except UnicodeDecodeError:
                    continue

    return todos


def split_todo_in_tag_and_title(todo: str, patterns: list):
    for pattern in patterns:
        if pattern in todo:
            tag = "".join(c for c in pattern if c.isalnum())
        if not todo.split(pattern)[0]:
            title = todo.split(pattern)[1].strip()
            title = title[1:].strip() if title.startswith(":") else title

    return tag.upper(), title


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
    "Description": "Welcome to kanban-python, I hope this helps your productivity",
    "Tag": "HI",
    "Status": "Ready",
    "Begin_Time": "",
    "Complete_Time": "",
    "Duration": "0",
    "Creation_Date": current_time_to_str(),
}
DUMMY_DB = {1: DUMMY_TASK}

FOOTER_LINK = "[link=https://github.com/Zaloog/kanban-python][blue]kanban-python[/]"
FOOTER_AUTHOR = "[/link][grey35] (by Zaloog)[/]"
FOOTER_FIRST = FOOTER_LINK + FOOTER_AUTHOR

FOOTER_LAST = f"version [blue]{__version__}[/]"
FOOTER = [FOOTER_FIRST, FOOTER_LAST]
