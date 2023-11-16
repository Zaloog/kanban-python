import configparser
import os
from pathlib import Path

config = configparser.ConfigParser(default_section=None)
config.optionxform = str
CONFIG_PATH = Path.home() / "pykanban.ini"


def create_init_config():
    config["settings.general"] = {
        "Active_Board": "",
        "Column_Min_Width": 40,
        "Show_Footer": "True",
    }
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


def check_if_current_active_board_in_board_list():
    active_board = get_active_db_name()
    return check_if_board_name_exists_in_config(active_board)


def get_list_of_visible_columns():
    config = read_config()
    columns_dict = config["settings.columns.visible"]
    return [col for col, vis in columns_dict.items() if vis == "True"]


def get_dict_of_all_columns():
    config = read_config()
    return config["settings.columns.visible"]


def delete_board_from_config(board_name):
    config = read_config()
    config["kanban_boards"].pop(board_name)
    save_config(config)


if __name__ == "__main__":
    pass
