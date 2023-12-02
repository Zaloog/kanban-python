import pytest

from kanban_python import config


def test_active_board_path(test_config):
    cfg = test_config
    board_name = "Testboard"
    cfg.kanban_boards_dict = board_name
    cfg.active_board = board_name

    expected_path = str(config.KANBAN_BOARDS_PATH / board_name / config.TASK_FILE_NAME)
    assert cfg.active_board_path == expected_path


def test_show_footer_setter(test_config):
    cfg = test_config
    cfg.show_footer = "False"
    assert cfg.show_footer == "False"


def test_col_min_width(test_config):
    cfg = test_config
    assert cfg.col_min_width == 35


def test_kanban_columns_dict_setter(test_config):
    cfg = test_config
    cfg.kanban_columns_dict = {"Archived": True}
    assert cfg.kanban_columns_dict["Archived"] == "True"


def test_vis_cols(test_config):
    cfg = test_config
    assert cfg.vis_cols == ["Ready", "Doing", "Done"]


def test_done_limit_setter(test_config):
    cfg = test_config
    cfg.done_limit = "11"
    assert cfg.done_limit == 11


def test_create_init_config(
    test_config_path, test_config_file_path, test_kanban_board_path
):
    config.create_init_config(test_config_path, test_kanban_board_path)
    cfg = config.KanbanConfig(path=test_config_file_path)

    assert ("settings.general" in cfg.config.sections()) is True
    assert ("settings.scanner" in cfg.config.sections()) is True
    assert ("settings.columns.visible" in cfg.config.sections()) is True
    assert ("kanban_boards" in cfg.config.sections()) is True

    assert cfg.config["settings.columns.visible"]["Ready"] == "True"
    assert cfg.config["settings.columns.visible"]["Doing"] == "True"
    assert cfg.config["settings.columns.visible"]["Done"] == "True"
    assert cfg.config["settings.columns.visible"]["Deleted"] == "False"
    assert cfg.config["settings.columns.visible"]["Archived"] == "False"

    assert cfg.config["settings.scanner"]["Files"] == ".py .md"
    assert cfg.config["settings.scanner"]["Patterns"] == "# TODO,#TODO,# BUG"

    assert cfg.kanban_boards is not True


def test_delete_current_folder_board_from_config(test_config):
    cfg = test_config
    cfg.config["kanban_boards"]["testboard1"] = "path1"
    cfg.config["kanban_boards"]["testboard2"] = "path1"
    cfg.config["kanban_boards"]["testboard3"] = "path3"

    config.delete_current_folder_board_from_config(cfg=cfg, curr_path="path1")

    assert ("path1" in cfg.kanban_boards_dict.values()) is False
    assert ("path3" in cfg.kanban_boards_dict.values()) is True


@pytest.mark.parametrize(
    "board, in_list",
    [("testboard1", True), ("testboard2", False)],
)
def test_check_if_board_name_exists_in_config(test_config, board, in_list):
    cfg = test_config
    cfg.config["kanban_boards"]["testboard1"] = ""

    assert (
        config.check_if_board_name_exists_in_config(
            board,
            cfg=cfg,
        )
        == in_list
    )


@pytest.mark.parametrize(
    "act_board, in_list",
    [("testboard1", True), ("testboard2", False)],
)
def test_check_if_current_active_board_in_board_list(test_config, act_board, in_list):
    cfg = test_config
    cfg.active_board = act_board
    cfg.config["kanban_boards"]["testboard1"] = ""

    assert config.check_if_current_active_board_in_board_list(cfg=cfg) == in_list


@pytest.mark.parametrize(
    "to_delete_board, board_left",
    [("testboard1", "testboard2"), ("testboard2", "testboard1")],
)
def test_delete_board_from_config(test_config, to_delete_board, board_left):
    cfg = test_config
    cfg.config["kanban_boards"]["testboard1"] = ""
    cfg.config["kanban_boards"]["testboard2"] = ""

    config.delete_board_from_config(cfg=cfg, board_name=to_delete_board)

    assert board_left in cfg.kanban_boards


def test_check_config_exists(test_config_file_path, test_config):
    assert config.check_config_exists(path=test_config_file_path) is True


def test_get_json_path():
    board_name = "Testboard"
    result = config.get_json_path(board_name)

    assert result == str(config.KANBAN_BOARDS_PATH / board_name / config.TASK_FILE_NAME)
