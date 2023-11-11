from rich.table import Table


def create_empty_table():
    table = Table(show_header=True, show_footer=True)
    table.add_column("Ready", justify='center', style='green')
    table.add_column("Doing", justify='center', style='green')
    table.add_column("Done", justify='center', style='green')

    return table

def add_tasks_from_db():
    pass

