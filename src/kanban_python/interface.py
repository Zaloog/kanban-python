from itertools import zip_longest

from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from .config import TASK_FILE, cfg
from .utils import (
    CAPTION_STRING,
    COLOR_DICT,
    FOOTER,
    calculate_time_delta_str,
    console,
    create_status_dict_for_rows,
    current_time_to_str,
)


# Board
#####################################################################################
def create_table(data: dict) -> Table:
    status_dict = create_status_dict_for_rows(data=data, vis_cols=cfg.vis_cols)

    table_name = cfg.active_board
    table = Table(
        title=f"[blue]Active Board: {table_name}[/]",
        highlight=True,
        show_header=True,
        show_footer=True if cfg.show_footer == "True" else False,
        caption=CAPTION_STRING,
    )

    for i, category in enumerate([COLOR_DICT.get(col, col) for col in cfg.vis_cols]):
        table.add_column(
            header=category + f"\t({len(status_dict[cfg.vis_cols[i]])} Task/s)",
            header_style="bold",
            justify="left",
            overflow="fold",
            footer=FOOTER[0]
            if i == 0
            else FOOTER[1]
            if i == len(cfg.vis_cols) - 1
            else "",
            min_width=cfg.col_min_width,
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

    console.print(f"\t[1] {COLOR_DICT['Ready']}")
    console.print(f"\t[2] {COLOR_DICT['Doing']}")
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
        "Status": "Ready" if str(status) == "1" else "Doing",
        "Tag": tag.upper(),
        "Creation_Date": current_time_to_str(),
        "Begin_Time": current_time_to_str() if str(status) == "2" else "",
    }
    return new_task


def input_update_task_title(current_title) -> str:
    return Prompt.ask(
        prompt="[1/4] Update Task Title",
        show_default=True,
        default=current_title,
    )


def input_update_task_description(current_desc) -> str:
    return Prompt.ask(
        prompt="[2/4] Update Task Description",
        show_default=True,
        default=current_desc,
    )


def input_update_task_tag(current_tag) -> str:
    return Prompt.ask(
        prompt="[3/4] Update Tag",
        show_default=True,
        default=current_tag,
    )


def input_update_task(current_task: dict) -> dict:
    title = input_update_task_title(current_task["Title"])
    description = input_update_task_description(current_task["Description"])
    tag = input_update_task_tag(current_task["Tag"])
    status = input_ask_to_what_status_to_move(current_task["Title"])

    if (status == "Doing") and (current_task["Status"] != "Doing"):
        start_doing = current_time_to_str()
        stop_doing = current_task.get("Complete_Time", "")
        duration = current_task.get("Duration", 0)
    elif (status != "Doing") and (current_task["Status"] == "Doing"):
        start_doing = current_task.get("Begin_Time", "")
        stop_doing = current_time_to_str()
        duration = calculate_time_delta_str(
            start_time_str=current_task.get("Begin_Time", ""), end_time_str=stop_doing
        ) + current_task.get("Duration", 0)
    else:
        start_doing = current_task.get("Begin_Time", "")
        stop_doing = current_task.get("Complete_Time", "")
        duration = current_task.get("Duration", 0)

    if status == "Done":
        console.print(
            f":sparkle: Congrats, you just completed '{title}'"
            + f" after {duration} minutes :muscle:"
        )

    updated_task = {
        "Title": title,
        "Description": description,
        "Status": status,
        "Tag": tag.upper(),
        "Begin_Time": start_doing,
        "Complete_Time": stop_doing,
        "Duration": duration,
    }
    current_task.update(updated_task)
    return current_task


def input_ask_which_task_to_update(data: dict) -> str:
    choice_task_ids = [
        id for id, task in data.items() if task["Status"] in cfg.vis_cols
    ]
    task_id_to_update = IntPrompt.ask(
        prompt="Which Task to update?",
        choices=choice_task_ids,
        show_choices=False,
    )
    return str(task_id_to_update)


def input_ask_to_what_status_to_move(task_title):
    possible_status = [cat for cat in cfg.kanban_columns_dict]

    console.print(f'Updating Status of Task "[white]{task_title}[/]"')
    for idx, status in enumerate(possible_status, start=1):
        console.print(f"\t[{idx}] {COLOR_DICT.get(status, status)}")

    new_status = IntPrompt.ask(
        prompt="New Status of Task?",
        show_choices=False,
        choices=[f"{i}" for i, _ in enumerate(possible_status, start=1)],
    )
    return possible_status[int(new_status) - 1]


# TODO not needed anymore i guess
def input_confirm_to_overwrite_db() -> bool:
    console.print(f":warning:  Existing [orange3]{TASK_FILE}[/] found :warning:")
    return Confirm.ask(
        "Do you want to wipe it clean and start from scratch:question_mark:"
    )


def input_confirm_set_board_active(name) -> bool:
    return Confirm.ask(
        f"Do you want to set the Board '{name}' as active:question_mark:"
    )


def input_ask_for_new_board_name() -> str:
    return Prompt.ask(
        prompt="A new folder will be created for your board\n"
        + ":warning:  [yellow]Only[/] use alpha-numeric characters or"
        + " [green]'-', '_', ' '[/] for new board names.\n"
        + "What should the new board be called?"
    )


def input_ask_for_change_board() -> str:
    boards = [b for b in cfg.kanban_boards]
    active_board_idx = boards.index(cfg.active_board) + 1
    for idx, board in enumerate(boards, start=1):
        console.print(f"[{idx}] {board}")

    answer = IntPrompt.ask(
        prompt="Which board to activate",
        choices=[f"{i}" for i, _ in enumerate(boards, start=1)],
        show_choices=False,
        default=active_board_idx,
        show_default=True,
    )
    return boards[int(answer) - 1]


def input_ask_for_delete_board() -> int:
    boards = [b for b in cfg.kanban_boards]
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
    updated_col_config = input_change_column_settings()
    cfg.kanban_columns_dict = updated_col_config

    footer_visible = input_change_footer_settings()
    done_limit = input_change_done_limit_settings()
    cfg.show_footer = "True" if footer_visible else "False"
    cfg.done_limit = done_limit


def input_change_column_settings():
    updated_column_dict = {}
    for col, vis in cfg.kanban_columns_dict.items():
        new_visible = Confirm.ask(
            prompt=f"Should Column {COLOR_DICT.get(col,col)} be visible?",
            default=True if vis == "True" else False,
            show_default=True,
        )
        updated_column_dict[col] = "True" if new_visible else "False"

    return updated_column_dict


def input_change_footer_settings():
    footer_visible = Confirm.ask(
        prompt="Should Footer be visible?",
        default=True if cfg.show_footer == "True" else False,
        show_default=True,
    )

    return footer_visible


def input_change_done_limit_settings():
    done_limit = IntPrompt.ask(
        prompt=f"What should the Limit of Tasks in {COLOR_DICT.get('Done','Done')} "
        + f"Column be, before moving to {COLOR_DICT.get('Archived','Archived')}?",
        default=cfg.done_limit,
        show_default=True,
    )

    return str(done_limit)


def input_confirm_change_current_settings():
    return Confirm.ask(
        prompt="Do you want to change :hammer_and_wrench: [grey69]Settings[/]?",
        default=False,
        show_default=True,
    )


def create_config_table():
    settings_table = Table(
        title=":hammer_and_wrench:  [grey69]Settings Overview[/]:hammer_and_wrench:",
        highlight=True,
        show_header=True,
        caption="pykanban.ini file is located in your "
        + "[light_green]$Home/.kanban-python[/] Directory",
    )
    for col in ["Option", "Current Value"]:
        settings_table.add_column(
            header=col,
            header_style="bold",
            justify="left",
            overflow="fold",
            min_width=30,
        )
    for section in cfg.config:
        if section:
            settings_table.add_section()
            settings_table.add_row(f"[blue]{section}[/]", "")
        for key, val in cfg.config[section].items():
            settings_table.add_row(key, val)

    return settings_table
