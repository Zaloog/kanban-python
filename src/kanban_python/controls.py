from json import dump, load

from .config import add_new_board, get_active_db_path, set_board_to_active
from .interface import (
    create_table,
    input_ask_for_change_board,
    input_ask_for_new_board_name,
    input_ask_to_what_category_to_move,
    input_ask_which_task_to_move,
    input_confirm_set_board_active,
    input_confirm_to_overwrite_db,
    input_create_new_task,
)
from .utils import DUMMY_DB, check_db_exists, console

# from pathlib import Path


def create_new_db() -> None:
    if check_db_exists():
        if not input_confirm_to_overwrite_db():
            return

    new_name = input_ask_for_new_board_name()
    add_new_board(board_name=new_name)

    with open("pykanban.json", "w", encoding="utf-8") as f:
        dump(DUMMY_DB, f, ensure_ascii=False, indent=4)

    if input_confirm_set_board_active(name=new_name):
        set_board_to_active(board_name=new_name)

    console.print("Created new [orange3]pykanban.json[/] file to save tasks")
    # TODO Motivational Quote


def save_db(data):
    path = get_active_db_path()
    with open(f"{path}/pykanban.json", "w", encoding="utf-8") as f:
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
    path = get_active_db_path()
    with open(f"{path}/pykanban.json", "r") as file:
        data = load(file)
    return data


def show():
    db_data = read_db()
    table = create_table(data=db_data)
    console.print(table)


def change_kanban_board():
    new_active_board = input_ask_for_change_board()
    set_board_to_active(board_name=new_active_board)
