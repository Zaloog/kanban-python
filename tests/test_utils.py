import datetime

import pytest
from freezegun import freeze_time

from kanban_python import utils


def test_get_motivational_quote():
    assert utils.get_motivational_quote() in utils.QUOTES


def test_current_time_to_str():
    current_time = datetime.datetime.now()
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


def test_scan_files(tmp_path, test_config):
    cfg = test_config

    folderlv1 = tmp_path / "folder1"
    folderlv2 = folderlv1 / ".folder2"

    folderlv1.mkdir()
    folderlv2.mkdir()

    py_filelv0 = tmp_path / "file.py"
    txt_filelv1 = folderlv1 / "file.txt"
    md_filelv1 = folderlv1 / "file.md"
    md_filelv2 = folderlv2 / "file.md"

    py_filelv0.touch()
    txt_filelv1.touch()
    md_filelv1.touch()
    md_filelv2.touch()

    result = utils.scan_files(path=tmp_path, endings=cfg.scanned_files)

    assert sorted(result) == sorted(
        [
            str(tmp_path / "file.py"),
            str(tmp_path / "folder1" / "file.md"),
        ]
    )


def test_scan_todos(test_config, tmp_path):
    cfg = test_config
    file_path = tmp_path / "file.py"
    file_path.touch()
    with open(file_path, "w") as file:
        file.write("# TODO: Pytest is cool")

    list_input = [file_path]

    result = utils.scan_for_todos(
        rel_path=tmp_path, file_paths=list_input, patterns=cfg.scanned_patterns
    )

    assert result == [("# TODO: Pytest is cool", "file.py")]
    pass


@pytest.mark.parametrize(
    "todo, pattern, expected_result",
    [
        ("#TODO Test this", ["#TODO"], ("TODO", "Test this")),
        ("# BUG : Test this", ["# TODO", "# BUG"], ("BUG", "Test this")),
    ],
)
def test_split_todo_in_tag_and_title(todo, pattern, expected_result):
    tag, title = utils.split_todo_in_tag_and_title(todo=todo, patterns=pattern)

    assert tag == expected_result[0]
    assert title == expected_result[1]


@pytest.mark.parametrize(
    "files, expected_result",
    [(".md .py", True), (".py  md", False), (".py .d3", False)],
)
def test_check_scanner_files_valid(files, expected_result):
    result = utils.check_scanner_files_valid(files)

    assert result is expected_result


@pytest.mark.parametrize(
    "patterns, expected_result",
    [("# TODO,#TODO", True), ("TODO,# BUG", False), ("TODO BUG", False)],
)
def test_check_scanner_patterns_valid(patterns, expected_result):
    result = utils.check_scanner_patterns_valid(patterns)

    assert result is expected_result


@pytest.mark.parametrize(
    "vis_cols, expected_result",
    [(["Ready"], ["1", "3", "HI"]), (["Done"], [])],
)
def test_get_tag_id_choices(test_task, vis_cols, expected_result):
    data_dict = {"1": test_task, "3": test_task}

    result = utils.get_tag_id_choices(data_dict=data_dict, vis_cols=vis_cols)
    assert sorted(result) == sorted(expected_result)


def test_get_iso_calender_info():
    date = "2023-12-05 23:41:41"
    year, week, weekday = utils.get_iso_calender_info(date)
    assert year == 2023
    assert week == 49
    assert weekday == 2


def test_create_dict_for_report_view():
    tasks = [
        {"Complete_Time": "2022-12-05 23:41:41"},
        {"Complete_Time": "2023-12-05 23:41:41"},
    ]

    result_max = 1
    result_dict = {2: {49: 1}}

    max_val, report_dict = utils.create_dict_for_report_view(tasks)
    assert result_max == max_val
    assert result_dict == report_dict


def test_create_color_mapping():
    task_amount = [1, 3, 4, 0, 5, 8, 12, 16, 25]
    max_val = 16
    result = utils.create_color_mapping(amount_list=task_amount, max_val=max_val)

    assert result == [1, 1, 1, 0, 2, 2, 3, 4]


@pytest.mark.parametrize(
    "date, expected_result",
    [
        ("2023-12-24", True),
        ("2023-17-3", False),
        ("30.05.2023", False),
        ("30.05.223", False),
    ],
)
def test_check_due_date_format(date, expected_result):
    result = utils.check_due_date_format(date)

    assert result is expected_result


@pytest.mark.parametrize(
    "datetime, expected_result",
    [
        ("2023-12-24 00:00:00", "2023-12-24"),
        ("", ""),
    ],
)
def test_due_date_datetime_to_date(datetime, expected_result):
    result = utils.due_date_datetime_to_date(datetime)

    assert result == expected_result


@pytest.mark.parametrize(
    "datetime, expected_result",
    [
        ("2023-12-24", "2023-12-24 23:59:59"),
        ("", ""),
    ],
)
def test_due_date_date_to_datetime(datetime, expected_result):
    result = utils.due_date_date_to_datetime(datetime)

    assert result == expected_result


def test_calculate_days_left_till_due():
    fake_now = datetime.datetime(2023, 12, 10, 0, 0, 0)
    test_time = "2023-12-24 23:59:59"
    delta_days = 14

    with freeze_time(fake_now):
        result = utils.calculate_days_left_till_due(test_time)

    assert result == delta_days


# def test_main(capsys):
# """CLI Tests"""
# # capsys is a pytest fixture that allows asserts against stdout/stderr
# # https://docs.pytest.org/en/stable/capture.html
# main(["7"])
# captured = capsys.readouterr()
# assert "The 7-th Fibonacci number is 13" in captured.out
