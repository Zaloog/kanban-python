from json import dump, load

from .config import (
    add_new_board_to_config,
    check_config_exists,
    check_if_board_name_exists_in_config,
    create_init_config,
    delete_current_folder_board_from_config,
    get_active_db_path,
    set_board_to_active,
)
from .interface import (
    create_table,
    input_ask_for_action,
    input_ask_for_change_board,
    input_ask_for_new_board_name,
    input_ask_which_task_to_update,
    input_confirm_set_board_active,
    input_confirm_to_overwrite_db,
    input_create_new_task,
    input_update_task,
)
from .utils import DUMMY_DB, check_db_exists, console


def create_new_db() -> None:
    if not check_config_exists():
        create_init_config()
        console.print("Created new [orange3]pykanban.ini[/] file @Home Directory")

    OVERWRITTEN_FLAG = False
    if check_db_exists():
        OVERWRITTEN_FLAG = True
        if not input_confirm_to_overwrite_db():
            return

    while True:
        new_name = input_ask_for_new_board_name()
        if not check_if_board_name_exists_in_config(new_name):
            break
        console.print(
            f":warning:  Board '{new_name}' already exists, choose a different name"
        )
    if OVERWRITTEN_FLAG:
        delete_current_folder_board_from_config()

    add_new_board_to_config(board_name=new_name)

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


def read_db(path: str = None) -> dict:
    if not path:
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


def update_task_from_db():
    db_data = read_db()
    selected_id = input_ask_which_task_to_update(db_data)
    updated_task = input_update_task(current_task=db_data[selected_id])
    db_data[selected_id] = updated_task
    save_db(data=db_data)


def get_user_action():
    return input_ask_for_action()
