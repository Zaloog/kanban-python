from json import dump
from pathlib import Path

from rich.console import Console

from .interface import create_empty_table


TASK = {
    'Name':'Test Task',
    'Description':'Non-existent',
    'Date':'Never',
    }

def create_new_db(args:dict)->None:
    name = args.new
    if args.globally:
        name = Path.home()/name

    with open(f'{name}.json', 'w', encoding='utf-8') as f:
        dump(TASK, f, ensure_ascii=False, indent=4)

    # TODO check if db already exists
    print(f'Created new {name}.json file to save tasks')


def check_db_exists(name:str) -> bool:
    pass


def add_tasks_from_db():
    pass


def show():
    table = create_empty_table()
    console = Console()
    console.print(table)
