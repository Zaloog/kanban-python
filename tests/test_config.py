import pytest

from kanban_python import config


def test_create_init_config(tmp_path):
    conf_path = tmp_path / "pykanban.ini"
    config.create_init_config(conf_path)
    cfg = config.KanbanConfig(path=conf_path)

    assert ("settings.general" in cfg.config.sections()) is True
    assert ("settings.columns.visible" in cfg.config.sections()) is True
    assert ("kanban_boards" in cfg.config.sections()) is True

    assert cfg.config["settings.columns.visible"]["Ready"] == "True"
    assert cfg.config["settings.columns.visible"]["Doing"] == "True"
    assert cfg.config["settings.columns.visible"]["Done"] == "True"
    assert cfg.config["settings.columns.visible"]["Deleted"] == "False"
    assert cfg.config["settings.columns.visible"]["Archived"] == "False"

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


def test_check_config_exists(tmp_path, test_config):
    assert config.check_config_exists(path=tmp_path / "pykanban.ini") is True


@pytest.mark.parametrize(
    "board, folder, exists",
    [("testboard1", "test1", True), ("testboard2", "test2", False)],
)
def test_check_current_path_exists_for_board(
    tmp_path, test_config, board, folder, exists
):
    cfg = test_config
    board_path = str(tmp_path / "test1" / "pykanban.json")
    cfg.config["kanban_boards"][board] = board_path
    check_path = str(tmp_path / folder / "pykanban.json")
    assert config.check_current_path_exists_for_board(cfg, check_path) == exists
