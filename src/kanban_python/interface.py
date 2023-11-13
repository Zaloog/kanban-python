from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from .utils import console, create_task_strings_for_rows, current_time_to_str


def create_table(data: dict):
    table = Table(
        show_header=True,
        show_footer=False,
        caption="Tasks have the following Structure:"
        + " [[cyan]ID[/]] ([orange3]TAG[/]) [white]Task Title[/]",
    )

    for category in ["[red]Ready[/]", "[yellow]Doing[/]", "[green]Done[/]"]:
        table.add_column(
            header=category,
            header_style="bold",
            justify="left",
            overflow="fold",
            min_width=40,
        )

    ready, doing, done = create_task_strings_for_rows(data=data)
    table.add_row(ready, doing, done)

    return table


def input_ask_for_action():
    console.print(
        "[yellow]Whats up!?[/], how can I help you being productive today :rocket:?"
    )
    console.print("\t[1] :clipboard: [green]Create new Task[/]")
    console.print("\t[2] :clockwise_vertical_arrows: [bold blue]Move Task[/]")
    console.print("\t[3] :cross_mark: [bold red]Close Kanban Board[/]")
    task = IntPrompt.ask(
        prompt="Choose wisely :books:",
        choices=[
            "1",
            "2",
            "3",
        ],
        show_choices=False,
    )
    return task


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
        default="OTHER",
    )

    status = Prompt.ask(
        prompt="[4/4] Status of Task",
        show_choices=True,
        choices=["ready", "doing"],
        show_default=True,
        default="ready",
    )

    new_task = {
        "Title": title,
        "Description": description,
        "Status": status,
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

    # reuse move prompt, take numbers
    status = Prompt.ask(
        prompt="[4/4] Update Status of Task",
        show_choices=True,
        choices=["ready", "doing"],
        show_default=True,
        default=current_task["Status"],
    )

    updated_task = {
        "Title": title,
        "Description": description,
        "Status": status,
        "Tag": tag.upper(),
    }
    current_task.update(updated_task)
    return current_task


def input_ask_which_task_to_move(data):
    possible_task_ids = [ids for ids, task in data.items() if task["Status"] != "done"]
    task_id_to_move = Prompt.ask(
        prompt="[1/2] Which task from "
        + "[bold red]Ready[/]|[yellow]Doing[/]"
        + " do you want to move?",
        choices=possible_task_ids,
        show_choices=False,
    )
    return task_id_to_move


def input_ask_to_what_category_to_move(data, id):
    current_status = data[id]["Status"]
    color_dict = {
        "ready": "[red]ready[/]",
        "doing": "[yellow]doing[/]",
        "done": "[green]done[/]",
    }
    possible_status = [
        cat for cat in ["ready", "doing", "done"] if current_status != cat
    ]

    console.print(
        f'Updating Status of Task [[cyan]{id}[/]] "[white]{data[id]["Title"]}[/]"'
    )
    console.print(f"\t[1] {color_dict[possible_status[0]]}")
    console.print(f"\t[2] {color_dict[possible_status[1]]}")
    new_status = IntPrompt.ask(
        prompt="[2/2] New Status of Task?",
        show_choices=False,
        choices=["1", "2"],
    )
    return possible_status[int(new_status) - 1]


def input_confirm_to_overwrite_db() -> bool:
    console.print(":warning:  Existing [orange3]pykanban.json[/] found :warning:")
    return Confirm.ask(
        "Do you want to wipe it clean and start from scratch:question_mark:"
    )
