from itertools import zip_longest

from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from .config import (
    get_active_db_name,
    get_dict_of_all_columns,
    get_list_of_current_boards,
    get_list_of_visible_columns,
    read_config,
    save_config,
)
from .utils import (
    CAPTION_STRING,
    COLUMN_COLOR_DICT,
    FOOTER,
    console,
    create_status_dict_for_rows,
    current_time_to_str,
)


# Board
#####################################################################################
def create_table(data: dict):
    config = read_config()
    footer_setting = config["settings.general"]["Show_Footer"]
    status_dict = create_status_dict_for_rows(data=data)
    vis_cols = get_list_of_visible_columns()

    table_name = get_active_db_name()
    table = Table(
        title=f"[blue]{table_name}[/]",
        highlight=True,
        show_header=True,
        show_footer=True if footer_setting == "True" else False,
        caption=CAPTION_STRING,
    )

    for i, category in enumerate([COLUMN_COLOR_DICT.get(col, col) for col in vis_cols]):
        table.add_column(
            header=category + f"\t({len(status_dict[vis_cols[i]])} Task/s)",
            header_style="bold",
            justify="left",
            overflow="fold",
            footer=FOOTER[0] if i == 0 else FOOTER[1] if i == len(vis_cols) - 1 else "",
            min_width=int(config["settings.general"]["Column_Min_Width"]),
        )

    for row_tasks in zip_longest(*status_dict.values()):
        table.add_row(*row_tasks)

    return table


def input_ask_for_action():
    console.print(
        "[yellow]Whats up!?[/], how can I help you being productive today :rocket:?"
    )
    console.print(
        "\t[1] :clipboard: [green]Create new Task[/]"
        + 2 * "\t"
        + "[2] :clockwise_vertical_arrows: [bold blue]Update/Check Task[/]"
    )
    console.print(
        "\t[3] :bookmark_tabs: [bold yellow]Change Kanban Board[/]"
        + "\t"
        + "[4] :cross_mark: [red]Delete Kanban Board[/]"
    )
    console.print("\t[5] :hammer_and_wrench:  [grey69]Show Current Settings[/]")
    action = IntPrompt.ask(
        prompt="Choose wisely :books:",
        choices=[
            "1",
            "2",
            "3",
            "4",
            "5",
        ],
        show_choices=False,
    )
    return action


def input_create_new_task() -> dict:
    title = Prompt.ask(
        prompt="[1/4] Add Task Title",
    )

    description = Prompt.ask(
        prompt="[2/4] Add Task Description",
        show_default=True,
        default=None,
    )

    tag = Prompt.ask(
        prompt="[3/4] Add a Tag",
        show_default=True,
        default="ETC",
    )

    console.print(f"\t[1] {COLUMN_COLOR_DICT['Ready']}")
    console.print(f"\t[2] {COLUMN_COLOR_DICT['Doing']}")
    status = IntPrompt.ask(
        prompt="[4/4] Status of Task",
        show_choices=False,
        choices=["1", "2"],
        show_default=True,
        default="1",
    )

    new_task = {
        "Title": title,
        "Description": description,
        "Status": "Ready" if status == "1" else "Doing",
        "Tag": tag.upper(),
        "Creation_Date": current_time_to_str(),
    }
    return new_task


def input_update_task(current_task: dict) -> dict:
    title = Prompt.ask(
        prompt="[1/4] Update Task Title",
        show_default=True,
        default=current_task["Title"],
    )
    description = Prompt.ask(
        prompt="[2/4] Update Task Description",
        show_default=True,
        default=current_task["Description"],
    )
    tag = Prompt.ask(
        prompt="[3/4] Update Tag", show_default=True, default=current_task["Tag"]
    )
    status = input_ask_to_what_status_to_move(current_task)
    updated_task = {
        "Title": title,
        "Description": description,
        "Status": status,
        "Tag": tag.upper(),
    }
    current_task.update(updated_task)
    return current_task


def input_ask_which_task_to_update(data):
    visible_cols = get_list_of_visible_columns()
    choice_task_ids = [
        id for id, task in data.items() if task["Status"] in visible_cols
    ]
    task_id_to_update = IntPrompt.ask(
        prompt="Which Task to update?",
        choices=choice_task_ids,
        show_choices=False,
    )
    return str(task_id_to_update)


def input_ask_to_what_status_to_move(current_task):
    task_title = current_task["Title"]
    col_dict = get_dict_of_all_columns()
    possible_status = [cat for cat in col_dict]

    console.print(f'Updating Status of Task "[white]{task_title}[/]"')
    for idx, status in enumerate(possible_status, start=1):
        console.print(f"\t[{idx}] {COLUMN_COLOR_DICT.get(status, status)}")

    new_status = IntPrompt.ask(
        prompt="New Status of Task?",
        show_choices=False,
        choices=[f"{i}" for i, _ in enumerate(possible_status, start=1)],
    )
    return possible_status[int(new_status) - 1]


def input_confirm_to_overwrite_db() -> bool:
    console.print(":warning:  Existing [orange3]pykanban.json[/] found :warning:")
    return Confirm.ask(
        "Do you want to wipe it clean and start from scratch:question_mark:"
    )


def input_confirm_set_board_active(name) -> bool:
    return Confirm.ask(
        f"Do you want to set the Board '{name}' as active:question_mark:"
    )


def input_ask_for_new_board_name():
    return Prompt.ask(prompt="What should the new board be called?")


def input_ask_for_change_board():
    boards = [b for b in get_list_of_current_boards()]
    for idx, board in enumerate(boards, start=1):
        console.print(f"[{idx}] {board}")

    answer = IntPrompt.ask(
        prompt="Which board to activate",
        choices=[f"{i}" for i, _ in enumerate(boards, start=1)],
        show_choices=False,
    )
    return boards[int(answer) - 1]


def input_ask_for_delete_board() -> int:
    boards = [b for b in get_list_of_current_boards()]
    for idx, board in enumerate(boards, start=1):
        console.print(f"[{idx}] {board}")

    answer = IntPrompt.ask(
        prompt="Which board to delete",
        choices=[f"{i}" for i, _ in enumerate(boards, start=1)],
        show_choices=False,
    )
    return boards[int(answer) - 1]


def input_confirm_delete_board(name) -> bool:
    return Confirm.ask(
        f"Are you sure you want to delete the Board '{name}':question_mark:"
    )


# Config Settings
#####################################################################################
def input_change_settings():
    config = read_config()
    updated_col_config = input_change_column_settings(config)
    config["settings.columns.visible"] = updated_col_config

    updated_general_config = input_change_general_settings(config)
    config["settings.general"] = updated_general_config
    save_config(config)


def input_change_column_settings(config):
    current_column_dict = config["settings.columns.visible"]
    for col, vis in current_column_dict.items():
        new_visible = Confirm.ask(
            prompt=f"Should Column {COLUMN_COLOR_DICT.get(col,col)} be visible?",
            default=True if vis == "True" else False,
            show_default=True,
        )
        current_column_dict[col] = "True" if new_visible else "False"

    return current_column_dict


def input_change_general_settings(config):
    current_general_dict = config["settings.general"]
    footer_visible = Confirm.ask(
        prompt="Should Footer be visible?",
        default=True if current_general_dict["Show_Footer"] == "True" else False,
        show_default=True,
    )
    current_general_dict["Show_Footer"] = "True" if footer_visible else "False"

    return current_general_dict


def input_confirm_change_current_settings():
    return Confirm.ask(
        prompt="Do you want to change :hammer_and_wrench: [grey69]Settings[/]?",
        default=False,
        show_default=True,
    )


def create_config_table():
    config = read_config()
    settings_table = Table(
        title=":hammer_and_wrench:  [grey69]Settings Overview[/]:hammer_and_wrench:",
        highlight=True,
        show_header=True,
        caption="pykanban.ini file is located in your [light_green]$Home[/] Directory",
    )
    for col in ["Option", "Current Value"]:
        settings_table.add_column(
            header=col,
            header_style="bold",
            justify="left",
            overflow="fold",
            min_width=30,
        )
    for section in config:
        if section:
            settings_table.add_section()
            settings_table.add_row(f"[blue]{section}[/]", "")
        for key, val in config[section].items():
            settings_table.add_row(key, val)

    return settings_table
