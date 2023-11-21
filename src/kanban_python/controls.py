from json import dump, load

from .config import (
    cfg,
    check_config_exists,
    check_current_path_exists_for_board,
    check_if_board_name_exists_in_config,
    check_if_current_active_board_in_board_list,
    create_init_config,
    delete_board_from_config,
    delete_current_folder_board_from_config,
)
from .interface import (
    create_config_table,
    create_table,
    input_ask_for_action,
    input_ask_for_change_board,
    input_ask_for_delete_board,
    input_ask_for_new_board_name,
    input_ask_which_task_to_update,
    input_change_settings,
    input_confirm_change_current_settings,
    input_confirm_delete_board,
    input_confirm_set_board_active,
    input_confirm_to_overwrite_db,
    input_create_new_task,
    input_update_task,
)
from .utils import (
    DUMMY_DB,
    check_db_exists,
    check_if_done_col_leq_X,
    check_if_there_are_visible_tasks_in_board,
    console,
    delete_json_file,
    move_first_done_task_to_archive,
)


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
            f":warning:  Board '{new_name}' already exists, choose a different Name."
        )

    if OVERWRITTEN_FLAG or check_current_path_exists_for_board():
        delete_current_folder_board_from_config()
        cfg.active_board = new_name

    cfg.kanban_boards_dict = new_name

    with open("pykanban.json", "w", encoding="utf-8") as f:
        dump(DUMMY_DB, f, ensure_ascii=False, indent=4)

    console.print("Created new [orange3]pykanban.json[/] file to save tasks")

    if input_confirm_set_board_active(name=new_name):
        cfg.active_board = new_name


def save_db(data):
    path = cfg.active_board_path
    with open(f"{path}/pykanban.json", "w", encoding="utf-8") as f:
        dump(data, f, ensure_ascii=False, indent=4)


def add_tasks_to_db():
    db_data = read_db()
    new_id = str(max(int(i) for i in db_data.keys()) + 1)
    db_data[new_id] = input_create_new_task()
    save_db(data=db_data)


def read_db(path: str = None) -> dict:
    if not path:
        path = cfg.active_board_path

    try:
        data = read_single_board(path)
        return data
    except FileNotFoundError:
        console.print(":warning: No [orange3]pykanban.json[/] file here anymore.")
        change_kanban_board()
    console.print("[red]Seems like the previous pykanban.json file was deleted[/]")
    console.print("Create new [orange3]pykanban.json[/] file here.")
    create_new_db()
    return read_db()


def read_single_board(path):
    with open(f"{path}/pykanban.json", "r") as file:
        data = load(file)
    return data


def show():
    if not check_if_current_active_board_in_board_list():
        console.print(
            "[yellow]Hmm, Something went wrong.[/] "
            + f"The active board '{cfg.active_board}' is not in the list of boards."
        )
        change_kanban_board()
        show()
        return
    db_data = read_db()
    table = create_table(data=db_data)
    console.print(table)


def change_kanban_board():
    new_active_board = input_ask_for_change_board()
    cfg.active_board = new_active_board


def delete_kanban_board():
    board_to_delete = input_ask_for_delete_board()
    if input_confirm_delete_board(board_to_delete):
        board_to_delete_path = cfg.kanban_boards_dict[board_to_delete]

        delete_json_file(board_to_delete_path)
        delete_board_from_config(board_to_delete)


def update_task_from_db():
    db_data = read_db()
    if not check_if_there_are_visible_tasks_in_board(db_data, cfg.vis_cols):
        console.print(":cross_mark:[red]No Tasks available on this Kanban board[/]")
        return
    selected_id = input_ask_which_task_to_update(db_data)
    updated_task = input_update_task(current_task=db_data[selected_id])
    db_data[selected_id] = updated_task

    while not check_if_done_col_leq_X(cfg=cfg, data=db_data):
        first_task_id, archive_task = move_first_done_task_to_archive(data=db_data)
        db_data[first_task_id] = archive_task
    save_db(data=db_data)


def get_user_action():
    return input_ask_for_action()


def change_settings():
    input_change_settings()


def show_settings():
    settings_table = create_config_table()
    console.print(settings_table)
    if input_confirm_change_current_settings():
        change_settings()
