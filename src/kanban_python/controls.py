from json import dump, load
from pathlib import Path

from .interface import (
    create_table,
    input_ask_to_what_category_to_move,
    input_ask_which_task_to_move,
    input_create_new_task,
)
from .utils import DUMMY_DB, console


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
    selected_id = input_ask_which_task_to_move(data=db_data)
    target_status = input_ask_to_what_category_to_move(data=db_data, id=selected_id)
    db_data[selected_id]["Status"] = target_status
    save_db(data=db_data)


def read_db():
    with open("pykanban.json", "r") as file:
        data = load(file)
    return data


def show():
    db_data = read_db()
    table = create_table(data=db_data)
    console.print(table)
