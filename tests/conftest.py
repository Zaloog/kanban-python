"""
    Dummy conftest.py for kanban_python.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest


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
