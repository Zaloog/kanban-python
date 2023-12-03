from json import dump, load

from rich.pretty import pprint

from .config import (
    cfg,
    check_if_board_name_exists_in_config,
    check_if_current_active_board_in_board_list,
    delete_board_from_config,
    get_json_path,
)
from .constants import DUMMY_DB, KANBAN_BOARDS_PATH, TASK_FILE_NAME
from .interface import (
    create_config_table,
    create_table,
    input_ask_for_action,
    input_ask_for_action_settings,
    input_ask_for_change_board,
    input_ask_for_delete_board,
    input_ask_for_new_board_name,
    input_ask_which_task_to_update,
    input_ask_which_tasks_to_show,
    input_change_column_settings,
    input_change_done_limit_settings,
    input_change_files_to_scan_settings,
    input_change_footer_settings,
    input_change_min_col_width_settings,
    input_change_patterns_to_scan_settings,
    input_confirm_add_todos_to_board,
    input_confirm_delete_board,
    input_confirm_set_board_active,
    input_create_new_task,
    input_update_task,
)
from .utils import (
    check_board_name_valid,
    check_if_done_col_leq_X,
    check_if_there_are_visible_tasks_in_board,
    check_scanner_files_valid,
    check_scanner_patterns_valid,
    console,
    current_time_to_str,
    delete_json_file,
    get_tag_id_choices,
    move_first_done_task_to_archive,
    scan_files,
    scan_for_todos,
    split_todo_in_tag_and_title,
)


# DB Controls
#####################################################################################
def create_new_db() -> None:
    while True:
        while True:
            new_board_name = input_ask_for_new_board_name()
            if check_board_name_valid(new_board_name):
                break
            console.print(f":warning:  '{new_board_name}' is [red]not[/] a valid Name.")

        if not check_if_board_name_exists_in_config(new_board_name):
            break
        console.print(
            f":warning:  Board '{new_board_name}' already exists, choose another Name."
        )

    cfg.kanban_boards_dict = new_board_name

    # Options:
    # 1. ~/.kanban-python/<BOARDNAME>.json
    # 2. ~/.kanban-python/kanban_boards/<BOARDNAME>.json
    # 3. ~/.kanban-python/kanban_boards/<BOARDNAME>/pykanban.json  <- THIS
    # 4. ~/.kanban-python/kanban_boards/<BOARDNAME>/<BOARDNAME>.json
    new_db_path = KANBAN_BOARDS_PATH / new_board_name

    if not new_db_path.exists():
        new_db_path.mkdir()

    with open(get_json_path(new_board_name), "w", encoding="utf-8") as f:
        dump(DUMMY_DB, f, ensure_ascii=False, indent=4)

    console.print(
        f"Created new [orange3]{TASK_FILE_NAME}[/] file at "
        + f"[orange3]{KANBAN_BOARDS_PATH / new_board_name}[/] to save tasks."
    )

    if input_confirm_set_board_active(name=new_board_name):
        cfg.active_board = new_board_name


def save_db(data):
    path = cfg.active_board_path
    with open(path, "w", encoding="utf-8") as f:
        dump(data, f, ensure_ascii=False, indent=4)


def add_tasks_to_db(tasks: dict | list[dict]) -> None:
    db_data = read_db()
    if isinstance(tasks, dict):
        new_id = str(max(int(i) for i in db_data.keys()) + 1)
        db_data[new_id] = tasks
    else:
        for task in tasks:
            new_id = str(max(int(i) for i in db_data.keys()) + 1)
            db_data[new_id] = task

    save_db(data=db_data)


def read_db(path: str = None) -> dict:
    if not path:
        path = cfg.active_board_path

    try:
        data = read_single_board(path)
        return data
    except FileNotFoundError:
        print(path)
        console.print(f":warning: No [orange3]{TASK_FILE_NAME}[/] file here anymore.")
        console.print("Please change to another board.")
        change_kanban_board()
    console.print(f"[red]Seems like the previous {TASK_FILE_NAME} file was deleted[/]")
    console.print(f"Create new [orange3]{TASK_FILE_NAME}[/] file here.")
    create_new_db()
    return read_db()


def read_single_board(path):
    with open(path, "r") as file:
        data = load(file)
    return data


# User Action Controls
#####################################################################################
# Get User Action
def get_user_action():
    return input_ask_for_action()


# Action 1
def add_new_task_to_db():
    new_task = input_create_new_task()
    add_tasks_to_db(tasks=new_task)


# Action 2
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


# Action 3
def change_kanban_board():
    new_active_board = input_ask_for_change_board()
    cfg.active_board = new_active_board


# Action 4
def show_tasks():
    db_data = read_db()
    choices = get_tag_id_choices(db_data, cfg.vis_cols)
    selection_criteria = input_ask_which_tasks_to_show(choices)
    for i, task in db_data.items():
        if selection_criteria in [i, task["Tag"]]:
            console.print(
                20 * "[bold blue]#[/]" + f" Task {i} " + 20 * "[bold blue]#[/]"
            )
            pprint(
                {
                    key: val
                    for key, val in task.items()
                    if key in ["Title", "Description", "Tag", "Status"]
                },
                console=console,
                expand_all=True,
            )


# Action 5
def delete_kanban_board():
    board_to_delete = input_ask_for_delete_board()
    if input_confirm_delete_board(board_to_delete):
        board_to_delete_path = cfg.kanban_boards_dict[board_to_delete]

        delete_json_file(board_to_delete_path)
        delete_board_from_config(board_to_delete)


def show():
    if not cfg.kanban_boards:
        console.print(":warning:  [red]No Boards created yet[/]:warning:")
        console.print("Use 'kanban init' to create a new kanban board.")
        raise KeyboardInterrupt

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


# Scan Functionality
#####################################################################################
def add_todos_to_board():
    files = scan_files(endings=cfg.scanned_files)
    todos = scan_for_todos(file_paths=files, patterns=cfg.scanned_patterns)
    if not todos:
        console.print(
            ":cross_mark: [red]Nothing found that "
            + "matches any of your provided patterns.[/]"
        )
        return
    # TODO Write Docs for kanban scan functionality
    # BUG This pattern also works
    if input_confirm_add_todos_to_board(todos=todos):
        todo_task_list = []
        for task, file in todos:
            tag, title = split_todo_in_tag_and_title(task, cfg.scanned_patterns)
            new_task = {
                "Title": title,
                "Description": f"from {file}",
                "Status": "Ready",
                "Tag": tag,
                "Creation_Date": current_time_to_str(),
                "Begin_Time": "",
                "Completion_Time": "",
                "Duration": 0,
            }

            todo_task_list.append(new_task)
        add_tasks_to_db(tasks=todo_task_list)


# Config Settings
#####################################################################################
def change_settings():
    while True:
        show_settings()
        settings_selection = input_ask_for_action_settings()

        if settings_selection == 1:
            change_kanban_board()

            new_min_col_widths = input_change_min_col_width_settings()
            cfg.col_min_width = new_min_col_widths

            done_limit = input_change_done_limit_settings()
            cfg.done_limit = done_limit

            footer_visible = input_change_footer_settings()
            cfg.show_footer = "True" if footer_visible else "False"

        if settings_selection == 2:
            updated_col_config = input_change_column_settings()
            cfg.kanban_columns_dict = updated_col_config

        if settings_selection == 3:
            while True:
                new_files_to_scan = input_change_files_to_scan_settings()
                if check_scanner_files_valid(new_files_to_scan):
                    cfg.scanned_files = new_files_to_scan
                    break
                console.print(
                    f":warning:  '{new_files_to_scan}' is [red]not[/] a valid."
                )

            while True:
                new_patterns_to_scan = input_change_patterns_to_scan_settings()
                if check_scanner_patterns_valid(new_patterns_to_scan):
                    cfg.scanned_patterns = new_patterns_to_scan
                    break
                console.print(
                    f":warning:  '{new_patterns_to_scan}' is [red]not[/] a valid."
                )

        if settings_selection == 4:
            break


def show_settings():
    settings_table = create_config_table()
    console.print(settings_table)
