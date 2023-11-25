from datetime import datetime

import pytest

from kanban_python import utils


def test_get_motivational_quote():
    assert utils.get_motivational_quote() in utils.QUOTES


def test_current_time_to_str():
    current_time = datetime.now()
    result = utils.current_time_to_str()
    expected_format = current_time.strftime("%Y-%m-%d %H:%M:%S")

    assert result == expected_format


def test_calculate_time_delta_str(start_time_str, end_time_str):
    delta = utils.calculate_time_delta_str(start_time_str, end_time_str)

    assert delta == 2.50


@pytest.mark.parametrize(
    "num_tasks, expected_result",
    [
        (1, True),
        (0, True),
        (11, False),
    ],
)
def test_check_if_done_col_leq_x(test_config, num_tasks, expected_result):
    cfg = test_config
    test_data = {i: {"Status": "Done"} for i in range(num_tasks)}
    result = utils.check_if_done_col_leq_X(cfg=cfg, data=test_data)

    assert result is expected_result


@pytest.mark.parametrize("first_task_id", [1, 2, 3])
def test_move_first_done_task_to_archive(first_task_id):
    test_data = {i: {"Status": "Done"} for i in range(first_task_id, 15)}
    idx, task = utils.move_first_done_task_to_archive(data=test_data)

    assert first_task_id == idx
    assert task["Status"] == "Archived"


@pytest.mark.parametrize(
    "vis_col, expected_result",
    [
        ("Ready", {"Ready": ["[[cyan]01[/]]([orange3]HI[/]) [white]Welcome Task[/]"]}),
        ("Doing", {"Doing": []}),
        ("Done", {"Done": []}),
    ],
)
def test_create_status_dict_for_rows(test_task, vis_col, expected_result):
    test_db = {"1": test_task}
    result_dict = utils.create_status_dict_for_rows(test_db, [vis_col])
    assert isinstance(result_dict, dict)

    assert result_dict == expected_result


@pytest.mark.parametrize(
    "vis_col, expected_result", [("Ready", True), ("Doing", False), ("Done", False)]
)
def test_check_if_there_are_visible_tasks_in_board(test_task, vis_col, expected_result):
    test_db = {"1": test_task}
    result = utils.check_if_there_are_visible_tasks_in_board(test_db, [vis_col])
    assert result == expected_result


@pytest.mark.parametrize(
    "file_there, output", [(True, "removed"), (False, "File already deleted")]
)
def test_delete_json_file(tmp_path, capsys, file_there, output):
    db_path = tmp_path / "boardname"
    db_file_path = db_path / "pykanban.json"
    if file_there:
        db_path.mkdir()
        db_file_path.touch()

    utils.delete_json_file(db_file_path)

    captured = capsys.readouterr()
    assert output in captured.out


@pytest.mark.parametrize(
    "name, expected_result",
    [("Test_123", True), ("Test123/", False), (".test_", False)],
)
def test_check_board_name_valid(name, expected_result):
    result = utils.check_board_name_valid(name)

    assert result is expected_result


# def test_main(capsys):
# """CLI Tests"""
# # capsys is a pytest fixture that allows asserts against stdout/stderr
# # https://docs.pytest.org/en/stable/capture.html
# main(["7"])
# captured = capsys.readouterr()
# assert "The 7-th Fibonacci number is 13" in captured.out
