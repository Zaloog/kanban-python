"""
    Dummy conftest.py for kanban_python.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest

from kanban_python import config


@pytest.fixture
def start_time_str():
    return "2023-11-01 10:00:00"


@pytest.fixture
def end_time_str():
    return "2023-11-01 10:02:30"


@pytest.fixture
def test_task():
    return {
        "Title": "Welcome Task",
        "Description": "Welcome to kanban-python, I hope this helps your productivity",
        "Tag": "HI",
        "Status": "Ready",
        "Begin_Time": "",
        "Complete_Time": "",
        "Duration": "0",
        "Creation_Date": "",
    }


@pytest.fixture
def test_config(tmp_path):
    conf_path = tmp_path / "pykanban.ini"
    config.create_init_config(conf_path)

    cfg = config.KanbanConfig(path=conf_path)
    return cfg
