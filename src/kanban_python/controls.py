from json import dump, load
from pathlib import Path

from rich.console import Console

from .interface import create_table, input_create_new_task
from .utils import current_time_to_str

DUMMY_TASK = {
    "Title": "Test Task",
    "Description": "Non-existent",
    "Tag": "Cool Tag",
    "Status": "ready",
    "Date": current_time_to_str(),
}
DUMMY_DB = {i: DUMMY_TASK for i in range(1, 5)}


def create_new_db(args: dict) -> None:
    name = args.new
    if args.globally:
        name = Path.home() / name

    with open(f"{name}.json", "w", encoding="utf-8") as f:
        dump(DUMMY_DB, f, ensure_ascii=False, indent=4)

    # TODO check if db already exists
    print(f"Created new {name}.json file to save tasks")


def check_db_exists(name: str) -> bool:
    pass


def save_db(data):
    with open("pykanban.json", "w", encoding="utf-8") as f:
        dump(data, f, ensure_ascii=False, indent=4)


def add_tasks_to_db():
    db_data = read_db()
    new_id = str(max(int(i) for i in db_data.keys()) + 1)
    db_data[new_id] = input_create_new_task()
    save_db(data=db_data)


def move_tasks_to_other_column():
    db_data = read_db()
    new_id = str(max(int(i) for i in db_data.keys()) + 1)
    db_data[new_id] = input_create_new_task()
    save_db(data=db_data)


def read_db():
    with open("pykanban.json", "r") as file:
        data = load(file)
    return data


def show():
    db_data = read_db()
    table = create_table(data=db_data)
    console = Console()
    console.print(table)
