from itertools import zip_longest

from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from .config import cfg
from .constants import BOARD_CAPTION_STRING, COLOR_DICT, CONFIG_FILE_PATH, FOOTER
from .utils import (
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
        caption=BOARD_CAPTION_STRING,
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
        + "[2] :clockwise_vertical_arrows: [bold cornflower_blue]Update/Check Task[/]"
    )
    console.print(
        "\t[3] :bookmark_tabs: [bold yellow]Change Kanban Board[/]"
        + "\t"
        + "[4] :magnifying_glass_tilted_left: [bold blue]Show Task Details[/]"
    )
    console.print(
        "\t[5] :cross_mark: [red]Delete Kanban Board[/]"
        + "\t"
        + "[6] :hammer_and_wrench:  [grey69]Show Current Settings[/]"
    )
    action = IntPrompt.ask(
        prompt="Choose wisely :books:",
        choices=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
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
        "Complete_Time": "",
        "Duration": 0,
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
        prompt="Which Task to update? Select an [[cyan]Id[/]]",
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
        prompt="[4/4] New Status of Task?",
        show_choices=False,
        choices=[f"{i}" for i, _ in enumerate(possible_status, start=1)],
    )
    return possible_status[int(new_status) - 1]


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
    boards = cfg.kanban_boards
    # if active Board is not in Board List dont show default
    try:
        active_board_idx = boards.index(cfg.active_board) + 1
    except ValueError:
        active_board_idx = None

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


def input_ask_for_delete_board() -> str:
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


def input_confirm_show_all_todos() -> bool:
    return Confirm.ask(
        prompt="Do you want to list all of them?",
        default=True,
        show_default=True,
    )


def print_all_todos(todos: list) -> None:
    pattern_dict = {pat: f"[orange3]{pat}[/]" for pat in cfg.scanned_patterns}

    for i, (todo, path) in enumerate(todos, start=1):
        todo_string = f"[cyan]{i}[/]) " if i > 9 else f"[cyan]0{i}[/]) "
        for pat, col_pat in pattern_dict.items():
            todo = todo.replace(pat, col_pat)
        todo_string += f"{todo:<90} "
        todo_string += f"[blue]{str(path):>10}[/] "
        console.print(todo_string)


def input_confirm_add_todos_to_board(todos) -> bool:
    # Question Also print tasks already in Board?
    console.print(f"Found [blue]{len(todos)}[/] TODOs.")
    if len(todos) > 10:
        if input_confirm_show_all_todos():
            print_all_todos(todos)
    else:
        print_all_todos(todos)

    return Confirm.ask(
        prompt="Add found Tasks to active board?", default=False, show_default=True
    )


def input_ask_which_tasks_to_show(choices):
    return Prompt.ask(
        prompt="What Task/s to show? Select an [[cyan]Id[/]] or ([orange3]Tag[/])?",
        default=False,
        show_default=False,
        choices=choices,
        show_choices=False,
    )


# Config Settings
#####################################################################################


# Ask for Actions
def input_ask_for_action_settings():
    console.print(
        "[yellow]Not happy with current settings!?[/],"
        + "which [blue]Section[/] do you want to change :hammer_and_wrench:?"
    )
    console.print(
        "\t[1] :clipboard: [blue]settings.general[/]"
        + 2 * "\t"
        + "[2] :eye:  [blue]settings.columns.visibility[/]"
    )
    console.print(
        "\t[3] :magnifying_glass_tilted_left: [blue]settings.scanner[/]"
        + 2 * "\t"
        + "[4] :cross_mark: [red]Go back to Kanban Board[/]"
    )
    action = IntPrompt.ask(
        prompt="Choose [blue]Section[/], where you want to change the Current Value",
        choices=[
            "1",
            "2",
            "3",
            "4",
        ],
        show_choices=False,
    )
    return action


# Show current Config Table
def create_config_table():
    settings_table = Table(
        title=":hammer_and_wrench:  [grey69]Settings Overview[/]:hammer_and_wrench:",
        highlight=True,
        show_header=True,
        caption=f"Your config file is located under [light_green]{CONFIG_FILE_PATH}[/]",
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


# Change settings.general
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


def input_change_min_col_width_settings():
    new_min_col_width = IntPrompt.ask(
        prompt="What should the minimum Column Width be?",
        default=cfg.col_min_width,
        show_default=True,
    )

    return new_min_col_width


# Change settings.columns.visible
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


# Change settings.scanner
def input_change_files_to_scan_settings():
    files_to_scan = Prompt.ask(
        prompt="Which Files to scan? Enter [green]' '[/] separated File Endings",
        default=" ".join(cfg.scanned_files),
        show_default=True,
    )

    return files_to_scan


def input_change_patterns_to_scan_settings():
    files_to_scan = Prompt.ask(
        prompt="Which Patterns to scan? Enter [green]','[/] separated Patterns",
        default=" ".join(cfg.scanned_patterns),
        show_default=True,
    )

    return files_to_scan
