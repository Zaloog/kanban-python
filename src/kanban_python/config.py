import configparser
from pathlib import Path

CONFIG_PATH = Path.home() / "pykanban.ini"


class KanbanConfig:
    def __init__(self, path=CONFIG_PATH) -> None:
        self.configpath = path
        self.config = configparser.ConfigParser(default_section=None)
        self.config.optionxform = str
        print("invoke class")
        self.config.read(path)

    def __repr__(self) -> str:
        output = ""
        for sec in self.config:
            if sec:
                output += 15 * "-"
                output += f"Section: {sec}"
                output += 15 * "-" + "\n"
            for key, val in self.config[sec].items():
                output += f"{key}: {val}\n"
        return output

    def save(self):
        with open(self.configpath, "w") as self.configfile:
            self.config.write(self.configfile)

    @property
    def active_board(self) -> str:
        return self.config["settings.general"]["Active_Board"]

    @active_board.setter
    def active_board(self, new_board):
        self.config["settings.general"]["Active_Board"] = new_board
        self.save()

    @property
    def kanban_boards(self) -> list:
        return [board for board in self.config["kanban_boards"]]

    @property
    def active_board_path(self) -> str:
        return self.config["kanban_boards"][self.active_board]

    @property
    def show_footer(self):
        return self.config["settings.general"]["Show_Footer"]

    @property
    def col_min_width(self) -> int:
        return int(self.config["settings.general"]["Column_Min_Width"])

    @property
    def kanban_boards_dict(self) -> dict:
        return self.config["settings.columns.visible"]

    @property
    def vis_cols(self) -> list:
        return [c for c, v in self.kanban_boards_dict.items() if v == "True"]


cfg = KanbanConfig(path=CONFIG_PATH)


def create_init_config():
    config = configparser.ConfigParser(default_section=None)
    config.optionxform = str
    config["settings.general"] = {
        "Active_Board": "",
        "Column_Min_Width": 35,
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
    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)


def add_new_board_to_config(board_name):
    cfg.config["kanban_boards"][board_name] = str(Path.cwd())
    cfg.save()


def set_board_to_active(board_name):
    cfg.config["settings.general"]["Active_Board"] = board_name
    cfg.save()


def get_active_db_name():
    return cfg.active_board


def get_active_db_path():
    return cfg.active_board_path


def delete_selected_board_from_config(boardname):
    cfg.config["kanban_boards"].pop(boardname)
    cfg.save()


def delete_current_folder_board_from_config():
    curr_path = str(Path.cwd())
    for b_name, b_path in cfg.kanban_boards_dict.items():
        if b_path == curr_path:
            cfg.config["kanban_boards"].pop(b_name)
    cfg.save()


def check_if_board_name_exists_in_config(boardname):
    return boardname in cfg.kanban_boards


def check_if_current_active_board_in_board_list():
    return check_if_board_name_exists_in_config(cfg.active_board)


def delete_board_from_config(board_name):
    cfg.config["kanban_boards"].pop(board_name)
    cfg.save()


def check_config_exists() -> bool:
    return Path(Path.home() / CONFIG_PATH).exists()
