import configparser
import os
from pathlib import Path

config = configparser.ConfigParser()
config.optionxform = str
CONFIG_PATH = Path.home() / "pykanban.ini"


def create_init_config():
    config["settings.general"] = {"Active_Board": "", "Column_Min_Width": 40}
    config["settings.columns.visible"] = {
        "Ready": True,
        "Doing": True,
        "Done": True,
        "Deleted": False,
        "Archived": False,
    }
    config["kanban_boards"] = {}
    save_config(config)


def save_config(config):
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def read_config():
    config.read(CONFIG_PATH)
    return config


# check if board name exists
def add_new_board_to_config(board_name):
    config = read_config()
    config["kanban_boards"][board_name] = str(Path.cwd())
    save_config(config)


def set_board_to_active(board_name):
    config = read_config()
    config["settings.general"]["Active_Board"] = board_name
    save_config(config)


def check_config_exists() -> bool:
    return os.path.exists(CONFIG_PATH)


def get_active_db_name():
    config = read_config()
    return config["settings.general"]["Active_Board"]


def get_active_db_path():
    config = read_config()
    active_board = get_active_db_name()
    return config["kanban_boards"][active_board]


def get_list_of_current_boards():
    config = read_config()
    return config["kanban_boards"].keys()


def delete_selected_board_from_config(boardname):
    config = read_config()
    config["kanban_boards"].pop(boardname)
    save_config(config)


def delete_current_folder_board_from_config():
    config = read_config()
    curr_path = str(Path.cwd())
    for b_name, b_path in config["kanban_boards"].items():
        if b_path == curr_path:
            config["kanban_boards"].pop(b_name)
    save_config(config)


def check_if_board_name_exists_in_config(boardname):
    config = read_config()
    return boardname in config["kanban_boards"]


if __name__ == "__main__":
    print(check_if_board_name_exists_in_config("Desktop13"))
