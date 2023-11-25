import configparser
from pathlib import Path

TASK_FILE = "pykanban.json"
CONFIG_PATH = Path.home() / ".kanban-python"
KANBAN_BOARDS_PATH = CONFIG_PATH / "kanban_boards"
CONFIG_FILE_PATH = CONFIG_PATH / "pykanban.ini"


class KanbanConfig:
    def __init__(self, path=CONFIG_FILE_PATH) -> None:
        self.configpath = path
        self._config = configparser.ConfigParser(default_section=None)
        self._config.optionxform = str
        self._config.read(path)

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
        with open(self.configpath, "w") as configfile:
            self.config.write(configfile)

    @property
    def config(self) -> configparser.ConfigParser:
        return self._config

    @property
    def active_board(self) -> str:
        return self._config["settings.general"]["Active_Board"]

    @active_board.setter
    def active_board(self, new_board):
        self.config["settings.general"]["Active_Board"] = new_board
        self.save()

    @property
    def kanban_boards(self) -> list:
        return [board for board in self.config["kanban_boards"]]

    @property
    def kanban_boards_dict(self) -> dict:
        return self.config["kanban_boards"]

    @kanban_boards_dict.setter
    def kanban_boards_dict(self, board_name: str) -> dict:
        self.config["kanban_boards"][board_name] = get_json_path(board_name)
        self.save()

    @property
    def active_board_path(self) -> str:
        return self.config["kanban_boards"][self.active_board]

    @property
    def show_footer(self):
        return self.config["settings.general"]["Show_Footer"]

    @show_footer.setter
    def show_footer(self, visible):
        self.config["settings.general"]["Show_Footer"] = visible
        self.save()

    @property
    def col_min_width(self) -> int:
        return int(self.config["settings.general"]["Column_Min_Width"])

    @property
    def kanban_columns_dict(self) -> dict:
        return self.config["settings.columns.visible"]

    @kanban_columns_dict.setter
    def kanban_columns_dict(self, updated_dict) -> dict:
        self.config["settings.columns.visible"] = updated_dict
        self.save()

    @property
    def vis_cols(self) -> list:
        return [c for c, v in self.kanban_columns_dict.items() if v == "True"]

    @property
    def done_limit(self) -> int:
        return int(self.config["settings.general"]["Done_Limit"])

    @done_limit.setter
    def done_limit(self, new_limit: int) -> None:
        self.config["settings.general"]["Done_Limit"] = new_limit
        self.save()


cfg = KanbanConfig(path=CONFIG_FILE_PATH)


def create_init_config(path=CONFIG_PATH):
    config = configparser.ConfigParser(default_section=None)
    config.optionxform = str
    config["settings.general"] = {
        "Active_Board": "",
        "Column_Min_Width": 35,
        "Done_Limit": 10,
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

    if not path.exists():
        path.mkdir()
        (path / "kanban_boards").mkdir()

    with open(path / "pykanban.ini", "w") as configfile:
        config.write(configfile)


def delete_current_folder_board_from_config(
    cfg=cfg, curr_path: str = str(Path.cwd())
) -> None:
    for b_name, b_path in cfg.kanban_boards_dict.items():
        if b_path == curr_path:
            cfg.config["kanban_boards"].pop(b_name)
    cfg.save()


def check_if_board_name_exists_in_config(boardname: str, cfg=cfg) -> bool:
    return boardname in cfg.kanban_boards


def check_if_current_active_board_in_board_list(cfg=cfg) -> bool:
    return check_if_board_name_exists_in_config(cfg=cfg, boardname=cfg.active_board)


def delete_board_from_config(board_name, cfg=cfg) -> None:
    cfg.config["kanban_boards"].pop(board_name)
    cfg.save()


def check_config_exists(path=CONFIG_FILE_PATH) -> bool:
    return path.exists()


def get_json_path(boardname: str):
    return str(KANBAN_BOARDS_PATH / boardname / TASK_FILE)
