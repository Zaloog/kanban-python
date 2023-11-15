import configparser
import os
from pathlib import Path

config = configparser.ConfigParser()
config.optionxform = str
CONFIG_PATH = Path.home() / "pykanban.ini"


def create_init_config():
    config["settings"] = {"Columns": ["Ready", "Doing", "Done"], "Active_Board": ""}
    config["kanban_boards"] = {}
    save_config(config)


def save_config(config):
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def read_config():
    config.read(CONFIG_PATH)
    return config


# check if board name exists
def add_new_board(board_name):
    config = read_config()
    config["kanban_boards"][board_name] = str(Path.cwd())
    save_config(config)


def set_board_to_active(board_name):
    config = read_config()
    config["settings"]["Active_Board"] = board_name
    save_config(config)


def check_config_exists() -> bool:
    return os.path.exists(CONFIG_PATH)


def get_active_db_name():
    config = read_config()
    return config["settings"]["Active_Board"]


def get_active_db_path():
    config = read_config()
    active_board = get_active_db_name()
    return config["kanban_boards"][active_board]


def get_list_of_current_boards():
    config = read_config()
    return config["kanban_boards"].keys()


if __name__ == "__main__":
    if not check_config_exists():
        create_init_config()

    board_name = "lalala"
    print(Path.cwd())
    print(read_config()["settings"]["Columns"])
    print(read_config()["settings"]["Active_Board"])
    add_new_board(board_name=board_name)
    print([i for i in read_config()["kanban_boards"]])
    set_board_to_active(board_name=board_name)
