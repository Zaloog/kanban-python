import calendar
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from random import choice

from rich.console import Console
from rich.progress import MofNCompleteColumn, Progress

from .constants import QUOTES, REPORT_FILE_NAME, REPORT_FILE_PATH

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
        # Add days left
        if all((task["Status"] in ["Ready", "Doing"], task.get("Due_Date", False))):
            days_left = calculate_days_left_till_due(task["Due_Date"])
            task_str += f" |[red]{days_left:02d}[/]|"
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


def scan_for_todos(
    file_paths: list, rel_path=Path.cwd(), patterns: list = ["#TODO", "# TODO"]
) -> list:
    todos = []
    with Progress(MofNCompleteColumn(), *Progress.get_default_columns()) as prog:
        task = prog.add_task("Files searched for TODOs...", total=len(file_paths))

        for file_path in file_paths:
            prog.update(task_id=task, advance=1)
            with open(file_path, "r") as file:
                try:
                    todos += [
                        (line.strip(), str(Path(file_path).relative_to(rel_path)))
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


def get_tag_id_choices(data_dict: dict, vis_cols: list) -> list:
    valid_ids = [i for i, task in data_dict.items() if task["Status"] in vis_cols]
    valid_tags = [
        task["Tag"] for task in data_dict.values() if task["Status"] in vis_cols
    ]

    valid_choices = list(set(valid_ids + valid_tags))
    return valid_choices


def check_scanner_files_valid(files: str) -> bool:
    for file in files.split(" "):
        if not file.startswith("."):
            return False
        if not all(char.isalpha() for char in file[1:]):
            return False
    return True


def check_scanner_patterns_valid(patterns: str) -> bool:
    for pattern in patterns.split(","):
        if not pattern.startswith("#"):
            return False
    return True


def get_iso_calender_info(date_str: str):
    year, week, weekday = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").isocalendar()
    return year, week, weekday


def create_dict_for_report_view(completed_tasks: list):
    report_dict = defaultdict(lambda: defaultdict(int))
    max_val = 0
    current_year = datetime.now().year
    for task in completed_tasks:
        year, week, day = get_iso_calender_info(task["Complete_Time"])
        if year != current_year:
            continue
        report_dict[day][week] += 1
        max_val = max(max_val, report_dict[day][week])

    return max_val, report_dict


def create_color_mapping(amount_list: list, max_val: int):
    mapped_list = []
    for val in amount_list:
        if val == 0:
            mapped_list.append(0)
        elif (val / max_val) <= 0.25:
            mapped_list.append(1)
        elif (val / max_val) <= 0.5:
            mapped_list.append(2)
        elif (val / max_val) <= 0.75:
            mapped_list.append(3)
        elif (val / max_val) <= 1:
            mapped_list.append(4)
        else:
            continue

    return mapped_list


def create_report_document(boards_dict: dict):
    date_dict = defaultdict(list)
    for _, task_dict in boards_dict.items():
        for _, task in task_dict.items():
            if not task["Complete_Time"]:
                continue
            completion_date = datetime.strptime(
                task["Complete_Time"], "%Y-%m-%d %H:%M:%S"
            ).date()
            date_dict[completion_date].append(f"- {task['Tag']} {task['Title']}\n")

    with open(REPORT_FILE_PATH / REPORT_FILE_NAME, "w") as report_file:
        last_year = ""
        last_month = ""
        last_day = ""
        for date, completed in sorted(date_dict.items()):
            if date.year != last_year:
                last_year = date.year
                report_file.write(f"# Tasks Completed in {date.year}\n")

            if date.month != last_month:
                last_month = date.month
                report_file.write(f"## {calendar.month_name[date.month]}\n")

            if date.day != last_day:
                last_day = date.day
                report_file.write(f"### {date}\n")

            report_file.write("".join(completed))

    return date_dict


def check_due_date_format(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def due_date_datetime_to_date(date_datetime: str) -> str:
    if date_datetime:
        date_str = str(datetime.strptime(date_datetime, "%Y-%m-%d %H:%M:%S").date())
        return date_str
    return date_datetime


def due_date_date_to_datetime(date_str: str) -> str:
    if date_str:
        date_datetime = str(
            datetime.strptime(f"{date_str} 23:59:59", "%Y-%m-%d %H:%M:%S")
        )
        return date_datetime
    return date_str


def calculate_days_left_till_due(due_date: str):
    time_now = datetime.now()
    time_due = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")

    delta_days = (time_due - time_now).days
    return delta_days
