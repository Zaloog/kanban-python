from rich.prompt import IntPrompt, Prompt  # ,Confirm
from rich.table import Table

from .utils import create_task_strings_for_rows, current_time_to_str


def create_table(data: dict):
    table = Table(show_header=True, show_footer=True)
    table.add_column(
        header="Ready",
        justify="left",
        min_width=50,
    )
    table.add_column(header="Doing", justify="left", min_width=50)
    table.add_column(
        header="Done",
        justify="left",
        min_width=50,
    )

    ready, doing, done = create_task_strings_for_rows(data=data)
    table.add_row(
        ready,
        doing,
        done,
    )

    return table


def input_ask_for_action():
    task = IntPrompt.ask(
        prompt="""
        [yellow]Whats up!?[/], how can I help you being productive today :rocket:?
        [green] [1] Create new Task [/]
        [bold blue] [2] Move Task [/]
        [bold red] [3] Close Kanban Board [/]
        Make your choice""",
        choices=[
            "1",
            "2",
            "3",
        ],
        show_choices=False,
    )
    return task


def input_create_new_task():
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
        "Date": current_time_to_str(),
    }
    return new_task


def input_ask_which_task_to_move():
    pass
